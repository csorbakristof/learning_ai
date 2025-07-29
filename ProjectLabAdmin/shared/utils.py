"""
Shared utilities for web scraping and Selenium operations
"""
import time
import logging
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
from .config import SELENIUM_TIMEOUT, REQUEST_TIMEOUT, USER_AGENT, LOGIN_WAIT_MESSAGE

logger = logging.getLogger(__name__)


class WebScrapingUtils:
    """Utilities for web scraping with requests and BeautifulSoup"""
    
    @staticmethod
    def get_page_content(url: str, headers: Optional[Dict[str, str]] = None) -> Optional[BeautifulSoup]:
        """
        Fetch page content using requests and return BeautifulSoup object
        
        Args:
            url: URL to fetch
            headers: Optional custom headers
            
        Returns:
            BeautifulSoup object or None if failed
        """
        if headers is None:
            headers = {"User-Agent": USER_AGENT}
        
        try:
            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    @staticmethod
    def extract_text_by_selector(soup: BeautifulSoup, selector: str) -> list:
        """
        Extract text from elements matching CSS selector
        
        Args:
            soup: BeautifulSoup object
            selector: CSS selector
            
        Returns:
            List of text content from matching elements
        """
        elements = soup.select(selector)
        return [elem.get_text(strip=True) for elem in elements]


class SeleniumUtils:
    """Utilities for Selenium web automation"""
    
    def __init__(self, headless: bool = False):
        """
        Initialize Selenium utilities
        
        Args:
            headless: Whether to run browser in headless mode
        """
        self.driver: Optional[webdriver.Chrome] = None
        self.headless = headless
    
    def setup_driver(self) -> webdriver.Chrome:
        """
        Set up Chrome WebDriver with appropriate options
        
        Returns:
            Chrome WebDriver instance
        """
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"--user-agent={USER_AGENT}")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(SELENIUM_TIMEOUT)
        
        logger.info("Chrome WebDriver initialized successfully")
        return self.driver
    
    def wait_for_user_login(self) -> bool:
        """
        Wait for user to complete login process
        
        Returns:
            True if user indicates login is complete
        """
        try:
            input(LOGIN_WAIT_MESSAGE)
            logger.info("User indicated login is complete")
            return True
        except KeyboardInterrupt:
            logger.info("Login process interrupted by user")
            return False
    
    def wait_for_element(self, by: By, value: str, timeout: int = SELENIUM_TIMEOUT) -> Optional[Any]:
        """
        Wait for element to be present and return it
        
        Args:
            by: Selenium By locator type
            value: Locator value
            timeout: Maximum wait time in seconds
            
        Returns:
            WebElement if found, None otherwise
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"Element not found: {by}={value}")
            return None
    
    def safe_click(self, by: By, value: str, timeout: int = SELENIUM_TIMEOUT) -> bool:
        """
        Safely click an element with wait
        
        Args:
            by: Selenium By locator type
            value: Locator value
            timeout: Maximum wait time in seconds
            
        Returns:
            True if clicked successfully, False otherwise
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            logger.info(f"Successfully clicked element: {by}={value}")
            return True
        except TimeoutException:
            logger.error(f"Element not clickable: {by}={value}")
            return False
        except WebDriverException as e:
            logger.error(f"Error clicking element {by}={value}: {e}")
            return False
    
    def safe_send_keys(self, by: By, value: str, text: str, timeout: int = SELENIUM_TIMEOUT) -> bool:
        """
        Safely send keys to an element with wait
        
        Args:
            by: Selenium By locator type
            value: Locator value
            text: Text to send
            timeout: Maximum wait time in seconds
            
        Returns:
            True if successful, False otherwise
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            element.clear()
            element.send_keys(text)
            logger.info(f"Successfully sent keys to element: {by}={value}")
            return True
        except TimeoutException:
            logger.error(f"Element not found for sending keys: {by}={value}")
            return False
        except WebDriverException as e:
            logger.error(f"Error sending keys to element {by}={value}: {e}")
            return False
    
    def close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed successfully")


def setup_logging(name: str) -> logging.Logger:
    """
    Set up colored logging for the application
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger
    """
    import colorlog
    from .config import LOG_LEVEL, LOG_FORMAT
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    if not logger.handlers:
        handler = colorlog.StreamHandler()
        formatter = colorlog.ColoredFormatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger
