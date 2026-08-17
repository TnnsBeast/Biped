# Beni Prototype 1 — what to print before the motors arrive

Everything here is exported straight from the verified Fusion assembly
(`Beni_Prototype1`) at High mesh refinement. All STLs are in millimetres and sit
at their assembly coordinates, not centred on the origin — every slicer will
drop them to the bed and centre them for you.

Chiral parts are exported **left-hand only**. Mirror in the slicer for the
right-hand part; there is no separate `_R` file.

---

## Print in this order

### 1. `GAUGE_Fit_Coupon.stl` — print this first, before anything else
14 cm³, ~25 min, PA-CF (the material you'll actually use for the links).

A 26 × 92 × 8 bar with six through-bores, one for every critical fit in the
robot:

| bore | what it is | target fit |
|---:|---|---|
| Ø19.0 | 6800 bearing seat, proximal arms | light press — bearing enters with thumb pressure, no rock |
| Ø16.0 | knee steel sleeve into the distal boss | light press |
| Ø10.0 | knee axle reference | slip, no rock |
| Ø6.0 | knee-stop dowel seat | light press |
| Ø4.05 | shoulder-output dowel (reamed in the metal hub) | slip |
| Ø4.0 | M3 heat-set insert bore | insert seats flush without splitting the wall |

Measure all six with pin gauges or calipers, then set your slicer's **hole /
X-Y size compensation** from the result. PA-CF typically comes out 0.1–0.25 mm
undersize on holes.

**This one print de-risks every other print.** Don't skip it — the Ø19 bearing
seats and the Ø16 sleeve bore are the two fits that will otherwise waste a
whole link.

### 2. The two motor stand-ins — this is what lets you test-fit without motors
PLA is fine; these are gauges, not parts.

- **`GAUGE_Shoulder_Motor_Interface.stl`** (31 cm³, Ø78 × 10)
  Replicates the GIM6010-8's mating geometry exactly as measured from the STEP:
  the Ø78 front face, **8 × Ø2.5 pilots on the Ø74 PCD** (tap M3), the Ø46 rotor
  step, the Ø34 pilot boss, the output face 3.5 mm proud with **6 × Ø2.5 pilots
  on the Ø25 PCD** and **3 × Ø4.05 dowel holes on the Ø20.4 PCD**.
  Press three Ø4 × 8 steel dowels into those holes and you have a working
  stand-in for the motor's anti-rotation pins.

- **`GAUGE_Wheel_Motor_Interface.stl`** (31 cm³, Ø53 × 33)
  Replicates the GIM4305-10: the full Ø53 × 33 envelope, **6 × Ø2.0 pilots on
  the Ø47.5 PCD** (tap M2.5), the Ø40.4 driver-cover boss, the bearing gland,
  and the output flange Ø37 at the far end with **3 × Ø2.5 on the Ø27 PCD**.
  Note it is the *full length* on purpose — use it to confirm the wheel drum
  clears the motor and that the driver cover nests in the distal plate's Ø41.5
  pocket.

### 3. `check_prints/` — PLA stand-ins of the metal parts
Print these in PLA **before ordering any machining**. They let you dry-assemble
the entire knee and shoulder stack and confirm every hole pattern lines up.

| file | real material | why print it |
|---|---|---|
| `Shoulder_Output_Hub_L.stl` | 7075-T6 | check the 3-dowel + 6 × M3 pattern against the shoulder gauge, and that the link's Ø34 root access bore lines up with the M3 counterbores |
| `Wheel_Hub_L.stl` | 7075-T6 | check the Ø37.3 register and the 3 × M3 against the wheel gauge |
| `Cart_Upper_Eye_L.stl`, `Cart_Lower_Eye_L.stl` | 7075-T6 | check the cartridge sits in the 20 mm spring channel and the Ø4 pins line up |
| `Knee_Stop_Arc_L.stl` | 3 mm steel | check the arc slot lands on the Ø6 dowel at −8° and +27° |
| `Knee_Sleeve_L.stl`, `Knee_Axle_L.stl`, `Knee_Magnet_Carrier_L.stl` | steel | check the double-D key engages and the axle inserts from inboard |

A printed Ø10 axle will not survive load, but it proves the **assembly order** —
which is the thing most likely to be wrong, and the thing that is most expensive
to discover after the metal is cut.

### 4. Structural PA-CF parts — only after step 1
Print one of each first and dry-fit before committing to the second set.

| file | vol cm³ | footprint | orientation | support |
|---|---:|---|---|---|
| `Chassis_Shoulder_Plate_L.stl` | 40.2 | 120 × 120 × 9 | flat, panel face on the bed | none |
| `Distal_Link_L.stl` | 45.0 | 137 × 122 × 30 | **on edge**, link axis vertical | none |
| `Proximal_Link_L.stl` | 63.1 | 142 × 127 × 32 | **on edge**, link axis vertical | none |
| `Chassis_Frame.stl` | 61.5 | 110 × 92 × 84 | flanges vertical, open box up | none |

"On edge" matters for the links: it puts primary bending loads in the print
plane and makes the 20 mm spring channel a through-slot, so nothing needs
internal support. Every part in this design is single-shell — there are no
enclosed cavities anywhere, so no print should ever need trapped support.

Print the structural parts at **high infill** (≥ 60 %, 4+ walls). The mass
figures in the BOM assume the modelled section is actually realised; a
lightly-infilled 5 mm knee arm is not the part that was analysed.

### 5. Wheel and covers — last, nothing depends on them
| file | material | note |
|---|---|---|
| `Wheel_Rim_L.stl` | PA-CF | web face down, drum prints up |
| `Wheel_Tyre_L.stl` | TPU 95A | Ø110 × 30; stretches onto the Ø96 rim seat |
| `Shoulder_Cable_Cover_L.stl` | ABS | 4 × M3 heat-set inserts |
| `Knee_Encoder_Bracket_L.stl` | ABS | 2 × M3 heat-set inserts |
| `Electronics_Tray.stl` | ABS | flat panel |

---

## What you *can* validate before the motors arrive

- Every bore fit and the slicer compensation (step 1).
- Both motor bolt patterns and the output-side dowel/screw patterns (step 2).
- The complete knee joint: bearing seats, sleeve, axle insertion direction,
  thrust washers, and that the axle **can only go in from inboard**.
- The spring cartridge in the 20 mm channel, both pivot pins, and that removing
  one clevis pin frees the spring.
- The knee stop: that the Ø6 dowel reaches the steel slot ends at −8° and +27°,
  and that the PU bumper starts touching around +20°.
- Driver access to all 32 audited screws.
- That the wheel drum clears the wheel motor and the distal plate.

## What you cannot validate yet

- Actual spring rate and preload — needs the real spring on a press.
- Anything load-bearing. PLA stand-ins prove geometry, not strength.
- Motor bolt-thread engagement depth, and the exact GIM6010-8 variant, bus
  voltage and driver configuration (still to confirm with the supplier).
- Harness bend radius in the shoulder clock-spring cavity — needs the real
  Ø3.0 high-flex cable.

## Hardware worth ordering now so it's on the bench for the dry fit

4 × 6800-2RS bearings · 4 × Ø4 × 32 clevis pins + E-clips · 2 × Ø6 × 9 hardened
dowels · 3 × Ø4 × 8 dowels per shoulder gauge · 10 × M3 brass heat-set inserts
(5 mm) · M3/M4/M2.5 SHCS assortment · 4 × Ø22/Ø16.5 × 0.5 PTFE thrust washers.
