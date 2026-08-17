# Beni Prototype 1 — Bill of Materials and Assembly Sequence

Quantities are **per robot** (two legs) unless noted. Left-hand parts are named
`*_L`; the right leg is the mirror image about Y = 0 and uses the same part
numbers with `_R`.

Masses are computed from the modelled solid volume × the density in the table.
Printed parts assume solid-equivalent density; see the note at the end.

---

## 1. Printed parts — PA-CF (carbon-filled nylon, ρ = 1.15 g/cm³)

| Part | Vol cm³ | Mass g | Qty | Total g | Print orientation |
|---|---:|---:|---:|---:|---|
| `Chassis_Shoulder_Plate_L/R` (side panel incl. motor interface) | 40.21 | 46.2 | 2 | 92.5 | flat, panel face on the bed; spiral lip prints up, no support |
| `Proximal_Link_L/R` | 63.09 | 72.6 | 2 | 145.1 | **on edge**, link axis vertical, arms in the XZ print plane so bending loads are in-plane; channel is a through-slot so no trapped support |
| `Distal_Link_L/R` | 44.98 | 51.7 | 2 | 103.5 | on edge, link axis vertical, same rationale |
| `Wheel_Rim_L/R` | 66.07 | 76.0 | 2 | 152.0 | web face down on the bed, drum prints up; no support |
| `Chassis_Frame` (centre cage, not mirrored) | 61.46 | 70.7 | 1 | 70.7 | flanges vertical, open box, no support |
| **Subtotal** | | | | **563.8** | |

## 2. Printed parts — ABS (ρ = 1.04 g/cm³)

| Part | Vol cm³ | Mass g | Qty | Total g | Print orientation |
|---|---:|---:|---:|---:|---|
| `Shoulder_Cable_Cover_L/R` | 15.49 | 16.1 | 2 | 32.2 | flange face down, wall prints up |
| `Knee_Encoder_Bracket_L/R` | 2.62 | 2.7 | 2 | 5.4 | shelf face down, posts print up |
| `Electronics_Tray` (centre, not mirrored) | 8.51 | 8.9 | 1 | 8.9 | flat |
| **Subtotal** | | | | **46.5** | |

## 3. Printed parts — TPU 95A (ρ = 1.20 g/cm³)

| Part | Vol cm³ | Mass g | Qty | Total g |
|---|---:|---:|---:|---:|
| `Wheel_Tyre_L/R` (Ø110 × 30, ID Ø96) | 67.95 | 81.5 | 2 | 163.0 |

## 4. Machined parts — 7075-T6 aluminium (ρ = 2.81 g/cm³)

| Part | Vol cm³ | Mass g | Qty | Total g | Key features |
|---|---:|---:|---:|---:|---|
| `Shoulder_Output_Hub_L/R` | 20.83 | 58.5 | 2 | 117.0 | 3 × Ø4.05 H7 dowel holes @ Ø20.4 PCD; 6 × Ø3.4 c'bore Ø6.2 @ Ø25 PCD; 6 × M4 @ Ø44 PCD × 7 deep; Ø6 cable port at r = 21 |
| `Wheel_Hub_L/R` | 12.69 | 35.7 | 2 | 71.4 | Ø37.3 H8 × 0.8 register; 3 × Ø3.4 c'bore Ø6.5 @ Ø27 PCD; 6 × M4 @ Ø46 PCD × 6 deep |
| `Cart_Upper_Eye_L/R` | 5.27 | 14.8 | 2 | 29.6 | Ø4.15 pivot bore; Ø5.0 H7 rod press bore; Ø13.4 × 4 spring spigot |
| `Cart_Lower_Eye_L/R` | 6.00 | 16.9 | 2 | 33.8 | Ø4.15 pivot bore; Ø5.6 rod bore 8.5 deep; Ø13.4 × 6 spring spigot |
| **Subtotal** | | | | **251.8** | |

## 5. Machined parts — steel (ρ = 7.85 g/cm³)

