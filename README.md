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
## Current print — convenience link

**Next, if not already printed: one ABS Mode A stand** — [direct STL download](https://raw.githubusercontent.com/TnnsBeast/Biped/main/first_article_stl/mode_a/ABS_FA_RIG_Stand_M3_INSERTS_PRINT_ORIENTED.stl).

This automatically maintained convenience section lists previously released
prints still useful for fixture preparation. No new CAD or STL is released by
the September 7 physical update. [Current next steps](PROJECT_STATUS.md#immediate-next-steps-after-the-september-7-mock-up).

**Completed and accepted, September 7:** provisional distal link and temporary
pin assembled with free supported movement/easy pin removal; both detached
spring caps fit the free spring; corrected proximal link fitted with all six
hub screws seating properly. Keep these parts and the accepted shoulder hub.
[Owner photo and acceptance scope](evidence/assembly/2026-09-07_owner_mockup/).
No repeat print is requested for the completed batch.

| Part, if still needed | Quantity / material | Required import orientation and supports |
|---|---|---|
| [Mode A stand](first_article_stl/mode_a/ABS_FA_RIG_Stand_M3_INSERTS_PRINT_ORIENTED.stl) | 1 ABS | Supplied mount face down; **no supports**; needs at least 300 mm on one bed axis |
| [Cable cover](first_article_stl/assembly_dry_fit/ABS_FA_Shoulder_Cable_Cover_L_CLEARANCE_PRINT_ORIENTED.stl) | 1 ABS | Supplied bed-ready orientation, holes vertical; **no supports** |
| [Front cable post](first_article_stl/mode_a/ABS_FA_RIG_Cable_Post_A_COVER_MOUNT_PRINT_ORIENTED.stl) | 1 ABS | Supplied broad face down, holes vertical; **no supports** |
| [Wheel hub, detached motor fit only](first_article_stl/assembly_dry_fit/ABS_FA_Wheel_Hub_L_OWNED_M4x8_D5p30_PRINT_ORIENTED.stl) | 1 ABS | Supplied bed-ready orientation, bores vertical; **no supports** |

Use the tuned enclosed ABS profile. Import unchanged: no rotation, scaling or
hole compensation. Preview the stand's blind-pocket roofs and hub counterbore
bridges, and inspect their printed undersides. Keep supports off functional
faces. [Stand/post traveller](first_article_stl/mode_a/) · [Cover/hub and receiver instructions](first_article_stl/assembly_dry_fit/)
· [Insert map](docs/assembly/heatset_receiver_map.md).

**Acceptance and assembly:** coupon the exact M3 insert before fitting the
stand's five receivers. Rehearse the panel fit and bench clamp/bolt hold-down;
secure the stand before mounting the shoulder. Follow the verified order:
panel/stand and housing screws first, cover/post next, proximal link last.
The front post uses two M3 × 12 in the upper cover positions; lower positions
remain M3 × 10. Check the real tie/harness through its eye before refitting the
link. Keep the provisional distal link detached during fixture preparation;
its printed pin is only for the [supported bench rehearsal](first_article_stl/knee_mockup/).
Fit the wheel hub to its unplugged motor separately from that mock-up.

**Still held:** final distal/steel-pin/retention stack, wheel rim, spring
cartridge and complete powered fixture. The passed caps are fit coupons;
keep the spring off the leg. The complete single-leg build stays ABS; PA-CF
and structural tests remain deferred. [Teensy Stage 0](firmware/teensy_stage0/)
can proceed with USB power and both motors disconnected while the steel pin
is in transit.
<!-- PRINT_QUEUE_END -->
