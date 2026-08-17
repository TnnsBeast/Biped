# Beni — Single-Leg Test Rig: Brief for the Fusion Agent

> **⛔ SUPERSEDED — 2026-08-11. Do not hand this to the fusion agent.**
> Replaced by **`fusion_brief_single_leg_rig.md`**, which carries the corrected
> force analysis (~53 N not 150–200 N), the 49 mm passive drop limit, the real
> ballast budget (0.807 kg), and the no-machining part routing as settled facts
> rather than corrections layered on top of superseded text.
> Kept only as working history.
>
> Also note: **no laser-cut and no machined parts** are used any more
> (`MANUFACTURING_CONSTRAINTS.md`), which supersedes every machining and
> laser-cutting reference below.

**Purpose.** Build one left leg on a bench stand and instrument it. One
GIM6010-8, one GIM4305-10, one Teensy 4.1, breadboarded logic, bench PSU. No
chassis, no second leg, no battery, no PCB.

**Read first:** `beni_prototype1_fusion_guide_rewritten.md` §4–§9 (frozen
kinematics — do not change them), `beni_prototype1_design_record.md` §2
(motor interfaces measured from STEP), `manufacturing/machined_parts_spec.md`
§1–§4, and `electronics/04_firmware.md` §1 (four numbers in the old brief that
are wrong).

**This document supersedes those on four points.** Where they disagree, this wins:

| Topic | Superseded by |
|---|---|
| Peak vertical force on the slide | §4.1 — **~53 N**, spring-limited. Not 150 N or 200 N. |
| Passive drop limit | §4.1 — **49 mm**, from the measured wheel rate |
| Ballast mass | §4.2 — the leg is **0.838 kg** already; ballast budget is 0.807 kg |
| Hop frequency on the rig | §4.2 — **2-DOF**, will not read exactly 3.67 Hz |

**Unresolved and out of scope for CAD, but they gate the build:** blocker B1
(wheel-driver max bus voltage) and conflicts C2/C3/C4 (motor dimensions and
masses) in `electronics/05_open_questions.md`. **Print the two `GAUGE_*` coupons
and test-fit them on the real motors before finalising any interface** — C2/C3
are ±4 mm and ±7 mm of motor length respectively.

---

## 1. The one design decision that matters

A leg bolted rigidly to a stand is a fit-check. **A leg whose shoulder axis
rides a vertical slide carrying half the robot's mass is a dynamics rig**, and
the arithmetic says it reproduces the real machine exactly:

```
Full robot:  k_eff 1747 N/m,  m 3.290 kg  →  ω_hop = √(1747/3.290) = 23.05 rad/s = 3.67 Hz
Per leg:     k_eff  873.5     m 1.645 kg  →  ω_hop = √(873.5/1.645) = 23.05 rad/s = 3.67 Hz
```

**The stiffness and static deflection are exact; the dynamics are close but not
identical.** One leg carrying 1.645 kg has the same spring rate, the same static
deflection and the same landing energy per leg as the assembled robot. The
3.67 Hz figure assumes a single mass on a single spring — **the real rig has
0.618 kg of shank and wheel below the spring (§4.2), so it is a 2-DOF system and
the measured mode will sit somewhat off 3.67 Hz.** That is a feature: the rig
measures the truth and the control model gets corrected. So this rig can
legitimately test:

- knee spring preload F₀ and rate k **as built** — every contact threshold and
  every row of the landing-energy table scales with these, and preload is
  shim-dependent (design record §1.2 assumes 30.0 N; **do not trust it**)
- the **3.67 Hz bounce mode**, which `electronics/04_firmware.md` §3.3 calls the
  largest control risk in the project
- **active shoulder damping** — c_φ ≈ 0.192 N·m·s/rad per leg, and whether it
  actually pulls ζ from 0.01 to 0.3
- the **φ_peak vs drop-height curve** (bring-up Stage 5), which is how `A_MAX`
  in the hard-stop CBF gets set
- **the corrected landing-energy result**: a 100 mm free drop bottoms the knees
  out. Passive capacity is ~49 mm. This rig is how you confirm that before the
  robot exists.

It cannot test balance, pitch dynamics or jumping — those need two legs and a
free body. Don't try.

**So: build the stand with two modes.**

