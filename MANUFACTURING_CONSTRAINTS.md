# Manufacturing constraints

**Authoritative. Read before adding any part to any build in this project.**

Stated by the project owner, 2026-08-12.

---

## The rule

> **3D printed parts and off-the-shelf parts only.**
> **No laser cutting. No machining.**

A manifold STL is not by itself a printable release. Print-axis dimensional
control and support-removal requirements are governed by `CLAUDE.md` hard rule
12.

"Off the shelf" means a catalogue item you can order and fit as-is: fasteners,
dowel pins, washers, shims, bearings, linear rail and blocks, aluminium
extrusion, springs, magnets. Cutting bought stock to length with a hacksaw is
fine. Anything that needs a mill, a lathe, a waterjet or a laser is not.

## What this rules out

| Not allowed | Was used for |
|---|---|
| Laser-cut sheet | `Knee_Stop_Arc_L`, `RIG_Ballast_Disc` |
| Milled / turned parts | the ten families in `archive/manufacturing/machined_parts_spec.md` |
| Ground flats, keyed features, reamed precision bores in metal | `Knee_Axle_L`'s double-D, `Knee_Sleeve_L` |

## Where each affected part went

For the single-leg rig, every one of these is resolved. Nothing is outstanding.

| Part | Was | Now | Where it is written up |
|---|---|---|---|
| `Shoulder_Output_Hub_L` | 7075 machined | **printed** + 3 bought Ø4 × 10 dowel pins + M4 inserts | `beni_rig_no_machining.md` §2.1 |
| `Wheel_Hub_L` | 7075 machined | **printed** + steel washers + a re-torque schedule | `beni_rig_no_machining.md` §2.1 |
| `Cart_Upper_Eye_L`, `Cart_Lower_Eye_L` | 7075 machined | **printed**, measured, real dimension fed back to the spring model | `beni_rig_no_machining.md` §2.4 |
| `Knee_Magnet_Carrier_L` | steel | **printed**, runout measured on an indicator | rig design record §4 |
| `Knee_Axle_L` | 4140 ground, double-D | **bought** Ø10 h6 hardened ground dowel pin | rig design record §4 |
| `Knee_Sleeve_L` | steel, double-D bore | **deleted** — its Ø16 bore is printed into `Distal_Link_L` as Ø10 | rig design record §4 |
| `Cart_Guide_Rod_L` | ground steel | **bought** Ø5 × 50 hardened shaft | rig design record §9 |
| `Cart_Preload_Shim_L` | shim stock | **bought** Ø19/Ø13.6 × 0.5 shim washers | rig design record §9 |
| **`Knee_Stop_Arc_L`** | **laser-cut 3 mm steel, 45 HRC** | **deleted.** The +27° hard stop is now a **compression column of bought M5 washers** inside the spring cartridge, with a printed TPU sleeve as the progressive bumper; `RIG_Knee_Stop_Plate_L` (printed) keeps the −8° stop and a +28° backup | **rig design record §8** |
| **`RIG_Ballast_Disc`** | **laser-cut 3 mm steel** | **`RIG_Ballast_Pot` × 2**, printed cups filled with off-the-shelf steel shot — **now [DEFERRED — MODE B] (2026-08-17): the Mode A build has no vertical slide, so there is nothing to ballast. The substitution stands if Mode B is ever built; the shot need not be bought now** | **rig design record §5** |

**Amended 2026-08-17 — the rig build is Mode A only.** This does not change any
substitution above; it changes only what has to be printed *now*. Deferred with
Mode B: `RIG_Rail`, `RIG_Blocks`, `RIG_Carriage`, `RIG_Index_Post`,
`RIG_Index_Bar`, `RIG_Mode_Pin`, `RIG_Bumpers`, `RIG_Ballast_Pot`. Added:
**`RIG_Stand`**, printed, which reacts the shoulder's own 11.00 N·m stall / 25.00
N·m proof yaw torque at a **42.00 mm** overhang and therefore **must be clamped to
the bench, not weighted** — see `fusion_agent_guide_mode_a.md`. The stand is fully
inside this constraint: printed part plus bought bench clamps, no machining, no
laser cutting.

## Threaded interfaces in printed parts

**Updated 2026-09-14: the owner confirmed the Ø5.3 ABS station passed all M4 × 8
installation and cooled-retention checks. Fusion verifies that diameter in both
documents. The nominal Ø4.0 M3 general-gauge station has now failed physically;
the dedicated Ø4.1–4.5 ABS ladder must select the replacement before any active
M3 receiver print or insertion. The two hubs are ABS first-article print releases;
the rim has a separate printability hold. The corrected proximal link is now in
use and all six M4 screws seat properly, closing its reported root-access/seating failure.**
Physical evidence: [M4 coupon PASS](evidence/inserts/2026-09-04_m4_coupon_pass/),
[M3 Ø4.0 FAIL](evidence/inserts/2026-09-14_m3_coupon_fail/),
and [corrected-link assembly PASS](evidence/assembly/2026-09-07_owner_mockup/).
This is the canonical insert map. The
owner's received assortments are indexed at
[`evidence/inserts/2026-09-02_received/`](evidence/inserts/2026-09-02_received/).
The same information is shown visually in the
[`docs/assembly/heatset_receiver_map.md`](docs/assembly/heatset_receiver_map.md).

