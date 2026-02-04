#!/usr/bin/env powershell

<#
.SYNOPSIS
    Auto Teams Leaver Script
    
.DESCRIPTION
    This script reads Teams URLs from teams_urls.txt and automatically opens each one
    in your default browser with a configurable delay, allowing you to manually leave each team.
    
.PARAMETER DelaySeconds
    Seconds to wait between opening each URL (default: 3)
    
.PARAMETER SkipConfirmation
    Skip the confirmation prompt and start immediately
    
.PARAMETER StartFromIndex
    Start from a specific team index (useful if you need to resume)
    
.EXAMPLE
    .\auto_leave_teams_clean.ps1
    # Uses default settings (3 second delay, shows confirmation)
    
.EXAMPLE
    .\auto_leave_teams_clean.ps1 -DelaySeconds 5 -SkipConfirmation
    # Uses 5 second delay and skips confirmation
    
.EXAMPLE
    .\auto_leave_teams_clean.ps1 -StartFromIndex 50
    # Starts from the 50th team (useful for resuming)
#>

param(
    [int]$DelaySeconds = 3,
    [switch]$SkipConfirmation,
    [int]$StartFromIndex = 0
)

# Colors for output
$Colors = @{
    Info = "Cyan"
    Success = "Green"
    Warning = "Yellow"
    Error = "Red"
    Progress = "Magenta"
}

function Write-ColorText {
    param([string]$Text, [string]$Color = "White")
    Write-Host $Text -ForegroundColor $Colors[$Color]
}

function Show-Header {
    Clear-Host
    Write-ColorText "═══════════════════════════════════════" "Info"
    Write-ColorText "        AUTO TEAMS LEAVER SCRIPT        " "Info"
    Write-ColorText "═══════════════════════════════════════" "Info"
    Write-Host ""
}

function Read-TeamsUrls {
    param([string]$FilePath)
    
    if (-not (Test-Path $FilePath)) {
        Write-ColorText "Error: File '$FilePath' not found!" "Error"
        return @()
    }
    
    Write-ColorText "Reading Teams URLs from '$FilePath'..." "Info"
    
    try {
        $content = Get-Content $FilePath -ErrorAction Stop
        $urls = $content | Where-Object { 
            $_ -match "^https://teams\.microsoft\.com/l/team/" 
        }
        
        if ($urls.Count -eq 0) {
            Write-ColorText "No Teams URLs found in the file!" "Warning"
            return @()
        }
        
        Write-ColorText "Found $($urls.Count) Teams URLs to process." "Success"
        return $urls
    }
    catch {
        Write-ColorText "Error reading file: $($_.Exception.Message)" "Error"
        return @()
    }
}

function Show-Preview {
    param([array]$Urls, [int]$StartIndex)
    
    $totalCount = $Urls.Count
    $remainingCount = $totalCount - $StartIndex
    
    Write-ColorText "PROCESSING SUMMARY:" "Info"
    Write-Host "  Total Teams URLs: " -NoNewline
    Write-ColorText $totalCount "Success"
    
    if ($StartIndex -gt 0) {
        Write-Host "  Starting from index: " -NoNewline
        Write-ColorText $StartIndex "Warning"
        Write-Host "  Teams to process: " -NoNewline
        Write-ColorText $remainingCount "Success"
    }
    
    Write-Host "  Delay between URLs: " -NoNewline
    Write-ColorText "$DelaySeconds seconds" "Info"
    
    $estimatedTime = [math]::Round(($remainingCount * $DelaySeconds) / 60, 1)
    Write-Host "  Estimated time: " -NoNewline
    Write-ColorText "$estimatedTime minutes" "Info"
    Write-Host ""
    
    if ($StartIndex -lt $totalCount -and $StartIndex -ge 0) {
        Write-ColorText "First few Teams to process:" "Info"
        $previewCount = [math]::Min(5, $remainingCount)
        for ($i = 0; $i -lt $previewCount; $i++) {
            $url = $Urls[$StartIndex + $i]
            $groupId = if ($url -match "groupId=([^&]+)") { $matches[1] } else { "Unknown" }
            Write-Host "  $($i + 1). " -NoNewline
            Write-ColorText $groupId "Progress"
        }
        if ($remainingCount -gt 5) {
            Write-ColorText "  ... and $($remainingCount - 5) more" "Info"
        }
    }
    Write-Host ""
}

function Get-UserConfirmation {
    Write-ColorText "IMPORTANT INSTRUCTIONS:" "Warning"
    Write-Host "1. Each Teams URL will open in your default browser"
    Write-Host "2. You need to manually click 'Leave team' for each one"
    Write-Host "3. Press Ctrl+C at any time to stop the script"
    Write-Host "4. The script will wait $DelaySeconds seconds between each URL"
    Write-Host ""
    
    do {
        Write-Host "Do you want to continue? " -NoNewline
        Write-ColorText "[Y/N]" "Info"
        $response = Read-Host
    } while ($response -notmatch '^[YyNn]$')
    
    return $response -match '^[Yy]$'
}

