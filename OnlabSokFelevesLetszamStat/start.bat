@echo off
echo ============================================================
echo University Course Statistics Downloader and Merger
echo ============================================================
echo.

echo Installing requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install requirements.
    echo Please check your Python installation and try again.
    pause
    exit /b 1
)

echo.
echo Requirements installed successfully.
echo.
echo Starting the application...
echo.

python main.py

echo.
pause
