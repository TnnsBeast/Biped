# Beni — wheeled biped, Prototype 1 and the single-leg test rig

A Beni-style wheeled biped: **body → active rotary shoulder → proximal link →
passive spring-loaded knee → distal link → driven wheel**, one leg per side.
Two Steadywin actuators per leg (GIM6010-8 shoulder, GIM4305-10 wheel), PA-CF
printed structure, Teensy 4.1 control.

> ## Build rule
> **3D printed and off-the-shelf parts only. No laser cutting, no machining.**
> Authoritative statement and the full list of what that changed:
> **[`MANUFACTURING_CONSTRAINTS.md`](MANUFACTURING_CONSTRAINTS.md)**

---

## Where things stand

| | Status |
|---|---|
| **Prototype 1**, two-leg robot | Modelled and verified in Fusion (`Biped → Beni_Prototype1`). 3290.1 g, `beni_lib.audit_all()` reports **0 problems**, revision 2. Not built. |
| **Single-leg test rig** | **Designed, verified, exported.** Fusion `Biped → Beni_SingleLegRig`. All six §4.4 release checks pass. Not built. |
| Electronics | Designed on paper (`electronics/`). Nothing wired. |
| Firmware | Specified, not written. |
| Physical hardware | **Nothing built yet.** The two motors are the gating purchase. |

The immediate next action is physical: **print `print_stl/GAUGE_Fit_Coupon.stl`
and the two `GAUGE_*_Motor_Interface.stl` coupons, and caliper both motors.** That
closes conflicts C2/C3/C4 and unblocks everything else.

---

## The two Fusion documents

| Document | What it is |
|---|---|
| `Beni_Prototype1` | The complete two-leg robot. **Master — do not edit casually.** |
| `Beni_SingleLegRig` | The test rig. A Save-As copy of the master with the right leg and chassis deleted and the `RIG_*` parts added. |

⚠ **In `Beni_SingleLegRig`, deleting any occurrence displaces both motor STEP
references** (the shoulder grows Y 5…49 → 5…75, the wheel motor moves 140 mm),
inventing clashes that have nothing to do with the design. Reproducible.
`isSuppressed = True` is **not** a workaround — the property is not readable on
this API build, so the assignment lands on the Python wrapper and changes nothing.
**Capture `transform2` for both `REF_*` occurrences and every child in their trees,
delete, then write them back and assert the bounding boxes.** After any structural
edit, `REF_GIM6010-8` must read Y 5.00…49.00 and `REF_GIM4305-10` Y 61.50…94.50.
Design record §6.2.

---

## Documents, in reading order

### The single-leg rig — build this first
| File | What it is |
|---|---|
| [`fusion_brief_single_leg_rig.md`](fusion_brief_single_leg_rig.md) | **The brief.** What the rig must do and why it is a dynamics rig, not a fit check. |
| [`beni_rig_no_machining.md`](beni_rig_no_machining.md) | Companion: per-part print orientations and the load arithmetic behind the routing. |
| [`beni_single_leg_rig_design_record.md`](beni_single_leg_rig_design_record.md) | **The answer.** As-built design, all six checks, mass properties, ten departures from the brief, purchase list. |
| [`rig_stl/README.md`](rig_stl/README.md) | What to print, in what orientation, and what will bite on each part. |

### Prototype 1 — the robot
| File | What it is |
|---|---|
| [`beni_prototype1_fusion_guide_rewritten.md`](beni_prototype1_fusion_guide_rewritten.md) | **Frozen kinematics** (§4–§9). Do not change without demonstrating a failure. |
| [`beni_prototype1_design_record.md`](beni_prototype1_design_record.md) | As-built record: motor interfaces measured from STEP, lateral layout, load cases, mass properties, every defect found and fixed. |
| [`beni_prototype1_bom_and_assembly.md`](beni_prototype1_bom_and_assembly.md) | BOM and assembly sequence. |
| [`beni_prototype1_rev2_changes.md`](beni_prototype1_rev2_changes.md) | The fourteen defects closed in revision 2 and how. |
| [`beni_prototype1_production_readiness_findings.md`](beni_prototype1_production_readiness_findings.md) | Audit that drove revision 2. |
| [`manufacturing/machined_parts_spec.md`](manufacturing/machined_parts_spec.md) | The ten machined families **as originally designed**. Superseded for building — see its banner. |

