@echo off
REM Batch file to run csv2pdf.py with virtual environment
REM This ensures we're in the correct directory and using the right Python environment

echo Starting CSV2PDF with Virtual Environment...
echo.

REM Change to the SmartdocKitolto directory
cd /d "E:\_learning_ai\SmartdocKitolto"

REM Verify we're in the correct directory
echo Current directory: %CD%
echo.

REM Check if csv2pdf.py exists
if not exist "csv2pdf.py" (
    echo ERROR: csv2pdf.py not found in current directory!
    echo Current directory: %CD%
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "E:\_learning_ai\.venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found at E:\_learning_ai\.venv\Scripts\python.exe
    pause
    exit /b 1
)

echo Found csv2pdf.py and virtual environment
echo Running script...
echo.

REM Run the Python script using the virtual environment
"E:\_learning_ai\.venv\Scripts\python.exe" csv2pdf.py

echo.
echo Script execution completed.
pause
