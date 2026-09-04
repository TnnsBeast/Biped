# 03 — Actuators, Compute and Sensing

Covers brief §10 deliverables **2** (actuator variants, protocol, pinouts) and
**5** (compute and sensor selection).

## 1. Actuators (deliverable 2)

### 1.1 GIM6010-8 — shoulder

**There is no separate 48 V model number.** One platform, characterised in a
24 V and a 48 V column. At **24 V**:

| Parameter | Value |
|---|---|
| Rated / stall torque | 5 N·m / 11 N·m |
| Rated / stall current | 10.5 A / 23.4 A (one manual says 25 A) |
| **Kt (output-referred)** | **0.47 N·m/A** (5 ÷ 10.5) |
| Speed | 120 rpm nominal, 420 rpm max output |
| Phase R / L | 0.42 Ω / 0.34 mH **[UNVERIFIED]** |
| Poles | 14 pole pairs |
| Gearbox | 8:1 planetary, steel, 15 arcmin backlash |
| Rated power | 252 W |
| Encoder | 16-bit, **mono-turn** (MT6816 or MA732) |
| Dimensions | Ø80 × **40 mm** — brief says 44 mm. **[CONFLICT]** |
| Mass | 388 g bare (brief assumes ~500 g with mounting) |
| Bus voltage | 12–56 V / 15–60 V / 12–72 V depending on source. **[UNVERIFIED]** |

**Jump check:** 5.9 N·m ÷ 0.47 = **12.6 A = 54% of peak.** Comfortable on
paper. See §1.4 for why "on paper" is doing work in that sentence.

### 1.2 GIM4305-10 — wheel

