# Beni Prototype 1 — Electronics & Firmware Handoff Brief

> **⚠ Superseded in part — 2026-08-11.** The electronics design that grew from
> this brief is now in **`electronics/README.md`** and the seven numbered
> documents (`01_power_and_battery.md` through `07_bom.md`). Those resolve the
> §3 blockers, correct several figures in this brief (notably: the 100 mm drop
> bottoms out — passive limit is ~49 mm, not "~10% margin" — and the unstable
> pole is 11.18 rad/s, not 9.7), and carry the authoritative BOM. **Read
> `electronics/05_open_questions.md` before ordering anything.**
>
> The single-leg test rig is specified in **`fusion_brief_single_leg_rig.md`**,
> which uses a Teensy 4.1 at 20 V on two CAN buses — not the custom STM32G474
> board or the three-bus architecture described here.

**Purpose.** Everything a researcher needs to specify the complete electrical
and software stack for this robot: power, actuators, sensors, wiring, compute,
and control firmware. The mechanics are frozen and verified; the electronics are
not yet designed at all.

**Status of the mechanical side:** complete, audited, 0 outstanding problems.
CAD is `Biped → Beni_Prototype1` in Fusion. Full change history in
`beni_prototype1_rev2_changes.md`.

**Status of the electrical side:** a 250 g battery envelope and a 120 g
"electronics" block exist in CAD as *mass placeholders with locations*. There is
no board, no wiring diagram, no connector, no BMS, no e-stop, no firmware.

> **Read §3 first.** Three hard constraints there (battery voltage, battery
> physical size, harness conductor count) each look like they may invalidate
> assumptions already baked into the BOM. Resolve those before designing
> anything downstream.

---

# 1. What the robot is

A **self-balancing wheeled biped** in the Mondo Robotics *Beni* serial
morphology. Two legs, each:

```
body ─▶ active rotary shoulder ─▶ proximal link ─▶ PASSIVE spring knee ─▶ distal link ─▶ driven wheel
        GIM6010-8, ±185°          L1 = 120 mm      −8°…+27°, no actuator   L2 = 120 mm    GIM4305-10, Ø110
```

It balances on two wheels like a Segway, and it is designed to **jump** by
rapidly rotating both shoulders to drive the wheels into the ground; the passive
knee springs absorb the landing.

**Only 4 actuators total: 2 shoulders + 2 wheels.** The knee has no motor. It is
a spring, and its angle is *measured*, not commanded.

## 1.1 Coordinate frame (used everywhere in this project)

| axis | direction |
|---|---|
| **+X** | forward |
| **+Y** | left |
| **+Z** | up |

Origin is on the **shoulder axis**, which is the global Y axis. All three joint
types rotate about **+Y**. At the nominal pose the wheel axis is directly below
the origin at (0, ±84, −154.269) mm.

## 1.2 Physical and dynamic properties (measured from CAD, not estimated)

| Property | Value |
|---|---:|
| Mass | **3.290 kg** |
| Overall L × W × H | 183 × 217 × 281 mm |
| Track (wheel centre to wheel centre) | 168 mm |
| Wheel diameter / radius | 110 mm / **55 mm** |
| Ride height (shoulder axis to ground) | 209.3 mm |
| **CoM** (X, Y, Z from shoulder axis) | **(+6.46, −0.00, −50.57) mm** |
| **CoM height above the wheel axis** | **103.7 mm** |
| Ixx about CoM (roll) | 0.03214 kg·m² |
| **Iyy about CoM (pitch — governs balance)** | **0.02508 kg·m²** |
| Izz about CoM (yaw) | 0.01706 kg·m² |
| Ixz about CoM | +0.002759 kg·m² |
| **Inverted-pendulum time constant** √(L/g) | **0.103 s** |

Per-link masses and full inertia tensors for all 6 moving links:
**`sim/beni.urdf`** and **`sim/beni_inertia.json`**. Mass closure is exact.

**What τ = 0.103 s means for you.** The unstable pole sits at ≈9.7 rad/s
(1.55 Hz). This is a *short, twitchy* pendulum — shorter than most balancing
robots. It drives the control-loop rate and the IMU latency budget (see §7).

**Standing trim.** The CoM is 6.46 mm forward of the wheel contact patch. That is
a permanent **0.21 N·m** bias (0.11 N·m per wheel) that the controller must hold,
and it means the equilibrium stance sits a few degrees off the nominal pose. It
is inherent to the bent-leg geometry and cannot be ballasted out.

