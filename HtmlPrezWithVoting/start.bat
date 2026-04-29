@echo off
REM Presentation Voting System - Startup Script
REM This script starts the Node.js server and opens the presentation

echo ============================================================
echo   PRESENTATION VOTING SYSTEM - STARTUP
echo ============================================================
echo.

REM Check if Node.js is installed
echo [1/4] Checking Node.js installation...
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Node.js is not installed!
    echo.
    echo Please install Node.js from: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

REM Get Node.js version
for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo     Node.js version: %NODE_VERSION%
echo     [OK]
echo.

REM Check if node_modules exists
echo [2/4] Checking dependencies...
if not exist "node_modules\" (
    echo     Dependencies not found. Installing...
    echo.
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ERROR: Failed to install dependencies!
        echo Please run 'npm install' manually to see the error.
        pause
        exit /b 1
    )
    echo     [OK]
) else (
    echo     Dependencies already installed.
    echo     [OK]
)
echo.

REM Start the server in background
echo [3/4] Starting server...
echo     Server will run on port 8000
echo     Press Ctrl+C in this window to stop the server
echo.
start /B node server.js

REM Wait for server to initialize
echo     Waiting for server to initialize...
timeout /t 3 /nobreak >nul

echo     [OK]
echo.

REM Open presentation in default browser
echo [4/4] Opening presentation in browser...
start http://localhost:8000/presentation.html
echo     [OK]
echo.

echo ============================================================
echo   SERVER IS RUNNING
echo ============================================================
echo.
echo Presentation URL: http://localhost:8000/presentation.html
echo Voting URL: Check the tunnel URL in the server output above
echo.
echo INSTRUCTIONS:
echo   1. The presentation should have opened in your browser
echo   2. Navigate to slide 2 to show the QR code
echo   3. Audience scans QR code to vote on their phones
echo   4. Navigate through slides normally
echo   5. Press 'V' on question slides to show vote details
echo.
echo To stop the server: Press Ctrl+C in this window
echo.
echo ============================================================
echo.

REM Keep the window open and show server output
node server.js

REM This line will only execute if the server stops
echo.
echo Server has stopped.
pause
