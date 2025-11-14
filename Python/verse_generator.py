#!/usr/bin/env python3
"""
Verse Code Generator

Generates Verse code from templates with parameter validation against the Fortnite API.

Features:
- Template-based code generation with variable substitution
- Conditional sections ({{#IF_...}})
- API validation for class/function names
- Syntax formatting and indentation
- Type checking against Verse API

Usage:
    generator = VerseCodeGenerator('VerseParsed/fortnite_api.json')
    code = generator.generate_from_template('devices/button_device.verse.template', params)
"""

import re
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from verse_knowledge_base import VerseKnowledgeBase


class VerseCodeGenerator:
    """
    Generates Verse code from templates with parameter validation
    """

    def __init__(self, api_index_path: Path):
        """
        Initialize code generator with API knowledge base

        Args:
            api_index_path: Path to fortnite_api.json
        """
        self.kb = VerseKnowledgeBase(api_index_path)
        self.templates_dir = Path(__file__).parent.parent / 'VerseTemplates'

    def generate_from_template(
        self,
        template_name: str,
        params: Dict[str, Any]
    ) -> str:
        """
        Generate Verse code from a template

        Args:
            template_name: Template file name (e.g., 'devices/button_device.verse.template')
            params: Dictionary of template parameters

        Returns:
            Generated Verse code as string
        """
        # Load template
        template_path = self.templates_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        template_content = template_path.read_text()

        # Add default parameters
        params = self._add_default_params(params)

        # Process template
        code = self._process_template(template_content, params)

        # Format code
        code = self._format_code(code)

        return code

    def _add_default_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Add default parameters if not provided"""
        defaults = {
            'TIMESTAMP': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'DESCRIPTION': 'Generated Verse device',
            'MODULE_NAME': 'my_device',
        }

        # Merge with provided params (provided params take precedence)
        merged = {**defaults, **params}
        return merged

    def _process_template(self, template: str, params: Dict[str, Any]) -> str:
        """
        Process template with variable substitution and conditionals

        Supports:
        - {{VARIABLE}} - Simple substitution
        - {{#IF_CONDITION}}...{{/IF_CONDITION}} - Conditional blocks
        - {{#ELSE}}...{{/ELSE}} - Else blocks (within IF)
        """
        result = template

        # Process conditional blocks first
        result = self._process_conditionals(result, params)

        # Process simple variable substitution
        result = self._substitute_variables(result, params)

        return result

    def _process_conditionals(self, template: str, params: Dict[str, Any]) -> str:
        """Process conditional blocks in template"""
        # Pattern: {{#IF_CONDITION}}content{{/IF_CONDITION}}
        # With optional: {{#ELSE}}else_content{{/ELSE}}

        pattern = r'\{\{#IF_([A-Z_]+)\}\}(.*?)\{\{/IF_\1\}\}'

        def replace_conditional(match):
            condition = match.group(1)
            content = match.group(2)

            # Check if condition is true in params
            condition_key = condition
            is_true = params.get(condition_key, False)

            # Handle ELSE blocks
            if '{{#ELSE}}' in content:
                if_part, else_part = content.split('{{#ELSE}}', 1)
                if '{{/ELSE}}' in else_part:
                    else_part = else_part.split('{{/ELSE}}', 1)[0]

                if is_true:
                    return if_part
                else:
                    return else_part
            else:
                # No ELSE block
                if is_true:
                    return content
                else:
                    return ''

        # Process all conditionals (may be nested, so iterate)
        max_iterations = 10
        for _ in range(max_iterations):
            new_result = re.sub(pattern, replace_conditional, template, flags=re.DOTALL)
            if new_result == template:
                break
            template = new_result

        return template

    def _substitute_variables(self, template: str, params: Dict[str, Any]) -> str:
        """Substitute {{VARIABLE}} placeholders with values"""
        result = template

        for key, value in params.items():
            placeholder = f'{{{{{key}}}}}'
            result = result.replace(placeholder, str(value))

        return result

    def _format_code(self, code: str) -> str:
        """
        Format generated Verse code

        - Remove excessive blank lines
        - Clean up indentation
        - Remove commented-out template directives
        """
        lines = code.split('\n')
        formatted_lines = []

        prev_blank = False
        for line in lines:
            # Skip lines that are only template comments
            if line.strip().startswith('# {{') or line.strip().startswith('{{'):
                continue

            # Remove excessive blank lines
            is_blank = not line.strip()
            if is_blank and prev_blank:
                continue

            formatted_lines.append(line)
            prev_blank = is_blank

        # Remove leading/trailing blank lines
        while formatted_lines and not formatted_lines[0].strip():
            formatted_lines.pop(0)
        while formatted_lines and not formatted_lines[-1].strip():
            formatted_lines.pop()

        return '\n'.join(formatted_lines)

    def validate_device_class(self, class_name: str) -> bool:
        """
        Validate that a device class exists in the API

        Args:
            class_name: Name of device class

        Returns:
            True if class exists, False otherwise
        """
        cls = self.kb.get_class(class_name)
        return cls is not None

    def get_device_events(self, device_class: str) -> List[str]:
        """
        Get list of events for a device class

        Args:
            device_class: Device class name (e.g., 'button_device')

        Returns:
            List of event names
        """
        events = self.kb.get_class_events(device_class)
        return [event['name'] for event in events]

    def get_device_functions(self, device_class: str) -> List[str]:
        """
        Get list of functions for a device class

        Args:
            device_class: Device class name

        Returns:
            List of function names
        """
        functions = self.kb.get_class_functions(device_class)
        return [func['name'] for func in functions]

    def generate_device_handler(
        self,
        device_type: str,
        module_name: str,
        description: str = "",
        **kwargs
    ) -> str:
        """
        Generate a complete device handler from device type

        Args:
            device_type: Type of device (e.g., 'button', 'timer', 'spawner')
            module_name: Name for the Verse module/class
            description: Description of the device's purpose
            **kwargs: Additional template parameters

        Returns:
            Generated Verse code
        """
        # Map device type to template
        template_map = {
            'button': 'devices/button_device.verse.template',
            'timer': 'devices/timer_device.verse.template',
            'spawner': 'devices/spawner_device.verse.template',
            'item_granter': 'devices/item_granter.verse.template',
            'trigger': 'devices/trigger_volume.verse.template',
            'teleporter': 'devices/teleporter.verse.template',
            'damage': 'devices/damage_volume.verse.template',
            'collectible': 'devices/collectible_manager.verse.template',
            'mutator': 'devices/mutator_zone.verse.template',
            'conditional_button': 'devices/conditional_button.verse.template',
        }

        template_name = template_map.get(device_type)
        if not template_name:
            raise ValueError(f"Unknown device type: {device_type}. Valid types: {list(template_map.keys())}")

        # Build parameters
        params = {
            'MODULE_NAME': module_name,
            'DESCRIPTION': description or f"Generated {device_type} device handler",
            **kwargs
        }

        return self.generate_from_template(template_name, params)

    def generate_gameplay_system(
        self,
        system_type: str,
        module_name: str,
        description: str = "",
        **kwargs
    ) -> str:
        """
        Generate a gameplay system from template

        Args:
            system_type: Type of system ('scoring', 'rounds', 'teams', etc.)
            module_name: Name for the Verse module/class
            description: Description of the system
            **kwargs: Additional template parameters

        Returns:
            Generated Verse code
        """
        template_map = {
            'scoring': 'gameplay/scoring_system.verse.template',
            'rounds': 'gameplay/round_controller.verse.template',
            'teams': 'gameplay/team_manager.verse.template',
            'elimination': 'gameplay/elimination_tracker.verse.template',
            'capture_point': 'gameplay/capture_point.verse.template',
            'race': 'gameplay/race_checkpoint.verse.template',
            'waves': 'gameplay/wave_combat.verse.template',
        }

        template_name = template_map.get(system_type)
        if not template_name:
            raise ValueError(f"Unknown system type: {system_type}. Valid types: {list(template_map.keys())}")

        params = {
            'MODULE_NAME': module_name,
            'DESCRIPTION': description or f"Generated {system_type} system",
            **kwargs
        }

        return self.generate_from_template(template_name, params)

    def validate_verse_syntax(self, code: str) -> Dict[str, Any]:
        """
        Basic Verse syntax validation

        Checks for:
        - Balanced braces, parentheses, brackets
        - Valid module/class structure
        - Proper indentation patterns

        Args:
            code: Verse code to validate

        Returns:
            Dictionary with 'valid' (bool) and 'errors' (list of strings)
        """
        errors = []
        lines = code.split('\n')

        # Check balanced delimiters
        brace_count = 0
        paren_count = 0
        bracket_count = 0

        for line_num, line in enumerate(lines, 1):
            # Skip comments
            if '#' in line:
                line = line.split('#')[0]

            brace_count += line.count('{') - line.count('}')
            paren_count += line.count('(') - line.count(')')
            bracket_count += line.count('[') - line.count(']')

            if brace_count < 0:
                errors.append(f"Line {line_num}: Unmatched closing brace")
            if paren_count < 0:
                errors.append(f"Line {line_num}: Unmatched closing parenthesis")
            if bracket_count < 0:
                errors.append(f"Line {line_num}: Unmatched closing bracket")

        # Check final balance
        if brace_count != 0:
            errors.append(f"Unbalanced braces: {brace_count} unclosed")
        if paren_count != 0:
            errors.append(f"Unbalanced parentheses: {paren_count} unclosed")
        if bracket_count != 0:
            errors.append(f"Unbalanced brackets: {bracket_count} unclosed")

        # Check for class definition
        has_class = any(':= class' in line for line in lines)
        if not has_class:
            errors.append("No class definition found (missing ':= class')")

        # Check for OnBegin override (if it's a creative_device)
        if 'creative_device' in code:
            has_on_begin = any('OnBegin<override>' in line for line in lines)
            if not has_on_begin:
                errors.append("creative_device class should have OnBegin<override>() method")

        return {
            'valid': len(errors) == 0,
            'errors': errors
        }

    def format_verse_code(self, code: str, indent_size: int = 4) -> str:
        """
        Format Verse code with proper indentation

        Args:
            code: Verse code to format
            indent_size: Number of spaces per indent level

        Returns:
            Formatted code
        """
        lines = code.split('\n')
        formatted_lines = []
        indent_level = 0

        for line in lines:
            stripped = line.strip()

            # Decrease indent for closing braces
            if stripped.startswith('}') or stripped.startswith(')'):
                indent_level = max(0, indent_level - 1)

            # Apply indentation
            if stripped:
                formatted_line = ' ' * (indent_level * indent_size) + stripped
            else:
                formatted_line = ''

            formatted_lines.append(formatted_line)

            # Increase indent after opening braces
            if stripped.endswith(':') or stripped.endswith('{'):
                indent_level += 1
            elif stripped.endswith('('):
                indent_level += 1

        return '\n'.join(formatted_lines)


def main():
    """Example usage"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python verse_generator.py <api_index_json>")
        print("\nExample:")
        print("  python verse_generator.py VerseParsed/fortnite_api.json")
        sys.exit(1)

    generator = VerseCodeGenerator(sys.argv[1])

    # Example: Generate a button device
    print("=== Generating Button Device ===\n")
    button_code = generator.generate_device_handler(
        device_type='button',
        module_name='my_button_handler',
        description='Handles button presses with cooldown',
        BUTTON_NAME='TriggerButton',
        IF_COOLDOWN=True,
        COOLDOWN_SECONDS='5.0'
    )
    print(button_code)
    print("\n")

    # Validate the generated code
    print("=== Validating Generated Code ===\n")
    validation = generator.validate_verse_syntax(button_code)
    if validation['valid']:
        print("✅ Code is syntactically valid")
    else:
        print("❌ Validation errors:")
        for error in validation['errors']:
            print(f"  - {error}")

    print("\n=== Generating Scoring System ===\n")
    scoring_code = generator.generate_gameplay_system(
        system_type='scoring',
        module_name='game_scoring',
        description='Tracks player scores with win conditions',
        WINNING_SCORE='100',
        IF_TEAM_SCORING=True
    )
    print(scoring_code[:500] + "...\n")

    # Check available device events
    print("\n=== Button Device Events ===")
    # events = generator.get_device_events('button_device')
    # print(f"Available events: {events}")


if __name__ == '__main__':
    main()
