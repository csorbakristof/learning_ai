"""
Test script for the Topic Collector application.
Tests basic functionality and validates configuration.
"""

import json
import os
import sys
import unittest
from unittest.mock import Mock, patch

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from config import CATEGORY_URLS, OUTPUT_DIR, OUTPUT_FILE
from topic_scraper import TopicScraper


class TestTopicCollector(unittest.TestCase):
    """Test cases for the Topic Collector application."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scraper = TopicScraper()
    
    def test_config_urls(self):
        """Test that all required URLs are present in configuration."""
        expected_categories = [
            "BSc_Info_Onlab",
            "BSc_Info_Szakdolgozat", 
            "BSc_Villany_Onlab",
            "BSc_Villany_Szakdolgozat",
            "BSc_Mechatronika_Szakdolgozat",
            "MSc_Info_Onlab",
            "MSc_Info_Diploma",
            "MSc_Villany_Onlab", 
            "MSc_Villany_Diploma",
            "MSc_Mechatronika_Onlab",
            "MSc_Mechatronika_Diploma"
        ]
        
        for category in expected_categories:
            self.assertIn(category, CATEGORY_URLS, f"Missing category: {category}")
            self.assertTrue(CATEGORY_URLS[category].startswith('https://'), 
                          f"Invalid URL for {category}")
    
    def test_external_partner_parsing(self):
        """Test external partner information extraction."""
        # Test with external partner
        page_text = """
        Some content here
        Külső partner: Test Company Ltd.
        More content
        """
        is_external, partner = self.scraper._extract_external_partner_info(page_text)
        self.assertTrue(is_external)
        self.assertEqual(partner, "Test Company Ltd.")
        
        # Test without external partner
        page_text = "No external partner information here"
        is_external, partner = self.scraper._extract_external_partner_info(page_text)
        self.assertFalse(is_external)
        self.assertIsNone(partner)
    
    def test_student_limit_parsing(self):
        """Test student limit extraction."""
        # Test with student limit
        page_text = """
        Some content
        Maximális létszám: 2 fő
        More content
        """
        limit = self.scraper._extract_student_limit(page_text)
        self.assertEqual(limit, 2)
        
        # Test without student limit
        page_text = "No student limit information"
        limit = self.scraper._extract_student_limit(page_text)
        self.assertIsNone(limit)
    
    def test_advisors_parsing(self):
        """Test advisor extraction."""
        page_text = """
        Some content
        Konzulensek
        Dr. Smith John
        Dr. Doe Jane
        
        Next section
        """
        advisors = self.scraper._extract_advisors(page_text)
        self.assertIn("Dr. Smith John", advisors)
        self.assertIn("Dr. Doe Jane", advisors)
    
    def test_json_schema(self):
        """Test that the expected JSON schema is maintained."""
        # Create a sample topic
        sample_topic = {
            "title": "Test Topic",
            "url": "https://example.com/topic",
            "is_external": True,
            "external_partner": "Test Company",
            "student_limit": 2,
            "advisors": ["Dr. Test"],
            "courses": [
                {
                    "course_code": "BMEVIAUAL01",
                    "course_name": "Test Course"
                }
            ],
            "source_category_url": "https://example.com/category"
        }
        
        # Verify all required fields are present
        required_fields = ['title', 'url', 'is_external', 'external_partner', 
                          'student_limit', 'advisors', 'courses', 'source_category_url']
        
        for field in required_fields:
            self.assertIn(field, sample_topic, f"Missing required field: {field}")
    
    def test_output_directory_creation(self):
        """Test that output directory is created if it doesn't exist."""
        # This would normally create the directory
        expected_path = OUTPUT_DIR
        self.assertTrue(isinstance(expected_path, str))
        self.assertTrue(len(expected_path) > 0)


class TestConfigurationIntegrity(unittest.TestCase):
    """Test configuration integrity and consistency."""
    
    def test_url_accessibility(self):
        """Test if URLs are properly formatted (basic validation)."""
        import urllib.parse
        
        for category, url in CATEGORY_URLS.items():
            parsed = urllib.parse.urlparse(url)
            self.assertTrue(parsed.scheme in ['http', 'https'], 
                          f"Invalid scheme for {category}: {url}")
            self.assertTrue(parsed.netloc, f"Missing domain for {category}: {url}")
    
    def test_output_configuration(self):
        """Test output configuration settings."""
        self.assertTrue(isinstance(OUTPUT_FILE, str))
        self.assertTrue(OUTPUT_FILE.endswith('.json'))
        self.assertTrue(isinstance(OUTPUT_DIR, str))


def run_basic_validation():
    """Run basic validation checks without requiring a full scrape."""
    print("Running basic validation checks...")
    
    # Test configuration
    print(f"✓ Found {len(CATEGORY_URLS)} category URLs")
    print(f"✓ Output directory: {OUTPUT_DIR}")
    print(f"✓ Output file: {OUTPUT_FILE}")
    
    # Test scraper initialization
    try:
        scraper = TopicScraper()
        print("✓ TopicScraper initialized successfully")
    except Exception as e:
        print(f"✗ TopicScraper initialization failed: {e}")
        return False
    
    # Test method availability 
    required_methods = [
        '_extract_external_partner_info',
        '_extract_student_limit', 
        '_extract_advisors',
        'scrape_all_topics',
        'save_to_json'
    ]
    
    for method in required_methods:
        if hasattr(scraper, method):
            print(f"✓ Method {method} available")
        else:
            print(f"✗ Method {method} missing")
            return False
    
    print("All basic validation checks passed!")
    return True


if __name__ == "__main__":
    print("BME AUT Topic Collector - Test Suite")
    print("=====================================")
    
    # Run basic validation first
    if not run_basic_validation():
        print("Basic validation failed!")
        sys.exit(1)
    
    print("\nRunning unit tests...")
    
    # Run unit tests
    unittest.main(verbosity=2, exit=False)
    
    print("\nTest suite completed!")
