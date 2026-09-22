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
length. This is the original 55 mm baseline. The owner has the recommended
yellow OD18 / ID9 × **50 mm spring**; the earlier longer-length report was a
typo, corrected on September 6. Keep that spring. The cartridge adaptation
is still unfinished; see the [spring record](evidence/springs/2026-09-05_reconciliation/)
before printing spring-loaded parts.

---

<!-- PRINT_QUEUE_START -->
## Current print — ordered-pin unpowered ABS mechanical article

**Print the two [ordered-pin fit ladders](first_article_stl/ordered_pin_fit/) first, then report the selected stations.** Use the actual Ø4 × 10 dowel and M4 × 40 clevis pin as go/no-go gauges; no pin measurement is required. Hold the large hub and link prints until those results are promoted into the CAD and the three affected STLs are confirmed or re-exported. The Ø6 × 10 captive stop is deliberately clearance-fit and needs no ladder.

Fusion verified both ladder B-Reps, controlled orientations, and closed-manifold meshes. It also verified the ordered hardware envelopes, all four preliminary replacement meshes, the full 24-pose sweep, OD18/ID9 spring envelope, guide and clevis insertion paths, steel knee-pin path, no-tyre wheel-shell service path, stop clearance through the permitted range, and positive stop contact 0.5° beyond each limit. [Fit-ladder evidence](evidence/assembly/2026-09-22_ordered_pin_fit_ladders/) · [ordered-pin evidence](evidence/assembly/2026-09-21_ordered_pin_integration/) · [complete motion evidence](evidence/assembly/2026-09-17_abs_spring_mechanical_test/).

### Print these calibration ladders now

| Part | Qty | Import orientation and supports |
|---|---:|---|
| [Ø4 × 10 root-dowel blind-socket ladder](first_article_stl/ordered_pin_fit/ABS_CAL_D4x10_ROOT_BLIND_SOCKET_LADDER_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged; broad face on bed; no supports; two Ø2 holes mark the Ø4.05 end |
| [M4 × 40 clevis link-land ladder](first_article_stl/ordered_pin_fit/ABS_CAL_M4x40_CLEVIS_LINK_LAND_LADDER_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged; boss/web face on bed; no supports; brim permitted; two Ø2 holes mark the Ø4.15 end |

### After the fit selection, print or replace these four parts

| Part | Qty | Import orientation and supports |
|---|---:|---|
| [Shoulder output hub with three Ø4 × 10 root sockets](first_article_stl/ordered_pin_integration/ABS_PINREV_Shoulder_Output_Hub_D4p15_ROOT_D4x10_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged, Ø56 outboard flange on bed; no supports; controlled socket bridges |
| [Proximal link with root sockets and integral M4 × 40 upper land](first_article_stl/ordered_pin_integration/ABS_PINREV_Proximal_Link_D19p15_ROOT_D4x10_M4x40_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged, broad outboard face on bed; no support in functional bores or channel |
| [Distal link with captive Ø6 × 10 socket and integral M4 × 40 lower land](first_article_stl/ordered_pin_integration/ABS_PINREV_Distal_Link_D10p30_D6x10_M4x40_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged, broad inboard face on bed; use only the traveller's selective supports and block all fit bores |
| [-8°…+15° closed-skin captive stop plate](first_article_stl/ordered_pin_integration/ABS_PINREV_Knee_Stop_Plate_15deg_D6x10_CAPTIVE_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged, closed skin on bed and channel upward; no supports |

### Reuse or print these unchanged September 17 parts

| Part | Qty | Import orientation and supports |
|---|---:|---|
| [Upper 50 mm cartridge eye](first_article_stl/mechanical_spring_test/ABS_TEST_Cart_Upper_Eye_50mm_AXIS_UP_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged, spring axis vertical; no supports; brim required |
| [Lower 50 mm cartridge eye](first_article_stl/mechanical_spring_test/ABS_TEST_Cart_Lower_Eye_50mm_AXIS_UP_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged, spring axis vertical; no supports; brim required |
| [Removable guide bar](first_article_stl/mechanical_spring_test/ABS_TEST_Cart_Guide_Bar_50mm_FLAT_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged, long face on bed; no supports |
| [Outboard knee-pin spacer](first_article_stl/mechanical_spring_test/ABS_TEST_Knee_Pin_Outboard_Spacer_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged; no supports |
| [Encoder bracket used as pin keeper](first_article_stl/mechanical_spring_test/ABS_TEST_Knee_Encoder_Bracket_PIN_KEEPER_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged; no supports |
| [No-tyre wheel shell](first_article_stl/mechanical_spring_test/ABS_TEST_Wheel_Rim_NoTyre_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged, broad web face on bed; no supports; print alone |

Use the tuned enclosed ABS profile: **0.20 mm layers, 4 walls, 5 top and 5 bottom layers, 30% infill**. Do not rotate, scale, compensate holes, drill, sand, file or heat-fit a failed article. The pointed roofs in the eye pivots are intentional self-supporting geometry.

### Existing parts and hardware that must pass first

1. The ordered-pin distal link is also the current Ø10.30 × 20.0 steel knee-pin article. Before installing the spring, confirm firm-thumb knee-pin insertion, hand withdrawal, no free spin, no radial rock, and acceptable axial play.
2. Install inserts only in the four new replacement parts. Retain the earlier hub, proximal link, distal link, and stop plate as evidence, not assembly parts.
3. Print and securely clamp the [Ø4.5 Mode A stand](first_article_stl/mode_a/ABS_FA_RIG_Stand_M3_INSERTS_PRINT_ORIENTED.stl). Replace a fitted Ø4.0 [shoulder plate](first_article_stl/assembly_dry_fit/ABS_FA_Chassis_Shoulder_Plate_L_M3_INSERTS_PRINT_ORIENTED.stl) before its insert installation.
4. Have the owned spring, **3 × Ø4 × 10 dowels**, **2 × M4 × 40 clevis pins with supplied cotters**, **2 × ISO 7089 M4 washers**, **1 × Ø6 × 10 dowel**, **3 × M3 × 10 stop screws**, the received steel knee pin, both 6800 bearings, and the printed wheel hub. The seller dimensions are already designed in; only visual inspection and hand fit are required.

Follow the [ordered-pin traveller](first_article_stl/ordered_pin_integration/) and then the unchanged September 17 sequence. Install the spring only with the knee resting at the -8° stop. Both motor power and communication cables stay unplugged. Clamp the stand, support the distal side by hand, keep the wheel clear, and record whether the leg settles and returns at -8°, 0°, 5°, 10° and 15°. Stop immediately for binding, cracking, stop bypass, coil contact, guide escape or loss of pin control.

The support-free no-tyre wheel shell is a suspended mechanical-test part. The final tyre-compatible structural rim, final pin retention, encoder coupling, ground contact, spring-rate/solid-height characterisation, intentional preload and powered motion remain held. Keep the TPU tyre off this article.

The earlier loose printed-pin mock-up and detached spring caps remain accepted historical evidence only. The provisional shin was destroyed during steel-pin recovery and must not be reprinted. [Earlier owner result](evidence/assembly/2026-09-07_owner_mockup/) · [real-pin failure and corrected receiver release](evidence/knee_fit/2026-09-16_distal_d10p30_release/).
<!-- PRINT_QUEUE_END -->
