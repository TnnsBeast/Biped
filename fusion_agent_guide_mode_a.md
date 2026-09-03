# Fusion Agent Guide — the Mode A build

**Written 2026-08-17.** This is the CAD handoff. It exists so an agent with Fusion
access can pick up the `Beni_SingleLegRig` model and finish the **Mode A** build
without re-deriving anything and without reading five other documents first.

**There is exactly one part to design: `RIG_Stand`.** Everything else in the Mode A
part set is already modelled and verified. The stand replaces `RIG_Base` +
`RIG_Column` + `RIG_Braces` + `RIG_Carriage` — four parts collapsing into one — and
no `build_rig_stand()` exists in `rig_lib.py` yet.

**Read §1 and §6 before you open the model.** §6 describes a *reproducible* way to
silently corrupt the assembly, and it fires on operations that are house style in
this codebase.

---

## 0. What you must not do

Three rules from `CLAUDE.md` that constrain this task specifically:

1. **3D printed and off-the-shelf parts only. No laser cutting, no machining.** The
   stand is a printed part plus bought bench clamps. If a design problem seems to
   need a machined bracket, solve it another way.
2. **Never invent, recompute or round an engineering number.** Every figure in this
   guide is copied from `rig_calc.py`, the design record or the brief. If you need a
   number that is not here, get it from `rig_calc.py` — do not derive it.
3. **Prefer editing builders over hand-editing the model.** Write
   `build_rig_stand()` in `rig_lib.py`. A stand that exists only as hand-modelled
   geometry cannot be re-run, and this project's models are reproducible by design.

And one from the brief: **do not distort the design to shrink the overhang.** 42.00
mm is already 67 % of Mode B. Prefer short stiff joints over clever ones.

---

## 1. The scope decision, in one paragraph

The rig was designed with two modes. The brief's §1 says *"Mode A is Mode B with a
pin through the carriage"*: Mode A bolts the shoulder rigid for actuator
characterisation, encoder cal, CAN, latency, torque and **spring F₀/k**; Mode B puts
the shoulder on a 400 mm vertical MGN12 rail ballasted to 1.645 kg for the bounce
mode and the drop series. **The build is Mode A only.** Mode B is **deferred, not
cancelled** — every Mode B figure is retained under a `[DEFERRED — MODE B]` marker
so the slide can be built later without re-deriving it.

**Mode A still measures the spring.** Brief §6 assigns step 6 — *known masses on the
wheel, φ vs force* — to Mode A, gated on *"F₀ and k measured, replacing the assumed
30.0 N"*. This matters because the assumed 30.0 N preload is upstream of the drop
table, the force ceiling and the stop-washer count. What deferring Mode B actually
costs: the bounce mode, the sprung/unsprung split, active shoulder damping, and the
φ_peak-vs-drop-height curve that sets `A_MAX` in the hard-stop CBF.

---

## 2. `RIG_Stand` — the requirement

### 2.1 The interface, and why it is fixed

The stand's outboard face **is** the motor's front mount face at **y = 42.0**. This
is not a choice — design record §1.1 fixes it: the GIM6010-8 is tapped 8 × M3 on the
Ø74 PCD from *both* ends, and bolting to the rear face was rejected because
`GAUGE_Shoulder_Motor_Interface.stl` models only the front 9.5 mm of the motor, and
the brief requires every interface to be gated on that coupon.

```
stand outboard face = motor front mount face   y = 42.00
+ Chassis_Shoulder_Plate_L 5.0                 y = 47.00
wheel centre plane (half-track)                y = 84.00
                                               --------
Mode A overhang                                  42.00 mm   (67 % of Mode B's 63.00)
```

⚠ **Anything you put between the stand and y = 42.0 — a washer, a spacer, a printed
pad, a shim — grows the overhang and scales all four moments in §2.2 linearly.**
This is §4 check 6.

