#!/usr/bin/env python3
"""
Test script for DLXLS - BME Topic Data Collection
This script tests the BME portal integration separately from the main application.
"""

import sys
from pathlib import Path

# Add shared module to path
sys.path.append(str(Path(__file__).parent.parent))

from dlxls_collector import BMETopicDataCollector
from shared import setup_logging


def test_dlxls_feature():
    """Test the DLXLS feature independently"""
    logger = setup_logging(__name__)
    
    logger.info("=" * 60)
    logger.info("Testing DLXLS - BME Topic Data Collection")
    logger.info("=" * 60)
    
    try:
        # Create collector instance
        collector = BMETopicDataCollector()
        
        # Test the collection process
        logger.info("Starting BME topic data collection...")
        data = collector.collect_topic_data()
        
        if data:
            logger.info(f"✅ Successfully collected {len(data)} student records")
            
            # Display sample data
            logger.info("\nSample collected data:")
            for i, record in enumerate(data[:3]):
                logger.info(f"  Record {i+1}: {record}")
            
            # Save the data
            if collector.save_processed_data():
                logger.info("✅ Data saved successfully")
            else:
                logger.warning("⚠️ Failed to save data")
                
            return True
        else:
            logger.error("❌ No data was collected")
            return False
            
    except KeyboardInterrupt:
        logger.info("Test interrupted by user")
        return False
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        return False


def main():
    """Main function"""
    success = test_dlxls_feature()
    
    if success:
        print("\n🎉 DLXLS feature test completed successfully!")
    else:
        print("\n❌ DLXLS feature test failed. Check the logs above.")


if __name__ == "__main__":
    main()
