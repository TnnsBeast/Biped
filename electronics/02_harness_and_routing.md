# 02 — Harness, Clock Spring and Routing

Covers brief §10 deliverables **3** (wiring diagram, CAN topology, grounding,
connector schedule) and **4** (clock-spring cable specification).

## 1. The architectural move: a satellite node per leg

The brief's §3.3 counts 7–10 conductors crossing each shoulder: wheel-motor
power (2), wheel-motor CAN (2), and the knee encoder (3 PWM / 4 I²C / 6 SPI).
That does not fit, and the encoder conductors are the worst of it — a
700 mm run of low-level signal alongside a motor's di/dt.

**Put a small CAN node on the proximal link.** It carries the AS5048A over a
40 mm SPI trace, and reports knee angle onto the same CAN pair the wheel
driver already needs. Crossing conductor count drops from 7–10 to **four**.

| | Without satellite | With satellite |
|---|---:|---:|
| Conductors across the clock spring | 7–10 | **4** |
| AS5048A SPI run length | ~700 mm | ~40 mm |
| Max reliable encoder rate | ~1 kHz (PWM mode) | **≥8 kHz SPI** |
| Added mass per leg | — | ~2–3 g |
| Added cost per leg | — | ~$4–8 |

**Satellite BOM (per leg):** STM32G0B1CBT6 (Cortex-M0+ 64 MHz, 2× FDCAN,
UFQFPN32 5 × 5 mm) · TCAN332G or TCAN1051 transceiver · 20 V → 3.3 V buck ·
AS5048A on the existing 14 × 14 mm PCB.

**Check first:** if the wheel driver board or the GIM4305-10's second-encoder
header can absorb the AS5048A directly, the satellite MCU disappears and the
conductor count is unchanged. The GIM4305-10 is documented as supporting a
separate encoder; the GIM6010-8 is documented as *not*. See
`05_open_questions.md`.

**Rejected alternatives:**

- **Slip rings.** Thinnest pancakes are 5.4–6.0 mm against a 4.0 mm cavity;
  capsule types need a through-bore the GIM6010-8 does not have (its output is
  solid — design record §2). Decisive objection: **±185° oscillatory duty
  causes fretting corrosion at the reversal points.** "10 M revolution" ratings
  assume continuous unidirectional rotation and do not transfer.
- **AS5048A in PWM mode.** The PWM output updates at only **1 kHz** — you
  cannot close a 1 kHz loop on it, and pulse-width edges are the single most
  noise-vulnerable signal you could choose for a 700 mm motor-adjacent run.
- **10BASE-T1S** — still needs two signal conductors, so it saves nothing.
- **Power-line comms (Yamar SIG60)** — 115.2 kbit/s and unproven next to a
  100 W inverter.

## 2. Clock-spring cable specification (deliverable 4)

### 2.1 The cavity constraint was read the wrong way round

The brief treats the 4.0 mm axial cavity height as a bend-thickness limit and
reasons toward FFC. In a spiral wrap the **curvature points radially**, so
bending strain is governed by *radial* thickness — of which there is 11.5 mm
(r = 20.5 → 32). The 4.0 mm axial dimension is the ribbon **width**, and after
PTFE slip sheets ~**3.4 mm** is usable. A 20-way 1.0 mm-pitch FFC is over
20 mm wide. FFC is out; a narrow round-conductor bundle is in.

### 2.2 Length — the design record's margin is wrong

Design record §4.3 claims ~430–470° of capacity from 400 mm of cable, i.e.
20–27% margin over the 370° requirement. Recomputing from the annulus:

```
Δθ = L·(r_o − r_i) / (2π·r_i·r_o)
   = 400 × 11 / (2π × 20.5 × 31.5)
   = 1.084 turns = 390°
```

That is **20° / 5.4% margin, not 27%.** Required length for exactly 370° is
**369 mm**, so 400 mm has almost nothing in hand once you subtract termination
and strain relief at both ends.

**Specify 470–500 mm of free spiral** (BOM currently says ≥400 mm — change
request in `05_open_questions.md`).

### 2.3 Radial fit check at 500 mm

With a 2.2 mm radial bundle thickness, cross-sectional area L·t = 1100 mm²:

```
fully wound IN :  π(r² − 20.5²) = 1100  →  r = 27.8 mm   < 32.0  ✓ (4.2 mm clear)
fully wound OUT:  π(32.0² − r²) = 1100  →  r = 26.0 mm   > 20.5  ✓ (5.5 mm clear)
```

Both ends clear. 500 mm is the recommended value.

### 2.4 Cable specification

| Parameter | Value |
|---|---|
| Conductors | **4** — V+ (20 V), V−, CAN_H, CAN_L |
| Power cores | 2 × **22 AWG** high-flex silicone, ~1.35 mm OD |
| Signal cores | 2 × **26 AWG** twisted pair, ~0.90 mm OD, foil screened |
| Lay-up | **2 wide × 2 deep**, flat-oval jacket ≈ **3.0 (W) × 2.2 (T) mm** |
| Jacket | Silicone, high-flex, extra-fine strand (≥0.05 mm filaments) |
| Free spiral length | **500 mm** (was ≥400) |
| Flex life | ±185°, target ≥1 M cycles |
| Slip sheets | PTFE, 0.15 mm, both faces of the cavity |
| Strain relief | Clamped at **both** the Ø7 plate grommet (r = 29) and the Ø6 hub port (r = 21) |

A 2-wide lay-up is required because four cores side by side would be ~4.5 mm,
over the 3.4 mm usable width. Two deep costs radial space, of which there is
plenty.

**Voltage drop:** 22 AWG is 52.9 mΩ/m; 0.7 m each way ⇒ 74 mΩ round trip.
At 2 A continuous that is 0.15 V; at the 5.6 A wheel stall, 0.41 V. Fine.

**Derating warning:** a conductor coiled in a sealed still-air cavity derates
roughly 50%. 24 AWG carries only ~1.8 A there — which is why the power cores
are 22 AWG and not 24.

### 2.5 Why 20 V and not 48 V across the spring

Earlier harness analysis concluded 48 V was necessary to make the cable fit,
because a ~100 W wheel motor at 24 V needs 4.9 A continuous / 12–15 A peak and
therefore 18–20 AWG (1.6–2.1 mm OD each), which does not fit. **That analysis
sized for a 100 W wheel.** The GIM4305-10 is a 1 N·m / 300 rpm part at 2 A
nominal and 5.6 A stall — roughly 40 W. At 20 V, 22 AWG is comfortable and the
48 V argument dissolves. This resolves the conflict flagged between the harness
and battery research streams.

## 3. Wiring diagram

```
                    ┌─────────────── CHASSIS ───────────────┐
   6S PACK ─XT30─────┤ loop key ─ 30A fuse ─ ideal diode     │
                    │      │                                 │
                    │      ├── shoulder L  ─XT30PB(2+2)──── GIM6010-8 L  [bus A]
                    │      ├── shoulder R  ─XT30PB(2+2)──── GIM6010-8 R  [bus A]
                    │      │
                    │      ├── 20 V buck ──┬── clock spring L ──┐
                    │      │               └── clock spring R ──┼─┐
                    │      │                                     │ │
                    │      └── LMR33630 5 V ── 3.6 V ── 3.3 V    │ │
                    │              │                             │ │
                    │        MAIN BOARD  STM32G474RET6           │ │
                    │         ├ ICM-42688-P (SPI1)               │ │
                    │         ├ FDCAN1 → TCAN3414 → bus A ───────┘ │
                    │         ├ FDCAN2 → TCAN3414 → bus B ─────────┘
                    │         ├ FDCAN3 → TCAN3414 → bus C
                    │         ├ INA228 + 2 mΩ shunt
                    │         └ BQ76952 (I²C) ── 6 balance taps
                    └────────────────────────────────────────┘

  PER LEG, across the clock spring (4 cores: 20 V, GND, CAN_H, CAN_L):
     → PROXIMAL LINK: satellite node (STM32G0B1 + TCAN332G + 3.3 V buck)
                       └─ 40 mm SPI ─→ AS5048A @ knee axle
     → across the knee (service loop, −8°…+27°, 4 cores)
                       └─→ GIM4305-10 wheel driver (SDC101)
```

## 4. CAN topology and termination

Three buses (rationale in `README.md`). Per bus:

