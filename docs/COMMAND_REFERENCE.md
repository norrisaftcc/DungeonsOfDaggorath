# Command Reference - Implementation Guide

## Movement Commands

### MOVE [direction]
- Default: Move forward one cell
- MOVE BACK: Move backward  
- MOVE LEFT: Strafe left
- MOVE RIGHT: Strafe right
- Time delay: 500ms forward, 700ms backward

### TURN direction
- TURN LEFT: Rotate 90° counter-clockwise
- TURN RIGHT: Rotate 90° clockwise  
- TURN AROUND: Rotate 180°
- Time delay: 370ms

### CLIMB direction
- CLIMB UP: Ascend ladder
- CLIMB DOWN: Descend ladder or hole
- Time delay: 1000ms

## Interaction Commands

### EXAMINE
- List items on floor
- Show backpack contents
- Display current status

### LOOK
- Return to dungeon view after EXAMINE

### GET hand item
- GET RIGHT TORCH: Pick up torch with right hand
- GET LEFT SWORD: Pick up sword with left hand
- Hand must be empty
- Item must be on floor

### PULL hand item
- PULL RIGHT TORCH: Get torch from backpack
- Hand must be empty
- Item must be in backpack

### STOW hand
- Put item from hand into backpack
- STOW RIGHT: Stow right hand item

### DROP hand  
- Drop item to floor
- DROP LEFT: Drop left hand item

## Combat Commands

### ATTACK hand
- Attack with weapon in specified hand
- ATTACK RIGHT: Attack with right hand
- Cooldown: 2 seconds

### USE hand
- Use item (torch, flask, scroll)
- USE RIGHT: Use right hand item

## Special Commands

### REVEAL hand
- Attempt to identify magical item
- Success based on player power

### INCANT word
- Activate ring magic
- INCANT STEEL, INCANT FIRE, etc.

## Meta Commands

### ZSAVE name
- Save game with specified name
- ZSAVE GAME1

### ZLOAD name  
- Load saved game
- ZLOAD GAME1

### RESTART
- Start new game from beginning

## Command Shortcuts
All commands can be abbreviated:
- M = MOVE
- T = TURN  
- G = GET
- A = ATTACK
- etc.

## Implementation Notes
1. Commands are case-insensitive
2. Parse shortest unique prefix
3. Invalid commands show error
4. Some commands have time delays
5. Hand designation required where applicable