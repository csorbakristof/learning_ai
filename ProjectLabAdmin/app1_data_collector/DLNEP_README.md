# DLNEP - Neptun Student Data Collection Feature

## Overview

The DLNEP feature implements automated collection of student data from all courses in the Neptun system (neptun.bme.hu). This feature is part of the Data Collector application and handles the following workflow:

1. **Login to Neptun** - Opens browser and waits for manual login
2. **Navigate to Courses** - Goes to the courses list page
3. **Extract Course List** - Identifies all available courses
4. **For Each Course**:
   - Click the dropdown menu ("Lehetőségek")
   - Select "Jegybeírás" to access course details
   - Find and click "Exportálás Excel-fájlba" button
   - Download the student list Excel file
5. **Process All Data** - Combines student data from all courses
6. **Save Results** - Saves consolidated student data to Excel file

## Usage

### Command Line
```powershell
cd app1_data_collector
E:/_AI_projects/ProjectLabAdmin/.venv/Scripts/python.exe test_dlnep.py
```

### Batch File
Double-click `test_dlnep.bat` in the `app1_data_collector` folder.

### Integrated with Main Application
The DLNEP feature is automatically included when running the main data collector:
```powershell
E:/_AI_projects/ProjectLabAdmin/.venv/Scripts/python.exe main.py
```

## Manual Steps Required

1. **Login Process**: When the browser opens, you need to:
   - Enter your Neptun credentials
   - Complete any 2FA if required
   - Wait for successful login
   - Press Enter in the console to continue

2. **Automated Processing**: The application will then:
   - Navigate to the courses list page
   - Identify all available courses
   - For each course, download the student list automatically
   - Process and combine all student data

## Configuration

Edit `app1_data_collector/config.py` to modify Neptun settings:

```python
NEPTUN_CONFIG = {
    'login_url': 'https://neptun.bme.hu/oktatoi/login.aspx',
    'courses_url': 'https://neptun.bme.hu/oktatoi/main.aspx?ismenuclick=true&ctrl=1902',
    'dropdown_alt_text': 'Lehetőségek',
    'grades_menu_text': 'Jegybeírás',
    'export_button_alt': 'Exportálás Excel-fájlba',
    'download_timeout': 30  # seconds
}
```

## Output Files

### Downloaded Files
- **Location**: `data/neptun_downloads/`
- **Format**: Multiple Excel files (.xlsx or .xls)
- **Content**: Raw student lists from each course

### Processed File
- **Location**: `data/neptun_student_data.xlsx`
- **Format**: Consolidated Excel file
- **Content**: Combined student data from all courses

### Main Output
- **Location**: `data/scraped_data.xlsx` (when run with main application)
- **Content**: Combined data from all collection sources (DLXLS + DLNEP)

## Data Structure

The processed data includes:
- Student names and IDs
- Course codes and names
- Enrollment information
- Additional metadata from Neptun
- Source course and file tracking

Sample output structure:
```json
[
    {
        "student_name": "John Doe",
        "student_id": "ABC123",
        "course_code": "VIAUAL04",
        "course_name": "Independent Laboratory",
        "source_course": "VIAUAL04",
        "source_file": "course_export.xlsx",
        ...
    }
]
```

## Automation Features

### Multi-Course Processing
- **Automatic Discovery**: Finds all courses in the system
- **Batch Processing**: Downloads student lists from all courses
- **Progress Tracking**: Reports progress for each course
- **Error Recovery**: Continues processing if individual courses fail

### Navigation Management
- **Smart Dropdown Detection**: Multiple strategies to find course options
- **Menu Navigation**: Handles dropdown menus and navigation
- **Page State Management**: Returns to course list after each download
- **Download Coordination**: Manages multiple file downloads

## Error Handling

The feature includes comprehensive error handling for:
- **Login failures** - Clear error messages and retry options
- **Course detection** - Fallback methods for different page layouts
- **Navigation issues** - Recovery from menu interaction failures
- **Download problems** - Timeout handling and file validation
- **File processing** - Robust Excel file reading with error recovery

## Troubleshooting

### Common Issues

1. **Courses not found**
   - Check if you're logged in correctly
   - Verify the courses page loaded completely
   - The page structure might have changed - check logs for details

2. **Dropdown menu not working**
   - Ensure JavaScript is enabled
   - Check for page load timing issues
   - Try refreshing the courses page manually

3. **"Jegybeírás" option not found**
   - Verify you have access to grade entry for courses
   - Check user permissions in Neptun
   - The menu text might have changed

4. **Export button not found**
   - Confirm you're on the correct course page
   - Check if Excel export is enabled for the course
   - Look for alternative export options

5. **Download failures**
   - Increase `download_timeout` in config
   - Check browser download settings
   - Ensure sufficient disk space

### Debug Information

The application provides detailed logging including:
- Course discovery process and results
- Navigation steps and outcomes  
- Download progress and file validation
- Error details with context

### Performance Considerations

- **Processing Time**: Depends on number of courses (typically 1-2 minutes per course)
- **Network Usage**: Downloads multiple Excel files
- **Browser Memory**: May increase with number of courses
- **File Storage**: Each course generates a separate Excel file

## Integration Notes

The DLNEP feature integrates with other data collection features:
- **DLXLS** - BME topic data collection (already implemented)
- **FUSION** - Data fusion from multiple sources (to be implemented)
- **MKXLSX** - Excel table creation for session planning (to be implemented)

The collected student data provides enrollment information that complements the topic data from DLXLS.

## Security Considerations

- **Credentials**: Never stored - manual login required each time
- **Downloads**: Saved to local folder, organized by course
- **Browser**: Runs in normal mode to support complex Neptun interface
- **Data**: Processed locally, no external transmission
- **Privacy**: Student data handled according to BME policies

## File Structure
```
app1_data_collector/
├── dlnep_collector.py         # Main DLNEP implementation  
├── test_dlnep.py             # Standalone test script
├── test_dlnep.bat            # Easy test execution
├── config.py                 # Updated with Neptun settings
└── main.py                   # Integrated with main app

data/
├── neptun_downloads/         # Individual course files
└── neptun_student_data.xlsx  # Consolidated student data
```

## Workflow Integration

1. **DLXLS** collects topic categories and student-topic assignments
2. **DLNEP** collects complete enrollment data from all courses  
3. **FUSION** will combine both data sources for complete picture
4. **MKXLSX** will use combined data to generate session planning template

This creates a comprehensive data collection system for the project laboratory session planning workflow.
