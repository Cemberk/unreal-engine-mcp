"""
Verse MCP Tools

MCP tools for Verse code generation, API querying, and UEFN integration.

Tools:
- generate_verse_device: Generate Verse device code from templates
- query_fortnite_api: Search Fortnite/Verse API
- validate_verse_code: Validate Verse syntax
- insert_or_update_verse_file: Write Verse code to UEFN project

Usage:
    These tools are imported into the main MCP server.
"""

import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from verse_generator import VerseCodeGenerator
from verse_knowledge_base import VerseKnowledgeBase

logger = logging.getLogger("VerseMCP")

# Initialize generator and knowledge base
try:
    PROJECT_ROOT = Path(__file__).parent.parent
    API_INDEX_PATH = PROJECT_ROOT / 'VerseParsed' / 'fortnite_api.json'

    generator = VerseCodeGenerator(API_INDEX_PATH)
    kb = VerseKnowledgeBase(API_INDEX_PATH)

    logger.info("Verse tools initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Verse tools: {e}")
    generator = None
    kb = None


def generate_verse_device(
    device_type: str,
    module_name: str,
    description: str = "",
    **kwargs
) -> str:
    """
    Generate Verse device code from template.

    Args:
        device_type: Type of device to generate. Options:
            - 'button': Interactive button handler
            - 'timer': Timer/countdown device
            - 'spawner': Item/prop spawner
            - 'item_granter': Item granting device
            - 'trigger': Trigger volume
            - 'teleporter': Teleporter device
            - 'damage': Damage volume
            - 'collectible': Collectible manager
            - 'mutator': Mutator zone
            - 'conditional_button': Conditional button
        module_name: Name for the generated Verse module/class
        description: Description of what the device does
        **kwargs: Additional template parameters (varies by device_type)

    Returns:
        Generated Verse code as string

    Examples:
        # Generate a button with cooldown
        code = generate_verse_device(
            device_type='button',
            module_name='my_button_handler',
            description='Handles button presses',
            BUTTON_NAME='TriggerButton',
            IF_COOLDOWN=True,
            COOLDOWN_SECONDS='5.0'
        )

        # Generate a timer
        code = generate_verse_device(
            device_type='timer',
            module_name='countdown_timer',
            description='10 second countdown',
            TIMER_NAME='GameTimer',
            DURATION_SECONDS='10.0',
            IS_REPEATING='false',
            IF_AUTO_START=True
        )

        # Generate a spawner
        code = generate_verse_device(
            device_type='spawner',
            module_name='item_spawner',
            description='Spawns collectibles',
            SPAWNER_NAME='CoinSpawner',
            SPAWN_DELAY_SECONDS='2.0',
            MAX_SPAWNS='10',
            IF_AUTO_SPAWN=True,
            IF_CONTINUOUS=True
        )
    """
    if not generator:
        return "Error: Verse generator not initialized. Check API index path."

    try:
        code = generator.generate_device_handler(
            device_type=device_type,
            module_name=module_name,
            description=description,
            **kwargs
        )

        logger.info(f"Generated {device_type} device: {module_name}")
        return code

    except Exception as e:
        logger.error(f"Failed to generate device: {e}")
        return f"Error generating device: {str(e)}"


def generate_gameplay_system(
    system_type: str,
    module_name: str,
    description: str = "",
    **kwargs
) -> str:
    """
    Generate Verse gameplay system code from template.

    Args:
        system_type: Type of gameplay system. Options:
            - 'scoring': Score tracking with win conditions
            - 'rounds': Round-based game controller
            - 'teams': Team management and scoring
            - 'elimination': Kill/death tracking
            - 'capture_point': Capture point/KOTH system
            - 'race': Race checkpoint system
            - 'waves': Wave-based combat
        module_name: Name for the generated Verse module/class
        description: Description of the system
        **kwargs: Additional template parameters

    Returns:
        Generated Verse code as string

    Examples:
        # Generate scoring system
        code = generate_gameplay_system(
            system_type='scoring',
            module_name='game_scoring',
            description='Track player scores',
            WINNING_SCORE='100',
            IF_TEAM_SCORING=True
        )

        # Generate round controller
        code = generate_gameplay_system(
            system_type='rounds',
            module_name='round_manager',
            description='Manage game rounds',
            ROUND_DURATION_SECONDS='300',
            INTERMISSION_SECONDS='10',
            MAX_ROUNDS='3',
            START_DELAY_SECONDS='5'
        )
    """
    if not generator:
        return "Error: Verse generator not initialized."

    try:
        code = generator.generate_gameplay_system(
            system_type=system_type,
            module_name=module_name,
            description=description,
            **kwargs
        )

        logger.info(f"Generated {system_type} system: {module_name}")
        return code

    except Exception as e:
        logger.error(f"Failed to generate gameplay system: {e}")
        return f"Error generating system: {str(e)}"


