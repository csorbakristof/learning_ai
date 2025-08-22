# Overview of the task to implement

This project creates SmartDoc PDF files based on data from Excel sheets. For example this can be the generation of contracts for several people. The data from Excel is transferred to the SmartDoc webpage which can import data from copy-pasted CSV content and then a button can be used to download the generated contract in a PDF file.

The smartdoc page we use is here, but it can only be accessed from inside BME:
https://smartdoc.bme.hu/Hallgatoi_munkaszerzodes_gradualisnak/Hallgatoi_munkaszerzodes_gradualisnak.html

An example for an empty data export can be found in the example.csv file. Header titles can be extracted from there.

In the followings, many software features have a code name shown in brackets like "(XLS2CSV)". We will use these code names to reference the features or functions.

# (XLS2CSV) Excel macro to generate CSV files

Starting from Excel, we assume to have a worksheet with the same columns as what we need in the CSV file. There can be 1 or multiple data lines.

The VBA macro to create here is triggered by pressing Ctrl-Shift-C in a column of the Excel worksheet. This column will be the "filename column". The triggered macro will generate an individual CSV file for every data line of the worksheet, and it will export all rows at once (not just the selected row). The CSV files contain the header line (the same for every CSV file, matching the first row of the worksheet). The second line contains the corresponding data line. The name of the CSV file is taken from the "filename column" in each row.

# (CSV2PDF) Python+Selenium console application

This Python script takes all CSV files in the current directory after each other and it converts them into PDF using the website.

- It opens the website https://smartdoc.bme.hu/Hallgatoi_munkaszerzodes_gradualisnak/Hallgatoi_munkaszerzodes_gradualisnak.html
    - If the webpage is not available, the script should show a clear error message and exit gracefully.
- For every CSV file
    - It clicks on the button titled "Adat export/import" at the botton of the page. (HTML input element ID "AdatExpImp".)
    - Copy-pastes the content of the CSV file content into the textbox. (HTML textarea element ID "csvBox".)
    - Clicks on the "CSV => HTML" button. (HTML input element ID "CsvToHTML")
    - There may be several warning popup windows at this point, click OK on them to go on.
    - Clicks on the "PDF letöltése" button (HTML input element ID "PDFLetoltes") to download the PDF file.
    - The script should wait for the PDF download to complete before proceeding to the next file.

## Implementation Status

### ✅ (XLS2CSV) - COMPLETED
- **File**: `xls2csv.bas`
- **Features implemented**:
  - VBA macro triggered by Ctrl+Shift+C
  - Interactive filename column selection
  - Exports all data rows to individual CSV files
  - **UTF-8 encoding support** (v2.0) - proper Hungarian character handling
  - Uses ADODB.Stream for UTF-8 file writing
  - **Automatic date formatting** (v2.1) - converts dates to YYYYMMDD format for SmartDoc compatibility
  - Proper CSV formatting with headers
  - Error handling for missing filenames
  - Hotkey registration function

### ✅ (CSV2PDF) - COMPLETED
- **File**: `csv2pdf.py`
- **Features implemented**:
  - Selenium-based web automation
  - Chrome WebDriver integration
  - SmartDoc website interaction
  - CSV file processing pipeline
  - **UTF-8 encoding support** - expects all CSV files to be UTF-8 encoded
  - Popup warning handling
  - Download completion waiting
  - Error handling and recovery
  - Comprehensive logging

### 📁 Additional Files Created
- `requirements.txt` - Python dependencies
- `run_csv2pdf.bat` - Windows batch file for easy execution
- `README.md` - Complete user documentation
- `test_csv2pdf.py` - Test script for CSV parsing

### 🚀 Usage Instructions
1. **Prepare Excel data** in `input.xlsm` with proper column structure
2. **Run XLS2CSV**: Press Ctrl+Shift+C in Excel to generate CSV files
3. **Run CSV2PDF**: Execute `python csv2pdf.py` or `run_csv2pdf.bat` to convert to PDFs
4. **Access from BME network** required for SmartDoc website

### ⚠️ Requirements
- Microsoft Excel with VBA support
- Python 3.7+ with selenium package
- Google Chrome browser
- BME network access for SmartDoc website