---

# 2. Actuators

Both are **Steadywin GIM-series integrated actuators** — motor + gearbox +
encoder + driver in one housing, commanded over CAN. You do **not** need to
design motor drivers.

## 2.1 Shoulder — Steadywin GIM6010-8 ×2

| | |
|---|---|
| Role | Rotates the whole leg. The only actuated leg joint. |
| Range | ±185° (370° total, **not** continuous rotation) |
| Envelope | Ø80 × 44 mm |
| Mount | 8 × M3 on Ø74 PCD |
| Output | 6 × M3 on Ø25 PCD + 3 × Ø4 anti-rotation pins on Ø20.4 PCD |
| Cable exit | notch in the Ø57 driver cover, at the **inboard** end (y = 5…16 mm) |
| Mass | ~500 g each (estimate — **weigh the delivered units**) |
| Published variants | 24 V: ~5 N·m rated / ~11 N·m stall · 48 V: ~4.6–5.4 N·m rated / ~17.2–17.9 N·m stall |

**The central open question of the whole design** — see §3.1.

## 2.2 Wheel — Steadywin GIM4305-10 ×2

| | |
|---|---|
| Role | Drives the wheel. Continuous rotation. |
| Envelope | Ø53 × 33 mm |
| Mount | 6 × M2.5 on Ø47.5 PCD |
| Output | 3 × M3 on Ø27 PCD, Ø37 flange |
| Cable exit | driver cover Ø40.4, recessed **inboard** into the distal link's Ø41.5 pocket at y = 61.5…67.5 |
| Mass | ~250 g each (estimate) |

Torque demand is comfortable — well inside any plausible rating:

| Case | Per wheel |
|---|---:|
| Accelerate at 1 m/s² | 0.09 N·m |
| Hold the 6.46 mm CoM trim | 0.11 N·m |
| Climb a 15° slope | 0.23 N·m |

## 2.3 Actuator research tasks

- Confirm the **exact variant** of both actuators (24 V vs 48 V) and get the real
  torque-speed curves, not just rated/stall numbers.
- Get the **CAN protocol specification**: bitrate, frame format, node-ID
  assignment, command set (torque / velocity / position / impedance modes),
  telemetry, and whether it is a MIT-Cheetah-style protocol, CANopen, or
  proprietary. Confirm whether firmware source or an SDK is available.
- Confirm the **built-in encoder**: absolute or incremental, resolution,
  whether it survives power cycles, and homing requirements.
- Confirm **connector types and pinouts** on both actuators.
- Confirm **maximum bus voltage and current limits**, and whether the driver has
  regenerative braking / a brake resistor requirement (relevant on landing).
- Confirm whether the driver supports a **direct torque/current command mode**.
  The jump and the landing damping both need torque control, not position
  control.

---

# 3. THREE HARD CONSTRAINTS TO RESOLVE FIRST

These came out of the mechanical audit and each one may invalidate a BOM
assumption. Do not design around the current BOM until these are settled.

## 3.1 Battery voltage may be wrong for the motors

The BOM specifies a **4S 2200 mAh** pack — 14.8 V nominal, 16.8 V full charge.
The GIM6010-8 is published in **24 V and 48 V** variants.

**A 4S pack cannot drive a 24 V-class actuator at rated performance.** Stall
torque is current-limited so it may survive, but the speed constant means top
speed and therefore *mechanical power* drop roughly in proportion to voltage —
and the jump is a power-limited manoeuvre, not a torque-limited one.

Likely resolution: **6S (22.2 V nominal, 25.2 V full)** for a 24 V actuator.
Verify against the actuator's absolute maximum input voltage — 25.2 V on a
nominally 24 V drive may exceed it.

Deliverable: a defensible pack voltage, with the actuator datasheet as evidence.

## 3.2 The battery envelope is physically too small

The CAD envelope is **69 (X) × 25 (Z) × 45 (Y) mm = 77.6 cm³** at 250 g.

- A standard 4S 2200 mAh LiPo is roughly **105 × 34 × 30 mm**. It does not fit —
  and 105 mm does not fit **anywhere** in this chassis in any orientation (the
  frame interior is about 102 (X) × 92 (Z) × 76 (Y) mm, and the middle of it is
  filled by the shoulder motors).
