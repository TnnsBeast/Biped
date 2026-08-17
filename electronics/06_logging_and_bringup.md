# 06 — Logging, Telemetry and Bring-Up

Covers brief §10 deliverable **9** (bring-up plan), plus the instrumentation
that has to exist before Stage 3.

## 1. Why logging comes first

This robot fails in **20–200 ms events**: a landing impact is ~20 ms, a thrust
is 60–80 ms, a fall from vertical is ~300 ms. **You cannot debug any of that by
watching it, and you cannot debug it over a 50 Hz telemetry link either.**
Every hour spent on the logging pipeline before the first powered test saves a
day of guessing later.

Three tiers, all built in Stage 1:

| Tier | Path | Rate | Use |
|---|---|---|---|
| **1. Onboard binary** | microSD, FatFs | **1 kHz, all channels** | Post-mortem. The only tier that survives a fall. |
| **2. Live plot** | UDP → PlotJuggler | 100–200 Hz, ~20 channels | Tuning while tethered |
| **3. Post-processing** | MCAP → Foxglove | offline | Synchronised replay, jump-by-jump comparison |

### 1.1 Onboard binary logger

~60 channels × 4 bytes at 1 kHz = **~240 kB/s**, ~14 MB per minute. A class-10
card does this comfortably; the failure mode is not throughput, it is **write
latency spikes** when the card does internal wear levelling.

Rules that make it work:

- **Preallocate with `f_expand()`** so the file is contiguous — this removes
  FAT-chain updates from the write path, and it is the single biggest win.
- **Lock-free SPSC ring buffer** filled by the 200 Hz logger task, drained in
  **4 kB blocks** by a low-priority writer task. Never write from the ISR.
- **Never block the control ISR on the card.** If the ring overflows, drop
  frames and increment a counter — a dropped log line is survivable, a missed
  control tick is not.
- **Fixed-width binary frames with a magic word and a sequence number**, not
  CSV. CSV formatting costs more CPU than the write.
- **Flush and close on fault latch**, and on the e-stop path. A log that ends
  10 ms before the interesting event is worthless.

Channel set: `t_us`, θ, θ̇, θ̂, gyro/accel raw ×6, φ_L/φ_R and rates,
θ_s_L/θ_s_R and rates, wheel positions/velocities, all four commanded and
measured torques, bus V and I, per-cell V, FSM state, fault word, CAN error
counters per bus, ISR execution time, loop-latency timestamp pair.

### 1.2 Live telemetry

PlotJuggler over UDP with a plain JSON or protobuf payload, 100–200 Hz,
decimated and **droppable** — the transmit task is the lowest priority in the
system and must never apply backpressure to anything.

### 1.3 Post-processing

Write an MCAP converter for the binary format once, early. Foxglove then gives
you synchronised multi-channel replay and lets you overlay two jumps. Budget
half a day; it pays for itself on the first tuning session.

## 2. Bring-up plan

**No stage starts until the previous stage's gate is green.** Every stage runs
on the stand until Stage 4.

Build the stand first: a rigid frame that holds the shoulder axis with wheels
clear of the ground, plus a **pitch-only gimbal** mode where the robot can
rotate freely in pitch but cannot fall over or travel. Most of Stage 3 lives on
that gimbal.

### Stage 0 — Bench, no motors

| | |
|---|---|
| **Do** | Power the main board from a **current-limited bench supply at 0.5 A**, never the pack. Bring up SWD, clocks, the three FDCAN peripherals in loopback, IMU SPI, SD card, telemetry. **Single-leg rig: use the Teensy 4.1 — bring up two CAN buses (500 kbps), IMU SPI, and the onboard microSD.** |
| **Gate** | All three CAN peripherals pass loopback. SD writes 240 kB/s sustained for 10 minutes with zero dropped frames. IMU streams at 8 kHz. |
| **Trap** | If SD throughput is marginal here it will be catastrophic under load. Fix it now. |

### Stage 1 — Estimator, no motors

| | |
|---|---|
| **Do** | Run the full 2-state KF. Hand-rotate the robot against a printed protractor. Verify the accelerometer-tilt correction (`04_firmware.md` §5.1) by shaking the chassis horizontally — a naive estimator shows tilt, a correct one does not. |
| **Gate** | **Static pitch bias <0.1°, noise <0.05° RMS, no drift over 10 minutes.** Gyro bias converges within 10 s of boot. |
| **Trap** | Do not proceed with a "good enough" estimator. A 1° bias is 0.92 m/s² of commanded acceleration — you will chase it as a control bug for a week. |

### Stage 2 — One actuator, free shaft, and the latency measurement

| | |
|---|---|
| **Do** | One GIM6010-8 on the bench, output free. Encoder calibration and save. Torque mode only. Sweep 0.1 → 5 N·m against a lever arm and a kitchen scale — this is the §1.4 torque check from `03_compute_and_can.md`. Measure phase R with a milliohm meter (C7). **Measure end-to-end loop latency**: toggle a GPIO at IMU-sample-complete and at torque-written-to-mailbox, scope both. |
| **Gate** | Measured torque within 20% of `Kt × I`. **End-to-end latency <8 ms.** No CAN errors in a 1-hour soak at 1 kHz. |
| **Trap** | Nothing downstream matters if latency fails. Published bench tests found 4.8–9.4 N·m against an 11 N·m rating; if you measure below 5.9 N·m, the jump spec changes here, not after the PCB order. |

