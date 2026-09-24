# Rig model inventory cleanup — September 24

`Beni_SingleLegRig` had accumulated four parts that the single-leg conversion
deletes. They were removed under the transform guard and the model was saved as
a new version. No printed part or released file changed.
[`model_cleanup_checks.json`](model_cleanup_checks.json) holds the results.

## What was wrong

A leg rebuild between September 21 and 23 ran two-leg builders inside the rig
(timeline 984–1349, after the September 17 ABS test parts at 900–965).
`beni_lib.build_cartridge()` ends in `rebuild_spring()`, which recreated the
right-hand `Knee_Spring_L(Mirror)`. `build_knee_stop()` recreated the steel
`Knee_Stop_Arc_L` and the PU `Knee_Bumper_Flex_L` / `Knee_Bumper_Ext_L`
alongside the Ø6 stop dowel. `rig_lib.build_rig_knee_stop_plate()` deletes the
arc, and the 2026-08-20 rig snapshot contains none of the four. Every other
difference from that snapshot is an intended replacement.

Effects: `rig_lib.checks_44()` checks 2 and 3 reported co-located overlaps.
They had been clean on August 20 and September 16. The README ABS-article image
showed the mirror spring floating beside the stand, together with the step-2
torque arm and scale pedestal. The released STLs, the 15-part baseline and the
assembly-manual views were unaffected; the manual shows only explicitly
selected parts.

## Fix

- `rig_lib.RIG_REMOVED` lists what the conversion removes.
  - `checks_44()` check 0 fails while any of them exists.
  - `remove_rig_excluded_parts()` is the guarded cleanup.
- Checks 2 and 3 skip `ABS_TEST_*` parts and the owned-spring envelope. Those
  parts share space with the structural parts they replace and are audited by
  `mechanical_spring_test_fusion.audit()`. This restores `checks_44()` to the
  structural Mode A audit it was on August 20.
- `mechanical_spring_test_fusion.NOT_IN_ABS_ARTICLE` defines what the ABS
  article omits; `_assembly_image()` uses it, views the leg from the
  front-outboard side, and restores visibility and camera.
- The four parts were deleted: 105 → 101 occurrences, 27 timeline features
  removed. Both motor references and every transform-placed part are guarded.

## Verification after cleanup

- `assert_all()`: 32 contracts pass; all 15 printed shapes equal the baseline.
- `mechanical_spring_test_fusion.audit()`:
  - 24 poses from −8° to +15° with zero interference;
  - stop contact at −8.5° and +15.5° (3.556 / 3.554 mm³, unchanged);
  - every insertion and service path clear.
- `checks_44()`, 358 s: check 0 clean; check 1 within 0.043 mm of guide §4;
  zero clashes over 17 shoulder poses and 6 floor stations; checks 4–8
  unchanged from the August 20 record. Before the removal, checks 2 and 3
  were already clean with the new ABS-article filter; check 0 alone failed,
  on exactly these four parts.
- Saved as `Beni_SingleLegRig` v31: 101 occurrences, 1325 timeline items,
  guards and `assert_all()` passing on the saved state.

To undo, promote v30 in Fusion's version history.
