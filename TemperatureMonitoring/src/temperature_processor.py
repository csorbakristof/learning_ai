"""
Temperature Monitoring Data Processor

A Python application for processing temperature sensor data from CSV files
packed in ZIP archives, generating visualizations and Excel reports.
"""

import zipfile
import csv
import pandas as pd
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TemperatureDataProcessor:
    """Main class for processing temperature monitoring data."""
    
    def __init__(self):
        self.data: List[Dict] = []
        
    def extract_zip_files(self, zip_path: str, extract_to: str = "data/extracted") -> List[str]:
        """
        Extract CSV files from a ZIP archive.
        
        Args:
            zip_path: Path to the ZIP file
            extract_to: Directory to extract files to
            
        Returns:
            List of extracted CSV file paths
        """
        extracted_files = []
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    if file_info.filename.endswith('.csv'):
                        zip_ref.extract(file_info, extract_to)
                        extracted_files.append(Path(extract_to) / file_info.filename)
                        logger.info(f"Extracted: {file_info.filename}")
                        
        except zipfile.BadZipFile:
            logger.error(f"Invalid ZIP file: {zip_path}")
            raise
        except Exception as e:
            logger.error(f"Error extracting ZIP file: {e}")
            raise
            
        return extracted_files
    
    def parse_csv_file(self, csv_path: str) -> Dict:
        """
        Parse a single CSV file according to the specified format.
        
        Args:
            csv_path: Path to the CSV file
            
        Returns:
            Dictionary containing device name and data records
        """
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            if len(lines) < 3:
                raise ValueError(f"CSV file {csv_path} has insufficient data")
                
            # First line: device name
            device_name = lines[0].strip()
            
            # Second line: headers (skip this)
            headers = lines[1].strip()
            
            # Parse data rows
            data_records = []
            invalid_lines = 0
            
            for line_num, line in enumerate(lines[2:], start=3):
                parts = line.strip().split(';')
                if len(parts) >= 4:
                    try:
                        # Convert CSV timestamp to datetime (Unix timestamp format)
                        csv_timestamp = float(parts[0])
                        timestamp = self._csv_timestamp_to_datetime(csv_timestamp)
                        
                        record = {
                            'timestamp': timestamp,
                            'temperature': float(parts[1]),
                            'humidity': float(parts[2]),
                            'battery_mv': int(parts[3])
                        }
                        data_records.append(record)
                        
                    except (ValueError, IndexError, OverflowError) as e:
                        invalid_lines += 1
                        if invalid_lines <= 10:  # Only log first 10 invalid lines to avoid spam
                            logger.warning(f"Skipping invalid line {line_num} in {csv_path}: {e}")
                        elif invalid_lines == 11:
                            logger.warning(f"More invalid lines found in {csv_path}, suppressing further warnings for this file...")
            
            if invalid_lines > 0:
                logger.info(f"Skipped {invalid_lines} invalid lines in {csv_path}, processed {len(data_records)} valid records")
                        
            return {
                'device_name': device_name,
                'data': data_records,
                'file_path': csv_path
            }
            
        except Exception as e:
            logger.error(f"Error parsing CSV file {csv_path}: {e}")
            raise
    
    def _csv_timestamp_to_datetime(self, csv_timestamp: float) -> datetime:
        """
        Convert CSV timestamp to Python datetime.
        Based on C# method: timestamps are seconds since Unix epoch (1970-01-01 UTC).
        """
        try:
            # Convert to integer seconds (handle float input)
            timestamp_seconds = int(csv_timestamp)
            
            # Check for reasonable timestamp range 
            # Unix epoch: 1970-01-01, reasonable range: 1970 to 2100
            min_timestamp = 0  # 1970-01-01
            max_timestamp = 4102444800  # ~2100-01-01
            
            if timestamp_seconds < min_timestamp or timestamp_seconds > max_timestamp:
                raise ValueError(f"Timestamp {timestamp_seconds} is out of reasonable range (1970-2100)")
            
            # Create datetime from Unix timestamp (UTC)
            return datetime.fromtimestamp(timestamp_seconds, tz=None)
            
        except (ValueError, OverflowError, OSError) as e:
            raise ValueError(f"Invalid timestamp {csv_timestamp}: {e}")
    
    def process_zip_file(self, zip_path: str) -> List[Dict]:
        """
        Process a complete ZIP file containing CSV files.
        
        Args:
            zip_path: Path to the ZIP file
            
        Returns:
            List of processed data dictionaries
        """
        logger.info(f"Processing ZIP file: {zip_path}")
        
        # Extract CSV files
        extracted_files = self.extract_zip_files(zip_path)
        
        # Process each CSV file
        processed_data = []
        for csv_file in extracted_files:
            try:
                data = self.parse_csv_file(str(csv_file))
                processed_data.append(data)
                logger.info(f"Processed {len(data['data'])} records from {data['device_name']}")
            except Exception as e:
                logger.error(f"Failed to process {csv_file}: {e}")
                
        return processed_data


def main():
    """Main entry point for the application."""
    processor = TemperatureDataProcessor()
    
    # Example usage
    zip_path = "data/temperature_data.zip"  # Update with actual path
    
    try:
        processed_data = processor.process_zip_file(zip_path)
        print(f"Successfully processed {len(processed_data)} devices")
        
        for device_data in processed_data:
            print(f"Device: {device_data['device_name']} - {len(device_data['data'])} records")
            
    except FileNotFoundError:
        print(f"ZIP file not found: {zip_path}")
        print("Please place your ZIP file in the data directory and update the path.")
    except Exception as e:
        print(f"Error processing data: {e}")


if __name__ == "__main__":
    main()
