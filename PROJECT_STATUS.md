# Beni project status and working guide

This is the working entry point for the project: current build state, immediate
actions, release gates, CAD hazards, authoritative documents, and reproduction
commands. For the public project overview and active print download, see
[`README.md`](README.md). Before changing the project, read
[`CLAUDE.md`](CLAUDE.md).

## Where things stand

**September 23 correction and full mechanical audit:** reprint the **shoulder
hub, proximal link and distal link** from PINREV2. The September 22 distal STL
lost its printed knee receiver and contained Ø16 despite its D10p30 filename;
the corrected receiver is Ø10.30 × 20.0. The owner also requested root-dowel
and clevis-link holes at Ø4.30 (+0.05 mm beyond the ladder selection), leaving
other pin fits unchanged. All 15 manual parts were audited. Keep the other
twelve prints: the owner confirmed the stand and shoulder plate were printed
after the Ø4.5 receiver promotion. The two ISO 7089 M4 cotter washers are not
in hand; the owner will try the unpowered article without them (1.2 mm
instead of 0.4 mm clevis-pin float, cotters bearing on ABS).
Live-CAD corruption of the upper eye and guide was repaired
without changing their correct released files. [Findings, reprint table and
regression safeguards](evidence/assembly/2026-09-23_mechanical_reprint_audit/) ·
[owner stand/plate and washer report](evidence/assembly/2026-09-23_owner_stand_plate_and_washers/).


> **Current scope decision, updated 2026-09-22 — complete the single-leg integration
> article in ABS; defer PA-CF to the two-leg structural build.** The active leg
> may be fully dry-assembled, hand-posed, wired, and commissioned with both
> motors under current limits while the wheel is clear and the printed path
> carries self-weight only. The owner-directed spring exception permits the
> released OD18 / ID9 / 50 mm cartridge at nominally zero compression at -8°
> and slow, hand-contained motion through +15°, with both motors unplugged and
> the wheel clear. This observes self-weight equilibrium only. Spring-rate and
> coil-bind characterisation, torque-arm, added-mass, ground-traction,
> stall/proof, drop and human-adjacent tests remain deferred with PA-CF.
>
> **Fixture scope remains Mode A only.** The shoulder-to-stand geometry remains
> useful for assembly and unloaded integration. The vertical MGN12 slide,
> ballast, index bar, mode pin, bumpers and drop series remain **deferred, not
> cancelled**. The CAD handoff is
> [`fusion_agent_guide_mode_a.md`](fusion_agent_guide_mode_a.md).

| | Status |
|---|---|
| **Prototype 1**, two-leg robot | Modelled, saved and verified in Fusion (`Biped → Beni_Prototype1`). The September access correction adds continuous M4 head/driver and complete screw-seat checks to `beni_lib.audit_all()`. The assembly audit and remaining release gates are linked below. Revision 2; not built. |
| **Single-leg test rig, Mode B** | **[DEFERRED]** — not the build. Its source now inherits the owner-selected Ø4.5 M3 receiver and Ø5.3 M4 receiver constants, but the stripped/deferred carriage was not rebuilt or released. Rebuild and verify it in Fusion when Mode B returns and repeat the M3 coupon for its eventual material/profile. |
| **Single-leg integration article / Mode A fixture** | **This is the active build, entirely in ABS.** The ordered-pin revision replaces the shoulder hub, proximal link, distal link, and stop plate so the purchased Ø4 × 10, M4 × 40, and Ø6 × 10 pins serve as locating, pivot, and captive-stop hardware. The actual pins selected Ø4.25; the owner now requests Ø4.30 for root-dowel sockets and clevis-link passages. The September 22 distal print failed with a missing receiver. PINREV2 corrects it and replaces the hub and both links; these three new prints are pending. The earlier stop plate and mechanical-test batch remain reusable, with Amazon pins received. Final-part pin fits, the physical D10 knee-pin checks, inserts and assembly remain open. The immediate article is an unpowered, clamped, wheel-clear, hand-contained self-weight test. Final D10 retention, encoder coupling, tyre-compatible structural rim, actual harness routing and electronics still gate powered use. |
| Electronics | Designed on paper (`electronics/`). Nothing wired. Mode A cuts Wave 0 to **~$25** plus a bench PSU. |
| Firmware | Stage 0 bench scaffold implemented and compile-verified for Teensy 4.1 in [`firmware/teensy_stage0/`](firmware/teensy_stage0/). It has no actuator command path; hardware gates remain unrun. |
| Physical hardware | **Both actuators and the 6800-2RS bearings are in hand.** Photo evidence: [`evidence/actuators/2026-08-20_received/`](evidence/actuators/2026-08-20_received/). **Spring received: Yellow / OD18 / ID9 / 50 mm free length**, matching the recommended order and both detached Ø8 pilots by physical fit. The test-only cartridge adaptation is now released; the real spring rate and solid height remain unmeasured. The ABS actuator-interface results are: GIM6010 housing PASS, original GIM6010 output Ø4.05 bore clearance FAIL followed by Ø4.15 ABS PASS, GIM4305 housing PASS with the real M2.5 screws, and GIM4305 output PASS. The owner printed the corrected Ø4.15 shoulder hub with Ø5.3 M4 receivers and successfully installed its inserts. Retain it as fit evidence; the active article now uses the ordered-pin hub with three root-dowel sockets. Continue using M3 × 8 for the eight housing screws because ×10 bottoms before clamping; the CAD/source now match this physical result. The face-flat Ø19.10 proximal link passed both bearing fits; the later wall-obstruction correction is printed, and the owner confirmed all six corrected-link screw seats on September 7. That printed link still has failed Ø4.0 M3 pockets and is superseded by the ordered-pin Ø19.15/Ø4.5 revision. Evidence: [`evidence/knee_fit/2026-09-02_proximal_link_full_depth/`](evidence/knee_fit/2026-09-02_proximal_link_full_depth/). The bought metal knee pins arrived on 2026-09-15; their count, measured diameter and tolerance evidence remain unverified. One fully seated through both installed bearings and the provisional shin. The bearings felt snug, but the owner isolated the seizure to the shin's nominal Ø10 printed bore and broke the provisional plastic shin to recover the pin. That bore is a physical FAIL; the initial 19.0 mm ladder made nominal Ø10.25 the firm-thumb candidate, and the owner conservatively selected Ø10.30 while the receiver was expected to span 21.6 mm. Fusion's subsequent service-path audit corrected the integrated receiver to the clear 20.0 mm fork gap. The ordered-pin distal link retains that Ø10.30 × 20.0 receiver and still needs physical insertion, withdrawal, spin, rock and axial-play checks. The bearing fit also needs a separate one-bearing-at-a-time hand test. [Physical result](evidence/knee_fit/2026-09-15_steel_pin_provisional_shin/) · [Fusion release](evidence/knee_fit/2026-09-16_distal_d10p30_release/). Voron-style M3 inserts plus photographed assortments are in hand. Their nominal Ø4.0 general-gauge station failed; on September 14 the owner selected the largest, unmarked-end station on the dedicated ladder, nominal Ø4.5. This is a qualitative best-fit report without a photograph, measured printed diameter, or separate spin/pull result. The mixed Kadriick case label shows 30 × M4 × 8 and 25 × M4 × 10. The owner confirmed the largest ABS M4 ladder station, Ø5.3, passed all installation and cooled-retention checks on 2026-09-04 and elected to retain M4. The September 20 pin order is in hand: 60 × Ø4 × 10 dowels, 8 × M4 × 40 clevis pins with cotters, and 15 × Ø6 × 10 dowels. The actual pins selected nominal Ø4.25 for both new calibrated interfaces. The active design consumes 3, 2, and 1 respectively; final-part visual inspection and binary hand fit remain, with no measurement requested. On September 23 the owner confirmed the printed stand and shoulder plate are post-September 14 Ø4.5 receiver prints and reported having no ISO 7089 M4 washers. The complete leg and wiring remain unfinished. |

