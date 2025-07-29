#!/usr/bin/env python3
"""
Quick script to examine the data files from DLXLS and DLNEP
"""

import pandas as pd
import os
from pathlib import Path

def examine_dlxls_data():
    """Examine DLXLS data structure"""
    print("=== DLXLS Data (BME Topic Data) ===")
    dlxls_file = Path("data/bme_topic_data.xlsx")
    if dlxls_file.exists():
        df = pd.read_excel(dlxls_file)
        print(f"Rows: {len(df)}")
        print(f"Columns: {df.columns.tolist()}")
        print("Sample data:")
        print(df.head(2))
        print("\n")
    else:
        print("DLXLS file not found")

def examine_dlnep_data():
    """Examine DLNEP data structure"""
    print("=== DLNEP Data (Neptun Downloads) ===")
    neptun_folder = Path("data/neptun_downloads")
    if neptun_folder.exists():
        files = list(neptun_folder.glob("*.xlsx"))
        print(f"Found {len(files)} files:")
        
        for file in files[:3]:  # Check first 3 files
            try:
                df = pd.read_excel(file)
                course_code = extract_course_code_from_filename(file.name)
                print(f"\nFile: {file.name}")
                print(f"Course code: {course_code}")
                print(f"Rows: {len(df)}")
                print(f"Columns: {df.columns.tolist()}")
                if len(df) > 0:
                    print("Sample data:")
                    print(df.head(2))
                    break
            except Exception as e:
                print(f"Error reading {file.name}: {e}")
    else:
        print("DLNEP folder not found")

def extract_course_code_from_filename(filename):
    """Extract course code from filename"""
    import re
    # Pattern to match BMEVI followed by letters/numbers
    match = re.search(r'(BMEVI[A-Z]+\d+)', filename.upper())
    return match.group(1) if match else "UNKNOWN"

if __name__ == "__main__":
    examine_dlxls_data()
    examine_dlnep_data()
