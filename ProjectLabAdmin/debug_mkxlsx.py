from app1_data_collector.mkxlsx_creator import SessionPlannerExcelCreator

creator = SessionPlannerExcelCreator()
success = creator.load_fused_data()

print(f"Fused data loaded: {success}")
if creator.fused_data:
    print(f"Fused data keys: {creator.fused_data.keys()}")
    if 'students' in creator.fused_data:
        students = creator.fused_data['students']
        print(f"Total students: {len(students)}")
        
        students_with_topics = [s for s in students if s.get('has_topic')]
        print(f"Students with topics: {len(students_with_topics)}")
        
        for student in students_with_topics:
            print(f"  - {student['student_name']}: {student.get('topic_category', 'NO CATEGORY')}")
else:
    print("No fused data available")
