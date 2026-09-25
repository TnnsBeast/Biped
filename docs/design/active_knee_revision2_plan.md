# Active-Knee Revision 2 plan (R2A)

Status: **architecture direction selected; planning only**. No replacement CAD,
STL, motor order, belt order, or powered test is released by this document.

The name **R2A** distinguishes this architecture reset from the repository's
older `Beni_Prototype1` “revision 2,” which was a production-readiness revision
of the passive-knee model.

## Decision

Replace the passive compression-spring knee with a **remotely actuated rotary
knee**. Keep the knee motor near the body/shoulder and transmit torque down the
proximal link with a synchronous toothed belt. The leg then has three commanded
axes:

1. shoulder rotation;
2. knee rotation through the remote belt drive;
3. wheel rotation.

The existing loose spring, two cartridge eyes, guide bar and spring clevises are
not part of R2A. A replaceable end-of-travel bumper may protect the mechanism.
Any later energy-storage element must have its own constrained load path and
must follow the active-joint prototype; it is not a prerequisite for the first
R2A leg.

The architectural basis is the [September 25 teardown review](../../evidence/reference/2026-09-25_beni_teardown/README.md),
combined with the physical failure of the existing spring mechanism: the owner
observed curved compression, end twisting and lateral spring ejection, while the
guide was disengaged in the unloaded pose. The earlier
[fixed-axis spring cassette](knee_spring_redesign.md) is superseded before CAD
work because it preserves the wrong passive-joint premise.

## Target mechanical layout

```text
 body/chassis
    ├── shoulder actuator ───────────────> proximal link angle
    └── knee actuator near shoulder
             └── synchronous belt in proximal link
                      └── knee output pulley ──> distal link angle
 distal link ────────────────────────────────> wheel actuator
```

The preferred packaging study puts the shoulder and knee actuator axes on the
same shoulder axis, like the teardown. This is a packaging goal rather than a
requirement. The owned GIM6010-8 has no usable through-bore, so R2A must compare:

| Candidate | Reason to study | Main issue to resolve |
|---|---|---|
| Coaxial actuators on opposite sides of the shoulder | Short belt path entrance and closest match to the observed architecture | Chassis width, independent outputs, bearing reactions, wiring and assembly order |
| Axially stacked coaxial actuators | Compact in the side view | Likely excessive lateral stack with the owned actuator; no through-shaft shortcut is available |
| Body-mounted offset knee actuator driving a shoulder-axis jackshaft | Preserves low leg inertia when exact coaxial packaging is infeasible | Adds a first belt stage, bearings and backlash; every pulley and shaft must be off-the-shelf or printed |

R2A should select the simplest candidate that fits the real hardware and meets
the torque, speed, service and print constraints. It does not need to reproduce
the teardown's internal packaging exactly.

### Preliminary screen against the recorded CAD stack

The existing CAD-derived lateral datum already rules out treating a second
GIM6010-8 as an easy drop-in. The two shoulder motors occupy `|y| = 5…49 mm`
around the shoulder axes and leave only the recorded `8 mm` centre slot between
their driver covers. The supplied GIM6010-8 geometry is `44.0 mm` long and has a
solid centre with only a shallow blind recess. A same-size motor cannot occupy
the centre slot or pass an independent shaft through the existing shoulder
motor. Putting another GIM6010-8 outside each current motor adds its full nominal
length before plates, bearings or belt structure and would move the legs farther
outboard.

That makes the **body-mounted offset knee motor plus shoulder-axis jackshaft the
default first skeleton** with the present packaging. A compact coaxial knee
motor remains a valid comparison only if actuator selection finds a substantially
smaller part with adequate load capability. The legacy top-forward free box is
a possible offset-motor search region, but it was previously assigned to the
battery and must be re-scanned in Fusion for both sides, cooling, wiring and
service access. These are screening conclusions from recorded datums, not a
Fusion fit proof.

## Kinematic consequence of a body-fixed knee motor

If the upper belt pulley is driven by a motor fixed to the body while the belt
centres are carried by the proximal link, shoulder motion and knee-motor motion
are coupled. Define:

