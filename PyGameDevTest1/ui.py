"""
UI and Menu System
"""
import pygame
from config import *
from enums import WeaponType


class Menu:
    """Main menu system"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.selected_index = 0
        self.options = ["Start Game", "Instructions", "Guide", "Quit"]
    
    def draw(self):
        """Draw main menu"""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_large.render("DYNABLASTER", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font_small.render("Bomberman Clone", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 160))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Menu options
        start_y = 280
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected_index else WHITE
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, start_y + i * 60))
            
            # Draw selection arrow
            if i == self.selected_index:
                arrow = self.font_medium.render(">", True, YELLOW)
                arrow_rect = arrow.get_rect(right=text_rect.left - 20, centery=text_rect.centery)
                self.screen.blit(arrow, arrow_rect)
            
            self.screen.blit(text, text_rect)
        
        # Controls hint
        hint = self.font_small.render("Arrow Keys + Enter", True, GRAY)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        self.screen.blit(hint, hint_rect)
    
    def handle_input(self, event):
        """Handle menu navigation"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                # Return action keys instead of full text
                actions = ["start", "instructions", "guide", "quit"]
                return actions[self.selected_index]
        return None


class InstructionsScreen:
    """Instructions/How to Play screen"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
    
    def draw(self):
        """Draw instructions"""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_large.render("HOW TO PLAY", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 40))
        self.screen.blit(title, title_rect)
        
        # Instructions
        instructions = [
            "",
            "CONTROLS:",
            "  Arrow Keys - Move",
            "  Spacebar - Place Bomb / Detonate Remote",
            "  1-5 Keys - Select Weapon",
            "  ESC / P - Pause",
            "",
            "WEAPONS:",
            "  1 - Standard Bomb (3s timer)",
            "  2 - Remote Bomb (detonate with Space)",
            "  3 - Time Bomb (5s timer)",
            "  4 - Kick Bomb (can be kicked)",
            "  5 - Landmine (invisible, enemy trigger)",
            "",
            "OBJECTIVE:",
            "  Defeat all enemies to win!",
            "",
            "ENEMIES:",
            "  Red - Normal speed, random movement",
            "  Orange - Fast movement",
            "  Purple - Smart, tracks player",
            "  Green - Wall Breaker, destroys blocks",
            "  Gray - Tank, needs multiple hits",
            "  Yellow - Bomb Layer, places bombs",
            "  Cyan - Ghost, phases through walls",
            "  Pink - Splitter, splits when destroyed",
            "",
            "POWER-UPS:",
            "  [B] Bomb Up - Place more bombs",
            "  [F] Fire Up - Larger explosions",
            "  [S] Speed Up - Move faster",
            "",
            "AVOID:",
            "  Your own explosions",
            "  Touching enemies",
        ]
        
        y = 90
        for line in instructions:
            if line.startswith("  "):
                text = self.font_small.render(line, True, WHITE)
            else:
                text = self.font_medium.render(line, True, YELLOW if line.endswith(":") else WHITE)
            text_rect = text.get_rect(left=150, top=y)
            self.screen.blit(text, text_rect)
            y += 30
        
        # Back instruction
        back_text = self.font_medium.render("Press ESC to return", True, GRAY)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 40))
        self.screen.blit(back_text, back_rect)
    
    def handle_input(self, event):
        """Handle input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back"
        return None


