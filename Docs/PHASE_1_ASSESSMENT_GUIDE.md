# Phase 1: UEFN Assessment Guide

This guide walks you through the assessment phase of the UEFN migration.

## Prerequisites

- [ ] Windows 10/11, macOS, or Linux with Wine/Proton
- [ ] Epic Games Launcher installed
- [ ] UE5.5+ installed (for asset export testing)
- [ ] ~20GB free disk space for UEFN installation

---

## Task 1: Install UEFN

### Steps

1. **Open Epic Games Launcher**
   - Launch the Epic Games Launcher application
   - Sign in with your Epic Games account

2. **Install UEFN**
   - Click on "Unreal Engine" tab
   - Find "UEFN" (Unreal Editor for Fortnite)
   - Click "Install"
   - Select installation directory (note this path for later)
   - Wait for download and installation to complete (~15-20 minutes)

3. **Launch UEFN**
   - Click "Launch" button
   - Wait for editor to initialize
   - You may be prompted to sign in to Epic Games again
   - Close any welcome screens

4. **Verify Installation**
   - Check that UEFN editor opens successfully
   - Note the version number (Help → About UEFN)
   - Close UEFN for now

### Expected Result
✅ UEFN installed and launches successfully

### Troubleshooting
- If UEFN won't install: Check Epic Games Launcher logs
- If editor crashes on launch: Update graphics drivers
- If login fails: Verify Epic Games account status

---

## Task 2: Locate Verse Digest Files

### What are Digest Files?
Digest files (`.digest.verse`) contain the complete API reference for Verse and Fortnite Creative. They are machine-readable definitions of all classes, functions, and types available in UEFN.

### Windows Instructions

1. **Open PowerShell**
   - Press `Win + X`, select "Windows PowerShell"

2. **Search for Digest Files**
   ```powershell
   # Search in typical UEFN installation directory
   Get-ChildItem "C:\Program Files\Epic Games\UEFN" -Recurse -Filter "*.digest.verse" -ErrorAction SilentlyContinue | Select-Object FullName
   ```

3. **Common Locations**
   - `C:\Program Files\Epic Games\UEFN\Engine\Extras\VerseDigests\`
   - `C:\Program Files\Epic Games\UEFN\FortniteGame\Content\VerseDigests\`
   - `C:\Program Files\Epic Games\UEFN\Engine\Plugins\*\Content\VerseDigests\`

### macOS Instructions

```bash
# Search in UEFN installation
find "/Users/Shared/Epic Games/UEFN" -name "*.digest.verse" 2>/dev/null
find "$HOME/Library/Application Support/Epic/UEFN" -name "*.digest.verse" 2>/dev/null
```

### Linux/WSL Instructions

```bash
# If using WSL, search Windows filesystem
find "/mnt/c/Program Files/Epic Games/UEFN" -name "*.digest.verse" 2>/dev/null

