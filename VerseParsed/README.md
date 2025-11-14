# Parsed Verse API Data

This directory contains processed and indexed Verse API data extracted from digest files.

## Contents (Phase 2)

- `fortnite_api.json` - Structured Fortnite Creative API index
- `verse_stdlib.json` - Verse standard library reference
- `api_index.sqlite` - Queryable database for fast lookups
- `markdown/` - Human-readable API documentation

## Structure

```json
{
  "classes": [
    {
      "name": "button_device",
      "module": "Fortnite.Devices",
      "inherits": "creative_device",
      "functions": [...],
      "events": [...],
      "properties": [...]
    }
  ],
  "functions": [...],
  "enums": [...]
}
```

## Purpose

This parsed data enables:
1. Fast API lookups for code generation
2. Type validation for Verse code
3. IntelliSense-like suggestions for the agent
4. Template parameter validation

## Status

- [ ] Parser implemented (Phase 2)
- [ ] Digest files parsed
- [ ] API index built
- [ ] Searchable database created