class GuideScreen:
    """Enemy and Weapon Guide screen"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 22)
    
    def draw(self):
        """Draw enemy and weapon guide"""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_large.render("ENEMY & WEAPON GUIDE", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 30))
        self.screen.blit(title, title_rect)
        
        # Two column layout
        left_x = 50
        right_x = SCREEN_WIDTH // 2 + 30
        
        # --- ENEMIES SECTION ---
        y = 80
        enemies_title = self.font_medium.render("ENEMIES:", True, (255, 100, 100))
        self.screen.blit(enemies_title, (left_x, y))
        y += 35
        
        enemies = [
            ("Red - Normal:", "Random movement, normal speed"),
            ("Orange - Fast:", "Fast random movement"),
            ("Purple - Smart:", "Tracks and chases player"),
            ("Green - Wall Breaker:", "Destroys soft blocks while moving"),
            ("Gray - Tank:", "Requires 2-3 hits to defeat"),
            ("Yellow - Bomb Layer:", "Places bombs periodically"),
            ("Cyan - Ghost:", "Can phase through walls"),
            ("Pink - Splitter:", "Splits into mini enemies when destroyed"),
        ]
        
        for name, desc in enemies:
            # Name in color
            name_text = self.font_small.render(name, True, YELLOW)
            self.screen.blit(name_text, (left_x + 10, y))
            y += 22
            # Description
            desc_text = self.font_small.render(desc, True, WHITE)
            self.screen.blit(desc_text, (left_x + 20, y))
            y += 30
        
        # --- WEAPONS SECTION ---
        y = 80
        weapons_title = self.font_medium.render("WEAPONS:", True, (100, 150, 255))
        self.screen.blit(weapons_title, (right_x, y))
        y += 35
        
        weapons = [
            ("Standard Bomb:", "3-second timer, cross explosion"),
            ("Line Bomb:", "Directional explosion in a line"),
            ("Time Bomb:", "Customizable timer"),
            ("Remote Bomb:", "Detonates with spacebar"),
            ("Kick Bomb:", "Can be kicked to slide"),
            ("Landmine:", "Invisible, triggers on enemy contact"),
        ]
        
        for name, desc in weapons:
            # Name in color
            name_text = self.font_small.render(name, True, (100, 255, 200))
            self.screen.blit(name_text, (right_x + 10, y))
            y += 22
            # Description
            desc_text = self.font_small.render(desc, True, WHITE)
            self.screen.blit(desc_text, (right_x + 20, y))
            y += 30
        
        # Note about weapon selection
        note_y = SCREEN_HEIGHT - 100
        note = self.font_small.render("(Weapon selection coming in future update)", True, GRAY)
        note_rect = note.get_rect(center=(SCREEN_WIDTH//2, note_y))
        self.screen.blit(note, note_rect)
        
        # Back instruction
        back_text = self.font_medium.render("Press ESC to return", True, GRAY)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 40))
        self.screen.blit(back_text, back_rect)
    
    def handle_input(self, event):
        """Handle input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back"
        return None


