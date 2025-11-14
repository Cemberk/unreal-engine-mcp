#!/usr/bin/env python3
"""
Export MCP Tools for UEFN/Fortnite Asset Export Pipeline

Provides MCP tool wrappers for exporting UE5 levels to UEFN/Fortnite Creative.
These tools orchestrate the asset export, manifest generation, and Verse code generation.

MCP Tools:
    1. export_level_to_uefn() - Export UE5 level to UEFN format
    2. generate_verse_spawn_map() - Generate Verse spawn code from level
    3. package_assets_for_fortnite() - Package and validate assets

Phase 4: Asset Export Pipeline
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from verse_spawn_generator import VerseSpawnGenerator


# Global generator instance
spawn_generator = None


def initialize_spawn_generator():
    """Initialize the spawn generator"""
    global spawn_generator
    if spawn_generator is None:
        spawn_generator = VerseSpawnGenerator()
    return spawn_generator


def export_level_to_uefn(
    level_name: str,
    actors_json: str,
    export_path: str,
    uefn_project_path: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None
) -> str:
    """
    Export UE5 level to UEFN format with asset manifest and Verse spawn code.

    This is the main export orchestrator that:
    1. Parses actor data from UE5 level
    2. Generates asset manifest mapping UE5 → UEFN paths
    3. Creates export directory structure
    4. Optionally generates Verse spawn code

    Args:
        level_name: Name of the UE5 level to export
        actors_json: JSON string containing actor data from level
                     Expected format: [{"name": "Actor1", "class": "StaticMeshActor",
                                       "location": {...}, "rotation": {...}, ...}, ...]
        export_path: Directory path where export files will be created
        uefn_project_path: Optional path to UEFN project for direct integration
        options: Optional export options:
                 - generate_spawn_code: bool (default True)
                 - spawn_on_begin: bool (default True)
                 - detailed_spawn_functions: bool (default False)
                 - asset_format: str (default 'fbx')

    Returns:
        JSON string with export summary:
        {
            "success": true,
            "level_name": "...",
            "export_path": "...",
            "manifest_path": "...",
            "spawn_code_path": "...",
            "total_actors": 123,
            "total_assets": 45,
            "actor_types": {...},
            "warnings": [...]
        }
    """
    try:
        # Parse inputs
        actors = json.loads(actors_json)
        options = options or {}
        export_dir = Path(export_path)

        # Initialize generator
        generator = initialize_spawn_generator()

        # Create export directory structure
        export_dir.mkdir(parents=True, exist_ok=True)
        assets_dir = export_dir / "Assets"
        verse_dir = export_dir / "Verse"
        manifests_dir = export_dir / "Manifests"

        for directory in [assets_dir, verse_dir, manifests_dir]:
            directory.mkdir(exist_ok=True)

        # Generate asset manifest
        manifest = generator.generate_asset_manifest(
            level_name=level_name,
            actors=actors,
            export_path=export_dir
        )

        # Save manifest
        manifest_path = manifests_dir / f"{level_name}_manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        # Generate Verse spawn code if requested
        spawn_code_path = None
        if options.get('generate_spawn_code', True):
            spawn_code = generator.generate_spawn_code(
                level_name=level_name,
                actors=actors,
                asset_manifest=manifest,
                options=options
            )

            spawn_code_path = verse_dir / f"{level_name}_spawner.verse"
            spawn_code_path.write_text(spawn_code)

        # Create export summary
        summary = {
            "success": True,
            "level_name": level_name,
            "export_path": str(export_dir),
            "manifest_path": str(manifest_path),
            "spawn_code_path": str(spawn_code_path) if spawn_code_path else None,
            "total_actors": len(actors),
            "total_assets": len(manifest['assets']),
            "actor_types": manifest['actor_types'],
            "export_date": datetime.now().isoformat(),
            "warnings": []
        }

        # Add warnings if any
        if manifest['total_actors'] == 0:
            summary['warnings'].append("No actors found in level data")

        if len(manifest['assets']) == 0:
            summary['warnings'].append("No assets found - actors may not have static meshes")

        # If UEFN project path provided, create integration notes
        if uefn_project_path:
            integration_notes_path = export_dir / "INTEGRATION_NOTES.md"
            integration_notes = _generate_integration_notes(
                level_name=level_name,
                uefn_project_path=uefn_project_path,
                manifest=manifest,
                spawn_code_path=spawn_code_path
            )
            integration_notes_path.write_text(integration_notes)
            summary['integration_notes_path'] = str(integration_notes_path)

        return json.dumps(summary, indent=2)

    except json.JSONDecodeError as e:
        return json.dumps({
            "success": False,
            "error": f"Invalid JSON in actors_json: {str(e)}"
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Export failed: {str(e)}"
        })


def generate_verse_spawn_map(
    level_name: str,
    actors_json: str,
    output_path: str,
    options: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate Verse spawn code from UE5 level data.

    Creates a Verse spawner device that recreates the level's actor layout.
    This is a focused tool for just generating the spawn code without full export.

    Args:
        level_name: Name of the level
        actors_json: JSON string with actor data
        output_path: Path where .verse file will be saved
        options: Generation options:
                 - spawn_on_begin: bool (default True)
                 - use_spawner_devices: bool (default True)
                 - detailed_spawn_functions: bool (default False)

    Returns:
        JSON string with generation result:
        {
            "success": true,
            "output_path": "...",
            "lines_of_code": 123,
            "actors_processed": 45,
            "code_preview": "..."
        }
    """
    try:
        # Parse inputs
        actors = json.loads(actors_json)
        options = options or {}
        output_file = Path(output_path)

        # Initialize generator
        generator = initialize_spawn_generator()

        # Create empty manifest (actual asset paths would come from export)
        asset_manifest = {
            'level_name': level_name,
            'assets': []
        }

        # Generate spawn code
        spawn_code = generator.generate_spawn_code(
            level_name=level_name,
            actors=actors,
            asset_manifest=asset_manifest,
            options=options
        )

        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Save to file
        output_file.write_text(spawn_code)

        # Create preview (first 500 chars)
        preview = spawn_code[:500] + "..." if len(spawn_code) > 500 else spawn_code

        return json.dumps({
            "success": True,
            "output_path": str(output_file),
            "lines_of_code": spawn_code.count('\n') + 1,
            "actors_processed": len(actors),
            "code_preview": preview,
            "file_size": len(spawn_code)
        }, indent=2)

    except json.JSONDecodeError as e:
        return json.dumps({
            "success": False,
            "error": f"Invalid JSON in actors_json: {str(e)}"
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Generation failed: {str(e)}"
        })


