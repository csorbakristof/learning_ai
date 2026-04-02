"""
Sprite classes for game objects
"""
import pygame
from config import *
from assets import get_sprite_cache
from enums import EnemyType, WallType, WeaponType, PowerUpType, EntityCategory, PassabilityCondition
from behaviors import (
    MovementBehavior, RandomMovement, TrackingMovement,
    ExplosionBehavior, CrossExplosion,
    PassabilityRule, AlwaysBlockRule, EntityTypeRule,
    WeaponBehavior, StandardBombBehavior
)


class Player(pygame.sprite.Sprite):
    """Player character"""
    
    def __init__(self, grid_x, grid_y, walls_group, soft_blocks_group, bombs_group):
        super().__init__()
        
        # Type classification for extensibility
        self.entity_category = EntityCategory.PLAYER
        
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.walls = walls_group
        self.soft_blocks = soft_blocks_group
        self.bombs = bombs_group
        
        # Player stats
        self.lives = INITIAL_LIVES
        self.max_bombs = INITIAL_MAX_BOMBS
        self.bomb_range = INITIAL_BOMB_RANGE
        self.speed = PLAYER_SPEED
        self.bombs_available = self.max_bombs
        
        # Special abilities (for future extensions)
        self.can_pass_bombs = False
        self.can_pass_walls = False
        self.has_shield = False
        self.can_kick_bombs = False
        self.can_remote_detonate = False
        
        # Load sprite image
        sprite_cache = get_sprite_cache()
        self.image = sprite_cache.player.copy()
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * TILE_SIZE
        self.rect.y = grid_y * TILE_SIZE + HEADER_HEIGHT
        
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
            self.grid_y = (self.rect.y - HEADER_HEIGHT) // TILE_SIZE
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
        self.target_y = new_grid_y * TILE_SIZE + HEADER_HEIGHT
        self.moving = True
    
    def is_position_blocked(self, grid_x, grid_y):
        """Check if a grid position is blocked by walls, soft blocks, or bombs"""
        # Check walls (with passability rules)
        for wall in self.walls:
            if wall.grid_x == grid_x and wall.grid_y == grid_y:
                # Check if player can pass through this wall
                if not self._can_pass_wall(wall):
                    return True
        
        # Check soft blocks (with passability rules)
        for block in self.soft_blocks:
            if block.grid_x == grid_x and block.grid_y == grid_y:
                # Check if player can pass through soft blocks
                if not self.can_pass_walls:  # can_pass_walls also allows soft blocks
                    return True
        
        # Check bombs (but allow moving away from current position)
        for bomb in self.bombs:
            if bomb.grid_x == grid_x and bomb.grid_y == grid_y:
                # Allow moving away from current position (e.g., after placing bomb)
                if grid_x != self.grid_x or grid_y != self.grid_y:
                    # Check if player can pass through bombs
                    if not self.can_pass_bombs:
                        return True
        
        return False
    
    def _can_pass_wall(self, wall):
        """Check if player can pass through a specific wall"""
        # Use wall's passability rule if it has one
        if hasattr(wall, 'passability_rule'):
            return wall.passability_rule.can_pass(self, wall)
        
        # Default: cannot pass indestructible walls
        if hasattr(wall, 'wall_type'):
            if wall.wall_type == WallType.INDESTRUCTIBLE:
                return False
            elif wall.wall_type == WallType.PLAYER_ONLY:
                return True
            elif wall.wall_type == WallType.MONSTER_ONLY:
                return False
        
        # Fallback: hard walls block, unless player has ability
        return self.can_pass_walls


class PowerUp(pygame.sprite.Sprite):
    """Power-up that enhances player abilities"""
    
    def __init__(self, grid_x, grid_y, powerup_type):
        super().__init__()
        
        # Type classification for extensibility
        self.entity_category = EntityCategory.POWERUP
        self.powerup_enum = self._string_to_enum(powerup_type)
        
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.powerup_type = powerup_type
        
        # Load sprite image based on type
        sprite_cache = get_sprite_cache()
        if powerup_type == POWERUP_BOMB:
            self.image = sprite_cache.powerup_bomb.copy()
        elif powerup_type == POWERUP_FIRE:
            self.image = sprite_cache.powerup_fire.copy()
        elif powerup_type == POWERUP_SPEED:
            self.image = sprite_cache.powerup_speed.copy()
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * TILE_SIZE
        self.rect.y = grid_y * TILE_SIZE + HEADER_HEIGHT
    
    def _string_to_enum(self, powerup_type):
        """Convert string type to enum for extensibility"""
        if powerup_type == POWERUP_BOMB:
            return PowerUpType.BOMB_UP
        elif powerup_type == POWERUP_FIRE:
            return PowerUpType.FIRE_UP
        elif powerup_type == POWERUP_SPEED:
            return PowerUpType.SPEED_UP
        return None


