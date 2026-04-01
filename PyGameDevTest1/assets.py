"""
Asset generation and sprite image creation
This module generates sprite images programmatically for all game objects.
Can be replaced with actual sprite sheets later.
"""
import pygame
from config import *


def create_player_sprite():
    """Create player sprite image"""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    
    # Body (blue circle)
    center = TILE_SIZE // 2
    pygame.draw.circle(surface, (100, 150, 255), (center, center), TILE_SIZE // 2 - 8)
    
    # Darker outline
    pygame.draw.circle(surface, (50, 100, 200), (center, center), TILE_SIZE // 2 - 8, 3)
    
    # Face - eyes
    eye_y = center - 6
    pygame.draw.circle(surface, WHITE, (center - 8, eye_y), 4)
    pygame.draw.circle(surface, WHITE, (center + 8, eye_y), 4)
    pygame.draw.circle(surface, BLACK, (center - 8, eye_y), 2)
    pygame.draw.circle(surface, BLACK, (center + 8, eye_y), 2)
    
    # Smile
    pygame.draw.arc(surface, BLACK, (center - 10, center - 5, 20, 15), 3.14, 0, 2)
    
    # Highlight for 3D effect
    pygame.draw.circle(surface, (200, 220, 255), (center - 8, center - 8), 6)
    
    return surface


def create_wall_sprite():
    """Create indestructible wall sprite"""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
    
    # Dark gray base
    surface.fill((60, 60, 60))
    
    # Stone brick pattern
    brick_color_dark = (50, 50, 50)
    brick_color_light = (70, 70, 70)
    
    # Horizontal bricks
    for y in range(0, TILE_SIZE, 21):
        offset = (y // 21) % 2 * (TILE_SIZE // 2)
        for x in range(-offset, TILE_SIZE, TILE_SIZE // 2):
            # Brick
            pygame.draw.rect(surface, brick_color_light, (x, y, TILE_SIZE // 2 - 2, 19))
            # Shadow
            pygame.draw.line(surface, brick_color_dark, (x, y + 19), (x + TILE_SIZE // 2 - 2, y + 19), 2)
            pygame.draw.line(surface, brick_color_dark, (x + TILE_SIZE // 2 - 2, y), (x + TILE_SIZE // 2 - 2, y + 19), 2)
    
    # Border for definition
    pygame.draw.rect(surface, (40, 40, 40), (0, 0, TILE_SIZE, TILE_SIZE), 2)
    
    return surface


def create_soft_block_sprite():
    """Create destructible soft block sprite"""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
    
    # Brown base (wooden crate look)
    surface.fill((139, 90, 43))
    
    # Wood grain texture
    grain_color = (120, 75, 35)
    for i in range(5):
        y = 10 + i * 12
        pygame.draw.line(surface, grain_color, (5, y), (TILE_SIZE - 5, y), 2)
    
    # Planks
    plank_color = (160, 110, 60)
    pygame.draw.rect(surface, plank_color, (8, 8, TILE_SIZE - 16, TILE_SIZE - 16))
    
    # Cross pattern (crate reinforcement)
    cross_color = (100, 65, 30)
    pygame.draw.line(surface, cross_color, (TILE_SIZE // 2, 8), (TILE_SIZE // 2, TILE_SIZE - 8), 3)
    pygame.draw.line(surface, cross_color, (8, TILE_SIZE // 2), (TILE_SIZE - 8, TILE_SIZE // 2), 3)
    
    # Border
    pygame.draw.rect(surface, (90, 60, 25), (0, 0, TILE_SIZE, TILE_SIZE), 2)
    
    # Highlight for depth
    pygame.draw.line(surface, (180, 140, 80), (2, 2), (TILE_SIZE - 3, 2), 2)
    pygame.draw.line(surface, (180, 140, 80), (2, 2), (2, TILE_SIZE - 3), 2)
    
    return surface


def create_bomb_sprite(pulse_phase=0):
    """
    Create bomb sprite image
    
    Args:
        pulse_phase: 0-1 value for pulsing animation
    """
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    
    center = TILE_SIZE // 2
    
    # Pulsing size based on phase
    base_radius = TILE_SIZE // 2 - 10
    radius = int(base_radius * (1 + pulse_phase * 0.15))
    
    # Shadow
    pygame.draw.circle(surface, (30, 30, 30, 100), (center + 2, center + 4), radius)
    
    # Black bomb body
    pygame.draw.circle(surface, BLACK, (center, center), radius)
    
    # Highlight for spherical look
    highlight_pos = (center - radius // 3, center - radius // 3)
    pygame.draw.circle(surface, (60, 60, 60), highlight_pos, radius // 3)
    
    # Fuse on top
    fuse_x = center
    fuse_y = center - radius
    pygame.draw.line(surface, (139, 69, 19), (fuse_x, fuse_y), (fuse_x - 5, fuse_y - 10), 3)
    
    # Spark at fuse tip (brighter when pulsing)
    spark_color = (255, int(200 + pulse_phase * 55), 0)
    pygame.draw.circle(surface, spark_color, (fuse_x - 5, fuse_y - 10), 3)
    
    return surface


def create_explosion_sprite():
    """Create explosion sprite image"""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    
    center = TILE_SIZE // 2
    
    # Multi-layered explosion effect
    # Outer orange layer
    pygame.draw.circle(surface, (255, 140, 0, 200), (center, center), TILE_SIZE // 2 - 4)
    
    # Middle yellow layer
    pygame.draw.circle(surface, (255, 200, 0, 220), (center, center), TILE_SIZE // 2 - 10)
    
    # Inner bright core
    pygame.draw.circle(surface, (255, 255, 150, 255), (center, center), TILE_SIZE // 2 - 16)
    
    # Add some "flames" around the edges
    for angle in range(0, 360, 45):
        import math
        rad = math.radians(angle)
        x = center + int(math.cos(rad) * (TILE_SIZE // 2 - 8))
        y = center + int(math.sin(rad) * (TILE_SIZE // 2 - 8))
        pygame.draw.circle(surface, (255, 100, 0, 180), (x, y), 6)
    
    return surface


def create_enemy_sprite():
    """Create enemy sprite image"""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    
    center = TILE_SIZE // 2
    
    # Red body (circular)
    pygame.draw.circle(surface, (220, 20, 20), (center, center), TILE_SIZE // 2 - 8)
    
    # Darker outline
    pygame.draw.circle(surface, (150, 0, 0), (center, center), TILE_SIZE // 2 - 8, 3)
    
    # Angry eyes
    eye_y = center - 6
    # White of eyes
    pygame.draw.circle(surface, WHITE, (center - 10, eye_y), 5)
    pygame.draw.circle(surface, WHITE, (center + 10, eye_y), 5)
    # Angry pupils (looking down)
    pygame.draw.circle(surface, BLACK, (center - 10, eye_y + 2), 3)
    pygame.draw.circle(surface, BLACK, (center + 10, eye_y + 2), 3)
    
    # Angry eyebrows
    pygame.draw.line(surface, BLACK, (center - 15, eye_y - 6), (center - 6, eye_y - 3), 3)
    pygame.draw.line(surface, BLACK, (center + 15, eye_y - 6), (center + 6, eye_y - 3), 3)
    
    # Grumpy mouth
    pygame.draw.arc(surface, BLACK, (center - 12, center + 2, 24, 16), 0, 3.14, 3)
    
    # Small horns for devilish look
    pygame.draw.polygon(surface, (180, 0, 0), [
        (center - 18, center - 16),
        (center - 15, center - 22),
        (center - 12, center - 16)
    ])
    pygame.draw.polygon(surface, (180, 0, 0), [
        (center + 18, center - 16),
        (center + 15, center - 22),
        (center + 12, center - 16)
    ])
    
    # Highlight
    pygame.draw.circle(surface, (255, 100, 100), (center - 10, center - 10), 8)
    
    return surface


def create_fast_enemy_sprite():
    """Create fast enemy sprite image (orange/yellow)"""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    
    center = TILE_SIZE // 2
    
    # Orange/yellow body (circular)
    pygame.draw.circle(surface, (255, 165, 0), (center, center), TILE_SIZE // 2 - 8)
    
    # Darker outline
    pygame.draw.circle(surface, (200, 100, 0), (center, center), TILE_SIZE // 2 - 8, 3)
    
    # Wild eyes (wider apart)
    eye_y = center - 5
    # White of eyes
    pygame.draw.circle(surface, WHITE, (center - 12, eye_y), 6)
    pygame.draw.circle(surface, WHITE, (center + 12, eye_y), 6)
    # Large pupils (excited look)
    pygame.draw.circle(surface, BLACK, (center - 12, eye_y), 4)
    pygame.draw.circle(surface, BLACK, (center + 12, eye_y), 4)
    
    # Speed lines behind head (motion effect)
    pygame.draw.line(surface, (255, 200, 0), (8, center - 8), (15, center - 10), 2)
    pygame.draw.line(surface, (255, 200, 0), (8, center), (15, center), 2)
    pygame.draw.line(surface, (255, 200, 0), (8, center + 8), (15, center + 10), 2)
    
    # Excited mouth (open)
    pygame.draw.circle(surface, BLACK, (center, center + 8), 6)
    pygame.draw.circle(surface, (200, 50, 50), (center, center + 10), 4)
    
    # Highlight
    pygame.draw.circle(surface, (255, 220, 100), (center - 8, center - 8), 8)
    
    return surface


def create_smart_enemy_sprite():
    """Create smart enemy sprite image (purple)"""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    
    center = TILE_SIZE // 2
    
    # Purple body (circular)
    pygame.draw.circle(surface, (150, 50, 200), (center, center), TILE_SIZE // 2 - 8)
    
    # Darker outline
    pygame.draw.circle(surface, (100, 20, 150), (center, center), TILE_SIZE // 2 - 8, 3)
    
    # Intelligent eyes (focused)
    eye_y = center - 4
    # White of eyes
    pygame.draw.circle(surface, WHITE, (center - 10, eye_y), 5)
    pygame.draw.circle(surface, WHITE, (center + 10, eye_y), 5)
    # Sharp pupils
    pygame.draw.circle(surface, BLACK, (center - 10, eye_y), 3)
    pygame.draw.circle(surface, BLACK, (center + 10, eye_y), 3)
    
    # Thinking expression (straight mouth)
    pygame.draw.line(surface, BLACK, (center - 8, center + 10), (center + 8, center + 10), 3)
    
    # Brain pattern on forehead (wavy lines)
    pygame.draw.arc(surface, (200, 150, 255), (center - 12, center - 18, 10, 8), 0, 3.14, 2)
    pygame.draw.arc(surface, (200, 150, 255), (center + 2, center - 18, 10, 8), 0, 3.14, 2)
    
    # Antenna/thinking symbol
    pygame.draw.circle(surface, (200, 100, 255), (center, center - 22), 3)
    pygame.draw.line(surface, (180, 80, 220), (center, center - 19), (center, center - 14), 2)
    
    # Highlight
    pygame.draw.circle(surface, (200, 150, 255), (center - 8, center - 8), 8)
    
    return surface


def create_powerup_bomb_sprite():
    """Create Bomb Up power-up sprite"""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    
    center = TILE_SIZE // 2
    
    # Cyan glowing base
    pygame.draw.circle(surface, (0, 255, 255, 200), (center, center), TILE_SIZE // 2 - 6)
    pygame.draw.circle(surface, (0, 200, 200), (center, center), TILE_SIZE // 2 - 6, 2)
    
    # White inner glow
    pygame.draw.circle(surface, (200, 255, 255, 150), (center, center), TILE_SIZE // 2 - 12)
    
    # "B" letter
    font = pygame.font.Font(None, 36)
    text = font.render("B", True, BLACK)
    text_rect = text.get_rect(center=(center, center))
    surface.blit(text, text_rect)
    
    # Sparkle effect
    pygame.draw.circle(surface, WHITE, (center - 15, center - 15), 2)
    pygame.draw.circle(surface, WHITE, (center + 15, center - 10), 2)
    pygame.draw.circle(surface, WHITE, (center + 12, center + 15), 2)
    
    return surface


def create_powerup_fire_sprite():
    """Create Fire Up power-up sprite"""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    
    center = TILE_SIZE // 2
    
    # Orange glowing base
    pygame.draw.circle(surface, (255, 140, 0, 200), (center, center), TILE_SIZE // 2 - 6)
    pygame.draw.circle(surface, (200, 100, 0), (center, center), TILE_SIZE // 2 - 6, 2)
    
    # Yellow inner glow
    pygame.draw.circle(surface, (255, 220, 100, 150), (center, center), TILE_SIZE // 2 - 12)
    
    # "F" letter
    font = pygame.font.Font(None, 36)
    text = font.render("F", True, BLACK)
    text_rect = text.get_rect(center=(center, center))
    surface.blit(text, text_rect)
    
    # Flame sparkles
    pygame.draw.circle(surface, (255, 200, 0), (center - 15, center - 15), 2)
    pygame.draw.circle(surface, (255, 200, 0), (center + 15, center - 10), 2)
    pygame.draw.circle(surface, (255, 200, 0), (center + 12, center + 15), 2)
    
    return surface


def create_powerup_speed_sprite():
    """Create Speed Up power-up sprite"""
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    
    center = TILE_SIZE // 2
    
    # Green glowing base
    pygame.draw.circle(surface, (0, 255, 100, 200), (center, center), TILE_SIZE // 2 - 6)
    pygame.draw.circle(surface, (0, 200, 80), (center, center), TILE_SIZE // 2 - 6, 2)
    
    # Lighter inner glow
    pygame.draw.circle(surface, (150, 255, 180, 150), (center, center), TILE_SIZE // 2 - 12)
    
    # "S" letter
    font = pygame.font.Font(None, 36)
    text = font.render("S", True, BLACK)
    text_rect = text.get_rect(center=(center, center))
    surface.blit(text, text_rect)
    
    # Speed lines
    pygame.draw.line(surface, (0, 150, 50), (center - 20, center - 8), (center - 12, center - 8), 2)
    pygame.draw.line(surface, (0, 150, 50), (center - 20, center), (center - 12, center), 2)
    pygame.draw.line(surface, (0, 150, 50), (center - 20, center + 8), (center - 12, center + 8), 2)
    
    return surface


class SpriteCache:
    """Cache for generated sprites to avoid recreating them"""
    
    def __init__(self):
        self.player = create_player_sprite()
        self.wall = create_wall_sprite()
        self.soft_block = create_soft_block_sprite()
        self.bomb_frames = [create_bomb_sprite(i / 10) for i in range(11)]  # 11 frames
        self.explosion = create_explosion_sprite()
        self.enemy = create_enemy_sprite()
        self.fast_enemy = create_fast_enemy_sprite()
        self.smart_enemy = create_smart_enemy_sprite()
        self.powerup_bomb = create_powerup_bomb_sprite()
        self.powerup_fire = create_powerup_fire_sprite()
        self.powerup_speed = create_powerup_speed_sprite()
    
    def get_bomb_frame(self, pulse_value):
        """Get bomb sprite frame based on pulse value (0.0 to 1.0)"""
        frame_index = int(pulse_value * 10)
        frame_index = max(0, min(10, frame_index))
        return self.bomb_frames[frame_index]


# Global sprite cache instance
_sprite_cache = None


def get_sprite_cache():
    """Get or create the global sprite cache"""
    global _sprite_cache
    if _sprite_cache is None:
        _sprite_cache = SpriteCache()
    return _sprite_cache
