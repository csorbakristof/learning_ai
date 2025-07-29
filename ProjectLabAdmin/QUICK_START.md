# ProjectLabAdmin - Quick Start Guide

## 🚀 Project Laboratory Session Planning Automation

This project automates the complete workflow for creating project laboratory presentation sessions, from data collection to session creation in web portals.

## Environment Setup Complete! ✅

Your Python environment has been successfully set up with all necessary dependencies for web scraping, data processing, and automation.

## What's Been Created

### 📁 Project Structure
```
ProjectLabAdmin/
├── app1_data_collector/           # Data collection application
│   ├── main.py                    # Main application entry point
│   ├── dlxls_collector.py         # BME topic data collection (DLXLS)
│   ├── dlnep_collector.py         # Neptun student data collection (DLNEP)  
│   ├── dlfusion_processor.py      # Data fusion processor (DLFUSION)
│   ├── mkxlsx_creator.py          # Excel planner creator (MKXLSX)
│   └── test_*.py                  # Test scripts for each feature
├── app2_web_automator/            # Web automation application
├── shared/                        # Shared utilities and configurations
├── data/                          # Generated data files
│   ├── downloads/                 # BME portal downloads
│   ├── neptun_downloads/          # Neptun system downloads
│   ├── bme_topic_data.xlsx        # Processed BME topic data
│   ├── fused_student_data.json    # Combined student data
│   └── session_planner.xlsx       # Session planning Excel file
├── .venv/                         # Python virtual environment
└── [documentation files]
```

### 🎯 Implemented Features

#### ✅ DLXLS - BME Topic Data Collection
- Automated login to BME portal (www.aut.bme.hu)
- Downloads student topic data from "Terhelés exportálása"
- Processes Excel worksheets containing topic information
- Extracts supervisor names, categories, and student assignments

#### ✅ DLNEP - Neptun Student Data Collection  
- Automated navigation to Neptun system (neptun.bme.hu)
- Intelligent course table detection using multiple criteria
- Batch downloads of student lists from all relevant courses
- Filters courses by "Dr. Csorba Kristóf" and "BMEVI" course codes

#### ✅ DLFUSION - Data Fusion
- Combines DLXLS and DLNEP data into unified JSON dataset
- Links students with their course enrollments and topic information
- Provides comprehensive statistics and data validation
- No need to re-run collections - uses existing downloaded files

#### ✅ MKXLSX - Session Planning Excel Creation
- Creates interactive Excel table for session planning
- Planner table: 15 columns (5 weekdays × 3 rooms) × 4 time slots
- Automatic statistics with Excel formulas
- Topic category analysis and session requirements calculation

### 📦 Installed Packages
- **Selenium & WebDriver Manager** - Browser automation
- **Requests & BeautifulSoup** - Web scraping  
- **OpenPyXL & Pandas** - Excel file processing
- **JSON handling** - Data fusion and storage
- **Logging & Configuration** - Robust error handling

## Quick Start

### 🚀 Complete Workflow Execution

**Option 1: Run Complete Data Collection Pipeline**
```powershell
# Activate virtual environment and run all features
.venv\Scripts\activate
cd app1_data_collector
python main.py  # Runs DLXLS → DLNEP → DLFUSION → MKXLSX
```

**Option 2: Run Individual Features**
```powershell
# Activate virtual environment
.venv\Scripts\activate
cd app1_data_collector

# Test individual features
python test_dlxls.py       # Test BME topic data collection
python test_dlnep.py       # Test Neptun student data collection  
python test_dlfusion.py    # Test data fusion (uses existing data)
python test_mkxlsx.py      # Test Excel planner creation
python test_workflow.py   # Test complete integrated workflow
```

**Option 3: Using Batch Files**
- `run_data_collector.bat` - Run the complete data collection pipeline
- `run_web_automator.bat` - Run the web automation application

### 📊 Feature-Specific Usage

#### DLXLS - BME Topic Data Collection
1. Run the feature (requires manual login to BME portal)
2. Waits for user to complete login at www.aut.bme.hu
3. Automatically navigates and downloads topic data
4. Processes and saves to `data/bme_topic_data.xlsx`

#### DLNEP - Neptun Student Data Collection  
1. Run the feature (requires manual login to Neptun)
2. Waits for user to complete login at neptun.bme.hu
3. Automatically finds course table using specification criteria
4. Downloads student lists from all matching courses
5. Saves individual Excel files to `data/neptun_downloads/`

#### DLFUSION - Data Fusion
1. **No manual intervention required**
2. Automatically loads existing DLXLS and DLNEP data
3. Combines data using Neptun codes as primary keys
4. Saves unified dataset to `data/fused_student_data.json`

#### MKXLSX - Session Planning Excel
1. **No manual intervention required**  
2. Uses DLFUSION data to create planning Excel
3. Creates interactive planner table with statistics
4. Saves to `data/session_planner.xlsx`

### 🎯 Typical Workflow
1. **Run DLXLS** - Collect BME topic data (manual login required)
2. **Run DLNEP** - Collect Neptun enrollment data (manual login required)
3. **Run DLFUSION** - Automatically combine the data
4. **Run MKXLSX** - Automatically create planning Excel
5. **Manual Planning** - Fill in session types in Excel
6. **Web Automation** - Use Web Automator for session creation

## Data Flow & Generated Files

