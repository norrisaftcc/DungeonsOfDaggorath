"""
Value objects - Immutable domain concepts
"""

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Tuple, Optional

class Direction(IntEnum):
    """Cardinal directions in the dungeon"""
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    
    def turn_left(self) -> 'Direction':
        """Return direction after turning left"""
        return Direction((self - 1) % 4)
    
    def turn_right(self) -> 'Direction':
        """Return direction after turning right"""
        return Direction((self + 1) % 4)
    
    def turn_around(self) -> 'Direction':
        """Return opposite direction"""
        return Direction((self + 2) % 4)
    
    def to_delta(self) -> Tuple[int, int]:
        """Convert to row/column delta for movement"""
        deltas = {
            Direction.NORTH: (-1, 0),
            Direction.EAST: (0, 1),
            Direction.SOUTH: (1, 0),
            Direction.WEST: (0, -1)
        }
        return deltas[self]

@dataclass(frozen=True)
class Position:
    """Immutable position in the dungeon"""
    row: int
    col: int
    level: int = 0
    
    def move(self, direction: Direction) -> 'Position':
        """Return new position after moving in direction"""
        delta_row, delta_col = direction.to_delta()
        return Position(
            row=self.row + delta_row,
            col=self.col + delta_col,
            level=self.level
        )
    
    def distance_to(self, other: 'Position') -> float:
        """Manhattan distance to another position"""
        if self.level != other.level:
            return float('inf')
        return abs(self.row - other.row) + abs(self.col - other.col)

@dataclass(frozen=True)
class Health:
    """Immutable health state"""
    current: int
    maximum: int
    
    def __post_init__(self):
        """Validate health values"""
        if self.current < 0:
            object.__setattr__(self, 'current', 0)
        if self.current > self.maximum:
            object.__setattr__(self, 'current', self.maximum)
    
    def take_damage(self, amount: int) -> 'Health':
        """Return new health after taking damage"""
        return Health(
            current=max(0, self.current - amount),
            maximum=self.maximum
        )
    
    def heal(self, amount: int) -> 'Health':
        """Return new health after healing"""
        return Health(
            current=min(self.maximum, self.current + amount),
            maximum=self.maximum
        )
    
    def is_alive(self) -> bool:
        """Check if entity is still alive"""
        return self.current > 0
    
    def percentage(self) -> float:
        """Health as percentage of maximum"""
        return (self.current / self.maximum) * 100 if self.maximum > 0 else 0

@dataclass(frozen=True)
class Light:
    """Light levels for visibility calculations"""
    physical: int = 0  # Normal light
    magical: int = 0   # Magical light (sees through darkness)
    
    def total(self) -> int:
        """Combined light level"""
        return self.physical + self.magical
    
    def decay(self, amount: int = 1) -> 'Light':
        """Return new light after decay"""
        return Light(
            physical=max(0, self.physical - amount),
            magical=max(0, self.magical - amount // 2)  # Magic decays slower
        )

@dataclass(frozen=True)
class Weight:
    """Weight calculation for burden system"""
    value: int
    
    def __add__(self, other: 'Weight') -> 'Weight':
        """Add weights together"""
        return Weight(self.value + other.value)
    
    def __sub__(self, other: 'Weight') -> 'Weight':
        """Subtract weights"""
        return Weight(max(0, self.value - other.value))
    
    def burden_penalty(self) -> int:
        """Calculate movement/combat penalty from weight"""
        return self.value // 10  # Original formula

@dataclass(frozen=True)
class Damage:
    """Damage calculation result"""
    physical: int = 0
    magical: int = 0
    
    def total(self) -> int:
        """Combined damage"""
        return self.physical + self.magical
    
    def apply_defense(self, physical_defense: int, magical_defense: int) -> 'Damage':
        """Return damage after applying defenses"""
        return Damage(
            physical=max(0, self.physical - physical_defense),
            magical=max(0, self.magical - magical_defense)
        )