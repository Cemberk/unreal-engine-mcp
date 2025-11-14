# UEFN/Fortnite MCP Migration Plan

## Executive Summary

This document outlines the migration strategy for converting the existing **Unreal Engine MCP** (13,400 lines of C++/Python code) to a **UEFN-compatible MCP** that can build Fortnite Creative islands using Verse and the Fortnite.com API.

### Current State
- **Architecture**: C++ Editor Plugin + Python MCP Server
- **Communication**: TCP Socket (127.0.0.1:55557)
- **Capabilities**: 27 MCP tools for actor spawning, Blueprint creation, physics, materials, and complex structure generation
- **Target Engine**: Unreal Engine 5.5+
- **Codebase**: ~6,100 lines C++, ~7,300 lines Python

### Target State
- **Architecture**: Hybrid approach using UE5.5+ for asset authoring + UEFN for Verse/runtime deployment
- **Verse Integration**: Agent generates valid Verse code for gameplay logic and device interactions
- **Asset Pipeline**: Export UE5 assets → Import to UEFN → Verse-driven gameplay
- **Communication**: Current MCP stack for UE5 + Verse code generation + optional UEFN remote control

---

## Migration Strategy: Three-Pronged Approach

### Approach A: Unreal Engine as Build Environment (HIGHEST PRIORITY)

**Rationale**: Keep the existing MCP stack for world-building and asset creation, then export to UEFN.

#### A.1: Current Capabilities to Preserve

**✅ Retain Fully (No Changes Needed)**
- All 11 building structure generation helpers:
  - `create_town()`, `construct_house()`, `construct_mansion()`
  - `create_castle_fortress()`, `create_suspension_bridge()`, `create_aqueduct()`
  - `create_tower()`, `create_arch()`, `create_pyramid()`, `create_wall()`, etc.
- Actor management tools: `get_actors_in_level()`, `find_actors_by_name()`, `delete_actor()`
- Transform manipulation: `set_actor_transform()`
- Material tools: `get_available_materials()`, `apply_material_to_actor()`

**⚠️ Adapt for UEFN Export**
- Blueprint creation → Generate as UE5 Blueprints, then convert to UEFN-compatible assets
- Physics properties → Tag for later Verse implementation (UEFN has different physics model)
- Material colors → Export material parameters for UEFN material instances

**❌ Deprecate (UEFN Limitations)**
- Direct UEFN Blueprint spawning (Verse handles this instead)
- Real-time compilation in UEFN (compile in UE5, import to UEFN)

#### A.2: Asset Export Pipeline (NEW)

**New MCP Tools to Add**:

```python
# Asset Export Tools
export_level_to_uefn(level_name, export_path, asset_manifest)
  → Exports actors, meshes, materials to UEFN-compatible format
  → Generates asset manifest (JSON) mapping UE5 → UEFN paths
  → Creates Verse scaffolding for spawning exported actors

package_assets_for_fortnite(asset_list, metadata)
  → Packages static meshes, materials, textures
  → Follows Epic's UEFN asset migration guidelines
  → Validates asset compatibility (poly count, texture sizes, etc.)

generate_verse_spawn_map(level_name)
  → Analyzes current level actors
  → Generates Verse code to recreate actor layout
  → Outputs SpawnerDevice configurations
```

**Implementation Path**:
1. **Extend C++ Plugin** (UnrealMCP):
   - Add `FEpicUnrealMCPExportCommands` class
   - Use `UAssetExportTask` API to export assets
   - Implement FBX/DataAsset export for UEFN compatibility
   - Generate JSON manifests for asset mapping

2. **Python Server Additions**:
   - Add `export_tools.py` helper module
   - Implement asset path resolution for UEFN
   - Create Verse code generation templates

3. **Workflow**:
   ```
   UE5 Editor (MCP-controlled)
     → Build level with existing tools
     → Export assets via new tools
     → Generate Verse spawn code
     → Manual import to UEFN
     → Verify in Fortnite Creative
   ```

---

### Approach B: Verse-Aware Agent (CRITICAL PATH)

**Rationale**: The agent must understand Verse syntax and the Fortnite.com API to generate valid gameplay code.

#### B.1: Verse Language Knowledge Base

**Data Sources to Integrate**:

1. **Verse Language Reference** (from dev.epicgames.com)
   - Syntax: classes, functions, attributes, concurrency
   - Type system: int, float, logic, string, option, arrays, maps
   - Failure context: `failable`, `?`, error handling
   - Concurrency: `race`, `spawn`, `sync`, `branch`

