# Alternative sideloading methods for Outlook add-ins
Write-Host "Alternative Sideloading Methods for Outlook" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green

$manifestPath = Join-Path $PSScriptRoot "manifest.xml"
$manifestUrl = "http://localhost:3001/manifest.xml"

Write-Host ""
Write-Host "METHOD 1: Manual File Copy (Simple)" -ForegroundColor Yellow
Write-Host "-----------------------------------" -ForegroundColor Yellow
Write-Host "1. Copy your manifest.xml to a shared network location or cloud storage"
Write-Host "2. In Outlook: File → Manage Add-ins → My Add-ins → Shared folder"
Write-Host "3. Browse to the location and select manifest.xml"

Write-Host ""
Write-Host "METHOD 2: AppSource Catalog (If available)" -ForegroundColor Yellow
Write-Host "-------------------------------------------" -ForegroundColor Yellow
Write-Host "1. In Outlook: File → Get Add-ins"
Write-Host "2. Click 'My Organization' tab (if available)"
Write-Host "3. Look for upload options there"

Write-Host ""
Write-Host "METHOD 3: Outlook Web App (OWA) Method" -ForegroundColor Yellow
Write-Host "---------------------------------------" -ForegroundColor Yellow
Write-Host "1. Go to https://outlook.office.com or https://outlook.live.com"
Write-Host "2. Click the gear icon (Settings) → View all Outlook settings"
Write-Host "3. Go to General → Manage add-ins"
Write-Host "4. Click 'Add a custom add-in' → 'Add from file'"
Write-Host "5. Upload your manifest.xml"
Write-Host "6. The add-in will sync to your desktop Outlook"

Write-Host ""
Write-Host "METHOD 4: Command Line with Office Tool" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host "If you have Office deployment tools installed:"
Write-Host "OfficeWebAddInTool.exe install -m `"$manifestPath`" -a Outlook"

Write-Host ""
Write-Host "METHOD 5: Direct Registry Edit (Advanced)" -ForegroundColor Yellow
Write-Host "------------------------------------------" -ForegroundColor Yellow
Write-Host "Use the registry-sideload.ps1 script in this folder"
Write-Host "Run: .\registry-sideload.ps1"

Write-Host ""
Write-Host "Troubleshooting Tips:" -ForegroundColor Cyan
Write-Host "--------------------" -ForegroundColor Cyan
Write-Host "• Make sure Outlook is completely closed before sideloading"
Write-Host "• Check that the server is running: $manifestUrl"
Write-Host "• Try running Outlook as Administrator"
Write-Host "• Clear Outlook cache: File → Options → Advanced → Outlook Data Files → Settings"
Write-Host "• Check Windows Event Viewer for Office/Outlook errors"
Write-Host "• Verify manifest.xml is valid XML (open in browser)"

Write-Host ""
Write-Host "Current Status:" -ForegroundColor Green
try {
    $null = Invoke-WebRequest -Uri $manifestUrl -UseBasicParsing -TimeoutSec 5
    Write-Host "✓ Server is running: $manifestUrl" -ForegroundColor Green
} catch {
    Write-Host "✗ Server not accessible: $manifestUrl" -ForegroundColor Red
}

if (Test-Path $manifestPath) {
    Write-Host "✓ Manifest file found: $manifestPath" -ForegroundColor Green
} else {
    Write-Host "✗ Manifest file not found: $manifestPath" -ForegroundColor Red
}