| Mode | Shoulder axis | Tests |
|---|---|---|
| **A — rigid** | Pinned to the column | Actuator characterisation, encoder cal, CAN, latency, torque measurement |
| **B — vertical slide** | On a linear rail, ballasted to 1.645 kg | Spring characterisation, bounce mode, damping, drop series |

Mode A is Mode B with a pin through the carriage. Design it that way — one
stand, one pin, not two rigs.

---

## 2. Parts reused unchanged

Do not redesign these. **STLs that exist in `print_stl/`:**
`Proximal_Link_L` · `Distal_Link_L` · `Wheel_Rim_L` · `Wheel_Tyre_L` ·
`Knee_Encoder_Bracket_L` · `Chassis_Shoulder_Plate_L` (5 mm PA-CF, Ø96, 8 × M3
on Ø74 PCD — **reuse as the motor-to-rig interface**, it already exists).

Also useful: `GAUGE_Shoulder_Motor_Interface.stl` and
`GAUGE_Wheel_Motor_Interface.stl` — **print these first and test-fit them on the
real motors before committing to any rig geometry.** They exist precisely to
catch the C2/C3 dimension conflicts (Ø80 × 40 vs × 44; Ø53 × 26 vs × 33).

**⚠ Parts referenced by this plan that have NO STL and NO CAD yet:**

**`manufacturing/machined_parts_spec.md` lists TEN machined families, not four**,
and six are on this rig's critical path. **`beni_rig_no_machining.md` resolves
all ten into printed parts, bought hardware, or one laser-cut plate** — read it
before modelling any of them. Summary:

| Part | Route |
|---|---|
| `Shoulder_Output_Hub_L` | **Print** + 3 × Ø4 dowel pins + M4 heat-set inserts |
| `Wheel_Hub_L` | **Print** + steel washers, re-torque schedule |
| `Cart_Upper_Eye_L` / `Cart_Lower_Eye_L` | **Print**, measure, feed real dims to the spring model |
| `Knee_Magnet_Carrier_L` | **Print**, verify 0.05 TIR on an indicator |
| `Knee_Axle_L` / `Knee_Sleeve_L` | **Buy** a shoulder bolt; double-D flats deleted |
| `Cart_Guide_Rod_L` / `Cart_Preload_Shim_L` | **Buy** stock shaft and shim washers |
| **`Knee_Stop_Arc_L`** | **Laser-cut 3 mm steel, ~$15. Not printable** — 534 N impact at 45 HRC |

**Print rules that matter more than infill:** 5 walls, 40% infill, 0.15 mm
layers, dry filament. **PA-CF is 84–102 MPa in XY but only 26–50 MPa in Z**, so
**orientation decides survival — 100% infill does not.** Per-part orientations
are in `beni_rig_no_machining.md`.

**Steps 1–9 can run without the stop arc. Do not run a single drop test in step
10 without it fitted.**

Also reused, not printed: the knee bearing stack (10 mm axle, 2 × 6800 sealed,
double shear) and the spring itself (OD 19, wire 2.6, free length ~55 mm,
~10.45 N/mm, chrome-silicon — A228 music wire acceptable for early prototypes).

## 3. Parts deleted for this build

| Deleted | Why |
|---|---|
| `Chassis_Frame`, `Electronics_Tray` | No chassis |
| Second leg, everything `_R` | One actuator of each |
| **The clock spring and its 500 mm cable** | **Biggest simplification available.** With no chassis there is nothing to hide the cable inside. Route it externally with a loose service loop through the existing Ø6.0 harness port at r = 21.0 in `Shoulder_Output_Hub_L`. Limit the rig to ±120° in software and the loop handles it trivially. |
| `Shoulder_Cable_Cover_L` | Follows from the above |
| Satellite CAN node | The knee encoder wires straight to the Teensy — see §5 |
| Battery, BMS, loop key | Bench PSU |

**Consequence to record:** the clock-spring design (CR-2, 500 mm free spiral,
5% wrap margin, PTFE slip sheets) gets **no validation in this build.** It is
still the highest-risk mechanical item in the project and it moves to the
two-leg build. Say so in the deliverables.

---

## 4. Parts to design

Bolt everything to **2020 aluminium extrusion**. Don't print structure you can
buy straight, and the T-slots give you free height adjustment.

