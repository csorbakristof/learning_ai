# ProjectLabAdmin

**Project Laboratory Session Planning Automation System**

This project automates the complete workflow for creating project laboratory presentation sessions in a web environment, from data collection to session planning and web automation.

## 🎯 Project Overview

The system automates the creation of project laboratory presentation sessions by:
1. **Collecting student topic data** from BME portal
2. **Gathering enrollment data** from Neptun system  
3. **Fusing data sources** into a unified dataset
4. **Creating Excel planning tables** for session scheduling
5. **Enabling web automation** for session creation

## 🏗️ Applications

### 1. Data Collector (`app1_data_collector`)
**Complete pipeline with 4 implemented features:**

#### ✅ DLXLS - BME Topic Data Collection
- Automated login to BME portal (www.aut.bme.hu)
- Downloads student topic assignments via "Terhelés exportálása"
- Processes Excel worksheets with topic information
- Extracts supervisor names, categories, and student data

#### ✅ DLNEP - Neptun Student Data Collection
- Automated navigation to Neptun system (neptun.bme.hu)
- Intelligent course table detection using multiple criteria
- Batch downloads of student lists from all relevant courses
- Filters by instructor ("Dr. Csorba Kristóf") and course codes ("BMEVI*")

#### ✅ DLFUSION - Data Fusion Processing
- Combines DLXLS and DLNEP data into unified JSON dataset
- Links students with course enrollments and topic information
- Provides comprehensive statistics and data validation
- Works with existing data files (no re-collection needed)

#### ✅ MKXLSX - Session Planning Excel Creation
- Creates interactive Excel table for session planning
- Planner table: 15 columns (5 weekdays × 3 rooms) × 4 time slots
- Automatic statistics with Excel formulas
- Topic category analysis and session requirements calculation

### 2. Web Automator (`app2_web_automator`)
- Framework ready for automated session creation
- Reads planning data from Excel files
- Performs automated actions on web portals using Selenium
- Handles form filling, session creation, and validation

## 🚀 Quick Start

### Complete Pipeline Execution
```powershell
# Activate virtual environment
.venv\Scripts\activate

# Run complete data collection pipeline
cd app1_data_collector
python main.py  # Executes DLXLS → DLNEP → DLFUSION → MKXLSX
```

### Individual Feature Execution
```powershell
cd app1_data_collector

# Run DLFUSION independently (lightweight, no Selenium dependencies)
python dlfusion_processor.py    # Data fusion (uses existing data files)

# Run complete workflow with all features
python main.py                  # Full pipeline with web automation

# Note: DLXLS and DLNEP require Selenium and manual login
# DLFUSION and MKXLSX work with existing data files only
```

## 📁 Project Structure

```
ProjectLabAdmin/
├── app1_data_collector/              # Data collection application
│   ├── main.py                       # Integrated workflow coordinator
│   ├── dlxls_collector.py            # BME topic data collection (DLXLS)
│   ├── dlnep_collector.py            # Neptun student data collection (DLNEP)
│   ├── dlfusion_processor.py         # Data fusion processor (DLFUSION)
│   ├── mkxlsx_creator.py             # Excel planner creator (MKXLSX)
│   └── test_*.py                     # Individual feature tests
├── app2_web_automator/               # Web automation application
│   ├── main.py                       # Web automation entry point
│   └── config.py                     # Automation configurations
├── shared/                           # Shared utilities and configurations
│   ├── __init__.py                   # Shared module initialization
│   ├── utils.py                      # Common utilities (logging, web scraping)
│   ├── config.py                     # Configuration settings
│   └── excel_handler.py              # Excel processing utilities
├── data/                             # Generated data files
│   ├── downloads/                    # BME portal downloads
│   ├── neptun_downloads/             # Neptun system downloads
│   ├── bme_topic_data.xlsx           # Processed BME topic data (DLXLS output)
│   ├── fused_student_data.json       # Combined student dataset (DLFUSION output)
│   └── session_planner.xlsx          # Session planning Excel (MKXLSX output)
├── specification/                    # Project documentation
│   ├── specification.md              # Detailed feature specifications
│   └── prompts.md                    # Development history and prompts
├── .venv/                            # Python virtual environment
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
├── QUICK_START.md                    # Quick start guide
├── InformationForAI.md               # AI agent reference
├── DLXLS_IMPLEMENTATION.md           # BME data collection documentation
├── DLFUSION_IMPLEMENTATION.md        # Data fusion documentation
└── MKXLSX_IMPLEMENTATION.md          # Excel creation documentation
```

