# Verse Digest Files

This directory contains raw Verse API digest files from UEFN installation.

## Required Files

Copy these files from your UEFN installation:
- `Fortnite.digest.verse` - Core Fortnite Creative API
- `Verse.digest.verse` - Verse standard library
- `FortnitePlaysetDeviceGraffiti.digest.verse` - Device APIs
- `UnrealEngine.digest.verse` - UE integration (if available)
- Any other `*.digest.verse` files found in UEFN

## Typical UEFN Digest Locations

**Windows**:
```
C:\Program Files\Epic Games\UEFN\Engine\Extras\VerseDigests\
C:\Program Files\Epic Games\UEFN\FortniteGame\Content\VerseDigests\
```

**Mac**:
```
/Users/Shared/Epic Games/UEFN/Engine/Extras/VerseDigests/
```

## How to Find

Run this command from project root:
```bash
# Windows (PowerShell)
Get-ChildItem "C:\Program Files\Epic Games\UEFN" -Recurse -Filter "*.digest.verse"

# Linux/Mac/WSL
find "/mnt/c/Program Files/Epic Games/UEFN" -name "*.digest.verse" 2>/dev/null
```

## Status

- [ ] Files copied
- [ ] Verified file count (should be 10-20 files)
- [ ] Ready for parsing (Phase 2)
