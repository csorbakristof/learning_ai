# SOLID Principles Presentation Starter Script
# This script starts the Node.js server with ngrok tunnel

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  SOLID Principles - Live Polling Presentation" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Get the script's directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Check if Node.js is installed
Write-Host "[1/3] Checking Node.js installation..." -ForegroundColor Yellow
$nodeInstalled = Get-Command node -ErrorAction SilentlyContinue
$npmInstalled = Get-Command npm -ErrorAction SilentlyContinue

if (-Not $nodeInstalled -or -Not $npmInstalled) {
    Write-Host "      ERROR: Node.js is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "      Please install Node.js from: https://nodejs.org/" -ForegroundColor Yellow
    Write-Host "      Download the LTS version and run the installer." -ForegroundColor Yellow
    Write-Host "      After installation, restart PowerShell and run this script again." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

$nodeVersion = node --version
Write-Host "      Node.js $nodeVersion detected." -ForegroundColor Green
Write-Host ""

Write-Host "[2/3] Checking dependencies..." -ForegroundColor Yellow

# Check if node_modules exists
if (-Not (Test-Path "node_modules")) {
    Write-Host "      Installing npm packages (first time setup)..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "      ERROR: npm install failed!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "      Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "      Dependencies already installed." -ForegroundColor Green
}

Write-Host ""
Write-Host "[3/3] Starting server..." -ForegroundColor Yellow

# Start the server
Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host "  Server is starting..." -ForegroundColor Green
Write-Host "  - Local presentation will open automatically" -ForegroundColor Green
Write-Host "  - Public ngrok URL will be displayed below" -ForegroundColor Green
Write-Host "  - QR codes will appear on question slides" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server when done." -ForegroundColor Yellow
Write-Host ""

# Run the server (this will block until stopped)
npm start
