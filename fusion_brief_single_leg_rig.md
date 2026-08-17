# Fusion Brief — Beni Single-Leg Test Rig

> ### ⚠ AMENDED 2026-08-12 — no laser-cut and no machined parts
>
> A constraint was added after this brief was written:
> **3D printed and off-the-shelf parts only. No laser cutting, no machining.**
> See **[`MANUFACTURING_CONSTRAINTS.md`](MANUFACTURING_CONSTRAINTS.md)**.
>
> Two things in this brief are superseded by it:
>
> | This brief says | Now |
> |---|---|
> | §2.2 — `Knee_Stop_Arc_L` is **"Laser-cut 3 mm steel, ~$15. Not printable"** | **Deleted.** The +27° hard stop is a compression column of bought M5 washers inside the spring cartridge, with a printed TPU sleeve as the bumper; a printed plate keeps the −8° stop and a +28° backup. Reasoning, Hertzian numbers and the verification sweep: rig design record **§8** |
> | §7 item 3 — deliver a **DXF** for `Knee_Stop_Arc_L` | **Withdrawn.** There is no laser part to cut. The retired DXFs sit in `archive_laser/` |
>
> Everything else in this brief stands. The answer to it is
> **[`beni_single_leg_rig_design_record.md`](beni_single_leg_rig_design_record.md)**,
> which also lists the **ten places the design departs from this brief** on
> numbers that did not survive recomputation — including the 300 mm rail (needs
> 400), the 49 mm drop limit (46.3), and the claim that the GAUGE coupons resolve
> conflict C2 (the shoulder coupon cannot).


**Supersedes `beni_single_leg_rig_plan.md`.** Companion reference:
`beni_rig_no_machining.md` (per-part print/buy routing and orientations).

**Build.** One left leg on a bench stand, instrumented. One GIM6010-8, one
GIM4305-10, one Teensy 4.1, breadboarded logic, bench PSU.
**No chassis, no second leg, no battery, no PCB, no custom machining.**

**Frozen inputs — do not change:** `beni_prototype1_fusion_guide_rewritten.md`
§4–§9 (kinematics), `beni_prototype1_design_record.md` §2 (motor interfaces
measured from STEP), `manufacturing/machined_parts_spec.md` (dimensions and fits,
even where the *material* is now printed).

**Where older docs disagree with this one, this wins:**

| Topic | Value here | Older docs say |
|---|---|---|
| Peak vertical force on the slide | **~53 N**, spring-limited | 150–200 N |
| Passive drop limit | **49 mm** | 60 mm or 100 mm |
| Ballast budget | **0.807 kg** (leg is 0.838 kg) | "ballast to 1.645 kg" |
| Rig hop frequency | **2-DOF, won't read 3.67 Hz** | 3.67 Hz exactly |
| Machined parts | **10 families, 9 eliminated** | "four machined parts" |

---

## 1. Purpose — why this is a dynamics rig, not a fit check

A leg bolted rigidly to a stand is a fit check. A leg whose shoulder axis rides a
vertical slide carrying half the robot's mass reproduces the real machine's
spring rate, static deflection and per-leg landing energy.

**Build one stand with two modes. Mode A is Mode B with a pin through the
carriage** — one stand, one pin, not two rigs.

| Mode | Shoulder axis | Tests |
|---|---|---|
| **A — rigid** | Pinned to the column | Actuator characterisation, encoder cal, CAN, latency, torque |
| **B — vertical slide** | On the rail, ballasted to 1.645 kg total | Spring characterisation, bounce mode, damping, drop series |

**What it can test:** knee spring preload F₀ and rate k *as built* (the spec's
30.0 N is shim-dependent — do not trust it); the leg bounce mode; active shoulder
damping; the φ_peak vs drop-height curve that sets `A_MAX` in the hard-stop CBF;
and whether a 100 mm drop really bottoms the knee out.

**What it cannot test:** balance, pitch dynamics, jumping, yaw, the clock spring,
the two-leg scissor stance. Don't try.

---

## 2. Parts — reuse, print, buy

### 2.1 Reuse as-is (STLs exist in `print_stl/`)

