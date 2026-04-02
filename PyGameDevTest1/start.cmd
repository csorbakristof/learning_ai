@echo off
REM Start Dynablaster (Bomberman Clone)
REM This script activates the virtual environment and runs the game

cd /d "%~dp0"
cd ..
call .venv\Scripts\activate.bat
cd PyGameDevTest1
python main.py
pause
