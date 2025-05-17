"""
Game constants and data structures for Dungeons of Daggorath
Based on Sprint 2 gameplay analysis
"""

from dataclasses import dataclass
from enum import IntEnum
from typing import Dict

class ItemType(IntEnum):
    """Item type classifications"""
    WEAPON = 1
    SHIELD = 2
    TORCH = 3
    FLASK = 4
    SCROLL = 5
    RING = 6

@dataclass
class ItemStats:
    """Statistics for game items"""
    name: str
    item_type: ItemType
    weight: int
    value: int  # Damage for weapons, duration for torches, etc.
    special: str = ""

# Item database based on gameplay testing
ITEMS: Dict[str, ItemStats] = {
    # Weapons
    "WOODEN_SWORD": ItemStats("Wooden Sword", ItemType.WEAPON, 15, 8),
    "IRON_SWORD": ItemStats("Iron Sword", ItemType.WEAPON, 30, 16),
    "ELVISH_SWORD": ItemStats("Elvish Sword", ItemType.WEAPON, 20, 32),
    
    # Shields
    "LEATHER_SHIELD": ItemStats("Leather Shield", ItemType.SHIELD, 25, 10),
    "BRONZE_SHIELD": ItemStats("Bronze Shield", ItemType.SHIELD, 40, 20),
    "MITHRIL_SHIELD": ItemStats("Mithril Shield", ItemType.SHIELD, 25, 30),
    
    # Torches (value = duration in seconds)
    "PINE_TORCH": ItemStats("Pine Torch", ItemType.TORCH, 10, 180),
    "LUNAR_TORCH": ItemStats("Lunar Torch", ItemType.TORCH, 8, 300),
    "SOLAR_TORCH": ItemStats("Solar Torch", ItemType.TORCH, 6, 480),
    
    # Flasks
    "HALE_FLASK": ItemStats("Hale Flask", ItemType.FLASK, 5, 25, "Restore health"),
    "ABYE_FLASK": ItemStats("Abye Flask", ItemType.FLASK, 5, 50, "Full restore"),
    "THEWS_FLASK": ItemStats("Thews Flask", ItemType.FLASK, 5, 100, "Increase power"),
}

# Game mechanics constants
class HeartbeatRates:
    """Heart rate modifiers (beats per minute)"""
    BASE_RATE = 60  # Resting
    MOVEMENT = 120  # Walking
    COMBAT = 180    # Fighting
    WEIGHT_FACTOR = 6  # BPM per 10 weight units
    
    FAINT_THRESHOLD = 180
    FAINT_DURATION = 10  # seconds
    DEATH_THRESHOLD = 250

class CombatMechanics:
    """Combat timing and damage"""
    ATTACK_COOLDOWN = 2.0  # seconds
    CREATURE_DAMAGE_MULT = {
        1: 0.5,  # Level 1 creatures
        2: 1.0,  # Level 2 creatures
        3: 1.5,  # Level 3 creatures
        4: 2.0,  # Level 4 creatures
        5: 3.0,  # Level 5 creatures (Wizard)
    }

class TorchMechanics:
    """Torch lighting ranges"""
    TORCH_RADIUS = {
        "PINE": 2,
        "LUNAR": 3,
        "SOLAR": 4,
    }
    
class MovementCosts:
    """Movement and turn delays (milliseconds)"""
    MOVE_FORWARD = 500
    MOVE_BACKWARD = 700
    TURN = 370
    CLIMB = 1000