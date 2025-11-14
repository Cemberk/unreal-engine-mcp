# Verse API Overview

**Build Version**: ++Fortnite+Release-38.10-CL-47888945  
**Generated**: Phase 2 - Verse Knowledge Base Implementation  
**Total Classes**: 1,184  
**Total Enums**: 4  
**Source Files**: 3 digest files  

---

## API Structure

The Verse/Fortnite API is organized into three main modules:

### 1. Fortnite.digest.verse
- **Purpose**: Core Fortnite Creative gameplay API
- **Contains**: Devices, gameplay systems, character interactions
- **Key Modules**:
  - `/Fortnite.com/Devices` - Creative devices (buttons, spawners, etc.)
  - `/Fortnite.com/Characters` - Player/character systems
  - `/Fortnite.com/Game` - Game management
  - `/Fortnite.com/UI` - User interface elements

### 2. Verse.digest.verse
- **Purpose**: Verse standard library
- **Contains**: Core language features, simulation, concurrency
- **Key Modules**:
  - `/Verse.org/Simulation` - Simulation and time functions
  - `/Verse.org/Concurrency` - Async/await patterns
  - `/Verse.org/Native` - Native type definitions

### 3. UnrealEngine.digest.verse
- **Purpose**: Unreal Engine integration layer
- **Contains**: Spatial math, transforms, engine systems
- **Key Modules**:
  - `/UnrealEngine.com/Temporary/SpatialMath` - Vector/rotation math
  - `/UnrealEngine.com/Temporary/Diagnostics` - Debugging utilities

---

## Device Categories

Fortnite Creative devices are the primary building blocks for gameplay:

### Core Interaction Devices
- `button_device` - Interactive buttons
- `trigger_device` - Trigger volumes
- `switch_device` - State switches

### Spawning Devices
- `item_spawner_device` - Item spawning
- `creature_spawner_device` - NPC/creature spawning
- `player_spawner_device` - Player respawning

### Game Management
- `score_manager_device` - Score tracking
- `end_game_device` - Win/loss conditions
- `timer_device` - Countdown timers
- `round_settings_device` - Round management

### Player Modification
- `item_granter_device` - Give items to players
- `item_remover_device` - Remove items from players
- `mutator_zone_device` - Apply effects in area
- `teleporter_device` - Teleportation

### UI/Feedback
- `hud_message_device` - Display messages
- `elimination_feed_device` - Elimination notifications
- `player_tracker_device` - Waypoints/markers

---

## Common Patterns

### Device Lifecycle

```verse
my_device := class(creative_device):
    @editable
    MyButton: button_device = button_device{}

    OnBegin<override>()<suspends>:void=
        # Subscribe to events
        MyButton.InteractedWithEvent.Subscribe(OnButtonPressed)

    OnButtonPressed(Agent:agent):void=
        Print("{Agent} pressed button")
```

### Event Subscription

Devices expose events via `listenable` types:
- `InteractedWithEvent` - Player interaction
- `TriggeredEvent` - Trigger activation
- `SuccessEvent` - Completion/success
- `ItemPickedUpEvent` - Item collection

### Player Queries

```verse
# Get all players
AllPlayers := GetPlayspace().GetPlayers()

# Get player's character
if (FortChar := Agent.GetFortCharacter[]):
    # Manipulate character

# Get player's team
if (Team := FortChar.GetTeam[]):
    TeamIndex := Team.GetTeamIndex()
```

### Concurrency

```verse
# Spawn asynchronous task
spawn:
    AsyncTask()

# Suspend execution
Sleep(DurationSeconds)

# Wait for condition
sync:
    loop:
        if (Condition):
            break
        Sleep(0.1)
```

---

## Type System

### Primitive Types
- `int` - Integer numbers
- `float` - Floating-point numbers
- `logic` - Boolean (true/false)
- `string` - Text strings

### Collections
- `[]T` - Arrays (e.g., `[]agent`, `[]int`)
- `[K]V` - Maps (e.g., `[agent]int`, `[string]float`)

### Optional Types
- `?T` - Optional value (may be false)
- Example: `?agent`, `?int`

### Spatial Types
- `vector3{X, Y, Z}` - 3D position
- `rotation{}` - 3D rotation
- `transform{}` - Position + rotation

---

## Effect Modifiers

Functions can have effect modifiers that indicate their behavior:

- `<suspends>` - May suspend execution (async)
- `<decides>` - May succeed or fail
- `<transacts>` - Reads/writes game state
- `<reads>` - Reads game state (no writes)
- `<native>` - Native engine implementation
- `<public>` - Public API
- `<override>` - Overrides base class

---

## Example Workflows

### Creating a Button Handler

```verse
button_handler := class(creative_device):
    @editable
    TriggerButton: button_device = button_device{}

    OnBegin<override>()<suspends>:void=
        TriggerButton.InteractedWithEvent.Subscribe(HandlePress)

    HandlePress(Agent:agent):void=
        Print("Button pressed by {Agent}")
```

### Managing Scores

```verse
score_tracker := class(creative_device):
    @editable
    ScoreManager: score_manager_device = score_manager_device{}

    var PlayerScores: [agent]int = map{}

    AddScore(Player:agent, Points:int):void=
        CurrentScore := if (Score := PlayerScores[Player]?) then Score else 0
        set PlayerScores[Player] = CurrentScore + Points
```

### Spawning Items

```verse
item_manager := class(creative_device):
    @editable
    ItemSpawner: item_spawner_device = item_spawner_device{}

    SpawnItem():void=
        ItemSpawner.Enable()

    StopSpawning():void=
        ItemSpawner.Disable()
```

---

## Next Steps

1. **Explore Templates**: Check `VerseTemplates/` for ready-to-use code templates
2. **Query API**: Use `verse_knowledge_base.py` to search for specific classes/functions
3. **Generate Code**: Use templates + API knowledge base for code generation

For detailed class documentation, use the knowledge base query tool:

```bash
python Python/verse_knowledge_base.py VerseParsed/fortnite_api.json
```

---

*Generated by Verse Knowledge Base - Phase 2*
