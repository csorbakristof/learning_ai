"""
Download module for fetching course statistics Excel files from the university website.
"""
import os
import time
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def clean_downloads_folder(downloads_dir):
    """Clean the downloads folder before starting."""
    if os.path.exists(downloads_dir):
        shutil.rmtree(downloads_dir)
    os.makedirs(downloads_dir, exist_ok=True)
    print(f"✓ Cleaned downloads folder: {downloads_dir}")


def setup_chrome_driver(downloads_dir):
    """Setup Chrome driver with download preferences."""
    chrome_options = Options()
    
    # Set download directory
    abs_downloads_dir = os.path.abspath(downloads_dir)
    prefs = {
        "download.default_directory": abs_downloads_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Initialize driver - let webdriver_manager handle the driver path
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception:
        # If direct Chrome fails, try with explicit service
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver


def wait_for_user_login(driver, initial_url):
    """Navigate to the URL and wait for user to login."""
    driver.get(initial_url)
    print("\n" + "="*60)
    print("Please login to the website in the browser window.")
    print("After successful login, press ENTER to continue...")
    print("="*60 + "\n")
    input()
    print("✓ Login confirmed. Starting download process...\n")


def wait_for_download(downloads_dir, timeout=3):
    """Wait for a file to finish downloading."""
    start_time = time.time()
    download_started = False
    
    while time.time() - start_time < timeout:
        # Check if there are any .crdownload files (Chrome partial downloads)
        temp_files = [f for f in os.listdir(downloads_dir) if f.endswith('.crdownload')]
        
        if temp_files:
            # Download has started
            download_started = True
            time.sleep(0.5)
            continue
        
        if download_started:
            # Download was in progress and now temp file is gone, so it's complete
            time.sleep(1)  # Extra wait to ensure file is fully written
            return True
        
        # No temp file yet, keep waiting for download to start
        time.sleep(0.5)
    
    # Check one more time if file appeared without .crdownload (instant download)
    files_after = [f for f in os.listdir(downloads_dir) if os.path.isfile(os.path.join(downloads_dir, f))]
    if files_after:
        return True
    
    return False


def download_semester_files(base_url_template, start_id=1):
    """
    Download Excel files for all available semesters.
    
    Args:
        base_url_template: URL template with {semester_id} placeholder
        start_id: Starting semester ID (default: 1)
    
    Returns:
        Number of files successfully downloaded
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    downloads_dir = os.path.join(script_dir, "downloads")
    
    # Clean downloads folder
    clean_downloads_folder(downloads_dir)
    
    # Setup Chrome driver
    driver = setup_chrome_driver(downloads_dir)
    
    try:
        # Navigate to first URL and wait for login
        initial_url = base_url_template.format(semester_id=start_id)
        wait_for_user_login(driver, initial_url)
        
        # Start downloading files
        semester_id = start_id
        successful_downloads = 0
        consecutive_failures = 0
        
        while True:
            url = base_url_template.format(semester_id=semester_id)
            print(f"Downloading semester {semester_id}...", end=" ", flush=True)
            
            # Count files before download
            files_before = len([f for f in os.listdir(downloads_dir) if os.path.isfile(os.path.join(downloads_dir, f))])
            
            # Navigate to URL - this triggers the download directly
            driver.get(url)
            
            # Wait for download to complete
            if wait_for_download(downloads_dir, timeout=3):
                files_after = len([f for f in os.listdir(downloads_dir) if os.path.isfile(os.path.join(downloads_dir, f))])
                if files_after > files_before:
                    print("✓ Success")
                    successful_downloads += 1
                    consecutive_failures = 0
                else:
                    print("✗ No new file detected")
                    consecutive_failures += 1
                    if consecutive_failures >= 3:
                        print(f"\n✓ No more files to download after ID {semester_id - 1}")
                        break
            else:
                print("✗ Download timeout")
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    print(f"\n✓ No more files to download after ID {semester_id - 1}")
                    break
            
            semester_id += 1
        
        print(f"\n✓ Downloaded {successful_downloads} files total")
        return successful_downloads
        
    except Exception as e:
        print(f"\n✗ Error during download process: {e}")
        raise
    finally:
        driver.quit()
        print("✓ Browser closed")


if __name__ == "__main__":
    base_url = "https://www.aut.bme.hu/Tasks/TaskGradeExport.aspx?SemesterId={semester_id}"
    try:
        download_semester_files(base_url)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