`Proximal_Link_L` · `Distal_Link_L` · `Wheel_Rim_L` · `Wheel_Tyre_L` ·
`Knee_Encoder_Bracket_L` · `Chassis_Shoulder_Plate_L` (5 mm PA-CF, Ø96,
8 × M3 on Ø74 PCD — **this is the motor-to-rig interface, it already exists**).

**Print `GAUGE_Shoulder_Motor_Interface.stl` and `GAUGE_Wheel_Motor_Interface.stl`
first and test-fit them on the real motors.** Conflicts C2/C3 are unresolved:
the shoulder is Ø80 × 40 *or* × 44, the wheel Ø53 × 26 *or* × 33. That is ±4 mm
and ±7 mm of motor length, and it moves your interfaces.

### 2.2 Formerly machined — now printed or bought

Full reasoning and per-part orientations in `beni_rig_no_machining.md`.

| Part | Route |
|---|---|
| `Shoulder_Output_Hub_L` | **Print** + 3 × Ø4 × 10 hardened dowel pins + M4 heat-set inserts |
| `Wheel_Hub_L` | **Print** + steel washers under every head, re-torque schedule |
| `Cart_Upper_Eye_L` / `Cart_Lower_Eye_L` | **Print**, then measure pivot-to-spigot and feed the real number to the spring model |
| `Knee_Magnet_Carrier_L` | **Print**, verify 0.05 TIR on an indicator |
| `Knee_Axle_L` + `Knee_Sleeve_L` | **Buy** one Ø10 shoulder bolt. Double-D flats deleted — see §2.3 |
| `Cart_Guide_Rod_L` | **Buy** Ø5 hardened ground shaft, cut to 50 mm |
| `Cart_Preload_Shim_L` | **Buy** Ø19/Ø13.6 × 0.5 shim washers |
| **`Knee_Stop_Arc_L`** | **Laser-cut 3 mm steel, ~$15.** Not printable — 534 N impact, 45 HRC |

**The dowel pins are not optional.** The printed hub's 3 × Ø4.05 register sees
63 MPa at proof load against PA-CF's ~40–50 MPa shear. Pressed steel pins move
the shear into metal. Print the holes Ø3.9 and ream to Ø4.05.

### 2.3 Open design question — delete the double-D flats

The 8.40 −0.02 axle flats and 8.60 +0.05 sleeve bore are the most
machining-intensive feature in the spec, and their only job is keying axle to
sleeve. **Proposal: run a plain Ø10 shoulder bolt directly in the two 6800
bearings**, with anti-rotation printed into the distal boss. The knee oscillates
±35° rather than rotating, and peak force is ~51 N.

**Confirm this works geometrically before adopting it** — it changes the knee's
construction, and the two-leg build may want the keyed version back.

### 2.4 Deleted for this build

Chassis, electronics tray, everything `_R`, the satellite CAN node (knee encoder
wires straight to the Teensy), battery/BMS/loop key (bench PSU), and **the clock
spring and its 500 mm cable** — route externally with a loose service loop
through the existing Ø6.0 harness port at r = 21.0 in the shoulder hub, and limit
the rig to ±120° in software.

**Record in the deliverables:** the clock spring gets **no validation** in this
build. It remains the highest-risk mechanical item and moves to the two-leg build.

### 2.5 Print settings — orientation, not infill

**PA-CF is 84–102 MPa in XY but only 26–50 MPa in Z.** Orientation decides
survival; 100% infill does not help and costs time and warp.

5 walls · 40% gyroid infill · 0.15 mm layers · top-of-range temp · minimal
cooling · **dry the filament.** Per-part orientations in
`beni_rig_no_machining.md` §2.

---

## 3. New parts to design

Bolt to **2020 aluminium extrusion** — don't print structure you can buy straight.

