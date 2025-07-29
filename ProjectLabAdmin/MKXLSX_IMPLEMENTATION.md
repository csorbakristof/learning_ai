# MKXLSX Feature Implementation

## Overview

The MKXLSX feature successfully creates an Excel table for session planning using the fused data from DLFUSION. The Excel file contains two main sections: a planner table for user input and automatic statistics calculations.

## Features Implemented

### ✅ Planner Table Structure
- **Columns**: 15 columns representing all weekday-room combinations
  - Weekdays: Monday, Tuesday, Wednesday, Thursday, Friday (5 days)
  - Rooms: QB203, QBF14, QBF15 (3 rooms)
  - Total: 5 × 3 = 15 columns
- **Rows**: 4 time slots as specified
  - 8:00-10:00
  - 10:00-12:00
  - 12:00-14:00
  - 14:00-16:00
- **Total Planning Slots**: 60 (15 columns × 4 rows)

### ✅ Session Types Support
- **Standard Types**: SW, HW, ENG, GEN, ONLINE, SPARE, NONE
- **Special Types**: ROBONAUT, AI (as mentioned in specification)
- **Custom Types**: Support for any additional session type codes

### ✅ Statistics Section
Two types of statistics as per specification:

#### 1. Topic Category Statistics
- Shows number of students per topic category
- Calculates required sessions (assuming 9 students per session)
- **Course Filtering**: Only counts students enrolled in the 13 specified statistics course codes
- Separates English and Hungarian topics according to specification
- Includes totals row
- Based on filtered DLFUSION data

#### 2. Session Type Statistics  
- Uses Excel COUNTIF formulas to count session types in planner table
- Updates automatically when user modifies the planner
- Includes descriptions for each session type  
- Covers all standard and special session types

### ✅ Course Filtering for Statistics
According to updated specification, statistics only consider students enrolled in:
- BMEVIAUMT00, BMEVIAUMT10, BMEVIAUMT12, BMEVIAUM026
- BMEVIAUAL01, BMEVIAUAL03, BMEVIAUAL04, BMEVIAUAL05
- BMEVIAUML10, BMEVIAUML12, BMEVIAUML11, BMEVIAUML13
- BMEVIAUM039

This ensures statistics accurately reflect the relevant student population for planning purposes.

### ✅ Excel Formatting
- Professional styling with colors and borders
- Clear section headers and instructions
- Appropriate column widths and row heights
- User-friendly layout with merged cells for titles

## Test Results

### ✅ Successful Implementation
- **Total Students**: 221 students processed from DLFUSION
- **Students with Topics**: 10 students
- **Required Sessions**: 2 sessions (based on 9 students per session)
- **Planning Capacity**: 60 available time slots

### 📊 Topic Categories Processed
- **Nincs megadva**: 8 students (1 session required)
- **Szoftver**: 2 students (1 session required)

### 📅 Planner Table Specifications
- **Time Slots**: 4 (as per specification)
- **Weekdays**: 5 (Monday to Friday)
- **Rooms**: 3 (QB203, QBF14, QBF15)
- **Total Slots**: 60 available planning positions

## File Structure

```
app1_data_collector/
├── mkxlsx_creator.py              # Main MKXLSX implementation
├── test_mkxlsx.py                 # Standalone test script
├── test_workflow.py               # Integrated workflow test
└── main.py                        # Updated to include MKXLSX in workflow
```

## Usage

### Method 1: Standalone Testing
```bash
cd app1_data_collector
python test_mkxlsx.py
```

### Method 2: Integrated Workflow Testing
```bash
cd app1_data_collector
python test_workflow.py
```

### Method 3: Through Main Application
```python
from mkxlsx_creator import SessionPlannerExcelCreator

creator = SessionPlannerExcelCreator()
success = creator.process_mkxlsx()
```

## Excel File Structure

### Upper Section: Session Planner Table
```
| Time Slot  | Mon QB203 | Mon QBF14 | Mon QBF15 | ... | Fri QBF15 |
|------------|-----------|-----------|-----------|-----|-----------|
| 8:00-10:00 |           |           |           | ... |           |
| 10:00-12:00|           |           |           | ... |           |
| 12:00-14:00|           |           |           | ... |           |
| 14:00-16:00|           |           |           | ... |           |
```

### Lower Section: Statistics
```
TOPIC CATEGORY STATISTICS
| Category      | Students | Required Sessions |
|---------------|----------|------------------|
| Nincs megadva |    8     |        1         |
| Szoftver      |    2     |        1         |
| TOTAL         |   10     |        2         |

SESSION TYPE STATISTICS  
| Session Type | Count in Planner | Description                    |
|--------------|------------------|--------------------------------|
| SW           | =COUNTIF(...)    | Software session              |
| HW           | =COUNTIF(...)    | Hardware and software session |
| ENG          | =COUNTIF(...)    | English course presentation   |
| GEN          | =COUNTIF(...)    | Generic session for all types |
| ONLINE       | =COUNTIF(...)    | Online generic session        |
| SPARE        | =COUNTIF(...)    | Spare time slot for later use |
| NONE         | =COUNTIF(...)    | Not used timeslot             |
| ROBONAUT     | =COUNTIF(...)    | Special ROBONAUT session      |
| AI           | =COUNTIF(...)    | Special AI session            |
```

## Key Advantages

1. **Specification Compliant**: Implements all requirements from the updated specification
2. **Dynamic Formulas**: Uses Excel COUNTIF formulas for automatic updates
3. **User Friendly**: Clear layout with instructions and professional formatting
4. **Flexible**: Supports both standard and custom session types
5. **Data-Driven**: Uses actual DLFUSION data for accurate statistics
6. **Integrated**: Seamlessly works with the complete data collection workflow

## Integration with Complete Workflow

The MKXLSX feature is now fully integrated into the main data collector workflow:

1. **DLXLS** → Collect BME topic data
2. **DLNEP** → Collect Neptun enrollment data  
3. **DLFUSION** → Combine and fuse the data
4. **MKXLSX** → Create Excel table for session planning ✅

## Next Steps

The Excel file is ready for:
1. **Manual Planning**: User fills in session types in the planner table
2. **Web Automation**: The completed Excel file can be used by the Web Automator application
3. **Session Creation**: Automated creation of sessions in the web portal

## Output Files

- **Input**: `data/fused_student_data.json` (from DLFUSION)
- **Output**: `data/session_planner.xlsx` (Excel file for planning)
- **Size**: ~6KB Excel file with full functionality
