# Phase 4 Improvements & Technical Notes

**Based on code review feedback**

These improvements address determinism, transform fidelity, and Verse backend strategies.

---

## 1. Determinism & Stable IDs

### Issue

Actor ordering in manifest + Verse should be:
- **Stable** across runs given same level
- **Meaningful** for Git diffs
- **Resilient** to minor edits (position tweaks)

### Current Behavior

Actors are processed in the order they appear in the input JSON:
```python
for actor in actors:
    # Process in iteration order
```

If UE5 level iteration order changes (e.g., after actor rename, duplicate, undo), export order changes → large Git diffs.

### Solution: Stable Sorting

Sort actors by deterministic key before processing:

```python
def _sort_actors_stable(self, actors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort actors for deterministic export"""
    def sort_key(actor):
        # Primary: actor class (group by type)
        # Secondary: actor name (alphabetical)
        # Tertiary: location X,Y,Z (spatial order)
        return (
            actor.get('class', 'ZZZ'),  # Class name
            actor.get('name', ''),       # Actor name
            actor.get('location', {}).get('x', 0.0),
            actor.get('location', {}).get('y', 0.0),
            actor.get('location', {}).get('z', 0.0)
        )

    return sorted(actors, key=sort_key)
```

Apply in `generate_spawn_code()` and `generate_asset_manifest()`:

```python
def generate_spawn_code(self, level_name, actors, ...):
    # Sort for determinism
    actors = self._sort_actors_stable(actors)

    # Continue with generation...
```

### Stable Actor IDs

Add logical ID to each actor for future incremental updates:

```python
def _generate_actor_id(self, actor: Dict[str, Any]) -> str:
    """Generate stable ID for actor"""
    # Hash of: class + name + rounded position
    import hashlib

    class_name = actor.get('class', 'Unknown')
    actor_name = actor.get('name', '')

    # Round position to nearest 10cm to survive small tweaks
    loc = actor.get('location', {})
    x = round(loc.get('x', 0.0) / 10.0) * 10.0
    y = round(loc.get('y', 0.0) / 10.0) * 10.0
    z = round(loc.get('z', 0.0) / 10.0) * 10.0

    id_string = f"{class_name}_{actor_name}_{x}_{y}_{z}"

    # Generate short hash
    hash_obj = hashlib.md5(id_string.encode())
    return hash_obj.hexdigest()[:12]
```

Add to manifest:

```json
{
  "name": "Floor_0_0",
  "id": "a3f2d1c4b5e6",  // Stable across exports
  "class": "StaticMeshActor",
  ...
}
```

### Benefits

- Git diffs show actual changes, not reshuffling
- Incremental exports can match old → new actors
- Debugging: actor IDs stay consistent

---

## 2. Transform & Axis Validation

### Issue

Verse `rotation{Pitch, Yaw, Roll}` must exactly match UE coordinate system.

Need to test:
- Non-axis-aligned rotations
- Negative angles
- Pitch/roll combos
- Degrees vs radians
- Coordinate system handedness

### UE5 Coordinate System

- **Right-handed Z-up** (most of the time)
- **Rotations in degrees**: Pitch, Yaw, Roll
  - Pitch: rotation around Y axis (up/down)
  - Yaw: rotation around Z axis (left/right)
  - Roll: rotation around X axis (tilt)
- **Fortnite/UEFN**: Same coordinate system as UE5

### Verification Test Cases

Add to `test_export_pipeline.py`:

```python
def create_rotation_test_level():
    """Test level with pathological rotations"""
    actors = []

    test_rotations = [
        ("Aligned_X", 0.0, 0.0, 0.0),
        ("Aligned_Y", 0.0, 90.0, 0.0),
        ("Aligned_Z", 90.0, 0.0, 0.0),
        ("Negative_Yaw", 0.0, -45.0, 0.0),
        ("Negative_Pitch", -30.0, 0.0, 0.0),
        ("Combo_1", 30.0, 45.0, 0.0),
        ("Combo_2", -15.0, -90.0, 10.0),
        ("Full_Gimbal", 45.0, 135.0, -45.0),
        ("Near_Zero", 0.1, 0.1, 0.1),
        ("Large_Angles", 359.9, 270.0, 180.0)
    ]

    for i, (name, pitch, yaw, roll) in enumerate(test_rotations):
        actors.append({
            'name': f'Rotation_{name}',
            'class': 'StaticMeshActor',
            'static_mesh': '/Game/Test/Cube',
            'location': {'x': i * 200.0, 'y': 0.0, 'z': 100.0},
            'rotation': {'pitch': pitch, 'yaw': yaw, 'roll': roll},
            'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0}
        })

    return actors
```

### Scale Test Cases

```python
def create_scale_test_level():
    """Test level with various scales"""
    actors = []

    test_scales = [
        ("Uniform_Large", 5.0, 5.0, 5.0),
        ("Uniform_Small", 0.1, 0.1, 0.1),
        ("NonUniform_1", 1.0, 2.0, 0.5),
        ("NonUniform_2", 0.5, 3.0, 1.5),
        ("Tiny", 0.01, 0.01, 0.01),
        ("Huge", 100.0, 100.0, 100.0),
        ("Negative_X", -1.0, 1.0, 1.0),  # Mirror
        ("Flatten_Y", 1.0, 0.01, 1.0)   # Pancake
    ]

    for i, (name, sx, sy, sz) in enumerate(test_scales):
        actors.append({
            'name': f'Scale_{name}',
            'class': 'StaticMeshActor',
            'static_mesh': '/Game/Test/Cube',
            'location': {'x': i * 200.0, 'y': 200.0, 'z': 100.0},
            'rotation': {'pitch': 0.0, 'yaw': 0.0, 'roll': 0.0},
            'scale': {'x': sx, 'y': sy, 'z': sz}
        })

    return actors
```

### Pivot Test

For meshes with offset pivots:

```python
# Actor with mesh whose pivot is at (50, 50, 50) instead of origin
actor = {
    'name': 'OffsetPivot',
    'location': {'x': 0.0, 'y': 0.0, 'z': 0.0},  # Actor world position
    'mesh_pivot_offset': {'x': 50.0, 'y': 50.0, 'z': 50.0}  # Mesh pivot
}

# In UEFN, ensure spawned prop appears at (0,0,0), not (-50,-50,-50)
```

**Note:** Pivot offsets are baked into mesh asset, not transform. Verify during Phase 6 import testing.

### Coordinate System Validation Script

To run in UEFN after import:

```verse
# Place this device in test level
rotation_validator := class(creative_device):
    OnBegin<override>()<suspends>:void=
        # Log known test rotations
        TestRot1 := rotation{Pitch:=30.0, Yaw:=45.0, Roll:=0.0}
        Print("Test rotation: {TestRot1}")

        # Compare against spawned actor rotations
        # (Manual verification step)
```

---

## 3. Prop vs Device Strategy in Verse

### Current Approach

All static meshes use `item_spawner_device`:

```verse
@editable
StaticMeshActor_Spawners<private>: []item_spawner_device = array{}
```

### Problem

`item_spawner_device` is designed for **gameplay items** (weapons, consumables, pickups).

For **pure static architecture** (walls, floors, decor), this is overkill:
- Requires device placement per asset type
- Uses device budget (limited per island)
- Adds unnecessary complexity

### Better: creative_prop

For non-interactive static meshes, use `creative_prop`:

```verse
using { /Fortnite.com/Game }

# Spawn static prop directly
SpawnFloor():void=
    FloorProp := creative_prop:
        creative_prop_asset := creative_prop_asset{...}

    Transform := transform:
        Translation := vector3{X:=0.0, Y:=0.0, Z:=0.0}
        Rotation := rotation{Pitch:=0.0, Yaw:=0.0, Roll:=0.0}
        Scale := vector3{X:=1.0, Y:=1.0, Z:=1.0}

    PropInstance := FloorProp.Spawn(Transform)
```