2. **Fortnite.com API Digest Files** (Ground Truth)
   - `Fortnite.digest.verse` → Core game API
   - `FortnitePlaysetDeviceGraffiti.digest.verse` → Device APIs
   - `Verse.digest.verse` → Standard library
   - `UnrealEngine.digest.verse` → UE integration (if available)

3. **UEFN VSCode Extension** (Optional)
   - Language Server Protocol (LSP) integration
   - IntelliSense/autocomplete data
   - Diagnostics and validation

**Implementation Strategy**:

**Option 1: Digest File Parsing (Recommended)**
- Parse `.digest.verse` files into structured JSON/schema
- Extract all classes, devices, functions, enums
- Build a queryable knowledge base (SQLite or JSON documents)
- Expose via MCP tools for agent reasoning

**Option 2: Web Scraping + Manual Curation**
- Scrape Verse API Reference pages
- Convert to markdown knowledge base
- Use Claude's extended context for reference

**Option 3: Hybrid (Best)**
- Parse digest files for machine-readable API
- Supplement with web docs for examples and explanations
- Create curated Verse code templates for common patterns

#### B.2: New Verse Generation MCP Tools

```python
# Verse Code Generation
generate_verse_device(module_name, device_type, config_params)
  → Creates Verse device class (extends FortnitePlaysetDevice)
  → Implements OnBegin(), Subscribe() patterns
  → Validates against Fortnite.com API types
  → Returns: Verse code string + file path

insert_or_update_verse_file(project_path, file_path, code)
  → Edits .verse files in UEFN project tree
  → Preserves existing code structure
  → Handles imports and module declarations

validate_verse_code(file_path)
  → Runs UEFN build/diagnostics
  → Parses error output
  → Returns: validation status + error messages

query_fortnite_api(search_query)
  → Searches Fortnite.com API knowledge base
  → Returns: matching classes, functions, parameters
  → Example: "How do I spawn an item?" → ItemGranter device

generate_verse_gameplay_logic(description, context)
  → Takes natural language description
  → Generates Verse code using Fortnite.com API
  → Handles common patterns (timers, scoring, team management, etc.)
```

**Implementation Requirements**:

1. **Verse Parser Module** (Python)
   ```python
   # verse_parser.py
   class DigestParser:
       def parse_digest_file(path: str) -> VerseModule
       def extract_classes() -> List[VerseClass]
       def extract_functions() -> List[VerseFunction]
       def build_api_index() -> Dict[str, APIEntry]
   ```

2. **Verse Code Generator** (Python)
   ```python
   # verse_generator.py
   class VerseCodeGenerator:
       def __init__(api_reference: VerseAPIReference)
       def generate_device(template: str, params: Dict) -> str
       def validate_syntax(code: str) -> ValidationResult
       def format_code(code: str) -> str
   ```

3. **UEFN Project Interface** (Python + Optional C++)
   ```python
   # uefn_interface.py
   class UEFNProject:
       def find_verse_files() -> List[Path]
       def update_verse_file(path: Path, content: str)
       def trigger_build() -> BuildResult
       def get_diagnostics() -> List[Diagnostic]
   ```

#### B.3: Knowledge Base Construction

**Phase 1: Digest File Acquisition**
1. Locate UEFN installation directory
2. Find digest files (typically in `Epic Games/UEFN/Engine/Extras/VerseDigests/`)
3. Copy to MCP project: `/home/user/unreal-engine-mcp/VerseDigests/`

**Phase 2: Parsing & Indexing**
1. Parse all `.digest.verse` files
2. Extract API surface:
   - Classes and their inheritance
   - Functions with signatures (parameters, return types, failure modes)
   - Attributes and properties
   - Enums and constants
3. Build searchable index (JSON or SQLite)
4. Generate markdown reference docs for agent context

**Phase 3: Template Library**
Create Verse code templates for common patterns:
- Device creation (button, trigger, spawner, etc.)
- Player interaction (damage, healing, teleport)
- Scoring systems (elimination tracker, round manager)
- UI elements (HUD messages, billboards)
- Team management (team assignment, score tracking)

**File Structure**:
```
/home/user/unreal-engine-mcp/
├── VerseDigests/                    # Raw digest files
│   ├── Fortnite.digest.verse
│   ├── Verse.digest.verse
│   └── FortnitePlaysetDevice*.digest.verse
├── VerseParsed/                     # Parsed API data
│   ├── fortnite_api.json            # Structured API index
│   ├── verse_stdlib.json            # Standard library
│   └── api_index.sqlite             # Queryable database
├── VerseTemplates/                  # Code templates
│   ├── devices/
│   │   ├── button_device.verse
│   │   ├── spawner_device.verse
│   │   └── timer_device.verse
│   ├── gameplay/
│   │   ├── scoring_system.verse
│   │   ├── team_manager.verse
│   │   └── round_controller.verse
│   └── utils/
│       ├── player_helpers.verse
│       └── math_utils.verse
└── Python/
    ├── verse_parser.py              # Digest parser
    ├── verse_generator.py           # Code generator
    └── verse_knowledge_base.py      # API query system
```

