# 05 — Open Questions, Conflicts and Change Requests

Covers brief §10 deliverable **10** (mechanical changes), plus everything that
is not yet resolved. **Read this before ordering anything.**

## 1. Blockers — work stops until these are answered

### B1. GIM4305-10 wheel-driver absolute-maximum DC bus voltage and regen clamp

⚠ **DRIVER PART NUMBER CORRECTED 2026-08-20.** This blocker was written against
an **SDC101**. The delivered order line reads **"GIM4305-10 … with GDZ34
driver"** (order screenshot, delivered 2026-08-16, user-confirmed as the source
of truth); the shoulder line reads **"motor-GDZ468-DE"**. The string "SDC101"
came from earlier research and appears nowhere in the vendor's own order record.
**Every voltage figure in the table below was asked about the wrong part number**
and does not necessarily transfer. Confirm against the label on the physical
driver.

**This single answer decides 5S vs 6S vs 6S-plus-buck**, and therefore the pack,
the harness gauge, the power tree and half the BOM.

Sources conflict badly:

| Source | Range |
|---|---|
| Base datasheet / reseller tables | 12–24 V |
| ~~SDC101~~ installation guide **[part number unconfirmed — see above]** | 12–36 V |
| Marketing copy | 12–48 V |
| One listing | 0–26 V rated, 30 V max, "supports 6S LiPo" |
| **GDZ34 boards, vendor doc tier (web, 2026-08-20)** | **12–40 V**, with one GIM4305-10 manual giving 12–24 V |

**Consequence for the rig: B1 no longer gates the Mode A build.** The rig runs at
**20 V**, which is inside every range above including the narrowest (12–24 V).
B1 still gates the two-leg pack decision, where 6S at 25.2 V full is the exposure.

The hazard is regen, not charge voltage. 25.2 V into a 24 V-max driver has
*negative* headroom before the wheel even starts back-driving.

### B2. Wheel-driver CAN protocol document and connector pinout

⚠ Same part-number correction as B1: written against ~~SDC101~~, delivered as
**GDZ34**.

The GIM4305-10 speaks a proprietary "SteadyWin" protocol or MIT mode — not
ODrive CANSimple. **The command table, the CAN MASTER ID semantics, the default
bitrate, and the 4-pin connector type and pinout are all unpublished.** You
cannot write the wheel driver's firmware or terminate its cable without them.

**Partial answers, vendor doc tier (web, 2026-08-20) — unverified, confirm
against the driver's own manual:** the GDZ series does CAN, RS485 and Modbus, and
the CAN interface is described as **MIT-protocol compatible** (a much better
starting point than "proprietary, undocumented"). CAN settings shown in the
GIM43-series driver docs: **1 Mbps**, 8-byte standard data frames, **default CAN
ID 1**. Start, stop, zero-position and mode-switch commands are defined in the
MIT-style set. The 4-pin connector part number is **still unpublished**.

⚠ **Bitrate mismatch to plan for.** `03_compute_and_can.md` specifies **500 kbps**
for the rig because "breadboard impedance cannot hold 1 Mbps stubs", while the
GDZ34 default appears to be **1 Mbps**. Either reconfigure the driver down to
500 kbps during bring-up, or keep stubs ≤30 mm and accept 1 Mbps. Do not assume
the driver comes up at the rate the firmware expects.

### B3. MIT-mode (0x008) scaling constants for the GIM6010-8

The bit packing is the standard Mini-Cheetah layout, but the
position/velocity/torque **ranges** were not recovered. Without them, any MIT
frame you send is a guess. Workaround in the meantime: use `0x00E
Set_Input_Torque`, which takes a plain float in N·m.

## 2. Unresolved conflicts

