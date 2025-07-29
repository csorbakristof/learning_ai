# InformationForAI.md

## 🤖 AI Agent Quick Reference for ProjectLabAdmin

This document provides a comprehensive overview for AI agents to quickly understand the ProjectLabAdmin codebase without needing to read all source files.

## 🎯 Project Purpose

**Project Laboratory Session Planning Automation**
- Automates data collection from BME portal and Neptun system
- Combines student enrollment and topic data 
- Creates Excel planning tables for scheduling presentation sessions
- Prepares data for web automation of session creation

## 🏗️ Architecture Overview

### Core Components
```
app1_data_collector/        # Main application - 4 features implemented
├── dlxls_collector.py      # BME topic data collection
├── dlnep_collector.py      # Neptun student enrollment collection  
├── dlfusion_processor.py   # Data fusion and combination
├── mkxlsx_creator.py       # Excel planner table creation
├── main.py                 # Integrated workflow coordinator
└── test_*.py               # Individual feature tests

app2_web_automator/         # Web automation (framework ready)
shared/                     # Common utilities and configurations
data/                       # Generated data files and downloads
```

### Data Flow Pipeline
```
1. DLXLS: BME Portal → bme_topic_data.xlsx
2. DLNEP: Neptun System → neptun_downloads/*.xlsx
3. DLFUSION: Combined data → fused_student_data.json  
4. MKXLSX: Planning Excel → session_planner.xlsx
5. Web Automator: Excel input → Automated session creation
```

## 🔧 Implementation Status

### ✅ Fully Implemented Features

**DLXLS (BME Topic Data Collection)**
- Location: `app1_data_collector/dlxls_collector.py`
- Class: `BMETopicDataCollector`
- Purpose: Scrapes student topic assignments from BME portal
- Login: Manual user login required at www.aut.bme.hu
- Output: `data/bme_topic_data.xlsx`
- Key Data: Student names, Neptun codes, supervisors, topic categories

**DLNEP (Neptun Student Data Collection)**  
- Location: `app1_data_collector/dlnep_collector.py`
- Class: `NeptunStudentDataCollector`
- Purpose: Downloads student enrollment lists from Neptun courses
- Login: Manual user login required at neptun.bme.hu
- Output: Multiple files in `data/neptun_downloads/`
- Key Features: Intelligent table detection, batch processing, course filtering

**DLFUSION (Data Fusion)**
- Location: `app1_data_collector/dlfusion_processor.py`  
- Class: `DataFusionProcessor`
- Purpose: Combines DLXLS and DLNEP data into unified dataset
- Input: Existing Excel files (no re-collection needed)
- Output: `data/fused_student_data.json`
- Key Features: Student matching by Neptun codes, comprehensive statistics

**MKXLSX (Excel Planning Table)**
- Location: `app1_data_collector/mkxlsx_creator.py`
- Class: `SessionPlannerExcelCreator`  
- Purpose: Creates interactive Excel table for session planning
- Input: DLFUSION JSON data
- Output: `data/session_planner.xlsx`
- Key Features: 15-column planner, automatic statistics with Excel formulas

## 🔍 Key Technical Details

### Data Collection Specifications

**DLXLS Data Sources:**
- URL: https://www.aut.bme.hu/StaffMembers/MyWorkload.aspx
- Action: Click "Terhelés exportálása" link
- Processing: Uses 2nd worksheet containing "konzultáció"
- Fields: Konzulens, Kategória, Téma címe, Hallgató neve, Hallg. nept

**DLNEP Data Sources:**
- URL: https://neptun.bme.hu/oktatoi/main.aspx?ismenuclick=true&ctrl=1902
- Table Detection: Multiple criteria filtering
  - Must contain "Dr. Csorba Kristóf" in instructor column
  - Course codes must start with "BMEVI"
  - Must have "Évközi jegy" in requirement column
- Process: Click dropdown → "Jegybeírás" → Set page size → Export Excel

**Data Fusion Logic:**
- Primary Key: Student Neptun codes
- Combines: Course enrollments + Topic assignments
- Output Format: JSON with metadata and student records
- Statistics: Category counts, session requirements, overlap analysis

**Excel Planning Structure:**
- Dimensions: 4 time slots × 5 weekdays × 3 rooms = 60 planning cells
- Time Slots: 8:00-10:00, 10:00-12:00, 12:00-14:00, 14:00-16:00
- Rooms: QB203, QBF14, QBF15
- Session Types: SW, HW, ENG, GEN, ONLINE, SPARE, NONE, ROBONAUT, AI

