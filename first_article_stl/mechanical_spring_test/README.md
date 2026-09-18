# Unpowered ABS spring-mechanical test

This batch completes a supported, motor-unplugged single-leg mechanical article
around the owned **OD18 / ID9 / 50 mm** yellow spring. It is a hand-operated
fit and behavior test. It does not establish spring rate, payload, ground
traction, powered-motion clearance, structural life, or a safe two-leg build.

The revised cartridge has 50.000 mm between its spring seats at the **-8°
extension stop**, so the spring installs with nominally zero compression. The
new printed stop limits the test to **+15°**, where Fusion gives a 39.760 mm
installed spring length and **10.240 mm compression**. The actual equilibrium
angle cannot be predicted until the spring rate is measured: this compression
spring opposes knee flexion, while the leg's self-weight flexes the knee.

## Print these files

Import every `PRINT_ORIENTED` STL unchanged. Do not rotate, scale, or apply
hole compensation.

| File | Qty | Purpose and bed orientation |
|---|---:|---|
| [`ABS_TEST_Cart_Upper_Eye_50mm_AXIS_UP_PRINT_ORIENTED.stl`](ABS_TEST_Cart_Upper_Eye_50mm_AXIS_UP_PRINT_ORIENTED.stl) | 1 | Upper eye, spring axis vertical; use a brim |
| [`ABS_TEST_Cart_Lower_Eye_50mm_AXIS_UP_PRINT_ORIENTED.stl`](ABS_TEST_Cart_Lower_Eye_50mm_AXIS_UP_PRINT_ORIENTED.stl) | 1 | Lower eye, spring axis vertical; use a brim |
| [`ABS_TEST_Cart_Guide_Bar_50mm_FLAT_PRINT_ORIENTED.stl`](ABS_TEST_Cart_Guide_Bar_50mm_FLAT_PRINT_ORIENTED.stl) | 1 | Removable 3.8 mm square guide, long face on the bed |
| [`ABS_TEST_Knee_Stop_Plate_15deg_PRINT_ORIENTED.stl`](ABS_TEST_Knee_Stop_Plate_15deg_PRINT_ORIENTED.stl) | 1 | -8° to +15° test stop, full plate face on the bed |
| [`ABS_TEST_Knee_Pin_Outboard_Spacer_PRINT_ORIENTED.stl`](ABS_TEST_Knee_Pin_Outboard_Spacer_PRINT_ORIENTED.stl) | 1 | Locates in the encoder bracket and limits outboard pin travel |
| [`ABS_TEST_Knee_Encoder_Bracket_PIN_KEEPER_PRINT_ORIENTED.stl`](ABS_TEST_Knee_Encoder_Bracket_PIN_KEEPER_PRINT_ORIENTED.stl) | 1 | Existing bracket reused as the outboard keeper plate |
| [`ABS_TEST_Wheel_Rim_NoTyre_PRINT_ORIENTED.stl`](ABS_TEST_Wheel_Rim_NoTyre_PRINT_ORIENTED.stl) | 1 | Support-free suspended-test wheel shell; broad web face on the bed |

Use the same enclosed ABS profile as the passed dimensional articles: **0.20 mm
layers, 4 walls, 5 top and 5 bottom layers, 30% infill**. Disable supports for
all seven files. A brim is required on both cartridge eyes and is permitted on
the other parts if the tuned ABS profile normally uses one. The eye pivot
passages have self-supporting pointed roofs; inspect them after printing and do
not drill, file, sand, heat, or force a failed fit.

Print the two eyes, guide and spacer together only if that plate has stable ABS
results. Print the wheel shell alone. Keep the labels with the two cartridge
eyes after removal.

## Existing parts required

This batch assumes these already released parts are printed or will be printed
from the active queue:

- the Ø4.5 M3 proximal-link replacement, with five inserts installed;
- the Ø10.30 × 20.0 distal steel-pin article after it passes its physical
  insertion, withdrawal, spin, rock, and axial-play checks;
- the accepted shoulder hub, wheel hub, shoulder plate as required, and the
  clamped Mode A stand.

Use the owned 50 mm spring, both 6800 bearings, the 10 × 35 steel knee pin,
**2 × Ø4 × 32 steel clevis pins with E-clips**, **1 × Ø6 × 9 steel stop dowel**,
3 × M3 × 6 stop-plate screws, 2 × M3 × 16 bracket screws, and 6 × M4 × 8 wheel
rim screws. Do not substitute printed cartridge pins or a printed stop dowel.
If the two clevis pins or the stop dowel are not in hand, stop before installing
the spring.