- On energy density alone: 4S 2200 mAh = 32.6 Wh. At ~275 Wh/L that needs
  ≈118 cm³. The 77.6 cm³ envelope holds ≈21 Wh — about **35 % short** of the
  energy the BOM claims for it.

So the specified pack needs ~50 % more volume than the box allows, **and** its
assumed form factor cannot be installed anywhere. Options to evaluate:

- two smaller packs in series/parallel, sited in the two free regions in §5;
- a custom pack built to the available envelope;
- cylindrical cells (18650 / 21700) — but note a 21700 is 21 × 70 mm and the
  free boxes are tight;
- accept less capacity and shorter runtime.

Deliverable: a real, orderable pack (or cell + custom-pack spec) that fits the
free space in §5, with its true mass and dimensions so the CoM can be re-checked.

## 3.3 The harness may not fit the clock-spring cavity

The shoulder has **no through-bore** (the GIM6010-8 output centre is a 0.5 mm
blind recess), so the wiring crossing the shoulder joint uses a **clock-spring
spiral cavity**. Every wire to everything distal of the shoulder goes through it.

| Cavity property | Value |
|---|---|
| Location | annular cavity between the fixed side panel and the rotating hub |
| Radial extent | r = 20 → 32 mm |
| Axial height | **4.0 mm** (y = 47 → 51) |
| Modelled harness envelope | r = 20.2 → 31.8, 3.6 mm tall, 6822 mm³ |
| Assumed cable | **Ø3.0 mm** high-flex silicone, ~400 mm coiled, ~3 turns |
| Rotation capacity | ~430–470° against the **370° required** (≈20 % margin) |
| Entry (fixed side) | Ø7 grommet in the panel at r = 29, angle 200° |
| Exit (rotating side) | Ø6 port in the hub at r = 21, angle 30.4° |

**The problem:** a single Ø3.0 cable must carry everything that crosses the
shoulder. Per leg that is at minimum:

| Load | Conductors |
|---|---|
| Wheel motor power (V+, V−) | 2, sized for peak current |
| Wheel motor CAN (H, L) | 2, ideally twisted, ideally shielded |
| Knee encoder | 3 (PWM) to 6 (SPI), or 4 (I²C) |
| **Total** | **7–10 conductors** |

A Ø3.0 OD jacketed cable holds roughly 4 × 24 AWG. 24 AWG is very likely
inadequate for wheel-motor peak current, and there is no allowance for a CAN
twisted pair plus shield.

Deliverable: a real cable specification (conductor count, gauge, shielding,
jacket OD, bend radius, flex-life rating) that fits a **≤4 mm** axial envelope
and survives ±185° × many thousands of cycles. If it cannot be one cable, work
out whether two smaller cables fit the r = 20…32 × 4 mm cavity side by side, and
recompute the wrap capacity — the mechanical design has ~20 % margin to spend.

Also specify **strain relief at both ends** (panel side and rotating hub side),
which the mechanical design requires but does not detail.

---

# 4. Sensors

## 4.1 Knee angle — AS5048A ×2 (the important one)

The knee is passive, so its angle is the **only** way to know leg compression.

| | |
|---|---|
| Part | AS5048A (or AS5047-class), 14-bit magnetic rotary encoder |
| PCB | 14 × 14 mm, at y = 98.3…99.9 mm, centred on the knee axis |
| Magnet | Ø6 × 2.5 mm **diametric** NdFeB, rotating with the distal link |
| Magnet face | y = 96.3 mm |
| Sensor package face | y = 97.3 mm → **1.00 mm mechanical clearance** |
| **Magnet-to-die gap** | **≈1.5 mm** (TSSOP-14 ≈1.0 mm thick, die near mid-package) |
| Mounting | ABS bracket on 2 × M3 heat-set inserts in the proximal link |
| Measured range | −8° … +27° (35° of travel out of 360°) |

Interfaces available on the AS5048A: **SPI**, **PWM**, and incremental **ABI**.
Choose based on the harness conductor budget in §3.3 — PWM needs only 3 wires
and is the cheapest across the clock spring, SPI needs 6 but is faster and
cleaner.

**This encoder is also your force sensor.** Knee angle → spring deflection →
spring force → ground reaction force, through the exact table in §8.2. That is
how the robot knows it has landed and how hard.

Research tasks: confirm the AS5048A works at a 1.5 mm die gap with a Ø6 × 2.5
diametric magnet (check the AMS magnet-selection app note); pick the interface;
specify the connector on a 14 × 14 mm board; decide whether to filter/interpolate
on-board or at the host.

