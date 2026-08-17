# 01 — Power, Battery and Safety

Covers brief §10 deliverables **1** (battery specification), **6** (power
budget) and **7** (safety design).

## 1. Power budget

Nothing here is measured. Every figure is an estimate built from the mechanics
in the brief and vendor constants; **the first bench run must put an inline
watt meter on the pack** and replace this table.

### 1.1 Peak — the jump

The brief (§8.4) gives a 3 g jump at **5.9 N·m per shoulder**. The GIM6010-8
constant is **Kt = 0.47 N·m/A output-referred** (5 N·m ÷ 10.5 A), so:

```
I_phase = 5.9 / 0.47 = 12.6 A   (peak/stall rating is 23.4 A → 54% of peak)
```

**The actuators are not the limit for the jump.** The thrust is a 30–50°
shoulder sweep in 60–80 ms, i.e. **6.5–14.5 rad/s at the output** — not the
~31 rad/s an earlier draft of this file assumed. Mechanical power is therefore
much lower than first estimated, and **copper loss dominates**:

| Term | W | Confidence |
|---|---:|---|
| Shoulder mechanical (2 × 8 N·m at ~12 rad/s output) | 190 | good |
| **Copper loss (2 × 17² × 0.42 Ω)** | **240** | **poor — phase R is [UNVERIFIED]** |
| Wheel actuators (spin-up during thrust, 77–99 mm of roll) | 60 | fair |
| Logic, sensors, satellites | 15 | good |
| **Peak bus power** | **≈505** | ±40% |

If phase R is really 0.15 Ω (the earlier assumption) rather than 0.42 Ω, the
copper term collapses to 87 W and peak bus power is **~350 W**. **Measuring
phase resistance is therefore worth more to this budget than any other single
measurement** — it is the difference between a 16 A and a 23 A design point.

Sizing against the pessimistic 505 W at 22.2 V gives **23 A**, and at
end-of-charge sag conditions call it **28 A**. Keeping headroom for the
unverified terms, design targets:

- **35 A for 200 ms** — conductors, connectors, shunt, FET.
- **6 A continuous** — thermal sizing.
- **50 A fault trip** — fuse and eFuse threshold.

### 1.2 Continuous

| Mode | Estimate | Notes |
|---|---:|---|
| Standing (balancing in place) | ~33 W | Continuous small corrections plus 0.21–1.02 N·m of standing pitch bias — see `03_compute_and_can.md` §5 |
| Driving | ~60 W | Rolling plus balance authority |
| Mixed development use | ~45 W | The number to size runtime against |
| Logic only (MCU, IMU, 2 satellites, 3 transceivers) | ~2.5 W | |

**A jump costs almost no energy — about 64 J (0.018 Wh) — but 23–28 A.**
This is the single most important fact about the power system: **the pack is
sized by power, not by energy.** It is why a small high-C LiPo beats a larger,
heavier Li-ion pack here, and it decides the chemistry outright.

## 2. Battery specification

### 2.1 The chosen pack

| Parameter | Value |
|---|---|
| Part | **GNB 6S 550 mAh "long type", GNB5506S100AHV** |
| Chemistry | LiHV LiPo — **charge to 4.20 V/cell, NOT 4.35 V** |
| Configuration | 6S1P, 22.2 V nominal / **25.2 V full** / 18.0 V empty |
| Capacity | 550 mAh, **12.2 Wh** |
| Dimensions | **36 × 18 × 71 mm** |
| Mass | **82 g** (vs a 250 g budget) |
| Density | 272 Wh/L, 152 Wh/kg |
| Connector | XT30 |
| Location | Top-forward free box, 36 (X) × 28 (Z) × 72 (Y) |

Fit: 36 × 18 × 71 into 36 × 28 × 72 leaves **10 mm of Z spare** and ~1 mm in
the other two axes. Site it centred on Y = 0 — CoM Y must stay at zero.

At a 28 A peak the pack sees **~51 C**. The 100 C rating covers it, but only
just, and only in 200 ms bursts. This is the strongest argument for 2P below.

### 2.2 Why not the alternatives

- **The BOM's 4S 2200 LiPo** — 105 × 34 × 30 mm. 105 mm fits nowhere in the
  chassis, and 14.8 V is too low for a 24 V-class actuator.
- **18650 cylindrical (6 × Molicel P26A)** — 275 g bare, ~305 g assembled,
  against a 250 g budget; and the 28 mm Z limit takes exactly one cell in the
  top-forward box.
