# Start Dynablaster (Bomberman Clone)
# This script activates the virtual environment and runs the game

# Get the script directory and navigate properly
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Go up one level to find .venv
Set-Location ..

# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Go back to game directory
Set-Location PyGameDevTest1

# Run the game
python main.py

# Keep window open if there's an error
if ($LASTEXITCODE -ne 0) {
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