---

### Approach C: Remote Control UEFN (EXPERIMENTAL)

**Rationale**: If UEFN includes the RemoteControlAPI plugin, we can automate editor operations just like UE5.

#### C.1: Feasibility Check

**Steps to Determine Support**:
1. Open UEFN Editor
2. Navigate to Edit → Plugins
3. Search for "Remote Control"
4. Check if `Remote Control API` and `Remote Control Web Interface` are available
5. If yes → Enable plugins and restart UEFN

**Expected Result**:
- ✅ Best Case: Plugin exists and works → Full editor automation possible
- ⚠️ Partial: Plugin exists but with restrictions → Limited automation
- ❌ Worst Case: Plugin not available → Skip this approach

#### C.2: Remote Control Integration (If Available)

**New MCP Tools**:

```python
# UEFN Remote Control Tools
rc_connect_uefn(host='127.0.0.1', port=7001)
  → Connect to UEFN Remote Control HTTP server
  → Verify connection and available presets

rc_get_preset_list()
  → Lists all Remote Control Presets in UEFN
  → Returns available properties and functions

rc_set_property(preset, object_path, property_name, value)
  → Sets property value on UEFN object
  → Example: Set actor location, material color, etc.

rc_call_function(preset, object_path, function_name, args)
  → Invokes function in UEFN
  → Example: Spawn actor, compile blueprint, etc.

rc_create_preset(name, objects)
  → Creates Remote Control Preset in UEFN
  → Exposes specified objects/properties for remote access
```

**Implementation**:
1. **Python HTTP Client** (no C++ needed):
   ```python
   # uefn_remote_control.py
   class UEFNRemoteControl:
       def __init__(self, host: str, port: int)
       def call_function(preset, obj, fn, args) -> Dict
       def set_property(preset, obj, prop, val) -> bool
       def get_property(preset, obj, prop) -> Any
   ```

2. **UEFN Setup Guide**:
   - Enable Remote Control plugins in UEFN
   - Create Remote Control Preset for common operations
   - Configure HTTP server settings
   - Test connectivity from Python

3. **Use Cases**:
   - Trigger builds from Python
   - Modify Verse file properties
   - Spawn preview actors in UEFN
   - Automate repetitive tasks

**Fallback**: If Remote Control API is not available, this approach is not viable. Fall back to manual UEFN workflows with Verse code generation only.

---

## Migration Phases

### Phase 1: Assessment & Setup (Week 1)

**Objectives**:
- Verify UEFN capabilities and limitations
- Acquire Verse digest files
- Set up UEFN development environment

**Tasks**:
1. ✅ Install UEFN (latest version)
2. ✅ Check for Remote Control API plugin availability
3. ✅ Locate and copy Verse digest files
4. ✅ Review Epic's UEFN documentation:
   - Asset migration guide (UE → UEFN)
   - Verse language reference
   - Fortnite.com API reference
5. ✅ Create test UEFN project
6. ✅ Test asset import workflow (UE5 → UEFN)

**Deliverables**:
- UEFN installation verified
- Digest files copied to project
- Feasibility report on Remote Control API
- Test asset pipeline documented

---

### Phase 2: Verse Knowledge Base (Week 2-3)

**Objectives**:
- Parse Verse digest files
- Build queryable API reference
- Create Verse code templates

**Tasks**:
1. ✅ Implement `verse_parser.py`:
   - Parse `.digest.verse` syntax
   - Extract classes, functions, attributes
   - Handle inheritance and module structure
2. ✅ Build API index:
   - JSON schema for API entries
   - SQLite database for fast queries
   - Markdown docs for human reference
3. ✅ Create Verse templates:
   - 10-15 device templates (Button, Spawner, Timer, etc.)
   - 5-10 gameplay patterns (Scoring, Teams, Rounds)
   - Utility functions (Player queries, math helpers)
4. ✅ Implement `verse_knowledge_base.py`:
   - Query API by name, type, category
   - Search by description/keywords
   - Return code examples

**Deliverables**:
- Verse API database (JSON + SQLite)
- 25-30 Verse code templates
- API query tool (Python module)
- Documentation on Verse patterns

---

### Phase 3: Verse Code Generation Tools (Week 4-5)

**Objectives**:
- Add MCP tools for Verse code generation
- Implement validation pipeline
- Test with sample UEFN projects

