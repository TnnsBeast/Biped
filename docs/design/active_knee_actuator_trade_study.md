# Active-knee actuator and transmission trade study

Status: **knee actuator recommended 2026-09-27 for the crank-and-pushrod R2A
concept; not purchased.** Prices and published specifications below were
checked on 2026-09-25. They exclude tax, shipping, linkage hardware and printed
parts. Vendor sites were not reachable from the 2026-09-27 session, so no price
has been re-checked.

## Recommendation

**Buy one more Steadywin GIM6010-8 for the knee.** Keep the owned GIM6010-8 as
the shoulder actuator and the owned GIM4305-10 as the wheel actuator.

The [R2A plan](active_knee_revision2_plan.md) copies Beni's knee drive: an
actuator on the shoulder axis, riding on the proximal link, turns a crank that
drives the distal link through a pushrod. [`r2a_calc.py`](../../r2a_calc.py)
shows that the linkage cannot add useful reduction.
- The μ ≥ 40° transmission-angle rule, applied over roughly 100° of knee
  travel, leaves only near-parallelograms, with N = 0.866–0.937 for the
  selected geometry.
- The knee actuator must therefore supply the knee torque directly: 2.15 N·m to
  stand at α = 80° for a 4.768 kg robot, and about 5.0 N·m for one full robot
  weight per leg at the crouch (figures updated 2026-09-27 to the
  Fusion-measured linkage mass).

The GIM6010-8 wins on four counts:

1. **Torque class.** Standing uses 43% of its 5 N·m rated torque at the knee,
   or 5.2 A after the linkage ratio (49% of rated current). Stall is 11 N·m.
2. **Bus voltage.** It runs on the owned 20 V bench bus, like the owned unit.
   The 20 V bus is fixed until blocker B1 clears.
3. **Electronics and firmware.** It speaks the same ODrive CANSimple protocol as
   the shoulder. It joins bus A as node 1, running 1 Mbit for two nodes at
   1 kHz, and needs no new driver code or transceiver.
4. **Mechanical interfaces.** Its housing mount (8 × M3 on Ø74) and output
   (6 × M3 on Ø25, 3 × Ø4 pins) match the owned unit. The printed plate, hub,
   dowel and insert designs, and every coupon they passed, carry over.

Its costs:
- **Mass.** 388 g bare, or 500 g per the brief (conflict C4 unresolved).
- **Size.** Its Ø80 × 44 mm envelope on the shoulder axis sets the 256.2 mm
  track and the 51° flexion stop.
- **Price.** No price is recorded in this repository; confirm it at order.

The 2026-09-25 advice against a second GIM6010-8 assumed a belt layout, where
the knee motor had to fit the proximal-link root or a body jackshaft. The crank
layout puts the actuator outboard on the shoulder axis, where its size costs
crouch depth and track width but no drive stage.

Stage the spending around the single-leg article. Buy **one** knee unit now.
Buy the two-leg units only after the single-leg digital, unpowered, detached
and wheel-clear gates pass. Order the linkage hardware (§6 of the plan)
against the calculated requirements, not a catalogue guess.

### How the other candidates screen for this layout

| Candidate | Result for the crank layout |
|---|---|
| RobStride 05, EduLite 05 | **Rejected.** Standing needs 134% / 119% of their published rated torque, and the linkage cannot make up the difference. |
| RobStride 00 | **Fallback.** The torque class fits: 43% at stance, 14 N·m peak, 310 g. Its published 24–60 V range excludes the 20 V bus. It also needs RobStride CAN at 1 Mbit on a separate bus and a new mechanical interface with its own coupons. Reconsider it only if knee mass must drop and B1 allows a bus of 24 V or more. |
| RobStride 01, 02 | Rejected for the same bus-voltage, protocol and interface reasons. Their Ø78.5 bodies bring no packaging gain over the GIM6010-8. |
| GIM4305-10, second unit | Rejected. At 1 N·m rated and 3.47 N·m stall it is weaker than the standing requirement. |

## Integrated actuator shortlist