## 4.2 IMU — not yet selected

A **12 × 12 mm datum pad** exists in CAD for it, standing 1.5 mm proud of the
electronics block's top face:

| | |
|---|---|
| Pad centre | X = −52.0, Z = 40.0…41.5 mm, centred on Y = 0 |
| Orientation | pad axes aligned to the robot frame (X fwd, Y left, Z up) |
| Position relative to CoM | **58.5 mm aft, 91.3 mm above** |

That offset matters: the IMU is **not** at the CoM, so accelerometer readings
include centripetal and angular-acceleration terms that must be compensated.

Research tasks: select the IMU (6-axis vs 9-axis; candidates worth comparing
include the BMI088, ICM-42688-P, LSM6DSOX and BNO085); decide whether to use a
sensor-fusion-on-chip part or run the filter on the host; specify sample rate
(≥1 kHz strongly preferred given τ = 0.103 s), interface (SPI preferred over
I²C for latency), and the calibration procedure. Specify mechanical isolation if
needed — the wheels and the jump landing are significant vibration sources.

## 4.3 Actuator-internal encoders

The GIM units have built-in encoders reporting shoulder and wheel angle over
CAN. Confirm resolution, absolute-vs-incremental behaviour, and latency. Wheel
odometry comes from here.

## 4.4 Sensors that do not exist yet and may be wanted

Foot/ground contact (currently inferred from knee angle), current sensing beyond
whatever the drivers report, pack voltage and per-cell monitoring, temperature
(motor and battery), and a bump/limit switch for self-righting detection.

---

# 5. Physical space available for electronics

Measured from the CAD by a verified free-space scan
(`snapshots/2026-08-08_post-production-fixes/free_volume.txt`). Occupancy
includes the modelled chassis parts plus an analytic shoulder-motor envelope.

**The dominant obstruction:** both shoulder motors are Ø80 cylinders about the Y
axis spanning |y| = 5…49 mm. **The entire region within r = 40 mm of the shoulder
axis is motor**, at every y. That is a big cylinder through the middle of the
chassis.

## 5.1 Usable free boxes (straddling the centre plane)

| Region | X (mm) | Z (mm) | Y (mm) | Size | Volume |
|---|---|---|---|---|---:|
| **Top-forward** | +4 … +40 | +42 … +70 | ±36 | 36 × 28 × 72 | **72.6 cm³** |
| **Centre slot** (between the two motor driver covers) | −44 … +40 | −18 … +42 | ±4 | 84 × 60 × 8 | 40.3 cm³ |
| **Aft-lower** | −64 … −44 | −18 … +2 | ±36 | 20 × 20 × 72 | 28.8 cm³ |

Plus the currently-modelled placeholder block at X −61.5…−44, Z 0…41.5, Y ±25
(17.5 × 41.5 × 50 mm), which you may re-shape freely.

**The centre slot is the interesting one.** It is only 8 mm thick, but it is
84 × 60 mm and it sits between the two motors on the centre plane — ideal for a
single main PCB. An 84 × 60 mm board is a generous size for an STM32/Teensy-class
controller plus CAN transceivers.

The **top-forward box** is the largest contiguous volume and the obvious battery
location; note the existing battery placeholder is *aft* (X −65…+4, Z 42…67), so
moving the pack forward will shift the CoM and must be re-checked (§9).

## 5.2 Free-space map

Contiguous free half-width in mm, measured outward from the centre plane
(y = 0). `.` means the centre plane itself is blocked there. The interior
half-width limit is 36 mm. Rows are Z (up), columns are X (forward).

