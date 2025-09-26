param(
    [Parameter(Mandatory=$true)]
    [string]$Directory
)

# Function to write colored output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

# Validate directory parameter
if (-not (Test-Path $Directory)) {
    Write-ColorOutput Red "Error: Directory '$Directory' does not exist."
    exit 1
}

if (-not (Test-Path $Directory -PathType Container)) {
    Write-ColorOutput Red "Error: '$Directory' is not a directory."
    exit 1
}

# Get absolute path
$Directory = Resolve-Path $Directory

Write-ColorOutput Green "Cleaning build artifacts from: $Directory"
Write-Host ""

# Define directories to remove
$DirsToRemove = @("bin", "obj", ".vs")

# Initialize counters
$TotalRemoved = 0
$TotalSizeMB = 0

foreach ($DirName in $DirsToRemove) {
    Write-ColorOutput Cyan "Searching for '$DirName' directories..."
    
    # Find all directories with the specified name
    $FoundDirs = Get-ChildItem -Path $Directory -Name $DirName -Directory -Recurse -Force -ErrorAction SilentlyContinue
    
    if ($FoundDirs) {
        foreach ($Dir in $FoundDirs) {
            $FullPath = Join-Path $Directory $Dir
            
            try {
                # Calculate directory size before removal
                $Size = 0
                if (Test-Path $FullPath) {
                    $Size = (Get-ChildItem -Path $FullPath -Recurse -Force -ErrorAction SilentlyContinue | 
                            Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
                    if ($Size) {
                        $SizeMB = [math]::Round($Size / 1MB, 2)
                        $TotalSizeMB += $SizeMB
                        Write-Host "  Removing: $FullPath ($SizeMB MB)" -ForegroundColor Yellow
                    } else {
                        Write-Host "  Removing: $FullPath (empty)" -ForegroundColor Yellow
                    }
                    
                    # Remove directory
                    Remove-Item -Path $FullPath -Recurse -Force -ErrorAction Stop
                    $TotalRemoved++
                }
            }
            catch {
                Write-ColorOutput Red "  Failed to remove: $FullPath"
                Write-ColorOutput Red "  Error: $($_.Exception.Message)"
            }
        }
    } else {
        Write-Host "  No '$DirName' directories found." -ForegroundColor Gray
    }
    
    Write-Host ""
}

# Summary
Write-ColorOutput Green "=== Cleanup Summary ==="
Write-Host "Total directories removed: $TotalRemoved" -ForegroundColor White
Write-Host "Total space freed: $([math]::Round($TotalSizeMB, 2)) MB" -ForegroundColor White

if ($TotalRemoved -eq 0) {
    Write-ColorOutput Gray "No build artifacts found to clean."
} else {
    Write-ColorOutput Green "Cleanup completed successfully!"
}