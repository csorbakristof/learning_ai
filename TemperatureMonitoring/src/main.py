"""
Main application for Temperature Monitoring Data Processor
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict
import logging

# Add src directory to path for imports
sys.path.append(str(Path(__file__).parent))

from temperature_processor import TemperatureDataProcessor
from visualizer import TemperatureVisualizer
from excel_exporter import ExcelExporter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('temperature_monitoring.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class TemperatureMonitoringApp:
    """Main application class for temperature monitoring."""
    
    def __init__(self):
        self.processor = TemperatureDataProcessor()
        self.visualizer = TemperatureVisualizer()
        self.exporter = ExcelExporter()
    
    def process_zip_file(self, zip_path: str, generate_reports: bool = True) -> List[Dict]:
        """
        Process a ZIP file and optionally generate reports.
        
        Args:
            zip_path: Path to the ZIP file
            generate_reports: Whether to generate visualizations and Excel reports
            
        Returns:
            List of processed device data
        """
        logger.info(f"Starting processing of {zip_path}")
        
        try:
            # Process the ZIP file
            device_data_list = self.processor.process_zip_file(zip_path)
            
            if not device_data_list:
                logger.warning("No data was processed from the ZIP file")
                return device_data_list
            
            logger.info(f"Successfully processed {len(device_data_list)} devices")
            
            if generate_reports:
                self._generate_all_reports(device_data_list)
            
            return device_data_list
            
        except Exception as e:
            logger.error(f"Error processing ZIP file: {e}")
            raise
    
    def _generate_all_reports(self, device_data_list: List[Dict]):
        """Generate all reports for the processed data."""
        logger.info("Generating reports...")
        
        # Generate individual device reports
        for device_data in device_data_list:
            try:
                # Create timeline visualization
                self.visualizer.create_temperature_timeline(device_data)
                
                # Export to Excel
                self.exporter.export_device_data(device_data)
                
            except Exception as e:
                logger.error(f"Error generating reports for {device_data['device_name']}: {e}")
        
        # Generate multi-device reports if multiple devices
        if len(device_data_list) > 1:
            try:
                # Multi-device comparisons
                self.visualizer.create_multi_device_comparison(device_data_list, 'temperature')
                self.visualizer.create_multi_device_comparison(device_data_list, 'humidity')
                self.visualizer.create_multi_device_comparison(device_data_list, 'battery_mv')
                
                # Statistics heatmap
                self.visualizer.create_statistics_heatmap(device_data_list)
                
                # Combined Excel report
                self.exporter.export_all_devices(device_data_list)
                
            except Exception as e:
                logger.error(f"Error generating multi-device reports: {e}")
        
        logger.info("Report generation completed")
    
    def print_summary(self, device_data_list: List[Dict]):
        """Print a summary of the processed data."""
        if not device_data_list:
            print("No data was processed.")
            return
        
        print("\n" + "="*60)
        print("TEMPERATURE MONITORING DATA SUMMARY")
        print("="*60)
        
        total_records = 0
        for device_data in device_data_list:
            device_name = device_data['device_name']
            data = device_data['data']
            record_count = len(data)
            total_records += record_count
            
            if data:
                import pandas as pd
                df = pd.DataFrame(data)
                
                print(f"\nDevice: {device_name}")
                print(f"  Records: {record_count}")
                print(f"  Time Range: {df['timestamp'].min()} to {df['timestamp'].max()}")
                print(f"  Temperature: {df['temperature'].min():.1f}°C to {df['temperature'].max():.1f}°C (avg: {df['temperature'].mean():.1f}°C)")
                print(f"  Humidity: {df['humidity'].min():.1f}% to {df['humidity'].max():.1f}% (avg: {df['humidity'].mean():.1f}%)")
                print(f"  Battery: {df['battery_mv'].min()}mV to {df['battery_mv'].max()}mV (avg: {df['battery_mv'].mean():.0f}mV)")
        
        print(f"\nTotal devices: {len(device_data_list)}")
        print(f"Total records: {total_records}")
        print("\nReports generated in the 'output' directory.")
        print("="*60)


def main():
    """Main entry point with command-line interface."""
    parser = argparse.ArgumentParser(description='Temperature Monitoring Data Processor')
    parser.add_argument('zip_file', help='Path to the ZIP file containing CSV data')
    parser.add_argument('--no-reports', action='store_true', 
                       help='Skip generating visualizations and Excel reports')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help='Set logging level')
    
    args = parser.parse_args()
    
    # Set logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    # Check if ZIP file exists
    zip_path = Path(args.zip_file)
    if not zip_path.exists():
        print(f"Error: ZIP file not found: {zip_path}")
        return 1
    
    # Process the data
    app = TemperatureMonitoringApp()
    
    try:
        device_data_list = app.process_zip_file(
            str(zip_path), 
            generate_reports=not args.no_reports
        )
        
        # Print summary
        app.print_summary(device_data_list)
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        logger.error(f"Application error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
