# Active-Knee Revision 2 plan (R2A)

Status: **concept selected 2026-09-27; planning only.** No R2A CAD, STL,
purchase or powered test is released by this document. R2A work lives on the
`r2a-active-knee` branch. Every mechanism, load and capability figure below is
printed by [`r2a_calc.py`](../../r2a_calc.py). Rerun the script rather than
editing a figure here, and replace its marked assumptions with Fusion geometry
at the digital gate.

The name **R2A** distinguishes this architecture reset from the repository's
older `Beni_Prototype1` “revision 2,” which was a production-readiness revision
of the passive-knee model.

## 1. Decision

On 2026-09-27 the owner directed that R2A copy the knee mechanics seen in the
[Beni teardown](../../evidence/reference/2026-09-25_beni_teardown/README.md),
reuse the owned actuators and electronics, and add one actuator per leg.

- **Knee:** a second **GIM6010-8** rides on the proximal-link root, coaxial
  with the shoulder axis, with its output facing inboard. A crank on its output
  turns inside the link. A rod-end pushrod runs down the former spring channel
  to a lever on the distal link behind the knee. The result is a four-bar whose
  ground link is the proximal link itself.
- **Shoulder:** unchanged. The owned GIM6010-8 drives the leg directly through
  the existing plate and printed output hub.
- **Wheel:** unchanged. The owned GIM4305-10 and the wheel module stay as they
  are.

Each leg therefore has three commanded axes: shoulder, knee crank and wheel.
The loose spring, cartridge eyes, guide bar and spring clevises are not part of
R2A.

## 2. What is copied from Beni, and what is not

| Beni (frame review) | R2A | Why |
|---|---|---|
| Hip-coaxial crank inside the thigh root, link along the thigh, lever on the shin behind the knee axle | **Copied** | The knee motor sits on the shoulder axis, so its weight adds no static shoulder torque and little leg inertia. The drive is stiff and slip-free, and it needs no tensioner. |
| Knee motor carried on the hip assembly (best-supported reading) | **Copied**: the knee actuator stator bolts to the proximal link | The knee coordinate is referenced to the proximal link, so there is no shoulder/knee coupling term. The knee reaction torque stays inside the leg. |
| Hip driven by an offset body motor through a short 2M belt to a large hip ring | **Not copied** | The owned GIM6010-8 already has an 8:1 planetary and drives the shoulder directly. A belt stage would add a ring pulley, a large bearing, a tensioner and backlash to a joint that does not need them. |
| Pancake motor inboard of the main hip bearing | **Not possible** | The GIM6010-8 output is solid ([design record §2.1](../../beni_prototype1_design_record.md)), so nothing can pass through the shoulder axis. The knee actuator goes outboard of the link root instead. |
| Wheel drive in the shin-end housing; wheel cable through the knee window | Wheel module unchanged; cable crosses the knee on the shin side | The existing wheel interface is kept. |

The Beni frames do not settle which of its two hip drives turns the knee crank.
That question does not affect R2A, because R2A's knee crank is driven by its
own actuator on the proximal link.

## 3. Mechanism

![R2A knee linkage schematic](r2a_knee_linkage.png)

The schematic is drawn by `python3 r2a_calc.py --plot`; it is not CAD. Frame:
the shoulder axis S and knee axis K lie on the proximal link, and α is the
interior knee angle (legacy φ = 80° − α).

| Item | Value |
|---|---|
| Crank, shoulder axis → crank pin | **32 mm** |
| Pushrod, pin to pin | **120 mm** (equal to L1) |
| Lever, knee axis → lever pin | **30 mm** |
| Lever position on the distal link | +168° from the distal-link direction: 12° short of straight through the knee |
| Working range | α = **51°** (flexion stop) … **150°** (extension stop); shoulder–axle 103.3 … 231.8 mm |
| Leg-length stroke | **128.5 mm**; the legacy passive 0 → +25° stroke was 46.1 mm |
| Crank travel | 94.4° for 103° of knee, including 2° overtravel at each stop |
| Knee-to-crank ratio N = dθc/dα | 0.866 at the stops … 0.937 mid-range |
| Transmission angle μ | ≥ 40.4° over the working range; 38.5° at full overtravel |
| Crank margin from toggle | 42.8° |
| Rod clearance to the Ø22 distal knee boss | 3.2 mm |
| Tyre to the wall around the crank sweep | 46.8 mm |

