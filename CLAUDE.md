# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a C++ port of the 1982 game "Dungeons of Daggorath" originally created for the TRS-80 Color Computer. It's a first-person dungeon crawler with text-based commands and real-time gameplay. The project supports multiple platforms including Windows, Unix/Linux, macOS, and web browsers via WebAssembly.

## Build Commands

### Native Build (Unix/Linux/macOS)
```bash
make            # Build native executable
make clean      # Clean build artifacts
```

### Windows Build
Uses Dev-C++ project file (`src/dod.dev`) or MinGW:
```bash
make            # Creates dod.exe
```

### WebAssembly Build (for web browsers)
```bash
cd src
emcc -o ../docs/index.html $(OBJECTS) -s USE_SDL=2 -O3 -s USE_SDL_MIXER=2 -s USE_REGAL=1 -s ALLOW_MEMORY_GROWTH=1 --preload-file ../assets@/ -s FULL_ES2=1 -s ASYNCIFY -s WASM=1 -s EXIT_RUNTIME=1 --shell-file standalone.html
```

## Architecture

### Core Components
- **Game Logic**: `dodgame.cpp/h` - Central game state and mechanics
- **Command Parser**: `parser.cpp/h` - Processes text commands (MOVE, TURN, GET, etc.)
- **Player System**: `player.cpp/h` - Player state, health, inventory
- **Creature System**: `creature.cpp/h` - Enemies and AI
- **Dungeon**: `dungeon.cpp/h` - Level layout and map generation
- **Objects**: `object.cpp/h` - Items, weapons, armor
- **Rendering**: `viewer.cpp/h` - Display system using SDL2/OpenGL
- **OS Abstraction**: `oslink.cpp/h` - Platform-specific code
- **Scheduler**: `sched.cpp/h` - Game timing and turn system

### Dependencies
- SDL2 (cross-platform multimedia)
- SDL2_mixer (audio)
- OpenGL (graphics)
- C++11 standard

### Key Game Files
- `assets/conf/opts.ini` - Game configuration (speed, screen size, audio)
- `assets/saved/game.dod` - Save game data
- `assets/sound/*.wav` - Sound effects (16 files)

### Build Architecture
- Makefiles use conditional compilation for different platforms
- WebAssembly builds use Emscripten with special flags for memory growth and file preloading
- Builds generate either:
  - Native executable: `dod` (Unix/macOS) or `dod.exe` (Windows)
  - Web version: `docs/index.html` with accompanying .js and .wasm files

## Development Notes

### Command System
The game uses a text-based command system. Commands include:
- Movement: MOVE (M), TURN (T), CLIMB (C)
- Interaction: GET (G), DROP (D), USE (U), ATTACK (A)
- Inventory: EXAMINE (E), PULL (P), STOW (S)
- Magic: INCANT (I), REVEAL (R)
- Meta: ZSAVE (ZS), ZLOAD (ZL), RESTART

### Cheat System
Debug/cheat commands available through SETCHEAT:
- NONE, ITEMS, INVULNERABLE, CRTSCALE, REVEAL, RING, TORCH

### Configuration
Game behavior controlled via `opts.ini`:
- creatureSpeed, turnDelay, moveDelay
- volumeLevel, keylayout
- screenWidth, fullScreen, graphicsMode