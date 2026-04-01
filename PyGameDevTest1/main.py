"""
Dynablaster - Bomberman Clone
Main game file
"""
import pygame
import random
from config import *
from sprites import Wall, SoftBlock


def grid_to_pixel(grid_x, grid_y):
    """Convert grid coordinates to pixel coordinates"""
    return grid_x * TILE_SIZE, grid_y * TILE_SIZE


def pixel_to_grid(pixel_x, pixel_y):
    """Convert pixel coordinates to grid coordinates"""
    return pixel_x // TILE_SIZE, pixel_y // TILE_SIZE


def generate_level(walls_group, soft_blocks_group):
    """
    Generate classic Bomberman level layout
    - Outer border walls
    - Checkerboard pattern of inner walls
    - Random soft blocks in empty spaces
    - Clear 3x3 area at starting position (top-left)
    """
    # Create border walls
    for x in range(GRID_WIDTH):
        walls_group.add(Wall(x, 0))  # Top border
        walls_group.add(Wall(x, GRID_HEIGHT - 1))  # Bottom border
    
    for y in range(GRID_HEIGHT):
        walls_group.add(Wall(0, y))  # Left border
        walls_group.add(Wall(GRID_WIDTH - 1, y))  # Right border
    
    # Create inner walls in checkerboard pattern
    for y in range(2, GRID_HEIGHT - 1, 2):
        for x in range(2, GRID_WIDTH - 1, 2):
            walls_group.add(Wall(x, y))
    
    # Define starting area (3x3 top-left area to keep clear)
    starting_area = [(1, 1), (2, 1), (1, 2)]
    
    # Place random soft blocks in empty spaces
    for y in range(1, GRID_HEIGHT - 1):
        for x in range(1, GRID_WIDTH - 1):
            # Skip if this position has a wall
            if any(wall.grid_x == x and wall.grid_y == y for wall in walls_group):
                continue
            
            # Skip starting area
            if (x, y) in starting_area:
                continue
            
            # Random chance to place soft block (about 60% coverage)
            if random.random() < 0.6:
                soft_blocks_group.add(SoftBlock(x, y))


def main():
    """Main game function"""
    # Initialize Pygame
    pygame.init()
    
    # Create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    
    # Create clock for FPS control
    clock = pygame.time.Clock()
    
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    soft_blocks = pygame.sprite.Group()
    
    # Generate level
    generate_level(walls, soft_blocks)
    
    # Add all sprites to the main group for rendering
    all_sprites.add(walls)
    all_sprites.add(soft_blocks)
    
    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update
        # (Nothing to update yet in Milestone 1)
        all_sprites.update()
        
        # Render
        screen.fill(GREEN)  # Background color (grass)
        all_sprites.draw(screen)
        
        # Update display
        pygame.display.flip()
        
        # Control frame rate
        clock.tick(FPS)
    
    # Cleanup
    pygame.quit()


if __name__ == "__main__":
    main()