**Owner update, 2026-09-07:** the temporary pin, provisional distal link and
two spring caps are printed, and provisional assembly succeeded. The owner
confirmed free supported knee movement/easy pin removal, both spring ends
seating flat on the detached caps without force or compression, and use of the
corrected proximal replacement with all six hub screws seating properly.
[Photo and physical acceptance scope](evidence/assembly/2026-09-07_owner_mockup/).
This is a provisional knee assembly; the complete leg and wiring remain unfinished.

**Latest M3 result and release, 2026-09-14:** the general fit gauge's nominal
Ø4.0 M3 station was too small. The owner then tested the Fusion-generated
Ø4.1–4.5 × 6.0 mm blind-pocket ladder and reported that the largest pocket,
furthest from the marker, works best. That station is nominal **Ø4.5**.
[Owner selection and limitations](evidence/inserts/2026-09-14_m3_coupon_pass/).
Fusion now uses Ø4.5 for the active stand, shoulder plate and proximal link and
for the future chassis-frame family. Both saved documents and the three active
ABS exports passed B-Rep/mesh verification. Replace any affected printed Ø4.0
part before installing M3 inserts.

**Steel knee-pin result and fit-article release, updated 2026-09-16:** the bought metal pins are now in hand.
One pin passed through both installed 6800 bearings snugly and was fully inserted
into the provisional shin, where the nominal Ø10 printed bore seized it. The
owner broke the provisional plastic shin to recover the pin and identified that
bore, rather than the bearings, as the cause of the seizure. The nominal Ø10 ×
19 mm ABS shin bore is therefore failed. Separately confirm each pin/bearing hand
fit. The owner printed the initial Ø22-boss ladder and found its largest,
unmarked-end station, nominal **Ø10.25**, gives the intended firm-thumb fit over
19.0 mm. The owner selected **Ø10.30**, one 0.05 mm step above that result,
while Fusion initially showed a 21.6 mm receiver. The final service audit found
that copying the deleted sleeve's 21.6 mm span into the printed boss overlapped
both bearing pockets and left no insertion/removal path. `Beni_SingleLegRig`
v26 now uses a Ø10.30 × 20.0 mm receiver in the clear fork gap, with 0.8 mm
clearance per side. Fusion printability, support removal, link insertion,
pin insertion, mesh and Mode A checks pass, and the bed-ready fit article is
released. Physical spin/rock/withdrawal and axial-play checks remain, while
retention and encoder coupling still gate powered use.
[Result and limits](evidence/knee_fit/2026-09-15_steel_pin_provisional_shin/) ·
[Fusion release](evidence/knee_fit/2026-09-16_distal_d10p30_release/) ·
[Optional diagnostic coupon](first_article_stl/knee_pin_fit/).

**Ordered-pin integration release, 2026-09-21:** the owner reports that the
assorted metric fasteners are already in hand. The September 20 order adds
15 × seller-listed Ø6 × 10 mm 304 stainless cylindrical pins, 60 × Ø4 × 10 mm
304 stainless cylindrical pins, and 8 × M4 × 40 mm 304 stainless single-hole
clevis pins with supplied cotters. Fusion now models those exact listed sizes.
Three Ø4 pins locate the shoulder root in purpose-built press/slip sockets; two
M4 × 40 pins cross integral 34.0 mm clevis lands plus ISO 7089 M4 washers; and
one Ø6 pin is captive between a blind distal socket and the stop plate's closed
skin. The four affected printed parts were rebuilt, motion/path audited, and
released as closed-manifold bed-ready meshes. **No owner measurement is
required.** The actual-pin ladder selection is now complete at Ø4.25 for both
the retained hub sockets and removable link passages. **[SUPERSEDED
2026-09-23: PINREV2 uses the owner-requested Ø4.30 for both.]** Visually reject damaged
hardware and perform the traveller's final-part binary checks without drilling,
filing, hammering, or screw pull-down. The hardware is not
`PHYSICAL ASSEMBLY VERIFIED` until those checks pass.
[Design evidence](evidence/assembly/2026-09-21_ordered_pin_integration/) ·
[print and assembly traveller](first_article_stl/ordered_pin_integration/).