**The structural joint is `Chassis_Shoulder_Plate_L`'s five existing frame-bolt
holes**, at (X, Z) = **(−60, −18), (−60, 48), (−60, 62), (30, 48), (30, 62)** on a
**120 × 120 × 5** panel spanning X −72…48, Z −48…72, with a Ø48 central bore and a
Ø64/Ø67 cable-cavity lip standing to y = 51. Those five are what the panel uses to
carry the leg on the *real robot*, so using them makes the rig reproduce the robot's
own load path — that is the whole point, and it is why you must not add a hole to
the panel.

Two patterns on the panel you must **not** use:

- **8 × Ø3.4 on the Ø74 PCD** — that is the motor's own pattern, already occupied by
  the motor's housing screws.
- **4 × Ø4.0 on the Ø88 PCD** — the removable clock-spring cover's M3 insert
  receivers. They are driven from the accessible outboard face and are not
  stand attachment points. Leave them clear of stand geometry.

Constants already in `rig_lib.py` to reuse rather than retype:
`PANEL_FRAME_BOLTS`, `PANEL_Y0`/`PANEL_Y1` (42.0/47.0), `PANEL_X0`…`PANEL_Z1`,
`MOTOR_R` (40.0), `HALF_TRACK` (84.0),
`WHEEL_R` (55.0), `Z_WHEEL_AXIS` (−154.269), `Z_FLOOR` (−209.269).

> **[CORRECTED 2026-09-02]** `INSERT_M3_D = 4.0`, insert length is 5.0,
> and the stand hole depth is 6.0 mm. Fusion verified five receivers spanning
> y = 36…42 with a 6 mm printed floor. Physical installation remains subject
> to the owner's Ø4.0 ABS insert coupon.

### 2.2 The load set — yaw dominates by 4×

From `rig_calc.mode_a_stand()`. **The design load is the actuator's own reaction
torque, not impact** — brief §4.1 wrote that about the MGN12H and it applies verbatim
to a printed stand.

| Load | Value | Axis | Note |
|---|---:|---|---|
| Pitch — spring-limited wheel force 54.80 N × 42.00 mm | **2.30 N·m** | X | trivial |
| Roll — its ground reaction 71.3 N × 42.00 mm | **2.99 N·m** | Z | trivial |
| **Yaw — shoulder stall about the motor axis** | **11.00 N·m** | **Y** | **DOMINANT** |
| Vector sum, yaw + roll | **11.40 N·m** | — | **design against this** |
| Yaw at proof screen | **25.00 N·m** | Y | screening load |

**The stand's job is torsional, not vertical.** The static hanging load is
irrelevant by comparison: 0.8382 kg of leg (8.22 N), or 1.2262 kg with a 388 g
GIM6010-8 and 1.3382 kg with a 500 g one — about 3 % of the yaw it is sized by. This
is also why **conflict C4 (motor mass 388/150 vs 500/250 g) decides nothing
structural in Mode A**; weigh the motors anyway for the two-leg budget.

The **54.80 N** force ceiling is a property of the *spring*, not the fixture — the
knee spring is the softest element in the load path, so nothing downstream can see
more than it transmits, however hard the leg is loaded. Deleting the slide does not
raise it. (51.44 N at +25°, 16.13 N at equilibrium.)

### 2.3 The five-bolt joint carries all of it

From `rig_calc.mode_a_bolt_group()`. In Mode A there is no MGN12H block, no register
and no dowel sharing the load — five M3 in shear are the entire joint.

| | |
|---|---|
| Group centroid | **X −24.00, Z +40.40** — 47.0 mm off the motor axis, *not* on it |
| Σr² about the centroid | 14 179 mm² |
| Worst radius | 68.60 mm |
| Worst screw shear at 11.00 N·m | **53.2 N** → 2.22 MPa bearing on an 8 mm wall |
| Worst screw shear at 25.00 N·m | **121.0 N** → 5.04 MPa bearing on an 8 mm wall |

Against PA-CF's ~84 MPa XY, **bearing is not the limit**. The limit is the M3
heat-set insert's grip in printed nylon. ⚠ **That magnitude is unverified.**
Published pull-out figures for M3 brass heat-sets scatter very widely with material
and hole geometry — roughly 200–400 N in PLA at the low end, and CNC Kitchen
measured up to ~1.4 kN at the small-hole end of its range — and **none of those
tests are PA-CF at our geometry, and our load case is shear rather than axial
pull-out.** So treat the insert as the weak element and design *for* it rather than
quoting a number at it: a 5.0 mm-deep coupon-controlled pocket, real material
around the boss, and a depth-stopped installation tip.