- `q_s`: proximal-link angle relative to the body;
- `q_k`: distal-link angle relative to the proximal link;
- `theta_km`: knee-motor pulley angle relative to the body;
- `G`: driven-pulley tooth count divided by drive-pulley tooth count.

For the simple open-belt case, the coordinate relationship is:

`theta_km - q_s = ± G q_k + datum`

The sign and datum depend on the final routing. This relationship must be
derived from the constrained Fusion mechanism and verified on the bench; it
must not be assumed from the sketch. A shoulder command therefore needs a
coordinated knee-motor command to hold knee angle. The controller should retain
an independent knee joint encoder during development so motor/joint disagreement
can detect belt slip, tooth skip, a loose pulley or a changed datum.

If the knee-motor stator rotates with the proximal link instead, the coordinate
mapping changes and the added motor mass becomes moving leg inertia. That option
requires a separate dynamics comparison.

## Mechanical work packages

### 1. Requirements and load cases

Freeze the R2A use cases before selecting a motor or ratio:

- standing and balancing range;
- crouch and extension range;
- desired jump and landing motion;
- allowable motor current and thermal duty;
- target robot mass after the added knee actuators;
- required knee torque, speed, mechanical power and impact load;
- service life and acceptable belt backlash.

Recompute the dynamics from the R2A CAD. The passive spring torque curve,
passive drop limits, existing URDF inertias and old jump explanation are not
valid for motor sizing.

### 2. Fusion architecture study

All inspection and model work goes through the Fusion MCP. Start from copies of
the current documents and keep the passive model as a historical baseline.

The first study must:

- measure the actual free space around the shoulder, proximal link and knee;
- place the delivered GIM6010-8 and GIM4305-10 reference geometry without
  altering their validated datums;
- compare the three motor layouts above;
- keep the existing shoulder, knee and wheel centres as the first comparison
  pose, while allowing them to change if the active mechanism requires it;
- sweep shoulder and knee coordinates independently and together;
- include belt spans, pulley flanges, bearings, fasteners, tools, guards,
  wiring, tension adjustment and removal paths;
- report whether one central belt or balanced side belts best controls shaft
  load and printed-link torsion.

No source-only geometry edit or local mesh inspection counts as a CAD result.

### 3. Actuator and reduction selection

Select the knee actuator only after the joint load cases exist. The current
wheel actuator remains required at the wheel; it is not available as the knee
actuator in a completed leg. The study may compare another owned-family motor
or a different off-the-shelf actuator, but must use traceable torque-speed,
voltage, encoder, mass, thermal and driver data.

Choose a standard synchronous-belt family and stocked pulley tooth counts. The
ratio must simultaneously satisfy knee torque, speed, motor operating range,
tooth engagement, wrap, belt tensile rating, backlash and package size. Record
the belt part number and printable service path before purchase. Structural
drive pulleys should be bought metal parts where an unmodified stocked part can
do the job; printed pulleys are limited to geometry and low-current proof unless
their load capacity is separately demonstrated.

### 4. Knee output stack

Redesign the knee as a belt-loaded rotary output rather than adding a pulley to
the current smooth-pin joint. The stack must provide:

- bearings sized for belt radial load plus leg reactions;
- positive torque transfer from the driven pulley to the distal link;
- axial retention independent of belt tension;
- a replaceable hard stop and compliant terminal bumper;
- an independent knee encoder and physical datum;
- belt/pulley removal without destroying the link;
- no threaded shank used as a bearing surface;
- no dependence on fastener pull-down to align printed parts.

The current Ø10 pin, 6800 bearings and distal receiver may be reused only if the
new load path and assembly audit prove them suitable. Their successful fit does
not establish a powered torque interface.

### 5. Proximal link and tensioning

The proximal link becomes a transmission housing. Its design must include a
guarded belt channel, access cover, debris exits that do not expose the belt to
the wheel, and a repeatable tension adjustment. Prefer a fixed motor and an
adjustable idler or cartridge so motor alignment stays tied to the shoulder
datum. The tensioner must be lockable, inspectable and reachable with the leg
assembled.

