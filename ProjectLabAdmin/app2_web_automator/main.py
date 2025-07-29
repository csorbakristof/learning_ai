#!/usr/bin/env python3
"""
Application 2: Web Automator
This application reads data from an Excel file and performs automated actions on a webpage using Selenium.
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add shared module to path
sys.path.append(str(Path(__file__).parent.parent))

from shared import SeleniumUtils, ExcelHandler, setup_logging
from shared.config import EXCEL_OUTPUT_FILE
from selenium.webdriver.common.by import By
import time


class WebAutomator:
    """Main web automation class"""
    
    def __init__(self, excel_file_path: Optional[Path] = None):
        self.logger = setup_logging(__name__)
        self.selenium_utils = SeleniumUtils(headless=False)
        self.excel_handler = ExcelHandler(excel_file_path)
        self.data: List[Dict[str, Any]] = []
    
    def load_data_from_excel(self, sheet_name: Optional[str] = None) -> bool:
        """
        Load data from Excel file
        
        Args:
            sheet_name: Name of the sheet to read from
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.info("Loading data from Excel file...")
        
        # Get available sheets if no sheet name provided
        if sheet_name is None:
            sheets = self.excel_handler.get_sheet_names()
            if not sheets:
                self.logger.error("No sheets found in Excel file")
                return False
            sheet_name = sheets[0]  # Use first sheet
            self.logger.info(f"Using sheet: {sheet_name}")
        
        data = self.excel_handler.read_excel_data(sheet_name)
        if data is None:
            self.logger.error("Failed to load data from Excel")
            return False
        
        self.data = data
        
        self.logger.info(f"Loaded {len(self.data)} records from Excel")
        return True
    
    def perform_web_actions(self, url: str, actions_config: List[Dict[str, Any]], require_login: bool = True) -> bool:
        """
        Perform automated actions on a webpage
        
        Args:
            url: Target website URL
            actions_config: Configuration for actions to perform
            require_login: Whether to wait for user login
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.info(f"Starting web automation on {url}")
        
        try:
            driver = self.selenium_utils.setup_driver()
            driver.get(url)
            
            if require_login:
                self.logger.info("Please complete the login process...")
                if not self.selenium_utils.wait_for_user_login():
                    return False
            
            # Process each record from Excel
            for i, record in enumerate(self.data):
                self.logger.info(f"Processing record {i+1}/{len(self.data)}: {record}")
                
                # Perform actions for this record
                success = self._execute_actions(driver, actions_config, record)
                if not success:
                    self.logger.error(f"Failed to process record {i+1}")
                    continue
                
                # Small delay between records
                time.sleep(1)
            
            self.logger.info("Web automation completed successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during web automation: {e}")
            return False
        
        finally:
            self.selenium_utils.close_driver()
    
    def _execute_actions(self, driver, actions_config: List[Dict[str, Any]], record: Dict[str, Any]) -> bool:
        """
        Execute a sequence of actions for a single record
        
        Args:
            driver: Selenium WebDriver instance
            actions_config: List of actions to perform
            record: Data record from Excel
            
        Returns:
            True if successful, False otherwise
        """
        try:
            for action in actions_config:
                action_type = action.get('type')
                
                if action_type == 'click':
                    by = getattr(By, action.get('by', 'ID'))
                    value = action.get('value', '')
                    if value:
                        self.selenium_utils.safe_click(by, value)
                
                elif action_type == 'input':
                    by = getattr(By, action.get('by', 'ID'))
                    value = action.get('value', '')
                    
                    # Get text from record or use static text
                    text = action.get('text', '')
                    field_name = action.get('field_name')
                    if field_name and field_name in record:
                        text = str(record[field_name])
                    
                    if value:
                        self.selenium_utils.safe_send_keys(by, value, text)
                
                elif action_type == 'select':
                    # Handle dropdown selections
                    by = getattr(By, action.get('by', 'ID'))
                    value = action.get('value', '')
                    option_text = action.get('option_text', '')
                    
                    # Get option from record if specified
                    field_name = action.get('field_name')
                    if field_name and field_name in record:
                        option_text = str(record[field_name])
                    
                    if value:
                        from selenium.webdriver.support.ui import Select
                        element = self.selenium_utils.wait_for_element(by, value)
                        if element:
                            select = Select(element)
                            if option_text:
                                try:
                                    select.select_by_visible_text(option_text)
                                except:
                                    select.select_by_value(option_text)
                
                elif action_type == 'wait':
                    seconds = action.get('seconds', 1)
                    time.sleep(seconds)
                
                elif action_type == 'submit':
                    by = getattr(By, action.get('by', 'ID'))
                    value = action.get('value', '')
                    if value:
                        element = self.selenium_utils.wait_for_element(by, value)
                        if element:
                            element.submit()
                
                elif action_type == 'navigate':
                    url = action.get('url', '')
                    if url:
                        driver.get(url)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error executing actions: {e}")
            return False
    
    def run_automation(self, target_url: str, actions_config: List[Dict[str, Any]], 
                      excel_sheet: Optional[str] = None, require_login: bool = True):
        """
        Run the complete automation process
        
        Args:
            target_url: URL of the target website
            actions_config: Configuration for actions to perform
            excel_sheet: Name of the Excel sheet to read
            require_login: Whether to wait for user login
        """
        self.logger.info("Starting web automation process...")
        
        try:
            # Load data from Excel
            if not self.load_data_from_excel(excel_sheet):
                return
            
            # Perform web actions
            self.perform_web_actions(target_url, actions_config, require_login)
            
        except KeyboardInterrupt:
            self.logger.info("Web automation interrupted by user")
        except Exception as e:
            self.logger.error(f"Error during automation: {e}")


def main():
    """Main entry point"""
    # Example usage - customize these for your specific needs
    
    automator = WebAutomator()
    
    # Example actions configuration
    actions_config = [
        {
            'type': 'wait',
            'seconds': 2
        },
        {
            'type': 'input',
            'by': 'ID',
            'value': 'search-field',
            'field_name': 'search_term'  # This will use the 'search_term' column from Excel
        },
        {
            'type': 'click',
            'by': 'ID',
            'value': 'search-button'
        },
        {
            'type': 'wait',
            'seconds': 3
        }
    ]
    
    # Run automation
    target_url = "https://example.com"  # Replace with your target URL
    automator.run_automation(
        target_url=target_url,
        actions_config=actions_config,
        require_login=True  # Set to False if login is not required
    )


if __name__ == "__main__":
    main()
