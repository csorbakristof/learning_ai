"""
Topic scraper module for extracting topic information from BME AUT website.
Uses Selenium for dynamic content handling and BeautifulSoup for HTML parsing.
"""

import json
import logging
import os
import time
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from config import (
    CATEGORY_URLS,
    SELENIUM_CONFIG,
    OUTPUT_DIR,
    OUTPUT_FILE,
    TOPICS_HEADING,
    EXTERNAL_PARTNER_TEXT,
    STUDENT_LIMIT_TEXT,
    ADVISORS_SECTION_TEXT,
    COURSE_GROUP_DROPDOWN_ID,
    COURSE_DROPDOWN_ID,
    DROPDOWN_WAIT_TIME,
    PAGE_LOAD_WAIT_TIME,
    COURSE_CODE_PREFIX,
    DEFAULT_STUDENT_LIMIT,
    DEFAULT_EXTERNAL_PARTNER
)


class TopicScraper:
    """Main class for scraping topic information from BME AUT website."""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.driver = None
        self.topics_data = []
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('topic_scraper.log')
            ]
        )
        return logging.getLogger(__name__)
    
    def _setup_driver(self) -> webdriver.Chrome:
        """Initialize and configure the Chrome WebDriver."""
        try:
            chrome_options = Options()
            if SELENIUM_CONFIG["headless"]:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument(f"--window-size={SELENIUM_CONFIG['window_size'][0]},{SELENIUM_CONFIG['window_size'][1]}")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            driver.implicitly_wait(SELENIUM_CONFIG["implicit_wait"])
            driver.set_page_load_timeout(SELENIUM_CONFIG["page_load_timeout"])
            
            self.logger.info("Chrome WebDriver initialized successfully")
            return driver
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def _wait_for_user_login(self):
        """Wait for user to log in to the BME AUT website."""
        if SELENIUM_CONFIG["headless"]:
            self.logger.warning("Running in headless mode - cannot wait for user login!")
            print("WARNING: Running in headless mode. User authentication required but not possible.")
            print("Please run without --headless flag to enable user login.")
            return False
        
        # Navigate to the BME AUT login page
        login_url = "https://www.aut.bme.hu"
        self.logger.info(f"Opening login page: {login_url}")
        self.driver.get(login_url)
        
        print("\n" + "="*60)
        print("USER LOGIN REQUIRED")
        print("="*60)
        print("The browser window has opened to the BME AUT website.")
        print("Please log in to your account using the 'Bejelentkezés' button.")
        print()
        print("Steps to log in:")
        print("1. Click 'Bejelentkezés' in the top menu")
        print("2. Enter your credentials and log in")
        print("3. Wait for the login to complete")
        print("4. Return to this terminal and press ENTER to continue")
        print()
        print("The application will continue automatically after you log in...")
        print("="*60)
        
        # Wait for user input
        input("Press ENTER after you have successfully logged in...")
        
        print("Continuing with topic scraping...")
        self.logger.info("User confirmed login completion")
        return True
    
    def _extract_topic_links(self, category_url: str) -> List[Tuple[str, str]]:
        """Extract topic links from a category page.
        
        Args:
            category_url: URL of the category page
            
        Returns:
            List of tuples containing (title, url) for each topic
        """
        try:
            response = requests.get(category_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the "Kiírt témák" heading
            topics_heading = None
            for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                if TOPICS_HEADING in heading.get_text():
                    topics_heading = heading
                    break
            
            if not topics_heading:
                self.logger.warning(f"Topics heading '{TOPICS_HEADING}' not found on {category_url}")
                return []
            
            # Find all links after the heading, but filter out advisor links
            topic_links = []
            current_element = topics_heading.next_sibling
            
            while current_element:
                if hasattr(current_element, 'find_all'):
                    links = current_element.find_all('a', href=True)
                    for link in links:
                        title = link.get_text().strip()
                        url = urljoin(category_url, link['href'])
                        
                        # Filter out advisor/staff links and other non-topic links
                        if title and url and self._is_topic_link(title, url):
                            topic_links.append((title, url))
                current_element = current_element.next_sibling
            
            self.logger.info(f"Found {len(topic_links)} topics on {category_url}")
            return topic_links
            
        except Exception as e:
            self.logger.error(f"Error extracting topic links from {category_url}: {e}")
            return []
    
    def _is_topic_link(self, title: str, url: str) -> bool:
        """Determine if a link is a topic link or something else (like advisor link).
        
        Args:
            title: Link text/title
            url: Link URL
            
        Returns:
            True if this appears to be a topic link, False otherwise
        """
        # Filter out advisor/staff profile links
        if '/Staff/' in url:
            self.logger.debug(f"Skipping staff link: {title} ({url})")
            return False
        
        # Filter out links that look like advisor names (contain "Dr." or common name patterns)
        if any(pattern in title for pattern in ['Dr.', 'Prof.', 'PhD']):
            self.logger.debug(f"Skipping advisor name: {title}")
            return False
        
        # Filter out very short titles that are likely not topics
        if len(title.strip()) < 3:
            self.logger.debug(f"Skipping short title: {title}")
            return False
        
        # Topic links should contain '/Task/' in the URL
        if '/Task/' not in url:
            self.logger.debug(f"Skipping non-task link: {title} ({url})")
            return False
        
        return True
    
    def _extract_external_partner_info(self, page_text: str) -> Tuple[bool, Optional[str]]:
        """Extract external partner information from page text.
        
        Args:
            page_text: Text content of the page
            
        Returns:
            Tuple of (is_external, external_partner_name)
        """
        if EXTERNAL_PARTNER_TEXT in page_text:
            lines = page_text.split('\n')
            for i, line in enumerate(lines):
                if EXTERNAL_PARTNER_TEXT in line:
                    # Get the partner name from the same line or next line
                    partner_text = line.replace(EXTERNAL_PARTNER_TEXT, '').strip()
                    if not partner_text and i + 1 < len(lines):
                        partner_text = lines[i + 1].strip()
                    return True, partner_text if partner_text else None
        return False, None
    
    def _extract_student_limit(self, page_text: str) -> Optional[int]:
        """Extract student limit from page text.
        
        Args:
            page_text: Text content of the page
            
        Returns:
            Student limit as integer or None if not found
        """
        try:
            lines = page_text.split('\n')
            for line in lines:
                if STUDENT_LIMIT_TEXT in line:
                    # Extract number from text like "2 fő"
                    import re
                    numbers = re.findall(r'\d+', line)
                    if numbers:
                        return int(numbers[0])
        except Exception as e:
            self.logger.warning(f"Error parsing student limit: {e}")
        return DEFAULT_STUDENT_LIMIT
    
    def _extract_advisors(self, page_text: str) -> List[str]:
        """Extract advisor names from page text.
        
        Args:
            page_text: Text content of the page
            
        Returns:
            List of advisor names
        """
        advisors = []
        try:
            lines = page_text.split('\n')
            in_advisors_section = False
            
            for line in lines:
                line = line.strip()
                if ADVISORS_SECTION_TEXT in line:
                    in_advisors_section = True
                    continue
                
                if in_advisors_section:
                    if line and not line.startswith('•') and not line.startswith('-'):
                        # Stop when we reach another section or empty line
                        if any(keyword in line.lower() for keyword in ['külső', 'maximális', 'részletek']):
                            break
                        advisors.append(line)
                    elif not line:  # Empty line might indicate end of section
                        break
        except Exception as e:
            self.logger.warning(f"Error parsing advisors: {e}")
        
        return advisors
    
    def _extract_courses(self, topic_url: str) -> List[Dict[str, str]]:
        """Extract course information using Selenium.
        
        Args:
            topic_url: URL of the topic detail page
            
        Returns:
            List of course dictionaries with course_code and course_name
        """
        courses = []
        try:
            self.driver.get(topic_url)
            time.sleep(PAGE_LOAD_WAIT_TIME)
            
            # Find course group dropdown
            try:
                course_group_dropdown = Select(self.driver.find_element(By.ID, COURSE_GROUP_DROPDOWN_ID))
            except NoSuchElementException:
                self.logger.warning(f"Course group dropdown not found on {topic_url}")
                return courses
            
            # First, collect all option values to avoid stale element issues
            option_values = []
            for option in course_group_dropdown.options[1:]:  # Skip first empty option
                value = option.get_attribute('value')
                if value:
                    option_values.append(value)
            
            # Iterate through course groups using collected values
            for option_value in option_values:
                try:
                    # Re-select the dropdown to avoid stale reference
                    course_group_dropdown = Select(self.driver.find_element(By.ID, COURSE_GROUP_DROPDOWN_ID))
                    course_group_dropdown.select_by_value(option_value)
                    time.sleep(DROPDOWN_WAIT_TIME)
                    
                    # Wait for course dropdown to be populated
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.ID, COURSE_DROPDOWN_ID))
                    )
                    
                    course_dropdown = Select(self.driver.find_element(By.ID, COURSE_DROPDOWN_ID))
                    
                    # Extract courses from dropdown
                    for course_option in course_dropdown.options[1:]:  # Skip first empty option
                        course_text = course_option.text.strip()
                        if course_text:
                            # Extract course code and format it
                            import re
                            code_match = re.search(r'([A-Z]{2,}[A-Z0-9]+)', course_text)
                            if code_match:
                                course_code = f"{COURSE_CODE_PREFIX}{code_match.group(1)}"
                                courses.append({
                                    "course_code": course_code,
                                    "course_name": course_text
                                })
                
                except Exception as e:
                    self.logger.warning(f"Error processing course group option: {e}")
                    continue
            
        except Exception as e:
            self.logger.error(f"Error extracting courses from {topic_url}: {e}")
        
        return courses
    
    def _scrape_topic_details(self, title: str, topic_url: str, source_category_url: str) -> Dict:
        """Scrape detailed information for a single topic.
        
        Args:
            title: Topic title
            topic_url: URL of the topic detail page
            source_category_url: URL of the source category page
            
        Returns:
            Dictionary containing topic information
        """
        try:
            self.driver.get(topic_url)
            time.sleep(PAGE_LOAD_WAIT_TIME)
            
            # Get page text content
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            # Extract information
            is_external, external_partner = self._extract_external_partner_info(page_text)
            student_limit = self._extract_student_limit(page_text)
            advisors = self._extract_advisors(page_text)
            courses = self._extract_courses(topic_url)
            
            topic_data = {
                "title": title,
                "url": topic_url,
                "is_external": is_external,
                "external_partner": external_partner,
                "student_limit": student_limit,
                "advisors": advisors,
                "courses": courses,
                "source_category_url": source_category_url
            }
            
            self.logger.info(f"Successfully scraped topic: {title}")
            return topic_data
            
        except Exception as e:
            self.logger.error(f"Error scraping topic details for {topic_url}: {e}")
            return {
                "title": title,
                "url": topic_url,
                "is_external": False,
                "external_partner": None,
                "student_limit": None,
                "advisors": [],
                "courses": [],
                "source_category_url": source_category_url
            }
    
    def scrape_all_topics(self) -> List[Dict]:
        """Scrape all topics from all category URLs.
        
        Returns:
            List of topic dictionaries
        """
        self.driver = self._setup_driver()
        
        try:
            # Wait for user to log in first
            if not self._wait_for_user_login():
                self.logger.error("Login required but not possible in current mode")
                return []
            
            for category_name, category_url in CATEGORY_URLS.items():
                self.logger.info(f"Processing category: {category_name}")
                
                # Extract topic links from category page
                topic_links = self._extract_topic_links(category_url)
                
                # Process each topic
                for title, topic_url in topic_links:
                    topic_data = self._scrape_topic_details(title, topic_url, category_url)
                    self.topics_data.append(topic_data)
                
                self.logger.info(f"Completed category: {category_name}")
            
            return self.topics_data
            
        finally:
            if self.driver:
                self.driver.quit()
    
    def save_to_json(self, filename: Optional[str] = None) -> str:
        """Save scraped data to JSON file.
        
        Args:
            filename: Optional filename, defaults to OUTPUT_FILE
            
        Returns:
            Path to the saved file
        """
        if filename is None:
            filename = OUTPUT_FILE
        
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.topics_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"Data saved to {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error saving data to JSON: {e}")
            raise


def main():
    """Main function to run the topic scraper."""
    scraper = TopicScraper()
    
    try:
        print("Starting topic scraping...")
        topics = scraper.scrape_all_topics()
        
        print(f"Scraped {len(topics)} topics successfully")
        
        output_path = scraper.save_to_json()
        print(f"Data saved to: {output_path}")
        
    except Exception as e:
        print(f"Error during scraping: {e}")
        logging.error(f"Application error: {e}")


if __name__ == "__main__":
    main()
