# Rig parts to print

Exported from the verified `Beni_SingleLegRig` assembly at High mesh refinement.
All STLs are in millimetres and sit at their **assembly coordinates**, not
centred on the origin — every slicer will drop them to the bed and centre them.

Companion: `../beni_single_leg_rig_design_record.md`.

> ## ⚠ AMENDED 2026-08-17 — MODE A ONLY
> The build is **Mode A**: the shoulder bolts rigid to a printed stand. The
> vertical slide, the ballast and the drop series are **deferred, not cancelled**.
>
> | Print now (Mode A) | Deferred (Mode B) |
> |---|---|
> | **`RIG_Stand`** *(exported 2026-08-20)*, `RIG_Torque_Arm`, `RIG_Floor_Plate` ⚠ *re-datumed to the bench, see §9*, `RIG_Cable_Post_A`, `RIG_Knee_Stop_Plate_L`, `RIG_Knee_Bumper_Tube_L`, `RIG_Knee_Collar_L`, `RIG_Knee_Magnet_Carrier_L`, and all five of `reroute/` | §1 `RIG_Carriage`, §2 `RIG_Index_Bar`, §8 `RIG_Ballast_Pot` × 2, plus the bought `RIG_Rail` / blocks / Ø8 mode pin / bumpers. `RIG_Cable_Post_B` is separately blocked pending a Mode A redesign; see §6. |
>
> `RIG_Stand` replaces `RIG_Carriage` as "the part everything else hangs on", and
> the overhang it works at is **42.00 mm, not 63.00** — Mode A deletes the block
> and the carriage from the lateral stack, so the stand's outboard face *is* the
> motor front mount face. Its requirement set is in
> **`../fusion_agent_guide_mode_a.md`**; the short version is 11.00 N·m of shoulder
> yaw stall / 25.00 N·m proof, and **it must be clamped to the bench, not
> weighted.**

---

## Settings — the same for every part here

Per `beni_rig_no_machining.md` §1. **Orientation is the strength lever; infill is
not.** PA-CF measures 84–102 MPa in XY but only 26–50 MPa in Z, so which way the
part lies on the bed decides whether it survives.

| Setting | Value | Why |
|---|---|---|
| Perimeters / walls | **5** | shells carry bending load; this is the main lever |
| Infill | **40 % gyroid** | past ~40 % the returns collapse. 100 % adds time and warp, not strength |
| Layer height | 0.15 mm | more interlayer bonds per mm of Z |
| Extrusion temp | **top of range** | layer adhesion is temperature-driven |
| Cooling | **minimal** | fast cooling is the #1 cause of weak Z bonds |
| Filament | **dried** | non-negotiable; wet nylon loses a large fraction of interlayer strength |

Structural release material is **PA-CF** unless a part is explicitly assigned a
different material.

**The first-article campaign is ABS.** Print `GAUGE_Fit_Coupon`, negative motor
mating coupons or the actual mating parts, assembly-rehearsal parts,
cable-routing parts, covers, floor-contact parts, and—if useful—the whole
unloaded dry-fit leg in ABS. The two existing `GAUGE_*_Motor_Interface` files
are positive motor stand-ins and are optional now that the motors are in hand.
Do not apply stall
torque, spring-characterisation loads, drops, or proof loads through the ABS load
path: `RIG_Stand`, both hubs, `RIG_Torque_Arm`, and the two cartridge eyes remain
PA-CF for loaded testing. An ABS coupon calibrates only the ABS campaign; repeat
the critical mating coupon in PA-CF before releasing PA-CF structural prints.
See `../beni_rig_no_machining.md` §4 for the load-path reasoning.

---

## Print in this order

### 0. First — `../print_stl/GAUGE_Fit_Coupon.stl`
Unchanged from the robot build, and it still de-risks every print here. Six
critical bores in one 26 × 92 × 8 bar. For the ABS campaign, test each bore with
the real matching fastener or dowel and record which nominal feature gives the
required fit. The result is material-, printer-, orientation-, and
profile-specific; do not reuse the ABS result later as PA-CF compensation.

