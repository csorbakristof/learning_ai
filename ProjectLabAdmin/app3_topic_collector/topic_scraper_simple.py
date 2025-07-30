"""
BME AUT Topic Scraper - Simplified Version

This module provides functionality to scrape topic information from BME AUT website
using static HTML parsing for improved performance and reliability.
"""

import json
import logging
import os
import re
import time
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from config import (
    CATEGORY_URLS,
    OUTPUT_DIR,
    OUTPUT_FILE,
    TOPICS_HEADING,
    EXTERNAL_PARTNER_TEXT,
    STUDENT_LIMIT_TEXT,
    ADVISORS_TEXT,
    BASE_URL,
    HTTP_TIMEOUT,
    REQUEST_DELAY,
    USER_AGENT
)


class TopicScraperSimple:
    """
    Simplified topic scraper that uses static HTML parsing instead of browser automation.
    """
    
    def __init__(self, output_file: Optional[str] = None):
        """Initialize the scraper with configuration."""
        self.output_file = output_file or os.path.join(OUTPUT_DIR, OUTPUT_FILE)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': USER_AGENT
        })
        
        # Setup logging - use existing root logger to avoid duplication
        self.logger = logging.getLogger('topic_scraper')
        # Don't add handlers if basicConfig was already called
        self.logger.setLevel(logging.INFO)
    
    def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch a web page and return parsed HTML."""
        try:
            self.logger.info(f"Fetching page: {url}")
            response = self.session.get(url, timeout=HTTP_TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except requests.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None
    
    def _extract_course_codes_from_text(self, text: str) -> List[str]:
        """Extract BME course codes from text using regex."""
        # Look for patterns like (VIAUAL01), (VIAUM039), etc. in parentheses
        # and add BME prefix
        course_codes = re.findall(r'\(([A-Z]{2,}[A-Z0-9]+)\)', text)
        # Add BME prefix and return
        return ['BME' + code for code in set(course_codes)]  # Remove duplicates and add BME prefix
    
    def _extract_topic_links_and_courses(self, soup: BeautifulSoup, category_url: str) -> List[Dict]:
        """Extract topic links and associated course codes from category page."""
        topics = []
        
        try:
            # First, extract course codes from "Kapcsolódó tárgyak" section
            category_course_codes = []
            related_courses_heading = "Kapcsolódó tárgyak"
            
            for heading in soup.find_all(['h1', 'h2', 'h3', 'h4']):
                if related_courses_heading in heading.get_text():
                    container = heading.find_next(['div', 'ul', 'ol'])
                    if container:
                        container_text = container.get_text()
                        # Extract course codes in parentheses and add BME prefix
                        raw_codes = re.findall(r'\(([A-Z]{2,}[A-Z0-9]+)\)', container_text)
                        category_course_codes = ['BME' + code for code in set(raw_codes)]
                        self.logger.info(f"Found category course codes: {category_course_codes}")
                        break
            
            # Then, find the "Kiírt témák" section
            topics_section = None
            for heading in soup.find_all(['h1', 'h2', 'h3', 'h4']):
                if TOPICS_HEADING in heading.get_text():
                    topics_section = heading
                    break
            
            if not topics_section:
                self.logger.warning(f"Topics section not found on {category_url}")
                return topics
            
            # Find the container with topics (usually follows the heading)
            container = topics_section.find_next(['div', 'ul', 'table'])
            if not container:
                self.logger.warning(f"Topics container not found on {category_url}")
                return topics
            
            # Extract topic entries - be more specific about BeautifulSoup types
            topic_links = container.find_all('a', href=True) if hasattr(container, 'find_all') else []
            
            for link in topic_links:
                href = link.get('href')
                if not href:
                    continue
                
                # Convert href to string if it's not already
                href_str = str(href) if href else ""
                if not href_str or href_str.startswith('#'):
                    continue
                
                # Skip advisor links (they usually contain names with titles)
                link_text = link.get_text().strip()
                if any(title in link_text for title in ['Dr.', 'Prof.', 'PhD']):
                    continue
                
                # Skip links that go to staff pages
                if '/Staff/' in href_str:
                    continue
                
                # Build full URL
                if href_str.startswith('/'):
                    full_url = urljoin(BASE_URL, href_str)
                else:
                    full_url = urljoin(category_url, href_str)
                
                # Only include task links
                if '/Task/' in full_url:
                    topics.append({
                        'title': link_text,
                        'url': full_url,
                        'course_codes': category_course_codes,  # Use category course codes
                        'source_category_url': category_url
                    })
                    
                    self.logger.debug(f"Found topic: {link_text} with {len(category_course_codes)} course codes")
            
            self.logger.info(f"Found {len(topics)} topics on {category_url}")
            return topics
            
        except Exception as e:
            self.logger.error(f"Error extracting topics from {category_url}: {e}")
            return topics
    
    def _extract_topic_details(self, topic_url: str) -> Dict:
        """Extract detailed information from a topic page."""
        details = {
            'is_external': False,
            'external_partner': None,
            'student_limit': None,
            'advisors': []
        }
        
        soup = self._fetch_page(topic_url)
        if not soup:
            return details
        
        try:
            page_text = soup.get_text()
            
            # Extract external partner information
            if EXTERNAL_PARTNER_TEXT in page_text:
                # Find the text after "Külső partner:"
                pattern = rf'{re.escape(EXTERNAL_PARTNER_TEXT)}\s*([^\n\r]+)'
                match = re.search(pattern, page_text)
                if match:
                    partner = match.group(1).strip()
                    if partner and partner.lower() not in ['nincs', 'n/a', '-']:
                        details['is_external'] = True
                        details['external_partner'] = partner
            
            # Extract student limit
            if STUDENT_LIMIT_TEXT in page_text:
                pattern = rf'{re.escape(STUDENT_LIMIT_TEXT)}\s*(\d+)'
                match = re.search(pattern, page_text)
                if match:
                    details['student_limit'] = int(match.group(1))
            
            # Extract advisors - they are in <a> tags with href="/Staff/"
            advisors = []
            advisor_links = soup.find_all('a', href=re.compile(r'/Staff/'))
            for link in advisor_links:
                advisor_name = link.get_text().strip()
                if advisor_name and advisor_name not in advisors:
                    advisors.append(advisor_name)
            
            details['advisors'] = advisors
            
        except Exception as e:
            self.logger.error(f"Error extracting details from {topic_url}: {e}")
        
        return details
    
    def _process_category(self, category_name: str, category_url: str) -> List[Dict]:
        """Process a single category and extract all topics."""
        self.logger.info(f"Processing category: {category_name}")
        
        soup = self._fetch_page(category_url)
        if not soup:
            return []
        
        # Extract topics and course codes from category page
        topic_entries = self._extract_topic_links_and_courses(soup, category_url)
        
        processed_topics = []
        
        for entry in topic_entries:
            # Add delay between requests to be respectful
            time.sleep(REQUEST_DELAY)
            
            # Extract detailed information from topic page
            details = self._extract_topic_details(entry['url'])
            
            # Prepare courses array
            courses = []
            for course_code in entry['course_codes']:
                courses.append({
                    'course_code': course_code,
                    'course_name': course_code  # Use code as name since we don't have full names
                })
            
            # Assemble final topic object
            topic = {
                'title': entry['title'],
                'url': entry['url'],
                'is_external': details['is_external'],
                'external_partner': details['external_partner'],
                'student_limit': details['student_limit'],
                'advisors': details['advisors'],
                'courses': courses,
                'source_category_url': entry['source_category_url']
            }
            
            processed_topics.append(topic)
            self.logger.info(f"Successfully processed topic: {entry['title']}")
        
        self.logger.info(f"Completed category: {category_name}")
        return processed_topics
    
    def scrape_all_topics(self) -> List[Dict]:
        """Scrape all topics from all categories."""
        all_topics = []
        
        self.logger.info("Starting topic scraping process...")
        self.logger.info(f"Processing {len(CATEGORY_URLS)} categories...")
        
        for category_name, category_url in CATEGORY_URLS.items():
            try:
                topics = self._process_category(category_name, category_url)
                all_topics.extend(topics)
                
                # Add delay between categories
                time.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Error processing category {category_name}: {e}")
                continue
        
        self.logger.info(f"Scraping completed. Total topics found: {len(all_topics)}")
        return all_topics
    
    def save_topics(self, topics: List[Dict]) -> None:
        """Save topics to JSON file."""
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(topics, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"Topics saved to {self.output_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving topics to {self.output_file}: {e}")
            raise
    
    def run(self) -> None:
        """Run the complete scraping process."""
        try:
            topics = self.scrape_all_topics()
            self.save_topics(topics)
            
            print(f"\nScraping completed successfully!")
            print(f"Total topics scraped: {len(topics)}")
            print(f"Output saved to: {self.output_file}")
            
        except KeyboardInterrupt:
            self.logger.info("Scraping interrupted by user")
            print("\nScraping interrupted by user.")
        
        except Exception as e:
            self.logger.error(f"Scraping failed: {e}")
            print(f"Scraping failed: {e}")
            raise
