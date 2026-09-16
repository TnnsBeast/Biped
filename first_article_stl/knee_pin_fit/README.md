# ABS knee-pin bore ladder — print and test

The received metal pin seized in the provisional shin's nominal Ø10 printed
bore. This calibration print replaces another full-link trial. Each station
reproduces the final distal link's **Ø22 boss, 19 mm engagement and bed-normal
bore axis**.

## Print

[Download the print-oriented STL](ABS_CAL_KNEE_PIN_BORE_LADDER_PRINT_ORIENTED.stl).

- Quantity: 1
- Material/profile: the same tuned enclosed ABS profile used for the active leg
- Layer height: 0.20 mm
- Walls: 4
- Top/bottom layers: 5 / 5
- Infill: 30%
- XY hole compensation: 0
- XY contour compensation: 0
- Supports: off
- Orientation: import unchanged; the thin runner and index tab are on the bed,
  and all five pin bores are vertical

The two small holes mark the **Ø10.05 end**. Moving away from them, the five
stations are:

| Station from marked end | Nominal bore |
|---:|---:|
| 1 | Ø10.05 mm |
| 2 | Ø10.10 mm |
| 3 | Ø10.15 mm |
| 4 | Ø10.20 mm |
| 5 | Ø10.25 mm |

These are calibration candidates. None is a released distal-link dimension
until the physical test selects it.

## Test

1. Inspect the recovered pin for scoring or a raised end burr. Do not sand its
   ground journal. Use one pin for every station.
2. First pass that pin through each 6800 bearing separately, without the shin.
   It must insert and withdraw under controlled thumb pressure. Stop and report
   if either bearing needs impact or clamp force.
3. Test the ladder dry and at room temperature, starting at the two-hole
   Ø10.05 end. Do not jump to a larger station first.
4. Push only with your fingers. Stop a trial as soon as force rises sharply.
   The 35 mm pin remains 16 mm exposed through the 19 mm coupon, so withdraw or
   push it back using the exposed ends. Do not hammer it into a station.
5. Select the **smallest** station that accepts controlled thumb pressure,
   does not spin freely in the boss and remains removable. Report the station
   number and whether the cooled pin spins, rocks or pulls out by hand.

If every station is too tight or the pin becomes trapped, break only that coupon
boss and report the last attempted station. Do not print the final shin yet.

## Verification

Fusion MCP built and inspected one closed solid with exact Ø22 × 19 mm stations
and bores Ø10.05–Ø10.25 in 0.05 mm steps. The print-oriented high-refinement STL
is a closed, non-degenerate manifold at Z=0. See
[`fusion_manifest.json`](fusion_manifest.json) and
[`mesh_verification.json`](mesh_verification.json).

![Fusion view of the print-oriented ladder](00_fusion_ABS_CAL_KNEE_PIN_BORE_LADDER_PRINT_ORIENTED.png)

