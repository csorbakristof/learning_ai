@echo off
REM Setup script for MS Teams Auto-Hide

echo ============================================
echo MS Teams Auto-Hide Setup
echo ============================================
echo.

echo Step 1: Installing Playwright...
python -m pip install playwright
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Playwright
    pause
    exit /b 1
)

echo.
echo Step 2: Installing Chrome browser driver...
python -m playwright install chrome
if %errorlevel% neq 0 (
    echo Note: Chrome may already be installed
    echo This is fine - continuing...
)

echo.
echo Step 3: Verifying installation...
python -c "from playwright.sync_api import sync_playwright; print('✓ Playwright installed successfully!')"
if %errorlevel% neq 0 (
    echo ERROR: Playwright verification failed
    pause
    exit /b 1
)

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo You can now run the script:
echo   - Dry run:  .\run_teams_auto_hide.bat --dry-run
echo   - Live run: .\run_teams_auto_hide.bat
echo.
pause
