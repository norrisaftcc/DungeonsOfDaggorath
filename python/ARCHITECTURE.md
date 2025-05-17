# Python Port Architecture - Clean Design

## Core Principles (Fowler-approved!)

### 1. Layer Separation
```
┌─────────────────────┐
│   Presentation      │  (UI: Terminal, Web, GUI)
├─────────────────────┤
│   Application       │  (Game Rules, Commands)
├─────────────────────┤
│   Domain           │  (Player, Creatures, Items)
├─────────────────────┤
│   Infrastructure   │  (Save/Load, Config, Audio)
└─────────────────────┘
```

### 2. Domain-Driven Design

**Core Domain Objects:**
- `Player` - The adventurer
- `Creature` - Monsters and the wizard
- `Item` - Weapons, shields, torches, etc.
- `Dungeon` - The maze structure
- `Room` - Individual dungeon cells

**Value Objects:**
- `Position` - Coordinates in dungeon
- `Direction` - North, South, East, West
- `Health` - Power and damage
- `Light` - Torch illumination

**Domain Services:**
- `CombatService` - Battle calculations
- `MovementService` - Navigation rules
- `VisibilityService` - Line of sight
- `HeartbeatService` - Health system

### 3. Repository Pattern
```python
class GameRepository(ABC):
    @abstractmethod
    def save_game(self, game_state: GameState) -> None:
        pass
    
    @abstractmethod
    def load_game(self, save_name: str) -> GameState:
        pass

class FileGameRepository(GameRepository):
    """File-based save system"""
    
class MemoryGameRepository(GameRepository):
    """In-memory for testing"""
```

### 4. Command Pattern
```python
class Command(ABC):
    @abstractmethod
    def execute(self, game_state: GameState) -> CommandResult:
        pass

class MoveCommand(Command):
    def __init__(self, direction: Direction):
        self.direction = direction
        
    def execute(self, game_state: GameState) -> CommandResult:
        # Validate move
        # Update position
        # Return result
```

### 5. Event System
```python
class Event:
    timestamp: float
    event_type: str

class PlayerMovedEvent(Event):
    from_position: Position
    to_position: Position

class CreatureAttackEvent(Event):
    creature_id: int
    damage: int

class EventBus:
    def publish(self, event: Event):
        # Notify subscribers
    
    def subscribe(self, event_type: type, handler: Callable):
        # Register handler
```

### 6. Dependency Injection
```python
class GameEngine:
    def __init__(
        self,
        dungeon: Dungeon,
        combat_service: CombatService,
        movement_service: MovementService,
        event_bus: EventBus,
        config: GameConfig
    ):
        self.dungeon = dungeon
        self.combat_service = combat_service
        # ... etc

# Clean construction
def create_game() -> GameEngine:
    config = GameConfig.load("classic.json")
    event_bus = EventBus()
    
    dungeon = Dungeon(config.dungeon_config)
    combat_service = CombatService(config.combat_config)
    movement_service = MovementService(dungeon)
    
    return GameEngine(
        dungeon=dungeon,
        combat_service=combat_service,
        movement_service=movement_service,
        event_bus=event_bus,
        config=config
    )
```

### 7. Testing Strategy
```python
# Unit tests for domain objects
class TestPlayer:
    def test_take_damage(self):
        player = Player(power=100)
        player.take_damage(20)
        assert player.current_health == 80

# Integration tests for services
class TestCombatService:
    def test_player_attacks_creature(self):
        combat = CombatService()
        result = combat.calculate_attack(player, creature)
        assert result.hit == True

# Acceptance tests for gameplay
class TestGameplay:
    def test_complete_level_one(self):
        game = create_test_game()
        game.execute_command("MOVE")
        game.execute_command("GET RIGHT TORCH")
        # ... full scenario
```

## Module Structure
```
python/
├── domain/
│   ├── __init__.py
│   ├── player.py
│   ├── creature.py
│   ├── item.py
│   ├── dungeon.py
│   └── value_objects.py
├── application/
│   ├── __init__.py
│   ├── game_engine.py
│   ├── commands.py
│   ├── services.py
│   └── events.py
├── infrastructure/
│   ├── __init__.py
│   ├── repositories.py
│   ├── config_loader.py
│   └── audio_system.py
├── presentation/
│   ├── __init__.py
│   ├── terminal_ui.py
│   ├── web_ui.py
│   └── api_server.py
└── tests/
    ├── unit/
    ├── integration/
    └── acceptance/
```

## Benefits

1. **Testable**: Each layer can be tested independently
2. **Flexible**: Easy to add new UIs or storage backends
3. **Maintainable**: Clear separation of concerns
4. **Extensible**: New features don't break existing code
5. **Understandable**: Domain model matches game concepts

## Implementation Plan

1. Start with pure domain model (no I/O)
2. Add repositories for persistence
3. Build command system
4. Create service layer
5. Add event bus
6. Build UI adapters
7. Comprehensive testing

This architecture lets us port the original game logic while keeping it clean and extensible!