```
   Z\X  -68 -64 -60 -56 -52 -48 -44 -40 -36 -32 -28 -24 -20 -16 -12  -8  -4   0   4   8  12  16  20  24  28  32  36
     70    .   .   .   .   .   .  36  36  36  36  36  36  36  36  36  36  36  36  36  36  36  36   .   .   .   .   .
     66    .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .  36  36  36  36  36  36  36  36  36
     62    .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .  36  36  36  36  36  36  36  36  36
     58    .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .  36  36  36  36  36  36  36  36  36
     54    .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .  36  36  36  36  36  36  36  36  36
     50    .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .  36  36  36  36  36  36  36  36  36
     46   36   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .   .  36  36  36  36  36  36  36  36  36
     42   36  36  36  36  36  36  36  36  36  36  36  36  36  36  36  36  36  36  36  36  36  36  36  36  36  36  36
     38   36  36   .   .   .   .  36  36  36  36  36  36  36  36  16  16  16  16  16  16  16  36  36  36  36  36  36
     34   36  36   .   .   .   .  36  36  36  36  36  36  16  16  16  16  16  16  16  16  16  16  16  36  36  36  36
     30   36  36   .   .   .   .  36  36  36  36  36  16  16  16  16  16  16  16  16  16  16  16  16  16  36  36  36
     26   36  36   .   .   .   .  36  36  36  36  16  16  16  16  16   4   4   4   4   4  16  16  16  16  16  36  36
     22   36  36   .   .   .   .  36  36  36  16  16  16  16   4   4   4   4   4   4   4   4   4  16  16  16  16  36
     18   36  36   .   .   .   .  36  36  36  16  16  16   4   4   4   4   4   4   4   4   4   4   4  16  16  16  36
     14   36  36   .   .   .   .  36  36  16  16  16   4   4   4   4   4   4   4   4   4   4   4   4   4  16  16  16
     10   36  36   .   .   .   .  36  36  16  16  16   4   4   4   4   4   4   4   4   4   4   4   4   4  16  16  16
      6   36  36   .   .   .   .  36  36  16  16  16   4   4   4   4   4   4   4   4   4   4   4   4   4  16  16  16
      2    .  36   .   .   .   .  36  36  16  16   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4  16  16
     -2    .  36  36  36  36  36  36  36  16  16   4   4   4   4   4   4   4   4   4   4   4   4   4   4   4  16  16
     -6    .  36  36  36  36  36  36  36  16  16  16   4   4   4   4   4   4   4   4   4   4   4   4   4  16  16  16
    -10    .  36  36  36  36  36  36  36  16  16  16   4   4   4   4   4   4   4   4   4   4   4   4   4  16  16  16
    -14    .  36  36  36  36  36  36  36  16  16  16   4   4   4   4   4   4   4   4   4   4   4   4   4  16  16  16
    -18    .  36  36  36  36  36  36  36  36  16  16  16   4   4   4   4   4   4   4   4   4   4   4  16  16  16  36
```

Reading it: the big `4` field through the middle is the 8 mm gap between the two
motor driver covers. The `.` block at X −60…−48, Z +2…+46 is the current
electronics placeholder, and the `.` block at Z +46…+66 left of X +4 is the
current battery — both of which you may move or re-shape. The `36` region at
X ≥ +4, Z ≥ +42 is genuinely empty.

Regenerate with the script that produced
`snapshots/2026-08-08_post-production-fixes/free_volume.txt`; it self-tests its
occupancy probes before reporting.

## 5.3 Other physical facts

- The chassis is an **open cage** — no skin, no lid, no ingress protection.
  Designing an enclosure is in scope if you want any.
- `Electronics_Tray` is a 2 mm ABS panel at X −64…−62, Z −16…+40, Y ±38,
  currently an unused mounting surface.
- The chassis frame is PA-CF, i.e. **electrically insulating and thermally
  insulating**. There is no metal chassis ground plane and no natural heatsink.
- No cooling of any kind is currently provided.

---

# 6. Wiring topology

## 6.1 What crosses which joint

| Run | Crosses | Notes |
|---|---|---|
| Shoulder motor ↔ body | **nothing** | motor is bolted to the body; short fixed run |
| Wheel motor ↔ body | shoulder (±185°) **and** knee (−8…+27°) | the long one |
| Knee encoder ↔ body | shoulder (±185°) only | encoder is on the proximal link |

## 6.2 Route for everything distal of the shoulder (per leg)

```
wheel motor connector  (y ≈ 61.5…67.5, in the distal plate's Ø41.5 pocket)
        │  up the distal link's 20 mm internal channel
        ├── knee service loop, sized for −8°…+27°
        │  up the proximal link's internal channel
        ├── Ø8 pass-through in the proximal link root, r = 21, angle 30.4°
        ├── Ø6 port in the rotating hub, r = 21, angle 30.4°   ── strain relief
        ├── CLOCK-SPRING CAVITY, r = 20…32, 4 mm tall, ~3 turns, ~400 mm
        └── Ø7 grommet in the fixed side panel, r = 29, angle 200°  ── strain relief
                → into the chassis
```

