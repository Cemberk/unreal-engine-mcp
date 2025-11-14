# Phase 6: Integration & Testing - PLAN

**Status**: 🚀 **READY TO START**
**Timeline**: Weeks 8-10 (Est. 2-3 weeks)
**Prerequisites**: Phases 1-4 complete, Phase 5 skipped

---

## Overview

Phase 6 validates the complete UE5 → UEFN export pipeline end-to-end with real project levels.

**Goals**:
1. Verify export pipeline works with production levels
2. Measure workflow performance and timings
3. Validate transform accuracy (positions, rotations, scales)
4. Test edge cases and stress scenarios
5. Document best practices and gotchas

---

## Test Strategy

### Tier 1: Validation Tests (Small Scale)

**Purpose**: Verify correctness of export pipeline

**Test Levels**:
1. **Transform Test Level** (20-30 actors)
   - Pathological rotations (negative angles, combos, gimbal cases)
   - Non-uniform scales (tiny, huge, mirrored)
   - Offset pivots
   - Mixed actor types

2. **Architecture Test** (50 actors)
   - Grid of floors, walls
   - Corner towers
   - Gates and doors
   - Validate spatial alignment

**Success Criteria**:
- [ ] All actors spawn at correct positions (±10cm tolerance)
- [ ] Rotations accurate (±5° tolerance)
- [ ] Scales accurate (±10% tolerance)
- [ ] No missing meshes or materials
- [ ] Verse code builds without errors

### Tier 2: Reference Tests (Medium Scale)

**Purpose**: Validate against known-good reference

**Test Levels**:
1. **Medieval Castle** (197 actors) - Already exported
   - Re-import and verify against export
   - Check reference counts match asset usage
   - Validate spawner device organization

**Success Criteria**:
- [ ] All 197 actors spawn correctly
- [ ] 13 unique assets imported successfully
- [ ] Verse build succeeds (<10 sec)
- [ ] Spawn time acceptable (<5 sec in Play mode)
- [ ] Visual match to UE5 level (screenshot comparison)

### Tier 3: Real Project Tests (Production Scale)

**Purpose**: Test with actual project content

**Test Levels** (choose 1-2):
1. **Town Level** (if available)
2. **Obstacle Course** (if available)
3. **Dungeon/Interior** (if available)

**Success Criteria**:
- [ ] Export completes without errors
- [ ] Manifest accurately reflects assets
- [ ] Import workflow completes in <10 minutes
- [ ] Gameplay testing shows correct behavior
- [ ] Performance acceptable in Fortnite Creative

### Tier 4: Stress Tests (Large Scale)

**Purpose**: Find performance limits and edge cases

**Test Scenarios**:
1. **Large Level** (500+ actors)
   - Generate procedural city block or maze
   - Test spawn performance
   - Measure memory usage
   - Validate device count limits

2. **High Asset Diversity** (100+ unique assets)
   - Many different meshes
   - Test manifest generation
   - FBX export time
   - Import workflow duration

3. **Complex Hierarchies**
   - Nested actor groups
   - Parented transforms
   - Blueprint actors (if supported)

**Success Criteria**:
- [ ] Document performance limits (max actors, spawn time, memory)
- [ ] Identify bottlenecks in workflow
- [ ] Establish recommendations for level size

---

## Test Procedure

### For Each Test Level

**1. Export from UE5**
```python
# Run export pipeline
result = await export_level_to_uefn(
    level_name='TestLevel',
    actors_json=json.dumps(actors),
    export_path='Exports/TestLevel',
    options={'generate_spawn_code': True}
)

# Verify export success
validation = await package_assets_for_fortnite(
    manifest_path='Exports/TestLevel/Manifests/TestLevel_manifest.json',
    export_path='Exports/TestLevel',
    validation_level='strict'
)
```

**Time**: Export phase

**2. Export FBX Assets from UE5**
- Open UE5 project
- Use manifest to identify assets
- Select in Content Browser
- Export as FBX to `Exports/TestLevel/Assets/`

**Time**: Manual FBX export

**3. Import to UEFN**
- Open UEFN project
- Create `ImportedAssets/TestLevel/` folder
- Import all FBX files
- Verify materials/textures

**Time**: Import phase

**4. Install Verse Code**
- Copy `TestLevel_spawner.verse` to UEFN project
- Build Verse (Ctrl+F7)
- Check for compilation errors

**Time**: Verse build

**5. Configure Spawner Device**
- Drag spawner device to island
- Place item_spawner_device instances
- Link to @editable arrays
- Configure spawner settings

**Time**: Device configuration

**6. Test in Fortnite Creative**
- Enter Play mode
- Observe actor spawning
- Check positions, rotations, scales
- Screenshot for comparison

**Time**: Testing