**Ordered-pin fit result, 2026-09-22:** the actual Ø4 × 10 dowel selected the
largest root-ladder station, nominal **Ø4.25**. The owner reported a relatively
tight thumb press fit and plier removal. The actual M4 × 40 clevis pin selected
the middle station, also nominal **Ø4.25**, and was reported to work well. No
pin measurement was requested. Fusion v29 promotes Ø4.25 to the hub's 5.0 mm
blind retained sockets and both link passages, while keeping the link-side root
sockets at Ø4.25 × 5.2, cartridge eyes at Ø4.4 × 19, and stop socket at Ø6.2.
The hub/proximal/distal meshes were re-exported and released; final-part
whitening/crack inspection and pin insertion/withdrawal remain assembly gates.
**[SUPERSEDED 2026-09-23: the v29 distal export lost its Ø10.30 receiver, and
the owner then requested Ø4.30 root/clevis holes. PINREV2 replaces all three
files.]**
[Physical/Fusion evidence](evidence/assembly/2026-09-22_ordered_pin_fit_ladders/).

**Owner material update, 2026-09-22:** all four Fusion v29 ordered-pin
replacements and all parts from the earlier mechanical-test print batch are
reported printed. The Ø4 × 10, M4 × 40 and Ø6 × 10 Amazon pin families are
reported received. Reuse the earlier two cartridge eyes, guide, D10 spacer,
bracket keeper and no-tyre shell; segregate the superseded hub, links and stop
plate. The version of any printed stand/shoulder plate and availability of two
ISO 7089 M4 washers have not been reported. **[SUPERSEDED 2026-09-23: stand and
plate confirmed Ø4.5; washers not in hand.]** Printed status does not establish
insert installation, bearing fit, final-part pin fit, stop behavior or a
completed assembly. [Owner report](evidence/assembly/2026-09-22_owner_printed_parts_and_pins/).

**Unpowered ABS spring-mechanical release, 2026-09-17:** Fusion now contains
and the repository now releases two 50 mm spring eyes, a removable guide bar,
a -8°…+15° stop plate, an outboard steel-pin spacer/keeper, and a support-free
no-tyre wheel shell. The owned spring is nominally uncompressed at -8°; Fusion
gives 3.257 mm compression at 0° and 10.240 mm at +15°. A 24-pose sweep, spring
envelope, stop overtravel proof, all installation/service paths, reference-motor
guards and all seven exported meshes pass. This is a clamped, unplugged,
wheel-clear, hand-contained self-weight observation only. The actual equilibrium
angle remains a physical result because the spring rate is not measured.
[Fusion evidence](evidence/assembly/2026-09-17_abs_spring_mechanical_test/) ·
[print and assembly traveller](first_article_stl/mechanical_spring_test/).

The September 7 shoulder cable cover, corrected front cable post, wheel hub
and general fit gauge remain printed. Cover/post/harness fit and wheel-hub
insert installation/detached motor fit are still unreported.
[Owner completion record and exact files](evidence/assembly/2026-09-07_small_parts_printed/).