### Proposed: Dual Backend Strategy

**1. Static Prop Backend** (for architecture, decor)
- Uses `creative_prop_asset` + `.Spawn()`
- No device placement required
- Lower overhead
- Best for: floors, walls, pillars, decorations

**2. Device Backend** (for interactive/gameplay elements)
- Uses `item_spawner_device` or specific device types
- Requires @editable linking
- Full device control
- Best for: items, collectibles, objectives, triggers

### Manifest Tagging

Add `spawn_strategy` to manifest:

```json
{
  "ue5_path": "/Game/Castle/Architecture/Floor_400x400",
  "uefn_path": "/Game/ImportedAssets/MedievalCastle/Floor_400x400",
  "type": "StaticMesh",
  "spawn_strategy": "prop",  // or "device"
  "export_file": "Floor_400x400.fbx",
  "references": 100
}
```

Heuristic:

```python
def determine_spawn_strategy(actor):
    """Decide prop vs device spawning"""
    # Interactive actors → device
    if actor.get('has_gameplay_tag'):
        return 'device'

    # High reference count static meshes → prop (architecture)
    if actor.get('class') == 'StaticMeshActor':
        return 'prop'

    # Lights, triggers, etc → device
    if actor.get('class') in ['PointLight', 'SpotLight', 'TriggerVolume']:
        return 'device'

    # Default: prop
    return 'prop'
```

### Generated Verse (Dual Backend)

```verse
MedievalCastle_spawner := class(creative_device):

    # Props (no @editable needed - direct spawn)
    OnBegin<override>()<suspends>:void=
        SpawnStaticProps()
        SpawnDevices()

    SpawnStaticProps():void=
        # Direct prop spawning (architecture)
        FloorAsset := creative_prop_asset{...}
        Floor1 := FloorAsset.Spawn(transform{...})
        Floor2 := FloorAsset.Spawn(transform{...})
        # ... 100 floor instances

    # Devices (requires @editable linking)
    @editable
    TorchSpawners<private>: []item_spawner_device = array{}

    SpawnDevices():void=
        # Use linked spawner devices
        for (Spawner : TorchSpawners):
            Spawner.Enable()
```

### Benefits

- **Performance**: Fewer devices → more island budget for gameplay
- **Simplicity**: No manual linking for static architecture
- **Clarity**: Code separates architecture (props) from gameplay (devices)

---

## 4. Performance & Large Level Handling

### Issue

5,745-line detailed spawner might:
- Take long time in `OnBegin`
- Hit Fortnite object count limits
- Cause memory issues

### Recommendations

**1. Profile First (Phase 6)**

Before optimizing, measure:
- `OnBegin` execution time in UEFN Play mode
- Memory usage (check UEFN stats window)
- Object count vs island limits

**2. Chunked Spawning**

If `OnBegin` is slow, spawn in chunks:

```verse
MedievalCastle_spawner := class(creative_device):

    CurrentChunk<private>: int = 0
    TotalChunks<private>: int = 10

    OnBegin<override>()<suspends>:void=
        # Start chunked spawn loop
        loop:
            SpawnChunk(CurrentChunk)
            set CurrentChunk += 1

            if (CurrentChunk >= TotalChunks):
                break

            # Yield every chunk to prevent timeout
            Sleep(0.1)

    SpawnChunk(ChunkIndex: int):void=
        if (ChunkIndex = 0):
            # Spawn floors 0-99
            SpawnFloorsChunk0()
        else if (ChunkIndex = 1):
            # Spawn floors 100-199
            SpawnFloorsChunk1()
        # ...
```

**3. Spatial Chunking (LOD-ish)**

