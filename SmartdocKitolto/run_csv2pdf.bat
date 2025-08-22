@echo off
echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Starting CSV to PDF conversion...
python csv2pdf.py

pause
