# 07 — Bill of Materials and Shopping List

Prices are **2026 indicative single-quantity USD** from Digi-Key / Mouser /
LCSC / hobby retail. Treat them as ±30% and re-check at order time. Anything
marked **[BLOCKED]** must not be ordered until `05_open_questions.md` clears it.

## 0. Order in three waves (+ a Wave 0 for the single-leg rig)

| Wave | When | Why |
|---|---|---|
| **0 — single-leg rig** | Now | **Teensy path.** Everything needed for the rig in `fusion_brief_single_leg_rig.md` §5 |
| **A — order now** | Today | Long lead or needed for Stages 0–2 of the **two-leg robot**, and unaffected by the open blockers |
| **B — after Steadywin answers B1** | Wheel-driver max bus voltage | Decides 5S vs 6S vs 6S+buck, i.e. the pack and half the power tree |
| **C — after rev-A board bring-up** | Stage 3 | Don't buy five of anything you haven't run once |

## Wave 0 — single-leg rig (~$45 electronics, excluding rig hardware)

The rig runs a **Teensy 4.1** (already in hand), two CAN buses at 500 kbps on
breadboarded TCAN3414s, and the knee AS5048A wired directly via SPI — no
satellite node, no custom PCB, no PCB lead time.

| Item | Part | Qty | Unit | Notes |
|---|---|---:|---:|---|
| CAN transceiver breakout | **TCAN3414** or TCAN332G, 3.3 V | 2 | $3 | One per bus. **Not SN65HVD230** (5 V — kills the Teensy) |
| IMU breakout | **ICM-42688-P** | 1 | $12 | Mount on the carriage, not the column |
| Knee encoder | **AS5048A** (TSSOP-14 breakout or PCB) | 1 | $12 | SPI direct to Teensy |
| Diametric magnet | 6 × 2.5 mm NdFeB | 2 | $2 | Spare |
| Brake resistor | 5 Ω, pulse-rated, ≥50 W | 1 | $6 | **Mandatory before any Mode B drop** |
| Comparator (brake chopper) | **TLV3011** | 1 | $2 | Set thresholds for 20 V bus (~21.5 V on / ~20.8 V off), not the 25.2 V pack |
| microSD cards | SanDisk Extreme 32 GB | 2 | $10 | Teensy's onboard socket |
| Bench PSU | any 0–30 V / 5 A, current-limited | 1 | $70 | **Run at 20 V, not 24 V** (blocker B1) |
| E-stop | XT30 loop key | 1 | $3 | |
| Breadboard + hookup wire | — | 1 | $10 | Logic only — motor current is soldered 16–18 AWG direct from PSU |

**You already own** the Teensy 4.1, both actuators, and a milliohm meter
(borrow if not). The bench PSU is shared with Wave A.

## Wave A — two-leg robot dev hardware, order now (~$310)

### A1. Development and instrumentation

| Item | Part | Qty | Unit | Notes |
|---|---|---:|---:|---:|
| Core board (Stage 0–1 dev) | WeAct **STM32G474CEU6** | 2 | $12 | Lets Stages 0–1 run during the 4–6 week PCB lead |
| Debug probe | ST-LINK V3 MINIE | 1 | $12 | Or a spare Nucleo's onboard probe |
| Tag-Connect cable | **TC2030-CTX-NL** | 1 | $40 | Painful price, worth it — no header height in the 8 mm slot |
| Bench PSU, current-limited | any 0–30 V / 5 A | 1 | $70 | **Stage 0 runs on this, never the pack** |
| Inline watt meter | Turnigy 130 A or similar | 1 | $25 | Replaces every estimate in `01` |
| USB logic analyser | any 8-ch 24 MHz | 1 | $12 | CAN and SPI sanity |
| microSD cards | SanDisk Extreme 32 GB | 3 | $10 | Buy three; you will corrupt one |
| Milliohm meter or 4-wire DMM | — | 1 | $60 | For C7 phase resistance. Borrow if possible |

### A2. Sensors and silicon (buy spares — these are cheap and small)

| Item | Part | Qty | Unit |
|---|---|---:|---:|
| IMU | **ICM-42688-P** | 4 | $9 |
| Knee encoder | **AS5048A** (SPI, TSSOP-14) | 4 | $12 |
| Diametric magnet for AS5048A | 6 × 2.5 mm NdFeB, axially diametric | 6 | $2 |
| CAN transceiver, main | **TCAN3414DRQ1** | 8 | $2 |
| CAN transceiver, satellite | **TCAN332GDR** | 5 | $2 |
| Satellite MCU | **STM32G0B1CBT6** | 4 | $5 |
| Main MCU | **STM32G474RET6** (LQFP64) | 3 | $9 |
| Power monitor | **INA228AIDGSR** | 3 | $4 |
| Shunt | 2 mΩ 2 W 2512, ≤1% | 4 | $2 |
| BMS AFE | **BQ76952PFBR** | 2 | $5 |
| 5 V buck | **LMR33630ADDAR** | 4 | $3 |
| Comparator (brake chopper) | **TLV3011AIDBVR** | 4 | $2 |
| Ideal-diode controller | **LM74700QDBVRQ1** | 3 | $2 |
| Windowed watchdog | **TPS3851G18DRVR** | 3 | $2 |
| Inductors | Coilcraft **XGL4020** series, 2.1 mm tall | 10 | $2 |

