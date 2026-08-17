# Beni Prototype 1 — Revision 2 Change Record

**Date:** 2026-08-08
**Scope:** Close the defects and production gaps identified in
`beni_prototype1_production_readiness_findings.md`.
**Baseline:** `snapshots/2026-08-08_pre-production-fixes/` (f3d + STEP +
metrics JSON + a named Fusion cloud version).
**Result:** `snapshots/2026-08-08_post-production-fixes/` (same set, REV2).

Everything below was verified by measurement out of the model, not by
inspection. The automated audit is `beni_lib.audit_all()`.

---

## 1. Status of every finding

| # | Finding | Status |
|---|---|---|
| 3.1 | No physical materials; no CoM or inertia | **Fixed** — §2 |
| 3.2 | Right leg an incomplete copy (3 parts missing, 2 stale) | **Fixed** — §3 |
| 3.3 | Three knee-stop screw heads physically collide | **Fixed** — §4 |
| 3.4 | Blind insert bores too shallow; screws bottom out | **Fixed** — §4 |
| 3.5 | `build_all()` would break the model | **Fixed** — §5 |
| 3.6 | Zero fillets in the whole design | **Fixed** — §6 |
| 3.7 | Tyre has no retention and no crown | **Fixed** — §7 |
| 3.8 | Interference audit hid three real defects behind a screw filter | **Fixed** — §8 |
| 3.9 | No STEP, no drawings, no tolerances for machined parts | **Fixed** — §9 |
| 3.10 | Electronics and harness are placeholders; no IMU datum | **Partly fixed** — §10 |
| 3.11 | Actuator sizing never checked against the duty cycle | **Quantified, not closed** — §11 |
| 3.12 | Items blocked on outside information | **Still open** — §11 |
| Tier 3 | Live Fusion joints | **Deliberately not done** — §12 |

**Audit result after the work:**

```
COUNTS:                  clean (72 part/side entries, 1 body each)
L/R PARITY:              clean (32 part families matched)
FASTENER HEAD CLEARANCE: clean
BLIND HOLES:             clean
SOURCE PARITY:           36 parts in model, 36 classified
TOTAL PROBLEMS:          0
```

Interference: 72 pairs, of which **70 are screw-shank-in-tap-drill modelling
artifacts** and 2 are the documented M4-stud-in-tap-drill artifact at the magnet
carrier. No structural clashes.

**Motion sweep, 22 poses** (`beni_lib.sweep_check()` — full knee range at the
shoulder nominal, full shoulder range at the knee nominal, and all four
knee/shoulder corners): **no genuine interferences.** Bumper crush reproduces
the revision-1 verified table exactly — 1.4 mm³ at φ = −8 on the extension pad,
then 2.4 / 8.6 / 12.7 mm³ on the flexion pad at φ = +22 / +25 / +27.

Kinematics re-verified after the full rebuild: the wheel axis matches the
closed-form solution to **0.0000 mm** at θ/φ = (0,0), (0,+25), (0,−8),
(−35,+12) and (+185,0).

---

## 2. Mass properties — the model now knows what it weighs

Every body carried the default "Steel". Fusion reported **8174.2 g**.

Fixed by `beni_lib.apply_materials()`, which creates design-local materials with
the right density per material class, and derives a density from the modelled
volume for the four bodies that are **envelopes rather than solids** (the spring,
the harness spiral, the battery and the electronics block).

| | before | after |
|---|---:|---:|
| Mass reported by Fusion | 8174.2 g | **3290.1 g** |
| CoM X (fore-aft) | — | **+6.46 mm** |
| CoM Y (lateral) | — | **−0.00 mm** |
| CoM height above the wheel axis | — | **103.7 mm** |
| Iyy about CoM (pitch) | — | **0.02508 kg·m²** |
| Ixx / Izz about CoM | — | 0.03214 / 0.01706 kg·m² |
| Ixz about CoM | — | +0.002759 kg·m² |
| Inverted-pendulum τ = √(L/g) | — | 0.103 s |

3290.1 g against the BOM's previous hand estimate of 3304 g, so the old
arithmetic was sound — but it lived in a markdown table, not in the model, and
there was no CoM or inertia anywhere.

