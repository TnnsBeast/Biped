# Ordered-pin mechanical integration — print and assembly traveller

Status: `FUSION VERIFIED / PRINT RELEASE / FINAL-PART HAND FIT PENDING`

Start with the [21-step illustrated assembly manual](../../docs/assembly/ordered_pin_picture_guide.md)
or its [printable PDF](../../output/pdf/beni_single_leg_assembly_manual.pdf)
at the bench; the detailed checklist remains below.

**September 23 correction: reprint the shoulder hub and both links from
PINREV2. Keep the existing closed-skin stop plate.** The September 22 distal
STL was mislabeled D10p30 but contained Ø16; its replacement restores the
Ø10.30 × 20.0 receiver. Root-dowel sockets and clevis-link passages now use
owner-requested **Ø4.30**, +0.05 mm beyond the Ø4.25 ladder selection, for easier
hand removal. This is a new fit candidate; final-part hand fit remains open.
Motor-pin passages, knee bore, cartridge eyes and captive stop clearances are
otherwise unchanged. See the [all-15-part audit](../../evidence/assembly/2026-09-23_mechanical_reprint_audit/)
for evidence and the keep/reprint decision for every part.

The three PINREV2 files below replace the corresponding September 22 prints.
The fourth row is retained hardware, not another required reprint.

| Part | Qty | Import orientation and supports |
|---|---:|---|
| [`ABS_PINREV2_Shoulder_Output_Hub_D4p15_ROOT_D4p30_PRINT_ORIENTED.stl`](ABS_PINREV2_Shoulder_Output_Hub_D4p15_ROOT_D4p30_PRINT_ORIENTED.stl) | 1 | Import unchanged with the Ø56 outboard flange on the bed. No supports. The three root-socket ceilings are controlled bridges. |
| [`ABS_PINREV2_Proximal_Link_D19p15_ROOT_D4p30_CLEVIS_D4p30_PRINT_ORIENTED.stl`](ABS_PINREV2_Proximal_Link_D19p15_ROOT_D4p30_CLEVIS_D4p30_PRINT_ORIENTED.stl) | 1 | Import unchanged with the broad outboard face on the bed. No support in bearing seats, root sockets, clevis bore, or open channel. |
| [`ABS_PINREV2_Distal_Link_D10p30_D6x10_CLEVIS_D4p30_PRINT_ORIENTED.stl`](ABS_PINREV2_Distal_Link_D10p30_D6x10_CLEVIS_D4p30_PRINT_ORIENTED.stl) | 1 | Import unchanged with the broad inboard face on the bed. Use support only under the knee-receiver land, raised web, wheel-end underside, and open-channel ceiling. Block support from every fit bore. |
| [`ABS_PINREV_Knee_Stop_Plate_15deg_D6x10_CAPTIVE_PRINT_ORIENTED.stl`](ABS_PINREV_Knee_Stop_Plate_15deg_D6x10_CAPTIVE_PRINT_ORIENTED.stl) | 1 | Import unchanged with the closed 0.8 mm skin on the bed and the pin channel opening upward. No supports. |

Use the tuned enclosed-ABS profile: **0.20 mm layers, 4 walls, 5 top and 5
bottom layers, 30% infill**. Do not rotate, scale, compensate holes, drill,
sand, file, or heat-fit a failed article.

The PINREV2 hub and links supersede their prior versions. Keep the ordered-pin
closed-skin stop plate; the older September 17 stop plate remains superseded. Reuse the unchanged two
50 mm cartridge eyes, guide bar, D10 knee-pin spacer, encoder-bracket keeper,
and no-tyre wheel shell from the
[`mechanical_spring_test`](../mechanical_spring_test/) batch.
Keep superseded hub/link prints and the old September 17 stop plate out of
the active assembly. The superseded September 22 hub, link and mislabeled Ø16
distal files were removed from this folder on September 23; they remain in
git history at `56b2507`. On September 23 the owner confirmed that the printed
stand and shoulder plate were made after the Ø4.5 M3-receiver promotion, so
both are current. [Owner report](../../evidence/assembly/2026-09-23_owner_stand_plate_and_washers/).
The already reported printed cable cover, front cable post, and wheel hub are
reusable after their pending fits and insert checks.

## Hardware consumed from the order

- 3 × Ø4 × 10 mm cylindrical dowels at the shoulder hub/root interface
- 2 × M4 × 40 mm single-hole clevis pins and their supplied cotters
- 1 × Ø6 × 10 mm cylindrical dowel at the knee stop

Also use 2 × ISO 7089 M4 steel washers, 4.3 × 9 × 0.8 mm, and 3 × M3 × 10
socket-head screws from the fastener inventory. The washers are the specified
bearing surface for the cotters; do not replace them with printed spacers.

