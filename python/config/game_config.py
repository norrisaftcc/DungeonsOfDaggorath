"""
Game configuration system - exposing internal values for modding
Based on Michael Spencer's documentation
"""

from dataclasses import dataclass, field
from typing import Dict, List
import json

@dataclass
class PlayerConfig:
    """Player starting values and limits"""
    starting_power: int = 160
    starting_position: tuple = (16, 11)  # row, col
    max_power: int = 32767
    damage_per_move: int = 1
    damage_per_attack: int = 2
    weight_penalty_factor: float = 0.1

@dataclass
class CreatureStats:
    """Individual creature configuration"""
    name: str
    power: int
    move_speed: int  # milliseconds between moves
    attack_speed: int  # milliseconds between attacks
    magic_offense: int  # 0-199 percentage
    magic_defense: int  # 0-199 percentage  
    phys_offense: int  # 0-199 percentage
    phys_defense: int  # 0-199 percentage
    damage: int
    sound_id: int

@dataclass
class ObjectStats:
    """Object/item configuration"""
    name: str
    obj_type: str  # TORCH, SWORD, SHIELD, FLASK, SCROLL, RING
    reveal_power: int  # Min power to reveal true nature
    weight: int
    value: int  # Damage for weapons, duration for torches, etc
    magic_offense: int
    magic_defense: int
    phys_offense: int
    phys_defense: int

@dataclass
class TorchConfig:
    """Torch specific settings"""
    name: str
    burn_time: int  # seconds
    phys_light: int  # Physical light radius
    magic_light: int  # Magical light radius
    decay_rate: float  # Light decay per second

@dataclass
class GameConfig:
    """Master game configuration"""
    player: PlayerConfig = field(default_factory=PlayerConfig)
    creatures: Dict[str, CreatureStats] = field(default_factory=dict)
    objects: Dict[str, ObjectStats] = field(default_factory=dict)
    torches: Dict[str, TorchConfig] = field(default_factory=dict)
    
    # Global settings
    heartbeat_base_rate: int = 60  # BPM
    faint_threshold: int = 180
    death_threshold: int = 250
    
    # Combat settings
    attack_probability_scale: float = 1.0
    damage_scale: float = 1.0
    
    @classmethod
    def load_from_json(cls, filename: str) -> 'GameConfig':
        """Load configuration from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        config = cls()
        
        # Load player config
        if 'player' in data:
            config.player = PlayerConfig(**data['player'])
            
        # Load creatures
        if 'creatures' in data:
            for name, stats in data['creatures'].items():
                config.creatures[name] = CreatureStats(**stats)
                
        # Load objects
        if 'objects' in data:
            for name, stats in data['objects'].items():
                config.objects[name] = ObjectStats(**stats)
                
        # Load torches
        if 'torches' in data:
            for name, stats in data['torches'].items():
                config.torches[name] = TorchConfig(**stats)
                
        # Load global settings
        for key in ['heartbeat_base_rate', 'faint_threshold', 'death_threshold',
                   'attack_probability_scale', 'damage_scale']:
            if key in data:
                setattr(config, key, data[key])
                
        return config
    
    def save_to_json(self, filename: str):
        """Save configuration to JSON file"""
        data = {
            'player': self.player.__dict__,
            'creatures': {name: creature.__dict__ 
                         for name, creature in self.creatures.items()},
            'objects': {name: obj.__dict__ 
                       for name, obj in self.objects.items()},
            'torches': {name: torch.__dict__ 
                       for name, torch in self.torches.items()},
            'heartbeat_base_rate': self.heartbeat_base_rate,
            'faint_threshold': self.faint_threshold,
            'death_threshold': self.death_threshold,
            'attack_probability_scale': self.attack_probability_scale,
            'damage_scale': self.damage_scale
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

# Default configuration - matches original game
DEFAULT_CONFIG = GameConfig()

# Original creature stats from assembly
DEFAULT_CONFIG.creatures = {
    "SPIDER": CreatureStats("Spider", 32, 1500, 2000, 0, 100, 100, 0, 8, 0),
    "VIPER": CreatureStats("Viper", 64, 1200, 1800, 50, 50, 50, 50, 16, 1),
    "GIANT": CreatureStats("Giant", 128, 1800, 2500, 0, 50, 150, 100, 32, 2),
    "BLOB": CreatureStats("Blob", 256, 2000, 3000, 100, 150, 50, 0, 64, 3),
    "KNIGHT": CreatureStats("Knight", 512, 800, 1200, 50, 100, 100, 150, 128, 4),
    "WIZARD": CreatureStats("Wizard", 32767, 500, 800, 150, 199, 100, 100, 256, 5)
}

# Original object stats
DEFAULT_CONFIG.objects = {
    "WOODEN_SWORD": ObjectStats("Wooden Sword", "SWORD", 0, 15, 8, 0, 0, 100, 0),
    "IRON_SWORD": ObjectStats("Iron Sword", "SWORD", 100, 30, 16, 0, 0, 150, 0),
    "ELVISH_SWORD": ObjectStats("Elvish Sword", "SWORD", 280, 20, 32, 100, 100, 100, 100),
    
    "LEATHER_SHIELD": ObjectStats("Leather Shield", "SHIELD", 0, 25, 10, 0, 50, 0, 100),
    "BRONZE_SHIELD": ObjectStats("Bronze Shield", "SHIELD", 125, 40, 20, 0, 100, 0, 150),
    "MITHRIL_SHIELD": ObjectStats("Mithril Shield", "SHIELD", 300, 25, 30, 100, 150, 100, 150),
}

# Original torch stats
DEFAULT_CONFIG.torches = {
    "PINE": TorchConfig("Pine Torch", 180, 3, 0, 0.01),
    "LUNAR": TorchConfig("Lunar Torch", 300, 5, 3, 0.008),
    "SOLAR": TorchConfig("Solar Torch", 480, 7, 5, 0.005)
}