Linkage map for firmware and the Fusion check. θc is measured from the
shoulder→knee line, positive toward the side away from the distal link:

| α | θc | N | μ | Crank torque to stand, 4.429 kg robot | Rod force at 1.5 × stall |
|---:|---:|---:|---:|---:|---:|
| 51° | 43.1° | 0.866 | 40.4° | 2.86 N·m | 735 N |
| 65° | 55.6° | 0.909 | 54.2° | 2.55 N·m | 616 N |
| 80° | 69.4° | 0.929 | 69.0° | 2.26 N·m | 547 N |
| 100° | 88.1° | 0.937 | 89.0° | 1.88 N·m | 516 N |
| 120° | 106.8° | 0.931 | 71.0° | 1.47 N·m | 542 N |
| 140° | 125.2° | 0.903 | 50.8° | 1.04 N·m | 641 N |
| 150° | 134.1° | 0.870 | 40.6° | 0.82 N·m | 735 N |

Design reasoning:

1. **Flexion stop.** The tyre reaches the parts on the shoulder axis before
   anything else. The outboard cheek that holds the actuator's 8 × M3 on Ø74 PCD
   needs R42.0, and the tyre shares 5 mm of its Y band. Leaving 5 mm of
   clearance gives d ≥ 102.0 mm, so α ≥ 50.30°; the stop is at 51°. The tyre
   against the link underside would allow 35.7°, so it does not govern.
2. **Extension stop.** It keeps the leg 30° from straight, so the knee retains
   moment arm and stays away from the straight-leg singularity.
3. **No useful reduction is available.** The classical 40° transmission-angle
   floor across roughly 100° of knee travel leaves almost no room for a variable
   ratio.
   - All 434 feasible geometries out of 222,794 searched are near-parallelograms.
   - The idealised push-off is flat across them, at 143–144 mm CoM rise.
   - Designs with N up to 2.2 exist but roughly double the rod force for no gain.

   The knee actuator must therefore supply roughly the full knee torque, and
   that sets its class (§5).
4. **Selection.** Among designs within 3% of the best push-off, the pin
   envelope is limited to 40 mm from the link line, and the lowest rod force
   wins.
5. **The rod is in tension whenever the leg carries weight.** Standing,
   push-off and landing all load it in tension. Only flexion torque, such as
   retracting the wheel, compresses it. An M5 steel rod over 120 mm has an Euler
   load of 1965 N against the 761 N design force, a factor of 2.58.
6. **Two-force member.** With spherical rod ends at both ends the pushrod
   carries only axial load. It tolerates small misalignment and puts no bending
   into the printed crank or lever. The crank and lever clevises are coplanar on
   the legacy cartridge plane, y = 74.5.
7. **Impact path.** Knee stops carry impacts directly between the proximal and
   distal links. The linkage sees at most the actuator's current-limited
   torque.

## 4. Lateral stack (left leg)

Datums inboard of y = 89.5 are unchanged from
[design record §3](../../beni_prototype1_design_record.md).

| y (mm) | Feature |
|---:|---|
| 5 … 59.5 | **Unchanged:** shoulder GIM6010-8, `Chassis_Shoulder_Plate_L`, printed `Shoulder_Output_Hub_L` with 6 × Kadriick M4 × 8 inserts on Ø44 PCD |
| 58.7 … 64.5 | Proximal-link **inboard half**, cheek at 59.5 … 64.5. It bolts to the hub with the existing 6 × M4 × 10. Knee bearing A stays at 58.7 … 63.7. |
| 64.5 … 84.5 | **Channel** (the former spring channel). The crank clevis, pushrod and lever clevis share the centre plane y = 74.5. The distal knee boss Ø22 spans 65 … 84. |
| 80 … 86 | Crank hub on the knee-actuator output face at y 86.0. It uses 3 × Ø4 × 10 dowels and 6 × M3, the shoulder-hub interface mirrored. |
| 84.5 … 90.3 | Proximal-link **outboard half**, cheek at 84.5 … 89.5. The knee-actuator mount face is at 89.5: 8 × M3 on Ø74 PCD, screwed from the channel side into the actuator's front threads. Knee bearing B stays at 85.3 … 90.3. |
| 90.5 … 114.5 | Knee-actuator Ø80 housing, on the shoulder axis |
| 115.5 … 126.5 | Knee-actuator Ø57 driver cover and cable exit |
| 59.5 … 104.5 | **Unchanged** wheel module: distal wheel-end plate, GIM4305-10, rim/tyre, hub |

