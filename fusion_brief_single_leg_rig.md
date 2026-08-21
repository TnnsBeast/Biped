# Fusion Brief — Beni Single-Leg Test Rig

> ### ⚠ AMENDED 2026-08-17 — MODE A ONLY. The slide, the ballast and the drop series are deferred
>
> Scope decision by the project owner: **build Mode A and only Mode A.** The
> point of this build is to get toward a *functional Beni*, not to perfect a test
> fixture, so every part that exists only to serve the test rig is deleted. The
> leg bolts to a **printed stand clamped to the bench**; there is no MGN12 rail,
> no carriage, no ballast, no drop release.
>
> | What that deletes | What survives, and why |
> |---|---|
> | `RIG_Rail` (400 mm MGN12 + 2 × MGN12H), `RIG_Carriage`, `RIG_Ballast` × 2, `RIG_Mode_Pin`, `RIG_Drop_Release`, `RIG_Hard_Stops`, `RIG_Index_Bar`/`RIG_Index_Post` | `RIG_Stand` (new, replaces base + column + carriage), `RIG_Floor_Plate`, `RIG_Torque_Arm`, `RIG_Cable_Posts`, the whole knee stack, both hubs, the cartridge eyes — all of these are *robot* parts or measure the robot |
> | Test steps **7–11** (§6): static release, pluck test, damping injection, drop series | Test steps **1–6**, which include **step 6, spring characterisation** — see below |
> | The brake chopper, its comparator, MOSFET, divider and heatsink (§5 trap 4) | Everything else in §5. No drops means no regen, so nothing has to sink it |
>
> **Mode A still measures the spring.** §6 assigns step 6 — *known masses on the
> wheel, φ vs force*, gating *"F₀ and k measured, replacing the assumed 30.0 N"* —
> to **Mode A**. Steps 1–6 are all bench/Mode A. So the Mode-A-only build does
> **not** forfeit F₀ and k as-built.
>
> **What deferring Mode B actually costs:** the leg bounce mode and its
> sprung/unsprung split (steps 8–9), active shoulder damping, and the φ_peak vs
> drop-height curve that sets `A_MAX` in the hard-stop CBF (steps 10–11). Those
> move to the two-leg build, where the real chassis provides the sprung mass the
> ballast was faking.
>
> Mode-B material is kept and marked **[DEFERRED — MODE B]** rather than deleted,
> because the arithmetic is verified and the rail can be added later: Mode A was
> always "Mode B with a pin through the carriage", and a stand is the pin taken to
> its logical end. The Mode A load set is `rig_calc.mode_a_stand()`.

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
> | §7 item 3 — deliver a **DXF** for `Knee_Stop_Arc_L` | **Withdrawn.** There is no laser part to cut. The retired DXFs sit in `archive/laser/` |
>
> Everything else in this brief stands. The answer to it is
> **[`beni_single_leg_rig_design_record.md`](beni_single_leg_rig_design_record.md)**,
> which also lists the **ten places the design departs from this brief** on
> numbers that did not survive recomputation — including the 300 mm rail (needs
> 400), the 49 mm drop limit (45 mm planning, 46.3 mm at the +24° gate), and the
> claim that the GAUGE coupons resolve conflict C2 (the shoulder coupon cannot).


Companion reference: `beni_rig_no_machining.md` (load arithmetic and print
settings). Authoritative per-part routing: `MANUFACTURING_CONSTRAINTS.md`.

**Build.** One left leg on a bench stand, instrumented. One GIM6010-8, one
GIM4305-10, one Teensy 4.1, breadboarded logic, bench PSU.
**No chassis, no second leg, no battery, no PCB, no custom machining.**

**Frozen inputs — do not change:** `beni_prototype1_fusion_guide_rewritten.md`
§4–§9 (kinematics), `beni_prototype1_design_record.md` §2 (motor interfaces
measured from STEP), `archive/manufacturing/machined_parts_spec.md` (dimensions and fits,
even where the *material* is now printed).

**Where older docs disagree with this one, this wins:**

