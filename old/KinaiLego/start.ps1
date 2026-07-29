Write-Host "Compiling ImageQuantizer.java..." -ForegroundColor Cyan
javac -source 8 -target 8 ImageQuantizer.java

if ($LASTEXITCODE -eq 0) {
    Write-Host "Compilation successful!" -ForegroundColor Green
    Write-Host "Starting application..." -ForegroundColor Cyan
    java ImageQuantizer
} else {
    Write-Host "Compilation failed!" -ForegroundColor Red
    pause
}