The **knee encoder** joins this route from the outboard side (its PCB is at
y = 98.3) through a cable slot in the bracket shelf, then inboard into the
proximal link channel.

Approximate run lengths per leg (compute exactly from CAD if it matters):
wheel motor ≈ 700 mm, knee encoder ≈ 570 mm — both dominated by the 400 mm
clock-spring coil.

## 6.3 Wiring research tasks

- Full **wiring diagram**: power distribution, CAN bus topology and termination
  (120 Ω at both physical ends — decide where they are given the star-ish
  layout), grounding and shield strategy, and the encoder runs.
- **CAN bus integrity** with 4 nodes on a bus whose branches pass through a
  rotating clock spring. Assess stub lengths and whether one bus or two
  (left/right) is better.
- **Connectors** at every joint that must be serviceable. Mechanical
  requirement: the wheel motor must be removable with the leg assembled, so its
  connector has to be reachable and unpluggable.
- **Flex life**: the clock-spring cable sees ±185° repeatedly. The mechanical
  test plan already calls for 500 cycles of ±185° followed by insulation
  inspection — specify the cable so it passes.
- **EMI**: motor phase currents and encoder signals share a confined space.

---

# 7. Compute and control

## 7.1 What the controller must do

1. **Balance** on two wheels. Unstable pole ≈9.7 rad/s (τ = 0.103 s). This is the
   baseline always-on task.
2. **Drive** — translate and turn via differential wheel torque.
3. **Ride-height / posture control** via the shoulders. Note the mechanism: the
   shoulder rotates the whole bent leg while the driven wheel rolls to take up
   the fore-aft motion. Shoulder squat at θ = +30° lowers the body 20.7 mm while
   the wheel travels 77.1 mm fore-aft.
4. **Jump** — rotate both shoulders fast to drive the wheels into the ground.
5. **Land** — the passive knees take the first impact; the shoulders must
   **yield and damp actively**, not lock. This is a torque-mode requirement.
6. **Self-right** — the shoulders have ±185° specifically so the robot can
   recover from being upside down.

## 7.2 Estimation

| Quantity | Source |
|---|---|
| Body pitch / roll / rates | IMU (with CoM-offset compensation, §4.2) |
| Shoulder angle | GIM6010-8 internal encoder, over CAN |
| Wheel angle / speed | GIM4305-10 internal encoder, over CAN |
| **Knee angle** | AS5048A, −8°…+27° |
| **Leg compression / ground force** | derived from knee angle via §8.2 |
| Contact detection | knee angle and its rate |

## 7.3 Loop rate guidance

With an unstable pole at 1.55 Hz, a control bandwidth of ~8–15 Hz is a
reasonable target, implying a **≥200 Hz** control loop and preferably 500–1000 Hz.
Landing events are much faster (a 1.4 m/s impact into a knee with ~16 mm of
travel is a ~20 ms event), so **contact detection and the landing response want
≥1 kHz**. Verify the CAN bus can sustain the required command+telemetry rate for
4 actuators at your chosen loop rate — this may be the binding constraint.

## 7.4 Compute research tasks

- Select the compute. Consider the split between a hard-real-time MCU
  (STM32/Teensy-class) for balance and CAN, and an optional Linux SBC for
  higher-level work. Evaluate whether an SBC is needed at all for Prototype 1.
- Board must fit §5 — the 84 × 60 × 8 mm centre slot is the natural home.
- Specify CAN interface hardware (transceivers, isolation?), power regulation
  from pack voltage to logic rails, and inrush/precharge.
- **Safety**: e-stop, motor disable, watchdog, brownout behaviour, and what
  happens on a CAN dropout mid-jump.
- **Battery management**: BMS or not, per-cell monitoring, low-voltage cutoff,
  charge port and charging strategy.
- Software stack: bare-metal vs RTOS vs ROS 2 / micro-ROS; how it interoperates
  with `sim/beni.urdf`.
- **Regenerative energy on landing** — where does it go? Check whether the
  drivers can sink it into the pack and whether a brake resistor is needed.

## 7.5 Simulation

`sim/beni.urdf` has the true masses and inertias for all 6 moving links, with
joint limits. Note two things when using it:

- The **knee is passive**. The URDF gives you the mechanical limits, but the
  simulator must supply the spring itself — a nonlinear joint spring following
  §8.2. It is not a constant-rate torsion spring; the moment arm rises with
  flexion.
- The cartridge is a floating two-pivot member. In the URDF its upper eye and rod
  are lumped into the thigh and its lower eye, shims and spring into the shank.