The M3 design family is the owner-reported Voron-style insert. The exact
AliExpress order variant still needs to be recorded. The general gauge's sole
nominal Ø4.0 candidate is too small in the owner's ABS result. A dedicated
Fusion-generated ladder now tests Ø4.1/4.2/4.3/4.4/4.5 × 6.0 mm blind pockets;
select the smallest physical pass before changing production geometry. Current
Ø4.0 part pockets remain historical source geometry and are held. The mixed
Kadriick case contains 30 × M4 × 8 and
25 × M4 × 10 inserts. Its label gives M4 thread pitch 0.7 mm, `d1=5.5 mm` and
`d2=5.0 mm`, but it does not unambiguously define the printed-hole diameter.
The same-profile ABS ladder tested Ø4.9/5.0/5.1/5.2/5.3 through bores. The
owner selected Ø5.3 and confirmed all acceptance checks. Repeat critical
coupons before the later PA-CF structural build.

| Printed thread destination | Qty, active ABS single leg | Insert / receiving feature | Current design status |
|---|---:|---|---|
| `Chassis_Shoulder_Plate_L`, cable-cover joint | 4 | Voron-style M3; current source is Ø4.0 through the 5.0 mm plate | **HOLD — Ø4.0 PHYSICAL FAIL.** Select the new ladder result, promote and re-export through Fusion before printing. The removable cover has Ø3.4 clearance holes and four M3 × 10 screws enter from its accessible outboard face. They engage 3.5 mm and stop 1.5 mm before the inboard plate face. When fitting revised cable post A, its 2 mm thickness requires M3 × 12 at the two upper positions; the lower two remain ×10. |
| `Proximal_Link_L` arm-B boss | 5 | Voron-style M3; printed part has Ø4.0 × 5.0 blind pockets (3 stop-plate + 2 encoder-bracket) | **INSERTION HOLD — Ø4.0 PHYSICAL FAIL.** Retain the Ø19.15 access-fixed ABS link for its accepted bearings and six M4 screw seats, but install no M3 inserts. Reassess replacement after the ladder winner is promoted in Fusion. |
| `RIG_Stand` panel interface | 5 | Voron-style M3; current source is Ø4.0 × 6.0 blind pocket for a 5.0 mm insert | **DO NOT PRINT — Ø4.0 PHYSICAL FAIL.** Fusion verified the surrounding geometry and zero stand interference; select the ladder winner, promote it and re-export before printing. The intended depth retains 1.0 mm insertion space and a 6.0 mm printed floor. |
| `Shoulder_Output_Hub_L` root flange | 6 | Owner-held Kadriick M4 × 8; owner-selected Ø5.3 through the full 8.0 mm flange | **OWNER HUB INSERT INSTALLATION AND CORRECTED-LINK SIX-SCREW SEATING PASS.** Retain the new Ø4.15 hub with Ø5.3 receivers and corrected link. M4 × 10 link screws have 6.2 mm engagement and 1.8 mm end clearance. The owner confirms all six M4 screws work properly on the replacement. |
| `Wheel_Hub_L` rim joint | 6 | Owner-held Kadriick M4 × 8; owner-selected Ø5.3 through the 6.0 mm hub | **ABS HUB PRINTED; INSERT/MOTOR FIT PENDING; RIM PRINTABILITY HOLD.** [September 7 completion](evidence/assembly/2026-09-07_small_parts_printed/). Install from the motor face: 6.0 mm embeds and 2.0 mm projects outboard. The rim’s six Ø6.0 × 2.2 reliefs retain 0.25 mm radial and 0.20 mm axial envelope clearance, with a Ø38 opening and 1.0 mm ligament. M4 × 8 rim screws have 6.0 mm engagement and 2.0 mm end clearance. The rim’s internal ledge and outer flange need a verified overhang solution; do not print it under the former no-support instruction. |

The active ABS article consumes **14 M3 inserts** before spares: 4 shoulder
plate + 5 proximal-link boss + 5 stand. It also consumes **12 of the 30 owned
M4 × 8 inserts**: six shoulder and six wheel. M4 × 10 was rejected because it
would add 2.0 mm more projection/relief without improving either joint; changing
these torque joints to M3 was rejected because it would reduce the specified
fastener size and mismatch the existing M4 clearance patterns. The owner elected to retain M4 on 2026-09-04. The M3 and M4
ABS ladders are in
[`first_article_stl/insert_fit/`](first_article_stl/insert_fit/).

