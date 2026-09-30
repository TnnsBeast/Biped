# R2A all-printed proof of concept (POC) — CAD evidence, 2026-09-29

Fusion document **`Beni_R2A_SingleLeg`**, project Biped. The POC stand-ins
are `POC_*` components built in place by [`r2a_poc_fusion.py`](../../../r2a_poc_fusion.py),
sharing space with the purchased parts they replace (the `ABS_TEST_*`
precedent). Two configurations live in one document:

- **article**: every part except `POC_*` (the released R2A article);
- **poc**: every part except the purchased or held ones: the knee GIM6010-8
  REF, rod ends, rod, jam nuts, Ø5 × 18 pins, 6800 bearings, M2.5 × 10 screws,
  encoder bracket, AS5048A board and its M3 × 16, magnet, encoder and
  knee-actuator cable envelopes, and the Ø110 rim/tyre (the no-tyre shell and
  the tyre gauge stand in).

`r2a_poc_fusion.poc_set()` and `article_set()` define them;
`show_config()` switches the view. Saved as **v8** (2026-09-29), which shows
the article with the POC parts hidden; v7 is an intermediate checkpoint. The
evidence files were computed on the v8 geometry before that save, so they
record version 7.

Everything here is **CAD evidence**. Nothing in this folder is a physical
result. The build and the demonstration are in the
[POC guide](../../../docs/assembly/r2a_poc_guide.md); the print files and
their acceptance tests are in [`r2a_poc_stl/`](../../../r2a_poc_stl/README.md).

## Files

| File | Written by | Contents |
|---|---|---|
| [`poc_measurements.json`](poc_measurements.json) | `write_record()` | POC design values, check-point θc, clearance rows at the gate's knee angles and their minima, the tyre-to-mock clearance, rotor free-turn, sweep summaries, POC placements. Input to `r2a_calc.py` §10. |
| [`sweep_poc.json`](sweep_poc.json) | `sweep('poc', …)` | Every overlap in the POC configuration over the gate's 140 poses, classified |
| [`sweep_article.json`](sweep_article.json) | `sweep('article', …)` | The same 140 poses in the article configuration with the POC parts present in the document |
| [`fine_scan_alpha_51_150.json`](fine_scan_alpha_51_150.json) | Fusion MCP script (`pushrod_segment()`, `min_dist`) | Pushrod and tyre-gauge clearances at every whole degree, α 51…150 |
| [`assembly_paths.json`](assembly_paths.json) | `run_paths()` | 34 POC insertion, tool and service paths |
| [`assembly_path_negative_controls.json`](assembly_path_negative_controls.json) | `negative_controls()` | Four wrong moves, all blocked |
| [`lock_pin_paths.json`](lock_pin_paths.json) | `lock_paths()` | The knob lock pin at each check point (clear) and 3° of knee away from it (blocked) |
| [`fastener_engagement.json`](fastener_engagement.json) | `fastener_engagement()` | Engagement and tip-to-floor clearance of every screw set that threads into a POC part or uses a POC washer |
| [`article_paths_with_poc_present.json`](article_paths_with_poc_present.json) | `r2a_paths_fusion.run_steps()` | The article's 33 paths re-run with the POC parts in the document |
| [`release_audit.json`](release_audit.json) | `audit()` | Dimensional contracts and the print audit of all 17 released files |

## Results

**Tyre to the mock actuator at the 51° flexion stop: 8.323 mm** (Ø110 tyre
gauge) and 8.481 mm (the modelled tyre), against 8.528 mm from the modelled
tyre to the real knee actuator. The closest point is on the Ø80 housing
(R40.0, y 91.1), not on an insert boss. The governing tyre clearance is
unchanged: **5.491 mm** to the outboard half, the article's 5.49 mm, above
the 5 mm rule. The knob and pointer sit at y ≥ 116.2, outboard of the tyre
band; the nearest part other than the mock itself is the tyre gauge,
22.739 mm away at the flexion stop.

**Interference.** Both configurations were swept over the digital gate's 140
poses (knee α 49…152° in 1° steps at shoulder 0; shoulder −120…+120° in 20°
steps at α 51°, 100° and 150°), every occurrence forced visible. **0 real
clashes in each.**

