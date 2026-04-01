# Task description

Help me create a Dynablaster-style game using Python and the PyGame package.

First, have a look at the documentation of the package here: https://www.pygame.org/docs/

# 1st task: Dynablaster overview

## Game Overview
**Dynablaster** (also known as **Bomberman** in other regions) is a classic video game franchise created by Shinichi Nakamoto and Shigeki Fujiwara, originally developed by Hudson Soft and currently owned by Konami. The European release was titled "Dyna Blaster" while most other regions knew it as Bomberman. The original game was released in Japan in July 1983.

## Core Gameplay Mechanics

### Game Modes
1. **Single Player Campaign**: Players must defeat enemies and reach an exit to progress through levels. Now we are going to implement only this single player mode.

### Basic Mechanics
- **Bomb Placement**: Players strategically place bombs that explode after a certain amount of time
- **Explosion Pattern**: Bombs explode in multiple directions (typically in a cross pattern: up, down, left, right)
- **Obstacles**: Players must destroy obstacles blocking their path
- **Enemies**: Various enemies must be eliminated to progress
- **Death Conditions**: Players die if they:
  - Touch an enemy
  - Get caught in any bomb's explosion (including their own)
  - This requires careful planning and timing

### Power-ups
Players can collect various power-ups that enhance their abilities:
- **Larger Explosions**: Increases the blast radius of bombs
- **More Bombs**: Allows placing multiple bombs simultaneously
- Other enhancements to movement speed, bomb timer, etc.

## Game Environment
- **Maze-based levels**: The game takes place in grid-based maze arenas
- **Destructible blocks**: Soft blocks can be destroyed to reveal paths and power-ups
- **Indestructible walls**: Hard walls form the permanent structure of the maze

## Genre
Puzzle, maze, and strategy game

## Key Strategic Elements
- Bomb placement requires careful timing and positioning
- Players must predict explosion patterns and plan escape routes
- Blocking opponents or enemies with strategic bomb placement
- Risk vs. reward: getting close to enemies/obstacles while avoiding your own explosions

# 2nd task: PyGame Package Analysis

Analysis of PyGame modules and features that can be used to implement a Bomberman-style game.

## Core Modules

### 1. **pygame.display** - Window and Screen Management
- `pygame.display.set_mode()` - Create the game window with specified dimensions
- `pygame.display.flip()` - Update the entire display surface to the screen
- `pygame.display.update()` - Update portions of the screen for better performance
- **Use Case**: Initialize game window, render the maze arena, and update screen each frame

### 2. **pygame.sprite** - Game Object Management
- **pygame.sprite.Sprite** - Base class for all game objects (player, enemies, bombs, walls, power-ups)
  - Requires `image` and `rect` attributes for rendering
  - `update()` method for custom behavior each frame
- **pygame.sprite.Group** - Container to organize and manage multiple sprites
  - `draw(surface)` - Render all sprites in the group
  - `update()` - Call update() on all contained sprites
- **pygame.sprite.LayeredUpdates** - Group with layer support for z-ordering
  - Useful for rendering bombs under explosions, or power-ups under the player
- **Collision Detection Functions**:
  - `pygame.sprite.spritecollide()` - Detect player colliding with enemies/power-ups/explosions
  - `pygame.sprite.groupcollide()` - Detect bombs hitting walls or enemies
  - `pygame.sprite.spritecollideany()` - Quick check if sprite hits anything in a group
- **Use Case**: 
  - Player, enemies, bombs, explosions, walls, and power-ups as sprites
  - Separate groups for different object types
  - Layer management for visual depth

### 3. **pygame.Rect** - Position and Collision Detection
- Flexible rectangle container with multiple anchor points (center, topleft, bottomright, etc.)
- Built-in collision methods:
  - `colliderect()` - Test if two rectangles overlap
  - `collidepoint()` - Test if a point is inside rectangle
  - `collidelist()` - Find first collision in a list of rectangles
- Position attributes: x, y, top, left, bottom, right, center, centerx, centery, width, height
- Movement methods: `move()`, `move_ip()` (in-place)
- **Use Case**: 
  - Grid-based positioning for maze layout
  - Collision detection between game entities
  - Bounding boxes for all sprites

### 4. **pygame.event** - Input and Event Handling
- `pygame.event.get()` - Retrieve all pending events
- `pygame.QUIT` - Window close event
- **Event Types**: KEYDOWN, KEYUP, MOUSEBUTTONDOWN, etc.
- **Use Case**: 
  - Detect player input (arrow keys or WASD for movement, spacebar for bomb placement)
  - Handle game exit event
  - Pause/resume game functionality

### 5. **pygame.key** - Keyboard State Management
- `pygame.key.get_pressed()` - Get current state of all keyboard keys
- Returns a dictionary-like object with key states
- Constants: `pygame.K_UP`, `pygame.K_DOWN`, `pygame.K_LEFT`, `pygame.K_RIGHT`, `pygame.K_SPACE`, etc.
- **Use Case**: 
  - Continuous movement detection (hold key to keep moving)
  - Smooth player controls
  - Bomb placement with spacebar

