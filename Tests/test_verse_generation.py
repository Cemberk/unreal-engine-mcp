#!/usr/bin/env python3
"""
Test Verse Code Generation

Generates 10 sample Verse devices to validate the code generation pipeline.

Usage:
    python test_verse_generation.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'Python'))

from verse_generator import VerseCodeGenerator


def main():
    """Generate sample Verse devices"""
    print("=== Verse Code Generation Test ===\n")

    # Initialize generator
    api_index = Path(__file__).parent.parent / 'VerseParsed' / 'fortnite_api.json'
    generator = VerseCodeGenerator(api_index)

    # Output directory
    output_dir = Path(__file__).parent / 'generated_verse'
    output_dir.mkdir(exist_ok=True)

    test_devices = [
        # 1. Simple button
        {
            'type': 'button',
            'name': 'simple_button',
            'params': {
                'BUTTON_NAME': 'ActionButton',
                'DESCRIPTION': 'Simple button press handler'
            }
        },
        # 2. Button with cooldown
        {
            'type': 'button',
            'name': 'cooldown_button',
            'params': {
                'BUTTON_NAME': 'CooldownButton',
                'DESCRIPTION': 'Button with 5 second cooldown',
                'IF_COOLDOWN': True,
                'COOLDOWN_SECONDS': '5.0'
            }
        },
        # 3. Limited use button
        {
            'type': 'button',
            'name': 'limited_button',
            'params': {
                'BUTTON_NAME': 'LimitedButton',
                'DESCRIPTION': 'Button with 3 uses',
                'IF_USE_COUNT': True,
                'MAX_USES': '3'
            }
        },
        # 4. Timer device
        {
            'type': 'timer',
            'name': 'countdown_timer',
            'params': {
                'TIMER_NAME': 'GameTimer',
                'DESCRIPTION': '60 second countdown timer',
                'DURATION_SECONDS': '60.0',
                'IS_REPEATING': 'false',
                'IF_AUTO_START': True
            }
        },
        # 5. Repeating timer
        {
            'type': 'timer',
            'name': 'interval_timer',
            'params': {
                'TIMER_NAME': 'IntervalTimer',
                'DESCRIPTION': '10 second repeating timer',
                'DURATION_SECONDS': '10.0',
                'IS_REPEATING': 'true',
                'IF_INTERVAL': True,
                'INTERVAL_SECONDS': '1.0'
            }
        },
        # 6. Item spawner
        {
            'type': 'spawner',
            'name': 'coin_spawner',
            'params': {
                'SPAWNER_NAME': 'CoinSpawner',
                'DESCRIPTION': 'Spawns collectible coins',
                'SPAWN_DELAY_SECONDS': '2.0',
                'MAX_SPAWNS': '10',
                'IF_AUTO_SPAWN': True,
                'IF_CONTINUOUS': True,
                'IF_RESPAWN_ON_PICKUP': True,
                'RESPAWN_DELAY_SECONDS': '5.0'
            }
        },
        # 7. Wave spawner
        {
            'type': 'spawner',
            'name': 'wave_spawner',
            'params': {
                'SPAWNER_NAME': 'EnemySpawner',
                'DESCRIPTION': 'Wave-based enemy spawning',
                'SPAWN_DELAY_SECONDS': '0.5',
                'MAX_SPAWNS': '50',
                'IF_WAVE_SPAWNING': True,
                'SPAWNS_PER_WAVE': '10',
                'WAVE_SPAWN_INTERVAL': '0.5'
            }
        },
        # 8. Trigger volume
        {
            'type': 'trigger',
            'name': 'checkpoint_trigger',
            'params': {
                'DESCRIPTION': 'Race checkpoint trigger'
            }
        },
        # 9. Collectible manager
        {
            'type': 'collectible',
            'name': 'coin_collector',
            'params': {
                'DESCRIPTION': 'Tracks coin collection progress'
            }
        },
        # 10. Conditional button
        {
            'type': 'conditional_button',
            'params': {
                'DESCRIPTION': 'Button requiring 100 score',
                'REQUIRED_SCORE': '100',
                'IF_SCORE_CONDITION': True
            }
        }
    ]

    results = []
    for i, device in enumerate(test_devices, 1):
        print(f"\n{i}. Generating {device.get('name', 'device')}...")

        try:
            code = generator.generate_device_handler(
                device_type=device['type'],
                module_name=device.get('name', f"test_device_{i}"),
                description=device['params'].get('DESCRIPTION', ''),
                **{k: v for k, v in device['params'].items() if k != 'DESCRIPTION'}
            )

            # Validate
            validation = generator.validate_verse_syntax(code)

            # Save to file
            filename = f"{device.get('name', f'device_{i}')}.verse"
            output_file = output_dir / filename
            output_file.write_text(code)

            results.append({
                'name': device.get('name', f'device_{i}'),
                'type': device['type'],
                'lines': code.count('\n') + 1,
                'size': len(code),
                'valid': validation['valid'],
                'errors': validation['errors'],
                'file': str(output_file)
            })

            status = "✅" if validation['valid'] else "❌"
            print(f"   {status} {device.get('name', 'device')}: {code.count(chr(10)) + 1} lines")
            if not validation['valid']:
                for error in validation['errors']:
                    print(f"      - {error}")

        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                'name': device.get('name', f'device_{i}'),
                'type': device['type'],
                'error': str(e)
            })

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    valid_count = sum(1 for r in results if r.get('valid', False))
    total_lines = sum(r.get('lines', 0) for r in results)
    total_size = sum(r.get('size', 0) for r in results)

    print(f"Total Devices Generated: {len(results)}")
    print(f"Valid Devices: {valid_count}/{len(results)}")
    print(f"Total Lines of Code: {total_lines}")
    print(f"Total Size: {total_size:,} bytes")
    print(f"Output Directory: {output_dir}")

    # List generated files
    print(f"\nGenerated Files:")
    for result in results:
        if 'file' in result:
            print(f"  • {Path(result['file']).name}")

    if valid_count == len(results):
        print("\n✅ All devices generated successfully!")
        return 0
    else:
        print(f"\n⚠️  {len(results) - valid_count} device(s) failed validation")
        return 1


if __name__ == '__main__':
    sys.exit(main())
