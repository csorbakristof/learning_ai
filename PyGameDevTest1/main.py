"""
Dynablaster - Bomberman Clone
Main game file
"""
import pygame
import random
from config import *
from sprites import Wall, SoftBlock, Player, Bomb, Explosion


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


def can_place_bomb(grid_x, grid_y, bombs_group):
    """Check if a bomb can be placed at the given grid position"""
    for bomb in bombs_group:
        if bomb.grid_x == grid_x and bomb.grid_y == grid_y:
            return False
    return True


def create_explosion(grid_x, grid_y, bomb_range, walls_group, soft_blocks_group, explosions_group):
    """
    Create explosion sprites in a cross pattern
    Returns list of soft blocks that were destroyed
    """
    destroyed_blocks = []
    
    # Create center explosion
    explosions_group.add(Explosion(grid_x, grid_y, is_center=True))
    
    # Create explosions in four directions
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Up, Down, Left, Right
    
    for dx, dy in directions:
        for distance in range(1, bomb_range + 1):
            ex = grid_x + (dx * distance)
            ey = grid_y + (dy * distance)
            
            # Check if hit a wall (indestructible) - stop explosion
            hit_wall = False
            for wall in walls_group:
                if wall.grid_x == ex and wall.grid_y == ey:
                    hit_wall = True
                    break
            
            if hit_wall:
                break  # Stop extending in this direction
            
            # Check if hit a soft block - destroy it and stop
            hit_block = False
            for block in soft_blocks_group:
                if block.grid_x == ex and block.grid_y == ey:
                    destroyed_blocks.append(block)
                    hit_block = True
                    break
            
            # Add explosion sprite at this position
            explosions_group.add(Explosion(ex, ey, is_center=False))
            
            if hit_block:
                break  # Stop extending in this direction after destroying block
    
    return destroyed_blocks



def main():
    """Main game function"""
    # Initialize Pygame
    pygame.init()
    
    # Create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    
    # Create clock for FPS control
    clock = pygame.time.Clock()
    
    # Create font for UI
    font = pygame.font.Font(None, 36)
    
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    soft_blocks = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    
    # Generate level
    generate_level(walls, soft_blocks)
    
    # Create player at starting position (grid 1, 1)
    player = Player(1, 1, walls, soft_blocks)
    
    # Add all sprites to the main group for rendering
    all_sprites.add(walls)
    all_sprites.add(soft_blocks)
    all_sprites.add(player)
    
    # Track key press for bomb placement (to avoid continuous placement)
    space_pressed = False
    
    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Input handling - continuous key checking for smooth movement
        keys = pygame.key.get_pressed()
        
        # Arrow keys
        if keys[pygame.K_UP]:
            player.move(0, -1)
        elif keys[pygame.K_DOWN]:
            player.move(0, 1)
        elif keys[pygame.K_LEFT]:
            player.move(-1, 0)
        elif keys[pygame.K_RIGHT]:
            player.move(1, 0)
        
        # WASD keys
        if keys[pygame.K_w]:
            player.move(0, -1)
        elif keys[pygame.K_s]:
            player.move(0, 1)
        elif keys[pygame.K_a]:
            player.move(-1, 0)
        elif keys[pygame.K_d]:
            player.move(1, 0)
        
        # Bomb placement with spacebar (only when player is aligned to grid)
        if keys[pygame.K_SPACE] and not space_pressed:
            if not player.moving and player.bombs_available > 0:
                if can_place_bomb(player.grid_x, player.grid_y, bombs):
                    bomb = Bomb(player.grid_x, player.grid_y, player.bomb_range, player)
                    bombs.add(bomb)
                    all_sprites.add(bomb)
                    player.bombs_available -= 1
                    space_pressed = True
        
        # Reset space key tracking
        if not keys[pygame.K_SPACE]:
            space_pressed = False
        
        # Update
        all_sprites.update()
        
        # Check for bombs ready to explode
        for bomb in bombs.copy():
            if bomb.is_ready_to_explode():
                # Create explosion
                destroyed_blocks = create_explosion(
                    bomb.grid_x, bomb.grid_y, bomb.bomb_range,
                    walls, soft_blocks, explosions
                )
                
                # Remove destroyed soft blocks
                for block in destroyed_blocks:
                    block.kill()
                    all_sprites.remove(block)
                
                # Add explosions to sprite groups
                all_sprites.add(explosions)
                
                # Return bomb to player
                bomb.owner.bombs_available += 1
                
                # Remove bomb
                bomb.kill()
                bombs.remove(bomb)
                all_sprites.remove(bomb)
        
        # Check collision between player and explosions
        explosion_hits = pygame.sprite.spritecollide(player, explosions, False)
        if explosion_hits:
            player.lives -= 1
            if player.lives <= 0:
                print(f"Game Over! You ran out of lives!")
                running = False
            else:
                # Respawn player at starting position
                player.rect.x = 1 * TILE_SIZE
                player.rect.y = 1 * TILE_SIZE
                player.grid_x = 1
                player.grid_y = 1
                player.target_x = player.rect.x
                player.target_y = player.rect.y
                player.moving = False
                print(f"Hit by explosion! Lives remaining: {player.lives}")
        
        # Render
        screen.fill(GREEN)  # Background color (grass)
        all_sprites.draw(screen)
        
        # Draw UI - Lives and Bombs
        lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
        bombs_text = font.render(f"Bombs: {player.bombs_available}/{player.max_bombs}", True, WHITE)
        
        # Draw text with black background for readability
        lives_rect = lives_text.get_rect(topleft=(10, 10))
        bombs_rect = bombs_text.get_rect(topleft=(10, 50))
        
        pygame.draw.rect(screen, BLACK, lives_rect.inflate(10, 5))
        pygame.draw.rect(screen, BLACK, bombs_rect.inflate(10, 5))
        
        screen.blit(lives_text, lives_rect)
        screen.blit(bombs_text, bombs_rect)
        
        # Update display
        pygame.display.flip()
        
        # Control frame rate
        clock.tick(FPS)
    
    # Cleanup
    pygame.quit()


if __name__ == "__main__":
    main()
