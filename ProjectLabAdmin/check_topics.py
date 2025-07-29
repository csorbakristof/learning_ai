import json

# Load the fused data
with open('data/fused_student_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('Students with topics and their enrolled courses:')
students_with_topics = [s for s in data['students'] if s['has_topic']]

for student in students_with_topics:
    print(f'Student: {student["student_name"]}')
    print(f'  Topic: {student["topic_title"]}')
    print(f'  Category: {student["topic_category"]}')
    courses = [c["course_code"] for c in student["enrolled_courses"]]
    print(f'  Enrolled courses: {courses}')
    print()

print(f'Total students with topics: {len(students_with_topics)}')
