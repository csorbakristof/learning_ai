"""
DLFUSION - Data fusion module
This module combines data from DLXLS and DLNEP into a single JSON dataset.
"""

import json
import pandas as pd
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys
import logging

# Simple logging setup to avoid dependency issues
def setup_logging(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


class DataFusionProcessor:
    """Processor for combining DLXLS and DLNEP data"""
    
    # Course codes that should be taken into account according to specification
    ALLOWED_COURSE_CODES = {
        'BMEVIAUAL01', 'BMEVIAUAL03', 'BMEVIAUAL04', 'BMEVIAUAL05', 
        'BMEVIAUAT00', 'BMEVIAUAT01', 'BMEVIAUAT02', 'BMEVIAUA019', 
        'BMEVIAUML10', 'BMEVIAUML11', 'BMEVIAUML12', 'BMEVIAUML13',
        'BMEVIAUMT00', 'BMEVIAUMT01', 'BMEVIAUMT03', 'BMEVIAUMT10', 
        'BMEVIAUMT11', 'BMEVIAUMT12', 'BMEVIAUMT13',
        'BMEVIAUM026', 'BMEVIAUM027', 'BMEVIAUM039'
    }
    
    def __init__(self):
        """Initialize the data fusion processor"""
        self.logger = setup_logging(__name__)
        self.dlxls_data = []
        self.dlnep_data = []
        self.fused_data = []
    
    def load_dlxls_data(self, file_path: Optional[Path] = None) -> bool:
        """
        Load DLXLS data from Excel file
        
        Args:
            file_path: Path to DLXLS Excel file (defaults to data/bme_topic_data.xlsx)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if file_path is None:
                file_path = Path(__file__).parent.parent / "data" / "bme_topic_data.xlsx"
            
            if not file_path.exists():
                self.logger.error(f"DLXLS file not found: {file_path}")
                return False
            
            self.logger.info(f"Loading DLXLS data from: {file_path}")
            df = pd.read_excel(file_path)
            
            # Convert to list of dictionaries and clean up the data
            self.dlxls_data = []
            for _, row in df.iterrows():
                course_code = str(row.get('Tárgy nept', '')).strip()
                
                # Add BME prefix if missing (handle both VIAUAL04 and BMEVIAUAL04 formats)
                if course_code and not course_code.startswith('BME'):
                    course_code = 'BME' + course_code
                
                student_data = {
                    'supervisor': str(row.get('Konzulens', '')).strip(),
                    'supervisor_id': str(row.get('Konz. száma', '')).strip(),
                    'course_name': str(row.get('Tárgy', '')).strip(),
                    'course_code': course_code,
                    'category': str(row.get('Kategória', '')).strip(),
                    'topic_title': str(row.get('Téma címe', '')).strip(),
                    'student_name': str(row.get('Hallgató neve', '')).strip(),
                    'student_neptun': str(row.get('Hallg. nept', '')).strip()
                }
                
                # Only add if we have essential data and course code is in allowed list
                if student_data['student_neptun'] and student_data['course_code']:
                    if student_data['course_code'] in self.ALLOWED_COURSE_CODES:
                        self.dlxls_data.append(student_data)
                    else:
                        self.logger.debug(f"Skipping DLXLS record for course {student_data['course_code']} - not in allowed list")
            
            self.logger.info(f"Loaded {len(self.dlxls_data)} student records from DLXLS (filtered by allowed course codes)")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading DLXLS data: {e}")
            return False
    
    def load_dlnep_data(self, folder_path: Optional[Path] = None) -> bool:
        """
        Load DLNEP data from multiple Excel files
        
        Args:
            folder_path: Path to folder containing DLNEP Excel files
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if folder_path is None:
                folder_path = Path(__file__).parent.parent / "data" / "neptun_downloads"
            
            if not folder_path.exists():
                self.logger.error(f"DLNEP folder not found: {folder_path}")
                return False
            
            self.logger.info(f"Loading DLNEP data from: {folder_path}")
            excel_files = list(folder_path.glob("*.xlsx"))
            
            if not excel_files:
                self.logger.error("No Excel files found in DLNEP folder")
                return False
            
            self.dlnep_data = []
            processed_files = 0
            
            for file_path in excel_files:
                try:
                    course_code, is_english_course = self._extract_course_info_from_filename(file_path.name)
                    
                    if not course_code.startswith("BMEVI"):
                        self.logger.warning(f"Skipping file with invalid course code: {file_path.name}")
                        continue
                    
                    df = pd.read_excel(file_path)
                    
                    if len(df) == 0:
                        self.logger.info(f"Skipping empty file: {file_path.name}")
                        continue
                    
                    # Process each student in the course
                    for _, row in df.iterrows():
                        student_data = {
                            'course_code': course_code,
                            'is_english_course': is_english_course,
                            'student_neptun': str(row.get('Neptunkód', '')).strip(),
                            'student_name': str(row.get('Név', '')).strip(),
                            'schedule_type': str(row.get('Tanrend típus', '')).strip(),
                            'current_semester_entries': str(row.get('Bejegyzések (Aktuális félév)', '')).strip(),
                            'entry': str(row.get('Bejegyzés', '')).strip(),
                            'partial_result': str(row.get('Részeredmény', '')).strip()
                        }
                        
                        # Only add if we have essential data and course code is in allowed list
                        if student_data['student_neptun'] and student_data['course_code']:
                            if student_data['course_code'] in self.ALLOWED_COURSE_CODES:
                                self.dlnep_data.append(student_data)
                            else:
                                self.logger.debug(f"Skipping DLNEP record for course {student_data['course_code']} - not in allowed list")
                    
                    processed_files += 1
                    course_type = "English" if is_english_course else "Hungarian"
                    self.logger.info(f"Processed {file_path.name}: {len(df)} students ({course_type} course)")
                    
                except Exception as e:
                    self.logger.warning(f"Error processing file {file_path.name}: {e}")
                    continue
            
            self.logger.info(f"Loaded {len(self.dlnep_data)} student enrollments from {processed_files} DLNEP files (filtered by allowed course codes)")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading DLNEP data: {e}")
            return False
    
    def _extract_course_code_from_filename(self, filename: str) -> str:
        """Extract course code from filename"""
        # Pattern to match BMEVI followed by letters/numbers
        match = re.search(r'(BMEVI[A-Z]+\d+)', filename.upper())
        return match.group(1) if match else "UNKNOWN"
    
    def _extract_course_info_from_filename(self, filename: str) -> tuple:
        """
        Extract course code and language info from filename
        
        Filename format: jegyimport_BMEVIxxxxxx_YY_...
        where YY starts with 'A' for English courses, otherwise Hungarian
        
        Returns:
            Tuple of (course_code, is_english)
        """
        try:
            # Pattern to match the filename format: jegyimport_BMEVIxxxxxx_YY_
            # Use case-insensitive matching since filenames are in uppercase
            pattern = r'jegyimport_([^_]+)_([^_]+)_'
            match = re.search(pattern, filename, re.IGNORECASE)
            
            if match:
                course_code = match.group(1).upper()
                course_type = match.group(2).upper()
                
                # Verify the course code starts with BMEVI
                if course_code.startswith('BMEVI'):
                    is_english = course_type.startswith('A')
                    return course_code, is_english
                else:
                    self.logger.warning(f"Course code {course_code} doesn't start with BMEVI in filename {filename}")
                    return course_code, False
            else:
                # Fallback to old method
                course_code = self._extract_course_code_from_filename(filename)
                # If we can't parse the format, assume Hungarian
                return course_code, False
                
        except Exception as e:
            self.logger.warning(f"Error parsing filename {filename}: {e}")
            course_code = self._extract_course_code_from_filename(filename)
            return course_code, False
    
    def _is_english_topic(self, topic_title: str) -> bool:
        """
        Check if a topic is English based on title prefix
        
        Args:
            topic_title: The topic title to check
            
        Returns:
            True if topic is English (starts with Z-ENG), False otherwise
        """
        if not topic_title:
            return False
        return topic_title.upper().startswith('Z-ENG')
    
    def _validate_course_coverage(self) -> None:
        """
        Validate that we have data for all required courses and warn about missing ones
        """
        # Get course codes found in DLXLS data
        dlxls_courses = set(record['course_code'] for record in self.dlxls_data if record['course_code'])
        
        # Get course codes found in DLNEP data
        dlnep_courses = set(record['course_code'] for record in self.dlnep_data if record['course_code'])
        
        # Check for missing courses
        missing_from_dlxls = set(self.ALLOWED_COURSE_CODES) - dlxls_courses
        missing_from_dlnep = set(self.ALLOWED_COURSE_CODES) - dlnep_courses
        
        if missing_from_dlxls:
            self.logger.warning(f"Missing DLXLS data for courses: {', '.join(sorted(missing_from_dlxls))}")
        
        if missing_from_dlnep:
            self.logger.warning(f"Missing DLNEP data for courses: {', '.join(sorted(missing_from_dlnep))}")
        
        # Log coverage summary
        self.logger.info(f"Course coverage: DLXLS has {len(dlxls_courses)}/{len(self.ALLOWED_COURSE_CODES)} courses, "
                        f"DLNEP has {len(dlnep_courses)}/{len(self.ALLOWED_COURSE_CODES)} courses")
    
    def fuse_data(self) -> bool:
        """
        Combine DLXLS and DLNEP data according to specification
        
        For each student, we need:
        - List of courses they are enrolled in (from DLNEP)
        - If they have a topic (from DLXLS): supervisor name and category
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.dlxls_data and not self.dlnep_data:
                self.logger.error("No data loaded for fusion")
                return False
            
            self.logger.info("Starting data fusion process...")
            
            # Validate course coverage and warn about missing courses
            self._validate_course_coverage()
            
            # Create a dictionary of students from DLNEP data (enrollments)
            students_dict = {}
            
            # First, collect all course enrollments per student
            for enrollment in self.dlnep_data:
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
                        'is_enrolled_in_english_course': False
                    }
                
                # Add course to enrolled courses if not already present
                course_info = {
                    'course_code': course_code,
                    'is_english_course': enrollment['is_english_course'],
                    'schedule_type': enrollment['schedule_type'],
                    'entry': enrollment['entry'],
                    'partial_result': enrollment['partial_result']
                }
                
                # Check if this course is already in the list
                course_exists = any(c['course_code'] == course_code for c in students_dict[neptun_code]['enrolled_courses'])
                if not course_exists:
                    students_dict[neptun_code]['enrolled_courses'].append(course_info)
                
                # Mark if student is enrolled in any English course
                if enrollment['is_english_course']:
                    students_dict[neptun_code]['is_enrolled_in_english_course'] = True
            
            # Now, add topic information from DLXLS data
            for topic_data in self.dlxls_data:
                neptun_code = topic_data['student_neptun']
                is_english_topic = self._is_english_topic(topic_data['topic_title'])
                
                # If student exists in enrollments, add topic info
                if neptun_code in students_dict:
                    students_dict[neptun_code]['has_topic'] = True
                    students_dict[neptun_code]['supervisor'] = topic_data['supervisor']
                    students_dict[neptun_code]['topic_category'] = topic_data['category']
                    students_dict[neptun_code]['topic_title'] = topic_data['topic_title']
                    students_dict[neptun_code]['is_english_topic'] = is_english_topic
                else:
                    # Student has topic but no enrollment data - still add them
                    students_dict[neptun_code] = {
                        'student_neptun': neptun_code,
                        'student_name': topic_data['student_name'],
                        'enrolled_courses': [],  # No enrollment data available
                        'has_topic': True,
                        'supervisor': topic_data['supervisor'],
                        'topic_category': topic_data['category'],
                        'topic_title': topic_data['topic_title'],
                        'is_english_topic': is_english_topic,
                        'is_enrolled_in_english_course': False
                    }
            
            # Convert to list format
            self.fused_data = list(students_dict.values())
            
            # Sort by student name for consistency
            self.fused_data.sort(key=lambda x: x['student_name'])
            
            self.logger.info(f"Data fusion completed. {len(self.fused_data)} students in fused dataset")
            
            # Log some statistics
            students_with_topics = sum(1 for s in self.fused_data if s['has_topic'])
            students_with_enrollments = sum(1 for s in self.fused_data if s['enrolled_courses'])
            
            self.logger.info(f"Statistics: {students_with_topics} students with topics, "
                           f"{students_with_enrollments} students with course enrollments")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error during data fusion: {e}")
            return False
    
    def save_fused_data(self, output_file: Optional[Path] = None) -> bool:
        """
        Save the fused data to JSON file
        
        Args:
            output_file: Path for output JSON file (defaults to data/fused_student_data.json)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.fused_data:
                self.logger.warning("No fused data to save")
                return False
            
            if output_file is None:
                output_file = Path(__file__).parent.parent / "data" / "fused_student_data.json"
            
            # Ensure output directory exists
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Create the final dataset structure
            dataset = {
                'metadata': {
                    'creation_date': pd.Timestamp.now().isoformat(),
                    'total_students': len(self.fused_data),
                    'students_with_topics': sum(1 for s in self.fused_data if s['has_topic']),
                    'students_with_enrollments': sum(1 for s in self.fused_data if s['enrolled_courses']),
                    'dlxls_records': len(self.dlxls_data),
                    'dlnep_records': len(self.dlnep_data)
                },
                'students': self.fused_data
            }
            
            # Save to JSON with proper formatting
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(dataset, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"Fused data saved to: {output_file}")
            self.logger.info(f"Dataset contains {len(self.fused_data)} students")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving fused data: {e}")
            return False
    
    def get_fusion_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the fusion process
        
        Returns:
            Dictionary with fusion statistics
        """
        if not self.fused_data:
            return {'error': 'No fused data available'}
        
        # Calculate various statistics
        students_with_topics = [s for s in self.fused_data if s['has_topic']]
        students_with_enrollments = [s for s in self.fused_data if s['enrolled_courses']]
        students_with_english_topics = [s for s in students_with_topics if s.get('is_english_topic', False)]
        students_with_hungarian_topics = [s for s in students_with_topics if not s.get('is_english_topic', False)]
        students_in_english_courses = [s for s in self.fused_data if s.get('is_enrolled_in_english_course', False)]
        
        # Course statistics
        all_courses = set()
        english_courses = set()
        hungarian_courses = set()
        
        for student in self.fused_data:
            for course in student['enrolled_courses']:
                course_code = course['course_code']
                all_courses.add(course_code)
                if course.get('is_english_course', False):
                    english_courses.add(course_code)
                else:
                    hungarian_courses.add(course_code)
        
        # Category statistics - separate Hungarian and English
        hungarian_categories = {}
        english_categories = {}
        
        for student in students_with_topics:
            category = student.get('topic_category', 'Unknown')
            if student.get('is_english_topic', False):
                english_categories[category] = english_categories.get(category, 0) + 1
            else:
                hungarian_categories[category] = hungarian_categories.get(category, 0) + 1
        
        return {
            'total_students': len(self.fused_data),
            'students_with_topics': len(students_with_topics),
            'students_with_enrollments': len(students_with_enrollments),
            'students_with_both': len([s for s in self.fused_data if s['has_topic'] and s['enrolled_courses']]),
            'students_with_english_topics': len(students_with_english_topics),
            'students_with_hungarian_topics': len(students_with_hungarian_topics),
            'students_in_english_courses': len(students_in_english_courses),
            'unique_courses': len(all_courses),
            'english_courses': len(english_courses),
            'hungarian_courses': len(hungarian_courses),
            'course_list': sorted(list(all_courses)),
            'english_course_list': sorted(list(english_courses)),
            'hungarian_course_list': sorted(list(hungarian_courses)),
            'hungarian_topic_categories': hungarian_categories,
            'english_topic_categories': english_categories,
            'dlxls_source_records': len(self.dlxls_data),
            'dlnep_source_records': len(self.dlnep_data)
        }
    
    def process_fusion(self, dlxls_file: Optional[Path] = None, 
                      dlnep_folder: Optional[Path] = None,
                      output_file: Optional[Path] = None) -> bool:
        """
        Complete fusion process: load, fuse, and save data
        
        Args:
            dlxls_file: Path to DLXLS Excel file
            dlnep_folder: Path to DLNEP folder
            output_file: Path for output JSON file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load DLXLS data
            if not self.load_dlxls_data(dlxls_file):
                self.logger.error("Failed to load DLXLS data")
                return False
            
            # Load DLNEP data
            if not self.load_dlnep_data(dlnep_folder):
                self.logger.error("Failed to load DLNEP data")
                return False
            
            # Fuse the data
            if not self.fuse_data():
                self.logger.error("Failed to fuse data")
                return False
            
            # Save the result
            if not self.save_fused_data(output_file):
                self.logger.error("Failed to save fused data")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in fusion process: {e}")
            return False


def main():
    """Main function for testing the DLFUSION feature"""
    processor = DataFusionProcessor()
    
    # Process the fusion
    success = processor.process_fusion()
    
    if success:
        # Print summary
        summary = processor.get_fusion_summary()
        print("Data Fusion Summary:")
        print(f"- Total students: {summary['total_students']}")
        print(f"- Students with topics: {summary['students_with_topics']}")
        print(f"  - Hungarian topics: {summary['students_with_hungarian_topics']}")
        print(f"  - English topics: {summary['students_with_english_topics']}")
        print(f"- Students with enrollments: {summary['students_with_enrollments']}")
        print(f"  - In English courses: {summary['students_in_english_courses']}")
        print(f"- Students with both: {summary['students_with_both']}")
        print(f"- Unique courses: {summary['unique_courses']}")
        print(f"  - English courses: {summary['english_courses']}")
        print(f"  - Hungarian courses: {summary['hungarian_courses']}")
        print(f"- Hungarian topic categories: {summary['hungarian_topic_categories']}")
        print(f"- English topic categories: {summary['english_topic_categories']}")
        print(f"- Source DLXLS records: {summary['dlxls_source_records']}")
        print(f"- Source DLNEP records: {summary['dlnep_source_records']}")
        print("Fusion completed successfully!")
    else:
        print("Fusion failed!")


if __name__ == "__main__":
    main()