**Tasks**:
1. ✅ Implement `verse_generator.py`:
   - Template-based code generation
   - Parameter validation against API
   - Syntax formatting (indentation, naming conventions)
2. ✅ Add MCP tools:
   - `generate_verse_device()`
   - `insert_or_update_verse_file()`
   - `validate_verse_code()`
   - `query_fortnite_api()`
3. ✅ UEFN build integration:
   - Trigger UEFN build via CLI or Remote Control
   - Parse diagnostics output
   - Return errors to agent
4. ✅ Testing:
   - Generate 10 sample devices
   - Validate in UEFN
   - Ensure compilation success

**Deliverables**:
- 4 new MCP tools for Verse
- Build validation pipeline
- 10 validated Verse device examples
- Integration tests

---

### Phase 4: Asset Export Pipeline (Week 6-7)

**Objectives**:
- Extend UE5 MCP to export UEFN-compatible assets
- Generate Verse spawn code from UE5 levels
- Document export workflow

**Tasks**:
1. ✅ C++ Plugin Extension:
   - Add `FEpicUnrealMCPExportCommands` class
   - Implement asset export (FBX, DataAsset, materials)
   - Generate asset manifest (JSON)
2. ✅ Python MCP Tools:
   - `export_level_to_uefn()`
   - `package_assets_for_fortnite()`
   - `generate_verse_spawn_map()`
3. ✅ Verse Spawn Code Generator:
   - Analyze UE5 level actors
   - Map to UEFN asset paths (using manifest)
   - Generate Verse `SpawnerDevice` configurations
   - Output actor positions, rotations, scales
4. ✅ End-to-End Test:
   - Build sample town in UE5 using existing tools
   - Export assets to UEFN
   - Import to UEFN project
   - Use generated Verse code to spawn structures
   - Verify in Fortnite Creative

**Deliverables**:
- 3 new MCP tools for asset export
- Asset export pipeline documentation
- Sample exported level (town or castle)
- Verse spawn code for sample level

---

### Phase 5: UEFN Remote Control (Week 8) [CONDITIONAL]

**Objectives**:
- If Remote Control API is available, integrate for editor automation
- If not available, skip and document limitations

**Tasks (If Available)**:
1. ✅ Enable Remote Control in UEFN
2. ✅ Create Remote Control Presets
3. ✅ Implement Python HTTP client
4. ✅ Add MCP tools (`rc_connect_uefn`, `rc_set_property`, etc.)
5. ✅ Test automation workflows
6. ✅ Document use cases

**Tasks (If Not Available)**:
1. ✅ Document limitation
2. ✅ Define manual workflow alternatives
3. ✅ Consider other automation methods (CLI, scripting)

**Deliverables**:
- Remote Control integration (if available)
- OR: Manual workflow documentation (if not)

---

### Phase 6: Integration & Testing (Week 9-10)

**Objectives**:
- Integrate all components
- End-to-end testing with real use cases
- Performance optimization
- Documentation

**Tasks**:
1. ✅ Full Workflow Test:
   - **UE5 Phase**:
     - Create complex structure (castle + town)
     - Apply materials and physics
     - Export assets + generate Verse
   - **UEFN Phase**:
     - Import assets to UEFN project
     - Insert generated Verse code
     - Build and validate
     - Launch in Fortnite Creative
     - Verify structure appears correctly
2. ✅ Agent Testing:
   - Test natural language → Verse generation
   - Validate API queries work correctly
   - Ensure error handling is robust
3. ✅ Performance:
   - Optimize Verse code generation speed
   - Improve asset export performance
   - Cache API queries
4. ✅ Documentation:
   - Update README.md
   - Create UEFN_WORKFLOW.md guide
   - Document all new MCP tools
   - Create video tutorial (optional)

**Deliverables**:
- Fully functional UEFN-MCP system
- Complete test suite
- Comprehensive documentation
- Sample UEFN project with generated content

---

### Phase 7: Deprecation & Cleanup (Week 11)

**Objectives**:
- Mark deprecated tools
- Maintain backward compatibility for UE5-only workflows
- Clean up unused code

**Tasks**:
1. ✅ Update tool descriptions:
   - Mark UE5-only tools clearly
   - Mark UEFN-compatible tools
   - Add Verse-specific tools
2. ✅ Deprecation notices:
   - `compile_blueprint()` → Use for UE5 only, not UEFN
   - Direct Blueprint spawning → Use Verse devices instead
3. ✅ Code cleanup:
   - Remove unused imports
   - Optimize helper modules
   - Add type hints (Python)
4. ✅ Versioning:
   - Tag current version as `v1.0-ue5-legacy`
   - New version as `v2.0-uefn-hybrid`

