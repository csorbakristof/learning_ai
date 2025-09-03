@echo off
echo ========================================
echo Learning AI - Start Local Site
echo ========================================
echo.

cd /d "%~dp0docs"
if errorlevel 1 (
    echo ERROR: Could not change to docs directory
    pause
    exit /b 1
)

echo Starting Jekyll server...
echo.
echo Your site will be available at:
echo http://localhost:4000/learning_ai/
echo.
echo Press Ctrl+C to stop the server
echo.

bundle exec jekyll serve --livereload
if errorlevel 1 (
    echo.
    echo ERROR: Failed to start Jekyll server
    echo.
    echo Make sure you have run setup_local_site.bat first
    echo.
    pause
)

pause