**CoM Y = −0.00 mm is now a standing symmetry check.** Any part missing from one
leg shows up here immediately; it is how the missing right-hand spring in §3 was
caught after the first repair pass.

**Fore-aft offset.** The battery moved aft (centre X = −0.5 → −30.5) and the
electronics block was placed at X = −52, taking the offset from **+11.97 mm to
+6.46 mm**. It does not go to zero, and chasing it further is not worth doing:
the offset is inherent to the bent-leg geometry — the two links and the knee
hardware sit around X = +45…+92 while both wheels and both shoulder motors sit
at X = 0 — and nulling it would need ~89 mm of travel on the entire 450 g
chassis group, which does not exist in a 110 mm frame.

What that means for controls, stated plainly: the residual is a **0.21 N·m
standing bias** (0.11 N·m per wheel, trivial for the wheel actuators), and the
**equilibrium stance is a few degrees off the nominal pose** rather than exactly
on it. That is a trim term, not a defect.

Per-link masses and full inertia tensors: `sim/beni.urdf`,
`sim/beni_inertia.json`.

---

## 3. The right leg is now structurally incapable of diverging

**What was wrong.** The entire right leg came from a single `MirrorFeature`
taken early. Fusion's mirror-to-new-component is not associative, so every
left-leg edit after that point was invisible to the right leg:

- `Knee_Axle_L`, `Knee_Sleeve_L`, `Knee_Spring_L` did not exist on the right at
  all — the right knee had no axle, no sleeve and no spring;
- `Proximal_Link_L(Mirror)` was 7263.36 mm³ heavier, exactly π·17²·8, the volume
  of the Ø34 hub-access bore. The six shoulder output-hub screws were
  unreachable on the right leg;
- `Knee_Encoder_Bracket_L(Mirror)` was missing the three Ø5 driver-clearance
  holes, so the right leg's knee-stop screws were covered by the bracket shelf.

**Fix.** `beni_lib.build_mirror()` drops the old mirror and rebuilds it from the
finished left leg, and it is now the last step of every rebuild. The failure
mode was not "the mirror was wrong", it was "the mirror was taken once" — so the
fix has to be procedural, not a one-time repair.

**Second-order bug found while verifying this.** `rebuild_spring()` is called by
`set_pose()`, and it only built the left spring. So merely *posing* the model
deleted the right leg's spring and re-created the left one as default steel
(51 g instead of 25.3 g). Posing the assembly silently corrupted it. Fixed:
`rebuild_spring()` now owns **both** springs and re-applies the material, and
`Knee_Spring_L` is excluded from the mirror. Verified by a pose round-trip.

**Third bug found the same way.** `drop_comp()` deleted only the *first*
matching occurrence, which made every builder non-idempotent in two compounding
ways — placements accumulated (57 M3 × 10 screws instead of 14 after one extra
build) and, because `new_comp()` reuses a surviving component, a second call
appended a whole new body to it (the 6800 bearing became four stacked copies of
itself). `drop_comp()` now clears the component completely, and
`audit_counts()` checks both occurrence counts and one-body-per-component.

**Fourth bug, introduced by the fix to the second and caught by the motion
sweep.** Making `rebuild_spring()` build both springs at the *same* knee angle
was wrong: mirrored occurrences are treated as STATIC by `classify()`, so during
a left-leg sweep the right leg stays at nominal, and a right spring built for the
left leg's knee angle is the wrong length for the un-posed right cartridge. It
read as ~320 mm³ of interference on the right leg at every φ ≠ 0.
`rebuild_spring(phi, phi_mirror=0.0)` now takes the two angles separately.

This one is worth recording for a second reason: the interference report labelled
the clashes `Cart_Lower_Eye_L ↔ Knee_Spring_L(Mirror)`, which looks impossible
because those parts are 150 mm apart in Y. Fusion reports a mirrored occurrence
under its **source occurrence's `name`** while the *component* carries the
`(Mirror)` suffix, so the pair looked like a left-vs-right collision. The only
way to tell was to read the bounding box of the interference body itself — all
of it was at negative Y. Trust the clash volume's location, not the names.

