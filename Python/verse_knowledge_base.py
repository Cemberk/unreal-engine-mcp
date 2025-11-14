#!/usr/bin/env python3
"""
Verse API Knowledge Base

Provides query interface to parsed Verse API data from digest files.
Supports searching for classes, functions, properties, and generating
code examples.

Usage:
    kb = VerseKnowledgeBase('VerseParsed/fortnite_api.json')
    results = kb.search_classes('button')
    device_info = kb.get_class('button_device')
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class SearchResult:
    """Represents a search result"""
    entity_type: str  # 'class', 'function', 'property', 'enum'
    name: str
    description: str
    relevance_score: float
    data: Dict[str, Any]

    def __repr__(self):
        return f"<{self.entity_type}: {self.name} (score: {self.relevance_score:.2f})>"


class VerseKnowledgeBase:
    """
    Queryable knowledge base of Verse API

    Provides methods to search and retrieve information about:
    - Classes and their members
    - Functions and their signatures
    - Properties and events
    - Enums and their values
    """

    def __init__(self, api_index_path: Path):
        """
        Initialize knowledge base from parsed API index

        Args:
            api_index_path: Path to fortnite_api.json (from verse_parser)
        """
        self.api_index_path = Path(api_index_path)
        self.api_data = self._load_api_data()

        # Build search indexes
        self.class_index = self._build_class_index()
        self.function_index = self._build_function_index()
        self.property_index = self._build_property_index()
        self.enum_index = self._build_enum_index()

    def _load_api_data(self) -> Dict[str, Any]:
        """Load API data from JSON file"""
        with open(self.api_index_path, 'r') as f:
            return json.load(f)

    def _build_class_index(self) -> Dict[str, Dict[str, Any]]:
        """Build index of all classes by name"""
        index = {}
        for file_name, file_data in self.api_data.get('files', {}).items():
            for cls in file_data.get('classes', []):
                index[cls['name'].lower()] = {
                    'source_file': file_name,
                    'data': cls
                }
        return index

    def _build_function_index(self) -> Dict[str, List[Dict[str, Any]]]:
        """Build index of all functions by name"""
        index = {}
        for file_name, file_data in self.api_data.get('files', {}).items():
            for cls in file_data.get('classes', []):
                for func in cls.get('functions', []):
                    func_name = func['name'].lower()
                    if func_name not in index:
                        index[func_name] = []
                    index[func_name].append({
                        'class': cls['name'],
                        'source_file': file_name,
                        'data': func
                    })
        return index

    def _build_property_index(self) -> Dict[str, List[Dict[str, Any]]]:
        """Build index of all properties by name"""
        index = {}
        for file_name, file_data in self.api_data.get('files', {}).items():
            for cls in file_data.get('classes', []):
                for prop in cls.get('properties', []):
                    prop_name = prop['name'].lower()
                    if prop_name not in index:
                        index[prop_name] = []
                    index[prop_name].append({
                        'class': cls['name'],
                        'source_file': file_name,
                        'data': prop
                    })
        return index

    def _build_enum_index(self) -> Dict[str, Dict[str, Any]]:
        """Build index of all enums by name"""
        index = {}
        for file_name, file_data in self.api_data.get('files', {}).items():
            for enum in file_data.get('enums', []):
                index[enum['name'].lower()] = {
                    'source_file': file_name,
                    'data': enum
                }
        return index

    def search_classes(self, query: str, limit: int = 10) -> List[SearchResult]:
        """
        Search for classes matching query

        Args:
            query: Search term (partial name, keyword)
            limit: Maximum results to return

        Returns:
            List of SearchResult objects sorted by relevance
        """
        results = []
        query_lower = query.lower()

        for class_name, class_info in self.class_index.items():
            score = self._calculate_relevance(query_lower, class_name, class_info['data'])
            if score > 0:
                results.append(SearchResult(
                    entity_type='class',
                    name=class_info['data']['name'],
                    description=class_info['data'].get('documentation', '')[:200],
                    relevance_score=score,
                    data=class_info['data']
                ))

        # Sort by relevance and limit
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:limit]

    def search_functions(self, query: str, limit: int = 10) -> List[SearchResult]:
        """Search for functions matching query"""
        results = []
        query_lower = query.lower()

        for func_name, func_list in self.function_index.items():
            for func_info in func_list:
                score = self._calculate_relevance(query_lower, func_name, func_info['data'])
                if score > 0:
                    results.append(SearchResult(
                        entity_type='function',
                        name=f"{func_info['class']}.{func_info['data']['name']}",
                        description=f"Returns {func_info['data'].get('return_type', 'void')}",
                        relevance_score=score,
                        data=func_info['data']
                    ))

        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:limit]

    def search_by_keyword(self, keyword: str, limit: int = 20) -> List[SearchResult]:
        """
        Search for any entity matching keyword

        Searches across classes, functions, properties with keyword
        in name or documentation.

        Args:
            keyword: Keyword to search for
            limit: Maximum results

        Returns:
            Combined search results from all entity types
        """
        all_results = []

        # Search classes
        all_results.extend(self.search_classes(keyword, limit=limit))

        # Search functions
        all_results.extend(self.search_functions(keyword, limit=limit))

        # Re-sort and limit
        all_results.sort(key=lambda x: x.relevance_score, reverse=True)
        return all_results[:limit]

    def get_class(self, class_name: str) -> Optional[Dict[str, Any]]:
        """
        Get complete class information by name

        Args:
            class_name: Exact or partial class name

        Returns:
            Class dictionary with all members, or None if not found
        """
        class_name_lower = class_name.lower()

        # Try exact match first
        if class_name_lower in self.class_index:
            return self.class_index[class_name_lower]['data']

        # Try partial match
        for cls_name, cls_info in self.class_index.items():
            if class_name_lower in cls_name:
                return cls_info['data']

        return None

    def get_devices(self) -> List[Dict[str, Any]]:
        """Get all device classes (classes ending with '_device')"""
        devices = []
        for class_name, class_info in self.class_index.items():
            if class_name.endswith('_device'):
                devices.append(class_info['data'])
        return devices

    def get_class_functions(self, class_name: str) -> List[Dict[str, Any]]:
        """Get all functions for a specific class"""
        cls = self.get_class(class_name)
        if cls:
            return cls.get('functions', [])
        return []

    def get_class_properties(self, class_name: str) -> List[Dict[str, Any]]:
        """Get all properties for a specific class"""
        cls = self.get_class(class_name)
        if cls:
            return cls.get('properties', [])
        return []

    def get_class_events(self, class_name: str) -> List[Dict[str, Any]]:
        """Get all events for a specific class"""
        cls = self.get_class(class_name)
        if cls:
            return cls.get('events', [])
        return []

    def find_classes_by_base(self, base_class: str) -> List[Dict[str, Any]]:
        """Find all classes that inherit from a specific base class"""
        results = []
        base_lower = base_class.lower()

        for class_info in self.class_index.values():
            cls = class_info['data']
            base_classes = [b.lower() for b in cls.get('base_classes', [])]
            if base_lower in base_classes:
                results.append(cls)

        return results

    def generate_function_signature(self, func_data: Dict[str, Any]) -> str:
        """
        Generate Verse function signature from function data

        Args:
            func_data: Function dictionary from API

        Returns:
            Verse function signature string
        """
        name = func_data['name']

        # Build modifiers
        modifiers = '<' + '><'.join(func_data.get('modifiers', [])) + '>'

        # Build parameters
        params = func_data.get('parameters', [])
        param_strs = [f"{p['name']}:{p['type']}" for p in params]
        params_str = ', '.join(param_strs)

        # Build effect modifiers
        effect_mods = func_data.get('effect_modifiers', [])
        effect_str = '<' + '><'.join(effect_mods) + '>' if effect_mods else ''

        # Return type
        return_type = func_data.get('return_type', 'void')

        return f"{name}{modifiers}({params_str}){effect_str}:{return_type}"

    def generate_class_skeleton(self, class_name: str) -> Optional[str]:
        """
        Generate a Verse class skeleton with stubs

        Args:
            class_name: Name of class to generate skeleton for

        Returns:
            Verse code string or None if class not found
        """
        cls = self.get_class(class_name)
        if not cls:
            return None

        lines = []

        # Class documentation
        if cls.get('documentation'):
            lines.append(f"# {cls['documentation']}")

        # Class definition
        base_classes = ', '.join(cls.get('base_classes', []))
        modifiers = '<' + '><'.join(cls.get('modifiers', [])) + '>'
        lines.append(f"{cls['name']}{modifiers} := class({base_classes}):")

        # Properties
        for prop in cls.get('properties', []):
            if prop.get('documentation'):
                lines.append(f"    # {prop['documentation']}")
            var_prefix = "var " if prop.get('is_var') else ""
            prop_mods = '<' + '><'.join(prop.get('modifiers', [])) + '>'
            lines.append(f"    {var_prefix}{prop['name']}{prop_mods}:{prop['type']} = external {{}}")
            lines.append("")

        # Functions
        for func in cls.get('functions', []):
            sig = self.generate_function_signature(func)
            lines.append(f"    {sig} = external {{}}")
            lines.append("")

        return '\n'.join(lines)

    def get_statistics(self) -> Dict[str, int]:
        """Get API statistics"""
        return {
            'total_classes': len(self.class_index),
            'total_functions': sum(len(funcs) for funcs in self.function_index.values()),
            'total_properties': sum(len(props) for props in self.property_index.values()),
            'total_enums': len(self.enum_index),
            'total_devices': len([c for c in self.class_index if c.endswith('_device')]),
            'build_version': self.api_data.get('build_version', 'unknown')
        }

    def _calculate_relevance(self, query: str, name: str, data: Dict[str, Any]) -> float:
        """Calculate relevance score for search result"""
        score = 0.0

        # Exact match
        if query == name:
            score += 100.0

        # Starts with query
        elif name.startswith(query):
            score += 75.0

        # Contains query
        elif query in name:
            score += 50.0

        # Check documentation
        doc = data.get('documentation', '').lower()
        if query in doc:
            score += 25.0

        # Bonus for device classes
        if name.endswith('_device'):
            score += 5.0

        # Bonus for public/accessible items
        modifiers = data.get('modifiers', [])
        if 'public' in modifiers:
            score += 2.0

        return score

    def export_device_catalog(self, output_path: Path):
        """Export a catalog of all devices with descriptions"""
        devices = self.get_devices()

        catalog = {
            'total_devices': len(devices),
            'build_version': self.api_data.get('build_version'),
            'devices': []
        }

        for device in devices:
            catalog['devices'].append({
                'name': device['name'],
                'base_classes': device.get('base_classes', []),
                'documentation': device.get('documentation', ''),
                'function_count': len(device.get('functions', [])),
                'property_count': len(device.get('properties', [])),
                'event_count': len(device.get('events', []))
            })

        with open(output_path, 'w') as f:
            json.dump(catalog, f, indent=2)


def main():
    """Example usage"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python verse_knowledge_base.py <api_index_json>")
        sys.exit(1)

    kb = VerseKnowledgeBase(sys.argv[1])

    # Print statistics
    stats = kb.get_statistics()
    print("=== Verse API Statistics ===")
    for key, value in stats.items():
        print(f"{key}: {value}")
    print()

    # Example searches
    print("=== Device Search (button) ===")
    results = kb.search_classes('button', limit=5)
    for r in results:
        print(f"{r.name} - {r.description[:100]}")
    print()

    # Show button_device details
    print("=== button_device Details ===")
    button_device = kb.get_class('button_device')
    if button_device:
        print(f"Name: {button_device['name']}")
        print(f"Base Classes: {', '.join(button_device['base_classes'])}")
        print(f"Functions: {len(button_device['functions'])}")
        print(f"Properties: {len(button_device['properties'])}")
        print(f"Events: {len(button_device['events'])}")
        print(f"\nDocumentation: {button_device.get('documentation', 'N/A')}")

        # Show first 3 functions
        print("\nFunctions:")
        for func in button_device['functions'][:3]:
            sig = kb.generate_function_signature(func)
            print(f"  {sig}")

        # Show events
        print("\nEvents:")
        for event in button_device['events']:
            print(f"  {event['name']}: listenable({event['payload_type']})")

    # Export device catalog
    print("\n=== Exporting Device Catalog ===")
    output_path = Path('VerseParsed/device_catalog.json')
    kb.export_device_catalog(output_path)
    print(f"Saved to: {output_path}")


if __name__ == '__main__':
    main()
