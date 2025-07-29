#!/usr/bin/env python3
"""
Test MKXLSX functionality
"""

from app1_data_collector.mkxlsx_creator import SessionPlannerExcelCreator

def main():
    print("=== TESTING MKXLSX ===")
    
    # Create and run MKXLSX
    creator = SessionPlannerExcelCreator()
    success = creator.process_mkxlsx()
    
    print(f"MKXLSX Success: {success}")
    
    if success:
        summary = creator.get_planning_summary()
        print("\n=== MKXLSX SUMMARY ===")
        print(f"Total students: {summary['total_students']}")
        print(f"Students with topics: {summary['students_with_topics']}")
        print(f"Required sessions: {summary['required_sessions']}")
        print(f"Planning slots: {summary['planner_dimensions']['total_slots']}")
        print(f"Hungarian categories: {summary['hungarian_topic_categories']}")
        print(f"English student count: {summary.get('english_student_count', 0)}")
        print(f"All summary keys: {list(summary.keys())}")
        print(f"Planner dimensions: {summary['planner_dimensions']}")
    else:
        print("MKXLSX failed!")

if __name__ == "__main__":
    main()
