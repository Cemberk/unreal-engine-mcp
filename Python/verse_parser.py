#!/usr/bin/env python3
"""
Verse Digest File Parser

Parses UEFN Verse digest files (.digest.verse) and extracts:
- Modules
- Classes (with inheritance)
- Enums
- Functions/Methods (with signatures)
- Properties
- Events
- Attributes

Output: Structured JSON/Python dictionaries for API indexing
"""

import re
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum as PyEnum


class EntityType(PyEnum):
    """Types of entities found in Verse digests"""
    MODULE = "module"
    CLASS = "class"
    ENUM = "enum"
    FUNCTION = "function"
    PROPERTY = "property"
    EVENT = "event"
    ENUM_VALUE = "enum_value"


@dataclass
class Modifier:
    """Represents a Verse modifier like <public>, <native>, etc."""
    name: str

    def __repr__(self):
        return f"<{self.name}>"


@dataclass
class Parameter:
    """Function/method parameter"""
    name: str
    type: str

    def __repr__(self):
        return f"{self.name}:{self.type}"


@dataclass
class FunctionSignature:
    """Complete function signature"""
    name: str
    modifiers: List[Modifier] = field(default_factory=list)
    parameters: List[Parameter] = field(default_factory=list)
    return_type: Optional[str] = None
    effect_modifiers: List[str] = field(default_factory=list)  # transacts, suspends, decides, reads
    is_external: bool = False
    is_override: bool = False
    is_native: bool = False
    is_native_callable: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'modifiers': [m.name for m in self.modifiers],
            'parameters': [{'name': p.name, 'type': p.type} for p in self.parameters],
            'return_type': self.return_type,
            'effect_modifiers': self.effect_modifiers,
            'is_external': self.is_external,
            'is_override': self.is_override,
            'is_native': self.is_native,
            'is_native_callable': self.is_native_callable
        }


@dataclass
class Property:
    """Class property or module variable"""
    name: str
    type: str
    modifiers: List[Modifier] = field(default_factory=list)
    is_var: bool = False
    is_external: bool = False
    is_editable: bool = False
    documentation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'type': self.type,
            'modifiers': [m.name for m in self.modifiers],
            'is_var': self.is_var,
            'is_external': self.is_external,
            'is_editable': self.is_editable,
            'documentation': self.documentation
        }


@dataclass
class Event:
    """Event/listenable property"""
    name: str
    payload_type: str
    modifiers: List[Modifier] = field(default_factory=list)
    is_override: bool = False
    documentation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'payload_type': self.payload_type,
            'modifiers': [m.name for m in self.modifiers],
            'is_override': self.is_override,
            'documentation': self.documentation
        }


@dataclass
class VerseClass:
    """Represents a Verse class"""
    name: str
    modifiers: List[Modifier] = field(default_factory=list)
    base_classes: List[str] = field(default_factory=list)
    functions: List[FunctionSignature] = field(default_factory=list)
    properties: List[Property] = field(default_factory=list)
    events: List[Event] = field(default_factory=list)
    documentation: str = ""
    is_abstract: bool = False
    is_final: bool = False
    is_concrete: bool = False
    module_path: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'modifiers': [m.name for m in self.modifiers],
            'base_classes': self.base_classes,
            'functions': [f.to_dict() for f in self.functions],
            'properties': [p.to_dict() for p in self.properties],
            'events': [e.to_dict() for e in self.events],
            'documentation': self.documentation,
            'is_abstract': self.is_abstract,
            'is_final': self.is_final,
            'is_concrete': self.is_concrete,
            'module_path': self.module_path
        }


@dataclass
class VerseEnum:
    """Represents a Verse enum"""
    name: str
    values: List[str] = field(default_factory=list)
    modifiers: List[Modifier] = field(default_factory=list)
    documentation: str = ""
    module_path: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'values': self.values,
            'modifiers': [m.name for m in self.modifiers],
            'documentation': self.documentation,
            'module_path': self.module_path
        }


@dataclass
class VerseModule:
    """Represents a Verse module"""
    name: str
    path: str
    classes: List[VerseClass] = field(default_factory=list)
    enums: List[VerseEnum] = field(default_factory=list)
    functions: List[FunctionSignature] = field(default_factory=list)
    properties: List[Property] = field(default_factory=list)
    submodules: List['VerseModule'] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'path': self.path,
            'classes': [c.to_dict() for c in self.classes],
            'enums': [e.to_dict() for e in self.enums],
            'functions': [f.to_dict() for f in self.functions],
            'properties': [p.to_dict() for p in self.properties],
            'submodules': [m.to_dict() for m in self.submodules],
            'attributes': self.attributes
        }


