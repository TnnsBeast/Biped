# Beni-Like Wheeled Biped — Prototype 1 Fusion Design Guide

> ### ⚠ BUILD CONSTRAINT, 2026-08-12 — two rules below are overridden
>
> **3D printed and off-the-shelf parts only. No laser cutting, no machining.**
> See **[`MANUFACTURING_CONSTRAINTS.md`](MANUFACTURING_CONSTRAINTS.md)**.
>
> The frozen kinematics (§4–§9 geometry, §17's freeze list) are **untouched** and
> remain the authority. Two *material and process* rules are not satisfiable and
> have been overridden with reasons:
>
> | Rule | Status |
> |---|---|
> | §9 — "Use a metal output hub/adapter where torque is transferred. **Do not use a printed friction-fit shaft/hub interface**" | **Overridden.** `Wheel_Hub_L` is printed and takes torque by friction at 3 × M3, ≈20.7 N·m capacity against a ≈4–5 N·m peak. Mitigations are mandatory, not optional: a steel washer under every screw head, and re-torque after the first hour then every ~10 hours, because preload in plastic creeps. `beni_rig_no_machining.md` §2.1 |
> | §10 — "Use metal for … **motor output hubs**" | **Overridden** for the same part and for `Shoulder_Output_Hub_L`, which is printed **plus three bought Ø4 × 10 hardened dowel pins**. The pins are what keep the constraint honest: the printed register alone sees 63 MPa at proof load against PA-CF's ~40–50 MPa shear, and the pins move the shear into steel. `beni_rig_no_machining.md` §2.1 |
>
> Everything else §10 asks for in metal is still metal, just **bought** rather than
> machined: the knee axle is a Ø10 hardened dowel pin, the cartridge pivots are Ø4
> clevis pins, and the final hard-stop surface is a stack of M5 washers loaded in
> compression (design record §8).


## 1. Mission and agent behavior

Design a **physically buildable first prototype that reproduces the mechanics of Mondo Robotics' current Beni-style serial leg**, using the supplied STEP files for:

- Shoulder: **Steadywin GIM6010-8**
- Wheel: **Steadywin GIM4305-10**

The design is not complete until it is manufacturable, printable, assemblable, serviceable, fully fastened, and collision-checked through its full motion.

### Work autonomously
Continue until the complete robot and all validation checks are finished.

Do **not** stop after normal phases to ask whether to continue. Do not ask for approval of routine engineering choices. If a detail is unspecified:

1. inspect the supplied STEP geometry and existing model;
2. make a conservative, practical engineering assumption;
3. record the assumption;
4. continue.

Only ask the user if work is genuinely blocked by missing/corrupt source geometry or irreconcilable requirements.

If subagents are available, use them **serially only**. Every subagent must inspect and verify the previous phase before modifying the model.

---

# 2. Architecture to reproduce

The best-supported reconstruction of Beni is:

**body → active rotary shoulder → proximal link → passive spring-loaded cylindrical knee/elbow → distal link → driven wheel**

This serial biped morphology is intentional. Mondo previously built a parallel-leg prototype and reported that it was mechanically stiffer and more robust, but moved to the current bipedal morphology. Do **not** replace this design with an Ascento-style four-bar, active knee, or telescoping leg simply because it is easier mechanically.

## Shoulder
- Shoulder motor is fixed to the body.
- The complete leg rotates about the shoulder output.
- Require **at least one complete 360° usable mechanical sweep**.
- Target Fusion joint range: approximately **-185° to +185°**.
- This means 360° total usable motion, **not necessarily unlimited multi-turn rotation**.
- The shoulder must move in either direction for normal posture, jumping, flips, recovery, and self-righting.

## Knee
The knee is **passive**. There is no knee actuator.

The knee contains the compliant spring mechanism and sits between the proximal and distal leg links. The exact internal Beni spring linkage is not public; the mechanism below is the engineered Prototype 1 implementation chosen because its kinematics and force curve work.

## Wheel
The wheel motor is fixed to the distal link and independently drives the wheel.

---

# 3. Important mechanical behavior

Do not model or reason about the passive knee as if it were commanded by shoulder position.

### Shoulder rotation does NOT automatically compress the knee
If the wheel can move freely, rotating the shoulder mainly rotates the whole bent leg. The passive knee changes angle only when forces acting through the distal link create enough moment about the knee to overcome the spring.

### Normal "squat" / ride-height change
For a deliberate low stance, the shoulder rotates the whole bent leg while the driven wheel rolls to accommodate the fore-aft motion. The passive knee should remain near its load-dependent equilibrium.

Do **not** require a deep static knee fold as the normal squat mechanism.

### Knee compression
Knee flexion occurs when wheel/ground forces create knee moment. This is strongest during:
- dynamic jump preload,
- takeoff,
- landing,
- terrain impacts.

Coordinated wheel torque can influence knee loading, but the design must not depend on the wheel motor statically forcing the knee to full compression.

### Jump
The important observed Beni behavior is:

**During a jump, the shoulder actuators rotate the leg assemblies so the lower/distal legs and wheels are driven rapidly downward against the ground. The resulting ground reaction loads and compresses the passive spring knees while accelerating the body upward.**

The phrase "drive the legs downward" describes the jump action. It does not limit shoulder rotation direction.

### Landing
The passive knee handles the first impact/compliance and stores/returns energy. The active shoulder must also be allowed to **yield and provide active damping** rather than mechanically locking during landing.

This follows the same general lesson demonstrated by Ascento: passive leg compliance is useful, but active hip/shoulder control can act as a virtual spring-damper during landing.

---

# 4. Frozen Prototype 1 kinematics

Use these as global Fusion parameters unless the motor STEP geometry proves a direct physical conflict.

| Parameter | Value |
|---|---:|
| Design mass | 3.5 kg |
| Static load, each leg | ~17.2 N |
| Wheel OD | 110 mm |
| Proximal link L1 | 120 mm |
| Distal link L2 | 120 mm |
| Nominal proximal-link angle | +50° from downward vertical |
| Nominal distal-link angle | -50° from downward vertical |
| Nominal wheel position | directly below shoulder |
| Passive knee extension stop | φ = -8° |
| Passive knee nominal | φ = 0° |
| Main flexion design point | φ = +25° |
| Physical flexion hard stop | φ = +27° |
| Structural link/knee width budget | ~28 mm |

### Knee-angle convention
With the proximal link fixed, positive knee flexion rotates the distal link farther away from vertical:

**distal angle = -50° - φ**

Do not reverse this convention accidentally.

### Fusion geometry checkpoints

With the shoulder fixed at nominal:

| Knee φ | Vertical wheel compression | Fore-aft wheel displacement |
|---:|---:|---:|
| -8° | -12.0 mm | 11.6 mm |
| 0° | 0 | 0 |
| +5° | 8.3 mm | 6.4 mm |
| +10° | 17.1 mm | 12.0 mm |
| +15° | 26.4 mm | 16.8 mm |
| +20° | 36.1 mm | 20.8 mm |
| +25° | **46.1 mm** | **24.0 mm** |

At nominal, shoulder-to-wheel vertical distance is approximately **154.3 mm**.

These numbers are verification checkpoints. If the Fusion model does not reproduce them within normal CAD rounding error, stop that phase, find the geometry error, and fix it before continuing.

---

# 5. Passive knee spring mechanism

Use a **guided compression-spring cartridge spanning the knee**, packaged inside the bent-leg/knee envelope and hidden/protected by a removable cylindrical knee cover.

This is not claimed to be Beni's exact hidden internal linkage. It is the Prototype 1 implementation.

## Anchor geometry

Let K be the knee axis.

- Proximal/upper cartridge pivot radius from K: **Ru = 36 mm**
- Distal/lower cartridge pivot radius from K: **Rl = 54 mm**
- Included angle between K→pivot vectors at nominal: **110°**
- As the knee flexes by φ, included angle becomes approximately **110° - φ**

The assembly may be rotated as a whole around K to package it, but the radii and relative angle must remain unchanged.

### Cartridge geometry checkpoints

| Knee φ | Pivot eye-to-eye length | Spring moment arm about K |
|---:|---:|---:|
| -8° | 77.70 mm | 22.09 mm |
| 0° | 74.44 mm | 24.54 mm |
| +10° | 69.91 mm | 27.39 mm |
| +20° | 64.90 mm | 29.95 mm |
| +25° | 62.23 mm | 31.12 mm |

Extension-to-+25° cartridge stroke: **15.47 mm**.

This rising moment arm is deliberate. Do not "simplify" the anchors into geometry with a nearly constant or falling moment arm.

---

# 6. Spring target

Prototype target:

- Compression spring
- Rate: **~10.45 N/mm**
- Force at -8°: **~30 N**
- Force at nominal: **~64 N**
- Force at +25°: **~192 N**

Expected per-leg vertical ground capacity:

| Knee φ | Approx. ground force | Equivalent static load |
|---:|---:|---:|
| -8° | 8.3 N | 0.49 g |
| 0° | 17.2 N | 1.00 g |
| +5° | 23.1 N | 1.35 g |
| +10° | 29.4 N | 1.71 g |
| +15° | 36.2 N | 2.11 g |
| +20° | 43.6 N | 2.54 g |
| +25° | **51.5 N** | **3.00 g** |

The effective wheel rate is mildly progressive, approximately **0.71 to 0.80 N/mm** through useful compression.

### Starting physical spring envelope
Model a replaceable spring approximately:

- OD: **19 mm**
- Wire: **2.6 mm**
- Mean coil diameter: ~16.4 mm
- Free length: **~55 mm**
- Active coils: ~9.8
- Closed/ground ends preferred
- Central guide rod
- Target material for repeated jumping: **ASTM A877/A877M valve-spring-quality chrome-silicon**, preferably shot-peened/preset

A228 music wire is acceptable for early prototypes.

Do not use ordinary ASTM A401 as the preferred repeated-jump spring material; the current ASTM A401 scope explicitly says it is not intended for high-cycle fatigue applications.

Treat the spring specification as **replaceable/tunable**, not a permanently trapped part.

---

# 7. Knee construction

Preferred starting hardware:

- **10 mm steel knee axle**
- **2 × 6800-series sealed bearings, 10×19×5 mm**
- Double-shear printed/metal-supported joint geometry
- Metal spacers/washers as required
- No printed axle
- No plain printed rotating bearing surface

### Spring cartridge
Use:
- ~5 mm steel guide rod,
- sliding spring seat with low-friction polymer bushing,
- metal spring seats where concentrated loads occur,
- ~4 mm steel cartridge pivot pins/shoulder screws,
- removable preload shims rather than a bulky adjustment mechanism,
- removable cartridge without removing the shoulder motor.

The spring line of action sits approximately **22–31 mm from the knee axis** through the useful range. Preserve clearance between the spring envelope, bearing stack, links, and fasteners using real solid geometry.

### Stops
- Extension: compliant contact just before **-8°**, then a positive mechanical stop.
- Flexion bumper begins around **+20°**.
- Main spring design point: **+25°**.
- Metal-backed positive hard stop: **+27°**.
- Never use coil bind as the travel stop.
- Never use a thin printed tab as the final crash load path.

Provide a replaceable polyurethane/TPU-style bumper pocket. Exact bumper compound is a bench-test tuning item.

### Knee sensing
Add an absolute knee-angle sensor provision:
- coaxial diametric magnet,
- AS5048A / AS5047-class magnetic encoder or equivalent,
- sensor fixed to one side, magnet rotating with the other,
- protected strain-relieved cable path.

The passive knee angle is required for state estimation, spring-deflection estimation, simulation matching, and landing control.

---

# 8. Shoulder module

Use the supplied GIM6010-8 STEP as the dimensional source of truth.

Do not use the stale assumption of 9 N·m rated / 25 N·m peak as motor capability.

Current Steadywin published GIM6010-8 variants are roughly:
- 24 V version: 5 N·m rated, 11 N·m stall
- 48 V versions: 4.6–5.4 N·m rated, about 17.2–17.9 N·m stall

Exact variant/driver must be verified separately.

### Mechanical design rule
Proof-design the shoulder mount/output interface around **~25 N·m** as a structural screening load even if the current motor cannot continuously produce it.

Keep the proximal link close to the motor output bearing to reduce cantilever. Only add an outboard support bearing if the STEP geometry allows a clean, non-overconstrained implementation.

### 360° wiring
Prototype 1 requires a full ~370° physical joint range, not unlimited spinning.

Preferred order:
1. inspect STEP for usable central/hollow cable routing;
2. if unavailable, use a high-flex harness/service loop routed close to the axis;
3. model the cable envelope through -185° to +185°;
4. add strain relief on both sides.

Do not add a slip ring unless unlimited repeated multi-turn rotation becomes an actual requirement.

---

# 9. Wheel module

Use the supplied GIM4305-10 STEP as the dimensional source of truth.

- Wheel OD: **110 mm**
- Use a metal output hub/adapter where torque is transferred.
- Do not use a printed friction-fit shaft/hub interface.
- The motor and connector must remain removable after the robot is assembled.
- Route wheel-motor wiring across the passive knee with sufficient service loop for -8° to +27°.

The ~28 mm budget applies primarily to the structural leg/knee package; do not corrupt the motor mounting geometry merely to force the wheel motor itself inside an impossible width.

---

# 10. Materials and FDM rules

## PA-CF — preferred for load-bearing parts
Use PA-CF for:
- shoulder motor mounts,
- proximal links,
- distal links,
- knee clevis/housing,
- wheel motor structural mount,
- major chassis load paths.

## ABS — acceptable for noncritical parts
ABS is appropriate for:
- covers/fairings,
- electronics trays,
- cable guides,
- guards,
- fit-check prototypes,
- low-load chassis panels.

Do **not** default to ABS for the shoulder output structure, knee bearing housings, hard-stop structure, or highly loaded links when PA-CF is available.

## Metal where required
Use metal for:
- knee axle,
- cartridge pivot pins,
- motor output hubs,
- bearing sleeves/spacers as needed,
- final hard-stop pins/surfaces,
- any small feature carrying concentrated impact load.

## Printability
For every printed component:
- explicitly choose print orientation;
- prefer primary bending loads in the print plane;
- avoid trapped supports;
- avoid inaccessible horizontal cavities;
- avoid thin material around bearings/inserts;
- split a part if that materially improves printing, strength, or assembly;
- model support-removal access where internal support would otherwise be required.

For structural joints, prefer **through-bolts + locknuts** over heat-set inserts. Use heat-set inserts mainly for covers and repeatedly serviced low-load parts.

---

# 11. Structural load cases

Use these as screening cases, not as claims of exact landing physics.

1. **Static:** 17.2 N vertical per wheel.
2. **Main knee operating point:** ~51.5 N vertical per wheel at +25°.
3. **Structural crash/proof screen:** apply up to approximately **275 N at one wheel** (about 8 g × total robot mass) through realistic worst-case directions/poses.

Check:
- knee axle/bearing loads,
- link bending,
- shoulder mount,
- motor-output adapter,
- wheel-motor mount,
- hard-stop path.

For printed PA-CF parts, do not treat isotropic Fusion FEA as final proof. Use conservative material properties, inspect stress concentrations, and require bench load/drop tests before jumping.

---

# 12. Landing energy design

A 3.5 kg robot dropped 100 mm reaches approximately **1.4 m/s** before contact.

The passive knee alone should not be expected to absorb the entire landing while remaining compliant. The current two-knee spring system provides useful impact shaping but the shoulder must participate.

Design intent:

**passive knee compliance + active shoulder yielding/damping + progressive final bumper**

Do not:
- lock the shoulder mechanically during landing;
- make the main knee spring extremely stiff just to survive a drop;
- add an oil damper in Prototype 1 unless testing shows active damping is insufficient.

Keep provisions modular so a small physical damper can be added later if needed.

---

# 13. Serial Fusion workflow

Use real Fusion components, not a monolithic body.

Run these phases **serially**:

### Phase 1 — Reference audit
- Import both STEP motors as immutable reference components.
- Measure mounting patterns, pilot/registers, shafts/outputs, connector envelopes, body envelopes.
- Create a global parameter table.
- Verify measurements before proceeding.

### Phase 2 — Shoulder module
Design individually:
1. chassis motor interface,
2. shoulder mount,
3. output hub/adapter,
4. shaft/bearing support if used,
5. cable routing envelope.

Assemble and sweep -185° to +185° before proceeding.

### Phase 3 — Proximal link
Create as a separate printable component. Add real fastener interfaces and service access.

### Phase 4 — Knee bearing stack
Create axle, bearings, spacers, clevis/tongue geometry and hardware. Verify actual assembly order.

### Phase 5 — Distal link
Create as a separate component with knee and wheel-motor interfaces.

### Phase 6 — Spring cartridge
Build all cartridge parts individually:
- pivots,
- guide rod,
- moving seat,
- fixed seat,
- spring,
- preload shims,
- retainers.

Check the eye-to-eye checkpoint table at -8°, 0°, +10°, +20°, +25°.

### Phase 7 — Stops and encoder
Add extension stop, progressive flexion bumper, hard stop, encoder magnet/sensor and wiring.

### Phase 8 — Wheel module
Motor mount, hub, wheel envelope, fasteners and wiring.

### Phase 9 — Complete one-leg assembly
Only now assemble the full leg.

Verify all combinations of:
- shoulder -185° to +185°,
- knee -8°, 0°, +10°, +20°, +25°, +27°,
- full wheel envelope.

Do not duplicate the leg until this passes.

### Phase 10 — Second leg and chassis
Duplicate/adapt the validated leg and design the chassis around the proven modules.

### Phase 11 — Manufacturing/assembly audit
For every component verify:
- print orientation,
- support accessibility,
- bearing insertion,
- motor insertion/removal,
- screw-driver access,
- nut access,
- cable installation,
- spring replacement,
- disassembly sequence.

### Phase 12 — Red-team audit
Deliberately search for:
- collisions hidden in normal view,
- impossible fastener installation,
- captive nuts/bearings/springs,
- parts that cannot be inserted after neighboring parts exist,
- trapped support,
- cable pinch/twist,
- inaccessible motor connectors,
- hard stops that load weak printed tabs,
- insufficient bearing-seat wall thickness,
- duplicate/interfering solids.

Fix every failure and rerun the affected checks.

---

# 14. Required motion/configuration checks

Create named Fusion positions/configurations for:

1. **Nominal stand** — knee 0°, wheel below shoulder.
2. **Shoulder squat** — knee near 0°, shoulder rotated enough to lower body while wheel rolls; verify no body/wheel collision.
3. **Knee extension** — -8°.
4. **Knee 10° compression**.
5. **Knee 20° compression / bumper engagement**.
6. **Knee 25° design compression**.
7. **Knee 27° hard stop**.
8. **Jump-drive pose** — shoulder oriented so active rotation can drive wheel/downstream link into the ground.
9. **Self-righting sweep** — full shoulder sweep with realistic knee/wheel envelopes.

Important: a deep static knee-fold squat is **not** a required normal behavior. At +25°, the spring geometry corresponds to roughly 3 g vertical loading; that pose is mainly a dynamic preload/landing state.

---

# 15. Acceptance checklist

Do not declare completion until all are true:

- full 360° shoulder sweep is physically possible;
- shoulder wiring survives the full sweep;
- nominal wheel axis is directly below the shoulder;
- Fusion reproduces the knee kinematic checkpoint table;
- Fusion reproduces the spring eye-to-eye checkpoint table;
- passive knee is a real revolute joint with real spring hardware;
- spring cannot escape or coil-bind before hard stop;
- knee bearings/axle are physically assemblable;
- spring cartridge can be replaced;
- bumper and hard stop have real load paths;
- knee encoder physically fits and can be wired;
- wheel motor and connectors are removable;
- every screw has tool access;
- every nut/washer/spacer has an installation path;
- every printed part has an explicit viable print orientation;
- no inaccessible support is required;
- one-leg assembly passes all collision sweeps before duplication;
- complete robot passes all shoulder/knee collision combinations;
- PA-CF is used for primary load paths unless a documented reason justifies another material;
- structural proof cases have been reviewed;
- BOM and assembly sequence are complete.

---

# 16. Deliverables

The Fusion project must contain:

- clean named components,
- global parameter table,
- immutable motor references,
- individual manufacturable parts,
- shoulder subassembly,
- knee subassembly,
- wheel subassembly,
- validated single-leg assembly,
- complete two-leg robot,
- real fasteners/bearings/shafts/spacers,
- functional shoulder/knee/wheel joints,
- cable-routing envelopes,
- named motion-check positions,
- exploded view or explicit assembly sequence,
- BOM.

Also provide a short engineering note with:
- assumptions made,
- unresolved risks,
- exact motor variant still needing electrical verification,
- spring items requiring supplier confirmation,
- recommended print order,
- recommended static load tests,
- recommended low-energy drop tests before any powered jump.

---

# 17. Do not change these without demonstrating a failure

For Prototype 1, preserve:

- serial Beni-like morphology;
- active 360° shoulder;
- passive spring knee;
- L1 = L2 = 120 mm;
- ±50° nominal link geometry;
- -8° to +27° passive knee range;
- Ru 36 mm / Rl 54 mm / 110° nominal spring-anchor geometry;
- ~10.45 N/mm replaceable main spring target;
- late-travel progressive bumper;
- active shoulder damping as part of landing strategy;
- PA-CF for primary printed load paths;
- no active telescoping leg;
- no Ascento-style parallel linkage;
- no active knee;
- no slip ring unless unlimited multi-turn shoulder rotation is actually required.

---

# Research basis / known uncertainty

The following were checked when this guide was rewritten:

- Mondo Robotics Beni product/spec page:
  https://mondorobotics.com/
- Mondo's early/current prototype development:
  https://www.reddit.com/r/MondoRobotics/comments/1uh7l10/early_prototypes_vs_current_build_the_rd_process/
- Mondo's parallel-leg vs biped discussion:
  https://www.reddit.com/r/robotics/comments/1rd6gin/we_built_both_parallel_leg_and_bipedal_versions/
- Mondo's older parallel-leg prototype:
  https://www.reddit.com/r/MondoRobotics/comments/1rxuuyu/before_there_were_legs_there_was_this/
- Mondo RL/sim-to-real notes:
  https://www.reddit.com/r/MondoRobotics/comments/1szuepv/our_rl_journey_so_far_what_we_learned_what_broke/
- The Verge hands-on Beni description:
  https://www.theverge.com/gadgets/962538/mondo-robotics-beni-robot-dog-preview
- Ascento paper:
  https://arxiv.org/abs/2005.11435
- Steadywin GIM6010-8 official page:
  https://www.steadywin.cn/en/pd.jsp?fromColId=0&id=116
- Steadywin GIM4305-10 official product page:
  https://www.steadywin.cn/pd.jsp?id=9
- ASTM A877/A877M high-fatigue chrome-silicon spring wire:
  https://store.astm.org/a0877_a0877m-17.html
- ASTM A401/A401M current scope:
  https://store.astm.org/a0401_a0401m-24.html

**Known uncertainty:** no public teardown or engineering drawing found exposes Beni's exact internal spring-knee linkage. The active-shoulder + serial passive cylindrical-knee + driven-wheel morphology is evidence-backed. The specific two-pivot guided compression-spring cartridge in this guide is an engineered reconstruction selected because its kinematics, progressive wheel rate, package size, serviceability, and first-prototype manufacturability have been checked.