| Part | Vol cm³ | Mass g | Qty | Total g | Notes |
|---|---:|---:|---:|---:|---|
| `Knee_Axle_L/R` | 2.82 | 22.1 | 2 | 44.2 | Ø10 h6 × 31.6 journal, Ø15 × 3 flange, **8.40 across flats** over the sleeve, M4 × 8 tapped outboard end |
| `Knee_Sleeve_L/R` | 2.75 | 21.6 | 2 | 43.2 | Ø16 OD × 21.6, **double-D bore 8.6 across flats** (axle 8.40) |
| `Knee_Magnet_Carrier_L/R` | 1.09 | 8.6 | 2 | 17.2 | Ø15 × 6 with M4 × 8 male stud and Ø6.1 × 2.5 magnet pocket |
| `Knee_Stop_Arc_L/R` | 2.16 | 17.0 | 2 | 34.0 | 3 mm plate, hardened; two-level arc slot; see the design record §7 |
| `Cart_Guide_Rod_L/R` | 0.98 | 7.7 | 2 | 15.4 | Ø5 × 50, one end press fit |
| `Cart_Preload_Shim_L/R` | 0.07 | 0.55 | 8 fitted + 8 spare | 8.8 | Ø19 / Ø13.6 × 0.5 |
| **Subtotal** | | | | **158.5** | |

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
| Heat-set insert | M3 brass, 5.0 long | 10 | 0.4 | 4.0 |
| Harness | Ø3.0 high-flex silicone, ≥ 400 mm coiled per shoulder | 2 | ~7 | 14.0 |

## 7. Fasteners

| Size | Where | Qty/leg | Qty/robot |
|---|---|---:|---:|
| M3 × 10 SHCS | shoulder plate → motor housing (Ø74 PCD) | 8 | 16 |
| M3 × 10 SHCS | output hub → motor output (Ø25 PCD) | 6 | 12 |
| M3 × 10 SHCS | shoulder plate → cable cover inserts (Ø88 PCD) | 4 | 8 |
| M4 × 10 SHCS | proximal link root → hub flange (Ø44 PCD) | 6 | 12 |
| M4 × 10 SHCS | wheel rim → wheel hub (Ø46 PCD) | 6 | 12 |
| M3 × 8 SHCS | knee stop arc → proximal arm B inserts | 3 | 6 |
| M3 × 8 SHCS | wheel hub → motor output (Ø27 PCD) | 3 | 6 |
| M2.5 × 12 SHCS | wheel motor → distal wheel-end plate (Ø47.5 PCD) | 6 | 12 |
| M3 × 16 SHCS | encoder bracket → arm B inserts | 2 | 4 |
| M3 × 10 SHCS | chassis frame → side panels (5 per side) | — | 10 |
| **Total** | | **44 + chassis** | **98** |

Fastener mass ≈ **131 g** per robot.

Also required: **10 × M3 brass heat-set inserts** — 3 per leg for the knee stop
arc and 2 per leg for the encoder bracket, both blind in the proximal arm-B
boss.

## 8. Mass roll-up

Computed from the final modelled volumes (see the Fusion part list) × density.

| Group | Mass g |
|---|---:|
| PA-CF printed (links, side panels, rim, chassis frame) | 563.8 |
| ABS printed (covers, encoder brackets, tray) | 46.5 |
| TPU tyres | 163.1 |
| 7075-T6 machined (hubs, cartridge eyes) | 251.7 |
| Steel machined (axles, sleeves, stop arcs, rods, shims, carriers) | 158.5 |
| Bearings (4 × 6800) | 26.0 |
| Springs (2, chrome-silicon) | 50.6 |
| Pins, dowels, magnets, PCBs, bumpers, inserts, harness, washers | 42.9 |
| Fasteners (98 screws) | 131.0 |
| **Structure + hardware subtotal** | **1434** |
| Shoulder actuators, 2 × GIM6010-8 @ ~500 g | 1000 |
| Wheel actuators, 2 × GIM4305-10 @ ~250 g | 500 |
| **Mechanical total** | **2934** |
| Battery, 4S 2200 mAh | ~250 |
| Compute, IMU, power distribution, wiring | ~120 |
| **ROBOT TOTAL** | **≈ 3304 g** |
| Design mass | 3500 g |
| **Margin** | **≈ 196 g (5.6 %)** |

The margin is real but thin, and both actuator masses are estimates that must be
confirmed by weighing the delivered units — a 10 % error on the shoulder pair
alone is 100 g. Reduction targets, in order of return:

1. **Wheel rim + tyre = 157.5 g each (315 g total).** A spoked tyre section or a
   5 mm TPU wall instead of 7 mm recovers 60–80 g.
