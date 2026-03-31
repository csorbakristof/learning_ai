"""
MS Teams Auto-Hide Script - Simplest CDP Version
Connects to Chrome with debugging enabled
"""
from playwright.sync_api import sync_playwright
import time
import sys
from datetime import datetime
from pathlib import Path

# Configuration
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

MAX_TEAMS_TO_PROCESS = 10000  # Process all teams
# Save log file in the same directory as this script
SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / "teams_hidden_log.txt"
REMOTE_DEBUGGING_PORT = 9222


class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {level}: {message}"
        print(formatted_msg)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(formatted_msg + "\n")
    
    def info(self, msg): self.log(msg, "INFO")
    def success(self, msg): self.log(msg, "SUCCESS")
    def error(self, msg): self.log(msg, "ERROR")
    def warning(self, msg): self.log(msg, "WARNING")


def matches_pattern(team_name):
    team_name_lower = team_name.lower()
    return any(pattern.lower() in team_name_lower for pattern in PATTERNS)


def hide_team(page, team, team_name, dry_run, logger):
    try:
        if dry_run:
            logger.info(f"[DRY RUN] Would hide: {team_name}")
            return True
        
        logger.info(f"Hovering over team: {team_name}")
        team.hover()
        time.sleep(0.5)
        
        # Find options button
        options_button = team.locator('button').filter(has_text="...").first
        if options_button.count() == 0:
            options_button = team.locator('[aria-label*="More options"]').first
        
        if options_button.count() == 0:
            logger.error(f"Could not find options button")
            return False
        
        options_button.click()
        time.sleep(0.8)
        
        # Click Hide
        hide_button = page.locator('text=Hide').first
        if hide_button.count() == 0:
            logger.error(f"Could not find Hide button")
            page.keyboard.press('Escape')
            return False
        
        hide_button.click()
        time.sleep(1)
        
        logger.success(f"Hidden: {team_name}")
        return True
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return False


def main():
    dry_run = '--dry-run' in sys.argv or '-d' in sys.argv
    logger = Logger(LOG_FILE)
    
    logger.info("="*70)
    logger.info("MS Teams Auto-Hide - Simple CDP Connection")
    logger.info(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    logger.info("="*70)
    
    hidden_teams = []
    skipped_teams = []
    error_teams = []
    
    try:
        with sync_playwright() as p:
            logger.info("Connecting to Chrome...")
            
            try:
                # Use IPv4 explicitly (127.0.0.1) instead of localhost
                browser = p.chromium.connect_over_cdp(f'http://127.0.0.1:{REMOTE_DEBUGGING_PORT}')
                logger.success("Connected!")
            except Exception as e:
                logger.error(f"Failed to connect: {str(e)}")
                logger.error("Make sure Chrome is running with:")
                logger.error(f"  chrome.exe --remote-debugging-port={REMOTE_DEBUGGING_PORT}")
                return
            
            # Get first page
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else None
            
            if not page:
                logger.error("No page found")
                return
            
            logger.info(f"Current page: {page.url}")
            
            if 'teams.microsoft.com' not in page.url:
                logger.warning("Not on Teams page!")
                logger.warning("Please navigate to Teams in Chrome")
                input("Press Enter when on Teams page...")
            
            time.sleep(2)
            
            # Find teams
            logger.info("Looking for teams...")
            teams = []
            
            # Try multiple selector strategies for the new Teams UI
            try:
                # Strategy 1: Cards with team information
                teams = page.locator('article').all()
                if teams:
                    logger.info(f"Found {len(teams)} teams using article selector")
            except:
                pass
            
            if not teams:
                try:
                    # Strategy 2: Divs with data-tid attribute
                    teams = page.locator('[data-tid*="team"]').all()
                    if teams:
                        logger.info(f"Found {len(teams)} teams using data-tid selector")
                except:
                    pass
            
            if not teams:
                try:
                    # Strategy 3: Traditional list items
                    teams = page.locator('[role="listitem"]').all()
                    if teams:
                        logger.info(f"Found {len(teams)} teams using listitem selector")
                except:
                    pass
            
            if not teams:
                logger.error("No teams found!")
                page.screenshot(path="debug.png")
                logger.info("Screenshot saved: debug.png")
                return
            
            logger.info(f"Found {len(teams)} teams")
            teams_to_process = teams[:MAX_TEAMS_TO_PROCESS]
            if len(teams_to_process) == len(teams):
                logger.info(f"Processing all {len(teams_to_process)} teams...")
            else:
                logger.info(f"Processing first {len(teams_to_process)}...")
            logger.info("-"*70)
            
            for i, team in enumerate(teams_to_process):
                try:
                    team_name = team.text_content().strip()
                    
                    # Skip empty or very short names
                    if not team_name or len(team_name) < 3:
                        continue
                    
                    # Skip container elements with huge concatenated text (> 500 chars means it's likely a container)
                    if len(team_name) > 500:
                        logger.info(f"\n[{i+1}/{len(teams_to_process)}] [SKIPPED: Container element with {len(team_name)} chars]")
                        continue
                    
                    logger.info(f"\n[{i+1}/{len(teams_to_process)}] {team_name}")
                    
                    if matches_pattern(team_name):
                        logger.warning("MATCHED!")
                        if hide_team(page, team, team_name, dry_run, logger):
                            hidden_teams.append(team_name)
                        else:
                            error_teams.append(team_name)
                    else:
                        logger.info("Skipped")
                        skipped_teams.append(team_name)
                    
                    time.sleep(0.5)
                        
                except Exception as e:
                    logger.error(f"Error: {e}")
                    error_teams.append("Unknown")
            
            # Summary
            logger.info("\n" + "="*70)
            logger.info("SUMMARY")
            logger.info("="*70)
            logger.info(f"Teams processed: {len(teams_to_process)}")
            logger.info(f"Hidden: {len(hidden_teams)}")
            logger.info(f"Skipped: {len(skipped_teams)}")
            logger.info(f"Errors: {len(error_teams)}")
            
            if hidden_teams:
                logger.info("\n✓ HIDDEN:")
                for team in hidden_teams:
                    logger.info(f"  - {team}")
            
            if error_teams:
                logger.warning("\n✗ ERRORS:")
                for team in error_teams:
                    logger.warning(f"  - {team}")
            
            logger.info(f"\nLog: {LOG_FILE}")
            
            if dry_run:
                logger.info("\nDRY RUN - no actual changes")
                logger.info("Run without --dry-run to hide teams")
            
            input("\nPress Enter to finish...")
            browser.close()
            
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()
