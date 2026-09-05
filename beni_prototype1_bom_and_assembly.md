# Beni Prototype 1 — Bill of Materials and Assembly Sequence

> ### ⚠ §4, §5 and the §8 roll-up are superseded for building
> **3D printed and off-the-shelf parts only, no laser cutting or machining** —
> [`MANUFACTURING_CONSTRAINTS.md`](MANUFACTURING_CONSTRAINTS.md), which carries the
> routing table for all ten machined families. §1–§3, §6, §7 and §9–§10 stand.
> See the banners on §4 and §8 before quoting any mass. Four assembly steps in §9
> reference deleted parts and are annotated inline.


**Revision 2 — 2026-08-08.** Masses in this revision are read straight out of
the Fusion model with real physical materials assigned, not computed by hand.
See `beni_prototype1_rev2_changes.md` for what changed and why.

**DFM refresh — 2026-09-01.** Fusion re-measured the §1 printed families after
the proximal face-flat redesign and the current scripted distal-link reroute.
The displayed §1 values and subtotal are the exact Fusion results from that
source build; the PA-CF density is unchanged.

Quantities are **per robot** (two legs) unless noted. Left-hand parts are named
`*_L`; the right leg is the mirror image about Y = 0 and uses the same part
numbers with `_R`.

Masses are computed from the modelled solid volume × the density in the table.
Printed parts assume solid-equivalent density; see the note at the end.

---

## 1. Printed parts — PA-CF (carbon-filled nylon, ρ = 1.15 g/cm³)

| Part | Vol cm³ | Mass g | Qty | Total g | Print orientation |
|---|---:|---:|---:|---:|---|
| `Chassis_Shoulder_Plate_L/R` (side panel incl. motor interface) | 40.2337 | 46.2687 | 2 | 92.5375 | flat, panel face on the bed; spiral lip prints up, no support |
| `Proximal_Link_L/R` | 66.7915 | 76.8102 | 2 | 153.6204 | outboard arm/bearing face flat, bearing axes normal to the bed; bed-ready export only, supports off, 20.0 mm channel bridge |
| `Distal_Link_L/R` | 46.1144 | 53.0315 | 2 | 106.0631 | **HOLD** — Fusion finds a 2633.0 mm² face-flat datum aligned with the critical Ø10 bore, but the real Ø10 h6 pin and final support/bridge audit still gate its export |
| `Wheel_Rim_L/R` | 67.4501 | 77.5676 | 2 | 155.1352 | **PRINTABILITY HOLD:** web-down orientation has unsupported internal and retaining-flange ledges; do not print until resolved. Carries the tyre bead groove, inboard retaining flange, owned-M4×8 insert-tip reliefs, and a Ø38 web opening that preserves a 1 mm ligament to those reliefs |
| `Chassis_Frame` (centre cage, not mirrored) | 61.1724 | 70.3483 | 1 | 70.3483 | flanges vertical, open box, no support |
| **Subtotal** | | | | **577.7044** | |

## 2. Printed parts — ABS (ρ = 1.04 g/cm³)

| Part | Vol cm³ | Mass g | Qty | Total g | Print orientation |
|---|---:|---:|---:|---:|---|
| `Shoulder_Cable_Cover_L/R` | 15.44 | 16.1 | 2 | 32.1 | flange face down, wall prints up |
| `Knee_Encoder_Bracket_L/R` | 2.61 | 2.7 | 2 | 5.4 | shelf face down, posts print up |
| `Electronics_Tray` (centre, not mirrored) | 8.51 | 8.9 | 1 | 8.9 | flat |
| **Subtotal** | | | | **46.4** | |

## 3. Printed parts — TPU 95A (ρ = 1.20 g/cm³)

| Part | Vol cm³ | Mass g | Qty | Total g |
|---|---:|---:|---:|---:|
| `Wheel_Tyre_L/R` (Ø110 crowned × 30, **free ID Ø94**) | 66.71 | 80.1 | 2 | 160.1 |

The tyre is **modelled at ID Ø96 in its installed, stretched state** so it does
not read as a permanent interference in every future audit. **Order it at free
ID Ø94** — 2 mm of stretch onto the Ø96 rim seat. Revision 2 also added:

