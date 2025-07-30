#!/usr/bin/env python3
"""Quick test of the scraper functionality after logging fix."""

import logging

# Setup logging like main_simple.py does
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from topic_scraper_simple import TopicScraperSimple

def test_functionality():
    """Test basic functionality."""
    scraper = TopicScraperSimple()
    print("Testing scraper functionality...")
    
    # Test category parsing
    category_url = 'https://www.aut.bme.hu/Education/BScInfo/Onlab'
    topics = scraper._extract_topic_links_and_courses(category_url, category_url)
    print(f"Found {len(topics)} topics")
    
    if topics:
        first_topic = topics[0]
        print(f"First topic: {first_topic['title']}")
        print(f"Course codes: {first_topic['courses']}")
        print("✅ Course extraction working!")
    
    print("Test completed.")

if __name__ == "__main__":
    test_functionality()
