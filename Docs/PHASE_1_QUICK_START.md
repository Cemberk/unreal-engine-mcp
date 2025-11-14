# Phase 1 Quick Start - TL;DR

Quick reference for completing Phase 1 assessment tasks.

## 1. Install UEFN (5 minutes)
```
Epic Games Launcher → Unreal Engine → UEFN → Install
```

## 2. Find Digest Files (2 minutes)

**Windows PowerShell**:
```powershell
Get-ChildItem "C:\Program Files\Epic Games\UEFN" -Recurse -Filter "*.digest.verse" | Select-Object FullName
```

**Linux/Mac/WSL**:
```bash
find "/mnt/c/Program Files/Epic Games/UEFN" -name "*.digest.verse" 2>/dev/null
```

## 3. Copy Digest Files (1 minute)

**Windows PowerShell**:
```powershell
Copy-Item "C:\Program Files\Epic Games\UEFN\Engine\Extras\VerseDigests\*.digest.verse" -Destination "C:\Users\esceb\OneDrive\Documents\GitHub\unreal-engine-mcp\VerseDigests"
```

**Linux/Mac/WSL**:
```bash
cp "/mnt/c/Program Files/Epic Games/UEFN/Engine/Extras/VerseDigests/"*.digest.verse "/mnt/c/Users/esceb/OneDrive/Documents/GitHub/unreal-engine-mcp/VerseDigests/"
```

## 4. Check Remote Control (3 minutes)
```
UEFN → Edit → Plugins → Search "Remote Control"
```
Document: Found or Not Found

## 5. Test Asset Import (10 minutes)
```
UE5: Create cube → Export as FBX
UEFN: Import FBX → Place in level → Verify
```

## 6. Verify Everything (1 minute)
```bash
cd /mnt/c/Users/esceb/OneDrive/Documents/GitHub/unreal-engine-mcp
ls VerseDigests/*.digest.verse | wc -l  # Should be 10-20
```

## Total Time: ~20-30 minutes

## What You Need to Tell Me After Completion:

1. **Digest file count**: How many `.digest.verse` files did you find?
2. **Remote Control API**: Available or not?
3. **Asset import**: Success or issues?
4. **Any blockers**: Problems encountered?

Once you provide this info, we proceed to Phase 2! 🚀
