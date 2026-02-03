# Clarification questions of the AI after first draft of spec.md

I've reviewed the specification. Before implementing this project, I have several clarification questions:

## Project Structure & Setup
1. **Where should the downloaded source Excel files be stored?** Should they be in a specific subdirectory (e.g., `downloads/` or `source_files/`)?

2. **Output file location**: Where should `AllSemesterProjectStats.xlsx` be saved? Same directory as the script or a specific output folder?

3. **Browser preference**: Which browser should Selenium use (Chrome, Firefox, Edge)? Do you have a preference or should it be configurable?

## Download Feature [DL]
4. **SemesterId range**: What's the current/maximum SemesterId value to iterate to? Should this be configurable or hardcoded? Should the script detect when downloads fail (404/invalid semester) and stop there?

5. **File naming**: What naming convention should be used for the downloaded Excel files? E.g., `semester_{id}.xlsx` or extract the semester name from the file after download?

6. **Duplicate handling**: If the script is run multiple times, should it:
   - Skip already downloaded files?
   - Re-download and overwrite?
   - Prompt the user?

## Data Extraction Feature [XLS2JSON]
7. **Table end detection**: The spec mentions "rows with merged cells" after the table. How should the script detect where the table actually ends? Should it stop at the first empty row or look for specific patterns?

8. **Data validation**: Should the script:
   - Skip rows with missing/invalid data?
   - Validate that Grade values are valid?
   - Handle any specific error cases?

9. **Processing mode**: When running [XLS2JSON], should it:
   - Process all files in the downloads folder?
   - Allow processing a specific subset?
   - Append to existing `AllSemesterProjectStats.xlsx` or always recreate it?

## General
10. **Error handling**: How should the script handle errors (network issues, malformed Excel files, login timeout)? Should it log errors and continue or stop execution?

11. **Progress feedback**: Should the script display progress information (e.g., "Downloading semester 5/30...", "Processing file 3/15...")?

Please provide guidance on these points so I can implement the solution according to your needs.