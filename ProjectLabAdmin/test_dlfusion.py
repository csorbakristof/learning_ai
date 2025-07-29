"""
Test script to run DLFUSION and MKXLSX from scratch
"""

from app1_data_collector.dlfusion_processor import DataFusionProcessor
from app1_data_collector.mkxlsx_creator import SessionPlannerExcelCreator

def main():
    print('🔄 Starting from DLFUSION...')

    # Run DLFUSION
    print('📊 Running DLFUSION (Data Fusion)...')
    processor = DataFusionProcessor()
    success = processor.process_fusion()

    if success:
        summary = processor.get_fusion_summary()
        print(f'✅ DLFUSION Results:')
        print(f'   • Total students: {summary["total_students"]}')
        print(f'   • Students with topics: {summary["students_with_topics"]}')
        print(f'   • Students with enrollments: {summary["students_with_enrollments"]}')
        print(f'   • Students with both: {summary["students_with_both"]}')
        print(f'   • Unique courses: {summary["unique_courses"]}')
        
        # Run MKXLSX
        print('📋 Running MKXLSX (Session Planning Excel)...')
        creator = SessionPlannerExcelCreator()
        xlsx_success = creator.create_session_planning_excel()
        
        if xlsx_success:
            print('✅ MKXLSX Results:')
            print('   • Session planning Excel created successfully')
            print('   • File: data/session_planner.xlsx')
        else:
            print('❌ MKXLSX failed')
            
        print('🎉 Process completed!')
    else:
        print('❌ DLFUSION failed')

if __name__ == "__main__":
    main()