**Deliverables**:
- Clean codebase with clear separation
- Version tags in git
- Migration guide (UE5-only → UEFN-hybrid)

---

## Technical Architecture

### Hybrid Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     AI Agent (Claude)                       │
│                                                             │
│  Tools:                                                     │
│  • UE5 world building (27 existing tools)                   │
│  • Verse code generation (4 new tools)                      │
│  • Asset export (3 new tools)                               │
│  • UEFN remote control (5 new tools) [optional]             │
│  • Fortnite API query (1 new tool)                          │
└─────────────────────────────────────────────────────────────┘
                     │
                     │ MCP Protocol (stdio)
                     ↓
┌─────────────────────────────────────────────────────────────┐
│              Python MCP Server                              │
│                                                             │
│  Modules:                                                   │
│  • unreal_mcp_server_advanced.py (existing)                 │
│  • verse_knowledge_base.py (new)                            │
│  • verse_generator.py (new)                                 │
│  • export_tools.py (new)                                    │
│  • uefn_remote_control.py (new, optional)                   │
│                                                             │
│  Data:                                                      │
│  • Verse API index (JSON/SQLite)                            │
│  • Verse code templates                                     │
│  • Asset export manifests                                   │
└─────────────────────────────────────────────────────────────┘
         │                           │
         │ TCP (UE5)                 │ HTTP (UEFN, optional)
         ↓                           ↓
┌──────────────────────┐    ┌──────────────────────┐
│  UE5 Editor (5.5+)   │    │  UEFN Editor         │
│                      │    │                      │
│  Plugin:             │    │  Plugins:            │
│  • UnrealMCP         │    │  • Remote Control?   │
│    (C++ EditorSys)   │    │                      │
│                      │    │  Content:            │
│  Used For:           │    │  • Imported assets   │
│  • Building worlds   │    │  • Verse scripts     │
│  • Creating assets   │    │                      │
│  • Physics setup     │    │  Used For:           │
│  • Exporting         │    │  • Gameplay logic    │
│                      │    │  • Island publishing │
└──────────────────────┘    └──────────────────────┘
         │                           │
         │ Export Pipeline           │
         └───────────────────────────┘
                (Manual or automated)
```

### Data Flow: UE5 → UEFN

```
1. Agent Request: "Create a medieval castle for Fortnite"
   ↓
2. Python MCP Server:
   • Uses existing UE5 tools: create_castle_fortress()
   • UE5 builds castle with 500+ actors
   ↓
3. Export Phase:
   • export_level_to_uefn() → Exports meshes, materials
   • generate_verse_spawn_map() → Analyzes castle structure
   • Creates Verse code:
     - Castle_Spawner device
     - 500 spawn calls with positions/rotations
   ↓
4. UEFN Import (Manual):
   • Import assets to UEFN Content Browser
   • Copy Verse code to project
   • Build in UEFN
   ↓
5. Fortnite Creative:
   • Island loads
   • Verse spawner runs
   • Castle appears in-game
