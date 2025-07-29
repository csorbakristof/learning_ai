#!/usr/bin/env python3
"""
Comprehensive integration test for DLFUSION + MKXLSX workflow
Tests the complete workflow from fused data to Excel table creation
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from main import DataCollector


def test_complete_workflow():
    """Test the complete DLFUSION + MKXLSX workflow"""
    print("🚀 Testing Complete Data Collection Workflow")
    print("=" * 60)
    print("This test runs DLFUSION + MKXLSX using existing data files.")
    print()
    
    # Check prerequisites
    print("🔍 Checking Prerequisites...")
    print("-" * 30)
    
    # Check DLXLS data
    dlxls_file = Path("../data/bme_topic_data.xlsx")
    if dlxls_file.exists():
        print("✅ DLXLS data found: ../data/bme_topic_data.xlsx")
    else:
        print("❌ DLXLS data not found: ../data/bme_topic_data.xlsx")
        return False
    
    # Check DLNEP data
    dlnep_folder = Path("../data/neptun_downloads")
    if dlnep_folder.exists():
        excel_files = list(dlnep_folder.glob("*.xlsx"))
        if excel_files:
            print(f"✅ DLNEP data found: {len(excel_files)} files in ../data/neptun_downloads/")
        else:
            print("❌ No DLNEP Excel files found in ../data/neptun_downloads/")
            return False
    else:
        print("❌ DLNEP folder not found: ../data/neptun_downloads/")
        return False
    
    print()
    
    # Create data collector
    collector = DataCollector()
    
    # Test DLFUSION
    print("🧪 Testing DLFUSION...")
    print("-" * 30)
    fusion_result = collector.collect_fused_data()
    
    if fusion_result.get('success'):
        print("✅ DLFUSION completed successfully!")
        summary = fusion_result['summary']
        print(f"   • Total students: {summary['total_students']}")
        print(f"   • Students with topics: {summary['students_with_topics']}")
        print(f"   • Students with enrollments: {summary['students_with_enrollments']}")
        print(f"   • Students with both: {summary['students_with_both']}")
        print(f"   • Unique courses: {summary['unique_courses']}")
        if summary['topic_categories']:
            print(f"   • Topic categories: {list(summary['topic_categories'].keys())}")
    else:
        print("❌ DLFUSION failed!")
        return False
    
    print()
    
    # Test MKXLSX
    print("🧪 Testing MKXLSX...")
    print("-" * 30)
    excel_result = collector.create_session_planning_excel()
    
    if excel_result.get('success'):
        print("✅ MKXLSX completed successfully!")
        summary = excel_result['summary']
        print(f"   • Planning slots available: {summary['planner_dimensions']['total_slots']}")
        print(f"   • Required sessions: {summary['required_sessions']}")
        print(f"   • Time slots: {summary['planner_dimensions']['time_slots']}")
        print(f"   • Weekdays: {summary['planner_dimensions']['weekdays']}")
        print(f"   • Rooms: {summary['planner_dimensions']['rooms']}")
        print(f"   • Session types supported: {len(summary['session_types_supported'])}")
        
        # Check if Excel file was created
        excel_file = Path("../data/session_planner.xlsx")
        if excel_file.exists():
            print(f"   • Excel file created: {excel_file.name} ({excel_file.stat().st_size} bytes)")
        else:
            print("   ❌ Excel file not found!")
            return False
    else:
        print("❌ MKXLSX failed!")
        return False
    
    print()
    print("=" * 60)
    print("🎉 Complete workflow test passed!")
    print()
    print("📁 Generated Files:")
    print("   • data/fused_student_data.json (DLFUSION output)")
    print("   • data/session_planner.xlsx (MKXLSX output)")
    print()
    print("📊 Excel File Contents:")
    print("   • Upper section: Session planner table (15 columns x 4 rows)")
    print("     - Columns: Monday-Friday x QB203,QBF14,QBF15")
    print("     - Rows: 8:00-10:00, 10:00-12:00, 12:00-14:00, 14:00-16:00")
    print("   • Lower section: Statistics with Excel formulas")
    print("     - Topic category counts and required sessions")
    print("     - Session type counters (automatically updated)")
    print()
    print("🎯 Next Steps:")
    print("   1. Open data/session_planner.xlsx in Excel")
    print("   2. Fill in session types (SW, HW, ENG, GEN, ONLINE, SPARE, NONE)")
    print("   3. Use the Web Automator app with the filled Excel file")
    print()
    return True


def main():
    """Main test execution"""
    success = test_complete_workflow()
    
    if not success:
        print("❌ Workflow test failed!")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
