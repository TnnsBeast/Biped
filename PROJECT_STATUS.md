# Beni project status and working guide

This is the working entry point for the project: current build state, immediate
actions, release gates, CAD hazards, authoritative documents, and reproduction
commands. For the public project overview and active print download, see
[`README.md`](README.md). Before changing the project, read
[`CLAUDE.md`](CLAUDE.md).

## Where things stand

**September 25 architecture reset — Active-Knee Revision 2 (R2A):** the owner
has selected a remotely actuated, belt-driven knee as the replacement direction.
A newly available Beni teardown shows two shoulder-area brushless motors on the
same axis and a toothed-belt reduction controlling the knee. That evidence
invalidates the project's prior assumption that Beni used a passive spring knee.
The active work item is now the
[R2A architecture plan](docs/design/active_knee_revision2_plan.md); the
[teardown observations and their limits](evidence/reference/2026-09-25_beni_teardown/)
are recorded separately. No R2A CAD, actuator choice, belt ratio, STL or purchase
is released. A dated [actuator trade study](docs/design/active_knee_actuator_trade_study.md)
shows that another GIM6010-8 should not be the default knee purchase. The
budget skeleton uses a compact integrated actuator on the proximal-link root
and one belt; a stronger body-fixed actuator plus jackshaft remains the
performance comparison. The legacy ABS article stays spring-free and unpowered
and remains useful only as fit, assembly and failure evidence.

**September 24 physical assembly report — spring-retention FAIL:** the owner
reports the three PINREV2 parts printed and the article assembled, with most
interfaces working well. During knee compression the spring bows and escapes
sideways. The spring cartridge is retired from the active design; remove the
spring and cancel powered commissioning of this article. The owner confirms the guide is disengaged with the spring uncompressed and
only intermittently enters during compression; the loose-guide assembly is
also unacceptable to the owner. This must be reconciled with the recorded
5.500 mm modeled overlap at -8°. Eye freedom, exact starting pose and damage
remain unconfirmed; no guide or cartridge replacement will be released. Do not infer
individual fit passes from the assembly report.
[Owner observation and diagnostic status](evidence/assembly/2026-09-24_spring_escape/).
The owner additionally reports end twisting and requests a mechanism-level
redesign. The earlier
[fixed-axis cassette study](docs/design/knee_spring_redesign.md) is
**[SUPERSEDED 2026-09-25]** because it preserved the passive-joint premise.
Existing pose checks impose eye alignment; they do not prove physical alignment
under load.


**September 24 CAD readiness on the second machine:** Fusion 2705.1.25 ignores
the STL surface deviation, so plain "High" exports would print the proximal
bearing seats 0.040 mm tighter than released. Every print export now uses
`stl_release`, and the release gate proves mesh↔B-Rep fidelity instead of
matching another machine's triangles. Both release scripts complete here
without changing a released file. [Release gate](evidence/assembly/2026-09-24_cross_machine_release_gate/).
Four parts that the rig conversion deletes had been resurrected by a
Sept 21–23 rebuild. They are removed in v31; `checks_44()` and the ABS-article
motion audit pass in full. [Model cleanup](evidence/assembly/2026-09-24_rig_model_cleanup/).
Neither change alters a printed part.

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


> **Current scope decision, updated 2026-09-25 — design and prove the R2A
> single-leg integration article in ABS; defer PA-CF to the two-leg structural
> build.** The legacy passive article stays spring-free and unpowered. The new
> ABS leg may progress through dry assembly, hand-driven belt motion, detached
> current-limited transmission checks and supported wheel-clear commissioning
> under self-weight only after each R2A gate is released. Torque-arm,
> added-mass, ground-traction, stall/proof, drop, jump and human-adjacent tests
> remain deferred with PA-CF.
>
> **Fixture scope remains Mode A only.** The shoulder-to-stand geometry remains
> useful for assembly and unloaded integration. The vertical MGN12 slide,
> ballast, index bar, mode pin, bumpers and drop series remain **deferred, not
> cancelled**. The CAD handoff is
> [`fusion_agent_guide_mode_a.md`](fusion_agent_guide_mode_a.md).

