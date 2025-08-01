# PowerShell script to sideload the dummy Outlook plugin
# This script helps with the sideloading process

Write-Host "Dummy Outlook Plugin Sideloader" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Check if server is running
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3001/manifest.xml" -UseBasicParsing -TimeoutSec 5
    Write-Host "✓ Server is running on http://localhost:3001" -ForegroundColor Green
} catch {
    Write-Host "✗ Server is not running on port 3001" -ForegroundColor Red
    Write-Host "Please start the server first with: npm start" -ForegroundColor Yellow
    exit 1
}

# Get the full path to manifest.xml
$manifestPath = Join-Path $PSScriptRoot "manifest.xml"

if (Test-Path $manifestPath) {
    Write-Host "✓ Found manifest.xml at: $manifestPath" -ForegroundColor Green
} else {
    Write-Host "✗ Could not find manifest.xml" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Manual Sideloading Steps:" -ForegroundColor Yellow
Write-Host "1. Open Outlook Desktop" -ForegroundColor White
Write-Host "2. Go to File → Options → Trust Center → Trust Center Settings → Add-ins" -ForegroundColor White
Write-Host "3. Click 'Manage Add-ins' (opens browser)" -ForegroundColor White
Write-Host "4. Click 'My add-ins' → 'Upload My Add-in' → 'Add from file...'" -ForegroundColor White
Write-Host "5. Select this file: $manifestPath" -ForegroundColor Cyan
Write-Host "6. Restart Outlook" -ForegroundColor White
Write-Host ""
Write-Host "Server URL: http://localhost:3001" -ForegroundColor Cyan
Write-Host "Manifest URL: http://localhost:3001/manifest.xml" -ForegroundColor Cyan

# Open the manifest file location in Explorer
Write-Host ""
$openExplorer = Read-Host "Open manifest folder in Explorer? (y/n)"
if ($openExplorer -eq 'y' -or $openExplorer -eq 'Y') {
    Start-Process "explorer.exe" -ArgumentList "/select,`"$manifestPath`""
}
