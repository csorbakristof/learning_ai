"""
Behavior strategies and patterns for game entities.
Provides extensible behavior system using composition and strategy pattern.
"""
import random
from abc import ABC, abstractmethod


class MovementBehavior(ABC):
    """Abstract base class for movement behaviors"""
    
    @abstractmethod
    def choose_direction(self, entity, **kwargs):
        """
        Choose next movement direction for entity
        
        Args:
            entity: The game entity (Enemy, Player, etc.)
            **kwargs: Additional context (player position, game state, etc.)
            
        Returns:
            tuple: (dx, dy) direction tuple
        """
        pass


class RandomMovement(MovementBehavior):
    """Random movement behavior - used by normal enemies"""
    
    def choose_direction(self, entity, **kwargs):
        """Choose random valid direction"""
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_grid_x = entity.grid_x + dx
            new_grid_y = entity.grid_y + dy
            
            if not entity.is_position_blocked(new_grid_x, new_grid_y):
                return (dx, dy)
        
        return (0, 0)  # Stay if no valid direction


class TrackingMovement(MovementBehavior):
    """Tracking behavior - moves toward target (smart enemies)"""
    
    def choose_direction(self, entity, **kwargs):
        """Choose direction toward target (usually player)"""
        player = kwargs.get('player')
        if not player:
            # Fall back to random if no player reference
            return RandomMovement().choose_direction(entity)
        
        # Calculate direction to player
        dx_to_player = player.grid_x - entity.grid_x
        dy_to_player = player.grid_y - entity.grid_y
        
        # Prioritize directions toward player
        directions = []
        
        if dx_to_player > 0:
            directions.append((1, 0))
        elif dx_to_player < 0:
            directions.append((-1, 0))
        
        if dy_to_player > 0:
            directions.append((0, 1))
        elif dy_to_player < 0:
            directions.append((0, -1))
        
        # Add other directions
        all_directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for d in all_directions:
            if d not in directions:
                directions.append(d)
        directions.append((0, 0))
        
        # Try directions in priority order
        for dx, dy in directions:
            new_grid_x = entity.grid_x + dx
            new_grid_y = entity.grid_y + dy
            
            if not entity.is_position_blocked(new_grid_x, new_grid_y):
                return (dx, dy)
        
        return (0, 0)


class WallEatingMovement(MovementBehavior):
    """Movement that can destroy soft blocks"""
    
    def __init__(self):
        pass
    
    def choose_direction(self, entity, **kwargs):
        """Choose direction - can move through soft blocks"""
        # Similar to random movement but doesn't check soft blocks
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]
        random.shuffle(directions)
        
        walls = kwargs.get('walls_group')
        for dx, dy in directions:
            new_grid_x = entity.grid_x + dx
            new_grid_y = entity.grid_y + dy
            
            # Only check hard walls, ignore soft blocks
            blocked = False
            if walls:
                for wall in walls:
                    if wall.grid_x == new_grid_x and wall.grid_y == new_grid_y:
                        blocked = True
                        break
            
            if not blocked:
                return (dx, dy)
        
        return (0, 0)


class ExplosionBehavior(ABC):
    """Abstract base class for explosion patterns"""
    
    @abstractmethod
    def create_explosion_pattern(self, grid_x, grid_y, bomb_range, **kwargs):
        """
        Generate explosion pattern coordinates
        
        Args:
            grid_x, grid_y: Center of explosion
            bomb_range: Range of explosion
            **kwargs: Additional parameters
            
        Returns:
            list: List of (x, y) tuples for explosion positions
        """
        pass


class CrossExplosion(ExplosionBehavior):
    """Standard cross-pattern explosion (current behavior)"""
    
    def create_explosion_pattern(self, grid_x, grid_y, bomb_range, **kwargs):
        """Create cross pattern"""
        positions = [(grid_x, grid_y)]  # Center
        
        # Four directions
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        for dx, dy in directions:
            for distance in range(1, bomb_range + 1):
                ex = grid_x + (dx * distance)
                ey = grid_y + (dy * distance)
                positions.append((ex, ey))
        
        return positions


class DirectionalExplosion(ExplosionBehavior):
    """Explosion in single direction"""
    
    def __init__(self, direction):
        self.direction = direction  # (dx, dy)
    
    def create_explosion_pattern(self, grid_x, grid_y, bomb_range, **kwargs):
        """Create directional pattern"""
        positions = [(grid_x, grid_y)]
        dx, dy = self.direction
        
        for distance in range(1, bomb_range + 1):
            ex = grid_x + (dx * distance)  
            ey = grid_y + (dy * distance)
            positions.append((ex, ey))
        
        return positions


class PenetratingExplosion(ExplosionBehavior):
    """Explosion that passes through soft blocks"""
    
    def create_explosion_pattern(self, grid_x, grid_y, bomb_range, **kwargs):
        """Create pattern that ignores soft blocks"""
        # Similar to cross but marks as penetrating
        return CrossExplosion().create_explosion_pattern(grid_x, grid_y, bomb_range, **kwargs)


class PassabilityRule(ABC):
    """Abstract base class for wall passability rules"""
    
    @abstractmethod
    def can_pass(self, entity, wall, **kwargs):
        """
        Check if entity can pass through wall
        
        Args:
            entity: The game entity trying to pass
            wall: The wall being checked
            **kwargs: Additional game state
            
        Returns:
            bool: True if entity can pass
        """
        pass


class AlwaysBlockRule(PassabilityRule):
    """Wall always blocks everything (indestructible wall)"""
    
    def can_pass(self, entity, wall, **kwargs):
        return False


