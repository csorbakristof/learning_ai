"""
MS Teams Auto-Hide Script - Using CDP Connection
Automatically hides Teams teams matching specific patterns.
"""
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

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

# Settings
MAX_TEAMS_TO_PROCESS = 10
LOG_FILE = "teams_hidden_log.txt"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    CHROME_PATH = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
REMOTE_DEBUGGING_PORT = 9222


class Logger:
    """Logs to both console and file"""
    def __init__(self, log_file):
        self.log_file = log_file
        self.start_time = datetime.now()
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {level}: {message}"
        print(formatted_msg)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(formatted_msg + "\n")
    
    def info(self, message):
        self.log(message, "INFO")
    
    def success(self, message):
        self.log(message, "SUCCESS")
    
    def error(self, message):
        self.log(message, "ERROR")
    
    def warning(self, message):
        self.log(message, "WARNING")


def matches_pattern(team_name: str) -> bool:
    """Check if team name contains any of the target patterns (case-insensitive)"""
    team_name_lower = team_name.lower()
    return any(pattern.lower() in team_name_lower for pattern in PATTERNS)


def launch_chrome_with_debugging(logger):
    """Launch Chrome with remote debugging enabled"""
    try:
        # Check if Chrome is already running with debugging
        try:
            import requests
            response = requests.get(f'http://localhost:{REMOTE_DEBUGGING_PORT}/json/version', timeout=2)
            if response.status_code == 200:
                logger.info("Chrome is already running with remote debugging enabled")
                return True
        except:
            pass
        
        # Launch Chrome with remote debugging
        logger.info("Launching Chrome with remote debugging...")
        cmd = [
            CHROME_PATH,
            f'--remote-debugging-port={REMOTE_DEBUGGING_PORT}',
            '--no-first-run',
            '--no-default-browser-check'
        ]
        
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)  # Wait for Chrome to start
        
        # Verify it's running
        try:
            import requests
            response = requests.get(f'http://localhost:{REMOTE_DEBUGGING_PORT}/json/version', timeout=5)
            if response.status_code == 200:
                logger.success("Chrome launched successfully with debugging enabled")
                return True
        except:
            pass
        
        logger.error("Failed to verify Chrome debugging port")
        return False
        
    except Exception as e:
        logger.error(f"Error launching Chrome: {str(e)}")
        return False


def hide_team(page, team, team_name, dry_run, logger):
    """Attempt to hide a team"""
    try:
        if dry_run:
            logger.info(f"[DRY RUN] Would hide: {team_name}")
            return True
        
        # Hover to reveal options menu
        logger.info(f"Hovering over team: {team_name}")
        team.hover()
        time.sleep(0.5)
        
        # Find and click "..." button - try multiple selector strategies
        logger.info(f"Looking for options button...")
        options_button = None
        
        # Strategy 1: ARIA label with "More options"
        try:
            options_button = team.locator('[aria-label*="More options"]').first
            if options_button.count() > 0:
                logger.info(f"Found options button via ARIA label")
        except:
            pass
        
        # Strategy 2: Button with specific class or role
        if not options_button or options_button.count() == 0:
            try:
                options_button = team.locator('button[role="button"]').filter(has_text="...").first
                if options_button.count() > 0:
                    logger.info(f"Found options button via text filter")
            except:
                pass
        
        # Strategy 3: Any button within the team item
        if not options_button or options_button.count() == 0:
            try:
                buttons = team.locator('button').all()
                # Try to find button that looks like options menu
                for btn in buttons:
                    aria_label = btn.get_attribute('aria-label') or ""
                    if 'more' in aria_label.lower() or 'options' in aria_label.lower():
                        options_button = btn
                        logger.info(f"Found options button via iteration")
                        break
            except:
                pass
        
        if not options_button or options_button.count() == 0:
            logger.error(f"Could not find options button for: {team_name}")
            return False
        
        # Click the options button
        logger.info(f"Clicking options button...")
        options_button.click()
        time.sleep(0.8)
        
        # Wait for menu and click "Hide"
        logger.info(f"Looking for 'Hide' menu item...")
        hide_button = page.locator('text=Hide').first
        
        if hide_button.count() == 0:
            # Try alternative text
            hide_button = page.locator('[role="menuitem"]').filter(has_text="Hide").first
        
        if hide_button.count() == 0:
            logger.error(f"Could not find 'Hide' menu item for: {team_name}")
            # Try to close menu by pressing Escape
            page.keyboard.press('Escape')
            return False
        
        logger.info(f"Clicking 'Hide'...")
        hide_button.click()
        time.sleep(1)
        
        logger.success(f"Successfully hidden: {team_name}")
        return True
        
    except Exception as e:
        logger.error(f"Exception while hiding team '{team_name}': {str(e)}")
        return False


