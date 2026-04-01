"""
Dynablaster - Bomberman Clone
Main game file
"""
import pygame
import random
from config import *
from sprites import Wall, SoftBlock, Player, Bomb, Explosion, Enemy


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


def spawn_enemies(num_enemies, walls_group, soft_blocks_group, player, enemies_group):
    """
    Spawn enemies at random valid positions away from player
    """
    spawned = 0
    max_attempts = 100
    attempts = 0
    
    while spawned < num_enemies and attempts < max_attempts:
        attempts += 1
        
        # Choose random position
        x = random.randint(1, GRID_WIDTH - 2)
        y = random.randint(1, GRID_HEIGHT - 2)
        
        # Check if position is valid (not blocked and not too close to player)
        is_blocked = False
        
        # Check walls
        for wall in walls_group:
            if wall.grid_x == x and wall.grid_y == y:
                is_blocked = True
                break
        
        # Check soft blocks
        if not is_blocked:
            for block in soft_blocks_group:
                if block.grid_x == x and block.grid_y == y:
                    is_blocked = True
                    break
        
        # Check distance from player (should be at least 3 tiles away)
        player_distance = abs(x - player.grid_x) + abs(y - player.grid_y)
        if player_distance < 3:
            is_blocked = True
        
        # Check if another enemy is already there
        if not is_blocked:
            for enemy in enemies_group:
                if enemy.grid_x == x and enemy.grid_y == y:
                    is_blocked = True
                    break
        
        # Spawn enemy if position is valid
        if not is_blocked:
            enemy = Enemy(x, y, walls_group, soft_blocks_group)
            enemies_group.add(enemy)
            spawned += 1



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
    enemies = pygame.sprite.Group()
    
    # Generate level
    generate_level(walls, soft_blocks)
    
    # Create player at starting position (grid 1, 1)
    player = Player(1, 1, walls, soft_blocks)
    
    # Spawn enemies
    num_enemies = 3  # Start with 3 enemies for MVP
    spawn_enemies(num_enemies, walls, soft_blocks, player, enemies)
    
    # Add all sprites to the main group for rendering
    all_sprites.add(walls)
    all_sprites.add(soft_blocks)
    all_sprites.add(enemies)
    all_sprites.add(player)
    
    # Game state
    score = 0
    blocks_destroyed = 0
    enemies_defeated = 0
    game_over = False
    victory = False
    
    # Track key press for bomb placement (to avoid continuous placement)
    space_pressed = False
    
    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Restart game on R key press after game over or victory
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (game_over or victory):
                    # Restart the game
                    main()
                    return
        
        # Only process game logic if not game over or victory
        if not game_over and not victory:
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
                    
                    # Remove destroyed soft blocks and update score
                    for block in destroyed_blocks:
                        block.kill()
                        all_sprites.remove(block)
                        soft_blocks.remove(block)
                        blocks_destroyed += 1
                        score += 10  # 10 points per block
                    
                    # Add explosions to sprite groups
                    all_sprites.add(explosions)
                    
                    # Return bomb to player
                    bomb.owner.bombs_available += 1
                    
                    # Remove bomb
                    bomb.kill()
                    bombs.remove(bomb)
                    all_sprites.remove(bomb)
            
            # Check collision between enemies and explosions
            for enemy in enemies.copy():
                explosion_hits = pygame.sprite.spritecollide(enemy, explosions, False)
                if explosion_hits:
                    enemy.kill()
                    enemies.remove(enemy)
                    all_sprites.remove(enemy)
                    enemies_defeated += 1
                    score += 100  # 100 points per enemy
            
            # Check collision between player and explosions
            explosion_hits = pygame.sprite.spritecollide(player, explosions, False)
            if explosion_hits:
                player.lives -= 1
                if player.lives <= 0:
                    game_over = True
                else:
                    # Respawn player at starting position
                    player.rect.x = 1 * TILE_SIZE
                    player.rect.y = 1 * TILE_SIZE
                    player.grid_x = 1
                    player.grid_y = 1
                    player.target_x = player.rect.x
                    player.target_y = player.rect.y
                    player.moving = False
            
            # Check collision between player and enemies
            enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
            if enemy_hits:
                player.lives -= 1
                if player.lives <= 0:
                    game_over = True
                else:
                    # Respawn player at starting position
                    player.rect.x = 1 * TILE_SIZE
                    player.rect.y = 1 * TILE_SIZE
                    player.grid_x = 1
                    player.grid_y = 1
                    player.target_x = player.rect.x
                    player.target_y = player.rect.y
                    player.moving = False
            
            # Check win condition - all enemies defeated
            if len(enemies) == 0:
                victory = True
        
        # Render
        screen.fill(GREEN)  # Background color (grass)
        all_sprites.draw(screen)
        
        # Draw UI - Lives, Bombs, Score, and Enemies remaining
        lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
        bombs_text = font.render(f"Bombs: {player.bombs_available}/{player.max_bombs}", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        enemies_text = font.render(f"Enemies: {len(enemies)}", True, WHITE)
        
        # Draw text with black background for readability
        lives_rect = lives_text.get_rect(topleft=(10, 10))
        bombs_rect = bombs_text.get_rect(topleft=(10, 50))
        score_rect = score_text.get_rect(topleft=(10, 90))
        enemies_rect = enemies_text.get_rect(topleft=(10, 130))
        
        pygame.draw.rect(screen, BLACK, lives_rect.inflate(10, 5))
        pygame.draw.rect(screen, BLACK, bombs_rect.inflate(10, 5))
        pygame.draw.rect(screen, BLACK, score_rect.inflate(10, 5))
        pygame.draw.rect(screen, BLACK, enemies_rect.inflate(10, 5))
        
        screen.blit(lives_text, lives_rect)
        screen.blit(bombs_text, bombs_rect)
        screen.blit(score_text, score_rect)
        screen.blit(enemies_text, enemies_rect)
        
        # Draw game over or victory screen
        if game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # Game over text
            game_over_font = pygame.font.Font(None, 72)
            game_over_text = game_over_font.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            screen.blit(game_over_text, game_over_rect)
            
            # Final score
            final_score_text = font.render(f"Final Score: {score}", True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            screen.blit(final_score_text, final_score_rect)
            
            # Stats
            stats_text = font.render(f"Blocks: {blocks_destroyed} | Enemies: {enemies_defeated}", True, WHITE)
            stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
            screen.blit(stats_text, stats_rect)
            
            # Restart instruction
            restart_text = font.render("Press R to Restart or ESC to Quit", True, YELLOW)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 110))
            screen.blit(restart_text, restart_rect)
        
        elif victory:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # Victory text
            victory_font = pygame.font.Font(None, 72)
            victory_text = victory_font.render("VICTORY!", True, YELLOW)
            victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            screen.blit(victory_text, victory_rect)
            
            # Final score
            final_score_text = font.render(f"Final Score: {score}", True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            screen.blit(final_score_text, final_score_rect)
            
            # Stats
            stats_text = font.render(f"Blocks: {blocks_destroyed} | Enemies: {enemies_defeated}", True, WHITE)
            stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
            screen.blit(stats_text, stats_rect)
            
            # Restart instruction
            restart_text = font.render("Press R to Restart or ESC to Quit", True, YELLOW)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 110))
            screen.blit(restart_text, restart_rect)
        
        # Update display
        pygame.display.flip()
        
        # Control frame rate
        clock.tick(FPS)
    
    # Cleanup
    pygame.quit()


if __name__ == "__main__":
    main()
