"""
Course download handling for Neptun system
Separated to follow Single Responsibility Principle
"""

import time
from pathlib import Path
from typing import Dict, Any, Optional
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class CoursePageNavigator:
    """Responsible for navigating to course detail pages"""
    
    def __init__(self, driver: WebDriver, logger: logging.Logger):
        self.driver = driver
        self.logger = logger
    
    def navigate_to_course_detail(self, course_info: Dict[str, Any]) -> bool:
        """
        Navigate to the course detail page by clicking the dropdown menu
        
        Args:
            course_info: Dictionary containing course information and elements
            
        Returns:
            True if navigation successful, False otherwise
        """
        try:
            course_code = course_info.get('course_code', 'UNKNOWN')
            self.logger.info(f"Navigating to course detail page for {course_code}")
            
            # Click on the dropdown menu to open the context menu
            dropdown_element = course_info['dropdown_element']
            
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_element)
            time.sleep(1)
            
            # Click to open the context menu
            actions = ActionChains(self.driver)
            actions.click(dropdown_element).perform()
            
            # Wait for the context menu to appear
            time.sleep(2)
            
            # Look for "Jegybeírás" menu item and click it
            menu_item = self._find_jegyberias_menu_item()
            if not menu_item:
                self.logger.error(f"Could not find 'Jegybeírás' menu item for course {course_code}")
                return False
            
            # Click on "Jegybeírás"
            actions.click(menu_item).perform()
            self.logger.info(f"Clicked 'Jegybeírás' for course {course_code}")
            
            # Wait for the course details page to load (as per spec: 2 seconds)
            time.sleep(2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error navigating to course detail: {e}")
            return False
    
    def _find_jegyberias_menu_item(self):
        """
        Find the 'Jegybeírás' menu item in the context menu
        
        Returns:
            WebElement of the menu item or None if not found
        """
        try:
            # Try different strategies to find the menu item
            strategies = [
                (By.XPATH, "//a[contains(text(), 'Jegybeírás')]"),
                (By.XPATH, "//*[contains(text(), 'Jegybeírás')]"),
                (By.PARTIAL_LINK_TEXT, "Jegybeírás"),
                (By.XPATH, "//td[contains(text(), 'Jegybeírás')]")
            ]
            
            for by, value in strategies:
                try:
                    elements = self.driver.find_elements(by, value)
                    if elements:
                        self.logger.debug(f"Found 'Jegybeírás' menu item using strategy: {by}")
                        return elements[0]
                except:
                    continue
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error finding 'Jegybeírás' menu item: {e}")
            return None


class StudentListDownloader:
    """Responsible for downloading student lists from course detail pages"""
    
    def __init__(self, driver: WebDriver, logger: logging.Logger, download_folder: Path):
        self.driver = driver
        self.logger = logger
        self.download_folder = download_folder
    
    def download_student_list(self, course_info: Dict[str, Any]) -> Optional[Path]:
        """
        Download the student list for a course
        
        Args:
            course_info: Dictionary containing course information
            
        Returns:
            Path to downloaded file or None if failed
        """
        try:
            course_code = course_info.get('course_code', 'UNKNOWN')
            self.logger.info(f"Starting download for course {course_code}")
            
            # Step 1: Set page size to maximum (500)
            if not self._set_page_size_to_maximum():
                self.logger.error(f"Failed to set page size for course {course_code}")
                return None
            
            # Step 2: Find and click the Excel export button
            download_path = self._click_excel_export_button(course_code)
            if not download_path:
                self.logger.error(f"Failed to download Excel file for course {course_code}")
                return None
            
            return download_path
            
        except Exception as e:
            self.logger.error(f"Error downloading student list: {e}")
            return None
    
    def _set_page_size_to_maximum(self) -> bool:
        """
        Set the page size selector to maximum value (500)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Look for the page size selector with specific ID
            page_size_selector = self.driver.find_element(By.ID, "o_course_mark_gridStudents_ddlPageSize")
            
            # Create Select object and choose the maximum value
            select = Select(page_size_selector)
            
            # Get all options and select the one with highest value
            options = select.options
            max_value = 0
            max_option = None
            
            for option in options:
                try:
                    value = int(option.get_attribute("value"))
                    if value > max_value:
                        max_value = value
                        max_option = option
                except ValueError:
                    continue
            
            if max_option:
                select.select_by_value(str(max_value))
                self.logger.info(f"Set page size to maximum value: {max_value}")
                time.sleep(2)  # Wait for page to update
                return True
            else:
                self.logger.error("Could not find maximum page size option")
                return False
                
        except NoSuchElementException:
            self.logger.error("Page size selector not found")
            return False
        except Exception as e:
            self.logger.error(f"Error setting page size: {e}")
            return False
    
    def _click_excel_export_button(self, course_code: str) -> Optional[Path]:
        """
        Find and click the Excel export button
        
        Args:
            course_code: Course code for logging purposes
            
        Returns:
            Path to downloaded file or None if failed
        """
        try:
            # Count files before download
            files_before = self._count_download_files()
            
            # Look for Excel export button by alt text
            export_button = self.driver.find_element(By.XPATH, "//input[@alt='Exportálás Excel-fájlba']")
            
            # Click the export button
            export_button.click()
            self.logger.info(f"Clicked Excel export button for course {course_code}")
            
            # Wait for download to complete
            downloaded_file = self._wait_for_download(files_before, course_code)
            return downloaded_file
            
        except NoSuchElementException:
            self.logger.error(f"Excel export button not found for course {course_code}")
            return None
        except Exception as e:
            self.logger.error(f"Error clicking Excel export button: {e}")
            return None
    
    def _count_download_files(self) -> int:
        """
        Count the number of files in the download folder
        
        Returns:
            Number of files in download folder
        """
        try:
            return len(list(self.download_folder.glob("*.xlsx")))
        except:
            return 0
    
    def _wait_for_download(self, files_before: int, course_code: str, timeout: int = 30) -> Optional[Path]:
        """
        Wait for a new file to appear in the download folder
        
        Args:
            files_before: Number of files before download started
            course_code: Course code for logging
            timeout: Maximum time to wait in seconds
            
        Returns:
            Path to the new downloaded file or None if timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            current_files = list(self.download_folder.glob("*.xlsx"))
            
            if len(current_files) > files_before:
                # Find the newest file
                newest_file = max(current_files, key=lambda f: f.stat().st_mtime)
                self.logger.info(f"Download completed for course {course_code}: {newest_file.name}")
                return newest_file
            
            time.sleep(1)
        
        self.logger.error(f"Download timeout for course {course_code}")
        return None


class DownloadSession:
    """Manages a complete download session for all courses"""
    
    def __init__(self, driver: WebDriver, logger: logging.Logger, download_folder: Path):
        self.driver = driver
        self.logger = logger
        self.navigator = CoursePageNavigator(driver, logger)
        self.downloader = StudentListDownloader(driver, logger, download_folder)
        self.downloaded_files = []
    
    def download_all_courses(self, courses: list) -> list:
        """
        Download student lists for all courses
        
        Args:
            courses: List of course dictionaries
            
        Returns:
            List of paths to downloaded files
        """
        self.logger.info(f"Starting download session for {len(courses)} courses")
        
        for idx, course_info in enumerate(courses, 1):
            course_code = course_info.get('course_code', 'UNKNOWN')
            self.logger.info(f"Processing course {idx}/{len(courses)}: {course_code}")
            
            try:
                # Navigate to course detail page
                if not self.navigator.navigate_to_course_detail(course_info):
                    self.logger.error(f"Failed to navigate to course {course_code}")
                    continue
                
                # Download student list
                downloaded_file = self.downloader.download_student_list(course_info)
                if downloaded_file:
                    self.downloaded_files.append(downloaded_file)
                    self.logger.info(f"Successfully downloaded: {downloaded_file.name}")
                else:
                    self.logger.error(f"Failed to download student list for course {course_code}")
                
                # Navigate back to course list for next iteration
                if idx < len(courses):  # Don't navigate back after last course
                    self._navigate_back_to_course_list()
                
            except Exception as e:
                self.logger.error(f"Error processing course {course_code}: {e}")
                continue
        
        self.logger.info(f"Download session completed. Downloaded {len(self.downloaded_files)} files")
        return self.downloaded_files
    
    def _navigate_back_to_course_list(self):
        """Navigate back to the course list page"""
        try:
            # Go back to the course list page
            self.driver.get("https://neptun.bme.hu/oktatoi/main.aspx?ismenuclick=true&ctrl=1902")
            time.sleep(3)  # Wait for page to load
        except Exception as e:
            self.logger.error(f"Error navigating back to course list: {e}")
