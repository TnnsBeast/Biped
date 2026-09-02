# Link print-datum audit — 2026-09-01

## Trigger

The owner reported that the ABS proximal link struggled to print because the
released native/on-edge orientation had no convincing flat bed face. That
observation was correct.

## Root cause

Fusion exact-B-Rep inspection found that the apparent long planar side stopped
**0.6079 mm above** the true low extrema of the two circular ends. The shared
`lozenge()` helper used `pi/2 + alpha` for the external tangent contact radius;
the correct sign is `pi/2 - alpha`. The old straight segment was therefore on
the chord side of each unequal end circle rather than tangent to both.

This was not treated as ABS shrinkage, a slicer problem, or a reason to add
throwaway feet. `beni_lib.lozenge_tangent_points()` now computes the exact
external-tangent contacts and both `pl_ep()` and `dl_epd()` derive their channel
wall line from the same function.

## Corrected ABS proximal article

Fusion MCP rebuilt the Ø19.10-seat first article in
`Beni_Prototype1_TestGauges`, verified one solid, and exported both the assembly
coordinate trace file and this bed-ready release:

- [`../../../first_article_stl/assembly_dry_fit/ABS_FA_Proximal_Link_L_D19p10_PRINT_ORIENTED.stl`](../../../first_article_stl/assembly_dry_fit/ABS_FA_Proximal_Link_L_D19p10_PRINT_ORIENTED.stl)
- [`../../../first_article_stl/assembly_dry_fit/proximal_d19p10_print_orientation_manifest.json`](../../../first_article_stl/assembly_dry_fit/proximal_d19p10_print_orientation_manifest.json)
- [`../../../first_article_stl/assembly_dry_fit/00_fusion_abs_proximal_d19p10_print_oriented.png`](../../../first_article_stl/assembly_dry_fit/00_fusion_abs_proximal_d19p10_print_oriented.png)

Fusion exact geometry:

- external-tangent support area: **3462.967 mm²**
- print rotation: **+134.260830° about Y**
- print-oriented B-Rep envelope: **169.3985 × 31.6000 × 62.0000 mm**
- minimum Z: **0.0000 mm**
- solid volume: **64.0181 cm³** (old pseudo-tangent article: 62.9765 cm³)
- bearing seats: **2 × Ø19.10 × 5.0 mm**, behind Ø17 retaining lips
- fork channel: open sideways; no trapped internal support

Bambu Studio 02.08.02.61 independently reports one manifold part, 6244 facets,
`min_z = 0`, a 169.386 × 31.600 × 62.000 mm mesh envelope, and 64.047 cm³ mesh
volume. The 5.1 mm³ mesh/B-Rep volume difference is tessellation error (0.008%).

The detached-link bearing insertion and reverse service paths were re-run after
the outline correction at 2 mm increments. Both sides remain
`CAD PATH VERIFIED` with 0 mm³ interference at every sample.

A rebuilt canonical one-leg assembly was also checked at the six combined
motion-envelope corners `(shoulder = 0, -185, +185°) × (knee = -8, +27°)`.
After excluding the intentionally co-located TestGauges coupons and duplicate
ABS first article, Fusion reported **0 genuine canonical clashes at all six
poses**. The saved owner-modified master document was not overwritten.

## Other print parts

The same Fusion supporting-plane audit found obvious large flat datums on the
shoulder plate, chassis frame, wheel rim, cable cover, encoder bracket,
electronics tray, shoulder hub, and wheel hub. They do not need a geometry
redesign for bed contact.

`Distal_Link_L` shares the corrected unequal-circle helper, but its wheel-end
plate and boss make its print case different. It is still gated by the real
Ø10 h6 knee-pin fit and needs its own final print-oriented re-export and exact
support/overhang check before printing. Do not infer its orientation from the
proximal file or use the legacy tall/native instruction as a release.

## Remaining physical gate

**[SUPERSEDED PHYSICAL RESULT, later 2026-09-01.]** The exact tangent fixed the
bed-contact defect, but the corrected on-edge article still failed its DFM gate:
support removal broke an internal Ø17 bearing-retention lip and the horizontal
Ø19.10 seat was not round enough for the bearing. The tangent correction remains
valid source geometry; only this print orientation/release is superseded.

The face-flat redesign and replacement release are recorded in
[`../2026-09-01_proximal_face_flat_redesign/`](../2026-09-01_proximal_face_flat_redesign/).
