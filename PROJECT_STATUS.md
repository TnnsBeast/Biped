# Beni project status and working guide

This is the working entry point for the project: current build state, immediate
actions, release gates, CAD hazards, authoritative documents, and reproduction
commands. For the public project overview and active print download, see
[`README.md`](README.md). Before changing the project, read
[`CLAUDE.md`](CLAUDE.md).

## Where things stand

> **Current scope decision, 2026-09-02 — complete the single-leg integration
> article in ABS; defer PA-CF to the two-leg structural build.** The active leg
> may be fully dry-assembled, hand-posed, wired, and commissioned with both
> motors under current limits while the wheel is clear and the printed path
> carries self-weight only. The main spring stays unloaded, and torque-arm,
> spring-characterisation, ground-traction, stall/proof, drop and human-adjacent
> tests are deferred with PA-CF. This supersedes the earlier plan to take Mode A
> step-6 spring data before the two-leg build.
>
> **Fixture scope remains Mode A only.** The shoulder-to-stand geometry remains
> useful for assembly and unloaded integration. The vertical MGN12 slide,
> ballast, index bar, mode pin, bumpers and drop series remain **deferred, not
> cancelled**. The CAD handoff is
> [`fusion_agent_guide_mode_a.md`](fusion_agent_guide_mode_a.md).

| | Status |
|---|---|
| **Prototype 1**, two-leg robot | Modelled, saved and verified in Fusion (`Biped → Beni_Prototype1`). `beni_lib.audit_all()` reports **0 problems**, including 6 shoulder M4, 6 wheel M4, 4 shoulder-plate M3, 5 proximal M3 and 10 chassis-frame M3 receivers. Revision 2; not built. |
| **Single-leg test rig, Mode B** | **[DEFERRED]** — not the build. Its source now has five Ø4.0 × 6.0 M3 and four Ø5.6 × 7.2 M4 carriage pockets; an isolated Fusion build verified all nine. |
| **Single-leg integration article / Mode A fixture** | **This is the active build, entirely in ABS.** `RIG_Stand` and the rear-face `RIG_Cable_Anchor_ModeA` are modelled and saved. The eight Mode A checks, including the added threaded-receiver audit, pass. The stand now has five Ø4.0 × 6.0 M3 pockets and zero fastener/stand interference. It remains an assembly/unloaded commissioning fixture; its measurement and structural-load programme is deferred. |
| Electronics | Designed on paper (`electronics/`). Nothing wired. Mode A cuts Wave 0 to **~$25** plus a bench PSU. |
| Firmware | Stage 0 bench scaffold implemented and compile-verified for Teensy 4.1 in [`firmware/teensy_stage0/`](firmware/teensy_stage0/). It has no actuator command path; hardware gates remain unrun. |
| Physical hardware | **Both actuators and the 6800-2RS bearings are in hand.** Photo evidence: [`evidence/actuators/2026-08-20_received/`](evidence/actuators/2026-08-20_received/). The owner reports that an AliExpress spring arrived at **150 mm free length** on 2026-09-01. That is not the Ø19 × 2.6 × **55 mm free** knee spring specified in the BOM and RFQ; do not install or trim it into the cartridge. The ABS actuator-interface results are: GIM6010 housing PASS, original GIM6010 output Ø4.05 bore clearance FAIL followed by Ø4.15 ABS PASS, GIM4305 housing PASS with the real M2.5 screws, and GIM4305 output PASS. The already-printed Ø4.15 shoulder hub remains valid motor-fit evidence but its legacy link holes make it unusable for assembly; **reprint the corrected Ø4.15 hub** after obtaining/couponing six `SL-B-M4-5.8` inserts. Continue using M3 × 8 for the eight housing screws because ×10 bottoms before clamping. The face-flat Ø19.10 ABS proximal link has accepted both real bearings and remains the build article; do not reprint it. Ø19.15 is only the future ABS preference. Evidence: [`evidence/knee_fit/2026-09-02_proximal_link_full_depth/`](evidence/knee_fit/2026-09-02_proximal_link_full_depth/). On 2026-09-02 the owner reported an eBay knee-pin order, believed to be a set of three, with delivery expected in roughly two weeks or later. The listing, quantity and h6/h5 tolerance evidence remain unverified. Voron-style M3 inserts plus photographed assortments are in hand; exact AliExpress dimensions still require the existing Ø4.0 ABS coupon. The short PSM M4 inserts are not in hand. No complete leg or wiring has been assembled yet. |

