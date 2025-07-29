"""
Course identification and validation logic for Neptun system
Separated to follow Single Responsibility Principle
"""

from typing import List, Dict, Any, Optional
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class CourseTableFinder:
    """Responsible for finding and validating the course table in Neptun"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.required_headings = ["Tárgykód", "Tárgy név", "Követelmény", "Oktatók", "Kijelölés"] 
    
    def find_course_table(self, driver: WebDriver):
        """
        Find the correct course table on the page
        
        Args:
            driver: Selenium WebDriver instance
            
        Returns:
            WebElement of the course table or None if not found
        """
        try:
            tables = driver.find_elements(By.TAG_NAME, "table")
            self.logger.info(f"Found {len(tables)} tables on the page")
            
            for table_idx, table in enumerate(tables):
                if self._is_course_table(table, table_idx):
                    return table
            
            self.logger.error("Could not find course table with required headings and content")
            return None
            
        except Exception as e:
            self.logger.error(f"Error finding course table: {e}")
            return None
    
    def _is_course_table(self, table, table_idx: int) -> bool:
        """
        Check if a table is the course table by validating its content
        
        Args:
            table: WebElement of the table to check
            table_idx: Index of the table for logging
            
        Returns:
            True if this is the course table, False otherwise
        """
        try:
            table_text = table.text
            headings_found = sum(1 for heading in self.required_headings if heading in table_text)
            
            if headings_found >= 4:  # Must have at least 4 of the 5 required headings
                # Also check if it contains "Dr. Csorba Kristóf" and "BMEVI"
                if "Dr. Csorba Kristóf" in table_text and "BMEVI" in table_text:
                    self.logger.info(f"Found course table at index {table_idx} with {headings_found}/5 required headings")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.warning(f"Error checking table {table_idx}: {str(e)}")
            return False


class CourseTableParser:
    """Responsible for parsing the course table structure and extracting data"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def parse_header_row(self, table):
        """
        Find and parse the header row to identify column positions
        
        Args:
            table: WebElement of the course table
            
        Returns:
            Dict mapping column names to their indices, or None if failed
        """
        try:
            rows = table.find_elements(By.TAG_NAME, "tr")
            self.logger.info(f"Found {len(rows)} rows in course table")
            
            for row_idx, row in enumerate(rows[:5]):  # Check first 5 rows for headers
                cells = row.find_elements(By.TAG_NAME, "th")
                if not cells:  # If no th elements, try td elements
                    cells = row.find_elements(By.TAG_NAME, "td")
                
                if len(cells) >= 5:  # Should have multiple columns
                    cell_texts = [cell.text.strip() for cell in cells]
                    header_indices = self._extract_header_indices(cell_texts)
                    
                    if header_indices:
                        self.logger.info(f"Found header row at index {row_idx}")
                        self.logger.info(f"Column mapping: {header_indices}")
                        return header_indices, row_idx
            
            self.logger.error("Could not find header row with required columns")
            return None, None
            
        except Exception as e:
            self.logger.error(f"Error parsing header row: {e}")
            return None, None
    
    def _extract_header_indices(self, cell_texts: List[str]) -> Optional[Dict[str, int]]:
        """
        Extract column indices from header cell texts
        
        Args:
            cell_texts: List of header cell text values
            
        Returns:
            Dict mapping column names to indices or None if not valid
        """
        header_indices = {}
        
        # Look for required column headers
        for idx, text in enumerate(cell_texts):
            if "Tárgykód" in text:
                header_indices["course_code"] = idx
            elif "Tárgy név" in text:
                header_indices["course_name"] = idx
            elif "Követelmény" in text:
                header_indices["requirement"] = idx
            elif "Oktatók" in text:
                header_indices["teachers"] = idx
            elif "Kijelölés" in text:
                header_indices["selection"] = idx
        
        # Check if we have the minimum required columns
        required_cols = ["course_code", "requirement", "teachers", "selection"]
        if all(col in header_indices for col in required_cols):
            return header_indices
        
        return None
    
    def extract_courses_from_rows(self, table, header_indices: Dict[str, int], header_row_idx: int) -> List[Dict[str, Any]]:
        """
        Extract course information from table rows
        
        Args:
            table: WebElement of the course table
            header_indices: Dict mapping column names to indices
            header_row_idx: Index of the header row to skip
            
        Returns:
            List of course dictionaries
        """
        courses = []
        
        try:
            rows = table.find_elements(By.TAG_NAME, "tr")
            
            for row_idx, row in enumerate(rows):
                if row_idx <= header_row_idx:  # Skip header rows
                    continue
                
                course_data = self._extract_course_from_row(row, header_indices, row_idx)
                if course_data:
                    courses.append(course_data)
            
            self.logger.info(f"Extracted {len(courses)} valid courses from table")
            return courses
            
        except Exception as e:
            self.logger.error(f"Error extracting courses from rows: {e}")
            return []
    
    def _extract_course_from_row(self, row, header_indices: Dict[str, int], row_idx: int) -> Optional[Dict[str, Any]]:
        """
        Extract course information from a single table row
        
        Args:
            row: WebElement of the table row
            header_indices: Dict mapping column names to indices
            row_idx: Row index for logging
            
        Returns:
            Course dictionary or None if invalid
        """
        try:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) <= max(header_indices.values()):
                return None
            
            # Extract basic course information
            course_code = cells[header_indices["course_code"]].text.strip()
            course_name = cells[header_indices.get("course_name", 0)].text.strip() if "course_name" in header_indices else ""
            requirement = cells[header_indices["requirement"]].text.strip()
            teachers = cells[header_indices["teachers"]].text.strip()
            
            # Validate course according to specification requirements
            if not self._is_valid_course(course_code, requirement, teachers):
                return None
            
            # Find the dropdown menu element
            dropdown_element = self._find_dropdown_menu(cells[header_indices["selection"]])
            if not dropdown_element:
                self.logger.warning(f"Could not find dropdown menu for course {course_code}")
                return None
            
            return {
                "course_code": course_code,
                "course_name": course_name,
                "requirement": requirement,
                "teachers": teachers,
                "row_element": row,
                "dropdown_element": dropdown_element,
                "row_index": row_idx
            }
            
        except Exception as e:
            self.logger.warning(f"Error processing row {row_idx}: {e}")
            return None
    
    def _is_valid_course(self, course_code: str, requirement: str, teachers: str) -> bool:
        """
        Validate if a course meets the specification requirements
        
        Args:
            course_code: The course code to validate
            requirement: The requirement text
            teachers: The teachers text
            
        Returns:
            True if course is valid, False otherwise
        """
        # Check if course code starts with "BMEVI"
        if not course_code.startswith("BMEVI"):
            return False
        
        # Check if requirement contains "Évközi jegy"
        if "Évközi jegy" not in requirement:
            return False
        
        # Check if teachers contain "Dr. Csorba Kristóf"
        if "Dr. Csorba Kristóf" not in teachers:
            return False
        
        return True
    
    def _find_dropdown_menu(self, selection_cell):
        """
        Find the dropdown menu element in the selection cell
        
        Args:
            selection_cell: WebElement of the selection cell
            
        Returns:
            WebElement of the dropdown menu or None if not found
        """
        try:
            # Look for element with specific attributes as per specification
            dropdown_candidates = selection_cell.find_elements(By.XPATH, 
                ".//*[@class='contextcell' and @title='Lehetőségek' and @alt='Lehetőségek']")
            
            if dropdown_candidates:
                return dropdown_candidates[0]
            
            # Fallback: look for any element with contextcell class
            dropdown_candidates = selection_cell.find_elements(By.CLASS_NAME, "contextcell")
            if dropdown_candidates:
                return dropdown_candidates[0]
            
            return None
            
        except Exception as e:
            return None


class CourseValidator:
    """Responsible for validating courses according to specification"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def filter_valid_courses(self, courses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter courses to only include valid ones according to specification
        
        Args:
            courses: List of course dictionaries
            
        Returns:
            List of valid course dictionaries
        """
        valid_courses = []
        
        for course in courses:
            if self._validate_course_data(course):
                valid_courses.append(course)
        
        self.logger.info(f"Filtered {len(valid_courses)} valid courses from {len(courses)} total")
        return valid_courses
    
    def _validate_course_data(self, course: Dict[str, Any]) -> bool:
        """
        Validate a single course data dictionary
        
        Args:
            course: Course dictionary to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["course_code", "requirement", "teachers", "dropdown_element"]
        
        # Check if all required fields are present
        for field in required_fields:
            if field not in course or not course[field]:
                self.logger.debug(f"Course {course.get('course_code', 'UNKNOWN')} missing field: {field}")
                return False
        
        return True
