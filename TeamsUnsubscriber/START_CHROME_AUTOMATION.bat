@echo off
REM ========================================================================
REM MS Teams Auto-Hide - Chrome Launcher with Remote Debugging
REM ========================================================================
REM This script prepares Chrome for automation using Chrome DevTools Protocol (CDP)
REM 
REM Why these steps are needed:
REM 1. Kill existing Chrome - DevTools remote debugging requires exclusive access
REM 2. Separate profile - Cannot use default profile when remote debugging is active
REM 3. Port 9222 - Standard CDP port for Playwright to connect via connect_over_cdp()
REM 4. IPv4 (127.0.0.1) - Script uses explicit IPv4 to avoid localhost IPv6 issues
REM ========================================================================

echo.
echo [Step 1/3] Closing all Chrome windows...
taskkill /F /IM chrome.exe >nul 2>&1
timeout /t 3 /nobreak >nul

echo.
echo [Step 2/3] Starting Chrome with debugging and automation profile...
echo   - Remote debugging port: 9222
echo   - Profile: %%TEMP%%\chrome_automation_profile
echo   - Opening: MS Teams

set PROFILE_DIR=%TEMP%\chrome_automation_profile

"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%PROFILE_DIR%" --no-first-run --no-default-browser-check https://teams.microsoft.com/v2/?ring=ring3_6

echo.
echo [Step 3/3] Verifying connection...
echo.
REM Note: If Chrome closed immediately, there was an error.
REM The automation script should now be able to connect to http://127.0.0.1:9222
pause
