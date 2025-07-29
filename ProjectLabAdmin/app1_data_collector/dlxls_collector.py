"""
DLXLS - Project topic data collection from BME portal
This module handles downloading and processing student topic data from the BME portal.
"""

import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

import sys
sys.path.append(str(Path(__file__).parent.parent))

from shared import SeleniumUtils, ExcelHandler, setup_logging


class BMETopicDataCollector:
    """Collector for student topic data from BME portal"""
    
    def __init__(self, download_folder: Optional[Path] = None):
        """
        Initialize the BME topic data collector
        
        Args:
            download_folder: Folder to save downloaded files (defaults to data folder)
        """
        self.logger = setup_logging(__name__)
        self.selenium_utils = SeleniumUtils(headless=False)
        
        # Set up download folder
        if download_folder is None:
            self.download_folder = Path(__file__).parent.parent / "data" / "downloads"
        else:
            self.download_folder = download_folder
        
        self.download_folder.mkdir(parents=True, exist_ok=True)
        
        # BME portal URLs and selectors
        self.login_url = "https://www.aut.bme.hu"
        self.workload_url = "https://www.aut.bme.hu/StaffMembers/MyWorkload.aspx"
        self.export_link_text = "Terhelés exportálása"
        
        self.collected_data = []
    
    def setup_driver_with_downloads(self):
        """Set up Chrome driver with download preferences"""
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
        
        # Set download preferences
        prefs = {
            "download.default_directory": str(self.download_folder.absolute()),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        
        self.selenium_utils.driver = driver
        return driver
    
    def login_to_portal(self) -> bool:
        """
        Navigate to BME portal and wait for user to complete login
        
        Returns:
            True if login successful, False otherwise
        """
        try:
            driver = self.setup_driver_with_downloads()
            
            self.logger.info(f"Navigating to BME portal: {self.login_url}")
            driver.get(self.login_url)
            
            self.logger.info("Please complete the login process in the browser...")
            if not self.selenium_utils.wait_for_user_login():
                return False
            
            # Verify we're logged in by checking if we can navigate to workload page
            self.logger.info(f"Navigating to workload page: {self.workload_url}")
            driver.get(self.workload_url)
            
            # Wait a moment for page to load
            time.sleep(3)
            
            # Check if we're on the right page
            if "MyWorkload" in driver.current_url or "workload" in driver.title.lower():
                self.logger.info("Successfully logged in and navigated to workload page")
                return True
            else:
                self.logger.error("Failed to navigate to workload page - login may have failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Error during login process: {e}")
            return False
    
    def download_excel_file(self) -> Optional[Path]:
        """
        Download the Excel file from the workload page
        
        Returns:
            Path to downloaded file or None if failed
        """
        try:
            driver = self.selenium_utils.driver
            if not driver:
                self.logger.error("No driver available")
                return None
            
            # Look for the export link
            self.logger.info(f"Looking for export link: '{self.export_link_text}'")
            
            # Try different methods to find the link
            export_link = None
            
            # Method 1: By link text
            try:
                export_link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, self.export_link_text))
                )
                self.logger.info("Found export link by link text")
            except TimeoutException:
                pass
            
            # Method 2: By partial link text  
            if not export_link:
                try:
                    export_link = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Terhelés"))
                    )
                    self.logger.info("Found export link by partial link text")
                except TimeoutException:
                    pass
            
            # Method 3: By text content in any element
            if not export_link:
                try:
                    export_link = driver.find_element(By.XPATH, f"//*[contains(text(), '{self.export_link_text}')]")
                    self.logger.info("Found export link by XPath text search")
                except Exception:
                    pass
            
            if not export_link:
                self.logger.error(f"Could not find export link '{self.export_link_text}'")
                # List all links for debugging
                links = driver.find_elements(By.TAG_NAME, "a")
                self.logger.info("Available links on page:")
                for link in links[:10]:  # Show first 10 links
                    text = link.get_attribute("innerText") or link.get_attribute("textContent") or ""
                    href = link.get_attribute("href") or ""
                    if text.strip():
                        self.logger.info(f"  - '{text.strip()}' -> {href}")
                return None
            
            # Clear download folder of old files
            for file in self.download_folder.glob("*.xls*"):
                try:
                    file.unlink()
                    self.logger.info(f"Removed old download: {file.name}")
                except Exception as e:
                    self.logger.warning(f"Could not remove old file {file.name}: {e}")
            
            # Click the export link
            self.logger.info("Clicking export link to download Excel file...")
            export_link.click()
            
            # Wait for download to complete
            self.logger.info("Waiting for download to complete...")
            downloaded_file = None
            max_wait_time = 30  # seconds
            start_time = time.time()
            
            while time.time() - start_time < max_wait_time:
                excel_files = list(self.download_folder.glob("*.xls*"))
                if excel_files:
                    # Check if file is still being downloaded (has .crdownload extension or is 0 bytes)
                    for file in excel_files:
                        if not file.name.endswith('.crdownload') and file.stat().st_size > 0:
                            downloaded_file = file
                            break
                    
                    if downloaded_file:
                        break
                
                time.sleep(1)
            
            if downloaded_file:
                self.logger.info(f"Successfully downloaded Excel file: {downloaded_file.name}")
                return downloaded_file
            else:
                self.logger.error("Download timed out or failed")
                return None
                
        except Exception as e:
            self.logger.error(f"Error downloading Excel file: {e}")
            return None
    
    def process_excel_file(self, excel_file_path: Path) -> List[Dict[str, Any]]:
        """
        Process the downloaded Excel file and extract student data
        
        Args:
            excel_file_path: Path to the Excel file
            
        Returns:
            List of student records with topic information
        """
        try:
            self.logger.info(f"Processing Excel file: {excel_file_path}")
            
            # Read all worksheets
            excel_data = pd.read_excel(excel_file_path, sheet_name=None)
            
            # Find the worksheet containing "konzultáció"
            target_sheet = None
            for sheet_name, sheet_data in excel_data.items():
                if "konzultáció" in sheet_name.lower():
                    target_sheet = sheet_name
                    break
            
            if not target_sheet:
                # If not found by name, try the second sheet (index 1)
                sheet_names = list(excel_data.keys())
                if len(sheet_names) >= 2:
                    target_sheet = sheet_names[1]
                    self.logger.info(f"Using second worksheet: {target_sheet}")
                else:
                    self.logger.error("Could not find worksheet containing 'konzultáció'")
                    return []
            else:
                self.logger.info(f"Found target worksheet: {target_sheet}")
            
            # Read the target worksheet
            df = excel_data[target_sheet]
            
            # Remove empty rows and columns
            df = df.dropna(how='all').dropna(axis=1, how='all')
            
            # Find the end of useful data (before copyright notice)
            copyright_row = None
            for idx, row in df.iterrows():
                row_text = ' '.join([str(cell) for cell in row if pd.notna(cell)])
                if "BME" in row_text and "Tanszék" in row_text:
                    copyright_row = idx
                    break
            
            if copyright_row is not None:
                df = df.iloc[:copyright_row]
                self.logger.info(f"Removed copyright section starting at row {copyright_row}")
            
            # Process the data - look for student information
            students_data = []
            
            # Try to identify columns containing student names and topic categories
            # This is a heuristic approach since we don't know the exact structure
            for idx, row in df.iterrows():
                row_dict = {}
                has_student_data = False
                
                for col_idx, cell_value in enumerate(row):
                    if pd.notna(cell_value):
                        cell_str = str(cell_value).strip()
                        
                        # Look for patterns that might indicate student data
                        if len(cell_str) > 2:  # Ignore very short values
                            # Add all non-empty cells with column headers
                            col_name = f"column_{col_idx}"
                            if col_idx < len(df.columns):
                                col_header = str(df.columns[col_idx])
                                if col_header and col_header != 'nan':
                                    col_name = col_header
                            
                            row_dict[col_name] = cell_str
                            has_student_data = True
                
                if has_student_data and len(row_dict) >= 2:  # At least 2 columns with data
                    students_data.append(row_dict)
            
            self.logger.info(f"Extracted {len(students_data)} student records")
            
            # Display first few records for verification
            if students_data:
                self.logger.info("Sample extracted data:")
                for i, record in enumerate(students_data[:3]):
                    self.logger.info(f"  Record {i+1}: {record}")
            
            return students_data
            
        except Exception as e:
            self.logger.error(f"Error processing Excel file: {e}")
            return []
    
    def collect_topic_data(self) -> List[Dict[str, Any]]:
        """
        Main method to collect student topic data from BME portal
        
        Returns:
            List of student records with topic information
        """
        try:
            # Step 1: Login to portal
            if not self.login_to_portal():
                self.logger.error("Failed to login to BME portal")
                return []
            
            # Step 2: Download Excel file
            excel_file = self.download_excel_file()
            if not excel_file:
                self.logger.error("Failed to download Excel file")
                return []
            
            # Step 3: Process Excel file
            student_data = self.process_excel_file(excel_file)
            
            if student_data:
                self.logger.info(f"Successfully collected data for {len(student_data)} students")
                self.collected_data = student_data
            else:
                self.logger.warning("No student data was extracted from the Excel file")
            
            return student_data
            
        except Exception as e:
            self.logger.error(f"Error in collect_topic_data: {e}")
            return []
        
        finally:
            # Clean up
            if self.selenium_utils.driver:
                self.selenium_utils.close_driver()
    
    def save_processed_data(self, output_file: Optional[Path] = None) -> bool:
        """
        Save the collected data to an Excel file
        
        Args:
            output_file: Path for output file (defaults to data/bme_topic_data.xlsx)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.collected_data:
            self.logger.warning("No data to save")
            return False
        
        if output_file is None:
            output_file = Path(__file__).parent.parent / "data" / "bme_topic_data.xlsx"
        
        try:
            excel_handler = ExcelHandler(output_file)
            success = excel_handler.create_excel_file(self.collected_data, "StudentTopics")
            
            if success:
                self.logger.info(f"Saved processed data to: {output_file}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error saving processed data: {e}")
            return False


def main():
    """Main function for testing the DLXLS feature"""
    collector = BMETopicDataCollector()
    
    # Collect data from BME portal
    data = collector.collect_topic_data()
    
    if data:
        # Save processed data
        collector.save_processed_data()
        print(f"Successfully collected and saved data for {len(data)} students")
    else:
        print("Failed to collect student topic data")


if __name__ == "__main__":
    main()
