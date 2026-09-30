# R2A print files — ABS single-leg integration article

Released 2026-09-27 from Fusion `Beni_R2A_SingleLeg` (geometry v3) by
[`r2a_release_fusion.py`](../r2a_release_fusion.py). Every file is bed-ready:
**import it unchanged — do not rotate, scale or mirror it**, and do not
compensate holes. Only left-hand parts exist; this is the left leg.

**Before buying anything, build the all-printed proof of concept**: it uses
these article parts unchanged with printed stand-ins for every purchased part
([`r2a_poc_stl/`](../r2a_poc_stl/README.md),
[POC guide](../docs/assembly/r2a_poc_guide.md)).

Scope (CLAUDE.md rule 7): ABS is for fit coupons, assembly, cable routing,
hand-driven kinematics and wheel-clear, current-limited commissioning under
self-weight. No torque-arm load, added mass, stall, ground contact, drop or
jump through these parts.

Release evidence: 37 dimensional contracts, the print audit of each bed pose,
the distal support-removal audit and the mesh fidelity of every file are in
[`evidence/r2a/2026-09-27_digital_gate/`](../evidence/r2a/2026-09-27_digital_gate/README.md).
Hashes are pinned in [`r2a_release_baseline.json`](../r2a_release_baseline.json)
and checked by `python3 verify_r2a_release.py`.

## Slicer profile

The tuned enclosed ABS profile used for the legacy article: **0.20 mm layers,
4 walls, 5 top and 5 bottom layers, 30 % infill.** No supports anywhere except
the five painted regions on the distal link. Do not drill, sand, file or
heat-fit a failed fit; record it and stop.

TPU plugs: TPU 95A, standing on an end face as exported, 100 % infill, no
supports.

## Print order

**Batch 1 — coupons first.** Nothing in batch 2 is worth printing until these
pass, because every new R2A fit is on them. Each coupon is cut by Fusion from
the released part B-Rep, so it prints the interface on the same build axis as
the part (rule 12).

| # | File | Qty | Material | On the bed | Tests |
|---:|---|---:|---|---|---|
| 1 | [`R2A_COUPON_Pin_Dowel_Ladder_ABS.stl`](R2A_COUPON_Pin_Dowel_Ladder_ABS.stl) | 1 | ABS | Flat plate, 64 × 44 mm | Ø5.05 / 5.10 / **5.15** / 5.20 / 5.25 clevis-pin passages in a 3.7 mm plate; Ø4.20 / **4.25** / 4.30 dowel holes in a 3.0 mm plate and as 7.0 mm-deep blind top-opening sockets. The notched corner marks the Ø5.05 / Ø4.20 end. Bold = the released value. |
| 2 | [`R2A_COUPON_Crank_Register_ABS.stl`](R2A_COUPON_Crank_Register_ABS.stl) | 1 | ABS | Output face down, 38.5 × 38.0 × 7.9 mm | The crank's output interface: three Ø4.15 factory-pin passages with Ø5.2 root reliefs, 6 × M3 clearance with Ø6.2 counterbores, 5.0 mm flange under the heads |
| 3 | [`R2A_COUPON_Crank_Clevis_ABS.stl`](R2A_COUPON_Crank_Clevis_ABS.stl) | 1 | ABS | Output face down, 32.0 × 31.3 × 16.3 mm | The crank ear: 8.4 mm ball gap, rod-end neck relief, Ø5.15 blind pin hole, two Ø4.25 cap-dowel sockets |
| 3a | [`R2A_Crank_Cap_L_ABS_OUTER_FACE_DOWN.stl`](R2A_Crank_Cap_L_ABS_OUTER_FACE_DOWN.stl) | **2** | ABS | Outer face down | One closes coupon 3; the other is the part |

**Batch 2 — the article, after batch 1 passes.**

