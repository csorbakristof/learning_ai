# PowerShell script to run CSV2PDF conversion
# Run this script from the SmartdocKitolto directory

Write-Host "=== SmartDoc CSV2PDF Converter ===" -ForegroundColor Green
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.7 or higher." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check for CSV files
$csvFiles = Get-ChildItem -Filter "*.csv" | Where-Object { $_.Name -ne "example.csv" }
if ($csvFiles.Count -eq 0) {
    Write-Host ""
    Write-Host "⚠️  No CSV files found (excluding example.csv)" -ForegroundColor Yellow
    Write-Host "Please generate CSV files first using the Excel macro (Ctrl+Shift+C)" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "Found $($csvFiles.Count) CSV file(s) to process:" -ForegroundColor Cyan
    foreach ($file in $csvFiles) {
        Write-Host "  - $($file.Name)" -ForegroundColor Cyan
    }
}

# Run the conversion
Write-Host ""
Write-Host "Starting CSV to PDF conversion..." -ForegroundColor Yellow
Write-Host "Note: This requires access to BME network for SmartDoc website" -ForegroundColor Yellow
Write-Host ""

try {
    python csv2pdf.py
} catch {
    Write-Host "✗ Error occurred during conversion" -ForegroundColor Red
}

Write-Host ""
Write-Host "Process completed. Check the output above for any errors." -ForegroundColor Green
Read-Host "Press Enter to exit"
