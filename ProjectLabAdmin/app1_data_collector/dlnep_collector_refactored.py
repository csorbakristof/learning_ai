"""
DLNEP - Student data collection from the Neptun system (Refactored)
This module handles downloading student lists from all courses in the Neptun system.
Refactored according to SOLID principles for better maintainability.
"""

import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd

import sys
sys.path.append(str(Path(__file__).parent.parent))

from shared import SeleniumUtils, ExcelHandler, setup_logging
from .course_identification import CourseTableFinder, CourseTableParser, CourseValidator
from .course_download import DownloadSession


class NeptunStudentDataCollectorRefactored:
    """Refactored collector for student data from Neptun system"""
    
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
        
        # Neptun system URLs
        self.login_url = "https://neptun.bme.hu/oktatoi/login.aspx"
        self.courses_url = "https://neptun.bme.hu/oktatoi/main.aspx?ismenuclick=true&ctrl=1902"
        
        # Initialize helper classes
        self.course_finder = CourseTableFinder(self.logger)
        self.course_parser = CourseTableParser(self.logger)
        self.course_validator = CourseValidator(self.logger)
        
        self.collected_data = []
        self.downloaded_files = []
    
    def setup_driver_with_downloads(self):
        """
        Set up Chrome driver with download preferences
        """
        try:
            # Configure download preferences
            download_prefs = {
                "download.default_directory": str(self.download_folder.absolute()),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            
            # Initialize driver with download preferences
            self.selenium_utils.setup_driver(
                headless=False,
                download_folder=self.download_folder,
                chrome_prefs=download_prefs
            )
            
            self.logger.info(f"Driver setup complete with download folder: {self.download_folder}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up driver: {e}")
            return False
    
    def login_to_neptun(self) -> bool:
        """
        Navigate to Neptun login page and wait for user to log in
        
        Returns:
            True if login successful, False otherwise
        """
        try:
            driver = self.selenium_utils.driver
            if not driver:
                self.logger.error("No driver available")
                return False
            
            self.logger.info("Navigating to Neptun login page...")
            driver.get(self.login_url)
            
            # Wait for user to log in manually
            self.logger.info("⏳ Please log in to Neptun manually. Waiting for login to complete...")
            print("⏳ Please log in to Neptun manually. Press Enter after you have logged in successfully.")
            input()
            
            # Navigate to courses page
            self.logger.info("Navigating to courses page...")
            driver.get(self.courses_url)
            time.sleep(3)  # Wait for page to load
            
            # Verify we're on the correct page
            if "main.aspx" in driver.current_url:
                self.logger.info("✅ Successfully logged in and navigated to courses page")
                return True
            else:
                self.logger.error("❌ Login verification failed - not on expected page")
                return False
                
        except Exception as e:
            self.logger.error(f"Error during login process: {e}")
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
            time.sleep(2)  # Wait for the page to fully load
            
            # Step 1: Find the course table
            course_table = self.course_finder.find_course_table(driver)
            if not course_table:
                return []
            
            # Step 2: Parse the header row to identify column positions
            header_indices, header_row_idx = self.course_parser.parse_header_row(course_table)
            if not header_indices:
                return []
            
            # Step 3: Extract courses from table rows
            courses = self.course_parser.extract_courses_from_rows(course_table, header_indices, header_row_idx)
            
            # Step 4: Validate and filter courses
            valid_courses = self.course_validator.filter_valid_courses(courses)
            
            self.logger.info(f"Total valid courses found: {len(valid_courses)}")
            return valid_courses
            
        except Exception as e:
            self.logger.error(f"Error getting course list: {e}")
            return []
    
    def collect_all_course_data(self) -> List[Dict[str, Any]]:
        """
        Collect student data from all courses in Neptun
        
        Returns:
            List of dictionaries containing course and student data
        """
        try:
            # Step 1: Setup driver
            self.logger.info("Setting up Chrome driver with download preferences...")
            if not self.setup_driver_with_downloads():
                return []
            
            # Step 2: Login to Neptun
            if not self.login_to_neptun():
                return []
            
            # Step 3: Get course list
            courses = self.get_course_list()
            if not courses:
                self.logger.error("No valid courses found")
                return []
            
            # Step 4: Download student lists for all courses
            download_session = DownloadSession(
                self.selenium_utils.driver, 
                self.logger, 
                self.download_folder
            )
            
            self.downloaded_files = download_session.download_all_courses(courses)
            
            # Step 5: Process downloaded files
            self.collected_data = self.process_downloaded_files()
            
            return self.collected_data
            
        except Exception as e:
            self.logger.error(f"Error in collect_all_course_data: {e}")
            return []
        
        finally:
            # Clean up
            if self.selenium_utils:
                self.selenium_utils.cleanup()
    
    def process_downloaded_files(self) -> List[Dict[str, Any]]:
        """
        Process all downloaded Excel files to extract student data
        
        Returns:
            List of dictionaries containing processed student data
        """
        processed_data = []
        
        try:
            excel_files = list(self.download_folder.glob("*.xlsx"))
            self.logger.info(f"Processing {len(excel_files)} downloaded Excel files...")
            
            excel_handler = ExcelHandler()
            
            for file_path in excel_files:
                try:
                    self.logger.info(f"Processing file: {file_path.name}")
                    
                    # Read Excel file
                    df = excel_handler.read_excel(file_path)
                    if df is None or df.empty:
                        self.logger.warning(f"Empty or invalid Excel file: {file_path.name}")
                        continue
                    
                    # Extract course code from filename
                    course_code = self._extract_course_code_from_filename(file_path.name)
                    
                    # Process each student row
                    for _, row in df.iterrows():
                        student_data = self._extract_student_data_from_row(row, course_code, file_path.name)
                        if student_data:
                            processed_data.append(student_data)
                    
                    self.logger.info(f"Processed {len(df)} students from {file_path.name}")
                    
                except Exception as e:
                    self.logger.error(f"Error processing file {file_path.name}: {e}")
                    continue
            
            self.logger.info(f"Total processed student records: {len(processed_data)}")
            return processed_data
            
        except Exception as e:
            self.logger.error(f"Error processing downloaded files: {e}")
            return []
    
    def save_processed_data(self, output_file: Optional[Path] = None) -> bool:
        """
        Save processed data to JSON file
        
        Args:
            output_file: Output file path (defaults to data/neptun_student_data.json)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if output_file is None:
                output_file = Path(__file__).parent.parent / "data" / "neptun_student_data.json"
            
            import json
            
            output_data = {
                "metadata": {
                    "total_students": len(self.collected_data),
                    "total_files_processed": len(self.downloaded_files),
                    "download_folder": str(self.download_folder),
                    "creation_date": pd.Timestamp.now().isoformat()
                },
                "students": self.collected_data
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Data saved to: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving data: {e}")
            return False
    
    def _extract_course_code_from_filename(self, filename: str) -> str:
        """Extract course code from filename"""
        # Pattern to match BMEVI followed by letters/numbers
        import re
        match = re.search(r'(BMEVI[A-Z]+\d+)', filename.upper())
        return match.group(1) if match else "UNKNOWN"
    
    def _extract_student_data_from_row(self, row, course_code: str, filename: str) -> Optional[Dict[str, Any]]:
        """Extract student data from Excel row"""
        try:
            # Extract student information from row
            # This assumes standard Neptun Excel format
            student_neptun = str(row.get('Neptun kód', '')).strip()
            student_name = str(row.get('Név', '')).strip()
            
            if not student_neptun or student_neptun == 'nan':
                return None
            
            return {
                'student_neptun': student_neptun,
                'student_name': student_name,
                'course_code': course_code,
                'source_file': filename,
                'schedule_type': str(row.get('Órarend típus', '')).strip(),
                'entry': str(row.get('Felvétel', '')).strip(),
                'partial_result': str(row.get('Részeredmény', '')).strip()
            }
            
        except Exception as e:
            self.logger.warning(f"Error extracting student data from row: {e}")
            return None


def main():
    """Main function for testing the refactored DLNEP collector"""
    collector = NeptunStudentDataCollectorRefactored()
    
    print("🚀 Starting DLNEP data collection...")
    data = collector.collect_all_course_data()
    
    if data:
        print(f"✅ Collection successful! Collected {len(data)} student records")
        
        # Save data
        if collector.save_processed_data():
            print("✅ Data saved successfully")
        else:
            print("❌ Failed to save data")
            
        # Show summary
        courses = set(record['course_code'] for record in data)
        print(f"📊 Summary:")
        print(f"   • Total students: {len(data)}")
        print(f"   • Unique courses: {len(courses)}")
        print(f"   • Downloaded files: {len(collector.downloaded_files)}")
        
    else:
        print("❌ Collection failed!")


if __name__ == "__main__":
    main()
