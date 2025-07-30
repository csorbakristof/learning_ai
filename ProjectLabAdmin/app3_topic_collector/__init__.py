"""
BME AUT Topic Collector Package

This package provides functionality to scrape course topic information
from the BME Department of Automation and Applied Informatics website.
"""

__version__ = "1.0.0"
__author__ = "AI Assistant"
__description__ = "BME AUT Topic Collector - Web scraper for university course topics"

from .topic_scraper import TopicScraper
from .config import CATEGORY_URLS, OUTPUT_DIR, OUTPUT_FILE

__all__ = ['TopicScraper', 'CATEGORY_URLS', 'OUTPUT_DIR', 'OUTPUT_FILE']