```

---

## Tool Mapping: UE5 → UEFN

| UE5 MCP Tool | UEFN Equivalent | Migration Strategy |
|--------------|-----------------|-------------------|
| `get_actors_in_level()` | N/A | **Export**: Generate Verse manifest instead |
| `spawn_blueprint_actor()` | Verse `Spawner.Spawn()` | **Generate**: Create Verse spawn code |
| `create_blueprint()` | Verse device class | **Generate**: Create Verse class file |
| `set_physics_properties()` | Verse `simulation_physics` | **Map**: Convert to Verse properties |
| `apply_material_to_actor()` | UEFN material assignment | **Export**: Tag in manifest, apply in UEFN |
| `create_town()` | *Keep in UE5* | **Hybrid**: Build in UE5, export to UEFN |
| `construct_house()` | *Keep in UE5* | **Hybrid**: Build in UE5, export to UEFN |
| `create_castle_fortress()` | *Keep in UE5* | **Hybrid**: Build in UE5, export to UEFN |
| All building tools | *Keep in UE5* | **Hybrid**: Build in UE5, export to UEFN |

**Key Insight**: Most building logic stays in UE5. New Verse tools handle gameplay/logic in UEFN.

---

## New MCP Tools Summary

### Category: Verse Code Generation (4 tools)

1. **`generate_verse_device(module_name, device_type, config)`**
   - **Purpose**: Create Verse device classes
   - **Input**: Device type (button, spawner, timer), configuration
   - **Output**: Verse code string, file path
   - **Example**: `generate_verse_device("CastleGameplay", "round_timer", {duration: 300})`

2. **`insert_or_update_verse_file(project_path, file_path, code)`**
   - **Purpose**: Edit Verse files in UEFN project
   - **Input**: UEFN project path, Verse file path, code content
   - **Output**: Success/failure status
   - **Example**: `insert_or_update_verse_file("/path/to/uefn", "Devices/Spawner.verse", code)`

3. **`validate_verse_code(file_path)`**
   - **Purpose**: Validate Verse syntax and build
   - **Input**: Verse file path
   - **Output**: Validation errors, warnings
   - **Example**: `validate_verse_code("Devices/Spawner.verse")` → `{errors: [], warnings: []}`

4. **`query_fortnite_api(search_query)`**
   - **Purpose**: Search Fortnite.com API knowledge base
   - **Input**: Search query (natural language or keyword)
   - **Output**: Matching API entries, code examples
   - **Example**: `query_fortnite_api("how to give item to player")` → `item_granter_device`

### Category: Asset Export (3 tools)

5. **`export_level_to_uefn(level_name, export_path, options)`**
   - **Purpose**: Export UE5 level to UEFN-compatible format
   - **Input**: UE5 level name, destination path, export options
   - **Output**: Exported files, asset manifest JSON
   - **Example**: `export_level_to_uefn("CastleLevel", "/exports/castle", {include_physics: true})`

6. **`package_assets_for_fortnite(asset_list, metadata)`**
   - **Purpose**: Package and validate assets for UEFN
   - **Input**: List of asset paths, metadata (author, description)
   - **Output**: Package file, validation report
   - **Example**: `package_assets_for_fortnite(["Meshes/Tower", "Materials/Stone"], {...})`

7. **`generate_verse_spawn_map(level_name)`**
   - **Purpose**: Generate Verse code to recreate UE5 level layout
   - **Input**: UE5 level name
   - **Output**: Verse code with spawn calls, positions, rotations
   - **Example**: `generate_verse_spawn_map("CastleLevel")` → Outputs `CastleSpawner.verse`

### Category: UEFN Remote Control (5 tools) [CONDITIONAL]

8. **`rc_connect_uefn(host, port)`**
   - **Purpose**: Connect to UEFN Remote Control HTTP server
   - **Input**: Host, port (default: 127.0.0.1:7001)
   - **Output**: Connection status
   - **Example**: `rc_connect_uefn("127.0.0.1", 7001)`

9. **`rc_get_preset_list()`**
   - **Purpose**: List available Remote Control Presets
   - **Output**: Preset names, exposed properties/functions
   - **Example**: `rc_get_preset_list()` → `["MyPreset", "BuildPreset"]`

10. **`rc_set_property(preset, object_path, property, value)`**
    - **Purpose**: Set property value in UEFN
    - **Input**: Preset name, object path, property name, new value
    - **Output**: Success/failure
    - **Example**: `rc_set_property("MyPreset", "/Game/Castle/Tower", "Height", 1000)`

11. **`rc_call_function(preset, object_path, function, args)`**
    - **Purpose**: Call function in UEFN
    - **Input**: Preset name, object path, function name, arguments
    - **Output**: Function return value
    - **Example**: `rc_call_function("BuildPreset", "/Game/Builder", "Compile", {})`

12. **`rc_create_preset(name, objects)`**
    - **Purpose**: Create new Remote Control Preset
    - **Input**: Preset name, objects to expose
    - **Output**: Success/failure
    - **Example**: `rc_create_preset("NewPreset", ["/Game/Actor1", "/Game/Actor2"])`

### Category: Utility (1 tool)

13. **`generate_gameplay_logic(description, context)`**
    - **Purpose**: Generate Verse gameplay code from natural language
    - **Input**: Description, context (devices, players, objectives)
    - **Output**: Verse code implementing described logic
    - **Example**: `generate_gameplay_logic("Players collect coins, first to 100 wins", {...})`

---

## File Structure Changes

### New Directories

```
/home/user/unreal-engine-mcp/
├── VerseDigests/                       # NEW: Raw Verse API digests
│   ├── Fortnite.digest.verse
│   ├── Verse.digest.verse
│   ├── FortnitePlaysetDeviceGraffiti.digest.verse
│   └── UnrealEngine.digest.verse
├── VerseParsed/                        # NEW: Parsed API data
│   ├── fortnite_api.json               # Structured Fortnite API
│   ├── verse_stdlib.json               # Verse standard library
│   ├── api_index.sqlite                # Searchable database
│   └── markdown/                       # Human-readable docs
│       ├── devices.md
│       ├── gameplay.md
│       └── utilities.md
├── VerseTemplates/                     # NEW: Code templates
│   ├── devices/
│   │   ├── button_device.verse.template
│   │   ├── spawner_device.verse.template
│   │   ├── timer_device.verse.template
│   │   ├── item_granter.verse.template
│   │   └── team_manager.verse.template
│   ├── gameplay/
│   │   ├── scoring_system.verse.template
│   │   ├── round_controller.verse.template
│   │   └── elimination_tracker.verse.template
│   └── utils/
│       ├── player_helpers.verse.template
│       └── math_utils.verse.template
├── Python/
│   ├── unreal_mcp_server_advanced.py   # EXISTING: Main server
│   ├── verse_parser.py                 # NEW: Digest parser
│   ├── verse_generator.py              # NEW: Code generator
│   ├── verse_knowledge_base.py         # NEW: API query system
│   ├── export_tools.py                 # NEW: Asset export helpers
│   ├── uefn_remote_control.py          # NEW: Remote Control client
│   └── helpers/                        # EXISTING: Building helpers
│       └── ... (all existing files)
├── Exports/                            # NEW: Exported assets
│   ├── manifests/                      # Asset manifests (JSON)
│   ├── meshes/                         # Exported FBX/DataAssets
│   ├── materials/                      # Material exports
│   └── verse/                          # Generated Verse spawn code
├── Tests/                              # NEW: Test suite
│   ├── test_verse_parser.py
│   ├── test_verse_generator.py
│   ├── test_export_pipeline.py
│   └── sample_projects/
│       ├── castle_export_test/
│       └── town_export_test/
└── Docs/                               # NEW: UEFN documentation
    ├── UEFN_WORKFLOW.md                # Step-by-step workflow guide
    ├── VERSE_PATTERNS.md               # Common Verse patterns
    ├── ASSET_EXPORT_GUIDE.md           # Asset export documentation
    └── REMOTE_CONTROL_SETUP.md         # Remote Control setup (if available)
