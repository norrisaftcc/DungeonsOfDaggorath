"""
Player domain entity - The adventurer exploring the dungeon
"""

from dataclasses import dataclass, field
from typing import Optional, List
from uuid import UUID, uuid4

from .value_objects import Position, Direction, Health, Weight, Light
from .item import Item, ItemType

@dataclass
class Player:
    """Player entity with domain logic"""
    id: UUID = field(default_factory=uuid4)
    position: Position = field(default_factory=lambda: Position(16, 11, 0))
    direction: Direction = Direction.NORTH
    health: Health = field(default_factory=lambda: Health(160, 160))
    
    # Inventory
    left_hand: Optional[Item] = None
    right_hand: Optional[Item] = None
    backpack: List[Item] = field(default_factory=list)
    
    # Heart system
    heart_rate: float = 4.0  # Beats per second
    heart_counter: float = 0.0
    
    # State flags
    is_fainting: bool = False
    faint_duration: float = 0.0
    
    def __post_init__(self):
        """Calculate initial values"""
        self._update_weight()
        self._update_heart_rate()
    
    @property
    def total_weight(self) -> Weight:
        """Calculate total carried weight"""
        weight = Weight(0)
        
        if self.left_hand:
            weight += self.left_hand.weight
        if self.right_hand:
            weight += self.right_hand.weight
            
        for item in self.backpack:
            weight += item.weight
            
        return weight
    
    @property
    def light_level(self) -> Light:
        """Calculate current light level from torches"""
        light = Light()
        
        # Check hands for active torches
        for item in [self.left_hand, self.right_hand]:
            if item and item.item_type == ItemType.TORCH and item.is_active:
                light = Light(
                    physical=light.physical + item.light_level.physical,
                    magical=light.magical + item.light_level.magical
                )
                
        return light
    
    def move(self, direction: Direction) -> Position:
        """Move in specified direction (domain logic only)"""
        if self.is_fainting:
            raise ValueError("Cannot move while fainting")
            
        # Calculate new position
        if direction == self.direction:
            # Moving forward
            new_position = self.position.move(self.direction)
        else:
            # Moving backward/sideways
            new_position = self.position.move(direction)
            
        return new_position
    
    def turn(self, direction: str) -> None:
        """Turn in specified direction"""
        if direction == "LEFT":
            self.direction = self.direction.turn_left()
        elif direction == "RIGHT":
            self.direction = self.direction.turn_right()
        elif direction == "AROUND":
            self.direction = self.direction.turn_around()
        else:
            raise ValueError(f"Invalid turn direction: {direction}")
    
    def take_damage(self, amount: int) -> None:
        """Take damage from an attack"""
        self.health = self.health.take_damage(amount)
        
        if not self.health.is_alive():
            raise PlayerDeathException("Player has died!")
    
    def heal(self, amount: int) -> None:
        """Heal from a flask or spell"""
        self.health = self.health.heal(amount)
    
    def pick_up_item(self, item: Item, hand: str) -> None:
        """Pick up an item into specified hand"""
        if hand == "LEFT":
            if self.left_hand is not None:
                raise ValueError("Left hand is full")
            self.left_hand = item
        elif hand == "RIGHT":
            if self.right_hand is not None:
                raise ValueError("Right hand is full")
            self.right_hand = item
        else:
            raise ValueError(f"Invalid hand: {hand}")
            
        self._update_weight()
        self._update_heart_rate()
    
    def drop_item(self, hand: str) -> Optional[Item]:
        """Drop item from specified hand"""
        item = None
        
        if hand == "LEFT":
            item = self.left_hand
            self.left_hand = None
        elif hand == "RIGHT":
            item = self.right_hand
            self.right_hand = None
        else:
            raise ValueError(f"Invalid hand: {hand}")
            
        self._update_weight()
        self._update_heart_rate()
        
        return item
    
    def stow_item(self, hand: str) -> None:
        """Move item from hand to backpack"""
        if hand == "LEFT":
            if self.left_hand is None:
                raise ValueError("No item in left hand")
            self.backpack.append(self.left_hand)
            self.left_hand = None
        elif hand == "RIGHT":
            if self.right_hand is None:
                raise ValueError("No item in right hand")
            self.backpack.append(self.right_hand)
            self.right_hand = None
        else:
            raise ValueError(f"Invalid hand: {hand}")
            
        self._update_weight()
        self._update_heart_rate()
    
    def pull_item(self, item_name: str, hand: str) -> None:
        """Pull item from backpack to hand"""
        # Find item in backpack
        item_index = None
        for i, item in enumerate(self.backpack):
            if item.name.upper() == item_name.upper():
                item_index = i
                break
                
        if item_index is None:
            raise ValueError(f"Item not found in backpack: {item_name}")
            
        item = self.backpack.pop(item_index)
        
        if hand == "LEFT":
            if self.left_hand is not None:
                raise ValueError("Left hand is full")
            self.left_hand = item
        elif hand == "RIGHT":
            if self.right_hand is not None:
                raise ValueError("Right hand is full")
            self.right_hand = item
        else:
            raise ValueError(f"Invalid hand: {hand}")
            
        self._update_weight()
        self._update_heart_rate()
    
    def use_item(self, hand: str) -> str:
        """Use item in specified hand"""
        if hand == "LEFT":
            item = self.left_hand
        elif hand == "RIGHT":
            item = self.right_hand
        else:
            raise ValueError(f"Invalid hand: {hand}")
            
        if item is None:
            raise ValueError(f"No item in {hand} hand")
            
        # Item-specific use logic would go here
        if item.item_type == ItemType.TORCH:
            if not item.is_active:
                item.activate()
                return f"Lit {item.name}"
            else:
                return f"{item.name} is already lit"
        elif item.item_type == ItemType.FLASK:
            # Heal based on flask type
            heal_amount = item.value
            self.heal(heal_amount)
            # Flask is consumed
            if hand == "LEFT":
                self.left_hand = None
            else:
                self.right_hand = None
            self._update_weight()
            return f"Drank {item.name}, healed {heal_amount} points"
        else:
            return f"Cannot use {item.name}"
    
    def update_heartbeat(self, delta_time: float) -> bool:
        """Update heartbeat counter, returns True if heart beats"""
        self.heart_counter += delta_time
        
        if self.heart_counter >= (1.0 / self.heart_rate):
            self.heart_counter = 0.0
            return True  # Heart beat occurred
            
        return False
    
    def check_fainting(self) -> None:
        """Check if player should faint from exhaustion"""
        # Original game: faint if heart rate too high for too long
        if self.heart_rate > 8.0:  # Threshold
            self.is_fainting = True
            self.faint_duration = 5.0  # 5 seconds
    
    def update_faint(self, delta_time: float) -> None:
        """Update fainting state"""
        if self.is_fainting:
            self.faint_duration -= delta_time
            if self.faint_duration <= 0:
                self.is_fainting = False
    
    def _update_weight(self) -> None:
        """Recalculate weight-based values"""
        # Weight affects heart rate
        self._update_heart_rate()
    
    def _update_heart_rate(self) -> None:
        """Recalculate heart rate based on activity and weight"""
        base_rate = 4.0
        
        # Weight penalty
        weight_penalty = self.total_weight.burden_penalty() * 0.5
        
        # Activity penalty would be added by movement/combat services
        
        self.heart_rate = base_rate + weight_penalty
        
        # Check for fainting
        self.check_fainting()

class PlayerDeathException(Exception):
    """Raised when player dies"""
    pass