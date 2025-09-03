@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Learning AI - GitHub Pages Local Setup
echo ========================================
echo.

REM Change to the docs directory
cd /d "%~dp0docs"
if errorlevel 1 (
    echo ERROR: Could not change to docs directory
    echo Make sure this batch file is in the root of your repository
    pause
    exit /b 1
)

echo Current directory: %CD%
echo.

REM Check if Ruby is installed
echo Checking Ruby installation...
ruby --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Ruby is not installed or not in PATH
    echo.
    echo Please install Ruby from: https://rubyinstaller.org/
    echo Choose the Ruby+Devkit version for Windows
    echo.
    pause
    exit /b 1
) else (
    echo Ruby is installed:
    ruby --version
)
echo.

REM Check if Bundler is installed
echo Checking Bundler installation...
bundle --version >nul 2>&1
if errorlevel 1 (
    echo Bundler not found. Installing Bundler...
    gem install bundler
    if errorlevel 1 (
        echo ERROR: Failed to install Bundler
        pause
        exit /b 1
    )
) else (
    echo Bundler is installed:
    bundle --version
)
echo.

REM Install Jekyll dependencies
echo Installing Jekyll dependencies...
echo This may take a few minutes on first run...
bundle install
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo.
    echo Try running these commands manually:
    echo   gem install bundler
    echo   bundle install
    echo.
    pause
    exit /b 1
)
echo.
echo Dependencies installed successfully!
echo.

REM Start Jekyll server
echo ========================================
echo Starting Jekyll development server...
echo ========================================
echo.
echo Your site will be available at:
echo http://localhost:4000/learning_ai/
echo.
echo Press Ctrl+C to stop the server
echo.

bundle exec jekyll serve --livereload --host=0.0.0.0 --port=4000
if errorlevel 1 (
    echo.
    echo ERROR: Failed to start Jekyll server
    echo.
    echo If you get port conflicts, try:
    echo   bundle exec jekyll serve --livereload --port=4001
    echo.
    pause
    exit /b 1
)

pause
