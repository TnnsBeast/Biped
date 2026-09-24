# Picture guide — GIM6010 shoulder to proximal link

This is the visual dry-fit sequence for the **left ABS single-leg article**. It
shows where the printed proximal link goes and which motor it belongs to.

> **Use the GIM6010-8 shoulder motor. Do not try this link on the GIM4305-10
> wheel motor.** Keep the motor unplugged, fit both 6800 bearings in the new
> proximal link, and support the knee end so the printed parts do not carry it as a
> cantilever. This is a fit check, not a powered or load test.

> **Updated 2026-09-23:** use the PINREV2 hub and proximal link reprints, with
> Ø4.30 root-dowel sockets. The September 22 ordered-pin prints and the earlier
> accepted hub and link remain fit evidence only. The three bought Ø4 × 10 root dowels enter the new
> hub before this shoulder assembly. Follow the
> [current ordered-pin traveller](../../first_article_stl/ordered_pin_integration/README.md#ordered-assembly)
> for the full unpowered leg sequence.

For this unpowered ordered-pin article, follow the
[current assembly traveller](../../first_article_stl/ordered_pin_integration/README.md#ordered-assembly).
The [two-leg BOM](../../beni_prototype1_bom_and_assembly.md#b-leg-build) is
background for the later structural build.

## Parts used in this check

- GIM6010-8 shoulder motor
- `Chassis_Shoulder_Plate_L`
- the current `ABS_PINREV2_Shoulder_Output_Hub_D4p15_ROOT_D4p30` hub with
  3 × Ø4 × 10 bought root dowels
- the current `ABS_PINREV2_Proximal_Link_D19p15_ROOT_D4p30_CLEVIS_D4p30` link and
  two 6800-2RS bearings
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

## 3. Install the revised printed output hub second

With the detached hub supported flat, install its six M4 × 8 inserts from the
outboard/link face and seat the three bought Ø4 × 10 dowels 5.0 mm into their
selected Ø4.30 blind sockets. Reject whitening or splitting. The iron must
not touch the dowel sockets.

Align the hub with the GIM6010's three factory pins and move it straight onto
the output face. The pins must enter with light finger pressure and the hub must
reach the metal face without screw force.

<img src="../../evidence/shoulder_assembly/2026-08-23_plate_sequence/02_hub_installs_after_plate.png" alt="Printed shoulder output hub approaching the GIM6010 after the shoulder plate is seated" width="760">

Once seated, finger-start the six **M3 × 10** output-hub screws.

The photograph below shows the **earlier** hub-to-real-motor fit. The shoulder
plate is absent and the pictured hub has been superseded, so use it only to
identify the motor/output direction:

<img src="../../evidence/shoulder_assembly/2026-08-23_plate_sequence/04_owner_shoulder_plate_attempt.jpg" alt="Owner photograph of the printed shoulder output hub seated on the real GIM6010 output" width="760">

## 4. Confirm the shoulder stack before adding the link

At this point the stationary plate is behind the printed rotating hub. Nothing
should be pinched between the hub and plate.

<img src="../../evidence/shoulder_assembly/2026-08-23_plate_sequence/03_final_shoulder_stack.png" alt="Completed GIM6010 shoulder plate and output hub stack before the proximal link is attached" width="760">

## 5. Identify the proximal-link root

The **large circular end with six counterbores and the Ø34 centre access** is the
shoulder end. The forked end containing the two installed 6800 bearings points
away from the shoulder motor toward the knee.

<img src="../../first_article_stl/ordered_pin_integration/00_fusion_ABS_PINREV2_Proximal_Link_D19p15_ROOT_D4p30_CLEVIS_D4p30_PRINT_ORIENTED.png" alt="Current ordered-pin proximal link showing the shoulder root and forked bearing end" width="760">

Do not put either end of this link against the GIM4305 wheel motor. That motor
mounts to the current ordered-pin distal link, while it is still detached.

## Where the heat inserts go

The proximal link does **not** bolt into the shoulder plate. Its six M4 screws
pass through the link's root counterbores and thread into six inserts installed
from the outboard face of the **rotating shoulder hub**.

<img src="../../first_article_stl/ordered_pin_integration/00_fusion_ABS_PINREV2_Shoulder_Output_Hub_D4p15_ROOT_D4p30_PRINT_ORIENTED.png" alt="Current ordered-pin hub with six M4 receiver bores and three root-dowel sockets" width="760">

The picture shows the current hub with Fusion-exported **Ø5.3 ABS M4 receivers**
and three Ø4.30 root-dowel sockets. Install six fresh M4 × 8 inserts in the
detached revised hub from the outboard/link face with a depth stop. Each
occupies the full 8.0 mm flange.
M4 × 10 link screws have 6.2 mm thread engagement and 1.8 mm end clearance in
the final pose. The corrected link has continuous head and driver access.

The four smaller M3 inserts in the shoulder area belong in the **stationary
shoulder plate**, only for the removable cable cover. The cover itself has four
Ø3.4 clearance holes and no inserts; its M3 × 10 screws are installed from the
accessible outboard face.

| Shoulder plate — four M3 receivers | Cable cover — four clearance holes |
|:---:|:---:|
| <img src="../../first_article_stl/assembly_dry_fit/00_fusion_ABS_FA_Chassis_Shoulder_Plate_L_M3_INSERTS_PRINT_ORIENTED.png" alt="Print-oriented shoulder plate with four M3 insert receivers around the motor opening" width="440"> | <img src="../../first_article_stl/assembly_dry_fit/00_fusion_ABS_FA_Shoulder_Cable_Cover_L_CLEARANCE_PRINT_ORIENTED.png" alt="Print-oriented shoulder cable cover with four clearance holes and no inserts" width="440"> |

## 6. Rehearse the revised link, then attach it

Use `ABS_PINREV2_Proximal_Link_D19p15_ROOT_D4p30_CLEVIS_D4p30_PRINT_ORIENTED.stl`.
Before fitting the link, pass each of the six M4 × 10 screws through its outer
access hole. Every head must rest flat on its counterbore floor without force.
The lightening opening now stops short of the previously clipped seat.

Rehearse both bearing seats with outer-race thumb pressure. Both bearings must
sit square and have no perceptible radial rock. Reuse old bearings only if they
can be removed without damage. The current replacement has five verified Ø4.5
M3 pockets selected from the same-profile ABS ladder. Install the five M3
inserts in this new link after inspection.

Support the knee end. Move the link straight onto the three new root dowels;
its Ø4.30 × 5.2 slip sockets must allow both faces to meet by hand. Then
finger-start all six M4 × 10 screws and check each head clamps flat. Do not
use screws to draw the link into place. Remove and refit it once to confirm
the service path.

If fitting front cable post A, put it on the outside of the cover first. Its
upper two screws are **M3 × 12**, replacing the two upper cover M3 × 10;
the lower two remain ×10. The post's eye projects beyond the cover edge. Route
the tie and harness before the link, then hand-check clearance with the knee
supported. Remove the link before servicing the cover; remove cover/post before
accessing the housing screws.

[Exact Fusion audit and physical acceptance](../../evidence/assembly/2026-09-05_access_fix/).
The PINREV2 distal reprint restores the selected Ø10.30 × 20.0 steel-pin
receiver; the September 22 distal print lacks it and must not be used. The
reprint's physical knee-pin fit and supported spring-free stop check are next. Keep both motors unplugged for this rehearsal.