| Part | Requirement |
|---|---|
| `RIG_Base` | 2020 frame, ≥400 × 300 mm footprint. **Must be clamped to the bench** — 1.6 kg arrested from a 100 mm drop is ~53 N peak (spring-limited) into the frame and it will walk. |
| `RIG_Column` | 2020 vertical, ≥500 mm, braced diagonally. Column deflection shows up directly as false knee deflection, so stiffness here is a measurement-quality issue. Must be tall enough for the rail plus mounting: a **300 mm rail gives 231 mm of usable travel** (300 − 45.4 block − ~24 mm of bumper and end clearance), which covers the 120 mm drop series plus equilibrium sag plus release hardware. 400 mm rail → 331 mm travel if you want headroom. |
| `RIG_Rail` | **MGN12 profile rail, 300 mm, with TWO MGN12H blocks** — not a round shaft, and not one block. See §4.1 for the moment arithmetic that forces the second block. A round shaft with LM bearings does not constrain rotation about its own axis, and the shoulder's reaction torque (up to ~11 N·m stall) would spin the carriage. Rail: 12 mm wide × 8 mm tall, M3 holes on **25 mm pitch, 10 mm end margin**. Mount to the 2020 column with M3 × 8 into M3 T-nuts; a 2020 + MGN12 pairing leaves **4 mm of extrusion each side**. |
| `RIG_Carriage` | Printed PA-CF plate **spanning both MGN12H blocks** (block centres ~80 mm apart; plate ≥140 mm long). Carries `Chassis_Shoulder_Plate_L` on its existing 8 × M3 Ø74 PCD, plus ballast pockets. **Mass-budget it** — the carriage counts toward the 1.645 kg. **⚠ The MGN12H block's 4 × M3 holes (20 × 20 mm pattern) are only 3.5 mm deep.** Screw length must not exceed `plate thickness + 3.0 mm`. An M3 × 12 into an 8 mm plate bottoms out and will either jack the carriage off the block or crack the casting. |
| `RIG_Ballast` | Pockets for stacked steel plate or M12 washers. **Target is a 1.645 kg TOTAL, of which the leg is already 0.838 kg — so the carriage + plate + ballast budget is 0.807 kg, not 1.645.** See §4.2. Make it adjustable — you will want 1.2 and 2.0 kg totals to confirm ω_hop ∝ 1/√m. |
| `RIG_Mode_Pin` | Ø8 pin through carriage into a reamed hole in the column = Mode A. Pin out = Mode B. |
| `RIG_Drop_Release` | Graduated pin holes up the column at **10 mm intervals from 20 to 100 mm** above the free-standing equilibrium height, plus a quick-release catch. Stage 5 is a 10 mm-step series and a repeatable release height is the whole experiment. **The passive limit is a 49 mm drop** (§4.1) — the spring reaches +25° there. Holes past ~70 mm are only usable in step 11 with the landing controller live, and 100 mm is the ceiling worth building. |
| `RIG_Hard_Stops` | Polyurethane bumpers top and bottom of the rail travel. The carriage must not be able to reach either end plate at speed, and must not be able to crush a hand. |
| `RIG_Torque_Arm` | **200 mm lever, bolts to `Shoulder_Output_Hub_L`'s 6 × M4 Ø44 PCD**, other end bears on a 5 kg kitchen scale. This is the highest-value cheap part on the list: published bench tests measured the GIM6010-8 at **4.8 N·m and 9.4 N·m against an 11 N·m rating**, and the jump needs 5.9 N·m. At 200 mm, 5.9 N·m reads 3.01 kgf. |
| `RIG_Floor_Plate` | Flat, hard, ≥250 mm fore-aft. A shoulder sweep rolls the wheel ~77 mm fore-aft, so the wheel needs room to roll or it scrubs and corrupts every force reading. |
| `RIG_Cable_Posts` | Two T-slot posts to carry the service loop clear of the rail and the wheel. |

### 4.1 Why two carriage blocks — the moment arithmetic

**Vendor figures, confirmed 2026-08-10.** MGN12H block 45.4 × 27 × 13 mm, 54 g;
C = 3.72 kN, C₀ = 5.88 kN; **MR 38.22 N·m, MP/MY 36.26 N·m each.**
Block M3 holes on a 20 × 20 mm pattern, **3.5 mm deep.**