The two `GAUGE_*_Motor_Interface.stl` files were re-measured against design
record §2 and every feature agrees, but they are positive stand-ins. They are
optional now that the motors are present and cannot perform the new physical
mating check. Use a negative ABS coupon or the actual ABS mating part instead.

For the current GIM6010 ABS article, do **not** use the nominal
`reroute/Shoulder_Output_Hub_L.stl`. The owner-tested Ø4.15 ABS variant and the
exact next-print sequence are in
[`../first_article_stl/assembly_dry_fit/`](../first_article_stl/assembly_dry_fit/).
That compensation is specific to the ABS profile and is not a structural
release dimension.

### 1. ~~`RIG_Carriage.stl`~~ — **[DEFERRED — MODE B]**
90.2 cm³, **103.7 g**, 154 × 170 × 8. Do not print this for the Mode A build; it
exists only to ride the MGN12 blocks. **`RIG_Stand` takes its place** and inherits
the two things below that were never about the slide:

- **The five-hole panel interface is unchanged.** Whatever mounts the motor must
  line up with `Chassis_Shoulder_Plate_L`'s existing frame-bolt holes at
  (−60, −18), (−60, 48), (−60, 62), (30, 48), (30, 62). Verified concentric in CAD;
  confirm on the print before installing inserts.
- **M3 heat-set inserts, 5.0 mm long, with a depth-stopped tip** — 5.0 mm bores in
  an 8 mm plate leave a 3 mm floor. Same rule on the stand.

The Mode B notes, for whenever the slide gets built: plate face flat on the bed so
the 63 mm overhang bends in the print plane and the eight block-screw counterbores
print as pockets; no support anywhere, every hole a through-feature.

### 2. ~~`RIG_Index_Bar.stl`~~ — **[DEFERRED — MODE B]**
114.3 cm³, 131.4 g. Indexes drop height on the slide, and Mode A runs no drops.
When built: flat on the bed, station holes vertical — the Ø8 pin bears across
layers, not along them. 17 stations at 10 mm pitch. Not on the slide, so its mass
does not matter.

### 3. `RIG_Floor_Plate.stl`
260 × 60 × 6, flat on the bed. **A 6 mm aluminium plate is the better part** if
you have one — the wheel rolls on this and the brief wants it flat and hard. The
STL is provided so the rig can be finished without a metal supplier. **Still
needed in Mode A**: it is what the wheel rests on, and it is what stops the leg
falling when the shoulder is de-energised.

### 4. `RIG_Knee_Collar_L.stl` and `RIG_Knee_Magnet_Carrier_L.stl`
Tiny, but the second one is an instrument mount.

- **Both: bore axis vertical**, so the Ø10 press fits are round.
- `RIG_Knee_Magnet_Carrier_L` carries the **0.05 TIR** concentricity that keeps
  the AS5048A honest. **Measure it on a dial indicator.** If runout exceeds
  ~0.1 mm, bond the magnet into the pocket using the Ø10 bore as the datum
  instead of trusting the printed step.
- The magnet bottoms on the dowel pin's own ground end face at y = 93.7, so the
  pocket depth is not what sets the air gap.

### 5. `RIG_Torque_Arm.stl`
93.6 cm³, 107.6 g. **Flat on the bed, arm plane parallel to the bed**, so the
200 mm bending load is fully in-plane. Bolts to the hub's 6 × M4 Ø44 PCD **in
place of the proximal link** — step 2 runs with the leg off.

### 6. `RIG_Cable_Post_A.stl`, `RIG_Cable_Post_B.stl`
Flat on the bed. Post A is clamped under two of the motor's eight M3 housing
screws, which become **M3 × 16** for that reason.