| # | Conflict | Impact | Resolution |
|---|---|---|---|
| C1 | GIM6010-8 abs-max bus: 56 V vs 60 V vs 72 V | Low at 6S — all three are comfortable | Ask, but do not wait |
| C2 | GIM6010-8 dimensions: brief says Ø80 × 44, research says Ø80 × 40 | 4 mm per side of CAD interface | **Measure the delivered unit** |
| C3 | GIM4305-10 dimensions: brief says Ø53 × 33, research says Ø53 × 26 | 7 mm at the wheel end plate | **Measure the delivered unit** |
| C4 | Actuator masses: BOM assumes 500 g / 250 g, research says 388 g / 150 g | ~420 g — **twice the entire robot margin, in the good direction** | **Weigh them on arrival.** If true, the whole mass picture relaxes and 6S2P is trivially affordable |
| C5 | Clock-spring capacity: design record 430–470°, recomputation 390° | 5% margin, not 27% | Resolved — see `02_harness_and_routing.md` §2.2. Design record needs correcting |
| C6 | Harness research said 48 V was required to fit the cable | Would have forced a different pack | Resolved — that analysis assumed a 100 W wheel; the GIM4305-10 is ~40 W. 20 V + 22 AWG fits |
| C7 | GIM6010-8 phase R: 0.42 Ω (research) vs 0.15 Ω (earlier assumption) | ±50 W in the peak power budget | Measure with a milliohm meter |
| C8 | Landing energy: brief says a 100 mm drop is 3.23 J vs 3.553 J capacity ("~10% margin"); recomputation says **4.85 J demand** | The brief omits the m·g·Δz work done during ~50 mm of compression. **A 100 mm free drop bottoms out; passive capacity is ~49 mm for the two-leg robot's 1-DOF model** (spring-rate method; see `fusion_brief_single_leg_rig.md` §4.3). **The single-leg rig's 2-DOF reality is tighter: 45 mm planning limit, +24° crossed at 46.3 mm** — `beni_single_leg_rig_design_record.md` §3 | Resolved analytically — see `04_firmware.md` correction 3. **The brief's drop-test gate has been rewritten** (`06_logging_and_bringup.md` Stage 5, `fusion_brief_single_leg_rig.md` §6). Verify empirically with the 10 mm-step drop series |
| C9 | Unstable pole: brief says 9.7 rad/s, URDF-derived model says **11.20 rad/s** | 15% less time to react; also a +6.53 rad/s RHP zero the brief does not mention | Resolved — see `04_firmware.md` §2. Design record corrected |
| C10 | Rotor inertia for both motors: **not published anywhere** | `N²·J_rotor` is 64× and 100× reflected; shifts `K_ẋ` by up to 13% and is the #1 sim-to-real gap | Ask Steadywin (Q15); failing that, measure by spin-down |

## 3. Questions for Steadywin

Send as one message, with the serial numbers and driver revisions of the units
in hand. Firmware and hardware revisions are coupled on these parts (HW 3.8
variant 1 → fw 0.5.13; HW 3.10 → 0.5.16), so a generic answer is not useful.

1. **GIM4305-10 / SDC101: absolute maximum DC bus voltage** for our driver
   revision, and the **overvoltage / regen clamp threshold**. Is 6S (25.2 V)
   safe including regenerative braking?
2. **GIM6010-8 absolute maximum DC bus voltage** for our revision. Published
   figures range 56–72 V.
3. Are the 24 V and 48 V GIM6010-8 columns **two SKUs or one motor
   characterised twice**? Which did we receive?
4. **Phase resistance and inductance**, measured, for both motors.
5. **SDC101 CAN protocol document** — full command table, frame layouts,
   default bitrate, and the CAN MASTER ID scheme.
6. **SDC101 4-pin connector**: manufacturer part number and pinout.
7. **GIM6010-8 MIT-mode (0x008) scaling ranges** for position, velocity and
   torque.
8. **Encoder behaviour**: is the GIM6010-8 encoder single- or multi-turn, and
   is position retained across a power cycle?