- **Track.** The track across the knee actuators is **253.0 mm**, against the
  legacy outer width of 209.0 mm.
- **Knee encoder.** The AS5048A and its magnet carrier stay on the outboard end
  of the knee pin, in their legacy stack. The knee actuator is 120 mm away at
  the shoulder, so the two do not interact.
- **Crank overhang.** The crank is supported only by the actuator's output
  bearing. The rod plane is 11.5 mm inboard of the output face, which puts an
  **8.7 N·m** moment on that bearing at the design rod force.

## 5. Knee actuator: a second GIM6010-8

Candidate data and the rejected options are kept in the
[trade study](active_knee_actuator_trade_study.md).

**Requirement.** Standing at α = 80° needs 2.00 N·m at the knee for the upper
mass estimate of 4.429 kg. After the 0.929 ratio that is 2.26 N·m at the crank,
or 4.8 A: 46% of the 10.5 A rated current. For push-off and landing, a leg force
equal to the whole robot's weight at the crouch needs about 4.6 N·m. The
actuator must also run on the 20 V bench bus (blocker B1).

**Why the GIM6010-8.**
- **Torque.** At the knee, standing uses 40% of its rated torque; stall is
  11 N·m.
- **Bus.** It runs on the 20 V bus that the owned unit already uses.
- **Protocol.** It speaks the same ODrive-CANSimple protocol as the shoulder,
  so it uses the same firmware and the same Teensy bus.
- **Interfaces.** It has the same housing mount (8 × M3 on Ø74) and output
  (6 × M3 on Ø25, plus 3 × Ø4 pins). The printed plate, hub, dowel and insert
  designs, and every coupon they passed, carry over.
- **Spares.** There is one actuator family to stock.

**What it costs.**
- **Mass.** It adds 388 g bare, or 500 g by the brief's figure (conflict C4
  unresolved). R2A two-leg mass becomes 4.205–4.429 kg.
- **Size.** The Ø80 housing on the shoulder axis sets the 253 mm track and the
  51° flexion stop.
- **Price.** No price is recorded in the repository; confirm it at order.

**Rejected candidates.**
- **RobStride 05 and EduLite 05:** standing would use 111–125% of their rated
  torque.
- **RobStride 00, 01 and 02:** each has the torque but needs at least 24 V, uses
  a different CAN protocol and a new mechanical interface. The RobStride 00
  remains the fallback if knee mass must drop after B1 allows a bus of 24 V or
  more.

**Capability** is idealised: legs are massless, and the torque-speed line uses
420 rpm at 24 V scaled to the bus voltage.
- **Push-off:** 130 mm CoM rise at 4.429 kg, 20 V and a 4.8 N·m cap; 199 mm at
  4.205 kg, 22.2 V and 9.4 N·m.
- **Landing:** holding 4.8 N·m from α = 140° to the stop absorbs a 179 mm free
  drop.

These are upper bounds for planning the load campaign. They are not a jump
rating, and no ABS jump or drop is authorised.

**Purchase.** Buy **one** unit for the single-leg article. The design is sized
to its STEP envelope, so the order does not have to wait for anything except
confirming price and lead time. Buy the two-leg units only after the single-leg
gates in §10 pass.

## 6. Reuse and new parts: single-leg article

