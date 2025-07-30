#!/usr/bin/env python3
"""
Deep HTML structure analysis
"""

import requests
from bs4 import BeautifulSoup
import re

def analyze_topic_page():
    test_url = "https://www.aut.bme.hu/Task/25-26-osz/5G-halozatba-kapcsolt-kamera"
    response = requests.get(test_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print("=== FULL HTML STRUCTURE AROUND KONZULENSEK ===")
    
    # Find konzulensek section more precisely
    konzulensek_text = soup.find(string=re.compile(r"Konzulensek"))
    if konzulensek_text:
        print(f"Found text: '{str(konzulensek_text).strip()}'")
        parent = konzulensek_text.parent
        print(f"Parent tag: {parent.name if parent and hasattr(parent, 'name') else 'None'}")
        
        # Get the containing structure
        container = parent.parent if parent else None
        if container and hasattr(container, 'name'):
            print(f"Container tag: {container.name}")
            print("Container content:")
            print(str(container)[:500])
            
            # Look for advisor information in the container
            print("\n=== SEARCHING FOR ADVISOR NAMES ===")
            container_text = container.get_text()
            advisor_names = re.findall(r'[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]+ [A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]+', container_text)
            print(f"Found potential advisor names: {advisor_names}")
    
    print("\n=== ALTERNATIVE: SEARCH FOR KNOWN ADVISOR NAMES ===")
    known_advisors = ["Gótzy Márton", "Blázovics László"]
    for advisor in known_advisors:
        if advisor in soup.get_text():
            print(f"Found '{advisor}' in page text")
            # Find the exact location
            elements = soup.find_all(string=re.compile(advisor))
            for elem in elements:
                print(f"  Found in: {elem.parent.name if elem.parent and hasattr(elem.parent, 'name') else 'text node'}")

def analyze_category_page():
    print("\n" + "="*60)
    print("ANALYZING CATEGORY PAGE FOR COURSE CODES")
    print("="*60)
    
    category_url = "https://www.aut.bme.hu/Education/BScInfo/Onlab"
    response = requests.get(category_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Save full HTML to file for inspection
    with open('category_page.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Saved full HTML to category_page.html")
    
    # Look for any BME course codes in the entire page
    page_text = soup.get_text()
    
    all_course_codes = re.findall(r'BME[A-Z]{2,}[A-Z0-9]+', page_text)
    print(f"All BME course codes found on page: {set(all_course_codes)}")
    
    # Look for the specific pattern that might contain course codes
    # Check if course codes appear anywhere near topic titles
    topics_section = None
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4']):
        if "Kiírt témák" in heading.get_text():
            topics_section = heading
            break
    
    if topics_section:
        # Get the next element (likely contains the topic list)
        next_elem = topics_section.find_next()
        if next_elem and hasattr(next_elem, 'name'):
            print(f"\nElement after 'Kiírt témák': {next_elem.name}")
            
            # Save this section to file for detailed inspection
            with open('topics_section.html', 'w', encoding='utf-8') as f:
                f.write(str(next_elem))
            print("Saved topics section to topics_section.html")

if __name__ == "__main__":
    analyze_topic_page()
    analyze_category_page()
