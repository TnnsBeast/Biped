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
not needed. Batch 2 is the unloaded ABS shoulder assembly in
[`assembly_dry_fit/`](assembly_dry_fit/). The original hub print proved the
motor interface but predated heat-set receiver design. Its replacement now
retains Ø4.15 and uses the owner-passed Ø5.3 M4 × 8 receivers. The owner has
printed it and successfully installed its inserts. The corrected proximal link
is printed and the owner confirmed all six hub screw seats on September 7.
The same folder contains
bed-ready shoulder-plate and cable-cover articles.

## 2026-09-04 owned-insert release

The owner confirmed the largest M4 × 8 ladder station, Ø5.3, passed all
installation and cooled-retention checks. Fusion incorporated it in both
saved documents. The two hubs and cable cover retain bed-ready ABS files in the
[receiver manifest](heatset_receiver_release_manifest.json). On September 14,
the owner selected Ø4.5 on the dedicated M3 ladder; the manifest, shoulder
plate, proximal link and stand exports now reflect that result.

The owner accepted the corrected hub's insert installation on 2026-09-05.
The **access-fixed Ø19.15 proximal link is printed with six-screw seating accepted**; use the final
[README print queue](../README.md#current-print--ordered-pin-unpowered-abs-mechanical-article). Two head
paths and one incomplete seat were corrected. The front cable post also now
mounts outside the cover. The final tyre-compatible wheel rim retains its
printability hold; the later no-tyre mechanical-test shell is separate.
[Current audit and acceptance](../evidence/assembly/2026-09-05_access_fix/).

## 2026-09-06 supported knee mock-up

The [temporary pin and provisional distal link](knee_mockup/) are printed and
provisionally assembled by owner report on September 7. Both spring caps are
also printed, with both spring ends seating flat uncompressed. Supported knee
movement and pin removal pass. [Photo and physical acceptance scope](../evidence/assembly/2026-09-07_owner_mockup/).
On September 15, the owner inserted a received metal pin into that provisional
shin. Its nominal Ø10 bore seized the pin, and the shin was broken to recover
it. The earlier loose Ø9.7 printed-pin result remains evidence, but the shin is
destroyed and must not be reprinted for another steel-pin trial. [Steel-pin
result](../evidence/knee_fit/2026-09-15_steel_pin_provisional_shin/).
The traveller remains scoped to two detached links supported on the bench;
the caps check the ends of the owned spring off the leg. Follow that batch's specific support
policy: **the distal mock-up needs selective supports**, while the pin and
caps print without supports. No main spring or motors attach to this mock-up.

## 2026-09-16 steel knee-pin bore result — Ø10.30 ABS selected

One received metal pin seated through both installed bearings and seized in the
provisional shin's nominal Ø10 ABS bore. The provisional shin was broken to
recover it. The owner printed the initial Ø10.05–Ø10.25 ladder
and found nominal Ø10.25 gives the intended firm-thumb fit through its 19.0 mm
station. The owner selected nominal Ø10.30, one 0.05 mm step above the physical
result, while the receiver was expected to span 21.6 mm. Fusion's final service
audit found that copied sleeve span trapped the link inside the bearing pockets,
so v26 confines the receiver to the clear 20.0 mm fork gap with 0.8 mm axial
clearance per side. Print the [released bed-ready distal fit article](assembly_dry_fit/ABS_FA_Distal_Link_L_D10p30_STEEL_PIN_FIT_PRINT_ORIENTED.stl)
and complete its physical insertion, withdrawal, spin, rock and axial-play
checks. The [21.6 mm full-span ladder](knee_pin_fit/) remains a conservative
optional diagnostic. Retention and encoder coupling still gate powered use.

## 2026-09-14 M3 receiver recalibration — Ø4.5 selected

The owner has printed the cable cover, corrected front cable post, wheel hub
and general fit gauge. [Exact files and completion record](../evidence/assembly/2026-09-07_small_parts_printed/).
The gauge's nominal Ø4.0 M3 station is too small.
[Physical result](../evidence/inserts/2026-09-14_m3_coupon_fail/). The owner
printed the Fusion-generated [Ø4.1–4.5 M3 ladder](insert_fit/) and selected the
largest, unmarked-end station, nominal Ø4.5. The active sources and exports were
promoted and verified through Fusion. Print the Ø4.5 corrected proximal-link
replacement and stand; print the Ø4.5 shoulder plate if the fitted plate is the
prior Ø4.0 revision. Detached motor-fit and cover/post/harness results are still pending;
the rear anchor is optional.
The [current print queue](../README.md#current-print--ordered-pin-unpowered-abs-mechanical-article) contains
the remaining prints, and [PROJECT_STATUS.md](../PROJECT_STATUS.md) maintains
the active mechanical, CAD and electronics work.

## 2026-09-17 unpowered spring-mechanical article

The new [mechanical spring test batch](mechanical_spring_test/) adapts the owned
OD18 / ID9 / 50 mm spring with two Ø8-pilot eyes, a removable square guide,
a -8°…+15° stop, an outboard steel-pin spacer/keeper and a support-free no-tyre
wheel shell. All seven STLs are print oriented and Fusion verified. The spring
is nominally uncompressed at -8° and reaches 10.240 mm modeled compression at
+15°. Use only with both motors unplugged, the stand clamped, the wheel clear
and the distal side hand-contained. The local README is the required print,
detached-fit, assembly and observation traveller.

This release does not clear the final tyre-compatible rim, final knee-pin
retention, encoder coupling, spring characterisation, ground contact or powered
motion. It depends on the Ø10.30 distal article passing its physical steel-pin
checks first.

## 2026-09-22 ordered-pin fit ladders

The two [ordered-pin ABS ladders](ordered_pin_fit/) are complete historical fit
evidence. Using the actual pins without measurement, the owner selected
nominal Ø4.25 for the root-dowel hub socket and nominal Ø4.25 for the clevis
link passages. Fusion v29 now contains those values and the large
[hub/proximal/distal production files](ordered_pin_integration/) were
re-exported and released for printing. The Ø6 × 10 captive stop remains a
deliberate Ø6.2 clearance fit and has no ladder. **[SUPERSEDED 2026-09-23:
the v29 distal export lost its Ø10.30 receiver, and the owner then requested
Ø4.30 root-dowel and clevis-link holes. Print the PINREV2 hub and links from
the [current queue](../README.md#current-print--ordered-pin-unpowered-abs-mechanical-article);
[audit](../evidence/assembly/2026-09-23_mechanical_reprint_audit/).]**

## Actuator-coupon slicer setup

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