| Class | POC | Article |
|---|---:|---:|
| screw in modelled STEP thread | 3220 | 4667 |
| cable envelope segments joined by construction | 140 | 420 |
| static STEP output pins vs rotating hub | 30 | 169 |
| TPU bumper designed crush | 64 | 64 |
| rigid stop engaged beyond the stop angle | 8 | 8 |
| alternative wheel parts | — | 280 |
| output screw in static STEP output flange | — | 93 |

The article counts equal the 2026-09-27 gate record exactly, so the POC parts
change nothing in the article configuration. `r2a_poc_fusion.classify()`
adds one class to `r2a_lib.classify_pair()`: the owned M2.5 × 12 in the wheel
motor's modelled STEP thread (≤ 40 mm³, as for the article's screws); its
depth is checked explicitly below.

**Clearances**, minimum over α 51…150° in 1° steps (`fine_scan_alpha_51_150.json`)
and at the gate's sampled angles (`poc_measurements.json`):

| Pair | POC | Article | Rule |
|---|---:|---:|---|
| Tyre (gauge) to the proximal link | 5.491 at α 51 | 5.49 | ≥ 5: pass |
| Pushrod rod and nut length to the distal link | 3.491 at α 51 | 2.80 | ≥ 2: pass |
| Pushrod, less its upper end, to the crank | **2.800** at α 149–150 | 1.95 | ≥ 2: pass (the article's tight spot) |
| Pushrod, less its lower end, to the lever | 3.491 at α 51 | 2.80 | ≥ 2: pass |
| Pushrod and thrust washers to the proximal halves and M4 heads | 4.337 | 3.70 | ≥ 2: pass |
| Thrust washer to the clevis ears | 0.20 | ball 0.20 | Designed float |
| Crank to the proximal halves | 0.80 | 0.80 | Printed running gap |
| Mock rotor and knob to the mock housing | 0.10 | — | Thrust gaps; journal 0.30 radial |
| Encoder arm to the protractor | 1.00 | — | Arm tip R39.0, ring R40.0 |
| Distal link, lever pin and pushrod to the protractor | 1.005 | — | |
| Wheel washers and screw heads to the wheel-cable envelope | 5.434 | — | |
| Mock actuator to the perimeter screw heads | 2.86 | — | At an insert boss |

The pushrod definitions follow `r2a_lib.gate_measurements()`: "rod and nut
length" is 27…93 mm from the crank pin, outside both 27 mm rod-end envelopes.
Pin-to-pin distance is 120.000 mm and the measured crank angle equals the
solver's in every sampled pose.

**Rejected on this evidence, before any file was released:**
- *Pushrod 8.0 mm thick* (the ball width). Its flat faces sat 1.30 mm from the
  crank's neck-relief ceiling (y 80.8) at the extension stop and 2.46 mm from
  the lever relief floor (y 70.2) at the flexion stop: the rectangle's corners
  lie outside the round nut envelope. The released pushrod is 5.0 mm thick
  (the rod's Y extent, 2.80 mm from both relief faces) with two Ø11 × 1.5
  printed thrust washers per eye taking up the ball width.
- *Mock housing with the real Ø78 land* over the first 1.0 mm. The ledge to
  Ø80, broken by the insert bosses, needed support in the bed pose; a 45°
  cone instead tessellated 0.0001 mm off the B-Rep where it met the bosses and
  failed `mesh_fidelity()`. The housing is Ø80 from the mount face.
- *Seven dial check points* (adding α 65° and 140°). Their lock holes fell
  9.0° and 4.5° of crank from their neighbours, leaving no wall between Ø4.30
  holes at R31. Five check points remain, all at least 18.7° apart.

**Deviations of the mock from the real actuator envelope**, all measured in
the sweep: five Ø9.0 insert bosses 1.5 mm proud of Ø80 over y 91.1…97.6
(a Ø4.5 receiver at R37 leaves 0.75 mm of wall inside Ø80); Ø80 instead of
Ø78 over y 91.1…92.1; the knob's pointer blade to R39.5 beyond the Ø57
driver cover, at y 116.2…128.0.

**Mock rotor.** Turned through 360° in 15° steps inside the housing with the
knob, key dowel, output dowels and knob screw: 0 overlap; minimum distance
0.10 mm (the thrust gaps).

**Lock pin.** At each check point α 55°, 80°, 100°, 120° and 145°
(θc 46.633°, 69.403°, 88.095°, 106.806°, 129.675°) the pin drops from +Y
through the knob boss into its dial hole with 0 overlap; 3° of knee away from
each it is blocked.

**Assembly, tool and service paths: 34 of 34 `CAD PATH VERIFIED`** (method of
`r2a_paths_fusion`: straight paths in 1 mm steps, 2 mm for the module; Ø3.2 /
Ø3.9 / Ø4.6 hex-key envelopes). They cover the mock sub-assembly (output
dowels, rotor, key, knob, knob screw and key), bushings, mock onto the
outboard half and its screws, crank and its screws, both pushrod eyes with
their thrust washers, caps and printed pins, the wheel-motor screws with the
printed washers, the inboard half, the whole POC knee module with the wheel
motor, the perimeter-screw key with the mock fitted, the knee pin, the
protractor and its screws, and the tyre gauge. As for the article's W1s, the
wheel-motor screw path excludes the motor, whose STEP holes are solid
modelled threads. Negative controls, all blocked: rotor into the housing from
+Y, pushrod through the crank slab, module moved inboard into the inboard
half, bushing B pushed past its lip. The article's 33 paths re-run with the
POC parts present equal the gate record.

**Fastener engagement** (`fastener_engagement.json`, all values mm):

| Screw set | Qty | Engagement | Tip to floor |
|---|---:|---:|---:|
| M3 × 10, mock mount, from the channel side (the article set) | 5 | 3.4 in a 5.0 insert | 2.6 |
| M3 × 10, crank to the mock output (the article set) | 6 | 5.0 | 1.0 |
| M3 × 10, knob to the rotor pilot | 1 | 4.3 | 2.7 |
| M3 × 10, protractor to the bracket inserts | 2 | 4.0 | 1.0 |
| M2.5 × 12 owned + 2.0 printed washer, wheel motor | 6 | 2.0 in the Ø2.0 × 3.0 STEP holes | 1.0 |

The wheel-motor stack reproduces the article's M2.5 × 10 exactly.

**Print release: 17 files**, coupons first. The contracts in `release_audit.json`
pass. The print audit finds no support face on any file: pocket ceilings
bridge ≤ 12 mm, chamfers and cones are at 45°, and the knob's counterbore
ceiling is a 1.4 mm ledge. Every file passes `mesh_fidelity()`: 0 open or
non-manifold edges, 0 vertices off the reviewed B-Rep, chord ≤ 0.005 mm.
Fingerprints are pinned in [`r2a_poc_release_baseline.json`](../../../r2a_poc_release_baseline.json).

## Traps found in this session

- **`design.computeAll()` displaces the knee REF.** Every `rig_lib.guarded()`
  call runs it, which is why the guard reports "rewrote 1 transform
  (`REF_GIM6010-8:2`)" after each build; the guard then restores it. The trap
  also reverts the appearance of base-feature bodies. Appearances for the
  renders are therefore set on the occurrences, and the knee REF is
  recomposed from the shoulder REF (`r2a_lib.add_knee_ref()`) and asserted
  afterwards (`r2a_poc_fusion.apply_looks()`, `r2a_images_fusion.apply_looks()`).
- **A 45° cone intersecting a non-coaxial cylinder** leaves tessellation
  vertices about 0.0001 mm inside the B-Rep, which fails `mesh_fidelity()`.
  Parallel-axis cylinders and coaxial cones pass.
- **Article sweeps must exclude `POC_*`.** `r2a_lib.sweep_chunk()` interferes
  every root occurrence and would report each stand-in against the part it
  replaces as a real clash. Use `r2a_poc_fusion.sweep('article', …)`.
- A timed-out MCP call is re-sent after the first run finishes, so a lock file
  plus a "skip what is done" loop lets retries continue a long sweep instead
  of duplicating it.

## Limits

- The printed stand-ins model no stiffness, friction or print shrinkage. The
  sweep checks interference only.
- The printed fits are design choices until the coupons pass
  ([`r2a_poc_stl/`](../../../r2a_poc_stl/README.md)).
- The POC validates the article's printed geometry, fits and kinematics; it
  says nothing about the purchased rod ends, the real knee actuator, loads or
  the PA-CF build.
