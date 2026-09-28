# R2A digital gate — 2026-09-27

Fusion document **`Beni_R2A_SingleLeg`**, project Beni. It is a copy of
`Beni_SingleLegRig` v31 made before any edit; the passive-knee parts were
removed under `r2a_lib.guarded()` and the R2A parts were built by
[`r2a_lib.py`](../../../r2a_lib.py). Saved versions: **v3** printed geometry;
**v4** part appearances for the renders; **v5** the knee-actuator and
wheel-motor screws shortened to × 10 (below). Every released shape signature
was re-checked equal before each save, so all three carry the released print
geometry. The legacy baselines were confirmed unchanged at the end of the
session: `Beni_SingleLegRig` v31, `Beni_Prototype1` v18.

Everything below is **CAD evidence**. Nothing in this folder is a physical
result. Design figures and the lateral stack live in the
[R2A plan](../../../docs/design/active_knee_revision2_plan.md); the loads
computed from these measurements are printed by
[`r2a_calc.py`](../../../r2a_calc.py).

## Files

| File | Written by | Contents |
|---|---|---|
| [`fusion_measurements.json`](fusion_measurements.json) | `r2a_lib.write_gate_record()` | Linkage, rod-end/jam-nut design envelope, Y stack, outline, clevis ears, stop contact angles, clearance rows at 11 knee angles, sweep summary, part volumes, linkage map, stand datums. Input to `r2a_calc.py` and `firmware/r2a/gen_linkage_table.py`. |
| [`sweep_interference.json`](sweep_interference.json) | `r2a_lib.sweep_chunk()` | Every detected overlap in 140 poses with its classification (v3). |
| [`sweep_after_screw_change.json`](sweep_after_screw_change.json) | `r2a_lib.sweep_chunk()` | 10-pose spot sweep on v5 after the fastener change: 0 real clashes. |
| [`assembly_paths.json`](assembly_paths.json) | `r2a_paths_fusion.run_steps()` | 33 insertion, tool and service paths on v5, each with its moving set, direction, travel and maximum overlap. |
| [`assembly_path_negative_controls.json`](assembly_path_negative_controls.json) | `r2a_paths_fusion.negative_controls()` | Four deliberately wrong moves, all reported blocked, and one informational key path. |
| [`fastener_engagement.json`](fastener_engagement.json) | `r2a_paths_fusion.fastener_engagement()` | Grip, thread engagement and tip-to-floor clearance of every R2A screw set, from the screws' planar end faces. |
| [`release_audit.json`](release_audit.json) | `r2a_release_fusion` | 37 dimensional contracts, the print audit of every part in its exported bed pose, the distal selective-support removal audit, and the released-file fingerprints. |

## Results

**Interference sweep: 140 poses, 0 real clashes.** Knee α 49…152° in 1°
steps at shoulder 0°, and shoulder −120…+120° in 20° steps at α 51°, 100° and
150°. Every occurrence was forced visible for the sweep (trap below). The
overlaps that remain are classified in `r2a_lib.classify_pair()`, each for a
stated reason:

| Class | Count | Why it is not a design clash |
|---|---:|---|
| screw in modelled STEP thread | 4667 | Screws sit in the STEP's solid threaded holes; ≤ 40 mm³ each |
| cable envelope segments joined by construction | 420 | Adjacent segments of one reference cable |
| alternative wheel parts | 280 | `Wheel_Rim_L`/`Wheel_Tyre_L` and `ABS_TEST_Wheel_Rim_NoTyre` occupy the same space by design |
| static STEP output pins vs rotating hub | 169 | The motor's three output pins are one solid with the static STEP; the part fixed to the output rotates off them (design record §11) |
| output screw in static STEP output flange | 93 | Same cause, for the six output screws |
| TPU bumper designed crush | 64 | Within 3° of a stop, the 1.0 mm plug protrusion is meant to compress |
| rigid stop engaged beyond the stop angle | 8 | Only at α 49–50° and 151–152°, past the rigid stop contact |