**7. Document Results**
- Record all timings
- Note any errors or warnings
- Capture screenshots
- Log issues/gotcas

**Time**: Documentation

---

## Measurements to Capture

### Timing Data

| Phase | Metric | Target | Notes |
|-------|--------|--------|-------|
| Export | Time to generate manifest | <5 sec | For 200 actors |
| Export | Time to generate Verse code | <10 sec | For 200 actors |
| Export | Lines of Verse generated | N/A | Track for size analysis |
| FBX Export | Time to export all assets | <5 min | For 20 unique assets |
| Import | Time to import to UEFN | <5 min | For 20 FBX files |
| Verse Build | Compilation time | <30 sec | For 200-actor spawner |
| Verse Build | Build errors/warnings | 0 | Should be clean |
| Configuration | Time to configure spawners | <5 min | Device placement + linking |
| Runtime | Spawn time in Play mode | <5 sec | For 200 actors |
| **Total** | **End-to-end workflow** | **<20 min** | **Target for 200-actor level** |

### Quality Data

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Position accuracy | ±10cm | Compare UE5 vs UEFN screenshots |
| Rotation accuracy | ±5° | Visual inspection + manual checks |
| Scale accuracy | ±10% | Measure spawned props in UEFN |
| Asset import success | 100% | All manifested assets imported |
| Verse build success | 100% | No compilation errors |
| Material correctness | >90% | Visual comparison (some loss expected) |

### Performance Data

| Metric | Measurement |
|--------|-------------|
| Memory usage (UEFN) | Check Stats window during import |
| Memory usage (Play) | During spawning and after |
| Frame rate | FPS during spawn vs steady-state |
| Object count | Check UEFN object limits |
| Device count | Track spawner devices used |
| Max actors tested | Find practical limit |

---

## Edge Cases to Test

### Transform Edge Cases

- [ ] Rotation: (0, 0, 0) - identity
- [ ] Rotation: (90, 90, 90) - all axes
- [ ] Rotation: (-45, 135, -30) - negative combos
- [ ] Rotation: (0.1, 0.1, 0.1) - near-zero
- [ ] Rotation: (359.9, 270, 180) - large angles
- [ ] Scale: (1, 1, 1) - uniform identity
- [ ] Scale: (5, 5, 5) - uniform large
- [ ] Scale: (0.1, 0.1, 0.1) - uniform small
- [ ] Scale: (1, 2, 0.5) - non-uniform
- [ ] Scale: (-1, 1, 1) - mirrored
- [ ] Position: (0, 0, 0) - origin
- [ ] Position: (10000, 10000, 5000) - far from origin
- [ ] Position: (-5000, -5000, 0) - negative coordinates

### Asset Edge Cases

- [ ] Asset with many materials (10+)
- [ ] Asset with LODs (multiple detail levels)
- [ ] Asset with collision meshes
- [ ] Asset with very high poly count (>100k triangles)
- [ ] Asset with procedural textures (how they export)
- [ ] Asset referenced by many actors (>100 instances)
- [ ] Asset with unusual pivots (far from geometry center)

### Level Edge Cases

- [ ] Level with no actors (empty)
- [ ] Level with 1 actor (minimal)
- [ ] Level with all same actor type (100 identical props)
- [ ] Level with many actor types (20+ classes)
- [ ] Level with deeply nested transforms (hierarchy depth)
- [ ] Level with actor names containing special chars (spaces, unicode)

---

## Deliverables

### Documentation

- [ ] **PHASE_6_STATUS.md**
  - Complete test results
  - All timing data
  - Quality measurements
  - Issues encountered & resolutions

- [ ] **Docs/WORKFLOW_TIMINGS.md**
  - Detailed timing breakdown per test level
  - Bottleneck analysis
  - Optimization recommendations

- [ ] **Docs/BEST_PRACTICES.md**
  - Lessons learned
  - Tips for efficient workflow
  - Common pitfalls and solutions
  - Recommended level size limits

- [ ] **Docs/TRANSFORM_VALIDATION_REPORT.md**
  - Position/rotation/scale accuracy data
  - Screenshots comparing UE5 vs UEFN
  - Known issues and workarounds

### Test Artifacts