| Item | Status | R2A use |
|---|---|---|
| GIM6010-8, shoulder | Owned | Unchanged |
| GIM4305-10, wheel | Owned | Unchanged |
| Teensy 4.1; 2 × Adafruit CAN Pal | Owned | Bus A: shoulder and knee GIM6010-8. Bus B: wheel. |
| AS5048A kit, BNO085, bench PSU at 20 V, WAGO distribution | Owned | Knee joint encoder, IMU, supply |
| `Chassis_Shoulder_Plate_L` (Ø4.5 M3 revision), `Shoulder_Output_Hub_L`, `RIG_Stand` | Printed / owned designs | Unchanged; re-run the stand load set for the added outboard mass |
| Ø10 × 35 knee pins, 6800-2RS pair, Ø10.30 × 20.0 distal receiver | Owned / proven fit | Knee stack unchanged in position |
| Wheel hub, rim/tyre | Printed | Unchanged; the rim keeps its existing printability hold |
| M3 Voron inserts (Ø4.5), Kadriick M4 × 8 (Ø5.3), M3 × 8, M4 × 10 | Owned / proven | Link-half joint, actuator mounts, hub |
| **Proximal-link inboard and outboard halves** | New print | Box-section link, actuator mount, crank and lever access windows |
| **Crank** | New print | Hub on the knee-actuator output, tip clevis for the upper rod end |
| **Distal link with integral lever** | New print | Legacy knee boss and wheel end, plus the lever clevis |
| Knee stops and TPU bumpers | New print, plus the washer column | Positive stops at 51° and 150° |
| **GIM6010-8, knee** | **Buy 1** | Knee actuator |
| 2 × M5 female spherical rod ends | Buy | Static radial rating ≥ 1521 N. Prefer one right-hand and one left-hand thread so length can be trimmed in place. |
| M5 steel threaded rod, cut to length; 2 × M5 jam nuts | Buy | Pushrod, 120.0 mm pin to pin |
| 2 × Ø5-shoulder screws (M4 thread), nylon-insert nuts, washers | Buy | Clevis pins; the smooth shoulder carries each rod-end ball, never a thread |
| Third CAN Pal | Optional | Only if bus A must stay at 500 kbit at 1 kHz |
| Legacy spring, cartridge eyes, guide rod, spring caps, cartridge pins; legacy proximal and distal prints | Retired | Evidence only |

## 7. Assembly and service sequence (concept; not yet `CAD PATH VERIFIED`)

On the bench, with every joint open:

1. Knee actuator to the outboard half: 8 × M3 × 8 from the channel side into
   the actuator's front threads. This is the same joint as the shoulder plate.
2. Crank to the actuator output: 3 × Ø4 × 10 dowels and 6 × M3 from the
   channel side.
3. Pushrod: set 120.0 mm pin to pin on a printed jig, then fit the upper rod
   end into the crank clevis on a Ø5 shoulder screw.
4. Distal link: fit the lower rod end into the lever clevis.

On the Mode A stand:

5. Inboard half to `Shoulder_Output_Hub_L`: 6 × M4 × 10 from the channel side.
6. Offer the outboard module (actuator, crank, rod and distal link) to the
   inboard half. Fit perimeter M3 screws from outboard into Ø4.5 inserts in the
   inboard half.
7. Insert the knee pin from outboard through bearing B, the distal receiver and
   bearing A, then fit the magnet carrier and the AS5048A bracket.
8. Fit the wheel module as on the legacy leg.
9. Harness. The wheel cable runs in a shin-side duct walled off from the rod
   and crosses the knee on the shin side. The knee-actuator cable leaves from
   its driver cover. Both exit the root in the external service loop; the rig
   limits the shoulder to ±120° in software ([electronics/02](../../electronics/02_harness_and_routing.md)).

**Service.** Pull the knee pin and the perimeter screws, and the knee-drive
module lifts off outboard with everything attached. Access windows over both
clevis pins let the rod come out without splitting the link.

**Rules that still apply.** No screw may pull a mismatched print into place.
Every screw must have a straight driver path before the halves close. Every
bearing seats in a face printed normal to its axis.

**Known sweep conflict to resolve at the digital gate.** Both screw sets that
install from the channel side leave their heads inside the crank's sweep band:

- the six M4 hub-screw heads, on the inboard cheek at R22 (y 64.5 … about
  68.5), against the crank's inboard clevis ear (y 66.5 … 70.5 at R24 … 40);
- the eight M3 actuator-mount heads, on the outboard cheek's channel face at
  R37 (about y 81.5 … 84.5), against the crank arm.

The options are:

- (a) low-head screws counterbored flush, with the cheek thickened as needed;
- (b) hold the knee actuator by its rear threads from an outboard cup. This
  leaves the channel face clean and grows the root to about R43, which still
  gives the 51° stop.

Fusion must show the chosen option clear through the full crank sweep.

## 8. Printing

