"""
Player module - Port of HUMAN.ASM/player.cpp
Handles player state, movement, and actions
"""

from enum import IntEnum
from dataclasses import dataclass
from typing import Optional

class Direction(IntEnum):
    """Player facing direction"""
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

@dataclass
class PlayerBlock:
    """
    Player state block - equivalent to PLRBLK in assembly
    Original was 16 bytes in zero page for fast access
    """
    # Position
    row: int = 16      # PROW - Starting position
    col: int = 11      # PCOL
    
    # Stats
    power: int = 160   # PPOW - Health/strength
    damage: int = 0    # PDAM - Current damage
    weight: int = 0    # POBJWT - Carried weight
    
    # Equipment
    left_hand: int = -1   # PLHAND - Object index
    right_hand: int = -1  # PRHAND - Object index
    
    # State
    direction: Direction = Direction.NORTH  # PDIR
    torch_id: int = -1   # PTORCH - Active torch
    
    # Heart system
    heart_rate: int = 4   # HEARTR - Base heart rate
    heart_counter: int = 4  # HEARTC - Countdown
    heart_state: int = 0   # HEARTS - Animation state
    heartbeat_on: bool = True  # HBEATF
    
    # Light levels
    right_light: int = 0  # PRLITE
    left_light: int = 0   # PMLITE
    
    # Other
    faint_counter: int = 0  # FAINT
    backpack_end: int = 0   # BAGPTR

class Player:
    """
    Player controller - handles all player actions
    Port of player.cpp / HUMAN.ASM
    """
    
    def __init__(self):
        self.state = PlayerBlock()
        self.turning = False
        self.moving = False
        
    def update(self, delta_time: float):
        """Update player state each frame"""
        # Update heartbeat
        if self.state.heartbeat_on:
            self.update_heartbeat(delta_time)
            
        # Update fainting
        if self.state.faint_counter > 0:
            self.state.faint_counter -= delta_time
            
    def update_heartbeat(self, delta_time: float):
        """
        Update heart counter and trigger heartbeat
        Original used interrupt-driven timing
        """
        self.state.heart_counter -= delta_time
        
        if self.state.heart_counter <= 0:
            # Reset counter
            self.state.heart_counter = self.state.heart_rate
            
            # Trigger heartbeat sound and animation
            self.trigger_heartbeat()
            
    def trigger_heartbeat(self):
        """Play heartbeat sound and update display"""
        # Toggle heart animation state
        self.state.heart_state = 1 - self.state.heart_state
        
        # This would trigger sound in the audio system
        # audio.play_heartbeat(self.state.heart_state)
        
    def calculate_heart_rate(self):
        """
        Calculate heart rate based on activity and weight
        Original algorithm from assembly
        """
        base_rate = 4  # Base heartbeats per second
        
        # Add weight penalty
        weight_penalty = self.state.weight // 10
        
        # Add activity penalty (if moving/fighting)
        activity_penalty = 2 if self.moving else 0
        
        self.state.heart_rate = max(1, base_rate - weight_penalty - activity_penalty)
        
    def turn(self, direction: str):
        """Turn player left, right, or around"""
        if direction == "LEFT":
            self.state.direction = Direction((self.state.direction - 1) % 4)
        elif direction == "RIGHT":
            self.state.direction = Direction((self.state.direction + 1) % 4)
        elif direction == "AROUND":
            self.state.direction = Direction((self.state.direction + 2) % 4)
            
    def move(self, backward: bool = False):
        """Move player forward or backward"""
        # Calculate new position based on direction
        delta_row, delta_col = self._get_direction_delta()
        
        if backward:
            delta_row = -delta_row
            delta_col = -delta_col
            
        new_row = self.state.row + delta_row
        new_col = self.state.col + delta_col
        
        # Check collision with dungeon walls
        # if dungeon.is_valid_position(new_row, new_col):
        #     self.state.row = new_row
        #     self.state.col = new_col
        #     self.moving = True
        
    def _get_direction_delta(self):
        """Get row/col delta for current direction"""
        deltas = {
            Direction.NORTH: (-1, 0),
            Direction.EAST: (0, 1),
            Direction.SOUTH: (1, 0),
            Direction.WEST: (0, -1)
        }
        return deltas[self.state.direction]
        
    def attack(self, hand: str):
        """Attack with weapon in specified hand"""
        obj_id = self.state.right_hand if hand == "RIGHT" else self.state.left_hand
        
        if obj_id < 0:
            return  # No weapon in hand
            
        # Get weapon stats and calculate damage
        # weapon = object_manager.get_object(obj_id)
        # damage = weapon.damage * self.state.power // 100
        
    def use_item(self, hand: str):
        """Use item in specified hand (torch, flask, etc)"""
        obj_id = self.state.right_hand if hand == "RIGHT" else self.state.left_hand
        
        if obj_id < 0:
            return
            
        # Handle different item types
        # item = object_manager.get_object(obj_id)
        # item.use(self)
        
    def get_item(self, hand: str, item_name: str):
        """Pick up item from floor"""
        # Find item on current position
        # obj_id = object_manager.find_at_position(self.state.row, self.state.col, item_name)
        pass
        
    def calculate_damage(self):
        """Calculate total damage from all sources"""
        # This would include damage from creatures, environment, etc
        pass