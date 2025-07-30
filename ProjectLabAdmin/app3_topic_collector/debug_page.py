"""
Debug script to inspect the HTML structure of a specific topic page
to see if the course dropdowns are present.
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def inspect_page_html(url):
    """Inspect the HTML structure of a topic page."""
    print(f"Inspecting page: {url}")
    print("="*60)
    
    # First, check with requests (static HTML)
    print("\n1. Static HTML content (requests):")
    try:
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for select elements
        selects = soup.find_all('select')
        print(f"Found {len(selects)} <select> elements in static HTML")
        for i, select in enumerate(selects):
            print(f"  Select {i+1}: id='{select.get('id', 'NO ID')}', name='{select.get('name', 'NO NAME')}'")
        
        # Look specifically for our target IDs
        course_group = soup.find('select', id='ddlCourseGroup')
        course = soup.find('select', id='ddlCourse')
        print(f"ddlCourseGroup found: {course_group is not None}")
        print(f"ddlCourse found: {course is not None}")
        
    except Exception as e:
        print(f"Error with requests: {e}")
    
    # Now check with Selenium (dynamic content)
    print("\n2. Dynamic content (Selenium):")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get(url)
        time.sleep(3)  # Wait for page to load
        
        # Look for select elements
        selects = driver.find_elements(By.TAG_NAME, "select")
        print(f"Found {len(selects)} <select> elements with Selenium")
        for i, select in enumerate(selects):
            element_id = select.get_attribute('id')
            element_name = select.get_attribute('name')
            print(f"  Select {i+1}: id='{element_id}', name='{element_name}'")
        
        # Look specifically for our target IDs
        try:
            course_group_elem = driver.find_element(By.ID, 'ddlCourseGroup')
            print(f"ddlCourseGroup found: YES")
            print(f"  Visible: {course_group_elem.is_displayed()}")
            print(f"  Enabled: {course_group_elem.is_enabled()}")
        except:
            print(f"ddlCourseGroup found: NO")
        
        try:
            course_elem = driver.find_element(By.ID, 'ddlCourse')
            print(f"ddlCourse found: YES")
            print(f"  Visible: {course_elem.is_displayed()}")
            print(f"  Enabled: {course_elem.is_enabled()}")
        except:
            print(f"ddlCourse found: NO")
        
        # Get page source snippet around selects
        page_source = driver.page_source
        if 'ddlCourseGroup' in page_source:
            print("\n3. Found 'ddlCourseGroup' in page source")
            # Find the line with ddlCourseGroup
            lines = page_source.split('\n')
            for i, line in enumerate(lines):
                if 'ddlCourseGroup' in line:
                    print(f"Line {i}: {line.strip()}")
                    # Show surrounding lines
                    for j in range(max(0, i-2), min(len(lines), i+3)):
                        if j != i:
                            print(f"Line {j}: {lines[j].strip()}")
                    break
        else:
            print("\n3. 'ddlCourseGroup' NOT found in page source")
        
        driver.quit()
        
    except Exception as e:
        print(f"Error with Selenium: {e}")

if __name__ == "__main__":
    url = "https://www.aut.bme.hu/Task/25-26-osz/5G-halozatba-kapcsolt-kamera"
    inspect_page_html(url)