`beni_lib.sweep_check()` now classifies known artifacts and designed contact
(bumper crush) so this class of confusion does not have to be re-litigated:
it prints real clashes only, and reports bumper crush as a positive result.

---

## 4. Fastener defects

### 4.1 Knee-stop screw heads (the crash load path)

`STOP_BOLT_A` was `(240°, 260°, 280°)` on a 15 mm radius. Centre-to-centre
2 × 15 × sin(10°) = **5.209 mm** against a **Ø5.5** M3 SHCS head: the three
heads overlapped by 0.29 mm and **could not all be fitted**. Confirmed by
interference at 1.03 mm³ per pair, which matches the closed-form lens area
exactly.

Now `(230°, 260°, 290°)` — 30° spacing, **7.765 mm** centres, 2.27 mm of gap
between heads and room for a 2.5 mm hex key on each. The arc plate grew 12° of
sector to carry the wider pattern (+2.3 g each, 2164 → 2463 mm³).

This is the fastener set that takes the entire hard-stop impact — 534 N at
r = 30 mm (214 N static × 2.5). The original driver-access audit modelled 32
hex-key envelopes and passed, because it only ever asked whether a tool could
reach a screw, never whether two screws could coexist.

### 4.2 Blind insert bores

Both blind-insert joints were wrong the same way: the bore was shallower than
the 5 mm insert, and the screw ran past the bore floor.

| joint | bore was | bore now | screw was | screw now | clearance now |
|---|---:|---:|---|---|---:|
| knee stop arc → arm B | 4.50 | **5.00** | M3 × 8 | **M3 × 6** | +2.00 mm |
| cable cover → inserts | 4.00 | **5.00** | M3 × 10 | **M3 × 8** | +2.00 mm |
| encoder bracket → arm B | 5.00 | 5.00 | M3 × 16 | M3 × 16 | +0.60 mm |

Arm B is only 5.8 mm thick at the boss, so 5.00 mm is the deepest bore that
leaves a floor (0.80 mm). That constrains the screw to M3 × 6, giving 3.0 mm of
thread into the insert — 1.0 × d, acceptable **because this joint is loaded in
shear, not pull-out**, which the design record already establishes.

Build note: the 0.80 mm blind floor means the inserts must go in with a
depth-stopped tip. Same floor as the encoder-bracket inserts, which were already
at that depth.

Both checks are now automated: `audit_fasteners()` (head-to-head clearance for
every screw pair sharing a seat plane) and `audit_blind_holes()` (bore depth vs
insert length vs screw reach).

---

## 5. `beni_lib.py` now actually reproduces the model

`build_all()` did not rebuild every part, and running it would have **silently
destroyed the chassis joint**:

- no builder existed for `Chassis_Frame`, `Electronics_Tray`, `Battery_4S2200`
  or `Shoulder_Cable_Spiral_L`;
- `build_shoulder_plate()` had drifted to a much older revision of the panel. The
  model's panel is a **rectangular lightened side panel** (−72…+42 × −24…+72,
  four lightening windows, six chassis-mount holes) with a Ø96 lobe around the
  motor. The builder made a bare Ø96 disc with no chassis holes at all.

So `build_all()` would have dropped the panel, rebuilt it without the
panel-to-frame bolt pattern, and left the frame orphaned with ten unmatched
holes — and the result would have looked fine.

All five builders were written from geometry reverse-engineered out of the
timeline, `build_all()` now ends with `add_fillets()`, and
`audit_source_parity()` checks that every modelled part has a class and vice
versa. `FRAME_BOLTS` is the single source of truth for the joint, shared by the
panel and the frame builders.

**One deliberate deletion.** The panel carried a sixth chassis hole at
(X = +30, Z = −18) with no matching boss on the frame. Giving the frame a
front-lower leg to reach it costs 19–29 g against a 210 g margin, and the
pattern is nowhere near load-limited — at the 25 N·m proof torque the worst of
the five bolts sees **82 N**. The orphan hole is deleted instead.