Vertical load is irrelevant — the whole rig is ~16 N against a 5.88 kN static
rating. **The binding constraint is moment**, and the lateral overhang is:

```
MGN12H block height              13.0 mm
RIG_Carriage plate                8.0     (assumed — recompute if changed)
Chassis_Shoulder_Plate_L          5.0     (design record §3)
                                 -----
rail plane → plate outer face    26.0 mm
plate outer face → wheel plane   37.0     (half-track 84.0 − plate outer y=47.0)
                                 -----
TOTAL lateral overhang           63.0 mm
```

**The peak vertical force is set by the spring, not by an impulse estimate.** The
knee spring is the softest element in the load path, so it caps the force it can
transmit. From the guide §4/§6 checkpoints (17.2 N at φ = 0, 51.5 N at +25°
over 46.1 mm of wheel travel), the per-leg effective wheel rate is
**k = 744 N/m (0.74 N/mm)** — matching `04_firmware.md`'s 0.71–0.80 N/mm.
Energy balance `½kx² = mg(h+x)` gives:

| Drop | Compression | Peak force | |
|---:|---:|---:|---|
| 20 mm | 29.5 mm | 38.1 N | ok |
| **49 mm** | **46.1 mm** | **50.4 N** | **passive limit — reaches +25°** |
| 100 mm | 65.9 mm | 65.1 N | bottoms out |

**Peak force at the +25° design point is ~51 N, and ~53 N against the hard
stop — not the 200 N an earlier pass assumed.** That estimate divided energy by
stroke and ignored that the spring cannot exceed 51.5 N at full travel. Redoing
the moments:

| Load, about which axis | Moment | fs, 1 block | fs, 2 blocks |
|---|---:|---:|---:|
| Impact 53 N × 63 mm (about X) | 3.36 N·m | 10.79 | 21.58 |
| **Shoulder reaction at 11 N·m stall (about Y)** | **11.00 N·m** | **3.30** | 6.59 |
| Vector sum | 11.50 N·m | **3.15** | **6.31** |

**So the impact is trivial and the actuator's own reaction torque is the real
load** — the opposite of the earlier conclusion. Both act about axes
perpendicular to the rail, so both are checked against MP/MY = 36.26 N·m.

**One block gives fs = 3.15**, which sits exactly on the bottom edge of HIWIN's
recommended **3.0–5.0 for impact and vibration** duty (1.0–3.0 is their normal-load
band). **Two blocks give 6.31.** Two is still the right call, for three reasons
that survive the corrected numbers:

- fs 3.15 is *at* the limit, not inside it, and stall torque is a real load case
  every time the CBF clamps or the leg hits a stop
- **clone rails derate ~30%**, which puts one block at fs ≈ 2.2 — below spec
- a two-block carriage is also far stiffer in pitch, and column/carriage
  compliance reads directly as false knee deflection in steps 6–9

The second block is ~$12. Buy it.

**Overhang is no longer the driver, so do not distort the design to shrink it.**
Every 10 mm removed buys only 0.5 N·m against an 11 N·m load. Prioritise
short, stiff bolted joints over minimum overhang.

### 4.2 The mass budget — and the sprung/unsprung split