⚠ **`RIG_Cable_Post_B.stl` is NOT printable for Mode A — do not send it to the
bed.** [BLOCKED 2026-08-20] The part mounted to `RIG_Column`'s T-slot, and
`strip_mode_b()` deleted the column, so the occurrence is no longer in the model.
`build_rig_cable_post_b()` (`rig_lib.py:735`) is intact but is still dimensioned
off the Mode B constants `RAIL_X`, `COL_Y0` and `TRAVEL_UP`, so the STL in this
directory (dated 2026-08-12) is geometry for a fixture that no longer exists. It
needs re-dimensioning against `RIG_Stand` before it is printed or re-exported.
Not redesigned here — it is a design decision about where the cable is anchored
now that the column is gone.

### 7. The knee stop parts
- **`RIG_Knee_Stop_Plate_L.stl`** — PA-CF, flat on the bed. Replaces the laser-cut
  steel arc. Bolts to the same three M3 inserts in the proximal arm-B boss with
  M3 × 6. Carries the −8° extension stop (3.9 MPa, printed conformal slot end) and
  a +28° flexion backup.
- **`RIG_Knee_Bumper_Tube_L.stl`** — **TPU 95A**, bore axis vertical. A sleeve that
  goes *around* the washer stack, not on top of it: the two must act in parallel
  or the steel never goes solid. Print at 3 walls so its rate stays soft.
- The +27° hard stop itself is bought: **16.571 mm of M5 washers** on the guide
  rod, bulked with 1.0 mm plain washers and trimmed with 0.2/0.3/0.5 mm DIN 988
  shim washers. **Set it after step 6, from the measured spring** — one 1.0 mm
  washer moves the stop by 1.83°.

### 8. ~~`RIG_Ballast_Pot.stl` × 2~~ — **[DEFERRED — MODE B]**
Open side up, no support. Fill with steel shot, airgun BBs or a jar of M4 nuts and
weigh on a kitchen scale — 344 g of capacity across the pair, and only ~37 g is
needed to hit 1.645 kg with a 500 g motor. **Mode A has nothing to ballast**: the
1.645 kg figure is the sprung mass on the slide, and there is no slide. Do not buy
the shot yet. This is also why conflict C4 (motor mass 388/150 vs 500/250 g) stops
being a rig-design risk — it was only ever deciding how much shot went in here.

### 9. `RIG_Stand.stl` — **the Mode A part**
Modelled 2026-08-17 by `rig_lib.build_rig_stand()`. **499.3 cm³, 574.2 g**,
200 × 32 × 299.3 (X × Y × Z), one body. Full requirement set:
**`../fusion_agent_guide_mode_a.md`** §2.

**Exported 2026-08-20** to `RIG_Stand.stl` (binary, MeshRefinementHigh, 2372
triangles). Measured from the model against the figures above: 499.3082 cm³,
574.2045 g, 200.0000 × 32.0000 × 299.3119, mount face y = 42.0000. Mesh bbox
reproduces the B-Rep to 0.0000 mm; mesh volume is +0.020 % from chordal
tessellation of the bores. Snapshot: `../snapshots/2026-08-20_rig-mode-a/`.

**Orientation: mount face (y = 42.00) flat on the bed, building inboard.** No
support anywhere, and the part's Y thickness only ever decreases away from the
bed (12 mm web, 32 mm foot, both sharing the y = 42.00 face).

- **Orientation follows the load, and the load is torsion, not bending.** The
  dominant case is the shoulder's own reaction: **11.00 N·m yaw at stall, 25.00
  N·m proof**, against 2.30 N·m pitch and 2.99 N·m roll. Yaw is a couple about Y,
  i.e. a couple lying *in* the XZ plane, and every layer of this print is an XZ
  slice — so the whole dominant load stays in the plane where PA-CF is 84–102 MPa
  instead of 26–50. Printed upright the same couple would try to peel layers.
- **The bed-facing face is the one that has to be flat.** It bears on
  `Chassis_Shoulder_Plate_L`'s inboard face over the five bolt landings, and the
  five Ø5.0 × 5.0 insert bores open on it, so they print as clean first-layer
  holes with no bridging.
