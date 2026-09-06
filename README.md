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

**Next: one temporary ABS knee pin** — [direct STL download](https://raw.githubusercontent.com/TnnsBeast/Biped/main/first_article_stl/knee_mockup/ABS_MOCKUP_Knee_Alignment_Pin_D9p7_PRINT_ORIENTED.stl).
Then print the [provisional distal link](https://raw.githubusercontent.com/TnnsBeast/Biped/main/first_article_stl/knee_mockup/ABS_MOCKUP_Distal_Link_L_PRINT_ORIENTED.stl) for the supported two-link bench assembly.

This automatically maintained section links the next verified print batch.
The corrected proximal link is printing; keep the accepted shoulder hub.
[Full print, support and assembly traveller](first_article_stl/knee_mockup/).

| Part | Quantity / material | Supplied orientation and support policy |
|---|---|---|
| Temporary Ø9.7 pin | 1 ABS | Grip on bed, shaft vertical; 0.20 mm layers, 4 walls, 100% infill; **no supports** |
| Provisional distal link | 1 ABS | Broad wheel-end face down, all bores vertical; **manual supports only in the two pictured regions** |
| [Spring-seat fit caps](https://raw.githubusercontent.com/TnnsBeast/Biped/main/first_article_stl/knee_mockup/ABS_Spring_Seat_Fit_Cap_D8_PRINT_ORIENTED.stl) | 2 ABS, optional | Broad base down, pilot vertical; **no supports**; try the free spring off the leg |

Import unchanged: no rotation, scaling or hole compensation. Use the tuned
ABS enclosure profile; the link and caps use 0.20 mm layers, 4 walls,
5 top/bottom layers and 30% infill. A brim is allowed. For the distal link,
follow the pictured support guide: 0.6 mm XY clearance, 0.4 mm top/bottom gap,
and no support in bores or on mating/bearing surfaces. Preview the support
removal paths and controlled bridges before printing.

**Acceptance:** the pin must slide freely through each bearing and the distal
bore by hand. Support both detached links on the bench, slide the distal tongue
into the fork, then insert the pin through both bearings and the tongue. No
thrust spacers or axial clamp are fitted. Gently hand-position and disassemble
once without force or rubbing. The older proximal print is usable for this
bench rehearsal if both bearings are seated and their lips are intact.

**This is a temporary, loose mock-up.** Keep motors, spring cartridge, stop
hardware, encoder and collar off it. Support both links so the pin carries no
leg weight. The distal mock-up may need replacement when the real steel pin
and retention stack are resolved. The two caps test the spring ends separately,
uncompressed; cartridge adaptation remains unfinished.

The [corrected proximal link](https://raw.githubusercontent.com/TnnsBeast/Biped/main/first_article_stl/assembly_dry_fit/ABS_FA_Proximal_Link_L_D19p15_M4_ACCESS_FIXED_PRINT_ORIENTED.stl)
is already printing. Its [traveller](first_article_stl/assembly_dry_fit/) retains
the six M4 screw-seat and bearing-fit acceptance checks and links the shoulder
plate, cover and wheel hub. The accepted hub stays in use. The corrected
[front cable anchor](first_article_stl/mode_a/ABS_FA_RIG_Cable_Post_A_COVER_MOUNT_PRINT_ORIENTED.stl)
uses two M3 × 12 in the upper cover positions; lower positions remain M3 × 10.

**Still held:** final distal/steel-pin/retention stack, wheel rim, spring
cartridge and the complete wired fixture. This batch does not release powered
motion or spring loading. The complete single-leg build stays ABS; PA-CF and
structural tests remain deferred.
<!-- PRINT_QUEUE_END -->