From `sim/beni_inertia.json` (authoritative; sums to 3.2901 kg, matching the
design record's 3.290):

| Item | Mass |
|---|---:|
| Base / chassis | 1.6137 kg |
| Thigh (one) | 0.2198 |
| Shank (one) | 0.4093 |
| Wheel (one) | 0.2091 |
| **One complete leg** | **0.8382 kg** |
| Half the robot | 1.6451 kg |

**So the ballast arithmetic is:**

```
target total on the slide          1.6451 kg
− leg as built (thigh+shank+wheel) 0.8382
                                   ------
carriage + shoulder plate + motor
+ ballast must come to             0.8069 kg
```

**The GIM6010-8 alone is 388–500 g of that** (C4 is unresolved — weigh it). With
a 5 mm PA-CF plate at ~40 g and two blocks at 108 g, the printed carriage plus
ballast has roughly **0.15–0.27 kg** to play with. **It is entirely possible the
rig is over 1.645 kg with zero added ballast.** Design the pockets so ballast can
be *removed* as well as added, and if it still overshoots, thin the carriage or
pocket it out rather than accepting a heavier slide.

**⚠ Then the important subtlety.** The §1 ω_hop identity assumes a single mass on
a single spring. The real rig is a two-mass system: the knee spring sits between
the thigh and the shank, so

- **sprung** (above the spring): carriage + plate + motor + thigh
- **unsprung** (below it): shank + wheel = **0.6184 kg**

That is **38% of the leg riding below the spring** — not a small perturbation.
A 2-DOF system has two modes, and the lower one is what the pluck test in step 8
will actually show. **Do not treat a measured frequency that differs from 3.67 Hz
as a build error.** Report the measured value and the mass split; the control
model gets corrected from the measurement, which is the entire point of the rig.

State the sprung and unsprung masses explicitly in the mass-properties
deliverable — they matter more than the total.

### 4.3 Checks to run in Fusion before releasing

1. Sweep the knee −8° → +27° with the shoulder at nominal and reproduce the
   guide §4 checkpoint table (φ = +25° → 46.1 mm vertical, 24.0 mm fore-aft).
   If it doesn't match, the error is in your model, not the table.
2. Sweep the shoulder ±120° and confirm the service loop never fouls the rail,
   the column, the carriage or the wheel.
3. Confirm the wheel clears the floor plate through the **whole** Mode B travel,
   including full knee extension at the top of the rail.
4. Mass-properties the carriage assembly. State the total, the ballast needed to
   reach 1.645 kg, **and the sprung/unsprung split** (§4.2).
5. Confirm the torque arm can't hit the column at any shoulder angle you intend
   to load it at.
6. **Confirm the 63 mm overhang stack-up against the real assembly** (§4.1). It
   assumes an 8 mm carriage plate; if yours differs, restate the moment table.
7. **Check the Mode A pin path takes load in shear, not bending** — Mode A sees
   the full 11 N·m stall torque with no rail compliance to absorb it, and it is
   the mode where the torque-arm test in step 2 runs.

---

## 5. Electronics for one leg

**Two CAN buses, not one** — the two actuators speak different protocols
(GIM6010-8 is ODrive CANSimple; the SDC101 is a proprietary SteadyWin/MIT
protocol). The Teensy 4.1 has three controllers, so this is free.

```
Bench PSU 20 V, current-limited ──[e-stop button]──[brake chopper]──┬── GIM6010-8   ─CAN1─┐
   (NOT a battery. NOT the pack.)                                   └── GIM4305-10  ─CAN2─┤
                                                                                          │
   Teensy 4.1 ── 2 × TCAN3414 (3.3 V!) ─────────────────────────────────────────────────┘
        ├── ICM-42688-P on SPI  (mount it on the carriage, not the column)
        ├── AS5048A at the knee, SPI direct — no satellite node needed
        └── microSD logging at 1 kHz, onboard socket
```

**Five things that will bite:**

1. **Run CAN at 500 kbps, not 1 Mbps.** Breadboards have no controlled
   impedance and you cannot hold the ≤30 mm stub rule. At 500 kbps a frame is
   ~270 µs, so 2 frames/ms per bus = **54% load** — fits comfortably on two
   buses, and the rig has no bandwidth pressure. The 1 Mbit/three-bus design is
   a two-leg problem.
2. **Breadboard the logic only.** Motor current gets discrete soldered wiring,
   16–18 AWG, direct from the PSU rail. A breadboard rail will not carry 10 A
   and the contact resistance will lie to your current sensing.
3. **The Teensy is 3.3 V and not 5 V tolerant**, at 4 mA recommended drive. Use
   3.3 V transceivers (TCAN3414 / TCAN332G). A 5 V SN65HVD230 breakout will
   damage it.
4. **A bench PSU cannot sink regen.** Every Mode B drop pushes energy back up
   the rail and a lab supply just lets the bus rise. **The 5 Ω brake chopper +
   TLV3011 from `electronics/01_power_and_battery.md` §7.2 is mandatory on this
   rig, not optional.** Build it before the first drop test, and confirm the
   hysteresis (~21.5 V on, ~20.8 V off for the 20 V rig bus) — without hysteresis the FET runs linear
   and cooks.
5. **The wheel driver's max bus voltage is still unconfirmed** (blocker B1 in
   `electronics/05_open_questions.md`). Sources say 12–24 V, 12–36 V and
   12–48 V. **Run the rig at 20 V, not 24 V**, until Steadywin answers. It costs
   nothing here and it protects the only wheel driver you own.

