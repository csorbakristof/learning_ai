#!/usr/bin/env python3
"""
Test script for DLFUSION feature
Tests the data fusion functionality using existing DLXLS and DLNEP data
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from dlfusion_processor import DataFusionProcessor


def main():
    """Main test function"""
    print("Testing DLFUSION feature...")
    print("=" * 50)
    
    # Create processor
    processor = DataFusionProcessor()
    
    # Run the complete fusion process
    success = processor.process_fusion()
    
    if success:
        print("✅ Data fusion completed successfully!")
        print()
        
        # Display summary
        summary = processor.get_fusion_summary()
        print("📊 Fusion Summary:")
        print(f"   • Total students: {summary['total_students']}")
        print(f"   • Students with topics: {summary['students_with_topics']}")
        print(f"     - Hungarian topics: {summary['students_with_hungarian_topics']}")
        print(f"     - English topics: {summary['students_with_english_topics']}")
        print(f"   • Students with enrollments: {summary['students_with_enrollments']}")
        print(f"     - In English courses: {summary['students_in_english_courses']}")
        print(f"   • Students with both: {summary['students_with_both']}")
        print(f"   • Unique courses: {summary['unique_courses']}")
        print(f"     - English courses: {summary['english_courses']}")
        print(f"     - Hungarian courses: {summary['hungarian_courses']}")
        print()
        
        if summary['course_list']:
            print("📚 All courses found:")
            for course in summary['course_list']:
                print(f"   • {course}")
            print()
            
        if summary['english_course_list']:
            print("🌍 English courses:")
            for course in summary['english_course_list']:
                print(f"   • {course}")
            print()
            
        if summary['hungarian_course_list']:
            print("🇭🇺 Hungarian courses:")
            for course in summary['hungarian_course_list']:
                print(f"   • {course}")
            print()
        
        if summary['hungarian_topic_categories']:
            print("🏷️  Hungarian topic categories:")
            for category, count in summary['hungarian_topic_categories'].items():
                print(f"   • {category}: {count} students")
            print()
            
        if summary['english_topic_categories']:
            print("🏷️  English topic categories:")
            for category, count in summary['english_topic_categories'].items():
                print(f"   • {category}: {count} students")
            print()
        
        print(f"💾 Data sources:")
        print(f"   • DLXLS records: {summary['dlxls_source_records']}")
        print(f"   • DLNEP records: {summary['dlnep_source_records']}")
        print()
        
        print("💾 Output file: data/fused_student_data.json")
        
        # Show some sample fused data
        if processor.fused_data:
            print("\n📋 Sample student data:")
            for i, student in enumerate(processor.fused_data[:3]):  # Show first 3 students
                print(f"   {i+1}. {student['student_name']} ({student['student_neptun']})")
                print(f"      • Courses: {len(student['enrolled_courses'])}")
                if student['has_topic']:
                    topic_type = "English" if student.get('is_english_topic', False) else "Hungarian"
                    print(f"      • Topic ({topic_type}): {student['topic_category']} - {student['supervisor']}")
                else:
                    print(f"      • Topic: None")
                    
                if student['enrolled_courses']:
                    print(f"      • Enrolled courses:")
                    for course in student['enrolled_courses'][:2]:  # Show first 2 courses
                        course_type = "English" if course.get('is_english_course', False) else "Hungarian"
                        print(f"        - {course['course_code']} ({course_type})")
                else:
                    print(f"      • Enrolled courses: None")
                print()
        
    else:
        print("❌ Data fusion failed!")
        print("Please check if DLXLS and DLNEP data files exist in the data folder.")


if __name__ == "__main__":
    main()
