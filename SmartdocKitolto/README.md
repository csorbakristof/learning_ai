# SmartDoc PDF Generator

This project creates SmartDoc PDF files based on data from Excel sheets. It consists of two main components:

1. **XLS2CSV**: Excel VBA macro to export data rows to individual CSV files
2. **CSV2PDF**: Python script to convert CSV files to PDF using SmartDoc website automation

## Prerequisites

### For XLS2CSV (Excel Macro)
- Microsoft Excel with VBA support
- The Excel file `input.xlsm` with your data

### For CSV2PDF (Python Script)
- Python 3.7 or higher
- Google Chrome browser
- ChromeDriver (usually auto-managed by Selenium)
- Access to BME network (for SmartDoc website)

## Installation

### Python Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

### Step 1: XLS2CSV - Export Excel Data to CSV Files

1. Open your Excel file (`input.xlsm`) with your data
2. Make sure your data is structured with:
   - First row: Column headers (matching the SmartDoc template)
   - Subsequent rows: Data for each document to generate
   - One column designated as the "filename column" (contains the name for each CSV file)

3. Import the VBA macro:
   - Press `Alt + F11` to open VBA Editor
   - Import the `xls2csv.bas` file or copy its content to a new module
   - Run the `RegisterHotkey` macro once to set up the Ctrl+Shift+C shortcut

4. Export CSV files:
   - Click on any cell in the column you want to use as the filename column
   - Press `Ctrl + Shift + C`
   - Select the filename column when prompted
   - The macro will generate individual CSV files for each data row

### Step 2: CSV2PDF - Convert CSV Files to PDF

#### Option A: Using the batch file (Windows)
```bash
run_csv2pdf.bat
```

#### Option B: Using Python directly
```bash
python csv2pdf.py
```

The script will:
1. Find all CSV files in the current directory
2. Open the SmartDoc website in Chrome
3. For each CSV file:
   - Import the data into SmartDoc
   - Convert to HTML format
   - Download the generated PDF
4. Close the browser when finished

## File Structure

```
SmartdocKitolto/
├── input.xlsm              # Your Excel data file
├── xls2csv.bas             # VBA macro for Excel export
├── csv2pdf.py              # Python script for PDF conversion
├── requirements.txt        # Python dependencies
├── run_csv2pdf.bat         # Windows batch file for easy execution
├── example.csv             # Example CSV format
└── README.md               # This file
```

## SmartDoc Website

The script uses the SmartDoc website at:
https://smartdoc.bme.hu/Hallgatoi_munkaszerzodes_gradualisnak/Hallgatoi_munkaszerzodes_gradualisnak.html

**Note**: This website is only accessible from within the BME network.

## CSV Format

The CSV files use UTF-8 encoding and follow this format:
- Semicolon-separated values (`;`)
- All values enclosed in double quotes (`"`)
- First row: Headers
- Second row: Data values
- UTF-8 encoding (properly handles Hungarian characters: á, é, í, ó, ő, ú, ű, ü)

**Note**: All CSV files must be UTF-8 encoded. The VBA macro (v2.0) automatically exports files in UTF-8 format.

Example:
```csv
"FMZ";"Hallgató neve";"Neptun kódja";"Kar neve"
"12345";"Teszt Elek";"ABC123";"VIK"
```

## Troubleshooting

### Common Issues

1. **SmartDoc website not accessible**
   - Ensure you're connected to the BME network
   - Check if the website URL is still valid

2. **Chrome/ChromeDriver issues**
   - Make sure Google Chrome is installed
   - Selenium will try to auto-manage ChromeDriver
   - If issues persist, manually install ChromeDriver

3. **CSV encoding problems**
   - Ensure CSV files are UTF-8 encoded (automatically handled by VBA macro v2.0)
   - Check that Hungarian characters (á, é, í, ó, ő, ú, ű, ü) display correctly
   - If you have old CSV files with encoding issues, regenerate them using the updated Excel macro

4. **Excel macro not working**
   - Enable macros in Excel security settings
   - Make sure VBA is available in your Excel installation
   - Run `RegisterHotkey` macro first to set up the keyboard shortcut

### Error Messages

- **"No CSV files found"**: Make sure you have CSV files in the same directory as the script
- **"SmartDoc website is not accessible"**: Check your BME network connection
- **"Chrome WebDriver initialization failed"**: Install or update Google Chrome

## Security Notes

- The script opens a web browser and automatically fills forms
- Only use on trusted networks and with legitimate data
- Be aware that the script will download files to your current directory

## Support

For issues related to:
- **SmartDoc website**: Contact BME IT support
- **VBA macro**: Check Excel VBA documentation
- **Python script**: Review error messages and ensure all dependencies are installed
