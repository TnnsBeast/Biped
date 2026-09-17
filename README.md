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
## Current print — unpowered ABS spring-mechanical article

**Start with the [upper cartridge eye direct download](https://raw.githubusercontent.com/TnnsBeast/Biped/main/first_article_stl/mechanical_spring_test/ABS_TEST_Cart_Upper_Eye_50mm_AXIS_UP_PRINT_ORIENTED.stl), then use the complete [print and assembly traveller](first_article_stl/mechanical_spring_test/).** This September 17 batch completes a clamped, motor-unplugged mechanical single-leg article around the owned **OD18 / ID9 / 50 mm** spring. It is limited to slow, hand-contained, wheel-clear self-weight observation from **-8° through +15°**.

Fusion verified all seven meshes, the full 24-pose sweep, OD18/ID9 spring envelope, guide and clevis insertion paths, steel knee-pin path, no-tyre wheel-shell service path, stop clearance through the permitted range, and positive stop contact 0.5° beyond each limit. At -8° the spring is nominally uncompressed; predicted compression is 3.257 mm at 0° and 10.240 mm at +15°. The actual resting angle is a physical observation because the owned spring rate is not measured. [Fusion evidence and images](evidence/assembly/2026-09-17_abs_spring_mechanical_test/).

### Print this mechanical-test batch

| Part | Qty | Import orientation and supports |
|---|---:|---|
| [Upper 50 mm cartridge eye](first_article_stl/mechanical_spring_test/ABS_TEST_Cart_Upper_Eye_50mm_AXIS_UP_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged, spring axis vertical; no supports; brim required |
| [Lower 50 mm cartridge eye](first_article_stl/mechanical_spring_test/ABS_TEST_Cart_Lower_Eye_50mm_AXIS_UP_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged, spring axis vertical; no supports; brim required |
| [Removable guide bar](first_article_stl/mechanical_spring_test/ABS_TEST_Cart_Guide_Bar_50mm_FLAT_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged, long face on bed; no supports |
| [-8°…+15° knee stop plate](first_article_stl/mechanical_spring_test/ABS_TEST_Knee_Stop_Plate_15deg_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged, full plate face on bed; no supports |
| [Outboard knee-pin spacer](first_article_stl/mechanical_spring_test/ABS_TEST_Knee_Pin_Outboard_Spacer_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged; no supports |
| [Encoder bracket used as pin keeper](first_article_stl/mechanical_spring_test/ABS_TEST_Knee_Encoder_Bracket_PIN_KEEPER_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged; no supports |
| [No-tyre wheel shell](first_article_stl/mechanical_spring_test/ABS_TEST_Wheel_Rim_NoTyre_PRINT_ORIENTED.stl) | 1 ABS | Import unchanged, broad web face on bed; no supports; print alone |

Use the tuned enclosed ABS profile: **0.20 mm layers, 4 walls, 5 top and 5 bottom layers, 30% infill**. Do not rotate, scale, compensate holes, drill, sand, file or heat-fit a failed article. The pointed roofs in the eye pivots are intentional self-supporting geometry.

### Existing parts and hardware that must pass first

1. Print and physically accept the [Ø10.30 × 20.0 distal steel-pin article](first_article_stl/assembly_dry_fit/ABS_FA_Distal_Link_L_D10p30_STEEL_PIN_FIT_PRINT_ORIENTED.stl): firm-thumb insertion, hand withdrawal, no free spin, no radial rock and acceptable axial play.
2. Print the [Ø4.5 M3 proximal-link replacement](first_article_stl/assembly_dry_fit/ABS_FA_Proximal_Link_L_D19p15_M4_ACCESS_FIXED_PRINT_ORIENTED.stl) before installing its five inserts. The printed Ø4.0 copy is retained only as fit evidence.
3. Print and securely clamp the [Ø4.5 Mode A stand](first_article_stl/mode_a/ABS_FA_RIG_Stand_M3_INSERTS_PRINT_ORIENTED.stl). Replace a fitted Ø4.0 [shoulder plate](first_article_stl/assembly_dry_fit/ABS_FA_Chassis_Shoulder_Plate_L_M3_INSERTS_PRINT_ORIENTED.stl) before its insert installation.
4. Have the owned spring, **2 × Ø4 × 32 clevis pins with E-clips**, **1 × Ø6 × 9 steel stop dowel**, the received steel knee pin, both 6800 bearings, the accepted shoulder hub and the printed wheel hub.

Follow the traveller's detached checks and assembly order. Install the spring only with the knee resting at the -8° stop. Both motor power and communication cables stay unplugged. Clamp the stand, support the distal side by hand, keep the wheel clear, and record whether the leg settles and returns at -8°, 0°, 5°, 10° and 15°. Stop immediately for binding, cracking, stop bypass, coil contact, guide escape or loss of pin control.

The support-free no-tyre wheel shell is a suspended mechanical-test part. The final tyre-compatible structural rim, final pin retention, encoder coupling, ground contact, spring-rate/solid-height characterisation, intentional preload and powered motion remain held. Keep the TPU tyre off this article.

The earlier loose printed-pin mock-up and detached spring caps remain accepted historical evidence only. The provisional shin was destroyed during steel-pin recovery and must not be reprinted. [Earlier owner result](evidence/assembly/2026-09-07_owner_mockup/) · [real-pin failure and corrected receiver release](evidence/knee_fit/2026-09-16_distal_d10p30_release/).
<!-- PRINT_QUEUE_END -->