Two consequences that should shape the geometry:

- **Spread the five landings as far as the panel allows.** Shear goes as 1/Σr², so a
  compact boss cluster is the one way to make this joint the failure point.
- **Do not model the joint as five bolts on a circle about the shoulder.** The
  centroid is 47.0 mm off-axis, so the yaw torque also tries to rotate the panel
  about that offset point.

### 2.4 It must be clamped, not weighted

This is the requirement most likely to be quietly skipped, so it gets its own
section. Hold-down needed to resist 11.00 N·m by dead weight alone:

| Base half-width | Weight needed |
|---:|---:|
| 100 mm | 110.0 N = **11.2 kg** |
| 150 mm | 73.3 N = 7.5 kg |
| 200 mm | 55.0 N = 5.6 kg |
| 250 mm | 44.0 N = 4.5 kg |
| 300 mm | 36.7 N = **3.7 kg** |

**A printed stand is ~0.3 kg.** No practical base width holds 11 N·m by dead weight.
The stand **must be clamped or bolted to the bench**, and the CAD must *show* the
clamp or bench-bolt path rather than assume it — that is new §4 check 7.

Design in explicit clamp landings: flat, parallel, accessible from above and below,
at least two per side, sized for a common F-clamp or bar-clamp jaw. For reference, an
Irwin Quick-Grip medium-duty one-handed bar clamp is rated up to **300 lbf** of
sustained force and the heavy-duty version up to **600 lbf**, so clamp *capacity* is
not the constraint — the constraint is whether your geometry gives the jaw something
square to bite on, and whether the printed landing crushes under it. Add bench clamps
to the purchase list; the Mode A build needs **more** of them than Mode B did.

### 2.5 Height, and the floor

The stand must hold the shoulder axis **≥ 221.31 mm** above the floor plate. That is
the ride height at the −8° extension stop, which is where a free leg actually rests:

| Knee angle | Shoulder axis above floor |
|---|---:|
| −8°, the extension stop | **221.31 mm** |
| 0°, the modelled pose | 209.27 mm |
| +25°, the design point | 163.19 mm |
| +27°, against the stop | 159.13 mm |

`RIG_Floor_Plate` (260 × 60 × 6) stays: it is what the wheel rests on, and it is
what stops the leg falling when the shoulder is de-energised. A 6 mm aluminium plate
is the better part if one is available — the wheel rolls ~77 mm during a shoulder
sweep, and if it scrubs, every force reading is corrupt.

Related figure, for step 6: **the preload floor is 8.25 N.** Below that a free leg
just rests on the −8° stop, so the threshold to watch during loading is φ leaving
the stop, not a force reading.

### 2.6 Print orientation

Per `beni_rig_no_machining.md` §1: **5 walls · 40 % gyroid · 0.15 mm layers ·
top-of-range temp · minimal cooling · dried filament.** PA-CF is 84–102 MPa in XY
and only 26–50 MPa in Z, so **orientation is the strength lever and infill is not.**

For the stand specifically: **the dominant load is torsion, not bending.** Keep the
11.00 N·m yaw path in the print plane; do not let it try to peel layers apart. State
the chosen orientation in the builder's docstring and in `rig_stl/README.md` §9,
which already has a placeholder entry for this part.

`beni_rig_no_machining.md` §3 also flags the measurement consequence: **the stand is
now the softest element in the load path**, and its deflection shows up as shoulder
*angle* error, not knee error — a different and more insidious artifact than the old
2020 column's bending. Stiffness here is measurement quality.

---

## 3. The Mode A part set

Five families, of which four already exist:

| Part | Status |
|---|---|
| **`RIG_Stand`** | **TO DESIGN.** No builder exists. |
| `RIG_Torque_Arm` | Exists — `build_rig_torque_arm()`. 200 mm lever on the hub's 6 × M4 Ø44 PCD, bearing on a 5 kg kitchen scale. Highest-value cheap part in the rig: published bench tests of this actuator found 4.8 and 9.4 N·m against an 11 N·m rating, and the jump needs 5.9 N·m = **3.01 kgf at 200 mm**. Re-run check 5 against the *stand*. |
| `RIG_Floor_Plate` | Exists — `build_rig_floor()`. Unchanged. |
| `RIG_Cable_Post_A` / `_B` | Exist. Post A is unchanged (clamped under two of the motor's eight M3 housing screws, which become **M3 × 16** for that reason, capped at y = 57 so the proximal link at 58.7 can sweep over). **Post B needs rework**: it currently mounts to the column T-slot above the carriage's travel, and there is no column. Re-route it to the stand — the routing is simpler now, with only the wheel and the stand to clear. |
| `RIG_Knee_Stop_Plate_L` | Exists — `build_rig_knee_stop_plate()`. Still required: it carries the **−8° extension stop**, which a free leg rests on in every unloaded pose. |

**Deferred with Mode B — do not build, do not delete the builders:**
`build_rig_base`, `build_rig_column`, `build_rig_braces`, `build_rig_rail`,
`build_rig_blocks`, `build_rig_carriage`, `build_rig_index_post`,
`build_rig_index_bar`, `build_rig_mode_pin`, `build_rig_bumpers`,
`build_rig_ballast`, `build_rig_ballast_pot`, and the `check3_mode_b_travel()` /
`slide_to()` harness.

**Also deferred:** the **+27° washer-column stop** inside the spring cartridge.
Steps 1–9 never approach +27°, so Mode A never needs it — but it is **mandatory
before any drop**, and its shim is meant to be set *after* step 6 from the measured
spring, where one 1.0 mm washer moves the stop by 1.83°.

Reused unchanged, all robot parts and all unaffected by the Mode A cut:
`Proximal_Link_L`, `Wheel_Rim_L`, `Wheel_Tyre_L` (TPU 95A), `Knee_Encoder_Bracket_L`
(ABS), `Chassis_Shoulder_Plate_L`, the knee bearings, the cartridge and the spring.
Reused **modified**: `Distal_Link_L` — its Ø16 sleeve bore is now Ø10 (design record
§4), and `rig_stl/reroute/Distal_Link_L.stl` supersedes the `print_stl/` copy.

When you add the builder, also add `'RIG_Stand': 'PACF'` to `RIG_PART_CLASS` in
`rig_lib.py`, or its mass will not be counted.

---

## 4. Checks before you release CAD

Brief §4.4, Mode A set: six checks become four, plus two replacements and one new.

| # | Check | Status |
|---|---|---|
| 1 | Knee sweep −8° → +27° at nominal shoulder reproduces guide §4: **φ = +25° → 46.1 mm vertical, 24.0 mm fore-aft.** | **Unchanged** — `check1_knee_sweep()`. A mismatch means your model is wrong, not the table. |
| 2 | Shoulder sweep ±120°; the service loop must not foul the stand or the wheel. | **Unchanged in intent** — `check2_shoulder_sweep()`. Rail, column and carriage leave the exclusion list; the stand joins it. |
| 3 | Wheel clears the floor plate at **every knee angle −8° → +27°** with the stand at its designed height. | **Replaced.** Was "through the whole Mode B travel". Now a knee-sweep check, and trivial in Mode A because the wheel is *on* the floor and the stand does not move. |
| 4 | Mass properties. | **Replaced.** `slide_mass()` / `sprung_split()` are Mode B. Do the §2.2 Mode A load report instead — `rig_calc.mode_a_stand()`. |
| 5 | Torque arm cannot hit the stand at any angle you intend to load. | **Re-run.** It passed against the column with Y bands disjoint by 38.5 mm; **the stand's Y bands are different.** Arm max radius is 200.4 mm against 209.3 mm to the floor. |
| 6 | Verify the **42.00 mm** Mode A overhang. | **Replaced.** Was "re-verify the 63 mm stack-up". Assert the stand's outboard face lands exactly on y = 42.0. |
| **7** | **Prove the hold-down.** | **NEW, Mode A only.** 11.00 N·m of yaw cannot be resisted by dead weight. The CAD must show the clamp or bench-bolt path. |

Update `checks_44()` accordingly — do not leave it calling `check3_mode_b_travel()`
and `check6_stackup()`, whose assert is hard-coded to 63.0, in a Mode A build.

Also carry forward, from §6.1 of the design record: `RIG_Torque_Arm ↔
Proximal_Link_L` is an **intentional** clash — the arm *replaces* the proximal link
on the hub's 6 × M4 Ø44 PCD, and step 2 runs with the leg off. It and
`RIG_Scale_Pedestal` are `STEP2_FIXTURES` and are excluded from the sweeps. With the
pedestal fitted, keep the shoulder within **−120…+25°**.

---

## 5. Deliverables

1. Fusion assembly, **Mode A only**, reused parts in place, checks 1/2/3/5/6 plus
   the new hold-down check verified.
2. `build_rig_stand()` in `rig_lib.py`, with its orientation and reasoning in the
   docstring, and `RIG_Stand` registered in `RIG_PART_CLASS`.
3. STLs for `RIG_Stand`, `RIG_Torque_Arm`, `RIG_Floor_Plate`, `RIG_Cable_Post_A/B`,
   `RIG_Knee_Stop_Plate_L` and the five re-routed formerly-machined parts, with
   print orientation stated per part. **No carriage, no ballast pot, no index bar.**
4. A **Mode A load report** — the numbers in §2.2/§2.3 confirmed against the built
   assembly, not against this document.
5. **A snapshot of the verified rig assembly.** `Beni_Prototype1` has two entries in
   `snapshots/`; `Beni_SingleLegRig` has none, despite being the active build and
   despite §6 documenting a reproducible way to corrupt it. This is the
   highest-value missing artifact in the project — do not skip it.
6. The design record §2.3 **dowel-pin recommendation survives intact**:
   `Shoulder_Output_Hub_L` needs its three Ø4 × 10 hardened dowel pins. The
   printed register alone sees 63 MPa at the 25 N·m proof load against PA-CF's
   ~40–50 MPa shear. **The pins are not optional, but machining is prohibited:**
   structural release now waits for an as-printed PA-CF press-fit coupon; revise
   the printed retention geometry if no coupon bore works.

---

## 6. ⚠ Traps that produce *passing* wrong answers

All five are from design record §6.2, recorded because each one silently produced a
passing result that was wrong. Trap 1 is the one that will cost you a day.

### 6.1 Deleting *any* occurrence displaces both motor STEP references

**Reproducible in `Beni_SingleLegRig`** — it fired twice on the same delete. Removing
one stray M3 screw re-resolved the two external STEP references: `REF_GIM6010-8` grew
from Y 5…49 to **Y 5…75**, and the wheel motor moved **140 mm**, inventing clashes
that had nothing to do with the design.

Two dead ends already tried, so do not repeat them:

- **`occurrence.isSuppressed = True` is not a fix.** The property is not readable on
  this API build, so the assignment lands silently on the Python wrapper and changes
  nothing in the model. It *looks* like it worked.
- **You cannot simply ban the operation.** `beni_lib.build_fasteners()` deletes its
  own origin master occurrences the same way — it is house style.

**What works:** capture `transform2.asArray()` for both `REF_*` occurrences **and
every child occurrence in their trees** (7 transforms), do the delete, then write the
transforms back and assert the bounding boxes. Undo also recovers it cleanly if you
catch it immediately.

**After any structural edit, assert both boxes:**

```
REF_GIM6010-8    must read  Y  5.00 … 49.00
REF_GIM4305-10   must read  Y 61.50 … 94.50
```

### 6.2 The other four

2. **`beni_lib.interference()` reports unresolvable names.** It falls back to
   `entity.name`, which for any body built without renaming is `"Body1"`. Every rig
   clash came back as `Body1 ↔ Body2`, a filter on `'RIG_'` matched nothing, and the
   first four builds reported **zero interference when there were 49 pairs** —
   including an 11 313 mm³ brace-through-post collision. **Use
   `rig_lib.real_clashes()`**, which resolves through `assemblyContext` then
   `parentComponent`.
3. **Fusion's occurrence bounding box inflates under rotation.** It is the
   axis-aligned box of the *untransformed* box, so at φ = +25° the Ø110 tyre reports
   as **146.2 mm** tall (110 × (cos 25 + sin 25)). Any clearance read off `bbox`
   min/max for a rotated part is overstated by up to a third. **The box *centre*
   transforms exactly** — that is why `wheel_bottom()` takes centre − 55.
4. **`Sketch.saveAsDXF` after `projectCutEdges` mirrored the hole pattern.** It
   wrote the outline at (+X, −Z) and the holes at (−X, −Z), 183 mm apart. No longer
   affects a deliverable — there are no laser parts — but it means Fusion's DXF
   export cannot be trusted without an independent area check.
5. **The spring cartridge's internal length is 9.0 mm shorter than its own dimension
   chain implies.** Deriving it instead of measuring it would have put the knee's
   hard stop at +10°. **Measure, don't derive.**

### 6.3 Two more from the conventions list

- **Chirality.** Only left-hand (`_L`) parts are modelled and exported; mirror in the
  slicer. Fusion reports a mirrored occurrence under its *source* occurrence's `name`
  while the component carries the `(Mirror)` suffix — **trust the clash volume's
  bounding box, not the names.**
- **`Beni_Prototype1` is the master.** The rig is a Save-As copy. Do not edit the
  master casually, and do not propagate a rig-only change into it.

---

## 7. Where the rest of it lives

| What | Where |
|---|---|
| Every Mode A number, recomputable | `rig_calc.py` → `mode_a_stand()`, `mode_a_bolt_group()` |
| The brief, amended for Mode A | `fusion_brief_single_leg_rig.md` — §3 part table, §4.1 loads, §4.4 checks, §6 test steps, §7 deliverables |
| As-built rig record | `beni_single_leg_rig_design_record.md` — §1.1 front-face decision, §2.2 panel interface, §2.3 stack-up and moments, §6.2 traps, §9 purchase list |
| Print settings and the compliance warning | `beni_rig_no_machining.md` §1, §3 |
| What to print and in what orientation | `rig_stl/README.md` |
| The manufacturing rule | `MANUFACTURING_CONSTRAINTS.md` |
| Electronics for the Mode A rig (~$25) | `electronics/07_bom.md` Wave 0 |
| Bring-up gates | `electronics/06_logging_and_bringup.md` Stages 0–2 |
| Working rules for this repo | `CLAUDE.md` |

Reproduce the current state:

```python
import sys; sys.path.insert(0, '/Users/neilchulani/Robots/Biped')
import rig_lib
rig_lib.checks_44()          # eight Mode A checks, including receivers
rig_lib.real_clashes()
```

```
python3 -c "import rig_calc; rig_calc.mode_a_stand(); rig_calc.mode_a_bolt_group()"
```

---

## 8. The honest summary

The Mode A cut trades one deferred measurement set — bounce mode, sprung/unsprung
split, shoulder damping, and the φ_peak curve that sets `A_MAX` — for eight fewer
`RIG_*` parts and ~$60 less linear motion, and it keeps the spring characterisation
that everything downstream is computed from.

What it does **not** do is de-risk the drop question. Both the energy method and the
spring-rate method say a 100 mm drop bottoms the knee out; the passive limit is
**45 mm** planning / 46.3 mm at the +24° gate crossing. Deferring step 10 means the
two-leg build inherits that unanswered, **alongside the clock spring**. Step 6's
measured curve at least lets you predict it honestly before committing to the robot.

⚠ And one standing discipline item, because it is easy to forget on a bench: **the
brake chopper is deferred with Mode B, so nothing may backdrive a motor.** A bench
PSU cannot sink regen — it will just let the bus rise. No hand-spinning the wheel
under power, no dropping the leg off the stand, no using the wheel motor as a brake.