| Topic | Value here | Older docs say |
|---|---|---|
| Peak vertical force on the slide | **~53 N**, spring-limited — superseded by **54.8 N** at the stop (§4.3). Mode A: same ceiling, it is a property of the spring not the fixture | 150–200 N |
| Passive drop limit | **49 mm** — itself superseded by **45 mm** planning / **46.3 mm** +24° crossing (§4.3). **[DEFERRED — MODE B]** | 60 mm or 100 mm |
| Ballast budget | **0.807 kg** (leg is 0.838 kg). **[DEFERRED — MODE B]** — no ballast | "ballast to 1.645 kg" |
| Rig hop frequency | **2-DOF, won't read 3.67 Hz**. **[DEFERRED — MODE B]** — no pluck test | 3.67 Hz exactly |
| Machined parts | **10 families, all 10 eliminated** | "four machined parts" |
| Lateral overhang at the mount | **42.00 mm** in Mode A; 63.00 mm was the Mode B stack (§4.1) | — |

---

## 1. Purpose — why this is a dynamics rig, not a fit check

A leg bolted rigidly to a stand is a fit check. A leg whose shoulder axis rides a
vertical slide carrying half the robot's mass reproduces the real machine's
spring rate, static deflection and per-leg landing energy.

**Build one stand with two modes. Mode A is Mode B with a pin through the
carriage** — one stand, one pin, not two rigs.

| Mode | Shoulder axis | Tests |
|---|---|---|
| **A — rigid** *(the build)* | Bolted to a printed stand clamped to the bench | Actuator characterisation, encoder cal, CAN, latency, torque, **and spring F₀/k (step 6)** |
| **B — vertical slide** | **[DEFERRED]** On the rail, ballasted to 1.645 kg total | Bounce mode, damping, drop series |

**Amended 2026-08-17.** Mode A is the whole build, and it is a fit check *plus*
an actuator and spring characterisation bench — which is what the project needs
next. The paragraph above is still true about what a slide buys, and that is
exactly the list Mode B takes with it when deferred: the bounce mode, the
sprung/unsprung split, and per-leg landing energy. Those are answered on the
two-leg robot, whose chassis is the sprung mass rather than a pot of steel shot.
Taking the pin to its logical end deletes the rail, the carriage, both blocks and
the ballast: **eight `RIG_*` parts and ~$60 of linear motion, for one deferred
measurement set.**

**What it can test:** knee spring preload F₀ and rate k *as built* (the spec's
30.0 N is shim-dependent — do not trust it) — step 6, in **Mode A**; shoulder
torque against a scale; encoder calibration; CAN and loop latency.

**What Mode B would have added, now deferred:** the leg bounce mode; active
shoulder damping; the φ_peak vs drop-height curve that sets `A_MAX` in the
hard-stop CBF; and whether a 100 mm drop really bottoms the knee out.

**What it cannot test:** balance, pitch dynamics, jumping, yaw, the clock spring,
the two-leg scissor stance. Don't try.

---

## 2. Parts — reuse, print, buy

### 2.1 Reuse as-is (STLs exist in `print_stl/`)

`Proximal_Link_L` · `Wheel_Rim_L` · `Wheel_Tyre_L` ·
`Knee_Encoder_Bracket_L` · `Chassis_Shoulder_Plate_L` (5 mm PA-CF, a
**120 × 120 × 5 side panel with a Ø48 bore** — **this is the motor-to-rig
interface, it already exists**; the rig bolts to its **five existing frame-bolt
holes**, see `beni_single_leg_rig_design_record.md` §2.2).

`Distal_Link_L` is **re-exported, not reused as-is** — adopting §2.3 prints the
deleted sleeve's bore into it as Ø10 (design record §4).

**Print `GAUGE_Shoulder_Motor_Interface.stl` and `GAUGE_Wheel_Motor_Interface.stl`
first and test-fit them on the real motors.** Conflicts C2/C3 are unresolved:
the shoulder is Ø80 × 40 *or* × 44, the wheel Ø53 × 26 *or* × 33. That is ±4 mm
and ±7 mm of motor length, and it moves your interfaces. **The coupons resolve
C3 only** — the shoulder coupon is 9.5 mm long and cannot see a 40-vs-44 mm
motor, so C2 needs a caliper across the real motor (design record §2.4).

### 2.2 Formerly machined — now printed or bought

Load arithmetic in `beni_rig_no_machining.md`; the full per-part orientation
table is in `beni_single_leg_rig_design_record.md` §7 and `rig_stl/README.md`.