- **Daisy-chain, never star.** Stubs ≤30 mm.
- **120 Ω at the two true electrical ends only.** Both Steadywin drivers may
  ship with integrated terminators — **check and disable the ones in the
  middle**, or you land at 30–40 Ω and nothing works above 250 kbit/s.
- **Split termination at the controller**: 2 × 60 Ω with a 4.7 nF cap to GND
  between them. Kills common-mode ringing.
- **Unpopulated common-mode choke footprint** in series with each pair.
- **Scope test points** on every CAN_H/CAN_L pair. You will need them.
- **No galvanic isolation.** ~3 mm of height and ~$4/channel to break a ground
  loop that does not exist on a 300 mm single-battery robot.

Bus ends, physically:

| Bus | Nodes | Terminate at |
|---|---|---|
| A — shoulders | main board, GIM6010-8 L, GIM6010-8 R | main board, and the farther shoulder |
| B — left leg | main board, satellite L, wheel L | main board, and wheel L |
| C — right leg | main board, satellite R, wheel R | main board, and wheel R |

## 5. Grounding and shielding

The chassis is PA-CF — **electrically insulating, so there is no chassis
ground and no ground plane outside the PCBs.** Consequences:

1. **Single-point star ground at the main board's power entry.** Every return
   comes back there; no daisy-chained grounds between subsystems.
2. **Separate analog and power ground pours** on the main board, joined at one
   point beneath the MCU. IMU and AS5048A analog returns go to the analog pour.
3. **Motor power and CAN in the same jacket is acceptable** at these currents
   *provided* the CAN pair is a screened twisted pair, screen grounded at the
   **chassis end only** (one end — grounding both invites a loop current).
4. **Keep the 5 Ω brake resistor's return out of the signal ground.** It is a
   140 W pulse path.
5. There is no shielding benefit from the structure. Any EMI mitigation has to
   be in the cable and the layout.

## 6. Connector schedule

| Ref | Location | Connector | Ways | Signals | Notes |
|---|---|---|---|---|---|
| J1 | Pack → chassis | XT30 (loop key inline) | 2 | V+, V− | Keyed. The hard disconnect. |
| J2 | Charge / balance | JST-XH 7-way | 7 | 6 taps + GND | Standard LiPo balance lead |
| J3/J4 | Chassis → shoulder | **AMASS XT30PB(2+2)-M** on drive, XT30(2+2)-F on cable | 4 | V+, GND, CAN_L, CAN_H | Steadywin's own. **NOT reverse-polarity protected — wrong polarity destroys the driver.** Pinout **[UNVERIFIED]**, from a CyberGear reference. |
| J5/J6 | Chassis → clock spring | JST GH 4-way, side-entry | 4 | 20 V, GND, CAN_H, CAN_L | Side-entry: GH top-entry is 7.3 mm and will not clear the 8 mm slot |
| J7/J8 | Clock spring → satellite | JST GH 4-way | 4 | as above | |
| J9/J10 | Satellite → AS5048A | JST SH 6-way | 6 | 3V3, GND, CSn, CLK, MISO, MOSI | 40 mm run |
| J11/J12 | Satellite → wheel driver | SDC101 4-pin | 4 | **[UNVERIFIED]** — type and pinout not published | Blocker; see `05_open_questions.md` |
| J13 | E-stop | JST SH 2-way | 2 | Fail-safe loop | Button *closes* to keep the FET on |
| J14 | Debug | Tag-Connect TC2030 | 6 | SWD + UART | **Bring SWD out** — USB flashing on these parts is not robust |

## 7. Mass

| Item | g |
|---|---:|
| Clock-spring cable, 2 × 500 mm | 16 |
| Body harness (motor power, CAN, e-stop, sense) | ~39 |
| **Wiring subtotal** | **~55** |
| Main PCB assembled | ~22 |
| Satellites, 2 × | ~6 |
| Connectors, fuse, loop key, shunt, brake resistor | ~20 |
| BMS / balance harness | ~15 |
| **Electronics total** | **~118 g** vs a 120 g budget |

**Wiring is the largest single line item — 46% of the electronics budget, more
than twice the main PCB.** Daisy-chaining CAN rather than starring it is worth
real grams as well as signal integrity. There is no margin here; every gram
added downstream comes out of the robot's 210 g total margin.
