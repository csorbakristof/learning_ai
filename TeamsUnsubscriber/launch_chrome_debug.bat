@echo off
echo ==============================================
echo Starting Chrome with Remote Debugging
echo ==============================================
echo.
echo Closing any existing Chrome instances...
taskkill /F /IM chrome.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

echo Starting Chrome with debugging enabled...
echo.

if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --no-first-run --no-default-browser-check
) else (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --no-first-run --no-default-browser-check
)

echo.
echo Chrome should now be running with debugging on port 9222
echo Navigate to Teams, then run the Python script.
echo.
pause