9. **Brake resistor**: recommended ohms and watts for the GIM6010-8's brake
   interface. Can the driver safely sink regen into a battery, and at what
   current?
10. **The 5-pin connector**: two pins are documented as the brake interface.
    What are the other three?
11. **Confirm dimensions**: Ø80 × 40 or × 44? Ø53 × 26 or × 33?
12. **Confirm masses**: 388 g and 150 g?
13. Is there an **official SDK or GitHub repository**? The manual points at
    `pip install odrive` and `odriverobotics/odrive_can`, tested only on
    Ubuntu 23.04 / ROS 2 Iron. The firmware appears to be a closed ODrive 0.5.x
    fork with no source release.
14. Confirm the **XT30PB(2+2) pinout** on the GIM6010-8. Our working assumption
    (1 = V+, 2 = GND, 3 = CAN_L, 4 = CAN_H) is taken from a CyberGear reference
    and is **unverified.** The drive is not reverse-polarity protected, so
    getting this wrong destroys it.
15. **Rotor inertia (J_rotor) for both motors**, motor-side, kg·m². Reflected
    through 8:1 and 10:1 this is 64× and 100×, it shifts the balance gains by
    up to 13%, and it is the largest single sim-to-real error source for a
    geared drive (`04_firmware.md` §3.2, §8). Not published in any datasheet we
    found. If it cannot be supplied, we will measure it by free spin-down.

## 4. Mechanical change requests (deliverable 10)

The CAD is parametric, so these are cheap now and expensive later. Ordered by
value.

### CR-1 — Open the top-forward box in Z from 28 to 40 mm. **[HIGH]**

Enables **6S2P**: two GNB 6S 550 packs, 164 g, 24.4 Wh. Doubles runtime from
~13 to ~26 min mixed, and halves peak C-rate from ~56 C to ~28 C — which
matters more than the runtime, because 56 C on a 100 C-rated pack in 200 ms
bursts is where cells go soft early. Still inside the 250 g battery allowance.
**The single highest-value change on this list.**

### CR-2 — Clock-spring free length 400 → 500 mm. **[HIGH]**

BOM §6 currently specifies "≥400 mm coiled per shoulder". At 400 mm the wrap
margin is 5%, not the 27% the design record claims. 500 mm still clears
radially at both wound-in (r = 27.8 < 32) and wound-out (r = 26.0 > 20.5).
Mass +2 g/leg. Also update design record §4.3 and §13.

### CR-3 — Move the power stage out of the 8 mm centre slot. **[HIGH]**

Put the 20 V buck, the 5 V buck and the brake resistor in the 36 × 28 × 72
top-forward box; feed only 5 V into the slot. PA-CF is ~0.5 W/m·K with no
airflow, and 1.5–2.0 W in a sealed 8 mm plastic slot is not survivable. The
slot then dissipates ~0.15 W. Requires a routing path for 5 V and the motor
branch between the two volumes.

### CR-9 — Move the IMU datum pad to wheel-axis height. **[HIGH]**

The pad at X = −52.0, Z = 40.0…41.5 sits **195 mm above the wheel axis** — the
largest lever arm available anywhere on the robot. At an achievable 20 rad/s²
of pitch acceleration the tangential term is 3.9 m/s², i.e. **22° of apparent
tilt against a 0.1° pitch-bias budget** (`03_compute_and_can.md` §4.2).
Relocating the pad to wheel-axis height makes r_z → 0 and the term vanishes; it
also puts the accelerometer where its output is directly comparable with wheel
odometry. Free in CAD today, and the software workaround (model-based θ̈) is
strictly worse. **If the pad cannot move, say so now** so the observer is
written for it from the start rather than retrofitted.

### CR-10 — MicroSD socket and log-card access. **[HIGH]**

