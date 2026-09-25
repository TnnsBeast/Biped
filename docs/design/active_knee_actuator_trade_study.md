# Active-knee actuator and transmission trade study

Status: **candidate screening only — no actuator or transmission is selected or
released for purchase**. Prices and published specifications were checked on
2026-09-25 and exclude tax, shipping, belt hardware, the independent knee
encoder and printed parts.

## Recommendation

Do **not** buy another GIM6010-8 for the knee at this stage. Preserve the owned
GIM6010-8 as the shoulder actuator and the owned GIM4305-10 as the wheel
actuator. Compare these two lower-cost R2A layouts in Fusion and against the
same knee load cases:

1. **Budget prototype — RobStride 05 on the proximal-link root.** Mount its
   stator to the proximal link as close to the shoulder axis as the service and
   cable paths allow, then run one synchronous belt to the knee output. This is
   the simplest active-knee package: one motor mount, one belt stage and no
   shoulder-axis jackshaft. Its published actuator price is **$110** and its
   published mass is **191 g**. It accepts the existing 20 V bench supply within
   its published 15–60 V range for bring-up. Its rated data are specified at
   48 V, so operation at 20 V does not establish rated speed or power. The added
   mass rotates with the proximal link, and the power/CAN cable must flex
   through the shoulder range.
2. **Performance comparison — RobStride 00 fixed to the body.** Drive a
   shoulder-axis jackshaft and then the knee belt. Its published actuator price
   is **$125**, with **5 N·m rated / 14 N·m peak** output and **310 g** mass.
   This keeps the motor mass on the chassis and has much more published torque
   than the compact candidates, but it adds a belt stage, bearings and assembly
   work. Its published voltage range starts at 24 V, so it cannot inherit the
   20 V test bus without a new power decision.

Those actuator/layout pairings are starting points rather than locked pairs. If
the compact actuator misses the load cases, the RobStride 00 should also be
checked in the simple proximal-root layout before accepting the jackshaft's
extra parts and backlash.

The **$80 EduLite 05** is the price-floor alternative for the budget layout. It
shares the RobStride 05's published 46 × 46 × 44 mm envelope and 15–60 V range,
but it is 51 g heavier and uses a powder-metallurgy reduction instead of the
RobStride 05's machined-steel reduction. It is worth retaining in the CAD and
load spreadsheet, but the $30 saving is not enough to choose it before the
jump and landing duty are known.

The R2A load cases remain the selection gate. The compact actuators' published
continuous output is only 1.6–1.8 N·m. An external reduction can exchange speed
for knee torque, but the ratio cannot be selected until required joint torque,
speed, belt losses, duty and thermal limits are calculated. Peak torque alone
is not a jump rating.

Stage the spending around the existing single-leg article. Buy **one** selected
knee actuator only after the load-case and Fusion-fit gates pass. Buy the second
unit for the two-leg robot only after the first unit passes detached-drive and
supported wheel-clear tests. There is no reason to buy a matched pair during
the architecture study.

## Integrated actuator shortlist

| Candidate | Published price | Size | Mass | Voltage | Published output | R2A reading |
|---|---:|---:|---:|---:|---:|---|
| RobStride 05 | $110 | 46 × 46 × 44 mm | 191 g | 15–60 V | 1.6 N·m rated, 5.5 N·m peak; 7.75:1 | Preferred compact prototype candidate; machined-steel gearing and lowest moving mass in this set |
| EduLite 05 | $80 | 46 × 46 × 44 mm | 242 g | 15–60 V | 1.8 N·m rated, 6 N·m peak; 9:1 | Lowest actuator price; useful price-floor comparison, with heavier powder-metallurgy gearing |
| RobStride 00 | $125 | 57 × 57 × 51 mm | 310 g | 24–60 V | 5 N·m rated, 14 N·m peak; 10:1 | Best size/output/price balance among the stronger candidates; compare as the chassis-fixed/jackshaft layout |
| RobStride 01 | $130 | 78.5 × 78.5 × 40 mm | 380 g | 24–48 V | 6 N·m rated, 17 N·m peak; 7.75:1 | Only $5 above RS00, but its larger diameter is less attractive around the present shoulder stack |
| RobStride 02 | $145 | 78.5 × 78.5 × 45.5 mm | 405 g | 24–60 V | 6 N·m rated, 17 N·m peak; 7.75:1 | Dual-encoder stronger comparison; larger and heavier than RS00 |

All five combine motor, controller, reduction and magnetic encoder(s), use FOC
and publish 1 Mbps CAN. The remote belt still needs an encoder at the physical
knee because an actuator-side encoder cannot detect belt slip, pulley motion or
a changed transmission datum.

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
| Cable or tendon transmission | Routes around tight spaces and can keep the motor on the chassis | Do not prefer over a synchronous belt. Stretch, pretension, drum layering and service drift add uncertainty to knee position and landing control. |
| Hobby servo or linear actuator | Simple command interface and low advertised price | Reject for the jump-capable knee unless a specific unit later supplies traceable continuous torque-speed, impact, backdrive and thermal data. |
| Printed planetary or cycloidal reducer | Custom ratio and compact packaging | Reject for the first structural design. It conflicts with the goal of a repeatable, low-backlash impact load path using printed and stocked parts without machining. |

## Fusion comparison to build next

The next Fusion study should build four skeletons:

- RobStride 05 envelope mounted on the proximal-link root, with one belt stage,
  full shoulder cable loop and actuator removal path;
- RobStride 00 body-fixed with the shoulder-axis jackshaft;
- a compact opposite-side coaxial actuator as a package check;
- an axially stacked actuator as a package check.

The EduLite 05 uses the same published outer envelope as the RobStride 05, so
carry it as a mass and cost alternate in the proximal-root skeleton rather than
creating a fifth layout.

For each skeleton, measure actuator centre distance from the shoulder axis,
moving inertia, belt centre planes, pulley wrap, tensioner access, cable bend
and pinch clearance, motor removal order, controller cooling and collision over
the full shoulder/knee sweep. Use the same derived torque-speed-duty points for
every actuator. Do not buy from this price screen alone.
