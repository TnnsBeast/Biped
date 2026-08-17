# Beni Prototype 1 — Electronics Design

**Revision 0 — 2026-08-09.** Written against `beni_electronics_handoff_brief.md` §10.
Mechanical side is frozen and audited; this is the first pass at the electrical side.

Every number here is traceable to either the CAD/design record (trusted), vendor
documentation (marked), or a calculation shown in-line (reproducible). Where a
figure could not be confirmed it is marked **[UNVERIFIED]** and appears in
`05_open_questions.md`. Do not order parts against an unverified figure.

## Reading order

| File | Covers | Brief §10 deliverable |
|---|---|---|
| `README.md` (this) | Decisions, §3 blockers, architecture | — |
| `01_power_and_battery.md` | Pack, power tree, budget, safety, regen | 1, 6, 7 |
| `02_harness_and_routing.md` | Clock spring, satellite node, connectors | 3, 4 |
| `03_compute_and_can.md` | Controller, IMU, CAN topology | 2, 5 |
| `04_firmware.md` | Plant model, LQR gains, jump/landing FSM, estimation | 8 |
| `05_open_questions.md` | Blockers, supplier questions, change requests | 10 |
| `06_logging_and_bringup.md` | Logging pipeline, 7-stage bring-up with gates | 9 |
| `07_bom.md` | Priced shopping list, ordered in three waves | — |

## The three §3 blockers — resolved

The brief says to resolve these before designing anything downstream. All three
now have answers, and **all three overturned an assumption baked into the BOM.**

### §3.1 Battery voltage — the brief blamed the wrong actuator

The brief assumed the GIM6010-8 shoulder sets the voltage ceiling. It does not.
The GIM6010-8 is a wide-input part (sources give 12–56 V, 15–60 V, or 12–72 V —
see `05_open_questions.md`). **The GIM4305-10 wheel actuator is the binding
constraint**: its SDC101 driver installation guide gives **12–36 V**, while
marketing copy claims 12–48 V and some reseller tables say 12–24 V.

The BOM's 4S pack (14.8 V nom) is too low regardless — a 4S pack cannot drive a
24 V-class actuator at rated performance, and the jump is power-limited.

**Decision: 6S LiPo (22.2 V nominal / 25.2 V full), with a 20 V buck feeding the
two wheel drivers.** The buck costs ~15 g and is deleted if Steadywin confirms
the 36 V rating in writing. This is the only option that is safe under *both*
the 24 V and the 36 V reading of the spec. See `01_power_and_battery.md` §2.

### §3.2 Battery physical size — cylindrical cells are out, and Z must open up

The CAD envelope is 69 × 25 × 45 mm = 77.6 cm³ at 250 g. A standard 4S 2200
LiPo is ~105 × 34 × 30 mm and 105 mm does not fit anywhere in the chassis.

Cylindrical cells fail on both axes: 6 × Molicel P26A 18650 is 275 g bare (over
the 250 g budget before assembly) and the 28 mm Z limit means the top-forward
box takes exactly **one** 18650. You need six and you can site two.

**Decision: GNB 6S 550 mAh "long type" (GNB5506S100AHV), 36 × 18 × 71 mm, 82 g,
12.2 Wh.** Near-exact match to the 36 × 28 × 72 mm top-forward box. It is a
**LiHV** pack — charge to 4.20 V/cell as ordinary LiPo, never 4.35 V.

Runtime is honest but short: ~18 min standing, ~10 min driving, ~13 min mixed.
**The single highest-value mechanical change available is opening chassis Z from
28 to 40 mm**, which allows 6S2P (2 packs, 164 g, 24.4 Wh) — double the runtime
and half the C-rate stress, still inside the mass budget. See `05_open_questions.md`.

### §3.3 Harness conductor count — the cavity constraint was misread

The brief treats the clock-spring cavity's 4.0 mm axial height as a *thickness*
limit and reasons about FFC. **It is a width limit.** In a clock spring the
bending curvature points radially, so bending strain is set by *radial*
thickness (12 mm available); the 4.0 mm axial dimension is the ribbon **width**
(~3.4 mm usable after slip sheets). A 20-way 1.0 mm-pitch FFC is 20+ mm wide and
cannot fit. At 3.4 mm you get 3 ways at 1.0 mm pitch or 6–7 at 0.5 mm.

**Decision: a satellite CAN node on the proximal link**, which drops the crossing
conductor count from 7–10 to **four** — V+, V−, CAN_H, CAN_L. The AS5048A then
runs full-rate SPI over a 40 mm PCB trace instead of 700 mm of cable next to a
motor. See `02_harness_and_routing.md`.

**Also corrected: the clock-spring wrap margin in the design record is wrong.**
§4.3 claims ~470° capacity / 27% margin from 400 mm of cable. Recomputing:

```
Δθ = L·(r_o − r_i) / (2π·r_i·r_o) = 400 × 11 / (2π × 20.5 × 31.5) = 1.084 turns = 390°
```

