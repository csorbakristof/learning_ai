@echo off
REM Presentation Voting System - Startup Script (PHP edition)
REM The voting backend is now a PHP script hosted on a public web server.
REM This script simply opens the local presentation file in your browser.
REM
REM Usage: start.bat [presentation_filename]
REM Example: start.bat sweep_questions.html
REM
REM BEFORE USE: open presentation.html and set PHP_SERVER_URL to the URL
REM of the directory on your web server where api.php and index.php live.

REM Set presentation file (default to presentation.html)
set PRESENTATION_FILE=%~1
if "%PRESENTATION_FILE%"=="" set PRESENTATION_FILE=sweep_questions.html

echo ============================================================
echo   PRESENTATION VOTING SYSTEM (PHP edition)
echo ============================================================
echo.
echo Presentation file: %PRESENTATION_FILE%
echo.
echo NOTE: Make sure PHP_SERVER_URL is configured in %PRESENTATION_FILE%
echo       and that api.php / index.php are deployed on your web server.
echo.

REM Open the presentation directly in the default browser (no local server needed)
echo Opening presentation in browser...
start "" "%~dp0%PRESENTATION_FILE%"
echo.

echo ============================================================
echo INSTRUCTIONS
echo ============================================================
echo.
echo   1. The presentation should have opened in your browser
echo   2. Navigate to slide 2 to show the QR code
echo      ^(audience members scan it to open the voting page^)
echo   3. Navigate through slides normally
echo   4. Press 'D' on question slides to show detailed vote counts
echo.
echo ============================================================
echo.
pause
    echo.
    echo ============================================================
) else (
    echo Server has stopped normally.
)
echo.
pause