class Wall(pygame.sprite.Sprite):
    """Indestructible wall block"""
    
    def __init__(self, grid_x, grid_y, wall_type=None, passability_rule=None):
        super().__init__()
        
        # Type classification for extensibility
        self.entity_category = EntityCategory.WALL
        self.wall_type = wall_type if wall_type else WallType.INDESTRUCTIBLE
        
        # Passability rule for conditional walls
        self.passability_rule = passability_rule if passability_rule else AlwaysBlockRule()
        
        self.grid_x = grid_x
        self.grid_y = grid_y
        
        # Load sprite image
        sprite_cache = get_sprite_cache()
        self.image = sprite_cache.wall.copy()
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * TILE_SIZE
        self.rect.y = grid_y * TILE_SIZE + HEADER_HEIGHT


class SoftBlock(pygame.sprite.Sprite):
    """Destructible soft block"""
    
    def __init__(self, grid_x, grid_y):
        super().__init__()
        
        # Type classification for extensibility
        self.entity_category = EntityCategory.WALL
        self.wall_type = WallType.DESTRUCTIBLE
        
        self.grid_x = grid_x
        self.grid_y = grid_y
        
        # Load sprite image
        sprite_cache = get_sprite_cache()
        self.image = sprite_cache.soft_block.copy()
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * TILE_SIZE
        self.rect.y = grid_y * TILE_SIZE + HEADER_HEIGHT


class Bomb(pygame.sprite.Sprite):
    """Bomb that explodes after a timer"""
    
    def __init__(self, grid_x, grid_y, bomb_range, owner, weapon_type=None, weapon_behavior=None, explosion_behavior=None):
        super().__init__()
        
        # Type classification for extensibility
        self.entity_category = EntityCategory.WEAPON
        self.weapon_type = weapon_type if weapon_type else WeaponType.STANDARD
        
        # Behavior composition for extensibility
        self.weapon_behavior = weapon_behavior if weapon_behavior else StandardBombBehavior()
        self.explosion_behavior = explosion_behavior if explosion_behavior else CrossExplosion()
        
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.bomb_range = bomb_range
        self.owner = owner  # Reference to player who placed it
        
        # Timer
        self.placed_time = pygame.time.get_ticks()
        self.timer = BOMB_TIMER
        
        # Load initial sprite image
        sprite_cache = get_sprite_cache()
        self.sprite_cache = sprite_cache  # Store reference for animation
        self.image = sprite_cache.get_bomb_frame(0)
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * TILE_SIZE
        self.rect.y = grid_y * TILE_SIZE + HEADER_HEIGHT
        
        self.exploded = False
        
        # Call behavior initialization
        self.weapon_behavior.on_place(self)
    
    def update(self):
        """Update bomb timer and check for explosion"""
        current_time = pygame.time.get_ticks()
        time_left = self.timer - (current_time - self.placed_time)
        
        # Animate bomb with pulsing effect based on time remaining
        if time_left > 0:
            # Calculate pulse value (0.0 to 1.0)
            pulse_value = (current_time % 500) / 500.0  # Pulse every 500ms
            self.image = self.sprite_cache.get_bomb_frame(pulse_value)
        
        # Call behavior update
        self.weapon_behavior.on_update(self)
        
        # Check if timer expired or behavior says to explode
        if time_left <= 0 and not self.exploded:
            self.exploded = True
        elif self.weapon_behavior.should_explode(self):
            self.exploded = True
    
    def is_ready_to_explode(self):
        """Check if bomb should explode"""
        return self.exploded or self.weapon_behavior.should_explode(self)


class Explosion(pygame.sprite.Sprite):
    """Explosion sprite that appears when bomb detonates"""
    
    def __init__(self, grid_x, grid_y, is_center=False):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        
        # Timer for explosion duration
        self.created_time = pygame.time.get_ticks()
        self.duration = EXPLOSION_DURATION
        
        # Load sprite image
        sprite_cache = get_sprite_cache()
        self.image = sprite_cache.explosion.copy()
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * TILE_SIZE
        self.rect.y = grid_y * TILE_SIZE + HEADER_HEIGHT
    
    def update(self):
        """Update explosion - it disappears after duration"""
        current_time = pygame.time.get_ticks()
        if current_time - self.created_time >= self.duration:
            self.kill()  # Remove from all groups


