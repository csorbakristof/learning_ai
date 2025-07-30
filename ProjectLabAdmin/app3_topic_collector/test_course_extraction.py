#!/usr/bin/env python3
"""
Test the updated course code extraction logic.
"""

import requests
from bs4 import BeautifulSoup
import re

def test_course_extraction():
    category_url = "https://www.aut.bme.hu/Education/BScInfo/Onlab"
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print("Testing course code extraction from category page...")
    
    # Look for "Kapcsolódó tárgyak" section
    related_courses_heading = "Kapcsolódó tárgyak"
    page_text = soup.get_text()
    
    if related_courses_heading in page_text:
        print(f"✓ Found '{related_courses_heading}' section")
        
        # Find the section
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4']):
            if related_courses_heading in heading.get_text():
                print(f"✓ Found heading: {heading}")
                
                # Get the container that follows
                container = heading.find_next(['div', 'ul', 'ol'])
                if container and hasattr(container, 'name'):
                    print(f"✓ Found container: {container.name}")
                    container_text = container.get_text()
                    print(f"Container text sample: {container_text[:300]}...")
                    
                    # Test the regex
                    course_codes = re.findall(r'\(([A-Z]{2,}[A-Z0-9]+)\)', container_text)
                    bme_codes = ['BME' + code for code in set(course_codes)]
                    
                    print(f"✓ Found course codes: {course_codes}")
                    print(f"✓ With BME prefix: {bme_codes}")
                    
                    # Also look for span elements with class="tip"
                    if hasattr(container, 'find_all'):
                        tip_spans = container.find_all('span', class_='tip')
                        print(f"✓ Found {len(tip_spans)} tip spans")
                        for span in tip_spans:
                            print(f"  Tip span content: {span.get_text()}")
                    else:
                        print("Container doesn't support find_all")
                break
    else:
        print(f"✗ '{related_courses_heading}' not found")

if __name__ == "__main__":
    test_course_extraction()
