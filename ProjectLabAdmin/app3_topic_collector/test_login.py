"""
Test script to verify login functionality and course dropdown access.
This script will test the login process and check if dropdowns appear after login.
"""

from topic_scraper import TopicScraper
from config import SELENIUM_CONFIG
import time

def test_login_and_dropdowns():
    """Test the login functionality and dropdown access."""
    print("BME AUT Topic Collector - Login Test")
    print("====================================")
    print()
    
    # Ensure we're not in headless mode
    SELENIUM_CONFIG["headless"] = False
    
    scraper = TopicScraper()
    scraper.driver = scraper._setup_driver()
    
    try:
        # Test login process
        print("Testing login process...")
        login_success = scraper._wait_for_user_login()
        
        if not login_success:
            print("Login test failed!")
            return
        
        # Test a specific topic page after login
        test_url = "https://www.aut.bme.hu/Task/25-26-osz/5G-halozatba-kapcsolt-kamera"
        print(f"\nTesting topic page after login: {test_url}")
        
        scraper.driver.get(test_url)
        time.sleep(3)
        
        # Check for dropdowns
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select
        
        try:
            course_group_dropdown = Select(scraper.driver.find_element(By.ID, "ddlCourseGroup"))
            print("✓ Course group dropdown found after login!")
            print(f"  Options: {len(course_group_dropdown.options)}")
            
            course_dropdown = scraper.driver.find_element(By.ID, "ddlCourse")
            print("✓ Course dropdown found after login!")
            
            # Test extracting courses
            print("\nTesting course extraction...")
            courses = scraper._extract_courses(test_url)
            print(f"Extracted {len(courses)} courses:")
            for course in courses[:5]:  # Show first 5
                print(f"  - {course['course_code']}: {course['course_name']}")
            if len(courses) > 5:
                print(f"  ... and {len(courses) - 5} more")
                
        except Exception as e:
            print(f"✗ Dropdowns still not found after login: {e}")
            
            # Check what selects are available
            selects = scraper.driver.find_elements(By.TAG_NAME, "select")
            print(f"Found {len(selects)} select elements:")
            for i, select in enumerate(selects):
                element_id = select.get_attribute('id')
                element_name = select.get_attribute('name')
                print(f"  {i+1}. id='{element_id}', name='{element_name}'")
        
        print("\nLogin test completed!")
        
    finally:
        if scraper.driver:
            print("\nClosing browser in 5 seconds...")
            time.sleep(5)
            scraper.driver.quit()

if __name__ == "__main__":
    test_login_and_dropdowns()
