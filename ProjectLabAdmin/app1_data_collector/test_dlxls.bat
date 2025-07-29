@echo off
echo DLXLS Feature Test - BME Topic Data Collection
echo ===============================================
echo.
echo This will test the BME portal integration to collect student topic data.
echo You will need to manually login to the BME portal when prompted.
echo.
pause
echo.
echo Starting DLXLS test...
echo.
cd /d "%~dp0"
"%~dp0..\\.venv\\Scripts\\python.exe" test_dlxls.py
echo.
pause
