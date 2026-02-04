@echo off
REM Teams Unsubscriber - Generate interactive HTML to manage Teams memberships
REM This script runs the Python Teams Unsubscriber HTML Generator

echo Starting Teams Unsubscriber HTML Generator...
echo.

REM Use the virtual environment Python directly
set PYTHON_CMD="E:/learning_ai/.venv/Scripts/python.exe"

REM Check if virtual environment Python exists
if not exist %PYTHON_CMD% (
    echo Error: Virtual environment Python not found at %PYTHON_CMD%
    echo.
    echo Please make sure the virtual environment is properly set up.
    echo You can create it by running: python -m venv E:/learning_ai/.venv
    echo Then install packages: %PYTHON_CMD% -m pip install msal requests
    echo.
    pause
    exit /b 1
)
echo Found Python: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

REM Navigate to the script directory
cd /d "%~dp0"

REM Run the Python script
echo Running UnsubscriberHtmlGenerator.py...
%PYTHON_CMD% UnsubscriberHtmlGenerator.py

REM Check if the script ran successfully
if errorlevel 1 (
    echo.
    echo Error: Script execution failed
    echo.
    echo Common issues and solutions:
    echo   1. Missing dependencies - Install with: %PYTHON_CMD% -m pip install msal requests
    echo   2. CLIENT_ID not configured - Edit UnsubscriberHtmlGenerator.py and set your CLIENT_ID
    echo   3. Network/authentication issues - Check internet connection and Microsoft account access
    echo.
    pause
    exit /b 1
)

echo.
echo Script completed successfully!
echo The teams_to_leave.html file should now be generated.
echo.

REM Open the generated HTML file if it exists
if exist "teams_to_leave.html" (
    echo Opening teams_to_leave.html in your default browser...
    start "" "teams_to_leave.html"
) else (
    echo Warning: teams_to_leave.html was not created
)

echo.
pause