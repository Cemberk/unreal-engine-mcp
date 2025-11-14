# UE5 to UEFN Export Workflow Guide

**Phase 4: Asset Export Pipeline**

This guide walks through the complete process of exporting a UE5 level to UEFN/Fortnite Creative using the export MCP tools.

> **Note on Automation**: UEFN does not expose automation APIs like Remote Control (by Epic's design for safety/consistency). Steps 3-7 below require manual interaction with UEFN. The export pipeline (Steps 1-2) is fully automated and reduces overall workflow time by ~90% compared to manual level recreation.

---

## Overview

The export pipeline consists of:

1. **Extract** actor data from UE5 level
2. **Export** level to structured format with manifest
3. **Export assets** from UE5 (manual FBX export)
4. **Import assets** to UEFN project
5. **Install** generated Verse spawn code
6. **Configure** spawner devices in UEFN
7. **Build & test** in Fortnite Creative

---

## Prerequisites

### Software Requirements
- ✅ Unreal Engine 5 project with level to export
- ✅ UEFN Editor installed (integrated with Fortnite)
- ✅ MCP server running with export tools enabled
- ✅ Python 3.8+ with required dependencies

### Knowledge Requirements
- Basic UE5 navigation
- UEFN editor basics
- Understanding of Verse programming (helpful but not required)

---

## Step 1: Extract Actor Data from UE5

### Option A: Using UE5 MCP Tools (Automated)

```python
# Use existing UE5 MCP tools to extract actor data
actors_json = await list_actors_in_level(
    level_path='/Game/Maps/CastleLevel',
    include_transforms=True,
    include_properties=True
)

# Save for later use
import json
with open('castle_actors.json', 'w') as f:
    f.write(actors_json)
```

### Option B: Manual Extraction (UE5 Python)

```python
# In UE5 Python console
import unreal
import json

def extract_level_actors(level_path):
    """Extract actors from UE5 level"""
    actors = []

    # Load level
    editor_subsystem = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    world = editor_subsystem.get_editor_world()

    for actor in world.get_all_level_actors():
        # Skip certain actor types
        if isinstance(actor, (unreal.CameraActor, unreal.Light)):
            continue

        # Get transform
        location = actor.get_actor_location()
        rotation = actor.get_actor_rotation()
        scale = actor.get_actor_scale3d()

        # Get static mesh if available
        static_mesh = None
        mesh_component = actor.get_component_by_class(unreal.StaticMeshComponent)
        if mesh_component:
            mesh = mesh_component.static_mesh
            if mesh:
                static_mesh = mesh.get_path_name()

        actor_data = {
            'name': actor.get_name(),
            'class': actor.get_class().get_name(),
            'location': {
                'x': location.x,
                'y': location.y,
                'z': location.z
            },
            'rotation': {
                'pitch': rotation.pitch,
                'yaw': rotation.yaw,
                'roll': rotation.roll
            },
            'scale': {
                'x': scale.x,
                'y': scale.y,
                'z': scale.z
            }
        }

        if static_mesh:
            actor_data['static_mesh'] = static_mesh

        actors.append(actor_data)

    return actors

# Extract and save
actors = extract_level_actors('/Game/Maps/CastleLevel')
with open('C:/Temp/castle_actors.json', 'w') as f:
    json.dump(actors, f, indent=2)

print(f"Extracted {len(actors)} actors")
```

### Expected Actor Data Format

```json
[
  {
    "name": "Floor_Main",
    "class": "StaticMeshActor",
    "static_mesh": "/Game/Architecture/Floor_400x400",
    "location": {"x": 0.0, "y": 0.0, "z": 0.0},
    "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
    "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
  },
  {
    "name": "Wall_North",
    "class": "StaticMeshActor",
    "static_mesh": "/Game/Architecture/Wall_400x400",
    "location": {"x": 0.0, "y": 400.0, "z": 0.0},
    "rotation": {"pitch": 0.0, "yaw": 0.0, "roll": 0.0},
    "scale": {"x": 1.0, "y": 1.0, "z": 1.0}
  }
]
```

---

## Step 2: Run Export Pipeline

### Using MCP Tool

```python
import json

# Load actors
with open('castle_actors.json') as f:
    actors = json.load(f)

# Export level
result = await export_level_to_uefn(
    level_name='CastleLevel',
    actors_json=json.dumps(actors),
    export_path='Exports/CastleLevel',
    uefn_project_path='C:/UEFN/MyCastle',  # Optional
    options={
        'generate_spawn_code': True,
        'spawn_on_begin': True,
        'detailed_spawn_functions': False
    }
)

# Check result
export_result = json.loads(result)
if export_result['success']:
    print(f"✅ Export successful!")
    print(f"   Manifest: {export_result['manifest_path']}")
    print(f"   Spawn code: {export_result['spawn_code_path']}")
    print(f"   Total actors: {export_result['total_actors']}")
    print(f"   Total assets: {export_result['total_assets']}")
else:
    print(f"❌ Export failed: {export_result['error']}")
```

### Direct Python Usage

```python
from export_mcp_tools import export_level_to_uefn
import json

# Load actors
with open('castle_actors.json') as f:
    actors = json.load(f)

# Export
result = export_level_to_uefn(
    level_name='CastleLevel',
    actors_json=json.dumps(actors),
    export_path='Exports/CastleLevel'
)

print(result)
```

### Output Structure

After export, you'll have:

```
Exports/CastleLevel/
├── Assets/                     # Empty - you'll export FBX files here
├── Verse/
│   └── CastleLevel_spawner.verse  # Generated spawn code
├── Manifests/
│   └── CastleLevel_manifest.json  # Asset manifest
└── INTEGRATION_NOTES.md       # Step-by-step guide
```

---

## Step 3: Export Assets from UE5

The manifest tells you which assets to export. Open the manifest:

```json
{
  "level_name": "CastleLevel",
  "total_actors": 45,
  "assets": [
    {
      "ue5_path": "/Game/Architecture/Floor_400x400",
      "uefn_path": "/Game/ImportedAssets/CastleLevel/Floor_400x400",
      "type": "StaticMesh",
      "export_file": "Floor_400x400.fbx",
      "references": 12
    },
    // ... more assets
  ]
}
```

### Export Process

1. **Open UE5 Content Browser**
   - Navigate to Content folder
   - Find assets listed in manifest

2. **Select Assets to Export**
   - Find `/Game/Architecture/Floor_400x400`
   - Right-click → Asset Actions → Export...
   - **OR** select multiple assets, right-click → Bulk Export

3. **Configure FBX Export Settings**
   - Format: FBX
   - Options:
     - ✅ Export Preview Mesh
     - ✅ Export Source Mesh
     - ✅ Export Collisions
     - ✅ Export Level of Detail
     - ❌ Export Morph Targets (unless needed)
     - ❌ Export Animations (unless needed)

4. **Export Location**
   - Save to: `Exports/CastleLevel/Assets/`
   - Use filename from manifest: `Floor_400x400.fbx`

5. **Repeat for All Assets**
   - Export each asset in manifest
   - Keep filenames consistent with manifest

### Bulk Export Script (Optional)

```python
# UE5 Python - Bulk export assets from manifest
import unreal
import json
from pathlib import Path

def bulk_export_from_manifest(manifest_path, output_dir):
    """Export all assets listed in manifest"""
    with open(manifest_path) as f:
        manifest = json.load(f)

    export_task_builder = unreal.AssetExportTaskBuilder()
    tasks = []

    for asset_data in manifest['assets']:
        ue5_path = asset_data['ue5_path']
        export_file = asset_data['export_file']

        # Load asset
        asset = unreal.load_asset(ue5_path)
        if not asset:
            print(f"⚠️  Asset not found: {ue5_path}")
            continue

        # Create export task
        task = unreal.AssetExportTask()
        task.object = asset
        task.filename = str(Path(output_dir) / export_file)
        task.automated = True
        task.replace_identical = True
        task.prompt = False

        tasks.append(task)

    # Execute export
    unreal.Exporter.run_asset_export_tasks(tasks)
    print(f"✅ Exported {len(tasks)} assets")

# Run export
bulk_export_from_manifest(
    'Exports/CastleLevel/Manifests/CastleLevel_manifest.json',
    'Exports/CastleLevel/Assets/'
)
```

---

## Step 4: Import Assets to UEFN

1. **Open UEFN Editor**
   - Launch Fortnite
   - Open UEFN from Fortnite launcher
   - Open your project

2. **Create Import Folder**
   - Content Browser → Content
   - Right-click → New Folder
   - Name: `ImportedAssets/CastleLevel`

3. **Import FBX Files**
   - Navigate to `ImportedAssets/CastleLevel`
   - Right-click → Import to `/Game/ImportedAssets/CastleLevel`
   - Select FBX files from `Exports/CastleLevel/Assets/`
   - Click Open

4. **Configure Import Settings**
   - **Mesh:**
     - Import Mesh: ✅ Yes
     - Transform: Use default
     - Import Materials: ✅ Yes
     - Import Textures: ✅ Yes

   - **Advanced:**
     - Auto Generate Collision: ✅ Yes
     - Build Nanite: ❌ No (not supported in UEFN)
     - Combine Meshes: ❌ No

   - Click **Import All**

5. **Verify Import**
   - Check Content Browser for imported meshes
   - Double-click to preview
   - Ensure materials loaded correctly

---

## Step 5: Install Verse Spawn Code

1. **Locate Generated Code**
   - File: `Exports/CastleLevel/Verse/CastleLevel_spawner.verse`
   - Open in text editor to review

2. **Copy to UEFN Project**
   - UEFN project Verse directory (typical location):
     - Windows: `C:/Users/{User}/Documents/UEFN/Projects/{ProjectName}/Verse/`
   - Copy `CastleLevel_spawner.verse` to project Verse folder

3. **Rebuild Verse Code**
   - In UEFN: **Ctrl+F7** (or Tools → Build Verse)
   - Check output panel for errors
   - Fix any compilation errors

4. **Verify Device Class**
   - Content Browser → Verse Devices
   - Look for `CastleLevel_spawner` device
   - Should appear with green checkmark

---

## Step 6: Configure Spawner Devices in UEFN

The generated Verse code has `@editable` properties for spawner devices. You need to configure these:

### Example Generated Code

```verse
CastleLevel_spawner := class(creative_device):
    @editable
    StaticMeshActor_Spawners<private>: []item_spawner_device = array{}

    OnBegin<override>()<suspends>:void=
        SpawnAllActors()
```

### Configuration Steps

1. **Place Spawner Device**
   - Drag `CastleLevel_spawner` from Content Browser to level
   - Position anywhere (doesn't affect spawn locations)

2. **Place Item Spawner Devices**
   - Devices → Item Spawner
   - Drag into level (one per asset type or per instance)
   - Configure each spawner:
     - Item to Spawn: Select imported mesh
     - Respawn: ❌ Off
     - Spawn When Receiving From: Device activation

3. **Link Spawners to Verse Device**
   - Select `CastleLevel_spawner` device in level
   - Details panel → Find `StaticMeshActor_Spawners` array
   - Click **+** to add elements
   - Drag item spawner devices into array slots

4. **Test Spawning**
   - Enter Play mode (Alt+P)
   - Spawners should trigger automatically via `OnBegin`
   - Verify actors spawn at correct positions

---

## Step 7: Build & Test

1. **Build Verse Code**
   - **Ctrl+F7** to rebuild
   - Check for errors

2. **Save Island**
   - Save all changes
   - File → Save All

3. **Test in Play Mode**
   - Click **Play** or press Alt+P
   - Observe actor spawning
   - Check positions and rotations

4. **Publish Island**
   - File → Publish Island
   - Test in Fortnite Creative

---

## Validation & Troubleshooting

### Validate Export Package

Before importing to UEFN, validate the export:

```python
result = await package_assets_for_fortnite(
    manifest_path='Exports/CastleLevel/Manifests/CastleLevel_manifest.json',
    export_path='Exports/CastleLevel',
    validation_level='strict'
)

validation = json.loads(result)
print(f"Valid: {validation['valid']}")
print(f"Errors: {validation['errors']}")
print(f"Warnings: {validation['warnings']}")
print(f"Recommendations: {validation['recommendations']}")
```

### Common Issues

#### Issue: "Asset not found" in UE5 export

**Solution:**
- Check asset path in manifest
- Ensure asset exists in Content Browser
- Verify spelling and case sensitivity

#### Issue: Verse compilation errors

**Solution:**
- Check Verse syntax in generated code
- Ensure proper indentation
- Verify device types match UEFN API

#### Issue: Spawners not triggering

**Solution:**
- Verify spawner devices are linked in array
- Check `OnBegin` is called (add Print statement)
- Ensure spawner devices are configured correctly

#### Issue: Actors spawn at wrong positions

**Solution:**
- Verify coordinate system conversion (UE5 vs UEFN)
- Check transform data in actor JSON
- Test with simple known coordinates first

#### Issue: Materials missing on imported meshes

**Solution:**
- Re-export FBX with "Export Materials" checked
- Manually assign materials in UEFN
- Check texture paths in FBX export

---

## Advanced Usage

### Generate Spawn Code Only

If you already have a manifest, just generate spawn code:

```python
result = await generate_verse_spawn_map(
    level_name='CastleLevel',
    actors_json=json.dumps(actors),
    output_path='CastleLevel_spawner.verse',
    options={'detailed_spawn_functions': True}
)
```

### Custom Export Options

```python
result = await export_level_to_uefn(
    level_name='CastleLevel',
    actors_json=json.dumps(actors),
    export_path='Exports/CastleLevel',
    options={
        'generate_spawn_code': True,      # Generate Verse code
        'spawn_on_begin': False,          # Don't auto-spawn
        'detailed_spawn_functions': True, # Individual spawn functions
        'use_spawner_devices': True       # Use item_spawner_device
    }
)
```

### Incremental Exports

Export only changed actors:

```python
# Load previous manifest
with open('Exports/CastleLevel/Manifests/CastleLevel_manifest.json') as f:
    old_manifest = json.load(f)

# Extract current actors
current_actors = extract_level_actors('/Game/Maps/CastleLevel')

# Find new/changed actors
new_actors = []
for actor in current_actors:
    is_new = True
    for old_actor in old_manifest.get('actors', []):
        if actor['name'] == old_actor['name']:
            # Check if changed
            if actor == old_actor:
                is_new = False
            break
    if is_new:
        new_actors.append(actor)

# Export only new actors
if new_actors:
    result = await export_level_to_uefn(
        level_name='CastleLevel_Update',
        actors_json=json.dumps(new_actors),
        export_path='Exports/CastleLevel_Update'
    )
```

---

## Best Practices

### Asset Organization
- ✅ Use consistent naming conventions
- ✅ Group related assets in folders
- ✅ Keep asset paths short and simple
- ✅ Avoid special characters in names

### Export Preparation
- ✅ Clean up unnecessary actors before export
- ✅ Remove duplicate meshes
- ✅ Merge similar actors when possible
- ✅ Test with small subset first

### UEFN Integration
- ✅ Create dedicated import folder per level
- ✅ Keep Verse code organized by purpose
- ✅ Test spawn code in small increments
- ✅ Use Print statements for debugging

### Performance
- ✅ Limit total spawned actors (UEFN has limits)
- ✅ Use instancing for repeated meshes
- ✅ Optimize mesh poly counts before export
- ✅ Test performance in Fortnite Creative mode

---

## Example: Complete Castle Export

Full example exporting a castle level:

```python
import json
from pathlib import Path

# 1. Extract actors (assume done in UE5)
# Result: castle_actors.json with 150 actors

# 2. Load actor data
with open('castle_actors.json') as f:
    actors = json.load(f)

print(f"Loaded {len(actors)} actors")

# 3. Export to UEFN
result = await export_level_to_uefn(
    level_name='MedievalCastle',
    actors_json=json.dumps(actors),
    export_path='Exports/MedievalCastle',
    uefn_project_path='C:/UEFN/CastleProject',
    options={
        'generate_spawn_code': True,
        'spawn_on_begin': True
    }
)

export_result = json.loads(result)

# 4. Check results
if export_result['success']:
    print("✅ Export complete!")
    print(f"   Actors: {export_result['total_actors']}")
    print(f"   Assets: {export_result['total_assets']}")
    print(f"   Actor types: {export_result['actor_types']}")

    # 5. Validate package
    validation = await package_assets_for_fortnite(
        manifest_path=export_result['manifest_path'],
        export_path='Exports/MedievalCastle',
        validation_level='strict'
    )

    val_result = json.loads(validation)
    if val_result['valid']:
        print("✅ Validation passed!")
    else:
        print(f"⚠️  Validation issues:")
        for error in val_result['errors']:
            print(f"   - {error}")

    # 6. Next steps
    print("\nNext steps:")
    print("1. Export FBX files from UE5 (see INTEGRATION_NOTES.md)")
    print("2. Import FBX to UEFN")
    print("3. Copy Verse code to UEFN project")
    print("4. Configure spawner devices")
    print("5. Build and test!")
else:
    print(f"❌ Export failed: {export_result['error']}")
```

**Expected Output:**
```
Loaded 150 actors
✅ Export complete!
   Actors: 150
   Assets: 42
   Actor types: {'StaticMeshActor': 145, 'PointLight': 5}
✅ Validation passed!

Next steps:
1. Export FBX files from UE5 (see INTEGRATION_NOTES.md)
2. Import FBX to UEFN
3. Copy Verse code to UEFN project
4. Configure spawner devices
5. Build and test!
```

---

## Summary

The UE5 → UEFN export workflow:

1. ✅ **Extract** actor data from UE5 level
2. ✅ **Export** using `export_level_to_uefn()` MCP tool
3. ✅ **Export assets** as FBX from UE5
4. ✅ **Import** FBX files to UEFN project
5. ✅ **Install** generated Verse spawn code
6. ✅ **Configure** spawner devices and link them
7. ✅ **Build & test** in Fortnite Creative

With this workflow, you can migrate entire UE5 levels to UEFN/Fortnite Creative efficiently!

---

*Export Workflow Guide - UEFN Migration Project*
*Last Updated: November 13, 2025*
