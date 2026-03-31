# Quick Reference Guide - MS Teams Auto-Hide

## Quick Start (4 Steps)

### 1. Launch Chrome with Debugging
```powershell
cd E:\learning_ai\TeamsUnsubscriber
.\START_CHROME_AUTOMATION.bat
```
This will:
- Close existing Chrome windows
- Launch Chrome with remote debugging on port 9222
- Open Teams automatically

### 2. Log Into Teams
- **Log in manually** in the Chrome window that opens
- Navigate to the Teams page if needed
- **Leave Chrome running** (don't close it!)

### 3. Test with Dry-Run (Preview Only)
```powershell
python teams_auto_hide_simple.py --dry-run
```
This shows what would be hidden without making changes.

### 4. Run Live Mode (Actually Hide Teams)
```powershell
python teams_auto_hide_simple.py
```
This will actually hide matching teams.

---

## Important Notes

### ✅ Do This
- Keep Chrome running while script executes
- Check `E:\learning_ai\TeamsUnsubscriber\teams_hidden_log.txt` for detailed logs
- Run dry-run first to preview changes
- Script processes first 10 teams at a time

### ❌ Don't Do This
- Don't close Chrome while script is running
- Don't use your default Chrome profile (script uses temp profile)
- Don't run multiple instances simultaneously

---

## Verification Commands

**Check if Chrome debugging is ready:**
```powershell
curl http://127.0.0.1:9222/json/version
```
Should return JSON with Chrome version info.

**Check script can find teams:**
Run dry-run mode - it will show how many teams were found.

---

## Current Configuration

**In `teams_auto_hide_simple.py`:**
- **Browser**: Chrome with DevTools Protocol (CDP)
- **Port**: 9222 (remote debugging)
- **Max Teams**: 10 per run (change `MAX_TEAMS_TO_PROCESS`)
- **Patterns**: 8 predefined patterns (case-insensitive)
- **Logging**: Console + `teams_hidden_log.txt`
- **Dry-run**: Available with `--dry-run` flag

**Matched Patterns:**
1. "Project Laboratory"
2. "Thesis Project"
3. "Diplomatervezés"
4. "Research Work"
5. "Önálló laboratórium"
6. "Informatics"
7. "Szakdolgozat-készítés"
8. "Diploma Thesis Design"

---

## Customization

### Change Number of Teams to Process
Edit `teams_auto_hide_simple.py`:
```python
MAX_TEAMS_TO_PROCESS = 10  # Change to 20, 50, etc.
```

### Add/Remove Patterns
Edit the `PATTERNS` list:
```python
PATTERNS = [
    "Project Laboratory",
    "Your Custom Pattern",  # Add your own
    # ...
]
```

### Change Delays
```python
time.sleep(0.5)  # Adjust delay between actions (seconds)
```

---

## Troubleshooting

### "Connection refused" Error
**Problem:** Script can't connect to Chrome
**Solution:**
1. Make sure Chrome is running via `START_CHROME_AUTOMATION.bat`
2. Verify port: `curl http://127.0.0.1:9222/json/version`
3. Check Chrome didn't crash (should stay open)

### "No teams found" Error
**Problem:** Script can't locate teams in the page
**Solution:**
1. Make sure you're logged into Teams
2. Navigate to: https://teams.microsoft.com/v2/
3. Wait for page to fully load
4. Check `debug.png` screenshot for page state

### Script Finds Container Element
**Normal:** You might see `[SKIPPED: Container element with XXXX chars]`
**Reason:** Script filters out container divs (>500 chars)
**Action:** None needed - this is expected behavior

### Profile Conflicts
**Problem:** "DevTools remote debugging requires a non-default data directory"
**Solution:** Script already uses temp profile (`%TEMP%\chrome_automation_profile`)

---

**File Overview

- `teams_auto_hide_simple.py` - **Main automation script (CDP approach)**
- `START_CHROME_AUTOMATION.bat` - **Chrome launcher with debugging**
- `teams_hidden_log.txt` - Execution log in `TeamsUnsubscriber` folder (created after run)
- `SimpleBrowserBasedUnsubscribe.md` - Full documentation
- `QUICK_START.md` - This file

**Debug files (created as needed):**
- `debug.png` - Screenshot when errors occur (in `TeamsUnsubscriber` folder)
