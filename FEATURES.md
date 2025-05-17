# Game Mode Features

## Hardcore Mode (Classic 1982 Experience)
- Preserves original gameplay exactly as designed
- Full heartbeat stress system with carrying penalties  
- No visual aids or modern conveniences
- Original sound-only creature detection
- Classic ZSAVE system only
- ONE autosave per dungeon level (mercy checkpoint)
- Permadeath option
- Original RNG behavior (including "unfair" moments)
- No auto-mapping
- No on-screen stats beyond heartbeat

## Modern Mode (Quality of Life)
- Auto-map that reveals as you explore (fog of war)
- Visual health/stamina indicators
- Save anywhere functionality
- Optional creature proximity indicators
- Inventory management improvements
- Reduced heartbeat penalties
- More forgiving RNG
- Tutorial hints for new players

## Return of the Wizard Mode (Sequel Campaign)
- Alternate campaign with new story
- Different visual theme (darker color scheme)
- Future expansions planned:
  - New dungeon layouts
  - Additional creatures
  - Wizard-specific mechanics
  - Extended ending

## New Features (All Modes)
- **Shop System**: Trade items between dungeon levels
  - Buy/sell weapons, shields, torches, flasks
  - Prices based on item rarity and dungeon depth
  - Special items only available in shop
- **Rumors System**: Learn about the dungeon
  - NPCs share hints about upcoming levels
  - Lore about the Wizard of Daggorath
  - Warnings about specific creatures
  - Optional quest hints
  - Special rumors in Wizard mode about his return

## Planned Sprint 1 Goals
1. Play original to document core mechanics
2. Add WebAssembly API tests
3. Implement mode selection at startup
4. Begin Python wrapper development
5. Design shop and rumors system architecture

## Configuration
Mode selection via command line:
- `--hardcore` or `-h`: Classic mode (Gus approved!)
- `--modern` or `-m`: Modern mode with QoL improvements
- `--wizard` or `-w`: Return of the Wizard campaign
- Default: Modern mode in original campaign
- Mode stored in opts.ini as:
  - `gameMode=[HARDCORE|MODERN]`
  - `campaign=[ORIGINAL|WIZARD]`