## 📊 Data Flow Pipeline

```
BME Portal (www.aut.bme.hu)
    ↓ DLXLS
bme_topic_data.xlsx (Topic assignments, supervisors, categories)
    ↓
Neptun System (neptun.bme.hu)  
    ↓ DLNEP
neptun_downloads/*.xlsx (Course enrollments, student lists)
    ↓
DLFUSION Processing
    ↓
fused_student_data.json (Unified dataset with 435 students)
    ↓
MKXLSX Excel Creation
    ↓  
session_planner.xlsx (Interactive planning table: 60 slots)
    ↓
Web Automator → Automated session creation
```

## ✅ Features Implemented

### DLXLS - BME Topic Data Collection
- **Purpose**: Collect student topic assignments from BME portal
- **Process**: Manual login → Navigate to "Terhelés exportálása" → Download → Process
- **Output**: `data/bme_topic_data.xlsx` with topic information
- **Key Data**: Student names, Neptun codes, supervisors, topic categories
- **Test**: `python test_dlxls.py`

### DLNEP - Neptun Student Data Collection  
- **Purpose**: Download student enrollment lists from Neptun courses
- **Process**: Manual login → Find course table → Batch download all courses
- **Output**: Multiple Excel files in `data/neptun_downloads/`
- **Filtering**: Courses with "Dr. Csorba Kristóf" and "BMEVI*" course codes
- **Test**: `python test_dlnep.py`

### DLFUSION - Data Fusion Processing
- **Purpose**: Combine DLXLS and DLNEP data into unified dataset
- **Process**: Load existing files → Match by Neptun codes → Generate statistics
- **Output**: `data/fused_student_data.json` with 435 student records
- **Features**: No re-collection needed, comprehensive statistics, runs independently
- **Run**: `python dlfusion_processor.py` (no web automation dependencies required)

### MKXLSX - Session Planning Excel Creation
- **Purpose**: Create interactive Excel table for session planning
- **Process**: Load fused data → Generate planner table → Add statistics
- **Output**: `data/session_planner.xlsx` with 60 planning slots
- **Features**: Real-time Excel formulas, topic category analysis
- **Test**: `python test_mkxlsx.py`

## 🎯 Generated Files

### Core Data Files
- **`data/bme_topic_data.xlsx`**: Clean BME topic data (477 records, 416 in allowed courses)
- **`data/neptun_downloads/*.xlsx`**: Raw Neptun course enrollment files (24 files, 16 allowed courses)
- **`data/fused_student_data.json`**: Unified dataset with 435 students
- **`data/session_planner.xlsx`**: Interactive planning table with 60 slots

### Automatic File Management
- **Downloads**: Automatically moved from browser download folder to project directories
- **Processing**: Real-time data cleaning and validation during collection
- **Updates**: Each feature can be run independently without affecting others
- **Backup**: Original downloaded files preserved in respective folders

## 🚀 Usage

### Quick Complete Workflow
```powershell
cd app1_data_collector
python main.py
# Follow prompts for each feature: DLXLS → DLNEP → DLFUSION → MKXLSX
```

### Running Individual Features
```powershell
cd app1_data_collector

# DLFUSION - Data fusion (lightweight, no dependencies)
python dlfusion_processor.py

# Complete workflow (requires Selenium and manual login)
python main.py
```

### Manual Login Required
1. **DLXLS**: Manual login to BME portal required
2. **DLNEP**: Manual login to Neptun system required
3. **DLFUSION**: No login required (processes existing files, runs standalone)
4. **MKXLSX**: No login required (processes existing files)

## 📋 Session Planning Workflow

1. **Data Collection** (DLXLS + DLNEP)
   - Collect topic assignments from BME portal
   - Download student lists from Neptun courses
   - 221 total students identified

2. **Data Fusion** (DLFUSION)
   - Combine both datasets by Neptun codes
   - Filter by allowed course codes (22 courses)
   - Generate comprehensive statistics (435 students)
   - Export unified JSON dataset
   - **Run standalone**: `python dlfusion_processor.py`

