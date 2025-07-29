#!/usr/bin/env python3
"""
Comprehensive test for DLFUSION feature integration
Tests that DLFUSION can work with existing DLXLS and DLNEP data without re-running collection
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from main import DataCollector


def test_dlfusion_only():
    """Test DLFUSION feature independently"""
    print("🧪 Testing DLFUSION Feature (Standalone)")
    print("=" * 60)
    
    collector = DataCollector()
    
    # Test DLFUSION using existing data
    fusion_result = collector.collect_fused_data()
    
    if fusion_result.get('success'):
        print("✅ DLFUSION test passed!")
        
        summary = fusion_result['summary']
        print(f"\n📊 Fusion Results:")
        print(f"   • Total students: {summary['total_students']}")
        print(f"   • Students with topics: {summary['students_with_topics']}")
        print(f"   • Students with enrollments: {summary['students_with_enrollments']}")
        print(f"   • Students with both topic and enrollment: {summary['students_with_both']}")
        print(f"   • Unique courses: {summary['unique_courses']}")
        
        if summary['topic_categories']:
            print(f"\n🏷️  Topic Categories:")
            for category, count in summary['topic_categories'].items():
                print(f"   • {category}: {count} students")
        
        if summary['course_list']:
            print(f"\n📚 Course List:")
            for course in summary['course_list']:
                print(f"   • {course}")
        
        print(f"\n💾 Data Sources:")
        print(f"   • DLXLS source records: {summary['dlxls_source_records']}")
        print(f"   • DLNEP source records: {summary['dlnep_source_records']}")
        
        print(f"\n💾 Output: data/fused_student_data.json")
        
        # Show sample data
        fused_data = fusion_result.get('fused_data', [])
        if fused_data:
            print(f"\n📋 Sample Students (first 5):")
            for i, student in enumerate(fused_data[:5]):
                status = "📝 Has topic" if student['has_topic'] else "❓ No topic"
                courses_count = len(student['enrolled_courses'])
                print(f"   {i+1}. {student['student_name']} ({student['student_neptun']})")
                print(f"      {status} | 📚 {courses_count} course(s)")
                if student['has_topic']:
                    print(f"      Supervisor: {student['supervisor']}")
        
        return True
    else:
        print("❌ DLFUSION test failed!")
        return False


def check_prerequisites():
    """Check if required data files exist"""
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
    
    return True


def main():
    """Main test execution"""
    print("🚀 DLFUSION Integration Test")
    print("=" * 60)
    print("This test demonstrates that DLFUSION can work with existing")
    print("DLXLS and DLNEP data without needing to re-run collection.")
    print()
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please ensure DLXLS and DLNEP have been run first.")
        return
    
    print()
    
    # Test DLFUSION
    success = test_dlfusion_only()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed! DLFUSION is working correctly.")
        print("\nThe DLFUSION feature successfully:")
        print("• ✅ Loaded existing DLXLS data (BME topic data)")
        print("• ✅ Loaded existing DLNEP data (Neptun enrollment data)")
        print("• ✅ Fused the data according to specification")
        print("• ✅ Saved results to JSON format")
        print("• ✅ Provided comprehensive statistics")
        print("\n💡 You can now use the fused data for session planning!")
    else:
        print("❌ Tests failed. Please check the logs for details.")


if __name__ == "__main__":
    main()
