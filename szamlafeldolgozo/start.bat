@echo off
setlocal

set "SCRIPT_DIR=%~dp0"

where py >nul 2>nul
if not errorlevel 1 (
    set "PYTHON_CMD=py -3"
) else (
    where python >nul 2>nul
    if not errorlevel 1 (
        set "PYTHON_CMD=python"
    ) else (
        echo Python was not found on PATH. Please install Python 3 and try again.
        exit /b 1
    )
)

echo Installing required dependencies: requests, pdfplumber, pypdf, pymupdf
%PYTHON_CMD% -m pip install requests pdfplumber pypdf pymupdf
if errorlevel 1 (
    echo Dependency installation failed.
    exit /b %errorlevel%
)

echo Starting document processor...
rem %PYTHON_CMD% "%SCRIPT_DIR%data-extractor.py" --zip-path "%SCRIPT_DIR%szamlak\szamlak.zip" --output-json "%SCRIPT_DIR%ujszamlak.json" --base-url "http://localhost:1234/v1" --model "local-model"
%PYTHON_CMD% "%SCRIPT_DIR%data-extractor.py" --zip-path "%SCRIPT_DIR%szamlak\drive-download-20260801T151302Z-1-001.zip" --output-json "%SCRIPT_DIR%ujszamlak.json" --base-url "http://localhost:1234/v1" --model "local-model"

