# MS Teams Auto-Hide Script - README

This script automatically hides MS Teams teams whose names match specific patterns using Playwright browser automation.

## Features

- ✅ Automatically hides teams matching defined patterns
- ✅ Uses your existing Chrome profile (no manual login required)
- ✅ Dry-run mode to preview changes before applying
- ✅ Processes first 10 teams (configurable)
- ✅ Detailed logging to both console and file
- ✅ Error handling - continues on failures
- ✅ Multiple selector strategies for robustness

## Target Patterns

Teams containing any of these strings (case-insensitive) will be hidden:
- "Project Laboratory"
- "Thesis Project"
- "Diplomatervezés"
- "Research Work"
- "Önálló laboratórium"
- "Informatics"
- "Szakdolgozat-készítés"
- "Diploma Thesis Design"

## Prerequisites

1. **Python 3.7+** installed
2. **Chrome browser** installed
3. **Already logged into MS Teams** in Chrome

## Installation

### Step 1: Install Playwright

Open PowerShell in this directory and run:

```powershell
python -m pip install playwright
```

### Step 2: Install Chrome browser driver

```powershell
python -m playwright install chrome
```

### Step 3: Verify installation

```powershell
python -c "from playwright.sync_api import sync_playwright; print('✓ Playwright ready')"
```

## Usage

### Important: Close Chrome First!
**You MUST close all Chrome browser windows before running the script**, as it needs exclusive access to your Chrome profile.

### Option 1: Dry Run (Recommended First)

Test the script without making any changes:

```powershell
.\run_teams_auto_hide.bat --dry-run
```

Or directly with Python:

```powershell
python teams_auto_hide.py --dry-run
```

This will:
- Show which teams would be hidden
- Not actually hide anything
- Help you verify the patterns work correctly

### Option 2: Live Run

Actually hide the teams:

```powershell
.\run_teams_auto_hide.bat
```

Or:

```powershell
python teams_auto_hide.py
```

## What Happens

1. Script checks for Chrome profile
2. Asks you to press Enter to continue (make sure Chrome is closed!)
3. Launches Chrome with your profile
4. Navigates to MS Teams
5. Locates teams in the sidebar
6. For each team (up to 10):
   - Checks if name matches patterns
   - If match: hovers, clicks "..." menu, clicks "Hide"
   - If no match: skips
   - Logs all actions
7. Shows summary report
8. Waits for you to press Enter before closing

## Output

### Console Output
Real-time progress updates with timestamps showing:
- Teams being checked
- Matches found
- Hide operations
- Errors encountered
- Summary report

### Log File
All output is also saved to: `teams_hidden_log.txt`

### Debug Screenshots
If something goes wrong, the script saves screenshots for debugging:
- `teams_page_debug.png` - If Teams page doesn't load properly
- `teams_list_debug.png` - If teams list can't be found

## Configuration

Edit `teams_auto_hide.py` to customize:

### Change number of teams to process
```python
MAX_TEAMS_TO_PROCESS = 10  # Change this number
```

### Modify patterns
```python
PATTERNS = [
    "Your Pattern Here",
    "Another Pattern",
    # Add or remove patterns
]
```

### Change Chrome profile path
```python
CHROME_PROFILE_PATH = r"C:\Your\Custom\Path\To\Chrome\Profile"
```

### Adjust delays
```python
time.sleep(0.5)  # Change sleep durations throughout the script
```

## Troubleshooting

### "Chrome profile not found"
- Check if Chrome is installed
- Verify the profile path in the script
- Default path: `%LOCALAPPDATA%\Google\Chrome\User Data`

### "Failed to launch browser"
- **Make sure Chrome is completely closed**
- Check Task Manager for chrome.exe processes
- Try closing Chrome and waiting 5-10 seconds

### "Could not find teams list"
- Check if you're logged into MS Teams
- The script will save a debug screenshot
- Open the screenshot and check what's on screen
- You may need to manually navigate to Teams first

### "Could not find options button"
- Teams UI may have changed
- Check the debug output and screenshots
- May need to update selectors in the script

### Script is too fast/slow
- Adjust `slow_mo=500` in the launch settings
- Modify `time.sleep()` durations throughout

## Safety Notes

- ✅ **Dry-run first**: Always test with `--dry-run` before live run
- ✅ **Limited scope**: Only processes first 10 teams by default
- ✅ **Reversible**: Hidden teams can be unhidden from Teams settings
- ✅ **No deletion**: This only hides teams, doesn't delete or leave them
- ✅ **Logged**: All actions are logged for review

## Tips

1. **Start with dry-run** to see what would happen
2. **Review the patterns** to make sure they match what you want
3. **Check the log file** after running to see exactly what happened
4. **Increase MAX_TEAMS_TO_PROCESS** gradually once comfortable
5. **Run multiple times** if you have many teams (10 at a time)

## Unhiding Teams

If you need to unhide a team later:
1. Open MS Teams
2. Click your profile picture → Settings
3. Go to General
4. Manage hidden teams
5. Find the team and unhide it

## Advanced Usage

### Process specific number of teams
Edit the script and change:
```python
MAX_TEAMS_TO_PROCESS = 20  # Process 20 instead of 10
```

### Add command line arguments
Modify the script to accept additional arguments like custom pattern files, different modes, etc.

### Scheduling
You could schedule this script to run periodically, but be cautious as Teams UI might change.

### Note on Commands
If `pip` or `playwright` commands are not recognized, use:
- `python -m pip` instead of `pip`
- `python -m playwright` instead of `playwright`

## Support

If something doesn't work:
1. Check the log file: `teams_hidden_log.txt`
2. Look at debug screenshots if generated
3. Make sure Chrome is completely closed
4. Verify you're logged into Teams
5. Try updating Playwright: `pip install --upgrade playwright`

## Version

- **Version**: 1.0
- **Date**: March 31, 2026
- **Browser**: Chrome
- **Framework**: Playwright with Python

---

**Note**: MS Teams web interface may change over time. If the script stops working, selectors may need to be updated.
