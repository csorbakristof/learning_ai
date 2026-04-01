"""
UI and Menu System
"""
import pygame
from config import *


class Menu:
    """Main menu system"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.selected_index = 0
        self.options = ["Start Game", "Instructions", "Quit"]
    
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
                actions = ["start", "instructions", "quit"]
                return actions[self.selected_index]
        return None


class InstructionsScreen:
    """Instructions/How to Play screen"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 60)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)
    
    def draw(self):
        """Draw instructions"""
        self.screen.fill(BLACK)
        
        # Title
        title = self.font_large.render("HOW TO PLAY", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title, title_rect)
        
        # Instructions
        instructions = [
            "",
            "CONTROLS:",
            "  Arrow Keys / WASD - Move",
            "  Spacebar - Place Bomb",
            "  ESC / P - Pause",
            "",
            "OBJECTIVE:",
            "  Defeat all enemies to win!",
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
        
        y = 120
        for line in instructions:
            if line.startswith("  "):
                text = self.font_small.render(line, True, WHITE)
            else:
                text = self.font_medium.render(line, True, YELLOW if line.endswith(":") else WHITE)
            text_rect = text.get_rect(left=150, top=y)
            self.screen.blit(text, text_rect)
            y += 35
        
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
    """Draw enhanced HUD"""
    font = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 24)
    
    # Level indicator (top center)
    level_text = font.render(f"LEVEL {level_num}", True, YELLOW)
    level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, 20))
    pygame.draw.rect(screen, BLACK, level_rect.inflate(20, 10))
    screen.blit(level_text, level_rect)
    
    # Lives (with heart icons)
    x, y = 10, 10
    lives_label = font.render("Lives:", True, WHITE)
    pygame.draw.rect(screen, BLACK, (x-5, y-5, 200, 35))
    screen.blit(lives_label, (x, y))
    
    # Draw hearts
    heart_x = x + 80
    for i in range(player.lives):
        pygame.draw.circle(screen, RED, (heart_x + i*25, y+15), 8)
        pygame.draw.circle(screen, RED, (heart_x + i*25 + 10, y+15), 8)
        points = [(heart_x + i*25 + 5, y+25), (heart_x + i*25 - 5, y+18), (heart_x + i*25 + 15, y+18)]
        pygame.draw.polygon(screen, RED, points)
    
    # Bombs
    y += 40
    bombs_text = font.render(f"Bombs: {player.bombs_available}/{player.max_bombs}", True, WHITE)
    pygame.draw.rect(screen, BLACK, (x-5, y-5, 200, 35))
    screen.blit(bombs_text, (x, y))
    
    # Power-ups (Bomb Range, Speed)
    y += 40
    pygame.draw.rect(screen, BLACK, (x-5, y-5, 200, 60))
    fire_text = font_small.render(f"Fire Range: {player.bomb_range}", True, ORANGE)
    screen.blit(fire_text, (x, y))
    speed_text = font_small.render(f"Speed: {player.speed}", True, (0, 255, 100))
    screen.blit(speed_text, (x, y+25))
    
    # Score
    y += 70
    score_text = font.render(f"Score: {score}", True, YELLOW)
    pygame.draw.rect(screen, BLACK, (x-5, y-5, 200, 35))
    screen.blit(score_text, (x, y))
    
    # Enemies remaining
    y += 40
    enemies_text = font.render(f"Enemies: {enemies_remaining}", True, RED)
    pygame.draw.rect(screen, BLACK, (x-5, y-5, 200, 35))
    screen.blit(enemies_text, (x, y))


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
