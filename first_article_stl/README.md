# First print — actuator fit gates (ABS)

The four base files in [`actuator_fit/`](actuator_fit/) are the nominal
STEP-to-real-hardware gates printed on 2026-08-22.  Their results route the next
prints below.  The Mode A cable anchor in [`mode_a/`](mode_a/) is validated too,
but it is not needed to pass the motor-fit gate.

## Batch 1: printed and tested 2026-08-22

| STL | Checks |
|---|---|
| `ABS_FIT_GIM6010_HOUSING.stl` | shoulder housing clearance and 8 × M3 PCD74 clocking |
| `ABS_FIT_GIM6010_OUTPUT.stl` | shoulder output M3 pattern and the three Ø4 locating pins |
| `ABS_FIT_GIM4305_HOUSING.stl` | wheel-motor driver-cover clearance and 6 × M2.5 pattern |
| `ABS_FIT_GIM4305_OUTPUT.stl` | wheel output M3 pattern and Ø37.3 × 0.8 register pocket |

Owner-reported result: GIM6010 housing PASS; GIM6010 output pattern aligned but
its Ø4.05 printed pin bores did not hand-fit; the follow-up Ø4.15 pin-bore
coupon PASSed with a light press; GIM4305 housing PASSed with the real M2.5
screws; GIM4305 output PASS. The GIM4305 coupons are standalone, opposite-face
interface gauges and are not intended to nest. The failed GIM6010 output coupon
remains the evidence for the failed Ø4.05 result.

These were built and exported from Fusion document
`Beni_Prototype1_TestGauges` through the Fusion MCP.  Fusion's exact B-Rep
validation and source dimensions are in
[`actuator_fit/fusion_manifest.json`](actuator_fit/fusion_manifest.json).
Independent binary-mesh inspection found one closed manifold shell per file,
zero open/non-manifold edges, and zero degenerate triangles.

## Batch 1B: GIM6010 output-pin clearance diagnostic

The three generated files in
[`actuator_fit/gim6010_pin_trials/`](actuator_fit/gim6010_pin_trials/) retain the
validated three-pin pattern and change only the printed pin-bore diameter:
Ø4.15, Ø4.20 and Ø4.25 mm. The
[diagnostic README](actuator_fit/gim6010_pin_trials/README.md) gives the print
order, identification marks and pass rule. These are ABS calibration values,
not released PA-CF dimensions.

The Ø4.15 coupon passed on 2026-08-22, so stop there; the larger two trials are
not needed. Batch 2 is the actual unloaded ABS shoulder assembly in
[`assembly_dry_fit/`](assembly_dry_fit/). The original hub print proved the
motor interface but predated heat-set receiver design. Its corrected
`_PRINT_ORIENTED` replacement now includes six M4 insert pockets; the same
folder also contains bed-ready shoulder-plate and cable-cover articles.

## 2026-09-02 threaded-receiver release

[`heatset_receiver_release_manifest.json`](heatset_receiver_release_manifest.json)
is the machine-readable release record for the corrected shoulder hub, wheel
hub, shoulder plate, cable cover, and Mode A stand. Fusion B-Rep checks verify
the receiver diameters/depths and each listed STL is already transformed to its
controlled bed face. From the owner's reported progress, **only the shoulder
hub is a required reprint**; retain the printed Ø19.10 proximal link and both
installed bearings. After the PSM inserts arrive, use the Fusion-generated
[`insert_fit/`](insert_fit/) 5.5/5.6/5.7 mm ABS pocket ladder before either hub.

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

A clean hand fit releases the corresponding ABS leg interface for the next
print. The GIM6010 output requires the smallest passing Batch 1B bore before
that release. No ABS result transfers to PA-CF: repeat the critical interface
coupon immediately before the later two-leg structural prints.

## Optional Batch 2: Mode A cable anchor

`mode_a/RIG_Cable_Anchor_ModeA.stl` is a 4 mm non-rotating strain-relief anchor
for the GIM6010 rear face.  Place either 41.0 × 15.45 mm broad face on the bed
(rotate 90° about X in the slicer), use the same ABS profile, and install with
2 × M3 × 8 SHCS plus washers.  It has 1 mm radial clearance around the STEP's
Ø57 driver cover and showed zero modeled interference in the complete rig.

Do not energise or backdrive either actuator as part of this fit test.  The
delivered connector pinouts are not fully verified, and the bench supply cannot
sink regenerative energy.
