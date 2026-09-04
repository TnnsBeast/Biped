# Mechanical and geometric datum for electronics

CAD-derived reference data extracted from the original electronics handoff brief
(`beni_electronics_handoff_brief.md`, since deleted — the rest of it was either
answered by `01`–`07` or specified an architecture that is not being built).
This is the **frozen datum** that
`electronics/01_power_and_battery.md` through `07_bom.md` are designed against.
Every number here comes from the Fusion model of **Beni Prototype 1, revision 2**
(`Biped → Beni_Prototype1`); if the model changes, these figures must be
re-extracted from CAD — they cannot be regenerated any other way.

The original brief requested a custom STM32G474 board, a 6S pack, three CAN
buses, a BMS and satellite nodes. **That is not what is being built.** The actual
current build target is the **single-leg test rig** — Teensy 4.1, 20 V bench
supply, breadboarded buses (`../fusion_brief_single_leg_rig.md`). Only the
geometry and dynamics below carry forward.

Two figures in the source brief were wrong and have been corrected here: the
unstable pole (§2) and the clock-spring rotation margin (§3).

---

## 1. Coordinate frame (brief §1.1)

| axis | direction |
|---|---|
| **+X** | forward |
| **+Y** | left |
| **+Z** | up |

Origin is on the **shoulder axis**, which is the global Y axis. All three joint
types rotate about **+Y**. At the nominal pose the wheel axis is directly below
the origin at (0, ±84, −154.269) mm.

---

## 2. Mass, inertia and pendulum dynamics (brief §1.2)

Measured from CAD, not estimated.

| Property | Value |
|---|---:|
| Mass | **3.309 kg** |
| Overall L × W × H | 183 × 217 × 281 mm |
| Track (wheel centre to wheel centre) | 168 mm |
| Wheel diameter / radius | 110 mm / **55 mm** |
| Ride height (shoulder axis to ground) | 209.3 mm |
| **CoM** (X, Y, Z from shoulder axis) | **(+6.47, −0.00, −50.10) mm** |
| **CoM height above the wheel axis** | **104.2 mm** |
| Ixx about CoM (roll) | 0.03231 kg·m² |
| **Iyy about CoM (pitch — governs balance)** | **0.02525 kg·m²** |
| Izz about CoM (yaw) | 0.01719 kg·m² |
| Ixz about CoM | +0.002796 kg·m² |
| **Inverted-pendulum time constant** √(L/g) | **0.103 s** |

Per-link masses and full inertia tensors for all 6 moving links:
**`sim/beni.urdf`** and **`sim/beni_inertia.json`**. Mass closure is exact.

**Unstable pole.** The unstable pole sits at **11.20 rad/s** (τ = 89 ms).[^pole]
This is a *short, twitchy* pendulum — shorter than most balancing robots. It
drives the control-loop rate and the IMU latency budget.

**Standing trim.** The CoM is 6.47 mm forward of the wheel contact patch. That is
a permanent **0.21 N·m** bias (0.11 N·m per wheel) that the controller must hold,
and it means the equilibrium stance sits a few degrees off the nominal pose. It
is inherent to the bent-leg geometry and cannot be ballasted out.

[^pole]: The original brief stated ≈9.7 rad/s (1.55 Hz) in both §1.2 and §7.1,
derived from the bare LIPM formula, which drops body pitch inertia and the wheel
reaction torque. The current URDF-derived value is 11.20 rad/s — see
`04_firmware.md` correction 1 and `05_open_questions.md` C9.

---

## 3. Clock-spring cavity geometry (brief §3.3)

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
| Entry (fixed side) | Ø7 grommet in the panel at r = 29, angle 200° |
| Exit (rotating side) | Ø6 port in the hub at r = 21, angle 30.4° |

**Rotation margin.** The brief and design record claimed ~430–470° of capacity
against the 370° required, i.e. "≈20 % margin". That is wrong. Recomputing from
the annulus gives 390° from 400 mm of cable — **20° / ~5 % margin**, with 369 mm
required for exactly 370°. See `02_harness_and_routing.md` §2.2. There is
essentially no margin to spend.

Strain relief is required at **both** ends (panel side and rotating hub side);
the mechanical design requires it but does not detail it.

---

## 4. Knee encoder mechanical stack — AS5048A (brief §4.1)

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

---

## 5. IMU datum pad (brief §4.2)

A **12 × 12 mm datum pad** exists in CAD for the IMU, standing 1.5 mm proud of
the electronics block's top face:

| | |
|---|---|
| Pad centre | X = −52.0, Z = 40.0…41.5 mm, centred on Y = 0 |
| Orientation | pad axes aligned to the robot frame (X fwd, Y left, Z up) |
| Position relative to CoM | **58.5 mm aft, 90.8 mm above** |

That offset matters: the IMU is **not** at the CoM, so accelerometer readings
include centripetal and angular-acceleration terms that must be compensated.

