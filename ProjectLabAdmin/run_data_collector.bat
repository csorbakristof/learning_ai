@echo off
echo ProjectLabAdmin - Data Collector
echo ==================================
echo.
echo Starting Data Collector Application...
echo.
cd /d "%~dp0app1_data_collector"
"%~dp0.venv\Scripts\python.exe" main.py
pause