| Part | Route |
|---|---|
| `Shoulder_Output_Hub_L` | **Print** + 3 × Ø4 × 10 hardened dowel pins + M4 heat-set inserts |
| `Wheel_Hub_L` | **Print** + steel washers under every head, re-torque schedule |
| `Cart_Upper_Eye_L` / `Cart_Lower_Eye_L` | **Print**, then measure pivot-to-spigot and feed the real number to the spring model |
| `Knee_Magnet_Carrier_L` | **Print**, verify 0.05 TIR on an indicator |
| `Knee_Axle_L` + `Knee_Sleeve_L` | **Buy** one Ø10 h6 hardened ground dowel pin. Double-D flats deleted — see §2.3 |
| `Cart_Guide_Rod_L` | **Buy** Ø5 hardened ground shaft, cut to 50 mm |
| `Cart_Preload_Shim_L` | **Buy** Ø19/Ø13.6 × 0.5 shim washers |

**The dowel pins are not optional.** The printed hub's 3 × Ø4.05 register sees
63 MPa at proof load against PA-CF's ~40–50 MPa shear. Pressed steel pins move
the shear into metal. Print the holes Ø3.9 and ream to Ø4.05.

### 2.3 Open design question — delete the double-D flats

The 8.40 −0.02 axle flats and 8.60 +0.05 sleeve bore are the most
machining-intensive feature in the spec, and their only job is keying axle to
sleeve. **Proposal: run a plain Ø10 h6 ground dowel pin directly in the two 6800
bearings**, with anti-rotation printed into the distal boss. The knee oscillates
±35° rather than rotating, and peak force is ~51 N. A shoulder bolt was
considered and **rejected** — its shoulder is h9/h11, which rattles in the
6800's Ø10 bore and puts noise straight into the knee-angle measurement; see
`beni_single_leg_rig_design_record.md` §4.

**Confirm this works geometrically before adopting it** — it changes the knee's
construction, and the two-leg build may want the keyed version back.

### 2.4 Deleted for this build

Chassis, electronics tray, everything `_R`, the satellite CAN node (knee encoder
wires straight to the Teensy), battery/BMS/loop key (bench PSU), and **the clock
spring and its 500 mm cable** — route externally with a loose service loop
through the existing Ø6.0 harness port at r = 21.0 in the shoulder hub, and limit
the rig to ±120° in software.

**Amended 2026-08-17 — also deleted, being Mode B only:** the MGN12 rail and both
MGN12H blocks, `RIG_Carriage`, both ballast pots, the index bar and post, the mode
pin, the drop release, the PU end bumpers, the 2020 base and column, **and the
brake chopper with its comparator, MOSFET, diode, divider and heatsink** (§5 trap
4). Nothing here is thrown away — see the header banner and §3.

**Record in the deliverables:** the clock spring gets **no validation** in this
build. It remains the highest-risk mechanical item and moves to the two-leg build.
**Mode A adds a second item to that list:** the drop series (steps 10–11) is also
deferred, so the knee's landing behaviour reaches the two-leg build unmeasured.
Step 6 measures the spring curve it would have been predicted from, which is the
next best thing.

### 2.5 Print settings — orientation, not infill

**PA-CF is 84–102 MPa in XY but only 26–50 MPa in Z.** Orientation decides
survival; 100% infill does not help and costs time and warp.

5 walls · 40% gyroid infill · 0.15 mm layers · top-of-range temp · minimal
cooling · **dry the filament.** Justifications for each setting in
`beni_rig_no_machining.md` §1; per-part orientations in
`beni_single_leg_rig_design_record.md` §7.

---

## 3. New parts to design

**Amended 2026-08-17 — Mode A only.** The table below is the original two-mode
part list. Eight rows are now **[DEFERRED — MODE B]**, and `RIG_Base` +
`RIG_Column` + `RIG_Carriage` collapse into one printed `RIG_Stand`. The Mode A
part list is five items:

| Part | Requirement (Mode A) |
|---|---|
| `RIG_Stand` | **New. Printed, bolted or clamped to the bench.** Carries `Chassis_Shoulder_Plate_L` on its five existing frame-bolt holes; its outboard face **is** the motor front mount face at y = 42.0, so the overhang is **42.00 mm, not 63.00** (67 % of Mode B — the block and the carriage plate are gone from the stack). Must react **11.00 N·m of yaw** at shoulder stall, 25.00 N·m at proof screen; pitch is only 2.30 N·m and roll 2.99 N·m. **It cannot be held down by dead weight** — 11 N·m needs 11.2 kg at 100 mm base half-width and still 3.7 kg at 300 mm, against a ~0.3 kg print. Clamp it. Hold the shoulder axis **≥ 221 mm** above the floor plate (that is the −8° extension-stop ride height; φ = 0 is 209.27 mm and the +27° stop 159.13 mm). |
| `RIG_Torque_Arm` | Unchanged. **200 mm lever on the shoulder hub's 6 × M4 Ø44 PCD**, bearing on a 5 kg kitchen scale. Highest-value cheap part here: published bench tests found **4.8 and 9.4 N·m against an 11 N·m rating**, and the jump needs 5.9 N·m — which reads **3.01 kgf** at 200 mm. |
| `RIG_Floor_Plate` | Unchanged. Flat, hard, ≥250 mm fore-aft. A shoulder sweep rolls the wheel ~77 mm; if it scrubs, every force reading is corrupt. |
| `RIG_Cable_Posts` | Unchanged in function, simpler in routing — there is no rail or carriage to clear, only the wheel and the stand. |
| `RIG_Knee_Stop_Plate_L` | Still required. It carries the **−8° extension stop**, which a free leg rests on at 8.25 N in every pose, Mode A included. The +27° washer-column stop inside the cartridge is only needed before step 10, so it is **[DEFERRED — MODE B]** along with the drop series (design record §8). |