Check tooth engagement and belt tracking at every commanded pose. Belt tension
must not be used to correct pulley misalignment, and the guard must contain a
thrown belt without becoming a structural bearing.

### 6. Chassis, power and control changes

R2A adds one actuator per leg. Rework the power tree, fusing, CAN topology,
harness, thermal path, mass properties, URDF and controller around six total
actuators for the two-leg robot. The existing four-actuator electronics plan is
a legacy baseline until this is complete.

The control model must include the shoulder/knee transmission coupling, belt
ratio and sign, motor and joint encoder datums, current limits, joint limits and
fault handling. Jumping becomes a coordinated shoulder-and-knee trajectory;
landing becomes an active impedance/current-control problem with mechanical
stops as the final protection.

## Verification ladder

1. **Digital mechanism gate:** constrained Fusion joints produce the intended
   shoulder and knee coordinates without prescribed alignment tricks; all
   collisions, service paths and print orientations pass.
2. **Unpowered transmission gate:** one printed ABS leg, no wheel contact and no
   spring, moves through its released range by hand. The belt tracks, tension is
   repeatable, the knee encoder agrees with pulley motion and every fastener is
   serviceable.
3. **Detached drive gate:** run the knee actuator and transmission off the leg
   under a current limit. Verify direction, ratio, encoder agreement, stop logic
   and fault handling.
4. **Wheel-clear single-leg gate:** mount the complete ABS article to the Mode A
   stand, support its weight, keep the wheel clear and use current-limited slow
   motion. ABS remains a geometry, assembly and controls article.
5. **Structural gate:** repeat fit coupons for the structural material, rebuild
   the two-leg load model and release the PA-CF parts through the existing Fusion
   and mesh gates.
6. **Ground and jump gates:** only the structural build proceeds to ground
   contact, progressive loading and a separately defined low-energy jump ladder.
   No ABS jump or drop is authorized.

Any belt walk, tooth skip, pulley motion on its hub, bearing bind, encoder
disagreement, cracked print, stop bypass or unexpected current ends the test at
that gate.

## R2A concept-freeze deliverables

The architecture is ready to freeze only when the repository contains:

- a Fusion layout with the selected motor arrangement and complete service
  sequence;
- traceable knee load cases and actuator operating points;
- selected belt and pulley part numbers with ratio and wrap evidence;
- a reviewed knee bearing/shaft/torque-transfer stack;
- updated mass properties, URDF and shoulder/knee coordinate mapping;
- an updated power/CAN/harness plan for the added actuators;
- print-orientation and insert/fastener maps for the ABS article;
- a gate-by-gate test traveller with explicit current and motion limits;
- a revised BOM separating owned, reusable and new parts.

## Immediate next actions

1. Create a read-only Fusion measurement report of the current shoulder stack,
   proximal-link free space and knee stack.
2. Build three skeleton layouts: opposite-side coaxial, axially stacked, and
   offset motor with shoulder-axis jackshaft.
3. Derive R2A joint load cases and compare candidate actuator operating points.
4. Select the transmission architecture, then design the knee output stack and
   belt tensioning around stocked parts.
5. Update electronics, firmware and simulation only after the motor and ratio
   are selected.
6. Release one ABS unpowered transmission article before any powered assembly.

## Sources and inherited constraints

- [Beni teardown evidence](../../evidence/reference/2026-09-25_beni_teardown/README.md).
- [Physical spring failure](../../evidence/assembly/2026-09-24_spring_escape/README.md).
- [Manufacturing constraints](../../MANUFACTURING_CONSTRAINTS.md): printed and
  off-the-shelf parts only.
- [Assembly verification](../../ASSEMBLY_VERIFICATION.md): insertion, tool,
  wiring and service paths are release requirements.
- [Delivered actuator evidence](../../evidence/actuators/2026-08-20_received/README.md).
- [Motor interface and lateral-stack datum](../../beni_prototype1_design_record.md),
  §§2–3. These are legacy geometry inputs, not an endorsement of the passive
  architecture.