The face-flat Ø19.10 first article is the physical ABS proximal link now in use;
do not reprint it merely to adopt the easier Ø19.15 preference. The scripted
default is Ø19.15 for a future ABS export, but no replacement STL has been
generated because no replacement is needed. The saved master retains Ø19.10;
the compensation is intentionally an ABS first-article override rather than a
two-leg PA-CF design dimension.

The 2026-09-02 insert redesign is complete in source, both saved Fusion
documents, and the print exports. The active receiver map is: four Voron-style
M3 inserts in `Chassis_Shoulder_Plate_L`, five in the existing proximal link,
five in `RIG_Stand`, six PSM Sonic-Lok `SL-B-M4-5.8` in the corrected shoulder
hub, and six `SL-B-M4-4.8` in `Wheel_Hub_L`. The cable cover is now a clearance
part fastened from the accessible outboard face; this removed four screw-head
clashes with the stand. The future chassis frame and deferred Mode-B carriage
are also corrected and Fusion-verified. The optional M2 satellite-PCB boss
remains an open architecture decision, not a missing receiver on an existing
part. Exact sizes, pocket depths, fasteners and physical coupon gates are in
[`MANUFACTURING_CONSTRAINTS.md`](MANUFACTURING_CONSTRAINTS.md#threaded-interfaces-in-printed-parts).

The only mandatory reprint from the owner's reported physical progress is the
**shoulder hub**. Keep the Ø19.10 proximal link and both installed bearings.
The stand, wheel hub, shoulder plate and cable cover were not reported printed;
when their turn comes, use only the new `_PRINT_ORIENTED` release files listed
in [`first_article_stl/heatset_receiver_release_manifest.json`](first_article_stl/heatset_receiver_release_manifest.json).

The immediate mechanical gate is the owner-reported eBay knee-pin order. It is
believed to contain three candidate pins and is not expected before about
2026-09-16; treat both facts as unverified until the listing or package is
recorded. On arrival, count the pins, confirm Ø10 × 35 mm and h6/h5 evidence,
hand-fit one through both 6800 bearing bores, and test the vertical Ø10
fit-coupon bore. That real steel-pin result plus the final Fusion support/bridge
and assembly-path audit gate a new bed-ready ABS `Distal_Link_L`.

A deliberately clearance-fit printed ABS pin may be used meanwhile as a
**supported, hand-posed alignment mandrel only**. It does not release the distal
link, prove the bearing fit, or establish the AS5048A angular datum. Do not use a
printed pin for powered motion, main-spring installation/preload, ground contact
or any load test; support the distal-side mock-up so the pin carries no leg
weight. No temporary-pin STL is released yet. In parallel, run
firmware/electronics Stage 0 with both motors disconnected. See the exact bore map in
[`print_stl/README.md`](print_stl/README.md). The GIM4305 procedure and
non-nesting explanation are in the illustrated
[`2026-08-22 actuator-coupon test guide`](evidence/actuator_fit/2026-08-22_coupon_test_guide/README.md).
They were built from the manufacturer STEP datums in Fusion and are ready to use
with the real actuators as go/no-go fixtures, so calipers are **not a blocker**.
The old `GAUGE_*_Motor_Interface.stl` files remain positive motor stand-ins and
are not substitutes for these mating coupons. The optional Mode A cable anchor
is in `first_article_stl/mode_a/`. PA-CF coupons and structural prints are now
deferred to the later two-leg build.

---

## The active Fusion documents

| Document | What it is |
|---|---|
| `Beni_Prototype1` | The complete two-leg robot. **Master — do not edit casually.** |
| `Beni_SingleLegRig` | The test rig. A Save-As copy of the master with the right leg and chassis deleted and the `RIG_*` parts added. |
| `Beni_Prototype1_TestGauges` | Fit gauges and the four ABS actuator-interface coupons. |

⚠ **In `Beni_SingleLegRig`, deleting any occurrence displaces both motor STEP
references** (the shoulder grows Y 5…49 → 5…75, the wheel motor moves 140 mm),
inventing clashes that have nothing to do with the design. Reproducible.
`isSuppressed = True` is **not** a workaround — the property is not readable on
this API build, so the assignment lands on the Python wrapper and changes nothing.
**Capture `transform2` for both `REF_*` occurrences and every child in their trees,
delete, then write them back and assert the bounding boxes.** After any structural
edit, `REF_GIM6010-8` must read Y 5.00…49.00 and `REF_GIM4305-10` Y 61.50…94.50.
Rig design record §6.2.

---

## Documents, in reading order

### The single-leg rig — build this first
| File | What it is |
|---|---|
| [`fusion_agent_guide_mode_a.md`](fusion_agent_guide_mode_a.md) | **The CAD handoff for the Mode A build.** Everything a Fusion agent needs to model `RIG_Stand` and the reduced part set: verified load table, the 42.00 mm overhang, the mount interface, the check list, and the model-corrupting traps. Read this before touching the model. |
| [`docs/assembly/shoulder_to_proximal_link.md`](docs/assembly/shoulder_to_proximal_link.md) | **Picture dry-fit guide.** Shows the verified plate-first, hub-second GIM6010 sequence and how the printed proximal link attaches to the shoulder hub. |
| [`docs/assembly/heatset_receiver_map.md`](docs/assembly/heatset_receiver_map.md) | **Picture insert map.** Shows every active receiver/clearance part, install direction, screw length, and corrected bed-ready STL. |
| [`ASSEMBLY_VERIFICATION.md`](ASSEMBLY_VERIFICATION.md) | **The physical-assembly release gate.** Required insertion-order/path, tool access, cable path, service path, and first-article rehearsal checks. |
| [`fusion_brief_single_leg_rig.md`](fusion_brief_single_leg_rig.md) | **The brief.** What the rig must do and why it is a dynamics rig, not a fit check. Amended 2026-08-17 for Mode A. |
| [`beni_single_leg_rig_design_record.md`](beni_single_leg_rig_design_record.md) | **The answer, and the authoritative rig document.** As-built design, all six checks, mass properties, eleven departures from the brief, purchase list. **§6.2's five measurement traps are the most reusable content in the project.** Mode B sections carry `[DEFERRED]` banners; the leg content is unaffected. |
| [`beni_rig_no_machining.md`](beni_rig_no_machining.md) | Companion: the canonical PA-CF print settings with per-setting reasoning, and the load arithmetic behind the printed-part routing. |
| [`rig_stl/README.md`](rig_stl/README.md) | What to print, in what orientation, and what will bite on each part. |

### Prototype 1 — the robot
| File | What it is |
|---|---|
| [`beni_prototype1_fusion_guide_rewritten.md`](beni_prototype1_fusion_guide_rewritten.md) | **Frozen kinematics** (§4–§9) and the requirements freeze. Do not change without demonstrating a failure. |
| [`beni_prototype1_design_record.md`](beni_prototype1_design_record.md) | As-built record: motor interfaces measured from STEP (§2), the authoritative lateral Y-stack (§3), load cases, mass properties (§14). |
| [`beni_prototype1_bom_and_assembly.md`](beni_prototype1_bom_and_assembly.md) | BOM, fastener schedule, and the assembly sequence with torques. |
| [`beni_prototype1_rev2_changes.md`](beni_prototype1_rev2_changes.md) | The fourteen defects closed in revision 2, and the Fusion/scripting failure modes found doing it. |

### Electronics
`electronics/` — power and battery, harness, compute and CAN, firmware, open
questions, logging and bring-up, BOM. Entry point:
[`electronics/README.md`](electronics/README.md). The CAD-derived geometry every
other electronics document is designed against — coordinate frame, inertia table,
free-space map, spring table — is
[`electronics/00_mechanical_datum.md`](electronics/00_mechanical_datum.md).

**`electronics/01`–`06` describe the two-leg robot**, which is not the active
build. Each carries a carve-out noting what the rig deletes (no pack, no BMS, no
custom PCB, no satellite nodes, no clock springs — a Teensy 4.1 on a 20 V bench
supply). `electronics/07_bom.md` Wave 0 is the rig's electronics shopping list.

### Archive
`archive/` — kept for provenance, not for building.

| | |
|---|---|
| [`archive/prototype1_production_readiness_audit.md`](archive/prototype1_production_readiness_audit.md) | The audit that drove revision 2, condensed. Its mass figures are superseded — the file says so. |
| `archive/manufacturing/` | The ten machined families **as originally designed**, with the fits and tolerances the printed substitutes must still meet. |
| `archive/laser/` | **Retired.** The steel stop-arc and ballast DXFs. `stop_arc_loops.json` is the only surviving source for the stop-arc profile. |

---

## Code

Everything geometric is scripted, so the models are reproducible rather than
hand-built.

| File | Runs where | What it does |
|---|---|---|
| `beni_lib.py` | inside Fusion | Builds every part of the robot (`build_all()`, `build_mirror()`), poses it (`set_pose()`), and audits it (`audit_all()`). |
| `beni_export.py` | inside Fusion | STEP per part, URDF + inertia JSON with a mass-closure assert, print STLs, viewer STLs. |
| `rig_lib.py` | inside Fusion | Builds every `RIG_*` part, including the completed Mode A `build_rig_stand()`, the §4.4 check suite (`checks_44()`), the Mode B travel harness (`slide_to()`), and an interference reporter whose names actually resolve (`real_clashes()`). The rail/block/carriage/index/pin/bumper/ballast builders and `check3_mode_b_travel()` are deferred with Mode B. |
| `rig_calc.py` | plain `python3` | Independent recomputation of the brief's arithmetic: spring curve, drop series, MGN12H moments, travel budget, mass budget, bounce mode, torque arm, and **`mode_a_stand()` — the verified Mode A load set** (42.00 mm overhang, the four moments, the tipping table, the step-6 mass/φ table). |
| `rig_export.py` | inside Fusion | Rig STLs, the targeted Mode A anchor, and the transient ABS-calibrated shoulder-hub first article, with print orientation recorded per part. |
| `first_article_fusion.py` | inside Fusion | Builds, validates and exports the four ABS actuator-interface coupons in `Beni_Prototype1_TestGauges`. |
| `readme_images_fusion.py` | Fusion MCP, with `Beni_Prototype1` active | Refreshes the full-robot, complete-leg, wheel-module, and knee-detail images used by the project homepage. |
| `stl_inspect.py` | plain `python3` | Recovers circular features from an STL mesh. Used to check the GAUGE coupons against the design record. |
| `fusion_bridge/` | both sides | Lets an agent without Fusion read the live model. `bridge.py` (plain `python3`) validates requests and reads results; `probe.py` + `ops.py` run inside Fusion. See [`fusion_bridge/PROTOCOL.md`](fusion_bridge/PROTOCOL.md). |
| `firmware/teensy_stage0/` | PlatformIO / Teensy 4.1 | Non-energizing Stage 0 scaffold: dual 500 kbit/s internal CAN loopback, BNO085 raw SPI acquisition and a 256 kB/s onboard-microSD gate. |

Reproduce the rig model:

```python
import sys; sys.path.insert(0, '/Users/neilchulani/Robots/Biped')
import rig_lib
rig_lib.checks_44()          # the six §4.4 release checks
rig_lib.real_clashes()       # interference, artifacts classified out
```

```
python3 rig_calc.py          # every number in the design record, recomputed
```

Mode A numbers only (the full script is slow):

```
python3 -c "import rig_calc; rig_calc.mode_a_stand()"
```

---

## Outputs

| Directory | Contents |
|---|---|
| `rig_stl/` | Rig parts to print, plus `reroute/` — the formerly-machined parts, now printed. `reroute/Distal_Link_L.stl` supersedes the `print_stl/` copy. |
| `first_article_stl/` | **Print this first.** ABS actuator mating coupons, the unloaded shoulder dry-fit batch, the optional Mode A cable anchor, Fusion manifests and mesh checksums. |
| `print_stl/` | Robot parts to print, the fit coupon, the two motor gauges |
| `sim/` | `beni.urdf` and `beni_inertia.json`, real inertias, mass closure asserted |
| `web/` | Browser viewer for posing the robot without Fusion |
| `snapshots/` | Timestamped model snapshots for Prototype 1 and the Mode A rig |
| `evidence/` | Dated physical-hardware photographs and observation indexes |
| `procurement/` | Dated purchasing workbooks; canonical requirements remain in the engineering BOM documents |
| `archive/manufacturing/step/` | STEP per part family (from when they were to be machined) |

---

## Known-unresolved, and gating

| | |
|---|---|
| **C2** | Shoulder motor length, 40 vs 44 mm. Manufacturer STEP and live Fusion geometry use **44.0000 mm nominal**. The existing positive stand-in is only 9.5 mm long, so it cannot report exact overall hardware length; use the delivered motor against a negative ABS mating coupon or the actual ABS mating part as a functional go/no-go. No structural consequence in the rig. |
| **C3** | Wheel motor length, 26 vs 33 mm. Manufacturer STEP and live Fusion geometry use **33.0000 mm nominal**. The existing full-length gauge is a positive stand-in; close assembly fit by placing the real motor into a negative ABS coupon or the actual ABS mating part. |
| **C4** | Actuator masses, 388/150 vs 500/250 g. ~~Decides whether rig ballast is 37.5 g or 149.5 g of shot.~~ **Mode A has no ballast, so this decides nothing structural in the rig** — it still matters to the two-leg mass and power budgets. Weigh them. |
| **B1** | Wheel-driver max bus voltage unconfirmed. Run the rig at 20 V. |
| Clock spring | Highest-risk mechanical item. **Gets no validation in the rig build** — deleted for it. Moves to the two-leg build still unproven. |
| Drop behaviour | **Now in the same category as the clock spring.** Mode A runs no drops, so the 45 mm passive limit, the φ_peak curve and `A_MAX` all move to the two-leg build unmeasured. Deliberate, and recorded in rig design record §11. |
| Main knee spring | **Received part is nonconforming by free length:** owner-reported 150 mm versus the specified 55 mm. The cartridge is 52.13 mm long at −8°, 48.87 mm at nominal and 35.57 mm at the +27° stop. Continue the exact spring RFQ; do not redesign the frozen knee around this part without first measuring its complete specification and demonstrating a kinematic/load failure. |
| Brake chopper | Deferred with Mode B, and **still uncomputed** (~21.5 V on / ~20.8 V off). ⚠ Until it is built, nothing may backdrive a motor. |
| Creep | Printed joints relax silently. Re-torque after the first hour, then periodically. Inspect the printed hub's dowel holes after every drop session. |
| Stand hold-down | **New in Mode A.** 11.00 N·m of shoulder yaw needs 11.2 kg at a 100 mm base half-width, 5.6 kg at 200 mm, 3.7 kg at 300 mm. The modelled stand is **574.2 g**, so it **must be clamped to the bench, not weighted.** Four clamp landings and 4 × M6 bench-bolt holes are in the CAD; the unloaded bench pull-test has no CAD equivalent and is still owed. |

### Open inconsistencies in the documents

Found during the 2026-08-17 cleanup and **not** resolved, because resolving them
needs a judgement call on the engineering:

- **Clock-spring capacity, 470° vs 430°.** `beni_prototype1_design_record.md` §4
  computes `L(1/rᵢ − 1/rₒ) ≈ 8.2 rad ≈ 470°` with "27 % margin" against the 370°
  needed; §13's acceptance checklist says the same cavity gives **430°**. Same
  geometry, two answers. Note 470/370 = 1.27, so the stated margin agrees with
  470 and not with 430. Separately, `electronics/02_harness_and_routing.md` §2.2
  recomputes the usable margin as **~5 %, not 27 %**.
- **Convex-substitute Hertzian ceiling.** `MANUFACTURING_CONSTRAINTS.md` says
  1.0–2.0 GPa; the rig design record §0 says 1.0–1.8 GPa (its §8 table lists
  2021 / 1808 / 1023 MPa).
- **7075-T6 subtotal**, 251.8 g (BOM §4 table) vs 251.7 g (BOM §8 roll-up).
- ~~**No rig snapshot.**~~ **[RESOLVED 2026-08-20]** `snapshots/2026-08-20_rig-mode-a/`
  now holds `Beni_SingleLegRig_ModeA.f3d`, `.step`, `mode_a_metrics.json` and a
  README, and the live document was saved as a named cloud version. Verified
  clean before and after: `ref_assert()` and `placed_assert()` both True,
  `checks_44()` all seven PASS.

### Found while exporting `RIG_Stand` (2026-08-20), and reported not resolved

- **`rig_stl/README.md` §9 bench-bolt pattern was wrong for the built part.**
  §9 read "X = ±88 and ±26"; `rig_lib.py:1625` is
  `STAND_BOLT_X = (-88.0, -26.0, 34.0, 88.0)` and the model measures **+34, not
  +26** — the set is asymmetric. Corrected at the row in §9 on 2026-08-20 with
  the constant cited. Recorded here because it was a *drill-pattern* error on the
  hold-down of a 574 g stand that must be clamped against 11.00 N·m of yaw; if
  any other document repeats the symmetric "±26", it is also wrong.
- **§9's second clamp landing was 11.5 mm long.** §9 recorded −43.5…−8;
  `checks_44()` check 7 measures **−32.0…−8.5** (23.5 mm, not 35.5). Still over
  the 20 mm minimum, so check 7 passes and nothing structural changes. Corrected
  inline in §9.
- ~~**`RIG_Cable_Post_B` has no Mode A geometry.**~~ **[RESOLVED 2026-08-20].**
  Post B correctly remains deferred with the deleted Mode B column.  Mode A now
  has a separate `RIG_Cable_Anchor_ModeA` on the two upper rear GIM6010 housing
  screws: 4 mm thick, clear of the Ø57 driver cover, zero modeled interference,
  and exported under `first_article_stl/mode_a/` for an ABS first article.
- **Guide §2.4 assumed a ~0.3 kg stand; the built part is 574.2045 g.** Reported
  as strengthening §2.4's hold-down conclusion rather than weakening it, but the
  assumed figure should be corrected where it is written. Related: `rig_calc`
  quotes bearing on an 8 mm wall where the built web is 12 mm — **unverified, and
  it was reported alongside a claim I could not reproduce (below), so treat it as
  needing a second look rather than as established.**
- **Reported but NOT reproduced — do not act on it.** The 2026-08-20 Fusion run
  also claimed `ARTIFACT_PAIRS`'s comment says the torque-arm pair is filtered
  while `_is_artifact()` has no such entry. Read directly: `ARTIFACT_PAIRS`
  (`rig_lib.py:773-792`) contains `('Cart_Lower_Eye_L',
  'RIG_Knee_Bumper_Tube_L')` — the cartridge tube — and `STEP2_FIXTURES`
  (`rig_lib.py:799`) is a separate constant with an accurate comment. No comment
  claims the torque-arm pair is in `ARTIFACT_PAIRS`; the two constants were
  conflated. The `Proximal_Link_L ↔ RIG_Torque_Arm` clash (14634.6 mm³) that
  prompted it **is** expected: bare `real_clashes()` does not filter
  `STEP2_FIXTURES`, only `checks_44()` does. Logged so it is not re-filed.

### Found while modelling `RIG_Stand` (2026-08-17), and reported not resolved

- **Guide §2.5 "shoulder axis ≥ 221.31 mm above the floor plate" vs guide §3
  "`RIG_Floor_Plate` … Unchanged".** The shoulder axis *is* the model origin, so
  the requirement cannot be met by a stand height — it lands on the floor plate,
  whose `build_rig_floor()` top face was `Z_FLOOR = −209.269` (the φ = 0 contact
  plane), **12.04 mm too high.** Resolved in favour of §2.5 as the harder
  requirement: the Mode A floor plate is re-datumed to the bench at
  `Z_FLOOR_A = −221.3119`, and `Z_FLOOR` is retained for the Mode B slide. Also
  re-datumed for the same reason: `RIG_Scale_Pedestal`, which stood on the
  deleted 2020 base.
- **≥ 221.31 mm and "the wheel rolls ~77 mm during a shoulder sweep" are
  mutually exclusive with a rigid stand.** Datuming the floor to the −8° reach
  makes the leg longest exactly at the contact point, so rotating the shoulder can
  only *lift* the wheel: at φ = −8 the wheel axis is 4.000° off plumb at
  r = 166.718, so it touches only for θ ∈ 0…+8.00° — an **8.00° window, ~23 mm of
  roll, not ~77 mm.** Loading the wheel through a sweep needs the floor *above*
  the −8° reach, which pre-compresses the knee and takes the leg off the extension
  stop that brief §6 says it rests on. 221.31 mm is the only height that satisfies
  "≥ 221.31" *and* leaves the floor touching at all. **Which of the two the rig
  actually needs is an engineering call, not a CAD one.**
- **Step 6's loading direction is unspecified, and the sign looks wrong.** Brief §6
  and `rig_calc.mode_a_stand()` tabulate "known masses on the wheel → φ" using
  `ground_force(φ)`, which is the *upward* force a grounded wheel carries. A mass
  hung on the wheel of a leg suspended at θ = 0 pulls **down**, which extends the
  knee onto its −8° stop instead of flexing it — and with the wheel resting on the
  floor and the shoulder rigid, φ is fixed by geometry and adding mass changes
  nothing. By the closed form the moment reverses sign at θ = 50.0°, so hung
  masses only flex the knee with the shoulder driven past +50°. **The step-6 table
  is not wrong as a φ-vs-force curve; what is missing is how the force is
  applied.** No CAD consequence, but it gates the one measurement Mode A exists for.
- **The repo records no modulus for PA-CF**, only strengths (84–102 MPa XY,
  26–50 MPa Z). Guide §2.6 and `beni_rig_no_machining.md` §3 both say the stand is
  now the softest element in the load path and that "stiffness here is measurement
  quality" — but there is no traceable E to compute a deflection or a
  shoulder-angle error from. The stand is designed to keep the dominant load
  in-plane and axial (0.28 MPa in the rails at stall) rather than to a stiffness
  number.
- **No print envelope is stated anywhere.** `RIG_Stand` is 200 × 32 × 299.3 mm and
  needs a bed ≥ 300 mm in one axis; the largest part accepted so far is
  `RIG_Index_Bar` at 280 mm. The 299.3 mm is not reducible — it is the 227.31 mm
  ride height plus the mount pad.
- **Guide §4 check 2 says "the stand joins [the exclusion list]".** Taken
  literally that would exclude the stand from the very check whose purpose is to
  prove nothing fouls it. Implemented the other way: the stand is checked, and it
  comes out clean at all 17 angles because its Y band (10…42) is disjoint from
  every moving part (≥ 45.49).