class PauseMenu:
    """Pause menu overlay"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.selected_index = 0
        self.options = ["Resume", "Restart", "Main Menu"]
    
    def draw(self):
        """Draw pause overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause title
        title = self.font_large.render("PAUSED", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title, title_rect)
        
        # Menu options
        start_y = 280
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected_index else WHITE
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, start_y + i * 60))
            
            # Draw selection arrow
            if i == self.selected_index:
                arrow = self.font_medium.render(">", True, YELLOW)
                arrow_rect = arrow.get_rect(right=text_rect.left - 20, centery=text_rect.centery)
                self.screen.blit(arrow, arrow_rect)
            
            self.screen.blit(text, text_rect)
    
    def handle_input(self, event):
        """Handle pause menu navigation"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                # Return action keys instead of full text
                actions = ["resume", "restart", "menu"]
                return actions[self.selected_index]
            elif event.key in [pygame.K_ESCAPE, pygame.K_p]:
                return "resume"
        return None


def draw_hud(screen, player, score, enemies_remaining, level_num=1):
    """Draw enhanced HUD in horizontal header bar"""
    # Draw header background
    header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, HEADER_HEIGHT)
    pygame.draw.rect(screen, BLACK, header_rect)
    pygame.draw.line(screen, GRAY, (0, HEADER_HEIGHT), (SCREEN_WIDTH, HEADER_HEIGHT), 2)
    
    # Use smaller fonts for compact header
    font = pygame.font.Font(None, 24)
    font_tiny = pygame.font.Font(None, 18)
    
    # Starting x position
    x = 10
    y = HEADER_HEIGHT // 2
    
    # Level indicator (left side)
    level_text = font.render(f"LV{level_num}", True, YELLOW)
    level_rect = level_text.get_rect(midleft=(x, y))
    screen.blit(level_text, level_rect)
    x += 60
    
    # Lives (with small hearts)
    lives_text = font_tiny.render("Lives:", True, WHITE)
    lives_rect = lives_text.get_rect(midleft=(x, y))
    screen.blit(lives_text, lives_rect)
    x += 40
    
    # Draw small hearts
    for i in range(player.lives):
        heart_x = x + i * 20
        heart_y = y
        pygame.draw.circle(screen, RED, (heart_x, heart_y), 5)
        pygame.draw.circle(screen, RED, (heart_x + 6, heart_y), 5)
        points = [(heart_x + 3, heart_y + 7), (heart_x - 3, heart_y + 2), (heart_x + 9, heart_y + 2)]
        pygame.draw.polygon(screen, RED, points)
    x += player.lives * 20 + 20
    
    # Separator
    pygame.draw.line(screen, GRAY, (x, 8), (x, HEADER_HEIGHT - 8), 1)
    x += 15
    
    # Bombs
    bombs_text = font.render(f"Bombs: {player.bombs_available}/{player.max_bombs}", True, WHITE)
    bombs_rect = bombs_text.get_rect(midleft=(x, y))
    screen.blit(bombs_text, bombs_rect)
    x += 120
    
    # Fire range
    fire_text = font.render(f"Fire: {player.bomb_range}", True, ORANGE)
    fire_rect = fire_text.get_rect(midleft=(x, y))
    screen.blit(fire_text, fire_rect)
    x += 80
    
    # Speed
    speed_text = font.render(f"Speed: {player.speed}", True, (0, 255, 100))
    speed_rect = speed_text.get_rect(midleft=(x, y))
    screen.blit(speed_text, speed_rect)
    x += 100    
    # Separator
    pygame.draw.line(screen, GRAY, (x, 8), (x, HEADER_HEIGHT - 8), 1)
    x += 15
    
    # Current weapon
    weapon_name = player.weapon_names.get(player.current_weapon, "Unknown")
    weapon_text = font.render(f"Weapon: {weapon_name}", True, (100, 200, 255))
    weapon_rect = weapon_text.get_rect(midleft=(x, y))
    screen.blit(weapon_text, weapon_rect)
    
    # Show key hint below weapon name
    weapon_key_map = {
        WeaponType.STANDARD: "1",
        WeaponType.REMOTE: "2",
        WeaponType.TIMED: "3",
        WeaponType.KICK: "4",
        WeaponType.LANDMINE: "5"
    }
    key_hint = weapon_key_map.get(player.current_weapon, "?")
    key_hint_text = font_tiny.render(f"[{key_hint}]", True, (80, 160, 200))
    key_hint_rect = key_hint_text.get_rect(midleft=(x + 5, y + 12))
    screen.blit(key_hint_text, key_hint_rect)
    
    x += 160    
    # Separator
    pygame.draw.line(screen, GRAY, (x, 8), (x, HEADER_HEIGHT - 8), 1)
    x += 15
    
    # Score (centered-right area)
    score_text = font.render(f"Score: {score}", True, YELLOW)
    score_rect = score_text.get_rect(midleft=(x, y))
    screen.blit(score_text, score_rect)
    x += 130
    
    # Enemies remaining (right side)
    enemies_text = font.render(f"Enemies: {enemies_remaining}", True, RED)
    enemies_rect = enemies_text.get_rect(midleft=(x, y))
    screen.blit(enemies_text, enemies_rect)


def draw_game_over_screen(screen, score, blocks_destroyed, enemies_defeated):
    """Draw game over screen"""
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 36)
    
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Game over text
    game_over_text = font_large.render("GAME OVER", True, RED)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80))
    screen.blit(game_over_text, game_over_rect)
    
    # Stats
    final_score = font_medium.render(f"Final Score: {score}", True, WHITE)
    final_score_rect = final_score.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 10))
    screen.blit(final_score, final_score_rect)
    
    stats = font_medium.render(f"Blocks: {blocks_destroyed} | Enemies: {enemies_defeated}", True, WHITE)
    stats_rect = stats.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
    screen.blit(stats, stats_rect)
    
    # Instructions
    restart_text = font_medium.render("Press R to Restart", True, YELLOW)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 90))
    screen.blit(restart_text, restart_rect)
    
    menu_text = font_medium.render("Press M for Main Menu", True, YELLOW)
    menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 130))
    screen.blit(menu_text, menu_rect)


class LevelTransitionScreen:
    """Level transition screen - shows when player completes a level"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
    
    def draw(self, level_num, score, blocks_destroyed, enemies_defeated):
        """Draw level complete screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Level complete text
        title = self.font_large.render(f"LEVEL {level_num} COMPLETE!", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 120))
        self.screen.blit(title, title_rect)
        
        # Level stats
        y = 220
        score_text = self.font_medium.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, y))
        self.screen.blit(score_text, score_rect)
        
        y += 60
        blocks_text = self.font_small.render(f"Blocks Destroyed: {blocks_destroyed}", True, WHITE)
        blocks_rect = blocks_text.get_rect(center=(SCREEN_WIDTH//2, y))
        self.screen.blit(blocks_text, blocks_rect)
        
        y += 50
        enemies_text = self.font_small.render(f"Enemies Defeated: {enemies_defeated}", True, WHITE)
        enemies_rect = enemies_text.get_rect(center=(SCREEN_WIDTH//2, y))
        self.screen.blit(enemies_text, enemies_rect)
        
        # Instructions
        y += 100
        continue_text = self.font_medium.render("Press SPACE for Next Level", True, YELLOW)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, y))
        self.screen.blit(continue_text, continue_rect)
        
        y += 60
        menu_text = self.font_small.render("Press M for Main Menu", True, GRAY)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, y))
        self.screen.blit(menu_text, menu_rect)


def draw_victory_screen(screen, score, blocks_destroyed, enemies_defeated, is_final_level=False):
    """Draw victory screen (level complete or game complete)"""
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 36)
    
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Victory text - different if final level
    if is_final_level:
        victory_text = font_large.render("GAME COMPLETE!", True, YELLOW)
        subtitle = font_medium.render("You defeated all enemies!", True, WHITE)
    else:
        victory_text = font_large.render("LEVEL COMPLETE!", True, YELLOW)
        subtitle = font_medium.render("", True, WHITE)
    
    victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
    screen.blit(victory_text, victory_rect)
    
    if is_final_level:
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(subtitle, subtitle_rect)
    
    # Stats
    final_score = font_medium.render(f"Final Score: {score}", True, WHITE)
    final_score_rect = final_score.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(final_score, final_score_rect)
    
    stats = font_medium.render(f"Blocks: {blocks_destroyed} | Enemies: {enemies_defeated}", True, WHITE)
    stats_rect = stats.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
    screen.blit(stats, stats_rect)
    
    # Instructions
    y_offset = 100 if is_final_level else 90
    if not is_final_level:
        next_text = font_medium.render("Press SPACE for Next Level", True, YELLOW)
        next_rect = next_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + y_offset))
        screen.blit(next_text, next_rect)
        y_offset += 40
    
    restart_text = font_medium.render("Press R to Restart", True, YELLOW)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + y_offset))
    screen.blit(restart_text, restart_rect)
    
    menu_text = font_medium.render("Press M for Main Menu", True, GRAY)
    menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + y_offset + 40))
    screen.blit(menu_text, menu_rect)