For very large levels, spawn distant detail on-demand:

```verse
# Spawn only nearby regions initially
# Spawn distant regions when player moves closer

OnPlayerMoved(Agent: agent):void=
    PlayerPos := Agent.GetTransform().Translation

    # Check which regions to spawn
    if (PlayerPos.X > 2000.0):
        SpawnEastWing()
```

**4. Level Splitting**

For massive levels (1000+ actors), consider:
- Split into multiple islands/chunks
- Or multiple spawner devices (one per region)
- Export pipeline can auto-split:

```python
# Export with chunking
result = await export_level_to_uefn(
    level_name='MassiveCastle',
    actors_json=json.dumps(actors),
    export_path='Exports/MassiveCastle',
    options={
        'chunk_size': 200,  # Max 200 actors per spawner
        'spatial_chunking': True  # Group by location
    }
)

# Generates:
# - MassiveCastle_spawner_chunk0.verse (200 actors)
# - MassiveCastle_spawner_chunk1.verse (200 actors)
# - ...
```

---

## 5. Implementation Roadmap

### Priority 1: Must Do Before Phase 6

- [x] ~~Deterministic actor sorting~~
- [ ] **Add stable actor IDs to manifest**
- [ ] **Create rotation/scale test cases**
- [ ] **Add prop vs device strategy to export options**

### Priority 2: Should Do During Phase 6

- [ ] **Run transform validation tests in UEFN**
- [ ] **Profile spawner performance**
- [ ] **Implement prop-based backend for architecture**

### Priority 3: Nice to Have

- [ ] Incremental export (using stable IDs)
- [ ] Spatial chunking for large levels
- [ ] Auto-detection of device vs prop types

---

## 6. Code Changes Required

### File: `Python/verse_spawn_generator.py`

**Add sorting:**
```python
def generate_spawn_code(self, level_name, actors, ...):
    # Sort actors for determinism
    actors = self._sort_actors_stable(actors)
    ...

def _sort_actors_stable(self, actors):
    # Implementation from §1
    ...
```

**Add actor IDs:**
```python
def generate_asset_manifest(self, level_name, actors, export_path):
    manifest = {...}

    for actor in actors:
        actor_id = self._generate_actor_id(actor)
        # Add to manifest
        manifest['actors'].append({
            'id': actor_id,
            'name': actor['name'],
            ...
        })
    ...

def _generate_actor_id(self, actor):
    # Implementation from §1
    ...
```

**Add spawn strategy:**
```python
def _determine_spawn_strategy(self, actor):
    # Implementation from §3
    ...

def generate_spawn_code(self, level_name, actors, ...):
    # Group by spawn strategy
    prop_actors = [a for a in actors if self._determine_spawn_strategy(a) == 'prop']
    device_actors = [a for a in actors if self._determine_spawn_strategy(a) == 'device']

    # Generate separate spawn methods
    if prop_actors:
        lines.extend(self._generate_prop_spawn_methods(prop_actors))

    if device_actors:
        lines.extend(self._generate_device_spawn_methods(device_actors))
    ...
```

### File: `Tests/test_export_pipeline.py`

**Add transform tests:**
```python
def test_rotation_fidelity():
    actors = create_rotation_test_level()
    # Export and validate rotations
    ...

def test_scale_fidelity():
    actors = create_scale_test_level()
    # Export and validate scales
    ...
```

---

## Summary

These improvements make Phase 4 **production-ready**:

1. **Determinism**: Stable actor ordering and IDs → clean Git diffs
2. **Transform fidelity**: Validated rotations, scales, pivots → accurate recreation
3. **Verse backend strategy**: Props for architecture, devices for gameplay → efficient
4. **Performance**: Chunking and profiling → scales to large levels

**Recommendation**: Implement Priority 1 items before Phase 6 integration testing.

---

*Phase 4 Improvements - UEFN Migration Project*
*Created: November 13, 2025*