Also removed: the dead `HW_SHCS_M3x14` / `M4x14` entries in `PART_CLASS`, the
stale `ENC_PCB_Y` constant, and the `Chassis_Deck_Top/Bottom` placeholders that
were never modelled.

---

## 6. Fillets

The design had **0 fillet features in 815 timeline entries** — 217 sharp-cornered
extrusions. For FDM PA-CF under impact this was the single highest-return
structural change available, because printed parts crack at sharp re-entrant
corners long before the nominal section stress is reached.

**41 fillets added** by `beni_lib.add_fillets()`, which selects edges
geometrically (Y-parallel line edges of a known length for cut corners, circular
edges of a known radius and Y for boss roots) and fillets **per edge**, so a
single edge that cannot take the radius does not abort the set.

| Part | Location | Radius |
|---|---|---|
| `Proximal_Link_L` | 20 mm spring-channel corners | R2.5 → R1.0 |
| `Proximal_Link_L` | root-pad step (Ø62 disc, the M4 root-bolt clamp face) | R2.0 |
| `Proximal_Link_L` | both knee bearing-boss roots (0.8 mm steps) | R0.5 |
| `Distal_Link_L` | channel corners | R2.5 → R1.0 |
| `Distal_Link_L` | wheel-end plate root (8 mm plate off the 5 mm arm) | R2.0 |
| `Distal_Link_L` | knee boss ends (Ø16 sleeve press fit) | R1.5 |
| `Chassis_Shoulder_Plate_L` | lightening-window corners | R2.0 |
| `Chassis_Frame` | web corners | R2.0 |

Net effect on mass is small and in the right direction: proximal link
−66.65 mm³, distal link −2.99, frame −288.42.

---

## 7. Tyre and rim

As modelled the tyre was a **4-face plain annulus** whose ID (Ø96) exactly
equalled the rim seat OD. No press fit, no bead, no lip, no crown — a smooth TPU
ring on a smooth PA-CF drum that would spin under braking and walk off inboard.

Three real features added:

1. **Bead groove + rib.** Groove cut into the drum at r = 46.5 → 48 over
   y = 82.5…85.5 (centred on the tyre centre plane), with a matching internal rib
   on the tyre. Locks the tyre axially and in torsion without relying on friction.
2. **Inboard flange** on the rim, r = 48 → 52 over y = 68…69. It has to live
   outboard of y = 67.5, because that is where the distal link's Ø112 relief
   starts — inboard of it the fork arms are still full section out to r ≈ 84 from
   the wheel axis. The drum was extended inboard to y = 68 so the flange shares
   the Ø96 face rather than meeting it on an edge, which would be non-manifold.
3. **Crowned tread**, a true R150.4 torus dropping 0.75 mm from Ø110 at the
   centre plane to Ø108.5 at each edge.

The tyre stays **modelled at ID Ø96 in its installed state** so it does not read
as a permanent 8000 mm³ interference in every future audit; the **free ID is
Ø94** and that is what the BOM orders. Mass is essentially unchanged (81.5 →
80.1 g each) for three functional gains.

Implementation note: this needed a revolve about a Y axis, which the library had
no way to do — every sketch helper was Y-normal. `sk_axial_y()` / `rev_profile()`
were added, mapping points through `modelToSketchSpace` rather than assuming a
sketch orientation, and using an in-sketch construction line as the axis because
`constructionAxes.add()` raises "Environment is not supported" from a script.

---

## 8. The audit harness now catches what it missed

The original interference audit was run with screws filtered out — and §4.1 and
§4.2 were both sitting in the screw-versus-part results. Four checks added to
`beni_lib`, each because its absence let a real defect through:

| Check | Catches |
|---|---|
| `audit_counts()` | duplicate occurrences, components with more than one body |
| `audit_lr_parity()` | any L/R divergence, by per-part volume and face census |
| `audit_fasteners()` | screw heads that overlap each other |
| `audit_blind_holes()` | bore depth vs insert length vs screw reach |
| `audit_source_parity()` | modelled parts with no builder or no material class |

`audit_all()` runs the set and prints a problem count. It reports **0**.

---

## 9. Manufacturing outputs

