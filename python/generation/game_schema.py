"""
Game Generation Schema - For LLM-based game creation
Defines the format for procedurally generated Daggorath-style games
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

@dataclass
class CreatureDefinition:
    """Define a creature type for the game"""
    id: str
    name: str
    description: str
    power: int
    speed: int  # milliseconds between moves
    attack_speed: int
    magic_offense: int  # 0-200
    magic_defense: int  # 0-200
    phys_offense: int   # 0-200
    phys_defense: int   # 0-200
    damage: int
    sound_description: str  # For LLM to generate sound
    behavior_pattern: str   # "aggressive", "defensive", "patrol", etc.
    
@dataclass
class ItemDefinition:
    """Define an item type"""
    id: str
    name: str
    description: str
    item_type: str  # "weapon", "shield", "torch", "flask", "scroll", "ring"
    weight: int
    value: int  # Damage for weapons, duration for torches, etc.
    magic_bonus: int
    physical_bonus: int
    special_ability: Optional[str] = None
    reveal_requirement: int = 0  # Power needed to identify

@dataclass
class RoomTheme:
    """Define room/level themes"""
    id: str
    name: str
    description: str
    wall_description: str
    floor_description: str
    ambient_sounds: List[str]
    lighting_modifier: float = 1.0
    danger_level: int = 1  # 1-5

@dataclass
class MazeConfig:
    """Maze generation parameters"""
    width: int
    height: int
    algorithm: str  # "recursive_backtrack", "prims", "wilsons", etc.
    room_density: float = 0.3  # Percentage of maze that's rooms vs corridors
    secret_passages: int = 0
    loops: int = 0  # Additional connections for multiple paths
    
@dataclass
class GameNarrative:
    """Story elements"""
    title: str
    setting: str  # "medieval", "sci-fi", "horror", etc.
    intro_text: str
    victory_text: str
    death_text: str
    level_descriptions: List[str]
    boss_encounter_text: str
    item_lore: Dict[str, str]  # item_id -> lore text

@dataclass
class GameDefinition:
    """Complete game definition that LLM can generate"""
    # Basic info
    game_id: str
    title: str
    theme: str  # "fantasy", "cyberpunk", "horror", etc.
    difficulty: str  # "easy", "normal", "hard", "nightmare"
    
    # Content
    creatures: List[CreatureDefinition]
    items: List[ItemDefinition]
    room_themes: List[RoomTheme]
    
    # Structure
    num_levels: int = 5
    maze_configs: List[MazeConfig] = field(default_factory=list)
    
    # Narrative
    narrative: GameNarrative = field(default_factory=GameNarrative)
    
    # Game rules
    starting_equipment: List[str] = field(default_factory=list)
    starting_position: tuple = (16, 11)
    victory_condition: str = "defeat_boss"
    
    # Balancing
    health_scaling: float = 1.0
    damage_scaling: float = 1.0
    speed_scaling: float = 1.0
    
    # Special features
    shop_enabled: bool = True
    rumors_enabled: bool = True
    custom_mechanics: List[str] = field(default_factory=list)

# Example prompts for LLM generation
LLM_GENERATION_PROMPT = """
Create a complete game definition for a Dungeons of Daggorath style game with the following theme: {theme}

The game should include:
1. {num_creatures} unique creature types
2. {num_items} different items (weapons, shields, consumables)
3. {num_levels} levels with increasing difficulty
4. A compelling narrative that fits the theme
5. Balanced gameplay mechanics

Output the game definition in the following JSON format:
{schema}

Be creative with names, descriptions, and lore. Ensure game balance by making later creatures more powerful and later items more effective.
"""

@dataclass
class GenerationConstraints:
    """Constraints for LLM generation"""
    theme: str
    num_creatures: int = 6
    num_items: int = 15
    num_levels: int = 5
    include_boss: bool = True
    difficulty_curve: str = "linear"  # or "exponential", "stepped"
    
def generate_game_prompt(constraints: GenerationConstraints) -> str:
    """Generate a prompt for LLM to create a game"""
    import json
    
    # Create example schema
    example = GameDefinition(
        game_id="example",
        title="Example Game",
        theme=constraints.theme,
        difficulty="normal",
        creatures=[
            CreatureDefinition(
                id="spider",
                name="Cave Spider",
                description="A venomous arachnid",
                power=50,
                speed=1500,
                attack_speed=2000,
                magic_offense=0,
                magic_defense=100,
                phys_offense=100,
                phys_defense=0,
                damage=10,
                sound_description="skittering",
                behavior_pattern="aggressive"
            )
        ],
        items=[
            ItemDefinition(
                id="iron_sword",
                name="Iron Sword",
                description="A sturdy blade",
                item_type="weapon",
                weight=30,
                value=20,
                magic_bonus=0,
                physical_bonus=150,
                special_ability=None,
                reveal_requirement=0
            )
        ],
        room_themes=[
            RoomTheme(
                id="dungeon",
                name="Dark Dungeon",
                description="Damp stone corridors",
                wall_description="rough stone blocks",
                floor_description="cold flagstones",
                ambient_sounds=["dripping water", "distant echoes"],
                lighting_modifier=0.8,
                danger_level=1
            )
        ],
        narrative=GameNarrative(
            title=constraints.theme + " Dungeon",
            setting=constraints.theme,
            intro_text="You enter the mysterious dungeon...",
            victory_text="You have conquered the dungeon!",
            death_text="You have perished in the darkness...",
            level_descriptions=["The entrance hall", "The deeper chambers"],
            boss_encounter_text="The final guardian awaits!",
            item_lore={}
        )
    )
    
    schema_json = json.dumps(example.__dict__, indent=2, default=str)
    
    return LLM_GENERATION_PROMPT.format(
        theme=constraints.theme,
        num_creatures=constraints.num_creatures,
        num_items=constraints.num_items,
        num_levels=constraints.num_levels,
        schema=schema_json
    )

# Game variations the LLM could generate
THEME_SUGGESTIONS = [
    "Medieval Fantasy",
    "Cyberpunk Dystopia", 
    "Cosmic Horror",
    "Steampunk Adventure",
    "Post-Apocalyptic",
    "Ancient Egyptian",
    "Pirate Island",
    "Haunted Mansion",
    "Space Station",
    "Underwater Ruins",
    "Wild West",
    "Samurai Castle",
    "Viking Fortress",
    "Aztec Temple",
    "Gothic Cathedral"
]

# Example usage
def generate_random_game(theme: str = "Medieval Fantasy") -> str:
    """Example of how to request a game from an LLM"""
    constraints = GenerationConstraints(
        theme=theme,
        num_creatures=8,
        num_items=20,
        num_levels=5,
        include_boss=True,
        difficulty_curve="exponential"
    )
    
    prompt = generate_game_prompt(constraints)
    
    # This would be sent to an LLM API
    # response = llm_api.generate(prompt)
    # game_def = GameDefinition.from_json(response)
    
    return prompt