def package_assets_for_fortnite(
    manifest_path: str,
    export_path: str,
    validation_level: str = "standard"
) -> str:
    """
    Package and validate assets for UEFN/Fortnite Creative deployment.

    Validates the asset manifest and export structure to ensure UEFN compatibility.

    Args:
        manifest_path: Path to the asset manifest JSON file
        export_path: Path to the export directory
        validation_level: Validation strictness:
                         - "basic": Check manifest structure only
                         - "standard": Check files and paths (default)
                         - "strict": Full UEFN compatibility validation

    Returns:
        JSON string with validation result:
        {
            "success": true,
            "valid": true,
            "manifest_path": "...",
            "export_path": "...",
            "total_assets": 45,
            "validated_assets": 45,
            "errors": [],
            "warnings": [],
            "recommendations": []
        }
    """
    try:
        # Load manifest
        manifest_file = Path(manifest_path)
        if not manifest_file.exists():
            return json.dumps({
                "success": False,
                "error": f"Manifest file not found: {manifest_path}"
            })

        with open(manifest_file) as f:
            manifest = json.load(f)

        export_dir = Path(export_path)
        if not export_dir.exists():
            return json.dumps({
                "success": False,
                "error": f"Export directory not found: {export_path}"
            })

        # Initialize validation result
        result = {
            "success": True,
            "valid": True,
            "manifest_path": str(manifest_file),
            "export_path": str(export_dir),
            "total_assets": len(manifest.get('assets', [])),
            "validated_assets": 0,
            "errors": [],
            "warnings": [],
            "recommendations": []
        }

        # Basic validation: manifest structure
        required_fields = ['level_name', 'export_date', 'assets', 'actor_types']
        for field in required_fields:
            if field not in manifest:
                result['errors'].append(f"Missing required field in manifest: {field}")
                result['valid'] = False

        # Validate assets
        assets = manifest.get('assets', [])
        validated_count = 0

        for i, asset in enumerate(assets):
            asset_errors = []

            # Check asset structure
            if 'ue5_path' not in asset:
                asset_errors.append(f"Asset {i}: Missing 'ue5_path'")
            if 'uefn_path' not in asset:
                asset_errors.append(f"Asset {i}: Missing 'uefn_path'")
            if 'type' not in asset:
                asset_errors.append(f"Asset {i}: Missing 'type'")

            # Standard validation: check export files
            if validation_level in ["standard", "strict"]:
                export_file = asset.get('export_file', '')
                if export_file:
                    asset_file = export_dir / "Assets" / export_file
                    if not asset_file.exists():
                        result['warnings'].append(
                            f"Export file not found: {export_file} (will need to be exported from UE5)"
                        )

            # Strict validation: UEFN compatibility checks
            if validation_level == "strict":
                # Check UEFN path format
                uefn_path = asset.get('uefn_path', '')
                if not uefn_path.startswith('/Game/'):
                    asset_errors.append(
                        f"Asset {i}: UEFN path should start with '/Game/', got: {uefn_path}"
                    )

                # Check asset type compatibility
                asset_type = asset.get('type', '')
                supported_types = ['StaticMesh', 'SkeletalMesh', 'Material', 'Texture']
                if asset_type not in supported_types:
                    result['warnings'].append(
                        f"Asset {i}: Type '{asset_type}' may not be fully supported in UEFN"
                    )

            if asset_errors:
                result['errors'].extend(asset_errors)
                result['valid'] = False
            else:
                validated_count += 1

        result['validated_assets'] = validated_count

        # Add recommendations
        if len(assets) == 0:
            result['recommendations'].append(
                "No assets in manifest - ensure static meshes are assigned to actors"
            )

        if validation_level == "basic":
            result['recommendations'].append(
                "Consider running 'standard' or 'strict' validation for more thorough checks"
            )

        result['recommendations'].append(
            "Assets must be manually exported from UE5 using File > Export Selected"
        )

        result['recommendations'].append(
            "Import exported assets to UEFN project using Content Browser > Import"
        )

        # Check for Verse spawn code
        verse_dir = export_dir / "Verse"
        if verse_dir.exists():
            verse_files = list(verse_dir.glob("*.verse"))
            if verse_files:
                result['verse_files'] = [str(f.name) for f in verse_files]
                result['recommendations'].append(
                    f"Found {len(verse_files)} Verse file(s) - copy to UEFN project Verse directory"
                )

        return json.dumps(result, indent=2)

    except json.JSONDecodeError as e:
        return json.dumps({
            "success": False,
            "error": f"Invalid JSON in manifest: {str(e)}"
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Validation failed: {str(e)}"
        })


