# Ordered-pin ABS fit ladders

Status: `OWNER SELECTED / CAD PROMOTED`

These two inexpensive calibration parts used the real ordered hardware as
go/no-go gauges, so **no measurement or calipers were required**. Their
September 22 results are now promoted into Fusion v29 and the refreshed
[ordered-pin production files](../ordered_pin_integration/).

## Selected results

- Root dowel: **Ø4.25**, the largest station farthest from the two-marker end.
  The owner reported it was relatively tight, pressed in with a thumb, and
  pulled out with pliers. This is the retained hub side; inspect each final hub
  socket for whitening or cracking during installation.
- M4 × 40 clevis pin: **Ø4.25**, the middle station. The owner reported that it
  worked well. This is the removable proximal/distal link-passage value; still
  confirm hand insertion and withdrawal through the completed link/eye stacks.

| File | What it reproduces | Size |
|---|---|---:|
| [`ABS_CAL_D4x10_ROOT_BLIND_SOCKET_LADDER_PRINT_ORIENTED.stl`](ABS_CAL_D4x10_ROOT_BLIND_SOCKET_LADDER_PRINT_ORIENTED.stl) | Five 5.0 mm-deep blind sockets with the final hub's 3.0 mm closed floor | 130 × 20 × 8 mm |
| [`ABS_CAL_M4x40_CLEVIS_LINK_LAND_LADDER_PRINT_ORIENTED.stl`](ABS_CAL_M4x40_CLEVIS_LINK_LAND_LADDER_PRINT_ORIENTED.stl) | Five Ø14 bosses with the longest actual 9.0 mm clevis-link passage | 130 × 15 × 9 mm |

Import both STLs unchanged. Use the same tuned enclosed-ABS profile as the
final parts: **0.20 mm layers, 4 walls, 5 top and 5 bottom layers, 30% infill**.
Do not rotate, scale, compensate holes, drill, sand, file, or ream. Neither
ladder needs supports. A brim is permitted on the clevis ladder.

The two Ø2 marker holes identify the small-diameter end. The test station
closest to those markers is the first value below; each station farther away
increases by 0.05 mm.

## Ø4 × 10 root-dowel blind sockets

Stations from the two-marker end: **Ø4.05, Ø4.10, Ø4.15, Ø4.20, Ø4.25 mm**.

1. Use actual Ø4 × 10 cylindrical dowels from the order, not an M4 clevis pin.
2. Start at the farthest station, Ø4.25. If it is loose, move one station
   toward the two markers, using a fresh dowel when necessary.
3. Select the smallest station where the dowel starts straight by hand, seats
   the full 5 mm with gentle smooth-jaw vise or arbor-press pressure, remains
   retained when the coupon is inverted, and causes no whitening, bulging, or
   cracking. Never hammer the pin.
4. It is acceptable to leave a retained test dowel in the selected station.
   The order contains enough dowels; do not damage the coupon trying to recover
   one.

This selects only the hub's locating/retaining side. The proximal link's
Ø4.25 × 5.2 mm sockets remain intentionally looser so the faces can mate by
hand before the six M4 screws clamp the joint.

## M4 × 40 clevis-link passages

Stations from the two-marker end: **Ø4.15, Ø4.20, Ø4.25, Ø4.30, Ø4.35 mm**.

1. Use one actual M4 × 40 single-hole clevis pin from the order.
2. Start at the farthest station, Ø4.35, and move one station at a time toward
   the two markers.
3. Select the smallest station the pin crosses completely with fingertip
   pressure and withdraws from by hand, without free radial rock. Do not use a
   hammer, clamp, abrasive, or drill.

The 9 mm passage is deliberate. Fusion inspection found the final link lands
are 5.0, 5.8, 8.2, and 9.0 mm long. The cartridge eyes between them already
have Ø4.4 × 19 mm passages. A solid 34 mm coupon would not reproduce the real
interrupted stack and could incorrectly select an oversized, sloppy bore.

## Recorded result

The recorded selections are `root dowel Ø4.25; clevis Ø4.25`. No pin dimensions
were requested or used. The hub, proximal link, and distal link were rebuilt in
Fusion and their bed-ready STLs were re-exported after the selection.

There is no Ø6 × 10 ladder. The stop pin is deliberately captured in a Ø6.2
clearance socket by the stop plate's closed skin; its socket neither locates
nor retains the joint, so a tighter empirical fit would add risk without
improving the mechanism.

Fusion B-Rep and mesh evidence, exact station geometry, orientations, and file
hashes are in [`fusion_manifest.json`](fusion_manifest.json). The owner report
and Fusion release record are in the
[release evidence](../../evidence/assembly/2026-09-22_ordered_pin_fit_ladders/).