**Stops**, bisected to 0.01°: flexion contact α = 51.00°, extension contact
α = 150.00°. Radial faces on the proximal halves and distal link; TPU Ø6 plugs
protrude 1.0 mm at R30.

**Clearances**, minimum over α 51…150° (rows in `fusion_measurements.json`):

| Pair | Minimum | Where | Rule |
|---|---:|---|---|
| Tyre to proximal link | 5.49 mm | flexion stop | ≥ 5 mm: pass |
| Rod and jam nuts to the distal knee boss | 2.80 mm | α ≤ 55° | ≥ 2 mm: pass |
| Rod group to the proximal halves | 3.70 mm | α ≥ 145° | ≥ 2 mm: pass |
| Rod group to the crank body | **1.95 mm** | extension stop | Joint-internal: the rod end pivots on the crank pin. Below the 2.0 mm general running clearance (`r2a_calc.CLR`) by 0.05 mm at the rigid stop only; see open items |
| Rod-end ball to each clevis ear | 0.20 mm | all poses | Designed axial float: 8.0 ball in an 8.4 gap |
| Crank to the proximal halves | 0.80 mm | all poses | Printed running gap |
| Distal link to proximal cheeks | 0.50 mm | α 55…145° | Printed running gap, legacy knee stack |
| Encoder arm to the proximal parts | 0.50 mm | all poses | Printed running gap |

Pin-to-pin distance is 120.000 mm in every sampled pose and the measured crank
angle equals the `r2a_calc.solve_linkage()` value to 0.001°, so the solver map
in firmware is the CAD map.

**Assembly, tool and service paths: 33 of 33 `CAD PATH VERIFIED`**
(`ASSEMBLY_VERIFICATION.md` labels). Linear paths are swept in 1 mm steps
(2 mm for the 19-part module) with a small offset along the path direction so
seated contact is not counted; tool paths use a Ø3.9 (M3) or Ø4.6 (M4)
100 mm key envelope on each screw axis. The sequence is written out in the
[R2A assembly guide](../../../docs/assembly/r2a_assembly_guide.md); the
wheel-module steps (W1…W3k, and S3w with the wheel motor and hub on the knee
module) follow the legacy order. Negative controls, all blocked as they should
be: crank pushed into the actuator (9819 mm³), knee pin pushed into its cap
(157 mm³), outboard half moved −Y into the inboard half (6620 mm³), hex key to
the actuator screws after the halves close (59.7 mm³ each: a Ø3.9 key through
the 5.0 mm inboard cheek). Informational, clear: the same key path with the
crank fitted, because the five used housing holes lie outside the crank sweep.

**Fastener engagement** (`fastener_engagement.json`; receiving depths from
[design record §2.1](../../../beni_prototype1_design_record.md) and the insert
lengths):

| Screw set | Qty | Grip | Engagement | Tip to floor |
|---|---:|---:|---:|---:|
| M3 × 10, knee actuator housing, from the channel side | 5 | 6.6 | 3.4 into the ~4.0 front thread | 0.6 to the thread end |
| M3 × 10, crank to actuator output | 6 | 5.0 | 5.0 into the 5 mm-deep output holes | **0.0** — the same screw and 5.0 mm clamp length as the assembled shoulder hub |
| M3 × 12, perimeter, outboard into inboard half | 6 | 6.6 | 5.0 (full insert) | 0.6 |
| M3 × 16, encoder bracket | 2 | 11.8 | 4.2 | 0.8 |
| M3 × 10, encoder arm to distal pads | 2 | 6.3 | 3.7 | 1.8 |
| M3 × 6, knee-pin cap | 2 | 2.9 | 3.1 | 1.9 |
| M4 × 10, inboard half to shoulder hub (legacy seat) | 6 | 3.8 | 6.2 into the 8.0 insert | — |
| M2.5 × 10, wheel motor to the distal wheel end | 6 | 8.0 | 2.0 into the Ø2.0 × 3.0 STEP holes | 1.0 |

All values in mm. Head height is taken as d (ISO 4762).

