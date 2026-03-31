@echo off
cls
echo.
echo ================================================
echo  MS Teams Auto-Hide Script - CDP Method
echo ================================================
echo.
echo STEP 1: Launch Chrome with debugging
echo ================================================
echo We'll launch Chrome with remote debugging enabled.
echo.
pause

echo.
echo Launching Chrome...
start "" "launch_chrome_debug.bat"

timeout /t 5 /nobreak > nul

echo.
echo ================================================
echo STEP 2: Navigate to Teams
echo ================================================
echo In the Chrome window that just opened:
echo   1. Navigate to: https://teams.microsoft.com/v2/?ring=ring3_6
echo   2. Log in if needed
echo   3. Wait for Teams to fully load
echo.
echo Once you're on the Teams page, come back here.
echo.
pause

echo.
echo ================================================
echo STEP 3: Running the script
echo ================================================
echo.

REM Check if using dry-run
set DRY_RUN_FLAG=
if "%1"=="--dry-run" set DRY_RUN_FLAG=--dry-run
if "%1"=="-d" set DRY_RUN_FLAG=--dry-run

if defined DRY_RUN_FLAG (
    echo Mode: DRY RUN - no actual changes
echo.
) else (
    echo Mode: LIVE - will actually hide teams!
    echo.
)

e:\learning_ai\.venv\Scripts\python.exe teams_auto_hide_simple.py %DRY_RUN_FLAG%

echo.echo ================================================
echo Script completed
echo ================================================
pause
