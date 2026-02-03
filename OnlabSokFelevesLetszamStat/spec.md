# Project overview

This project aims to download university course statistics from a website and merge them into a cumulative statistics. The main question to answer is how the student count on each course is evolving over time.

In the followings, every section/subsection is a separate feature. The code name we will use to address it appears at the beginning of the title in brackets like [DL].

Use Python and Selenium to implement this project.

# Data source

# [DL] Downloading the excel files

The data are stored in excel files which can be downloaded from a website. The URL has the form 
https://www.aut.bme.hu/Tasks/TaskGradeExport.aspx?SemesterId=30
where the SemesterID is an integer from 1 to the index of the current semester.
As the website requires login, the script should launch a browser and navigate to the first URL to download. But then, it should wait for the user to login. In the console, the script should wait for an Enter key from the user to confirm successful login. Then, it can iterate along all SemesterId values (appearing in the URL above) and download all the excel files. These will be called the source excel files.

# [XLS2JSON] Extracting the data from the excel files

This step extracts the data from the souce excel files from above and merges them into a new Excel file.

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
- Column B: StudentNeptunCode
- Column C: CourseName
- Column D: CourseNeptunCode
- Column E: Grade
- Column F: GradedBy

The name of the resulting Excel table should be AllSemesterProjectStats.xlsx

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

5. **File naming**:
The download process should preserve the filename sent by the server. No need to extract information from the filename.

6. **Duplicate handling**:
If the script is run multiple times, it should re-download and overwrite. Before starting, the "downloads/" directory should be cleaned.

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
