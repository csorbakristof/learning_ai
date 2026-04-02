# Architecture Extensibility Guide

This document explains the refactored game architecture that supports extensible enemies, weapons, and walls.

## Overview

The codebase has been refactored to support future extensions without breaking existing functionality. The architecture now uses:

1. **Type Classification** via enums
2. **Behavior Composition** via strategy pattern
3. **Passability Rules** for conditional walls
4. **Weapon System** with pluggable behaviors

## File Structure

- **enums.py** - Type definitions (EnemyType, WallType, WeaponType, PowerUpType, etc.)
- **behaviors.py** - Behavior strategies (movement, explosions, passability, weapons)
- **sprites.py** - Game entities (now with type attributes and behavior composition)
- **config.py** - Game constants (unchanged)

## Type System

All game entities now have type classification:

### Entity Categories
```python
from enums import EntityCategory

player.entity_category == EntityCategory.PLAYER
enemy.entity_category == EntityCategory.ENEMY
wall.entity_category == EntityCategory.WALL
```

### Specific Types
```python
from enums import EnemyType, WallType, WeaponType

enemy.enemy_type == EnemyType.NORMAL  # or FAST, SMART, WALL_EATER, etc.
wall.wall_type == WallType.INDESTRUCTIBLE  # or DESTRUCTIBLE, PLAYER_ONLY, etc.
bomb.weapon_type == WeaponType.STANDARD  # or MOVING, REMOTE, etc.
```

## Extending Enemy Types

### Creating a Wall-Eating Enemy

```python
from sprites import Enemy
from enums import EnemyType
from behaviors import WallEatingMovement

# Create enemy that can eat through soft blocks
wall_eater = Enemy(
    grid_x=5, grid_y=5,
    walls_group=walls,
    soft_blocks_group=soft_blocks,
    bombs_group=bombs,
    speed_multiplier=1.0,
    enemy_type=EnemyType.WALL_EATER,
    movement_behavior=WallEatingMovement()
)
wall_eater.can_eat_walls = True  # Enable wall-eating ability
```

### Creating a Bomb-Placing Enemy

```python
from sprites import Enemy
from enums import EnemyType

bomb_placer = Enemy(
    grid_x=5, grid_y=5,
    walls_group=walls,
    soft_blocks_group=soft_blocks,
    bombs_group=bombs,
    enemy_type=EnemyType.BOMB_PLACER
)
bomb_placer.can_place_bombs = True

# In game loop, check if enemy should place bomb
if bomb_placer.can_place_bombs and should_place_bomb():
    # Place bomb at enemy position
    new_bomb = Bomb(bomb_placer.grid_x, bomb_placer.grid_y, range=2, owner=bomb_placer)
    bombs_group.add(new_bomb)
```

### Custom Movement Behavior

```python
from behaviors import MovementBehavior

class PatrolMovement(MovementBehavior):
    """Enemy patrols back and forth"""
    
    def __init__(self, patrol_points):
        self.patrol_points = patrol_points
        self.current_target_index = 0
    
    def choose_direction(self, entity, **kwargs):
        target = self.patrol_points[self.current_target_index]
        
        # Move toward current patrol point
        dx = 0 if entity.grid_x == target[0] else (1 if target[0] > entity.grid_x else -1)
        dy = 0 if entity.grid_y == target[1] else (1 if target[1] > entity.grid_y else -1)
        
        # When reached, move to next point
        if entity.grid_x == target[0] and entity.grid_y == target[1]:
            self.current_target_index = (self.current_target_index + 1) % len(self.patrol_points)
        
        return (dx, dy)

# Use patrol behavior
patrol_enemy = Enemy(
    grid_x=3, grid_y=3,
    walls_group=walls,
    soft_blocks_group=soft_blocks,
    bombs_group=bombs,
    enemy_type=EnemyType.NORMAL,
    movement_behavior=PatrolMovement([(3,3), (10,3), (10,8), (3,8)])
)
```

## Extending Weapon Types

### Creating a Moving Bomb

```python
from sprites import Bomb
from enums import WeaponType
from behaviors import MovingBombBehavior

# Bomb that slides in a direction until hitting obstacle
moving_bomb = Bomb(
    grid_x=player.grid_x,
    grid_y=player.grid_y,
    bomb_range=player.bomb_range,
    owner=player,
    weapon_type=WeaponType.MOVING,
    weapon_behavior=MovingBombBehavior(direction=(1, 0))  # Slides right
)
```

### Creating a Remote-Controlled Bomb

```python
from sprites import Bomb
from enums import WeaponType
from behaviors import RemoteBombBehavior

# Create remote bomb
remote_bomb = Bomb(
    grid_x=player.grid_x,
    grid_y=player.grid_y,
    bomb_range=player.bomb_range,
    owner=player,
    weapon_type=WeaponType.REMOTE,
    weapon_behavior=RemoteBombBehavior()
)

# Player needs detonation ability
player.can_remote_detonate = True

# In game loop, when detonation key pressed
if keys[pygame.K_RETURN] and player.can_remote_detonate:
    # Trigger all remote bombs
    for bomb in bombs_group:
        if bomb.weapon_type == WeaponType.REMOTE:
            bomb.weapon_behavior.trigger()
```

### Custom Explosion Pattern

