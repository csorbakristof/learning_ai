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

## Phase 1: Project Setup and Basic Game Loop

### Step 1.1: Project Structure Setup
- Create project directory: `PyGameDevTest1/`
- Create subdirectories:
  - `assets/` - for images, sounds, fonts
  - `assets/images/` - sprite images
  - `assets/sounds/` - sound effects
  - `assets/fonts/` - custom fonts (optional)
- Create main game file: `main.py`
- Create requirements file: `requirements.txt` (include pygame)
- Install pygame: `pip install pygame`

### Step 1.2: Basic Game Window
- Initialize pygame
- Create game window with fixed dimensions (e.g., 800x600 or 960x640)
- Set window title and icon
- Create game clock for FPS control
- Implement basic game loop:
  - Event handling (quit event)
  - Screen clearing with background color
  - Display update
  - Frame rate limiting (60 FPS)
- Test: Window opens and closes properly

### Step 1.3: Constants and Configuration
- Create `config.py` file with game constants:
  - Screen dimensions (WIDTH, HEIGHT)
  - Grid dimensions (GRID_WIDTH, GRID_HEIGHT)
  - Tile size (TILE_SIZE = 64)
  - Frame rate (FPS = 60)
  - Colors (RGB values)
  - Game timing constants (bomb timer, explosion duration, etc.)

## Phase 2: Grid System and Static Elements

### Step 2.1: Grid System Implementation
- Implement grid coordinate to pixel coordinate conversion functions
- Create grid data structure (2D array/list) to represent maze
- Define cell types: empty, wall, soft_block
- Implement function to convert grid position to screen position
- Test: Verify coordinate conversions are correct

### Step 2.2: Wall Sprites (Indestructible)
- Create `Wall` class inheriting from `pygame.sprite.Sprite`
- For now, use colored rectangles (gray/dark)
- Add image and rect attributes
- Implement wall placement based on grid pattern
- Create walls group: `pygame.sprite.Group()`
- Test: Walls render on screen in grid pattern

### Step 2.3: Soft Block Sprites (Destructible)
- Create `SoftBlock` class inheriting from `pygame.sprite.Sprite`
- Use different color than walls (brown/light gray)
- Implement soft block placement (random or pattern-based)
- Ensure spawn area around starting position is clear
- Create soft_blocks group
- Test: Soft blocks render correctly and don't block spawn area

### Step 2.4: Level Generation
- Create `generate_level()` function
- Implement classic Bomberman level pattern:
  - Outer walls forming border
  - Inner walls in checkerboard pattern (every other row/column)
  - Soft blocks randomly placed in empty spaces
  - Clear 3x3 area at starting position (usually top-left)
- Test: Generated level looks like classic Bomberman maze

## Phase 3: Player Character

### Step 3.1: Player Sprite Creation
- Create `Player` class inheriting from `pygame.sprite.Sprite`
- For now, use colored rectangle or circle (blue/white)
- Initialize at starting position (grid 1,1 typically)
- Add image and rect attributes
- Set initial stats:
  - Position (grid coordinates)
  - Speed
  - Max bombs (initially 1)
  - Bomb range (initially 1)
  - Lives (3)
- Add player to sprites groups
- Test: Player renders at correct starting position

### Step 3.2: Player Movement (Grid-Based)
- Implement movement input detection (arrow keys or WASD)
- Implement grid-based movement:
  - Move one full grid cell at a time
  - Movement should be smooth (interpolation)
  - Or snap to grid immediately for simplicity
- Store target position and current position
- Update movement in player's `update()` method
- Test: Player moves in four directions

### Step 3.3: Collision Detection with Walls
- Implement collision checking before allowing movement
- Check if target grid cell is empty, wall, or soft block
- Only allow movement to empty cells
- Use pygame collision detection or grid-based lookup
- Test: Player cannot walk through walls or soft blocks

### Step 3.4: Player Animation (Optional for now)
- Can add later: walking animation frames
- Direction-based sprite (facing up/down/left/right)
- For MVP, single sprite is sufficient

## Phase 4: Bomb Mechanics