| Candidate | Published price | Size | Mass | Voltage | Published output | R2A reading |
|---|---:|---:|---:|---:|---:|---|
| RobStride 05 | $110 | 46 × 46 × 44 mm | 191 g | 15–60 V | 1.6 N·m rated, 5.5 N·m peak; 7.75:1 | **[SUPERSEDED 2026-09-27]** was the belt-layout budget pick; rejected for the crank layout (stance 134 % of rated at the 4.768 kg mass) |
| EduLite 05 | $80 | 46 × 46 × 44 mm | 242 g | 15–60 V | 1.8 N·m rated, 6 N·m peak; 9:1 | **[SUPERSEDED 2026-09-27]** was the price-floor alternate; rejected for the crank layout (stance 119 % of rated at the 4.768 kg mass) |
| RobStride 00 | $125 | 57 × 57 × 51 mm | 310 g | 24–60 V | 5 N·m rated, 14 N·m peak; 10:1 | Fallback for the crank layout if B1 permits ≥ 24 V; the jackshaft layout it was paired with is rejected |
| RobStride 01 | $130 | 78.5 × 78.5 × 40 mm | 380 g | 24–48 V | 6 N·m rated, 17 N·m peak; 7.75:1 | Rejected: ≥ 24 V, new protocol and interface, no packaging gain over the GIM6010-8 |
| RobStride 02 | $145 | 78.5 × 78.5 × 45.5 mm | 405 g | 24–60 V | 6 N·m rated, 17 N·m peak; 7.75:1 | Rejected: as RobStride 01; dual encoder noted |

All five combine motor, controller, reduction and magnetic encoder(s), use FOC
and publish 1 Mbps CAN. They are retained here as dated comparison data.

Official sources:

- [RobStride product and price index](https://www.robstride.com/)
- [RobStride 05 specifications](https://robstride.com/products/robStride05)
- [EduLite 05 specifications](https://www.robstride.com/products/eduLite05)
- [RobStride 00 specifications](https://www.robstride.com/products/robStride00)
- [RobStride 01 specifications](https://robstride.com/products/robStride01)
- [RobStride 02 specifications](https://www.robstride.com/products/robStride02)
- [RobStride sample code and tools](https://www.robstride.com/open-source)

## Why the inexpensive outrunner route is not the baseline

A bare hobby outrunner makes the motor price look low, but it does not include
the joint reduction, motor controller, load encoder, enclosure, connectors or
tuning work.

The traceable ODrive example is already more expensive than the integrated
candidates before transmission parts: the official D5065 motor is **$89** and
the single-axis S1 controller is **$149**, for **$238** before an off-axis
encoder, pulleys, belt and guarding. It is a capable, open development path,
but not the low-cost path for this robot.

A Flipsky H5055 plus Mini FSESC6.7 Pro is **$120** at the checked prices before
an encoder and reduction. The motor alone is listed at **475 g**, and the ESC
vendor says a newer firmware upgrade may damage the controller and recommends
retaining factory firmware 5.2. That combination may be useful on a bench for
motor-control experiments, but it adds mass and integration risk without a
clear cost advantage over a compact integrated actuator.

Official sources:

- [ODrive D5065 motor](https://shop.odriverobotics.com/products/odrive-custom-motor-d5065)
- [ODrive D5065 electrical data](https://docs.odriverobotics.com/v/latest/hardware/odrive-motors.html)
- [ODrive S1 controller](https://shop.odriverobotics.com/products/odrive-s1)
- [Flipsky H5055 motor](https://flipsky.net/collections/new-accessories/products/brushless-dc-motor-h5055-5055-200kv-1380w)
- [Flipsky Mini FSESC6.7 Pro](https://flipsky.net/products/mini-fsesc6-7-pro-70a)

## Other mechanisms considered

| Concept | Why it is interesting | Decision for R2A |
|---|---|---|
| One central knee motor driving both legs | One knee actuator for the whole robot and naturally synchronized extension | Keep only as a jump-demonstrator idea. It mechanically couples the knees and removes the independent leg motion needed for balance, uneven ground and recovery. |
| Motor-preloaded spring with latch or clutch | A small motor could charge the spring slowly and release high peak power | Defer. It adds a latch, reset sequence and stored-energy hazard while providing poor active landing control. It could become a later jump module after the active knee works. |
| Synchronous belt down the proximal link | Keeps the motor near the shoulder and allows a ratio | **Superseded 2026-09-27 by the crank and pushrod.** It needs a tensioner, a guard, two pulley shafts and a slip-detecting encoder, and its ratio buys nothing once the knee actuator must be 5 N·m-class. Reasoning is in the [R2A plan](active_knee_revision2_plan.md) §11. |
| Cable or tendon transmission | Routes around tight spaces and can keep the motor on the chassis | Do not prefer over the rod linkage. Stretch, pretension, drum layering and service drift add uncertainty to knee position and landing control. |
| Hobby servo or linear actuator | Simple command interface and low advertised price | Reject for the jump-capable knee unless a specific unit later supplies traceable continuous torque-speed, impact, backdrive and thermal data. |
| Printed planetary or cycloidal reducer | Custom ratio and compact packaging | Reject for the first structural design. It conflicts with the goal of a repeatable, low-backlash impact load path using printed and stocked parts without machining. |

## Next step

The R2A plan's digital gate, §10 step 1, replaces the four belt-layout
skeletons that were proposed here on 2026-09-25. Build the single crank layout
around the GIM6010-8 STEP envelope and rerun `r2a_calc.py` with modelled
geometry.