- **21700 (6 × P45B)** — 460 g. Not close.
- **A larger Li-ion pack** — more Wh/kg but far worse C-rate. The robot needs
  amps, not watt-hours.

### 2.3 Runtime (80% DoD, 9.8 Wh usable)

| Mode | Runtime |
|---|---:|
| Standing (33 W) | ~18 min |
| Driving (60 W) | ~10 min |
| Mixed (45 W) | ~13 min |

**This is a bench runtime, not a demo runtime.** See the 6S2P change request
in `05_open_questions.md` — opening chassis Z from 28 to 40 mm gives 2 packs,
164 g, 24.4 Wh, ~26 min mixed, and halves C-rate stress from ~56 C to ~28 C.

## 3. Bus voltage and the wheel-driver problem

6S at full charge is 25.2 V. The GIM4305-10's SDC101 driver is documented as
12–24 V in some places and 12–36 V in others. **The hazard is not the charge
voltage, it is regen.** On landing the wheels back-drive; at 25.2 V into a
24 V-max driver there is *negative* headroom before regen even starts.

Three ways to run this:

| Option | Verdict |
|---|---|
| **A.** Get Steadywin to confirm 36 V for the driver rev in hand | Best, but blocked on a supplier answer |
| **B.** Undercharge to 3.95 V/cell (23.7 V full) | Loses 22% of capacity on a pack that is already short |
| **C. 6S bus for the shoulders + a ~20 V / 100 W buck for both wheel drivers** | **Chosen.** ~15 g, deleted if (A) lands |
| **D.** Drop to 5S (21.0 V full, 3.0 V / 14% regen headroom) | Fallback if the buck proves troublesome; costs jump headroom |

Option C also isolates the wheel drivers from pack transients, which is
worth something independently.

## 4. Power tree

```
6S pack ──[XT30 loop key]──[30A slow blade fuse]──[LM74700 ideal diode + 75V N-FET]──┐
                                                                                      │
                                        ┌──── shoulder L GIM6010-8  (22.2 V direct) ──┤
                                        ├──── shoulder R GIM6010-8  (22.2 V direct) ──┤
                                        ├──[20 V / 100 W buck]──┬── wheel L ──────────┤
                                        │                       └── wheel R ──────────┤
                                        └──[LMR33630 → 5 V 3 A]─┬── satellites (via clock spring)
                                                                └──[buck 3.6 V]──[LDO 3.3 V]── MCU / IMU / AS5048A
```

**Component choices and why:**

- **LMR33630ADDAR** for 24 V → 5 V. 36 V input rating gives real margin over
  25.2 V plus regen overshoot; synchronous, >95%, ~1.0 mm tall. TPS62933's
  30 V is uncomfortably close to a regen spike. **TPS54331 is
  non-synchronous — reject.**
- **5 V → 3.6 V buck → 3.3 V LDO** for the IMU and AS5048A analog rail. The
  LDO drops only 0.3 V so it cleans the rail without meaningful heat.
- **Reverse polarity: LM74700-Q1 ideal-diode controller + 75 V N-FET**, with
  **SMBJ58A / SMBJ26A back-to-back** TVS. TI states a single bidirectional TVS
  is unsuitable for 24 V battery protection. For the high-current motor branch,
  rely on the keyed XT30/XT60 rather than adding series silicon.
- **Bulk capacitance: ~200 µF ceramic/polymer**, for ripple and di/dt only.

### 4.1 Bulk caps cannot absorb landing regen — a useful negative result

```
E = ½·C·(V₂² − V₁²) = ½·C·(26.5² − 25.2²) = 33.6·C   [J, C in farads]
470 µF stores 0.016 J.  Absorbing the 3 J of landing energy needs ~89,000 µF.
```

**The battery absorbs regen. Capacitors do not, and no realistic bank will.**
Anyone proposing "just add more bulk" should be shown this line.

## 5. Inrush and precharge

Four drivers with ~600–900 µF **[UNVERIFIED]** of DC-link capacitance across
~60 mΩ of wiring gives a theoretical **~400 A instantaneous** at connection.
That welds XT30 contacts.

**P-channel MOSFET soft-start (~2 g)** with a 10 Ω gate-side precharge:
initial current 2.5 A, τ = 8 ms, settled in 5τ = 40 ms, total dissipation
0.25 J — a 10 Ω 1 W part is sufficient. Chosen over XT90-S anti-spark (12 g)
and a relay bypass (8 g).

