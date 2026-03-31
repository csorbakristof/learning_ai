# Optimized script to extract T2_Terasz temperature data using JSON deserialization

$jsonPath = "e:\learning_ai\ITMP_http_eloadas\temperatures\temperature_database.json"
$csvPath = "e:\learning_ai\ITMP_http_eloadas\temperatures\temperatures.csv"
$deviceName = "T2_Terasz"

Write-Host "Extracting temperature data for $deviceName" -ForegroundColor Cyan
Write-Host "Output: $csvPath" -ForegroundColor Gray
Write-Host ""

try {
    # Read and deserialize JSON file
    Write-Host "Reading JSON file..." -ForegroundColor Yellow
    $jsonContent = Get-Content -Path $jsonPath -Raw | ConvertFrom-Json
    
    Write-Host "Parsing complete. Extracting device data..." -ForegroundColor Yellow
    
    # Access the device directly using property notation
    if ($jsonContent.devices.PSObject.Properties.Name -contains $deviceName) {
        $device = $jsonContent.devices.$deviceName
        
        Write-Host "Found device: $deviceName" -ForegroundColor Green
        Write-Host "Records found: $($device.records.Count)" -ForegroundColor Cyan
        
        # Extract temperature records using simple filtering
        $temperatureData = $device.records | Select-Object -Property `
            @{Name='DateTime'; Expression={$_.timestamp}}, `
            @{Name='Temperature'; Expression={$_.temperature}}
        
        # Export to CSV
        Write-Host "Exporting to CSV..." -ForegroundColor Yellow
        $temperatureData | Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8
        
        Write-Host ""
        Write-Host "Extraction complete!" -ForegroundColor Green
        Write-Host "Total temperature records: $($temperatureData.Count)" -ForegroundColor Cyan
        Write-Host "Output file: $csvPath" -ForegroundColor Cyan
        Write-Host ""
        
        # Show sample of extracted data
        Write-Host "First 5 records:" -ForegroundColor Yellow
        $temperatureData | Select-Object -First 5 | Format-Table -AutoSize
        Write-Host ""
        Write-Host "Last 5 records:" -ForegroundColor Yellow
        $temperatureData | Select-Object -Last 5 | Format-Table -AutoSize
    }
    else {
        Write-Host "Error: Device '$deviceName' not found in JSON file." -ForegroundColor Red
        Write-Host "Available devices:" -ForegroundColor Yellow
        $jsonContent.devices.PSObject.Properties.Name | ForEach-Object { Write-Host "  - $_" }
    }
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    # If it's a memory error, suggest the old line-by-line method
    if ($_.Exception.Message -match "memory|OutOfMemory") {
        Write-Host ""
        Write-Host "The JSON file is too large to load into memory." -ForegroundColor Yellow
        Write-Host "Consider using the line-by-line parsing method instead." -ForegroundColor Yellow
    }
}
