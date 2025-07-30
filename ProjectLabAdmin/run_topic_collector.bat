@echo off
REM Batch file to run the BME AUT Topic Collector
REM Make sure you're running this from the ProjectLabAdmin directory

echo BME AUT Topic Collector
echo =======================

REM Check if Python virtual environment exists
if exist ".venv\Scripts\python.exe" (
    echo Using virtual environment...
    set PYTHON_CMD=.venv\Scripts\python.exe
) else (
    echo Using system Python...
    set PYTHON_CMD=python
)

REM Change to the topic collector directory
cd app3_topic_collector

REM Run the application
echo Starting topic collection...
%PYTHON_CMD% main.py %*

REM Return to parent directory
cd ..

echo.
echo Topic collection completed!
pause