class Enemy(pygame.sprite.Sprite):
    """Enemy with random movement AI"""
    
    def __init__(self, grid_x, grid_y, walls_group, soft_blocks_group, bombs_group, speed_multiplier=1.0, enemy_type=None, movement_behavior=None):
        super().__init__()
        
        # Type classification for extensibility
        self.entity_category = EntityCategory.ENEMY
        self.enemy_type = enemy_type if enemy_type else EnemyType.NORMAL
        
        # Behavior composition for extensibility
        self.movement_behavior = movement_behavior if movement_behavior else RandomMovement()
        
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.walls = walls_group
        self.soft_blocks = soft_blocks_group
        self.bombs = bombs_group
        
        # Movement properties
        self.speed = int(ENEMY_SPEED * speed_multiplier)
        self.moving = False
        self.target_x = grid_x * TILE_SIZE
        self.target_y = grid_y * TILE_SIZE
        
        # AI properties
        self.direction_timer = 0
        self.direction_change_interval = 1000  # Change direction every 1 second
        self.current_direction = (0, 0)
        
        # Special abilities (for future enemy types)
        self.can_eat_walls = False
        self.can_place_bombs = False
        self.can_teleport = False
        
        # Load sprite image
        sprite_cache = get_sprite_cache()
        self.image = sprite_cache.enemy.copy()
        
        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = grid_x * TILE_SIZE
        self.rect.y = grid_y * TILE_SIZE + HEADER_HEIGHT
    
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
            self.grid_y = (self.rect.y - HEADER_HEIGHT) // TILE_SIZE
            self.moving = False
        
        # AI: Choose and move in random direction periodically
        if not self.moving:
            if current_time - self.direction_timer >= self.direction_change_interval:
                self.choose_random_direction()
                self.direction_timer = current_time
    
    def choose_random_direction(self):
        """Choose a random valid direction and try to move"""
        # Use behavior pattern for extensibility
        direction = self.movement_behavior.choose_direction(self)
        
        if direction:
            dx, dy = direction
            new_grid_x = self.grid_x + dx
            new_grid_y = self.grid_y + dy
            
            # Apply the chosen direction (already validated by behavior)
            self.target_x = new_grid_x * TILE_SIZE
            self.target_y = new_grid_y * TILE_SIZE + HEADER_HEIGHT
            self.moving = True
            self.current_direction = (dx, dy)
    
    def is_position_blocked(self, grid_x, grid_y):
        """Check if a grid position is blocked by walls, soft blocks, or bombs"""
        # Check walls (with passability rules)
        for wall in self.walls:
            if wall.grid_x == grid_x and wall.grid_y == grid_y:
                # Check if enemy can pass through this wall
                if not self._can_pass_wall(wall):
                    # Special case: wall-eating enemies can pass soft blocks
                    if self.can_eat_walls and hasattr(wall, 'wall_type') and wall.wall_type == WallType.DESTRUCTIBLE:
                        continue  # Can pass
                    return True
        
        # Check soft blocks
        for block in self.soft_blocks:
            if block.grid_x == grid_x and block.grid_y == grid_y:
                # Wall-eating enemies can pass through soft blocks
                if not self.can_eat_walls:
                    return True
        
        # Check bombs (but allow moving away from current position)
        for bomb in self.bombs:
            if bomb.grid_x == grid_x and bomb.grid_y == grid_y:
                # Allow moving away from current position
                if grid_x != self.grid_x or grid_y != self.grid_y:
                    return True
        
        return False
    
    def _can_pass_wall(self, wall):
        """Check if enemy can pass through a specific wall"""
        # Use wall's passability rule if it has one
        if hasattr(wall, 'passability_rule'):
            return wall.passability_rule.can_pass(self, wall)
        
        # Default: check wall type
        if hasattr(wall, 'wall_type'):
            if wall.wall_type == WallType.INDESTRUCTIBLE:
                return False
            elif wall.wall_type == WallType.MONSTER_ONLY:
                return True
            elif wall.wall_type == WallType.PLAYER_ONLY:
                return False
        
        # Fallback: walls block enemies
        return False


class FastEnemy(Enemy):
    """Fast enemy that moves quickly and changes direction more frequently"""
    
    def __init__(self, grid_x, grid_y, walls_group, soft_blocks_group, bombs_group):
        # Initialize with 2x speed multiplier and type
        super().__init__(
            grid_x, grid_y, walls_group, soft_blocks_group, bombs_group,
            speed_multiplier=2.0,
            enemy_type=EnemyType.FAST,
            movement_behavior=RandomMovement()
        )
        
        # Faster direction changes
        self.direction_change_interval = 500  # Change direction every 0.5 seconds
        
        # Load fast enemy sprite
        sprite_cache = get_sprite_cache()
        self.image = sprite_cache.fast_enemy.copy()


class SmartEnemy(Enemy):
    """Smart enemy that tracks the player and moves toward them"""
    
    def __init__(self, grid_x, grid_y, walls_group, soft_blocks_group, bombs_group, player):
        # Initialize with tracking behavior
        super().__init__(
            grid_x, grid_y, walls_group, soft_blocks_group, bombs_group,
            speed_multiplier=1.2,
            enemy_type=EnemyType.SMART,
            movement_behavior=TrackingMovement()
        )
        
        self.player = player
        self.direction_change_interval = 800  # Update path every 0.8 seconds
        
        # Load smart enemy sprite
        sprite_cache = get_sprite_cache()
        self.image = sprite_cache.smart_enemy.copy()
    
    def choose_random_direction(self):
        """Choose direction toward player (smart AI) - override to pass player context"""
        # Use behavior pattern with player context
        direction = self.movement_behavior.choose_direction(self, player=self.player)
        
        if direction:
            dx, dy = direction
            new_grid_x = self.grid_x + dx
            new_grid_y = self.grid_y + dy
            
            # Apply the chosen direction (already validated by behavior)
            self.target_x = new_grid_x * TILE_SIZE
            self.target_y = new_grid_y * TILE_SIZE + HEADER_HEIGHT
            self.moving = True
            self.current_direction = (dx, dy)

