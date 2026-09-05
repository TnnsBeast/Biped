# Picture guide — GIM6010 shoulder to proximal link

This is the visual dry-fit sequence for the **left ABS single-leg article**. It
shows where the printed proximal link goes and which motor it belongs to.

> **Use the GIM6010-8 shoulder motor. Do not try this link on the GIM4305-10
> wheel motor.** Keep the motor unplugged, leave the two 6800 bearings in the
> link, and support the knee end so the printed parts do not carry the link as a
> cantilever. This is a fit check, not a powered or load test.

> **Updated 2026-09-04:** the corrected Ø4.15 ABS hub with owner-passed Ø5.3
> insert pockets is ready to print for detached insert installation and motor
> fit. The **six-screw proximal-link joint remains on hold**: two screw heads
> cannot follow the straight outboard path through the link's internal wall.
> Keep the printed link and bearings while a detached loading rehearsal checks
> whether an alternate insertion angle works. Do not force the screws.

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

<img src="../../first_article_stl/assembly_dry_fit/00_fusion_ABS_FA_Shoulder_Output_Hub_L_D4p15_OWNED_M4x8_D5p30_PRINT_ORIENTED.png" alt="Coupon-selected print-oriented shoulder hub with six full-depth M4 insert bores in its outboard flange" width="760">

The picture shows the Fusion-exported **Ø5.3 ABS receiver** selected by the
owner's passing ladder. Install six M4 × 8 inserts in the detached hub from the
outboard/link face with a depth stop. Each occupies the full 8.0 mm flange.
M4 × 10 link screws have 6.2 mm thread engagement and 1.8 mm end clearance in
the final pose, but their complete loading path is not yet released.

The four smaller M3 inserts in the shoulder area belong in the **stationary
shoulder plate**, only for the removable cable cover. The cover itself has four
Ø3.4 clearance holes and no inserts; its M3 × 10 screws are installed from the
accessible outboard face.

| Shoulder plate — four M3 receivers | Cable cover — four clearance holes |
|:---:|:---:|
| <img src="../../first_article_stl/assembly_dry_fit/00_fusion_ABS_FA_Chassis_Shoulder_Plate_L_M3_INSERTS_PRINT_ORIENTED.png" alt="Print-oriented shoulder plate with four M3 insert receivers around the motor opening" width="440"> | <img src="../../first_article_stl/assembly_dry_fit/00_fusion_ABS_FA_Shoulder_Cable_Cover_L_CLEARANCE_PRINT_ORIENTED.png" alt="Print-oriented shoulder cable cover with four clearance holes and no inserts" width="440"> |

## 6. Resolve screw loading before attaching the link

**BLOCKED — no six-screw assembly release yet.** The new Fusion sweep found
two M4 × 10 screw heads colliding with the link's internal wall on a straight
approach through the opposite arm. A Ø3.5 driver fits, but the larger screw
heads do not share that path. The previous instruction to insert all six
screws through the access holes is withdrawn.

Keep the link detached, with its bearings installed. Try loading each loose
M4 × 10 screw into its root counterbore by hand, without force. If another
angle lets all six seat, record the sequence so it can be checked before the
link is attached. A blocked screw is a stop condition, not a reason to push,
drill, heat or file the printed wall. No replacement link is requested before
this physical check.

The body-only link insertion and removal path is clear in Fusion, but this
alone does not close the screw-loading gate. Full evidence:
[2026-09-04 assembly checks](../../ASSEMBLY_VERIFICATION.md#2026-09-04-release-checks-and-new-blockers).

After the shoulder joint is physically rehearsed, the distal-link build still
waits for the real Ø10 h6/h5 × 35 mm steel knee pin and its own printability
check. Keep both motors unplugged during these assembly rehearsals.
