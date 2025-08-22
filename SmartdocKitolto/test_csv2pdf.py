#!/usr/bin/env python3
"""
Test script for CSV2PDF functionality - tests CSV parsing without web automation
"""

import glob
from csv2pdf import CSV2PDFConverter

def test_csv_parsing():
    """Test CSV file parsing functionality"""
    print("=== CSV2PDF Test Mode ===")
    
    converter = CSV2PDFConverter()
    
    # Get CSV files
    csv_files = converter.get_csv_files()
    if not csv_files:
        print("No CSV files found for testing.")
        return False
    
    print(f"\nTesting CSV file parsing:")
    
    for csv_file in csv_files:
        print(f"\nTesting: {csv_file}")
        content = converter.read_csv_content(csv_file)
        
        if content:
            lines = content.split('\n')
            print(f"  ✓ File read successfully")
            print(f"  ✓ Lines found: {len(lines)}")
            print(f"  ✓ First line (header): {lines[0][:100]}..." if len(lines[0]) > 100 else f"  ✓ First line (header): {lines[0]}")
            if len(lines) > 1:
                print(f"  ✓ Second line (data): {lines[1][:100]}..." if len(lines[1]) > 100 else f"  ✓ Second line (data): {lines[1]}")
        else:
            print(f"  ✗ Failed to read file")
    
    return True

if __name__ == "__main__":
    test_csv_parsing()
