# Registry-based sideloading for Outlook add-ins
# This method directly registers the add-in in Windows Registry

param(
    [switch]$Remove,
    [switch]$List
)

$AddInName = "DummyHelloWorldPlugin"
$ManifestUrl = "http://localhost:3001/manifest.xml"

# Registry paths for Outlook add-ins
$RegistryPaths = @(
    "HKCU:\Software\Microsoft\Office\16.0\WEF\Developer",
    "HKCU:\Software\Microsoft\Office\Outlook\Addins\$AddInName"
)

function Test-ServerRunning {
    try {
        $response = Invoke-WebRequest -Uri $ManifestUrl -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

function Install-AddIn {
    Write-Host "Installing Dummy Plugin via Registry..." -ForegroundColor Green
    
    # Check if server is running
    if (-not (Test-ServerRunning)) {
        Write-Host "✗ Server is not running on port 3001" -ForegroundColor Red
        Write-Host "Please start the server first with: npm start" -ForegroundColor Yellow
        return
    }
    
    try {
        # Create Developer registry key if it doesn't exist
        $devPath = "HKCU:\Software\Microsoft\Office\16.0\WEF\Developer"
        if (-not (Test-Path $devPath)) {
            New-Item -Path $devPath -Force | Out-Null
        }
        
        # Register the add-in
        Set-ItemProperty -Path $devPath -Name $AddInName -Value $ManifestUrl -Type String
        
        Write-Host "✓ Add-in registered successfully!" -ForegroundColor Green
        Write-Host "Manifest URL: $ManifestUrl" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Restart Outlook completely (close all Outlook windows)" -ForegroundColor White
        Write-Host "2. Open Outlook and create a new email" -ForegroundColor White
        Write-Host "3. Look for the 'Dummy Hello World Plugin' panel on the right" -ForegroundColor White
        
    } catch {
        Write-Host "✗ Failed to register add-in: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function Remove-AddIn {
    Write-Host "Removing Dummy Plugin from Registry..." -ForegroundColor Yellow
    
    try {
        $devPath = "HKCU:\Software\Microsoft\Office\16.0\WEF\Developer"
        if (Test-Path $devPath) {
            Remove-ItemProperty -Path $devPath -Name $AddInName -ErrorAction SilentlyContinue
        }
        
        Write-Host "✓ Add-in removed successfully!" -ForegroundColor Green
        Write-Host "Please restart Outlook to see changes." -ForegroundColor Yellow
        
    } catch {
        Write-Host "✗ Failed to remove add-in: $($_.Exception.Message)" -ForegroundColor Red
    }
}

function List-AddIns {
    Write-Host "Registered Developer Add-ins:" -ForegroundColor Green
    
    $devPath = "HKCU:\Software\Microsoft\Office\16.0\WEF\Developer"
    if (Test-Path $devPath) {
        $addins = Get-ItemProperty -Path $devPath -ErrorAction SilentlyContinue
        if ($addins) {
            $addins.PSObject.Properties | Where-Object { $_.Name -notmatch "^PS" } | ForEach-Object {
                Write-Host "  $($_.Name): $($_.Value)" -ForegroundColor Cyan
            }
        } else {
            Write-Host "  No add-ins registered" -ForegroundColor Gray
        }
    } else {
        Write-Host "  Developer registry path not found" -ForegroundColor Gray
    }
}

# Main execution
Write-Host "Outlook Add-in Registry Manager" -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green

if ($Remove) {
    Remove-AddIn
} elseif ($List) {
    List-AddIns
} else {
    Install-AddIn
}