- an **internal bead rib** at r = 46.5 → 48 over y = 82.5…85.5, mating a groove
  cut in the rim drum, which locks the tyre axially and in torsion without
  relying on friction. As previously modelled the tyre ID exactly equalled the
  rim OD, so there was no press fit at all and it would have spun under braking;
- an **inboard flange** on the rim at r = 48 → 52 over y = 68…69 for the tyre to
  butt against, so it cannot walk off inboard (there was nothing there before);
- a **crowned tread**, R150.4, dropping 0.75 mm from Ø110 at the centre plane to
  Ø108.5 at each edge — a contact patch instead of 30 mm of line contact, which
  is what gives the machine any camber tolerance at all.

## 4. Formerly-machined families — historical masses, not a shopping list
### Was 7075-T6 aluminium (ρ = 2.81 g/cm³)

> **Do not order from §4 or §5.** These are the ten machined families **as they
> were designed**, retained for their masses and key features. All ten are
> rerouted to printed or bought parts — the part-by-part routing table (was /
> now / where it is written up) is in
> [`MANUFACTURING_CONSTRAINTS.md`](MANUFACTURING_CONSTRAINTS.md). `Knee_Sleeve_L`
> and `Knee_Stop_Arc_L` are **deleted outright**. The 414.7 g of §4 + §5 parts
> below does not exist in this form in any build.

| Part | Vol cm³ | Mass g | Qty | Total g | Key features |
|---|---:|---:|---:|---:|---|
| `Shoulder_Output_Hub_L/R` | 20.83 | 58.5 | 2 | 117.0 | 3 × Ø4.05 H7 dowel holes @ Ø20.4 PCD; 6 × Ø3.4 c'bore Ø6.2 @ Ø25 PCD; 6 × M4 @ Ø44 PCD × 7 deep; Ø6 cable port at r = 21 |
| `Wheel_Hub_L/R` | 12.69 | 35.7 | 2 | 71.4 | Ø37.3 H8 × 0.8 register; 3 × Ø3.4 c'bore Ø6.5 @ Ø27 PCD; 6 × M4 @ Ø46 PCD × 6 deep |
| `Cart_Upper_Eye_L/R` | 5.27 | 14.8 | 2 | 29.6 | Ø4.15 pivot bore; Ø5.0 H7 rod press bore; Ø13.4 × 4 spring spigot |
| `Cart_Lower_Eye_L/R` | 6.00 | 16.9 | 2 | 33.8 | Ø4.15 pivot bore; Ø5.6 rod bore 8.5 deep; Ø13.4 × 6 spring spigot |
| **Subtotal** | | | | **251.8** | |

## 5. Formerly-machined families, continued — was steel (ρ = 7.85 g/cm³)

*Historical masses, not a shopping list — see the §4 banner.*

| Part | Vol cm³ | Mass g | Qty | Total g | Notes |
|---|---:|---:|---:|---:|---|
| `Knee_Axle_L/R` | 2.82 | 22.1 | 2 | 44.2 | Ø10 h6 × 31.6 journal, Ø15 × 3 flange, **8.40 across flats** over the sleeve, M4 × 8 tapped outboard end |
| `Knee_Sleeve_L/R` | 2.75 | 21.6 | 2 | 43.2 | Ø16 OD × 21.6, **double-D bore 8.6 across flats** (axle 8.40) |
| `Knee_Magnet_Carrier_L/R` | 1.09 | 8.6 | 2 | 17.2 | Ø15 × 6 with M4 × 8 male stud and Ø6.1 × 2.5 magnet pocket |
| `Knee_Stop_Arc_L/R` | 2.46 | 19.4 | 2 | 38.7 | 3 mm plate, hardened; two-level arc slot; bolt circle now 30° spaced; see the design record §7 |
| `Cart_Guide_Rod_L/R` | 0.98 | 7.7 | 2 | 15.4 | Ø5 × 50, one end press fit |
| `Cart_Preload_Shim_L/R` | 0.07 | 0.55 | 8 fitted + 8 spare | 8.8 | Ø19 / Ø13.6 × 0.5 |
| **Subtotal** | | | | **162.9** | |

## 6. Purchased items