### 6. **pygame.time** - Timing and Frame Rate Control
- **pygame.time.Clock** - Frame rate management
  - `tick(fps)` - Limit frame rate and return milliseconds since last call
  - Ensures consistent game speed across different hardware
- `pygame.time.get_ticks()` - Get milliseconds since pygame.init()
- **Use Case**: 
  - Control game loop at 60 FPS
  - Bomb timer (explosion after 3 seconds)
  - Enemy AI update intervals
  - Explosion animation timing
  - Power-up duration tracking

### 7. **pygame.Surface** - Image and Graphics Storage
- Main drawing canvas for the game
- `fill(color)` - Clear screen with background color
- `blit(source, dest)` - Draw one surface onto another
- `get_rect()` - Get rectangular area of the surface
- **Use Case**: 
  - Main game screen
  - Individual sprite images
  - Background tiles
  - Explosion effects

### 8. **pygame.draw** - Drawing Primitives
- `pygame.draw.rect()` - Draw rectangles
- `pygame.draw.circle()` - Draw circles
- `pygame.draw.line()` - Draw lines
- Useful for prototyping or simple graphics
- **Use Case**: 
  - Grid visualization during development
  - Simple placeholder graphics before adding sprites
  - Debug visualization (collision boxes, explosion radius)

### 9. **pygame.image** - Image Loading
- `pygame.image.load()` - Load images from disk (PNG, JPG, GIF, BMP)
- `pygame.image.convert()` - Optimize image for faster blitting
- `pygame.image.convert_alpha()` - Convert with alpha transparency
- **Use Case**: 
  - Load sprite images for player, enemies, walls, bombs
  - Background textures
  - Power-up icons
  - Explosion animations

### 10. **pygame.font** - Text Rendering
- `pygame.font.Font()` - Load TrueType fonts
- `pygame.font.SysFont()` - Load system fonts
- `render()` - Create text surface
- **Use Case**: 
  - Display score
  - Show remaining lives
  - Level number
  - Power-up timers
  - Game over / victory messages

### 11. **pygame.mixer** - Sound Effects
- `pygame.mixer.Sound()` - Load and play sound effects
- `pygame.mixer.music` - Stream background music
- Multiple channels for simultaneous sounds
- **Use Case**: 
  - Bomb placement sound
  - Explosion sound
  - Power-up collection sound
  - Enemy defeat sound
  - Background music
  - Player death sound

### 12. **pygame.transform** - Image Manipulation
- `pygame.transform.scale()` - Resize images
- `pygame.transform.rotate()` - Rotate images
- `pygame.transform.flip()` - Flip horizontally/vertically
- **Use Case**: 
  - Scale sprites to fit grid cells
  - Rotate player sprite based on facing direction
  - Create explosion animation frames
  - Resize images for different screen resolutions

## Implementation Architecture

### Suggested Class Structure
```
Game Loop (main)
├── Display Manager (pygame.display)
├── Clock (pygame.time.Clock)
├── Sprite Groups
│   ├── all_sprites (pygame.sprite.Group)
│   ├── walls (pygame.sprite.Group)
│   ├── soft_blocks (pygame.sprite.Group)
│   ├── bombs (pygame.sprite.Group)
│   ├── explosions (pygame.sprite.Group)
│   ├── enemies (pygame.sprite.Group)
│   └── powerups (pygame.sprite.Group)
└── Game Objects (pygame.sprite.Sprite subclasses)
    ├── Player
    ├── Enemy
    ├── Bomb
    ├── Explosion
    ├── Wall (indestructible)
    ├── SoftBlock (destructible)
    └── PowerUp
```

### Game Loop Pattern
```python
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

while running:
    # Event handling (pygame.event)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Input processing (pygame.key)
    keys = pygame.key.get_pressed()
    
    # Update game state (sprite.update())
    all_sprites.update()
    
    # Collision detection (sprite.spritecollide())
    # Check player vs enemies, bombs vs walls, etc.
    
    # Rendering
    screen.fill(background_color)
    all_sprites.draw(screen)
    
    # Display update
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()
```

## Grid-Based Movement System

For Bomberman's grid-based maze, we can use:
- **Tile size constant** (e.g., 32x32 or 64x64 pixels)
- **Grid coordinates** converted to pixel coordinates
- **Rect positioning** aligned to grid for snap-to-grid movement
- **Collision detection** using Rect methods before moving to new grid cell

## Summary

PyGame provides all necessary components for Bomberman implementation:
- **Core game loop** with display and timing control
- **Sprite system** for organized game object management
- **Collision detection** for game interactions
- **Input handling** for player controls
- **Graphics and animation** support
- **Sound effects** for enhanced gameplay experience

The modular design of PyGame allows building the game incrementally, starting with basic movement and gradually adding bombs, enemies, power-ups, and polish.

# 3rd Task: Plans for the implementation

Plan the implementation steps of the game. Create a step-by-step plan here, which guides you along the process.

