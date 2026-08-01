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

echo Installing required dependency: requests
%PYTHON_CMD% -m pip install requests
if errorlevel 1 (
    echo Dependency installation failed.
    exit /b %errorlevel%
)

echo Starting document processor...
python data-extractor.py --zip-path "szamlak/szamlak.zip" --output-json "ujszamlak.json" --api-key "6ZAAA6D-8TKM1FJ-GG4XEZN-AS5JS7S" --workspace-slug "billextractor"
