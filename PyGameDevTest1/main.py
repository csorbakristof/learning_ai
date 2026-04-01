"""
Dynablaster - Bomberman Clone
Main game file
"""
import pygame
import random
from config import *
from sprites import Wall, SoftBlock, Player, Bomb, Explosion, Enemy, PowerUp
from ui import Menu, InstructionsScreen, PauseMenu, LevelTransitionScreen, draw_hud, draw_game_over_screen, draw_victory_screen
from levels import get_level, get_total_levels, is_final_level


def grid_to_pixel(grid_x, grid_y):
    """Convert grid coordinates to pixel coordinates"""
    return grid_x * TILE_SIZE, grid_y * TILE_SIZE


def pixel_to_grid(pixel_x, pixel_y):
    """Convert pixel coordinates to grid coordinates"""
    return pixel_x // TILE_SIZE, pixel_y // TILE_SIZE


def generate_level(walls_group, soft_blocks_group, soft_block_density=0.6):
    """
    Generate classic Bomberman level layout
    - Outer border walls
    - Checkerboard pattern of inner walls
    - Random soft blocks in empty spaces
    - Clear 3x3 area at starting position (top-left)
    
    Args:
        walls_group: Sprite group for walls
        soft_blocks_group: Sprite group for soft blocks
        soft_block_density: Percentage of available spaces to fill (0.0-1.0)
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
            
            # Random chance to place soft block based on density
            if random.random() < soft_block_density:
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


def spawn_enemies(num_enemies, walls_group, soft_blocks_group, bombs_group, player, enemies_group, speed_multiplier=1.0):
    """
    Spawn enemies at random valid positions away from player
    
    Args:
        num_enemies: Number of enemies to spawn
        walls_group: Sprite group for walls
        soft_blocks_group: Sprite group for soft blocks
        player: Player object
        enemies_group: Sprite group for enemies
        speed_multiplier: Speed multiplier for enemy difficulty scaling
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
            enemy = Enemy(x, y, walls_group, soft_blocks_group, bombs_group, speed_multiplier)
            enemies_group.add(enemy)
            spawned += 1



def init_game(level_config, previous_player_stats=None):
    """
    Initialize game with fresh state for a specific level
    
    Args:
        level_config: LevelConfig object defining the level parameters
        previous_player_stats: Optional dict with player stats to carry over from previous level
            Keys: 'lives', 'max_bombs', 'bomb_range', 'speed', 'score'
    
    Returns:
        Dictionary containing game state
    """
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    soft_blocks = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    
    # Generate level with specified density
    generate_level(walls, soft_blocks, level_config.soft_block_density)
    
    # Create player at starting position (grid 1, 1)
    player = Player(1, 1, walls, soft_blocks, bombs)
    
    # Carry over player stats from previous level if provided
    if previous_player_stats:
        player.lives = previous_player_stats.get('lives', INITIAL_LIVES)
        player.max_bombs = previous_player_stats.get('max_bombs', INITIAL_MAX_BOMBS)
        player.bombs_available = player.max_bombs  # Reset available bombs
        player.bomb_range = previous_player_stats.get('bomb_range', INITIAL_BOMB_RANGE)
        player.speed = previous_player_stats.get('speed', PLAYER_SPEED)
    
    # Spawn enemies with level-specific speed multiplier
    spawn_enemies(level_config.num_enemies, walls, soft_blocks, bombs, player, enemies, 
                  level_config.enemy_speed_multiplier)
    
    # Add all sprites to the main group for rendering
    all_sprites.add(walls)
    all_sprites.add(soft_blocks)
    all_sprites.add(powerups)
    all_sprites.add(enemies)
    all_sprites.add(player)
    
    # Game state
    score = previous_player_stats.get('score', 0) if previous_player_stats else 0
    
    game_state = {
        'all_sprites': all_sprites,
        'walls': walls,
        'soft_blocks': soft_blocks,
        'bombs': bombs,
        'explosions': explosions,
        'enemies': enemies,
        'powerups': powerups,
        'player': player,
        'score': score,
        'blocks_destroyed': 0,  # Reset per-level stats
        'enemies_defeated': 0,
        'game_over': False,
        'victory': False,
        'space_pressed': False,
        'level_num': level_config.level_num
    }
    
    return game_state


