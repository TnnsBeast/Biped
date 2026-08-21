# First print — actuator fit gates (ABS)

Print the four files in [`actuator_fit/`](actuator_fit/) now.  They are the
cheapest way to close the nominal STEP-to-real-hardware interfaces before a
full leg consumes a long print.  The Mode A cable anchor in [`mode_a/`](mode_a/)
is validated too, but it is not needed to pass the motor-fit gate.

## Batch 1: print now

| STL | Checks |
|---|---|
| `ABS_FIT_GIM6010_HOUSING.stl` | shoulder housing clearance and 8 × M3 PCD74 clocking |
| `ABS_FIT_GIM6010_OUTPUT.stl` | shoulder output M3 pattern and the three Ø4 locating pins |
| `ABS_FIT_GIM4305_HOUSING.stl` | wheel-motor driver-cover clearance and 6 × M2.5 pattern |
| `ABS_FIT_GIM4305_OUTPUT.stl` | wheel output M3 pattern and Ø37.3 × 0.8 register pocket |

These were built and exported from Fusion document
`Beni_Prototype1_TestGauges` through the Fusion MCP.  Fusion's exact B-Rep
validation and source dimensions are in
[`actuator_fit/fusion_manifest.json`](actuator_fit/fusion_manifest.json).
Independent binary-mesh inspection found one closed manifold shell per file,
zero open/non-manifold edges, and zero degenerate triangles.

## Slicer setup

- Material: the owner's normal, tuned **ABS** profile in an enclosure.
- No scaling and no hole compensation for the first pass.  The purpose is to
  measure the printer/material result, not hide it.
- 0.20 mm layers, 4 walls, 5 top and 5 bottom layers, 30% infill.
- Print every coupon exactly as exported: largest circular face on the bed.
- No supports.  Add a brim only if this ABS/printer combination normally warps.
- Keep the four parts labelled in the slicer or print them one at a time; the
  two housing rings are easy to confuse after removal.

## Test without calipers

Use the delivered actuator, its real screws and its real locating pins as the
go/no-go fixture.  Do not drill, file, sand, heat or force the coupon before the
first result is recorded.

1. Place the matching coupon on the interface by hand.  It must reach the
   mating face without rocking or being hammered.
2. Start two opposite screws with fingertips only.  They must both enter the
   threads without bending the coupon or pulling it sideways.
3. Check the remaining holes with loose screw shanks.  For the GIM6010 output,
   all three factory pins must enter together; do not tap them in.
4. Photograph the seated face and any obstruction.  Record whether the failure
   is the centre/register, bolt circle, pin circle, or hole clearance.
5. Remove the coupon.  A print that needed screw torque to seat is a **fail**,
   even if it eventually went flat.

A clean hand fit on all four coupons releases the corresponding ABS leg parts
for the next print.  It does not release PA-CF structural loading: repeat the
critical interface coupon in the eventual structural material first.

## Optional Batch 2: Mode A cable anchor

`mode_a/RIG_Cable_Anchor_ModeA.stl` is a 4 mm non-rotating strain-relief anchor
for the GIM6010 rear face.  Place either 41.0 × 15.45 mm broad face on the bed
(rotate 90° about X in the slicer), use the same ABS profile, and install with
2 × M3 × 8 SHCS plus washers.  It has 1 mm radial clearance around the STEP's
Ø57 driver cover and showed zero modeled interference in the complete rig.

Do not energise or backdrive either actuator as part of this fit test.  The
delivered connector pinouts are not fully verified, and the bench supply cannot
sink regenerative energy.