---

# 8. Reference data for control code

## 8.1 Joint limits and conventions

| Joint | Type | Range | Axis | Notes |
|---|---|---|---|---|
| Shoulder | revolute, **actuated** | −185°…+185° | +Y | not continuous |
| Knee | revolute, **PASSIVE** | −8°…+27° | +Y | hard stops both ends |
| Wheel | continuous, **actuated** | ∞ | +Y | r = 55 mm |

Knee sign convention, do not reverse it: with the proximal link fixed,
**distal link angle = −50° − φ**. Positive φ = flexion = the leg compressing.
φ = +20° is where the progressive bumper first touches; +25° is the design point;
+27° is the metal hard stop.

Forward kinematics at shoulder angle θ, knee angle φ (nominal link angle
A = 50°, L1 = L2 = 120 mm), in the sagittal plane before applying θ:

```
knee   K = ( L1·sin A,            −L1·cos A )                 = ( 91.925, −77.135)
wheel  W = ( Kx + L2·sin(−A−φ),   Kz − L2·cos(−A−φ) )
then rotate both about +Y by θ.
```

## 8.2 The knee spring — this is your force sensor

Cartridge anchors: upper pivot radius Ru = 36 mm, lower Rl = 54 mm from the knee
axis, included angle (110° − φ). Spring rate 10.45 N/mm.

```
eye_to_eye(φ) = sqrt(Ru² + Rl² − 2·Ru·Rl·cos(110° − φ))
moment_arm(φ) = Ru·Rl·sin(110° − φ) / eye_to_eye(φ)
spring_force(φ) = 30.0 + 10.45·(eye_to_eye(−8°) − eye_to_eye(φ))     [N]
ground_force(φ) = spring_force(φ)·moment_arm(φ) / |Wx(φ) − Kx|       [N per wheel]
```

| φ | eye-to-eye mm | moment arm mm | spring force N | **ground force N** | vertical compression mm |
|---:|---:|---:|---:|---:|---:|
| −8° | 77.70 | 22.09 | 30.0 | **8.3** | −12.04 |
| 0° | 74.44 | 24.54 | 64.0 | **17.1** | 0.00 |
| +5° | 72.24 | 25.99 | 87.1 | **23.0** | 8.31 |
| +10° | 69.91 | 27.39 | 111.4 | **29.4** | 17.13 |
| +15° | 67.46 | 28.71 | 137.0 | **36.2** | 26.42 |
| +20° | 64.90 | 29.95 | 163.8 | **43.5** | 36.09 |
| +25° | 62.23 | 31.12 | 191.6 | **51.4** | 46.08 |
| +27° | 61.14 | 31.56 | 203.0 | **54.8** | 50.14 |

Effective wheel rate is mildly progressive, ≈0.745 N/mm. Preload is mechanically
tunable from 30.0 N down to 9.1 N at φ = −8° by removing shims — so the
controller should **read** the preload from a calibration, not assume it.

## 8.3 Energy and load limits

| | |
|---|---:|
| Energy the two knees absorb, φ = 0 → +27° | **3.553 J** |
| Energy of a 100 mm free drop at 3.29 kg | 3.23 J (impact 1.40 m/s) |
| Margin | ≈10 % — **the shoulders must participate in landing** |

> **[CORRECTION — 2026-08-11]** The ≈10% figure omits m·g·Δz work done during
> the ~50 mm of compression. When included, demand is **4.85 J** vs 3.55 J
> capacity — **a 100 mm free drop bottoms out.** Passive free-drop capacity is
> **~49 mm** (spring-rate method). See `electronics/04_firmware.md` correction 3.

| Knee torque at the +27° hard stop | 6.41 N·m |
| Structural proof load | 275 N at one wheel (≈8 g) |

**Do not let the controller reach the +27° stop.** The mechanical test plan
requires **(a) a 49 mm free drop never exceeds +24° passively, and (b) a 100 mm
drop never exceeds +24° with the shoulder landing controller active** — see
`electronics/06_logging_and_bringup.md` Stage 5.

## 8.4 Shoulder torque demand — the gating number

| Case | Required per leg |
|---|---:|
| Hold the leg statically | 0.49 N·m |
| **Drive a 3 g jump (lever ≈120 mm)** | **≈5.9 N·m** |
| Structural proof design | 25 N·m (structure only) |

