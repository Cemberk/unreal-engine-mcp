# Verse Code Templates

This directory contains reusable Verse code templates for common patterns.

## Template Categories

### devices/
Pre-built Verse device templates:
- `button_device.verse.template` - Button interaction handler
- `spawner_device.verse.template` - Actor spawning system
- `timer_device.verse.template` - Countdown/interval timers
- `item_granter.verse.template` - Item giving system
- `team_manager.verse.template` - Team assignment logic
- `damage_volume.verse.template` - Player damage zones
- `teleporter.verse.template` - Teleportation devices

### gameplay/
Gameplay system templates:
- `scoring_system.verse.template` - Point tracking
- `round_controller.verse.template` - Round-based game flow
- `elimination_tracker.verse.template` - Kill/death tracking
- `capture_point.verse.template` - Territory control
- `race_checkpoint.verse.template` - Racing game logic

### utils/
Utility function templates:
- `player_helpers.verse.template` - Player query/manipulation
- `math_utils.verse.template` - Vector/math helpers
- `ui_helpers.verse.template` - HUD message utilities

## Template Format

Templates use placeholders for code generation:
```verse
{{MODULE_NAME}} := class(creative_device):
    @editable
    {{DEVICE_PROPERTY}} : {{DEVICE_TYPE}} = {{DEVICE_TYPE}}{}

    OnBegin<override>()<suspends>:void=
        {{EVENT_SUBSCRIPTION}}
```

## Status

- [ ] 10-15 device templates created (Phase 2)
- [ ] 5-10 gameplay templates created (Phase 2)
- [ ] Utility templates created (Phase 2)
- [ ] Template engine implemented (Phase 3)
