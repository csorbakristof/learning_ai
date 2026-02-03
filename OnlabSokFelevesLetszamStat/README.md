# University Course Statistics Downloader and Merger

This project downloads university course statistics from the AUT BME website and merges them into a cumulative statistics file to track student count evolution over time.

## Features

- **[DL] Download Excel Files**: Automatically downloads course statistics Excel files for all available semesters
- **[XLS2JSON] Extract and Merge Data**: Processes all downloaded files, looks up course aliases, and creates a consolidated Excel output
- **[CourseHeadCountMatrix] Statistics Matrix**: Creates a matrix showing student counts by semester and course with a stacked column chart
- **[PopulationTimelines] Population Timelines**: Creates a time-shifted view of the data to visualize progression patterns

## Requirements

- Python 3.7+
- Chrome browser installed
- Active internet connection
- Valid credentials for the AUT BME website

## Installation

1. Clone or navigate to this directory

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

The required packages are:
- `selenium`: For browser automation
- `openpyxl`: For Excel file processing
- `webdriver-manager`: For automatic Chrome driver management

## Usage

### Run Complete Pipeline

To download and process all files in one go:

```bash
python main.py
```

This will:
1. Clean the `downloads/` folder
2. Open Chrome browser for you to login
3. Download all available semester files
4. Process and merge them into `output/AllSemesterProjectStats.xlsx`

### Run Individual Modules

You can also run each module separately:

**Download only:**
```bash
python downloader.py
```

**Extract and merge only (after downloading):**
```bash
python extractor.py
```

## How It Works

### Download Process [DL]

1. Creates `downloads/` folder if it doesn't exist (preserves existing files)
2. Opens Chrome browser and navigates to https://www.aut.bme.hu/Tasks/TaskManagement.aspx for login
3. Waits for you to manually login (press ENTER after login)
4. Iterates through all semester IDs (starting from 1) downloading from TaskGradeExport.aspx URLs
5. Renames downloaded files to `PortalResults_SemesterIdXX.xlsx`
6. Skips download if file already exists (incremental download)
7. Stops when it detects 3 consecutive failures (indicating no more semesters)

### Extraction Process [XLS2JSON]

1. Reads all Excel files from `downloads/` folder
2. Loads course aliases from `CourseAliases.xlsx`
3. Extracts semester name from cell A1 (between quotes)
4. Reads data from row 5 onwards (row 4 is header)
5. Collects columns: StudentNeptunCode, CourseName, CourseNeptunCode, Grade, GradedBy
6. Looks up CourseAlias and CoursesSemesterIndex for each CourseNeptunCode (stops with error if not found)
7. **Filters out rows where CourseAlias is "NA"**
8. Skips rows where Grade or GradedBy is missing or contains only "-"
9. Stops at the first empty row
10. Merges all data into worksheet "AllSemesterData" in `output/AllSemesterProjectStats.xlsx`

### Statistics Matrix [StatMatrix]

1. Creates a "CourseHeadCounts" worksheet in the output file
2. Generates a matrix with:
   - Rows: Semester names
   - Columns: CoursesSemesterIndex values
   - Values: Count of students in each semester/course combination
3. Adds a stacked column chart titled "Evolution of headcounts"
4. Chart shows semester progression with all courses stacked

### Population Timelines [PopulationTimelines]

1. Creates a "PopulationTimelines" worksheet in the output file
2. Generates a time-shifted matrix to visualize progression patterns:
   - Rows: SemesterIds (instead of semester names)
   - Columns: CoursesSemesterIndex values (same as CourseHeadCounts)
   - Each row is shifted right by N cells, where N = (max SemesterId - current row's SemesterId)
   - This creates a diagonal pattern showing how courses align across time
3. Helps visualize temporal relationships between semesters and courses

## Output Format

The output file `AllSemesterProjectStats.xlsx` contains three worksheets:

### Worksheet 1: AllSemesterData

Data is sorted by SemesterId in ascending order.

| Column A | Column B | Column C | Column D | Column E | Column F | Column G | Column H | Column I |
|----------|----------|----------|----------|----------|----------|----------|----------|----------|
| SemesterName | SemesterId | StudentNeptunCode | CourseName | CourseNeptunCode | Grade | GradedBy | CourseAlias | CoursesSemesterIndex |

### Worksheet 2: CourseHeadCounts

A matrix showing student counts with:
- Rows: Semester names
- Columns: CoursesSemesterIndex values
- Values: Number of students

Plus a stacked column chart visualizing the evolution of headcounts over time.

### Worksheet 3: PopulationTimelines

A time-shifted matrix showing student counts with:
- Rows: SemesterIds
- Columns: CoursesSemesterIndex values (with shifts applied)
- Values: Number of students
- Each row is shifted right to create a diagonal alignment pattern

This view helps identify temporal patterns and course progression relationships.

## Directory Structure

```
OnlabSokFelevesLetszamStat/
├── main.py                 # Main orchestration script
├── downloader.py           # Download module [DL]
├── extractor.py            # Extraction module [XLS2JSON] and statistics [StatMatrix]
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── spec.md                # Project specification
├── CourseAliases.xlsx     # Course alias lookup table
├── downloads/             # Downloaded Excel files (auto-created)
└── output/               # Merged output file (auto-created)
```

## Troubleshooting

**Chrome driver issues:**
- The script uses `webdriver-manager` to automatically download the correct Chrome driver
- Make sure Chrome browser is installed and up to date

**Download timeout:**
- If downloads are slow, the script waits up to 30 seconds per file
- Check your internet connection if timeouts occur

**Login issues:**
- Make sure to complete the login process before pressing ENTER
- The script will wait indefinitely for you to confirm login

**No files downloaded:**
- Check that the base URL is correct
- Verify your login credentials
- Ensure you have access to the course statistics

**Missing course alias error:**
- Check that `CourseAliases.xlsx` exists in the project directory
- Verify that all CourseNeptunCodes in the downloaded data have corresponding entries
- Add missing entries to `CourseAliases.xlsx` if needed

## Error Handling

The script will stop and display an error message if:
- Network connection fails
- Excel files are malformed
- Required data cannot be extracted
- Any unexpected error occurs

All errors are displayed in the console with descriptive messages.
