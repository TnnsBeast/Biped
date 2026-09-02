# Batch 2 — unloaded ABS shoulder assembly

The owner's Ø4.15 GIM6010 output-pin coupon passed on 2026-08-22: it is not a
loose slip fit, but it seats easily with light fingertip pressure.  That is the
selected compensation for this ABS printer/profile.  It does **not** change the
nominal Fusion assembly or release a PA-CF structural part.

## Print now, in this order

The GIM4305 housing coupon has now passed with the real M2.5 screws; these
shoulder prints never depended on that separate wheel-end gate.

1. [`../../print_stl/GAUGE_Fit_Coupon.stl`](../../print_stl/GAUGE_Fit_Coupon.stl)
   — 26 × 92 × 8 mm. Print flat. This is the next short print because it gates
   the Ø19 bearing seats and Ø10 knee axle before either long link is printed.
2. [`ABS_FA_Shoulder_Output_Hub_L_D4p15.stl`](ABS_FA_Shoulder_Output_Hub_L_D4p15.stl)
   — the actual shoulder hub with only its three pin bores changed from the
   nominal Ø4.05 to the owner-tested ABS Ø4.15. Rotate the assembly-coordinate
   STL 90° about X and place the Ø56 flange face flat on the bed.
3. [`../../print_stl/Chassis_Shoulder_Plate_L.stl`](../../print_stl/Chassis_Shoulder_Plate_L.stl)
   — print flat with the panel face on the bed and spiral cable lip upward. The
   GIM6010 housing coupon already released this interface for ABS dry assembly.

Optional while the printer is running:
[`../mode_a/RIG_Cable_Anchor_ModeA.stl`](../mode_a/RIG_Cable_Anchor_ModeA.stl),
with either broad face on the bed. It is useful later but does not gate the leg.

Use the same tuned, enclosed ABS profile as the successful coupon: no scaling
or hole compensation, 0.20 mm layers, 4 walls, 5 top and bottom layers, and
30% infill. These are unloaded geometry/assembly articles, not structural
parts. A brim is fine if this ABS profile normally needs one.

## What to test

1. Put the hub onto all three GIM6010 factory pins simultaneously. It should
   reproduce the Ø4.15 coupon result and reach the metal face with light finger
   pressure. Do not use screws to pull it down. **OWNER PASS, 2026-08-23.**
2. Finger-start two opposite of the six M3 output screws, then check the other
   four. Do not tighten or energise the actuator. **OWNER PASS, 2026-08-23.**
3. **Remove the output hub first.** Hold the plate with its raised circular
   cable-spiral lip facing away from the actuator and its flat panel face toward
   the stationary housing. From the actuator's output/front side, pass the
   plate's centre opening over the **bare output rotor**; the Ø80 actuator
   housing stays behind the plate and never passes through it. Seat the plate on
   the stationary housing face, finger-start two opposite M3 housing screws,
   then confirm the remaining six. Only after the plate is seated should the
   output hub be reinstalled. Do not draw the plate sideways with screws.
   Use **M3 × 8** housing screws for fastening; M3 × 10 bottoms in the
   actuator's 4.0 mm-deep threads before it can clamp this 5 mm plate.
   **OWNER ASSEMBLY PASS, 2026-08-23.** The staged
   Fusion views and owner evidence are
   [`../../evidence/shoulder_assembly/2026-08-23_plate_sequence/`](../../evidence/shoulder_assembly/2026-08-23_plate_sequence/).
4. When the 6800 bearings and Ø10 axle/dowel are on the bench, test the fit
   coupon before printing either link. The Ø19 bearing bore must be a
   thumb-pressure light press with no rock. The Ø10 h6 × 35 mm knee pin must be
   a light press, not a loose slip: the pin-to-distal-link press is the rig's
   angular reference. Record fit only; do not alter the coupon.

Stop after this batch until the remaining gates close:

- Do not print `Proximal_Link_L` until the real 6800 bearing passes the Ø19
  gauge (thumb-pressure light press, no rock).
- GIM4305 housing is **OWNER PASS, 2026-08-23** with the real M2.5 screws. Do
  not print the rerouted `Distal_Link_L` until the remaining real Ø10 h6 knee
  pin passes the fit coupon as a light press.
- Do not install/preload the knee spring or apply torque-arm, ground-traction,
  stall, proof or drop load through these ABS parts. After the complete leg and
  electronics gates close, the Mode A stand may hold it for wheel-clear,
  current-limited, short slow motor commands under self-weight only.
- While the steel knee pins are in transit, a deliberately loose printed ABS
  pin may align a fully supported mock-up for hand posing only. It is not the
  Ø10 h6 fit gauge or angular datum. Do not release the distal link or run a
  motor, spring, ground-contact or load test on the printed pin.
- Repeat the critical coupons immediately before the later two-leg PA-CF
  structural build; the Ø4.15 ABS result must not be copied blindly into the
  PA-CF hub.

## Verification

Fusion MCP generated this transient component from `Beni_SingleLegRig`,
exported the high-refinement binary STL, and then discarded the cloud-document
change. Fusion was reopened clean. Exact B-Rep validation found one solid,
three Ø4.15 cylinder faces on the manufacturer-derived Ø20.4 PCD, and the
nominal 56 × 14 × 56 mm envelope. Independent mesh checks found 5,616
triangles, one closed manifold shell, zero open/non-manifold edges, and zero
degenerate triangles. [`fusion_manifest.json`](fusion_manifest.json) records
the Fusion result.