**Why two sets changed to × 10 in v5.** The knee-actuator STEP has Ø2.459 ×
4.0 mm threads at the Ø74 PCD (y 91.1…95.1) and a Ø4.5 bore behind them; the
design record §2.1 says "~4.0 mm thread … Ø6.0 through-bore between". But the
legacy delivered-actuator test found that an M3 × 10 through the 5 mm shoulder
panel (5.0 mm protrusion) bottoms before it clamps
([BOM §9 B1](../../../beni_prototype1_bom_and_assembly.md)). An M3 × 12 through
the 6.6 mm outboard cheek would protrude 5.4 mm, so the set is M3 × 10. For the
wheel motor, the STEP's six M2.5 holes are Ø2.0 × 3.0 blind (y 67.5…70.5); the
legacy M2.5 × 12 through the 8.0 mm wheel-end plate reaches y 71.5, 1.0 mm
past the floor. The legacy wheel end is otherwise unchanged; the conflict with
the legacy BOM row is listed in `PROJECT_STATUS.md`.

**Print release: 37 of 37 contracts pass; 12 files released.** Each contract
measures the diameter and Y span of a cylinder on the part's B-Rep. The print
audit classifies every downward face in the exported bed pose. Only the distal
link has faces that need support. Its five regions, the knee web (two), the
knee-receiver land, the open-channel ceiling and the wheel-end underside, each
have a Fusion support envelope with 0.4 mm top/bottom and 0.6 mm lateral gaps
and a straight removal path with zero interference. Every file passes
`mesh_fidelity()`: 0 open or non-manifold edges, 0 vertices off the reviewed
B-Rep, chord ≤ 0.004 mm. Fingerprints are pinned in
[`r2a_release_baseline.json`](../../../r2a_release_baseline.json) and checked by
`python3 verify_r2a_release.py` (also in CI).

## Traps found in this session

- **A hidden linked occurrence drops out of `Design.analyzeInterference`.** The
  three motor STEP references are linked; hidden ordinary occurrences stay in.
  A sweep run after an inspection view had hidden the REFs silently stopped
  checking the motors. `r2a_lib.sweep_chunk()` now forces every occurrence
  visible and restores the view afterwards; the sweep above was re-run that way.
- **`rig_lib.guarded()` reverts an intentional transform change.** It restores
  every captured transform, so a transform written inside the guard is undone.
  Set placement transforms after the guard, then re-run `ref_assert()`.
- **`design.snapshots.add()` followed by `computeAll()` displaced every REF.**
  Recovered with undo. R2A scripts never capture snapshots.
- **The ≤ 40 mm³ "screw in STEP thread" class can hide a screw that runs past
  a STEP hole floor.** A screw overlapping its modelled minor-diameter thread
  and 1 mm of solid beyond it still totals under 40 mm³. Screw depth is
  therefore checked explicitly by `r2a_paths_fusion.fastener_engagement()`,
  against hole spans measured on the STEP, not by the sweep.
- Occurrence bounding boxes carry a 0.01 mm pad; exact spans come from planar
  faces in assembly context.
- The knee `REF_GIM6010-8:2` carries child transforms inside its linked STEP,
  so its placement is composed on the shoulder REF's `transform2`
  (`r2a_lib.knee_ref_matrix()`). `r2a_lib.ref_assert()` adds its guard:
  Y 84.1…128.1.

## Limits

- The rod ends, rod and jam nuts are **modelled envelopes**, not a vendor part.
  The envelope is the purchasing requirement in the
  [ordering guide](../../../procurement/r2a_ordering_guide.md); a larger part has
  not been checked.
- `R2A_Encoder_Bracket_L` is modelled around a 14 × 14 × 1.6 mm board envelope
  because the AS5048A adapter-board outline is not in the repository. It is
  **on hold**, not released.
- Hardware masses are envelope volumes × density. Nothing here was weighed.
- The crank screws reach the floor of the output's 5 mm holes (above). The
  shoulder hub uses the identical stack and assembled physically, but the
  usable tapped depth is not recorded; the crank must seat flat on the output
  before any screw bottoms.
- The sweep checks interference, not stiffness, backlash or print shrinkage.
