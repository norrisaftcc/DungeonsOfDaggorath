# 6809 Assembly to Python Translation Guide

## Understanding the Original Architecture

### Memory Map (Original CoCo)
```
$0000-$00FF - Direct Page (fast access)
$0100-$05FF - System variables
$0600-$3FFF - Program code
$4000-$5FFF - Screen memory
$6000-$7FFF - Game data
```

### Key 6809 Patterns to Python

1. **Direct Page Variables**
   ```assembly
   ; 6809 - Fast zero-page access
   PLRBLK  RMB     16      ; Player block
   CCBLND  RMB     32*14   ; Creature blocks
   ```
   ```python
   # Python equivalent
   class GameState:
       def __init__(self):
           self.player = PlayerBlock()
           self.creatures = [CreatureBlock() for _ in range(32)]
   ```

2. **Task Control Blocks**
   ```assembly
   ; Original used linked list
   TCB     FCB     TYPE    ; Task type
           FDB     NEXT    ; Next TCB pointer
           FDB     TIME    ; Execution time
   ```
   ```python
   # Python version
   class Task:
       def __init__(self, task_type, frequency):
           self.type = task_type
           self.frequency = frequency
           self.next_time = 0
   ```

3. **Interrupt-Driven Timing**
   ```assembly
   ; 6809 used hardware interrupts
   IRQ     LDA     TIMER
           DECA
           STA     TIMER
           BEQ     DOTASK
           RTI
   ```
   ```python
   # Python uses event loop
   def game_loop(self):
       clock = pygame.time.Clock()
       while self.running:
           delta = clock.tick(60)  # 60 FPS
           self.scheduler.update(delta)
   ```

4. **Creature AI Logic**
   ```assembly
   ; Simple state machine
   CMOVE   LDA     CCBLND,X  ; Get creature state
           CMPA    #DEAD
           BEQ     CMEXIT
           JSR     FINDPLR   ; Pathfinding
   ```
   ```python
   # Object-oriented approach
   class Creature:
       def update(self):
           if self.state == CreatureState.DEAD:
               return
           self.find_path_to_player()
           self.move()
   ```

5. **Random Number Generator**
   ```assembly
   ; Linear Feedback Shift Register
   RANDOM  ROL     SEED
           ROL     SEED+1
           ROL     SEED+2
           BCC     RAND1
           EOR     #$B4      ; Polynomial
   RAND1   RTS
   ```
   ```python
   # Preserve original RNG for compatibility
   class RNG:
       def __init__(self, seed):
           self.seed = seed
           
       def next(self):
           # LFSR implementation
           bit = ((self.seed >> 0) ^ 
                  (self.seed >> 2) ^ 
                  (self.seed >> 3) ^ 
                  (self.seed >> 5)) & 1
           self.seed = (self.seed >> 1) | (bit << 15)
           return self.seed & 0xFF
   ```

### Critical Game Mechanics

1. **Heartbeat System**
   - Originally tied to 60Hz interrupt
   - Heart rate affects all timing
   - Must preserve exact feel

2. **Line of Sight**
   - Used efficient bit manipulation
   - Ray casting in 4 directions
   - Critical for creature behavior

3. **Sound Timing**
   - Synchronized with game events
   - Used CoCo's DAC directly
   - Need sample-accurate playback

4. **Combat Calculations**
   - Fixed-point arithmetic
   - Damage tables in ROM
   - Predictable outcomes

### Translation Challenges

1. **Timing Precision**
   - 6809 was cycle-accurate
   - Python has GC pauses
   - Use fixed timestep

2. **Memory Layout**
   - Assembly used absolute addresses
   - Python needs object references
   - Maintain data locality

3. **Bit Manipulation**
   - Assembly excelled at this
   - Python is slower
   - Use numpy for performance

### Best Practices

1. Keep original algorithms intact
2. Document magic numbers
3. Preserve timing relationships
4. Test against C++ version
5. Profile performance critical sections