def main():
    # Check for dry-run mode
    dry_run = '--dry-run' in sys.argv or '-d' in sys.argv
    
    # Initialize logger
    logger = Logger(LOG_FILE)
    logger.info("="*70)
    logger.info("MS Teams Auto-Hide Script Started (CDP Connection Method)")
    logger.info(f"Mode: {'DRY RUN (no actual changes)' if dry_run else 'LIVE (will hide teams)'}")
    logger.info(f"Max teams to process: {MAX_TEAMS_TO_PROCESS}")
    logger.info(f"Target patterns: {', '.join(PATTERNS)}")
    logger.info("="*70)
    
    # Check if Chrome exists
    if not os.path.exists(CHROME_PATH):
        logger.error(f"Chrome not found at: {CHROME_PATH}")
        logger.error("Please update CHROME_PATH in the script.")
        return
    
    logger.info(f"Chrome path: {CHROME_PATH}")
    
    # Launch or connect to Chrome
    if not launch_chrome_with_debugging(logger):
        logger.error("Failed to launch Chrome with debugging. Please try:")
        logger.error(f"  {CHROME_PATH} --remote-debugging-port={REMOTE_DEBUGGING_PORT}")
        return
    
    logger.info("Chrome is ready. You should now:")
    logger.info("1. Navigate to MS Teams in the Chrome browser window")
    logger.info("2. Log in if needed")
    logger.info("3. Go to the Teams page")
    logger.warning("\nPress Enter once you're on the Teams page...")
    input()
    
    hidden_teams = []
    skipped_teams = []
    error_teams = []
    
    try:
        with sync_playwright() as p:
            logger.info("Connecting to Chrome...")
            
            try:
                browser = p.chromium.connect_over_cdp(f'http://localhost:{REMOTE_DEBUGGING_PORT}')
                logger.success("Connected to Chrome!")
                
                # Get the active context and page
                contexts = browser.contexts
                if not contexts:
                    logger.error("No browser contexts found")
                    return
                
                context = contexts[0]
                pages = context.pages
                
                if not pages:
                    logger.error("No pages found in browser")
                    return
                
                # Use the first page (should be Teams)
                page = pages[0]
                logger.info(f"Using page: {page.url}")
                
            except Exception as e:
                logger.error(f"Failed to connect to Chrome: {str(e)}")
                logger.error("Make sure Chrome is running with remote debugging.")
                return
            
            time.sleep(2)  # Additional wait for dynamic content
            
            # Wait for teams list to load
            logger.info("Waiting for teams list to load...")
            try:
                # Try different selectors for the teams list
                found = False
                selectors = [
                    '[data-tid="team-list"]',
                    '[role="navigation"]',
                    '[aria-label*="Teams"]',
                    'nav[role="navigation"]'
                ]
                
                for selector in selectors:
                    try:
                        page.wait_for_selector(selector, timeout=10000)
                        logger.info(f"Teams list found with selector: {selector}")
                        found = True
                        break
                    except:
                        continue
                
                if not found:
                    logger.warning("Could not find teams list with known selectors - taking screenshot...")
                    page.screenshot(path="teams_page_debug.png")
                    logger.info("Screenshot saved as: teams_page_debug.png")
                    logger.info("Please inspect the page manually and update selectors.")
                    logger.warning("Continuing with best effort...")
                    
            except Exception as e:
                logger.error(f"Error waiting for teams list: {str(e)}")
            
            # Get all team elements - try multiple strategies
            logger.info("Locating team elements...")
            teams = []
            
            try:
                # Strategy 1: List items in navigation
                teams = page.locator('[role="navigation"] [role="listitem"]').all()
                if teams:
                    logger.info(f"Found {len(teams)} teams using navigation listitem selector")
            except:
                pass
            
            if not teams:
                try:
                    # Strategy 2: Any list items
                    teams = page.locator('[role="listitem"]').all()
                    if teams:
                        logger.info(f"Found {len(teams)} teams using generic listitem selector")
                except:
                    pass
            
            if not teams:
                logger.error("Could not find any team elements!")
                logger.info("Taking screenshot for debugging...")
                page.screenshot(path="teams_list_debug.png")
                logger.info("Screenshot saved as: teams_list_debug.png")
                return
            
            # Limit to first N teams
            teams_to_process = teams[:MAX_TEAMS_TO_PROCESS]
            logger.info(f"Processing first {len(teams_to_process)} teams...")
            logger.info("-"*70)
            
            for i, team in enumerate(teams_to_process):
                try:
                    # Extract team name
                    team_name = team.text_content().strip()
                    
                    # Skip if empty or very short (likely not a real team name)
                    if not team_name or len(team_name) < 3:
                        continue
                    
                    logger.info(f"\n[{i+1}/{len(teams_to_process)}] Team: {team_name}")
                    
                    if matches_pattern(team_name):
                        logger.warning(f"MATCHED pattern - attempting to hide...")
                        if hide_team(page, team, team_name, dry_run, logger):
                            hidden_teams.append(team_name)
                        else:
                            error_teams.append(team_name)
                    else:
                        logger.info(f"Skipped - no pattern match")
                        skipped_teams.append(team_name)
                    
                    # Small delay between teams
                    time.sleep(0.5)
                        
                except Exception as e:
                    logger.error(f"Error processing team: {e}")
                    error_teams.append(f"Unknown team (error: {str(e)})")
            
            logger.info("\n" + "="*70)
            logger.info("SUMMARY REPORT")
            logger.info("="*70)
            logger.info(f"Total teams processed: {len(teams_to_process)}")
            logger.info(f"Teams hidden: {len(hidden_teams)}")
            logger.info(f"Teams skipped: {len(skipped_teams)}")
            logger.info(f"Errors encountered: {len(error_teams)}")
            
            if hidden_teams:
                logger.info("\n✓ HIDDEN TEAMS:")
                for team in hidden_teams:
                    logger.info(f"  - {team}")
            
            if error_teams:
                logger.warning("\n✗ TEAMS WITH ERRORS:")
                for team in error_teams:
                    logger.warning(f"  - {team}")
            
            logger.info("\n" + "="*70)
            logger.info("Script completed!")
            logger.info(f"Log saved to: {LOG_FILE}")
            
            if dry_run:
                logger.info("\nThis was a DRY RUN - no actual changes were made.")
                logger.info("Run without --dry-run flag to actually hide teams.")
            
            input("\nPress Enter to disconnect (Chrome will stay open)...")
            browser.close()
            
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()