| File | Qty | Material | On the bed | Supports | Bed footprint × height |
|---|---:|---|---|---|---|
| [`R2A_Prox_Inboard_L_ABS_Y59p5_DOWN.stl`](R2A_Prox_Inboard_L_ABS_Y59p5_DOWN.stl) | 1 | ABS | Inboard (hub) face, y 59.5 | None; four insert/plug ceilings bridge, one Ø17 bearing lip | 178.4 × 145.1 × 25.0 mm |
| [`R2A_Prox_Outboard_L_ABS_Y91p1_DOWN.stl`](R2A_Prox_Outboard_L_ABS_Y91p1_DOWN.stl) | 1 | ABS | Outboard (actuator-mount) face, y 91.1 | None; four ceilings bridge, one lip | 178.4 × 145.1 × 6.6 mm |
| [`R2A_Crank_L_ABS_OUTPUT_FACE_DOWN.stl`](R2A_Crank_L_ABS_OUTPUT_FACE_DOWN.stl) | 1 | ABS | Output (register) face | None; three 0.7 mm pin-relief lips | 59.9 × 49.3 × 16.3 mm |
| Crank cap (batch 1, item 3a) | — | | | | |
| [`R2A_Lever_Cap_L_ABS_OUTER_FACE_DOWN.stl`](R2A_Lever_Cap_L_ABS_OUTER_FACE_DOWN.stl) | 1 | ABS | Outer face | None | 26.1 × 30.1 × 3.7 mm |
| [`R2A_Distal_Link_L_ABS_Y59p5_DOWN.stl`](R2A_Distal_Link_L_ABS_Y59p5_DOWN.stl) | 1 | ABS | Inboard face, y 59.5 | **Selective**, below | 165.4 × 138.2 × 31.5 mm |
| [`R2A_Encoder_Arm_L_ABS_TOP_FACE_DOWN.stl`](R2A_Encoder_Arm_L_ABS_TOP_FACE_DOWN.stl) | 1 | ABS | Magnet (top) face | None; magnet-pocket ceiling bridges | 33.4 × 40.5 × 6.3 mm |
| [`R2A_Knee_Pin_Cap_L_ABS_OUTER_FACE_DOWN.stl`](R2A_Knee_Pin_Cap_L_ABS_OUTER_FACE_DOWN.stl) | 1 | ABS | Outer face | None; two counterbore ceilings bridge | 34.0 × 34.0 × 5.9 mm |
| [`R2A_Knee_Bumper_TPU95A_D6x4.stl`](R2A_Knee_Bumper_TPU95A_D6x4.stl) | **4** | TPU 95A | End face | None | Ø6 × 4.0 mm |

**On hold — do not print:** `R2A_Encoder_Bracket_L`. It is modelled around a
14 × 14 × 1.6 mm envelope because the AS5048A adapter-board outline is not in
the repository. Release needs the board's outline, hole pattern and
connector position from the owned board.

**Retired — do not print:** the legacy proximal link, distal link, spring caps,
cartridge eyes, guide bar, stop plate and pin keeper. R2A reuses the printed
PINREV2 shoulder hub, `Chassis_Shoulder_Plate_L`, `Shoulder_Cable_Cover_L`,
`RIG_Stand`, `RIG_Cable_Post_A`, wheel hub and no-tyre wheel shell unchanged.

### Distal link supports

Paint supports **only** under these five downward faces (heights above the
bed): the two knee-web undersides at 6.3 mm, the Ø16 knee-receiver annulus at
5.8 mm, the wheel-end underside at 5.0 mm, and the open-channel ceiling at
25.0 mm. Use **≥ 0.4 mm top and bottom Z distance and 0.6 mm XY distance**.
Block supports from every bore (Ø10.30 receiver, Ø5.15 lever pin, Ø4.25 dowel
sockets, Ø4.5 insert pockets), the Ø41.5 motor opening and the wheel-motor
mounting face. This is the policy of the legacy distal release that printed
and assembled; Fusion shows each region's envelope has a straight removal
path with zero interference (`release_audit.json`).

## Acceptance tests

