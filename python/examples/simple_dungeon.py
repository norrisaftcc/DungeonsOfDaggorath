"""
Simple Dungeon - A minimal game to demonstrate the engine architecture
Shows how any game can use our clean domain/application/presentation layers
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from uuid import UUID, uuid4
from enum import Enum

# Domain Layer - Pure game logic
@dataclass
class Position:
    x: int
    y: int
    
    def move(self, dx: int, dy: int) -> 'Position':
        return Position(self.x + dx, self.y + dy)

@dataclass
class Entity:
    id: UUID = field(default_factory=uuid4)
    name: str = "Unknown"
    position: Position = field(default_factory=lambda: Position(0, 0))
    health: int = 100
    attack: int = 10

class TileType(Enum):
    EMPTY = "."
    WALL = "#"
    DOOR = "D"
    TREASURE = "$"
    EXIT = "E"

@dataclass
class Room:
    tiles: List[List[TileType]]
    width: int
    height: int
    
    def get_tile(self, pos: Position) -> TileType:
        if 0 <= pos.x < self.width and 0 <= pos.y < self.height:
            return self.tiles[pos.y][pos.x]
        return TileType.WALL

# Simple game state
@dataclass
class SimpleGame:
    player: Entity
    room: Room
    treasures_collected: int = 0
    is_complete: bool = False

# Application Layer - Game logic and commands
class Command:
    """Base command class"""
    pass

@dataclass
class MoveCommand(Command):
    direction: str  # "north", "south", "east", "west"

@dataclass
class AttackCommand(Command):
    target_id: UUID

class GameEngine:
    """Simple game engine demonstrating clean architecture"""
    
    def __init__(self, game_state: SimpleGame):
        self.game_state = game_state
        self.event_history: List[str] = []
    
    def execute_command(self, command: Command) -> str:
        """Execute a command and return result message"""
        if isinstance(command, MoveCommand):
            return self._handle_move(command)
        elif isinstance(command, AttackCommand):
            return self._handle_attack(command)
        else:
            return "Unknown command"
    
    def _handle_move(self, command: MoveCommand) -> str:
        """Handle movement command"""
        # Calculate new position
        dx, dy = 0, 0
        if command.direction == "north":
            dy = -1
        elif command.direction == "south":
            dy = 1
        elif command.direction == "east":
            dx = 1
        elif command.direction == "west":
            dx = -1
        
        new_pos = self.game_state.player.position.move(dx, dy)
        
        # Check if move is valid
        tile = self.game_state.room.get_tile(new_pos)
        
        if tile == TileType.WALL:
            self.event_history.append(f"Player bumped into wall")
            return "You can't go that way!"
        
        # Execute move
        self.game_state.player.position = new_pos
        self.event_history.append(f"Player moved to {new_pos.x},{new_pos.y}")
        
        # Check for special tiles
        if tile == TileType.TREASURE:
            self.game_state.treasures_collected += 1
            self.event_history.append("Player found treasure!")
            return "You found a treasure!"
        elif tile == TileType.EXIT:
            self.game_state.is_complete = True
            self.event_history.append("Player reached the exit!")
            return "You've reached the exit! Game complete!"
        
        return f"You move {command.direction}"

# Infrastructure Layer - Save/Load
import json

class GameRepository:
    """Handle game persistence"""
    
    def save_game(self, game_state: SimpleGame, filename: str):
        """Save game to JSON"""
        data = {
            "player": {
                "name": game_state.player.name,
                "x": game_state.player.position.x,
                "y": game_state.player.position.y,
                "health": game_state.player.health
            },
            "treasures_collected": game_state.treasures_collected,
            "is_complete": game_state.is_complete
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_game(self, filename: str) -> SimpleGame:
        """Load game from JSON"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        player = Entity(
            name=data["player"]["name"],
            position=Position(data["player"]["x"], data["player"]["y"]),
            health=data["player"]["health"]
        )
        
        # Create default room for demo
        room = self._create_demo_room()
        
        return SimpleGame(
            player=player,
            room=room,
            treasures_collected=data["treasures_collected"],
            is_complete=data["is_complete"]
        )
    
    def _create_demo_room(self) -> Room:
        """Create a simple demo room"""
        # Simple 5x5 room with walls, treasure, and exit
        layout = [
            "#####",
            "#..D#",
            "#.$.#",
            "#...#",
            "###E#"
        ]
        
        tiles = []
        for row in layout:
            tile_row = []
            for char in row:
                if char == '#':
                    tile_row.append(TileType.WALL)
                elif char == '.':
                    tile_row.append(TileType.EMPTY)
                elif char == 'D':
                    tile_row.append(TileType.DOOR)
                elif char == '$':
                    tile_row.append(TileType.TREASURE)
                elif char == 'E':
                    tile_row.append(TileType.EXIT)
            tiles.append(tile_row)
        
        return Room(tiles=tiles, width=5, height=5)