function Open-TeamsUrl {
    param([string]$Url, [int]$Index, [int]$Total)
    
    try {
        # Extract team ID for display
        $groupId = if ($Url -match "groupId=([^&]+)") { $matches[1] } else { "Unknown ID" }
        
        Write-Host "[$($Index + 1)/$Total] " -NoNewline -ForegroundColor $Colors["Progress"]
        Write-Host "Opening team: " -NoNewline
        Write-ColorText $groupId "Info"
        
        # Open URL in browser by launching browser directly
        # Try Chrome first, then Edge
        $chromePath = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        $edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        
        if (Test-Path $chromePath) {
            Start-Process -FilePath $chromePath -ArgumentList $Url
        }
        elseif (Test-Path $edgePath) {
            Start-Process -FilePath $edgePath -ArgumentList $Url
        }
        else {
            # Fallback to other paths
            $chromePath64 = "C:\Program Files\Google\Chrome\Application\chrome.exe"
            $edgePath64 = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
            
            if (Test-Path $chromePath64) {
                Start-Process -FilePath $chromePath64 -ArgumentList $Url
            }
            elseif (Test-Path $edgePath64) {
                Start-Process -FilePath $edgePath64 -ArgumentList $Url
            }
            else {
                throw "Could not find Chrome or Edge browser"
            }
        }
        
        return $true
    }
    catch {
        Write-ColorText "Error opening URL: $($_.Exception.Message)" "Error"
        return $false
    }
}

function Start-ProcessingTeams {
    param([array]$Urls, [int]$StartIndex)
    
    $totalCount = $Urls.Count
    $processedCount = 0
    $errorCount = 0
    
    Write-ColorText "Starting to process Teams URLs..." "Success"
    Write-ColorText "Press Ctrl+C to stop at any time." "Warning"
    Write-Host ""
    
    for ($i = $StartIndex; $i -lt $totalCount; $i++) {
        try {
            $success = Open-TeamsUrl -Url $Urls[$i] -Index $i -Total $totalCount
            
            if ($success) {
                $processedCount++
            } else {
                $errorCount++
            }
            
            # Don't wait after the last URL
            if ($i -lt ($totalCount - 1)) {
                Write-Host "Waiting $DelaySeconds seconds..." -ForegroundColor $Colors["Info"]
                Start-Sleep -Seconds $DelaySeconds
            }
            
            Write-Host ""
        }
        catch {
            Write-ColorText "Unexpected error: $($_.Exception.Message)" "Error"
            $errorCount++
        }
    }
    
    # Show summary
    Write-Host ""
    Write-ColorText "═══════════════════════════════════════" "Success"
    Write-ColorText "           PROCESSING COMPLETE          " "Success"
    Write-ColorText "═══════════════════════════════════════" "Success"
    Write-Host "Teams processed: " -NoNewline
    Write-ColorText $processedCount "Success"
    if ($errorCount -gt 0) {
        Write-Host "Errors: " -NoNewline
        Write-ColorText $errorCount "Error"
    }
    Write-Host "Total time: " -NoNewline
    Write-ColorText "$([math]::Round(($processedCount * $DelaySeconds) / 60, 1)) minutes" "Info"
}

# Main execution
try {
    Show-Header
    
    # Read URLs from file
    $urlsFile = Join-Path $PSScriptRoot "teams_urls.txt"
    $teamsUrls = Read-TeamsUrls -FilePath $urlsFile
    
    if ($teamsUrls.Count -eq 0) {
        Write-ColorText "No Teams URLs to process. Exiting." "Warning"
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Validate start index
    if ($StartFromIndex -ge $teamsUrls.Count) {
        Write-ColorText "Start index ($StartFromIndex) is greater than total URLs ($($teamsUrls.Count)). Exiting." "Error"
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    if ($StartFromIndex -lt 0) {
        $StartFromIndex = 0
    }
    
    # Show preview
    Show-Preview -Urls $teamsUrls -StartIndex $StartFromIndex
    
    # Get confirmation unless skipped
    if (-not $SkipConfirmation) {
        if (-not (Get-UserConfirmation)) {
            Write-ColorText "Operation cancelled by user." "Warning"
            Read-Host "Press Enter to exit"
            exit 0
        }
    }
    
    Write-Host ""
    
    # Process the URLs
    Start-ProcessingTeams -Urls $teamsUrls -StartIndex $StartFromIndex
    
    Write-Host ""
    Write-ColorText "Script completed! Remember to actually leave the teams in your browser." "Success"
    Read-Host "Press Enter to exit"
}
catch {
    Write-ColorText "Fatal error: $($_.Exception.Message)" "Error"
    Write-ColorText "Stack trace: $($_.Exception.StackTrace)" "Error"
    Read-Host "Press Enter to exit"
    exit 1
}
