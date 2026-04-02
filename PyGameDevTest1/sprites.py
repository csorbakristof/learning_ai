"""
Sprite classes for game objects
"""
import pygame
import random
from config import *
from assets import get_sprite_cache
from enums import EnemyType, WallType, WeaponType, PowerUpType, EntityCategory, PassabilityCondition
from behaviors import (
    MovementBehavior, RandomMovement, TrackingMovement, WallEatingMovement,
    ExplosionBehavior, CrossExplosion,
    PassabilityRule, AlwaysBlockRule, EntityTypeRule,
    WeaponBehavior, StandardBombBehavior, RemoteBombBehavior, TimeBombBehavior, KickBombBehavior, LandmineBehavior
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
        
        # Weapon selection
        self.current_weapon = WeaponType.STANDARD
        self.weapon_names = {
            WeaponType.STANDARD: "Standard",
            WeaponType.REMOTE: "Remote",
            WeaponType.TIMED: "Time Bomb",
            WeaponType.KICK: "Kick Bomb",
            WeaponType.LANDMINE: "Landmine"
        }
        
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
        
        # Check for kick bombs first
        for bomb in self.bombs:
            if bomb.grid_x == new_grid_x and bomb.grid_y == new_grid_y:
                # If it's a kick bomb and not already sliding, kick it
                if bomb.weapon_type == WeaponType.KICK and not bomb.sliding:
                    bomb.kick((dx, dy))
                    return  # Don't move player, just kick the bomb
        
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
    
    def __init__(self, grid_x, grid_y, bomb_range, owner, weapon_type=None, weapon_behavior=None, explosion_behavior=None, walls_group=None, soft_blocks_group=None):
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
        
        # References for collision detection (used by kick bombs)
        self.walls = walls_group
        self.soft_blocks = soft_blocks_group
        
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
        
        # Sliding state for kick bombs
        self.sliding = False
        self.slide_direction = None
        self.slide_speed = 4  # Pixels per frame
        self.target_grid_x = grid_x
        self.target_grid_y = grid_y
        
        # Call behavior initialization
        self.weapon_behavior.on_place(self)
        
        # Make landmines semi-transparent
        if self.weapon_type == WeaponType.LANDMINE:
            self.image.set_alpha(80)  # Very faint
    
    def update(self, enemies_group=None):
        """Update bomb timer and check for explosion"""
        current_time = pygame.time.get_ticks()
        time_left = self.timer - (current_time - self.placed_time)
        
        # Animate bomb with pulsing effect based on time remaining (not for landmines)
        if time_left > 0 and self.weapon_type != WeaponType.LANDMINE:
            # Calculate smooth pulse value (0.0 to 1.0 and back) using triangle wave
            pulse_value = abs(((current_time % 1000) / 500.0) - 1.0)
            self.image = self.sprite_cache.get_bomb_frame(pulse_value)
        
        # Handle sliding for kick bombs
        if self.sliding and self.slide_direction:
            self._update_sliding()
        
        # Call behavior update with enemies group
        self.weapon_behavior.on_update(self, enemies_group=enemies_group)
        
        # Check if timer expired or behavior says to explode
        # Landmines should not explode on timer, only on enemy contact
        if self.weapon_type == WeaponType.LANDMINE:
            if self.weapon_behavior.should_explode(self, enemies_group=enemies_group):
                self.exploded = True
        else:
            if time_left <= 0 and not self.exploded:
                self.exploded = True
            elif self.weapon_behavior.should_explode(self):
                self.exploded = True
    
    def _update_sliding(self):
        """Handle sliding movement for kick bombs"""
        dx, dy = self.slide_direction
        
        # Calculate target position
        target_x = self.target_grid_x * TILE_SIZE
        target_y = self.target_grid_y * TILE_SIZE + HEADER_HEIGHT
        
        # Move towards target
        if self.rect.x < target_x:
            self.rect.x = min(self.rect.x + self.slide_speed, target_x)
        elif self.rect.x > target_x:
            self.rect.x = max(self.rect.x - self.slide_speed, target_x)
        
        if self.rect.y < target_y:
            self.rect.y = min(self.rect.y + self.slide_speed, target_y)
        elif self.rect.y > target_y:
            self.rect.y = max(self.rect.y - self.slide_speed, target_y)
        
        # Check if reached target grid position
        if self.rect.x == target_x and self.rect.y == target_y:
            # Update grid position
            self.grid_x = self.target_grid_x
            self.grid_y = self.target_grid_y
            
            # Try to continue sliding to next tile
            next_grid_x = self.grid_x + dx
            next_grid_y = self.grid_y + dy
            
            # Check if next position is blocked
            if self._can_slide_to(next_grid_x, next_grid_y):
                self.target_grid_x = next_grid_x
                self.target_grid_y = next_grid_y
            else:
                # Stop sliding if blocked
                self.sliding = False
                self.slide_direction = None
    
    def _can_slide_to(self, grid_x, grid_y):
        """Check if bomb can slide to a grid position"""
        # Check bounds
        if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y < 0 or grid_y >= GRID_HEIGHT:
            return False
        
        # Check for walls
        if self.walls:
            for wall in self.walls:
                if wall.grid_x == grid_x and wall.grid_y == grid_y:
                    return False
        
        # Check for soft blocks
        if self.soft_blocks:
            for block in self.soft_blocks:
                if block.grid_x == grid_x and block.grid_y == grid_y:
                    return False
        
        return True
    
    def kick(self, direction):
        """Start sliding in a direction"""
        if hasattr(self.weapon_behavior, 'kick'):
            self.weapon_behavior.kick(direction)
            self.sliding = True
            self.slide_direction = direction
            self.target_grid_x = self.grid_x + direction[0]
            self.target_grid_y = self.grid_y + direction[1]
    
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

class WallBreakerEnemy(Enemy):
    """Wall breaker enemy that destroys soft blocks while moving"""
    
    def __init__(self, grid_x, grid_y, walls_group, soft_blocks_group, bombs_group):
        # Initialize with wall-eating behavior
        super().__init__(
            grid_x, grid_y, walls_group, soft_blocks_group, bombs_group,
            speed_multiplier=0.8,  # Slower than normal
            enemy_type=EnemyType.WALL_EATER,
            movement_behavior=WallEatingMovement()
        )
        
        self.can_eat_walls = True
        self.direction_change_interval = 1200  # Change direction every 1.2 seconds
        
        # Load wall breaker sprite  
        sprite_cache = get_sprite_cache()
        self.image = sprite_cache.wall_breaker_enemy.copy()
    
    def choose_random_direction(self):
        """Choose direction - can move through soft blocks"""
        # Use behavior pattern with walls context
        direction = self.movement_behavior.choose_direction(self, walls_group=self.walls)
        
        if direction:
            dx, dy = direction
            new_grid_x = self.grid_x + dx
            new_grid_y = self.grid_y + dy
            
            # Check if there's a soft block to destroy
            for block in self.soft_blocks.copy():
                if block.grid_x == new_grid_x and block.grid_y == new_grid_y:
                    # Destroy the soft block
                    block.kill()
                    self.soft_blocks.remove(block)
                    break
            
            # Apply the chosen direction
            self.target_x = new_grid_x * TILE_SIZE
            self.target_y = new_grid_y * TILE_SIZE + HEADER_HEIGHT
            self.moving = True
            self.current_direction = (dx, dy)


class TankEnemy(Enemy):
    """Tank enemy that requires multiple hits to defeat"""
    
    def __init__(self, grid_x, grid_y, walls_group, soft_blocks_group, bombs_group):
        super().__init__(
            grid_x, grid_y, walls_group, soft_blocks_group, bombs_group,
            speed_multiplier=0.5,  # Very slow
            enemy_type=EnemyType.NORMAL,  # Use NORMAL for now
            movement_behavior=RandomMovement()
        )
        
        self.health = 2  # Requires 2 hits
        self.max_health = 2
        self.damaged = False
        self.direction_change_interval = 1500  # Change direction every 1.5 seconds
        
        # Load tank sprite
        sprite_cache = get_sprite_cache()
        self.image = sprite_cache.tank_enemy.copy()
    
    def take_damage(self):
        """Take one point of damage"""
        self.health -= 1
        if self.health == 1 and not self.damaged:
            self.damaged = True
            # Change sprite to damaged version
            sprite_cache = get_sprite_cache()
            self.image = sprite_cache.tank_enemy_damaged.copy()
        return self.health > 0  # Return True if still alive


class BombLayerEnemy(Enemy):
    """Enemy that places bombs periodically"""
    
    def __init__(self, grid_x, grid_y, walls_group, soft_blocks_group, bombs_group, game_state=None):
        super().__init__(
            grid_x, grid_y, walls_group, soft_blocks_group, bombs_group,
            speed_multiplier=1.0,
            enemy_type=EnemyType.BOMB_PLACER,
            movement_behavior=RandomMovement()
        )
        
        self.can_place_bombs = True
        self.last_bomb_time = 0
        self.bomb_interval = 5000  # Place bomb every 5 seconds
        self.game_state = game_state
        self.direction_change_interval = 1000
        
        # Load sprite
        sprite_cache = get_sprite_cache()
        self.image = sprite_cache.bomb_layer_enemy.copy()
    
    def update(self):
        """Update enemy and check if should place bomb"""
        super().update()
        
        # Check if should place bomb
        if self.game_state and self.can_place_bombs:
            import pygame
            current_time = pygame.time.get_ticks()
            if current_time - self.last_bomb_time >= self.bomb_interval:
                self.place_bomb()
                self.last_bomb_time = current_time
    
    def place_bomb(self):
        """Place a bomb at current position"""
        if self.game_state:
            from sprites import Bomb
            # Check if there's already a bomb here
            bomb_exists = any(b.grid_x == self.grid_x and b.grid_y == self.grid_y 
                            for b in self.game_state['bombs'])
            if not bomb_exists:
                bomb = Bomb(self.grid_x, self.grid_y, 1, self, 
                          walls_group=self.walls, soft_blocks_group=self.soft_blocks)  # Range 1, owner is enemy
                bomb.timer = 2000  # 2 second timer for enemy bombs
                self.game_state['bombs'].add(bomb)
                self.game_state['all_sprites'].add(bomb)


class GhostEnemy(Enemy):
    """Ghost enemy that can phase through walls"""
    
    def __init__(self, grid_x, grid_y, walls_group, soft_blocks_group, bombs_group):
        super().__init__(
            grid_x, grid_y, walls_group, soft_blocks_group, bombs_group,
            speed_multiplier=1.1,
            enemy_type=EnemyType.TELEPORTER,
            movement_behavior=RandomMovement()
        )
        
        self.can_teleport = True
        self.phasing = False
        self.phase_cooldown = 0
        self.direction_change_interval = 900
        
        # Load sprite
        sprite_cache = get_sprite_cache()
        self.image = sprite_cache.ghost_enemy.copy()
        self.image.set_alpha(180)  # Semi-transparent
    
    def is_position_blocked(self, grid_x, grid_y):
        """Ghost can phase through walls occasionally"""
        import pygame
        current_time = pygame.time.get_ticks()
        
        # Check if phasing is on cooldown
        if current_time < self.phase_cooldown:
            return super().is_position_blocked(grid_x, grid_y)
        
        # 30% chance to phase through walls
        if random.random() < 0.3:
            self.phasing = True
            self.phase_cooldown = current_time + 3000  # 3 second cooldown
            # Only check bombs, ignore walls
            for bomb in self.bombs:
                if bomb.grid_x == grid_x and bomb.grid_y == grid_y:
                    if grid_x != self.grid_x or grid_y != self.grid_y:
                        return True
            return False
        
        return super().is_position_blocked(grid_x, grid_y)


class SplitterEnemy(Enemy):
    """Enemy that splits into smaller enemies when destroyed"""
    
    def __init__(self, grid_x, grid_y, walls_group, soft_blocks_group, bombs_group, game_state=None, is_mini=False):
        super().__init__(
            grid_x, grid_y, walls_group, soft_blocks_group, bombs_group,
            speed_multiplier=1.3 if is_mini else 0.9,
            enemy_type=EnemyType.NORMAL,
            movement_behavior=RandomMovement()
        )
        
        self.is_mini = is_mini
        self.game_state = game_state
        self.direction_change_interval = 800 if is_mini else 1100
        
        # Load sprite
        sprite_cache = get_sprite_cache()
        if is_mini:
            self.image = sprite_cache.mini_enemy.copy()
        else:
            self.image = sprite_cache.splitter_enemy.copy()
    
    def split(self):
        """Split into 2-3 mini enemies"""
        if self.is_mini or not self.game_state:
            return []
        
        # Create 2-3 mini enemies near this position
        mini_enemies = []
        num_minis = random.randint(2, 3)
        
        # Try to place minis in adjacent cells
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        random.shuffle(directions)
        
        for i in range(min(num_minis, len(directions))):
            dx, dy = directions[i]
            new_x = self.grid_x + dx
            new_y = self.grid_y + dy
            
            # Check if position is valid
            blocked = False
            for wall in self.walls:
                if wall.grid_x == new_x and wall.grid_y == new_y:
                    blocked = True
                    break
            for block in self.soft_blocks:
                if block.grid_x == new_x and block.grid_y == new_y:
                    blocked = True
                    break
            
            if not blocked:
                mini = SplitterEnemy(new_x, new_y, self.walls, self.soft_blocks, 
                                    self.bombs, self.game_state, is_mini=True)
                mini_enemies.append(mini)
        
        return mini_enemies