```python
from behaviors import ExplosionBehavior

class CircularExplosion(ExplosionBehavior):
    """Explosion in all 8 directions"""
    
    def create_explosion_pattern(self, grid_x, grid_y, bomb_range, **kwargs):
        positions = [(grid_x, grid_y)]  # Center
        
        # 8 directions including diagonals
        directions = [
            (0, -1), (0, 1), (-1, 0), (1, 0),  # Cardinal
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal
        ]
        
        for dx, dy in directions:
            for distance in range(1, bomb_range + 1):
                ex = grid_x + (dx * distance)
                ey = grid_y + (dy * distance)
                positions.append((ex, ey))
        
        return positions

# Use circular explosion
circular_bomb = Bomb(
    grid_x=player.grid_x,
    grid_y=player.grid_y,
    bomb_range=2,
    owner=player,
    explosion_behavior=CircularExplosion()
)
```

## Extending Wall Types

### Creating Player-Only Walls

```python
from sprites import Wall
from enums import WallType, EntityCategory
from behaviors import EntityTypeRule

# Wall that only player can pass through
player_only_wall = Wall(
    grid_x=5,
    grid_y=5,
    wall_type=WallType.PLAYER_ONLY,
    passability_rule=EntityTypeRule(allowed_types=[EntityCategory.PLAYER])
)
walls_group.add(player_only_wall)
```

### Creating Monster-Only Walls

```python
from sprites import Wall
from enums import WallType, EntityCategory
from behaviors import EntityTypeRule

# Wall that only enemies can pass through
monster_only_wall = Wall(
    grid_x=7,
    grid_y=3,
    wall_type=WallType.MONSTER_ONLY,
    passability_rule=EntityTypeRule(allowed_types=[EntityCategory.ENEMY])
)
walls_group.add(monster_only_wall)
```

### Creating Conditional Walls

```python
from sprites import Wall
from enums import WallType
from behaviors import ConditionalRule

# Wall passable only if player has collected enough power-ups
def has_key_powerup(entity, wall, **kwargs):
    return hasattr(entity, 'bomb_range') and entity.bomb_range >= 3

key_wall = Wall(
    grid_x=8,
    grid_y=5,
    wall_type=WallType.CONDITIONAL,
    passability_rule=ConditionalRule(has_key_powerup)
)
walls_group.add(key_wall)
```

### Creating Temporary Walls

```python
from sprites import Wall
from enums import WallType

# Wall that disappears after time
class TemporaryWall(Wall):
    def __init__(self, grid_x, grid_y, duration=5000):
        super().__init__(grid_x, grid_y, wall_type=WallType.TEMPORARY)
        self.created_time = pygame.time.get_ticks()
        self.duration = duration
    
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.created_time >= self.duration:
            self.kill()  # Remove from all groups

temp_wall = TemporaryWall(6, 4, duration=3000)  # Lasts 3 seconds
walls_group.add(temp_wall)
```

## Special Player Abilities

The player now has flags for special abilities that can be enabled:

```python
# Enable special abilities
player.can_pass_bombs = True      # Walk through bombs
player.can_pass_walls = True      # Walk through soft blocks
player.has_shield = True          # Protected from explosions
player.can_kick_bombs = True      # Kick bombs to move them
player.can_remote_detonate = True # Detonate bombs remotely
```

These can be granted via power-ups:

```python
# When player collects special power-up
if powerup.powerup_enum == PowerUpType.WALL_PASS:
    player.can_pass_walls = True
elif powerup.powerup_enum == PowerUpType.BOMB_PASS:
    player.can_pass_bombs = True
elif powerup.powerup_enum == PowerUpType.SHIELD:
    player.has_shield = True
```

## Backward Compatibility

All existing code continues to work without modification:

```python
# Old code still works - defaults are provided
wall = Wall(grid_x=3, grid_y=4)  # Uses default INDESTRUCTIBLE type
enemy = Enemy(grid_x=5, grid_y=6, walls, soft_blocks, bombs)  # Uses NORMAL type
bomb = Bomb(grid_x=1, grid_y=1, bomb_range=2, owner=player)  # Uses STANDARD type
```

Optional parameters allow extensibility when needed:

```python
# New extended code
wall = Wall(grid_x=3, grid_y=4, wall_type=WallType.PLAYER_ONLY, passability_rule=custom_rule)
enemy = Enemy(grid_x=5, grid_y=6, walls, soft_blocks, bombs, enemy_type=EnemyType.WALL_EATER, movement_behavior=custom_behavior)
bomb = Bomb(grid_x=1, grid_y=1, bomb_range=2, owner=player, weapon_type=WeaponType.REMOTE, weapon_behavior=remote_behavior)
```

## Future Implementation Steps

When ready to implement new features:

1. **Choose the feature** (e.g., wall-eating enemy)
2. **Create behavior class** if needed (e.g., in behaviors.py)
3. **Create sprite sprites** in assets.py
4. **Instantiate with new type** in spawn/generation code
5. **Update game logic** to handle new interactions

The architecture is now ready for any of these extensions:
- Wall-eating enemies
- Bomb-placing enemies
- Moving bombs
- Remote-controlled bombs
- Player shields
- Player teleportation
- Conditional walls
- Temporary obstacles
- And many more!

## Summary

The refactoring provides:
- ✅ Type system for categorizing entities
- ✅ Behavior composition for extensible AI and mechanics
- ✅ Passability rules for complex wall interactions
- ✅ Weapon system supporting various bomb types
- ✅ Player abilities framework
- ✅ 100% backward compatibility
- ✅ All existing functionality preserved

No gameplay changes were made - this is purely architectural preparation for future features!
