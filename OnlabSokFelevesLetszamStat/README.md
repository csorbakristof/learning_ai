# University Course Statistics Downloader and Merger

This project downloads university course statistics from the AUT BME website and merges them into a cumulative statistics file to track student count evolution over time.

## Features

- **[DL] Download Excel Files**: Automatically downloads course statistics Excel files for all available semesters
- **[XLS2JSON] Extract and Merge Data**: Processes all downloaded files, looks up course aliases, and creates a consolidated Excel output
- **[StatMatrix] Statistics Matrix**: Creates a matrix showing student counts by semester and course with a stacked column chart

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

1. The script cleans the `downloads/` folder
2. Opens Chrome browser and navigates to the first semester URL
3. Waits for you to manually login (press ENTER after login)
4. Iterates through all semester IDs (starting from 1)
5. Downloads Excel files for each semester
6. Stops when it detects 3 consecutive failures (indicating no more semesters)

### Extraction Process [XLS2JSON]

1. Reads all Excel files from `downloads/` folder
2. Loads course aliases from `CourseAliases.xlsx`
3. Extracts semester name from cell A1 (between quotes)
4. Reads data from row 5 onwards (row 4 is header)
5. Collects columns: StudentNeptunCode, CourseName, CourseNeptunCode, Grade, GradedBy
6. Looks up CourseAlias for each CourseNeptunCode (stops with error if not found)
7. Skips rows where Grade or GradedBy is missing or contains only "-"
8. Stops at the first empty row
9. Merges all data into worksheet "AllSemesterData" in `output/AllSemesterProjectStats.xlsx`

### Statistics Matrix [StatMatrix]

1. Creates a "CourseHeadCounts" worksheet in the output file
2. Generates a matrix with:
   - Rows: Semester names
   - Columns: Course aliases
   - Values: Count of students in each semester/course combination
3. Adds a stacked column chart titled "Evolution of headcounts"
4. Chart shows semester progression with all courses stacked

## Output Format

The output file `AllSemesterProjectStats.xlsx` contains two worksheets:

### Worksheet 1: AllSemesterData

| Column A | Column B | Column C | Column D | Column E | Column F | Column G |
|----------|----------|----------|----------|----------|----------|----------|
| SemesterName | StudentNeptunCode | CourseName | CourseNeptunCode | Grade | GradedBy | CourseAlias |

### Worksheet 2: CourseHeadCounts

A matrix showing student counts with:
- Rows: Semester names
- Columns: Course aliases
- Values: Number of students

Plus a stacked column chart visualizing the evolution of headcounts over time.

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
