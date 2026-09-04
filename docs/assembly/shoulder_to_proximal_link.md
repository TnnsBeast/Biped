# Picture guide — GIM6010 shoulder to proximal link

This is the visual dry-fit sequence for the **left ABS single-leg article**. It
shows where the printed proximal link goes and which motor it belongs to.

> **Use the GIM6010-8 shoulder motor. Do not try this link on the GIM4305-10
> wheel motor.** Keep the motor unplugged, leave the two 6800 bearings in the
> link, and support the knee end so the printed parts do not carry the link as a
> cantilever. This is a fit check, not a powered or load test.

> **REPRINT REQUIRED AFTER THE M4 COUPON, updated 2026-09-03:** the
> already-printed Ø4.15 hub is a verified
> hub-to-motor fit article only. Do not put inserts into its legacy Ø3.3 holes.
> The replacement preserves that Ø4.15 fit and uses six owner-held M4 × 8
> inserts through the full 8.0 mm flange. Its exact printed bore is not released
> until the new ABS ladder selects it.

The canonical fastener schedule and final assembly requirements remain in
[`beni_prototype1_bom_and_assembly.md`](../../beni_prototype1_bom_and_assembly.md#b-leg-build).

## Parts used in this check

- GIM6010-8 shoulder motor
- `Chassis_Shoulder_Plate_L`
- the coupon-selected `ABS_FA_Shoulder_Output_Hub_L_D4p15` replacement
- the printed face-flat proximal link with both 6800-2RS bearings installed
- 8 × M3 × 8 housing screws
- 6 × M3 × 10 shoulder-output-hub screws
- 6 × owner-held Kadriick M4 × 8 heat-set inserts and
  6 × M4 × 10 proximal-link-to-hub screws

For the initial dry fit, only finger-start the screws. Do not apply final torque
or use screws to pull parts together.

## 1. Start with the output hub removed

The shoulder plate goes over the **bare output rotor** from the motor's front
side. The Ø80 motor housing stays behind the plate; it is not supposed to pass
through the plate opening.

<img src="../../evidence/shoulder_assembly/2026-08-23_plate_sequence/01_plate_approaches_bare_motor.png" alt="Shoulder plate approaching the bare GIM6010 motor while the output hub is removed" width="760">

Hold the plate with its raised cable-spiral lip facing away from the motor and
its flat panel face toward the stationary motor housing.

## 2. Seat the plate on the stationary housing

Finger-start two opposite **M3 × 8** housing screws, then verify that the other
six start freely. Do not substitute M3 × 10 screws here: they bottom before the
5 mm plate is clamped.

If you are routing the real harness, place it in the plate's cable spiral before
the output hub and proximal link cover this area.

## 3. Install the printed output hub second

Align the hub with the GIM6010's three factory pins and move it straight onto
the output face. The pins must enter with light finger pressure and the hub must
reach the metal face without screw force.

<img src="../../evidence/shoulder_assembly/2026-08-23_plate_sequence/02_hub_installs_after_plate.png" alt="Printed shoulder output hub approaching the GIM6010 after the shoulder plate is seated" width="760">

Once seated, finger-start the six **M3 × 10** output-hub screws.

The photograph below confirms only the hub-to-real-motor fit. The shoulder
plate is not installed in this photograph, so use it as fit evidence—not as the
assembly order:

<img src="../../evidence/shoulder_assembly/2026-08-23_plate_sequence/04_owner_shoulder_plate_attempt.jpg" alt="Owner photograph of the printed shoulder output hub seated on the real GIM6010 output" width="760">

## 4. Confirm the shoulder stack before adding the link

At this point the stationary plate is behind the printed rotating hub. Nothing
should be pinched between the hub and plate.

<img src="../../evidence/shoulder_assembly/2026-08-23_plate_sequence/03_final_shoulder_stack.png" alt="Completed GIM6010 shoulder plate and output hub stack before the proximal link is attached" width="760">

## 5. Identify the proximal-link root

The **large circular end with six counterbores and the Ø34 centre access** is the
shoulder end. The forked end containing the two installed 6800 bearings points
away from the shoulder motor toward the knee.

<img src="../../first_article_stl/assembly_dry_fit/01_fusion_abs_proximal_d19p10_with_bearings.png" alt="ABS proximal link showing the large circular shoulder root and forked bearing end" width="760">

Do not put either end of this link against the GIM4305 wheel motor. That motor
eventually mounts to the unreleased distal link.

## Where the heat inserts go

The proximal link does **not** bolt into the shoulder plate. Its six M4 screws
pass through the link's root counterbores and thread into six inserts installed
from the outboard face of the **rotating shoulder hub**.

<img src="../../first_article_stl/assembly_dry_fit/00_fusion_ABS_FA_Shoulder_Output_Hub_L_D4p15_OWNED_M4x8_D5p10_PROVISIONAL_DO_NOT_PRINT_PRINT_ORIENTED.png" alt="Provisional print-oriented shoulder hub with six full-depth M4 insert bores in its outboard flange" width="760">

The picture is the Fusion-verified **provisional Ø5.1 candidate, not a print
release**. First print the
[`owned-M4×8 ladder`](../../first_article_stl/insert_fit/README.md). After its
winning bore is promoted into Fusion, install six M4 × 8 inserts from the
outboard/link face with a depth stop. Each occupies the full 8.0 mm flange. An
M4 × 10 screw through the link engages 6.2 mm and stops 1.8 mm before the
motor-side insert end.

The four smaller M3 inserts in the shoulder area belong in the **stationary
shoulder plate**, only for the removable cable cover. The cover itself has four
Ø3.4 clearance holes and no inserts; its M3 × 10 screws are installed from the
accessible outboard face.

| Shoulder plate — four M3 receivers | Cable cover — four clearance holes |
|:---:|:---:|
| <img src="../../first_article_stl/assembly_dry_fit/00_fusion_ABS_FA_Chassis_Shoulder_Plate_L_M3_INSERTS_PRINT_ORIENTED.png" alt="Print-oriented shoulder plate with four M3 insert receivers around the motor opening" width="440"> | <img src="../../first_article_stl/assembly_dry_fit/00_fusion_ABS_FA_Shoulder_Cable_Cover_L_CLEARANCE_PRINT_ORIENTED.png" alt="Print-oriented shoulder cable cover with four clearance holes and no inserts" width="440"> |

## 6. Fit the proximal link to the shoulder hub

This step is released only after the physical ladder result is incorporated in
the **new corrected hub** and its six owned M4 × 8 inserts are installed. Do
not use M4 × 10 inserts: the extra length has no available purpose here. See the canonical
[printed-thread map](../../MANUFACTURING_CONSTRAINTS.md#threaded-interfaces-in-printed-parts).

Support the bearing end on a block or folded towel. Bring the link's large root
face squarely onto the hub's outboard flange and align the six Ø44 bolt-circle
positions.

1. Finger-start two opposite **M4 × 10** screws through the link into the hub.
2. Confirm the remaining four screws also start freely.
3. Confirm the root face sits flush all the way around.
4. Confirm the hub screws remain reachable through the link's Ø34 centre access
   and the M4 driver path is clear through the link's Ø9 access holes.
5. Stop at the dry-fit state; keep the motor unplugged and the link supported.

The final orientation looks like the upper link in this complete-leg view:

<img src="../readme/beni_leg_side.png" alt="Complete Fusion leg view showing the proximal link attached to the GIM6010 shoulder hub" width="760">

## Pass / stop decision

**PASS** only with the corrected hub when the link reaches the hub face without
force, all six M4 screws finger-start, the faces remain flush, and the link
clears the stationary plate and cable path.

**STOP** with the already-printed legacy Ø4.15 hub, or if a screw is needed to
draw the link into position, a screw starts crooked, the root rocks, or the
link touches the stationary plate. Photograph the exact interference and
remove the link rather than forcing it.

After this check, the distal-link build remains on hold until a real Ø10 h6/h5 ×
35 mm steel knee pin passes the recorded fit gate. Do not energize the shoulder
with only the proximal link cantilevered from it.
