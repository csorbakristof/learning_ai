@echo off
echo Closing all Chrome windows...
taskkill /F /IM chrome.exe >nul 2>&1
timeout /t 3 /nobreak >nul

echo.
echo Starting Chrome with debugging...
cd "C:\Program Files (x86)\Google\Chrome\Application"
start chrome.exe --remote-debugging-port=9222 --remote-allow-origins=*

timeout /t 5 /nobreak >nul
echo.
echo Chrome should now be running.
echo Navigate to Teams: https://teams.microsoft.com/v2/?ring=ring3_6
echo.
echo Keep this window open and run the Python script in another window.
pause
