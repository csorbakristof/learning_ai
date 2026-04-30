"""
Level Configuration System
"""
from config import *


class LevelConfig:
    """Configuration for a single level"""
    
    def __init__(self, level_num, num_enemies, soft_block_density, enemy_speed_multiplier=1.0):
        """
        Create level configuration
        
        Args:
            level_num: Level number (1-indexed)
            num_enemies: Number of enemies to spawn
            soft_block_density: Percentage of available spaces to fill with soft blocks (0.0-1.0)
            enemy_speed_multiplier: Speed multiplier for enemies (1.0 = normal)
        """
        self.level_num = level_num
        self.num_enemies = num_enemies
        self.soft_block_density = soft_block_density
        self.enemy_speed_multiplier = enemy_speed_multiplier
    
    def __repr__(self):
        return f"Level {self.level_num}: {self.num_enemies} enemies, {self.soft_block_density*100}% blocks, {self.enemy_speed_multiplier}x speed"


# Define all game levels
LEVELS = [
    # Level 1: Tutorial level - Easy
    LevelConfig(
        level_num=1,
        num_enemies=3,
        soft_block_density=0.60,  # 60% coverage - lots of blocks for cover
        enemy_speed_multiplier=1.0  # Normal speed
    ),
    
    # Level 2: Intermediate
    LevelConfig(
        level_num=2,
        num_enemies=4,
        soft_block_density=0.50,  # 50% coverage - less cover
        enemy_speed_multiplier=1.2  # 20% faster enemies
    ),
    
    # Level 3: Advanced
    LevelConfig(
        level_num=3,
        num_enemies=5,
        soft_block_density=0.40,  # 40% coverage - limited cover
        enemy_speed_multiplier=1.4  # 40% faster enemies
    ),
    
    # Level 4: Expert
    LevelConfig(
        level_num=4,
        num_enemies=6,
        soft_block_density=0.35,  # 35% coverage - very limited cover
        enemy_speed_multiplier=1.6  # 60% faster enemies
    ),
    
    # Level 5: Master (Final Level)
    LevelConfig(
        level_num=5,
        num_enemies=7,
        soft_block_density=0.30,  # 30% coverage - minimal cover
        enemy_speed_multiplier=1.8  # 80% faster enemies
    ),
]


def get_level(level_num):
    """
    Get level configuration by number (1-indexed)
    
    Args:
        level_num: Level number (1-5)
    
    Returns:
        LevelConfig object, or None if level doesn't exist
    """
    if 1 <= level_num <= len(LEVELS):
        return LEVELS[level_num - 1]
    return None


def get_total_levels():
    """Get total number of levels in the game"""
    return len(LEVELS)


def is_final_level(level_num):
    """Check if this is the final level"""
    return level_num >= len(LEVELS)