| | Status |
|---|---|
| **Prototype 1**, two-leg robot | Legacy passive-knee model saved in Fusion (`Biped → Beni_Prototype1`, v18). It remains the dimensional and failure-analysis baseline; it is no longer the target architecture. The September access correction adds continuous M4 head/driver and complete screw-seat checks to `beni_lib.audit_all()`. Revision 2; not built. **v18 predates the September 21 ordered-pin source.** On 2026-09-24 a read-only `audit_all()` reported 6 problems: hardware counts, and source parity for the Ø4 × 32 clevis pins and Ø6 × 9 dowel still modelled, against M4 × 40 pins, washers, root dowels and Ø6 × 10 in `beni_lib`. Do not spend effort rebuilding it as the future robot; preserve it while R2A starts in a separate Fusion copy. |
| **Single-leg test rig, Mode B** | **[DEFERRED]** — not the build. Its source now inherits the owner-selected Ø4.5 M3 receiver and Ø5.3 M4 receiver constants, but the stripped/deferred carriage was not rebuilt or released. Rebuild and verify it in Fusion when Mode B returns and repeat the M3 coupon for its eventual material/profile. |
| **Single-leg integration article / Mode A fixture** | The legacy passive ABS article is assembled and retained as physical fit and failure evidence. It is not the active architecture. Keep the spring removed and the motors unpowered. The stand remains useful for the future R2A wheel-clear integration article after its interfaces are revalidated. |
| **Active-Knee Revision 2 (R2A)** | Architecture plan and actuator price screen complete; no CAD or hardware release. The selected direction is a shoulder-area knee actuator with synchronous-belt drive through a redesigned proximal link, plus an independent knee encoder. The first Fusion comparison is a compact proximal-root motor with one belt versus a stronger body-fixed motor and shoulder-axis jackshaft. RobStride 05/EduLite 05/RobStride 00 are candidates only; load cases, Fusion fit, ratio, belt family, knee output stack and new power budget remain open. |
| Electronics | The current documents describe the legacy four-actuator robot. Nothing is wired. R2A requires six total actuators for the two-leg robot and a new power, CAN, harness, thermal and firmware review after knee motor selection. |
| Firmware | Stage 0 bench scaffold implemented and compile-verified for Teensy 4.1 in [`firmware/teensy_stage0/`](firmware/teensy_stage0/). It has no actuator command path; hardware gates remain unrun. |
| Physical hardware | **The GIM6010-8 shoulder actuator, GIM4305-10 wheel actuator, 6800-2RS bearings, pins, fasteners and assembled legacy ABS article are in hand.** [Actuator photographs](evidence/actuators/2026-08-20_received/). The two actuators remain candidates for their original roles; R2A needs a third actuator per leg. Preserve the accepted motor-interface, insert and pin-fit results as process evidence, but recheck every reused interface against its new load and service path. The Yellow / OD18 / ID9 / 50 mm spring and its cartridge are retired from R2A after the physical escape. Detailed fit history remains in the dated evidence and legacy sections below. |

**[HISTORICAL] Owner update, 2026-09-07:** the temporary pin, provisional distal link and
two spring caps are printed, and provisional assembly succeeded. The owner
confirmed free supported knee movement/easy pin removal, both spring ends
seating flat on the detached caps without force or compression, and use of the
corrected proximal replacement with all six hub screws seating properly.
[Photo and physical acceptance scope](evidence/assembly/2026-09-07_owner_mockup/).
This was a provisional knee assembly. The corrected legacy article was later
assembled and is now retained spring-free as evidence.

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
accepted shoulder hub as physical evidence. The owner later printed the
ordered-pin replacements for the legacy passive build. Their files remain in
the [historical first-article archive](first_article_stl/ordered_pin_integration/),
but they are no longer in the active print queue.
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

## Immediate next steps for Active-Knee Revision 2

1. Keep the assembled passive article spring-free and unpowered. Photograph or
   measure it only when a specific R2A interface question needs physical
   evidence; do not spend another print cycle improving the spring cartridge.
2. Through the Fusion MCP, create a read-only measurement report for the
   current shoulder stack, proximal-link free space, knee bearing stack,
   fastener paths and harness envelope.
3. In a separate Fusion copy, compare four R2A skeletons: a compact motor on the
   proximal-link root, opposite-side coaxial motors, axially stacked motors, and
   a body-mounted offset knee motor driving a shoulder-axis jackshaft.
