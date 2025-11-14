using { /Fortnite.com/Devices }
using { /Fortnite.com/Characters }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/Diagnostics }

# Wave-based enemy spawning
# Template: Item/Prop Spawner Device
# Handles spawning items, props, or NPCs at specified locations
# Generated: 2025-11-13 18:47:14

wave_spawner := class(creative_device):

    @editable
    EnemySpawner: item_spawner_device = item_spawner_device{}

    @editable
    SpawnDelay<private>:float = 0.5

    @editable
    MaxSpawns<private>:int = 50

    var CurrentSpawnCount<private>:int = 0
    var IsSpawningActive<private>:logic = false

    # Called when the device is started in a running game
    OnBegin<override>()<suspends>:void=
        # Subscribe to spawner events
        EnemySpawner.ItemPickedUpEvent.Subscribe(OnItemPickedUp)
        EnemySpawner.ItemSpawnedEvent.Subscribe(OnItemSpawned)

        Print("wave_spawner initialized")

    # Start spawning items
    StartSpawning()<suspends>:void=
        set IsSpawningActive = true
        Print("Spawning started")

    # Stop spawning items
    StopSpawning():void=
        set IsSpawningActive = false
        EnemySpawner.Disable()
        Print("Spawning stopped")

    # Spawn a single item
    SpawnItem():void=
        if (CurrentSpawnCount < MaxSpawns or MaxSpawns = -1):
            EnemySpawner.Enable()
            set CurrentSpawnCount = CurrentSpawnCount + 1
            Print("Item spawned (count: {CurrentSpawnCount})")

        else:
            Print("Max spawns reached")
            StopSpawning()

    # Continuous spawning loop
    ContinuousSpawnLoop()<suspends>:void=
        loop:
            if (not IsSpawningActive):
                break

            SpawnItem()
            Sleep(SpawnDelay)

    # Handles item picked up event
    OnItemPickedUp(Agent:agent):void=
        Print("{Agent} picked up item")

    # Handles item spawned event
    OnItemSpawned():void=
        Print("Item spawned")

    # Reset spawner
    ResetSpawner():void=
        set CurrentSpawnCount = 0
        set IsSpawningActive = false
        
        Print("Spawner reset")