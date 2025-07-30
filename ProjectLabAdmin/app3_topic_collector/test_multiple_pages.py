"""
Debug script to check multiple topic pages for course dropdowns
and test different wait times.
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def check_page_for_dropdowns(driver, url, wait_time=5):
    """Check a specific page for course dropdowns."""
    print(f"\nChecking: {url}")
    print("-" * 80)
    
    try:
        driver.get(url)
        print(f"Page loaded, waiting {wait_time} seconds...")
        time.sleep(wait_time)
        
        # Check for any select elements
        selects = driver.find_elements(By.TAG_NAME, "select")
        print(f"Found {len(selects)} <select> elements")
        
        if selects:
            for i, select in enumerate(selects):
                element_id = select.get_attribute('id')
                element_name = select.get_attribute('name')
                is_visible = select.is_displayed()
                print(f"  Select {i+1}: id='{element_id}', name='{element_name}', visible={is_visible}")
        
        # Try to find our specific dropdowns with explicit wait
        try:
            print("Waiting for ddlCourseGroup with explicit wait...")
            wait = WebDriverWait(driver, 10)
            course_group = wait.until(EC.presence_of_element_located((By.ID, "ddlCourseGroup")))
            print("✓ ddlCourseGroup found with explicit wait!")
            print(f"  Visible: {course_group.is_displayed()}")
            print(f"  Enabled: {course_group.is_enabled()}")
            
            # If found, try to find the course dropdown too
            course_dropdown = driver.find_element(By.ID, "ddlCourse")
            print("✓ ddlCourse also found!")
            print(f"  Visible: {course_dropdown.is_displayed()}")
            print(f"  Enabled: {course_dropdown.is_enabled()}")
            
            return True
            
        except Exception as e:
            print(f"✗ Dropdowns not found even with explicit wait: {e}")
            
            # Check if there's any JavaScript that might be loading them
            page_source = driver.page_source
            if 'ddlCourseGroup' in page_source:
                print("  BUT 'ddlCourseGroup' text found in page source")
            if 'select' in page_source.lower():
                print("  'select' text found in page source")
            
            return False
            
    except Exception as e:
        print(f"Error loading page: {e}")
        return False

def main():
    """Test multiple topic pages for dropdowns."""
    # Test URLs - mix of different topics
    test_urls = [
        "https://www.aut.bme.hu/Task/25-26-osz/5G-halozatba-kapcsolt-kamera",
        "https://www.aut.bme.hu/Task/25-26-osz/Net-alapu-fejlesztes", 
        "https://www.aut.bme.hu/Task/25-26-osz/AI-Need-for-speed",
        "https://www.aut.bme.hu/Task/25-26-osz/Beosztastervezesi-algoritmusok"
    ]
    
    print("Testing multiple topic pages for course dropdowns...")
    print("=" * 80)
    
    # Setup Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        results = []
        for url in test_urls:
            has_dropdowns = check_page_for_dropdowns(driver, url, wait_time=8)
            results.append((url, has_dropdowns))
        
        print("\n" + "=" * 80)
        print("SUMMARY:")
        print("=" * 80)
        for url, has_dropdowns in results:
            topic_name = url.split('/')[-1]
            status = "✓ HAS DROPDOWNS" if has_dropdowns else "✗ NO DROPDOWNS"
            print(f"{topic_name:40} {status}")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