```

---

## Risk Assessment & Mitigation

### High-Risk Items

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Remote Control API not available in UEFN** | Medium | High (70%) | Skip Approach C, rely on manual workflows + Verse generation |
| **Digest files inaccessible** | High | Low (20%) | Fallback to web scraping + manual API documentation |
| **Verse syntax too complex to parse** | Medium | Medium (40%) | Use regex + heuristics, accept 80% accuracy, manual refinement |
| **Asset export incompatibility** | High | Medium (30%) | Test early with sample assets, iterate on export formats |
| **UEFN performance issues with large structures** | Medium | Medium (50%) | Optimize Verse spawn code, use batching, limit actor counts |
| **Epic changes Verse API frequently** | Medium | Medium (40%) | Version-lock digest files, update parser as needed |

### Medium-Risk Items

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **UE5 → UEFN workflow too manual** | Low | High (60%) | Document workflow clearly, create automation scripts where possible |
| **Agent generates invalid Verse** | Medium | Medium (40%) | Implement validation pipeline, iterate on templates |
| **Asset size limits in UEFN** | Low | Low (20%) | Validate asset sizes during export, provide warnings |

---

## Success Criteria

### Phase 2 (Verse Knowledge Base) Success:
- ✅ Parse all digest files with 90%+ accuracy
- ✅ Build queryable API index with <100ms query time
- ✅ Create 25+ Verse templates covering common use cases
- ✅ Agent can find correct API for 80%+ of natural language queries

### Phase 3 (Verse Generation) Success:
- ✅ Generate valid Verse code for 10+ device types
- ✅ Validation pipeline catches 95%+ of syntax errors
- ✅ Generated code compiles in UEFN without modification for 70%+ of cases

### Phase 4 (Asset Export) Success:
- ✅ Export complete UE5 level to UEFN-compatible format
- ✅ Generated Verse spawn code recreates 90%+ of original layout
- ✅ Exported assets load in UEFN without errors
- ✅ End-to-end workflow (UE5 → export → UEFN → Fortnite) works for sample project

### Phase 6 (Integration) Success:
- ✅ Complete castle or town built in UE5, exported, and visible in Fortnite Creative
- ✅ Agent generates working Verse gameplay logic from natural language
- ✅ All new MCP tools documented and tested
- ✅ Performance acceptable (export <5min, Verse generation <10s)

---

## Open Questions & Decisions Needed

1. **Digest File Acquisition**:
   - Q: Where exactly are digest files located in UEFN installation?
   - Decision: Need to locate and copy these first (Phase 1)

2. **Remote Control API**:
   - Q: Is Remote Control API available in UEFN?
   - Decision: Check UEFN plugins list (Phase 1)
   - Impact: Determines if Approach C is viable

3. **Asset Export Format**:
   - Q: What format does UEFN prefer? FBX? DataAssets? Custom?
   - Decision: Research Epic's UEFN asset migration docs (Phase 1)
   - Impact: Affects export pipeline implementation

4. **Verse Validation**:
   - Q: Can we trigger UEFN build from CLI or API?
   - Decision: Test UEFN CLI options (Phase 3)
   - Impact: Determines validation approach (automated vs manual)

5. **Performance Targets**:
   - Q: What's acceptable for large structure export/spawn?
   - Decision: Set based on Phase 4 testing
   - Impact: May need to optimize or limit actor counts

6. **Backward Compatibility**:
   - Q: Do we maintain full UE5-only workflow or deprecate it?
   - Decision: Keep both (Phase 7) - mark tools clearly
   - Impact: Code maintenance burden

---

## Recommended Next Steps (Immediate Actions)

### Step 1: Environment Setup (This Week)
```bash
# Install UEFN
# Download from Epic Games Launcher → UEFN

