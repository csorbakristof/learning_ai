"""
Sprite classes for game objects
"""
import pygame
from config import *


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