### Step 4.1: Bomb Sprite Creation
- Create `Bomb` class inheriting from `pygame.sprite.Sprite`
- Visual: colored circle or square (black/dark gray)
- Store bomb properties:
  - Position (grid coordinates)
  - Timer (e.g., 3000 milliseconds)
  - Range (inherited from player's bomb_range)
  - Owner (player reference)
- Create bombs group
- Test: Can create bomb object

### Step 4.2: Bomb Placement
- Detect bomb placement input (spacebar)
- Check if player can place bomb:
  - Must be on grid-aligned position
  - Cannot place if bomb already exists at that position
  - Must have bombs available (max_bombs limit)
- Place bomb at player's current grid position
- Decrement available bombs counter
- Test: Player can place bombs on grid

### Step 4.3: Bomb Timer and Explosion Trigger
- Implement bomb timer countdown using pygame.time.get_ticks()
- When timer reaches zero:
  - Remove bomb from game
  - Trigger explosion
  - Increment player's available bombs counter
- Test: Bomb disappears after 3 seconds

### Step 4.4: Explosion Creation
- Create `Explosion` class inheriting from `pygame.sprite.Sprite`
- Implement explosion pattern:
  - Center at bomb position
  - Extend in 4 directions (up, down, left, right)
  - Range determined by bomb's range value
  - Stop at walls (indestructible)
  - Destroy soft blocks (stop after hitting one)
- Create separate explosion sprites for:
  - Center
  - Horizontal segments
  - Vertical segments
  - End caps (optional visual enhancement)
- Create explosions group
- Set explosion duration (e.g., 500ms)
- Test: Explosion appears in cross pattern when bomb explodes

### Step 4.5: Explosion Effects on Environment
- Check explosion collision with soft blocks
- Remove soft blocks hit by explosion
- Explosion stops extending in that direction after hitting soft block
- Test: Soft blocks are destroyed by explosions

### Step 4.6: Explosion Damage to Player
- Check explosion collision with player
- If player is in explosion area:
  - Decrease player lives
  - Respawn player or game over
- Implement temporary invulnerability after respawn (optional)
- Test: Player takes damage from explosions

## Phase 5: Enemy Implementation

### Step 5.1: Basic Enemy Sprite
- Create `Enemy` class inheriting from `pygame.sprite.Sprite`
- Visual: different colored rectangle (red/purple)
- Initialize at random valid position (not too close to player)
- Enemy properties:
  - Position
  - Movement speed
  - AI type (random, chase, patrol)
- Create enemies group
- Test: Enemy renders on screen

### Step 5.2: Enemy AI - Random Movement
- Implement simple random movement AI:
  - Choose random direction at intervals
  - Move in that direction until hitting obstacle
  - Then choose new random direction
- Check collisions with walls and soft blocks
- Update position in enemy's `update()` method
- Test: Enemy moves around maze randomly

### Step 5.3: Enemy AI - Smarter Behavior (Optional)
- Implement pathfinding toward player (A* or simple chase)
- Or implement patrol patterns
- Add variety with different enemy types and behaviors
- Can be added later for complexity

### Step 5.4: Enemy Collision with Player
- Check collision between player and enemies
- If collision detected:
  - Player loses life
  - Respawn or game over
- Test: Player takes damage when touching enemy

### Step 5.5: Enemy Destruction by Explosions
- Check explosion collision with enemies
- Remove enemy when hit by explosion
- Add score points for defeating enemy
- Optional: death animation
- Test: Enemies are destroyed by explosions

## Phase 6: Power-ups

### Step 6.1: Power-up System Design
- Define power-up types:
  - Bomb Up (increase max bombs)
  - Fire Up (increase explosion range)
  - Speed Up (increase movement speed)
  - (Optional) Bomb Pass (walk through bombs)
  - (Optional) Wall Pass (walk through soft blocks)
- Create `PowerUp` class inheriting from `pygame.sprite.Sprite`
- Store power-up type and effects

### Step 6.2: Power-up Generation
- When soft block is destroyed:
  - Random chance to spawn power-up (e.g., 30%)
  - Power-up appears at block's position
- Create powerups group
- Test: Power-ups appear when soft blocks destroyed

### Step 6.3: Power-up Collection
- Check collision between player and power-ups
- When collected:
  - Apply effect to player (increase bombs, range, speed)
  - Remove power-up from game
  - Play collection sound (optional)
- Test: Player collects power-ups and gains effects

### Step 6.4: Power-up Visual Distinction
- Use different colors or shapes for different power-up types
- Or load icon images for each type
- Test: Can distinguish power-up types visually

## Phase 7: Game State Management

### Step 7.1: Win Condition
- Check if all enemies are defeated
- Display victory message
- Show score and stats
- Option to restart or quit
- Test: Win condition triggers correctly

### Step 7.2: Lose Condition
- Check if player lives reach zero
- Display game over message
- Show final score
- Option to restart or quit
- Test: Lose condition triggers correctly

### Step 7.3: Level Progression
- After winning level, advance to next level
- Increase difficulty:
  - More enemies
  - Fewer soft blocks
  - Faster enemies
  - Different maze patterns
- Reset player position and power-ups
- Track current level number
- Test: Can complete multiple levels

### Step 7.4: Score System
- Track score based on:
  - Enemies defeated
  - Soft blocks destroyed
  - Time bonus (optional)
  - Power-ups collected
- Display score on screen during gameplay
- Test: Score updates correctly

### Step 7.5: Lives Display
- Show remaining lives on screen
- Visual representation (hearts or icons)
- Update when player takes damage
- Test: Lives display updates correctly

## Phase 8: User Interface

### Step 8.1: HUD (Heads-Up Display)
- Create UI elements:
  - Score counter (top-left or top-center)
  - Lives remaining (top-right)
  - Current level number
  - Time remaining (optional)
- Render text using pygame.font
- Update HUD every frame
- Test: HUD displays correct information

### Step 8.2: Main Menu
- Create menu screen before game starts
- Menu options:
  - Start Game
  - Instructions
  - Quit
- Implement menu navigation
- Test: Can navigate menu and start game

### Step 8.3: Pause System
- Detect pause input (ESC or P key)
- Pause game loop (stop updates, keep rendering)
- Show pause overlay
- Resume when pause key pressed again
- Test: Game pauses and resumes correctly

### Step 8.4: Game Over / Victory Screen
- Create end game screens
- Display final stats
- Options: Restart or Main Menu
- Test: End screens display correctly

## Phase 9: Audio and Polish

### Step 9.1: Sound Effects
- Find or create sound files:
  - Bomb placement
  - Explosion
  - Power-up collection
  - Enemy defeat
  - Player hit/death
  - Menu selection
- Load sounds using pygame.mixer
- Play sounds at appropriate times
- Test: Sounds play correctly

### Step 9.2: Background Music
- Find or create background music
- Load music using pygame.mixer.music
- Play music in loop during gameplay
- Different music for menu and game
- Test: Music plays continuously

### Step 9.3: Visual Improvements
- Replace colored rectangles with sprites:
  - Load sprite images for all game objects
  - Player, enemies, walls, soft blocks, bombs, explosions
- Scale sprites to fit grid cells
- Test: All sprites display correctly

### Step 9.4: Animations
- Add animation frames for:
  - Player walking (4 directions)
  - Bomb pulsing/blinking
  - Explosion expanding
  - Enemy movement
- Implement animation frame switching
- Test: Animations play smoothly

### Step 9.5: Particle Effects (Optional)
- Add visual effects:
  - Explosion particles
  - Power-up sparkles
  - Dust clouds when moving
- Test: Effects enhance visual appeal

## Phase 10: Testing and Refinement

### Step 10.1: Bug Testing
- Test all game mechanics thoroughly
- Check edge cases:
  - Multiple bombs at once
  - Chain explosions (bomb triggering bomb)
  - Player death during movement
  - Power-up collection while moving
- Fix any found bugs

### Step 10.2: Gameplay Balancing
- Adjust difficulty parameters:
  - Enemy speed
  - Bomb timer
  - Explosion duration
  - Power-up spawn rate
  - Level progression difficulty
- Test with real gameplay sessions
- Make adjustments for fun factor

### Step 10.3: Performance Optimization
- Profile game performance
- Optimize sprite rendering if needed
- Reduce unnecessary calculations
- Ensure 60 FPS on target hardware
- Test: Game runs smoothly

### Step 10.4: Code Cleanup
- Refactor code for readability
- Add comments and docstrings
- Organize code into modules:
  - `sprites.py` - all sprite classes
  - `config.py` - constants
  - `utils.py` - helper functions
  - `main.py` - game loop
- Follow PEP 8 style guide
- Test: Code is clean and maintainable

### Step 10.5: Documentation
- Write README.md:
  - Game description
  - How to install
  - How to play (controls)
  - Screenshots
- Add inline code documentation
- Create user manual if needed

## Phase 11: Advanced Features (Optional)

### Step 11.1: Multiple Game Modes
- Classic mode
- Time attack mode
- Survival mode (endless enemies)
- Puzzle mode (preset levels)

### Step 11.2: Local Multiplayer
- Support 2-4 players on same keyboard
- Different control schemes for each player
- Battle mode (last player standing)

### Step 11.3: Level Editor
- Create tool to design custom levels
- Save/load level files
- Share levels with others

### Step 11.4: High Score Table
- Save high scores to file
- Display leaderboard
- Track best times per level

### Step 11.5: Settings Menu
- Adjustable volume
- Control customization
- Graphics quality options
- Fullscreen toggle

## Implementation Priority Summary

**MVP (Minimum Viable Product) - Must Have:**
- Phase 1: Setup and basic loop
- Phase 2: Grid and walls
- Phase 3: Player movement
- Phase 4: Bombs and explosions
- Phase 5: Basic enemy
- Phase 7: Win/lose conditions (basic)

**Enhanced Version - Should Have:**
- Phase 6: Power-ups
- Phase 7: Full game state management
- Phase 8: UI elements
- Phase 9: Sound effects (basic)

**Polished Version - Nice to Have:**
- Phase 9: Full audio and visual polish
- Phase 10: Testing and refinement
- Phase 11: Advanced features

**Recommended Development Order:**
1. Get basic window and grid working (Phase 1-2)
2. Add player movement with collision (Phase 3)
3. Implement bombs and explosions (Phase 4)
4. Add simple enemy (Phase 5)
5. Implement win/lose conditions (Phase 7, basic)
6. Add power-ups (Phase 6)
7. Create UI and menus (Phase 8)
8. Add audio (Phase 9.1-9.2)
9. Replace placeholders with real sprites (Phase 9.3)
10. Test and polish (Phase 10)
11. Add advanced features as desired (Phase 11)

---

# Development Milestones

This section breaks down the MVP implementation into **4 testable milestones**. Each milestone produces working, testable code that builds upon the previous one.

## Milestone 1: Foundation - Maze Environment
**Phases: 1-2 (Project Setup, Grid System, Static Elements)**

**Goal:** Create the basic game window with a visible maze that has walls and soft blocks arranged in the classic Bomberman pattern.

**Includes:**
- Project structure setup (directories, requirements.txt)
- Basic game window with pygame initialization
- Game loop with event handling and FPS control
- Constants and configuration file (config.py)
- Grid coordinate system and conversion functions
- Wall sprites (indestructible) with grid placement
- Soft block sprites (destructible) with random placement
- Level generation with classic Bomberman pattern:
  - Outer border walls
  - Checkerboard pattern of inner walls
  - Random soft blocks in empty spaces
  - Clear 3x3 starting area

**Deliverable:** A window displaying a Bomberman-style maze with gray walls and brown soft blocks on a grid.

**Test Criteria:**
- Window opens at correct size (e.g., 960x640)
- Game loop runs at stable 60 FPS
- Maze displays with proper grid alignment
- Can close window with X button
- Level pattern matches classic Bomberman layout
- Starting area (top-left) is clear of obstacles

**Files Created:**
- `main.py` - game loop
- `config.py` - constants and settings
- `sprites.py` - Wall and SoftBlock classes (or separate files)
- `requirements.txt` - pygame dependency

---

## Milestone 2: Player Character and Movement
**Phases: 3 (Player Character)**

**Goal:** Add a controllable player character that can navigate the maze with proper collision detection.

**Includes:**
- Player sprite class with initial position
- Grid-based movement system (smooth or snap-to-grid)
- Input handling for movement (arrow keys or WASD)
- Collision detection with walls and soft blocks
- Player can only move to empty grid cells
- Visual representation (colored rectangle/circle as placeholder)
- Player stats initialization (speed, max bombs, bomb range, lives)

**Deliverable:** A player character that moves around the maze using keyboard controls, correctly blocked by walls and soft blocks.

**Test Criteria:**
- Player renders at starting position (grid 1,1)
- Arrow keys/WASD move player in 4 directions
- Movement is smooth and properly aligned to grid
- Player cannot walk through walls
- Player cannot walk through soft blocks
- Player movement feels responsive (no lag)

**Files Modified:**
- `sprites.py` - Add Player class
- `main.py` - Add player creation and input handling

---

## Milestone 3: Bombs and Explosions
**Phases: 4 (Bomb Mechanics)**

**Goal:** Implement the core gameplay mechanic - placing bombs that explode in a cross pattern, destroying soft blocks and affecting the player.

**Includes:**
- Bomb sprite class with timer
- Bomb placement input (spacebar)
- Bomb placement rules:
  - Max bombs limit (initially 1)
  - Cannot place bomb where one exists
  - Must be grid-aligned
- Bomb timer (3 seconds countdown)
- Explosion sprite class
- Explosion pattern generation:
  - Cross pattern (4 directions)
  - Range-based extension
  - Stops at indestructible walls
  - Destroys soft blocks (stops after hitting)
- Explosion effects:
  - Destroys soft blocks on contact
  - Damages player on contact (loses life)
- Explosion duration and cleanup
- Bomb counter management (return bomb after explosion)

**Deliverable:** Fully functional bomb system where player can place bombs that explode in cross patterns, destroy soft blocks, and can hurt the player.

**Test Criteria:**
- Spacebar places bomb at player position
- Bomb appears on grid
- Bomb explodes after ~3 seconds
- Explosion extends in 4 directions (up, down, left, right)
- Explosion stops at walls
- Explosion destroys soft blocks and stops
- Soft blocks disappear when hit by explosion
- Player takes damage when caught in explosion
- Can only place 1 bomb at a time initially
- After explosion, can place another bomb
- Multiple bombs can exist if power-up collected (later)

**Files Modified:**
- `sprites.py` - Add Bomb and Explosion classes
- `main.py` - Add bomb placement logic and collision checks
- `config.py` - Add bomb/explosion timing constants

---

## Milestone 4: Complete MVP - Enemies and Game States
**Phases: 5 (Enemy Implementation) + 7 Basic (Win/Lose Conditions)**

**Goal:** Add enemies with basic AI and implement win/lose conditions to create a complete, playable game.

**Includes:**

**Enemy System:**
- Enemy sprite class with random movement AI
- Enemy spawning at valid positions (away from player)
- Random movement behavior:
  - Choose random direction periodically
  - Move until hitting obstacle
  - Change direction when blocked
- Enemy collision with player (player loses life)
- Enemy destruction by explosions
- Multiple enemies on screen (2-4 for testing)

**Game State Management:**
- Player lives tracking (3 lives)
- Life loss on collision or explosion damage
- Basic respawn system or immediate game over
- Win condition: All enemies defeated
- Lose condition: Player lives reach zero
- Victory message display
- Game over message display
- Basic score tracking (enemies defeated + blocks destroyed)
- Score display on screen
- Lives display on screen
- Option to restart after win/lose

**Deliverable:** A fully playable Bomberman game where you must defeat all enemies while avoiding their touch and your own bombs. Game ends with win or lose screen.

**Test Criteria:**
- Enemies appear on screen at valid positions
- Enemies move randomly around maze
- Enemies avoid walls and soft blocks
- Touching enemy damages player (loses 1 life)
- Explosions destroy enemies
- Game ends (win) when all enemies defeated
- Victory message displays with score
- Game ends (lose) when player loses all lives
- Game over message displays
- Score updates when destroying blocks and enemies
- Lives counter displays and updates correctly
- Can restart game after winning or losing

**Files Modified:**
- `sprites.py` - Add Enemy class
- `main.py` - Add game state management, win/lose logic, score/lives display
- `config.py` - Add enemy and game state constants

---

## Post-MVP Enhancement Path

After completing all 4 milestones, you'll have a fully playable Bomberman MVP. The recommended enhancement order:

1. **Add Power-ups (Phase 6)** - Increases replayability and strategy
2. **Improve UI (Phase 8)** - Add menus, HUD, pause functionality
3. **Add Audio (Phase 9.1-9.2)** - Sound effects and background music
4. **Visual Polish (Phase 9.3-9.4)** - Replace placeholders with sprites and animations
5. **Testing & Balancing (Phase 10)** - Fine-tune difficulty and fix bugs
6. **Advanced Features (Phase 11)** - Optional enhancements as desired

---

## How to Use These Milestones

**When implementing**, work through the milestones sequentially:
- Complete all tasks in Milestone 1, test it works
- Move to Milestone 2, test movement works
- Move to Milestone 3, test bombs work
- Complete Milestone 4 for full MVP

**Each milestone should be:**
- Fully functional and testable
- Runnable as a standalone state of the game
- Building upon the previous milestone

**Prompt examples:**
- "Implement Milestone 1 - Foundation"
- "Start working on Milestone 2"
- "Let's add the player character (Milestone 2)"
- "Implement the bomb system (Milestone 3)"

