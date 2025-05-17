"""Item domain entity representing objects in the game."""

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Optional, Any, Dict
from uuid import UUID, uuid4

from .value_objects import Position, Weight, Light


class ItemType(Enum):
    """Categories of items."""
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    QUEST = "quest"
    TREASURE = "treasure"
    TORCH = "torch"  # Special category for torches


@dataclass
class ItemTemplate:
    """Template for creating items."""
    
    name: str
    item_type: ItemType
    value: int
    weight: int
    description: str
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def create_instance(self, position: Position) -> 'Item':
        """Create a new item instance from this template."""
        return Item(
            template=self,
            position=position
        )


@dataclass
class Item:
    """Item instance in the game world."""
    
    id: UUID = field(default_factory=uuid4)
    template: ItemTemplate = None
    position: Optional[Position] = None  # None if in inventory
    is_equipped: bool = False
    is_active: bool = False  # For torches
    condition: float = 1.0  # 1.0 = perfect, 0.0 = broken
    properties: Dict[str, Any] = field(default_factory=dict)
    light_level: Light = field(default_factory=lambda: Light())
    
    @property
    def name(self) -> str:
        """Get item name."""
        return self.template.name
    
    @property
    def item_type(self) -> ItemType:
        """Get item type."""
        return self.template.item_type
    
    @property
    def value(self) -> int:
        """Get item value adjusted for condition."""
        return int(self.template.value * self.condition)
    
    @property
    def weight(self) -> Weight:
        """Get item weight."""
        return Weight(self.template.weight)
    
    @property
    def damage(self) -> int:
        """Get weapon damage if applicable."""
        if self.item_type == ItemType.WEAPON:
            base_damage = self.template.properties.get("damage", 0)
            return int(base_damage * self.condition)
        return 0
    
    @property
    def defense(self) -> int:
        """Get armor defense if applicable."""
        if self.item_type == ItemType.ARMOR:
            base_defense = self.template.properties.get("defense", 0)
            return int(base_defense * self.condition)
        return 0
    
    def use(self) -> Dict[str, Any]:
        """Use the item if it's consumable."""
        if self.item_type == ItemType.CONSUMABLE:
            effect = self.template.properties.copy()
            effect.update(self.properties)
            return effect
        return {}
    
    def equip(self) -> None:
        """Equip the item."""
        if self.item_type in [ItemType.WEAPON, ItemType.ARMOR]:
            self.is_equipped = True
    
    def unequip(self) -> None:
        """Unequip the item."""
        self.is_equipped = False
    
    def degrade(self, amount: float = 0.1) -> None:
        """Reduce item condition."""
        self.condition = max(0.0, self.condition - amount)
    
    def repair(self, amount: float = 0.5) -> None:
        """Repair item condition."""
        self.condition = min(1.0, self.condition + amount)
    
    def activate(self) -> None:
        """Activate item (mainly for torches)."""
        if self.item_type == ItemType.CONSUMABLE and "duration" in self.template.properties:
            self.is_active = True
            # Set light level for torches
            if self.template.name.upper() == "TORCH":
                self.light_level = Light(physical=5, magical=0)


# Standard item templates
TORCH = ItemTemplate("Torch", ItemType.CONSUMABLE, 5, 1, "Provides light", {"duration": 500})
SWORD = ItemTemplate("Sword", ItemType.WEAPON, 50, 5, "A sharp blade", {"damage": 10})
SHIELD = ItemTemplate("Shield", ItemType.ARMOR, 40, 8, "Wooden shield", {"defense": 5})
RING = ItemTemplate("Ring", ItemType.TREASURE, 100, 0, "Golden ring", {"value_multiplier": 2})
SCROLL = ItemTemplate("Scroll", ItemType.CONSUMABLE, 25, 0, "Magic scroll", {"spell": "reveal"})

# Weapons
DAGGER = ItemTemplate("Dagger", ItemType.WEAPON, 20, 2, "Small blade", {"damage": 5})
MACE = ItemTemplate("Mace", ItemType.WEAPON, 60, 10, "Heavy club", {"damage": 15})

# Armor
LEATHER_ARMOR = ItemTemplate("Leather Armor", ItemType.ARMOR, 30, 6, "Light armor", {"defense": 3})
CHAIN_MAIL = ItemTemplate("Chain Mail", ItemType.ARMOR, 80, 15, "Metal rings", {"defense": 8})

# Consumables
FLASK = ItemTemplate("Flask", ItemType.CONSUMABLE, 15, 1, "Healing potion", {"heal": 50})
ELIXIR = ItemTemplate("Elixir", ItemType.CONSUMABLE, 50, 1, "Full restoration", {"heal": 200})

# Original game torches with proper codes
WOOD_TORCH = ItemTemplate("Wood Torch", ItemType.CONSUMABLE, 5, 1, "Basic torch", {"duration": 500, "code": "TO"})
PINE_TORCH = ItemTemplate("Pine Torch", ItemType.CONSUMABLE, 8, 1, "Better torch", {"duration": 800, "code": "TO"})
LUNAR_TORCH = ItemTemplate("Lunar Torch", ItemType.CONSUMABLE, 15, 1, "Magical torch", {"duration": 2000, "code": "TO"})
SOLAR_TORCH = ItemTemplate("Solar Torch", ItemType.CONSUMABLE, 20, 1, "Eternal torch", {"duration": 10000, "code": "TO"})

# All standard item templates
STANDARD_ITEMS = [
    WOOD_TORCH, PINE_TORCH, LUNAR_TORCH, SOLAR_TORCH,
    SWORD, SHIELD, RING, SCROLL,
    DAGGER, MACE, LEATHER_ARMOR, CHAIN_MAIL,
    FLASK, ELIXIR
]

# Update TORCH to be the basic torch
TORCH = WOOD_TORCH