Not strictly a chassis change, but it constrains one: the main board needs a
**push-pull micro-SD socket, 1.2–1.4 mm tall, bottom-side**, plus four SDIO
lines and a card-detect. The chassis needs a **slot or removable cover giving
card access without disassembly** — you will pull this card dozens of times a
day during Stages 3–6. The robot fails in 20–200 ms events and cannot be
debugged any other way; see `06_logging_and_bringup.md` §1.

### CR-4 — Satellite PCB mount on each proximal link. **[MEDIUM]**
**Two-leg robot only — moot for the rig**, which has no satellite node (the
AS5048A is read directly by the Teensy). Still live for the two-leg build.
A ~20 × 25 mm boss with two M2 heat-set inserts, inboard face, within 40 mm of
the knee axle so the AS5048A SPI run stays short. ~2 g of print. Delete this if
the SDC101's second-encoder header can take the AS5048A directly (B2).

### CR-5 — Strain-relief clamps at both clock-spring grommets. **[MEDIUM]**

Assembly steps B3 and B5 call for strain relief but no part carries it. Add a
small clamp feature (or a printed saddle plus a cable tie) at the Ø7 plate
grommet at r = 29 and the Ø6 hub port at r = 21. **This is the part that fails
first if it is left to the builder's judgement.**

### CR-6 — PTFE slip sheets in the clock-spring cavity. **[MEDIUM]**

**Two-leg robot only — moot for the rig**, whose clock spring is deleted. Still
live for the two-leg build.

0.15 mm PTFE on both cavity faces. Costs 0.3 mm of the 4.0 mm usable width
(already accounted — the cable is specified at 2.2 mm thick × 3.0 mm wide) and
removes the dominant wear mechanism on a ±185° oscillating spiral. Two die-cut
annuli per shoulder, negligible mass.

### CR-7 — Vent the centre slot. **[LOW]**

Two or three 8 mm slots in the chassis frame above and below the PCB. Buys
little in still air, but it is free at print time and cannot hurt.

### CR-8 — Main PCB mounting in the centre slot. **[LOW]**

Four M2.5 standoffs or printed bosses on an 84 × 60 footprint, with the board
plane centred in the 8 mm so both sides get their 3.5 / 2.5 mm. Confirm the
board outline against the real slot before fab — this is the change most likely
to bite during rev-A bring-up.

## 5. Things to verify with your own hands before committing

In priority order. Every one of these is cheap now and expensive after a PCB
order.

1. **Weigh both actuators.** C4 — potentially 420 g of margin.
2. **Measure both actuators.** C2, C3 — the CAD interfaces depend on it.
3. **Measure GIM6010-8 output torque on a lever arm.** Published bench tests
   found 4.8–9.4 N·m against an 11 N·m rating. The jump needs 5.9 N·m.
4. **Put an inline watt meter on the pack** on the first powered bench run.
   Every power figure in `01_power_and_battery.md` is an estimate.
5. **Measure phase resistance** on both motors (C7).
6. **Scope the CAN bus** and confirm nothing in the middle of a chain is
   terminated.
7. **Confirm the WeAct core board's 36.28 mm** against the 36.0 mm box, if you
   end up on the fallback controller.
8. **Measure the knee spring in situ** — preload F₀ and rate k. Every contact
   threshold in `04_firmware.md` §4 and every row of the landing-energy table
   scales with them, and preload is shim-dependent. **Do not assume 30.0 N.**
9. **Measure rotor inertia by spin-down** if Steadywin will not supply it (C10).
10. **Run the 10 mm-step drop series** (`06_logging_and_bringup.md` Stage 5) and
    plot φ_peak vs height before believing any landing-energy number here.

## 6. Deferred to prototype 2

- Linux SBC / ROS 2 planner over 3 Mbaud DMA UART. Not in the balance loop.
- CAN-FD. Neither Steadywin part supports it today; the three-bus split makes
  it unnecessary anyway.
- Galvanic isolation on CAN.
- Any attempt to control roll in flight — there is no actuator for it.