### Critical Implementation Notes

**Selenium Automation Challenges:**
- Neptun system has multiple tables - requires precise filtering
- Dynamic content loading requires appropriate wait times (2 seconds)
- Stale element references handled by re-finding elements
- Page size selector must be changed before export to avoid popups

**Data Processing Considerations:**  
- Excel files may have inconsistent formatting
- Empty course files are skipped during processing
- Student matching handles cases where students have topics but no enrollments
- Session calculations assume 9 students per session

**Error Handling Patterns:**
- Comprehensive logging with timestamps
- Graceful degradation when files are missing
- User confirmation required for manual login steps
- Automatic retry mechanisms for stale elements

## 🧪 Testing & Verification

### Test Scripts Available
- `test_dlxls.py` - BME data collection test
- `test_dlnep.py` - Neptun data collection test  
- `test_dlfusion.py` - Data fusion test
- `test_mkxlsx.py` - Excel creation test
- `test_workflow.py` - Complete integration test

### Sample Data Volumes
- **DLXLS**: ~10 students with topic assignments
- **DLNEP**: ~213 student enrollments across 6 courses
- **DLFUSION**: 221 total students, 2 students with both topic and enrollment
- **MKXLSX**: 60 planning slots, 2 required sessions

### Expected File Sizes
- `bme_topic_data.xlsx`: ~2-5KB
- Individual Neptun downloads: ~1-3KB each
- `fused_student_data.json`: ~3500 lines, comprehensive dataset
- `session_planner.xlsx`: ~6KB with formulas and formatting

## 🔧 Extension Points

### Adding New Features
- New collectors: Follow pattern in existing `*_collector.py` files
- Data processors: Extend `DataFusionProcessor` class
- Excel generators: Modify `SessionPlannerExcelCreator`
- Web automation: Configure `app2_web_automator` for session creation

### Configuration Options
- Time slots and rooms: Modify arrays in `mkxlsx_creator.py`
- Session types: Update `session_types` and `special_session_types` lists
- Data sources: Add new URLs and selectors in collector classes
- Statistics: Extend fusion processor with additional calculations

### Common Modification Patterns
- URL changes: Update in respective collector classes
- New data fields: Extend data extraction and fusion logic
- Different Excel layouts: Modify column mappings and processing
- Additional filtering: Add criteria to table detection logic

## 🚨 Critical Dependencies

### Required for Operation
- **Python Virtual Environment**: `.venv/` with all packages installed
- **Chrome Browser**: For Selenium automation
- **Manual Login Access**: User credentials for BME and Neptun systems
- **Network Access**: To BME and Neptun web portals

### File Dependencies
- **Shared Utilities**: All features use `shared/` module
- **Sequential Processing**: DLFUSION needs DLXLS/DLNEP output
- **Excel Libraries**: OpenPyXL for advanced Excel formatting
- **JSON Processing**: Standard library for data fusion output

## 🎯 AI Agent Development Guidelines

### Quick Start for AI Agents
1. **Understand the pipeline**: DLXLS → DLNEP → DLFUSION → MKXLSX
2. **Check test scripts**: They demonstrate proper usage patterns
3. **Review specification.md**: Contains detailed requirements
4. **Examine existing code**: All features are fully implemented
5. **Use logging**: All classes have comprehensive logging

### Common Tasks for AI Agents
- **Bug fixes**: Check logs, review error handling patterns
- **Feature extensions**: Follow existing class patterns
- **Configuration changes**: Modify constants in appropriate files
- **New data sources**: Create new collector classes
- **Output format changes**: Modify processor classes

### Code Quality Standards
- **Logging**: Use `setup_logging(__name__)` pattern
- **Error Handling**: Try/except with specific error messages
- **Documentation**: Docstrings for all methods
- **Testing**: Create test scripts for new features
- **Type Hints**: Use where appropriate for clarity

## 📋 Quick Command Reference

```powershell
# Activate environment
.venv\Scripts\activate

# Run complete pipeline
cd app1_data_collector
python main.py

# Test individual features  
python test_dlfusion.py    # Uses existing data
python test_mkxlsx.py      # Uses existing data
python test_workflow.py   # Complete integration test

# Manual feature execution
python -c "from dlxls_collector import BMETopicDataCollector; BMETopicDataCollector().collect_topic_data()"
```

This reference should enable any AI agent to quickly understand and work with the ProjectLabAdmin codebase without extensive source code analysis.