![Fusion view of the Ø4.15 ABS first-article hub](00_fusion_abs_shoulder_hub_d4p15.png)

---

# Batch 3 — unloaded ABS proximal-link bearing rehearsal — complete

The owner's Ø19.10 ladder bore passed on 2026-08-31. The face-flat full-depth
Ø19.10 link then accepted both real bearings on 2026-09-02 and remains the build
article, but the owner reports that it is slightly tighter than preferred.
Ø19.15 is now preferred for any future ABS proximal print because the ladder
bore retains the bearing without movement at easier thumb pressure. No
replacement link is required. Physical record:
[`../../evidence/knee_fit/2026-09-02_proximal_link_full_depth/`](../../evidence/knee_fit/2026-09-02_proximal_link_full_depth/).

## Printed article retained

Print
[`ABS_FA_Proximal_Link_L_D19p10_PRINT_ORIENTED.stl`](ABS_FA_Proximal_Link_L_D19p10_PRINT_ORIENTED.stl)
in the same enclosed ABS profile as the passing ladder: no scaling or slicer
hole compensation, 0.20 mm layers, 4 walls, 5 top and bottom layers and 30%
infill. This is an unloaded assembly article, not a structural proof part.

The `_PRINT_ORIENTED` file is already face-flat on the outboard arm/bearing
face, with both Ø19.10 bearing axes along +Z. **Do not rotate it or use “lay on
face.”** Its mesh envelope is 141.921 × 127.127 × 31.600 mm with `min_z = 0`.
Set supports off. The 20.0 mm fork opening is a controlled bridge; no support
may touch that channel, either bearing seat or either Ø17 retention lip. Use a
normal ABS brim if the tuned profile benefits from one. The assembly-coordinate
file without the suffix is retained for traceability, but is not the file to
print.

This is the third release attempt. Print 1 exposed the unequal-circle tangent
error; that source correction remains. Print 2 used the corrected on-edge datum,
but support removal broke an internal Ø17 retention edge and the horizontal
bearing seat was not round enough for the real bearing. The passing ladder bore
was vertical, so its compensation did not transfer to a horizontal production
bore.

The redesign extends arm B by the bearing boss's existing 0.8 mm allowance so
the whole outboard arm shares the existing Y = 90.3 boss plane. It does not move
the bearing stack or widen the 31.6 mm knee envelope. Fusion verifies a
4213.248 mm² support face and 66.7616 cm³ ABS article.

## Bearing installation rehearsal

Status: **PHYSICAL BEARING FIT VERIFIED from the owner report.** The existing
Ø19.10 link is retained; Ø19.15 is a future-ABS preference, not a reprint order.

1. Confirm the unsupported channel bridge is intact, with no loose strands or
   droop obstructing the fork. There should be no slicer support to remove.
2. Keep the proximal link detached. Do not install the distal link, axle,
   cartridge, stop arc, encoder or cables first.
3. Do not apply retaining compound during the ABS rehearsal.
4. From the inboard open face, press the first 6800-2RS bearing in the +Y
   direction using both thumbs on the **outer race** until it seats on the Ø17
   retaining lip.
5. From the outboard open face, press the second bearing in the −Y direction in
   the same way.
6. Both bearings must enter squarely with firm thumb pressure, finish flush with
   the outside boss faces, and have no perceptible radial rock. Do not use a
   clamp, hammer, screw or fastener pull-down. Stop if the full-depth pockets
   feel materially tighter than the ladder.
7. Leave the bearings installed for the next unloaded knee dry assembly. For
   service, remove the detached link and reverse the same open-face paths with
   an internal bearing puller; sacrificing the bearing being replaced is
   acceptable, damaging the printed link is not.

There are no fasteners or cables in this operation. Fusion sampled both full
insertion paths every 2 mm and found 0 mm³ interference at every pose, including
the final seats. The reverse paths are the service paths. Records:

- [`proximal_d19p10_fusion_manifest.json`](proximal_d19p10_fusion_manifest.json)
- [`proximal_d19p10_print_orientation_manifest.json`](proximal_d19p10_print_orientation_manifest.json)
- [`proximal_d19p10_path_verification.json`](proximal_d19p10_path_verification.json)

Fusion exact-B-Rep verification found one solid body, two Ø19.10 cylindrical
seat faces, 5.0 mm seat depth and the two Ø17 retaining-lip openings. The prior
topology fixes remain: Ø8.2 harness clearance prevents the root-access tangent,
and the R1.0 relief removes the open-channel knife edge. The final Fusion
high-refinement print-oriented STL has 6,064 facets; Bambu Studio 02.08.02.61
reports one part, `manifold = yes`, `min_z = 0`, and a
141.921310 × 127.126659 × 31.600000 mm mesh envelope.

![Fusion view of the face-flat link with both bearing axes vertical](00_fusion_abs_proximal_d19p10_print_oriented.png)

PA-CF is deferred to the later two-leg structural build. Repeat the bearing
coupon in PA-CF immediately before those structural prints; no ABS compensation
transfers.