| Part | Requirement |
|---|---|
| `RIG_Base` | 2020 frame, ≥400 × 300 mm. **Clamp it to the bench** or it walks under drop loads. |
| `RIG_Column` | 2020 vertical ≥500 mm, diagonally braced. **Column and carriage compliance reads directly as false knee deflection** — stiffness here is measurement quality, and printed hubs make it worse. |
| `RIG_Rail` | **MGN12 rail, 300 mm, with TWO MGN12H blocks.** Not a round shaft (won't resist rotation about its own axis), not one block (§4.1). Rail 12 × 8 mm, M3 holes at 25 mm pitch / 10 mm end margin. M3 × 8 into M3 T-nuts; 2020 + MGN12 leaves 4 mm of extrusion each side. **300 mm gives 231 mm usable travel** (300 − 45.4 block − ~24 mm bumpers), enough for the 100 mm drop series plus sag plus release gear. |
| `RIG_Carriage` | PA-CF plate **spanning both blocks** (~80 mm centres, plate ≥140 mm), carrying `Chassis_Shoulder_Plate_L` on its 8 × M3 Ø74 PCD, plus ballast pockets. **⚠ The MGN12H's 4 × M3 holes (20 × 20 pattern) are only 3.5 mm deep** — screw length ≤ plate thickness + 3.0 mm, or you jack the carriage off the block or crack the casting. |
| `RIG_Ballast` | Pockets for steel plate or M12 washers. **Budget is 0.807 kg, not 1.645** (§4.2). Must allow ballast to be **removed** — the rig may already overshoot. Adjustable, for 1.2 / 1.645 / 2.0 kg runs. |
| `RIG_Mode_Pin` | Ø8 pin, carriage into a reamed column hole = Mode A. **Load it in shear, not bending** — Mode A takes full 11 N·m stall with no rail compliance. |
| `RIG_Drop_Release` | Pin holes at 10 mm intervals, **20 to 100 mm** above free-standing equilibrium, plus a quick-release catch. Passive limit is 49 mm (§4.3); past ~70 mm needs the landing controller live. |
| `RIG_Hard_Stops` | PU bumpers top and bottom. The carriage must not reach an end plate at speed, or crush a hand. |
| `RIG_Torque_Arm` | **200 mm lever on the shoulder hub's 6 × M4 Ø44 PCD**, bearing on a 5 kg kitchen scale. Highest-value cheap part here: published bench tests found **4.8 and 9.4 N·m against an 11 N·m rating**, and the jump needs 5.9 N·m — which reads **3.01 kgf** at 200 mm. |
| `RIG_Floor_Plate` | Flat, hard, ≥250 mm fore-aft. A shoulder sweep rolls the wheel ~77 mm; if it scrubs, every force reading is corrupt. |
| `RIG_Cable_Posts` | Two T-slot posts carrying the service loop clear of rail and wheel. |

---

## 4. The numbers that constrain the design

### 4.1 Two carriage blocks — moment, not load

**MGN12H (confirmed vendor data):** 45.4 × 27 × 13 mm, 54 g, C 3.72 kN,
C₀ 5.88 kN, **MR 38.22 N·m, MP/MY 36.26 N·m**, M3 × 3.5 deep on 20 × 20.

Vertical load is irrelevant (~16 N vs 5.88 kN). Moment binds. Lateral overhang:

```
block 13.0 + carriage 8.0 + shoulder plate 5.0  = 26.0 mm to plate outer face
+ (half-track 84.0 − plate outer y 47.0)        = 37.0 mm to wheel plane
                                                  ------
                                                   63.0 mm
```

| Load | Moment | fs, 1 block | fs, 2 blocks |
|---|---:|---:|---:|
| Impact 53 N × 63 mm | 3.36 N·m | 10.79 | 21.58 |
| **Shoulder stall 11 N·m** | **11.00** | **3.30** | 6.59 |
| Vector sum | 11.50 | **3.15** | **6.31** |

**The impact is trivial; the actuator's own reaction torque is the real load.**
One block sits at fs 3.15 — the bottom edge of HIWIN's 3.0–5.0 impact-duty band.
Two gives 6.31. Buy two because fs 3.15 is *at* the limit not inside it, **clone
rails derate ~30%** (one block → fs 2.2), and two blocks are far stiffer in pitch.

**Overhang is not the driver — don't distort the design to shrink it.** 10 mm
buys 0.5 N·m against an 11 N·m load. Prefer short stiff joints.

### 4.2 Mass — and the sprung/unsprung split

From `sim/beni_inertia.json` (sums to 3.2901 kg, matching the design record):
base 1.6137 · thigh 0.2198 · shank 0.4093 · wheel 0.2091.

```
half robot                        1.6451 kg
− one leg (thigh+shank+wheel)     0.8382
                                  ------
carriage + plate + motor + ballast 0.8069 kg
```

**The GIM6010-8 alone is 388–500 g of that** (C4 unresolved — weigh it). With a
5 mm plate ~40 g and two blocks 108 g, the printed carriage plus ballast has
~0.15–0.27 kg. **The rig may exceed 1.645 kg with zero ballast** — design for
removal, and thin or pocket the carriage rather than accept a heavier slide.

**⚠ Then the subtlety.** The knee spring sits between thigh and shank, so
**shank + wheel = 0.618 kg is unsprung — 38% of the leg.** This is a 2-DOF
system with two modes. **A pluck test reading other than 3.67 Hz is not a build
error.** Report the measured value and the mass split; the control model gets
corrected from the measurement. That is the point of the rig.

### 4.3 Spring force and the drop ceiling

The knee spring is the softest element in the load path, so **it caps
transmissible force.** From the guide's checkpoints (17.2 N at φ=0, 51.5 N at
+25° over 46.1 mm), the per-leg effective wheel rate is **k = 744 N/m** —
consistent with `04_firmware.md`'s 0.71–0.80 N/mm. Energy balance ½kx² = mg(h+x):

