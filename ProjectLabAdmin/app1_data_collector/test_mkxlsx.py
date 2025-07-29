#!/usr/bin/env python3
"""
Test script for MKXLSX feature
Tests the Excel table creation for session planning using DLFUSION data
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from mkxlsx_creator import SessionPlannerExcelCreator


def main():
    """Main test function"""
    print("Testing MKXLSX feature...")
    print("=" * 50)
    
    # Create Excel creator
    creator = SessionPlannerExcelCreator()
    
    # Run the complete MKXLSX process
    success = creator.process_mkxlsx()
    
    if success:
        print("✅ MKXLSX completed successfully!")
        print()
        
        # Display summary
        summary = creator.get_planning_summary()
        print("📊 Session Planning Summary:")
        print(f"   • Total students: {summary['total_students']}")
        print(f"   • Students with topics: {summary['students_with_topics']}")
        print(f"   • Required sessions (9 per session): {summary['required_sessions']}")
        print()
        
        if summary['hungarian_topic_categories']:
            print("🏷️  Hungarian Topic Categories:")
            for category, count in summary['hungarian_topic_categories'].items():
                import math
                sessions_needed = math.ceil(count / 9)
                print(f"   • {category}: {count} students ({sessions_needed} sessions)")
            print()
            
        if summary['english_student_count'] > 0:
            import math
            sessions_needed = math.ceil(summary['english_student_count'] / 9)
            print("🌍 English Topics (ENG):")
            print(f"   • ENG: {summary['english_student_count']} students ({sessions_needed} sessions)")
            print()
        
        dims = summary['planner_dimensions']
        print("📅 Planner Table Structure:")
        print(f"   • Time slots: {dims['time_slots']} ({', '.join(creator.time_slots)})")
        print(f"   • Weekdays: {dims['weekdays']} ({', '.join(creator.weekdays)})")
        print(f"   • Rooms: {dims['rooms']} ({', '.join(creator.rooms)})")
        print(f"   • Total planning slots: {dims['total_slots']}")
        print()
        
        print("🎯 Supported Session Types:")
        print(f"   • Standard: {', '.join(creator.session_types)}")
        print(f"   • Special: {', '.join(creator.special_session_types)}")
        print()
        
        print("📁 Output file: ../data/session_planner.xlsx")
        print("💡 The Excel file contains:")
        print("   • Upper section: Planner table for entering session types")
        print("   • Lower section: Statistics with automatic Excel formulas")
        
    else:
        print("❌ MKXLSX test failed!")
        print("Please check if DLFUSION data exists (data/fused_student_data.json)")


if __name__ == "__main__":
    main()