- **`manufacturing/step/*.step`** — one STEP AP214 per machined part family, all
  ten. A shop could not previously quote or program anything, because STL was the
  only output.
- **`manufacturing/machined_parts_spec.md`** — fits, tolerances, surface finish,
  hardness and handedness for all ten, with the H7/H8/h6/n6 classes actually
  called out instead of described in prose. Includes the hardness spec on
  `Knee_Stop_Arc_L` (45 HRC through, or 50–55 HRC cased at the slot ends) that
  the BOM previously left as the word "hardened" on the final crash surface.
- **`print_stl/`** re-exported from the corrected model, including the eight
  PLA check-prints of the metal parts. The `GAUGE_*` motor stand-ins are
  untouched — they live in `Beni_Prototype1_TestGauges` and nothing here affects
  them.
- **`web/`** viewer regenerated, 27 meshes, 147 350 triangles, 0.96 MB. The
  manifest is now derived from `beni_lib.classify()` and `PART_CLASS` instead of
  being hand-maintained, so it cannot drift from the model. `web/check.py`
  passes: 81/81 poses, all seven kinematic groups present.

---

## 10. Electronics — modelled, not yet designed

`Chassis_Electronics` now exists: a 120 g block at X = −61.5…−44, Z = 0…41.5,
Y = ±25, carrying a **12 × 12 mm IMU datum pad** standing 1.5 mm proud of its
top face with its axes aligned to the robot frame. That pad is the reference the
CoM and inertia in §2 are stated against, so it needs to be a real face in the
model rather than a note.

It has to sit **aft of the shoulder motors**: both motors are Ø80 cylinders about
the Y axis spanning |y| = 5…49, so the whole region r < 40 from the shoulder axis
is motor territory at every y. The first placement attempt put the block inside
both motors (1019 mm³ of interference) and its IMU pad inside the battery —
caught by the interference re-run, not by eye.

Clearances as built: 4.00 mm to the shoulder motor, 0.50 mm to the battery.

**Still a placeholder, not a design.** There is no board outline, no connector
placement, no CAN routing or termination, no power distribution, no e-stop, no
charge port and no chassis skin. What has changed is that the 120 g now has a
location, so the mass properties are real.

**Encoder air gap — documentation was wrong, geometry was fine.** Measured:
magnet face at y = 96.30, sensor package face at 97.30, so **1.00 mm of
mechanical clearance**. The AS5048A is a TSSOP-14 about 1.0 mm thick with the die
near mid-package, so the **magnet-to-die gap is ≈1.5 mm** — inside the AMS
operating window for a Ø6 × 2.5 diametric magnet. The design record's "1.00 mm
air gap" was measuring to the package face, not the die. No geometry changed;
the claim is now stated correctly.

---

## 11. Still open

**Actuator sizing (quantified here for the first time).** The structure is
proof-designed to 25 N·m at the shoulder, which is conservative and right. But
nobody had checked whether the motor can produce the motion the design depends
on:

| case | required per leg | GIM6010-8 |
|---|---:|---|
| hold the leg statically | 0.49 N·m | trivial |
| **drive a 3 g jump through the leg (lever ≈120 mm)** | **≈5.9 N·m** | ~4.6–5.4 N·m **rated**, 11–17.9 N·m stall |

The jump — the entire point of the passive knee — sits **at or just above
continuous rated torque** and depends on peak capability. Probably fine for a
short impulse, but it is the design's central assumption and it is unverified.
It also promotes the exact-variant question from a footnote to a gating item.

Wheel side is comfortable: 0.09 N·m to accelerate at 1 m/s², 0.11 N·m to hold
the residual CoM offset, 0.23 N·m on a 15° slope.

**Landing energy, recomputed.** The two knees absorb **1.776 J each, 3.553 J for
the pair**, φ = 0 → +27° (numerically integrated). A 100 mm free drop at the
corrected 3.29 kg mass carries **3.227 J**, so there is now **+10 % margin**
rather than the ≈0 % the design record recorded against 3.5 kg. The conclusion
is unchanged: the shoulder must participate.

