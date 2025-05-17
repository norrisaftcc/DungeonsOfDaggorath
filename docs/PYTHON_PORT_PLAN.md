# Python Port Plan - Reading the Code

## Sprint 3: Python Port from Source Analysis

### Team Approach
- **Gus**: Read the 6809 assembly (original) and explain algorithms  
- **Maya**: Map C++ structures to Python classes
- **Rahul**: Implement Python version with modern patterns
- **Chen**: Design modular, extensible architecture

### Analysis Strategy

1. **Start with Core Data Structures**
   - Player state (PLRBLK in assembly)
   - Creature blocks (CCBLND)
   - Object control blocks (OCBLND)
   - Dungeon layout (MAZLND)

2. **Map Game Loop**
   - Scheduler (SCHED)
   - Task system (TCB)
   - Input processing
   - Display updates

3. **Core Systems to Port**
   ```
   Assembly File -> C++ Class -> Python Module
   HUMAN.ASM    -> player.cpp -> player.py
   CRETUR.ASM   -> creature.cpp -> creature.py
   OBJECT.ASM   -> object.cpp -> object.py
   DGNGEN.ASM   -> dungeon.cpp -> dungeon.py
   VIEWER.ASM   -> viewer.cpp -> viewer.py
   SCHED.ASM    -> sched.cpp -> scheduler.py
   ```

4. **Key Algorithms**
   - Random number generator (original used LFSR)
   - Line of sight calculations
   - Creature AI pathfinding
   - Combat calculations
   - Heartbeat timing

### Python Architecture Goals

```python
# Modern, Pythonic design
class DaggorathGame:
    def __init__(self):
        self.player = Player()
        self.dungeon = Dungeon()
        self.creatures = CreatureManager()
        self.objects = ObjectManager()
        self.scheduler = Scheduler()
        self.viewer = Viewer()
        
    def run(self):
        """Main game loop"""
        while not self.game_over:
            self.scheduler.tick()
            self.process_input()
            self.update_state()
            self.render()
```

### Challenges

1. **Timing System**
   - Original used interrupt-driven timing
   - Python needs event-based approach
   - Preserve original game feel

2. **Memory Layout**
   - Assembly had direct memory access
   - Need to translate to objects/arrays

3. **Sound System**
   - Original used CoCo sound hardware
   - Map to pygame or similar

4. **Graphics**
   - Original used character graphics
   - Could use pygame, curses, or web canvas

### Documentation Process

For each module:
1. Read assembly source
2. Understand C++ port
3. Document algorithm
4. Design Python version
5. Implement with tests

### Example: Heartbeat System

```assembly
; Original 6809
HEART   LDA     HEARTC
        DECA
        STA     HEARTC
        BNE     HRTOUT
        ; Make heartbeat sound
```

```cpp
// C++ version
if (player.HEARTC-- == 0) {
    player.HEARTC = player.HEARTR;
    Mix_PlayChannel(/*...*/);
}
```

```python
# Python version
class Player:
    def update_heartbeat(self, delta_time):
        self.heart_counter -= delta_time
        if self.heart_counter <= 0:
            self.heart_counter = self.heart_rate
            self.play_heartbeat_sound()
```

### Next Steps

1. Set up Python project structure
2. Create base classes
3. Port one system at a time
4. Test against C++ version
5. Add modern enhancements

### Resources Needed

- [ ] Assembly code documentation
- [ ] C++ code walkthrough
- [ ] Test cases from original
- [ ] Sound/graphics assets
- [ ] Timing specifications