#!/usr/bin/env python3
"""
Debug script to test advisor and course code extraction.
"""

import requests
from bs4 import BeautifulSoup
import re

# Test with a specific topic page
test_url = "https://www.aut.bme.hu/Task/25-26-osz/5G-halozatba-kapcsolt-kamera"

def test_extraction():
    print("Testing extraction from:", test_url)
    
    # Fetch the page
    response = requests.get(test_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    page_text = soup.get_text()
    
    print("\n=== PAGE TEXT SAMPLE ===")
    print(page_text[:1000])  # First 1000 characters
    
    print("\n=== LOOKING FOR ADVISORS ===")
    # Check for advisor section
    advisors_text = "Konzulensek"
    if advisors_text in page_text:
        print(f"✓ Found '{advisors_text}' in page text")
        
        # Find the advisors section
        for element in soup.find_all(text=re.compile(advisors_text)):
            print(f"Found advisor text element: {element.strip()}")
            parent = element.parent
            print(f"Parent element: {parent.name if parent else 'None'}")
            
            if parent:
                print("Next siblings:")
                for i, sibling in enumerate(parent.find_next_siblings()):
                    if i > 3:  # Limit output
                        break
                    text = sibling.get_text().strip()
                    print(f"  Sibling {i}: {text[:100]}...")
    else:
        print(f"✗ '{advisors_text}' not found in page text")
    
    print("\n=== LOOKING FOR STUDENT LIMIT ===")
    student_limit_text = "Maximális létszám:"
    if student_limit_text in page_text:
        print(f"✓ Found '{student_limit_text}' in page text")
        pattern = rf'{re.escape(student_limit_text)}\s*(\d+)'
        match = re.search(pattern, page_text)
        if match:
            print(f"✓ Student limit: {match.group(1)}")
        else:
            print("✗ Could not extract student limit number")
    else:
        print(f"✗ '{student_limit_text}' not found in page text")
    
    print("\n=== LOOKING FOR EXTERNAL PARTNER ===")
    external_text = "Külső partner:"
    if external_text in page_text:
        print(f"✓ Found '{external_text}' in page text")
        pattern = rf'{re.escape(external_text)}\s*([^\n\r]+)'
        match = re.search(pattern, page_text)
        if match:
            partner = match.group(1).strip()
            print(f"✓ External partner: '{partner}'")
        else:
            print("✗ Could not extract external partner text")
    else:
        print(f"✗ '{external_text}' not found in page text")

def test_category_page():
    print("\n" + "="*60)
    print("TESTING CATEGORY PAGE COURSE EXTRACTION")
    print("="*60)
    
    category_url = "https://www.aut.bme.hu/Education/BScInfo/Onlab"
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print(f"Testing category page: {category_url}")
    
    # Look for "Kiírt témák" section
    topics_heading = "Kiírt témák"
    topics_section = None
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4']):
        if topics_heading in heading.get_text():
            topics_section = heading
            print(f"✓ Found topics section: {heading}")
            break
    
    if topics_section:
        container = topics_section.find_next(['div', 'ul', 'table'])
        if container:
            print(f"✓ Found container: {container.name}")
            
            # Get first few topic links
            topic_links = container.find_all('a', href=True) if hasattr(container, 'find_all') else []
            print(f"✓ Found {len(topic_links)} links")
            
            for i, link in enumerate(topic_links[:3]):  # Check first 3
                href = str(link.get('href', ''))
                if '/Task/' in href:
                    title = link.get_text().strip()
                    print(f"\n--- Topic {i+1}: {title} ---")
                    
                    # Look for course codes in surrounding text
                    parent = link.parent
                    if parent:
                        surrounding_text = parent.get_text()
                        print(f"Parent text: {surrounding_text[:200]}...")
                        
                        # Extract course codes
                        course_codes = re.findall(r'BME[A-Z]{2,}[A-Z0-9]+', surrounding_text)
                        print(f"Course codes found: {course_codes}")
                        
                        if not course_codes:
                            # Try looking at more siblings
                            for sibling in parent.find_next_siblings():
                                sibling_text = sibling.get_text()
                                more_codes = re.findall(r'BME[A-Z]{2,}[A-Z0-9]+', sibling_text)
                                course_codes.extend(more_codes)
                                if len(sibling_text) > 300:  # Don't go too far
                                    break
                            print(f"Extended search course codes: {course_codes}")

if __name__ == "__main__":
    test_extraction()
    test_category_page()