3. **Planning Table Creation** (MKXLSX)
   - Create Excel table with 60 planning slots
   - Add automatic Excel formulas for statistics
   - Include topic category analysis

4. **Manual Session Planning**
   - Open `session_planner.xlsx`
   - Use dropdown menus to assign students to slots
   - Monitor real-time statistics updates

5. **Future Automation** (App2)
   - Export finalized assignments
   - Automatically create calendar events
   - Send notifications to students

## 🛠️ Technical Implementation

### Data Collection Architecture
- **Chrome WebDriver**: Automated browser control with headless options
- **Download Management**: Automatic file detection and organization
- **Error Handling**: Robust retry mechanisms and fallback strategies
- **Session Management**: Persistent login states across operations

### Excel Processing Features
- **Multi-sheet Support**: Read and write complex Excel structures
- **Formula Integration**: Automatic Excel formula generation for statistics
- **Data Validation**: Real-time validation during collection and processing
- **Format Preservation**: Maintain original formatting where possible

### Configuration System
- **Modular Configuration**: Separate configs for each feature
- **Environment Variables**: Secure credential management
- **Flexible Selectors**: CSS and XPath selector support
- **Timing Controls**: Configurable wait times and timeouts

## ⚙️ Dependencies

### Core Dependencies
- **selenium**: Web browser automation (4.22.0+)
- **requests**: HTTP requests and API calls
- **beautifulsoup4**: HTML parsing and extraction
- **openpyxl**: Excel file operations and formatting
- **pandas**: Data manipulation and analysis
- **webdriver-manager**: Automatic Chrome driver management
- **python-dotenv**: Environment variable management
- **colorlog**: Colored console logging

### System Requirements
- **Python**: 3.9+ (tested with 3.13.3)
- **Chrome Browser**: Latest version for Selenium automation
- **Windows**: Tested on Windows with PowerShell
- **Memory**: 4GB+ recommended for large dataset processing

## 📊 Current Statistics

### Data Collection Results
- **BME Topics**: 477 students with topic data (filtered to 416 in allowed courses)
- **Neptun Courses**: 24 courses processed (BMEVI prefix, filtered to 16 allowed)
- **Total Students**: 435 unique students identified in fused dataset
- **Data Fusion**: 192 students with both topics and enrollments
- **Planning Slots**: 60 session slots generated in Excel

### Performance Metrics
- **DLXLS**: ~2-3 minutes (manual login + automated processing)
- **DLNEP**: ~3-5 minutes (manual login + batch downloads)
- **DLFUSION**: <5 seconds (lightweight, no dependencies, processes existing files)
- **MKXLSX**: <15 seconds (Excel generation only)

## 🔄 Next Steps

### Immediate Development
1. **Enhanced Error Handling**: More robust network failure recovery
2. **Configuration UI**: Web interface for settings management
3. **Data Validation**: Advanced validation rules for collected data
4. **Export Options**: Multiple output formats (CSV, JSON, XML)

### Future Features (App2)
1. **Automated Session Creation**: Calendar integration
2. **Student Notifications**: Email/SMS automation
3. **Progress Tracking**: Real-time session monitoring
4. **Report Generation**: Automated analytics and insights

## 📝 Documentation

### Implementation Guides
- **`DLXLS_IMPLEMENTATION.md`**: BME data collection details
- **`DLFUSION_IMPLEMENTATION.md`**: Data fusion architecture
- **`MKXLSX_IMPLEMENTATION.md`**: Excel creation specifications
- **`QUICK_START.md`**: Step-by-step setup and usage guide
- **`InformationForAI.md`**: AI agent development reference

### Specifications
- **`specification/specification.md`**: Complete feature requirements
- **`specification/prompts.md`**: Development history and context

## 🤝 Support

For issues or questions:
1. Check the relevant implementation documentation
2. Review the test scripts for usage examples
3. Check logs in the console output for detailed error information
4. Ensure all dependencies are properly installed in the virtual environment

---

**Project Status**: ✅ All core features implemented and tested  
**Last Updated**: 2024-12-19  
**Version**: 1.0.0 - Complete automated laboratory session planning system
