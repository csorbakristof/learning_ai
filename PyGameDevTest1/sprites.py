"""
Sprite classes for game objects
"""
import pygame
from config import *


class Player(pygame.sprite.Sprite):
    """Player character"""
    
    def __init__(self, grid_x, grid_y, walls_group, soft_blocks_group):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.walls = walls_group
        self.soft_blocks = soft_blocks_group
        
        # Player stats
        self.lives = INITIAL_LIVES
        self.max_bombs = INITIAL_MAX_BOMBS
        self.bomb_range = INITIAL_BOMB_RANGE
        self.speed = PLAYER_SPEED
        self.bombs_available = self.max_bombs
        
        # Create visual representation (blue circle on white square)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)  # Transparent background matches field
        pygame.draw.circle(self.image, BLUE, 
                          (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2 - 8)
        # Add white outline
        pygame.draw.circle(self.image, WHITE, 
                          (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2 - 8, 3)
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * TILE_SIZE
        self.rect.y = grid_y * TILE_SIZE
        
        # Movement state
        self.moving = False
        self.target_x = self.rect.x
        self.target_y = self.rect.y
    
    def update(self):
        """Update player position"""
        # Smooth movement towards target position
        if self.rect.x < self.target_x:
            self.rect.x = min(self.rect.x + self.speed, self.target_x)
        elif self.rect.x > self.target_x:
            self.rect.x = max(self.rect.x - self.speed, self.target_x)
        
        if self.rect.y < self.target_y:
            self.rect.y = min(self.rect.y + self.speed, self.target_y)
        elif self.rect.y > self.target_y:
            self.rect.y = max(self.rect.y - self.speed, self.target_y)
        
        # Update grid position when aligned
        if self.rect.x == self.target_x and self.rect.y == self.target_y:
            self.grid_x = self.rect.x // TILE_SIZE
            self.grid_y = self.rect.y // TILE_SIZE
            self.moving = False
    
    def move(self, dx, dy):
        """
        Attempt to move in the specified direction
        dx, dy should be -1, 0, or 1
        """
        # Only allow new movement if not currently moving
        if self.moving:
            return
        
        # Calculate target grid position
        new_grid_x = self.grid_x + dx
        new_grid_y = self.grid_y + dy
        
        # Check if target position is valid (not blocked)
        if self.is_position_blocked(new_grid_x, new_grid_y):
            return
        
        # Set movement target
        self.target_x = new_grid_x * TILE_SIZE
        self.target_y = new_grid_y * TILE_SIZE
        self.moving = True
    
    def is_position_blocked(self, grid_x, grid_y):
        """Check if a grid position is blocked by walls or soft blocks"""
        # Check walls
        for wall in self.walls:
            if wall.grid_x == grid_x and wall.grid_y == grid_y:
                return True
        
        # Check soft blocks
        for block in self.soft_blocks:
            if block.grid_x == grid_x and block.grid_y == grid_y:
                return True
        
        return False


class PowerUp(pygame.sprite.Sprite):
    """Power-up that enhances player abilities"""
    
    def __init__(self, grid_x, grid_y, powerup_type):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.powerup_type = powerup_type
        
        # Create visual representation based on type
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)  # Transparent background
        
        if powerup_type == POWERUP_BOMB:
            # Bomb Up - Cyan/Blue icon
            pygame.draw.circle(self.image, (0, 200, 255), 
                              (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3)
            pygame.draw.circle(self.image, WHITE, 
                              (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3, 3)
            # Draw "B" for bomb
            font = pygame.font.Font(None, 32)
            text = font.render("B", True, WHITE)
            text_rect = text.get_rect(center=(TILE_SIZE//2, TILE_SIZE//2))
            self.image.blit(text, text_rect)
            
        elif powerup_type == POWERUP_FIRE:
            # Fire Up - Orange/Red icon
            pygame.draw.circle(self.image, ORANGE, 
                              (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3)
            pygame.draw.circle(self.image, YELLOW, 
                              (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3, 3)
            # Draw "F" for fire
            font = pygame.font.Font(None, 32)
            text = font.render("F", True, WHITE)
            text_rect = text.get_rect(center=(TILE_SIZE//2, TILE_SIZE//2))
            self.image.blit(text, text_rect)
            
        elif powerup_type == POWERUP_SPEED:
            # Speed Up - Green icon
            pygame.draw.circle(self.image, (0, 255, 100), 
                              (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3)
            pygame.draw.circle(self.image, WHITE, 
                              (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3, 3)
            # Draw "S" for speed
            font = pygame.font.Font(None, 32)
            text = font.render("S", True, WHITE)
            text_rect = text.get_rect(center=(TILE_SIZE//2, TILE_SIZE//2))
            self.image.blit(text, text_rect)
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * TILE_SIZE
        self.rect.y = grid_y * TILE_SIZE


class Wall(pygame.sprite.Sprite):
    """Indestructible wall block"""
    
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        
        # Create visual representation
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(DARK_GRAY)
        # Add a border for visual distinction
        pygame.draw.rect(self.image, GRAY, self.image.get_rect(), 3)
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * TILE_SIZE
        self.rect.y = grid_y * TILE_SIZE


class SoftBlock(pygame.sprite.Sprite):
    """Destructible soft block"""
    
    def __init__(self, grid_x, grid_y):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        
        # Create visual representation
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BROWN)
        # Add pattern for visual interest
        pygame.draw.rect(self.image, LIGHT_BROWN, self.image.get_rect(), 4)
        # Draw a simple cross pattern
        pygame.draw.line(self.image, LIGHT_BROWN, 
                        (TILE_SIZE//2, 10), (TILE_SIZE//2, TILE_SIZE-10), 3)
        pygame.draw.line(self.image, LIGHT_BROWN, 
                        (10, TILE_SIZE//2), (TILE_SIZE-10, TILE_SIZE//2), 3)
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * TILE_SIZE
        self.rect.y = grid_y * TILE_SIZE


class Bomb(pygame.sprite.Sprite):
    """Bomb that explodes after a timer"""
    
    def __init__(self, grid_x, grid_y, bomb_range, owner):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.bomb_range = bomb_range
        self.owner = owner  # Reference to player who placed it
        
        # Timer
        self.placed_time = pygame.time.get_ticks()
        self.timer = BOMB_TIMER
        
        # Create visual representation (black circle that pulses)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)  # Transparent background
        pygame.draw.circle(self.image, BLACK, 
                          (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3)
        # Add fuse (small red circle on top)
        pygame.draw.circle(self.image, RED, 
                          (TILE_SIZE//2, TILE_SIZE//4), 5)
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * TILE_SIZE
        self.rect.y = grid_y * TILE_SIZE
        
        self.exploded = False
    
    def update(self):
        """Update bomb timer and check for explosion"""
        current_time = pygame.time.get_ticks()
        time_left = self.timer - (current_time - self.placed_time)
        
        # Pulse effect - make bomb blink faster as timer runs out
        if time_left > 0:
            blink_rate = max(100, time_left // 10)
            if (current_time // blink_rate) % 2 == 0:
                # Redraw bomb with different size for pulse effect
                self.image.fill(GREEN)
                size = TILE_SIZE//3 + 3
                pygame.draw.circle(self.image, BLACK, 
                                  (TILE_SIZE//2, TILE_SIZE//2), size)
                pygame.draw.circle(self.image, RED, 
                                  (TILE_SIZE//2, TILE_SIZE//4), 5)
            else:
                self.image.fill(GREEN)
                pygame.draw.circle(self.image, BLACK, 
                                  (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3)
                pygame.draw.circle(self.image, RED, 
                                  (TILE_SIZE//2, TILE_SIZE//4), 5)
        
        # Check if timer expired
        if time_left <= 0 and not self.exploded:
            self.exploded = True
    
    def is_ready_to_explode(self):
        """Check if bomb should explode"""
        return self.exploded


class Explosion(pygame.sprite.Sprite):
    """Explosion sprite that appears when bomb detonates"""
    
    def __init__(self, grid_x, grid_y, is_center=False):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        
        # Timer for explosion duration
        self.created_time = pygame.time.get_ticks()
        self.duration = EXPLOSION_DURATION
        
        # Create visual representation (orange/yellow fire)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)
        
        if is_center:
            # Center explosion is larger
            pygame.draw.circle(self.image, ORANGE, 
                              (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2 - 5)
            pygame.draw.circle(self.image, YELLOW, 
                              (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3)
        else:
            # Side explosions are more directional
            pygame.draw.circle(self.image, ORANGE, 
                              (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2 - 8)
            pygame.draw.circle(self.image, YELLOW, 
                              (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//4)
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * TILE_SIZE
        self.rect.y = grid_y * TILE_SIZE
    
    def update(self):
        """Update explosion - it disappears after duration"""
        current_time = pygame.time.get_ticks()
        if current_time - self.created_time >= self.duration:
            self.kill()  # Remove from all groups


class Enemy(pygame.sprite.Sprite):
    """Enemy with random movement AI"""
    
    def __init__(self, grid_x, grid_y, walls_group, soft_blocks_group, speed_multiplier=1.0):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.walls = walls_group
        self.soft_blocks = soft_blocks_group
        
        # Movement properties
        self.speed = int(ENEMY_SPEED * speed_multiplier)
        self.moving = False
        self.target_x = grid_x * TILE_SIZE
        self.target_y = grid_y * TILE_SIZE
        
        # AI properties
        self.direction_timer = 0
        self.direction_change_interval = 1000  # Change direction every 1 second
        self.current_direction = (0, 0)
        
        # Create visual representation (red circle)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)  # Transparent background
        pygame.draw.circle(self.image, RED, 
                          (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2 - 8)
        # Add angry eyes
        eye_y = TILE_SIZE//2 - 5
        pygame.draw.circle(self.image, WHITE, (TILE_SIZE//2 - 8, eye_y), 4)
        pygame.draw.circle(self.image, WHITE, (TILE_SIZE//2 + 8, eye_y), 4)
        pygame.draw.circle(self.image, BLACK, (TILE_SIZE//2 - 8, eye_y), 2)
        pygame.draw.circle(self.image, BLACK, (TILE_SIZE//2 + 8, eye_y), 2)
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * TILE_SIZE
        self.rect.y = grid_y * TILE_SIZE
    
    def update(self):
        """Update enemy position and AI"""
        current_time = pygame.time.get_ticks()
        
        # Update position - smooth movement towards target
        if self.rect.x < self.target_x:
            self.rect.x = min(self.rect.x + self.speed, self.target_x)
        elif self.rect.x > self.target_x:
            self.rect.x = max(self.rect.x - self.speed, self.target_x)
        
        if self.rect.y < self.target_y:
            self.rect.y = min(self.rect.y + self.speed, self.target_y)
        elif self.rect.y > self.target_y:
            self.rect.y = max(self.rect.y - self.speed, self.target_y)
        
        # Update grid position when aligned
        if self.rect.x == self.target_x and self.rect.y == self.target_y:
            self.grid_x = self.rect.x // TILE_SIZE
            self.grid_y = self.rect.y // TILE_SIZE
            self.moving = False
        
        # AI: Choose and move in random direction periodically
        if not self.moving:
            if current_time - self.direction_timer >= self.direction_change_interval:
                self.choose_random_direction()
                self.direction_timer = current_time
    
    def choose_random_direction(self):
        """Choose a random valid direction and try to move"""
        import random
        
        # Possible directions: up, down, left, right, stay
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]
        
        # Shuffle directions to try random ones first
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_grid_x = self.grid_x + dx
            new_grid_y = self.grid_y + dy
            
            # Check if position is valid
            if not self.is_position_blocked(new_grid_x, new_grid_y):
                self.target_x = new_grid_x * TILE_SIZE
                self.target_y = new_grid_y * TILE_SIZE
                self.moving = True
                self.current_direction = (dx, dy)
                break
    
    def is_position_blocked(self, grid_x, grid_y):
        """Check if a grid position is blocked by walls or soft blocks"""
        # Check walls
        for wall in self.walls:
            if wall.grid_x == grid_x and wall.grid_y == grid_y:
                return True
        
        # Check soft blocks
        for block in self.soft_blocks:
            if block.grid_x == grid_x and block.grid_y == grid_y:
                return True
        
        return False
