# Dungeons of Daggorath - Gameplay Notes

## Session 1: Initial Exploration
**Date**: Sprint 2, Day 1
**Player**: Gus Thompson

### Starting Sequence
```
EXAMINE
LOOK
PULL RIGHT TORCH
USE RIGHT
PULL LEFT SWORD
TURN LEFT
MOVE
MOVE
MOVE
MOVE
```

### Observations
1. **Heartbeat System**
   - Heart rate increases with movement
   - Carrying heavy items increases rate faster
   - Must rest periodically or collapse
   - Sound is critical feedback mechanism

2. **Combat Mechanics**
   - ATTACK with equipped weapon
   - Timing crucial - can't attack too rapidly
   - Different creatures have different speeds
   - Shield blocks some damage automatically

3. **Light Management**
   - Torches burn out over time
   - Pine < Lunar < Solar torch brightness
   - Darkness = death (creatures attack freely)
   - Must manage torch inventory carefully

4. **Sound Design**
   - Each creature has distinct sound
   - Volume indicates proximity
   - Stereo positioning shows direction
   - Critical for survival in darkness

### Bugs Found
- [ ] Sound sometimes cuts out after save/load
- [ ] Creature movement occasionally stutters
- [ ] Text input accepts invalid commands without error
- [ ] Torch countdown timer seems inconsistent

### Enhancement Ideas
- Visual heartbeat indicator for Modern mode
- Auto-equip next torch when current burns out
- Minimap showing explored areas
- Creature bestiary in menu

## Session 2: Combat & Items

### Advanced Heartbeat Mechanics
- Base rate: 4 beats/second (resting)
- Movement: +2 beats/second
- Combat: +3 beats/second
- Carrying weight formula: rate += (weight / 10)
- Fainting threshold: 180 BPM for >10 seconds
- Death: 250 BPM or fainting while creature present

### Item Types Discovered
1. **Weapons**
   - Wooden Sword: Damage 8, Weight 15
   - Iron Sword: Damage 16, Weight 30
   - Elvish Sword: Damage 32, Weight 20

2. **Shields**  
   - Leather Shield: Block 10%, Weight 25
   - Bronze Shield: Block 20%, Weight 40
   - Mithril Shield: Block 30%, Weight 25

3. **Torches**
   - Pine Torch: 3 min, Radius 2
   - Lunar Torch: 5 min, Radius 3  
   - Solar Torch: 8 min, Radius 4

### Combat Strategy
- Listen for creature sounds
- Turn to face before attacking
- Attack timing: 1 hit per 2 seconds max
- Retreat if heartbeat >150 BPM
- Use walls to limit creature approach angles