| Drop | Compression | Peak force | |
|---:|---:|---:|---|
| 20 mm | 29.5 mm | 38.1 N | ok |
| **49 mm** | **46.1 mm** | **50.4 N** | **passive limit, reaches +25°** |
| 100 mm | 65.9 mm | 65.1 N | bottoms out |

**Peak force is ~51 N at design point, ~53 N against the stop.** Take **49 mm**
as the planning limit — it uses the measured wheel rate directly and is more
conservative than the 60 mm energy-method figure in `04_firmware.md`.

### 4.4 Checks before releasing CAD

1. Sweep the knee −8° → +27° at nominal shoulder and reproduce guide §4:
   **φ = +25° → 46.1 mm vertical, 24.0 mm fore-aft.** Mismatch means your model
   is wrong, not the table.
2. Sweep the shoulder ±120°; the service loop must not foul rail, column,
   carriage or wheel.
3. Wheel clears the floor plate through the **whole** Mode B travel, including
   full knee extension at the top of the rail.
4. Mass-properties the carriage: total, ballast to reach 1.645 kg, **and the
   sprung/unsprung split.**
5. Torque arm can't hit the column at any angle you intend to load.
6. Re-verify the 63 mm stack-up (§4.1) against the real assembly — it assumes an
   8 mm carriage plate.

---

## 5. Electronics

**Two CAN buses** — the actuators speak different protocols (GIM6010-8 is ODrive
CANSimple; the SDC101 is proprietary SteadyWin/MIT). The Teensy 4.1 has three
controllers, so this is free.

```
Bench PSU 20 V, current-limited ─[e-stop]─[brake chopper]─┬─ GIM6010-8  ─CAN1─┐
   (NOT a battery)                                        └─ GIM4305-10 ─CAN2─┤
   Teensy 4.1 ── 2 × TCAN3414 (3.3 V) ──────────────────────────────────────┘
        ├── ICM-42688-P on SPI  (on the CARRIAGE, not the column)
        ├── AS5048A at the knee, SPI direct
        └── microSD logging at 1 kHz, onboard socket
```

**Five things that will bite:**

1. **500 kbps, not 1 Mbps.** Breadboards have no controlled impedance and can't
   hold the ≤30 mm stub rule. At 500 k a frame is ~270 µs → 54% load on 2
   frames/ms. The 1 Mbit three-bus design is a two-leg problem.
2. **Breadboard logic only.** Motor current gets soldered 16–18 AWG straight from
   the PSU. Breadboard rails won't carry 10 A and contact resistance will lie to
   your current sensing.
3. **The Teensy is 3.3 V and not 5 V tolerant.** A 5 V SN65HVD230 breakout kills it.
4. **A bench PSU cannot sink regen.** Every Mode B drop pushes energy back and the
   supply just lets the bus rise. **The 5 Ω brake chopper + TLV3011 is mandatory
   here** (`electronics/01_power_and_battery.md` §7.2). Build it before the first
   drop. **Re-scale its thresholds for a 20 V bus** — the published 26.5 V on /
   25.6 V off is set for the 25.2 V pack and would never fire here. Target ~21.5 V
   on / ~20.8 V off, and confirm the hysteresis exists or the FET runs linear.