class NeverBlockRule(PassabilityRule):
    """Wall never blocks anything (empty space)"""
    
    def can_pass(self, entity, wall, **kwargs):
        return True


class EntityTypeRule(PassabilityRule):
    """Wall blocks/allows based on entity type"""
    
    def __init__(self, allowed_types):
        self.allowed_types = allowed_types  # List of EntityCategory
    
    def can_pass(self, entity, wall, **kwargs):
        """Check if entity type is in allowed list"""
        from enums import EntityCategory
        entity_type = getattr(entity, 'entity_category', None)
        return entity_type in self.allowed_types


class ConditionalRule(PassabilityRule):
    """Wall passability based on game state/conditions"""
    
    def __init__(self, condition_check):
        self.condition_check = condition_check  # Callable that returns bool
    
    def can_pass(self, entity, wall, **kwargs):
        """Check custom condition"""
        return self.condition_check(entity, wall, **kwargs)


class WeaponBehavior(ABC):
    """Abstract base class for weapon behaviors"""
    
    @abstractmethod
    def on_place(self, weapon, **kwargs):
        """Called when weapon is placed"""
        pass
    
    @abstractmethod
    def on_update(self, weapon, **kwargs):
        """Called each frame"""
        pass
    
    @abstractmethod
    def should_explode(self, weapon, **kwargs):
        """Check if weapon should explode"""
        pass


class StandardBombBehavior(WeaponBehavior):
    """Standard timed bomb behavior (current)"""
    
    def on_place(self, weapon, **kwargs):
        """Initialize timer"""
        pass  # Already handled in Bomb.__init__
    
    def on_update(self, weapon, **kwargs):
        """Update timer"""
        pass  # Already handled in Bomb.update
    
    def should_explode(self, weapon, **kwargs):
        """Check if timer expired"""
        import pygame
        current_time = pygame.time.get_ticks()
        time_left = weapon.timer - (current_time - weapon.placed_time)
        return time_left <= 0 or weapon.exploded


class MovingBombBehavior(WeaponBehavior):
    """Bomb that slides until hitting obstacle"""
    
    def __init__(self, direction):
        self.direction = direction
        self.moving = True
    
    def on_place(self, weapon, **kwargs):
        """Start moving"""
        self.moving = True
    
    def on_update(self, weapon, **kwargs):
        """Move bomb if not blocked"""
        if self.moving:
            # TODO: Implement sliding logic
            pass
    
    def should_explode(self, weapon, **kwargs):
        """Explode on timer or when stopped"""
        return StandardBombBehavior().should_explode(weapon, **kwargs)


class RemoteBombBehavior(WeaponBehavior):
    """Bomb that explodes on command"""
    
    def __init__(self):
        self.detonation_triggered = False
    
    def on_place(self, weapon, **kwargs):
        """Initialize"""
        self.detonation_triggered = False
    
    def on_update(self, weapon, **kwargs):
        """Check for detonation command"""
        # TODO: Check for detonation input
        pass
    
    def should_explode(self, weapon, **kwargs):
        """Explode when triggered"""
        return self.detonation_triggered
    
    def trigger(self):
        """Manually trigger detonation"""
        self.detonation_triggered = True


class KickBombBehavior(WeaponBehavior):
    """Bomb that can be kicked to slide"""
    
    def __init__(self):
        self.kicked = False
        self.kick_direction = None
        self.sliding = False
    
    def on_place(self, weapon, **kwargs):
        """Initialize kick state"""
        self.kicked = False
        self.sliding = False
    
    def on_update(self, weapon, **kwargs):
        """Handle sliding motion"""
        if self.sliding and self.kick_direction:
            # Bomb should slide - handled in Bomb class
            pass
    
    def should_explode(self, weapon, **kwargs):
        """Explode on timer"""
        return StandardBombBehavior().should_explode(weapon, **kwargs)
    
    def kick(self, direction):
        """Kick the bomb in a direction"""
        self.kicked = True
        self.kick_direction = direction
        self.sliding = True


class LandmineBehavior(WeaponBehavior):
    """Bomb that triggers on enemy contact"""
    
    def __init__(self):
        self.triggered_by_enemy = False
    
    def on_place(self, weapon, **kwargs):
        """Initialize"""
        self.triggered_by_enemy = False
    
    def on_update(self, weapon, **kwargs):
        """Check for enemy collision"""
        # Check if any enemy is on this tile
        enemies = kwargs.get('enemies_group')
        if enemies and hasattr(weapon, 'grid_x'):
            for enemy in enemies:
                if enemy.grid_x == weapon.grid_x and enemy.grid_y == weapon.grid_y:
                    self.triggered_by_enemy = True
                    break
    
    def should_explode(self, weapon, **kwargs):
        """Explode when enemy steps on it"""
        return self.triggered_by_enemy


class TimeBombBehavior(WeaponBehavior):
    """Bomb with customizable timer"""
    
    def __init__(self, custom_timer=3000):
        self.custom_timer = custom_timer
    
    def on_place(self, weapon, **kwargs):
        """Set custom timer"""
        weapon.timer = self.custom_timer
    
    def on_update(self, weapon, **kwargs):
        """Update timer"""
        pass
    
    def should_explode(self, weapon, **kwargs):
        """Check if custom timer expired"""
        import pygame
        current_time = pygame.time.get_ticks()
        time_left = weapon.timer - (current_time - weapon.placed_time)
        return time_left <= 0 or weapon.exploded
