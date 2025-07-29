#!/usr/bin/env python3
"""
Application 1: Data Collector
This application scrapes data from web pages and saves it to an Excel file.
It can use both requests/BeautifulSoup for simple scraping and Selenium for complex interactions.
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add shared module to path
sys.path.append(str(Path(__file__).parent.parent))

from shared import WebScrapingUtils, SeleniumUtils, ExcelHandler, setup_logging
from shared.config import EXCEL_OUTPUT_FILE
from selenium.webdriver.common.by import By

# Import DLXLS feature
from dlxls_collector import BMETopicDataCollector

# Import DLNEP feature  
from dlnep_collector import NeptunStudentDataCollector

# Import DLFUSION feature
from dlfusion_processor import DataFusionProcessor

# Import MKXLSX feature
from mkxlsx_creator import SessionPlannerExcelCreator


class DataCollector:
    """Main data collector class"""
    
    def __init__(self):
        self.logger = setup_logging(__name__)
        self.web_utils = WebScrapingUtils()
        self.selenium_utils = SeleniumUtils(headless=False)  # Set to True for headless mode
        self.excel_handler = ExcelHandler()
        self.collected_data = []
    
    def scrape_with_requests(self, url: str, selectors: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Scrape data using requests and BeautifulSoup
        
        Args:
            url: URL to scrape
            selectors: Dictionary mapping field names to CSS selectors
            
        Returns:
            List of dictionaries containing scraped data
        """
        self.logger.info(f"Scraping {url} with requests...")
        
        soup = self.web_utils.get_page_content(url)
        if not soup:
            return []
        
        data = []
        
        # Extract data based on selectors
        for field_name, selector in selectors.items():
            elements = self.web_utils.extract_text_by_selector(soup, selector)
            
            # If this is the first field, create records
            if not data:
                data = [{field_name: element} for element in elements]
            else:
                # Add field to existing records
                for i, element in enumerate(elements):
                    if i < len(data):
                        data[i][field_name] = element
        
        self.logger.info(f"Scraped {len(data)} records from {url}")
        return data
    
    def scrape_with_selenium(self, url: str, actions: List[Dict[str, Any]], require_login: bool = False) -> List[Dict[str, Any]]:
        """
        Scrape data using Selenium for complex interactions
        
        Args:
            url: URL to scrape
            actions: List of actions to perform (click, input, wait, etc.)
            require_login: Whether to wait for user login
            
        Returns:
            List of dictionaries containing scraped data
        """
        self.logger.info(f"Scraping {url} with Selenium...")
        
        try:
            driver = self.selenium_utils.setup_driver()
            driver.get(url)
            
            if require_login:
                self.logger.info("Waiting for user to complete login...")
                if not self.selenium_utils.wait_for_user_login():
                    return []
            
            data = []
            
            # Perform actions
            for action in actions:
                action_type = action.get('type')
                
                if action_type == 'click':
                    by = getattr(By, action.get('by', 'ID'))
                    value = action.get('value', '')
                    if value:
                        self.selenium_utils.safe_click(by, value)
                
                elif action_type == 'input':
                    by = getattr(By, action.get('by', 'ID'))
                    value = action.get('value', '')
                    text = action.get('text', '')
                    if value:
                        self.selenium_utils.safe_send_keys(by, value, text)
                
                elif action_type == 'wait':
                    seconds = action.get('seconds', 1)
                    import time
                    time.sleep(seconds)
                
                elif action_type == 'extract':
                    # Extract data from current page
                    selectors = action.get('selectors', {})
                    for field_name, selector in selectors.items():
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        values = [elem.text.strip() for elem in elements]
                        
                        # Add to data
                        if not data:
                            data = [{field_name: value} for value in values]
                        else:
                            for i, value in enumerate(values):
                                if i < len(data):
                                    data[i][field_name] = value
            
            self.logger.info(f"Scraped {len(data)} records with Selenium")
            return data
            
        except Exception as e:
            self.logger.error(f"Error during Selenium scraping: {e}")
            return []
        
        finally:
            self.selenium_utils.close_driver()
    
    def collect_neptun_student_data(self) -> List[Dict[str, Any]]:
        """
        Collect student data from Neptun system (DLNEP feature)
        
        Returns:
            List of student records from all courses
        """
        self.logger.info("Starting Neptun student data collection (DLNEP)...")
        
        try:
            # Create Neptun student data collector
            neptun_collector = NeptunStudentDataCollector()
            
            # Collect data from all courses
            course_results = neptun_collector.collect_all_course_data()
            
            if course_results:
                self.logger.info(f"Successfully processed {len(course_results)} courses")
                
                # Process downloaded files to extract student data
                student_data = neptun_collector.process_downloaded_files()
                
                if student_data:
                    self.logger.info(f"Successfully collected {len(student_data)} student records")
                    
                    # Save to separate file for reference
                    neptun_collector.save_processed_data()
                    
                    return student_data
                else:
                    self.logger.warning("No student data was extracted from Neptun files")
                    return []
            else:
                self.logger.warning("No courses were processed from Neptun system")
                return []
                
        except Exception as e:
            self.logger.error(f"Error during Neptun student data collection: {e}")
            return []
    
    def collect_bme_topic_data(self) -> List[Dict[str, Any]]:
        """
        Collect student topic data from BME portal (DLXLS feature)
        
        Returns:
            List of student records with topic information
        """
        self.logger.info("Starting BME topic data collection (DLXLS)...")
        
        try:
            # Create BME topic data collector
            bme_collector = BMETopicDataCollector()
            
            # Collect data from BME portal
            topic_data = bme_collector.collect_topic_data()
            
            if topic_data:
                self.logger.info(f"Successfully collected {len(topic_data)} student topic records")
                
                # Save to separate file for reference
                bme_collector.save_processed_data()
                
                return topic_data
            else:
                self.logger.warning("No topic data was collected from BME portal")
                return []
                
        except Exception as e:
            self.logger.error(f"Error during BME topic data collection: {e}")
            return []
    
    def collect_fused_data(self) -> Dict[str, Any]:
        """
        Collect and fuse data from DLXLS and DLNEP sources (DLFUSION feature)
        
        Returns:
            Dictionary containing fused student data and metadata
        """
        self.logger.info("Starting data fusion (DLFUSION)...")
        
        try:
            # Create data fusion processor
            fusion_processor = DataFusionProcessor()
            
            # Process the fusion using existing downloaded files
            success = fusion_processor.process_fusion()
            
            if success:
                summary = fusion_processor.get_fusion_summary()
                self.logger.info(f"Data fusion completed successfully:")
                self.logger.info(f"- Total students: {summary['total_students']}")
                self.logger.info(f"- Students with topics: {summary['students_with_topics']}")
                self.logger.info(f"- Students with enrollments: {summary['students_with_enrollments']}")
                self.logger.info(f"- Students with both: {summary['students_with_both']}")
                self.logger.info(f"- Unique courses: {summary['unique_courses']}")
                
                return {
                    'fused_data': fusion_processor.fused_data,
                    'summary': summary,
                    'success': True
                }
            else:
                self.logger.error("Data fusion failed")
                return {'success': False}
                
        except Exception as e:
            self.logger.error(f"Error during data fusion: {e}")
            return {'success': False}
    
    def create_session_planning_excel(self) -> Dict[str, Any]:
        """
        Create Excel table for session planning (MKXLSX feature)
        
        Returns:
            Dictionary containing Excel creation results and metadata
        """
        self.logger.info("Starting Excel table creation for session planning (MKXLSX)...")
        
        try:
            # Create session planner Excel creator
            excel_creator = SessionPlannerExcelCreator()
            
            # Process the MKXLSX using existing fused data
            success = excel_creator.process_mkxlsx()
            
            if success:
                summary = excel_creator.get_planning_summary()
                self.logger.info(f"Session planning Excel created successfully:")
                self.logger.info(f"- Total students: {summary['total_students']}")
                self.logger.info(f"- Students with topics: {summary['students_with_topics']}")
                self.logger.info(f"- Required sessions: {summary['required_sessions']}")
                self.logger.info(f"- Planning slots available: {summary['planner_dimensions']['total_slots']}")
                
                return {
                    'summary': summary,
                    'success': True
                }
            else:
                self.logger.error("Excel table creation failed")
                return {'success': False}
                
        except Exception as e:
            self.logger.error(f"Error during Excel table creation: {e}")
            return {'success': False}
    
    def add_sample_scrapers(self):
        """Add some sample scraping configurations"""
        
        # DLXLS: Collect BME topic data
        topic_data = self.collect_bme_topic_data()
        if topic_data:
            self.collected_data.extend(topic_data)
        
        # DLNEP: Collect Neptun student data
        student_data = self.collect_neptun_student_data()
        if student_data:
            self.collected_data.extend(student_data)
        
        # DLFUSION: Fuse data from DLXLS and DLNEP
        fusion_result = self.collect_fused_data()
        if fusion_result.get('success'):
            self.logger.info("Data fusion completed successfully")
            print("\n🔗 DLFUSION Results:")
            summary = fusion_result['summary']
            print(f"   • Total students: {summary['total_students']}")
            print(f"   • Students with topics: {summary['students_with_topics']}")
            print(f"   • Students with enrollments: {summary['students_with_enrollments']}")
            print(f"   • Unique courses: {summary['unique_courses']}")
        
        # MKXLSX: Create Excel table for session planning
        excel_result = self.create_session_planning_excel()
        if excel_result.get('success'):
            self.logger.info("Session planning Excel created successfully")
            print("\n📊 MKXLSX Results:")
            summary = excel_result['summary']
            print(f"   • Session planning Excel created")
            print(f"   • Planning slots: {summary['planner_dimensions']['total_slots']}")
            print(f"   • Required sessions: {summary['required_sessions']}")
            if summary['hungarian_topic_categories'] or summary['english_topic_categories']:
                total_categories = len(summary['hungarian_topic_categories']) + len(summary['english_topic_categories'])
                print(f"   • Topic categories: {total_categories}")
        
        # Example 1: Simple web scraping with requests (kept for demonstration)
        # sample_data_1 = self.scrape_with_requests(
        #     url="https://quotes.toscrape.com/",
        #     selectors={
        #         'quote': '.quote .text',
        #         'author': '.quote .author',
        #         'tags': '.quote .tags'
        #     }
        # )
        # self.collected_data.extend(sample_data_1)
        
        # You can add more scrapers here...
        
    def save_to_excel(self) -> bool:
        """
        Save collected data to Excel file
        
        Returns:
            True if successful, False otherwise
        """
        if not self.collected_data:
            self.logger.warning("No data to save")
            return False
        
        success = self.excel_handler.create_excel_file(self.collected_data)
        if success:
            self.logger.info(f"Data saved to {EXCEL_OUTPUT_FILE}")
        
        return success
    
    def run(self):
        """Run the data collection process"""
        self.logger.info("Starting data collection...")
        
        try:
            # Add your scraping logic here
            self.add_sample_scrapers()
            
            # Save to Excel
            if self.save_to_excel():
                self.logger.info("Data collection completed successfully!")
            else:
                self.logger.error("Failed to save data to Excel")
        
        except KeyboardInterrupt:
            self.logger.info("Data collection interrupted by user")
        except Exception as e:
            self.logger.error(f"Error during data collection: {e}")


def main():
    """Main entry point"""
    collector = DataCollector()
    collector.run()


if __name__ == "__main__":
    main()
