"""
Example configuration for the Topic Collector application.
Copy this file to config.py and modify as needed.
"""

import os
from typing import Dict, List

# Category URLs to scrape - modify these if new categories are added
EXAMPLE_CATEGORY_URLS = {
    # BSc Level
    "BSc_Info_Onlab": "https://www.aut.bme.hu/Education/BScInfo/Onlab",
    "BSc_Info_Szakdolgozat": "https://www.aut.bme.hu/Education/BScInfo/Szakdolgozat",
    "BSc_Villany_Onlab": "https://www.aut.bme.hu/Education/BScVillany/Onlab",
    "BSc_Villany_Szakdolgozat": "https://www.aut.bme.hu/Education/BScVillany/Szakdolgozat",
    "BSc_Mechatronika_Szakdolgozat": "https://www.aut.bme.hu/Education/BScMechatronika/Szakdolgozat",
    
    # MSc Level  
    "MSc_Info_Onlab": "https://www.aut.bme.hu/Education/MScInfo/Onlab",
    "MSc_Info_Diploma": "https://www.aut.bme.hu/Education/MScInfo/Diploma",
    "MSc_Villany_Onlab": "https://www.aut.bme.hu/Education/MScVillany/Onlab",
    "MSc_Villany_Diploma": "https://www.aut.bme.hu/Education/MScVillany/Diploma",
    "MSc_Mechatronika_Onlab": "https://www.aut.bme.hu/Education/MScMechatronika/Onlab",
    "MSc_Mechatronika_Diploma": "https://www.aut.bme.hu/Education/MScMechatronika/Diploma"
}

# Selenium configuration - adjust based on your system and preferences
EXAMPLE_SELENIUM_CONFIG = {
    "implicit_wait": 10,           # Seconds to wait for elements to appear
    "page_load_timeout": 30,       # Seconds to wait for page loads
    "headless": False,             # Set to True to run without browser window
    "window_size": (1920, 1080)   # Browser window size
}

# File paths - adjust if you want different output locations
EXAMPLE_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
EXAMPLE_OUTPUT_FILE = "topics.json"

# Scraping constants - only modify if the website structure changes
EXAMPLE_TOPICS_HEADING = "Kiírt témák"
EXAMPLE_EXTERNAL_PARTNER_TEXT = "Külső partner:"
EXAMPLE_STUDENT_LIMIT_TEXT = "Maximális létszám:"
EXAMPLE_ADVISORS_SECTION_TEXT = "Konzulensek"

# HTML element IDs - only modify if the website structure changes
EXAMPLE_COURSE_GROUP_DROPDOWN_ID = "ddlCourseGroup" 
EXAMPLE_COURSE_DROPDOWN_ID = "ddlCourse"

# Wait times (in seconds) - increase if website is slow to respond
EXAMPLE_DROPDOWN_WAIT_TIME = 3      # Wait after dropdown selection
EXAMPLE_PAGE_LOAD_WAIT_TIME = 2     # Wait after page navigation

# Course code prefix - modify if course codes change format
EXAMPLE_COURSE_CODE_PREFIX = "BME"

# Default values for missing data
EXAMPLE_DEFAULT_STUDENT_LIMIT = None
EXAMPLE_DEFAULT_EXTERNAL_PARTNER = None

# Advanced settings
EXAMPLE_ADVANCED_CONFIG = {
    # Retry settings
    "max_retries": 3,
    "retry_delay": 5,
    
    # Request settings
    "request_timeout": 30,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    
    # Browser options
    "browser_options": [
        "--disable-blink-features=AutomationControlled",
        "--disable-extensions",
        "--no-first-run",
        "--disable-default-apps"
    ],
    
    # Logging settings
    "log_level": "INFO",
    "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

# Example usage:
# To use these example settings, copy them to your config.py file:
#
# CATEGORY_URLS = EXAMPLE_CATEGORY_URLS
# SELENIUM_CONFIG = EXAMPLE_SELENIUM_CONFIG
# OUTPUT_DIR = EXAMPLE_OUTPUT_DIR
# etc.