### 📋 Complete Data Pipeline
```
BME Portal → DLXLS → bme_topic_data.xlsx
     ↓
Neptun System → DLNEP → neptun_downloads/*.xlsx  
     ↓
DLFUSION → fused_student_data.json
     ↓  
MKXLSX → session_planner.xlsx
     ↓
Web Automator → Automated session creation
```

### 📁 Generated Files Explained

**data/bme_topic_data.xlsx** (DLXLS output)
- Student topic assignments
- Supervisor information  
- Topic categories
- Ready for fusion processing

**data/neptun_downloads/*.xlsx** (DLNEP output)
- Individual course enrollment files
- Student Neptun codes and names
- Course-specific data
- Named with course codes (BMEVI*)

**data/fused_student_data.json** (DLFUSION output)
- Combined student dataset
- Course enrollments per student
- Topic information where available
- Complete metadata and statistics

**data/session_planner.xlsx** (MKXLSX output)
- Interactive planning table (15 columns × 4 rows)
- Automatic statistics with Excel formulas
- Ready for manual session type assignment
- Input for Web Automator application

### 🎯 Session Types & Planning

**Standard Session Types:**
- **SW** - Software session
- **HW** - Hardware and software session  
- **ENG** - English course presentation
- **GEN** - Generic session for all types
- **ONLINE** - Online generic session
- **SPARE** - Spare time slot for later use
- **NONE** - Not used timeslot

**Special Session Types:**
- **ROBONAUT** - Special ROBONAUT sessions
- **AI** - Special AI sessions
- **Custom codes** - Any additional session types

**Planning Structure:**
- **Time Slots**: 8:00-10:00, 10:00-12:00, 12:00-14:00, 14:00-16:00
- **Weekdays**: Monday through Friday
- **Rooms**: QB203, QBF14, QBF15
- **Total Capacity**: 60 planning slots (4 × 5 × 3)

## Testing & Debugging

### 🧪 Test Scripts Available
```powershell
# Individual feature tests
python test_dlxls.py           # Test BME data collection
python test_dlnep.py           # Test Neptun data collection  
python test_dlfusion.py        # Test data fusion
python test_mkxlsx.py          # Test Excel creation
python test_workflow.py       # Test complete integration

# Main application test
python main.py                 # Run complete pipeline
```

### 📊 Sample Test Results
```
DLFUSION Results:
• Total students: 221
• Students with topics: 10  
• Students with enrollments: 213
• Unique courses: 6

MKXLSX Results:
• Planning slots: 60
• Required sessions: 2
• Topic categories: 2
```

### 🐛 Common Issues & Solutions

**Chrome Driver Issues**
- Automatically handled by WebDriver Manager
- No manual driver management needed

**Login Timeouts**  
- Manual login required for BME and Neptun systems
- Applications wait for user confirmation
- Press Enter in console after completing login

**Element Not Found (Neptun)**
- Multiple filtering criteria implemented
- Searches for "Dr. Csorba Kristóf" text
- Validates "BMEVI" course code prefix
- Checks for required table headings

**Excel File Access**
- Close Excel files before running applications
- Generated files are automatically overwritten
- Use data backup if needed

**Virtual Environment**
- Always activate with `.venv\Scripts\activate`
- All dependencies are pre-installed
- No additional package installation needed

## Next Steps

### 🎯 Production Usage
1. **Complete Data Collection** - Run DLXLS and DLNEP features
2. **Generate Planning File** - DLFUSION and MKXLSX create session_planner.xlsx
3. **Manual Planning** - Fill in session types in Excel planner table
4. **Web Automation** - Use Web Automator for automated session creation
5. **Schedule Regular Updates** - Set up periodic data collection

### 📋 Manual Planning Process
1. Open `data/session_planner.xlsx` in Excel
2. Review topic category statistics (lower section)
3. Fill in session types in planner table (upper section):
   - Use SW, HW, ENG, GEN, ONLINE, SPARE, NONE
   - Add special types like ROBONAUT, AI as needed
4. Watch statistics update automatically via Excel formulas
5. Save completed planning file for Web Automator

### 🔧 Customization Options
- **Time Slots**: Modify time ranges in `mkxlsx_creator.py`
- **Rooms**: Update room list in `mkxlsx_creator.py`  
- **Session Types**: Add custom session types as needed
- **Data Sources**: Extend with additional data collection features
- **Web Automation**: Configure app2_web_automator for session creation

## Documentation & Support

### 📖 Available Documentation
- **README.md** - Project overview and architecture
- **specification/specification.md** - Detailed feature specifications
- **DLXLS_IMPLEMENTATION.md** - BME data collection details
- **DLFUSION_IMPLEMENTATION.md** - Data fusion documentation  
- **MKXLSX_IMPLEMENTATION.md** - Excel creation details
- **InformationForAI.md** - AI agent quick reference

### 🆘 Getting Help
- Review test scripts for usage examples
- Check implementation documentation for detailed explanations
- Examine shared utilities for advanced features
- Use logging output for debugging information

### 🎉 Project Status
**All core features implemented and tested:**
- ✅ DLXLS - BME topic data collection
- ✅ DLNEP - Neptun student data collection  
- ✅ DLFUSION - Data fusion and JSON generation
- ✅ MKXLSX - Excel session planner creation
- 🔧 Web Automator - Ready for session creation configuration

**Your environment is ready for complete project laboratory session planning automation!** 🚀
