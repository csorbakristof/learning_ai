#!/usr/bin/env python3
"""
BME AUT Topic Collector - Main Application (Simplified)

A console application for scraping topic information from BME AUT website
using static HTML parsing for improved performance and reliability.
"""

import argparse
import logging
import os
import sys

from topic_scraper_simple import TopicScraperSimple


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description='BME AUT Topic Collector - Scrape course topics using static HTML parsing'
    )
    parser.add_argument(
        '--output', '-o',
        default='../data/topics.json',
        help='Output JSON file path (default: ../data/topics.json)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    print("BME AUT Topic Collector (Simplified)")
    print("====================================")
    print(f"Output file: {args.output}")
    print(f"Verbose logging: {args.verbose}")
    print("\nUsing static HTML parsing - no browser automation required!")
    
    try:
        print("Initializing scraper...")
        scraper = TopicScraperSimple(output_file=args.output)
        
        print("Starting topic scraping process...")
        print("This process is much faster than the previous Selenium-based approach...")
        
        scraper.run()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
        return 1
    except Exception as e:
        print(f"Application failed: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