Original two-mode table, retained for the Mode B restart. Bolt to **2020
aluminium extrusion** — don't print structure you can buy straight.

| Part | Requirement | Mode A |
|---|---|---|
| `RIG_Base` | 2020 frame, ≥400 × 300 mm. **Clamp it to the bench** or it walks under drop loads. | superseded by `RIG_Stand`; the clamp requirement carries over and hardens |
| `RIG_Column` | 2020 vertical ≥500 mm, diagonally braced. **Column and carriage compliance reads directly as false knee deflection** — stiffness here is measurement quality, and printed hubs make it worse. | superseded by `RIG_Stand`; **the compliance warning carries over unchanged** and matters more, because a printed stand is softer than braced 2020 |
| `RIG_Rail` | **MGN12 rail with TWO MGN12H blocks.** Not a round shaft (won't resist rotation about its own axis), not one block (§4.1). Rail 12 × 8 mm, M3 holes at 25 mm pitch / 10 mm end margin. M3 × 8 into M3 T-nuts; 2020 + MGN12 leaves 4 mm of extrusion each side. Length must cover the 100 mm drop series plus sag plus release gear: **300 mm gives 231 mm usable travel** (300 − 45.4 block − ~24 mm bumpers) for **one** block, but two blocks need **400 mm** — §4.1. | **[DEFERRED — MODE B]** |
| `RIG_Carriage` | PA-CF plate **spanning both blocks** (~80 mm centres, plate ≥140 mm), carrying `Chassis_Shoulder_Plate_L` on its **five existing frame-bolt holes** (§2.1), plus ballast pockets. **⚠ The MGN12H's 4 × M3 holes (20 × 20 pattern) are only 3.5 mm deep** — screw length ≤ plate thickness + 3.0 mm, or you jack the carriage off the block or crack the casting. | **[DEFERRED — MODE B]**; the five-hole interface moves to `RIG_Stand` |
| `RIG_Ballast` | Pockets for steel plate or M12 washers. **Budget is 0.807 kg, not 1.645** (§4.2). Must allow ballast to be **removed** — the rig may already overshoot. Adjustable, for 1.645 / 2.0 kg runs; the **1.2 kg run is not achievable** (§4.2). | **[DEFERRED — MODE B]** |
| `RIG_Mode_Pin` | Ø8 pin, carriage into a reamed column hole = Mode A. **Load it in shear, not bending** — Mode A takes full 11 N·m stall with no rail compliance. | **[DEFERRED]** — no carriage to pin. **The 11 N·m note is the live requirement**: it is now `RIG_Stand`'s design load |
| `RIG_Drop_Release` | Pin holes at 10 mm intervals, **20 to 100 mm** above free-standing equilibrium, plus a quick-release catch. Passive limit is 45 mm (§4.3); past ~70 mm needs the landing controller live. | **[DEFERRED — MODE B]** |
| `RIG_Hard_Stops` | PU bumpers top and bottom. The carriage must not reach an end plate at speed, or crush a hand. | **[DEFERRED — MODE B]** — nothing travels |
| `RIG_Torque_Arm` | **200 mm lever on the shoulder hub's 6 × M4 Ø44 PCD**, bearing on a 5 kg kitchen scale. Highest-value cheap part here: published bench tests found **4.8 and 9.4 N·m against an 11 N·m rating**, and the jump needs 5.9 N·m — which reads **3.01 kgf** at 200 mm. | **keep** |
| `RIG_Floor_Plate` | Flat, hard, ≥250 mm fore-aft. A shoulder sweep rolls the wheel ~77 mm; if it scrubs, every force reading is corrupt. | **keep** |
| `RIG_Cable_Posts` | Two T-slot posts carrying the service loop clear of rail and wheel. | **keep**, simplified |

---

## 4. The numbers that constrain the design

**The arithmetic behind §4.1–§4.3 is not reproduced here.** It is done at higher
fidelity — exact integration rather than closed-form energy balance, and measured
rather than assumed masses — in `beni_single_leg_rig_design_record.md` §2.3 and
§3, and it is reproducible from `rig_calc.py`. What follows is the conclusion
each subsection reached, and where the design record's recomputation moved it.

### 4.1 Two carriage blocks — moment, not load

**[DEFERRED — MODE B] as a purchase.** No rail is bought and no block is fitted.
**The physics is not deferred and it is now the stand's design driver.**

**Vertical load is irrelevant. Moment binds, and the actuator's own reaction
torque is the real load — the impact is trivial.** That sentence was written
about the MGN12H and it applies verbatim to the printed stand. Mode A moments,
from `rig_calc.mode_a_stand()`:

| Load | Value | Note |
|---|---|---|
| Pitch, spring-limited wheel force 54.80 N × 42.00 mm | **2.30 N·m** | trivial |
| Roll, its ground reaction 71.3 N × 42.00 mm | **2.99 N·m** | trivial |
| **Yaw, shoulder stall about the motor axis** | **11.00 N·m** | **dominant** |
| Vector sum, yaw + roll | **11.40 N·m** | design against this |
| Yaw at proof screen | **25.00 N·m** | screening load |

**Overhang is 42.00 mm in Mode A, not 63.00** — the block (13.0) and the carriage
plate (8.0) are out of the stack, so the stand's outboard face is the motor front
mount face at y = 42.0. **Don't distort the design to shrink it further.** Prefer
short stiff joints.

Superseded, and now moot: this brief's **300 mm** rail and its "231 mm usable
travel" are the *one-block* figures; two blocks at 80 mm centres occupy 125.4 mm,
so the rail would be 400 mm. Kept for the Mode B restart. Moment factors of
safety, the as-built 63.00 mm Mode B stack-up and the rail-length arithmetic:
design record §2.1 and §2.3, and `rig_calc.py`.

### 4.2 Mass — and the sprung/unsprung split

**[DEFERRED — MODE B].** With no slide and no ballast there is no mass budget to
blow: the stand carries a static **0.8382 kg** of leg (8.22 N), or **1.2262 kg**
with a 388 g GIM6010-8 and **1.3382 kg** with a 500 g one (conflict C4). That is
a hanging load, not a sprung mass, and it is 3 % of the yaw load the stand is
sized by. **C4 stops being a rig-design risk in Mode A** — weigh the motors
anyway, because the two-leg robot's budget still depends on it.

The subtlety below survives as *physics to be measured later*, not as a rig
requirement:

**⚠** The knee spring sits between thigh and shank, so a large fraction of the leg
is **unsprung**. This is a 2-DOF system with two modes. **A pluck test reading
other than 3.67 Hz is not a build error.** Report the measured value and the mass
split; the control model gets corrected from the measurement. In Mode A there is
no pluck test — this moves to the two-leg build.

Superseded: the brief estimated the ballast budget; the design record measures
it off the built assembly. The **bare slide is 1607.6 g**, so this brief's
request for a **1.2 kg run is impossible** — it would need 408 g *removed* and
there is nothing left to remove. Runs of 1.645 and 2.0 kg are achievable.
Measured mass roll-up, sprung/unsprung split and the ballast provision: design
record §5; the bounce-mode prediction: §3.1.

### 4.3 Spring force and the drop ceiling

**Conclusion: the knee spring is the softest element in the load path, so it
caps transmissible force.** Nothing downstream of the knee can see more than the
spring can transmit, however hard the leg is dropped. **This is what makes Mode A
safe to design against a flat 54.80 N** — the ceiling is a property of the
spring, not of the fixture, so deleting the slide does not raise it.

**The drop ceiling itself is [DEFERRED — MODE B]** — there are no drops. Retained
because it is the gate the two-leg build inherits, and because step 10 is the
test that changes the project:

Superseded on both numbers. Peak force is **54.8 N** at the stop, not ~53 N
(51.4 N at +25°). The passive drop limit is **46.3 mm**, not 49 mm: this brief's
own step-10 gate is φ_peak < +24°, which is reached at 46.3 mm, so a 49 mm drop
already breaks the gate. +25° is at 50.7 mm and the +27° stop at 60.0 mm. Take
**45 mm** as the passive planning limit. The energy-method 60 mm figure in
`04_firmware.md` is likewise superseded. Full drop table by exact integration of
the frozen spring curve: design record §3, from `rig_calc.py`.

### 4.4 Checks before releasing CAD

**Mode A set — six checks become four.**

1. Sweep the knee −8° → +27° at nominal shoulder and reproduce guide §4:
   **φ = +25° → 46.1 mm vertical, 24.0 mm fore-aft.** Mismatch means your model
   is wrong, not the table. **Unchanged.**
2. Sweep the shoulder ±120°; the service loop must not foul the stand or the
   wheel. **Rail, column and carriage are gone from the list.**
3. Wheel clears the floor plate at **every knee angle −8° → +27°** with the stand
   at its designed height — the shoulder axis sits 221.31 mm up at the extension
   stop and 159.13 mm at the +27° stop, so the check is on knee sweep, not on
   slide travel. *(Was: through the whole Mode B travel.)*
4. Torque arm can't hit the stand at any angle you intend to load. **Unchanged in
   intent; the obstacle is the stand, not the column.**

Deferred with Mode B:

5. ~~Mass-properties the carriage: total, ballast to reach 1.645 kg, **and the
   sprung/unsprung split.**~~ **[DEFERRED — MODE B]** — no carriage. Do still
   mass-property the leg; the Mode A stand load set is in
   `rig_calc.mode_a_stand()`.
6. ~~Re-verify the 63 mm stack-up against the real assembly — it assumes an 8 mm
   carriage plate.~~ **Replaced:** verify the **42.00 mm** Mode A overhang, which
   assumes the stand's outboard face lands exactly on the motor front mount face
   at y = 42.0. If you put a plate in between, the overhang grows and every
   moment in §4.1 scales with it.

**New, Mode A only — 7. Prove the hold-down.** The stand reacts 11.00 N·m of yaw
and cannot be weighted (§3, `RIG_Stand`). The CAD must show the clamp or the
bench-bolt path, not assume it.

---

## 5. Electronics

**Two CAN buses** — the actuators speak different protocols (GIM6010-8 is ODrive
CANSimple; the SDC101 is proprietary SteadyWin/MIT). The Teensy 4.1 has three
controllers, so this is free. **Each controller needs its own transceiver**, so
two buses = two transceiver breakouts.

```
Bench PSU 20 V, current-limited ─[e-stop]─┬─ GIM6010-8  ─CAN1─┐
   (NOT a battery)                        └─ GIM4305-10 ─CAN2─┤
   Teensy 4.1 ── 2 × CAN Pal (3.3 V) ────────────────────────┘
        ├── IMU on SPI  (on the STAND, as close to the shoulder axis as it fits)
        ├── AS5048A at the knee, SPI direct
        └── microSD logging at 1 kHz, onboard socket
```

**Amended 2026-08-17 (Mode A).** Three changes to the block diagram above:

- **The brake chopper is out of the power path.** It existed only to sink Mode B
  drop regen (trap 4). No drops, no regen. See trap 4.
- **`TCAN3414` → Adafruit CAN Pal (PID 5708, TJA1051T/3).** The TCAN3414 is
  surface-mount and this build is breadboarded. The CAN Pal has an onboard charge
  pump so it runs from a single **3.3 V** rail, which is what trap 3 demands.
  Verified in stock at Adafruit at $3.95; the Digi-Key line (1528-5708-ND) was
  **not** confirmed, so buy from Adafruit unless you check Digi-Key yourself.
- **IMU: the on-hand BNO085 substitutes, with one gate consequence.** It mounts on
  the stand instead of the carriage. **It cannot meet the 8 kHz IMU gate in
  step 1** — the BNO085's SH-2 raw gyro report tops out around 1 kHz and its
  calibrated/uncalibrated gyro reports at 100 Hz, against the ICM-42688-P's
  32 kHz. Re-scope the gate to **1 kHz raw**, which still clears the ≥2 kHz
  requirement's *intent* only at the knee encoder, not at the IMU. `electronics/03`
  §4's rule stands and matters more here: **never use the BNO085's on-chip
  fusion** — its 6.6 ms fused latency is 38° of phase lag and it will eat the
  <8 ms loop-latency gate in step 4 by itself. Read raw, fuse on the Teensy. If
  step 4 fails, the ICM-42688-P is the fix.

**Five things that will bite:**

1. **500 kbps, not 1 Mbps.** Breadboards have no controlled impedance and can't
   hold the ≤30 mm stub rule. At 500 k a frame is ~270 µs → 54% load on 2
   frames/ms. The 1 Mbit three-bus design is a two-leg problem.
2. **Breadboard logic only.** Motor current gets soldered 16–18 AWG straight from
   the PSU. Breadboard rails won't carry 10 A and contact resistance will lie to
   your current sensing.
3. **The Teensy is 3.3 V and not 5 V tolerant.** A 5 V SN65HVD230 breakout kills
   it. This is why the transceiver is a TJA1051T/3 part and not the common
   SN65HVD230 module.
4. **A bench PSU cannot sink regen — [DEFERRED — MODE B].** Every Mode B drop
   pushes energy back and the supply just lets the bus rise. The 5 Ω brake chopper
   + TLV3011 was **mandatory before the first drop**
   (`electronics/01_power_and_battery.md` §7.2). **Mode A has no drops**, so
   nothing drives the bus up: the resistor, comparator, MOSFET, diode, divider and
   its heatsink all come out of Wave 0. **Build it before the first drop, and
   before the two-leg build** — that is not optional, it is deferred. Its
   thresholds still need re-scaling for a 20 V bus when it is built: the published
   26.5 V on / 25.6 V off is set for the 25.2 V pack and would never fire here.
   Target ~21.5 V on / ~20.8 V off, and confirm the hysteresis exists or the FET
   runs linear. **Those divider values are still uncomputed.**
   ⚠ Consequence to hold onto: **until the chopper exists, do not let the leg
   backdrive either motor faster than the PSU can absorb** — no hand-spinning the
   wheel under power, no dropping the leg by hand off the stand.
5. **Run at 20 V, not 24 V.** The wheel driver's max bus voltage is unconfirmed
   (blocker B1: sources say 12–24, 12–36 and 12–48 V). Costs nothing here and
   protects the only wheel driver you own.

---

## 6. Test order — each step gates the next

Full gate criteria in `electronics/06_logging_and_bringup.md`.

| # | Mode | Test | Gate |
|---|---|---|---|
| 1 | bench | Teensy: 2 × CAN loopback, IMU raw stream, SD 240 kB/s for 10 min | zero dropped frames. **IMU gate re-scoped to 1 kHz raw** for the on-hand BNO085 (§5) |
| 2 | A | Shoulder encoder cal; **torque arm sweep 0.1 → 6 N·m** | within 20% of Kt·I; **≥5.9 N·m reachable** |
| 3 | A | Phase R with a milliohm meter; **weigh and caliper both motors** | resolves C2, C3, C4, C7 |
| 4 | A | **Loop latency**: GPIO at IMU-sample and torque-write, scoped | **<8 ms end-to-end.** Fuse on the Teensy — the BNO085's own fused output spends 6.6 ms of this budget before you start (§5) |
| 5 | A | Knee sweep −8° → +27° by hand, log AS5048A | monotonic, no wrap or dropout |
| 6 | A | **Spring characterisation**: known masses on the wheel, φ vs force | F₀ and k measured, replacing the assumed 30.0 N |
| 7 | ~~B~~ | **[DEFERRED]** Static release at equilibrium, measure ride height | matches predicted φ within 1° |
| 8 | ~~B~~ | **[DEFERRED] Pluck test**: displace 10 mm, release, log φ | 3–4 Hz, ζ ≈ 0.01. **Record it; don't expect 3.67** (§4.2) |
| 9 | ~~B~~ | **[DEFERRED]** Repeat with shoulder damping injection | **ζ → 0.3** |
| 10 | ~~B~~ | **[DEFERRED] Drop series, 20 mm up in 10 mm steps** | φ_peak < +24°; **extrapolate before every step up.** Passive limit ~45 mm (+24° crossed at 46.3 mm, §4.3) |
| 11 | ~~B~~ | **[DEFERRED]** Repeat with the landing controller live | 100 mm without hitting +24° |

**Amended 2026-08-17 — the build runs steps 1–6 and stops.** That is the whole
Mode A programme and it is where the actuator, encoder, CAN, latency and **spring
F₀/k** answers come from. Steps 7–11 need the slide, the ballast, the drop release
and the brake chopper, and all four are deferred.

**Step 6 is now the last step and the most valuable one.** It replaces the assumed
30.0 N preload with a measured F₀ and k, and every downstream number in this
project — the drop table, the force ceiling, the stop-washer count — is computed
from that spring curve. Known masses on the wheel against measured φ, from
`rig_calc.mode_a_stand()`:

| Added mass | Force at wheel | φ |
|---|---|---|
| 0.5 kg | 4.90 N | below preload — still on the −8° stop |
| 1.0 kg | 9.81 N | −6.55° |
| 2.0 kg | 19.61 N | +2.16° |
| 3.0 kg | 29.42 N | +10.05° |
| 4.0 kg | 39.23 N | +17.14° |
| 5.0 kg | 49.03 N | +23.53° |

⚠ **Preload floor: a free leg rests on the −8° extension stop at 8.25 N.** Below
that the knee does not move at all, so **threshold contact detection on φ, not on
estimated force** — and don't read the 0.5 kg row as a soft spring.

**The knee hard stop must be fitted before step 10. Do not run one drop without
it.** Steps 1–9 never approach +27°, so **Mode A never needs the +27° washer
column** — but it *does* need `RIG_Knee_Stop_Plate_L`'s −8° stop, which the leg
rests on in every unloaded pose (8.25 N, above).

**Step 10 is the one that changes the project — and it is deferred, so the project
has not been de-risked yet.** The old brief claimed a 100 mm drop has ~10% margin;
both the energy method and the spring-rate method say it bottoms out. Deferring it
means the two-leg build inherits that question unanswered, alongside the clock
spring. Know that going in. Step 6's measured curve at least lets you *predict* it
honestly before you build the robot.

**Never extrapolate past the last measured point.** If the trend hits +24° at
40 mm, stop at 40 mm.

---

## 7. Deliverables

**Amended 2026-08-17 — Mode A only.** The CAD handoff for the stand is
`fusion_agent_guide_mode_a.md`.

1. Fusion assembly, **Mode A only**, reused parts in place, the four §4.4 checks
   plus the new hold-down check verified.
2. STLs for `RIG_Stand`, `RIG_Torque_Arm`, `RIG_Floor_Plate`, `RIG_Cable_Post_A/B`,
   `RIG_Knee_Stop_Plate_L` **and** the re-routed formerly-machined parts, with
   print orientation and settings stated per part (§2.5). **No carriage, no
   ballast pot, no index bar.**
3. Purchase list. **The linear-motion section is deleted:** no MGN12 rail, no
   MGN12H blocks, no rail screws or T-nuts, no block screws, no PU bumpers, no
   ballast shot, no 2020 extrusion or T-nuts for a base and column. What remains
   is 3 × Ø4 × 10 dowel pins, M4 heat-set inserts, M3 heat-set inserts, Ø10 h6
   hardened ground dowel pin, Ø5 × 50 hardened shaft, shim washers, steel washers,
   M5 washers for the cartridge column *(that stack is deferred with step 10, but
   buy it — it is a few dollars and the −8° plate is not the +27° stop)*, and the
   stand's bench clamps or bolts.
4. **Mode A load report** rather than a slide mass-properties report: the leg's
   static hanging mass, the four moments at the stand mount, and the hold-down
   method. All of it is `rig_calc.mode_a_stand()`. **If the stand's overhang comes
   out above 42.00 mm, say so** — every moment scales with it, and that is a design
   change, not a rounding error. ~~Total on the slide, ballast to reach 1.645 kg,
   and the sprung/unsprung split~~ **[DEFERRED — MODE B]**.
5. **A recommendation on §2.3** (delete the double-D flats, Ø10 h6 ground dowel
   pin direct in the bearings) — confirmed geometrically, or rejected with a reason.
   **Unchanged: this is knee construction, not rig scaffolding, and it survives the
   Mode A cut intact.**
6. A short note on what this rig **cannot** test: balance, pitch dynamics,
   jumping, yaw, the clock spring, the two-leg scissor stance — **and now, in Mode
   A, the bounce mode, shoulder damping and the drop series (§1).**

---

## 8. Known-unresolved, outside CAD scope but gating the build

- **B1** — wheel-driver max bus voltage. Run at 20 V until Steadywin answers.
- **C2 / C3** — motor dimensions, ±4 mm and ±7 mm. **Print the GAUGE coupons** —
  they settle C3; C2 needs a caliper across the real motor (§2.1).
- **C4** — actuator masses (388/150 g vs 500/250 g). Weigh them; it decides
  whether the ballast budget in §4.2 is comfortable or negative.
- **Creep.** Printed joints relax silently. **Re-torque after the first hour,
  then periodically**, and inspect the printed hub's dowel holes for ovalisation
  after every drop session.
