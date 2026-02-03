"""
Main script to orchestrate the download and extraction process.
"""
import os
import sys
from downloader import download_semester_files
from extractor import merge_all_files


def main():
    """Main function to run the complete pipeline."""
    print("="*60)
    print("University Course Statistics Downloader and Merger")
    print("="*60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    downloads_dir = os.path.join(script_dir, "downloads")
    output_dir = os.path.join(script_dir, "output")
    
    try:
        # Step 1: Download files
        print("\n[Step 1/2] Downloading Excel files from website...")
        print("-"*60)
        base_url = "https://www.aut.bme.hu/Tasks/TaskGradeExport.aspx?SemesterId={semester_id}"
        login_url = "https://www.aut.bme.hu/Tasks/TaskManagement.aspx"
        num_downloaded = download_semester_files(base_url, login_url=login_url)
        
        # Step 2: Extract and merge data
        print("\n[Step 2/2] Extracting and merging data...")
        print("-"*60)
        output_file = merge_all_files(downloads_dir, output_dir)
        
        # Success
        print("\n" + "="*60)
        print("✓ Process completed successfully!")
        print(f"✓ Output file: {output_file}")
        print("="*60)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n✗ Process interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n\n✗ Error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
