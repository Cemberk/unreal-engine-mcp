# UEFN Asset Exports

This directory contains assets exported from UE5 for UEFN import.

## Subdirectories

### manifests/
JSON manifests mapping UE5 assets to UEFN paths:
```json
{
  "level_name": "CastleLevel",
  "export_date": "2024-01-01",
  "assets": [
    {
      "ue5_path": "/Game/Structures/Castle/Tower",
      "uefn_path": "/Game/ImportedAssets/Castle/Tower",
      "type": "StaticMesh",
      "file": "meshes/Tower.fbx"
    }
  ]
}
```

### meshes/
Exported static meshes (FBX format):
- Compatible with UEFN import
- Validated poly counts (<100k tris recommended)
- LODs preserved where possible

### materials/
Material definitions and textures:
- Material instance parameters (JSON)
- Texture files (PNG/TGA)
- Material setup documentation

### verse/
Generated Verse spawn code:
- `{LevelName}_Spawner.verse` - Main spawner device
- Actor positions, rotations, scales
- Material assignments
- Physics properties (as comments)

## Workflow

1. Build level in UE5 using MCP tools
2. Run `export_level_to_uefn(level_name)` → Generates all files
3. Review manifest in `manifests/{level_name}.json`
4. Import meshes to UEFN Content Browser
5. Copy Verse code to UEFN project
6. Build and test in Fortnite Creative

## Status

- [ ] Export pipeline implemented (Phase 4)
- [ ] Sample exports created
- [ ] Import workflow verified
