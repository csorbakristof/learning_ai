"""
Quick demo script to show the JSON output format with a few topics.
This version will stop after processing a few topics to show the structure.
"""

import json
import os
import sys
from topic_scraper import TopicScraper
from config import CATEGORY_URLS, OUTPUT_DIR

def quick_demo():
    """Run a quick demo with limited topics to show JSON structure."""
    print("Topic Collector - Quick Demo")
    print("============================")
    
    # Select first category for demo
    demo_category = list(CATEGORY_URLS.keys())[0]
    demo_url = CATEGORY_URLS[demo_category]
    
    print(f"Processing category: {demo_category}")
    print(f"URL: {demo_url}")
    print("Limiting to first 3 topics for demo...")
    print()
    
    try:
        scraper = TopicScraper()
        
        # Get topic links
        topic_links = scraper._extract_topic_links(demo_url)
        print(f"Found {len(topic_links)} topics total")
        
        # Process only first 3 topics
        demo_topics = []
        for i, (title, url) in enumerate(topic_links[:3]):
            print(f"Processing topic {i+1}: {title}")
            topic_data = scraper._scrape_topic_details(title, url, demo_url)
            demo_topics.append(topic_data)
        
        # Create output directory if needed
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Save demo data
        demo_file = os.path.join(OUTPUT_DIR, "demo_topics.json")
        with open(demo_file, 'w', encoding='utf-8') as f:
            json.dump(demo_topics, f, ensure_ascii=False, indent=2)
        
        print(f"\nDemo data saved to: {demo_file}")
        print("\nFirst topic structure:")
        print(json.dumps(demo_topics[0], ensure_ascii=False, indent=2))
        
        return demo_file
        
    except Exception as e:
        print(f"Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    quick_demo()
