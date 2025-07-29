"""
Data loaders for DLFUSION - separated according to SRP
"""

import pandas as pd
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging


class CourseCodeValidator:
    """Validates course codes according to specification"""
    
    def __init__(self, allowed_course_codes: set):
        self.allowed_course_codes = allowed_course_codes
    
    def is_valid_course(self, course_code: str) -> bool:
        """Check if course code is in the allowed list"""
        return course_code in self.allowed_course_codes


class DLXLSDataLoader:
    """Responsible for loading and processing DLXLS data"""
    
    def __init__(self, logger: logging.Logger, course_validator: CourseCodeValidator):
        self.logger = logger
        self.course_validator = course_validator
    
    def load_data(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Load DLXLS data from Excel file
        
        Args:
            file_path: Path to DLXLS Excel file
            
        Returns:
            List of student data dictionaries
        """
        try:
            self.logger.info(f"Loading DLXLS data from: {file_path}")
            
            if not file_path.exists():
                self.logger.error(f"DLXLS file not found: {file_path}")
                return []
            
            # Read the second worksheet (containing "konzultáció")
            excel_file = pd.ExcelFile(file_path)
            target_sheet = self._find_consultation_sheet(excel_file)
            
            if not target_sheet:
                self.logger.error("Could not find consultation worksheet")
                return []
            
            df = pd.read_excel(file_path, sheet_name=target_sheet)
            self.logger.info(f"Read {len(df)} rows from worksheet '{target_sheet}'")
            
            # Process the data
            student_data = self._process_dlxls_dataframe(df)
            
            # Filter by allowed course codes
            filtered_data = [
                student for student in student_data 
                if student.get('course_code') and 
                self.course_validator.is_valid_course(student['course_code'])
            ]
            
            self.logger.info(f"Loaded {len(filtered_data)} student records from DLXLS (filtered by allowed course codes)")
            return filtered_data
            
        except Exception as e:
            self.logger.error(f"Error loading DLXLS data: {e}")
            return []
    
    def _find_consultation_sheet(self, excel_file) -> Optional[str]:
        """Find the worksheet containing 'konzultáció' in its name"""
        for sheet_name in excel_file.sheet_names:
            if 'konzultáció' in sheet_name.lower():
                return sheet_name
        return None
    
    def _process_dlxls_dataframe(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Process DLXLS dataframe to extract student information"""
        processed_data = []
        
        for _, row in df.iterrows():
            try:
                student_data = self._extract_dlxls_student_data(row)
                if student_data and student_data.get('student_neptun'):
                    processed_data.append(student_data)
            except Exception as e:
                self.logger.warning(f"Error processing DLXLS row: {e}")
                continue
        
        return processed_data
    
    def _extract_dlxls_student_data(self, row) -> Optional[Dict[str, Any]]:
        """Extract student data from a DLXLS row"""
        try:
            # Extract student information (adjust column names based on actual Excel structure)
            student_neptun = str(row.get('Neptun', '')).strip()
            student_name = str(row.get('Név', '')).strip()
            supervisor = str(row.get('Konzulens', '')).strip()
            topic_category = str(row.get('Kategória', '')).strip()
            topic_title = str(row.get('Téma címe', '')).strip()
            course_code = str(row.get('Tárgykód', '')).strip()
            
            # Skip empty rows
            if not student_neptun or student_neptun == 'nan':
                return None
            
            # Determine if this is an English topic
            is_english_topic = self._is_english_topic(topic_title)
            
            return {
                'student_neptun': student_neptun,
                'student_name': student_name,
                'supervisor': supervisor if supervisor != 'nan' else None,
                'topic_category': topic_category if topic_category != 'nan' else None,
                'topic_title': topic_title if topic_title != 'nan' else None,
                'course_code': course_code if course_code != 'nan' else None,
                'is_english_topic': is_english_topic,
                'has_topic': bool(topic_title and topic_title != 'nan')
            }
            
        except Exception as e:
            self.logger.warning(f"Error extracting DLXLS student data: {e}")
            return None
    
    def _is_english_topic(self, topic_title: str) -> bool:
        """Check if a topic is English based on title prefix"""
        if not topic_title:
            return False
        return topic_title.upper().startswith('Z-ENG')


class DLNEPDataLoader:
    """Responsible for loading and processing DLNEP data"""
    
    def __init__(self, logger: logging.Logger, course_validator: CourseCodeValidator):
        self.logger = logger
        self.course_validator = course_validator
    
    def load_data(self, folder_path: Path) -> List[Dict[str, Any]]:
        """
        Load DLNEP data from folder containing Excel files
        
        Args:
            folder_path: Path to folder containing DLNEP Excel files
            
        Returns:
            List of student enrollment dictionaries
        """
        try:
            self.logger.info(f"Loading DLNEP data from: {folder_path}")
            
            if not folder_path.exists():
                self.logger.error(f"DLNEP folder not found: {folder_path}")
                return []
            
            excel_files = list(folder_path.glob("*.xlsx"))
            if not excel_files:
                self.logger.error(f"No Excel files found in: {folder_path}")
                return []
            
            all_student_data = []
            processed_files = 0
            
            for file_path in excel_files:
                student_data = self._process_dlnep_file(file_path)
                all_student_data.extend(student_data)
                if student_data:  # Only count non-empty files
                    processed_files += 1
            
            # Filter by allowed course codes
            filtered_data = [
                student for student in all_student_data 
                if student.get('course_code') and 
                self.course_validator.is_valid_course(student['course_code'])
            ]
            
            self.logger.info(f"Loaded {len(filtered_data)} student enrollments from {processed_files} DLNEP files (filtered by allowed course codes)")
            return filtered_data
            
        except Exception as e:
            self.logger.error(f"Error loading DLNEP data: {e}")
            return []
    
    def _process_dlnep_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Process a single DLNEP Excel file"""
        try:
            # Read the Excel file
            df = pd.read_excel(file_path)
            
            if df.empty:
                self.logger.info(f"Skipping empty file: {file_path.name}")
                return []
            
            # Extract course information from filename
            course_code, is_english_course = self._extract_course_info_from_filename(file_path.name)
            
            # Process each student row
            student_data = []
            for _, row in df.iterrows():
                student_info = self._extract_dlnep_student_data(row, course_code, is_english_course, file_path.name)
                if student_info:
                    student_data.append(student_info)
            
            course_type = "English" if is_english_course else "Hungarian"
            self.logger.info(f"Processed {file_path.name}: {len(df)} students ({course_type} course)")
            
            return student_data
            
        except Exception as e:
            self.logger.warning(f"Error processing file {file_path.name}: {e}")
            return []
    
    def _extract_course_info_from_filename(self, filename: str) -> tuple:
        """Extract course code and language info from filename"""
        try:
            # Pattern to match the filename format: jegyimport_BMEVIxxxxxx_YY_
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
                return course_code, False
                
        except Exception as e:
            self.logger.warning(f"Error parsing filename {filename}: {e}")
            course_code = self._extract_course_code_from_filename(filename)
            return course_code, False
    
    def _extract_course_code_from_filename(self, filename: str) -> str:
        """Extract course code from filename (fallback method)"""
        match = re.search(r'(BMEVI[A-Z]+\d+)', filename.upper())
        return match.group(1) if match else "UNKNOWN"
    
    def _extract_dlnep_student_data(self, row, course_code: str, is_english_course: bool, filename: str) -> Optional[Dict[str, Any]]:
        """Extract student data from DLNEP Excel row"""
        try:
            # Extract student information from row
            student_neptun = str(row.get('Neptun kód', '')).strip()
            student_name = str(row.get('Név', '')).strip()
            
            if not student_neptun or student_neptun == 'nan':
                return None
            
            return {
                'student_neptun': student_neptun,
                'student_name': student_name,
                'course_code': course_code,
                'is_english_course': is_english_course,
                'source_file': filename,
                'schedule_type': str(row.get('Órarend típus', '')).strip(),
                'entry': str(row.get('Felvétel', '')).strip(),
                'partial_result': str(row.get('Részeredmény', '')).strip()
            }
            
        except Exception as e:
            self.logger.warning(f"Error extracting DLNEP student data: {e}")
            return None
