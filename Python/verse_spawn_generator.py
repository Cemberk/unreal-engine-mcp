#!/usr/bin/env python3
"""
Verse Spawn Code Generator

Generates Verse code to spawn actors based on UE5 level data.
Creates SpawnerDevice classes that recreate level layouts in UEFN.

Usage:
    generator = VerseSpawnGenerator()
    verse_code = generator.generate_spawn_code(actors_data, options)
"""

import json
import math
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class VerseSpawnGenerator:
    """
    Generates Verse code to spawn actors from UE5 level data
    """

    def __init__(self):
        """Initialize the spawn generator"""
        pass

    def _sort_actors_stable(self, actors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sort actors for deterministic export.

        Ensures stable ordering across exports for clean Git diffs.

        Sort key:
            1. Actor class (group by type)
            2. Actor name (alphabetical)
            3. Location X, Y, Z (spatial order)

        Args:
            actors: List of actor dictionaries

        Returns:
            Sorted list of actors
        """
        def sort_key(actor):
            return (
                actor.get('class', 'ZZZ'),  # Class name (ZZZ ensures Unknown sorts last)
                actor.get('name', ''),       # Actor name
                actor.get('location', {}).get('x', 0.0),
                actor.get('location', {}).get('y', 0.0),
                actor.get('location', {}).get('z', 0.0)
            )

        return sorted(actors, key=sort_key)

    def _generate_actor_id(self, actor: Dict[str, Any]) -> str:
        """
        Generate stable ID for actor.

        ID is deterministic and survives small position tweaks (rounds to 10cm).
        Useful for incremental exports and tracking actors across versions.

        Args:
            actor: Actor dictionary

        Returns:
            12-character hex ID (MD5 hash prefix)
        """
        class_name = actor.get('class', 'Unknown')
        actor_name = actor.get('name', '')

        # Round position to nearest 10cm to survive small tweaks
        loc = actor.get('location', {})
        x = round(loc.get('x', 0.0) / 10.0) * 10.0
        y = round(loc.get('y', 0.0) / 10.0) * 10.0
        z = round(loc.get('z', 0.0) / 10.0) * 10.0

        # Create deterministic ID string
        id_string = f"{class_name}_{actor_name}_{x}_{y}_{z}"

        # Generate short hash (first 12 chars of MD5)
        hash_obj = hashlib.md5(id_string.encode())
        return hash_obj.hexdigest()[:12]

    def generate_spawn_code(
        self,
        level_name: str,
        actors: List[Dict[str, Any]],
        asset_manifest: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate Verse code to spawn actors

        Args:
            level_name: Name of the level
            actors: List of actor dictionaries with transform, class, properties
            asset_manifest: Asset manifest mapping UE5 paths to UEFN paths
            options: Generation options

        Returns:
            Generated Verse code as string
        """
        options = options or {}

        # Sort actors for deterministic output (clean Git diffs)
        actors = self._sort_actors_stable(actors)

        # Build module name
        module_name = self._sanitize_name(level_name) + "_spawner"

        # Start building code
        lines = []

        # Imports
        lines.extend(self._generate_imports())
        lines.append("")

        # Documentation
        lines.append(f"# {level_name} Level Spawner")
        lines.append(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"# Total Actors: {len(actors)}")
        lines.append("")

        # Class definition
        lines.append(f"{module_name} := class(creative_device):")
        lines.append("")

        # Properties for spawner devices
        if options.get('use_spawner_devices', True):
            lines.extend(self._generate_spawner_properties(actors, asset_manifest))
            lines.append("")

        # OnBegin method
        lines.extend(self._generate_on_begin(actors, options))
        lines.append("")

        # Spawn methods
        lines.extend(self._generate_spawn_methods(actors, asset_manifest, options))

        return '\n'.join(lines)

    def _generate_imports(self) -> List[str]:
        """Generate import statements"""
        return [
            "using { /Fortnite.com/Devices }",
            "using { /Verse.org/Simulation }",
            "using { /UnrealEngine.com/Temporary/SpatialMath }",
            "using { /UnrealEngine.com/Temporary/Diagnostics }"
        ]

    def _generate_spawner_properties(
        self,
        actors: List[Dict[str, Any]],
        asset_manifest: Dict[str, Any]
    ) -> List[str]:
        """Generate @editable spawner device properties"""
        lines = []

        # Group actors by type
        actor_types = {}
        for actor in actors:
            actor_class = actor.get('class', 'Unknown')
            if actor_class not in actor_types:
                actor_types[actor_class] = []
            actor_types[actor_class].append(actor)

        # Generate spawner arrays for each type
        for i, (actor_class, actors_of_type) in enumerate(actor_types.items()):
            sanitized_class = self._sanitize_name(actor_class)
            lines.append(f"    @editable")
            lines.append(f"    {sanitized_class}_Spawners<private>: []item_spawner_device = array{{}}")

        return lines

    def _generate_on_begin(
        self,
        actors: List[Dict[str, Any]],
        options: Dict[str, Any]
    ) -> List[str]:
        """Generate OnBegin method"""
        lines = [
            "    # Called when the device is started in a running game",
            "    OnBegin<override>()<suspends>:void=",
            "        Print(\"Level spawner initialized\")",
            ""
        ]

        if options.get('spawn_on_begin', True):
            lines.append("        # Spawn all actors")
            lines.append("        SpawnAllActors()")

        return lines

    def _generate_spawn_methods(
        self,
        actors: List[Dict[str, Any]],
        asset_manifest: Dict[str, Any],
        options: Dict[str, Any]
    ) -> List[str]:
        """Generate spawn methods for actors"""
        lines = []

        # Main spawn all method
        lines.append("    # Spawn all actors from the level")
        lines.append("    SpawnAllActors():void=")

        # Group actors by type for organized spawning
        actor_groups = self._group_actors_by_type(actors)

        for actor_type, actors_of_type in actor_groups.items():
            sanitized_type = self._sanitize_name(actor_type)
            lines.append(f"        Spawn{sanitized_type}Actors()")

        lines.append("")

        # Generate individual spawn methods for each type
        for actor_type, actors_of_type in actor_groups.items():
            lines.extend(self._generate_type_spawn_method(actor_type, actors_of_type, asset_manifest))
            lines.append("")

        # Generate individual actor spawn functions
        if options.get('detailed_spawn_functions', False):
            for i, actor in enumerate(actors):
                lines.extend(self._generate_actor_spawn_function(i, actor, asset_manifest))
                lines.append("")

        return lines

    def _generate_type_spawn_method(
        self,
        actor_type: str,
        actors: List[Dict[str, Any]],
        asset_manifest: Dict[str, Any]
    ) -> List[str]:
        """Generate spawn method for a specific actor type"""
        sanitized_type = self._sanitize_name(actor_type)

        lines = [
            f"    # Spawn {len(actors)} {actor_type} actor(s)",
            f"    Spawn{sanitized_type}Actors():void="
        ]

        # Generate spawn calls for each actor
        for i, actor in enumerate(actors):
            location = actor.get('location', {})
            rotation = actor.get('rotation', {})

            x = location.get('x', 0.0)
            y = location.get('y', 0.0)
            z = location.get('z', 0.0)

            pitch = rotation.get('pitch', 0.0)
            yaw = rotation.get('yaw', 0.0)
            roll = rotation.get('roll', 0.0)

            # Convert to Verse vector3 and rotation
            lines.append(f"        # Actor {i + 1}: {actor.get('name', 'Unnamed')}")
            lines.append(f"        Location_{i} := vector3{{X:={x:.2f}, Y:={y:.2f}, Z:={z:.2f}}}")
            lines.append(f"        Rotation_{i} := rotation{{Pitch:={pitch:.2f}, Yaw:={yaw:.2f}, Roll:={roll:.2f}}}")

            # Spawn call (commented out - needs actual spawner device)
            lines.append(f"        # Spawn actor at Location_{i} with Rotation_{i}")
            lines.append(f"        # SpawnerDevice.SpawnProp(Location_{i}, Rotation_{i})")
            lines.append("")

        return lines

    def _generate_actor_spawn_function(
        self,
        index: int,
        actor: Dict[str, Any],
        asset_manifest: Dict[str, Any]
    ) -> List[str]:
        """Generate individual spawn function for an actor"""
        lines = []

        actor_name = actor.get('name', f'Actor_{index}')
        sanitized_name = self._sanitize_name(actor_name)

        lines.append(f"    # Spawn {actor_name}")
        lines.append(f"    Spawn{sanitized_name}():void=")

        location = actor.get('location', {})
        rotation = actor.get('rotation', {})
        scale = actor.get('scale', {'x': 1.0, 'y': 1.0, 'z': 1.0})

        lines.append(f"        Location := vector3{{")
        lines.append(f"            X:={location.get('x', 0.0):.2f},")
        lines.append(f"            Y:={location.get('y', 0.0):.2f},")
        lines.append(f"            Z:={location.get('z', 0.0):.2f}")
        lines.append(f"        }}")
        lines.append(f"")
        lines.append(f"        Rotation := rotation{{")
        lines.append(f"            Pitch:={rotation.get('pitch', 0.0):.2f},")
        lines.append(f"            Yaw:={rotation.get('yaw', 0.0):.2f},")
        lines.append(f"            Roll:={rotation.get('roll', 0.0):.2f}")
        lines.append(f"        }}")
        lines.append(f"")
        lines.append(f"        Scale := vector3{{")
        lines.append(f"            X:={scale.get('x', 1.0):.2f},")
        lines.append(f"            Y:={scale.get('y', 1.0):.2f},")
        lines.append(f"            Z:={scale.get('z', 1.0):.2f}")
        lines.append(f"        }}")
        lines.append(f"")
        lines.append(f"        # Spawn actor with transform")
        lines.append(f"        # SpawnerDevice.SpawnProp(Location, Rotation, Scale)")

        return lines

    def _group_actors_by_type(self, actors: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group actors by their class type"""
        groups = {}
        for actor in actors:
            actor_class = actor.get('class', 'Unknown')
            if actor_class not in groups:
                groups[actor_class] = []
            groups[actor_class].append(actor)
        return groups

    def _sanitize_name(self, name: str) -> str:
        """Sanitize name for use as Verse identifier"""
        # Remove Blueprint prefix/suffix
        name = name.replace('Blueprint', '').replace('_C', '')

        # Remove invalid characters
        sanitized = ''.join(c if c.isalnum() or c == '_' else '_' for c in name)

        # Ensure it starts with a letter or underscore
        if sanitized and not (sanitized[0].isalpha() or sanitized[0] == '_'):
            sanitized = '_' + sanitized

        # Remove consecutive underscores
        while '__' in sanitized:
            sanitized = sanitized.replace('__', '_')

        return sanitized or 'Unnamed'

    def generate_asset_manifest(
        self,
        level_name: str,
        actors: List[Dict[str, Any]],
        export_path: Path
    ) -> Dict[str, Any]:
        """
        Generate asset manifest for UE5 -> UEFN mapping

        Args:
            level_name: Name of the level
            actors: List of actors to export
            export_path: Path where assets will be exported

        Returns:
            Asset manifest dictionary
        """
        # Sort actors for deterministic output
        actors = self._sort_actors_stable(actors)

        manifest = {
            'level_name': level_name,
            'export_date': datetime.now().isoformat(),
            'export_path': str(export_path),
            'total_actors': len(actors),
            'actors': [],  # Add actors list with IDs
            'assets': [],
            'actor_types': {}
        }

        # Collect unique asset references
        asset_map = {}

        for actor in actors:
            actor_class = actor.get('class', 'Unknown')
            mesh_path = actor.get('static_mesh', '')

            # Generate stable ID for actor
            actor_id = self._generate_actor_id(actor)

            # Add actor to manifest with ID
            manifest['actors'].append({
                'id': actor_id,
                'name': actor.get('name', 'Unnamed'),
                'class': actor_class,
                'location': actor.get('location', {}),
                'rotation': actor.get('rotation', {}),
                'scale': actor.get('scale', {'x': 1.0, 'y': 1.0, 'z': 1.0})
            })

            if mesh_path and mesh_path not in asset_map:
                asset_map[mesh_path] = {
                    'ue5_path': mesh_path,
                    'uefn_path': self._generate_uefn_path(mesh_path, level_name),
                    'type': 'StaticMesh',
                    'export_file': self._generate_export_filename(mesh_path),
                    'references': 0
                }

            if mesh_path in asset_map:
                asset_map[mesh_path]['references'] += 1

            # Track actor types
            if actor_class not in manifest['actor_types']:
                manifest['actor_types'][actor_class] = 0
            manifest['actor_types'][actor_class] += 1

        # Add assets to manifest
        manifest['assets'] = list(asset_map.values())

        return manifest

    def _generate_uefn_path(self, ue5_path: str, level_name: str) -> str:
        """Generate UEFN content path from UE5 path"""
        # Extract asset name
        parts = ue5_path.split('/')
        asset_name = parts[-1] if parts else 'Asset'

        # Generate UEFN path
        return f"/Game/ImportedAssets/{level_name}/{asset_name}"

    def _generate_export_filename(self, asset_path: str) -> str:
        """Generate export filename for asset"""
        parts = asset_path.split('/')
        asset_name = parts[-1] if parts else 'Asset'
        return f"{asset_name}.fbx"


def main():
    """Example usage"""
    import sys

    print("=== Verse Spawn Code Generator ===\n")

    # Example actor data
    actors = [
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
        },
        {
            'name': 'Pillar_1',
            'class': 'StaticMeshActor',
            'static_mesh': '/Game/StarterContent/Architecture/Pillar_50x500',
            'location': {'x': 0.0, 'y': 400.0, 'z': 0.0},
            'rotation': {'pitch': 0.0, 'yaw': 0.0, 'roll': 0.0},
            'scale': {'x': 1.0, 'y': 1.0, 'z': 1.0}
        }
    ]

    asset_manifest = {
        'level_name': 'TestLevel',
        'assets': []
    }

    generator = VerseSpawnGenerator()

    # Generate spawn code
    print("Generating spawn code...")
    code = generator.generate_spawn_code(
        level_name='TestLevel',
        actors=actors,
        asset_manifest=asset_manifest,
        options={'spawn_on_begin': True}
    )

    print("\n=== Generated Verse Code ===\n")
    print(code)

    # Generate manifest
    print("\n\n=== Generating Asset Manifest ===\n")
    manifest = generator.generate_asset_manifest(
        level_name='TestLevel',
        actors=actors,
        export_path=Path('Exports/TestLevel')
    )

    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
