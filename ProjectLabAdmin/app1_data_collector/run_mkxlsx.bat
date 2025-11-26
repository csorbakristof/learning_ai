@echo off
REM Batch script to run MKXLSX (Session Planning Excel Creator)
REM This script creates session_planner.xlsx from fused_student_data.json

echo ============================================================
echo MKXLSX - Session Planning Excel Creator
echo ============================================================
echo.

REM Change to the script's directory
cd /d "%~dp0"

REM Run the MKXLSX creator using the virtual environment Python
echo Running MKXLSX creator...
E:\_learning_ai\.venv\Scripts\python.exe mkxlsx_creator.py

REM Check if successful
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================
    echo MKXLSX completed successfully!
    echo Output: ..\data\session_planner.xlsx
    echo ============================================================
) else (
    echo.
    echo ============================================================
    echo MKXLSX failed with error code %ERRORLEVEL%
    echo ============================================================
)

echo.
pause