5. **Run at 20 V, not 24 V.** The wheel driver's max bus voltage is unconfirmed
   (blocker B1: sources say 12–24, 12–36 and 12–48 V). Costs nothing here and
   protects the only wheel driver you own.

---

## 6. Test order — each step gates the next

Full gate criteria in `electronics/06_logging_and_bringup.md`.

| # | Mode | Test | Gate |
|---|---|---|---|
| 1 | bench | Teensy: 2 × CAN loopback, IMU 8 kHz, SD 240 kB/s for 10 min | zero dropped frames |
| 2 | A | Shoulder encoder cal; **torque arm sweep 0.1 → 6 N·m** | within 20% of Kt·I; **≥5.9 N·m reachable** |
| 3 | A | Phase R with a milliohm meter; **weigh and caliper both motors** | resolves C2, C3, C4, C7 |
| 4 | A | **Loop latency**: GPIO at IMU-sample and torque-write, scoped | **<8 ms end-to-end** |
| 5 | A | Knee sweep −8° → +27° by hand, log AS5048A | monotonic, no wrap or dropout |
| 6 | A | **Spring characterisation**: known masses on the wheel, φ vs force | F₀ and k measured, replacing the assumed 30.0 N |
| 7 | B | Static release at equilibrium, measure ride height | matches predicted φ within 1° |
| 8 | B | **Pluck test**: displace 10 mm, release, log φ | 3–4 Hz, ζ ≈ 0.01. **Record it; don't expect 3.67** (§4.2) |
| 9 | B | Repeat with shoulder damping injection | **ζ → 0.3** |
| 10 | B | **Drop series, 20 mm up in 10 mm steps** | φ_peak < +24°; **extrapolate before every step up.** Passive limit ~49 mm |
| 11 | B | Repeat with the landing controller live | 100 mm without hitting +24° |

**Steps 1–9 can run without `Knee_Stop_Arc_L`. Do not run one drop in step 10
without it fitted.**

**Step 10 is the one that changes the project.** The old brief claimed a 100 mm
drop has ~10% margin; both the energy method and the spring-rate method say it
bottoms out. If the measured curve confirms it, the spring or the jump target
changes — and finding out here costs an afternoon instead of a robot.

**Never extrapolate past the last measured point.** If the trend hits +24° at
40 mm, stop at 40 mm.

---

## 7. Deliverables

1. Fusion assembly, both modes, reused parts in place, §4.4 checks verified.
2. STLs for the new `RIG_*` parts **and** the re-routed formerly-machined parts,
   with print orientation and settings stated per part (§2.5).
3. **DXF for `Knee_Stop_Arc_L`**, ready to upload for laser cutting. Slot ends
   ~0.3 mm undersize to file to fit.
4. Purchase list: extrusion cut lengths, **MGN12 rail 300 mm + 2 × MGN12H
   blocks**, M3 × 8 rail screws + T-nuts, block screws sized to the 3.5 mm thread
   depth, 3 × Ø4 × 10 dowel pins, M4 heat-set inserts, Ø10 shoulder bolt, Ø5 × 50
   hardened shaft, shim washers, steel washers, PU bumpers, ballast.
5. Mass-properties report: total on the slide, ballast to reach 1.645 kg, **and
   the sprung/unsprung split.** If it exceeds 1.645 kg unballasted, say so — that
   is a design change, not a rounding error.
6. **A recommendation on §2.3** (delete the double-D flats, shoulder bolt direct
   in the bearings) — confirmed geometrically, or rejected with a reason.
7. A short note on what this rig **cannot** test: balance, pitch dynamics,
   jumping, yaw, the clock spring, the two-leg scissor stance.

---

## 8. Known-unresolved, outside CAD scope but gating the build

- **B1** — wheel-driver max bus voltage. Run at 20 V until Steadywin answers.
- **C2 / C3** — motor dimensions, ±4 mm and ±7 mm. **Print the GAUGE coupons.**
- **C4** — actuator masses (388/150 g vs 500/250 g). Weigh them; it decides
  whether the ballast budget in §4.2 is comfortable or negative.
- **Creep.** Printed joints relax silently. **Re-torque after the first hour,
  then periodically**, and inspect the printed hub's dowel holes for ovalisation
  after every drop session.