| Parameter | Value |
|---|---|
| Driver | **SDC101** |
| Rated / stall torque | 1 N·m / 3.47 N·m |
| Rated / stall current | 2 A / 5.6 A |
| Kt | 0.62 N·m/A |
| Phase R / L | 1.15 Ω / 0.41 mH |
| Speed | 300 rpm nominal (366 max) |
| Gearbox | 10:1 |
| Encoder | 14-bit, **separate-encoder support: YES** |
| Dimensions | Ø53 × **26 mm** — brief says 33 mm. **[CONFLICT]** |
| Mass | ~150 g with driver (brief assumes ~250 g) |
| Bus voltage | 12–36 V (installation guide) / 12–48 V (marketing) / 12–24 V (resellers). **[UNVERIFIED — this is the #1 blocker]** |

At 300 rpm output on a Ø110 wheel: **1.73 m/s** top speed. 1 N·m on a 55 mm
radius is **18.2 N** of tractive force per wheel — 1.1 g of horizontal
acceleration for the pair. Adequate for balance authority.

### 1.3 Protocols — the two actuators do not speak the same language

**GIM6010-8: an ODrive CANSimple derivative.** `CAN_ID = (node_id << 5) |
cmd_id`, 11-bit IDs, node 0–63, default node 0. **Default 500 kbps, max
1 Mbps. CAN 2.0 only — the manual states it "does not currently support FDCan
mode."** Recovered command set:

| ID | Command | ID | Command |
|---|---|---|---|
| 0x001 | Heartbeat | 0x012 | Get_Bus_Voltage_Current |
| 0x002 | Estop | 0x013 | Get_Iq |
| 0x003 | Get_Error | 0x014 | Set_Flexibility |
| 0x004/5 | RxSdo / TxSdo | 0x015 | Get_Rotor_Position |
| 0x006 | Set_Axis_Node_ID | 0x016 | Set_Axis_Request_State |
| 0x007 | Set_Axis_State | 0x017 | Get_Motor_Bus_Current |
| **0x008** | **Mit_Control** | 0x018 | Clear_Errors |
| 0x009 | Get_Encoder_Estimates | 0x019 | Set_Linear_Count |
| 0x00A | Get_Encoder_Count | 0x01A | Set_Pos_Gain |
| 0x00B | Set_Controller_Mode | 0x01B | Set_Vel_Gains |
| 0x00C/D/**E** | Set_Input_Pos / _Vel / **_Torque** (f32 N·m) | 0x01C/D | Get_Torques / Get_Powers |
| 0x00F–0x011 | limits | 0x01E/F | Disable_Can / Save_Configuration |

The 0x008 MIT frame uses the standard Mini-Cheetah packing (16-bit position,
12-bit velocity/Kp/Kd/torque; `kp_int = kp·4095/500`, `kd_int = kd·4095/5`),
but **the position/velocity/torque scaling ranges were not recovered** — you
cannot write a correct packer without them. Use 0x00E (`Set_Input_Torque`,
plain float) until they are confirmed.

**GIM4305-10 / SDC101: not ODrive.** CAN, RS485 and RS232; a Windows tool
switches between a proprietary **"SteadyWin"** mode (with its own CAN MASTER ID
concept, unrelated to ODrive addressing) and **"MIT"** mode. No CANSimple. The
command table and the 4-pin connector pinout are **not published**.

This protocol split is the first of two independent reasons for three CAN
buses. The second is bandwidth.

### 1.4 The red flag on rated torque

A published bench test on a 200 mm arm measured the GIM6010-8 at **~4.8 N·m
with an ODrive Micro** and **~9.4 N·m with a Tinymovr R5.3**, against an
11 N·m rating; an earlier test got 3 N·m. **Rated stall is only reachable with
a controller that will actually push 23–25 A.** The 5.9 N·m jump requirement
sits above the low measurement and below the high one.

**Action: measure torque on a lever arm before trusting the jump budget.**
This is on the bring-up plan as a gate, not a nice-to-have.

## 2. CAN bandwidth — why one bus does not work

Classical CAN, 11-bit ID, 8 data bytes = 108 bits before stuffing. The stuff
region is 98 bits, so worst case adds 24 stuff bits:

```
worst case  132 bits + 3 IFS  →  135 µs @ 1 Mbit
typical                       →  ~117 µs
```

At 1 kHz with 4 actuator nodes you need command + reply each = **8 frames/ms**:

| Configuration | Load |
|---|---|
| 1 bus, 1 Mbit classical, 11-bit IDs | **94% typical / 108% worst — fails** |
| 1 bus, 29-bit IDs | 160 µs/frame → **128% — hopeless** |
| CAN-FD 1M/5M | 39% — but **neither Steadywin part supports FD** |
| 2 buses split L/R | 47% / 54% |
| **3 buses (A = shoulders, B = left leg, C = right leg)** | **47% / 35% / 35%** |

Buses B and C carry three frames per millisecond each — wheel command, wheel
reply, satellite knee report — because the satellite is unidirectional and
needs no command frame.

Populate three TCAN3414 transceivers (3.3 V single supply, 8 Mbps, SOT-23-8).
**Do not use SN65HVD230** — it is 1 Mbps classic-only and is commonly
mis-specified into designs like this one.

## 3. Main controller

**Custom 84 × 60 × 1.0 mm 4-layer board around an STM32G474RET6.**

Why: 170 MHz Cortex-M4F, **3 × FDCAN** (exactly the three buses), LQFP64 at
10 × 10 × 1.4 mm, plentiful timers and SPI. The board fills the centre slot
(84 × 60 × 8 mm) and nothing off the shelf both fits and has three CAN
controllers.

**The 8 mm slot is a component-HEIGHT problem, not an area problem.** 84 × 60
is 50 cm², generous. But 8 mm total across *both* sides rules out electrolytics,
standard 4–6 mm inductors, 2.54 mm headers (8.5 mm), XT30/XT60, and the
Adafruit Feather M4 CAN (7.2 mm on its own).

Height plan: **top side ≤3.5 mm** (Coilcraft XGL4020 inductors at 2.1 mm,
ceramic and polymer caps only), **bottom side ≤2.5 mm**, **side-entry JST SH**
throughout.

**Mandatory: an onboard microSD socket.** The robot fails in 200 ms events and
cannot be debugged by watching it. The firmware logs ~60 channels at 1 kHz
(~240 kB/s) to a preallocated contiguous file; see `06_logging_and_bringup.md`.
Use a **push-pull micro-SD socket, 1.2–1.4 mm tall, bottom-side**, and budget
four SDIO lines plus a card-detect. This is not optional instrumentation — it
is the difference between tuning the robot and guessing at it.

Effort: 2–3 days schematic, 3–5 days layout, 1.5–3 weeks fab. $150–350 for
five assembled. **Budget 4–6 weeks and plan for a rev B.**

**Single-leg rig: use a Teensy 4.1, not the custom board.**

The rig needs only two CAN buses (one per actuator), the Teensy has three CAN
controllers and an onboard microSD socket, and it is in hand today. No PCB lead
time, no PCB revision, no 8 mm slot constraint (the rig has no chassis). Wire
two TCAN3414 breakouts on a breadboard at **500 kbps** (breadboard impedance
cannot hold 1 Mbps stubs). The knee encoder AS5048A runs SPI directly to the
Teensy — no satellite node needed for a single leg. See
`fusion_brief_single_leg_rig.md` §5.

**Fallbacks for the two-leg robot, in order:**

1. **WeAct STM32G431CBU6 / G474CEU6 core board**, 36.28 × 28.14 mm, in the
   36 × 28 × 72 top-forward box — but 36.28 vs 36.0 mm needs an interference
   check, and it displaces the battery.
2. **Teensy 4.1** — 3 CAN controllers, needs a milled relief for the bottom
   microSD socket.

**Rejected:** RP2350 (can2040 soft-CAN has no bus-off state, no error frames,
and loses messages under contention), ESP32-S3 (TWAI is classic-only and has
known errata), RoboMaster Type-C (16 mm, 38 g), Portenta, pi3hat (doesn't fit).

**No Linux SBC in prototype 1.** A Pi Zero 2 W is 12 g and 0.4–3.0 W into an
insulating chassis — it puts you over the 120 g budget and quadruples the
thermal load. Worse, a published micro-ROS serial integration measured
**28.7 ms mean round-trip**, roughly 15× the entire delay budget. Add it at
P2 over a 3 Mbaud DMA UART, as a planner, never in the balance loop.

## 4. IMU

**TDK InvenSense ICM-42688-P.**

| | ICM-42688-P | BMI088 | BNO085 | ADIS16505 |
|---|---|---|---|---|
| Gyro noise | **2.8 mdps/√Hz** | 14 | — | best |
| Height | **0.91 mm** | 0.95 | 1.4 | **5 mm** |
| Anti-alias filter | **on-chip, 42–3979 Hz programmable** | fixed | — | yes |
| Latency | SPI raw, negligible | raw | **6.6 ms fused** | low |
| Price / lead | ~$8, stocked | **26–40 wk lead (2026)** | ~$20 | **$598–860** |

**Configuration: 8 kHz ODR, AAF set to 250–500 Hz, decimate in firmware to
1 kHz.** The decimation is a second digital anti-alias stage and buys √8 of
noise reduction for free.

**Never use on-chip sensor fusion.** The BNO085's fused output runs at ~100 Hz
with 6.6 ms latency — at the robot's ω_c ≈ 100 rad/s that is **38° of phase
lag**, which is the entire stability margin and then some.

### 4.1 Aliasing is the dominant IMU risk

Structural vibration above Nyquist folds down as **fake slow tilt rate**, and
no downstream filter can remove it once it is in the samples. Mitigate in this
order:

1. **Stiffen the mount.** Free.
2. **Consider isolation, carefully.** A 25 Hz gel mount puts new dynamics
   *inside* the 8–16 Hz control band. A stiffer 100–200 Hz mount is usually the
   better answer on a machine this small.
3. **Configure the AAF.**
4. **Add a measured notch** — only after you have a spectrum from the real
   robot.

### 4.2 The datum pad is in the worst possible place

The brief's IMU datum pad (§4.2) is 12 × 12 mm at X = −52.0, Z = 40.0…41.5,
centred on Y = 0 — **58.5 mm aft and 90.8 mm above the CoM**, which puts it
**195 mm above the wheel axis.** The lever-arm error scales with that height,
and 195 mm is the largest value available anywhere on the robot.

The gyro needs no correction (ω is identical everywhere on a rigid body). The
accelerometer does:

```
a_ref,x = a_imu,x − θ̈·r_z + θ̇²·r_x
a_ref,z = a_imu,z + θ̈·r_x + θ̇²·r_z
```

With r_z = 0.195 m referred to the wheel axis, at an achievable pitch
acceleration of 20 rad/s² (τ/J = 1.2/0.0606) the tangential term is
**3.9 m/s² — 22° of apparent tilt.** The pitch-bias budget is 0.1°. This is
not a correction, it is the dominant error term.

**Recommendation: move the IMU to wheel-axis height** so r_z → 0 and the term
vanishes. This is a mechanical change (CR-9 in `05_open_questions.md`) and it
is cheap now. It also places the IMU near the rolling contact, so its
acceleration is directly comparable to wheel odometry.

If the pad cannot move, **compute θ̈ from the model** — `θ̈ = 124.96·θ −
102.80·τ`, using quantities the controller already has, with no lag and no
differentiation. Differentiating the gyro is the worst of the three options.

Two further notes:

- The lever arm is **not constant.** The IMU is on `base_link` but the CoM
  moves with shoulder angle and knee flexion. Recompute **r** from forward
  kinematics each cycle, or reference everything to the shoulder axis (fixed in
  `base_link`) and carry a constant offset.
- Implement the compensation **inside the observer**, driven by the estimator's
  smooth ω̂/α̂, not as a post-correction on raw samples.

## 5. Knee sensing — and a coupling nobody has budgeted for

**AS5048A, read at ≥2 kHz** from the satellite. The landing impact transient
is ~20 ms; 100 Hz is useless and 1 kHz is marginal. Note the AS5048A's
**~90.7 µs typical / 110.2 µs maximum propagation delay** — about 9% of a 1 ms
tick of pure irreducible latency. **Read encoders at the top of the tick.**

The knee sensor is not only a sensor. Because τ_knee(φ) is known analytically
(brief §8.2), deflection gives knee torque gives leg axial force gives ground
reaction force. **The AS5048A is a load cell at zero added mass** — 14 bits
over 360° is 0.022°/LSB, or **0.025 N per leg**, 0.16% of body weight.

**But there is a preload floor.** The 30 N spring preload means a free leg
rests against the −8° stop reading **8.25 N**, and 1 g static stance sits at
only φ = −0.835°. Everything below ~0.52 g is indistinguishable — all of it is
at the stop. **Contact detection must therefore threshold on φ, not on
estimated force.** Also subtract shank inertia during fast swings: the shank is
409 g, so at 20 m/s² it contributes 8.2 N, which is larger than the entire
usable force span.

### 5.1 New finding: the contact patch translates aft under compression

Forward kinematics (A = 50°, L1 = L2 = 120 mm) gives the wheel contact X as a
function of knee flexion φ:

| φ | contact X | CoM ahead of contact | pitch torque |
|---|---:|---:|---:|
| 0° | 0.00 mm | 6.47 mm | 0.21 N·m (0.10/wheel) |
| +10° | −12.00 mm | 18.46 mm | 0.60 N·m (0.30/wheel) |
| +20° | −20.84 mm | 27.30 mm | 0.88 N·m (0.44/wheel) |
| +25° | −23.99 mm | 30.45 mm | 0.98 N·m (0.49/wheel) |
| +27° | −25.00 mm | 31.46 mm | 1.02 N·m (0.51/wheel) |

The 0.21 N·m standing bias documented in the design record is the **φ = 0 case
only.** Under compression it grows ~5× to 1.02 N·m nose-down, and it **arrives
as a step exactly at touchdown**, which is the worst possible moment.

**Consequence: the balance controller needs φ as a feedforward input, not
merely as a contact-detection flag.** This is carried into `04_firmware.md`.

## 6. Current sensing and thermal

**INA228** (0–85 V, 20-bit, ±163.84 mV / ±40.96 mV shunt FS, with energy,
charge and on-die temperature registers) on a **2 mΩ 2 W 2512 shunt** — 80 mV
and 3.2 W at 40 A, but only in ~20 ms bursts. Add an **independent resistor
divider into an MCU ADC** for overvoltage detection, so the safety path does
not depend on an I²C transaction completing.

**Thermal: PA-CF is not a heat path.** ~0.5 W/m·K, roughly 400× worse than
aluminium. There is no metal, no heatsink and no airflow. Rule of thumb:
~15.3 cm²/W of two-sided copper for a 40 °C rise in free air; sealed inside
plastic, **budget 1.0–1.2 W for a 40 °C rise, 0.5 W for a comfortable 20 °C.**

| Build | Slot dissipation | Verdict |
|---|---:|---|
| MCU only | ~0.15 W | Fine |
| MCU + loaded Pi Zero 2 W | ~0.65 W | Acceptable, marginal |
| Power stage at 3 A in the slot | 1.5–2.0 W | **Not acceptable** |

**Highest-value thermal change: move the power stage out of the 8 mm slot into
the 36 × 28 × 72 box and feed 5 V into the slot.** Derate every part for a
50 °C internal ambient.
