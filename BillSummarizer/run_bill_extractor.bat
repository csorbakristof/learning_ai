@echo off
REM Hungarian Bill Information Extractor - Batch File Launcher
REM This script helps run the bill_extractor.py with proper environment setup

echo ===============================================
echo  Hungarian Bill Information Extractor
echo ===============================================

cd /d "%~dp0"

echo Current directory: %CD%
echo.

REM Check if Python script exists
if not exist "bill_extractor.py" (
    echo ERROR: bill_extractor.py not found in current directory!
    pause
    exit /b 1
)

REM Check if virtual environment exists (assuming it's in parent directory)
if exist "..\.venv\Scripts\python.exe" (
    echo Using virtual environment...
    set PYTHON_CMD=..\.venv\Scripts\python.exe
) else (
    echo Using system Python...
    set PYTHON_CMD=python
)

echo.
echo Available PDF files in current directory:
dir *.pdf /b 2>nul
if errorlevel 1 echo No PDF files found in current directory.

echo.
set /p INPUT_DIR="Enter directory containing PDF files (or press Enter for current directory): "
if "%INPUT_DIR%"=="" set INPUT_DIR=.

echo.
set /p OUTPUT_FILE="Enter output CSV filename (or press Enter for default 'számla_összesítő.csv'): "
if "%OUTPUT_FILE%"=="" set OUTPUT_FILE=számla_összesítő.csv

echo.
echo Processing PDF files in: %INPUT_DIR%
echo Output file: %OUTPUT_FILE%
echo.

REM Install dependencies if needed
echo Checking dependencies...
%PYTHON_CMD% -c "import pdfplumber" 2>nul
if errorlevel 1 (
    echo Installing pdfplumber...
    %PYTHON_CMD% -m pip install pdfplumber
)

echo.
echo Starting bill extraction...
echo.

REM Run the Python script
%PYTHON_CMD% bill_extractor.py "%INPUT_DIR%" -o "%OUTPUT_FILE%"

echo.
echo Script execution completed.
echo Check the log file 'bill_extraction.log' for detailed information.
echo.

if exist "%OUTPUT_FILE%" (
    echo Success! Results saved to: %OUTPUT_FILE%
    echo.
    set /p OPEN_CSV="Open CSV file? (y/N): "
    if /i "%OPEN_CSV%"=="y" start "" "%OUTPUT_FILE%"
) else (
    echo Warning: Output file was not created. Check the log for errors.
)

pause
