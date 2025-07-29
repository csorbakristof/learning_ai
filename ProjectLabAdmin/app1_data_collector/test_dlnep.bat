@echo off
echo DLNEP Feature Test - Neptun Student Data Collection
echo ===================================================
echo.
echo This will test the Neptun system integration to collect student data.
echo You will need to manually login to the Neptun system when prompted.
echo The application will then automatically download student lists from all courses.
echo.
pause
echo.
echo Starting DLNEP test...
echo.
cd /d "%~dp0"
"%~dp0..\\.venv\\Scripts\\python.exe" test_dlnep.py
echo.
pause
