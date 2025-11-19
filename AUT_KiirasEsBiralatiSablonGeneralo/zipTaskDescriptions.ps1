# zipTaskDescriptions.ps1
# Creates zip files for each subdirectory in the "output" folder
# Each zip file contains all the contents of its corresponding subdirectory

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Define the output directory path
$outputDir = Join-Path $scriptDir "output"

# Check if output directory exists
if (-not (Test-Path $outputDir -PathType Container)) {
    Write-Host "Error: 'output' directory not found at: $outputDir" -ForegroundColor Red
    Write-Host "Please ensure the script is in the same directory as the 'output' folder." -ForegroundColor Yellow
    exit 1
}

# Get all subdirectories in output
$subdirectories = Get-ChildItem -Path $outputDir -Directory

if ($subdirectories.Count -eq 0) {
    Write-Host "No subdirectories found in 'output' folder." -ForegroundColor Yellow
    exit 0
}

Write-Host "Found $($subdirectories.Count) subdirectories to process..." -ForegroundColor Green
Write-Host ""

$successCount = 0
$errorCount = 0

foreach ($subdir in $subdirectories) {
    $subdirName = $subdir.Name
    $subdirPath = $subdir.FullName
    $zipFileName = "$subdirName.zip"
    $zipFilePath = Join-Path $outputDir $zipFileName
    
    Write-Host "Processing: $subdirName" -ForegroundColor Cyan
    
    try {
        # Check if files exist in the subdirectory
        $files = Get-ChildItem -Path $subdirPath -File
        
        if ($files.Count -eq 0) {
            Write-Host "  Warning: No files found in '$subdirName' - skipping" -ForegroundColor Yellow
            continue
        }
        
        # Remove existing zip file if it exists
        if (Test-Path $zipFilePath) {
            Remove-Item $zipFilePath -Force
            Write-Host "  Removed existing zip file" -ForegroundColor Yellow
        }
        
        # Create zip file with all contents of the subdirectory
        Compress-Archive -Path "$subdirPath\*" -DestinationPath $zipFilePath -Force
        
        Write-Host "  Created: $zipFileName ($($files.Count) files)" -ForegroundColor Green
        $successCount++
        
    } catch {
        Write-Host "  Error creating zip for '$subdirName': $($_.Exception.Message)" -ForegroundColor Red
        $errorCount++
    }
}

Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor White
Write-Host "Successfully created: $successCount zip files" -ForegroundColor Green

if ($errorCount -gt 0) {
    Write-Host "Errors encountered: $errorCount" -ForegroundColor Red
}

Write-Host "Zip files location: $outputDir" -ForegroundColor Cyan

if ($successCount -gt 0) {
    Write-Host ""
    Write-Host "Created zip files:" -ForegroundColor White
    Get-ChildItem -Path $outputDir -Filter "*.zip" | ForEach-Object {
        $size = [math]::Round($_.Length / 1KB, 1)
        Write-Host "  $($_.Name) ($size KB)" -ForegroundColor Gray
    }
}