**Blocked on suppliers, unchanged:** exact GIM6010-8 variant / bus voltage /
driver firmware / CAN and encoder configuration; spring rate tolerance and
achieved solid height (only 4.89 mm of margin at the +27° stop); PU bumper
compound (49 % crush is at the top of sensible); PA-CF print parameters.

---

## 12. Live Fusion joints — deliberately not added

The findings document listed real joints with limits as Tier 3, to make the model
movable by someone without `beni_lib.py`. **I did not add them, and the reason is
that they would break something load-bearing.**

Posing in this project is done by writing occurrence transforms
(`beni_lib.set_pose()`), and that mechanism is what every collision sweep,
clearance table and kinematic verification in the design record runs on. Fusion
joints constrain occurrence transforms, so live joints and scripted posing cannot
coexist — adding joints would have traded a verified 0.0000 mm-accurate
verification harness for the ability to drag the model by hand.

The need is already met from two directions:

- **`sim/beni.urdf`** carries the real kinematic tree with mechanical limits
  (shoulder ±185°, knee −8°…+27°, wheel continuous) and true inertias. That is
  the handoff that actually matters, and it is machine-readable.
- **`web/index.html`** already provides interactive posing with correct
  kinematics for anyone who does not have Fusion at all.

What was added instead: the limits are now **Fusion user parameters**
(`joint_shoulder_min/max`, `joint_knee_min/max`, `joint_knee_bumper`) so they are
visible in the CAD parameter table rather than living only in convention.

If live joints are wanted later, the right move is a separate derived document,
not the master assembly.

---

## 13. What changed in the source

| File | Change |
|---|---|
| `beni_lib.py` | 1742 → ~2790 lines. Fixed `drop_comp` idempotency; added `find_all_occ`, `sk_axial_y`, `rev_profile`, `add_fillets` + edge selectors, `build_chassis_frame`, `build_electronics_tray`, `build_battery`, `build_electronics_block`, `build_cable_spiral`, `build_mirror`, `drop_mirror`, `apply_materials`, `mass_report`, `mass_by_part`, and the five `audit_*` functions. Rewrote `build_shoulder_plate`, `build_wheel`, `rebuild_spring`, `build_fasteners`. |
| `beni_export.py` | **new** — STEP per machined part, URDF + inertia JSON with a hard mass-closure check, print STL set, viewer STL set with a derived manifest. |
| `manufacturing/machined_parts_spec.md` | **new** |
| `manufacturing/step/*.step` | **new**, 10 files |
| `sim/beni.urdf`, `sim/beni_inertia.json` | **new** |
| `beni_prototype1_bom_and_assembly.md` | fastener schedule, masses, mass properties, tyre spec, assembly torques |
| `web/build.py` | `GROUP_ORDER` was missing the `wheel` group |
| `print_stl/`, `web/models/`, `web/index.html` | re-exported |

The URDF exporter has a **mass-closure assertion**: every gram in the assembly
must land in exactly one link. It caught the four cartridge clevis pins (15.2 g)
going nowhere on the first run, which is the kind of error that otherwise ships
into a controller as a slightly-too-light robot.

---

## 14. Recommended next actions

1. **Print `GAUGE_Fit_Coupon.stl` and measure all six bores.** Nothing else
   should be printed or machined first; PA-CF hole shrinkage decides whether the
   Ø19 bearing seats and Ø16 sleeve bore need to be modelled oversize.
2. **Send `manufacturing/step/` + the spec sheet out for quote.**
3. **Close the actuator question with the supplier** (§11) before any jump
   tuning, since the jump case sits at rated torque.
4. **Load `sim/beni.urdf`** and check that the balance controller is happy with
   τ = 0.103 s and a +6.46 mm standing trim.
5. **Then run the bench sequence** already specified in design record §8 —
   dry fit, knee stack, static sweep, spring rate on a press, static load at
   17.2 / 51.5 / 275 N, drops at 20 / 50 / 100 mm, 500-cycle cable endurance.
   No powered jump until the +27° stop is confirmed never reached at 100 mm.
6. **Design the electronics for real** (§10) — that is now the largest remaining
   block of unspecified work.