By hand, without measuring, unless stated. Record each result as a dated
observation in `evidence/`. Stop at the first failure; a failed fit is a
re-release, never a rework.

**Coupon 1 — pin and dowel ladder.** Needs one Ø5 × 18 dowel pin (to buy) and
Ø4 × 10 dowels (owned).
- The Ø5 pin must pass the **Ø5.15** passage by hand with no force and no
  perceptible radial rock. The clevis pins float between cheek faces, so this
  is a free slip fit. Note the smallest station it passes.
- A Ø4 × 10 dowel must press into the **Ø4.25** plate hole and blind socket
  straight, by firm thumb or vice pressure, without whitening or splitting,
  and must not fall out when the coupon is inverted and shaken.
- If Ø5.15 or Ø4.25 fails, record which station passes and hold batch 2: the
  released parts carry Ø5.15 and Ø4.25.

**Coupon 2 — crank register.** Test on the new knee GIM6010-8 when it arrives.
Do not remove the accepted shoulder hub just to test a coupon.
- The coupon sits flat on the output face over the three factory pins by hand,
  with no rock and no rotational play you can feel.
- All six M3 × 10 start by hand and **clamp the coupon before any screw
  bottoms**: once snug it cannot be turned. The screw tips reach the floor of
  the 5 mm output holes in CAD (the same stack as the assembled shoulder hub),
  so a screw that stops turning while the coupon is still loose is a failure.
- It lifts off by hand once the screws are out.

**Coupon 3 — crank clevis**, with the second crank cap, two Ø4 × 10 dowels,
one purchased rod end and one Ø5 × 18 pin.
- Press the dowels into the coupon, fit the rod-end ball into the gap, press
  the cap onto the dowels, and slide the pin in from the cap side.
- The ball has slight end float (0.2 mm per side in CAD) and no binding. The
  rod end swivels through its full swing without its housing or neck touching
  an ear or the neck relief. The pin withdraws by hand.
- Hold batch 2 if the chosen rod end does not fit the modelled envelope in the
  [ordering guide](../procurement/r2a_ordering_guide.md) item 2.

**Batch 2 detached checks** (before inserts, before any stack):
- Each 6800-2RS seats squarely in its Ø19.15 seat by thumb pressure on the
  outer race with no perceptible rock: seat A in the inboard half, seat B in
  the outboard half. Run the steel Ø10 pin through each bearing separately.
- The steel Ø10 pin enters the distal Ø10.30 × 20.0 receiver by firm thumb
  pressure, withdraws by hand, and has no free spin or radial rock.
- The inboard half meets the shoulder hub's face by hand over the three
  Ø4 × 10 root dowels (Ø4.30 slip holes).
- Each Ø6 TPU plug presses to the bottom of its blind bore (flush with the
  inboard face on the inboard half, 1.6 mm below the outer face on the
  outboard half) and stands proud of its radial stop face.
- Lever and crank pins pass their cap and ear holes by hand; cap dowels press
  as on coupon 1.
- The two proximal halves meet at the wall tops (y 84.5) by hand with no rock,
  before any insert is installed.

**Heat-set inserts** (Voron-style M3 × 5 in Ø4.5 receivers, flush, 12 total):
two in the inboard half's inboard face (knee-pin cap), six in the inboard
half's wall tops (perimeter), two in the outboard half's outer face (encoder
bracket, even while the bracket is on hold) and two in the distal link's
outboard pads (encoder arm). Let each cool; reject a proud, tilted or loose
insert. No other R2A part takes inserts.

## Assembly status

**`CAD PATH VERIFIED`** — 33 of 33 insertion, tool and service paths in Fusion
([`assembly_paths.json`](../evidence/r2a/2026-09-27_digital_gate/assembly_paths.json)).
**Not yet physically rehearsed.** The sequence is the
[R2A assembly guide](../docs/assembly/r2a_assembly_guide.md); powered gates are
the [test traveller](../docs/assembly/r2a_test_traveller.md).
