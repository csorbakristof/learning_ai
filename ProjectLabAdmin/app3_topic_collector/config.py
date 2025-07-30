"""
Configuration module for Topic Collector application.
Contains URLs, settings, and constants used throughout the application.
"""

import os
from typing import Dict, List

# Category URLs to scrape
CATEGORY_URLS = {
    "BSc_Info_Onlab": "https://www.aut.bme.hu/Education/BScInfo/Onlab",
    "BSc_Info_Szakdolgozat": "https://www.aut.bme.hu/Education/BScInfo/Szakdolgozat",
    "BSc_Villany_Onlab": "https://www.aut.bme.hu/Education/BScVillany/Onlab",
    "BSc_Villany_Szakdolgozat": "https://www.aut.bme.hu/Education/BScVillany/Szakdolgozat",
    "BSc_Mechatronika_Szakdolgozat": "https://www.aut.bme.hu/Education/BScMechatronika/Szakdolgozat",
    "MSc_Info_Onlab": "https://www.aut.bme.hu/Education/MScInfo/Onlab",
    "MSc_Info_Diploma": "https://www.aut.bme.hu/Education/MScInfo/Diploma",
    "MSc_Villany_Onlab": "https://www.aut.bme.hu/Education/MScVillany/Onlab",
    "MSc_Villany_Diploma": "https://www.aut.bme.hu/Education/MScVillany/Diploma",
    "MSc_Mechatronika_Onlab": "https://www.aut.bme.hu/Education/MScMechatronika/Onlab",
    "MSc_Mechatronika_Diploma": "https://www.aut.bme.hu/Education/MScMechatronika/Diploma"
}

# Selenium configuration
SELENIUM_CONFIG = {
    "implicit_wait": 10,
    "page_load_timeout": 30,
    "headless": False,  # Set to True for headless mode
    "window_size": (1920, 1080)
}

# File paths
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT_FILE = "topics.json"

# Scraping constants
TOPICS_HEADING = "Kiírt témák"
EXTERNAL_PARTNER_TEXT = "Külső partner:"
STUDENT_LIMIT_TEXT = "Maximális létszám:"
ADVISORS_SECTION_TEXT = "Konzulensek"

# HTML element IDs
COURSE_GROUP_DROPDOWN_ID = "ddlCourseGroup"
COURSE_DROPDOWN_ID = "ddlCourse"

# Wait times (in seconds)
DROPDOWN_WAIT_TIME = 3
PAGE_LOAD_WAIT_TIME = 2

# Course code prefix
COURSE_CODE_PREFIX = "BME"

# Default values
DEFAULT_STUDENT_LIMIT = None
DEFAULT_EXTERNAL_PARTNER = None
