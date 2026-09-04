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

**Print one ABS fit coupon now:** [direct raw-GitHub download — owned M4×8
insert ladder](https://raw.githubusercontent.com/TnnsBeast/Biped/main/first_article_stl/insert_fit/ABS_CAL_OWNED_M4x8_INSERT_POCKET_LADDER_PRINT_ORIENTED.stl).
Quantity 1, using the same tuned enclosed ABS profile planned for the leg. The
file is already oriented on its 60 × 16 mm face with all five bores vertical:
do not rotate, scale, apply hole compensation, or add supports. Use one insert
from the **M4 × 8** compartment of the Kadriick mixed case at each attempted
station. The Ø2 marker identifies Ø4.9; moving away from it gives
Ø4.9/5.0/5.1/5.2/5.3. Accept the smallest station that heat-sets square without
splitting/bulging and resists firm hand spin and pull after cooling. Report the
winning station before printing a hub.

**No larger M4 production part is released yet.** Ø5.1 is the scripted centre
candidate only. After the physical result is fed back through Fusion, the only
mandatory reprint from the work completed so far will be the Ø4.15 shoulder
hub. The already-printed hub remains motor-fit evidence but its legacy link
holes cannot receive inserts. The redesigned shoulder uses six owned M4 × 8
inserts through its full 8 mm flange. The wheel uses six more, with 6 mm
embedded in the hub and 2 mm housed by new near-circular rim reliefs. M4 × 10
is not needed.

**Keep the face-flat Ø19.10 ABS proximal link and both installed bearings.** Do
not reprint it. Ø19.15 remains the preference only if a future ABS replacement
is needed. After the coupon-selected hub is released and its inserts are fitted,
the supported, unplugged link may be dry-fitted to the **GIM6010 shoulder motor
only** with six M4 × 10 screws. The illustrated sequence is in the [picture
assembly guide](docs/assembly/shoulder_to_proximal_link.md).

`RIG_Stand`, `Wheel_Hub_L`, `Wheel_Rim_L`,
`Chassis_Shoulder_Plate_L`, and `Shoulder_Cable_Cover_L` were not reported
printed, so they will be new prints—not reprints. The M4 hub/rim candidates are
currently named `PROVISIONAL_DO_NOT_PRINT`. Their geometry and exact
insert/fastener map are recorded in
[`first_article_stl/heatset_receiver_release_manifest.json`](first_article_stl/heatset_receiver_release_manifest.json)
and [the printed-thread map](MANUFACTURING_CONSTRAINTS.md#threaded-interfaces-in-printed-parts).

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
