# Configuration settings for both applications
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SHARED_DIR = PROJECT_ROOT / "shared"

# Excel file settings
EXCEL_OUTPUT_FILE = DATA_DIR / "scraped_data.xlsx"
DEFAULT_SHEET_NAME = "ScrapedData"

# Selenium settings
SELENIUM_TIMEOUT = 30
WEBDRIVER_IMPLICIT_WAIT = 10
LOGIN_WAIT_MESSAGE = "Please complete the login process in the browser, then press Enter to continue..."

# Web scraping settings
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2

# User agent for requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s"
