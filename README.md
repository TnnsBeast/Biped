# Beni

![Beni Prototype 1](docs/readme/beni_full_robot.png)

A mostly 3D-printed wheeled biped with active shoulders, passive spring-loaded
knees, and a driven wheel on each leg. A complete ABS single-leg integration
article is the active build; PA-CF structural printing is deferred to the later
two-leg build.

**[Current status](PROJECT_STATUS.md)** · **[Mechanical design](beni_prototype1_design_record.md)** · **[Electronics](electronics/README.md)** · **[Firmware](firmware/README.md)** · **[Interactive viewer](web/)**

## Mechanisms

| Complete leg | Wheel motor and hub | Passive knee |
|:---:|:---:|:---:|
| <img src="docs/readme/beni_leg_side.png" alt="Complete Beni leg in Fusion" width="440"> | <img src="docs/readme/beni_wheel_module.png" alt="Beni wheel module with the motor housing fixed inboard and the output hub outboard" width="440"> | <img src="docs/readme/beni_knee_detail.png" alt="Beni passive knee detail in Fusion" width="440"> |

## Shoulder assembly path

| Plate first | Hub through plate | Final stack |
|:---:|:---:|:---:|
| <img src="evidence/shoulder_assembly/2026-08-23_plate_sequence/01_plate_approaches_bare_motor.png" alt="Shoulder plate approaching the bare actuator" width="440"> | <img src="evidence/shoulder_assembly/2026-08-23_plate_sequence/02_hub_installs_after_plate.png" alt="Shoulder hub installed after the plate" width="440"> | <img src="evidence/shoulder_assembly/2026-08-23_plate_sequence/03_final_shoulder_stack.png" alt="Final shoulder assembly" width="440"> |

[Shoulder picture assembly guide](docs/assembly/shoulder_to_proximal_link.md) · [Heat-set receiver picture map](docs/assembly/heatset_receiver_map.md) · [Assembly-path evidence and acceptance result](evidence/shoulder_assembly/2026-08-23_plate_sequence/README.md) · [First-article prints](first_article_stl/README.md) · [Manufacturing constraints](MANUFACTURING_CONSTRAINTS.md)

The CAD gallery is exported from the live Fusion model with
[`readme_images_fusion.py`](readme_images_fusion.py) and should be refreshed with
model changes.

The passive-knee detail includes the live `Knee_Spring_L` helical body: Ø19 OD,
Ø2.6 wire and an 11.8-total-coil representation rebuilt to the current cartridge
length. The ordered part requirement remains 55 mm free length; CAD coil-bind
acceptance is governed by the specified 30.68 mm solid height and physical test.

---

<!-- PRINT_QUEUE_START -->
## Current print — convenience link

**Print one corrected ABS proximal link:** [direct raw-GitHub STL download](https://raw.githubusercontent.com/TnnsBeast/Biped/main/first_article_stl/assembly_dry_fit/ABS_FA_Proximal_Link_L_D19p15_M4_ACCESS_FIXED_PRINT_ORIENTED.stl).

This automatically maintained section links the next verified print. The
owner's new shoulder hub and insert installation passed. Keep that hub. The
replacement link clears the wall from two M4 head paths and restores the full
seat beneath a third head. It uses the selected Ø19.15 ABS bearing preference.

**Quantity 1, ABS.** Import the supplied orientation unchanged: broad outboard
arm/bearing face on the bed, all critical bores vertical. No rotation, scaling,
hole compensation or supports. Use the same tuned enclosed ABS profile as the
passing coupon: 0.20 mm layers, 4 walls, 5 top/bottom layers, 30% infill; use a
brim if that profile needs one. Preview the 20 mm channel and root-pad bridges;
check for drooping strands, damaged bearing lips or uneven screw seats.

**Acceptance:** before attachment, pass all six **M4 × 10 screws** through the
link's access passages; each head must sit flat without force. Rehearse both
bearing seats with outer-race thumb pressure and no radial rock. Install the
five knee M3 inserts while the link is open, after the exact-insert coupon
passes. Support the knee end and attach it to the accepted hub; all six M4
screws must start freely and clamp without pulling the print into place.
Keep the motor unplugged. [Assembly steps and audit](evidence/assembly/2026-09-05_access_fix/).

The old Ø19.10 print remains bearing-fit evidence; its access defect now
justifies replacement. Reuse bearings only if removed without damage. Do not
put M4 inserts into the link—the six M4 receivers are in the accepted hub.

Other bed-ready ABS files, quantity 1 each if needed: [shoulder plate](first_article_stl/assembly_dry_fit/ABS_FA_Chassis_Shoulder_Plate_L_M3_INSERTS_PRINT_ORIENTED.stl),
[cable cover](first_article_stl/assembly_dry_fit/ABS_FA_Shoulder_Cable_Cover_L_CLEARANCE_PRINT_ORIENTED.stl),
[wheel hub](first_article_stl/assembly_dry_fit/ABS_FA_Wheel_Hub_L_OWNED_M4x8_D5p30_PRINT_ORIENTED.stl), and
[stand](first_article_stl/mode_a/ABS_FA_RIG_Stand_M3_INSERTS_PRINT_ORIENTED.stl).
Use their unchanged supplied orientations and no supports; the stand requires
at least 300 mm bed length. Confirm the exact M3 insert coupon before heat
installation. Part-specific acceptance and limitations are in the
[receiver map](docs/assembly/heatset_receiver_map.md).

The corrected [front cable anchor](first_article_stl/mode_a/ABS_FA_RIG_Cable_Post_A_COVER_MOUNT_PRINT_ORIENTED.stl)
is also available, quantity 1 ABS, supplied flat orientation, no supports.
It fits outside the cable cover using **two M3 × 12** in its upper positions;
the lower two cover screws remain M3 × 10. Check its eye stays open with the
cover fitted and that the tie/harness clears the supported moving link.

**Still held:** wheel rim (unsupported ledges), distal link (real steel-pin fit
and printability), knee collar (retention), and the complete wired fixture
(actual harness routing, floor disposition and electronics). The cable-post
geometry clash is corrected. The wheel hub is available for detached
motor fit while the rim is held. The next full-leg phase remains ABS,
wheel-clear and current-limited under self-weight only after all gates close;
no spring preload or structural loading. PA-CF is deferred.
<!-- PRINT_QUEUE_END -->