**The jump sits at or just above continuous rated torque** (~4.6–5.4 N·m) and
depends on peak/stall capability. This is the design's central unverified
assumption and it is why §2.3 and §3.1 matter so much.

---

# 9. Mass and CoM budget — you must not break this

| | |
|---|---:|
| Current total | **3290 g** |
| Design mass | 3500 g |
| **Margin** | **≈210 g (6.0 %)** |
| Battery allowance in that total | 250 g |
| Electronics allowance in that total | 120 g |

Both actuator masses are estimates; a 10 % error on the shoulder pair alone is
100 g, i.e. half the margin.

**Whatever you add, report its mass and location so the CoM can be re-checked.**
Two properties are load-bearing for the controller:

- **CoM Y must stay ≈0.** It is currently −0.00 mm. Anything mounted off-centre
  breaks lateral symmetry.
- **CoM X and height** set the standing trim and τ. Moving the battery forward
  into the top-forward box (§5.1) will change both.

`beni_lib.mass_report()` recomputes all of this from the CAD in one call.

---

# 10. Explicit deliverables requested

1. **Resolved battery specification** — chemistry, voltage/series count,
   capacity, real physical dimensions that fit §5, mass, discharge rating,
   connector, and a source. Plus BMS/charging approach.
2. **Confirmed actuator variants** with datasheets, torque-speed curves, CAN
   protocol documentation, and connector pinouts.
3. **Full wiring diagram** — power distribution, CAN topology and termination,
   encoder runs, grounding and shielding, connector schedule.
4. **Clock-spring cable specification** that fits a ≤4 mm axial envelope, carries
   7–10 conductors including wheel-motor power, and survives ±185° flex life.
5. **Compute and sensor selection** — main controller, IMU, any auxiliary
   sensors, with a board outline that fits §5.
6. **Power budget** — standing, driving, jumping, and estimated runtime.
7. **Safety design** — e-stop, watchdog, low-voltage cutoff, CAN-loss behaviour,
   regenerative energy handling on landing.
8. **Firmware architecture** — loop rates, task decomposition, state estimation,
   the balance controller, the jump and landing state machine, and the
   calibration/homing procedure.
9. **A bring-up plan** that fits the existing mechanical test sequence: encoder
   check → static sweeps → spring-rate calibration → static load → low-energy
   drops → powered jump last.
10. **Any mechanical changes you need**, called out explicitly — mounting
    features, cable routing, an enclosure, cooling. The CAD is parametric
    (`beni_lib.py`) and these are cheap to add now.

---

# 11. Source material

## In this repository

| File | What it holds |
|---|---|
| `beni_prototype1_rev2_changes.md` | current state and every recent design decision |
| `beni_prototype1_design_record.md` | as-designed record: kinematics, layout, load cases, clearances |
| `beni_prototype1_bom_and_assembly.md` | BOM, fastener schedule, mass roll-up, assembly sequence |
| `beni_prototype1_fusion_guide_rewritten.md` | the original requirements/spec |
| **`sim/beni.urdf`**, `sim/beni_inertia.json` | kinematic tree, true masses and inertias |
| `manufacturing/machined_parts_spec.md` | part tolerances and fits (nothing is machined any more — see `MANUFACTURING_CONSTRAINTS.md`) |
| `snapshots/2026-08-08_post-production-fixes/free_volume.txt` | the free-space scan behind §5 |
| `beni_lib.py` | parametric CAD source; `mass_report()`, `audit_all()` |
| `web/index.html` | self-contained 3D viewer with live kinematics |

## External references (from the original spec — re-verify, they may be stale)

- Steadywin GIM6010-8: <https://www.steadywin.cn/en/pd.jsp?fromColId=0&id=116>
- Steadywin GIM4305-10: <https://www.steadywin.cn/pd.jsp?id=9>
- Mondo Robotics Beni: <https://mondorobotics.com/>
- Ascento (the closest published wheeled-biped control work): <https://arxiv.org/abs/2005.11435>
- AS5048A datasheet and the AMS magnet-selection app note (find current links)

## Known-stale figures — do not trust these if you see them quoted

- "9 N·m rated / 25 N·m peak" for the GIM6010-8 — **wrong**, it is an old
  assumption that survives in some early notes. 25 N·m is a *structural proof*
  figure, never a motor capability claim.
- Any robot mass of 8174 g — that was a CAD artifact from unassigned materials,
  now fixed. The real figure is 3290 g.
