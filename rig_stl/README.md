# Rig parts to print

Exported from the verified `Beni_SingleLegRig` assembly at High mesh refinement.
All STLs are in millimetres and sit at their **assembly coordinates**, not
centred on the origin — every slicer will drop them to the bed and centre them.

Companion: `../beni_single_leg_rig_design_record.md`.

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

Material is **PA-CF** for everything in this directory unless noted.

---

## Print in this order

### 0. First — `../print_stl/GAUGE_Fit_Coupon.stl`
Unchanged from the robot build, and it still de-risks every print here. Six
critical bores in one 26 × 92 × 8 bar; measure them and set the slicer's hole /
X-Y size compensation from the result. PA-CF typically comes out 0.1–0.25 mm
undersize on holes.

The two `GAUGE_*_Motor_Interface.stl` coupons are also worth printing — both were
re-measured against design record §2 and every feature agrees. Note that the
**shoulder coupon is only 9.5 mm long** and cannot resolve conflict C2 (motor
length 40 vs 44 mm); see the design record §2.4.

### 1. `RIG_Carriage.stl` — the part everything else hangs on
90.2 cm³, **103.7 g**, 154 × 170 × 8.

- **Orientation: plate face flat on the bed.** Bending from the 63 mm overhang
  then stays in the print plane, and the eight block-screw counterbores print as
  pockets rather than needing support.
- No support anywhere. The Ø82 central bore and every hole is a through-feature.
- **Check before fitting:** the five M3 insert bores must line up with
  `Chassis_Shoulder_Plate_L`'s existing frame-bolt holes at (−60, −18),
  (−60, 48), (−60, 62), (30, 48), (30, 62). Verified concentric in CAD; confirm
  on the print before installing inserts.
- Install M3 heat-set inserts (5.0 mm long) with a depth-stopped tip: the bores
  are 5.0 mm deep in an 8 mm plate, leaving a 3 mm floor.

### 2. `RIG_Index_Bar.stl`
114.3 cm³, 131.4 g. **Flat on the bed, station holes vertical** — the Ø8 pin
bears across layers, not along them. 17 stations at 10 mm pitch. Not on the
slide, so its mass does not matter.

### 3. `RIG_Floor_Plate.stl`
260 × 60 × 6, flat on the bed. **A 6 mm aluminium plate is the better part** if
you have one — the wheel rolls on this and the brief wants it flat and hard. The
STL is provided so the rig can be finished without a metal supplier.

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

### 8. `RIG_Ballast_Pot.stl` × 2
Open side up, no support. Fill with steel shot, airgun BBs or a jar of M4 nuts and
weigh on a kitchen scale — 344 g of capacity across the pair, and only ~37 g is
needed to hit 1.645 kg with a 500 g motor.

---

## `reroute/` — formerly machined, now printed

These five were 7075 or steel in `manufacturing/machined_parts_spec.md`. Routing
per `beni_rig_no_machining.md` §3. **Print one of each and dry-fit before
committing to a second set.**

| File | Was | Orientation | The thing that will bite |
|---|---|---|---|
| `Shoulder_Output_Hub_L.stl` | 7075-T6 | **flange face flat on the bed** | Torque then loads the bolt circle in XY and the three dowel holes see shear **across** layers. **Print the Ø4.05 holes at Ø3.9 and ream to Ø4.05**, and press in three Ø4 × 10 hardened dowel pins — without them the printed register sees 63 MPa against PA-CF's ~40–50 MPa shear at proof load. Use M4 heat-set inserts **5.8 mm long**, not 8 mm: the flange is 8 mm thick and an 8 mm insert breaks through. |
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

## What you can validate before the motors arrive

- Every bore fit and the slicer compensation (the fit coupon).
- Both motor bolt patterns and the output-side dowel/screw patterns (the gauges).
- That the carriage's five insert bores match the panel, and its eight block
  screws match the MGN12H 20 × 20 pattern.
- The whole knee stack in its **new** form: Ø10 dowel pin straight through both
  6800s, pressed into the printed distal boss, collar on, magnet carrier on.
- **Assembly order.** The eight carriage-to-block screws are captive under the
  panel, so the order is: carriage → blocks → panel + motor. Confirm you can
  reach them all before the motor goes on.
