# CLAUDE.md

AI assistant guidance for Dungeons of Daggorath codebase.

## Overview
C++ port of 1982 TRS-80 game. First-person dungeon crawler with text commands and real-time gameplay. Cross-platform: Windows, Unix/Linux, macOS, WebAssembly.

## Quick Reference
- **Build**: See [docs/BUILD.md](docs/BUILD.md)
- **Architecture**: See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)  
- **Commands**: See [docs/COMMANDS.md](docs/COMMANDS.md)

## Key Points
- SDL2/OpenGL based renderer
- Text command parser (MOVE, TURN, GET, etc.)
- Real-time turn-based combat
- Save/load system
- Configuration via `assets/conf/opts.ini`