"""
Enum types and constants for game object categorization.
This module provides extensibility for different game object types.
"""
from enum import Enum, auto


class EnemyType(Enum):
    """Types of enemies with different behaviors"""
    NORMAL = auto()          # Random movement (current default enemy)
    FAST = auto()            # Quick random movement (current FastEnemy)
    SMART = auto()           # Tracks and chases player (current SmartEnemy)
    WALL_EATER = auto()      # Can destroy and pass through soft blocks
    BOMB_PLACER = auto()     # Places bombs to trap player
    OBSTACLE_CREATOR = auto() # Creates temporary obstacles
    TELEPORTER = auto()      # Can teleport short distances


class WallType(Enum):
    """Types of walls with different passability rules"""
    INDESTRUCTIBLE = auto()   # Standard wall (current Wall class)
    DESTRUCTIBLE = auto()     # Soft block (current SoftBlock class)
    MONSTER_ONLY = auto()     # Passable only by enemies
    PLAYER_ONLY = auto()      # Passable only by player
    CONDITIONAL = auto()      # Requires special item/condition to pass
    TEMPORARY = auto()        # Disappears after time
    ONE_WAY = auto()          # Can pass in one direction only


class WeaponType(Enum):
    """Types of weapons/bombs with different behaviors"""
    STANDARD = auto()         # Normal bomb (current Bomb class)
    MOVING = auto()           # Bomb that slides until hitting obstacle
    REMOTE = auto()           # Explodes on command
    TIMED = auto()            # Custom timer length
    LANDMINE = auto()         # Explodes when enemy steps on it
    PENETRATING = auto()      # Explosion passes through soft blocks
    DIRECTIONAL = auto()      # Explodes in one direction only


class PowerUpType(Enum):
    """Types of power-ups with different effects"""
    BOMB_UP = auto()          # Increase max bombs (current)
    FIRE_UP = auto()          # Increase explosion range (current)
    SPEED_UP = auto()         # Increase movement speed (current)
    SHIELD = auto()           # Temporary protection from explosions
    TELEPORT = auto()         # Ability to teleport
    WALL_PASS = auto()        # Pass through soft blocks
    BOMB_PASS = auto()        # Pass through bombs
    KICK_BOMB = auto()        # Kick bombs to move them
    THROW_BOMB = auto()       # Throw bombs over obstacles
    REMOTE_DETONATOR = auto() # Remote control for bombs


class EntityCategory(Enum):
    """High-level categories for collision and interaction rules"""
    PLAYER = auto()
    ENEMY = auto()
    WALL = auto()
    WEAPON = auto()
    POWERUP = auto()
    PROJECTILE = auto()


class PassabilityCondition(Enum):
    """Conditions required to pass through conditional walls"""
    NONE = auto()             # No special condition (always passable or impassable)
    HAS_KEY = auto()          # Player has key item
    POWER_UP_LEVEL = auto()   # Player has certain power-up level
    ENEMY_ONLY = auto()       # Only enemies can pass
    PLAYER_ONLY = auto()      # Only player can pass
    BOMB_COUNT = auto()       # Player has certain number of bombs
    AFTER_TIME = auto()       # After certain time has elapsed
