# Learning AI - GitHub Pages Local Setup (PowerShell)
# This script sets up and runs the Jekyll site locally

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Learning AI - GitHub Pages Local Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to docs directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$docsPath = Join-Path $scriptPath "docs"

if (-not (Test-Path $docsPath)) {
    Write-Host "ERROR: docs directory not found" -ForegroundColor Red
    Write-Host "Make sure this script is in the root of your repository" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Set-Location $docsPath
Write-Host "Current directory: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Check if Ruby is installed
Write-Host "Checking Ruby installation..." -ForegroundColor Yellow
try {
    $rubyVersion = & ruby --version 2>$null
    Write-Host "Ruby is installed: $rubyVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Ruby is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Ruby from: https://rubyinstaller.org/" -ForegroundColor Yellow
    Write-Host "Choose the Ruby+Devkit version for Windows" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# Check if Bundler is installed
Write-Host "Checking Bundler installation..." -ForegroundColor Yellow
try {
    $bundlerVersion = & bundle --version 2>$null
    Write-Host "Bundler is installed: $bundlerVersion" -ForegroundColor Green
} catch {
    Write-Host "Bundler not found. Installing Bundler..." -ForegroundColor Yellow
    & gem install bundler
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install Bundler" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}
Write-Host ""

# Install Jekyll dependencies
Write-Host "Installing Jekyll dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes on first run..." -ForegroundColor Cyan
& bundle install
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Write-Host ""
    Write-Host "Try running these commands manually:" -ForegroundColor Yellow
    Write-Host "  gem install bundler" -ForegroundColor White
    Write-Host "  bundle install" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""
Write-Host "Dependencies installed successfully!" -ForegroundColor Green
Write-Host ""

# Start Jekyll server
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Jekyll development server..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your site will be available at:" -ForegroundColor Green
Write-Host "http://localhost:4000/learning_ai/" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

& bundle exec jekyll serve --livereload --host=0.0.0.0 --port=4000
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to start Jekyll server" -ForegroundColor Red
    Write-Host ""
    Write-Host "If you get port conflicts, try:" -ForegroundColor Yellow
    Write-Host "  bundle exec jekyll serve --livereload --port=4001" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
}

Read-Host "Press Enter to exit"
