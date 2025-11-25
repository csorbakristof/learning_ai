#!/usr/bin/env python3
"""
Standalone script to run DLFUSION feature
This version directly incorporates the DLFUSION logic to avoid dependency issues
"""

import sys
from pathlib import Path
import logging
import json
import pandas as pd
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

# Set up basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Course codes that should be taken into account according to specification
ALLOWED_COURSE_CODES = {
    'BMEVIAUAL01', 'BMEVIAUAL03', 'BMEVIAUAL04', 'BMEVIAUAL05', 
    'BMEVIAUAT00', 'BMEVIAUAT01', 'BMEVIAUAT02', 'BMEVIAUA019', 
    'BMEVIAUML10', 'BMEVIAUML11', 'BMEVIAUML12', 'BMEVIAUML13',
    'BMEVIAUMT00', 'BMEVIAUMT01', 'BMEVIAUMT03', 'BMEVIAUMT10', 
    'BMEVIAUMT11', 'BMEVIAUMT12', 'BMEVIAUMT13',
    'BMEVIAUM026', 'BMEVIAUM027', 'BMEVIAUM039'
}

def main():
    """Run DLFUSION feature"""
    print("=" * 60)
    print("DLFUSION - Data Fusion Feature")
    print("=" * 60)
    
    # Create processor
    processor = DataFusionProcessor()
    
    # Process fusion
    print("\n🔄 Processing data fusion...")
    success = processor.process_fusion()
    
    if success:
        print("\n✅ DLFUSION completed successfully!")
        
        # Get and display summary
        summary = processor.get_fusion_summary()
        print("\n📊 Fusion Results:")
        print(f"   • Total students: {summary['total_students']}")
        print(f"   • Students with topics: {summary['students_with_topics']}")
        print(f"   • Students with enrollments: {summary['students_with_enrollments']}")
        print(f"   • Students with both: {summary['students_with_both']}")
        print(f"   • Unique courses: {summary['unique_courses']}")
        
        if summary['topic_categories']:
            print(f"   • Topic categories: {', '.join(summary['topic_categories'])}")
        
        print(f"\n📁 Output saved to: data/fused_student_data.json")
        
        # Show data source info
        print(f"\n📥 Data Sources:")
        print(f"   • DLXLS records: {summary['dlxls_records']}")
        print(f"   • DLNEP records: {summary['dlnep_records']}")
        
        return 0
    else:
        print("\n❌ DLFUSION failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
