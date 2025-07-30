"""
Main entry point for the Topic Collector application.
This module provides the console interface for running the topic scraper.
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime

# Add parent directory to path to import shared modules if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from topic_scraper import TopicScraper
from config import OUTPUT_DIR, OUTPUT_FILE


def setup_logging(log_level: str = "INFO"):
    """Set up logging configuration for the application."""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(f'topic_collector_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
        ]
    )


def print_statistics(topics_data: list):
    """Print statistics about the scraped data."""
    if not topics_data:
        print("No topics were scraped.")
        return
    
    total_topics = len(topics_data)
    external_topics = sum(1 for topic in topics_data if topic.get('is_external', False))
    topics_with_courses = sum(1 for topic in topics_data if topic.get('courses'))
    
    # Count topics by source category
    category_counts = {}
    for topic in topics_data:
        source_url = topic.get('source_category_url', 'Unknown')
        category_counts[source_url] = category_counts.get(source_url, 0) + 1
    
    print("\n" + "="*60)
    print("SCRAPING STATISTICS")
    print("="*60)
    print(f"Total topics scraped: {total_topics}")
    print(f"External topics: {external_topics}")
    print(f"Topics with course information: {topics_with_courses}")
    print("\nTopics by category:")
    for category, count in category_counts.items():
        category_name = category.split('/')[-1] if '/' in category else category
        print(f"  {category_name}: {count}")
    print("="*60)


def validate_output(output_path: str) -> bool:
    """Validate the generated JSON output."""
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print("ERROR: Output is not a list")
            return False
        
        # Validate schema for first few items
        required_fields = ['title', 'url', 'is_external', 'external_partner', 
                          'student_limit', 'advisors', 'courses', 'source_category_url']
        
        for i, item in enumerate(data[:5]):  # Check first 5 items
            if not isinstance(item, dict):
                print(f"ERROR: Item {i} is not a dictionary")
                return False
            
            for field in required_fields:
                if field not in item:
                    print(f"ERROR: Item {i} missing required field: {field}")
                    return False
        
        print(f"✓ Output validation passed for {len(data)} topics")
        return True
        
    except Exception as e:
        print(f"ERROR: Output validation failed: {e}")
        return False


def main():
    """Main function with command line argument handling."""
    parser = argparse.ArgumentParser(
        description="BME AUT Topic Collector - Scrape course topics from the university website",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Run with default settings
  python main.py --verbose          # Run with detailed logging
  python main.py --output my_topics.json  # Save to custom filename
  python main.py --headless         # Run in headless mode
        """
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=OUTPUT_FILE,
        help=f'Output filename (default: {OUTPUT_FILE})'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode'
    )
    
    parser.add_argument(
        '--validate-only',
        type=str,
        help='Only validate an existing JSON file (provide path)'
    )
    
    args = parser.parse_args()
    
    # Set up logging
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(log_level)
    
    logger = logging.getLogger(__name__)
    
    # Handle validation-only mode
    if args.validate_only:
        if os.path.exists(args.validate_only):
            success = validate_output(args.validate_only)
            sys.exit(0 if success else 1)
        else:
            print(f"ERROR: File not found: {args.validate_only}")
            sys.exit(1)
    
    # Configure headless mode if requested
    if args.headless:
        from config import SELENIUM_CONFIG
        SELENIUM_CONFIG["headless"] = True
        logger.info("Running in headless mode")
        print("WARNING: Headless mode enabled - user login will not be possible!")
        print("The application requires user authentication to access course dropdowns.")
        print("Consider running without --headless flag for full functionality.")
        print()
    
    # Start scraping
    print("BME AUT Topic Collector")
    print("=======================")
    print(f"Output file: {args.output}")
    print(f"Headless mode: {args.headless}")
    print(f"Verbose logging: {args.verbose}")
    print()
    
    try:
        print("Initializing scraper...")
        scraper = TopicScraper()
        
        print("Starting topic scraping process...")
        print("This may take several minutes depending on the number of topics...")
        print()
        
        # Scrape all topics
        topics_data = scraper.scrape_all_topics()
        
        if not topics_data:
            print("WARNING: No topics were scraped!")
            sys.exit(1)
        
        # Save to JSON
        output_path = scraper.save_to_json(args.output)
        
        # Print statistics
        print_statistics(topics_data)
        
        # Validate output
        if validate_output(output_path):
            print(f"\n✓ Successfully completed! Data saved to: {output_path}")
        else:
            print(f"\n⚠ Completed with validation errors. Check: {output_path}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user.")
        logger.info("Application interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        logger.error(f"Application failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
