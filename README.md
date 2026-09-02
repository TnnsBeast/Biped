# Beni

![Beni Prototype 1](docs/readme/beni_full_robot.png)

A mostly 3D-printed wheeled biped with active shoulders, passive spring-loaded
knees, and a driven wheel on each leg. The single-leg Mode A rig is the active
build; the complete robot is modeled but not yet built.

**[Current status](PROJECT_STATUS.md)** · **[Mechanical design](beni_prototype1_design_record.md)** · **[Electronics](electronics/README.md)** · **[Firmware](firmware/README.md)** · **[Interactive viewer](web/)**

## Mechanisms

| Complete leg | Wheel motor and hub | Passive knee |
|:---:|:---:|:---:|
| <img src="docs/readme/beni_leg_side.png" alt="Complete Beni leg in Fusion" width="440"> | <img src="docs/readme/beni_wheel_module.png" alt="Beni wheel module with the motor housing fixed inboard and the output hub outboard" width="440"> | <img src="docs/readme/beni_knee_detail.png" alt="Beni passive knee detail in Fusion" width="440"> |

## Shoulder assembly path

| Plate first | Hub through plate | Final stack |
|:---:|:---:|:---:|
| <img src="evidence/shoulder_assembly/2026-08-23_plate_sequence/01_plate_approaches_bare_motor.png" alt="Shoulder plate approaching the bare actuator" width="440"> | <img src="evidence/shoulder_assembly/2026-08-23_plate_sequence/02_hub_installs_after_plate.png" alt="Shoulder hub installed after the plate" width="440"> | <img src="evidence/shoulder_assembly/2026-08-23_plate_sequence/03_final_shoulder_stack.png" alt="Final shoulder assembly" width="440"> |

[Assembly-path evidence and acceptance result](evidence/shoulder_assembly/2026-08-23_plate_sequence/README.md) · [First-article prints](first_article_stl/README.md) · [Manufacturing constraints](MANUFACTURING_CONSTRAINTS.md)

The CAD gallery is exported from the live Fusion model with
[`readme_images_fusion.py`](readme_images_fusion.py) and should be refreshed with
model changes.

---

<!-- PRINT_QUEUE_START -->
## Current print — convenience link

This automatically maintained section keeps the next released print easy to
find while the project iterates.

**[ABS proximal link, Ø19.10 bearing bores — download STL](https://raw.githubusercontent.com/TnnsBeast/Biped/main/first_article_stl/assembly_dry_fit/ABS_FA_Proximal_Link_L_D19p10_PRINT_ORIENTED.stl)** — 1 × ABS.

Import as-is; it is already face-flat with both bearing axes vertical. Use
0.20 mm layers, 4 walls, 5 top/bottom layers, 30% infill, and a brim. Set
**supports off**: the 20.0 mm fork opening is a controlled bridge, and no support
may touch either bearing seat or the Ø17 retention lips. Expected size:
**141.921 × 127.127 × 31.600 mm**.

**After printing:** thumb-press one 6800-2RS bearing into each open outside face.
Before inserting them, confirm the bridged channel roof is intact and has no
loose strands or droop obstructing the fork. Both bearings must then enter
square, seat flush, have no rock, and remain removable without a clamp or
retaining compound. Follow the
[full test and acceptance instructions](first_article_stl/assembly_dry_fit/README.md#batch-3--unloaded-abs-proximal-link-bearing-rehearsal).

**Hold:** do not print the distal link yet; the Ø10 h6 knee pin and its DFM and
assembly-path verification still gate that release.
<!-- PRINT_QUEUE_END -->
