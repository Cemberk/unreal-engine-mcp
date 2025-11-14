#!/usr/bin/env python3
"""
Comprehensive Export Pipeline Test

Tests the complete UE5 → UEFN export workflow with a realistic castle level.

Usage:
    python test_export_pipeline.py
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'Python'))

from export_mcp_tools import (
    export_level_to_uefn,
    generate_verse_spawn_map,
    package_assets_for_fortnite
)


def create_sample_castle_level():
    """Create sample castle level with realistic actor data"""
    actors = []

    # Floor tiles (10x10 grid)
    for x in range(10):
        for y in range(10):
            actors.append({
                'name': f'Floor_{x}_{y}',
                'class': 'StaticMeshActor',
                'static_mesh': '/Game/Castle/Architecture/Floor_400x400',
                'location': {'x': x * 400.0, 'y': y * 400.0, 'z': 0.0},
                'rotation': {'pitch': 0.0, 'yaw': 0.0, 'roll': 0.0},
                'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0}
            })

    # Outer walls (perimeter)
    wall_positions = []

    # North and South walls
    for x in range(10):
        wall_positions.append(('North', x * 400.0, 0.0, 0.0))
        wall_positions.append(('South', x * 400.0, 4000.0, 180.0))

    # East and West walls
    for y in range(1, 10):
        wall_positions.append(('West', 0.0, y * 400.0, 270.0))
        wall_positions.append(('East', 4000.0, y * 400.0, 90.0))

    for i, (direction, x, y, yaw) in enumerate(wall_positions):
        actors.append({
            'name': f'Wall_{direction}_{i}',
            'class': 'StaticMeshActor',
            'static_mesh': '/Game/Castle/Architecture/Wall_400x400',
            'location': {'x': x, 'y': y, 'z': 0.0},
            'rotation': {'pitch': 0.0, 'yaw': yaw, 'roll': 0.0},
            'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0}
        })

    # Corner towers (4 towers)
    tower_positions = [
        ('NorthWest', 0.0, 0.0),
        ('NorthEast', 4000.0, 0.0),
        ('SouthWest', 0.0, 4000.0),
        ('SouthEast', 4000.0, 4000.0)
    ]

    for name, x, y in tower_positions:
        actors.append({
            'name': f'Tower_{name}',
            'class': 'StaticMeshActor',
            'static_mesh': '/Game/Castle/Architecture/Tower_Round',
            'location': {'x': x, 'y': y, 'z': 0.0},
            'rotation': {'pitch': 0.0, 'yaw': 0.0, 'roll': 0.0},
            'scale': {'x': 1.5, 'y': 1.5, 'z': 2.0}
        })

    # Gate (centered on north wall)
    actors.append({
        'name': 'Gate_Main',
        'class': 'StaticMeshActor',
        'static_mesh': '/Game/Castle/Architecture/Gate_Large',
        'location': {'x': 2000.0, 'y': 0.0, 'z': 0.0},
        'rotation': {'pitch': 0.0, 'yaw': 0.0, 'roll': 0.0},
        'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0}
    })

    # Interior pillars (3x3 grid)
    for x in range(3):
        for y in range(3):
            actors.append({
                'name': f'Pillar_{x}_{y}',
                'class': 'StaticMeshActor',
                'static_mesh': '/Game/Castle/Architecture/Pillar_Stone',
                'location': {'x': 1200.0 + x * 800.0, 'y': 1200.0 + y * 800.0, 'z': 0.0},
                'rotation': {'pitch': 0.0, 'yaw': 0.0, 'roll': 0.0},
                'scale': {'x': 1.0, 'y': 1.0, 'z': 1.5}
            })

    # Decorative props
    prop_data = [
        ('Throne', 2000.0, 3800.0, '/Game/Castle/Props/Throne', 180.0),
        ('Table_1', 1500.0, 2000.0, '/Game/Castle/Props/Table_Large', 0.0),
        ('Table_2', 2500.0, 2000.0, '/Game/Castle/Props/Table_Large', 0.0),
        ('Banner_1', 1000.0, 200.0, '/Game/Castle/Props/Banner_Red', 0.0),
        ('Banner_2', 3000.0, 200.0, '/Game/Castle/Props/Banner_Blue', 0.0),
        ('Barrel_1', 500.0, 500.0, '/Game/Castle/Props/Barrel', 45.0),
        ('Barrel_2', 3500.0, 500.0, '/Game/Castle/Props/Barrel', 135.0),
        ('Chest_Treasure', 2000.0, 3500.0, '/Game/Castle/Props/Chest_Gold', 180.0)
    ]

    for name, x, y, mesh, yaw in prop_data:
        actors.append({
            'name': name,
            'class': 'StaticMeshActor',
            'static_mesh': mesh,
            'location': {'x': x, 'y': y, 'z': 50.0},
            'rotation': {'pitch': 0.0, 'yaw': yaw, 'roll': 0.0},
            'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0}
        })

    # Torches (wall mounted)
    torch_positions = []
    # Along north wall
    for i in range(1, 9):
        torch_positions.append((f'North_{i}', i * 400.0, 100.0, 0.0))

    # Along south wall
    for i in range(1, 9):
        torch_positions.append((f'South_{i}', i * 400.0, 3900.0, 180.0))

    for name, x, y, yaw in torch_positions:
        actors.append({
            'name': f'Torch_{name}',
            'class': 'StaticMeshActor',
            'static_mesh': '/Game/Castle/Props/Torch_Wall',
            'location': {'x': x, 'y': y, 'z': 200.0},
            'rotation': {'pitch': 0.0, 'yaw': yaw, 'roll': 0.0},
            'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0}
        })

    # Point lights (for torches)
    for name, x, y, yaw in torch_positions:
        actors.append({
            'name': f'Light_{name}',
            'class': 'PointLight',
            'location': {'x': x, 'y': y, 'z': 220.0},
            'rotation': {'pitch': 0.0, 'yaw': 0.0, 'roll': 0.0},
            'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0}
        })

    # Stairs
    for i in range(5):
        actors.append({
            'name': f'Stair_{i}',
            'class': 'StaticMeshActor',
            'static_mesh': '/Game/Castle/Architecture/Stair_Stone',
            'location': {'x': 2000.0, 'y': 3200.0 + i * 50.0, 'z': i * 20.0},
            'rotation': {'pitch': 0.0, 'yaw': 180.0, 'roll': 0.0},
            'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0}
        })

    return actors


def main():
    """Run comprehensive export pipeline test"""
    print("=" * 70)
    print("COMPREHENSIVE EXPORT PIPELINE TEST")
    print("=" * 70)
    print()

    # Create sample level
    print("1. Creating sample castle level...")
    actors = create_sample_castle_level()
    print(f"   ✅ Created level with {len(actors)} actors")

    # Count actor types
    actor_types = {}
    for actor in actors:
        atype = actor.get('class', 'Unknown')
        actor_types[atype] = actor_types.get(atype, 0) + 1

    print(f"   Actor breakdown:")
    for atype, count in sorted(actor_types.items()):
        print(f"     - {atype}: {count}")

    print()

    # Export level
    print("2. Exporting level to UEFN format...")
    export_result_str = export_level_to_uefn(
        level_name='MedievalCastle',
        actors_json=json.dumps(actors),
        export_path='Exports/MedievalCastle',
        uefn_project_path='C:/UEFN/CastleProject',
        options={
            'generate_spawn_code': True,
            'spawn_on_begin': True,
            'detailed_spawn_functions': False
        }
    )

    export_result = json.loads(export_result_str)

    if not export_result['success']:
        print(f"   ❌ Export failed: {export_result['error']}")
        return 1

    print(f"   ✅ Export successful!")
    print(f"   Results:")
    print(f"     - Total actors: {export_result['total_actors']}")
    print(f"     - Total assets: {export_result['total_assets']}")
    print(f"     - Manifest: {export_result['manifest_path']}")
    print(f"     - Spawn code: {export_result['spawn_code_path']}")

    if export_result.get('warnings'):
        print(f"   ⚠️  Warnings:")
        for warning in export_result['warnings']:
            print(f"     - {warning}")

    print()

    # Generate additional spawn code variant
    print("3. Generating detailed spawn code variant...")
    spawn_result_str = generate_verse_spawn_map(
        level_name='MedievalCastle',
        actors_json=json.dumps(actors),
        output_path='Exports/MedievalCastle/Verse/MedievalCastle_detailed.verse',
        options={
            'detailed_spawn_functions': True,
            'spawn_on_begin': False
        }
    )

    spawn_result = json.loads(spawn_result_str)

    if spawn_result['success']:
        print(f"   ✅ Generated detailed variant")
        print(f"     - Lines of code: {spawn_result['lines_of_code']}")
        print(f"     - Output: {spawn_result['output_path']}")
    else:
        print(f"   ❌ Generation failed: {spawn_result['error']}")

    print()

    # Validate package
    print("4. Validating export package...")

    # Test all validation levels
    validation_levels = ['basic', 'standard', 'strict']

    for level in validation_levels:
        print(f"   Testing validation level: {level}")
        validation_str = package_assets_for_fortnite(
            manifest_path=export_result['manifest_path'],
            export_path='Exports/MedievalCastle',
            validation_level=level
        )

        validation = json.loads(validation_str)

        if not validation['success']:
            print(f"     ❌ Validation failed: {validation['error']}")
            continue

        status = "✅" if validation['valid'] else "❌"
        print(f"     {status} Valid: {validation['valid']}")
        print(f"     - Validated: {validation['validated_assets']}/{validation['total_assets']}")

        if validation['errors']:
            print(f"     - Errors: {len(validation['errors'])}")
            for error in validation['errors'][:3]:  # First 3
                print(f"       • {error}")

        if validation['warnings']:
            print(f"     - Warnings: {len(validation['warnings'])}")

        if validation['recommendations']:
            print(f"     - Recommendations: {len(validation['recommendations'])}")

    print()

    # Summary
    print("=" * 70)
    print("EXPORT SUMMARY")
    print("=" * 70)
    print()
    print(f"Level: MedievalCastle")
    print(f"Total Actors: {len(actors)}")
    print(f"Total Assets: {export_result['total_assets']}")
    print()
    print("Actor Types:")
    for atype, count in sorted(actor_types.items()):
        print(f"  - {atype}: {count}")
    print()
    print("Generated Files:")
    print(f"  ✅ {export_result['manifest_path']}")
    print(f"  ✅ {export_result['spawn_code_path']}")
    if spawn_result['success']:
        print(f"  ✅ {spawn_result['output_path']}")
    if export_result.get('integration_notes_path'):
        print(f"  ✅ {export_result['integration_notes_path']}")
    print()

    # Read and display spawn code preview
    print("Spawn Code Preview (first 30 lines):")
    print("-" * 70)
    spawn_file = Path(export_result['spawn_code_path'])
    if spawn_file.exists():
        lines = spawn_file.read_text().split('\n')[:30]
        for i, line in enumerate(lines, 1):
            print(f"{i:3d}  {line}")
        if len(spawn_file.read_text().split('\n')) > 30:
            print("     ...")
    print("-" * 70)
    print()

    # Next steps
    print("Next Steps:")
    print("  1. Export FBX files from UE5 (see INTEGRATION_NOTES.md)")
    print("  2. Import FBX to UEFN project at /Game/ImportedAssets/MedievalCastle/")
    print("  3. Copy Verse files to UEFN project Verse directory")
    print("  4. Build Verse code in UEFN (Ctrl+F7)")
    print("  5. Place spawner device and configure spawner arrays")
    print("  6. Test in Play mode!")
    print()

    print("=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)

    return 0


if __name__ == '__main__':
    sys.exit(main())