def main():
    """Main game function"""
    # Initialize Pygame
    pygame.init()
    
    # Create game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    
    # Create clock for FPS control
    clock = pygame.time.Clock()
    
    # Game states
    STATE_MENU = "menu"
    STATE_PLAYING = "playing"
    STATE_PAUSED = "paused"
    STATE_INSTRUCTIONS = "instructions"
    
    current_state = STATE_MENU
    
    # Create UI objects
    menu = Menu(screen)
    instructions_screen = InstructionsScreen(screen)
    pause_menu = PauseMenu(screen)
    
    # Level tracking
    current_level = 1
    
    # Game state (will be initialized when starting game)
    game_state = None
    
    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                # Menu state
                if current_state == STATE_MENU:
                    action = menu.handle_input(event)
                    if action == "start":
                        # Start from level 1
                        current_level = 1
                        level_config = get_level(current_level)
                        game_state = init_game(level_config)
                        current_state = STATE_PLAYING
                    elif action == "instructions":
                        current_state = STATE_INSTRUCTIONS
                    elif action == "quit":
                        running = False
                
                # Instructions state
                elif current_state == STATE_INSTRUCTIONS:
                    if event.key == pygame.K_ESCAPE:
                        current_state = STATE_MENU
                
                # Playing state
                elif current_state == STATE_PLAYING:
                    # Pause game
                    if event.key in (pygame.K_ESCAPE, pygame.K_p) and not (game_state['game_over'] or game_state['victory']):
                        current_state = STATE_PAUSED
                    
                    # Game over or victory - restart or return to menu
                    elif game_state['game_over']:
                        if event.key == pygame.K_r:
                            # Restart from level 1
                            current_level = 1
                            level_config = get_level(current_level)
                            game_state = init_game(level_config)
                        elif event.key == pygame.K_m:
                            current_state = STATE_MENU
                            game_state = None
                    
                    # Victory - advance to next level or complete game
                    elif game_state['victory']:
                        if event.key == pygame.K_SPACE and not is_final_level(current_level):
                            # Advance to next level, carrying over player stats
                            current_level += 1
                            level_config = get_level(current_level)
                            player_stats = {
                                'lives': game_state['player'].lives,
                                'max_bombs': game_state['player'].max_bombs,
                                'bomb_range': game_state['player'].bomb_range,
                                'speed': game_state['player'].speed,
                                'score': game_state['score']
                            }
                            game_state = init_game(level_config, player_stats)
                        elif event.key == pygame.K_r:
                            # Restart from level 1
                            current_level = 1
                            level_config = get_level(current_level)
                            game_state = init_game(level_config)
                        elif event.key == pygame.K_m:
                            current_state = STATE_MENU
                            game_state = None
                
                # Paused state
                elif current_state == STATE_PAUSED:
                    # Resume with ESC or P
                    if event.key in (pygame.K_ESCAPE, pygame.K_p):
                        current_state = STATE_PLAYING
                    else:
                        action = pause_menu.handle_input(event)
                        if action == "resume":
                            current_state = STATE_PLAYING
                        elif action == "restart":
                            # Restart from level 1
                            current_level = 1
                            level_config = get_level(current_level)
                            game_state = init_game(level_config)
                            current_state = STATE_PLAYING
                        elif action == "menu":
                            current_state = STATE_MENU
                            game_state = None
        
        # Update and Render based on current state
        if current_state == STATE_MENU:
            menu.draw()
        
        elif current_state == STATE_INSTRUCTIONS:
            instructions_screen.draw()
        
        elif current_state == STATE_PAUSED:
            # Draw the paused game in background
            screen.fill(BLACK)  # Fill entire screen with black
            game_area = pygame.Rect(0, HEADER_HEIGHT, SCREEN_WIDTH, GAME_AREA_HEIGHT)
            pygame.draw.rect(screen, GREEN, game_area)  # Game field background
            game_state['all_sprites'].draw(screen)
            draw_hud(screen, game_state['player'], game_state['score'], 
                    len(game_state['enemies']), current_level)
            
            # Draw pause menu overlay
            pause_menu.draw()
        
        elif current_state == STATE_PLAYING and game_state:
            # Only process game logic if not game over or victory
            if not game_state['game_over'] and not game_state['victory']:
                # Input handling - continuous key checking for smooth movement
                keys = pygame.key.get_pressed()
                
                # Arrow keys
                if keys[pygame.K_UP]:
                    game_state['player'].move(0, -1)
                elif keys[pygame.K_DOWN]:
                    game_state['player'].move(0, 1)
                elif keys[pygame.K_LEFT]:
                    game_state['player'].move(-1, 0)
                elif keys[pygame.K_RIGHT]:
                    game_state['player'].move(1, 0)
                
                # WASD keys
                if keys[pygame.K_w]:
                    game_state['player'].move(0, -1)
                elif keys[pygame.K_s]:
                    game_state['player'].move(0, 1)
                elif keys[pygame.K_a]:
                    game_state['player'].move(-1, 0)
                elif keys[pygame.K_d]:
                    game_state['player'].move(1, 0)
                
                # Bomb placement with spacebar (only when player is aligned to grid)
                if keys[pygame.K_SPACE] and not game_state['space_pressed']:
                    player = game_state['player']
                    if not player.moving and player.bombs_available > 0:
                        if can_place_bomb(player.grid_x, player.grid_y, game_state['bombs']):
                            bomb = Bomb(player.grid_x, player.grid_y, player.bomb_range, player)
                            game_state['bombs'].add(bomb)
                            game_state['all_sprites'].add(bomb)
                            player.bombs_available -= 1
                            game_state['space_pressed'] = True
                
                # Reset space key tracking
                if not keys[pygame.K_SPACE]:
                    game_state['space_pressed'] = False
                
                # Update
                game_state['all_sprites'].update()
                
                # Check for bombs ready to explode
                for bomb in game_state['bombs'].copy():
                    if bomb.is_ready_to_explode():
                        # Create explosion
                        destroyed_blocks = create_explosion(
                            bomb.grid_x, bomb.grid_y, bomb.bomb_range,
                            game_state['walls'], game_state['soft_blocks'], game_state['explosions']
                        )
                        
                        # Add explosions to sprite groups
                        game_state['all_sprites'].add(game_state['explosions'])
                        
                        # Check for chain explosions: trigger other bombs hit by this explosion
                        for other_bomb in game_state['bombs'].copy():
                            if other_bomb != bomb and not other_bomb.exploded:
                                # Check if other bomb is in explosion range
                                explosion_hits = pygame.sprite.spritecollide(other_bomb, game_state['explosions'], False)
                                if explosion_hits:
                                    # Trigger immediate explosion
                                    other_bomb.exploded = True
                        
                        # Remove destroyed soft blocks and update score
                        for block in destroyed_blocks:
                            # Spawn power-up with chance
                            if random.random() < POWERUP_SPAWN_CHANCE:
                                # Random power-up type
                                powerup_type = random.choice([POWERUP_BOMB, POWERUP_FIRE, POWERUP_SPEED])
                                powerup = PowerUp(block.grid_x, block.grid_y, powerup_type)
                                game_state['powerups'].add(powerup)
                                game_state['all_sprites'].add(powerup)
                            
                            block.kill()
                            game_state['all_sprites'].remove(block)
                            game_state['soft_blocks'].remove(block)
                            game_state['blocks_destroyed'] += 1
                            game_state['score'] += 10  # 10 points per block
                        
                        # Return bomb to player
                        bomb.owner.bombs_available += 1
                        
                        # Remove bomb
                        bomb.kill()
                        game_state['bombs'].remove(bomb)
                        game_state['all_sprites'].remove(bomb)
                
                # Check collision between enemies and explosions
                for enemy in game_state['enemies'].copy():
                    explosion_hits = pygame.sprite.spritecollide(enemy, game_state['explosions'], False)
                    if explosion_hits:
                        enemy.kill()
                        game_state['enemies'].remove(enemy)
                        game_state['all_sprites'].remove(enemy)
                        game_state['enemies_defeated'] += 1
                        game_state['score'] += 100  # 100 points per enemy
                
                # Check collision between player and explosions
                explosion_hits = pygame.sprite.spritecollide(game_state['player'], game_state['explosions'], False)
                if explosion_hits:
                    game_state['player'].lives -= 1
                    if game_state['player'].lives <= 0:
                        game_state['game_over'] = True
                    else:
                        # Respawn player at starting position
                        player = game_state['player']
                        player.rect.x = 1 * TILE_SIZE
                        player.rect.y = 1 * TILE_SIZE + HEADER_HEIGHT
                        player.grid_x = 1
                        player.grid_y = 1
                        player.target_x = player.rect.x
                        player.target_y = player.rect.y
                        player.moving = False
                
                # Check collision between player and enemies
                enemy_hits = pygame.sprite.spritecollide(game_state['player'], game_state['enemies'], False)
                if enemy_hits:
                    game_state['player'].lives -= 1
                    if game_state['player'].lives <= 0:
                        game_state['game_over'] = True
                    else:
                        # Respawn player at starting position
                        player = game_state['player']
                        player.rect.x = 1 * TILE_SIZE
                        player.rect.y = 1 * TILE_SIZE + HEADER_HEIGHT
                        player.grid_x = 1
                        player.grid_y = 1
                        player.target_x = player.rect.x
                        player.target_y = player.rect.y
                        player.moving = False
                
                # Check collision between player and power-ups
                powerup_hits = pygame.sprite.spritecollide(game_state['player'], game_state['powerups'], True)
                for powerup in powerup_hits:
                    player = game_state['player']
                    # Apply power-up effect
                    if powerup.powerup_type == POWERUP_BOMB:
                        if player.max_bombs < MAX_BOMBS:
                            player.max_bombs += 1
                            player.bombs_available += 1
                    elif powerup.powerup_type == POWERUP_FIRE:
                        if player.bomb_range < MAX_BOMB_RANGE:
                            player.bomb_range += 1
                    elif powerup.powerup_type == POWERUP_SPEED:
                        if player.speed < MAX_SPEED:
                            player.speed += 1
                    # Remove from all_sprites
                    game_state['all_sprites'].remove(powerup)
                    game_state['score'] += 50  # Bonus points for collecting power-up
                
                # Check win condition - all enemies defeated
                if len(game_state['enemies']) == 0:
                    game_state['victory'] = True
            
            # Render game
            screen.fill(BLACK)  # Fill entire screen with black
            game_area = pygame.Rect(0, HEADER_HEIGHT, SCREEN_WIDTH, GAME_AREA_HEIGHT)
            pygame.draw.rect(screen, GREEN, game_area)  # Game field background (grass)
            game_state['all_sprites'].draw(screen)
            
            # Draw enhanced HUD
            draw_hud(screen, game_state['player'], game_state['score'], 
                    len(game_state['enemies']), current_level)
            
            # Draw game over or victory screen
            if game_state['game_over']:
                draw_game_over_screen(screen, game_state['score'], 
                                     game_state['blocks_destroyed'], 
                                     game_state['enemies_defeated'])
            elif game_state['victory']:
                draw_victory_screen(screen, game_state['score'], 
                                   game_state['blocks_destroyed'], 
                                   game_state['enemies_defeated'],
                                   is_final_level(current_level))
        
        # Update display
        pygame.display.flip()
        
        # Control frame rate
        clock.tick(FPS)
    
    # Cleanup
    pygame.quit()


if __name__ == "__main__":
    main()