def _generate_integration_notes(
    level_name: str,
    uefn_project_path: str,
    manifest: Dict[str, Any],
    spawn_code_path: Optional[Path]
) -> str:
    """Generate integration notes for UEFN project"""
    notes = f"""# UEFN Integration Notes
## Level: {level_name}

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**UEFN Project**: {uefn_project_path}

---

## Overview

This export contains:
- **{manifest['total_actors']}** actors from UE5 level
- **{len(manifest['assets'])}** unique assets requiring export
- **{len(manifest['actor_types'])}** different actor types

---

## Integration Steps

### 1. Export Assets from UE5

The following assets need to be exported from your UE5 project:

"""

    # List assets
    for i, asset in enumerate(manifest['assets'][:10], 1):  # First 10
        notes += f"{i}. `{asset['ue5_path']}` → `{asset['export_file']}`\n"

    if len(manifest['assets']) > 10:
        notes += f"\n... and {len(manifest['assets']) - 10} more assets (see manifest)\n"

    notes += """
**Export Process:**
1. Open UE5 project
2. Select assets in Content Browser
3. Right-click → Asset Actions → Export
4. Choose FBX format
5. Export to `Assets/` directory in this export

### 2. Import to UEFN

1. Open UEFN Editor
2. Navigate to Content Browser
3. Create folder: `ImportedAssets/{level_name}/`
4. Right-click → Import
5. Select exported FBX files
6. Configure import settings (use defaults for most cases)

### 3. Copy Verse Spawn Code

"""

    if spawn_code_path:
        notes += f"""Verse spawn code generated: `{spawn_code_path.name}`

**Installation:**
1. Copy `{spawn_code_path.name}` to your UEFN project Verse directory
2. Typical path: `{uefn_project_path}/Content/{level_name}/`
3. Rebuild Verse code in UEFN
4. Add spawner device to your island
5. Configure spawner device properties in editor

"""
    else:
        notes += "Verse spawn code not generated. Use `generate_verse_spawn_map()` to create it.\n\n"

    notes += """### 4. Configure Spawners

The generated Verse code creates `@editable` properties for spawner devices.
You'll need to:
1. Place Item Spawner devices in your UEFN island
2. Configure them for each asset type
3. Link spawners to the spawner device properties

---

## Actor Type Summary

"""

    for actor_type, count in manifest['actor_types'].items():
        notes += f"- **{actor_type}**: {count} instance(s)\n"

    notes += """
---

## Troubleshooting

**Assets not appearing in UEFN:**
- Ensure FBX export settings are correct
- Check import log for errors
- Verify asset paths in manifest

**Verse code errors:**
- Rebuild Verse code (Ctrl+F7)
- Check UEFN log for compilation errors
- Verify spawner device types match assets

**Spawners not working:**
- Ensure spawner devices are placed and linked
- Check transform data (position/rotation/scale)
- Verify spawner device settings

---

*Generated by UEFN Export Pipeline - Phase 4*
"""

    return notes


