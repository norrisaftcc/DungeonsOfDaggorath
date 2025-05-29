# Architecture Overview

## Core Components
- **dodgame.cpp/h**: Central game state and mechanics
- **parser.cpp/h**: Text command processing
- **player.cpp/h**: Player state, health, inventory
- **creature.cpp/h**: Enemy AI and behavior
- **dungeon.cpp/h**: Level layout and generation
- **object.cpp/h**: Items, weapons, armor
- **viewer.cpp/h**: SDL2/OpenGL rendering
- **oslink.cpp/h**: Platform abstraction layer
- **sched.cpp/h**: Game timing and turn system
- **rng.cpp/h**: Random number generation

## Key Files
- `assets/conf/opts.ini`: Game configuration
- `assets/saved/game.dod`: Save data
- `assets/sound/*.wav`: 16 sound effects

## Configuration (opts.ini)
- Speed: creatureSpeed, turnDelay, moveDelay
- Audio: volumeLevel
- Display: screenWidth, fullScreen, graphicsMode
- Input: keylayout