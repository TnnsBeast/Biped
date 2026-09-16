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

**Next: calibrate the received steel knee pin in the full-depth ABS ladder** — [direct STL download](https://raw.githubusercontent.com/TnnsBeast/Biped/main/first_article_stl/knee_pin_fit/ABS_CAL_KNEE_PIN_BORE_LADDER_PRINT_ORIENTED.stl). Print it alone in ABS from the supplied orientation and start at the two-hole Ø10.05 end. The [Ø4.5-receiver proximal replacement](first_article_stl/assembly_dry_fit/ABS_FA_Proximal_Link_L_D19p15_M4_ACCESS_FIXED_PRINT_ORIENTED.stl) remains next in the integration queue.

This automatically maintained convenience section lists previously released
prints still useful for fixture preparation. The nominal Ø4.0 M3 station in the
general gauge failed, and the owner selected the largest station on the new
same-profile ladder: **Ø4.5 × 6.0 mm**. Fusion now carries Ø4.5 throughout the
active ABS M3 receiver family. [Selection and Fusion verification](evidence/inserts/2026-09-14_m3_coupon_pass/).

**Completed and accepted, September 7:** provisional distal link and temporary
pin assembled with free supported movement/easy pin removal; both detached
spring caps fit the free spring; corrected proximal link fitted with all six
hub screws seating properly.
[Owner photo and acceptance scope](evidence/assembly/2026-09-07_owner_mockup/).
Keep the surviving parts and the accepted shoulder hub. That acceptance applies
only to the loose printed-pin mock-up.

**Steel-pin update, September 15:** one received metal pin passed snugly through
the installed bearings but seized in the provisional shin's nominal Ø10 printed
bore. The owner broke the provisional plastic shin to recover the pin. Do not
repeat that bore in another full link. The released full-depth ladder reproduces
the final Ø22 × 19 mm boss at Ø10.05–Ø10.25 in 0.05 mm steps. [Physical result](evidence/knee_fit/2026-09-15_steel_pin_provisional_shin/) · [Ladder instructions](first_article_stl/knee_pin_fit/).

**Also printed, September 7:** shoulder cable cover, corrected front cable
post, wheel hub and general fit gauge. These four prints are complete; the
gauge's M3 station later failed. Motor-fit and cover/post/harness checks remain pending.
[Owner completion record](evidence/assembly/2026-09-07_small_parts_printed/).
The general gauge supplied only one M3 candidate; its nominal Ø4.0 hole is an
owner-reported FAIL. The dedicated ladder has since selected Ø4.5.

| Part, if still needed | Quantity / material | Required import orientation and supports |
|---|---|---|
| [Knee-pin full-depth bore ladder](first_article_stl/knee_pin_fit/ABS_CAL_KNEE_PIN_BORE_LADDER_PRINT_ORIENTED.stl) | 1 ABS calibration print | Import unchanged with the thin runner on the bed; **no supports**. Two index holes mark Ø10.05; stations increase to Ø10.25 in 0.05 mm steps. |
| [Corrected proximal link, Ø4.5 M3 revision](first_article_stl/assembly_dry_fit/ABS_FA_Proximal_Link_L_D19p15_M4_ACCESS_FIXED_PRINT_ORIENTED.stl) | 1 ABS replacement | Import unchanged with the outboard arm face down; **no supports**. Inspect the controlled bridge undersides and Ø17 bearing-retention lips. |
| [Mode A stand, Ø4.5 M3 revision](first_article_stl/mode_a/ABS_FA_RIG_Stand_M3_INSERTS_PRINT_ORIENTED.stl) | 1 ABS, separate plate | Import unchanged with the mount face down; **no supports**; requires at least 300 mm on one bed axis |
| [Rear Mode A cable anchor — optional](first_article_stl/mode_a/RIG_Cable_Anchor_ModeA.stl) | 1 ABS | Rotate this assembly-coordinate file onto either broad face; **no supports** |
| [Shoulder plate, Ø4.5 M3 revision](first_article_stl/assembly_dry_fit/ABS_FA_Chassis_Shoulder_Plate_L_M3_INSERTS_PRINT_ORIENTED.stl) | 1 ABS if the fitted plate is the prior Ø4.0 revision | Import unchanged with the full inboard panel face down; **no supports** |

Use the tuned enclosed ABS profile. Import the `PRINT_ORIENTED` files unchanged:
no rotation, scaling or hole compensation. The optional rear anchor is the
exception: lay either 41.0 × 15.45 mm broad face on the bed, as described in its
traveller. Preview the stand's blind-pocket roofs and the proximal link's
channel/root-pad bridges, then inspect their printed undersides. Keep supports off functional
faces. [Stand/post traveller](first_article_stl/mode_a/) · [Link, plate and receiver instructions](first_article_stl/assembly_dry_fit/)
· [Insert map](docs/assembly/heatset_receiver_map.md).

The owner reports that the unmarked-end, largest M3 ladder pocket works best.
That station is nominal Ø4.5. This is a qualitative same-profile ABS selection;
no measured printed diameter, photograph, or separate spin/pull result was
supplied. Repeat the coupon before the later PA-CF build. [Full M3 result](evidence/inserts/2026-09-14_m3_coupon_pass/).

**Acceptance and assembly:** the Ø4.5 source and the three affected ABS exports
have passed Fusion B-Rep and mesh verification. Replace the already printed
corrected proximal link because its five pockets are the failed Ø4.0 revision.
Print the stand next, and replace a fitted Ø4.0 shoulder plate before installing
its four cover inserts. Then rehearse the panel fit and bench clamp/bolt hold-down;
secure the stand before mounting the shoulder. Follow the verified order:
panel/stand and housing screws first, cover/post next, proximal link last.
The front post uses two M3 × 12 in the upper cover positions; lower positions
remain M3 × 10. Check the real tie/harness through its eye before refitting the
link. The optional rear anchor uses two M3 × 8 plus washers and fits before
enclosing the rear wiring. The provisional distal link was destroyed during
steel-pin recovery; retain its earlier result as evidence only. Its printed pin
was limited to the [supported bench rehearsal](first_article_stl/knee_mockup/).
Fit the wheel hub to its unplugged motor separately.

**Still held:** final distal/steel-pin/retention stack, wheel rim, spring
cartridge and complete powered fixture. The passed caps are fit coupons;
keep the spring off the leg. The complete single-leg build stays ABS; PA-CF
and structural tests remain deferred. [Teensy Stage 0](firmware/teensy_stage0/)
can proceed with USB power and both motors disconnected while the received
steel pin is inspected and the released bore ladder selects the shin compensation.

The TPU tyre remains coupled to the held rim. Knee stop/encoder parts and the
magnet carrier have legacy STLs but are not added to this print batch: full
knee assembly still awaits corrected steel-pin bore selection and retention,
and their current bed-ready
print release needs verification before adding them to this queue. Cartridge
eyes and the internal bumper await the owned-spring adaptation. Two-leg and
Mode B parts are deferred.
<!-- PRINT_QUEUE_END -->