---

## 6. Test order

Each step gates the next. Full gate criteria in
`electronics/06_logging_and_bringup.md`.

| # | Mode | Test | Gate |
|---|---|---|---|
| 1 | bench | Teensy: 2 × CAN loopback, IMU 8 kHz, SD at 240 kB/s for 10 min | zero dropped frames |
| 2 | A | Shoulder encoder cal; **torque arm sweep 0.1 → 6 N·m** | measured within 20% of Kt·I; **≥5.9 N·m reachable** |
| 3 | A | Measure phase R with a milliohm meter; **weigh and caliper both motors** | resolves conflicts C2, C3, C4, C7 |
| 4 | A | **Loop latency**: GPIO toggle at IMU-sample and at torque-write, scoped | **<8 ms end-to-end** |
| 5 | A | Knee sweep −8° → +27° by hand, log AS5048A | monotonic, no wrap, no dropout |
| 6 | A | **Spring characterisation**: known masses on the wheel, φ vs force | F₀ and k measured, replacing the assumed 30.0 N |
| 7 | B | Static: release at equilibrium, measure ride height | matches predicted φ within 1° |
| 8 | B | **Pluck test**: displace 10 mm and release, log φ | **3–4 Hz, ζ ≈ 0.01.** Record the value; do not expect exactly 3.67 (§4.2) |
| 9 | B | Repeat with shoulder damping injection active | **ζ → 0.3** |
| 10 | B | **Drop series, 20 mm → up in 10 mm steps.** Plot φ_peak vs height | φ_peak < +24°; **extrapolate before every step up.** Expect the passive limit near **49 mm** (§4.1) |
| 11 | B | Repeat the series with the landing controller live | 100 mm without hitting +24° |

**Step 10 is the one that changes the project.** The old brief claims a 100 mm
drop has ~10% energy margin; recomputation says it bottoms out. Two independent
routes agree: the energy method in `electronics/04_firmware.md` gives 4.85 J
demand vs 3.55 J capacity (passive limit ~49 mm by the spring-rate method), and
§4.1 gives a passive limit of **49 mm**. **Take the 49 mm figure as the planning
number** — it uses the measured per-leg wheel rate directly and is the more
conservative of the two. Either way the conclusion holds: if the measured curve
confirms it, the spring or the jump target changes, and finding out on this rig
costs one afternoon instead of one robot.

Do not extrapolate past the last measured point. If the trend hits +24° at
40 mm, stop at 40 mm.

---

## 7. Deliverables

1. Fusion assembly of the one-leg rig, both modes, with the reused parts
   in place and the geometry checkpoints of §4.3 verified.
2. STLs for the new `RIG_*` printed parts, print orientation stated per part.
3. Purchase list: extrusion cut lengths, **MGN12 rail 300 mm + 2 × MGN12H
   blocks**, M3 × 8 rail screws + M3 T-nuts, block screws sized to the 3.5 mm
   thread depth, fasteners, bumpers, ballast.
4. Mass-properties report for the carriage assembly, stating **the total on the
   slide, the ballast figure to reach 1.645 kg, and the sprung/unsprung split**
   (§4.2). If the assembly already exceeds 1.645 kg with no ballast, say so —
   that is a design change, not a rounding error.
5. **Status of the ten parts in `beni_rig_no_machining.md`**: which are modelled,
   which are printed, and whether the laser-cut `Knee_Stop_Arc_L` DXF is ready.
   Steps 6–11 are blocked without the spring cartridge; step 10 is blocked
   without the stop arc.
6. **Print orientation and settings per part**, following
   `beni_rig_no_machining.md` §1 — orientation is the strength lever, not infill.
7. **A recommendation on the §2.3 knee redesign** (delete the double-D flats, run
   a shoulder bolt directly in the 6800 bearings). It removes the two hardest
   parts but changes the knee's construction — the fusion agent should confirm
   it works geometrically before it is adopted.
8. A short note on what this rig **cannot** test: balance, pitch dynamics,
   jumping, yaw, the clock spring, and the two-leg scissor stance.
