"""Creature domain entity representing monsters in the game."""

from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid4

from .value_objects import Position, Health


@dataclass
class CreatureType:
    """Type of creature with base stats."""
    
    name: str
    base_health: int
    damage: int
    defense: int
    speed: int
    description: str
    sound: Optional[str] = None
    
    def create_instance(self, position: Position, level: int = 0) -> 'Creature':
        """Create a new creature instance of this type."""
        health_multiplier = 1 + (level * 0.1)  # 10% health increase per level
        max_health = int(self.base_health * health_multiplier)
        
        return Creature(
            creature_type=self,
            position=position,
            health=Health(max_health, max_health),
            level=level
        )


@dataclass
class Creature:
    """Creature instance in the game world."""
    
    id: UUID = field(default_factory=uuid4)
    creature_type: CreatureType = field(default_factory=lambda: SPIDER)
    position: Position = field(default_factory=lambda: Position(0, 0, 0))
    health: Health = field(default_factory=lambda: Health(10, 10))
    level: int = 0
    is_active: bool = True
    
    @property
    def name(self) -> str:
        """Get creature name."""
        return self.creature_type.name
    
    @property
    def damage(self) -> int:
        """Get creature damage."""
        return self.creature_type.damage + self.level
    
    @property
    def defense(self) -> int:
        """Get creature defense."""
        return self.creature_type.defense + self.level
    
    @property
    def speed(self) -> int:
        """Get creature speed."""
        return self.creature_type.speed
    
    def take_damage(self, amount: int) -> None:
        """Apply damage to creature."""
        self.health = self.health.take_damage(amount)
        if self.health.current <= 0:
            self.is_active = False
    
    def heal(self, amount: int) -> None:
        """Heal creature."""
        self.health = self.health.heal(amount)
    
    def move_to(self, position: Position) -> None:
        """Move creature to new position."""
        self.position = position


# Standard creature types
SPIDER = CreatureType("Spider", 10, 5, 2, 3, "A small venomous spider", "00_squeak.wav")
VIPER = CreatureType("Viper", 15, 8, 3, 4, "A deadly serpent", "01_rattle.wav")
SCORPION = CreatureType("Scorpion", 20, 10, 4, 3, "An armored arachnid", "02_growl.wav")
KNIGHT = CreatureType("Knight", 40, 15, 8, 2, "An undead warrior", "04_klank.wav")
BLOB = CreatureType("Blob", 30, 12, 5, 1, "A gelatinous creature", "0C_gluglg.wav")
WRAITH = CreatureType("Wraith", 25, 18, 2, 5, "A ghostly apparition", "08_pssht.wav")
WIZARD = CreatureType("Wizard", 50, 20, 10, 3, "The evil sorcerer", "0D_phaser.wav")

# All standard creature types
STANDARD_CREATURES = [SPIDER, VIPER, SCORPION, KNIGHT, BLOB, WRAITH, WIZARD]