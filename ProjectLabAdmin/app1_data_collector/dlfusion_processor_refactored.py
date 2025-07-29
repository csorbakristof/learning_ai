"""
DLFUSION - Data fusion module (Refactored)
This module combines data from DLXLS and DLNEP into a single JSON dataset.
Refactored according to SOLID principles for better maintainability.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

sys.path.append(str(Path(__file__).parent.parent))
from shared import setup_logging
from data_loaders import DLXLSDataLoader, DLNEPDataLoader, CourseCodeValidator
from data_fusion import DataFusionEngine, FusionDataValidator, FusionDataExporter


class DataFusionProcessorRefactored:
    """Refactored processor for combining DLXLS and DLNEP data"""
    
    # Course codes that should be taken into account according to specification
    ALLOWED_COURSE_CODES = {
        'BMEVIAUAL01', 'BMEVIAUAL03', 'BMEVIAUAL04', 'BMEVIAUAL05', 
        'BMEVIAUAT00', 'BMEVIAUAT01', 'BMEVIAUA019', 
        'BMEVIAUML10', 'BMEVIAUML11', 'BMEVIAUML12', 'BMEVIAUML13',
        'BMEVIAUMT00', 'BMEVIAUMT01', 'BMEVIAUMT03', 'BMEVIAUMT10', 
        'BMEVIAUMT11', 'BMEVIAUMT12', 'BMEVIAUMT13',
        'BMEVIAUM026', 'BMEVIAUM027', 'BMEVIAUM039'
    }
    
    def __init__(self):
        """Initialize the refactored data fusion processor"""
        self.logger = setup_logging(__name__)
        
        # Initialize components following Dependency Injection principle
        self.course_validator = CourseCodeValidator(self.ALLOWED_COURSE_CODES)
        self.dlxls_loader = DLXLSDataLoader(self.logger, self.course_validator)
        self.dlnep_loader = DLNEPDataLoader(self.logger, self.course_validator)
        self.fusion_engine = DataFusionEngine(self.logger)
        self.fusion_validator = FusionDataValidator(self.logger, self.ALLOWED_COURSE_CODES)
        self.data_exporter = FusionDataExporter(self.logger)
        
        # Data storage
        self.dlxls_data = []
        self.dlnep_data = []
        self.fused_data = []
    
    def process_fusion(self, dlxls_file: Optional[Path] = None, dlnep_folder: Optional[Path] = None, 
                      output_file: Optional[Path] = None) -> bool:
        """
        Process the complete data fusion workflow
        
        Args:
            dlxls_file: Path to DLXLS Excel file (defaults to data/bme_topic_data.xlsx)
            dlnep_folder: Path to DLNEP folder (defaults to data/neptun_downloads)
            output_file: Path to output JSON file (defaults to data/fused_student_data.json)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Set default paths
            if dlxls_file is None:
                dlxls_file = Path(__file__).parent.parent / "data" / "bme_topic_data.xlsx"
            if dlnep_folder is None:
                dlnep_folder = Path(__file__).parent.parent / "data" / "neptun_downloads"
            if output_file is None:
                output_file = Path(__file__).parent.parent / "data" / "fused_student_data.json"
            
            self.logger.info("Starting DLFUSION data processing...")
            
            # Step 1: Load DLXLS data
            self.dlxls_data = self.dlxls_loader.load_data(dlxls_file)
            
            # Step 2: Load DLNEP data
            self.dlnep_data = self.dlnep_loader.load_data(dlnep_folder)
            
            # Step 3: Validate course coverage
            self.fusion_validator.validate_course_coverage(self.dlxls_data, self.dlnep_data)
            
            # Step 4: Perform data fusion
            self.fused_data = self.fusion_engine.fuse_data(self.dlxls_data, self.dlnep_data)
            
            if not self.fused_data:
                self.logger.error("Data fusion resulted in empty dataset")
                return False
            
            # Step 5: Export to JSON
            success = self.data_exporter.save_to_json(
                self.fused_data, 
                len(self.dlxls_data), 
                len(self.dlnep_data),
                output_file
            )
            
            if success:
                self.logger.info("DLFUSION processing completed successfully")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error in DLFUSION processing: {e}")
            return False
    
    def get_fusion_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the fusion results
        
        Returns:
            Dictionary containing fusion statistics
        """
        if not self.fused_data:
            return {'error': 'No fused data available'}
        
        return self.fusion_validator.analyze_fusion_results(self.fused_data)
    
    def get_sample_data(self, count: int = 3) -> List[Dict[str, Any]]:
        """
        Get sample student data for display
        
        Args:
            count: Number of sample records to return
            
        Returns:
            List of sample student records
        """
        return self.fused_data[:count] if self.fused_data else []


def main():
    """Main function for testing the refactored DLFUSION processor"""
    processor = DataFusionProcessorRefactored()
    
    print("🚀 Starting DLFUSION data processing...")
    success = processor.process_fusion()
    
    if success:
        print("✅ Data fusion completed successfully!")
        
        # Show summary
        summary = processor.get_fusion_summary()
        print(f"📊 Fusion Summary:")
        print(f"   • Total students: {summary['total_students']}")
        print(f"   • Students with topics: {summary['students_with_topics']}")
        print(f"   • Students with enrollments: {summary['students_with_enrollments']}")
        print(f"   • Students with both: {summary['students_with_both']}")
        print(f"   • Unique courses: {summary['unique_courses']}")
        print(f"   • English courses: {summary['english_courses']}")
        print(f"   • Hungarian courses: {summary['hungarian_courses']}")
        print(f"   • Students in English courses: {summary['students_in_english_courses']}")
        
        # Show sample data
        sample_data = processor.get_sample_data()
        if sample_data:
            print(f"📋 Sample student data:")
            for idx, student in enumerate(sample_data, 1):
                courses_count = len(student.get('enrolled_courses', []))
                topic_status = "Has topic" if student.get('has_topic') else "No topic"
                print(f"   {idx}. {student['student_name']} ({student['student_neptun']})")
                print(f"      • Courses: {courses_count}")
                print(f"      • Topic: {topic_status}")
                
                # Show enrolled courses
                if student.get('enrolled_courses'):
                    print(f"      • Enrolled courses:")
                    for course in student['enrolled_courses']:
                        lang = "English" if course.get('is_english') else "Hungarian"
                        print(f"        - {course['course_code']} ({lang})")
        
    else:
        print("❌ Data fusion failed!")


if __name__ == "__main__":
    main()