# Test/demo function
def demo_export():
    """Demonstrate the export tools"""
    print("=== Export MCP Tools Demo ===\n")

    # Example actor data
    actors_data = [
        {
            'name': 'Floor_1',
            'class': 'StaticMeshActor',
            'static_mesh': '/Game/StarterContent/Architecture/Floor_400x400',
            'location': {'x': 0.0, 'y': 0.0, 'z': 0.0},
            'rotation': {'pitch': 0.0, 'yaw': 0.0, 'roll': 0.0},
            'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0}
        },
        {
            'name': 'Wall_1',
            'class': 'StaticMeshActor',
            'static_mesh': '/Game/StarterContent/Architecture/Wall_400x400',
            'location': {'x': 400.0, 'y': 0.0, 'z': 0.0},
            'rotation': {'pitch': 0.0, 'yaw': 90.0, 'roll': 0.0},
            'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0}
        }
    ]

    # Export level
    print("1. Testing export_level_to_uefn()...")
    result = export_level_to_uefn(
        level_name='DemoLevel',
        actors_json=json.dumps(actors_data),
        export_path='Exports/DemoLevel',
        options={'generate_spawn_code': True}
    )

    result_data = json.loads(result)
    print(f"   Export {'succeeded' if result_data['success'] else 'failed'}")
    if result_data['success']:
        print(f"   - Actors: {result_data['total_actors']}")
        print(f"   - Assets: {result_data['total_assets']}")
        print(f"   - Manifest: {result_data['manifest_path']}")
        print(f"   - Spawn code: {result_data['spawn_code_path']}")

    # Generate spawn map
    print("\n2. Testing generate_verse_spawn_map()...")
    result = generate_verse_spawn_map(
        level_name='DemoLevel',
        actors_json=json.dumps(actors_data),
        output_path='Exports/DemoLevel/Verse/spawner.verse'
    )

    result_data = json.loads(result)
    print(f"   Generation {'succeeded' if result_data['success'] else 'failed'}")
    if result_data['success']:
        print(f"   - Lines: {result_data['lines_of_code']}")
        print(f"   - File: {result_data['output_path']}")

    # Package assets
    print("\n3. Testing package_assets_for_fortnite()...")
    result = package_assets_for_fortnite(
        manifest_path='Exports/DemoLevel/Manifests/DemoLevel_manifest.json',
        export_path='Exports/DemoLevel',
        validation_level='standard'
    )

    result_data = json.loads(result)
    print(f"   Validation {'succeeded' if result_data['success'] else 'failed'}")
    if result_data['success']:
        print(f"   - Valid: {result_data['valid']}")
        print(f"   - Assets: {result_data['validated_assets']}/{result_data['total_assets']}")
        if result_data['errors']:
            print(f"   - Errors: {len(result_data['errors'])}")
        if result_data['warnings']:
            print(f"   - Warnings: {len(result_data['warnings'])}")

    print("\n✅ Demo complete!")


if __name__ == '__main__':
    demo_export()