2. **Fasteners at 131 g.** Switching the ~40 non-structural M3/M4 screws to
   aluminium or titanium recovers 40–50 g.
3. **Chassis frame at 70.7 g.** The webs are unlightened because the helper
   library only sketches on Y-normal planes; hand-lightening them in the Fusion
   UI is worth ~25 g.
4. **Proximal link at 72.6 g each.** The arms could go from 5.0 to 4.2 mm away
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
4. Fit the two PTFE thrust washers, place the distal link into the proximal
   fork channel and align the bores.
5. **Insert `Knee_Axle_L` from the inboard side** through bearing 1, the sleeve
   and bearing 2. The double-D must engage the sleeve — do not force it.
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
2. Bolt `Wheel_Rim_L` to the hub, **6 × M4 × 10** on the Ø46 PCD, 2.5 N·m.
3. Stretch the TPU tyre onto the Ø96 rim seat.

*The 3 hub screws stay reachable through the rim's Ø40 central hole after the
wheel is fully assembled.*

### B. Leg build

1. Bolt `Chassis_Shoulder_Plate_L` to the shoulder motor's **front** face,
   **8 × M3 × 10** on the Ø74 PCD, 1.2 N·m. Heads stand on the y = 47 face.
2. Fit 4 × M3 heat-set inserts in `Shoulder_Cable_Cover_L`, then fasten the
   cover through the plate from **inside the chassis**, 4 × M3 × 10.
   *Do this before the chassis is closed.*
3. Feed the harness out through the plate's Ø7 grommet hole at r = 29, lay in
   the spiral (≥ 400 mm, ~3 turns, inner end toward r = 21) and strain-relieve
   at the plate.
4. Bolt `Shoulder_Output_Hub_L` to the motor output: engage the **3 × Ø4 dowel
   pins first**, then 6 × M3 × 10 through the deep counterbores, 1.2 N·m.
5. Pass the harness through the hub's Ø6 port at r = 21 and strain-relieve on
   the hub's outboard face. **Both ends now have strain relief.**
6. Fit 5 × M3 heat-set inserts in the proximal link's arm B boss (3 for the
   stop arc, 2 for the encoder bracket).
7. Complete **A1** (knee stack) — proximal link + distal link joined.
8. Fit the two `HW_ClevisPin_D4x32` to install **A2** (cartridge): upper pin at
   U first, then compress and fit the lower pin at Lp. E-clips both sides.
9. Press `HW_DowelPin_D6x9` into the distal arm B at r = 30, protruding
   3.5 mm outboard. Retaining compound.
10. Bond the PU bumpers into the stop arc's outer-layer bays, then bolt
    `Knee_Stop_Arc_L` to the arm B inserts, 3 × M3 × 8, 1.0 N·m.
    **Check by hand that the knee now stops at −8° and +27°.**
11. Bolt the proximal link root to the hub flange, **6 × M4 × 10** through the
    counterbores at Ø44 PCD, 2.5 N·m, using the Ø9 access holes in arm B for
    the driver. *The 6 output-hub screws remain serviceable through the link's
    Ø34 root access hole without removing the link.*
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

1. `Chassis_Shoulder_Plate_L/R` — simplest, validates PA-CF settings and the
   Ø74 hole pattern against the real motor before anything else is printed.
2. `Distal_Link_L/R` — check the Ø16 sleeve fit and the Ø41.5 cover clearance.
3. `Proximal_Link_L/R` — check the Ø19 bearing seats and the Ø34 root access.
4. `Wheel_Rim_L/R`, then the TPU tyres.
5. ABS covers and the encoder bracket last (non-critical).

Print a **Ø19 bearing-seat coupon and a Ø16 sleeve coupon first** and measure
them; PA-CF shrinkage will decide whether the seats need to be modelled
oversize or reamed.

---

### Density note

Printed-part masses assume the modelled solid volume at full material density.
A part printed with 4 walls and 30 % infill will come out roughly 25–30 %
lighter than tabulated, which is margin, not error. Structural parts
(`Proximal_Link_L`, `Distal_Link_L`, `Chassis_Shoulder_Plate_L`) should be
printed at high infill so the modelled section is actually realised, and their
tabulated mass should be treated as the real figure.
