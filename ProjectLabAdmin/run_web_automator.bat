@echo off
echo ProjectLabAdmin - Web Automator
echo =================================
echo.
echo Starting Web Automator Application...
echo.
cd /d "%~dp0app2_web_automator"
"%~dp0.venv\Scripts\python.exe" main.py
pause