**Washer deviation, September 23:** the owner has no M4 washers and will try
this unpowered article without them. Each clevis pin then floats up to 1.2 mm
instead of 0.4 mm and its cotter bears on the ABS land. This is accepted only
for the clamped, unplugged, hand-contained test: inspect both cotter faces
after step 11 and fit washers before repeated cycling or powered use.
[Arithmetic and limits](../../evidence/assembly/2026-09-23_owner_stand_plate_and_washers/#iso-7089-m4-washers).

No dimensional measurement is required. The seller dimensions are already in
the CAD, and the owner requested Ø4.30 after selecting Ø4.25 with the actual pins.
Check that the pieces are undamaged and perform the final-part hand-fit steps
below. A pin that needs drilling, filing, hammering, or screw pull-down is a
failed interface, not a request to rework the hardware.

## Kit check

Collect everything before step 1. Counts come from the steps below; skip any
insert already installed in an accepted part.

| Group | Items |
|---|---|
| Printed, reprint | new PINREV2 shoulder hub (D), proximal link (E), distal link (G) |
| Printed, keep | stand (A), shoulder plate (B), cable cover, front cable post, stop plate (K), upper and lower cartridge eyes (L, N), guide bar (M), knee-pin spacer (Q), keeper bracket (P), no-tyre shell (R), wheel hub (J) |
| Actuators and bearings | GIM6010-8 (C) and GIM4305-10 (H), both unplugged; 2 × 6800-2RS (F) |
| Pins and spring | Ø10 × 35 steel knee pin; 3 × Ø4 × 10 dowels; 2 × M4 × 40 clevis pins with supplied cotters; 1 × Ø6 × 10 dowel; owned OD18 / ID9 / 50 mm spring; 2 × ISO 7089 M4 washers (**not in hand**, see deviation above) |
| Heat-set inserts | 12 × M4 × 8: 6 in hub D, 6 in wheel hub J. 14 × 5 mm M3: 5 in proximal E, 4 in plate B, 5 in stand A |
| Socket-head screws | M2.5 × 12: 6 (wheel motor). M3 × 8: 11 (8 shoulder housing, 3 wheel hub). M3 × 10: 16 (5 plate-to-stand, 2 lower cover, 6 shoulder hub, 3 stop plate). M3 × 12: 2 (post and upper cover). M3 × 16: 2 (keeper bracket). M4 × 8: 6 (no-tyre shell). M4 × 10: 6 (proximal root) |
| Bench | clamps for the stand, depth-controlled insert tip, hex keys, pliers for the cotters |

## Ordered assembly

Keep both motor power and communication cables unplugged. Support the links,
knee and wheel during detached fit work. Clamp or bolt the current Mode A stand
to the bench before attaching the leg; keep the wheel clear of the bench and
floor. The two ISO 7089 M4 washers for the clevis cotters are not in hand; the
steps below note where they go if fitted later.

1. Sort and inspect the prints. Use the three PINREV2 parts, retained closed-skin stop plate and the six
   retained September 17 pieces, not the previous hub, links or stop plate.
   Reject cracks, lifted mating faces, blocked bores, damaged bearing lips, or
   a damaged closed skin on the stop plate. The stand and shoulder plate in
   hand are the owner-confirmed Ø4.5 M3-receiver versions. Keep the spring
   off the leg for the first fit and stop checks.
2. Rehearse detached interfaces before inserts or a loaded stack. Each 6800
   bearing must fit squarely in the **new** proximal link with thumb pressure
   on its outer race and no perceptible rock; transfer bearings from the older
   link only if they come out undamaged. Run the steel D10 pin through each
   bearing separately. With both bearings installed, offer the new distal link
   into the fork and insert the steel pin from inboard by firm thumb pressure.
   It must fully seat, withdraw by hand, and have no free spin or radial rock
   in the Ø10.30 × 20.0 printed receiver or unacceptable axial play. Check
   that each M4 × 10 root screw passes through the new proximal access path and
   sits flat. Separately check the guide, spring pilots, cartridge eyes, both
   M4 × 40 pins, and spacer-to-bracket locator using the
   [September 17 detached-fit steps](../mechanical_spring_test/README.md#detached-fit-checks).
   Stop at any failed fit; do not drill, file, hammer or use screws to draw
   parts together.
3. Install inserts in detached, accepted prints per the
   [receiver map](../../docs/assembly/heatset_receiver_map.md): six owned
   M4 × 8 inserts from the **new hub's outboard/link face**, five M3 inserts in
   the **new proximal link** (three stop, two bracket), and the released stand,
   shoulder plate and wheel-hub inserts if they have not already been fitted.
   Keep the three root-dowel sockets clear of heat and plastic. Let each
   receiver cool and reject a proud, tilted or loose insert. The stop plate,
   distal link, cartridge eyes and cable cover receive no inserts.
4. With the hub detached and its flange supported flat, start three Ø4 × 10
   dowels straight into its Ø4.30 blind sockets by hand. Seat each 5.0 mm deep. Stop for whitening,
   splitting or a cocked pin. Offer the proximal root over their exposed halves
   as a trial: its Ø4.30 × 5.2 sockets must let the faces meet by hand. Confirm hand withdrawal and no objectionable play with the root assembled.
   Support the dowels while mating the root; the screws capture them. Remove
   the proximal link for the shoulder and cable-cover steps.
5. Assemble the shoulder in the established order: fit the current shoulder
   plate over the **bare output rotor** of the unplugged GIM6010 and fasten the
   stationary housing with **8 × M3 × 8**; attach the plate to the clamped
   stand with **5 × M3 × 10**. Route the real cable and fit the already printed
   cable cover/front post before the link if those are included in this
   article. The upper post/cover screws are **M3 × 12**, the lower two are
   **M3 × 10**. Rehearse cable and tie clearance without energizing either
   motor. Align the hub on the motor's three factory pins, seat it against the
   metal output face by hand, and fit **6 × M3 × 10** output-hub screws.
   Follow the [shoulder picture guide](../../docs/assembly/shoulder_to_proximal_link.md)
   for the plate/rotor direction and service order.
6. Support the knee end and bring the new proximal root straight onto the
   three protruding dowels. Confirm full face contact **before** starting its
   **6 × M4 × 10** screws; then finger-start all six and check every head sits
   flat. The screws clamp the joint and make the dowels axially captive. Remove
   and refit once if necessary to prove the service path.
7. Prepare the wheel end while the distal link is detached: fit the unplugged
   GIM4305 with **6 × M2.5 × 12** from the inboard side, and fit the accepted
   wheel hub to its output with **3 × M3 × 8**. The hub's six M4 inserts are
   installed from its motor face before this joint. Keep the no-tyre shell off
   until the knee, stop and cartridge have passed their fits; keep the TPU tyre
   off this test article.
8. With both bearings in the new proximal fork, insert the detached distal
   link and the D10 steel pin from the inboard side. Confirm hand withdrawal
   again. Put one Ø6 × 10 dowel in the distal link's Ø6.2 × 4.5 blind stop
   socket, then fasten the **new closed-skin stop plate to the proximal link's
   three M3 inserts** with **3 × M3 × 10**. The plate captures the dowel with
   0.3 mm axial clearance; no glue or press fit is used. Before adding the
   spring, hand-pose the supported knee and confirm positive stops at -8° and
   +15° without binding or bypass.
9. With the knee at -8°, fit the upper cartridge eye radially, then pass an
   M4 × 40 clevis pin **inboard to outboard** through the actual link/eye stack.
   Put one ISO 7089 M4 washer against the printed outboard face (omitted under
   the September 23 washer deviation) and fit the supplied cotter, oriented
   radially away from the knee. Insert the guide
   through the **round center of the upper Ø8 spring pilot**, slide the free
   50 mm spring over it, and slide the lower eye onto the exposed guide and
   into the distal clevis. Its pin must pass with fingertip pressure. Add the
   second washer (if in hand) and cotter in the same orientation. Seat cotters
   fully without reshaping them and add no printed spacers. If the lower eye
   needs more than slight hand compression, stop rather than pulling it in
   with a pin, screw or clamp.
10. Put the D10 outboard spacer's locator in the printed bracket's center hole
    and attach the bracket to the proximal link's two M3 inserts with
    **2 × M3 × 16**. The spacer limits outboard knee-pin travel; hand control
    still prevents inboard escape during this test. Fit the no-tyre wheel shell
    to the accepted wheel hub with **6 × M4 × 8**; keep it suspended. Remove
    the bracket before servicing the stop screws, and remove the stop and
    cartridge hardware before withdrawing the knee pin.
11. Only after those detached and spring-free checks pass, perform the
    [September 17 unpowered hand test](../mechanical_spring_test/README.md#hand-test).
    With one hand containing the distal side, move slowly through -8°, 0°,
    +5°, +10° and +15°. Stop for binding, whitening or cracking, coil contact,
    guide escape, pin migration, a loose cotter or stop bypass. Record the
    settle/return tendency; it does not establish spring rate or authorize
    powered motion. Without washers, finish by inspecting both cotter contact
    faces for indentation or whitening.

The ordered hardware remains `FINAL-PART HAND FIT PENDING` until these binary
checks pass. This does not require calipers and does not authorize powered
motion, ground contact, added mass, or structural testing.

## Verification record

The September 23 correction verifies measured Ø4.30 root/clevis-link holes,
the restored Ø10.30 × 20.0 knee receiver, complete proximal screw seats,
40 mm clevis insertion paths, washer/cotter space and captive Ø6 stop stack.
The 24-pose -8°…+15° sweep, link/pin service paths and selective-support removal
checks pass. Each released STL is a closed manifold and matches the reviewed
Fusion geometry and bed orientation. See the [full audit and regression
checks](../../evidence/assembly/2026-09-23_mechanical_reprint_audit/) and
[`fusion_manifest.json`](fusion_manifest.json). New Ø4.30 physical fits remain
unverified until the replacement prints pass the hand checks.
