# Project overview

This project aims to download university course statistics from a website and merge them into a cumulative statistics. The main question to answer is how the student count on each course is evolving over time.

In the followings, every section/subsection is a separate feature. The code name we will use to address it appears at the beginning of the title in brackets like [DL].

Use Python and Selenium to implement this project.

# Data source

# [DL] Downloading the excel files

The data are stored in excel files which can be downloaded from a website. The URL has the form 
https://www.aut.bme.hu/Tasks/TaskGradeExport.aspx?SemesterId=30
where the SemesterID is an integer from 1 to the index of the current semester.

As the website requires login, the script should launch a browser and navigate to the URL https://www.aut.bme.hu/Tasks/TaskManagement.aspx .
But then, it should wait for the user to login. In the console, the script should wait for an Enter key from the user to confirm successful login. Then, it can iterate along all SemesterId values (appearing in the URL above) and download all the excel files. These will be called the source excel files.

Rename the downloaded Excel files to reflect the SemesterId as "PortalResults_SemesterIdXX.xlsx" where XX stands for the SemesterId value. If the file already exists, do not download it again.

# [XLS2JSON] Extracting the data from the excel files

This step extracts the data from the souce excel files from above and merges them into a new Excel file on a worksheet called "AllSemesterData". If it already exists, overwrite it.

The source excel files contain a table with some other rows before and after it. The Semester name (referred to as SemesterName) is stored in the A1 cell between citation marks like "2025-2026 ősz" in the form:
"2025-2026 ősz" félév - téma osztályzatok

The table header is in row 4. We will need the following columns (with known column index):
- Column B: StudentNeptunCode
- Column C: CourseName
- Column D: CourseNeptunCode
- Column E: Grade
- Column F: GradedBy

After the table there may be rows with merged cells, make the script resilient to that issue.

Collect all these data from all the source excel tables and export them into a single Excel file with the following columns:

- Column A: SemesterName
- Column B: SemesterId
- Column C: StudentNeptunCode
- Column D: CourseName
- Column E: CourseNeptunCode
- Column F: Grade
- Column G: GradedBy
- Column H: CourseAlias
- Column I: CoursesSemesterIndex

Add the records by increasing SemesterId.

CourseAlias and CoursesSemesterIndex is assigned via a lookup based on CourseNeptunCode.
The lookup table is located in the excel file "CourseAlieses.xlsx". If a Neptun code is missing, show an error message with it and stop. If CourseAlias is "NA", skip that row from the resulting Excel file.

The name of the resulting Excel table should be AllSemesterProjectStats.xlsx

# [CourseHeadCountMatrix] Statistics matrix

On a separate worksheet (called CourseHeadCounts) in the resulting XLSX create a matrix with the following statistics:
- Rows should be the SemesterName
- Columns should be the CoursesSemesterIndex
- Cell values should be the number of rows in AllSemesterData belonging to this SemesterName and CourseAlias.

In this worksheet insert a graph showing the semester name as the horizontal axis and the student counts for every CourseAlies stacked over each other (stacked column chart). The title should be "Evolution of headcounts".

- [PopulationTimeslines] Population timelines

Create a worksheet called PopulationTimelines where you copy the data from the CourseHeadCountMatrix, but
- use SemesterId instead of SemesterName, and
- every row is shifted with a different N number of cells. After the SemesterId, add N empty cells before the data, where N is the maximal SemesterId minus the current SemesterId of the row. See the following example:

Original table:

SemesterId  | 6 | 7 | 8
1           | 1 | 2 | 3
2           | 4 | 5 | 6
3           | 7 | 8 | 9

New table:

SemesterId  | 6 | 7 | 8 |   |  
1           |   |   | 1 | 2 | 3
2           |   | 4 | 5 | 6 |  
3           | 7 | 8 | 9 |   |  

# Answers on the clarification questions of the AI

## Project Structure & Setup
1. **Where should the downloaded source Excel files be stored?** 
Store the files just beside the script in a "downloads/" subdirectory.

2. **Output file location**:
Store output in a subdirectory called "output/".

3. **Browser preference**:
Prefer Chrome to be used by Selenium.

## Download Feature [DL]
4. **SemesterId range**:
Start from 1 and the script should detect when downloads fail (404/invalid semester) and stop there.

6. **Duplicate handling**:
If the script is run multiple times, it should only re-download the new files. Do not clean the "downloads/" directory before starting.

## Data Extraction Feature [XLS2JSON]
7. **Table end detection**:
The script should stop at the first empty row.

8. **Data validation**:
No data validation is needed. When Grade and GradedBy is missing or contains only "-", skip that row.

9. **Processing mode**:
When running [XLS2JSON], it should it process all files in the downloads folder. And it should overwrite existing output files if they exist.

## General
10. **Error handling**:
If there is any error, the script should inform the user and stop.

11. **Progress feedback**:
The script should display progress information (e.g., "Downloading semester 5/30...", "Processing file 3/15...")?