- ⚠ **Footprint is 200 × 299 mm, so it needs a bed ≥ 300 mm in one axis.**
  **RESOLVED 2026-08-20: the printer is a Bambu Lab H2S, build volume
  340 × 320 × 340 mm** (vendor spec, web, 2026-08-20 — the first build envelope
  recorded in this repo). `RIG_Stand` **fits outright in the orientation above**;
  the splice contingency below is not needed and is retained only in case the
  part is ever built on a smaller machine. The 299.3 mm is not negotiable — it is
  227.31 mm of ride height plus the pad up to the panel's top edge — and it is
  the *smallest* dimension of the three, so no other orientation fits a smaller
  bed. If a printer cannot take it, split it low in the column where the section
  is largest and splice with a bolted lap; do **not** split near the mount pad.
- **Overhang is 42.00 mm** from the stand's outboard face to the wheel plane.
  ⚠ Anything you shim in between — a washer, a spacer, a printed pad — scales all
  four moments. Verified 42.000 mm in CAD with a 0.000 mm gap to the panel.
- **It must be clamped, not weighted.** 11.00 N·m needs 11.2 kg of hold-down at a
  100 mm base half-width, 7.5 at 150, 5.6 at 200, 4.5 at 250, 3.7 at 300. This
  stand is 0.574 kg. **Four clamp landings** are modelled on the foot's top face
  (X −100…−77.5, **−32.0…−8.5** [CORRECTED 2026-08-20 — was recorded −43.5…−8;
  measured 23.5 mm, not 35.5. Still over the 20 mm minimum, so check 7 passes],
  +8…+61.5, +77.5…+100, each 32 mm wide in Y), plus
  **4 × M6 bench-bolt holes** at **X = −88, −26, +34, +88** — Ø6.5 through with
  Ø11 × 7 counterbores so the heads sit sub-flush and the landing still takes a
  jaw. ⚠ **The bolt set is asymmetric.** This row previously read "X = ±88 and
  ±26"; the built part has its third hole at **+34, not +26**. Source of truth is
  `rig_lib.py:1625`, `STAND_BOLT_X = (-88.0, -26.0, 34.0, 88.0)`, confirmed
  against the model 2026-08-20. Drill from the STL or from that constant, not
  from a symmetric assumption.
  Buy the clamps — the Mode A build needs more of them than Mode B did.
- **Shoulder axis ≥ 221.31 mm above the floor plate** — that is the ride height at
  the −8° extension stop, i.e. where a free leg actually rests. ⚠ Met by dropping
  the **bench plane** to Z = −227.31 and putting `RIG_Floor_Plate` on it, *not* by
  a stand height: the shoulder axis is the model origin. The floor plate's old
  Z = −209.269 top face is the φ = 0 contact plane and is 12.04 mm too high for
  Mode A. See `build_rig_floor()`.
- Same five-hole panel interface and same 5.0 mm M3 inserts as §1 — but in a 12 mm
  web, so each bore leaves a **7 mm floor**, not 3 mm. Still use a depth-stopped
  installation tip: the insert's grip is the joint's weak element.

---

## `reroute/` — formerly machined, now printed

These five were 7075 or steel in `archive/manufacturing/machined_parts_spec.md`. Routing
per `beni_rig_no_machining.md` §2. **Print one of each and dry-fit before
committing to a second set.**