4. Derive the active-knee load cases and select an actuator, belt family, pulley
   ratio and knee output stack from traceable data. Do not buy against the
   teardown's apparent proportions.
5. Update the power, CAN, harness, URDF and control plan after the motor and
   ratio are selected. Retain an independent knee encoder for transmission fault
   detection during development.
6. Release one unpowered ABS belt-transmission article through the existing
   Fusion, assembly-path, mesh and orientation gates. Only after it passes may a
   detached, current-limited drive test be specified.

The accepted fit results from the legacy article may inform R2A, but no old pin,
bearing, insert or link interface is inherited without checking its new load and
service path. The full work breakdown and release ladder are in
[`docs/design/active_knee_revision2_plan.md`](docs/design/active_knee_revision2_plan.md).

---

## The active Fusion documents

| Document | What it is |
|---|---|
| `Beni_Prototype1` | Legacy passive-knee two-leg robot. **Historical master — preserve; do not convert in place.** |
| `Beni_SingleLegRig` | Legacy passive-knee ABS rig, saved as v31 on 2026-09-24. Preserve it as the assembled article's CAD/evidence baseline. Start R2A in a separate Fusion copy after the read-only measurement report. |
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

### Active-Knee Revision 2 — design this next

| File | What it is |
|---|---|
| [`docs/design/active_knee_revision2_plan.md`](docs/design/active_knee_revision2_plan.md) | Architecture decision, motor-layout trade study, belt-drive work packages, coupled kinematics and release ladder. |
| [`docs/design/active_knee_actuator_trade_study.md`](docs/design/active_knee_actuator_trade_study.md) | Dated integrated-actuator price/spec comparison, alternative mechanisms and recommended budget/performance Fusion skeletons. |
| [`evidence/reference/2026-09-25_beni_teardown/`](evidence/reference/2026-09-25_beni_teardown/) | Timestamped teardown observations and explicit limits on what the video establishes. |

### Legacy single-leg rig — physical evidence baseline
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
| `mechanical_spring_test_fusion.py` | Fusion MCP, with `Beni_SingleLegRig` active | Builds and audits the unpowered 50 mm spring cartridge, guide, -8°…+15° stop, outboard pin keeper stack and no-tyre wheel shell. `audit()` runs the 24-pose sweep, stop proof and insertion paths; `release()` exports the six current spring-test files (the stop plate is released by the ordered-pin script). A directory argument makes either a dry run. |
| `ordered_pin_integration_fusion.py` | Fusion MCP, with `Beni_SingleLegRig` active | Releases the four ordered-pin parts (PINREV2 hub/links plus the stop plate) around the ordered Ø4 × 10, M4 × 40, and Ø6 × 10 hardware; verifies meshes and writes the ordered-pin manifest/evidence. `refresh_images()` recaptures their release images without rewriting the STLs; a directory argument to `release()` is a dry run. |
| `mechanical_release_audit_fusion.py` | Fusion MCP, with `Beni_SingleLegRig` active | The fail-closed release gate: `assert_all()` checks 32 measured interface contracts and every native face of the 15 printed parts against the reviewed `mechanical_release_baseline.json`. `assert_export()` accepts a bed-ready mesh that matches the pinned fingerprint or passes the machine-independent `mesh_fidelity()` proof against the reviewed B-Rep. `regression_tests()` runs the negative controls. Exporters never update the baseline; only the logged `accept_shapes()`, `accept_released_files()` and `accept_verified_sources()` review steps do. |
| `stl_release.py` | Fusion MCP | The print tessellation standard used by every STL exporter: a 0.004 mm chord on the largest curved radius, set through the normal deviation because Fusion 2705.1.25 ignores surface deviation. [Record](evidence/assembly/2026-09-24_cross_machine_release_gate/). |
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
| Main knee spring | **[RETIRED FROM R2A]** Yellow / OD18 / ID9 / 50 mm. It remains physical evidence from the failed passive article; do not reinstall it. R2A has no main compression spring. Any later energy-storage element requires a new, constrained load path and a separate release. [Spring record](evidence/springs/2026-09-05_reconciliation/) · [failure record](evidence/assembly/2026-09-24_spring_escape/). |
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