def query_fortnite_api(
    search_query: str,
    search_type: str = "all",
    limit: int = 10
) -> str:
    """
    Search the Fortnite/Verse API for classes, functions, or keywords.

    Args:
        search_query: Search term (class name, keyword, function name, etc.)
        search_type: Type of search. Options:
            - 'all': Search all entity types
            - 'classes': Search only classes
            - 'functions': Search only functions
            - 'devices': Search only device classes
        limit: Maximum number of results to return (default: 10)

    Returns:
        Formatted search results as string

    Examples:
        # Search for button devices
        results = query_fortnite_api('button', search_type='classes')

        # Search for spawn-related functions
        results = query_fortnite_api('spawn', search_type='functions')

        # Find all devices
        results = query_fortnite_api('device', search_type='devices')

        # General keyword search
        results = query_fortnite_api('player score', search_type='all')
    """
    if not kb:
        return "Error: Verse knowledge base not initialized."

    try:
        results_text = []
        results_text.append(f"=== Search Results for '{search_query}' ===\n")

        if search_type == 'classes' or search_type == 'all':
            class_results = kb.search_classes(search_query, limit=limit)
            if class_results:
                results_text.append(f"\n📦 Classes ({len(class_results)}):\n")
                for i, result in enumerate(class_results, 1):
                    results_text.append(f"{i}. {result.name}")
                    if result.description:
                        desc = result.description[:100] + "..." if len(result.description) > 100 else result.description
                        results_text.append(f"   {desc}")
                    results_text.append(f"   Relevance: {result.relevance_score:.1f}\n")

        if search_type == 'functions' or search_type == 'all':
            func_results = kb.search_functions(search_query, limit=limit)
            if func_results:
                results_text.append(f"\n🔧 Functions ({len(func_results)}):\n")
                for i, result in enumerate(func_results, 1):
                    results_text.append(f"{i}. {result.name}")
                    if result.description:
                        results_text.append(f"   {result.description}")
                    results_text.append(f"   Relevance: {result.relevance_score:.1f}\n")

        if search_type == 'devices':
            devices = kb.get_devices()
            matching_devices = [d for d in devices if search_query.lower() in d['name'].lower()]
            if matching_devices:
                results_text.append(f"\n🎮 Devices ({len(matching_devices)}):\n")
                for i, device in enumerate(matching_devices[:limit], 1):
                    results_text.append(f"{i}. {device['name']}")
                    if device.get('documentation'):
                        doc = device['documentation'][:100] + "..." if len(device['documentation']) > 100 else device['documentation']
                        results_text.append(f"   {doc}")
                    results_text.append(f"   Functions: {len(device.get('functions', []))}, Events: {len(device.get('events', []))}\n")

        if search_type == 'all':
            stats = kb.get_statistics()
            results_text.append(f"\n📊 API Statistics:")
            results_text.append(f"   Total Classes: {stats['total_classes']}")
            results_text.append(f"   Total Functions: {stats['total_functions']}")
            results_text.append(f"   Total Devices: {stats['total_devices']}")
            results_text.append(f"   Build Version: {stats['build_version']}")

        result_str = '\n'.join(results_text)
        logger.info(f"API query: '{search_query}' (type: {search_type}) - {len(results_text)} results")
        return result_str

    except Exception as e:
        logger.error(f"API query failed: {e}")
        return f"Error querying API: {str(e)}"


def get_class_details(class_name: str) -> str:
    """
    Get detailed information about a specific Verse/Fortnite class.

    Args:
        class_name: Name of the class (exact or partial match)

    Returns:
        Formatted class details including functions, properties, and events

    Examples:
        details = get_class_details('button_device')
        details = get_class_details('timer_device')
    """
    if not kb:
        return "Error: Verse knowledge base not initialized."

    try:
        cls = kb.get_class(class_name)
        if not cls:
            return f"Class '{class_name}' not found. Try query_fortnite_api() to search."

        lines = []
        lines.append(f"=== {cls['name']} ===\n")

        if cls.get('documentation'):
            lines.append(f"📝 Description:")
            lines.append(f"{cls['documentation']}\n")

        if cls.get('base_classes'):
            lines.append(f"🔗 Inherits From: {', '.join(cls['base_classes'])}\n")

        if cls.get('modifiers'):
            lines.append(f"🏷️  Modifiers: {', '.join(cls['modifiers'])}\n")

        # Events
        events = cls.get('events', [])
        if events:
            lines.append(f"\n⚡ Events ({len(events)}):")
            for event in events:
                lines.append(f"  • {event['name']}: listenable({event['payload_type']})")

        # Functions
        functions = cls.get('functions', [])
        if functions:
            lines.append(f"\n🔧 Functions ({len(functions)}):")
            for func in functions[:10]:  # Limit to first 10
                sig = kb.generate_function_signature(func)
                lines.append(f"  • {sig}")
            if len(functions) > 10:
                lines.append(f"  ... and {len(functions) - 10} more")

        # Properties
        properties = cls.get('properties', [])
        if properties:
            lines.append(f"\n📦 Properties ({len(properties)}):")
            for prop in properties[:10]:  # Limit to first 10
                var_prefix = "var " if prop.get('is_var') else ""
                editable = "@editable " if prop.get('is_editable') else ""
                lines.append(f"  • {editable}{var_prefix}{prop['name']}: {prop['type']}")
            if len(properties) > 10:
                lines.append(f"  ... and {len(properties) - 10} more")

        return '\n'.join(lines)

    except Exception as e:
        logger.error(f"Get class details failed: {e}")
        return f"Error getting class details: {str(e)}"


