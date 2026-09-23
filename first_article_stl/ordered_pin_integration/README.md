# Ordered-pin mechanical integration — print and assembly traveller

Status: `FUSION VERIFIED / PRINT RELEASE / FINAL-PART HAND FIT PENDING`

> **Calibration closed September 22:** the owner selected nominal Ø4.25 for
> both the root-dowel hub socket and clevis-link passages using the actual
> ordered pins. Fusion v29 and all four files below contain those values. The
> coupon result releases these prints; the printed assemblies still receive
> the binary hand-fit checks below.

This September 21 batch makes the purchased pin sizes part of the load path
and retention design. It is not a collection of loose spacers. Print these
four replacement parts before continuing the unpowered ABS single-leg
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

1. Print and visually inspect all four replacements. Reject cracks, lifted fit
   faces, blocked bores, or a damaged closed skin on the stop plate.
2. Install heat-set inserts using the existing
   [receiver map](../../docs/assembly/heatset_receiver_map.md). Keep the three
   Ø4 root sockets clear of the iron and molten ABS.
3. Support the shoulder hub's flange flat. Start three Ø4 × 10 dowels straight
   into its Ø4.25 blind sockets using thumb pressure or, if needed, a
   smooth-jaw vise or controlled arbor press, never a hammer. Seat each 5.0 mm
   deep. Stop if the hub whitens, splits, or a pin cocks. Offer the proximal
   root over the exposed halves;
   its Ø4.25 × 5.2 sockets are the slip side. The faces must meet by hand before
   the six M4 screws are installed. The screws clamp the faces and make the
   dowels axially captive; they must not pull the parts into alignment.
4. Place one Ø6 × 10 dowel in the distal link's Ø6.2 × 4.5 blind socket. Fit
   the new stop plate with 3 × M3 × 10 screws. Its closed outer skin captures
   the pin with 0.3 mm axial clearance, so no glue or press fit is used.
5. Complete the unchanged cartridge, guide, spring, D10 knee-pin keeper, and
   wheel-shell sequence in the September 17 traveller. At each cartridge eye,
   insert an M4 × 40 clevis pin from inboard to outboard, place one specified
   M4 washer against the printed outboard face, then install the supplied
   cotter. Rotate the clevis pin so the cotter lies radially away from the knee
   and seat the cotter fully without bending or reshaping it. The integral
   printed lands provide the designed 34.0 mm retained stack; add no spacer.
6. Clamp the Mode A stand, leave both motor power and communication cables
   unplugged, keep the wheel clear, and contain the distal side by hand. Move
   slowly only from -8° through +15° and follow every stop condition in the
   September 17 traveller.

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