class VerseDigestParser:
    """
    Parses Verse digest files and extracts API information
    """

    # Regex patterns for parsing
    MODIFIER_PATTERN = r'<([a-z_]+)>'
    MODULE_PATTERN = r'^(\w+)<public>\s*:=\s*module:'
    CLASS_PATTERN = r'^(\w+)<([^>]+)>\s*:=\s*class<([^>]*)>\(([^)]*)\):'
    ENUM_PATTERN = r'^(\w+)<([^>]+)>\s*:=\s*enum<([^>]*)>:'
    FUNCTION_PATTERN = r'^(\w+)<([^>]+)>\(([^)]*)\)(<[^:]+>)?:([^=]+)=\s*external'
    PROPERTY_PATTERN = r'^(var\s+)?(\w+)<([^>]+)>:([^=]+)=\s*external'
    EVENT_PATTERN = r'^(\w+)<([^>]+)>:listenable\(([^)]+)\)\s*=\s*external'
    ATTRIBUTE_PATTERN = r'@(\w+)\s*\{([^}]+)\}'
    COMMENT_PATTERN = r'^\s*#(.*)$'

    def __init__(self):
        self.current_module_path = []
        self.current_documentation = []
        self.current_attributes = {}

    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Parse a digest file and return structured data

        Args:
            file_path: Path to .digest.verse file

        Returns:
            Dictionary containing modules, classes, enums, etc.
        """
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        result = {
            'build_version': self._extract_build_version(lines),
            'modules': [],
            'classes': [],
            'enums': [],
            'total_classes': 0,
            'total_functions': 0,
            'total_properties': 0
        }

        # Parse the file line by line
        root_module = self._parse_module_content(lines)

        # Flatten the module tree and collect all entities
        self._flatten_modules(root_module, result)

        # Calculate statistics
        result['total_classes'] = len(result['classes'])
        result['total_functions'] = sum(len(c['functions']) for c in result['classes'])
        result['total_properties'] = sum(len(c['properties']) for c in result['classes'])

        return result

    def _extract_build_version(self, lines: List[str]) -> str:
        """Extract build version from header"""
        for line in lines[:10]:
            if 'Generated from build:' in line:
                match = re.search(r'Generated from build:\s*(.+)', line)
                if match:
                    return match.group(1).strip()
        return "unknown"

    def _parse_modifiers(self, modifier_text: str) -> List[Modifier]:
        """Parse modifiers like <public><native><final>"""
        modifiers = []
        for match in re.finditer(self.MODIFIER_PATTERN, modifier_text):
            modifiers.append(Modifier(match.group(1)))
        return modifiers

    def _parse_parameters(self, params_text: str) -> List[Parameter]:
        """Parse function parameters"""
        if not params_text or not params_text.strip():
            return []

        parameters = []
        # Split by comma, but be careful of nested types like map[string]int
        param_parts = []
        depth = 0
        current = ""

        for char in params_text:
            if char in '[{(<':
                depth += 1
            elif char in ']})>':
                depth -= 1
            elif char == ',' and depth == 0:
                param_parts.append(current.strip())
                current = ""
                continue
            current += char

        if current.strip():
            param_parts.append(current.strip())

        for part in param_parts:
            if ':' in part:
                name, ptype = part.split(':', 1)
                parameters.append(Parameter(name.strip(), ptype.strip()))

        return parameters

    def _parse_class_line(self, line: str, indent_level: int) -> Optional[VerseClass]:
        """Parse a class definition line"""
        # Pattern: class_name<modifiers> := class<class_modifiers>(base_classes):
        match = re.match(r'^\s*(\w+)<([^>]+)>\s*:=\s*class<([^>]*)>\(([^)]*)\):', line)
        if not match:
            return None

        name = match.group(1)
        name_modifiers = self._parse_modifiers(match.group(2))
        class_modifiers_text = match.group(3)
        base_classes_text = match.group(4)

        verse_class = VerseClass(
            name=name,
            modifiers=name_modifiers,
            base_classes=[b.strip() for b in base_classes_text.split(',') if b.strip()],
            documentation='\n'.join(self.current_documentation)
        )

        # Parse class modifiers
        if class_modifiers_text:
            class_modifiers = self._parse_modifiers(f'<{class_modifiers_text}>')
            for mod in class_modifiers:
                if mod.name == 'abstract':
                    verse_class.is_abstract = True
                elif mod.name == 'final':
                    verse_class.is_final = True
                elif mod.name == 'concrete':
                    verse_class.is_concrete = True

        self.current_documentation = []
        return verse_class

    def _parse_enum_line(self, line: str) -> Optional[VerseEnum]:
        """Parse an enum definition line"""
        match = re.match(r'^\s*(\w+)<([^>]+)>\s*:=\s*enum<([^>]*)>:', line)
        if not match:
            return None

        name = match.group(1)
        modifiers = self._parse_modifiers(match.group(2))

        verse_enum = VerseEnum(
            name=name,
            modifiers=modifiers,
            documentation='\n'.join(self.current_documentation)
        )

        self.current_documentation = []
        return verse_enum

    def _parse_function_line(self, line: str) -> Optional[FunctionSignature]:
        """Parse a function/method definition line"""
        # Pattern: FunctionName<modifiers>(params)<effect_modifiers>:return_type = external {}
        pattern = r'^\s*(\w+)<([^>]+)>\(([^)]*)\)(<[^:]+>)?:([^=]+)=\s*external'
        match = re.match(pattern, line)

        if not match:
            return None

        name = match.group(1)
        modifiers = self._parse_modifiers(match.group(2))
        params = self._parse_parameters(match.group(3))
        effect_mods_text = match.group(4) or ""
        return_type = match.group(5).strip()

        # Parse effect modifiers
        effect_modifiers = []
        if effect_mods_text:
            effect_modifiers = [m.name for m in self._parse_modifiers(effect_mods_text)]

        func = FunctionSignature(
            name=name,
            modifiers=modifiers,
            parameters=params,
            return_type=return_type,
            effect_modifiers=effect_modifiers,
            is_external=True
        )

        # Check for special modifiers
        for mod in modifiers:
            if mod.name == 'override':
                func.is_override = True
            elif mod.name == 'native':
                func.is_native = True
            elif mod.name == 'native_callable':
                func.is_native_callable = True

        return func

    def _parse_property_line(self, line: str) -> Optional[Property]:
        """Parse a property definition line"""
        # Pattern: var? PropertyName<modifiers>:type = external {}
        pattern = r'^\s*(var\s+)?(\w+)<([^>]+)>:([^=]+)=\s*external'
        match = re.match(pattern, line)

        if not match:
            return None

        is_var = bool(match.group(1))
        name = match.group(2)
        modifiers = self._parse_modifiers(match.group(3))
        ptype = match.group(4).strip()

        prop = Property(
            name=name,
            type=ptype,
            modifiers=modifiers,
            is_var=is_var,
            is_external=True,
            documentation='\n'.join(self.current_documentation)
        )

        # Check for editable attribute
        if hasattr(self, '_last_attribute') and self._last_attribute == 'editable':
            prop.is_editable = True
            self._last_attribute = None

        self.current_documentation = []
        return prop

    def _parse_event_line(self, line: str) -> Optional[Event]:
        """Parse an event/listenable definition line"""
        # Pattern: EventName<modifiers>:listenable(payload_type) = external {}
        pattern = r'^\s*(\w+)<([^>]+)>:listenable\(([^)]+)\)\s*=\s*external'
        match = re.match(pattern, line)

        if not match:
            return None

        name = match.group(1)
        modifiers = self._parse_modifiers(match.group(2))
        payload_type = match.group(3).strip()

        event = Event(
            name=name,
            payload_type=payload_type,
            modifiers=modifiers,
            documentation='\n'.join(self.current_documentation)
        )

        # Check for override
        for mod in modifiers:
            if mod.name == 'override':
                event.is_override = True

        self.current_documentation = []
        return event

    def _parse_module_content(self, lines: List[str]) -> VerseModule:
        """Parse module content recursively"""
        root_module = VerseModule(name="root", path="/")
        current_class = None
        current_enum = None
        current_indent = 0

        for i, line in enumerate(lines):
            # Skip header comments
            if i < 10 and line.strip().startswith('#'):
                continue

            # Track documentation comments
            if line.strip().startswith('#'):
                comment = line.strip()[1:].strip()
                self.current_documentation.append(comment)
                continue

            # Track attributes
            if line.strip().startswith('@'):
                attr_match = re.match(r'@(\w+)', line.strip())
                if attr_match:
                    self._last_attribute = attr_match.group(1)
                continue

            # Empty line - reset documentation
            if not line.strip():
                if not current_class and not current_enum:
                    self.current_documentation = []
                continue

            # Calculate indentation
            indent = len(line) - len(line.lstrip())

            # Class definition
            if ':= class' in line:
                verse_class = self._parse_class_line(line, indent)
                if verse_class:
                    root_module.classes.append(verse_class)
                    current_class = verse_class
                    current_enum = None
                continue

            # Enum definition
            if ':= enum' in line:
                verse_enum = self._parse_enum_line(line)
                if verse_enum:
                    root_module.enums.append(verse_enum)
                    current_enum = verse_enum
                    current_class = None
                continue

            # If we're inside a class, parse members
            if current_class and indent > 0:
                # Try function
                func = self._parse_function_line(line)
                if func:
                    current_class.functions.append(func)
                    continue

                # Try event
                event = self._parse_event_line(line)
                if event:
                    current_class.events.append(event)
                    continue

                # Try property
                prop = self._parse_property_line(line)
                if prop:
                    current_class.properties.append(prop)
                    continue

            # If we're inside an enum, parse values
            if current_enum and indent > 0:
                # Enum values are simple identifiers
                enum_value = line.strip()
                if enum_value and not enum_value.startswith('#'):
                    current_enum.values.append(enum_value)
                continue

        return root_module

    def _flatten_modules(self, module: VerseModule, result: Dict[str, Any]):
        """Flatten module tree and collect all entities"""
        for cls in module.classes:
            result['classes'].append(cls.to_dict())

        for enum in module.enums:
            result['enums'].append(enum.to_dict())

        for submodule in module.submodules:
            self._flatten_modules(submodule, result)


def parse_digest_file(file_path: Path) -> Dict[str, Any]:
    """
    Convenience function to parse a digest file

    Args:
        file_path: Path to .digest.verse file

    Returns:
        Structured dictionary of parsed API data
    """
    parser = VerseDigestParser()
    return parser.parse_file(file_path)


def parse_all_digests(digest_dir: Path) -> Dict[str, Any]:
    """
    Parse all digest files in a directory

    Args:
        digest_dir: Directory containing .digest.verse files

    Returns:
        Combined dictionary of all API data
    """
    all_data = {
        'build_version': '',
        'files': {},
        'total_classes': 0,
        'total_enums': 0,
        'total_functions': 0,
        'total_properties': 0
    }

    for digest_file in digest_dir.glob('*.digest.verse'):
        print(f"Parsing {digest_file.name}...")
        data = parse_digest_file(digest_file)

        all_data['files'][digest_file.stem] = data
        all_data['total_classes'] += data.get('total_classes', 0)
        all_data['total_enums'] += len(data.get('enums', []))
        all_data['total_functions'] += data.get('total_functions', 0)
        all_data['total_properties'] += data.get('total_properties', 0)

        if not all_data['build_version'] and data.get('build_version'):
            all_data['build_version'] = data['build_version']

    return all_data


if __name__ == '__main__':
    import json
    import sys

    if len(sys.argv) < 2:
        print("Usage: python verse_parser.py <digest_file_or_directory>")
        sys.exit(1)

    path = Path(sys.argv[1])

    if path.is_file():
        # Parse single file
        result = parse_digest_file(path)
        print(json.dumps(result, indent=2))
    elif path.is_dir():
        # Parse all files in directory
        result = parse_all_digests(path)
        print(f"\n=== Summary ===")
        print(f"Build Version: {result['build_version']}")
        print(f"Total Classes: {result['total_classes']}")
        print(f"Total Enums: {result['total_enums']}")
        print(f"Total Functions: {result['total_functions']}")
        print(f"Total Properties: {result['total_properties']}")

        # Optionally save to file
        output_file = path / 'parsed_api.json'
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nSaved to: {output_file}")
    else:
        print(f"Error: {path} is not a file or directory")
        sys.exit(1)
