# Beni Prototype 1 — Production-Readiness Audit and Findings

> ### ⚠ Finding 3.9 and recommendation 7 are resolved by deletion, not by drawings
>
> **3D printed and off-the-shelf parts only, no laser cutting or machining** —
> [`MANUFACTURING_CONSTRAINTS.md`](MANUFACTURING_CONSTRAINTS.md).
>
> §3.9 ("manufacturing outputs do not exist for the machined parts") and Tier-1
> recommendation 7 ("produce real manufacturing outputs for the 10 machined
> parts") no longer apply as written: **there are no machined parts.** All ten
> families are printed, bought, or deleted. The STEP exports and
> `manufacturing/machined_parts_spec.md` were produced anyway and remain useful as
> the statement of the *fits and load cases* those parts must satisfy.
>
> Every other finding in this document stands.


> **RESOLVED 2026-08-08 — see `beni_prototype1_rev2_changes.md`.**
> Every finding in Part 3 below has been closed except §3.10 (electronics, now
> modelled but still not designed), §3.11 (actuator duty cycle, now quantified —
> the 3 g jump needs ≈5.9 N·m per leg against ~4.6–5.4 N·m rated) and §3.12
> (supplier confirmations). Five automated checks were added to `beni_lib` so
> each defect class cannot recur; `beni_lib.audit_all()` reports **0 problems**.
>
> Seven *further* defects were found during the fix work, three of them hidden by
> the way the original audits were scoped — including a stale mirror that left
> the right knee with no axle, no sleeve and no spring, a `rebuild_spring()` that
> corrupted the assembly on every pose, and a `drop_comp()` that made every
> builder non-idempotent. Those are recorded in the change document, not here.
>
> This document is kept as written, as the record of what the audit found.

**Date:** 2026-08-08
**Scope:** Full context gather across the `Biped` folder and the live Fusion
model `Biped → Beni_Prototype1`, followed by an independent audit aimed at
production readiness.
**Method:** Every number below was either re-derived from first principles in
Python or measured directly out of the open Fusion document via the Fusion MCP
(B-Rep face geometry, body volumes, per-body centroids, interference analysis,
timeline inspection). Nothing here is taken on trust from the existing
documents.

---

# Part 1 — What exists

## 1.1 The machine

A **wheeled biped** in the Mondo Robotics *Beni* serial morphology:

```
body ──▶ active rotary shoulder ──▶ proximal link ──▶ passive spring knee ──▶ distal link ──▶ driven wheel
         (GIM6010-8, ±185°)          (L1 = 120 mm)     (−8° … +27°)           (L2 = 120 mm)    (GIM4305-10, Ø110)
```

Deliberately **not** an Ascento-style parallel four-bar, not an active knee, not
telescoping. The knee is purely passive: a guided compression-spring cartridge
spanning the joint. The shoulder is the only actuated leg joint; the wheel is
independently driven.

**Envelope, measured from the model:** 182.9 (X) × 217.0 (Y) × 281.3 (Z) mm,
track 168 mm, ride height (shoulder axis to ground) 209.3 mm.

## 1.2 Files in the folder

| Path | Lines | What it is |
|---|---:|---|
| `beni_prototype1_fusion_guide_rewritten.md` | 601 | The **requirements document**. Frozen kinematics, spring targets, materials rules, 12-phase workflow, acceptance checklist, §17 freeze list. This is the spec, not the design. |
| `beni_prototype1_design_record.md` | 509 | The **as-designed record**. Verification tables, motor STEP audit, lateral layout, assumptions/deviations, load cases, defects found and fixed. |
| `beni_prototype1_bom_and_assembly.md` | 255 | BOM (per-robot), fastener schedule, mass roll-up, assembly sequence, print order. |
| `beni_lib.py` | 1742 | The **parametric build source**. Geometry helpers, kinematics closed forms, part builders, posing engine, interference harness. |
| `print_stl/` | 12 STL + README | Print-ready STLs, PLA check-prints of the metal parts, two motor stand-in gauges, a 6-bore fit coupon. |
| `web/` | viewer + 24 STL | Self-contained three.js viewer with live kinematics (`index.html`, 2 MB, geometry embedded as gzip+base64). `check.py` headless-tests the posing maths in node. |
| `CAD Imports/` | 2 STEP + 2 ASCII STEP | The supplied Steadywin motor geometry — dimensional source of truth. |

## 1.3 The Fusion model, as it actually stands

Document `Beni_Prototype1` (project `Biped`, lineage `mrn7U3LF…`):

- **156 root occurrences**, **79 components**, **815 timeline entries**
- Feature mix: 217 extrudes, 212 sketches, 212 construction planes, 11 revolves,
  **1 mirror**, 162 occurrence adds
- **31 user parameters** (`L1`, `Ru`, `Rl`, `phi_stop`, `spring_rate`, …)
- 2 external references: `REF_GIM6010-8`, `REF_GIM4305-10`, plus one mirrored
  local copy of each
- **0 joints, 0 as-built joints, 0 rigid groups, 0 snapshots, 0 named views**

Motion is produced by scripted occurrence transforms (`beni_lib.set_pose`),
not by Fusion joints. That is a deliberate, documented choice.

## 1.4 The lateral stack (left leg), frozen

Everything hangs off this table. `y` is global, `+Y` = left-outboard.

| y (mm) | Feature |
|---:|---|
| 5 … 16 | shoulder motor driver cover Ø57 |
| 17 … 41 | shoulder motor housing Ø80 |
| **42** | **housing mount face — 8 × M3 @ Ø74 PCD** |
| 42 … 47 | `Chassis_Shoulder_Plate_L`, 5 mm PA-CF, Ø96 |
| **45.5** | **output mount face — 6 × M3 @ Ø25 PCD + 3 × Ø4 pins to y = 49** |
| 45.5 … 59.5 | `Shoulder_Output_Hub_L`, 7075-T6, Ø38 body → Ø56 flange |
| 47 … 51 | clock-spring harness cavity, r = 20 … 32 |
| 51.5 … 53.5 | `Shoulder_Cable_Cover_L`, 2 mm ABS |
| **59.5** | **leg inboard face** |
| 58.7 … 64.5 | proximal arm A (5 mm + 0.8 boss); 6800 bearing 58.7 … 63.7 |
| 63.7 … 85.3 | knee steel sleeve Ø16/Ø10, double-D bore |
| **64.5 … 84.5** | **spring channel, 20.0 mm** — cartridge centred on y = 74.5 |
| 84.5 … 90.3 | proximal arm B; 6800 bearing 85.3 … 90.3 |
| **89.5** | **leg outboard face** |
| 90.3 … 93.3 | `Knee_Stop_Arc_L`, 3 mm hardened steel, two-level arc slot |
| 90.3 … 96.3 | `Knee_Magnet_Carrier_L`, magnet face at 96.3 |
| 97.3 | encoder package face — **1.00 mm** air gap |
| 59.5 … 67.5 | distal wheel-end plate, 8 mm |
| **67.5** | **wheel motor mount face — 6 × M2.5 @ Ø47.5 PCD** |
| 69 … 99 | rim + tyre, Ø110 (centre y = 84) |
| **94.5** | wheel motor output flange face |
| 94.5 … 100.5 | `Wheel_Hub_L`, 7075-T6 |

Nothing rotating crosses y = 53.5, so the chassis is free below |y| ≤ 47 —
this is why the ±185° shoulder sweep is clean by construction, not just by test.

## 1.5 Motor interface geometry (audited from the supplied STEP)

**GIM6010-8 (shoulder)** — 44.0 mm long, Ø80 housing, datum = mount face at x = 0:
- Housing mount: **8 × M3 on Ø74.0 PCD**, ~4.0 mm thread
- Output mount face at **x = +3.5**: **6 × M3 on Ø25.0 PCD × 5 mm deep**
- **3 × Ø4.0 anti-rotation pins on Ø20.4 PCD**, protruding 3.5 mm
- Ø34 pilot boss is **unusable as a register** (root fillet blends to Ø36.4,
  under 0.2 mm of straight land) — the hub locates on the three dowel pins instead
- Centre is a **0.5 mm blind recess, not a through-bore** → no central cable route

**GIM4305-10 (wheel)** — 33.0 mm long, Ø53 housing:
- Housing mount: **6 × M2.5 on Ø47.5 PCD** × ~3 mm deep
- Output flange at x = −27.0: Ø37.0 OD, **3 × M3 on Ø27.0 PCD × 4 mm deep**
- Output register only **1 mm deep** → hub centres on a Ø37.3 H8 × 0.8 counterbore

---

# Part 2 — The mechanics, verified

I re-derived the entire kinematic and force chain independently. **The core
mechanism is correct.** Every checkpoint in the guide and every table in the
design record reproduces.

## 2.1 Knee kinematics

Convention: with the proximal link fixed, `distal angle = −50° − φ`.
Nominal shoulder-to-wheel vertical = **154.269 mm**, wheel exactly below the
shoulder axis at φ = 0 (X = 0.0000).

| φ | vert. compression | fore-aft | guide (v / f-a) |
|---:|---:|---:|---|
| −8° | −12.04 | +11.63 | −12.0 / 11.6 ✓ |
| 0° | 0.00 | 0.00 | 0 / 0 ✓ |
| +5° | 8.31 | −6.37 | 8.3 / 6.4 ✓ |
| +10° | 17.13 | −12.00 | 17.1 / 12.0 ✓ |
| +15° | 26.42 | −16.83 | 26.4 / 16.8 ✓ |
| +20° | 36.09 | −20.84 | 36.1 / 20.8 ✓ |
| +25° | 46.08 | −23.99 | 46.1 / 24.0 ✓ |
| +27° | 50.14 | −25.00 | — |

## 2.2 Cartridge geometry and force

Anchors: Ru = 36, Rl = 54, included angle 110° − φ.

| φ | eye-to-eye | moment arm | spring F | wheel F | guide wheel F |
|---:|---:|---:|---:|---:|---|
| −8° | 77.70 | 22.09 | 30.0 N | 8.25 N | 8.3 ✓ |
| 0° | 74.44 | 24.54 | 64.0 N | 17.09 N | 17.2 ✓ |
| +10° | 69.91 | 27.39 | 111.4 N | 29.36 N | 29.4 ✓ |
| +20° | 64.90 | 29.95 | 163.8 N | 43.50 N | 43.6 ✓ |
| +25° | 62.23 | 31.12 | 191.6 N | 51.44 N | 51.5 ✓ |
| +27° | 61.14 | 31.56 | 203.0 N | 54.80 N | — |

Stroke −8° → +25° = **15.47 mm** (guide: 15.47 ✓). Effective wheel rate
0 → +25° = **0.745 N/mm**, inside the 0.71–0.80 band. The **rising** moment arm
(22.09 → 31.56 mm) is what makes the wheel rate progressive; this is the single
most important thing not to "simplify".

## 2.3 Spring internal budget

Pin-to-pin dead length 25.57 mm. Solid height = 11.8 coils × 2.6 = 30.68 mm.

| φ | spring length | deflection | force | margin over solid |
|---:|---:|---:|---:|---:|
| −8° | 52.13 | 2.87 | 30.0 N | 21.45 |
| 0° | 48.87 | 6.13 | 64.0 N | 18.19 |
| +25° | 36.66 | 18.34 | 191.6 N | 5.98 |
| +27° | 35.57 | 19.43 | 203.0 N | **4.89** |

The spring **cannot coil-bind before the +27° metal stop**, with 4.89 mm to
spare. Rate check: `k = G·d⁴/(8·D³·n) = 79300 × 2.6⁴/(8 × 16.4³ × 9.8)
= 10.48 N/mm` vs the 10.45 target. Preload tunable 9.1 … 30.0 N by removing
0–4 × 0.5 mm shims.

## 2.4 Hard-stop load path

Knee torque at +27° = 203.0 N × 31.56 mm = **6.408 N·m**. At the stop-pin
radius of 30 mm that is **214 N**, taken as **534 N** with a 2.5× impact
factor. Path is: Ø6 hardened dowel → steel slot end → 3 × M3 in shear →
printed boss. No thin printed tab is ever the last line of defence. Correct
by design intent.

Bumpers: 7.5 mm PU block first contacts at **φ = +20.0°** and is crushed
3.67 mm (49 %) at +27°; 3.0 mm extension block contacts at **−6.5°**, crushed
0.79 mm (26 %) at −8°. Both in open-ended bays, replaceable without touching
the bearing stack.

## 2.5 Landing energy — corrected

Energy the two passive knees absorb, φ = 0 → +27° (numerically integrated, not
trapezoid-approximated): **1.776 J per knee, 3.553 J for the pair.**

A 100 mm free drop arrives at 1.40 m/s carrying:
- 3.434 J at the 3.5 kg design mass → **0 % margin**
- 3.286 J at the **3.352 kg corrected mass** (see §3.1) → **+8 % margin**

So the drop case is marginally better than the design record states, but the
conclusion is unchanged: **the shoulder must participate.** The progressive PU
bumper adds ≈ 0.7 J per knee at the very end of travel; active shoulder
yielding has to supply the rest. No oil damper is fitted, which is the correct
Prototype-1 call.

> **[CORRECTION — 2026-08-11]** The +8% margin figure above omits m·g·Δz
> gravity work during ~50 mm of spring compression. Including it raises demand
> to **4.85 J** — a 100 mm free drop **bottoms out.** Passive free-drop
> capacity is **~49 mm** (spring-rate method). See `electronics/04_firmware.md`
> correction 3. The conclusion is stronger, not just "unchanged."

---

# Part 3 — New findings

Everything in this part is new. It was not in the design record.

## 3.1 The mass properties in the model are wrong, and there is no CoM or inertia

**Every single body in the design carries the material "Steel".** Only
appearances were assigned (`beni_lib.apply_appearances`); physical materials
were never set. Consequence:

| | value |
|---|---:|
| Fusion's own reported mass | **8174.2 g** |
| Fusion's own reported CoM | (10.78, 0.40, −69.93) mm |
| Corrected mass (densities applied by hand, per body) | **3232.2 g** modelled |
| + compute/IMU/PDB/wiring, not modelled | ~120 g |
| **Corrected robot total** | **≈ 3352 g** |
| Design mass | 3500 g |
| Margin | **≈ 148 g (4.2 %)** |

The BOM's 3304 g figure is close and essentially sound — the 48 g delta is
because `Knee_Spring_L` is modelled as its full outer *envelope* at steel
density (51.4 g modelled vs 25.3 g real spring), which over-counts by ~26 g per
leg, offset by right-leg parts missing from the model.

**Corrected CoM, computed per-body from true centroids and true densities:**

| | value |
|---|---:|
| CoM X (fore-aft, from shoulder axis) | **+11.97 mm** |
| CoM Y (lateral) | −0.17 mm |
| CoM Z | −53.60 mm |
| **CoM height above the wheel axis** | **100.7 mm** |
| Ixx (roll) | 0.0299 kg·m² |
| **Iyy (pitch — governs balance)** | **0.0208 kg·m²** |
| Izz (yaw) | 0.0144 kg·m² |
| Inverted-pendulum length | 100.7 mm → **√(L/g) = 0.101 s** |

Two things fall out of this, and both are production-critical:

1. **The CoM is 12 mm forward of the wheel contact patch at nominal stance.**
   That is a permanent standing pitch bias of 3.352 × 9.81 × 0.01197
   = **0.394 N·m**, which the wheel motors must hold continuously, or the robot
   creeps. Fix by shifting the battery and electronics aft ~12 mm — the battery
   alone (250 g of a 3.35 kg robot) needs to move about 160 mm aft to null it,
   or the chassis mass distribution needs rebalancing. Cheap to fix now,
   annoying to fix after the frame is printed.

2. **The pendulum is only 100.7 mm long.** Time constant 0.101 s. This robot is
   squat and will be twitchy — the balance controller needs a fast loop and the
   IMU placement/latency budget is tight. It is not wrong, but it is a
   consequence of putting 1000 g of shoulder motor at Z ≈ 0 and 815 g of wheel
   + wheel motor at Z ≈ −154, and it should be a conscious decision rather than
   an emergent one.

**Nothing downstream — controller, sim, URDF, Isaac/MuJoCo export — can be
built until these numbers exist in the model rather than in this document.**

## 3.2 The right leg is not a complete copy of the left

The entire right leg comes from **a single `MirrorFeature`**. Fusion's
mirror-as-new-component is not associative to features added to the source
component afterwards. Three parts and two feature sets were added after the
mirror was taken, and none propagated.

**Right-leg parts that do not exist at all** (component present, zero bodies):

| Part | Left | Right |
|---|---:|---:|
| `Knee_Axle_L` | 1 | **0** |
| `Knee_Sleeve_L` | 1 | **0** |
| `Knee_Spring_L` | 1 | **0** |

The right knee has **no axle, no sleeve, and no spring**. The right leg as
modelled cannot be built and cannot be load-analysed.

**Right-leg parts that exist but differ geometrically from the left:**

| Part | Left vol | Right vol | Δ | Missing feature |
|---|---:|---:|---:|---|
| `Proximal_Link_L(Mirror)` | 63093.07 mm³ | 70356.44 mm³ | **+7263.36** | the Ø34 root access bore (π·17²·8 = 7263.2 mm³ — exact match) |
| `Knee_Encoder_Bracket_L(Mirror)` | 2614.88 mm³ | 2726.12 mm³ | **+111.24** | the 3 × Ø5 driver-clearance holes (r = 2.5 faces: L = 3, R = 0) |

These are **exactly defects #4 and #5 from design record §11**, which were
fixed on the left and never propagated to the right. So on the right leg:

- the **six shoulder output-hub M3 screws are unreachable** — no hex key can get
  to them, and the hub is not serviceable without removing the link;
- the **three knee-stop M3 screws are covered** by the encoder bracket shelf.

`Distal_Link_L(Mirror)` was checked and is byte-identical in face signature and
volume — the divergence is limited to the two parts above.

Positionally the mirror is perfect: I verified L/R world bounding boxes for 13
part families and X/Z match to 0.000 mm with Y exactly negated in every case.
The problem is purely feature staleness, not placement.

## 3.3 The three knee-stop screw heads physically collide

`STOP_BOLT_A = (240°, 260°, 280°)` at `STOP_BOLT_R = 15.0` mm from the knee axis.

| pair | centre distance | M3 SHCS head Ø5.50 |
|---|---:|---|
| 240° ↔ 260° | 5.209 mm | **overlap 0.29 mm** |
| 260° ↔ 280° | 5.209 mm | **overlap 0.29 mm** |
| 240° ↔ 280° | 10.261 mm | clear 4.76 mm |

Fusion's interference analysis confirms it: 4 clashes (2 pairs × 2 legs) at
**1.03 mm³** each. Closed-form lens area for two Ø5.5 circles at 5.209 mm
centres × 3.0 mm head height = 1.02 mm³ — exact match.

The three screws **cannot all be fitted**. This is the fastener set that
carries the entire crash load path from the hard stop (534 N of impact shear).
The design record's driver-access audit modelled 32 hex-key envelopes and found
zero obstructions, but it never checked **head-to-head** clearance.

Minimum fix: open the angular spacing to ≥ 24° (6.25 mm centres, 0.75 mm head
gap) or move to `STOP_BOLT_R = 18` mm (6.25 mm at 20°). Either changes the arc
plate and the arm-B insert pattern. Both parts are affected on both legs.

## 3.4 The knee-stop insert bores are 0.5 mm too shallow, and the screws bottom out

| item | value |
|---|---|
| insert bore in the proximal arm-B boss | Ø4.0, y = 85.80 … 90.30 → **4.50 mm deep** |
| BOM heat-set insert | M3 brass, **5.00 mm long** → 0.50 mm too long for the bore |
| M3×8 screw seated at y = 93.30 | shank reaches y = **85.30** → 0.50 mm past the bore floor |

Confirmed by interference: `HW_SHCS_M3x8 ↔ Proximal_Link_L`, 6 clashes at
**3.53 mm³** = π × 1.5² × 0.5, exact.

Consequence: the insert stands 0.5 mm proud of the boss face, so the 3 mm steel
arc plate sits on three brass pips instead of on the printed boss; and the
screw bottoms out in the blind hole before it clamps. **The knee hard stop is
not actually fastened down.**

For contrast, the encoder-bracket inserts are correct: Ø4.0 × 5.00 mm deep,
M3×16 reaching y = 85.90, 0.60 mm clear of the floor. The bug is isolated to
the stop-arc pattern (`build_proximal_link`, the `KNEE_BOSS_B_Y1 - 4.5` cut).

The cable-cover screws show the same signature at smaller magnitude:
`HW_SHCS_M3x10 ↔ Shoulder_Cable_Cover_L`, 8 clashes at 7.07 mm³
= π × 1.5² × 1.0 → those screws run 1.0 mm past their insert bores too.

## 3.5 `beni_lib.build_all()` is not safe to run against the current model

The design record's opening line says *"Parametric build source: `beni_lib.py`
(`build_all()` reconstructs every modelled part)."* **It does not.**

**Parts in the model with no builder function anywhere in `beni_lib.py`:**

- `Chassis_Frame` (26 timeline features, 70.7 g, the part that structurally
  joins the two legs)
- `Electronics_Tray`
- `Battery_4S2200`
- `Shoulder_Cable_Spiral_L` (the harness envelope)

**And the shoulder plate has diverged from its builder.** The model's
`Chassis_Shoulder_Plate_L` carries **6 chassis-mount Ø3.4 holes** on a
rectangular grid at (X, Z) = (+30, −18), (+30, +48), (+30, +62), (−60, −18),
(−60, +48), (−60, +62), spanning y = 42 … 47. `build_shoulder_plate()` creates
**none of them** — it only cuts 8 × Ø3.4 at PCD 74, 4 × Ø3.4 at PCD 88, the Ø7
grommet and the Ø48 bore.

So calling `build_all()` today would `drop_comp('Chassis_Shoulder_Plate_L')` and
rebuild it **without the chassis interface**, silently disconnecting the two
legs from the frame, while leaving the orphaned `Chassis_Frame` in place with
its 10 now-unmatched Ø3.4 holes. The model would look fine and be unbuildable.

The build script and the model are no longer the same design. Either the
chassis builders get written and the plate builder gets its chassis holes, or
the "reproducible from source" claim has to be withdrawn — right now it is a
trap.

Related housekeeping: the timeline still contains 7 features under a component
`HW_SHCS_M3x14` that no longer exists in the assembly, and `beni_lib.PART_CLASS`
still lists `HW_SHCS_M3x14` and `HW_SHCS_M4x14` (superseded by M3x10/M4x10).
`beni_lib.ENC_PCB_Y = 97.8` with a *"1.5 mm air gap"* comment is dead code —
`build_encoder()` hard-codes 98.3 and the real gap is 1.00 mm.

## 3.6 There is not a single fillet or chamfer in the design

Timeline feature census: **217 extrudes, 11 revolves, 0 FilletFeature,
0 ChamferFeature.**

Every part is built from sharp-cornered extrusions. For the PA-CF printed
structure under impact loading, this is the highest-value structural change
available, and none of the following load-bearing re-entrant corners has a
radius:

- the root of both knee bearing bosses where they meet the fork arms
- the two ends of the 20 mm spring channel (the classic FDM crack initiation
  site — a sharp slot end in a part loaded in bending)
- the root-pad step on the proximal link (8 mm pad → 5 mm arm)
- the wheel-end plate root on the distal link (8 mm plate → 5 mm arm)
- the cartridge eye slot roots in both aluminium eyes
- every lightening-slot corner in both links

FDM parts fail at sharp internal corners, in the layer plane, long before the
nominal section stress is reached. The design record's own §5 FEA caveat
("isotropic FEA is not proof for PA-CF") is exactly right, and the mitigation
for that caveat is generous radii — which are absent.

## 3.7 The tyre has no retention and no crown

`Wheel_Tyre_L` is a **4-face plain annulus**: Ø96 ID, Ø110 OD, 30 mm wide.

- **Tyre ID Ø96.0 = rim seat OD Ø96.0.** Zero interference is modelled. As
  drawn the tyre is a free slip fit on a smooth PA-CF drum with no bead, no
  groove, no lip and no adhesive land. Under braking or a hard direction
  reversal it will rotate on the rim. A real design wants ~2 mm of stretch
  (ID Ø94) plus a retention feature.
- **No axial retention inboard.** The rim drum runs y = 69 … 104.5 and the tyre
  occupies y = 69 … 99, so there is a 5.5 mm step outboard but *nothing* at
  y = 69. The tyre can walk off inboard.
- **No crown.** A cylinder on a flat floor gives 30 mm of line contact and zero
  camber tolerance. For a balancing machine that makes lateral scrub and
  contact-point estimation worse than it needs to be; a 60–80 mm crown radius
  costs nothing.

Also: the wheel rim + tyre is **315 g of the 3352 g robot (9.4 %)** and it is
all at maximum radius, i.e. it is the dominant contributor to the wheels'
rotational inertia and therefore to how hard the balance controller has to
work. It is also the BOM's own #1 mass-reduction target.

## 3.8 Interference is genuinely clean — with one caveat worth stating

Whole-assembly analysis, coincident faces excluded, threshold 0.5 mm³:
**89 pairs, of which 88 are screw-shank-in-tap-drill modelling artifacts.**

| pair (L+R merged) | count | total mm³ | max mm³ | verdict |
|---|---:|---:|---:|---|
| motor body ↔ M3×10 | 28 | 400.72 | 16.35 | artifact (screw in motor's tapped hole) |
| M4×10 ↔ `Shoulder_Output_Hub_L` | 12 | 298.60 | 24.88 | artifact |
| M4×10 ↔ `Wheel_Hub_L` | 12 | 288.96 | 24.08 | artifact |
| motor body ↔ M2.5×12 | 12 | 122.52 | 10.21 | artifact |
| motor body ↔ M3×8 | 6 | 76.87 | 12.81 | artifact |
| M3×10 ↔ `Shoulder_Cable_Cover_L` | 8 | 56.55 | 7.07 | **real — §3.4, screw 1.0 mm past bore** |
| `Knee_Axle_L` ↔ `Knee_Magnet_Carrier_L` | 1 | 32.11 | 32.11 | artifact (M4 stud in tap drill), documented |
| M3×8 ↔ `Proximal_Link_L` | 6 | 21.21 | 3.53 | **real — §3.4, screw 0.5 mm past bore** |
| M3×8 ↔ M3×8 | 4 | 4.12 | 1.03 | **real — §3.3, screw heads collide** |

So the design record's "interference clear" claim holds for the *structure*, and
the two artifacts it documented are real artifacts. But the audit was run with
screws filtered out, and filtering the screws is exactly what hid §3.3 and
§3.4. **Three real defects were sitting in the screw-vs-part results.**

## 3.9 Manufacturing outputs do not exist for the machined parts

`print_stl/` is genuinely good work — the Ø19/Ø16/Ø10/Ø6/Ø4.05/Ø4 six-bore fit
coupon and the two motor stand-in gauges are exactly the right way to de-risk
before the motors land, and the "print this first" ordering is correct.

But there are **10 machined part families** — `Shoulder_Output_Hub_L`,
`Wheel_Hub_L`, `Cart_Upper_Eye_L`, `Cart_Lower_Eye_L`, `Knee_Axle_L`,
`Knee_Sleeve_L`, `Knee_Magnet_Carrier_L`, `Knee_Stop_Arc_L`, `Cart_Guide_Rod_L`,
`Cart_Preload_Shim_L` — and for those there is:

- **no STEP or Parasolid export** (only STL, from which no shop will quote or
  program)
- **no dimensioned drawing** (0 drawing documents in the project)
- **no tolerance callouts anywhere in CAD** — the H7/H8/h6 fits exist only as
  prose in the BOM (`Ø4.05 H7`, `Ø37.3 H8`, `Ø10 h6`, `8.40 across flats`)
- **no surface-finish, heat-treat or hardness callouts** — `Knee_Stop_Arc_L` is
  described as "hardened" with no spec, and it is the crash load path
- **no material certs called out** for the 7075-T6 or the spring steel

This is the single largest gap between "verified CAD" and "production". A
machine shop cannot start.

## 3.10 The electronics and harness are placeholders

Modelled: `Battery_4S2200` (a 77.6 cm³ rectangular block), `Electronics_Tray`
(an 8.5 cm³ flat panel), `Shoulder_Cable_Spiral_L` (a swept harness envelope).

Not modelled anywhere: compute board, IMU (and there is no defined IMU mounting
location or orientation datum — which the balance controller needs to know to
0.1°), CAN bus wiring and termination, power distribution, e-stop/kill switch,
charge port, connectors, fusing, or any chassis skin/cover. The 120 g line item
in the BOM is a placeholder for all of it.

Two specific consequences:

- **No IMU datum** means the corrected CoM and inertia of §3.1 have nowhere to
  be referenced from.
- The **encoder air gap needs re-checking against the real part.** The model
  puts the magnet face at y = 96.3 and the *package* face at 97.3 → 1.00 mm.
  But the AS5048A sensing die sits inside its package, so the true
  magnet-to-die gap will be ≈ 1.5–1.7 mm. With a Ø6 × 2.5 diametric magnet that
  is at the upper end of usable and will cost signal amplitude. The design
  record's "encoder die ↔ magnet 1.00 mm — the design air gap" line is
  measuring to the package, not the die.

## 3.11 Actuator sizing has never been checked against the duty cycle

The structure is proof-designed to 25 N·m at the shoulder, which is
conservative and correct. But **nobody has checked whether the motor can
produce the motion the design depends on.** First-order numbers:

| case | required | GIM6010-8 capability |
|---|---:|---|
| hold the leg statically (0.55 kg at ~90 mm) | 0.49 N·m | trivial |
| **drive a 3 g jump through the leg (lever ~120 mm)** | **≈ 5.9 N·m per leg** | ~4.6–5.4 N·m **rated**, 11–17.9 N·m stall |

The jump — the whole point of the passive knee — sits **right at or just above
continuous rated torque** and depends on peak/stall capability. That is
probably fine for a short impulse, but it is the design's central assumption and
it is currently unverified. It also makes the exact variant and bus voltage
(§3.12) a gating item, not a footnote.

Wheel side is comfortable:

| case | required per wheel | GIM4305-10 |
|---|---:|---|
| accelerate at 1 m/s² | 0.092 N·m | ample |
| hold the 12 mm CoM offset of §3.1 | 0.197 N·m | ample |
| 15° slope | 0.234 N·m | ample |

## 3.12 Items still genuinely blocked on outside information

Carried forward from design record §9, all still open:

1. **Exact GIM6010-8 variant, bus voltage, driver firmware, CAN and
   absolute-encoder configuration.** Now a gating item because of §3.11.
2. **Spring supplier confirmation** — Ø19 OD × 2.6 wire × 55 free × ~9.8 active
   coils, closed and ground, chrome-silicon ASTM A877/A877M, shot-peened and
   preset. Need achievable rate tolerance (±5 % assumed) and actual solid height
   (30.68 mm assumed, and the +27° margin is only 4.89 mm).
3. **PU bumper compound.** 49 % crush on the flexion bumper is at the upper end
   of sensible for ~90 A polyurethane. Bench-test tuning item.
4. **PA-CF print parameters.** All mass and section figures assume the modelled
   solid is realised. A lightly-infilled 5 mm knee arm is not the part that was
   analysed.

---

# Part 4 — What is solid, and should not be touched

It is worth being explicit about this, because the list of findings above is
long and the underlying design is good.

- **The kinematic core is correct and fully verified.** Ru/Rl/110° anchor
  geometry, the rising moment arm, the progressive wheel rate, the 154.269 mm
  nominal, the wheel directly under the shoulder — all reproduce exactly.
- **The spring cannot coil-bind before the metal stop.** 4.89 mm of margin,
  independently confirmed.
- **The 30 mm leg width is a forced consequence, not a choice**, and the
  reasoning in design record §4.1 is right: the guide's frozen anchor geometry
  fixes the minimum moment arm at 22.09 mm, which mandates a 20 mm clear
  channel, which leaves 5 mm arms — and a 6800 bearing (Ø19) needs that.
- **Locating the shoulder hub on the three Ø4 anti-rotation pins instead of the
  Ø34 pilot boss is the right call**, and the STEP evidence for it (root fillet
  blends to Ø36.4) is sound.
- **The clock-spring harness solution is correct** given the motor has no
  through-bore: r = 20 … 32 × 4 mm cavity, ~400 mm of Ø3.0 cable giving ≈ 470°
  against 370° needed, 27 % margin, strain relief on both ends.
- **The ±185° sweep is clean by construction as well as by test** — the
  Y-separation argument (all chassis within |y| ≤ 51, leg's inboard-most part
  is a body of revolution) makes the clearance rotation-invariant.
- **Assembly and disassembly logic is genuinely well thought through.** Spring
  changes with one clevis pin. Wheel motor removable with the leg assembled.
  Axle insertable only from inboard, and the sequence respects it.
- **`print_stl/` is exemplary de-risking.** The fit coupon and motor gauges let
  the whole knee and shoulder stack be dry-assembled before any motor or any
  metal arrives.
- **The web viewer is a real asset**, and `web/check.py` — headless-testing the
  posing maths in node with a stubbed three.js — is the right instinct. It
  passes: 81/81 poses, `update()` ok, all 7 groups present.

---

# Part 5 — Recommended path to production readiness

Ordered by (blocking × cheapness). Items 1–4 are all defects that make the
current model unbuildable or unfaithful; they should be closed before any new
design work.

### Tier 0 — the model is currently wrong (do these first)

1. **Rebuild the right leg from the left, properly.** Delete the single
   `MirrorFeature` output and re-mirror after all left-leg features are final,
   or better: drive both legs from `beni_lib` with a `side` parameter so they
   cannot diverge again. Recovers the missing axle, sleeve and spring, and the
   two stale parts. *(§3.2)*
2. **Fix the knee-stop screw pattern.** Open to ≥ 24° spacing or move to
   r = 18 mm. Touches `Knee_Stop_Arc_L` and the arm-B insert pattern on both
   legs. *(§3.3)*
3. **Deepen the stop-arc insert bores to 5.0 mm** (and re-check every blind
   insert bore against its insert length and screw length — the cable cover has
   the same bug at 1.0 mm). *(§3.4)*
4. **Assign real physical materials to all 79 components** so Fusion reports
   true mass, CoM and inertia. Then re-run the roll-up and publish the CoM and
   inertia tensor as model output rather than as a table in a markdown file.
   *(§3.1)*

### Tier 1 — required before anything is manufactured

5. **Reconcile `beni_lib.py` with the model.** Write `build_chassis_frame()`,
   `build_electronics_tray()`, `build_battery()`, `build_cable_spiral()`; add
   the 6 chassis-mount holes to `build_shoulder_plate()`; delete the dead
   `HW_SHCS_M3x14`/`M4x14` entries and the stale `ENC_PCB_Y`. Then prove it:
   `build_all()` into a scratch document and diff volumes against the master.
   Until that diff is clean, put a warning at the top of the design record.
   *(§3.5)*
6. **Add fillets.** Start with the spring-channel ends, both bearing-boss roots,
   and the two root-pad steps. R2–R3 where package allows, R1 minimum.
   Highest structural return of anything on this list. *(§3.6)*
7. **Produce real manufacturing outputs for the 10 machined parts:** STEP 214
   exports, dimensioned drawings with the H7/H8/h6 fits and across-flats
   tolerances actually called out, hardness spec on `Knee_Stop_Arc_L`, material
   spec on the 7075 and the spring. *(§3.9)*

### Tier 2 — design maturity

8. **Fix the tyre/rim interface:** tyre ID to Ø94 for 2 mm stretch, add a
   retention bead or groove, add an inboard lip, add a 60–80 mm crown. *(§3.7)*
9. **Rebalance for CoM.** Move the battery and electronics aft to null the
   12 mm forward offset, and decide deliberately whether 100.7 mm of pendulum
   height is what you want. *(§3.1)*
10. **Define the electronics and harness for real** — compute, IMU with a stated
    mounting datum and orientation, CAN routing, power distribution, e-stop,
    charge port, chassis skin. *(§3.10)*
11. **Verify the encoder air gap against the real AS5048A package**, not the
    package face. Consider a thicker magnet or a shorter carrier. *(§3.10)*
12. **Close the actuator question:** confirm the GIM6010-8 variant and bus
    voltage, then check the jump duty cycle against the real torque-speed curve
    rather than against the rated figure. *(§3.11, §3.12)*

### Tier 3 — the things that make it a robot rather than an assembly

13. **Add real Fusion joints with limits** (shoulder revolute ±185°, knee
    revolute −8…+27, wheel revolute) so the model is movable by someone who
    does not have `beni_lib.py`, and so joint limits are enforced by the CAD
    rather than by convention.
14. **Export a URDF/MJCF** with the corrected masses and inertias from item 4.
    This is the actual handoff to controls and sim, and it is impossible today.
15. **Extend the audit harness to catch what it missed.** `beni_lib` needs a
    fastener audit that checks head-to-head clearance, screw length vs blind
    hole depth, and insert length vs bore depth — the three checks whose absence
    produced §3.3 and §3.4 — and an L/R parity check that compares per-part
    volumes and face signatures, which would have caught §3.2 immediately.
16. **Then run the bench sequence** already correctly specified in design record
    §8: dry fit → knee stack → static sweep → spring rate on a press → static
    load 17.2/51.5/275 N → drops at 20/50/100 mm → 500-cycle cable endurance.
    No powered jump until the +27° stop is confirmed never reached at 100 mm.

---

## Summary

The **mechanism is right and the engineering reasoning behind it is sound** —
every kinematic, force, stroke, coil-bind and energy number in the existing
documents reproduces independently, and several of the non-obvious calls (dowel
location instead of the pilot boss, 30 mm leg width, clock-spring harness,
metal-backed stop path) are correct and well-argued.

What is missing is the transition from *verified geometry* to *manufacturable
product*. Concretely: the right leg is an incomplete copy, three fastener
defects would stop the build on the bench, the model has no true mass
properties and therefore no CoM or inertia for controls, the build script no
longer reproduces the model, there is not one fillet in a design that lives or
dies on FDM impact strength, and the ten machined parts have no drawings.

None of that is deep — it is all a few days of focused work, and items 1–4 are
the ones that matter most because until they are closed, every downstream
number is being computed against a model that does not describe the robot.
