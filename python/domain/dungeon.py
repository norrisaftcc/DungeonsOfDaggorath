"""Dungeon domain entity representing the game map."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Set, Tuple, Optional
from uuid import UUID, uuid4

from .value_objects import Position


class CellType(Enum):
    """Types of dungeon cells."""
    WALL = "wall"
    FLOOR = "floor"
    DOOR = "door"
    STAIRS_UP = "stairs_up"
    STAIRS_DOWN = "stairs_down"
    SECRET = "secret"
    ENTRANCE = "entrance"
    EXIT = "exit"
    BOSS = "boss"
    SHOP = "shop"


@dataclass
class Cell:
    """A single cell in the dungeon."""
    
    cell_type: CellType
    is_revealed: bool = False
    properties: Dict[str, any] = field(default_factory=dict)
    
    @property
    def is_passable(self) -> bool:
        """Check if the cell can be walked through."""
        return self.cell_type not in [CellType.WALL, CellType.SECRET]
    
    @property
    def is_transparent(self) -> bool:
        """Check if the cell allows vision through it."""
        return self.cell_type not in [CellType.WALL, CellType.SECRET, CellType.DOOR]


@dataclass
class Room:
    """A room in the dungeon."""
    
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    positions: Set[Position] = field(default_factory=set)
    description: str = ""
    properties: Dict[str, any] = field(default_factory=dict)
    
    @property
    def center(self) -> Position:
        """Get the center position of the room."""
        if not self.positions:
            return Position(0, 0, 0)
        
        sum_row = sum(p.row for p in self.positions)
        sum_col = sum(p.col for p in self.positions)
        count = len(self.positions)
        
        return Position(sum_row // count, sum_col // count, next(iter(self.positions)).level)
    
    @property
    def bounds(self) -> Tuple[int, int, int, int]:
        """Get room boundaries (min_x, min_y, max_x, max_y)."""
        if not self.positions:
            return (0, 0, 0, 0)
        
        positions_list = list(self.positions)
        min_row = min(p.row for p in positions_list)
        max_row = max(p.row for p in positions_list)
        min_col = min(p.col for p in positions_list)
        max_col = max(p.col for p in positions_list)
        
        return (min_row, min_col, max_row, max_col)
    
    def add_position(self, position: Position) -> None:
        """Add a position to the room."""
        self.positions.add(position)
    
    def contains(self, position: Position) -> bool:
        """Check if a position is in this room."""
        return position in self.positions


@dataclass
class Level:
    """A single level of the dungeon."""
    
    depth: int
    width: int
    height: int
    cells: Dict[Tuple[int, int], Cell] = field(default_factory=dict)
    rooms: List[Room] = field(default_factory=list)
    
    def get_cell(self, x: int, y: int) -> Cell:
        """Get a cell at the given coordinates."""
        return self.cells.get((x, y), Cell(CellType.WALL))
    
    def set_cell(self, x: int, y: int, cell: Cell) -> None:
        """Set a cell at the given coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[(x, y)] = cell
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if a position is valid in this level."""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_room_at(self, position: Position) -> Optional[Room]:
        """Get the room at a given position, if any."""
        for room in self.rooms:
            if room.contains(position):
                return room
        return None
    
    def add_room(self, room: Room) -> None:
        """Add a room to this level."""
        self.rooms.append(room)
        
        # Set floor cells for all room positions
        for pos in room.positions:
            if pos.level == self.depth:
                self.set_cell(pos.row, pos.col, Cell(CellType.FLOOR))


@dataclass
class Dungeon:
    """The complete dungeon structure."""
    
    id: UUID = field(default_factory=uuid4)
    name: str = "Dungeon of Daggorath"
    levels: Dict[int, Level] = field(default_factory=dict)
    entrance: Position = field(default_factory=lambda: Position(11, 16, 0))
    properties: Dict[str, any] = field(default_factory=dict)
    
    def get_level(self, depth: int) -> Optional[Level]:
        """Get a level by depth."""
        return self.levels.get(depth)
    
    def add_level(self, level: Level) -> None:
        """Add a level to the dungeon."""
        self.levels[level.depth] = level
    
    def get_cell(self, position: Position) -> Cell:
        """Get a cell at the given position."""
        level = self.get_level(position.level)
        if level:
            return level.get_cell(position.row, position.col)
        return Cell(CellType.WALL)
    
    def set_cell(self, position: Position, cell: Cell) -> None:
        """Set a cell at the given position."""
        level = self.get_level(position.level)
        if level:
            level.set_cell(position.row, position.col, cell)
    
    def is_valid_position(self, position: Position) -> bool:
        """Check if a position is valid in the dungeon."""
        level = self.get_level(position.level)
        return level is not None and level.is_valid_position(position.row, position.col)
    
    def get_neighbors(self, position: Position) -> List[Position]:
        """Get valid neighboring positions."""
        neighbors = []
        for drow, dcol in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = Position(position.row + drow, position.col + dcol, position.level)
            if self.is_valid_position(new_pos):
                cell = self.get_cell(new_pos)
                if cell.is_passable:
                    neighbors.append(new_pos)
        return neighbors
    
    def reveal_area(self, position: Position, radius: int = 1) -> None:
        """Reveal cells around a position."""
        level = self.get_level(position.level)
        if not level:
            return
        
        for drow in range(-radius, radius + 1):
            for dcol in range(-radius, radius + 1):
                row, col = position.row + drow, position.col + dcol
                if level.is_valid_position(row, col):
                    cell = level.get_cell(row, col)
                    cell.is_revealed = True


# Factory functions for creating standard dungeons
def create_standard_level(depth: int, width: int = 32, height: int = 32) -> Level:
    """Create a standard dungeon level."""
    level = Level(depth=depth, width=width, height=height)
    
    # Fill with walls
    for x in range(width):
        for y in range(height):
            level.set_cell(x, y, Cell(CellType.WALL))
    
    return level


def create_room(level: Level, row: int, col: int, width: int, height: int, name: str = "") -> Room:
    """Create a rectangular room."""
    room = Room(name=name)
    
    for drow in range(height):
        for dcol in range(width):
            pos = Position(row + drow, col + dcol, level.depth)
            room.add_position(pos)
    
    level.add_room(room)
    return room