- **Proximal-link halves** print cheek-down. The bearing seats, knee-pin bore,
  actuator bore and clevis-pin holes are then normal to the bed, as on the
  passing face-flat proximal link and the 6800 bore coupon. The open channel
  side faces up, so there is no internal support.
- **Crank** prints flat, with its dowel and screw holes normal to the bed, as
  on the printed shoulder hub.
- **Distal link** prints as the legacy face-flat part, with the lever clevis
  holes normal to the bed.
- **Fits that already have coupons:** Ø4.5 M3 and Ø5.3 M4 insert receivers,
  the Ø19.10 6800 bore, the Ø10.30 knee receiver and the shoulder-hub dowel
  fit.
- **Fits that need new coupons:** Ø5 shoulder-screw holes in the clevis cheeks,
  rod-end side clearance, and the crank-to-output register.
- **Materials.** ABS is for fit, assembly, hand motion and wheel-clear,
  current-limited commissioning only (CLAUDE.md rule 7). The structural build
  is PA-CF, with the coupons repeated. At the design rod force, a Ø5 pin in
  double shear runs at 19.4 MPa, and bearing on two 4 mm cheeks is 19.0 MPa,
  against 84–102 MPa for PA-CF in XY.
- Every part is released through the CLAUDE.md rule 12 orientation, overhang
  and support audit.

## 9. Electronics and firmware

- **Bus A** (Teensy CAN1 on a CAN Pal): shoulder GIM6010-8 as node 0 and knee
  GIM6010-8 as node 1, both ODrive CANSimple.
  - Before connecting, change the new unit's node ID from its default of 0.
  - At 1 Mbit, two nodes with command and reply at 1 kHz load the bus to 46.8%
    typical / 54.0% worst.
  - At 500 kbit the same traffic fails (93.6% / 108.0%). Either run 1 Mbit or
    drop the loop to 500 Hz.
- **Bus B:** wheel SDC101, unchanged.
- **Knee encoder.** The AS5048A on the knee pin gives absolute knee angle and
  checks the linkage map. The GIM6010-8 encoder is mono-turn
  ([electronics/03 §1.1](../../electronics/03_compute_and_can.md)); confirm
  whether it reads the rotor or the output. If it reads the rotor, the output
  angle is ambiguous at power-up, and the AS5048A supplies the absolute
  reference.
- **Knee command:** θc = f(α) from the §3 map, to be replaced by the
  Fusion-measured map. There is no shoulder term.
- **Power and regen.**
  - On the rig the knee carries only the leg's own weight.
  - On the two-leg robot, standing draws 4.8 A per knee, about 9.7 W of copper
    loss (phase R is still unverified).
  - The brake chopper is deferred, so no powered actuator may be backdriven by
    hand.
- **Two-leg harness.** The legacy four-conductor clock-spring plan carries one
  CAN pair. The knee adds a second protocol-compatible node per leg; revise the
  harness under B7 before the two-leg build.

## 10. Verification ladder

1. **Digital gate.** In a separate R2A copy of `Beni_SingleLegRig`, build the
   §3 linkage.
   - Sweep α from 49° to 152° with the shoulder moving independently.
   - Confirm the 5 mm tyre and 2 mm rod clearances, every assembly path, tool
     access and cable path, and every print orientation.
   - Replace the envelope assumptions in `r2a_calc.py` with modelled geometry
     and rerun it.
2. **Unpowered linkage gate.** The ABS article on the Mode A stand, with the
   actuators disconnected, is moved by hand through its range. The AS5048A must
   match the linkage map with no bind, and the stops must engage before the
   overtravel limit.
3. **Detached drive gate.** Run the knee actuator, crank and rod off the leg
   under a current limit. Verify direction, map, encoder agreement, stop logic
   and fault handling.
4. **Wheel-clear single-leg gate.** Run on the Mode A stand, weight supported,
   wheel clear, slow and current-limited.
5. **Structural gate.** Print PA-CF parts after repeating the coupons, and
   rebuild the two-leg load model.
6. **Ground and jump gates.** Structural two-leg build only, under a separately
   defined low-energy ladder.

Any bind, rod-end play beyond its specification, cracked print, stop bypass,
encoder disagreement or unexpected current ends the test at that gate.

## 11. Rejected alternatives