Future/deferred interfaces remain visible rather than silently inheriting the
active quantities:

| Printed thread destination | Scope | Status |
|---|---|---|
| `Chassis_Frame`, 5 per side | two-leg build | **SOURCE RECALIBRATION REQUIRED / DEFERRED.** Ten current Ø4.0 × 6.0 blind M3 pockets sit in local Ø10 × 6.5 bosses. Their surrounding geometry previously passed Fusion, but Ø4.0 has now failed physically; apply the appropriate material-specific coupon result before the future print release. |
| Optional proximal-link satellite-PCB boss, 2 × M2 per leg | two-leg build / electronics CR-4 | **OPEN DESIGN.** The boss does not exist yet and may be deleted if the final motor-controller architecture reads the knee encoder directly. If retained, select one of the owned M2 insert lengths by coupon and model its pocket before the boss is released. |
| `RIG_Carriage`, 5 × M3 | **[DEFERRED — MODE B]** | **SOURCE RECALIBRATION REQUIRED / DEFERRED.** Isolated Fusion build verified the surrounding geometry for five current Ø4.0 × 6.0 blind pockets; choose a material-specific passing coupon before any future release. |
| `RIG_Carriage`, 4 × M4 ballast studs | **[DEFERRED — MODE B]** | **SOURCE UPDATED / DEFERRED.** The builder inherits the owner-selected Ø5.3 ABS diameter for four through receivers and the full 8 mm insert. Rebuild and verify the deferred carriage through Fusion when Mode B returns; no carriage print is released now. |
| `RIG_Knee_Collar_L` | active knee | **UNRELEASED RETENTION DESIGN — DO NOT PRINT.** The current 3 mm collar does not overlap the Ø10 pin and its Ø2.5 hole is axial, not a working radial set-screw receiver. A clamp collar also cannot be selected from CAD alone because the 35 mm pin allocation leaves no proven free shaft. Resolve after measuring the delivered eBay pin and the real bearing/link stack. This is not an insert interface. |

Do **not** add inserts to clearance parts. `Shoulder_Cable_Cover_L` is now a
clearance part; its receiving inserts are in `Chassis_Shoulder_Plate_L`.
`Chassis_Shoulder_Plate_L` also fastens to the GIM6010's metal housing threads;
`Shoulder_Output_Hub_L` fastens to the GIM6010's metal output threads;
`Distal_Link_L` and `Wheel_Hub_L` fasten to the GIM4305's metal threads.
`Knee_Encoder_Bracket_L`, `RIG_Knee_Stop_Plate_L`, and `Wheel_Rim_L` carry
clearance holes; their receiving inserts belong in the proximal link or wheel
hub as identified above. The rim's six larger recesses clear projecting insert
ends and are not receivers. No active printed joint calls for an M2 or M5
insert.

## The one place this cost real margin

Everything above is a lateral move or an improvement except the knee hard stop.

The steel arc worked because its slot ends were **conformal** — a 3.1 mm *concave*
radius bearing on a Ø6 dowel, about 257 MPa at the 534 N crash load. Nothing
printed or off-the-shelf reproduces a concave 3.1 mm steel face, and every convex
substitute reverts to Hertzian line contact at **1.0–2.0 GPa**. That is why the
stop was moved into the spring cartridge as a compression column instead of being
substituted in place: a column has no contact-stress problem at all.

What it costs, honestly:

- the working stop is **inside the cartridge and not inspectable** without pulling
  a clevis pin;
- it reacts through two **printed** spigot faces at 9.9 MPa rather than a hardened
  steel slot end — a factor of 8 below the material, but plastic where there used
  to be steel in the final crash path;
- its engagement angle depends on the printed eyes' achieved dead length, so it
  must be **set by measurement after step 6**, not from a drawing.

Full reasoning, the Hertzian numbers for every substitute considered, and the
verification sweep: `beni_single_leg_rig_design_record.md` §8.

## Scope

The constraint governs **what gets built**. It does not invalidate the design
records that describe the two-leg robot as originally engineered:

- `archive/manufacturing/machined_parts_spec.md` still correctly specifies the ten
  machined families **as they were designed**. It is not a shopping list for the
  rig build — see its own banner.
- `beni_prototype1_design_record.md` and `beni_prototype1_bom_and_assembly.md`
  describe Prototype 1 with machined hubs and axles. That is history, and the
  mass and load numbers in them are still the reference.

If the two-leg build later gets access to a shop or a laser, the retired steel
arc files are preserved under `archive/laser/`.
