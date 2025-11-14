using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/SpatialMath }
using { /UnrealEngine.com/Temporary/Diagnostics }

# MedievalCastle Level Spawner
# Generated: 2025-11-13 18:59:47
# Total Actors: 197

MedievalCastle_spawner := class(creative_device):

    @editable
    StaticMeshActor_Spawners<private>: []item_spawner_device = array{}
    @editable
    PointLight_Spawners<private>: []item_spawner_device = array{}

    # Called when the device is started in a running game
    OnBegin<override>()<suspends>:void=
        Print("Level spawner initialized")

        # Spawn all actors
        SpawnAllActors()

    # Spawn all actors from the level
    SpawnAllActors():void=
        SpawnStaticMeshActorActors()
        SpawnPointLightActors()

    # Spawn 181 StaticMeshActor actor(s)
    SpawnStaticMeshActorActors():void=
        # Actor 1: Floor_0_0
        Location_0 := vector3{X:=0.00, Y:=0.00, Z:=0.00}
        Rotation_0 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_0 with Rotation_0
        # SpawnerDevice.SpawnProp(Location_0, Rotation_0)

        # Actor 2: Floor_0_1
        Location_1 := vector3{X:=0.00, Y:=400.00, Z:=0.00}
        Rotation_1 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_1 with Rotation_1
        # SpawnerDevice.SpawnProp(Location_1, Rotation_1)

        # Actor 3: Floor_0_2
        Location_2 := vector3{X:=0.00, Y:=800.00, Z:=0.00}
        Rotation_2 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_2 with Rotation_2
        # SpawnerDevice.SpawnProp(Location_2, Rotation_2)

        # Actor 4: Floor_0_3
        Location_3 := vector3{X:=0.00, Y:=1200.00, Z:=0.00}
        Rotation_3 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_3 with Rotation_3
        # SpawnerDevice.SpawnProp(Location_3, Rotation_3)

        # Actor 5: Floor_0_4
        Location_4 := vector3{X:=0.00, Y:=1600.00, Z:=0.00}
        Rotation_4 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_4 with Rotation_4
        # SpawnerDevice.SpawnProp(Location_4, Rotation_4)

        # Actor 6: Floor_0_5
        Location_5 := vector3{X:=0.00, Y:=2000.00, Z:=0.00}
        Rotation_5 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_5 with Rotation_5
        # SpawnerDevice.SpawnProp(Location_5, Rotation_5)

        # Actor 7: Floor_0_6
        Location_6 := vector3{X:=0.00, Y:=2400.00, Z:=0.00}
        Rotation_6 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_6 with Rotation_6
        # SpawnerDevice.SpawnProp(Location_6, Rotation_6)

        # Actor 8: Floor_0_7
        Location_7 := vector3{X:=0.00, Y:=2800.00, Z:=0.00}
        Rotation_7 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_7 with Rotation_7
        # SpawnerDevice.SpawnProp(Location_7, Rotation_7)

        # Actor 9: Floor_0_8
        Location_8 := vector3{X:=0.00, Y:=3200.00, Z:=0.00}
        Rotation_8 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_8 with Rotation_8
        # SpawnerDevice.SpawnProp(Location_8, Rotation_8)

        # Actor 10: Floor_0_9
        Location_9 := vector3{X:=0.00, Y:=3600.00, Z:=0.00}
        Rotation_9 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_9 with Rotation_9
        # SpawnerDevice.SpawnProp(Location_9, Rotation_9)

        # Actor 11: Floor_1_0
        Location_10 := vector3{X:=400.00, Y:=0.00, Z:=0.00}
        Rotation_10 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_10 with Rotation_10
        # SpawnerDevice.SpawnProp(Location_10, Rotation_10)

        # Actor 12: Floor_1_1
        Location_11 := vector3{X:=400.00, Y:=400.00, Z:=0.00}
        Rotation_11 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_11 with Rotation_11
        # SpawnerDevice.SpawnProp(Location_11, Rotation_11)

        # Actor 13: Floor_1_2
        Location_12 := vector3{X:=400.00, Y:=800.00, Z:=0.00}
        Rotation_12 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_12 with Rotation_12
        # SpawnerDevice.SpawnProp(Location_12, Rotation_12)

        # Actor 14: Floor_1_3
        Location_13 := vector3{X:=400.00, Y:=1200.00, Z:=0.00}
        Rotation_13 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_13 with Rotation_13
        # SpawnerDevice.SpawnProp(Location_13, Rotation_13)

        # Actor 15: Floor_1_4
        Location_14 := vector3{X:=400.00, Y:=1600.00, Z:=0.00}
        Rotation_14 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_14 with Rotation_14
        # SpawnerDevice.SpawnProp(Location_14, Rotation_14)

        # Actor 16: Floor_1_5
        Location_15 := vector3{X:=400.00, Y:=2000.00, Z:=0.00}
        Rotation_15 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_15 with Rotation_15
        # SpawnerDevice.SpawnProp(Location_15, Rotation_15)

        # Actor 17: Floor_1_6
        Location_16 := vector3{X:=400.00, Y:=2400.00, Z:=0.00}
        Rotation_16 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_16 with Rotation_16
        # SpawnerDevice.SpawnProp(Location_16, Rotation_16)

        # Actor 18: Floor_1_7
        Location_17 := vector3{X:=400.00, Y:=2800.00, Z:=0.00}
        Rotation_17 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_17 with Rotation_17
        # SpawnerDevice.SpawnProp(Location_17, Rotation_17)

        # Actor 19: Floor_1_8
        Location_18 := vector3{X:=400.00, Y:=3200.00, Z:=0.00}
        Rotation_18 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_18 with Rotation_18
        # SpawnerDevice.SpawnProp(Location_18, Rotation_18)

        # Actor 20: Floor_1_9
        Location_19 := vector3{X:=400.00, Y:=3600.00, Z:=0.00}
        Rotation_19 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_19 with Rotation_19
        # SpawnerDevice.SpawnProp(Location_19, Rotation_19)

        # Actor 21: Floor_2_0
        Location_20 := vector3{X:=800.00, Y:=0.00, Z:=0.00}
        Rotation_20 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_20 with Rotation_20
        # SpawnerDevice.SpawnProp(Location_20, Rotation_20)

        # Actor 22: Floor_2_1
        Location_21 := vector3{X:=800.00, Y:=400.00, Z:=0.00}
        Rotation_21 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_21 with Rotation_21
        # SpawnerDevice.SpawnProp(Location_21, Rotation_21)

        # Actor 23: Floor_2_2
        Location_22 := vector3{X:=800.00, Y:=800.00, Z:=0.00}
        Rotation_22 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_22 with Rotation_22
        # SpawnerDevice.SpawnProp(Location_22, Rotation_22)

        # Actor 24: Floor_2_3
        Location_23 := vector3{X:=800.00, Y:=1200.00, Z:=0.00}
        Rotation_23 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_23 with Rotation_23
        # SpawnerDevice.SpawnProp(Location_23, Rotation_23)

        # Actor 25: Floor_2_4
        Location_24 := vector3{X:=800.00, Y:=1600.00, Z:=0.00}
        Rotation_24 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_24 with Rotation_24
        # SpawnerDevice.SpawnProp(Location_24, Rotation_24)

        # Actor 26: Floor_2_5
        Location_25 := vector3{X:=800.00, Y:=2000.00, Z:=0.00}
        Rotation_25 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_25 with Rotation_25
        # SpawnerDevice.SpawnProp(Location_25, Rotation_25)

        # Actor 27: Floor_2_6
        Location_26 := vector3{X:=800.00, Y:=2400.00, Z:=0.00}
        Rotation_26 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_26 with Rotation_26
        # SpawnerDevice.SpawnProp(Location_26, Rotation_26)

        # Actor 28: Floor_2_7
        Location_27 := vector3{X:=800.00, Y:=2800.00, Z:=0.00}
        Rotation_27 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_27 with Rotation_27
        # SpawnerDevice.SpawnProp(Location_27, Rotation_27)

        # Actor 29: Floor_2_8
        Location_28 := vector3{X:=800.00, Y:=3200.00, Z:=0.00}
        Rotation_28 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_28 with Rotation_28
        # SpawnerDevice.SpawnProp(Location_28, Rotation_28)

        # Actor 30: Floor_2_9
        Location_29 := vector3{X:=800.00, Y:=3600.00, Z:=0.00}
        Rotation_29 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_29 with Rotation_29
        # SpawnerDevice.SpawnProp(Location_29, Rotation_29)

        # Actor 31: Floor_3_0
        Location_30 := vector3{X:=1200.00, Y:=0.00, Z:=0.00}
        Rotation_30 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_30 with Rotation_30
        # SpawnerDevice.SpawnProp(Location_30, Rotation_30)

        # Actor 32: Floor_3_1
        Location_31 := vector3{X:=1200.00, Y:=400.00, Z:=0.00}
        Rotation_31 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_31 with Rotation_31
        # SpawnerDevice.SpawnProp(Location_31, Rotation_31)

        # Actor 33: Floor_3_2
        Location_32 := vector3{X:=1200.00, Y:=800.00, Z:=0.00}
        Rotation_32 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_32 with Rotation_32
        # SpawnerDevice.SpawnProp(Location_32, Rotation_32)

        # Actor 34: Floor_3_3
        Location_33 := vector3{X:=1200.00, Y:=1200.00, Z:=0.00}
        Rotation_33 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_33 with Rotation_33
        # SpawnerDevice.SpawnProp(Location_33, Rotation_33)

        # Actor 35: Floor_3_4
        Location_34 := vector3{X:=1200.00, Y:=1600.00, Z:=0.00}
        Rotation_34 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_34 with Rotation_34
        # SpawnerDevice.SpawnProp(Location_34, Rotation_34)

        # Actor 36: Floor_3_5
        Location_35 := vector3{X:=1200.00, Y:=2000.00, Z:=0.00}
        Rotation_35 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_35 with Rotation_35
        # SpawnerDevice.SpawnProp(Location_35, Rotation_35)

        # Actor 37: Floor_3_6
        Location_36 := vector3{X:=1200.00, Y:=2400.00, Z:=0.00}
        Rotation_36 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_36 with Rotation_36
        # SpawnerDevice.SpawnProp(Location_36, Rotation_36)

        # Actor 38: Floor_3_7
        Location_37 := vector3{X:=1200.00, Y:=2800.00, Z:=0.00}
        Rotation_37 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_37 with Rotation_37
        # SpawnerDevice.SpawnProp(Location_37, Rotation_37)

        # Actor 39: Floor_3_8
        Location_38 := vector3{X:=1200.00, Y:=3200.00, Z:=0.00}
        Rotation_38 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_38 with Rotation_38
        # SpawnerDevice.SpawnProp(Location_38, Rotation_38)

        # Actor 40: Floor_3_9
        Location_39 := vector3{X:=1200.00, Y:=3600.00, Z:=0.00}
        Rotation_39 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_39 with Rotation_39
        # SpawnerDevice.SpawnProp(Location_39, Rotation_39)

        # Actor 41: Floor_4_0
        Location_40 := vector3{X:=1600.00, Y:=0.00, Z:=0.00}
        Rotation_40 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_40 with Rotation_40
        # SpawnerDevice.SpawnProp(Location_40, Rotation_40)

        # Actor 42: Floor_4_1
        Location_41 := vector3{X:=1600.00, Y:=400.00, Z:=0.00}
        Rotation_41 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_41 with Rotation_41
        # SpawnerDevice.SpawnProp(Location_41, Rotation_41)

        # Actor 43: Floor_4_2
        Location_42 := vector3{X:=1600.00, Y:=800.00, Z:=0.00}
        Rotation_42 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_42 with Rotation_42
        # SpawnerDevice.SpawnProp(Location_42, Rotation_42)

        # Actor 44: Floor_4_3
        Location_43 := vector3{X:=1600.00, Y:=1200.00, Z:=0.00}
        Rotation_43 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_43 with Rotation_43
        # SpawnerDevice.SpawnProp(Location_43, Rotation_43)

        # Actor 45: Floor_4_4
        Location_44 := vector3{X:=1600.00, Y:=1600.00, Z:=0.00}
        Rotation_44 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_44 with Rotation_44
        # SpawnerDevice.SpawnProp(Location_44, Rotation_44)

        # Actor 46: Floor_4_5
        Location_45 := vector3{X:=1600.00, Y:=2000.00, Z:=0.00}
        Rotation_45 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_45 with Rotation_45
        # SpawnerDevice.SpawnProp(Location_45, Rotation_45)

        # Actor 47: Floor_4_6
        Location_46 := vector3{X:=1600.00, Y:=2400.00, Z:=0.00}
        Rotation_46 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_46 with Rotation_46
        # SpawnerDevice.SpawnProp(Location_46, Rotation_46)

        # Actor 48: Floor_4_7
        Location_47 := vector3{X:=1600.00, Y:=2800.00, Z:=0.00}
        Rotation_47 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_47 with Rotation_47
        # SpawnerDevice.SpawnProp(Location_47, Rotation_47)

        # Actor 49: Floor_4_8
        Location_48 := vector3{X:=1600.00, Y:=3200.00, Z:=0.00}
        Rotation_48 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_48 with Rotation_48
        # SpawnerDevice.SpawnProp(Location_48, Rotation_48)

        # Actor 50: Floor_4_9
        Location_49 := vector3{X:=1600.00, Y:=3600.00, Z:=0.00}
        Rotation_49 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_49 with Rotation_49
        # SpawnerDevice.SpawnProp(Location_49, Rotation_49)

        # Actor 51: Floor_5_0
        Location_50 := vector3{X:=2000.00, Y:=0.00, Z:=0.00}
        Rotation_50 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_50 with Rotation_50
        # SpawnerDevice.SpawnProp(Location_50, Rotation_50)

        # Actor 52: Floor_5_1
        Location_51 := vector3{X:=2000.00, Y:=400.00, Z:=0.00}
        Rotation_51 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_51 with Rotation_51
        # SpawnerDevice.SpawnProp(Location_51, Rotation_51)

        # Actor 53: Floor_5_2
        Location_52 := vector3{X:=2000.00, Y:=800.00, Z:=0.00}
        Rotation_52 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_52 with Rotation_52
        # SpawnerDevice.SpawnProp(Location_52, Rotation_52)

        # Actor 54: Floor_5_3
        Location_53 := vector3{X:=2000.00, Y:=1200.00, Z:=0.00}
        Rotation_53 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_53 with Rotation_53
        # SpawnerDevice.SpawnProp(Location_53, Rotation_53)

        # Actor 55: Floor_5_4
        Location_54 := vector3{X:=2000.00, Y:=1600.00, Z:=0.00}
        Rotation_54 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_54 with Rotation_54
        # SpawnerDevice.SpawnProp(Location_54, Rotation_54)

        # Actor 56: Floor_5_5
        Location_55 := vector3{X:=2000.00, Y:=2000.00, Z:=0.00}
        Rotation_55 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_55 with Rotation_55
        # SpawnerDevice.SpawnProp(Location_55, Rotation_55)

        # Actor 57: Floor_5_6
        Location_56 := vector3{X:=2000.00, Y:=2400.00, Z:=0.00}
        Rotation_56 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_56 with Rotation_56
        # SpawnerDevice.SpawnProp(Location_56, Rotation_56)

        # Actor 58: Floor_5_7
        Location_57 := vector3{X:=2000.00, Y:=2800.00, Z:=0.00}
        Rotation_57 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_57 with Rotation_57
        # SpawnerDevice.SpawnProp(Location_57, Rotation_57)

        # Actor 59: Floor_5_8
        Location_58 := vector3{X:=2000.00, Y:=3200.00, Z:=0.00}
        Rotation_58 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_58 with Rotation_58
        # SpawnerDevice.SpawnProp(Location_58, Rotation_58)

        # Actor 60: Floor_5_9
        Location_59 := vector3{X:=2000.00, Y:=3600.00, Z:=0.00}
        Rotation_59 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_59 with Rotation_59
        # SpawnerDevice.SpawnProp(Location_59, Rotation_59)

        # Actor 61: Floor_6_0
        Location_60 := vector3{X:=2400.00, Y:=0.00, Z:=0.00}
        Rotation_60 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_60 with Rotation_60
        # SpawnerDevice.SpawnProp(Location_60, Rotation_60)

        # Actor 62: Floor_6_1
        Location_61 := vector3{X:=2400.00, Y:=400.00, Z:=0.00}
        Rotation_61 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_61 with Rotation_61
        # SpawnerDevice.SpawnProp(Location_61, Rotation_61)

        # Actor 63: Floor_6_2
        Location_62 := vector3{X:=2400.00, Y:=800.00, Z:=0.00}
        Rotation_62 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_62 with Rotation_62
        # SpawnerDevice.SpawnProp(Location_62, Rotation_62)

        # Actor 64: Floor_6_3
        Location_63 := vector3{X:=2400.00, Y:=1200.00, Z:=0.00}
        Rotation_63 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_63 with Rotation_63
        # SpawnerDevice.SpawnProp(Location_63, Rotation_63)

        # Actor 65: Floor_6_4
        Location_64 := vector3{X:=2400.00, Y:=1600.00, Z:=0.00}
        Rotation_64 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_64 with Rotation_64
        # SpawnerDevice.SpawnProp(Location_64, Rotation_64)

        # Actor 66: Floor_6_5
        Location_65 := vector3{X:=2400.00, Y:=2000.00, Z:=0.00}
        Rotation_65 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_65 with Rotation_65
        # SpawnerDevice.SpawnProp(Location_65, Rotation_65)

        # Actor 67: Floor_6_6
        Location_66 := vector3{X:=2400.00, Y:=2400.00, Z:=0.00}
        Rotation_66 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_66 with Rotation_66
        # SpawnerDevice.SpawnProp(Location_66, Rotation_66)

        # Actor 68: Floor_6_7
        Location_67 := vector3{X:=2400.00, Y:=2800.00, Z:=0.00}
        Rotation_67 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_67 with Rotation_67
        # SpawnerDevice.SpawnProp(Location_67, Rotation_67)

        # Actor 69: Floor_6_8
        Location_68 := vector3{X:=2400.00, Y:=3200.00, Z:=0.00}
        Rotation_68 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_68 with Rotation_68
        # SpawnerDevice.SpawnProp(Location_68, Rotation_68)

        # Actor 70: Floor_6_9
        Location_69 := vector3{X:=2400.00, Y:=3600.00, Z:=0.00}
        Rotation_69 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_69 with Rotation_69
        # SpawnerDevice.SpawnProp(Location_69, Rotation_69)

        # Actor 71: Floor_7_0
        Location_70 := vector3{X:=2800.00, Y:=0.00, Z:=0.00}
        Rotation_70 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_70 with Rotation_70
        # SpawnerDevice.SpawnProp(Location_70, Rotation_70)

        # Actor 72: Floor_7_1
        Location_71 := vector3{X:=2800.00, Y:=400.00, Z:=0.00}
        Rotation_71 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_71 with Rotation_71
        # SpawnerDevice.SpawnProp(Location_71, Rotation_71)

        # Actor 73: Floor_7_2
        Location_72 := vector3{X:=2800.00, Y:=800.00, Z:=0.00}
        Rotation_72 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_72 with Rotation_72
        # SpawnerDevice.SpawnProp(Location_72, Rotation_72)

        # Actor 74: Floor_7_3
        Location_73 := vector3{X:=2800.00, Y:=1200.00, Z:=0.00}
        Rotation_73 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_73 with Rotation_73
        # SpawnerDevice.SpawnProp(Location_73, Rotation_73)

        # Actor 75: Floor_7_4
        Location_74 := vector3{X:=2800.00, Y:=1600.00, Z:=0.00}
        Rotation_74 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_74 with Rotation_74
        # SpawnerDevice.SpawnProp(Location_74, Rotation_74)

        # Actor 76: Floor_7_5
        Location_75 := vector3{X:=2800.00, Y:=2000.00, Z:=0.00}
        Rotation_75 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_75 with Rotation_75
        # SpawnerDevice.SpawnProp(Location_75, Rotation_75)

        # Actor 77: Floor_7_6
        Location_76 := vector3{X:=2800.00, Y:=2400.00, Z:=0.00}
        Rotation_76 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_76 with Rotation_76
        # SpawnerDevice.SpawnProp(Location_76, Rotation_76)

        # Actor 78: Floor_7_7
        Location_77 := vector3{X:=2800.00, Y:=2800.00, Z:=0.00}
        Rotation_77 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_77 with Rotation_77
        # SpawnerDevice.SpawnProp(Location_77, Rotation_77)

        # Actor 79: Floor_7_8
        Location_78 := vector3{X:=2800.00, Y:=3200.00, Z:=0.00}
        Rotation_78 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_78 with Rotation_78
        # SpawnerDevice.SpawnProp(Location_78, Rotation_78)

        # Actor 80: Floor_7_9
        Location_79 := vector3{X:=2800.00, Y:=3600.00, Z:=0.00}
        Rotation_79 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_79 with Rotation_79
        # SpawnerDevice.SpawnProp(Location_79, Rotation_79)

        # Actor 81: Floor_8_0
        Location_80 := vector3{X:=3200.00, Y:=0.00, Z:=0.00}
        Rotation_80 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_80 with Rotation_80
        # SpawnerDevice.SpawnProp(Location_80, Rotation_80)

        # Actor 82: Floor_8_1
        Location_81 := vector3{X:=3200.00, Y:=400.00, Z:=0.00}
        Rotation_81 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_81 with Rotation_81
        # SpawnerDevice.SpawnProp(Location_81, Rotation_81)

        # Actor 83: Floor_8_2
        Location_82 := vector3{X:=3200.00, Y:=800.00, Z:=0.00}
        Rotation_82 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_82 with Rotation_82
        # SpawnerDevice.SpawnProp(Location_82, Rotation_82)

        # Actor 84: Floor_8_3
        Location_83 := vector3{X:=3200.00, Y:=1200.00, Z:=0.00}
        Rotation_83 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_83 with Rotation_83
        # SpawnerDevice.SpawnProp(Location_83, Rotation_83)

        # Actor 85: Floor_8_4
        Location_84 := vector3{X:=3200.00, Y:=1600.00, Z:=0.00}
        Rotation_84 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_84 with Rotation_84
        # SpawnerDevice.SpawnProp(Location_84, Rotation_84)

        # Actor 86: Floor_8_5
        Location_85 := vector3{X:=3200.00, Y:=2000.00, Z:=0.00}
        Rotation_85 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_85 with Rotation_85
        # SpawnerDevice.SpawnProp(Location_85, Rotation_85)

        # Actor 87: Floor_8_6
        Location_86 := vector3{X:=3200.00, Y:=2400.00, Z:=0.00}
        Rotation_86 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_86 with Rotation_86
        # SpawnerDevice.SpawnProp(Location_86, Rotation_86)

        # Actor 88: Floor_8_7
        Location_87 := vector3{X:=3200.00, Y:=2800.00, Z:=0.00}
        Rotation_87 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_87 with Rotation_87
        # SpawnerDevice.SpawnProp(Location_87, Rotation_87)

        # Actor 89: Floor_8_8
        Location_88 := vector3{X:=3200.00, Y:=3200.00, Z:=0.00}
        Rotation_88 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_88 with Rotation_88
        # SpawnerDevice.SpawnProp(Location_88, Rotation_88)

        # Actor 90: Floor_8_9
        Location_89 := vector3{X:=3200.00, Y:=3600.00, Z:=0.00}
        Rotation_89 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_89 with Rotation_89
        # SpawnerDevice.SpawnProp(Location_89, Rotation_89)

        # Actor 91: Floor_9_0
        Location_90 := vector3{X:=3600.00, Y:=0.00, Z:=0.00}
        Rotation_90 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_90 with Rotation_90
        # SpawnerDevice.SpawnProp(Location_90, Rotation_90)

        # Actor 92: Floor_9_1
        Location_91 := vector3{X:=3600.00, Y:=400.00, Z:=0.00}
        Rotation_91 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_91 with Rotation_91
        # SpawnerDevice.SpawnProp(Location_91, Rotation_91)

        # Actor 93: Floor_9_2
        Location_92 := vector3{X:=3600.00, Y:=800.00, Z:=0.00}
        Rotation_92 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_92 with Rotation_92
        # SpawnerDevice.SpawnProp(Location_92, Rotation_92)

        # Actor 94: Floor_9_3
        Location_93 := vector3{X:=3600.00, Y:=1200.00, Z:=0.00}
        Rotation_93 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_93 with Rotation_93
        # SpawnerDevice.SpawnProp(Location_93, Rotation_93)

        # Actor 95: Floor_9_4
        Location_94 := vector3{X:=3600.00, Y:=1600.00, Z:=0.00}
        Rotation_94 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_94 with Rotation_94
        # SpawnerDevice.SpawnProp(Location_94, Rotation_94)

        # Actor 96: Floor_9_5
        Location_95 := vector3{X:=3600.00, Y:=2000.00, Z:=0.00}
        Rotation_95 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_95 with Rotation_95
        # SpawnerDevice.SpawnProp(Location_95, Rotation_95)

        # Actor 97: Floor_9_6
        Location_96 := vector3{X:=3600.00, Y:=2400.00, Z:=0.00}
        Rotation_96 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_96 with Rotation_96
        # SpawnerDevice.SpawnProp(Location_96, Rotation_96)

        # Actor 98: Floor_9_7
        Location_97 := vector3{X:=3600.00, Y:=2800.00, Z:=0.00}
        Rotation_97 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_97 with Rotation_97
        # SpawnerDevice.SpawnProp(Location_97, Rotation_97)

        # Actor 99: Floor_9_8
        Location_98 := vector3{X:=3600.00, Y:=3200.00, Z:=0.00}
        Rotation_98 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_98 with Rotation_98
        # SpawnerDevice.SpawnProp(Location_98, Rotation_98)

        # Actor 100: Floor_9_9
        Location_99 := vector3{X:=3600.00, Y:=3600.00, Z:=0.00}
        Rotation_99 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_99 with Rotation_99
        # SpawnerDevice.SpawnProp(Location_99, Rotation_99)

        # Actor 101: Wall_North_0
        Location_100 := vector3{X:=0.00, Y:=0.00, Z:=0.00}
        Rotation_100 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_100 with Rotation_100
        # SpawnerDevice.SpawnProp(Location_100, Rotation_100)

        # Actor 102: Wall_South_1
        Location_101 := vector3{X:=0.00, Y:=4000.00, Z:=0.00}
        Rotation_101 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_101 with Rotation_101
        # SpawnerDevice.SpawnProp(Location_101, Rotation_101)

        # Actor 103: Wall_North_2
        Location_102 := vector3{X:=400.00, Y:=0.00, Z:=0.00}
        Rotation_102 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_102 with Rotation_102
        # SpawnerDevice.SpawnProp(Location_102, Rotation_102)

        # Actor 104: Wall_South_3
        Location_103 := vector3{X:=400.00, Y:=4000.00, Z:=0.00}
        Rotation_103 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_103 with Rotation_103
        # SpawnerDevice.SpawnProp(Location_103, Rotation_103)

        # Actor 105: Wall_North_4
        Location_104 := vector3{X:=800.00, Y:=0.00, Z:=0.00}
        Rotation_104 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_104 with Rotation_104
        # SpawnerDevice.SpawnProp(Location_104, Rotation_104)

        # Actor 106: Wall_South_5
        Location_105 := vector3{X:=800.00, Y:=4000.00, Z:=0.00}
        Rotation_105 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_105 with Rotation_105
        # SpawnerDevice.SpawnProp(Location_105, Rotation_105)

        # Actor 107: Wall_North_6
        Location_106 := vector3{X:=1200.00, Y:=0.00, Z:=0.00}
        Rotation_106 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_106 with Rotation_106
        # SpawnerDevice.SpawnProp(Location_106, Rotation_106)

        # Actor 108: Wall_South_7
        Location_107 := vector3{X:=1200.00, Y:=4000.00, Z:=0.00}
        Rotation_107 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_107 with Rotation_107
        # SpawnerDevice.SpawnProp(Location_107, Rotation_107)

        # Actor 109: Wall_North_8
        Location_108 := vector3{X:=1600.00, Y:=0.00, Z:=0.00}
        Rotation_108 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_108 with Rotation_108
        # SpawnerDevice.SpawnProp(Location_108, Rotation_108)

        # Actor 110: Wall_South_9
        Location_109 := vector3{X:=1600.00, Y:=4000.00, Z:=0.00}
        Rotation_109 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_109 with Rotation_109
        # SpawnerDevice.SpawnProp(Location_109, Rotation_109)

        # Actor 111: Wall_North_10
        Location_110 := vector3{X:=2000.00, Y:=0.00, Z:=0.00}
        Rotation_110 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_110 with Rotation_110
        # SpawnerDevice.SpawnProp(Location_110, Rotation_110)

        # Actor 112: Wall_South_11
        Location_111 := vector3{X:=2000.00, Y:=4000.00, Z:=0.00}
        Rotation_111 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_111 with Rotation_111
        # SpawnerDevice.SpawnProp(Location_111, Rotation_111)

        # Actor 113: Wall_North_12
        Location_112 := vector3{X:=2400.00, Y:=0.00, Z:=0.00}
        Rotation_112 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_112 with Rotation_112
        # SpawnerDevice.SpawnProp(Location_112, Rotation_112)

        # Actor 114: Wall_South_13
        Location_113 := vector3{X:=2400.00, Y:=4000.00, Z:=0.00}
        Rotation_113 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_113 with Rotation_113
        # SpawnerDevice.SpawnProp(Location_113, Rotation_113)

        # Actor 115: Wall_North_14
        Location_114 := vector3{X:=2800.00, Y:=0.00, Z:=0.00}
        Rotation_114 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_114 with Rotation_114
        # SpawnerDevice.SpawnProp(Location_114, Rotation_114)

        # Actor 116: Wall_South_15
        Location_115 := vector3{X:=2800.00, Y:=4000.00, Z:=0.00}
        Rotation_115 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_115 with Rotation_115
        # SpawnerDevice.SpawnProp(Location_115, Rotation_115)

        # Actor 117: Wall_North_16
        Location_116 := vector3{X:=3200.00, Y:=0.00, Z:=0.00}
        Rotation_116 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_116 with Rotation_116
        # SpawnerDevice.SpawnProp(Location_116, Rotation_116)

        # Actor 118: Wall_South_17
        Location_117 := vector3{X:=3200.00, Y:=4000.00, Z:=0.00}
        Rotation_117 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_117 with Rotation_117
        # SpawnerDevice.SpawnProp(Location_117, Rotation_117)

        # Actor 119: Wall_North_18
        Location_118 := vector3{X:=3600.00, Y:=0.00, Z:=0.00}
        Rotation_118 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_118 with Rotation_118
        # SpawnerDevice.SpawnProp(Location_118, Rotation_118)

        # Actor 120: Wall_South_19
        Location_119 := vector3{X:=3600.00, Y:=4000.00, Z:=0.00}
        Rotation_119 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_119 with Rotation_119
        # SpawnerDevice.SpawnProp(Location_119, Rotation_119)

        # Actor 121: Wall_West_20
        Location_120 := vector3{X:=0.00, Y:=400.00, Z:=0.00}
        Rotation_120 := rotation{Pitch:=0.00, Yaw:=270.00, Roll:=0.00}
        # Spawn actor at Location_120 with Rotation_120
        # SpawnerDevice.SpawnProp(Location_120, Rotation_120)

        # Actor 122: Wall_East_21
        Location_121 := vector3{X:=4000.00, Y:=400.00, Z:=0.00}
        Rotation_121 := rotation{Pitch:=0.00, Yaw:=90.00, Roll:=0.00}
        # Spawn actor at Location_121 with Rotation_121
        # SpawnerDevice.SpawnProp(Location_121, Rotation_121)

        # Actor 123: Wall_West_22
        Location_122 := vector3{X:=0.00, Y:=800.00, Z:=0.00}
        Rotation_122 := rotation{Pitch:=0.00, Yaw:=270.00, Roll:=0.00}
        # Spawn actor at Location_122 with Rotation_122
        # SpawnerDevice.SpawnProp(Location_122, Rotation_122)

        # Actor 124: Wall_East_23
        Location_123 := vector3{X:=4000.00, Y:=800.00, Z:=0.00}
        Rotation_123 := rotation{Pitch:=0.00, Yaw:=90.00, Roll:=0.00}
        # Spawn actor at Location_123 with Rotation_123
        # SpawnerDevice.SpawnProp(Location_123, Rotation_123)

        # Actor 125: Wall_West_24
        Location_124 := vector3{X:=0.00, Y:=1200.00, Z:=0.00}
        Rotation_124 := rotation{Pitch:=0.00, Yaw:=270.00, Roll:=0.00}
        # Spawn actor at Location_124 with Rotation_124
        # SpawnerDevice.SpawnProp(Location_124, Rotation_124)

        # Actor 126: Wall_East_25
        Location_125 := vector3{X:=4000.00, Y:=1200.00, Z:=0.00}
        Rotation_125 := rotation{Pitch:=0.00, Yaw:=90.00, Roll:=0.00}
        # Spawn actor at Location_125 with Rotation_125
        # SpawnerDevice.SpawnProp(Location_125, Rotation_125)

        # Actor 127: Wall_West_26
        Location_126 := vector3{X:=0.00, Y:=1600.00, Z:=0.00}
        Rotation_126 := rotation{Pitch:=0.00, Yaw:=270.00, Roll:=0.00}
        # Spawn actor at Location_126 with Rotation_126
        # SpawnerDevice.SpawnProp(Location_126, Rotation_126)

        # Actor 128: Wall_East_27
        Location_127 := vector3{X:=4000.00, Y:=1600.00, Z:=0.00}
        Rotation_127 := rotation{Pitch:=0.00, Yaw:=90.00, Roll:=0.00}
        # Spawn actor at Location_127 with Rotation_127
        # SpawnerDevice.SpawnProp(Location_127, Rotation_127)

        # Actor 129: Wall_West_28
        Location_128 := vector3{X:=0.00, Y:=2000.00, Z:=0.00}
        Rotation_128 := rotation{Pitch:=0.00, Yaw:=270.00, Roll:=0.00}
        # Spawn actor at Location_128 with Rotation_128
        # SpawnerDevice.SpawnProp(Location_128, Rotation_128)

        # Actor 130: Wall_East_29
        Location_129 := vector3{X:=4000.00, Y:=2000.00, Z:=0.00}
        Rotation_129 := rotation{Pitch:=0.00, Yaw:=90.00, Roll:=0.00}
        # Spawn actor at Location_129 with Rotation_129
        # SpawnerDevice.SpawnProp(Location_129, Rotation_129)

        # Actor 131: Wall_West_30
        Location_130 := vector3{X:=0.00, Y:=2400.00, Z:=0.00}
        Rotation_130 := rotation{Pitch:=0.00, Yaw:=270.00, Roll:=0.00}
        # Spawn actor at Location_130 with Rotation_130
        # SpawnerDevice.SpawnProp(Location_130, Rotation_130)

        # Actor 132: Wall_East_31
        Location_131 := vector3{X:=4000.00, Y:=2400.00, Z:=0.00}
        Rotation_131 := rotation{Pitch:=0.00, Yaw:=90.00, Roll:=0.00}
        # Spawn actor at Location_131 with Rotation_131
        # SpawnerDevice.SpawnProp(Location_131, Rotation_131)

        # Actor 133: Wall_West_32
        Location_132 := vector3{X:=0.00, Y:=2800.00, Z:=0.00}
        Rotation_132 := rotation{Pitch:=0.00, Yaw:=270.00, Roll:=0.00}
        # Spawn actor at Location_132 with Rotation_132
        # SpawnerDevice.SpawnProp(Location_132, Rotation_132)

        # Actor 134: Wall_East_33
        Location_133 := vector3{X:=4000.00, Y:=2800.00, Z:=0.00}
        Rotation_133 := rotation{Pitch:=0.00, Yaw:=90.00, Roll:=0.00}
        # Spawn actor at Location_133 with Rotation_133
        # SpawnerDevice.SpawnProp(Location_133, Rotation_133)

        # Actor 135: Wall_West_34
        Location_134 := vector3{X:=0.00, Y:=3200.00, Z:=0.00}
        Rotation_134 := rotation{Pitch:=0.00, Yaw:=270.00, Roll:=0.00}
        # Spawn actor at Location_134 with Rotation_134
        # SpawnerDevice.SpawnProp(Location_134, Rotation_134)

        # Actor 136: Wall_East_35
        Location_135 := vector3{X:=4000.00, Y:=3200.00, Z:=0.00}
        Rotation_135 := rotation{Pitch:=0.00, Yaw:=90.00, Roll:=0.00}
        # Spawn actor at Location_135 with Rotation_135
        # SpawnerDevice.SpawnProp(Location_135, Rotation_135)

        # Actor 137: Wall_West_36
        Location_136 := vector3{X:=0.00, Y:=3600.00, Z:=0.00}
        Rotation_136 := rotation{Pitch:=0.00, Yaw:=270.00, Roll:=0.00}
        # Spawn actor at Location_136 with Rotation_136
        # SpawnerDevice.SpawnProp(Location_136, Rotation_136)

        # Actor 138: Wall_East_37
        Location_137 := vector3{X:=4000.00, Y:=3600.00, Z:=0.00}
        Rotation_137 := rotation{Pitch:=0.00, Yaw:=90.00, Roll:=0.00}
        # Spawn actor at Location_137 with Rotation_137
        # SpawnerDevice.SpawnProp(Location_137, Rotation_137)

        # Actor 139: Tower_NorthWest
        Location_138 := vector3{X:=0.00, Y:=0.00, Z:=0.00}
        Rotation_138 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_138 with Rotation_138
        # SpawnerDevice.SpawnProp(Location_138, Rotation_138)

        # Actor 140: Tower_NorthEast
        Location_139 := vector3{X:=4000.00, Y:=0.00, Z:=0.00}
        Rotation_139 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_139 with Rotation_139
        # SpawnerDevice.SpawnProp(Location_139, Rotation_139)

        # Actor 141: Tower_SouthWest
        Location_140 := vector3{X:=0.00, Y:=4000.00, Z:=0.00}
        Rotation_140 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_140 with Rotation_140
        # SpawnerDevice.SpawnProp(Location_140, Rotation_140)

        # Actor 142: Tower_SouthEast
        Location_141 := vector3{X:=4000.00, Y:=4000.00, Z:=0.00}
        Rotation_141 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_141 with Rotation_141
        # SpawnerDevice.SpawnProp(Location_141, Rotation_141)

        # Actor 143: Gate_Main
        Location_142 := vector3{X:=2000.00, Y:=0.00, Z:=0.00}
        Rotation_142 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_142 with Rotation_142
        # SpawnerDevice.SpawnProp(Location_142, Rotation_142)

        # Actor 144: Pillar_0_0
        Location_143 := vector3{X:=1200.00, Y:=1200.00, Z:=0.00}
        Rotation_143 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_143 with Rotation_143
        # SpawnerDevice.SpawnProp(Location_143, Rotation_143)

        # Actor 145: Pillar_0_1
        Location_144 := vector3{X:=1200.00, Y:=2000.00, Z:=0.00}
        Rotation_144 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_144 with Rotation_144
        # SpawnerDevice.SpawnProp(Location_144, Rotation_144)

        # Actor 146: Pillar_0_2
        Location_145 := vector3{X:=1200.00, Y:=2800.00, Z:=0.00}
        Rotation_145 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_145 with Rotation_145
        # SpawnerDevice.SpawnProp(Location_145, Rotation_145)

        # Actor 147: Pillar_1_0
        Location_146 := vector3{X:=2000.00, Y:=1200.00, Z:=0.00}
        Rotation_146 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_146 with Rotation_146
        # SpawnerDevice.SpawnProp(Location_146, Rotation_146)

        # Actor 148: Pillar_1_1
        Location_147 := vector3{X:=2000.00, Y:=2000.00, Z:=0.00}
        Rotation_147 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_147 with Rotation_147
        # SpawnerDevice.SpawnProp(Location_147, Rotation_147)

        # Actor 149: Pillar_1_2
        Location_148 := vector3{X:=2000.00, Y:=2800.00, Z:=0.00}
        Rotation_148 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_148 with Rotation_148
        # SpawnerDevice.SpawnProp(Location_148, Rotation_148)

        # Actor 150: Pillar_2_0
        Location_149 := vector3{X:=2800.00, Y:=1200.00, Z:=0.00}
        Rotation_149 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_149 with Rotation_149
        # SpawnerDevice.SpawnProp(Location_149, Rotation_149)

        # Actor 151: Pillar_2_1
        Location_150 := vector3{X:=2800.00, Y:=2000.00, Z:=0.00}
        Rotation_150 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_150 with Rotation_150
        # SpawnerDevice.SpawnProp(Location_150, Rotation_150)

        # Actor 152: Pillar_2_2
        Location_151 := vector3{X:=2800.00, Y:=2800.00, Z:=0.00}
        Rotation_151 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_151 with Rotation_151
        # SpawnerDevice.SpawnProp(Location_151, Rotation_151)

        # Actor 153: Throne
        Location_152 := vector3{X:=2000.00, Y:=3800.00, Z:=50.00}
        Rotation_152 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_152 with Rotation_152
        # SpawnerDevice.SpawnProp(Location_152, Rotation_152)

        # Actor 154: Table_1
        Location_153 := vector3{X:=1500.00, Y:=2000.00, Z:=50.00}
        Rotation_153 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_153 with Rotation_153
        # SpawnerDevice.SpawnProp(Location_153, Rotation_153)

        # Actor 155: Table_2
        Location_154 := vector3{X:=2500.00, Y:=2000.00, Z:=50.00}
        Rotation_154 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_154 with Rotation_154
        # SpawnerDevice.SpawnProp(Location_154, Rotation_154)

        # Actor 156: Banner_1
        Location_155 := vector3{X:=1000.00, Y:=200.00, Z:=50.00}
        Rotation_155 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_155 with Rotation_155
        # SpawnerDevice.SpawnProp(Location_155, Rotation_155)

        # Actor 157: Banner_2
        Location_156 := vector3{X:=3000.00, Y:=200.00, Z:=50.00}
        Rotation_156 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_156 with Rotation_156
        # SpawnerDevice.SpawnProp(Location_156, Rotation_156)

        # Actor 158: Barrel_1
        Location_157 := vector3{X:=500.00, Y:=500.00, Z:=50.00}
        Rotation_157 := rotation{Pitch:=0.00, Yaw:=45.00, Roll:=0.00}
        # Spawn actor at Location_157 with Rotation_157
        # SpawnerDevice.SpawnProp(Location_157, Rotation_157)

        # Actor 159: Barrel_2
        Location_158 := vector3{X:=3500.00, Y:=500.00, Z:=50.00}
        Rotation_158 := rotation{Pitch:=0.00, Yaw:=135.00, Roll:=0.00}
        # Spawn actor at Location_158 with Rotation_158
        # SpawnerDevice.SpawnProp(Location_158, Rotation_158)

        # Actor 160: Chest_Treasure
        Location_159 := vector3{X:=2000.00, Y:=3500.00, Z:=50.00}
        Rotation_159 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_159 with Rotation_159
        # SpawnerDevice.SpawnProp(Location_159, Rotation_159)

        # Actor 161: Torch_North_1
        Location_160 := vector3{X:=400.00, Y:=100.00, Z:=200.00}
        Rotation_160 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_160 with Rotation_160
        # SpawnerDevice.SpawnProp(Location_160, Rotation_160)

        # Actor 162: Torch_North_2
        Location_161 := vector3{X:=800.00, Y:=100.00, Z:=200.00}
        Rotation_161 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_161 with Rotation_161
        # SpawnerDevice.SpawnProp(Location_161, Rotation_161)

        # Actor 163: Torch_North_3
        Location_162 := vector3{X:=1200.00, Y:=100.00, Z:=200.00}
        Rotation_162 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_162 with Rotation_162
        # SpawnerDevice.SpawnProp(Location_162, Rotation_162)

        # Actor 164: Torch_North_4
        Location_163 := vector3{X:=1600.00, Y:=100.00, Z:=200.00}
        Rotation_163 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_163 with Rotation_163
        # SpawnerDevice.SpawnProp(Location_163, Rotation_163)

        # Actor 165: Torch_North_5
        Location_164 := vector3{X:=2000.00, Y:=100.00, Z:=200.00}
        Rotation_164 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_164 with Rotation_164
        # SpawnerDevice.SpawnProp(Location_164, Rotation_164)

        # Actor 166: Torch_North_6
        Location_165 := vector3{X:=2400.00, Y:=100.00, Z:=200.00}
        Rotation_165 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_165 with Rotation_165
        # SpawnerDevice.SpawnProp(Location_165, Rotation_165)

        # Actor 167: Torch_North_7
        Location_166 := vector3{X:=2800.00, Y:=100.00, Z:=200.00}
        Rotation_166 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_166 with Rotation_166
        # SpawnerDevice.SpawnProp(Location_166, Rotation_166)

        # Actor 168: Torch_North_8
        Location_167 := vector3{X:=3200.00, Y:=100.00, Z:=200.00}
        Rotation_167 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_167 with Rotation_167
        # SpawnerDevice.SpawnProp(Location_167, Rotation_167)

        # Actor 169: Torch_South_1
        Location_168 := vector3{X:=400.00, Y:=3900.00, Z:=200.00}
        Rotation_168 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_168 with Rotation_168
        # SpawnerDevice.SpawnProp(Location_168, Rotation_168)

        # Actor 170: Torch_South_2
        Location_169 := vector3{X:=800.00, Y:=3900.00, Z:=200.00}
        Rotation_169 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_169 with Rotation_169
        # SpawnerDevice.SpawnProp(Location_169, Rotation_169)

        # Actor 171: Torch_South_3
        Location_170 := vector3{X:=1200.00, Y:=3900.00, Z:=200.00}
        Rotation_170 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_170 with Rotation_170
        # SpawnerDevice.SpawnProp(Location_170, Rotation_170)

        # Actor 172: Torch_South_4
        Location_171 := vector3{X:=1600.00, Y:=3900.00, Z:=200.00}
        Rotation_171 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_171 with Rotation_171
        # SpawnerDevice.SpawnProp(Location_171, Rotation_171)

        # Actor 173: Torch_South_5
        Location_172 := vector3{X:=2000.00, Y:=3900.00, Z:=200.00}
        Rotation_172 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_172 with Rotation_172
        # SpawnerDevice.SpawnProp(Location_172, Rotation_172)

        # Actor 174: Torch_South_6
        Location_173 := vector3{X:=2400.00, Y:=3900.00, Z:=200.00}
        Rotation_173 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_173 with Rotation_173
        # SpawnerDevice.SpawnProp(Location_173, Rotation_173)

        # Actor 175: Torch_South_7
        Location_174 := vector3{X:=2800.00, Y:=3900.00, Z:=200.00}
        Rotation_174 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_174 with Rotation_174
        # SpawnerDevice.SpawnProp(Location_174, Rotation_174)

        # Actor 176: Torch_South_8
        Location_175 := vector3{X:=3200.00, Y:=3900.00, Z:=200.00}
        Rotation_175 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_175 with Rotation_175
        # SpawnerDevice.SpawnProp(Location_175, Rotation_175)

        # Actor 177: Stair_0
        Location_176 := vector3{X:=2000.00, Y:=3200.00, Z:=0.00}
        Rotation_176 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_176 with Rotation_176
        # SpawnerDevice.SpawnProp(Location_176, Rotation_176)

        # Actor 178: Stair_1
        Location_177 := vector3{X:=2000.00, Y:=3250.00, Z:=20.00}
        Rotation_177 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_177 with Rotation_177
        # SpawnerDevice.SpawnProp(Location_177, Rotation_177)

        # Actor 179: Stair_2
        Location_178 := vector3{X:=2000.00, Y:=3300.00, Z:=40.00}
        Rotation_178 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_178 with Rotation_178
        # SpawnerDevice.SpawnProp(Location_178, Rotation_178)

        # Actor 180: Stair_3
        Location_179 := vector3{X:=2000.00, Y:=3350.00, Z:=60.00}
        Rotation_179 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_179 with Rotation_179
        # SpawnerDevice.SpawnProp(Location_179, Rotation_179)

        # Actor 181: Stair_4
        Location_180 := vector3{X:=2000.00, Y:=3400.00, Z:=80.00}
        Rotation_180 := rotation{Pitch:=0.00, Yaw:=180.00, Roll:=0.00}
        # Spawn actor at Location_180 with Rotation_180
        # SpawnerDevice.SpawnProp(Location_180, Rotation_180)


    # Spawn 16 PointLight actor(s)
    SpawnPointLightActors():void=
        # Actor 1: Light_North_1
        Location_0 := vector3{X:=400.00, Y:=100.00, Z:=220.00}
        Rotation_0 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_0 with Rotation_0
        # SpawnerDevice.SpawnProp(Location_0, Rotation_0)

        # Actor 2: Light_North_2
        Location_1 := vector3{X:=800.00, Y:=100.00, Z:=220.00}
        Rotation_1 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_1 with Rotation_1
        # SpawnerDevice.SpawnProp(Location_1, Rotation_1)

        # Actor 3: Light_North_3
        Location_2 := vector3{X:=1200.00, Y:=100.00, Z:=220.00}
        Rotation_2 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_2 with Rotation_2
        # SpawnerDevice.SpawnProp(Location_2, Rotation_2)

        # Actor 4: Light_North_4
        Location_3 := vector3{X:=1600.00, Y:=100.00, Z:=220.00}
        Rotation_3 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_3 with Rotation_3
        # SpawnerDevice.SpawnProp(Location_3, Rotation_3)

        # Actor 5: Light_North_5
        Location_4 := vector3{X:=2000.00, Y:=100.00, Z:=220.00}
        Rotation_4 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_4 with Rotation_4
        # SpawnerDevice.SpawnProp(Location_4, Rotation_4)

        # Actor 6: Light_North_6
        Location_5 := vector3{X:=2400.00, Y:=100.00, Z:=220.00}
        Rotation_5 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_5 with Rotation_5
        # SpawnerDevice.SpawnProp(Location_5, Rotation_5)

        # Actor 7: Light_North_7
        Location_6 := vector3{X:=2800.00, Y:=100.00, Z:=220.00}
        Rotation_6 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_6 with Rotation_6
        # SpawnerDevice.SpawnProp(Location_6, Rotation_6)

        # Actor 8: Light_North_8
        Location_7 := vector3{X:=3200.00, Y:=100.00, Z:=220.00}
        Rotation_7 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_7 with Rotation_7
        # SpawnerDevice.SpawnProp(Location_7, Rotation_7)

        # Actor 9: Light_South_1
        Location_8 := vector3{X:=400.00, Y:=3900.00, Z:=220.00}
        Rotation_8 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_8 with Rotation_8
        # SpawnerDevice.SpawnProp(Location_8, Rotation_8)

        # Actor 10: Light_South_2
        Location_9 := vector3{X:=800.00, Y:=3900.00, Z:=220.00}
        Rotation_9 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_9 with Rotation_9
        # SpawnerDevice.SpawnProp(Location_9, Rotation_9)

        # Actor 11: Light_South_3
        Location_10 := vector3{X:=1200.00, Y:=3900.00, Z:=220.00}
        Rotation_10 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_10 with Rotation_10
        # SpawnerDevice.SpawnProp(Location_10, Rotation_10)

        # Actor 12: Light_South_4
        Location_11 := vector3{X:=1600.00, Y:=3900.00, Z:=220.00}
        Rotation_11 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_11 with Rotation_11
        # SpawnerDevice.SpawnProp(Location_11, Rotation_11)

        # Actor 13: Light_South_5
        Location_12 := vector3{X:=2000.00, Y:=3900.00, Z:=220.00}
        Rotation_12 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_12 with Rotation_12
        # SpawnerDevice.SpawnProp(Location_12, Rotation_12)

        # Actor 14: Light_South_6
        Location_13 := vector3{X:=2400.00, Y:=3900.00, Z:=220.00}
        Rotation_13 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_13 with Rotation_13
        # SpawnerDevice.SpawnProp(Location_13, Rotation_13)

        # Actor 15: Light_South_7
        Location_14 := vector3{X:=2800.00, Y:=3900.00, Z:=220.00}
        Rotation_14 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_14 with Rotation_14
        # SpawnerDevice.SpawnProp(Location_14, Rotation_14)

        # Actor 16: Light_South_8
        Location_15 := vector3{X:=3200.00, Y:=3900.00, Z:=220.00}
        Rotation_15 := rotation{Pitch:=0.00, Yaw:=0.00, Roll:=0.00}
        # Spawn actor at Location_15 with Rotation_15
        # SpawnerDevice.SpawnProp(Location_15, Rotation_15)

