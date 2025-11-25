"""
DLNEP - Student data collection from the Neptun system
This module handles downloading student lists from all courses in the Neptun system.
"""

import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import sys
sys.path.append(str(Path(__file__).parent.parent))

from shared import SeleniumUtils, ExcelHandler, setup_logging


class NeptunStudentDataCollector:
    """Collector for student data from Neptun system"""
    
    def __init__(self, download_folder: Optional[Path] = None):
        """
        Initialize the Neptun student data collector
        
        Args:
            download_folder: Folder to save downloaded files (defaults to data/neptun_downloads)
        """
        self.logger = setup_logging(__name__)
        self.selenium_utils = SeleniumUtils(headless=False)
        
        # Set up download folder
        if download_folder is None:
            self.download_folder = Path(__file__).parent.parent / "data" / "neptun_downloads"
        else:
            self.download_folder = download_folder
        
        self.download_folder.mkdir(parents=True, exist_ok=True)
        
        # Neptun system URLs and selectors
        self.login_url = "https://neptun.bme.hu/oktatoi/login.aspx"
        self.courses_url = "https://neptun.bme.hu/oktatoi/main.aspx?ismenuclick=true&ctrl=1902"
        
        self.collected_data = []
        self.downloaded_files = []
    
    def setup_driver_with_downloads(self):
        """Set up Chrome driver with download preferences for Neptun"""
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium import webdriver
        
        chrome_options = Options()
        if self.selenium_utils.headless:
            chrome_options.add_argument("--headless")
        
        # Configure download behavior
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Set download preferences
        prefs = {
            "download.default_directory": str(self.download_folder.absolute()),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_settings.popups": 0
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        
        # Execute script to hide webdriver detection
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.selenium_utils.driver = driver
        return driver
    
    def login_to_neptun(self) -> bool:
        """
        Navigate to Neptun login page and wait for user to complete login
        
        Returns:
            True if login successful, False otherwise
        """
        try:
            driver = self.setup_driver_with_downloads()
            
            self.logger.info(f"Navigating to Neptun login page: {self.login_url}")
            driver.get(self.login_url)
            
            # Wait for page to load
            time.sleep(2)
            
            self.logger.info("Please complete the login process in the Neptun system...")
            if not self.selenium_utils.wait_for_user_login():
                return False
            
            # Verify login by checking if we can navigate to courses page
            self.logger.info(f"Navigating to courses page: {self.courses_url}")
            driver.get(self.courses_url)
            
            # Wait for courses page to load
            time.sleep(2)
            
            # Check if we're on the right page by looking for course table
            try:
                # Look for elements that would indicate we're on the courses page
                WebDriverWait(driver, 10).until(
                    lambda d: "Tárgykód" in driver.page_source or "course" in driver.current_url.lower()
                )
                self.logger.info("Successfully logged in and navigated to courses page")
                return True
            except TimeoutException:
                self.logger.error("Failed to navigate to courses page - login may have failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Error during Neptun login process: {e}")
            return False
    
    def get_course_list(self) -> List[Dict[str, Any]]:
        """
        Extract the list of courses from the courses page
        
        Returns:
            List of course dictionaries with course code, name, and row element
        """
        try:
            driver = self.selenium_utils.driver
            if not driver:
                self.logger.error("No driver available")
                return []
            
            self.logger.info("Extracting course list from Neptun...")
            
            # Wait for the page to fully load
            time.sleep(2)
            
            courses = []
            
            # Try to find the courses table
            # Look for table with specific headings and structure
            try:
                # First, try to find a table with course data
                tables = driver.find_elements(By.TAG_NAME, "table")
                self.logger.info(f"Found {len(tables)} tables on the page")
                
                # Find the correct course table by looking for specific headings
                course_table = None
                self.logger.info("Looking for course table with required headings...")
                
                required_headings = ["Tárgykód", "Tárgy név", "Követelmény", "Oktatók", "Kijelölés"]
                
                for table_idx, table in enumerate(tables):
                    try:
                        # Check if table has the required headings
                        table_text = table.text
                        headings_found = sum(1 for heading in required_headings if heading in table_text)
                        
                        if headings_found >= 4:  # Must have at least 4 of the 5 required headings
                            # Also check if it contains "Dr. Csorba Kristóf" and "BMEVI"
                            if "Dr. Csorba Kristóf" in table_text and "BMEVI" in table_text:
                                course_table = table
                                self.logger.info(f"Found course table at index {table_idx} with {headings_found}/5 required headings")
                                break
                        
                    except Exception as e:
                        self.logger.warning(f"Error checking table {table_idx}: {str(e)}")
                        continue
                
                if not course_table:
                    self.logger.error("Could not find course table with required headings and content")
                    return []
                
                # Find the header row to identify column positions
                header_row = None
                header_indices = {}
                
                rows = course_table.find_elements(By.TAG_NAME, "tr")
                self.logger.info(f"Found {len(rows)} rows in course table")
                
                for row_idx, row in enumerate(rows[:5]):  # Check first 5 rows for headers
                    try:
                        cells = row.find_elements(By.TAG_NAME, "th")
                        if not cells:  # If no th elements, try td elements
                            cells = row.find_elements(By.TAG_NAME, "td")
                        
                        if len(cells) >= 5:  # Should have multiple columns
                            cell_texts = [cell.text.strip() for cell in cells]
                            
                            # Check if this looks like a header row
                            if "Tárgykód" in cell_texts and "Oktatók" in cell_texts:
                                header_row = row
                                # Map column names to indices
                                for i, text in enumerate(cell_texts):
                                    if "Tárgykód" in text:
                                        header_indices['course_code'] = i
                                    elif "Tárgy név" in text:
                                        header_indices['course_name'] = i
                                    elif "Követelmény" in text:
                                        header_indices['requirement'] = i
                                    elif "Oktatók" in text:
                                        header_indices['instructors'] = i
                                    elif "Kijelölés" in text:
                                        header_indices['selection'] = i
                                
                                self.logger.info(f"Found header row at index {row_idx}, column mapping: {header_indices}")
                                break
                                
                    except Exception as e:
                        self.logger.warning(f"Error checking potential header row {row_idx}: {str(e)}")
                        continue
                
                if not header_row or not header_indices:
                    self.logger.error("Could not identify column structure in course table")
                    return []
                
                # Now extract valid course rows
                course_rows = []
                for row_idx, row in enumerate(rows):
                    try:
                        if row == header_row:  # Skip header row
                            self.logger.debug(f"Row {row_idx}: Skipped (header row)")
                            continue
                            
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if len(cells) < max(header_indices.values()) + 1:  # Not enough columns
                            self.logger.debug(f"Row {row_idx}: Skipped (not enough columns: {len(cells)} < {max(header_indices.values()) + 1})")
                            continue
                        
                        # Check course code (must start with "BMEVI")
                        course_code_idx = header_indices.get('course_code', 0)
                        course_code = cells[course_code_idx].text.strip()
                        if not course_code.startswith("BMEVI"):
                            self.logger.debug(f"Row {row_idx}: Skipped (course code '{course_code}' does not start with 'BMEVI')")
                            continue
                        
                        # Check requirement (must contain "Évközi jegy")
                        requirement_idx = header_indices.get('requirement', 2)
                        if requirement_idx < len(cells):
                            requirement = cells[requirement_idx].text.strip()
                            if "Évközi jegy" not in requirement:
                                self.logger.debug(f"Row {row_idx}: Skipped (course {course_code} - requirement '{requirement}' does not contain 'Évközi jegy')")
                                continue
                        
                        # Check instructors (must contain "Dr. Csorba Kristóf")
                        instructors_idx = header_indices.get('instructors', 4)
                        if instructors_idx < len(cells):
                            instructors = cells[instructors_idx].text.strip()
                            if "Dr. Csorba Kristóf" not in instructors:
                                self.logger.debug(f"Row {row_idx}: Skipped (course {course_code} - instructor '{instructors}' is not 'Dr. Csorba Kristóf')")
                                continue
                        
                        course_rows.append(row)
                        self.logger.info(f"Row {row_idx}: Valid course found - {course_code}")
                        
                    except Exception as e:
                        self.logger.warning(f"Row {row_idx}: Error checking row - {str(e)}")
                        continue
                
                self.logger.info(f"Found {len(course_rows)} valid course rows")
                
                courses = []
                
                # Process courses one by one to avoid stale element references
                for i in range(len(course_rows)):
                    try:
                        # Re-find the course table and rows each time to avoid stale elements
                        tables = driver.find_elements(By.TAG_NAME, "table")
                        current_course_table = None
                        
                        # Find the correct course table again
                        for table in tables:
                            try:
                                table_text = table.text
                                if "Dr. Csorba Kristóf" in table_text and "BMEVI" in table_text:
                                    required_headings = ["Tárgykód", "Tárgy név", "Követelmény", "Oktatók", "Kijelölés"]
                                    headings_found = sum(1 for heading in required_headings if heading in table_text)
                                    if headings_found >= 4:
                                        current_course_table = table
                                        break
                            except:
                                continue
                        
                        if not current_course_table:
                            self.logger.warning(f"Could not re-find course table for course {i}")
                            continue
                        
                        # Get current course rows
                        current_rows = current_course_table.find_elements(By.TAG_NAME, "tr")
                        current_course_rows = []
                        
                        for row in current_rows:
                            try:
                                cells = row.find_elements(By.TAG_NAME, "td")
                                if len(cells) < 3:
                                    self.logger.debug(f"Re-scan: Skipped row (not enough columns: {len(cells)} < 3)")
                                    continue
                                
                                # Apply the same filtering criteria
                                course_code_idx = header_indices.get('course_code', 1)
                                if course_code_idx >= len(cells):
                                    self.logger.debug(f"Re-scan: Skipped row (course_code index {course_code_idx} >= {len(cells)} cells)")
                                    continue
                                    
                                course_code = cells[course_code_idx].text.strip()
                                if not course_code.startswith("BMEVI"):
                                    self.logger.debug(f"Re-scan: Skipped row (course '{course_code}' does not start with 'BMEVI')")
                                    continue
                                
                                requirement_idx = header_indices.get('requirement', 3)
                                if requirement_idx < len(cells):
                                    requirement = cells[requirement_idx].text.strip()
                                    if "Évközi jegy" not in requirement:
                                        self.logger.debug(f"Re-scan: Skipped row (course {course_code} - requirement '{requirement}' does not contain 'Évközi jegy')")
                                        continue
                                
                                instructors_idx = header_indices.get('instructors', 15)
                                if instructors_idx < len(cells):
                                    instructors = cells[instructors_idx].text.strip()
                                    if "Dr. Csorba Kristóf" not in instructors:
                                        self.logger.debug(f"Re-scan: Skipped row (course {course_code} - instructor '{instructors}' is not 'Dr. Csorba Kristóf')")
                                        continue
                                
                                current_course_rows.append(row)
                                self.logger.debug(f"Re-scan: Valid course found - {course_code}")
                            except Exception as e:
                                self.logger.debug(f"Re-scan: Error checking row - {str(e)}")
                                continue
                        
                        # Get the course at index i
                        if i >= len(current_course_rows):
                            self.logger.warning(f"Course index {i} out of range, only {len(current_course_rows)} courses found")
                            continue
                        
                        row = current_course_rows[i]
                        cells = row.find_elements(By.TAG_NAME, "td")
                        
                        # Extract course information using header indices
                        course_code_idx = header_indices.get('course_code', 1)
                        course_name_idx = header_indices.get('course_name', 2)
                        
                        course_code = cells[course_code_idx].text.strip()
                        course_name = cells[course_name_idx].text.strip() if course_name_idx < len(cells) else "Unknown"
                        
                        # Look for the dropdown menu with specific attributes
                        dropdown_element = None
                        
                        # Look for dropdown element with the specific attributes from specification
                        try:
                            # Try multiple selectors based on the specification attributes
                            selectors = [
                                "*[class='contextcell'][role='menu'][title='Lehetőségek']",
                                "*[class='contextcell'][alt='Lehetőségek']",
                                "*[role='menu'][title='Lehetőségek']",
                                "*[aria-describedby='contextmenu_help'][title='Lehetőségek']",
                                "img[alt='Lehetőségek']",
                                "*[title='Lehetőségek']"
                            ]
                            
                            for selector in selectors:
                                try:
                                    dropdown_element = row.find_element(By.CSS_SELECTOR, selector)
                                    if dropdown_element:
                                        self.logger.info(f"Found dropdown using selector: {selector}")
                                        break
                                except:
                                    continue
                            
                            # If still not found, try XPath approaches
                            if not dropdown_element:
                                xpath_selectors = [
                                    ".//*[@class='contextcell' and @role='menu' and @title='Lehetőségek']",
                                    ".//*[@class='contextcell' and @alt='Lehetőségek']",
                                    ".//*[@role='menu' and @title='Lehetőségek']",
                                    ".//*[@title='Lehetőségek']",
                                    ".//*[contains(@onfocus, 'A2.HandleClick')]"
                                ]
                                
                                for xpath in xpath_selectors:
                                    try:
                                        dropdown_element = row.find_element(By.XPATH, xpath)
                                        if dropdown_element:
                                            self.logger.info(f"Found dropdown using XPath: {xpath}")
                                            break
                                    except:
                                        continue
                                        
                        except Exception as e:
                            self.logger.warning(f"Error searching for dropdown element: {str(e)}")
                        
                        if not dropdown_element:
                            self.logger.warning(f"Could not find dropdown element for course {course_code}")
                            continue
                        
                        if course_code and len(course_code) > 2:  # Basic validation
                            course_info = {
                                'course_code': course_code,
                                'course_name': course_name,
                                'row_element': row,
                                'dropdown_element': dropdown_element,
                                'index': i
                            }
                            courses.append(course_info)
                            self.logger.info(f"Found course: {course_code} - {course_name}")
                            
                            # Process this course immediately to avoid stale elements
                            downloaded_file = self.download_course_student_list(course_info)
                            if downloaded_file:
                                self.downloaded_files.append(downloaded_file)
                            
                            # Navigate back to course list
                            self.logger.info("Navigating back to courses page...")
                            driver.get(self.courses_url)
                            time.sleep(2)  # Wait for page to load completely
                    
                    except Exception as e:
                        self.logger.warning(f"Error processing course {i}: {e}")
                        continue
                
            except Exception as e:
                self.logger.error(f"Error finding course table: {e}")
                
                # Fallback: look for any elements that might contain course information
                self.logger.info("Trying fallback method to find courses...")
                page_text = driver.page_source
                if "Tárgykód" in page_text:
                    self.logger.info("Found 'Tárgykód' in page, but couldn't parse table structure")
                else:
                    self.logger.warning("'Tárgykód' not found in page source")
            
            self.logger.info(f"Total courses found: {len(courses)}")
            return courses
            
        except Exception as e:
            self.logger.error(f"Error getting course list: {e}")
            return []
    
    def download_course_student_list(self, course_info: Dict[str, Any]) -> Optional[Path]:
        """
        Download student list for a specific course
        
        Args:
            course_info: Dictionary containing course information and elements
            
        Returns:
            Path to downloaded file or None if failed
        """
        try:
            driver = self.selenium_utils.driver
            if not driver:
                return None
            
            course_code = course_info['course_code']
            self.logger.info(f"Downloading student list for course: {course_code}")
            
            # Step 1: Click on the dropdown menu ("Lehetőségek") to open floating menu
            dropdown_element = course_info.get('dropdown_element')
            if not dropdown_element:
                self.logger.warning(f"No dropdown element found for course {course_code}")
                return None
            
            # Try to trigger the dropdown menu using focus event (as per specification)
            try:
                # First try to focus on the element to trigger the onfocus event
                ActionChains(driver).move_to_element(dropdown_element).perform()
                time.sleep(1)
                
                # Try to click or focus to trigger A2.HandleClick event
                try:
                    dropdown_element.click()
                    # self.logger.info(f"Clicked dropdown for course {course_code}")
                except:
                    # If click doesn't work, try focus
                    try:
                        driver.execute_script("arguments[0].focus();", dropdown_element)
                        # self.logger.info(f"Focused dropdown for course {course_code}")
                    except Exception as e:
                        self.logger.warning(f"Could not focus dropdown: {e}")
                
                time.sleep(2)  # Wait for floating menu to appear
                
            except Exception as e:
                self.logger.warning(f"Failed to interact with dropdown for course {course_code}: {e}")
                return None
            
            # Step 2: Look for and click "Jegybeírás" option in the floating menu
            try:
                # Wait longer for the floating menu to appear
                time.sleep(2)
                
                # Look for "Jegybeírás" in various ways
                jegybeiras_element = None
                
                # Try different selectors for the menu item
                selectors = [
                    "//*[contains(text(), 'Jegybeírás')]",
                    "//a[contains(text(), 'Jegybeírás')]",
                    "//span[contains(text(), 'Jegybeírás')]",
                    "//div[contains(text(), 'Jegybeírás')]",
                    "//*[@title='Jegybeírás']"
                ]
                
                for selector in selectors:
                    try:
                        jegybeiras_element = WebDriverWait(driver, 8).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        if jegybeiras_element:
                            self.logger.info(f"Found 'Jegybeírás' element using: {selector}")
                            break
                    except:
                        continue
                
                if not jegybeiras_element:
                    self.logger.error(f"Could not find 'Jegybeírás' option for course {course_code}")
                    return None
                
                # Click on "Jegybeírás"
                jegybeiras_element.click()
                # self.logger.info(f"Clicked 'Jegybeírás' for course {course_code}")
                time.sleep(2)  # Wait 2 seconds for course details to load
                
            except TimeoutException:
                self.logger.warning(f"Could not find 'Jegybeírás' option for course {course_code}")
                return None
            
            # Step 3: First change page size selector to maximum (500), then click export button
            try:
                # Step 3a: Find and change the page size dropdown to maximum value
                try:
                    page_size_dropdown = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "o_course_mark_gridStudents_ddlPageSize"))
                    )
                    
                    # Create Select object and choose the maximum value (500)
                    from selenium.webdriver.support.ui import Select
                    select = Select(page_size_dropdown)
                    
                    # Try to select 500, or the highest available option
                    try:
                        select.select_by_value("500")
                        # self.logger.info(f"Selected page size 500 for course {course_code}")
                    except:
                        # If 500 is not available, select the last (highest) option
                        options = select.options
                        if options:
                            last_option = options[-1]
                            option_value = last_option.get_attribute("value")
                            if option_value:
                                select.select_by_value(option_value)
                                # self.logger.info(f"Selected page size {last_option.text} for course {course_code}")
                            else:
                                self.logger.warning(f"Could not get value for last option in course {course_code}")
                    
                    # Wait a moment for the page to update after changing page size
                    time.sleep(2)
                    
                except TimeoutException:
                    self.logger.warning(f"Could not find page size dropdown for course {course_code}, continuing anyway")
                except Exception as e:
                    self.logger.warning(f"Error changing page size for course {course_code}: {e}")
                
                # Step 3b: Look for and click "Exportálás Excel-fájlba" button
                export_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@alt='Exportálás Excel-fájlba' or contains(text(), 'Exportálás Excel-fájlba') or contains(@title, 'Exportálás Excel-fájlba')]"))
                )
                export_button.click()
                # self.logger.info(f"Clicked export button for course {course_code}")
                
                # Wait for download to complete
                downloaded_file = self._wait_for_download(course_code)
                if downloaded_file:
                    self.logger.info(f"Successfully downloaded student list for {course_code}: {downloaded_file.name}")
                    return downloaded_file
                else:
                    self.logger.warning(f"Download timeout for course {course_code}")
                    return None
                
            except TimeoutException:
                self.logger.warning(f"Could not find export button for course {course_code}")
                return None
            
        except Exception as e:
            self.logger.error(f"Error downloading student list for course {course_info.get('course_code', 'unknown')}: {e}")
            return None
        
        finally:
            # Navigate back to courses list for next course
            try:
                if driver:
                    driver.get(self.courses_url)
                    time.sleep(2)
            except Exception as e:
                self.logger.warning(f"Could not navigate back to courses list: {e}")
    
    def _wait_for_download(self, course_code: str, max_wait_time: int = 30) -> Optional[Path]:
        """
        Wait for download to complete for a specific course
        
        Args:
            course_code: Course code to identify the download
            max_wait_time: Maximum time to wait in seconds
            
        Returns:
            Path to downloaded file or None if timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            # Look for Excel files containing the course code
            excel_files = list(self.download_folder.glob(f"*{course_code}*.xls*"))
            
            for file in excel_files:
                # Check if file is complete (not being downloaded)
                if not file.name.endswith('.crdownload') and file.stat().st_size > 0:
                    # Check if file was created recently (within last minute)
                    file_age = time.time() - file.stat().st_mtime
                    if file_age < 60:  # File created within last minute
                        self.logger.debug(f"Found downloaded file for {course_code}: {file.name} (age: {file_age:.1f}s)")
                        return file
            
            time.sleep(1)
        
        self.logger.warning(f"Download timeout for {course_code} after {max_wait_time}s")
        return None
    
    def collect_all_course_data(self) -> List[Dict[str, Any]]:
        """
        Main method to collect student data from all courses in Neptun
        
        Returns:
            List of course information with download status
        """
        try:
            # Step 0: Clean up old downloads
            self.logger.info("Cleaning up old Excel files from download folder...")
            old_files = list(self.download_folder.glob("*.xls*"))
            for file in old_files:
                try:
                    if not file.name.endswith('.crdownload'):
                        file.unlink()
                        self.logger.debug(f"Removed old file: {file.name}")
                except Exception as e:
                    self.logger.warning(f"Could not remove old file {file.name}: {e}")
            
            if old_files:
                self.logger.info(f"Removed {len([f for f in old_files if not f.name.endswith('.crdownload')])} old Excel files")
            
            # Step 1: Login to Neptun
            if not self.login_to_neptun():
                self.logger.error("Failed to login to Neptun system")
                return []
            
            # Step 2: Get list of courses and process them immediately
            courses = self.get_course_list()
            if not courses:
                self.logger.error("No courses found in Neptun system")
                return []
            
            self.logger.info(f"Completed processing {len(courses)} courses")            # The courses have already been processed in get_course_list()
            # Return summary of results
            download_results = []
            for i, course_info in enumerate(courses):
                result = {
                    'course_code': course_info['course_code'],
                    'course_name': course_info['course_name'],
                    'download_successful': True,  # If it's in the list, it was processed
                    'downloaded_file': None  # Files are tracked in self.downloaded_files
                }
                download_results.append(result)
            
            self.logger.info(f"Download process completed. Successfully downloaded {len(self.downloaded_files)} course files.")
            return download_results
            
        except Exception as e:
            self.logger.error(f"Error in collect_all_course_data: {e}")
            return []
        
        finally:
            # Clean up
            if self.selenium_utils.driver:
                self.selenium_utils.close_driver()
    
    def process_downloaded_files(self) -> List[Dict[str, Any]]:
        """
        Process all downloaded Excel files and extract student data
        
        Returns:
            List of student records from all courses
        """
        all_students = []
        
        for file_path in self.downloaded_files:
            try:
                self.logger.info(f"Processing downloaded file: {file_path.name}")
                
                # Read Excel file
                df = pd.read_excel(file_path)
                
                # Convert to dict records
                students = df.to_dict('records')
                
                # Add course information to each student record
                course_code = self._extract_course_code_from_filename(file_path.name)
                for student in students:
                    student['source_course'] = course_code
                    student['source_file'] = file_path.name
                
                all_students.extend(students)
                self.logger.info(f"Extracted {len(students)} students from {file_path.name}")
                
            except Exception as e:
                self.logger.error(f"Error processing file {file_path}: {e}")
                continue
        
        self.logger.info(f"Total students processed: {len(all_students)}")
        self.collected_data = all_students
        return all_students
    
    def _extract_course_code_from_filename(self, filename: str) -> str:
        """Extract course code from downloaded filename"""
        # Simple heuristic to extract course code
        # This might need adjustment based on actual filename patterns
        import re
        match = re.search(r'([A-Z]+\d+)', filename.upper())
        return match.group(1) if match else "UNKNOWN"
    
    def save_processed_data(self, output_file: Optional[Path] = None) -> bool:
        """
        Save the collected student data to an Excel file
        
        Args:
            output_file: Path for output file (defaults to data/neptun_student_data.xlsx)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.collected_data:
            self.logger.warning("No student data to save")
            return False
        
        if output_file is None:
            output_file = Path(__file__).parent.parent / "data" / "neptun_student_data.xlsx"
        
        try:
            excel_handler = ExcelHandler(output_file)
            success = excel_handler.create_excel_file(self.collected_data, "NeptunStudents")
            
            if success:
                self.logger.info(f"Saved Neptun student data to: {output_file}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error saving Neptun student data: {e}")
            return False


def main():
    """Main function for testing the DLNEP feature"""
    collector = NeptunStudentDataCollector()
    
    # Collect data from Neptun system
    results = collector.collect_all_course_data()
    
    if results:
        # Process downloaded files
        student_data = collector.process_downloaded_files()
        
        if student_data:
            # Save processed data
            collector.save_processed_data()
            print(f"Successfully collected and saved data for {len(student_data)} students from {len(results)} courses")
        else:
            print("No student data was extracted from downloaded files")
    else:
        print("Failed to collect course data from Neptun system")


if __name__ == "__main__":
    main()
