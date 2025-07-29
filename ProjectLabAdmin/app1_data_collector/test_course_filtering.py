"""
Test course filtering in MKXLSX
"""

import json
from pathlib import Path
from mkxlsx_creator import SessionPlannerExcelCreator

def test_course_filtering():
    """Test that MKXLSX course filtering works correctly"""
    
    # Create test data with students in different courses
    test_data = {
        "students": [
            {
                "student_neptun": "TEST01",
                "student_name": "Test Student 1",
                "enrolled_courses": [
                    {"course_code": "BMEVIAUMT00", "is_english": False}  # In statistics list
                ],
                "has_topic": True,
                "topic_category": "Software",
                "is_english_topic": False
            },
            {
                "student_neptun": "TEST02", 
                "student_name": "Test Student 2",
                "enrolled_courses": [
                    {"course_code": "BMEVIAUML10", "is_english": True}  # In statistics list
                ],
                "has_topic": True,
                "topic_category": "Hardware",
                "is_english_topic": True
            },
            {
                "student_neptun": "TEST03",
                "student_name": "Test Student 3", 
                "enrolled_courses": [
                    {"course_code": "BMEVIAUAT01", "is_english": True}  # NOT in statistics list
                ],
                "has_topic": True,
                "topic_category": "Software",
                "is_english_topic": False
            }
        ]
    }
    
    # Save test data
    test_file = Path("test_fused_data.json")
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    # Create MKXLSX creator and load test data
    creator = SessionPlannerExcelCreator()
    creator.load_fused_data(test_file)
    
    # Get summary to check filtering
    summary = creator.get_planning_summary()
    
    print("🧪 Course Filtering Test Results:")
    print(f"   • Total students in test data: {len(test_data['students'])}")
    print(f"   • Students with topics (filtered): {summary['students_with_topics']}")
    print(f"   • Hungarian topic categories: {summary['hungarian_topic_categories']}")
    print(f"   • English student count: {summary['english_student_count']}")
    
    # Expected results:
    # - TEST01: Has BMEVIAUMT00 (in list) + Hungarian topic → should be counted
    # - TEST02: Has BMEVIAUMT01 (in list) + English topic → should be counted as English
    # - TEST03: Has BMEVIAUAT01 (NOT in list) → should be filtered out
    
    expected_students_with_topics = 2  # TEST01 and TEST02
    expected_hungarian_categories = {"Software": 1}  # Only TEST01
    expected_english_count = 1  # Only TEST02
    
    # Verify results
    success = True
    if summary['students_with_topics'] != expected_students_with_topics:
        print(f"❌ Expected {expected_students_with_topics} students with topics, got {summary['students_with_topics']}")
        success = False
        
    if summary['hungarian_topic_categories'] != expected_hungarian_categories:
        print(f"❌ Expected Hungarian categories {expected_hungarian_categories}, got {summary['hungarian_topic_categories']}")
        success = False
        
    if summary['english_student_count'] != expected_english_count:
        print(f"❌ Expected {expected_english_count} English students, got {summary['english_student_count']}")
        success = False
    
    if success:
        print("✅ Course filtering test passed!")
    else:
        print("❌ Course filtering test failed!")
    
    # Cleanup
    test_file.unlink()
    
    return success

if __name__ == "__main__":
    test_course_filtering()
