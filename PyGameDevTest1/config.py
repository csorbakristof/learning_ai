"""
Game Configuration and Constants
"""

# Screen settings
SCREEN_WIDTH = 960
HEADER_HEIGHT = 50  # Height of status bar at top
GAME_AREA_HEIGHT = 640  # Height of actual game field
SCREEN_HEIGHT = GAME_AREA_HEIGHT + HEADER_HEIGHT  # Total screen height
FPS = 60

# Grid settings
TILE_SIZE = 64
GRID_WIDTH = 15  # Number of tiles horizontally
GRID_HEIGHT = 10  # Number of tiles vertically

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
BROWN = (139, 69, 19)
LIGHT_BROWN = (180, 120, 70)
GREEN = (0, 180, 0)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Game settings
BOMB_TIMER = 3000  # milliseconds
EXPLOSION_DURATION = 500  # milliseconds
PLAYER_SPEED = 3  # pixels per frame
ENEMY_SPEED = 2  # pixels per frame

# Player initial stats
INITIAL_BOMB_RANGE = 1
INITIAL_MAX_BOMBS = 1
INITIAL_LIVES = 3

# Power-up spawn chance (0.0 to 1.0)
POWERUP_SPAWN_CHANCE = 0.3

# Power-up types
POWERUP_BOMB = "bomb_up"
POWERUP_FIRE = "fire_up"
POWERUP_SPEED = "speed_up"

# Power-up limits
MAX_BOMB_RANGE = 5
MAX_BOMBS = 5
MAX_SPEED = 6

# Window title
WINDOW_TITLE = "Dynablaster - Bomberman Clone"
