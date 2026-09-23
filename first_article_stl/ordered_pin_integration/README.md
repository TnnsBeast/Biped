# Ordered-pin mechanical integration — print and assembly traveller

Status: `FUSION VERIFIED / PRINT RELEASE / FINAL-PART HAND FIT PENDING`

**Owner update, September 22:** all four revised parts in this batch are
reported printed, the retained September 17 mechanical-test parts are reported
printed, and the three Amazon pin families are reported in hand. No final-part
fit or completed assembly has been reported. See the
[owner material record](../../evidence/assembly/2026-09-22_owner_printed_parts_and_pins/).

> **Calibration closed September 22:** the owner selected nominal Ø4.25 for
> both the root-dowel hub socket and clevis-link passages using the actual
> ordered pins. Fusion v29 and all four files below contain those values. The
> coupon result releases these prints; the printed assemblies still receive
> the binary hand-fit checks below.

This September 21 batch makes the purchased pin sizes part of the load path
and retention design. It is not a collection of loose spacers. These are the
four replacement parts in the unpowered ABS single-leg
assembly:

| Part | Qty | Import orientation and supports |
|---|---:|---|
| [`ABS_PINREV_Shoulder_Output_Hub_D4p15_ROOT_D4x10_PRINT_ORIENTED.stl`](ABS_PINREV_Shoulder_Output_Hub_D4p15_ROOT_D4x10_PRINT_ORIENTED.stl) | 1 | Import unchanged with the Ø56 outboard flange on the bed. No supports. The three root-socket ceilings are controlled bridges. |
| [`ABS_PINREV_Proximal_Link_D19p15_ROOT_D4x10_M4x40_PRINT_ORIENTED.stl`](ABS_PINREV_Proximal_Link_D19p15_ROOT_D4x10_M4x40_PRINT_ORIENTED.stl) | 1 | Import unchanged with the broad outboard face on the bed. No support in bearing seats, root sockets, clevis bore, or open channel. |
| [`ABS_PINREV_Distal_Link_D10p30_D6x10_M4x40_PRINT_ORIENTED.stl`](ABS_PINREV_Distal_Link_D10p30_D6x10_M4x40_PRINT_ORIENTED.stl) | 1 | Import unchanged with the broad inboard face on the bed. Use support only under the knee-receiver land, raised web, wheel-end underside, and open-channel ceiling. Block support from every fit bore. |
| [`ABS_PINREV_Knee_Stop_Plate_15deg_D6x10_CAPTIVE_PRINT_ORIENTED.stl`](ABS_PINREV_Knee_Stop_Plate_15deg_D6x10_CAPTIVE_PRINT_ORIENTED.stl) | 1 | Import unchanged with the closed 0.8 mm skin on the bed and the pin channel opening upward. No supports. |

Use the tuned enclosed-ABS profile: **0.20 mm layers, 4 walls, 5 top and 5
bottom layers, 30% infill**. Do not rotate, scale, compensate holes, drill,
sand, file, or heat-fit a failed article.

These four files supersede the earlier shoulder hub, proximal link, distal
link, and September 17 stop plate for this build. Reuse the unchanged two
50 mm cartridge eyes, guide bar, D10 knee-pin spacer, encoder-bracket keeper,
and no-tyre wheel shell from the
[`mechanical_spring_test`](../mechanical_spring_test/) batch.
Keep the older four structural prints out of the active assembly. The printed
stand and shoulder plate are not yet identified as the current Ø4.5 M3-receiver
versions; check their source files before installing inserts. The already
reported printed cable cover, front cable post, and wheel hub are reusable
after their pending fits and insert checks.

## Hardware consumed from the order

- 3 × Ø4 × 10 mm cylindrical dowels at the shoulder hub/root interface
- 2 × M4 × 40 mm single-hole clevis pins and their supplied cotters
- 1 × Ø6 × 10 mm cylindrical dowel at the knee stop

Also use 2 × ISO 7089 M4 steel washers, 4.3 × 9 × 0.8 mm, and 3 × M3 × 10
socket-head screws from the fastener inventory. The washers are the specified
bearing surface for the cotters; do not replace them with printed spacers.

No dimensional measurement is required. The seller dimensions are already in
the CAD, and the actual ordered pins selected the two Ø4.25 printed interfaces.
Check that the pieces are undamaged and perform the final-part hand-fit steps
below. A pin that needs drilling, filing, hammering, or screw pull-down is a
failed interface, not a request to rework the hardware.

## Ordered assembly

Keep both motor power and communication cables unplugged. Support the links,
knee and wheel during detached fit work. Clamp or bolt the current Mode A stand
to the bench before attaching the leg; keep the wheel clear of the bench and
floor. Have **two ISO 7089 M4 steel washers** for the clevis cotters. Their
presence was not confirmed in the owner update, so check before closing either
clevis joint.

1. Sort and inspect the prints. Use the four revised parts above and the six
   retained September 17 pieces, not the previous hub, links or stop plate.
   Reject cracks, lifted mating faces, blocked bores, damaged bearing lips, or
   a damaged closed skin on the stop plate. Verify that any stand and shoulder
   plate to be used are the released Ø4.5 M3-receiver versions. Keep the spring
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
   dowels straight into its Ø4.25 blind sockets with thumb pressure or a
   controlled smooth-jaw press. Seat each 5.0 mm deep. Stop for whitening,
   splitting or a cocked pin. Offer the proximal root over their exposed halves
   as a trial: its Ø4.25 × 5.2 sockets must let the faces meet by hand. Remove
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
   Put one ISO 7089 M4 washer against the printed outboard face and fit the
   supplied cotter, oriented radially away from the knee. Insert the guide
   through the **round center of the upper Ø8 spring pilot**, slide the free
   50 mm spring over it, and slide the lower eye onto the exposed guide and
   into the distal clevis. Its pin must pass with fingertip pressure. Add the
   second steel washer and cotter in the same orientation. Seat cotters fully
   without reshaping them and add no printed spacers. If the lower eye needs
   more than slight hand compression, stop rather than pulling it in with a
   pin, screw or clamp.
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
    powered motion.

The ordered hardware remains `FINAL-PART HAND FIT PENDING` until these binary
checks pass. This does not require calipers and does not authorize powered
motion, ground contact, added mass, or structural testing.

## Verification record

Fusion v29 verified the selected Ø4.25 hub sockets and link passages, exact
40 mm clevis insertion paths, washer/cotter space, the captive Ø6 stop stack,
the three shoulder-root dowel locations, the unchanged calibrated print faces,
and all -8°…+15° hand poses. Every STL is a closed manifold with zero
non-manifold edges and zero degenerate triangles. See the
[release evidence](../../evidence/assembly/2026-09-21_ordered_pin_integration/)
and [`fusion_manifest.json`](fusion_manifest.json).