def validate_verse_code(code: str) -> str:
    """
    Validate Verse code syntax.

    Performs basic syntax validation:
    - Balanced braces, parentheses, brackets
    - Valid class structure
    - Proper method declarations

    Args:
        code: Verse code to validate

    Returns:
        Validation results as formatted string

    Examples:
        result = validate_verse_code(generated_code)
    """
    if not generator:
        return "Error: Verse generator not initialized."

    try:
        validation = generator.validate_verse_syntax(code)

        lines = []
        lines.append("=== Verse Code Validation ===\n")

        if validation['valid']:
            lines.append("✅ Code is syntactically valid")
        else:
            lines.append("❌ Validation Failed\n")
            lines.append(f"Errors ({len(validation['errors'])}):")
            for error in validation['errors']:
                lines.append(f"  • {error}")

        # Additional stats
        num_lines = code.count('\n') + 1
        has_class = ':= class' in code
        has_device = 'creative_device' in code

        lines.append(f"\n📊 Code Statistics:")
        lines.append(f"  Lines: {num_lines}")
        lines.append(f"  Has class definition: {'✅' if has_class else '❌'}")
        lines.append(f"  Is creative_device: {'✅' if has_device else '❌'}")

        return '\n'.join(lines)

    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return f"Error validating code: {str(e)}"


def insert_or_update_verse_file(
    project_path: str,
    file_path: str,
    code: str,
    create_if_missing: bool = True
) -> str:
    """
    Write or update a Verse file in a UEFN project.

    Args:
        project_path: Path to UEFN project root directory
        file_path: Relative path to Verse file (e.g., 'Devices/MyDevice.verse')
        code: Verse code content to write
        create_if_missing: Create file if it doesn't exist (default: True)

    Returns:
        Status message

    Examples:
        result = insert_or_update_verse_file(
            project_path='/path/to/uefn/project',
            file_path='Devices/ButtonHandler.verse',
            code=generated_code
        )
    """
    try:
        project_root = Path(project_path)
        if not project_root.exists():
            return f"Error: Project path does not exist: {project_path}"

        # Full path to verse file
        verse_file = project_root / file_path

        # Check if file exists
        if verse_file.exists() and not create_if_missing:
            return f"Error: File already exists: {verse_file}"

        # Create parent directories if needed
        verse_file.parent.mkdir(parents=True, exist_ok=True)

        # Write code to file
        verse_file.write_text(code, encoding='utf-8')

        logger.info(f"Wrote Verse file: {verse_file}")

        return f"✅ Successfully wrote Verse file:\n  Path: {verse_file}\n  Size: {len(code)} characters\n  Lines: {code.count(chr(10)) + 1}"

    except Exception as e:
        logger.error(f"Failed to write Verse file: {e}")
        return f"Error writing file: {str(e)}"


def list_available_templates() -> str:
    """
    List all available Verse templates.

    Returns:
        Formatted list of templates by category
    """
    try:
        templates_dir = Path(__file__).parent.parent / 'VerseTemplates'

        lines = []
        lines.append("=== Available Verse Templates ===\n")

        # Device templates
        device_dir = templates_dir / 'devices'
        if device_dir.exists():
            devices = sorted([f.stem.replace('.verse', '') for f in device_dir.glob('*.verse.template')])
            lines.append(f"🎮 Device Templates ({len(devices)}):")
            for device in devices:
                lines.append(f"  • {device}")
            lines.append("")

        # Gameplay templates
        gameplay_dir = templates_dir / 'gameplay'
        if gameplay_dir.exists():
            systems = sorted([f.stem.replace('.verse', '') for f in gameplay_dir.glob('*.verse.template')])
            lines.append(f"🎯 Gameplay Templates ({len(systems)}):")
            for system in systems:
                lines.append(f"  • {system}")
            lines.append("")

        # Utility templates
        utils_dir = templates_dir / 'utils'
        if utils_dir.exists():
            utils = sorted([f.stem.replace('.verse', '') for f in utils_dir.glob('*.verse.template')])
            lines.append(f"🔧 Utility Templates ({len(utils)}):")
            for util in utils:
                lines.append(f"  • {util}")

        return '\n'.join(lines)

    except Exception as e:
        return f"Error listing templates: {str(e)}"