# Presentation Layer - Terminal UI
class TerminalUI:
    """Simple terminal interface"""
    
    def __init__(self, engine: GameEngine):
        self.engine = engine
    
    def render(self):
        """Render current game state"""
        game = self.engine.game_state
        room = game.room
        
        print("\n" + "="*20)
        print(f"Health: {game.player.health} | Treasures: {game.treasures_collected}")
        print("="*20)
        
        # Render room
        for y in range(room.height):
            row = ""
            for x in range(room.width):
                if game.player.position.x == x and game.player.position.y == y:
                    row += "@"  # Player
                else:
                    tile = room.get_tile(Position(x, y))
                    if tile == TileType.WALL:
                        row += "#"
                    elif tile == TileType.EMPTY:
                        row += "."
                    elif tile == TileType.DOOR:
                        row += "D"
                    elif tile == TileType.TREASURE:
                        row += "$"
                    elif tile == TileType.EXIT:
                        row += "E"
            print(row)
        
        print("\nCommands: north/south/east/west, quit")
    
    def get_input(self) -> Optional[Command]:
        """Get command from user"""
        user_input = input("> ").strip().lower()
        
        if user_input in ["north", "south", "east", "west"]:
            return MoveCommand(direction=user_input)
        elif user_input == "quit":
            return None
        else:
            print("Unknown command!")
            return self.get_input()
    
    def show_message(self, message: str):
        """Display a message to the user"""
        print(f"\n{message}")

# Main game loop
def main():
    """Run the simple dungeon game"""
    # Create game components
    repo = GameRepository()
    
    # Create initial game state
    player = Entity(name="Hero", position=Position(1, 1))
    room = repo._create_demo_room()
    game_state = SimpleGame(player=player, room=room)
    
    # Create engine and UI
    engine = GameEngine(game_state)
    ui = TerminalUI(engine)
    
    print("Welcome to Simple Dungeon!")
    print("Find the treasure and reach the exit!")
    
    # Main game loop
    while not game_state.is_complete:
        ui.render()
        
        command = ui.get_input()
        if command is None:
            print("Thanks for playing!")
            break
        
        result = engine.execute_command(command)
        ui.show_message(result)
    
    if game_state.is_complete:
        print("\nCongratulations! You've completed the game!")
        print(f"Final score: {game_state.treasures_collected} treasures")
    
    # Show event history
    print("\nGame History:")
    for event in engine.event_history:
        print(f"  - {event}")

# API Usage Example
def api_example():
    """Show how the game works as an API"""
    # Create game
    repo = GameRepository()
    player = Entity(name="Bot", position=Position(1, 1))
    room = repo._create_demo_room()
    game_state = SimpleGame(player=player, room=room)
    engine = GameEngine(game_state)
    
    # AI/Bot can play via API
    moves = ["east", "south", "south", "east"]
    
    for move in moves:
        result = engine.execute_command(MoveCommand(direction=move))
        print(f"Bot moved {move}: {result}")
        print(f"Bot position: {game_state.player.position}")
    
    print(f"\nBot collected {game_state.treasures_collected} treasures")
    print(f"Game complete: {game_state.is_complete}")

if __name__ == "__main__":
    # Run the game
    main()
    
    # Or run API example
    # api_example()