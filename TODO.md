# TODO List - Dungeons of Daggorath Revival

## Sprint 1 ✅ (Complete)
- [x] Fix macOS ARM64 build
- [x] Fix OpenGL initialization crash
- [x] Document feature roadmap
- [x] Set up Python development environment

## Sprint 2 (In Progress)
- [x] Play test and document core mechanics
- [x] Create Python wrapper foundation
- [x] Extend C API for testing
- [x] Clean up deprecation warnings
- [x] Design modding system
- [x] Add bezel support
- [ ] Test and debug input system

## Sprint 3 - Python Engine/Simulation
- [x] Complete domain layer (entities, value objects)
- [ ] Implement application layer (commands, services)
- [ ] Create infrastructure layer (repositories, config)
- [ ] Build presentation layer (terminal, web, API)
- [ ] Create simple demo game
- [ ] Add comprehensive tests

## Sprint 4 - Core Features
- [ ] Implement shop system
- [ ] Add rumors/dialogue system
- [ ] Create "Return of the Wizard" mode
- [ ] Implement color schemes
- [ ] Add text interface for LLMs

## Sprint 5 - Advanced Features
- [ ] **Custom maze generation using MazeBuilder**
  - [ ] Integrate https://github.com/norrisaftcc/MazeBuilder
  - [ ] Allow custom dungeon layouts
  - [ ] Support procedural generation
  - [ ] Enable map editor functionality
- [ ] Add scripting system for speedruns/demos
- [ ] Implement save/load scripts
- [ ] Create multiplayer support
- [ ] Add achievement system

## Sprint 6 - Polish & Release
- [ ] Complete documentation
- [ ] Create installer packages
- [ ] Add tutorial mode
- [ ] Implement accessibility features
- [ ] Beta testing
- [ ] Final release

## Ongoing Tasks
- [ ] Code reviews
- [ ] Performance optimization
- [ ] Bug fixes
- [ ] Community feedback integration

## Nice-to-Have Features
- [ ] VR support
- [ ] Mobile version
- [ ] Steam integration
- [ ] Mod workshop
- [ ] Level editor GUI
- [ ] Replay system
- [ ] Tournament mode

## Themed Editions

### Cyberpunk Edition (William Gibson style)
- [ ] Create cyberpunk game configuration with:
  - [ ] ICE (Intrusion Countermeasures Electronics) as enemies
    - Black ICE (deadly security programs)
    - White ICE (defensive barriers)  
    - Gray ICE (trackers and alarms)
  - [ ] Replace weapons with:
    - Icebreakers (attack programs)
    - Logic bombs
    - Virus payloads
    - Data spikes
  - [ ] Replace armor with:
    - Firewalls
    - Proxy shields
    - Encryption layers
  - [ ] Replace consumables with:
    - Memory buffers (health)
    - CPU boosters (speed)
    - Bandwidth enhancers
  - [ ] Replace magic items with:
    - AI assistants
    - Quantum processors
    - Neural interfaces
  - [ ] Cyberspace maze instead of dungeon
    - Data nodes instead of rooms
    - Network connections instead of corridors
    - System cores instead of treasure
  - [ ] Replace torch system with:
    - Scan radius (visibility)
    - Stealth rating (detection avoidance)
  - [ ] Matrix-style visual theme
    - Green/black terminal aesthetic
    - ASCII art representations
    - Glitch effects
  - [ ] Gibson-esque narrative elements:
    - Corporate datastores to raid
    - AI entities to encounter
    - Black market upgrades
    - Reputation system with hacker collectives

## Technical Debt
- [ ] Replace remaining sprintf calls
- [ ] Modernize C++ code
- [ ] Improve error handling
- [ ] Add logging system
- [ ] Create proper build system (CMake?)

## Research & Experiments
- [ ] AI agent training
- [ ] Difficulty curve analysis
- [ ] Player behavior studies
- [ ] Procedural content generation
- [ ] Network architecture for multiplayer