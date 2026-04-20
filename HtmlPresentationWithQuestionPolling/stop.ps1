Write-Host "Stopping presentation server and ngrok tunnel..." -ForegroundColor Cyan

# Stop Node.js server processes running server.js
$nodeProcesses = Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object {
    $_.Path -and (Get-CimInstance Win32_Process -Filter "ProcessId = $($_.Id)" | Select-Object -ExpandProperty CommandLine) -like "*server.js*"
}

if ($nodeProcesses) {
    Write-Host "Stopping Node.js server..." -ForegroundColor Yellow
    $nodeProcesses | Stop-Process -Force
    Write-Host "✓ Node.js server stopped" -ForegroundColor Green
} else {
    Write-Host "○ No Node.js server process found" -ForegroundColor Gray
}

# Stop ngrok processes
$ngrokProcesses = Get-Process -Name "ngrok" -ErrorAction SilentlyContinue

if ($ngrokProcesses) {
    Write-Host "Stopping ngrok tunnel..." -ForegroundColor Yellow
    $ngrokProcesses | Stop-Process -Force
    Write-Host "✓ ngrok tunnel stopped" -ForegroundColor Green
} else {
    Write-Host "○ No ngrok process found" -ForegroundColor Gray
}

Write-Host "`nAll processes stopped successfully!" -ForegroundColor Cyan