| File | Was | Orientation | The thing that will bite |
|---|---|---|---|
| `Shoulder_Output_Hub_L.stl` | 7075-T6 | **flange face flat on the bed** | Torque then loads the bolt circle in XY and the three dowel holes see shear **across** layers. **Structural release is pending a PA-CF press-fit coupon for the bought Ø4 × 10 hardened dowels.** The former Ø3.9-and-ream instruction is retired because machining is prohibited. Without the steel dowels the printed register sees 63 MPa against PA-CF's ~40–50 MPa shear at proof load. Use M4 heat-set inserts **5.8 mm long**, not 8 mm: the flange is 8 mm thick and an 8 mm insert breaks through. |
| `Wheel_Hub_L.stl` | 7075-T6 | flat, register face up | Torque is carried by **friction**, and preload in plastic creeps. **Steel washer under every screw head**, and re-torque after the first hour then every ~10 hours. The Ø37.3 register is centring only and prints fine at 5 walls. |
| `Cart_Upper_Eye_L.stl` | 7075-T6 | **pivot bore axis vertical** | Printed on its side the eye splits along a layer. Carries the **11.00 ±0.05** pivot-to-spigot dimension: **measure what you actually achieved and feed the real number into the spring model** rather than chasing nominal. Step 6 measures F₀ and k anyway, so a print error is detectable. |
| `Cart_Lower_Eye_L.stl` | 7075-T6 | pivot bore axis vertical | Same, for **14.57 ±0.05** including 2.0 mm of shims. |
| `Distal_Link_L.stl` | PA-CF already | **on edge, link axis vertical** | **RE-EXPORTED — this supersedes `../print_stl/Distal_Link_L.stl`.** Its Ø16 steel-sleeve bore is now **Ø10**, because adopting §2.3 prints the sleeve's function into the link. Volume 45.0 → 47.6 cm³. On edge puts primary bending in the print plane and makes the 20 mm spring channel a through-slot, so nothing needs internal support. |

`Knee_Stop_Arc_L` is **gone entirely** — there are no laser-cut parts. The +27°
crash stop moved into the spring cartridge as a compression stack (a stack of
bought M5 washers plus a printed TPU sleeve), and `RIG_Knee_Stop_Plate_L` is a
printed part that keeps only the −8° extension stop and a +28° backup. Full
reasoning and the verification sweep are in the design record §8.

---

## Reused unchanged from `../print_stl/`

`Proximal_Link_L` · `Wheel_Rim_L` · `Wheel_Tyre_L` (TPU 95A) ·
`Knee_Encoder_Bracket_L` (ABS) · `Chassis_Shoulder_Plate_L`.

Nothing in this build modifies those five, and no new hole was put in any of
them.

---

## What the first-article campaign validates

- Every bore fit and the ABS slicer compensation (`GAUGE_Fit_Coupon`).
- Both real motor interfaces using negative ABS mating coupons or the actual ABS
  mating parts. The existing positive motor stand-ins remain useful for CAD-side
  checks but do not fit onto the delivered motors.
- That **the stand's** five insert bores match the panel. ~~and its eight block
  screws match the MGN12H 20 × 20 pattern~~ — **[DEFERRED — MODE B]**, there are no
  blocks.
- **The stand's clamp access and flat seating**, without applying meaningful
  torque to an ABS first article. The loaded hold-down release test is for the
  PA-CF stand: clamp it to the bench, then push at the
  wheel with a luggage scale to make ~11 N·m about the shoulder axis (≈52 N at the
  209 mm nominal lever) and confirm nothing lifts, slips or visibly twists. This
  is the one Mode A check with no CAD equivalent, and it is the check that decides
  whether the whole build is trustworthy.
- **That the nominal 42.00 mm overhang assembles correctly.** The value comes
  from the STEP/Fusion stack. Without calipers, fully seat the motor and panel,
  confirm every mating face closes, and verify the wheel plane lands correctly
  over the floor plate. Every moment in the load table still uses the 42.00 mm
  CAD datum.
- The whole knee stack in its **new** form: Ø10 dowel pin straight through both
  6800s, pressed into the printed distal boss, collar on, magnet carrier on.
- **Assembly order.** ~~The eight carriage-to-block screws are captive under the
  panel, so the order is: carriage → blocks → panel + motor.~~ **[DEFERRED — MODE
  B].** Mode A is simpler — stand → panel + motor → leg — but the same rule
  applies: confirm you can reach every fastener before the motor goes on, because
  the panel hides whatever is behind it.