# Native Linux (if running UEFN via Wine/Proton)
find "$HOME/.local/share/Epic/UEFN" -name "*.digest.verse" 2>/dev/null
```

### Expected Files

You should find 10-20 `.digest.verse` files, including:
- ✅ `Fortnite.digest.verse` - Core Fortnite API (CRITICAL)
- ✅ `Verse.digest.verse` - Verse standard library (CRITICAL)
- ✅ `FortnitePlaysetDeviceGraffiti.digest.verse` - Device APIs
- ✅ Various device-specific digests (Button, Spawner, Timer, etc.)
- ✅ `UnrealEngine.digest.verse` - UE integration (if available)

### What to Do

1. **List all found files**
   - Copy the output to a text file
   - Count the total number of files

2. **Verify critical files exist**
   - Ensure `Fortnite.digest.verse` is present
   - Ensure `Verse.digest.verse` is present

3. **Note the directory path**
   - You'll need this for the copy step

### Expected Result
✅ Found 10-20 digest files
✅ Located installation directory
✅ Critical files (`Fortnite.digest.verse`, `Verse.digest.verse`) confirmed

### Troubleshooting
- **No files found**: Try searching the entire UEFN installation directory
- **Permission denied**: Run PowerShell/terminal as administrator
- **Different path**: UEFN might be installed in a custom location - check Epic Games Launcher settings

---

## Task 3: Check for Remote Control API Plugin

### Purpose
The Remote Control API would allow us to automate UEFN editor operations via HTTP, similar to how the UE5 MCP works. This is experimental - it may or may not be available.

### Steps

1. **Launch UEFN**
   - Open UEFN from Epic Games Launcher

2. **Open Plugins Menu**
   - Click `Edit` → `Plugins`
   - Wait for plugin list to load

3. **Search for Remote Control**
   - In the search box, type: `Remote Control`
   - Look for these plugins:
     - ✅ `Remote Control API`
     - ✅ `Remote Control Web Interface`
     - ✅ `Web Remote Control`

4. **Document Findings**
   - Take a screenshot of the plugins list
   - Note which plugins are available:
     - Plugin name
     - Version
     - Whether it's enabled/disabled
     - Any dependencies listed

5. **Test Enabling (Optional)**
   - If plugins are found, try enabling them
   - Restart UEFN if prompted
   - Check if any new menu items appear
   - Look for Remote Control settings (Edit → Project Settings → Plugins → Remote Control)

### Expected Result A (Best Case)
✅ Remote Control API plugins found
✅ Plugins can be enabled
✅ HTTP server settings accessible
→ **Action**: We can implement Approach C (UEFN automation)

### Expected Result B (Likely Case)
❌ Remote Control plugins not found in UEFN
→ **Action**: Skip Approach C, rely on Verse generation + manual workflows

### What to Record

Create a file `phase1_findings.txt` with:
```
Remote Control API Status: [AVAILABLE / NOT AVAILABLE]
Plugin Name (if found): _____________
Plugin Version: _____________
HTTP Server Port: _____________ (if configurable)
Notes: _____________
```

---

## Task 4: Test Asset Import Workflow

### Purpose
Verify that we can export assets from UE5 and import them into UEFN successfully.

### Prerequisites
- UE5.5+ installed
- UEFN installed
- Sample UE5 project (or create a blank one)

### Part A: Export from UE5

1. **Create Test Asset in UE5**
   - Launch UE5
   - Create new blank project (or open existing)
   - Create a simple static mesh (cube/sphere) or use a starter content mesh

2. **Export as FBX**
   - Right-click the static mesh in Content Browser
   - Select `Asset Actions` → `Export`
   - Choose FBX format
   - Export location: Desktop or known folder
   - Use default FBX settings
   - Note the file size and export time

3. **Alternative: Export via File Menu**
   - Select the asset
   - `File` → `Export Selected`
   - Save as `.fbx`

### Part B: Import to UEFN

1. **Launch UEFN**
   - Create new UEFN project (or use existing test project)

2. **Import FBX**
   - In Content Browser, click `Import`
   - Navigate to the exported FBX file
   - Select it and click `Open`
   - Review import settings dialog:
     - Mesh settings
     - Material handling
     - Collision settings
   - Click `Import` or `Import All`

3. **Verify Import**
   - Check if mesh appears in Content Browser
   - Double-click to view in Static Mesh Editor
   - Verify:
     - ✅ Geometry looks correct
     - ✅ Materials imported (or created placeholder)
     - ✅ Scale is reasonable
     - ✅ Collision generated
   - Drag mesh into UEFN level to test

4. **Test in UEFN Level**
   - Place imported mesh in level
   - Try moving, rotating, scaling
   - Save level
   - Test play (if possible)

### Expected Result
✅ FBX exports from UE5 successfully
✅ FBX imports to UEFN without errors
✅ Mesh appears correctly in UEFN
✅ Mesh can be placed and manipulated in level

### Document Findings

Record in `phase1_findings.txt`:
```
Asset Export/Import Test:
- UE5 Version: _____________
- UEFN Version: _____________
- Test Asset: _____________
- FBX Export: [SUCCESS / FAILED]
- UEFN Import: [SUCCESS / FAILED]
- Issues Encountered: _____________
- Notes: _____________
```

### Troubleshooting
- **Import fails**: Check FBX version (2014-2020 typically supported)
- **Materials missing**: Expected - we'll handle materials separately
- **Scale wrong**: Note scale factor for future exports
- **Collision issues**: May need to configure collision export settings

---

## Task 5: Copy Digest Files to Project

### Prerequisites
- Task 2 completed (digest files located)
- Project directory accessible

### Windows (PowerShell)

```powershell
# Set variables
$UEFNDigestPath = "C:\Program Files\Epic Games\UEFN\Engine\Extras\VerseDigests"
$ProjectPath = "C:\Users\esceb\OneDrive\Documents\GitHub\unreal-engine-mcp\VerseDigests"

# Copy all digest files
Copy-Item "$UEFNDigestPath\*.digest.verse" -Destination $ProjectPath -Verbose

# Verify
Get-ChildItem $ProjectPath -Filter "*.digest.verse" | Select-Object Name, Length
```

### Linux/macOS/WSL

```bash
# Set variables (update paths as needed)
UEFN_DIGEST_PATH="/mnt/c/Program Files/Epic Games/UEFN/Engine/Extras/VerseDigests"
PROJECT_PATH="/mnt/c/Users/esceb/OneDrive/Documents/GitHub/unreal-engine-mcp/VerseDigests"