| Alternative | Why it lost |
|---|---|
| Synchronous belt down the proximal link (the 2026-09-25 plan) | It needs a tensioner, a guard, two pulley shafts and a slip-detecting encoder. Printed pulleys are load-limited. Its ratio buys nothing, because the knee actuator must be 5 N·m-class anyway. Beni does not use it. |
| Beni's exact hip: offset body motor, belt to a hip ring, pancake knee motor inboard | It would retire the proven shoulder stack, and it adds a large bearing and a belt stage to a joint the owned GIM6010-8 already drives directly. |
| Body-fixed knee actuator with a shoulder-axis jackshaft | The GIM6010-8 output is solid, so a shaft would have to come from outboard, across the leg's sweep. The knee reaction would load the body and couple the shoulder and knee coordinates. |
| Knee actuator at the knee or on the distal link | It moves about 0.4 kg away from the shoulder axis, adding shoulder gravity torque and leg inertia, and it widens the knee. |
| Knee actuator part-way along the proximal link | It adds m·r² leg inertia and static shoulder torque for no packaging gain. |
| Strongly variable-ratio four-bar | With about 100° of travel under the μ ≥ 40° rule, ratios up to 2.2 cost 1229–1579 N of rod force for no push-off gain. |
| RobStride 05 / EduLite 05 | Standing would use 111–125% of rated torque. |
| RobStride 00 / 01 / 02 | They need at least 24 V, a new protocol and a new interface. The RobStride 00 is the fallback if mass must drop after B1 allows a higher bus voltage. |
| Hobby servo, cable drive, printed reducer, spring latch | Unchanged from the [trade study](active_knee_actuator_trade_study.md). |

## 12. Open items

- Replace every `ASSUMPTION` in `r2a_calc.py` with Fusion geometry: the R8
  rod-end and R4.5 jam-nut envelopes, the root wall, and the 60 g per leg
  linkage-mass allowance.
- Measure mass properties and regenerate the URDF; resolve C4, the actuator
  mass conflict.
- **Knee stops.** The 275 N proof screen at the flexion stop gives 851 N at a
  R35 stop, and actuator stall into that stop gives 272 N. Adapt the legacy
  washer-column stop ([rig design record §8](../../beni_single_leg_rig_design_record.md)).
- Find where the GIM6010-8 encoder reads (rotor or output); this decides homing.
- Check the 8.7 N·m crank-overhang moment against the actuator's output bearing.
  The shoulder unit carries the whole leg on the same bearing, but no rating is
  recorded.
- Resolve the crank-sweep conflict with the channel-side M4 and M3 screw heads
  (§7).
- Open the proximal-link box on the lever side of the knee, so the lever sweep
  (R30 plus the rod-end eye) runs clear of the box walls. The knee bearings stay
  in the legacy arm positions.
- Re-run the `RIG_Stand` load set with the added outboard mass.
- Revise the two-leg harness across the shoulder (B7).
- Confirm the GIM6010-8 price and lead time.

## 13. Concept-freeze deliverables

The architecture is ready to freeze when the branch contains:

- the Fusion R2A skeleton, with the measured linkage map and complete service
  sequence;
- `r2a_calc.py` rerun with its assumptions replaced by modelled geometry;
- the knee stop and bumper design;
- selected rod-end, rod and pin part numbers checked against the §6
  requirements;
- updated mass properties, URDF and linkage map in firmware;
- an updated power, CAN and harness plan for three actuators per leg;
- print-orientation and insert/fastener maps for the ABS article;
- a gate-by-gate test traveller with explicit current and motion limits.

## Sources and inherited constraints

- [Beni teardown evidence](../../evidence/reference/2026-09-25_beni_teardown/README.md)
- [Physical spring failure](../../evidence/assembly/2026-09-24_spring_escape/README.md)
- [Manufacturing constraints](../../MANUFACTURING_CONSTRAINTS.md): printed and
  off-the-shelf parts only.
- [Assembly verification](../../ASSEMBLY_VERIFICATION.md): insertion, tool,
  wiring and service paths are release requirements.
- [Delivered actuator evidence](../../evidence/actuators/2026-08-20_received/README.md)
- [Motor interface and lateral-stack datum](../../beni_prototype1_design_record.md),
  §§2–3: legacy geometry inputs, unchanged inboard of y = 89.5.
