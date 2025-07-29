#!/usr/bin/env python3
"""
Test script for DLNEP - Neptun Student Data Collection
This script tests the Neptun system integration separately from the main application.
"""

import sys
from pathlib import Path

# Add shared module to path
sys.path.append(str(Path(__file__).parent.parent))

from dlnep_collector import NeptunStudentDataCollector
from shared import setup_logging


def test_dlnep_feature():
    """Test the DLNEP feature independently"""
    logger = setup_logging(__name__)
    
    logger.info("=" * 60)
    logger.info("Testing DLNEP - Neptun Student Data Collection")
    logger.info("=" * 60)
    
    try:
        # Create collector instance
        collector = NeptunStudentDataCollector()
        
        # Test the collection process
        logger.info("Starting Neptun student data collection...")
        results = collector.collect_all_course_data()
        
        if results:
            logger.info(f"✅ Successfully processed {len(results)} courses")
            
            # Display course results
            logger.info("\nCourse processing results:")
            for result in results:
                status = "✅" if result['download_successful'] else "❌"
                logger.info(f"  {status} {result['course_code']} - {result['course_name']}")
            
            # Process downloaded files
            student_data = collector.process_downloaded_files()
            
            if student_data:
                logger.info(f"✅ Successfully extracted {len(student_data)} student records")
                
                # Display sample data
                logger.info("\nSample student data:")
                for i, record in enumerate(student_data[:3]):
                    logger.info(f"  Student {i+1}: {record}")
                
                # Save the data
                if collector.save_processed_data():
                    logger.info("✅ Data saved successfully")
                else:
                    logger.warning("⚠️ Failed to save data")
                    
                return True
            else:
                logger.warning("⚠️ No student data was extracted from downloaded files")
                return False
        else:
            logger.error("❌ No courses were processed")
            return False
            
    except KeyboardInterrupt:
        logger.info("Test interrupted by user")
        return False
    except Exception as e:
        logger.error(f"❌ Test failed with error: {e}")
        return False


def main():
    """Main function"""
    success = test_dlnep_feature()
    
    if success:
        print("\n🎉 DLNEP feature test completed successfully!")
    else:
        print("\n❌ DLNEP feature test failed. Check the logs above.")


if __name__ == "__main__":
    main()
