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

# 2nd task: Dynablaster overview

Analyse which parts of the package we can use to implement a bomberman-style game and summarize these in this section.

