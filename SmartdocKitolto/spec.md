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
