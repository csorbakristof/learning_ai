# MS Teams Auto-Hide Task

## Quick Start Guide

**TL;DR - Working solution using Chrome DevTools Protocol:**

1. **Launch Chrome with debugging:**
   ```powershell
   cd E:\learning_ai\TeamsUnsubscriber
   .\START_CHROME_AUTOMATION.bat
   ```

2. **Log into Teams** in the Chrome window that opens

3. **Run automation script (dry-run first):**
   ```powershell
   python teams_auto_hide_simple.py --dry-run
   ```

4. **Run live mode** to actually hide teams:
   ```powershell
   python teams_auto_hide_simple.py
   ```

See [Working Solution](#working-solution-chrome-devtools-protocol-cdp-approach) section below for detailed documentation.

---

## Objective
Automatically hide MS Teams teams whose names match specific patterns by using browser automation.

## Context
- **Teams Page**: Navigate to `https://teams.microsoft.com/v2/?ring=ring3_6`
- **Target Patterns**: Teams containing any of:
  - "Project Laboratory"
  - "Thesis Project"
  - "Diplomatervezés" (Hungarian for "Thesis Project")
- **Action**: Hide matching teams using the "..." menu → "Hide" option

## Task Description

### Starting Point
Navigate to the MS Teams web interface at:
```
https://teams.microsoft.com/v2/?ring=ring3_6
```

### Process Flow
1. **Navigate to Teams Page**: Open the main Teams page where all teams are listed
2. **Locate Teams List**: Find the section/sidebar containing all teams (usually on the left side)
3. **Iterate Through Visible Teams**: For each team in the list:
   - Read the team name
   - Check if the team name contains any of the target patterns (case-insensitive)
   - If it matches:
     - Locate the "..." (more options) button for that specific team
     - Click on it to open the context menu
     - Find and click the "Hide" option
     - Wait for confirmation that the action completed
   - Log the result (hidden/skipped)
4. **Handle Scrolling**: If the teams list is scrollable, ensure all teams are processed
5. **Report**: Generate a summary of all actions taken

### UI Elements to Target
Based on the Teams web interface structure:
- **Teams List**: The left sidebar containing all teams
  - Look for a list/navigation component with team names
  - Teams are typically displayed as list items with names visible
- **Team Name**: Text element within each team list item
- **More Options Button**: Look for ellipsis ("...") button next to each team name, typically:
  - Class patterns: `fui-Primitive`, `fui-Icon`, or similar Fluent UI classes
  - SVG icons with specific classes
  - May appear on hover over the team item
- **Dynamic Content**: Teams list may load dynamically, wait for it to appear
- **Scrolling**: The teams list may require scrolling to see all teams
- **Hover Actions**: The "..." menu might only appear on hover
- **Rate Limiting**: Add delays between actions to avoid issues
- **Error Handling**: Handle cases where:
  - Page doesn't load
  - Teams list is not visible
  - Team name cannot be extracted
  - Menu options are not available
  - Team is already hidden
- **Logging**: Keep detailed logs of:
  - Teams foundere:
  - Page doesn't load
  - Team name cannot be extracted
  - Menu options are not available
  - Team is already hidden
- **Logging**: Keep detailed logs of:
  - Teams checked
  - Teams hidden
  - Errors encountered

## Navigates to the MS Teams main page: https://teams.microsoft.com/v2/?ring=ring3_6
2. Waits for the page to fully load and the teams list to appear (wait for network idle)
3. Locates the teams list section (typically in the left sidebar)
4. Gets all team elements from the list
5. For each team in the list:
   - Extracts the team name
   - Checks if the team name matches any of these patterns (case-insensitive, name has to contain one of these as substring):
     * "Project Laboratory"
     * "Thesis Project"
     * "Diplomatervezés"
     * "Research Work"
     * "Önálló laboratórium"
     * "Informatics"
     * "Szakdolgozat-készítés"
     * "Diploma Thesis Design"
   - If it matches:
     * Hover over the team item (may be needed to reveal the "..." button)
     * Find and click the "..." (more options) button for that team
     * Wait for the context menu to appear
     * Click the "Hide" option in the menu
     * Wait for the action to complete
     * Log: "Hidden: [Team Name]"
   - If it doesn't match:
     * Log: "Skipped: [Team Name]"
6. Handle scrolling if needed to process all teams in the list
7. Output a summary report with:
   - Total teams found
   - Teams hidden (with names)
   - Teams skipped (with names)
   - Any errors encountered

Requirements:
- Use a browser automation framework (Playwright recommended for modern web apps)
- Handle authentication by using an existing browser profile or manual login step
- Add appropriate waits (1-2 seconds between actions)
- Handle dynamic loading of teams list
- Include error handling and retry logic
- Make the script configurable (patterns should be easy to modify)
- Provide progress updates during execution

Technical hints:
- MS Teams uses Fluent UI components
- Wait for elements using stable selectors (data attributes or ARIA labels preferred)
- The teams list is usually a navigation component on the left side
- Team names are visible as text in the list items
- The "..." menu might be a button with aria-label="More options" or similar
- The button may only appear on hover, so use page.hover() before clicking
- Use page.waitForSelector() with appropriate timeouts
- Consider scrolling within the teams list container if it's scrollable
- MS Teams uses Fluent UI components
- WNavigate to: https://teams.microsoft.com/v2/?ring=ring3_6
4. Login if needed
5. Go through the teams list on the left sidebar:
   - Check each team name
   - If it matches pattern (contains "Project Laboratory", "Thesis Project", or "Diplomatervezés"):
     * Hover over the team
     * Click "..." button
     * Click "Hide"
   - Continue to next team
6. Scroll through the entire list to ensure all teams are checked
## Alternative Approach: Manual with Simple Browser

If automation is complex, use VS Code Simple Browser manually:

1. Open Command Palette (Ctrl+Shift+P)
2. Run "Simple Browser: Show"
3. For each URL in `teams_urls.txt`:
   - Copy URL
   - Paste in Simple Browser
   - Check team name
   - If matches pattern: Click "..." → "Hide"
   - Move to next URL

## Expected Outcomes
- Matching teams are hidden from the Teams sidebar
- Non-matching teams remain visible
- A log/report of all actions taken

## Notes
- Teams can be unhidden later from Teams settings if needed
- This operation only affects visibility, not membership
- Consider testing with 2-3 URLs first before processing all teams

---

## ⚠️ Original Approach (Has Issues - See CDP Approach Above)

**Note:** The browser profile approach below was the initial plan but encountered several issues during implementation. **Use the [CDP approach](#working-solution-chrome-devtools-protocol-cdp-approach) above instead**, which is the verified working solution.

Issues with this approach:
- Profile conflicts when Chrome is running
- "DevTools remote debugging requires a non-default data directory" error  
- IPv6 localhost connection problems

---

## Playwright with Python Implementation

### Why Playwright with Python?
- **Modern web app support**: Excellent handling of MS Teams' dynamic Fluent UI components
- **Auto-waiting**: Built-in smart waiting reduces timing issues
- **Browser profiles**: Can use existing logged-in Edge/Chrome profile (no manual login needed)
- **Hover interactions**: Native support for hover-to-reveal menus
- **Robust selectors**: Strong support for ARIA labels, data attributes, and text content
- **Active development**: Maintained by Microsoft, well-documented

### Setup Instructions

#### 1. Install Python Prerequisites
```powershell
# Install Playwright
pip install playwright

# Install browser binaries (Chromium recommended, or Edge)
playwright install chromium
# OR for Edge:
playwright install msedge
```

#### 2. Verify Installation
```powershell
python -c "from playwright.sync_api import sync_playwright; print('Playwright installed successfully')"
```

### Implementation Approach

#### Option A: Use Existing Browser Profile (Recommended)
This allows you to reuse your existing Teams login session.

**Find your browser profile:**
- **Edge**: `%LOCALAPPDATA%\Microsoft\Edge\User Data`
- **Chrome**: `%LOCALAPPDATA%\Google\Chrome\User Data`

**Note**: Close the browser before running the script when using an existing profile.

#### Option B: Manual Login
Launch browser in normal (non-headless) mode and log in manually when prompted.

### Script Structure

**File: `teams_auto_hide.py`**

```python
from playwright.sync_api import sync_playwright
import time
import re

# Configuration
TEAMS_URL = "https://teams.microsoft.com/v2/?ring=ring3_6"
PATTERNS = [
    "Project Laboratory",
    "Thesis Project",
    "Diplomatervezés",
    "Research Work",
    "Önálló laboratórium",
    "Informatics",
    "Szakdolgozat-készítés",
    "Diploma Thesis Design"
]

def matches_pattern(team_name: str) -> bool:
    """Check if team name contains any of the target patterns (case-insensitive)"""
    team_name_lower = team_name.lower()
    return any(pattern.lower() in team_name_lower for pattern in PATTERNS)

def main():
    with sync_playwright() as p:
        # Launch browser (choose one approach)
        
        # Approach 1: With existing profile (recommended)
        browser = p.chromium.launch_persistent_context(
            user_data_dir=r"C:\Users\YourUsername\AppData\Local\Microsoft\Edge\User Data",
            headless=False,
            slow_mo=500  # Slow down operations for visibility
        )
        page = browser.pages[0]
        
        # Approach 2: Fresh browser with manual login
        # browser = p.chromium.launch(headless=False, slow_mo=500)
        # page = browser.new_page()
        
        # Navigate to Teams
        page.goto(TEAMS_URL, wait_until="networkidle")
        
        # Wait for teams list to load (adjust selector as needed)
        page.wait_for_selector('[data-tid="team-list"]', timeout=30000)
        
        # Get all team elements
        teams = page.locator('[role="listitem"]').all()
        
        hidden_teams = []
        skipped_teams = []
        
        for i, team in enumerate(teams):
            try:
                # Extract team name
                team_name = team.text_content().strip()
                
                print(f"[{i+1}/{len(teams)}] Checking: {team_name}")
                
                if matches_pattern(team_name):
                    # Hover to reveal options menu
                    team.hover()
                    time.sleep(0.5)
                    
                    # Find and click "..." button
                    options_button = team.locator('[aria-label*="More options"]').first
                    options_button.click()
                    
                    # Wait for menu and click "Hide"
                    page.locator('text=Hide').click()
                    time.sleep(1)
                    
                    hidden_teams.append(team_name)
                    print(f"  ✓ Hidden: {team_name}")
                else:
                    skipped_teams.append(team_name)
                    print(f"  - Skipped: {team_name}")
                    
            except Exception as e:
                print(f"  ✗ Error processing team: {e}")
        
        # Summary report
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Total teams found: {len(teams)}")
        print(f"Teams hidden: {len(hidden_teams)}")
        print(f"Teams skipped: {len(skipped_teams)}")
        print("\nHidden teams:")
        for team in hidden_teams:
            print(f"  - {team}")
        
        browser.close()

if __name__ == "__main__":
    main()
```

### Key Implementation Details

#### Selector Strategy
1. **Teams List Container**: `[data-tid="team-list"]` or `[role="navigation"]`
2. **Team Items**: `[role="listitem"]` within the teams list
3. **Team Name**: Usually the main text content of the list item
4. **Options Button**: `[aria-label*="More options"]` or button with ellipsis
5. **Hide Menu Item**: `text=Hide` or `[role="menuitem"]:has-text("Hide")`

#### Error Handling Enhancements
```python
# Add retry logic
def hide_team_with_retry(team, team_name, max_retries=3):
    for attempt in range(max_retries):
        try:
            team.hover()
            time.sleep(0.5)
            options_button = team.locator('[aria-label*="More options"]').first
            options_button.click()
            page.locator('text=Hide').click()
            return True
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
    return False
```

#### Scrolling Support
```python
# If teams list is scrollable, scroll to load all teams
teams_container = page.locator('[data-tid="team-list"]')
teams_container.evaluate("element => element.scrollTo(0, element.scrollHeight)")
time.sleep(2)  # Wait for lazy loading
```

### Running the Script

```powershell
# Navigate to the project directory
cd e:\learning_ai\TeamsUnsubscriber

# Run the script
python teams_auto_hide.py
```

### Debugging Tips

1. **Inspect Elements**: Use browser DevTools (F12) to verify selectors
2. **Slow Mode**: Keep `slow_mo=500` to watch actions in real-time
3. **Screenshots**: Add `page.screenshot(path="debug.png")` for debugging
4. **Console Logs**: Check browser console for errors
5. **Verbose Mode**: Add more print statements to track progress

### Testing Approach

---

## Working Solution: Chrome DevTools Protocol (CDP) Approach

### Overview
After troubleshooting, the **Chrome DevTools Protocol (CDP)** approach proved most reliable:
- Connects to an already-running Chrome instance via remote debugging port
- Uses IPv4 (127.0.0.1) explicitly to avoid localhost IPv6 issues
- Requires separate automation profile (not the default Chrome profile)
- User logs into Teams manually, then automation script controls the browser

### Why CDP Instead of Browser Profiles?
**Problem with persistent contexts:**
- Chrome error: "DevTools remote debugging requires a non-default data directory"
- Cannot use `launch_persistent_context()` with default profiles
- Profile conflicts when Chrome is already running

**CDP Solution:**
- Launch Chrome manually with debugging enabled
- Script connects to existing Chrome session
- No profile conflicts
- User stays logged in to Teams

### Setup Steps

#### 1. Install Python Prerequisites
```powershell
# Activate virtual environment (if using one)
e:\learning_ai\.venv\Scripts\Activate.ps1

# Install Playwright
pip install playwright

# Install Chromium browser
playwright install chromium

# Install requests library for connection verification
pip install requests
```

#### 2. Launch Chrome with Remote Debugging

**Option A: Use the provided batch file (Recommended)**
```powershell
cd E:\learning_ai\TeamsUnsubscriber
.\START_CHROME_AUTOMATION.bat
```

**Option B: Manual launch**
```powershell
# Close all Chrome windows first
taskkill /F /IM chrome.exe

# Launch Chrome with debugging enabled
& "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" `
  --remote-debugging-port=9222 `
  --user-data-dir="$env:TEMP\chrome_automation_profile" `
  https://teams.microsoft.com/v2/?ring=ring3_6
```

#### 3. Log into Teams
- Chrome will open to Teams page
- **Log in manually** if needed
- Navigate to the Teams main page
- Leave Chrome running

#### 4. Run the Automation Script

**Dry-run mode (preview only, no changes):**
```powershell
python teams_auto_hide_simple.py --dry-run
```

**Live mode (actually hide teams):**
```powershell
python teams_auto_hide_simple.py
```

### Working Script Structure

**File: `teams_auto_hide_simple.py`**

Key features:
```python
import sys
import time
import requests
from playwright.sync_api import sync_playwright

# Configuration
REMOTE_DEBUGGING_PORT = 9222
MAX_TEAMS_TO_PROCESS = 10  # Process first 10 teams
LOG_FILE = "teams_hidden_log.txt"

# Patterns to match (case-insensitive substring matching)
PATTERNS = [
    "Project Laboratory",
    "Thesis Project",
    "Diplomatervezés",
    "Research Work",
    "Önálló laboratórium",
    "Informatics",
    "Szakdolgozat-készítés",
    "Diploma Thesis Design"
]

# Connect to Chrome via CDP using IPv4 explicitly
browser = p.chromium.connect_over_cdp(f'http://127.0.0.1:{REMOTE_DEBUGGING_PORT}')

# Use existing Chrome context and page
context = browser.contexts[0]
page = context.pages[0]

# Find teams using multiple selector strategies
try:
    teams = page.locator('article').all()  # Card-based layout
except:
    teams = page.locator('[data-tid*="team"]').all()  # Data attributes

# Process each team
for team in teams:
    team_name = team.text_content().strip()
    
    # Filter out container elements (>500 chars = likely a container)
    if len(team_name) > 500:
        continue
    
    # Check patterns and hide if match
    if matches_pattern(team_name):
        hide_team(team, dry_run)
```

### Key Implementation Details

#### IPv4 Connection (Critical)
```python
# ✓ CORRECT - Use explicit IPv4
browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')

# ✗ WRONG - May try IPv6 and fail
browser = p.chromium.connect_over_cdp('http://localhost:9222')
```

#### Container Element Filtering
Teams UI has container elements with concatenated text from all children:
```python
# Skip container elements with huge text content
if len(team_name) > 500:
    logger.info(f"[SKIPPED: Container element with {len(team_name)} chars]")
    continue
```

#### Selector Strategy Priority
1. **`article`** elements (card-based Teams UI)
2. **`[data-tid*="team"]`** (data attribute matching)
3. **`[role="listitem"]`** (traditional list items)

### Verification Commands

**Check if Chrome debugging port is responding:**
```powershell
curl http://127.0.0.1:9222/json/version
```

**Expected output:**
```json
{
  "Browser": "Chrome/...",
  "Protocol-Version": "1.3",
  "User-Agent": "Mozilla/5.0 ...",
  "WebKit-Version": "..."
}
```

### Troubleshooting

#### "Connection refused" errors
- Make sure Chrome is running with `--remote-debugging-port=9222`
- Verify port is open: `curl http://127.0.0.1:9222/json/version`
- Check no firewall is blocking port 9222

#### "No teams found" errors
- Navigate to Teams page in Chrome: https://teams.microsoft.com/v2/
- Make sure you're logged in
- Wait for Teams to fully load before running script
- Check debug.png screenshot for UI state

#### "Container element" warnings
- Normal behavior - script filters out container divs
- Only individual team cards should be processed

#### Profile conflicts
- Use separate profile: `--user-data-dir="%TEMP%\chrome_automation_profile"`
- Never use default profile with remote debugging

### Configuration

**Script configuration** in `teams_auto_hide_simple.py`:
- `MAX_TEAMS_TO_PROCESS = 10` - Process first 10 teams at a time
- `REMOTE_DEBUGGING_PORT = 9222` - Chrome debugging port
- `LOG_FILE = "teams_hidden_log.txt"` - Log file path
- `PATTERNS = [...]` - List of patterns to match (case-insensitive)

**Dry-run mode:**
```powershell
python teams_auto_hide_simple.py --dry-run  # Preview only
python teams_auto_hide_simple.py            # Actually hide teams
```

---

## Original Answers and Requirements

**Initial requirements (before troubleshooting):**

- Browser Choice: Chrome
- Authentication Method: Use existing browser profile
- Pattern Configuration: Hardcode patterns in the script
- Safety Features:
  - ✅ **Dry-run mode** - Implemented with `--dry-run` flag
  - ✅ **No confirmation needed** - Script runs immediately
  - ✅ **Process 10 at a time** - Configured via `MAX_TEAMS_TO_PROCESS = 10`
  - ✅ **Continue on errors** - Error handling logs and continues
- Output/Logging: ✅ Both console and `teams_hidden_log.txt`
- Location: `e:\learning_ai\TeamsUnsubscriber\teams_auto_hide_simple.py`

**What changed during implementation:**
- ❌ **Browser profile approach failed** → ✅ **CDP connection approach works**
- ❌ **`launch_persistent_context()` had conflicts** → ✅ **`connect_over_cdp()` reliable**
- ❌ **localhost had IPv6 issues** → ✅ **127.0.0.1 explicit IPv4 works**
- ✅ **Manual Teams login required** (user logs in, then script automates)
- ✅ **Added container element filtering** (>500 chars = skip)
- ✅ **Multiple selector strategies** (article, data-tid, role-based)

**Final working approach:** Chrome DevTools Protocol with manual Chrome launch and Teams login.

---

