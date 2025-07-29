"""
Data fusion logic for combining DLXLS and DLNEP data
Separated according to SRP
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
import logging


class DataFusionEngine:
    """Responsible for the core data fusion logic"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def fuse_data(self, dlxls_data: List[Dict[str, Any]], dlnep_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Fuse DLXLS and DLNEP data into a unified dataset
        
        Args:
            dlxls_data: List of student topic data from DLXLS
            dlnep_data: List of student enrollment data from DLNEP
            
        Returns:
            List of fused student records
        """
        try:
            if not dlxls_data and not dlnep_data:
                self.logger.error("No data provided for fusion")
                return []
            
            self.logger.info("Starting data fusion process...")
            
            # Create a dictionary of students from DLNEP data (enrollments)
            students_dict = {}
            
            # First, collect all course enrollments per student
            for enrollment in dlnep_data:
                neptun_code = enrollment['student_neptun']
                course_code = enrollment['course_code']
                
                if neptun_code not in students_dict:
                    students_dict[neptun_code] = {
                        'student_neptun': neptun_code,
                        'student_name': enrollment['student_name'],
                        'enrolled_courses': [],
                        'has_topic': False,
                        'supervisor': None,
                        'topic_category': None,
                        'topic_title': None,
                        'is_english_topic': False,
                    }
                
                # Add course to enrolled courses list
                course_info = {
                    'course_code': course_code,
                    'is_english': enrollment['is_english_course'],
                    'schedule_type': enrollment.get('schedule_type', ''),
                    'entry': enrollment.get('entry', ''),
                    'partial_result': enrollment.get('partial_result', '')
                }
                
                students_dict[neptun_code]['enrolled_courses'].append(course_info)
            
            # Then, add topic information from DLXLS data
            for topic_data in dlxls_data:
                neptun_code = topic_data['student_neptun']
                
                if neptun_code in students_dict:
                    # Student exists in both datasets
                    students_dict[neptun_code].update({
                        'has_topic': topic_data['has_topic'],
                        'supervisor': topic_data['supervisor'],
                        'topic_category': topic_data['topic_category'],
                        'topic_title': topic_data['topic_title'],
                        'is_english_topic': topic_data['is_english_topic']
                    })
                else:
                    # Student only in DLXLS (has topic but no enrollments in allowed courses)
                    students_dict[neptun_code] = {
                        'student_neptun': neptun_code,
                        'student_name': topic_data['student_name'],
                        'enrolled_courses': [],
                        'has_topic': topic_data['has_topic'],
                        'supervisor': topic_data['supervisor'],
                        'topic_category': topic_data['topic_category'],
                        'topic_title': topic_data['topic_title'],
                        'is_english_topic': topic_data['is_english_topic']
                    }
            
            # Convert dictionary to list
            fused_students = list(students_dict.values())
            
            self.logger.info(f"Data fusion completed. {len(fused_students)} students in fused dataset")
            
            # Log statistics
            students_with_topics = sum(1 for s in fused_students if s['has_topic'])
            students_with_enrollments = sum(1 for s in fused_students if s['enrolled_courses'])
            
            self.logger.info(f"Statistics: {students_with_topics} students with topics, {students_with_enrollments} students with course enrollments")
            
            return fused_students
            
        except Exception as e:
            self.logger.error(f"Error during data fusion: {e}")
            return []


class FusionDataValidator:
    """Validates and analyzes fused data"""
    
    def __init__(self, logger: logging.Logger, allowed_course_codes: set):
        self.logger = logger
        self.allowed_course_codes = allowed_course_codes
    
    def validate_course_coverage(self, dlxls_data: List[Dict[str, Any]], dlnep_data: List[Dict[str, Any]]) -> None:
        """
        Validate that we have data for all required courses and warn about missing ones
        """
        # Get course codes found in DLXLS data
        dlxls_courses = set(record['course_code'] for record in dlxls_data if record.get('course_code'))
        
        # Get course codes found in DLNEP data
        dlnep_courses = set(record['course_code'] for record in dlnep_data if record.get('course_code'))
        
        # Check for missing courses
        missing_from_dlxls = self.allowed_course_codes - dlxls_courses
        missing_from_dlnep = self.allowed_course_codes - dlnep_courses
        
        if missing_from_dlxls:
            self.logger.warning(f"Missing DLXLS data for courses: {', '.join(sorted(missing_from_dlxls))}")
        
        if missing_from_dlnep:
            self.logger.warning(f"Missing DLNEP data for courses: {', '.join(sorted(missing_from_dlnep))}")
        
        # Log coverage summary
        self.logger.info(f"Course coverage: DLXLS has {len(dlxls_courses)}/{len(self.allowed_course_codes)} courses, "
                        f"DLNEP has {len(dlnep_courses)}/{len(self.allowed_course_codes)} courses")
    
    def analyze_fusion_results(self, fused_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze the fusion results and return statistics
        
        Args:
            fused_data: List of fused student records
            
        Returns:
            Dictionary containing fusion statistics
        """
        total_students = len(fused_data)
        students_with_topics = sum(1 for s in fused_data if s.get('has_topic'))
        students_with_enrollments = sum(1 for s in fused_data if s.get('enrolled_courses'))
        students_with_both = sum(1 for s in fused_data if s.get('has_topic') and s.get('enrolled_courses'))
        
        # Analyze courses
        all_courses = set()
        english_courses = set()
        hungarian_courses = set()
        
        for student in fused_data:
            for course in student.get('enrolled_courses', []):
                course_code = course.get('course_code')
                if course_code:
                    all_courses.add(course_code)
                    if course.get('is_english'):
                        english_courses.add(course_code)
                    else:
                        hungarian_courses.add(course_code)
        
        # Count students in English courses
        students_in_english_courses = 0
        for student in fused_data:
            has_english_course = any(
                course.get('is_english', False) 
                for course in student.get('enrolled_courses', [])
            )
            if has_english_course:
                students_in_english_courses += 1
        
        return {
            'total_students': total_students,
            'students_with_topics': students_with_topics,
            'students_with_enrollments': students_with_enrollments,
            'students_with_both': students_with_both,
            'unique_courses': len(all_courses),
            'english_courses': len(english_courses),
            'hungarian_courses': len(hungarian_courses),
            'students_in_english_courses': students_in_english_courses,
            'all_courses_list': sorted(all_courses),
            'english_courses_list': sorted(english_courses),
            'hungarian_courses_list': sorted(hungarian_courses)
        }


class FusionDataExporter:
    """Responsible for exporting fused data to JSON"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def save_to_json(self, fused_data: List[Dict[str, Any]], dlxls_count: int, dlnep_count: int, 
                    output_file: Path) -> bool:
        """
        Save fused data to JSON file
        
        Args:
            fused_data: List of fused student records
            dlxls_count: Number of DLXLS records processed
            dlnep_count: Number of DLNEP records processed
            output_file: Path to output JSON file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create metadata
            metadata = {
                "creation_date": pd.Timestamp.now().isoformat(),
                "total_students": len(fused_data),
                "students_with_topics": sum(1 for s in fused_data if s.get('has_topic')),
                "students_with_enrollments": sum(1 for s in fused_data if s.get('enrolled_courses')),
                "dlxls_records": dlxls_count,
                "dlnep_records": dlnep_count
            }
            
            # Create output structure
            output_data = {
                "metadata": metadata,
                "students": fused_data
            }
            
            # Save to JSON file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Fused data saved to: {output_file}")
            self.logger.info(f"Dataset contains {len(fused_data)} students")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving fused data: {e}")
            return False
