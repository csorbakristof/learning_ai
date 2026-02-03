#!/usr/bin/env python3
"""
Quick script to count students enrolled in specific courses
"""

import json
from pathlib import Path

# Target course codes
TARGET_COURSES = {
    'BMEVIAUMT00', 'BMEVIAUMT10', 'BMEVIAUMT12', 'BMEVIAUM026',
    'BMEVIAUAL01', 'BMEVIAUAL03', 'BMEVIAUAL04', 'BMEVIAUAL05',
    'BMEVIAUML10', 'BMEVIAUML12', 'BMEVIAUML11', 'BMEVIAUML13',
    'BMEVIAUM039'
}
# no: 'BMEVIAUMT11', 'BMEVIAUAT02'

def main():
    # Load fused data
    data_file = Path(__file__).parent.parent / "data" / "fused_student_data.json"
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_students = len(data['students'])
    students_in_target_courses = 0
    students_with_topics_in_target_courses = 0
    
    # Count students enrolled in target courses
    for student in data['students']:
        enrolled_courses = student.get('enrolled_courses', [])
        
        # Check if student is enrolled in any target course
        has_target_course = any(
            course.get('course_code') in TARGET_COURSES
            for course in enrolled_courses
        )
        
        if has_target_course:
            students_in_target_courses += 1
            
            # Also count if they have a topic
            if student.get('has_topic'):
                students_with_topics_in_target_courses += 1
    
    # Print results
    print("=" * 60)
    print("STUDENT ENROLLMENT COUNT")
    print("=" * 60)
    print(f"\nTotal students in dataset: {total_students}")
    print(f"\nStudents enrolled in target courses: {students_in_target_courses}")
    print(f"Students with topics in target courses: {students_with_topics_in_target_courses}")
    print(f"Students without topics in target courses: {students_in_target_courses - students_with_topics_in_target_courses}")
    print(f"\nPercentage enrolled in target courses: {students_in_target_courses / total_students * 100:.1f}%")
    print("\nTarget courses:")
    for course in sorted(TARGET_COURSES):
        print(f"  - {course}")
    print("=" * 60)

if __name__ == "__main__":
    main()
