"""
LLM Game Generator - Creates complete games using AI
"""

import json
import requests
from typing import Dict, Any, Optional
from pathlib import Path

from .game_schema import (
    GameDefinition, CreatureDefinition, ItemDefinition,
    RoomTheme, MazeConfig, GameNarrative, GenerationConstraints
)

class LLMGameGenerator:
    """Generate complete game definitions using LLM"""
    
    def __init__(self, api_endpoint: str = "http://127.0.0.1:1234", api_key: Optional[str] = None):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
        }
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    def generate_game(self, theme: str, constraints: Optional[GenerationConstraints] = None) -> GameDefinition:
        """Generate a complete game using LLM"""
        if constraints is None:
            constraints = GenerationConstraints(theme=theme)
        
        # Create the prompt
        prompt = self._create_generation_prompt(constraints)
        
        # Call LLM API
        game_json = self._call_llm(prompt)
        
        # Parse response into GameDefinition
        game_def = self._parse_game_definition(game_json)
        
        # Validate and balance the game
        game_def = self._validate_and_balance(game_def)
        
        return game_def
    
    def _create_generation_prompt(self, constraints: GenerationConstraints) -> str:
        """Create detailed prompt for game generation"""
        prompt = f"""
You are a game designer creating a complete game in the style of Dungeons of Daggorath.

Theme: {constraints.theme}
Requirements:
- {constraints.num_creatures} unique creatures with escalating difficulty
- {constraints.num_items} items (weapons, shields, torches, consumables)
- {constraints.num_levels} dungeon levels
- Compelling narrative that fits the theme
- Balanced gameplay progression

Create a complete game definition with:

1. CREATURES: Each should have:
   - Unique name and description fitting the theme
   - Power scaling from 30 to 30000
   - Appropriate speed (1000-3000ms)
   - Magic/physical attack/defense (0-200)
   - Distinctive sound description
   - Behavior pattern

2. ITEMS: Include:
   - 3 weapon tiers 
   - 3 shield tiers
   - 3 torch types
   - 4 consumable types
   - 2 special items
   - Theme-appropriate names

3. NARRATIVE:
   - Engaging intro text
   - Victory message
   - Death message
   - Per-level descriptions
   - Boss encounter text
   - Item lore

4. LEVEL DESIGN:
   - Maze configurations for each level
   - Room themes
   - Increasing difficulty

Output as JSON matching this structure:
{{
    "game_id": "unique_id",
    "title": "Game Title",
    "theme": "{constraints.theme}",
    "difficulty": "normal",
    "creatures": [...],
    "items": [...],
    "room_themes": [...],
    "num_levels": {constraints.num_levels},
    "maze_configs": [...],
    "narrative": {{...}},
    "starting_equipment": ["torch", "weapon"],
    "victory_condition": "defeat_boss"
}}
"""
        return prompt
    
    def _call_llm(self, prompt: str) -> Dict[str, Any]:
        """Call the LLM API and get JSON response"""
        try:
            # OpenAI-compatible API call
            payload = {
                "model": "gpt-4",  # or whatever model
                "messages": [
                    {"role": "system", "content": "You are a creative game designer."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 4000,
                "response_format": {"type": "json_object"}
            }
            
            response = requests.post(
                f"{self.api_endpoint}/chat/completions",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                return json.loads(content)
            else:
                raise Exception(f"LLM API error: {response.status_code}")
                
        except Exception as e:
            print(f"Error calling LLM: {e}")
            # Return a default game for testing
            return self._get_default_game()
    
    def _parse_game_definition(self, game_json: Dict[str, Any]) -> GameDefinition:
        """Parse JSON into GameDefinition object"""
        # Convert JSON to dataclass instances
        creatures = [CreatureDefinition(**c) for c in game_json.get('creatures', [])]
        items = [ItemDefinition(**i) for i in game_json.get('items', [])]
        room_themes = [RoomTheme(**r) for r in game_json.get('room_themes', [])]
        
        # Parse maze configs
        maze_configs = []
        for config in game_json.get('maze_configs', []):
            maze_configs.append(MazeConfig(**config))
        
        # Parse narrative
        narrative_data = game_json.get('narrative', {})
        narrative = GameNarrative(**narrative_data)
        
        # Create game definition
        game_def = GameDefinition(
            game_id=game_json.get('game_id', 'generated'),
            title=game_json.get('title', 'Generated Game'),
            theme=game_json.get('theme', 'fantasy'),
            difficulty=game_json.get('difficulty', 'normal'),
            creatures=creatures,
            items=items,
            room_themes=room_themes,
            num_levels=game_json.get('num_levels', 5),
            maze_configs=maze_configs,
            narrative=narrative,
            starting_equipment=game_json.get('starting_equipment', []),
            victory_condition=game_json.get('victory_condition', 'defeat_boss')
        )
        
        return game_def
    
    def _validate_and_balance(self, game_def: GameDefinition) -> GameDefinition:
        """Validate and auto-balance the generated game"""
        # Ensure difficulty progression
        if game_def.creatures:
            # Sort creatures by power
            game_def.creatures.sort(key=lambda c: c.power)
            
            # Ensure proper scaling
            min_power = 30
            max_power = 30000
            for i, creature in enumerate(game_def.creatures):
                expected_power = min_power + (max_power - min_power) * (i / len(game_def.creatures))
                if creature.power < expected_power * 0.5 or creature.power > expected_power * 2:
                    creature.power = int(expected_power)
        
        # Ensure items have proper scaling
        weapon_items = [i for i in game_def.items if i.item_type == "weapon"]
        if weapon_items:
            weapon_items.sort(key=lambda i: i.value)
            for i, weapon in enumerate(weapon_items):
                expected_damage = 10 + (40 * i / len(weapon_items))
                if weapon.value < expected_damage * 0.5:
                    weapon.value = int(expected_damage)
        
        # Ensure we have required mazes
        if len(game_def.maze_configs) < game_def.num_levels:
            for i in range(len(game_def.maze_configs), game_def.num_levels):
                size = 20 + (i * 5)  # Increasing size
                game_def.maze_configs.append(
                    MazeConfig(
                        width=size,
                        height=size,
                        algorithm="recursive_backtrack",
                        room_density=0.3 + (i * 0.05),
                        secret_passages=i,
                        loops=i
                    )
                )
        
        return game_def
    
    def _get_default_game(self) -> Dict[str, Any]:
        """Return a default game for testing when LLM is unavailable"""
        return {
            "game_id": "default_fantasy",
            "title": "The Classic Dungeon",
            "theme": "Medieval Fantasy",
            "difficulty": "normal",
            "creatures": [
                {
                    "id": "rat",
                    "name": "Giant Rat",
                    "description": "A diseased rodent",
                    "power": 30,
                    "speed": 1500,
                    "attack_speed": 2000,
                    "magic_offense": 0,
                    "magic_defense": 50,
                    "phys_offense": 80,
                    "phys_defense": 20,
                    "damage": 5,
                    "sound_description": "squeaking",
                    "behavior_pattern": "aggressive"
                },
                {
                    "id": "skeleton",
                    "name": "Skeleton Warrior",
                    "description": "Animated bones",
                    "power": 100,
                    "speed": 1200,
                    "attack_speed": 1800,
                    "magic_offense": 50,
                    "magic_defense": 100,
                    "phys_offense": 120,
                    "phys_defense": 80,
                    "damage": 15,
                    "sound_description": "rattling bones",
                    "behavior_pattern": "patrol"
                }
            ],
            "items": [
                {
                    "id": "wooden_sword",
                    "name": "Wooden Sword",
                    "description": "A basic training sword",
                    "item_type": "weapon",
                    "weight": 15,
                    "value": 10,
                    "magic_bonus": 0,
                    "physical_bonus": 100,
                    "reveal_requirement": 0
                }
            ],
            "room_themes": [
                {
                    "id": "dungeon",
                    "name": "Stone Dungeon",
                    "description": "Cold stone walls",
                    "wall_description": "rough granite blocks",
                    "floor_description": "damp flagstones",
                    "ambient_sounds": ["dripping water"],
                    "lighting_modifier": 0.8,
                    "danger_level": 1
                }
            ],
            "num_levels": 5,
            "maze_configs": [],
            "narrative": {
                "title": "The Classic Dungeon",
                "setting": "Medieval Fantasy",
                "intro_text": "You descend into the ancient dungeon...",
                "victory_text": "You have defeated the evil!",
                "death_text": "You have fallen in battle...",
                "level_descriptions": ["The entrance", "Deeper chambers"],
                "boss_encounter_text": "The dark lord awaits!",
                "item_lore": {}
            },
            "starting_equipment": ["pine_torch", "wooden_sword"],
            "victory_condition": "defeat_boss"
        }
    
    def save_game_definition(self, game_def: GameDefinition, filename: str):
        """Save game definition to file"""
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(game_def.__dict__, f, indent=2, default=str)
    
    def load_game_definition(self, filename: str) -> GameDefinition:
        """Load game definition from file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        return self._parse_game_definition(data)

# Example usage
def create_random_game():
    """Example: Generate a random themed game"""
    import random
    
    themes = [
        "Cyberpunk Space Station",
        "Haunted Victorian Mansion",
        "Underwater Atlantis",
        "Wild West Ghost Town",
        "Samurai Castle",
        "Aztec Temple",
        "Steampunk Airship"
    ]
    
    generator = LLMGameGenerator()
    theme = random.choice(themes)
    
    print(f"Generating {theme} game...")
    
    constraints = GenerationConstraints(
        theme=theme,
        num_creatures=8,
        num_items=20,
        num_levels=5,
        include_boss=True
    )
    
    game = generator.generate_game(theme, constraints)
    
    # Save the generated game
    filename = f"games/{theme.lower().replace(' ', '_')}.json"
    generator.save_game_definition(game, filename)
    
    print(f"Generated game saved to {filename}")
    print(f"Title: {game.title}")
    print(f"Creatures: {len(game.creatures)}")
    print(f"Items: {len(game.items)}")
    
    return game

if __name__ == "__main__":
    # Generate a random game
    game = create_random_game()