## Detached fit checks

The guide bar does **not** enter the teardrop-shaped side passage. That passage
is the horizontal Ø4 clevis-pin hole; its pointed roof is only a self-supporting
print feature. Insert the guide along the spring axis through the round hole in
the raised Ø8 cylindrical spring pilot. The guide then runs through the center
of the spring.

1. Slide the guide bar into the upper eye through the round opening in its
   raised spring pilot. It must bottom by hand and pull out by hand. Fusion
   provides 0.626 mm diametral room around the bar's diagonal; any binding or
   layer split is a failed print.
2. Slide the lower eye over the free end of the guide. It must move through the
   full available travel without catching.
3. Place each end of the free spring over its Ø8 pilot. Both ends must sit flat
   without spreading, force, or visible rocking, matching the passed detached
   cap test.
4. Pass each Ø4 clevis pin through its printed eye by hand. The pointed roof is
   print clearance above the pin, not a second working position.
5. Seat the spacer's Ø7.6 locator in the encoder bracket's Ø8 center hole. It
   must sit flat and remain removable.

## Assembly order

Keep both motors unplugged throughout. Clamp or bolt the Mode A stand to the
bench before the leg is attached, support the knee and wheel, and keep the wheel
clear of the floor.

1. Install the two bearings and assemble the proximal and released distal links
   with the steel knee pin. Confirm the pin still withdraws by hand before
   adding the spring hardware.
2. Install the Ø6 × 9 steel dowel in the distal link and bolt the new test stop
   plate to the three proximal-link inserts with M3 × 6 screws. Hand-pose the
   spring-free knee and confirm it stops at -8° and +15°.
3. Put the knee at the -8° stop. Insert the upper cartridge eye radially into
   its proximal-link clevis and install the upper steel clevis pin and E-clips.
4. Insert the guide bar through the round center of the upper eye's raised Ø8
   pilot. Slide the free spring over the guide and onto that pilot. With the
   lower eye's raised pilot facing the other spring end, slide its round center
   opening over the exposed guide, then bring its pivot into the distal-link
   clevis. The lower clevis pin must enter with fingertip pressure. If more than slight hand
   compression is needed, stop and record the achieved gap; do not pull the
   parts together with a pin, screw, clamp, or tool.
5. Put the printed spacer on the encoder bracket with its small locator in the
   bracket center hole. Bolt the bracket to the two proximal-link inserts with
   M3 × 16 screws. The spacer should sit 0.3 mm beyond the modeled knee-pin end
   and leave 0.5 mm to the bracket plate. It limits outboard pin travel; the
   firm-thumb receiver fit and the operator's hand remain the inboard control
   for this test.
6. Bolt the no-tyre test wheel shell to the accepted wheel hub with six M4 × 8
   screws. This shell omits the unsupported inner ledge, tyre bead, and inboard
   flange. Do not fit the TPU tyre and do not put this shell on the floor.

Fusion found clear radial paths for both cartridge eyes, clear 40 mm insertion
paths for the guide and both clevis pins, a clear 30 mm spring-over-guide path,
and a clear 40 mm outboard service path for the test wheel shell.

## Hand test

Keep one hand on the distal link or wheel at all times. Move slowly through
**-8°, 0°, +5°, +10°, and +15°**. Never push through either stop.

At each position, reduce hand support gradually and observe whether the
self-weight/spring balance settles, returns toward extension, or moves toward
the +15° stop. A useful result is a smooth, repeatable tendency with no spring
bowing, guide binding, eye cracking, pin migration, or stop-plate marking. It is
also valid for the leg to settle at an undesired angle; that result tells us the
unknown spring rate does not balance this ABS article as hoped.

Stop immediately for coil contact, scraping, guide buckling, a click or crack,
visible whitening, a moving knee pin, a loose clevis clip, or a stop that does
not engage. Do not add weight, allow ground contact, bounce the leg, backdrive
or power either motor, or use the result as a payload test.

The exact Fusion sweep, service paths, stop-overtravel proof, print orientations,
and mesh hashes are in [`fusion_manifest.json`](fusion_manifest.json) and the
[release evidence](../../evidence/assembly/2026-09-17_abs_spring_mechanical_test/).