# Copy files
cp "$UEFN_DIGEST_PATH"/*.digest.verse "$PROJECT_PATH/" -v

# Verify
ls -lh "$PROJECT_PATH"/*.digest.verse
```

### Manual Copy (Alternative)

1. Navigate to UEFN digest directory in File Explorer/Finder
2. Select all `.digest.verse` files
3. Copy (`Ctrl+C` / `Cmd+C`)
4. Navigate to project `VerseDigests/` directory
5. Paste (`Ctrl+V` / `Cmd+V`)

### Verify Copy

Check that files are present:
```bash
cd /mnt/c/Users/esceb/OneDrive/Documents/GitHub/unreal-engine-mcp
ls -lh VerseDigests/*.digest.verse
```

Expected output:
```
-rwxrwxrwx 1 user user  500K Nov 13 17:00 Fortnite.digest.verse
-rwxrwxrwx 1 user user  200K Nov 13 17:00 Verse.digest.verse
-rwxrwxrwx 1 user user   50K Nov 13 17:00 FortnitePlaysetDeviceGraffiti.digest.verse
... (more files)
```

### Expected Result
✅ All digest files copied to `VerseDigests/`
✅ File count matches source directory
✅ Files are readable (not corrupted)

---

## Task 6: Document Findings

### Create Phase 1 Assessment Report

Create `Docs/PHASE_1_FINDINGS.md` with the following information:

```markdown
# Phase 1 Assessment - Findings Report

**Date**: [Insert Date]
**UEFN Version**: [e.g., 5.5.0-12345678]
**Assessment Status**: [COMPLETE / IN PROGRESS]

---

## 1. UEFN Installation

- **Status**: [SUCCESS / FAILED]
- **Installation Path**: _____________
- **Version**: _____________
- **Disk Space Used**: _____________
- **Issues**: _____________

---

## 2. Verse Digest Files

- **Status**: [FOUND / NOT FOUND]
- **Location**: _____________
- **File Count**: _____________ files
- **Critical Files Present**:
  - [ ] Fortnite.digest.verse
  - [ ] Verse.digest.verse
  - [ ] FortnitePlaysetDeviceGraffiti.digest.verse
- **Total Size**: _____________
- **Issues**: _____________

---

## 3. Remote Control API

- **Status**: [AVAILABLE / NOT AVAILABLE]
- **Plugin Name**: _____________
- **Plugin Version**: _____________
- **Can Be Enabled**: [YES / NO]
- **HTTP Port**: _____________ (if configurable)
- **Decision**:
  - [ ] Implement Approach C (automation)
  - [x] Skip Approach C (manual workflows)
- **Notes**: _____________

---

## 4. Asset Import Workflow

- **UE5 Version**: _____________
- **Export Test**: [SUCCESS / FAILED]
- **Import Test**: [SUCCESS / FAILED]
- **Test Asset**: _____________
- **Issues Encountered**:
  - _____________
- **Scale Factor**: _____________ (UE5 → UEFN)
- **Material Handling**: _____________
- **Workflow Validated**: [YES / NO]

---

## 5. Digest Files Copied

- **Status**: [SUCCESS / FAILED]
- **Files Copied**: _____________ files
- **Verification**: [PASSED / FAILED]
- **Ready for Parsing**: [YES / NO]

---

## Overall Assessment

**Phase 1 Complete**: [YES / NO]

**Green Lights** (Ready to Proceed):
- [ ] UEFN installed and functional
- [ ] Digest files acquired and copied
- [ ] Asset workflow validated
- [ ] Remote Control decision made

**Blockers**:
- _____________

**Recommendations**:
- _____________

**Next Steps**:
1. Proceed to Phase 2: Verse Knowledge Base
2. Implement digest file parser
3. Begin building API index

---

**Prepared By**: [Your Name]
**Review Date**: [Date]
```

---

## Summary Checklist

Before proceeding to Phase 2, verify:

- [x] ✅ Directory structure created
- [ ] ✅ UEFN installed and tested
- [ ] ✅ Digest files located
- [ ] ✅ Remote Control API checked
- [ ] ✅ Asset workflow validated
- [ ] ✅ Digest files copied to project
- [ ] ✅ Phase 1 findings documented

---

## Next Phase

Once all tasks are complete:
→ **Proceed to Phase 2: Verse Knowledge Base Implementation**
- Implement `verse_parser.py`
- Parse digest files
- Build API index
- Create Verse templates

---

## Support

If you encounter issues:
1. Check UEFN documentation: https://dev.epicgames.com/documentation/en-us/uefn
2. Review UEFN forums: https://forums.unrealengine.com/c/development-discussion/uefn
3. Consult `UEFN_MIGRATION_PLAN.md` for detailed technical specs
4. Report issues to the project repository

---

*Phase 1 Assessment Guide - UEFN Migration Project*