# Locate digest files
find /path/to/UEFN -name "*.digest.verse"

# Copy to project
cp /path/to/digests/* /home/user/unreal-engine-mcp/VerseDigests/

# Check for Remote Control API
# Open UEFN → Edit → Plugins → Search "Remote Control"
```

### Step 2: Digest File Analysis (This Week)
```python
# Quick script to analyze digest structure
import re
from pathlib import Path

digest_files = list(Path("VerseDigests").glob("*.digest.verse"))
for f in digest_files:
    content = f.read_text()
    classes = re.findall(r'class\s+(\w+)', content)
    functions = re.findall(r'(\w+)\s*:=\s*\(', content)
    print(f"{f.name}: {len(classes)} classes, {len(functions)} functions")
```

### Step 3: Proof of Concept (Next Week)
1. Create simple Verse device manually in UEFN
2. Test asset import from UE5 to UEFN
3. Verify build process and error reporting
4. Document any issues or limitations

### Step 4: Create Migration Branch (After POC)
```bash
# This plan should be on a new branch
git checkout -b claude/uefn-migration-implementation

# Start implementing Phase 2 (Verse parser)
# Commit progress regularly
```

---

## Conclusion

This migration plan provides a **hybrid approach** that:
1. **Preserves** the existing UE5 MCP's powerful world-building capabilities
2. **Adds** Verse code generation for UEFN gameplay logic
3. **Bridges** the two environments via asset export pipeline
4. **Optionally** automates UEFN if Remote Control API is available

**Total Estimated Effort**: 10-11 weeks for full implementation
**Lines of Code**: ~5,000-7,000 new Python lines (Verse parser, generator, export tools)
**Preservation**: 100% of existing building helpers retained

**Key Innovation**: Rather than abandoning the UE5 MCP, we **augment** it to become a UEFN asset factory while adding Verse intelligence for gameplay. This gives us the best of both worlds: UE5's full editor power for content creation + UEFN's Fortnite integration for gameplay.

---

## Appendix A: Verse Language Primer

### Core Syntax Elements

```verse
# Module declaration
using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }

# Class definition
my_device := class(creative_device):
    # Attributes
    @editable
    MyButton : button_device = button_device{}

    # Functions
    OnBegin<override>()<suspends>:void=
        MyButton.InteractedWithEvent.Subscribe(OnButtonPressed)

    OnButtonPressed(Agent:agent):void=
        Print("Button pressed by {Agent}")
```

### Key Concepts
- **Failure Context**: `<decides>`, `<suspends>`, `failable`
- **Concurrency**: `spawn{}`, `race{}`, `sync{}`
- **Types**: `int`, `float`, `logic`, `string`, `option[T]`, `[]T` (array), `[K]V` (map)
- **Devices**: Extend `creative_device`, use `@editable` for properties
- **Events**: Subscribe pattern for player interactions

---

## Appendix B: Resource Links

### Epic Official Documentation
- **Verse Language Reference**: https://dev.epicgames.com/documentation/en-us/uefn/verse-language-reference
- **Verse API Reference**: https://dev.epicgames.com/documentation/en-us/uefn/verse-api-reference
- **UEFN Quick Start**: https://dev.epicgames.com/documentation/en-us/uefn/quick-start-guide
- **Asset Migration**: https://dev.epicgames.com/documentation/en-us/uefn/importing-assets-from-unreal-engine

### Community Resources
- **Verse Discord**: https://discord.gg/uefn (unofficial)
- **UEFN Reddit**: r/FortniteCreative
- **Verse Examples**: https://github.com/topics/uefn-verse (community repos)

### Unreal Engine (for comparison)
- **Remote Control API**: https://docs.unrealengine.com/5.3/en-US/remote-control-api-in-unreal-engine/
- **Editor Utility Widgets**: https://docs.unrealengine.com/5.3/en-US/editor-utility-widgets/

---

*End of Migration Plan*