### Electronics
`electronics/` — power and battery, harness, compute and CAN, firmware, open
questions, logging and bring-up, BOM. Entry point:
[`electronics/README.md`](electronics/README.md). Handoff summary:
[`beni_electronics_handoff_brief.md`](beni_electronics_handoff_brief.md).

### Superseded
`beni_single_leg_rig_plan.md` — replaced by `fusion_brief_single_leg_rig.md`.
Kept as working history only.

---

## Code

Everything geometric is scripted, so the models are reproducible rather than
hand-built.

| File | Runs where | What it does |
|---|---|---|
| `beni_lib.py` | inside Fusion | Builds every part of the robot (`build_all()`, `build_mirror()`), poses it (`set_pose()`), and audits it (`audit_all()`). |
| `beni_export.py` | inside Fusion | STEP per machined part, URDF + inertia JSON with a mass-closure assert, print STLs, viewer STLs. |
| `rig_lib.py` | inside Fusion | Builds every `RIG_*` part, the §4.4 check suite (`checks_44()`), the Mode B travel harness (`slide_to()`), and an interference reporter whose names actually resolve (`real_clashes()`). |
| `rig_calc.py` | plain `python3` | Independent recomputation of the brief's arithmetic: spring curve, drop series, MGN12H moments, travel budget, mass budget, bounce mode, torque arm. |
| `rig_export.py` | inside Fusion | Rig STLs, with the print orientation recorded per part. |
| `manufacturing/stl_inspect.py` | plain `python3` | Recovers circular features from an STL mesh. Used to check the GAUGE coupons against the design record. |

Reproduce the rig model:

```python
import sys; sys.path.insert(0, '/Users/neilchulani/Fun/Robots/Biped')
import rig_lib
rig_lib.checks_44()          # the six §4.4 release checks
rig_lib.real_clashes()       # interference, artifacts classified out
```

```
python3 rig_calc.py          # every number in the design record, recomputed
```

---

## Outputs

| Directory | Contents |
|---|---|
| `rig_stl/` | Rig parts to print, plus `reroute/` — the formerly-machined parts, now printed |
| `print_stl/` | Robot parts to print, the fit coupon, the two motor gauges, PLA check prints |
| `manufacturing/step/` | STEP per part family (from when they were to be machined) |
| `sim/` | `beni.urdf` and `beni_inertia.json`, real inertias, mass closure asserted |
| `web/` | Browser viewer for posing the robot without Fusion |
| `snapshots/` | Timestamped model snapshots |
| `archive_laser/` | **Retired.** The steel stop-arc and ballast DXFs, kept only in case the two-leg build gets a laser. |

---

## Known-unresolved, and gating

| | |
|---|---|
| **C2** | Shoulder motor length, 40 vs 44 mm. **The GAUGE coupon cannot resolve this** — it is only 9.5 mm long. Caliper the motor. No structural consequence in the rig. |
| **C3** | Wheel motor length, 26 vs 33 mm. The wheel coupon is full length; hold it against the motor. |
| **C4** | Actuator masses, 388/150 vs 500/250 g. Decides whether rig ballast is 37.5 g or 149.5 g of shot. Weigh them. |
| **B1** | Wheel-driver max bus voltage unconfirmed. Run the rig at 20 V. |
| Clock spring | Highest-risk mechanical item. **Gets no validation in the rig build** — deleted for it. Moves to the two-leg build still unproven. |
| Creep | Printed joints relax silently. Re-torque after the first hour, then periodically. Inspect the printed hub's dowel holes after every drop session. |