- [ ] **Tests/Phase6/**
  - Transform test level export
  - Architecture test export
  - Medieval Castle re-export (for comparison)
  - Real project level export (if available)

- [ ] **Screenshots/**
  - UE5 level screenshots (reference)
  - UEFN imported level screenshots (comparison)
  - Side-by-side comparisons

### Code Updates

- [ ] **Updated EXPORT_WORKFLOW_GUIDE.md**
  - Real-world timings
  - Tested on Windows (your machine)
  - Screenshots of UEFN import process

- [ ] **Bug fixes** (if any found during testing)
  - Rotation conversion issues
  - Scale handling
  - Asset path edge cases

---

## Success Criteria (Phase 6)

### Must Have (MVP)

- [ ] At least 2 test levels successfully exported and imported
- [ ] Medieval Castle (197 actors) validates successfully
- [ ] All timings documented (<20 min end-to-end for 200-actor level)
- [ ] Transform accuracy within tolerances (±10cm, ±5°, ±10%)
- [ ] Zero critical bugs blocking workflow
- [ ] Complete documentation of workflow with screenshots

### Should Have

- [ ] 1 real project level tested
- [ ] Stress test completed (500+ actor level)
- [ ] Performance limits documented
- [ ] Best practices guide written
- [ ] Known issues documented with workarounds

### Nice to Have

- [ ] Video walkthrough of workflow
- [ ] Automated transform validation script
- [ ] Performance profiling data
- [ ] Recommendations for Phase 7 optimizations

---

## Risk Mitigation

### Potential Issues & Plans

**Issue**: Transform accuracy problems (rotations off)
- **Mitigation**: Test with known rotations first, validate conversion
- **Fallback**: Document manual adjustment process

**Issue**: Material/texture loss during FBX export
- **Mitigation**: Expected for some materials; document limitations
- **Fallback**: Manual material assignment in UEFN

**Issue**: UEFN actor/device limits hit
- **Mitigation**: Test incrementally, document limits found
- **Fallback**: Level chunking strategy (split into regions)

**Issue**: Verse compilation errors
- **Mitigation**: Validate generated code thoroughly
- **Fallback**: Fix generator, regenerate

**Issue**: Poor performance (slow spawning, low FPS)
- **Mitigation**: Measure early, optimize Verse code
- **Fallback**: Chunked spawning, LOD strategies

---

## Timeline Estimate

### Week 8: Validation & Reference Tests

**Days 1-2**: Tier 1 (Transform + Architecture tests)
- Create test levels in UE5
- Export and import to UEFN
- Measure accuracy

**Days 3-4**: Tier 2 (Medieval Castle re-test)
- Re-export with latest pipeline
- Validate against previous export
- Document any differences

**Day 5**: Document findings, fix any bugs

### Week 9: Real Project & Stress Tests

**Days 1-2**: Tier 3 (Real project level)
- Select level from actual project
- Full workflow test
- Document real-world issues

**Days 3-4**: Tier 4 (Stress tests)
- Generate large test levels
- Find performance limits
- Document recommendations

**Day 5**: Consolidate results, write reports

### Week 10: Documentation & Polish

**Days 1-2**: Complete all documentation
- PHASE_6_STATUS.md
- WORKFLOW_TIMINGS.md
- BEST_PRACTICES.md
- TRANSFORM_VALIDATION_REPORT.md

**Days 3-4**: Update guides with real-world data
- Screenshots from actual workflow
- Timing data
- Tips and tricks

**Day 5**: Final review, Phase 6 completion

---

## Next Steps

**Immediate** (This Week):
1. ✅ Document Phase 5 skip decision (done)
2. ✅ Update EXPORT_WORKFLOW_GUIDE.md (done)
3. 🔄 Create Phase 6 plan (this document)
4. ⏭️ Identify test level candidates (user decision)
5. ⏭️ Start Tier 1 tests (transform validation)

**Short Term** (Week 8):
- Run all Tier 1 and Tier 2 tests
- Document timings and quality metrics
- Fix any critical bugs found

**Medium Term** (Weeks 9-10):
- Complete Tier 3 and Tier 4 tests
- Write comprehensive documentation
- Prepare for Phase 7 (if needed)

---

## Open Questions

1. **Which real project level to test?**
   - Town, castle, dungeon, obstacle course?
   - User should select based on what's most representative

2. **How thorough should stress testing be?**
   - Find absolute limits or just practical limits?
   - Balance time investment vs value

3. **Video walkthrough worth the effort?**
   - Useful for documentation
   - Time-consuming to produce
   - User decision

4. **Should we implement prop vs device backend now?**
   - From PHASE_4_IMPROVEMENTS.md
   - Or defer to Phase 7?

---

## Conclusion

Phase 6 is the validation phase - proving the export pipeline works end-to-end with real content.

**Key Focus Areas**:
- ✅ Correctness (transforms, assets, Verse code)
- ✅ Performance (timings, limits, optimization)
- ✅ Documentation (real-world data, best practices)

**Expected Outcome**: Validated, production-ready UE5 → UEFN export pipeline with comprehensive documentation.

**After Phase 6**: Decide if Phase 7 (Deprecation & Cleanup) is needed, or if the pipeline is ready for production use.

---

*Phase 6 Integration & Testing Plan - UEFN Migration Project*
*Created: November 13, 2025*
*Status: Ready to Start*
