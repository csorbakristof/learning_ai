#!/usr/bin/env python3
"""
CSV2PDF Script: Convert CSV files to PDF using SmartDoc website automation

This script processes all UTF-8 encoded CSV files in the current directory and converts them to PDF
using the SmartDoc website at BME through Selenium automation.

The script includes configurable delays (BROWSER_OPERATION_DELAY) after each browser operation
to ensure stability and avoid overwhelming the website.

Requirements:
- selenium
- chrome driver
- Access to BME network for SmartDoc website
- CSV files must be UTF-8 encoded (use xls2csv.bas v2.0 to generate them)
"""

import os
import time
import glob
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import sys

# Configuration constants
BROWSER_OPERATION_DELAY = 5  # Seconds to wait after each browser operation


class CSV2PDFConverter:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.smartdoc_url = "https://smartdoc.bme.hu/Hallgatoi_munkaszerzodes_gradualisnak/Hallgatoi_munkaszerzodes_gradualisnak.html"
        
    def setup_driver(self):
        """Initialize Chrome WebDriver with appropriate options"""
        print("Setting up Chrome WebDriver...")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Set download directory to current directory
        download_dir = str(Path.cwd().absolute())
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            # Try to use system Chrome driver first
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            print("Chrome WebDriver initialized successfully.")
            return True
        except WebDriverException as e:
            print(f"Error initializing Chrome WebDriver: {e}")
            print("Please ensure Chrome and ChromeDriver are installed and accessible.")
            return False
    
    def test_website_access(self):
        """Test if the SmartDoc website is accessible"""
        print(f"Testing access to SmartDoc website: {self.smartdoc_url}")
        
        try:
            self.driver.get(self.smartdoc_url)
            time.sleep(BROWSER_OPERATION_DELAY)
            # Wait for page to load and check if we can find the expected elements
            self.wait.until(EC.presence_of_element_located((By.ID, "AdatExpImp")))
            print("✓ SmartDoc website is accessible and page loaded successfully.")
            return True
        except TimeoutException:
            print("✗ ERROR: SmartDoc website is not accessible or page elements not found.")
            print("This script requires access to BME network to reach the SmartDoc website.")
            return False
        except Exception as e:
            print(f"✗ ERROR accessing SmartDoc website: {e}")
            return False
    
    def get_csv_files(self):
        """Get list of CSV files in current directory"""
        csv_files = glob.glob("*.csv")
        if not csv_files:
            print("No CSV files found in current directory.")
            return []
        
        print(f"Found {len(csv_files)} CSV file(s):")
        for csv_file in csv_files:
            print(f"  - {csv_file}")
        return csv_files
    
    def read_csv_content(self, csv_file):
        """Read CSV file content (UTF-8 encoded only)
        
        Note: All CSV files are expected to be UTF-8 encoded.
        Use xls2csv.bas v2.0 to generate properly encoded CSV files.
        """
        try:
            with open(csv_file, 'r', encoding='utf-8-sig') as f:  # utf-8-sig removes BOM
                content = f.read()
            
            # Strip any remaining BOM characters that might be present
            content = content.lstrip('\ufeff')
            
            # Strip leading/trailing whitespace but preserve internal structure
            content = content.strip()
            
            return content
        except Exception as e:
            print(f"Error reading CSV file {csv_file}: {e}")
            print("Ensure the CSV file is UTF-8 encoded (regenerate with xls2csv.bas v2.0 if needed)")
            return None
    
    def process_csv_file(self, csv_file):
        """Process a single CSV file through the SmartDoc website"""
        print(f"\nProcessing: {csv_file}")
        
        # Read CSV content
        csv_content = self.read_csv_content(csv_file)
        if csv_content is None:
            return False
        
        try:
            # Step 1: Click on "Adat export/import" button
            print("  1. Clicking 'Adat export/import' button...")
            adat_button = self.wait.until(EC.element_to_be_clickable((By.ID, "AdatExpImp")))
            adat_button.click()
            time.sleep(BROWSER_OPERATION_DELAY)
            
            # Step 2: Find CSV textbox and paste content
            print("  2. Pasting CSV content into textbox...")
            csv_box = self.wait.until(EC.presence_of_element_located((By.ID, "csvBox")))
            csv_box.clear()
            csv_box.send_keys(csv_content)
            time.sleep(BROWSER_OPERATION_DELAY)
            
            # Step 3: Click "CSV => HTML" button
            print("  3. Clicking 'CSV => HTML' button...")
            # csv_to_html_button = self.wait.until(EC.element_to_be_clickable((By.ID, "CsvToHTML")))
            # csv_to_html_button.click()
            # time.sleep(BROWSER_OPERATION_DELAY)
            
            # Manual step: Wait for user to click "CSV => HTML" button
            print("  3. MANUAL STEP: Please click the 'CSV => HTML' button in the browser manually.")
            input("      Press Enter after you have clicked the 'CSV => HTML' button to continue...")
            time.sleep(BROWSER_OPERATION_DELAY)
            
            # Step 4: Handle potential warning popups
            print("  4. Handling potential warning popups...")
            time.sleep(2)  # Wait a bit for popups to appear
            self.handle_warning_popups()
            time.sleep(BROWSER_OPERATION_DELAY)
            
            # Step 5: Click "PDF letöltése" button
            print("  5. Clicking 'PDF letöltése' button...")
            pdf_button = self.wait.until(EC.element_to_be_clickable((By.ID, "PDFLetoltes")))
            pdf_button.click()
            time.sleep(BROWSER_OPERATION_DELAY)
            
            # Step 6: Wait for download to complete
            print("  6. Waiting for PDF download to complete...")
            self.wait_for_download()
            
            print(f"✓ Successfully processed {csv_file}")
            return True
            
        except TimeoutException as e:
            print(f"✗ Timeout error processing {csv_file}: {e}")
            return False
        except Exception as e:
            print(f"✗ Error processing {csv_file}: {e}")
            return False
    
    def handle_warning_popups(self):
        """Handle any warning popup windows that may appear"""
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                # Try to find and dismiss alert dialogs
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                print(f"    Warning popup detected: {alert_text}")
                alert.accept()  # Click OK
                time.sleep(1)  # Wait a bit before checking for more popups
            except:
                # No more alerts
                break
    
    def wait_for_download(self):
        """Wait for PDF download to complete"""
        # Simple wait strategy - wait for a reasonable time
        # In a production environment, you might want to monitor the download directory
        time.sleep(5)
    
    def convert_all_csv_files(self):
        """Main method to convert all CSV files to PDF"""
        print("=== CSV2PDF Converter Starting ===")
        
        # Setup WebDriver
        if not self.setup_driver():
            return False
        
        try:
            # Test website access
            if not self.test_website_access():
                return False
            
            # Get CSV files
            csv_files = self.get_csv_files()
            if not csv_files:
                return False
            
            # Process each CSV file
            successful = 0
            failed = 0
            
            for csv_file in csv_files:
                if self.process_csv_file(csv_file):
                    successful += 1
                else:
                    failed += 1
                
                # Delay between files using the configurable constant
                time.sleep(BROWSER_OPERATION_DELAY)
            
            print(f"\n=== Conversion Complete ===")
            print(f"Successfully processed: {successful} files")
            print(f"Failed: {failed} files")
            
            return failed == 0
            
        finally:
            if self.driver:
                print("Closing browser...")
                self.driver.quit()


def main():
    """Main entry point"""
    converter = CSV2PDFConverter()
    success = converter.convert_all_csv_files()
    
    if success:
        print("\n✓ All CSV files converted successfully!")
        sys.exit(0)
    else:
        print("\n✗ Some errors occurred during conversion.")
        sys.exit(1)


if __name__ == "__main__":
    main()