Against a 370° requirement that is **20° / 5% margin, not 27%.** Specify
**470–500 mm** of free spiral.

## System architecture

```
         6S LiPo 22.2V ──┬── fuse 30A ── P-FET soft-start ── XT30 loop key
                         │
              ┌──────────┼──────────────┬──────────────────┐
              │          │              │                  │
        shoulder L   shoulder R    20V buck ──┬── wheel L   │
        GIM6010-8    GIM6010-8               └── wheel R    │
              │          │                    │        │    │
          [CAN bus A: ODrive CANSimple]   [bus B]  [bus C]  │
              └────┬─────┘                    │        │    │
                   │                          │        │    │
              MAIN BOARD (STM32G474RET6, 84 × 60 × 1.0 mm, centre slot)
                   │                          │        │
                ICM-42688-P IMU        satellite L  satellite R
                                       (STM32G0B1 + AS5048A, proximal link)
```

**Three CAN buses, not one.** This falls out of two independent constraints that
happen to agree:

1. **Protocol.** The two actuators do not speak the same protocol. The GIM6010-8
   is an ODrive CANSimple derivative (`ID = node_id<<5 | cmd_id`); the
   GIM4305-10's SDC101 runs a proprietary "SteadyWin" or MIT protocol with its
   own master-ID scheme. Mixing them on one bus is possible but miserable.
2. **Bandwidth.** A single 1 Mbit classical bus cannot carry 4 nodes at 1 kHz —
   94% load typical, **108% worst-case** with bit stuffing. Neither actuator
   supports CAN-FD, so the FD escape hatch is closed.

The split — **A = both shoulders, B = left wheel + left satellite, C = right
wheel + right satellite** — lands every bus at 35–47% load, keeps each protocol
on its own wire, and matches the three FDCAN peripherals on an STM32G474RET6
exactly. It also means each clock spring carries only *its own* leg's bus, so
the 4-conductor crossing works with no sharing.

## Standing decisions

| Area | Decision |
|---|---|
| Bus voltage | 6S LiPo, 25.2 V full; 20 V buck for wheel drivers |
| Pack | GNB 6S 550 mAh long type, 82 g (2P if Z opens to 40 mm) |
| Controller | Custom 84 × 60 × 1.0 mm 4-layer, STM32G474RET6 |
| IMU | ICM-42688-P, 8 kHz ODR, AAF 250–500 Hz, decimate to 1 kHz |
| CAN | 3 × classical 1 Mbit, TCAN3414 transceivers |
| Knee sensing | AS5048A on a satellite STM32G0B1CBT6 node, per leg |
| Control rate | 1 kHz (500 Hz floor) |
| E-stop | XT30 loop key (primary) + fail-safe soft stop + windowed WDT |
| Estimated mass | ~118 g against a 120 g budget — no margin |

## Four numbers in the brief that are wrong

Found while deriving the control design from `sim/beni.urdf` and
`sim/beni_inertia.json`. Full working in `04_firmware.md` §1.

| Brief | Actual |
|---|---|
| Unstable pole 9.7 rad/s | **11.18 rad/s** (τ = 89 ms). The LIPM formula drops body pitch inertia and the wheel reaction torque. |
| A 100 mm drop has ~10% energy margin on the knees | **It bottoms out.** The brief omits gravity work during the 50 mm of compression: 4.85 J demand vs 3.55 J capacity. Passive limit is ~49 mm (spring-rate method). |
| Clock spring: 27% wrap margin | **5%** (§3.3 above). |
| Shoulders control ride height | **dRide/dθ_s = 0 at the nominal pose.** Zero height, damping and CBF authority at θ_s = 0. Fixed by a scissor stance. |

Consequence for the test plan: the brief's gate *"no powered jump until a 100 mm
drop never reaches +27°"* **cannot be passed passively.** It is replaced with a
49 mm passive gate plus a 100 mm gate run with the shoulder landing controller
live — see `06_logging_and_bringup.md` Stage 5.

Two further findings that are not brief errors but change the design:

- **The IMU datum pad is 195 mm above the wheel axis** — the worst location on
  the robot. At 20 rad/s² of pitch acceleration the lever arm produces 22° of
  apparent tilt against a 0.1° budget. Move it (CR-9).
- **A leg bounce mode at 3.67 Hz sits only 2.06× above the balance pole**, with
  ζ ≈ 0.01. Active shoulder damping is mandatory, not optional.

## Status

All ten §10 deliverables are drafted across `01`–`06`. Nothing here has been
built or measured: every power figure is an estimate pending an inline watt
meter, the peak-power number swings ±40% on an unverified phase resistance, and
the wheel driver's maximum bus voltage — the one answer that decides the pack —
is still outstanding with Steadywin. **Read `05_open_questions.md` before
ordering anything.**

The shopping list is in `07_bom.md`, split into a wave you can order today
(~$310, dev hardware and sensors) and a wave that is blocked on Steadywin.