| Item | Spec | Qty | Unit g | Total g |
|---|---|---:|---:|---:|
| Shoulder actuator | **Steadywin GIM6010-8** (variant TBC — see design record §9) | 2 | ~500 | 1000 |
| Wheel actuator | **Steadywin GIM4305-10** | 2 | ~250 | 500 |
| Knee bearing | **6800-2RS, 10 × 19 × 5**, sealed | 4 | 6.5 | 26.0 |
| Main knee spring | Ø19 OD × **2.6 mm wire** × **55 mm free** × ~9.8 active coils, closed & ground, **chrome-silicon ASTM A877/A877M**, shot-peened + preset, **10.45 N/mm** | 2 | 25.3 | 50.6 |
| Cartridge pivot pin | Ø4 × 32 clevis pin + E-clip (DIN 6799-4) | 4 | 3.8 | 15.2 |
| Knee stop dowel | Ø6 × 9 hardened dowel, h6 | 2 | 2.0 | 4.0 |
| Knee angle sensor | **AS5048A** (or AS5047-class) on a 14 × 14 PCB | 2 | ~2 | 4.0 |
| Encoder magnet | Ø6 × 2.5 **diametric** NdFeB | 2 | 0.53 | 1.1 |
| Flexion bumper | Ø6.2 × 7.5 arc block, PU ~90 A | 2 | <0.1 | 0.2 |
| Extension bumper | Ø6.2 × 3.0 arc block, PU ~90 A | 2 | <0.1 | 0.2 |
| Knee thrust washer | PTFE/POM, Ø22 / Ø16.5 × 0.5 (as required) | 4 | 0.1 | 0.4 |
| Heat-set insert | Voron-style M3 × 5.0; exact owned variant remains coupon-gated | 14 active single-leg (including stand) / 28 two-leg robot | ~0.4 | track from achieved parts |
| Heat-set insert | Owner-held Kadriick M4 × 8, shoulder root; Ø5.3 ABS bore owner PASS, 2026-09-04 | 6 | — | — |
| Heat-set insert | Owner-held Kadriick M4 × 8, wheel rim joint; Ø5.3 ABS bore owner PASS, 2026-09-04 | 6 | — | — |
| Harness | Ø3.0 high-flex silicone, ≥ 400 mm coiled per shoulder | 2 | ~7 | 14.0 |

## 7. Fasteners

| Size | Where | Qty/leg | Qty/robot |
|---|---|---:|---:|
| **M3 × 8 SHCS** | shoulder plate → motor housing (Ø74 PCD); **not ×10**, which bottoms in the 4.0 mm-deep actuator thread through the 5 mm panel | 8 | 16 |
| M3 × 10 SHCS | output hub → motor output (Ø25 PCD) | 6 | 12 |
| **M3 × 10 SHCS** | cable cover → shoulder-plate inserts, installed from accessible outboard face (Ø88 PCD) | 4 | 8 |
| M4 × 10 SHCS | proximal link root → hub flange (Ø44 PCD) | 6 | 12 |
| **M4 × 8 SHCS** | wheel rim → short wheel-hub inserts (Ø46 PCD) | 6 | 12 |
| **M3 × 6 SHCS** | knee stop arc → proximal arm B inserts | 3 | 6 |
| M3 × 8 SHCS | wheel hub → motor output (Ø27 PCD) | 3 | 6 |
| M2.5 × 12 SHCS | wheel motor → distal wheel-end plate (Ø47.5 PCD) | 6 | 12 |
| M3 × 16 SHCS | encoder bracket → arm B inserts | 2 | 4 |
| M3 × 10 SHCS | chassis frame → side panels (5 per side) | — | 10 |
| **Total** | | **44 + chassis** | **98** |

Fastener mass ≈ **123 g** per robot (model figure).