### Stage 3 — Balance on the gimbal

| | |
|---|---|
| **Do** | Full four-actuator bus, robot on the pitch gimbal. Start with the **very-soft** gains `[−0.500, −1.422, −7.592, −0.855]` (20 ms margin), then the soft set. Add the ∫θ state. Verify the wheel-odometry shank term with the chock test (`04_firmware.md` §5.2). |
| **Gate** | Holds pitch within ±2° against a hand push, recovers in <1 s, **no growing 3–4 Hz oscillation**, no CAN faults. Latency still <8 ms with all four nodes live. |
| **Trap** | **This is where the 3.67 Hz bounce mode shows up.** If pitch oscillation grows as you raise K_θ, that is the mode, not a gain problem. Turn on shoulder damping injection (`c_φ ≈ 0.19 N·m·s/rad`) and bias the stance to θ_s ≈ ±12° so the shoulders have authority. |

### Stage 4 — Free balancing

| | |
|---|---|
| **Do** | Off the stand, tether from above, foam mat, **helmet on the IMU end** — a fall onto the datum pad ruins the calibration. Zero velocity command first, then rate-limited velocity to 0.5 m/s. |
| **Gate** | 5 minutes standing without intervention. Drives 2 m and stops. **Peak current logged and compared against `01_power_and_battery.md` — this is where the estimated power budget gets replaced with measurements.** |
| **Trap** | Rate-limit the operator velocity command to ~0.5 Hz. The RHP zero at +6.53 rad/s means a step velocity command makes the robot go backwards first; an operator who fights that will drive it into the floor. |

### Stage 5 — Drop tests, unpowered then powered

| | |
|---|---|
| **Do** | Drop from a hoist, shoulders held at a fixed extended pose, **starting at 20 mm** and increasing in 10 mm steps. Log φ peak on every drop and plot φ_peak vs drop height. Then repeat with the landing impedance controller live. |
| **Gate** | **The brief's gate — "no powered jump until a 100 mm drop never reaches +27°" — cannot be passed passively.** Passive capacity is ~49 mm (`fusion_brief_single_leg_rig.md` §4.3). Replace it with: **(a) a 49 mm free drop never exceeds +24° passively, and (b) a 100 mm drop never exceeds +24° with the shoulder landing controller active.** |
| **Trap** | Extrapolate the φ_peak curve before each step up. If the trend line hits +24° at 40 mm, do not "just try" 50 mm. Use the measured curve to set `A_MAX` in the CBF. **Never extrapolate past the last measured point.** |

### Stage 6 — Jumping

| | |
|---|---|
| **Do** | Tethered from above, over a mat. **Scissor crouch** (L = +θ, R = −θ). Ramp thrust torque in 10% increments from a 20% baseline. Log takeoff θ̇ every attempt. |
| **Gate** | Repeatable hop with **takeoff \|θ̇\| < 1 rad/s** and a landing that recovers to BALANCE without hitting the hard stop. Then remove the tether. |
| **Trap** | Angular momentum is conserved in flight — you cannot fix a bad takeoff. If takeoff θ̇ is high, fix the crouch symmetry and the thrust ramp; do not add flight-phase gain. |

## 3. Cross-cutting rules

- **Torque mode always.** Never the drive's internal position mode past Stage 2.
- **Every stage runs with logging on.** A test you did not log is a test you did
  not run.
- **Version the log format** with a header word, and commit the parser alongside
  the firmware. A month of logs you can no longer decode is a real failure mode.
- **Re-run Stage 1's estimator gate after any fall** onto the IMU end.
- **Test-jump at ≤4.1 V/cell**, never straight off the charger — regen has
  nowhere to go at full charge (`01_power_and_battery.md` §7.2).
- Keep the **loop key** within reach at every stage from 3 onward, and keep the
  robot on a mat.

## 4. Schedule

| Stage | Elapsed | Notes |
|---|---|---|
| 0–1 | 1–2 weeks | Can start on a dev board before the PCB arrives |
| 2 | 3–5 days | Blocked on actuators in hand |
| 3 | 1–2 weeks | The bounce mode may eat a week on its own |
| 4 | 3–5 days | |
| 5 | 1 week | Slow by design — 10 mm steps |
| 6 | 2+ weeks | Open-ended |

Runs concurrently with a **4–6 week PCB lead time** (`03_compute_and_can.md`
§3), so Stages 0–1 should be done on the WeAct fallback board while the custom
board is in fab. **For the single-leg rig, use the Teensy 4.1** — no PCB lead
time, no fallback needed. Stages 0–5 map directly to
`fusion_brief_single_leg_rig.md` §6 (steps 1–11).
