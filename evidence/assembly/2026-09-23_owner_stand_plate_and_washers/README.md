# Owner report — stand/plate revision and cotter washers

Date: 2026-09-23. Source: owner's answers in the project conversation.
Status: `STAND/PLATE REVISION CONFIRMED / WASHERS NOT IN HAND`.

## Stand and shoulder plate

The owner reports that the printed Mode A stand and shoulder plate were both
downloaded and printed **after** the September 14 Ø4.5 M3-receiver promotion
(commit `be98009`). Both files kept the same names across the Ø4.0 and Ø4.5
revisions, so download timing is the only identifier. These prints are
therefore the current Ø4.5 receiver versions:

- [`ABS_FA_RIG_Stand_M3_INSERTS_PRINT_ORIENTED.stl`](../../../first_article_stl/mode_a/ABS_FA_RIG_Stand_M3_INSERTS_PRINT_ORIENTED.stl)
- [`ABS_FA_Chassis_Shoulder_Plate_L_M3_INSERTS_PRINT_ORIENTED.stl`](../../../first_article_stl/assembly_dry_fit/ABS_FA_Chassis_Shoulder_Plate_L_M3_INSERTS_PRINT_ORIENTED.stl)

The September 23 audit's "conditional keep" for both parts becomes **keep**; no
stand or plate reprint is required. This is a report of download timing, not
a physical pocket inspection. Insert installation in either part has not been
reported.

## ISO 7089 M4 washers

The owner does not have the two ISO 7089 M4 washers (4.3 × 9 × 0.8 mm) that
sit between each printed clevis land and its supplied cotter, and intends to
attempt the unpowered assembly without them. The CAD and release keep the
washers; this is an owner-accepted deviation for this article only.

Consequence, from the seller-drawing values recorded by the Fusion v30 audit
([`fusion_mechanical_audit.json`](../2026-09-23_mechanical_reprint_audit/fusion_mechanical_audit.json)):
the retaining hole is Ø1.6 at 36.0 mm from the pin head, and the printed stack
is 34.0 mm.

| | Printed face to near hole edge |
|---|---:|
| With washer, as released: 36.0 − 1.6/2 − 34.0 − 0.8 | 0.4 mm |
| Without washer: 36.0 − 1.6/2 − 34.0 | 1.2 mm |

Without the washer each clevis pin can float up to 1.2 mm axially, plus the
cotter wire's clearance in its hole. The cotter then bears directly on the
ABS land instead of on steel. The spring force acts across the pins (radially),
so this changes axial retention and wear, not the load path. The Ø4.0 shaft in
its Ø4.30 bore leaves no gap a cotter leg can enter.

Accepted scope and checks:

- Unpowered, clamped, wheel-clear, hand-contained self-weight test only.
- Seat each cotter fully, legs spread, radially away from the knee.
- After the -8°…+15° hand test, inspect both cotter contact faces. Stop and fit
  washers if either face shows indentation, whitening, or a cotter riding on
  the edge of the land.
- Fit the two washers before any repeated cycling or powered commissioning.