---

## 6. Physical space available for electronics (brief §5)

Measured from the CAD by a verified free-space scan
(`snapshots/2026-08-08_post-production-fixes/free_volume.txt`). Occupancy
includes the modelled chassis parts plus an analytic shoulder-motor envelope.

**The dominant obstruction:** both shoulder motors are Ø80 cylinders about the Y
axis spanning |y| = 5…49 mm. **The entire region within r = 40 mm of the shoulder
axis is motor**, at every y. That is a big cylinder through the middle of the
chassis.

### 6.1 Usable free boxes, straddling the centre plane (brief §5.1)

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
moving the pack forward will shift the CoM and must be re-checked.

### 6.2 Free-space map (brief §5.2)

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

### 6.3 Other physical facts (brief §5.3)

- The chassis is an **open cage** — no skin, no lid, no ingress protection.
  Designing an enclosure is in scope if you want any.
- `Electronics_Tray` is a 2 mm ABS panel at X −64…−62, Z −16…+40, Y ±38,
  currently an unused mounting surface.
- The chassis frame is PA-CF, i.e. **electrically insulating and thermally
  insulating**. There is no metal chassis ground plane and no natural heatsink.
- No cooling of any kind is currently provided.

---

## 7. Harness route for everything distal of the shoulder, per leg (brief §6.2)

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

---

## 8. Forward kinematics and the knee sign convention (brief §8.1)

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

---

## 9. The knee spring — this is your force sensor (brief §8.2)

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

Every drop-series number in the rig documents traces back to this table.

---

## 10. Knee energy and load limits (brief §8.3)

| | |
|---|---:|
| Energy the two knees absorb, φ = 0 → +27° | **3.553 J** |
| Knee torque at the +27° hard stop | 6.41 N·m |
| Structural proof load | 275 N at one wheel (≈8 g) |

**Do not let the controller reach the +27° stop.** The mechanical test plan
requires **(a) a 45 mm free drop never exceeds +24° passively, and (b) a 100 mm
drop never exceeds +24° with the shoulder landing controller active** — see
`electronics/06_logging_and_bringup.md` Stage 5.

> The brief's "100 mm free drop = 3.23 J, ≈10 % margin" comparison omits the
> m·g·Δz work done during the ~50 mm of compression. With it included, demand is
> **4.85 J** vs 3.55 J capacity — **a 100 mm free drop bottoms out.** Passive
> free-drop capacity is **~49 mm** on the two-leg robot's 1-DOF model; the
> single-leg rig's 2-DOF integration gives a **45 mm** planning limit with +24°
> crossed at **46.3 mm** (`../beni_single_leg_rig_design_record.md` §3). See
> `electronics/04_firmware.md` correction 3.

---

## 11. Source material and known-stale figures (brief §11)

### In this repository

| File | What it holds |
|---|---|
| `beni_prototype1_rev2_changes.md` | current state and every recent design decision |
| `beni_prototype1_design_record.md` | as-designed record: kinematics, layout, load cases, clearances |
| `beni_prototype1_bom_and_assembly.md` | BOM, fastener schedule, mass roll-up, assembly sequence |
| `beni_prototype1_fusion_guide_rewritten.md` | the original requirements/spec |
| **`sim/beni.urdf`**, `sim/beni_inertia.json` | kinematic tree, true masses and inertias |
| `archive/manufacturing/machined_parts_spec.md` | part tolerances and fits (nothing is machined any more — see `MANUFACTURING_CONSTRAINTS.md`) |
| `snapshots/2026-08-08_post-production-fixes/free_volume.txt` | the free-space scan behind §6 |
| `beni_lib.py` | parametric CAD source; `mass_report()`, `audit_all()` |
| `web/index.html` | self-contained 3D viewer with live kinematics |

### External references (from the original spec — re-verify, they may be stale)

- Steadywin GIM6010-8: <https://www.steadywin.cn/en/pd.jsp?fromColId=0&id=116>
- Steadywin GIM4305-10: <https://www.steadywin.cn/pd.jsp?id=9>
- Mondo Robotics Beni: <https://mondorobotics.com/>
- Ascento (the closest published wheeled-biped control work): <https://arxiv.org/abs/2005.11435>
- AS5048A datasheet and the AMS magnet-selection app note (find current links)

### Known-stale figures — do not trust these if you see them quoted

- "9 N·m rated / 25 N·m peak" for the GIM6010-8 — **wrong**, it is an old
  assumption that survives in some early notes. 25 N·m is a *structural proof*
  figure, never a motor capability claim.
- Any robot mass of 8174 g — that was a CAD artifact from unassigned materials,
  now fixed. The current Fusion figure is 3309 g.
- An unstable pole of 9.7 rad/s — superseded by 11.20 rad/s (§2).
- A clock-spring rotation margin of 20–27 % — it is ~5 % (§3).
