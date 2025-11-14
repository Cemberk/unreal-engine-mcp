using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/SpatialMath }
using { /UnrealEngine.com/Temporary/Diagnostics }

# DemoLevel Level Spawner
# Generated: 2025-11-13 18:54:56
# Total Actors: 2

DemoLevel_spawner := class(creative_device):

    @editable
    StaticMeshActor_Spawners<private>: []item_spawner_device = array{}

    # Called when the device is started in a running game
    OnBegin<override>()<suspends>:void=
        Print("Level spawner initialized")

        # Spawn all actors
        SpawnAllActors()

    # Spawn all actors from the level
    SpawnAllActors():void=
        SpawnStaticMeshActorActors()

    # Spawn 2 StaticMeshActor actor(s)
    SpawnStaticMeshActorActors():void=
        # Actor 1: Floor_1
        Location_0 := vector3{X:=0.00, Y:=0.00, Z:=0.00}
        Rotation_0 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_0 with Rotation_0
        # SpawnerDevice.SpawnProp(Location_0, Rotation_0)

        # Actor 2: Wall_1
        Location_1 := vector3{X:=400.00, Y:=0.00, Z:=0.00}
        Rotation_1 := rotation{Pitch:=0.00, Yaw:=90.00, Roll:=0.00}
        # Spawn actor at Location_1 with Rotation_1
        # SpawnerDevice.SpawnProp(Location_1, Rotation_1)