**Earlier corrected Ø19.15 ABS proximal link:** the Ø4.0 M3-receiver revision
was printed and its six M4 screw seats were accepted. Retain it and the earlier
accepted shoulder hub as physical evidence. The owner now reports printing the
ordered-pin replacements for the active build. Their files remain in the
[README print queue](README.md#current-print--ordered-pin-unpowered-abs-mechanical-article).
Fusion found two wall-obstructed M4 head paths and one screw seat cut into by
the large lightening opening. The corrected link clears the paths and retains
complete seating lands. The five knee M3 paths remain unobstructed and now use
the owner-selected Ø4.5 diameter in the released replacement. Those accepted
prints established the process dimensions; final-part fit of the newly printed
ordered-pin versions remains unreported.

The corrected front cable post fits outside the cover and uses two M3 × 12
screws in the upper cover positions. Its Ø8 eye lies beyond the cover edge.
The other two cover screws remain M3 × 10. Install it before the link, and
verify the real tie/harness routing during the supported dry assembly.

The complete [assembly audit, evidence and acceptance steps](evidence/assembly/2026-09-05_access_fix/)
cover the adjacent receiver and fastener families. The exact insert map stays
in [MANUFACTURING_CONSTRAINTS.md](MANUFACTURING_CONSTRAINTS.md#threaded-interfaces-in-printed-parts).
The Ø4.5 promotion is saved in `Beni_SingleLegRig` v23 and `Beni_Prototype1` v18.
The master audit reports zero problems; the rig's 49 ordered fastener paths
pass. The audit records motion-check scope and the repaired CAD screw-pose
classification issue separately from physical acceptance.
The owner confirmed the replacement's six-screw seating on September 7.
Its full-depth bearing seating/radial-rock check was not separately reported.
Its Ø19.15 bores use the previously selected easier-thumb-pressure ABS
preference; the saved assembly bearing nominal is retained.

**Still held:** the final tyre-compatible structural wheel rim (unsupported inward
ledge and retaining flange), final knee collar/pin retention, encoder coupling,
actual harness routing, and complete powered fixture/electronics acceptance. The
support-free no-tyre shell is released only for the wheel-clear mechanical test.
The wheel hub remains available for detached motor fit. The floor
contradiction concerns the future contact/load procedure and is not closed by
this access correction.

The nominal Ø10 provisional bore failed, Ø10.25 gave the intended firm-thumb
fit in the initial 19.0 mm coupon, and the owner selected Ø10.30 conservatively.
The released ABS receiver spans 20.0 mm. Record the received pin count, confirm Ø10 × 35 mm and
h6/h5 evidence, inspect the recovered pin, and test the candidates through each
bearing separately. Print the released fit article and complete its insertion,
withdrawal, spin, rock and axial-play checks. Fusion support/bridge and
assembly/service-path audits are complete; retention and encoder coupling remain held.

A deliberately clearance-fit printed ABS pin may be used meanwhile as a
**supported, hand-posed alignment mandrel only**. It does not release the distal
link, prove the bearing fit, or establish the AS5048A angular datum. Do not use a
printed pin for powered motion, main-spring installation/preload, ground contact
or any load test; support the distal-side mock-up so the pin carries no leg
weight. **The supported mock-up batch is now released, 2026-09-06:** a Ø9.7 printed
alignment pin, a provisional distal link that enters with both bearings already
installed, and two optional detached spring-seat fit caps. The mock-up omits
the original protruding thrust lands and has no axial clamp. It is not a final
distal/retention release. Follow the [print and bench traveller](first_article_stl/knee_mockup/)
for selective supports, weight support, insertion order and physical acceptance.
For this historical September 6 mock-up, the spring stays off the leg and the
caps check its ends uncompressed on the bench. Its detached-cap scope is
superseded by the separate, controlled September 17
[spring-mechanical release](first_article_stl/mechanical_spring_test/), which
uses the Ø10.30 distal article and a dedicated -8°…+15° stop. The September 7
owner report confirms the earlier batch was printed and assembled, with
supported free movement, easy pin removal and detached spring-cap fit all
passing. In parallel, run
firmware/electronics Stage 0 with both motors disconnected. See the exact bore map in
[`print_stl/README.md`](print_stl/README.md). The GIM4305 procedure and
non-nesting explanation are in the illustrated
[`2026-08-22 actuator-coupon test guide`](evidence/actuator_fit/2026-08-22_coupon_test_guide/README.md).
They were built from the manufacturer STEP datums in Fusion and are ready to use
with the real actuators as go/no-go fixtures, so calipers are **not a blocker**.
The old `GAUGE_*_Motor_Interface.stl` files remain positive motor stand-ins and
are not substitutes for these mating coupons. The optional Mode A cable anchor
is in `first_article_stl/mode_a/`. PA-CF coupons and structural prints are now
deferred to the later two-leg build.

## Immediate next steps after the September 23 PINREV2 correction

1. Reprint the PINREV2 hub and both links, retain the closed-skin stop plate and
   six mechanical-test parts, then follow the
   [ordered-pin assembly traveller](first_article_stl/ordered_pin_integration/README.md#ordered-assembly)
   from its [kit check](first_article_stl/ordered_pin_integration/README.md#kit-check).
   Inspect printed fit faces and the stop plate's closed skin. The stand and
   shoulder plate in hand are owner-confirmed Ø4.5 receiver prints; no fixture
   part needs printing. Without the two ISO 7089 M4 washers, inspect both
   cotter faces after the hand test and fit washers before any repeated
   cycling or powered use.
2. Complete the detached bearing, D10 steel knee-pin, root-screw, guide and
   clevis fits first. Install inserts in the **new hub and proximal link**,
   plus current stand, plate and wheel hub as needed. Seat the three Ø4 × 10
   dowels in the hub, hand-mate the proximal root, assemble the knee with the
   real steel pin, then capture the Ø6 × 10 stop pin with the new plate. Prove
   the -8° and +15° stops with the spring absent. Any failed fit stops the
   sequence; no drilled or forced repair is an accepted first article.
3. Reuse the reported printed cartridge eyes, guide, D10 spacer, bracket
   keeper and no-tyre wheel shell after their detached checks. Follow the
   [September 17 spring sequence](first_article_stl/mechanical_spring_test/README.md#assembly-order)
   at the -8° stop with the stand clamped, motors unplugged, wheel clear and
   distal side hand-contained. Move slowly through -8°, 0°, 5°, 10° and 15°.
   Stop at the first bind, crack, stop bypass, coil contact, guide escape, or
   loss of pin control. Final D10 retention and encoder coupling still gate
   powered use.
4. Inspect the already printed cable cover, front post and wheel hub. Their
   inserts, detached motor fits and actual harness routing remain physical
   checks; printing does not close them. The rear cable anchor remains optional.
5. Run [Teensy Stage 0](firmware/teensy_stage0/) in parallel: USB power, both
   motors disconnected, internal CAN loopback, BNO085 acquisition and the
   microSD gate. Hardware results are still owed; the prior compile is not a pass.
   The final tyre-compatible structural rim, final pin retention, encoder
   coupling, spring-rate/solid-height characterisation and powered motion remain
   held for later work.

The ordered-pin proximal link retains the accepted Ø19.15 bearing seat and Ø4.5
M3 receiver values. The Mode A stand and conditional shoulder plate remain the
Ø4.5 releases from the September 14 result. Motor commissioning waits for the
final mechanical, fixture, harness, and electronics gates.

---

## The active Fusion documents

| Document | What it is |
|---|---|
| `Beni_Prototype1` | The complete two-leg robot. **Master — do not edit casually.** |
| `Beni_SingleLegRig` | The active ABS integration rig, saved as v30 on 2026-09-23 (PINREV2). It contains the test-only 50 mm cartridge eyes/guide, owner-requested Ø4.30 ordered-pin shoulder-root sockets and clevis-link passages, the restored Ø10.30 × 20.0 knee receiver, captive Ø6 × 10 stop, outboard D10 pin spacer/keeper, no-tyre wheel shell, and owned-spring reference envelope. |
| `Beni_Knee_Supported_DryFit` | Separate saved ABS bench mock-up, v1. Temporary pin and provisional distal link; spring caps are detached fit coupons. [Save and native re-inspection record](evidence/assembly/2026-09-06_supported_knee_mockup/fusion_document.json). |
| `Beni_Prototype1_TestGauges` | Fit gauges and the four ABS actuator-interface coupons. |

⚠ **In `Beni_SingleLegRig`, deleting any occurrence displaces both motor STEP
references** (the shoulder grows Y 5…49 → 5…75, the wheel motor moves 140 mm),
inventing clashes that have nothing to do with the design. Reproducible.
`isSuppressed = True` is **not** a workaround — the property is not readable on
this API build, so the assignment lands on the Python wrapper and changes nothing.
**Capture `transform2` for both `REF_*` occurrences and every child in their trees,
delete, then write them back and assert the bounding boxes.** After any structural
edit, `REF_GIM6010-8` must read Y 5.00…49.00 and `REF_GIM4305-10` Y 61.50…94.50.
Rig design record §6.2.

---

## Documents, in reading order

### The single-leg rig — build this first
| File | What it is |
|---|---|
| [`fusion_agent_guide_mode_a.md`](fusion_agent_guide_mode_a.md) | **The CAD handoff for the Mode A build.** Everything a Fusion agent needs to model `RIG_Stand` and the reduced part set: verified load table, the 42.00 mm overhang, the mount interface, the check list, and the model-corrupting traps. Read this before touching the model. |
| [`docs/assembly/ordered_pin_picture_guide.md`](docs/assembly/ordered_pin_picture_guide.md) | **Current illustrated assembly manual.** 23-page printable PDF and page gallery: visual parts key plus 21 operations with native Fusion v30 exploded views, insertion arrows, hardware and fit checks. Covers the unpowered article; physical assembly acceptance remains pending. |
| [`docs/assembly/shoulder_to_proximal_link.md`](docs/assembly/shoulder_to_proximal_link.md) | **Shoulder close-up.** Shows the verified plate-first, hub-second GIM6010 sequence and how the printed proximal link attaches to the shoulder hub. |
| [`docs/assembly/heatset_receiver_map.md`](docs/assembly/heatset_receiver_map.md) | **Picture insert map.** Shows every active receiver/clearance part, install direction, screw length, and corrected bed-ready STL. |
| [`ASSEMBLY_VERIFICATION.md`](ASSEMBLY_VERIFICATION.md) | **The physical-assembly release gate.** Required insertion-order/path, tool access, cable path, service path, and first-article rehearsal checks. |
| [`fusion_brief_single_leg_rig.md`](fusion_brief_single_leg_rig.md) | **The brief.** What the rig must do and why it is a dynamics rig, not a fit check. Amended 2026-08-17 for Mode A. |
| [`beni_single_leg_rig_design_record.md`](beni_single_leg_rig_design_record.md) | **The answer, and the authoritative rig document.** As-built design, all six checks, mass properties, eleven departures from the brief, purchase list. **§6.2's five measurement traps are the most reusable content in the project.** Mode B sections carry `[DEFERRED]` banners; the leg content is unaffected. |
| [`beni_rig_no_machining.md`](beni_rig_no_machining.md) | Companion: the canonical PA-CF print settings with per-setting reasoning, and the load arithmetic behind the printed-part routing. |
| [`rig_stl/README.md`](rig_stl/README.md) | What to print, in what orientation, and what will bite on each part. |

### Prototype 1 — the robot
| File | What it is |
|---|---|
| [`beni_prototype1_fusion_guide_rewritten.md`](beni_prototype1_fusion_guide_rewritten.md) | **Frozen kinematics** (§4–§9) and the requirements freeze. Do not change without demonstrating a failure. |
| [`beni_prototype1_design_record.md`](beni_prototype1_design_record.md) | As-built record: motor interfaces measured from STEP (§2), the authoritative lateral Y-stack (§3), load cases, mass properties (§14). |
| [`beni_prototype1_bom_and_assembly.md`](beni_prototype1_bom_and_assembly.md) | BOM, fastener schedule, and the assembly sequence with torques. |
| [`beni_prototype1_rev2_changes.md`](beni_prototype1_rev2_changes.md) | The fourteen defects closed in revision 2, and the Fusion/scripting failure modes found doing it. |

### Electronics
`electronics/` — power and battery, harness, compute and CAN, firmware, open
questions, logging and bring-up, BOM. Entry point:
[`electronics/README.md`](electronics/README.md). The CAD-derived geometry every
other electronics document is designed against — coordinate frame, inertia table,
free-space map, spring table — is
[`electronics/00_mechanical_datum.md`](electronics/00_mechanical_datum.md).

**`electronics/01`–`06` describe the two-leg robot**, which is not the active
build. Each carries a carve-out noting what the rig deletes (no pack, no BMS, no
custom PCB, no satellite nodes, no clock springs — a Teensy 4.1 on a 20 V bench
supply). `electronics/07_bom.md` Wave 0 is the rig's electronics shopping list.

### Archive
`archive/` — kept for provenance, not for building.

| | |
|---|---|
| [`archive/prototype1_production_readiness_audit.md`](archive/prototype1_production_readiness_audit.md) | The audit that drove revision 2, condensed. Its mass figures are superseded — the file says so. |
| `archive/manufacturing/` | The ten machined families **as originally designed**, with the fits and tolerances the printed substitutes must still meet. |
| `archive/laser/` | **Retired.** The steel stop-arc and ballast DXFs. `stop_arc_loops.json` is the only surviving source for the stop-arc profile. |

---

## Code

Everything geometric is scripted, so the models are reproducible rather than
hand-built.

| File | Runs where | What it does |
|---|---|---|
| `beni_lib.py` | inside Fusion | Builds every part of the robot (`build_all()`, `build_mirror()`), poses it (`set_pose()`), and audits it (`audit_all()`). |
| `beni_export.py` | inside Fusion | STEP per part, URDF + inertia JSON with a mass-closure assert, print STLs, viewer STLs. |
| `rig_lib.py` | inside Fusion | Builds every `RIG_*` part, including the completed Mode A `build_rig_stand()`, the §4.4 check suite (`checks_44()`), the Mode B travel harness (`slide_to()`), and an interference reporter whose names actually resolve (`real_clashes()`). The rail/block/carriage/index/pin/bumper/ballast builders and `check3_mode_b_travel()` are deferred with Mode B. |
| `rig_calc.py` | plain `python3` | Independent recomputation of the brief's arithmetic: spring curve, drop series, MGN12H moments, travel budget, mass budget, bounce mode, torque arm, and **`mode_a_stand()` — the verified Mode A load set** (42.00 mm overhang, the four moments, the tipping table, the step-6 mass/φ table). |
| `rig_export.py` | inside Fusion | Rig STLs, the targeted Mode A anchor, and the transient ABS-calibrated shoulder-hub first article, with print orientation recorded per part. |
| `first_article_fusion.py` | Fusion MCP | Builds, validates and exports the ABS actuator coupons, 6800 ladder, full-depth knee-pin bore ladder and proximal first article in `Beni_Prototype1_TestGauges`. |
| `knee_mockup_fusion.py` | Fusion MCP | Creates the separate supported ABS knee mock-up, temporary pin and detached spring-seat caps; checks assembly/support paths and exported meshes. |
| `distal_first_article_fusion.py` | Fusion MCP, with `Beni_SingleLegRig` active | Audits the Ø10.30 × 20.0 mm distal receiver, link and pin service paths, four selective-support regions and the bed-ready mesh; writes the v26 release evidence. |
| `mechanical_spring_test_fusion.py` | Fusion MCP, with `Beni_SingleLegRig` active | Builds and audits the unpowered 50 mm spring cartridge, guide, -8°…+15° stop, outboard pin keeper stack and no-tyre wheel shell; exports the seven bed-ready ABS files and September 17 evidence. |
| `ordered_pin_integration_fusion.py` | Fusion MCP, with `Beni_SingleLegRig` active | Releases the four ordered-pin parts (PINREV2 hub/links plus the stop plate) around the ordered Ø4 × 10, M4 × 40, and Ø6 × 10 hardware; verifies meshes and writes the ordered-pin manifest/evidence. `refresh_images()` recaptures their release images without rewriting the STLs. |
| `mechanical_release_audit_fusion.py` | Fusion MCP, with `Beni_SingleLegRig` active | The fail-closed release gate: `assert_all()` checks 32 measured interface contracts and every native face of the 15 printed parts against the reviewed `mechanical_release_baseline.json`; `assert_export()` checks each bed-ready mesh fingerprint. Exporters call it; they never update the baseline. |
| `verify_mechanical_release.py` | plain `python3`, also GitHub CI | Byte-hash gate: the 15 released STLs and the Fusion-verified source files must match the baseline. A changed source fails until it is re-verified in Fusion and its hash is updated deliberately. |
| `ordered_pin_fit_ladders_fusion.py` | Fusion MCP, with `Beni_SingleLegRig` active | Generates the September 22 root-dowel and clevis-passage ABS ladders in a temporary unsaved Fusion document, verifies their controlled orientations/B-Reps/meshes, and leaves the active rig unmodified. |
| `readme_images_fusion.py` | Fusion MCP, with `Beni_Prototype1` active | Refreshes the full-robot, complete-leg, wheel-module, and knee-detail images used by the project homepage. |
| `stl_inspect.py` | plain `python3` | Recovers circular features from an STL mesh. Used to check the GAUGE coupons against the design record. |
| `fusion_bridge/` | both sides | Lets an agent without Fusion read the live model. `bridge.py` (plain `python3`) validates requests and reads results; `probe.py` + `ops.py` run inside Fusion. See [`fusion_bridge/PROTOCOL.md`](fusion_bridge/PROTOCOL.md). |
| `firmware/teensy_stage0/` | PlatformIO / Teensy 4.1 | Non-energizing Stage 0 scaffold: dual 500 kbit/s internal CAN loopback, BNO085 raw SPI acquisition and a 256 kB/s onboard-microSD gate. |

Reproduce the rig model:

```python
import sys; sys.path.insert(0, '/Users/neilchulani/Personal/Biped')   # this machine's checkout
import rig_lib
rig_lib.checks_44()          # the six §4.4 release checks
rig_lib.real_clashes()       # interference, artifacts classified out
import mechanical_release_audit_fusion as A; A.assert_all()   # release gate
```

```
python3 rig_calc.py          # every number in the design record, recomputed
python3 verify_mechanical_release.py   # released-file and verified-source hashes
```

Mode A numbers only (the full script is slow):

```
python3 -c "import rig_calc; rig_calc.mode_a_stand()"
```

---

## Outputs

| Directory | Contents |
|---|---|
| `rig_stl/` | Rig parts to print, plus `reroute/` — the formerly-machined parts, now printed. `reroute/Distal_Link_L.stl` supersedes the `print_stl/` copy. |
| `first_article_stl/` | **Print this first.** ABS actuator mating coupons, the unloaded shoulder dry-fit batch, the optional Mode A cable anchor, Fusion manifests and mesh checksums. |
| `print_stl/` | Robot parts to print, the fit coupon, the two motor gauges |
| `sim/` | `beni.urdf` and `beni_inertia.json`, real inertias, mass closure asserted |
| `web/` | Browser viewer for posing the robot without Fusion |
| `snapshots/` | Timestamped model snapshots for Prototype 1 and the Mode A rig |
| `evidence/` | Dated physical-hardware photographs and observation indexes |
| `procurement/` | Dated purchasing workbooks; canonical requirements remain in the engineering BOM documents |
| `archive/manufacturing/step/` | STEP per part family (from when they were to be machined) |

---

## Known-unresolved, and gating

| | |
|---|---|
| **C2** | Shoulder motor length, 40 vs 44 mm. Manufacturer STEP and live Fusion geometry use **44.0000 mm nominal**. The existing positive stand-in is only 9.5 mm long, so it cannot report exact overall hardware length; use the delivered motor against a negative ABS mating coupon or the actual ABS mating part as a functional go/no-go. No structural consequence in the rig. |
| **C3** | Wheel motor length, 26 vs 33 mm. Manufacturer STEP and live Fusion geometry use **33.0000 mm nominal**. The existing full-length gauge is a positive stand-in; close assembly fit by placing the real motor into a negative ABS coupon or the actual ABS mating part. |
| **C4** | Actuator masses, 388/150 vs 500/250 g. ~~Decides whether rig ballast is 37.5 g or 149.5 g of shot.~~ **Mode A has no ballast, so this decides nothing structural in the rig** — it still matters to the two-leg mass and power budgets. Weigh them. |
| **B1** | Wheel-driver max bus voltage unconfirmed. Run the rig at 20 V. |
| Clock spring | Highest-risk mechanical item. **Gets no validation in the rig build** — deleted for it. Moves to the two-leg build still unproven. |
| Drop behaviour | **Now in the same category as the clock spring.** Mode A runs no drops, so the 45 mm passive limit, the φ_peak curve and `A_MAX` all move to the two-leg build unmeasured. Deliberate, and recorded in rig design record §11. |
| Main knee spring | **Owned and correct by ordered variant:** Yellow / OD18 / ID9 / 50 mm. Owner confirmed 5 cm on 2026-09-06; the earlier 15 cm report was a typo. No wrong-delivery or replacement-order hold remains. A test-only Ø8-pilot cartridge is released for the unpowered -8°…+15° ABS mechanical article. The owned spring's rate and solid height, intentional preload, and the final PA-CF cartridge remain unresolved. [Spring record](evidence/springs/2026-09-05_reconciliation/) · [test release](evidence/assembly/2026-09-17_abs_spring_mechanical_test/). |
| Brake chopper | Deferred with Mode B, and **still uncomputed** (~21.5 V on / ~20.8 V off). ⚠ Until it is built, nothing may backdrive a motor. |
| Creep | Printed joints relax silently. Re-torque after the first hour, then periodically. Inspect the printed hub's dowel holes after every drop session. |
| Stand hold-down | **New in Mode A.** 11.00 N·m of shoulder yaw needs 11.2 kg at a 100 mm base half-width, 5.6 kg at 200 mm, 3.7 kg at 300 mm. The modelled stand is **574.2 g**, so it **must be clamped to the bench, not weighted.** Four clamp landings and 4 × M6 bench-bolt holes are in the CAD; the unloaded bench pull-test has no CAD equivalent and is still owed. |

### Open inconsistencies in the documents

Found during the 2026-08-17 cleanup and **not** resolved, because resolving them
needs a judgement call on the engineering:

- **Clock-spring capacity, 470° vs 430°.** `beni_prototype1_design_record.md` §4
  computes `L(1/rᵢ − 1/rₒ) ≈ 8.2 rad ≈ 470°` with "27 % margin" against the 370°
  needed; §13's acceptance checklist says the same cavity gives **430°**. Same
  geometry, two answers. Note 470/370 = 1.27, so the stated margin agrees with
  470 and not with 430. Separately, `electronics/02_harness_and_routing.md` §2.2
  recomputes the usable margin as **~5 %, not 27 %**.
- **Convex-substitute Hertzian ceiling.** `MANUFACTURING_CONSTRAINTS.md` says
  1.0–2.0 GPa; the rig design record §0 says 1.0–1.8 GPa (its §8 table lists
  2021 / 1808 / 1023 MPa).
- **7075-T6 subtotal**, 251.8 g (BOM §4 table) vs 251.7 g (BOM §8 roll-up).
- ~~**No rig snapshot.**~~ **[RESOLVED 2026-08-20]** `snapshots/2026-08-20_rig-mode-a/`
  now holds `Beni_SingleLegRig_ModeA.f3d`, `.step`, `mode_a_metrics.json` and a
  README, and the live document was saved as a named cloud version. Verified
  clean before and after: `ref_assert()` and `placed_assert()` both True,
  `checks_44()` all seven PASS.

### Found while exporting `RIG_Stand` (2026-08-20), and reported not resolved

- **`rig_stl/README.md` §9 bench-bolt pattern was wrong for the built part.**
  §9 read "X = ±88 and ±26"; `rig_lib.py:1625` is
  `STAND_BOLT_X = (-88.0, -26.0, 34.0, 88.0)` and the model measures **+34, not
  +26** — the set is asymmetric. Corrected at the row in §9 on 2026-08-20 with
  the constant cited. Recorded here because it was a *drill-pattern* error on the
  hold-down of a 574 g stand that must be clamped against 11.00 N·m of yaw; if
  any other document repeats the symmetric "±26", it is also wrong.
- **§9's second clamp landing was 11.5 mm long.** §9 recorded −43.5…−8;
  `checks_44()` check 7 measures **−32.0…−8.5** (23.5 mm, not 35.5). Still over
  the 20 mm minimum, so check 7 passes and nothing structural changes. Corrected
  inline in §9.
- ~~**`RIG_Cable_Post_B` has no Mode A geometry.**~~ **[RESOLVED 2026-08-20].**
  Post B correctly remains deferred with the deleted Mode B column.  Mode A now
  has a separate `RIG_Cable_Anchor_ModeA` on the two upper rear GIM6010 housing
  screws: 4 mm thick, clear of the Ø57 driver cover, zero modeled interference,
  and exported under `first_article_stl/mode_a/` for an ABS first article.
- **Guide §2.4 assumed a ~0.3 kg stand; the built part is 574.2045 g.** Reported
  as strengthening §2.4's hold-down conclusion rather than weakening it, but the
  assumed figure should be corrected where it is written. Related: `rig_calc`
  quotes bearing on an 8 mm wall where the built web is 12 mm — **unverified, and
  it was reported alongside a claim I could not reproduce (below), so treat it as
  needing a second look rather than as established.**
- **Reported but NOT reproduced — do not act on it.** The 2026-08-20 Fusion run
  also claimed `ARTIFACT_PAIRS`'s comment says the torque-arm pair is filtered
  while `_is_artifact()` has no such entry. Read directly: `ARTIFACT_PAIRS`
  (`rig_lib.py:773-792`) contains `('Cart_Lower_Eye_L',
  'RIG_Knee_Bumper_Tube_L')` — the cartridge tube — and `STEP2_FIXTURES`
  (`rig_lib.py:799`) is a separate constant with an accurate comment. No comment
  claims the torque-arm pair is in `ARTIFACT_PAIRS`; the two constants were
  conflated. The `Proximal_Link_L ↔ RIG_Torque_Arm` clash (14634.6 mm³) that
  prompted it **is** expected: bare `real_clashes()` does not filter
  `STEP2_FIXTURES`, only `checks_44()` does. Logged so it is not re-filed.

### Found while modelling `RIG_Stand` (2026-08-17), and reported not resolved

- **Guide §2.5 "shoulder axis ≥ 221.31 mm above the floor plate" vs guide §3
  "`RIG_Floor_Plate` … Unchanged".** The shoulder axis *is* the model origin, so
  the requirement cannot be met by a stand height — it lands on the floor plate,
  whose `build_rig_floor()` top face was `Z_FLOOR = −209.269` (the φ = 0 contact
  plane), **12.04 mm too high.** Resolved in favour of §2.5 as the harder
  requirement: the Mode A floor plate is re-datumed to the bench at
  `Z_FLOOR_A = −221.3119`, and `Z_FLOOR` is retained for the Mode B slide. Also
  re-datumed for the same reason: `RIG_Scale_Pedestal`, which stood on the
  deleted 2020 base.
- **≥ 221.31 mm and "the wheel rolls ~77 mm during a shoulder sweep" are
  mutually exclusive with a rigid stand.** Datuming the floor to the −8° reach
  makes the leg longest exactly at the contact point, so rotating the shoulder can
  only *lift* the wheel: at φ = −8 the wheel axis is 4.000° off plumb at
  r = 166.718, so it touches only for θ ∈ 0…+8.00° — an **8.00° window, ~23 mm of
  roll, not ~77 mm.** Loading the wheel through a sweep needs the floor *above*
  the −8° reach, which pre-compresses the knee and takes the leg off the extension
  stop that brief §6 says it rests on. 221.31 mm is the only height that satisfies
  "≥ 221.31" *and* leaves the floor touching at all. **Which of the two the rig
  actually needs is an engineering call, not a CAD one.**
- **Step 6's loading direction is unspecified, and the sign looks wrong.** Brief §6
  and `rig_calc.mode_a_stand()` tabulate "known masses on the wheel → φ" using
  `ground_force(φ)`, which is the *upward* force a grounded wheel carries. A mass
  hung on the wheel of a leg suspended at θ = 0 pulls **down**, which extends the
  knee onto its −8° stop instead of flexing it — and with the wheel resting on the
  floor and the shoulder rigid, φ is fixed by geometry and adding mass changes
  nothing. By the closed form the moment reverses sign at θ = 50.0°, so hung
  masses only flex the knee with the shoulder driven past +50°. **The step-6 table
  is not wrong as a φ-vs-force curve; what is missing is how the force is
  applied.** No CAD consequence, but it gates the one measurement Mode A exists for.
- **The repo records no modulus for PA-CF**, only strengths (84–102 MPa XY,
  26–50 MPa Z). Guide §2.6 and `beni_rig_no_machining.md` §3 both say the stand is
  now the softest element in the load path and that "stiffness here is measurement
  quality" — but there is no traceable E to compute a deflection or a
  shoulder-angle error from. The stand is designed to keep the dominant load
  in-plane and axial (0.28 MPa in the rails at stall) rather than to a stiffness
  number.
- **No print envelope is stated anywhere.** `RIG_Stand` is 200 × 32 × 299.3 mm and
  needs a bed ≥ 300 mm in one axis; the largest part accepted so far is
  `RIG_Index_Bar` at 280 mm. The 299.3 mm is not reducible — it is the 227.31 mm
  ride height plus the mount pad.
- **Guide §4 check 2 says "the stand joins [the exclusion list]".** Taken
  literally that would exclude the stand from the very check whose purpose is to
  prove nothing fouls it. Implemented the other way: the stand is checked, and it
  comes out clean at all 17 angles because its Y band (10…42) is disjoint from
  every moving part (≥ 45.49).