## 6. BMS and cell monitoring

**TI BQ76952.** I²C at 400 kHz, 3S–16S, per-cell differential measurement to
±10 mV, integrated balancing, coulomb counter, current sense, 9 thermistor
inputs, ~$4, no significant height.

**Rejected:**

- **Daly / JBD smart BMS** — a JBD 6S 40 A board is 130 × 65 × 10 mm. It fits
  none of the three free boxes.
- **Series discharge FETs** — mass, Rds(on) in the highest-current path in the
  robot, and a failure mode where the BMS trips mid-jump and drops the machine.
  **Monitor and warn; do not interrupt.**
- **A resistor-divider ladder** — cumulative balance taps give **±330 mV
  worst-case error on a cell** (8%) with 1% resistors. Useless for LiPo.

### 6.1 Low-voltage cutoff must be load-compensated

At 30 A with ~50 mΩ pack ESR the terminal voltage sags **1.5 V**. A naive
per-cell LVC false-trips on every single jump. Estimate open-circuit voltage:

```
V_OCV ≈ V_measured + I × R_est
```

with R_est learned at startup from a known step load. Trip on OCV, not terminal.

## 7. Safety design (deliverable 7)

Layered, with the outermost layer purely mechanical.

| Layer | Mechanism | Trips on |
|---|---|---|
| 1. Human | **XT30 loop key** in the pack lead | Manual pull. The only guaranteed disconnect. |
| 2. Fuse | 30 A **slow-blow** blade | Hard short. Slow, because a jump legitimately draws 31 A. Not a polyfuse — too slow to reset, too resistive. |
| 3. eFuse | P-FET soft-start doubling as an electronic disconnect | >50 A, or firmware command |
| 4. Soft e-stop | Momentary button, **fail-safe: the button CLOSES the circuit that holds the FET on** | Press, or wire break |
| 5. Watchdog | **Windowed** WDT (TI TPS3851 / STWD100 / MAX16998) | Too-fast *or* too-slow kicks. TPS3823 and MAX6369 are simple timeout parts — a runaway 50 kHz ISR keeps feeding them. |
| 6. CAN watchdog | Per-driver, independent of the main MCU | Setpoints absent >50 ms |
| 7. LVC | BQ76952 + load compensation (§6.1) | OCV per cell below threshold |

Wire the WDT reset line to **both** the MCU reset **and** the actuator power
gate. Kick the internal IWDG from the 1 kHz control ISR only — never from a
background task, or the watchdog stops testing the thing that matters.

### 7.1 CAN loss mid-jump — a two-stage timeout

Neither obvious answer is right. Holding stiff means landing on a rigid strut;
zeroing torque immediately means the legs collapse in flight.

```
t > ~20–50 ms   →  low-stiffness position hold toward a landing-ready pose,
                   generous damping
t > ~500 ms     →  zero torque, latch fault
```

A jumping robot that loses comms mid-extension is a projectile. This behaviour
must live **in each driver**, not in the main MCU that just went silent.

### 7.2 Regen handling on landing

Landing dumps up to ~3 J back through the wheels and shoulders. The pack
absorbs it (§4.1) — **except** in three cases, which is why a brake chopper is
still required:

1. Pack at full charge and unable to accept current.
2. BMS or connector opens mid-flight.
3. Contact bounce on landing.

**Hysteretic shunt regulator:**

| Parameter | Value |
|---|---|
| Turn-on | 26.5 V |
| Turn-off | 25.6 V |
| Hysteresis | ~0.9 V, via 1 MΩ positive feedback — **mandatory**, or the FET runs linear and cooks |
| R_brake | 5 Ω (5.3 A, 140 W instantaneous, burst-rated) |
| Comparator | TLV3011 + logic-level N-FET |

Add a firmware duty limiter: latch an e-stop if the shunt has been active more
than 200 ms cumulative. **Do not put the brake resistor in the 8 mm centre
slot** — see the thermal note in `03_compute_and_can.md`.

Free mitigation for case 1: **test-jump at ≤4.1 V/cell**, never straight off
the charger.

### 7.3 Standing rule

**Never disconnect the pack while the motors can be back-driven.** With no
sink the bus runs away and kills the drivers. Loop key out only when the robot
is on its stand and stationary.
