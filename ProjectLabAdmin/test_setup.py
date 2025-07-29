#!/usr/bin/env python3
"""
Test script to verify the environment setup
"""
import sys
from pathlib import Path

# Add shared module to path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from shared import WebScrapingUtils, SeleniumUtils, ExcelHandler, setup_logging
        print("✓ Shared modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import shared modules: {e}")
        return False
    
    try:
        import selenium
        print("✓ Selenium imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import selenium: {e}")
        return False
    
    try:
        import requests
        import bs4
        print("✓ Web scraping modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import web scraping modules: {e}")
        return False
    
    try:
        import openpyxl
        import pandas
        print("✓ Excel handling modules imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Excel modules: {e}")
        return False
    
    return True

def test_excel_operations():
    """Test Excel file operations"""
    print("\nTesting Excel operations...")
    
    try:
        from shared import ExcelHandler
        
        # Create test data
        test_data = [
            {'name': 'John Doe', 'email': 'john@example.com', 'age': 30},
            {'name': 'Jane Smith', 'email': 'jane@example.com', 'age': 25}
        ]
        
        # Test Excel handler
        excel_handler = ExcelHandler(Path(__file__).parent / "data" / "test.xlsx")
        
        # Create Excel file
        if excel_handler.create_excel_file(test_data, "TestSheet"):
            print("✓ Excel file creation successful")
        else:
            print("✗ Excel file creation failed")
            return False
        
        # Read Excel file
        read_data = excel_handler.read_excel_data("TestSheet")
        if read_data and len(read_data) == 2:
            print("✓ Excel file reading successful")
        else:
            print("✗ Excel file reading failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Excel operations test failed: {e}")
        return False

def test_web_scraping():
    """Test web scraping functionality"""
    print("\nTesting web scraping...")
    
    try:
        from shared import WebScrapingUtils
        
        utils = WebScrapingUtils()
        
        # Test with a simple webpage
        soup = utils.get_page_content("https://httpbin.org/html")
        if soup:
            print("✓ Web scraping with requests successful")
            
            # Test text extraction
            titles = utils.extract_text_by_selector(soup, "h1")
            if titles:
                print(f"✓ Text extraction successful: found {len(titles)} titles")
            else:
                print("! No titles found (may be normal)")
        else:
            print("✗ Web scraping failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Web scraping test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("ProjectLabAdmin Environment Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_excel_operations,
        test_web_scraping
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! Environment is ready.")
    else:
        print("✗ Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()