### A3. Mechanical / harness consumables

| Item | Spec | Qty | Unit |
|---|---|---:|---:|
| Clock-spring cable | 4-core, 2 × 22 AWG + screened 26 AWG pair, silicone high-flex, flat-oval ≈3.0 × 2.2 mm | 1.5 m | ~$25/m |
| PTFE sheet | 0.15 mm, for slip sheets (CR-6) | 1 sheet | $12 |
| JST GH 4-way, side-entry | connector + crimped leads | 10 | $1 |
| JST SH 6-way / 2-way | + leads | 10 | $1 |
| XT30 + XT30 loop key | — | 4 | $3 |
| Blade fuse holder + 30 A slow-blow | inline | 2 | $4 |
| Brake resistor | 5 Ω, pulse-rated, ≥50 W continuous equivalent | 2 | $6 |
| Foam mat + overhead tether | for Stages 4–6 | 1 | $40 |

**Do not skip the mat and tether.** They are the cheapest line items here and
they are what stops Stage 4 from ending the project.

## Wave B — blocked on B1 (~$60–120)

| Item | Part | Qty | Unit | Condition |
|---|---|---:|---:|---|
| **Battery** | **GNB 6S 550 mAh long type, GNB5506S100AHV**, 36 × 18 × 71 mm, 82 g | 2 | $35 | **[BLOCKED on B1.]** 2 packs = a spare, or 6S2P if CR-1 lands |
| Balance charger | any 6S LiHV-capable | 1 | $60 | **Charge to 4.20 V/cell, not 4.35** |
| 20 V buck module | 100 W, 25 V in → 20 V out, ~15 g | 2 | $12 | **Deleted entirely if Steadywin confirms ≥30 V** for the SDC101 |
| Wheel-driver mating connector | SDC101 4-pin | 4 | ? | **[BLOCKED on B2 — type unpublished]** |
| Shoulder mating connector | AMASS **XT30PB(2+2)-F** | 4 | $2 | Pinout **[UNVERIFIED]** — confirm before first power-on (Q14) |

**B1 is the one answer that unblocks the most money.** Everything about the pack,
the buck, the harness gauge and the regen design hangs on it.

## Wave C — after rev-A bring-up

| Item | Qty | Unit | Notes |
|---|---:|---:|---|
| Main PCB, 84 × 60 × 1.0 mm 4-layer, assembled | 5 | $30–70 | JLCPCB/PCBWay. **Budget a rev B.** 4–6 week lead |
| Satellite PCB, ~14 × 25 mm 2-layer, assembled | 6 | $8 | Cheap — order spares |
| Stencils | 2 | $10 | |

## 1. Cost summary

| Wave | Range |
|---|---:|
| 0 — single-leg rig electronics | **~$45** (excl. bench PSU shared with Wave A) |
| A — dev, sensors, silicon, harness | **$280–340** |
| B — pack, charger, buck, connectors | **$160–220** |
| C — PCBs, two revisions | **$300–500** |
| **Total electronics for prototype 1** | **≈$750–1,050** |

Excludes the actuators (already in hand) and the chassis. The **PCB revisions
are the largest single line** and the most likely to grow — assume two spins.

## 2. What is deliberately *not* on this list

- **A Linux SBC.** Deferred to prototype 2 (`03_compute_and_can.md` §3).
- **A commercial BMS board.** A JBD 6S is 130 × 65 × 10 mm and fits nowhere.
- **Slip rings.** Rejected on fretting corrosion under ±185° oscillatory duty.
- **CAN isolators.** ~3 mm of height to break a ground loop that does not exist.
- **Large bulk capacitance.** It cannot absorb regen — see the arithmetic in
  `01_power_and_battery.md` §4.1.
- **A load cell of any kind.** The AS5048A already resolves 0.025 N per leg.

## 3. Mass check against the BOM

| Item | g |
|---|---:|
| Battery (1 × GNB 6S 550) | 82 |
| Main PCB assembled | 22 |
| Satellites, 2 × | 6 |
| Clock-spring cable, 2 × 500 mm | 16 |
| Body harness | 39 |
| Connectors, fuse, loop key, shunt, brake resistor | 20 |
| BMS / balance harness | 15 |
| 20 V buck (deleted if B1 clears) | 15 |
| **Total** | **215 g** |

Against a **250 g battery + 120 g electronics = 370 g** allowance, that is
comfortable — **but only because the battery came in at 82 g instead of 250 g.**
The electronics line alone is ~133 g against 120 g and is already over. If C4
holds and the actuators are really 388 g / 150 g rather than 500 g / 250 g, the
whole picture relaxes by ~420 g and 6S2P becomes free.

**Weigh the actuators before you finalise anything on this page.**
