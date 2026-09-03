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

This automatically maintained section keeps the next released print easy to
find while the project iterates.

**Reprint one part from the work completed so far: the shoulder hub.** Use
[`ABS_FA_Shoulder_Output_Hub_L_D4p15_PRINT_ORIENTED.stl`](first_article_stl/assembly_dry_fit/ABS_FA_Shoulder_Output_Hub_L_D4p15_PRINT_ORIENTED.stl).
It preserves the owner-tested Ø4.15 motor-pin fit and adds six verified Ø5.6 ×
7.2 pockets for PSM Sonic-Lok `SL-B-M4-5.8` inserts. The already-printed hub is
still useful as motor-fit evidence, but it cannot attach the link.

**Keep the face-flat Ø19.10 ABS proximal link and both installed bearings.** Do
not reprint it. Ø19.15 remains the preference only if a future ABS replacement
is needed. After the corrected hub's inserts pass their coupon and are fitted,
the supported, unplugged link may be dry-fitted to the **GIM6010 shoulder motor
only** with six M4 × 10 screws. The illustrated sequence is in the
[picture assembly guide](docs/assembly/shoulder_to_proximal_link.md).

`RIG_Stand`, `Wheel_Hub_L`, `Chassis_Shoulder_Plate_L`, and
`Shoulder_Cable_Cover_L` were not reported printed, so they are new prints—not
reprints. Their corrected bed-ready files and exact insert/fastener map are in
[`first_article_stl/heatset_receiver_release_manifest.json`](first_article_stl/heatset_receiver_release_manifest.json)
and [the printed-thread map](MANUFACTURING_CONSTRAINTS.md#threaded-interfaces-in-printed-parts).
The two short PSM M4 insert families are not in the photographed assortments;
obtain them, then print the
[`Ø5.5/5.6/5.7 M4 insert ladder`](first_article_stl/insert_fit/README.md)
before committing those joints.

**Next release gate:** do not print the distal link yet. Candidate eBay knee
pins are ordered (believed to be a set of three; quantity, exact specification
and delivery remain to be verified). A real Ø10 h6/h5 × 35 mm steel pin must
pass the fit coupon, and the corrected face-flat distal link still needs its
final Fusion support/bridge and assembly-path audit. A printed ABS pin is only a
supported hand-alignment placeholder—not a release gauge or powered-test pin.
`RIG_Knee_Collar_L` is also unreleased: its current geometry does not retain the
pin and must wait for measurements of the delivered hardware and bearing stack.
PA-CF is deferred until the later two-leg structural build.
<!-- PRINT_QUEUE_END -->
