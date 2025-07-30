"""
Demo script for the Topic Collector application.
Tests the scraping functionality with a single URL for demonstration.
"""

import os
import sys
import json
from datetime import datetime

from topic_scraper import TopicScraper
from config import CATEGORY_URLS


def demo_scraping():
    """Demonstrate the scraping functionality with a single category."""
    print("BME AUT Topic Collector - Demo")
    print("==============================")
    print()
    
    # Select first category for demo
    demo_category = list(CATEGORY_URLS.keys())[0]
    demo_url = CATEGORY_URLS[demo_category]
    
    print(f"Demo category: {demo_category}")
    print(f"Demo URL: {demo_url}")
    print()
    
    try:
        scraper = TopicScraper()
        
        # Test topic link extraction first (no Selenium needed)
        print("Testing topic link extraction...")
        topic_links = scraper._extract_topic_links(demo_url)
        
        if topic_links:
            print(f"✓ Found {len(topic_links)} topic links:")
            for i, (title, url) in enumerate(topic_links[:3], 1):  # Show first 3
                print(f"  {i}. {title}")
                print(f"     URL: {url}")
                if i >= 3 and len(topic_links) > 3:
                    print(f"     ... and {len(topic_links) - 3} more")
                    break
        else:
            print("⚠ No topic links found")
            return
        
        print()
        print("Demo completed successfully!")
        print("Note: Full scraping with Selenium would require user interaction.")
        print("To run the full scraper, use: python main.py")
        
    except Exception as e:
        print(f"Demo failed: {e}")
        import traceback
        traceback.print_exc()


def test_parsing_functions():
    """Test the parsing functions with sample data."""
    print("\nTesting parsing functions:")
    print("-" * 30)
    
    scraper = TopicScraper()
    
    # Test external partner parsing
    sample_text_1 = """
    Some content here
    Külső partner: Example Company Ltd.
    More content follows
    """
    
    is_external, partner = scraper._extract_external_partner_info(sample_text_1)
    print(f"External partner test: {is_external}, '{partner}'")
    
    # Test student limit parsing
    sample_text_2 = """
    Various information
    Maximális létszám: 3 fő
    Additional details
    """
    
    limit = scraper._extract_student_limit(sample_text_2)
    print(f"Student limit test: {limit}")
    
    # Test advisor parsing
    sample_text_3 = """
    Topic description
    Konzulensek
    Dr. Smith John
    Dr. Doe Jane
    
    Next section starts here
    """
    
    advisors = scraper._extract_advisors(sample_text_3)
    print(f"Advisors test: {advisors}")


if __name__ == "__main__":
    demo_scraping()
    test_parsing_functions()
    
    print("\n" + "="*50)
    print("Demo completed!")
    print("For full functionality, run: python main.py")