The former 10-piece M3 row covered only the two proximal arm-B bosses and
omitted both shoulder-plate cover receivers, the active Mode A stand, and every
printed M4 receiving thread. It was not a purchase quantity. Use the canonical
[printed-thread map](MANUFACTURING_CONSTRAINTS.md#threaded-interfaces-in-printed-parts):
the active single-leg ABS article needs **14 owner-supplied Voron-style M3
inserts** before spares, plus **12 of the 30 owner-held Kadriick M4 × 8
inserts**: six shoulder and six wheel. The Ø5.3 ABS ladder station passed and
was promoted through Fusion on 2026-09-04. The hubs are print-ready; the link
screw-loading path and rim printability have separate holds in
[ASSEMBLY_VERIFICATION.md](ASSEMBLY_VERIFICATION.md#2026-09-04-release-checks-and-new-blockers).

**Fastener corrections retained in the current release:**

- **Knee stop arc: M3 × 8 → M3 × 6**, on a **30° bolt spacing** (was 20°) on the
  same r = 15 mm circle. *That part is now deleted — this row is kept only because
  it is why the audits exist.*
- **Cable cover, current service-path correction: M3 × 10 from outboard.** The
  four inserts now live through the 5 mm shoulder plate; the removable cover
  has clearance holes. Each screw traverses 6.5 mm of cover, engages 3.5 mm in
  brass and stops 1.5 mm before the inaccessible inboard plate face. This
  supersedes revision 2's M3 × 8 screw driven from inside the chassis.

The later delivered-actuator/rig audit adds one more active correction:
**shoulder motor housing: M3 × 10 → M3 × 8** through the 5 mm panel. The
GIM6010 housing thread is 4.0 mm deep, so ×10 bottoms instead of clamping. This
is Departure 7 in
[`beni_single_leg_rig_design_record.md`](beni_single_leg_rig_design_record.md).

Full account of both defects, with the arithmetic:
[`beni_prototype1_rev2_changes.md`](beni_prototype1_rev2_changes.md) §4.
Blind-hole geometry is now checked automatically by
`beni_lib.audit_fasteners()` and `audit_blind_holes()`.

## 8. Mass roll-up

> ### ⚠ THIS ROLL-UP IS NO LONGER VALID FOR A PRINTED BUILD
> Every figure below was computed with **metal densities**. In particular the
> **`7075-T6 machined … 251.7 g`** and **`Steel machined … 162.9 g`** lines are
> 414.6 g of parts that no longer exist in that form — the hubs and eyes are now
> printed (far lighter), and `Knee_Sleeve_L` and `Knee_Stop_Arc_L` are deleted
> entirely. Therefore **the `3290.1 g` total and the `≈ 210 g` margin are stale
> in the conservative direction** and must not be quoted for a build. They remain
> the correct as-engineered reference for Prototype 1. For a real build mass, use
> [`beni_single_leg_rig_design_record.md`](beni_single_leg_rig_design_record.md) §5.

**Read directly out of the Fusion model** (`beni_lib.mass_by_part()`), with
physical materials and densities assigned per body. Previously every body in
the model carried the default "Steel" and Fusion reported the robot at 8174 g;
this table is now the model's own answer, not a hand calculation beside it.

| Group | Mass g |
|---|---:|
| PA-CF printed (links, side panels, rim, chassis frame) | 565.7 |
| ABS printed (covers, encoder brackets, tray) | 46.4 |
| TPU tyres | 160.1 |
| 7075-T6 machined (hubs, cartridge eyes) — **STALE, now printed** | 251.7 |
| Steel machined (axles, sleeves, stop arcs, rods, shims, carriers) — **STALE, mostly deleted or bought** | 162.9 |
| Bearings (4 × 6800) | 26.0 |
| Springs (2, chrome-silicon) | 50.6 |
| Pins, dowels, magnets, PCBs, bumpers, harness | 38.4 |
| Fasteners (88 modelled screws) | 118.4 |
| **Structure + hardware subtotal** | **1420** |
| Shoulder actuators, 2 × GIM6010-8 @ ~500 g | 1000 |
| Wheel actuators, 2 × GIM4305-10 @ ~250 g | 500 |
| **Mechanical total** | **2920** |
| Battery, 4S 2200 mAh (`Battery_4S2200`) | 250 |
| Compute, IMU, power distribution, wiring (`Chassis_Electronics`) | 120 |
| **ROBOT TOTAL (Fusion)** | **3290.1 g** |
| Design mass | 3500 g |
| **Margin** | **≈ 210 g (6.0 %)** |

The 10 chassis-frame → side-panel M3 × 10 screws (≈4.6 g) are the only
fasteners in the BOM that are not modelled, so the figure above is 3290 g and
the full-hardware figure is ≈3295 g. Both actuator masses are still estimates
and must be confirmed by weighing the delivered units — a 10 % error on the
shoulder pair alone is 100 g, which is half the margin.

The swept-helical `Knee_Spring_L` body carries a derived density that preserves
the specified 25.3 g through regenerated poses. `Shoulder_Cable_Spiral_L` is a
7 g harness envelope; `Battery_4S2200` and `Chassis_Electronics` are mass
placeholders at 250 g and 120 g. All are listed in `beni_lib.MASS_OVERRIDE_G`.

### Mass properties

Mass, CoM and the full inertia tensor — the numbers controls actually needs —
are in **[`beni_prototype1_design_record.md`](beni_prototype1_design_record.md)
§14**, which is the single authoritative copy. Per-link masses and inertia
tensors for all six moving links are in `sim/beni.urdf` and
`sim/beni_inertia.json`.

Reduction targets, in order of return, if the 210 g margin needs to grow:

1. **Wheel rim + tyre = 157.3 g each (314.5 g total).** A spoked tyre section or
   a 5 mm TPU wall instead of 7 mm recovers 60–80 g.
2. **Fasteners at 123 g.** Switching the ~40 non-structural M3/M4 screws to
   aluminium or titanium recovers 40–50 g.
3. **Chassis frame at 70.3 g.** The webs are only lightly lightened; hand-work
   in the Fusion UI is worth ~25 g.
4. **Proximal link at 72.5 g each.** The arms could go from 5.0 to 4.2 mm away
   from the bearing bosses for ~20 g total.

None of these touch frozen geometry.

## 9. Assembly sequence

Order is mandatory where noted. All torque figures are starting values for
PA-CF and 7075 and should be confirmed on a scrap coupon.

### A. Sub-assemblies

**A1 — Knee bearing stack (per leg)**
1. Press `HW_Bearing_6800` into the proximal arm A pocket **from the inboard
   face**, seating it on the Ø17 lip at y = 63.7. Retaining compound.
2. Press the second `HW_Bearing_6800` into arm B **from the outboard face**,
   seating on the Ø17 lip at y = 85.3.
3. Press `Knee_Sleeve_L` into the distal link's Ø16 knee boss bore, with the
   double-D flats aligned to the sagittal plane. It protrudes 1.3 mm each side.
   > **[SUPERSEDED — skip this step.]** `Knee_Sleeve_L` is **deleted**. The Ø16
   > bore is now **printed directly into `Distal_Link_L` as Ø10**, so the axle
   > runs in the printed link. See
   > [`beni_single_leg_rig_design_record.md`](beni_single_leg_rig_design_record.md) §4.
4. Fit the two PTFE thrust washers, place the distal link into the proximal
   fork channel and align the bores.
5. **Insert `Knee_Axle_L` from the inboard side** through bearing 1, the sleeve
   and bearing 2. The double-D must engage the sleeve — do not force it.
   > **[SUPERSEDED — no double-D engagement.]** `Knee_Axle_L` is a **bought
   > Ø10 h6 hardened ground dowel pin** with no flats; the double-D was
   > deliberately deleted. The axle simply slides through. Insertion direction
   > and the anti-rotation substitute are in rig design record **§4**.
6. Screw `Knee_Magnet_Carrier_L` into the axle's M4 end with thread locker,
   0.8 N·m. Confirm free rotation and < 0.1 mm axial float.
7. Bond the Ø6 × 2.5 diametric magnet into the carrier pocket.

*This step must precede the cartridge — the axle cannot be inserted afterwards.*

**A2 — Spring cartridge (per leg)**
1. Press `Cart_Guide_Rod_L` into `Cart_Upper_Eye_L`.
2. Slide the spring over the rod onto the upper eye's Ø13.4 spigot.
3. Stack four `Cart_Preload_Shim_L` on `Cart_Lower_Eye_L`'s spigot.
4. Offer the lower eye up, compressing the spring, and align both pivot bores.
   *The assembly separates if either pin is removed — this is what makes the
   spring replaceable.*

**A3 — Wheel (per leg)**
1. Bolt `Wheel_Hub_L` to the wheel motor's output flange, **3 × M3 × 8**
   into the Ø27 PCD threads, 1.2 N·m. Register on the Ø37.3 H8 recess.
   > **[SUPERSEDED — the register is not machined any more.]** `Wheel_Hub_L` is
   > **printed**, so a Ø37.3 H8 recess cannot be held as an H8 fit. It is
   > replaced by a printed register plus **steel washers under the screws and a
   > re-torque schedule** to handle plastic creep. See
   > [`beni_rig_no_machining.md`](beni_rig_no_machining.md) §2.1 and rig design
   > record §4.
2. With the owner-passed Ø5.3 ABS receiver promoted through Fusion, install
   6 × owner-held M4 × 8 inserts while the hub is detached, from the
   corrected wheel hub's **motor face** with a depth stop. Leave 6.0 mm embedded
   and 2.0 mm projecting outboard into the mating rim's six Ø6.0 × 2.2
   reliefs. **RIM PRINT/ASSEMBLY HOLD, 2026-09-04:** resolve its unsupported
   ledges before this following assembly step. Then bolt `Wheel_Rim_L` with
   **6 × M4 × 8** on the Ø46 PCD,
   2.5 N·m. The screws engage 6.0 mm and stop 2.0 mm before the insert's
   motor-side end.
3. Stretch the TPU tyre onto the Ø96 rim seat.

*The 3 hub screws stay reachable through the rim's Ø38 central hole after the
wheel is fully assembled.*

### B. Leg build

1. With `Shoulder_Output_Hub_L` **removed**, bring
   `Chassis_Shoulder_Plate_L` in from the shoulder motor's output/front side.
   Its raised circular cable-spiral lip faces away from the motor and its flat
   panel face faces the stationary housing. The centre opening passes over the
   bare output rotor; the actuator housing stays behind the plate and does not
   pass through it. Bolt the plate to the motor's **front** face,
   **8 × M3 × 8** on the Ø74 PCD, 1.2 N·m. Do not use ×10: it puts 5 mm of screw
   into a 4.0 mm-deep actuator thread and bottoms before clamping. Heads stand
   on the y = 47 face. This
   insertion path is Fusion-verified and recorded in
   [`evidence/shoulder_assembly/2026-08-23_plate_sequence/`](evidence/shoulder_assembly/2026-08-23_plate_sequence/).
2. After the owned Voron-style M3 insert passes the Ø4.0 ABS pocket coupon, fit
   4 × M3 heat-set inserts flush in the **outboard face of
   `Chassis_Shoulder_Plate_L`**. `Shoulder_Cable_Cover_L` has clearance holes
   only. Fasten it from the accessible outboard face with 4 × **M3 × 10**;
   this joint remains serviceable after the stand or chassis frame is fitted.
3. Feed the harness out through the plate's Ø7 grommet hole at r = 29, lay in
   the spiral (≥ 400 mm, ~3 turns, inner end toward r = 21) and strain-relieve
   at the plate.
4. Bolt `Shoulder_Output_Hub_L` to the motor output: engage the **3 × Ø4 dowel
   pins first**, then 6 × M3 × 10 through the deep counterbores, 1.2 N·m.
5. Pass the harness through the hub's Ø6 port at r = 21 and strain-relieve on
   the hub's outboard face. **Both ends now have strain relief.**
6. After the same coupon gate, fit 5 × M3 heat-set inserts in the proximal
   link's arm B boss (3 for the stop arc, 2 for the encoder bracket).
7. Complete **A1** (knee stack) — proximal link + distal link joined.
8. Fit the two `HW_ClevisPin_D4x32` to install **A2** (cartridge): upper pin at
   U first, then compress and fit the lower pin at Lp. E-clips both sides.
9. Press `HW_DowelPin_D6x9` into the distal arm B at r = 30, protruding
   3.5 mm outboard. Retaining compound.
10. Bond the PU bumpers into the stop arc's outer-layer bays, then bolt
    `Knee_Stop_Arc_L` to the arm B inserts, **3 × M3 × 6**, 1.0 N·m.
    **Check by hand that the knee now stops at −8° and +27°.**
    *M3 × 6, not × 8: an × 8 bottoms out on the bore floor before it clamps.
    The three heads sit 7.765 mm apart on the 30°-spaced r = 15 circle, so a
    2.5 mm hex key reaches each of them without fouling its neighbours.*
    > **[SUPERSEDED — steps 9 and 10 both. Do not build this.]**
    > `Knee_Stop_Arc_L` is **deleted** (it was laser-cut steel) and the Ø6 dowel
    > that engaged its slot goes with it. The **+27° hard stop is now a
    > compression column of bought M5 washers** inside the spring cartridge, with
    > a printed TPU sleeve as the progressive bumper; a printed
    > `RIG_Knee_Stop_Plate_L` keeps the **−8° stop** and a +28° backup. Its
    > engagement angle must be **set by measurement**, not from a drawing,
    > because it depends on the printed eyes' achieved dead length. Full design:
    > [`beni_single_leg_rig_design_record.md`](beni_single_leg_rig_design_record.md) §8.
11. **[HUB PRINT READY / LINK SCREW-LOADING HOLD, 2026-09-04.]** Print the
    corrected Ø4.15 ABS hub with owner-passed Ø5.3 receivers. Install its six
    M4 × 8 inserts from the detached hub's outboard face using a depth stop;
    each occupies the full 8 mm flange. Repeat the unplugged motor fit.
    The final joint specifies **6 × M4 × 10** on Ø44 PCD, but two screw heads
    hit the existing link's internal wall on a straight insertion path. Keep
    the printed link and bearings pending a detached loading rehearsal; do
    not release or torque this joint before an alternate path is demonstrated.
    The six M3 hub screws remain accessible through the Ø34 root opening.
12. Bolt the wheel motor to the distal wheel-end plate, **6 × M2.5 × 12**
    inserted **from the inboard face**, 0.6 N·m. The driver cover nests in the
    plate's Ø41.5 hole and its two M2 screws stay accessible.
13. Route the wheel-motor harness up the distal link, across the knee with a
    service loop sized for −8° … +27°, and into the proximal link's channel.
14. Fit **A3** (wheel).
15. Mount the encoder PCB to `Knee_Encoder_Bracket_L`, then bolt the bracket to
    the arm B inserts, 2 × M3 × 16. Verify the **1.0 mm** magnet-to-die gap.
16. Power up the encoder and confirm it reads monotonically over −8° … +27°.

### C. Disassembly notes (design intent)

- The spring can be changed by removing **one clevis pin** — no need to touch
  the bearing stack, the shoulder or the wheel.
- The wheel motor and its connector come off with the 6 M2.5 screws while the
  leg stays assembled.
- The shoulder motor's output screws are reachable through the link's root
  access hole; the motor itself comes out after removing the link.
- The knee axle can only be withdrawn inboard, so the cartridge and the stop
  arc must come off first.

---

## 10. Recommended print order

For the active single-leg article, start with the corrected shoulder hub in
the [current print queue](README.md#current-print--convenience-link). The
remaining sequence is gated as follows:

1. Corrected `Chassis_Shoulder_Plate_L` and cable cover, if needed. Confirm the
   exact owned M3 insert coupon before heat installation.
2. `Proximal_Link_L/R` — the face-flat Ø19.10 ABS first article passed full-depth
   bearing installation and remains the build part. Use Ø19.15 for a future ABS
   reprint; it retains the bearing at easier thumb pressure. Check Ø34 root
   access during the complete single-leg rehearsal. **The six M4 root screws
   have an assembly-path hold:** rehearse loading them into the detached link
   before another link print is considered.
3. `Distal_Link_L/R` — **hold** until the real Ø10 h6 pin passes and a corrected
   tangent-source, bed-ready STL clears its dedicated DFM audit; then check the
   Ø10 angular-reference fit and Ø41.5 cover clearance.
   A clearance-fit printed ABS pin may be used only to hand-align a fully
   supported mock-up while the steel pins are in transit; it does not clear this
   gate and must not carry powered, spring, ground-contact or load testing.
4. The Ø5.3 ABS `Wheel_Hub_L` is available for detached motor fit.
   **Hold `Wheel_Rim_L/R`** until its internal ledge and outer flange have a
   verified printable solution; then rehearse rim/tyre installation.
5. ABS covers and the encoder bracket last (non-critical).

Repeat the **Ø19 bearing-seat coupon** immediately before the later two-leg
PA-CF structural build. PA-CF shrinkage decides its own compensation; do not
copy the ABS value or ream the printed seat.

*Note: the Ø16 sleeve fit named in step 2 and above is now a **Ø10** bore printed
straight into `Distal_Link_L` — `Knee_Sleeve_L` is deleted. The print order itself
is unchanged. Use `print_stl/GAUGE_Fit_Coupon.stl`, which carries both bores.*

---

### Density note

Printed-part masses assume the modelled solid volume at full material density.
A part printed with 4 walls and 30 % infill will come out roughly 25–30 %
lighter than tabulated, which is margin, not error. Structural parts
(`Proximal_Link_L`, `Distal_Link_L`, `Chassis_Shoulder_Plate_L`) should be
printed at high infill so the modelled section is actually realised, and their
tabulated mass should be treated as the real figure.
