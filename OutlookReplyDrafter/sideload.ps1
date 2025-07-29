# Set source path to your manifest file
$manifestSource = "e:\_AI_projects\OutlookReplyDrafter\outlook-addin\manifest.xml"

# Destination folder for sideloaded add-ins
$wefPath = "$env:LOCALAPPDATA\Microsoft\Office\16.0\Wef"

# Create folder if it doesn't exist
if (!(Test-Path $wefPath)) {
    New-Item -ItemType Directory -Path $wefPath | Out-Null
}

# Copy the manifest file
Copy-Item -Path $manifestSource -Destination $wefPath -Force

# Confirm
Write-Host "✅ Manifest copied to: $wefPath"
Write-Host "➡️ Restart Outlook to see the add-in."
