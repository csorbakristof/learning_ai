# DLXLS - BME Topic Data Collection Feature

## Overview

The DLXLS feature implements automated collection of student topic data from the BME portal (www.aut.bme.hu). This feature is part of the Data Collector application and handles the following workflow:

1. **Login to BME Portal** - Opens browser and waits for manual login
2. **Navigate to Workload Page** - Goes to MyWorkload.aspx
3. **Download Excel File** - Clicks "Terhelés exportálása" link
4. **Process Data** - Extracts student information from the downloaded Excel file
5. **Save Results** - Saves processed data to a new Excel file

## Usage

### Command Line
```powershell
cd app1_data_collector
E:/_AI_projects/ProjectLabAdmin/.venv/Scripts/python.exe test_dlxls.py
```

### Batch File
Double-click `test_dlxls.bat` in the `app1_data_collector` folder.

### Integrated with Main Application
The DLXLS feature is automatically included when running the main data collector:
```powershell
E:/_AI_projects/ProjectLabAdmin/.venv/Scripts/python.exe main.py
```

## Manual Steps Required

1. **Login Process**: When the browser opens, you need to:
   - Enter your BME credentials
   - Complete any 2FA if required
   - Wait for successful login
   - Press Enter in the console to continue

2. **Verification**: The application will automatically:
   - Navigate to the workload page
   - Find and click the export link
   - Download the Excel file
   - Process the data

## Configuration

Edit `app1_data_collector/config.py` to modify BME portal settings:

```python
BME_PORTAL_CONFIG = {
    'login_url': 'https://www.aut.bme.hu',
    'workload_url': 'https://www.aut.bme.hu/StaffMembers/MyWorkload.aspx',
    'export_link_text': 'Terhelés exportálása',
    'target_worksheet_keyword': 'konzultáció',
    'download_timeout': 30  # seconds
}
```

## Output Files

### Downloaded File
- **Location**: `data/downloads/`
- **Format**: Excel file (.xlsx or .xls)
- **Content**: Raw data from BME portal

### Processed File
- **Location**: `data/bme_topic_data.xlsx`
- **Format**: Cleaned Excel file
- **Content**: Extracted student names and topic categories

### Main Output
- **Location**: `data/scraped_data.xlsx` (when run with main application)
- **Content**: Combined data from all collection sources

## Data Structure

The processed data includes:
- Student names
- Topic categories (SW, HW, etc.)
- Additional metadata from the BME system
- All non-empty columns from the source worksheet

Sample output structure:
```json
[
    {
        "column_0": "Student Name",
        "column_1": "Topic Category", 
        "column_2": "Additional Info",
        ...
    }
]
```

## Error Handling

The feature includes robust error handling for:
- **Login failures** - Retries and clear error messages
- **Network issues** - Timeout handling and retries
- **Missing elements** - Multiple search strategies for the export link
- **File processing** - Fallback to second worksheet if needed
- **Download failures** - Timeout detection and cleanup

## Troubleshooting

### Common Issues

1. **Export link not found**
   - Check if you're logged in correctly
   - Verify the page loaded completely
   - The link text might have changed - check the logs for available links

2. **Download timeout**
   - Increase `download_timeout` in config
   - Check your internet connection
   - Ensure popup blockers aren't interfering

3. **Excel processing errors**
   - Verify the downloaded file isn't corrupted
   - Check if the worksheet structure has changed
   - Look for the worksheet containing "konzultáció"

4. **Login issues**
   - Clear browser cache/cookies
   - Try logging in manually first
   - Check if 2FA is required

### Debug Information

The application provides detailed logging including:
- Available links on the page (when export link isn't found)
- Sample extracted data for verification
- File download progress
- Worksheet analysis results

### Browser Requirements

- **Chrome** - Required (automatically managed via WebDriver Manager)
- **JavaScript enabled** - Required for portal functionality
- **Cookies enabled** - Required for login persistence
- **Downloads allowed** - Required for file download

## Integration Notes

The DLXLS feature is designed to integrate with other data collection features:
- **DLNEP** - Neptun system data collection (to be implemented)
- **FUSION** - Data fusion from multiple sources (to be implemented)
- **MKXLSX** - Excel table creation for session planning (to be implemented)

The collected topic data serves as input for the session planning workflow described in the main specification.

## Security Considerations

- **Credentials**: Never stored - manual login required each time
- **Downloads**: Saved to local folder, cleaned up automatically
- **Browser**: Runs in normal mode to support manual login
- **Data**: Processed locally, no external transmission

## File Structure
```
app1_data_collector/
├── dlxls_collector.py      # Main DLXLS implementation  
├── test_dlxls.py          # Standalone test script
├── test_dlxls.bat         # Easy test execution
├── config.py              # Configuration settings
└── main.py                # Integrated with main app
```
