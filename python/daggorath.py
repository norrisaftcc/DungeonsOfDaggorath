"""
Python wrapper for Dungeons of Daggorath
Provides high-level interface to the game engine
"""

import ctypes
import os
import subprocess
import time
from enum import Enum
from typing import Optional, List, Dict
import json

class Direction(Enum):
    """Movement and turning directions"""
    FORWARD = ""
    BACK = "BACK"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    AROUND = "AROUND"

class Hand(Enum):
    """Which hand to use for actions"""
    LEFT = "LEFT"
    RIGHT = "RIGHT"

class Command(Enum):
    """Game commands"""
    MOVE = "MOVE"
    TURN = "TURN"
    CLIMB = "CLIMB"
    EXAMINE = "EXAMINE"
    LOOK = "LOOK"
    GET = "GET"
    PULL = "PULL"
    STOW = "STOW"
    DROP = "DROP"
    ATTACK = "ATTACK"
    USE = "USE"
    REVEAL = "REVEAL"
    INCANT = "INCANT"
    ZSAVE = "ZSAVE"
    ZLOAD = "ZLOAD"
    RESTART = "RESTART"

class DaggorathGame:
    """High-level interface to Dungeons of Daggorath"""
    
    def __init__(self, game_path: str = "../dod"):
        self.game_path = os.path.abspath(game_path)
        self.process: Optional[subprocess.Popen] = None
        self.lib: Optional[ctypes.CDLL] = None
        
    def start_subprocess(self):
        """Start game as subprocess with pipe communication"""
        self.process = subprocess.Popen(
            [self.game_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
    def start_library(self):
        """Load game as shared library for direct access"""
        # This would require building game as .so/.dylib
        # For now, we'll use the WebAssembly approach
        pass
        
    def send_command(self, command: str):
        """Send a command string to the game"""
        if self.process:
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()
            
    def move(self, direction: Direction = Direction.FORWARD):
        """Move in a direction"""
        cmd = f"{Command.MOVE.value}"
        if direction != Direction.FORWARD:
            cmd += f" {direction.value}"
        self.send_command(cmd)
        
    def turn(self, direction: Direction):
        """Turn in a direction"""
        self.send_command(f"{Command.TURN.value} {direction.value}")
        
    def attack(self, hand: Hand = Hand.RIGHT):
        """Attack with weapon in specified hand"""
        self.send_command(f"{Command.ATTACK.value} {hand.value}")
        
    def use(self, hand: Hand):
        """Use item in specified hand"""
        self.send_command(f"{Command.USE.value} {hand.value}")
        
    def get_item(self, hand: Hand, item: str):
        """Pick up item from floor"""
        self.send_command(f"{Command.GET.value} {hand.value} {item}")
        
    def pull_item(self, hand: Hand, item: str):
        """Pull item from backpack"""
        self.send_command(f"{Command.PULL.value} {hand.value} {item}")
        
    def examine(self):
        """Examine surroundings and inventory"""
        self.send_command(Command.EXAMINE.value)
        
    def save_game(self, name: str):
        """Save current game state"""
        self.send_command(f"{Command.ZSAVE.value} {name}")
        
    def load_game(self, name: str):
        """Load saved game"""
        self.send_command(f"{Command.ZLOAD.value} {name}")


# Example usage for testing
if __name__ == "__main__":
    game = DaggorathGame()
    
    # Test command generation
    print("Testing command generation:")
    print(f"Move forward: {Command.MOVE.value}")
    print(f"Turn left: {Command.TURN.value} {Direction.LEFT.value}")
    print(f"Attack right: {Command.ATTACK.value} {Hand.RIGHT.value}")
    
    # Would start actual game like:
    # game.start_subprocess()
    # game.examine()
    # game.pull_item(Hand.RIGHT, "TORCH")
    # game.use(Hand.RIGHT)