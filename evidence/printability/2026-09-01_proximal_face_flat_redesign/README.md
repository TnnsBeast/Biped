# Proximal link face-flat redesign — 2026-09-01

## Trigger

The owner's second ABS proximal-link print used the corrected exact-tangent
release. During support removal, an internal thin edge at the bearing retention
feature broke away. The Ø19.10 bearing seat also printed out of round with its
axis parallel to the bed, so the real 6800-2RS bearing did not fit even though
the same nominal Ø19.10 compensation passed in the vertical-axis ladder.

This invalidates the old assumption that the coupon's bore compensation can be
transferred across print orientations.

## Geometry change

`beni_lib.build_proximal_link()` now extends arm B by the bearing boss's existing
0.8 mm allowance, from the old general arm face at Y = 89.5 to the existing
outboard boss plane at Y = 90.3. It does not move either bearing seat, retention
lip, insert, hub interface or the 58.7…90.3 mm overall knee envelope.

Fusion exact B-Rep verification of the Ø19.10 ABS article reports:

- one solid body;
- 4213.248 mm² coplanar outboard support face;
- 141.9253 × 127.1345 × 31.6000 mm print-oriented envelope;
- two Ø19.10 × 5.0 mm bearing seats and two Ø17 retention openings;
- 66.7616 cm³ solid volume;
- both bearing axes along +Z after a −90° X rotation;
- 20.0 mm fork opening treated as a controlled bridge;
- no slicer support permitted in the channel, bearing seats or at the lips.

The nominal Ø19.00 source body is 66.7915 cm³ and 76.8102 g in Fusion's PA-CF
material. Its support face is 4216.241 mm².

## CAD and mesh verification

The revised body was installed transiently into a clean `Beni_SingleLegRig`
under the full transform guard. `ref_assert()` and `placed_assert()` passed.
All seven Mode A checks passed; the 17-pose shoulder sweep and six-pose floor/
knee check both reported zero clashes. Both bearing insertion and reverse
service paths remain `CAD PATH VERIFIED`, with 0 mm³ interference at every
2 mm sample.

Fusion MCP exported the replacement bed-ready file:

- [`../../../first_article_stl/assembly_dry_fit/ABS_FA_Proximal_Link_L_D19p10_PRINT_ORIENTED.stl`](../../../first_article_stl/assembly_dry_fit/ABS_FA_Proximal_Link_L_D19p10_PRINT_ORIENTED.stl)
- [`../../../first_article_stl/assembly_dry_fit/proximal_d19p10_print_orientation_manifest.json`](../../../first_article_stl/assembly_dry_fit/proximal_d19p10_print_orientation_manifest.json)
- [`../../../first_article_stl/assembly_dry_fit/00_fusion_abs_proximal_d19p10_print_oriented.png`](../../../first_article_stl/assembly_dry_fit/00_fusion_abs_proximal_d19p10_print_oriented.png)

The revised component is saved in `Beni_Prototype1_TestGauges`. The
already-modified `Beni_Prototype1` master was not overwritten; its rebuild is
held behind this ABS physical gate.

Bambu Studio 02.08.02.61 independently reports one part, 6064 facets,
`manifold = yes`, `min_z = 0`, a 141.921310 × 127.126659 × 31.600000 mm mesh
envelope and 66.789734 cm³ mesh volume. An independent edge audit reports zero
degenerate facets and every mesh edge used exactly twice.

## Adjacent-family audit

Fusion audited the immediately related printed families for a broad supporting
plane aligned with their critical circular features. The shoulder plate, both
hubs, both cartridge eyes, wheel rim, encoder bracket, Mode A stand, torque arm,
cable anchor, knee stop plate and magnet carrier already have suitable planes.

`Distal_Link_L` is the one related hold. Its live body already has a 2633.0 mm²
supporting face aligned with the critical Ø10 knee-pin bore, so a geometry change
is not yet indicated. It still needs its real Ø10 h6 pin gate, a face-flat
bed-ready export and a final support/bridge audit before release.

## Physical gate

Print the replacement STL as imported, with supports off. Before installing a
bearing, confirm that the 20.0 mm channel bridge is intact and does not obstruct
the fork. Then repeat the two-bearing insertion test: firm thumb pressure,
square entry, flush seats, no radial rock and tool-free removal. This remains an
unloaded ABS assembly article; PA-CF requires its own same-orientation coupon.
