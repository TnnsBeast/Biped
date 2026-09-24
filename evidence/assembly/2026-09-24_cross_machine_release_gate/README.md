# Cross-machine STL release gate — September 24

Scope: every bed-ready print STL exported through Fusion MCP for the ABS
single-leg article, plus the two-leg print and coupon exporters. Fusion
`Beni_SingleLegRig` v30 was used unsaved; no geometry or pinned file changed.
[`release_gate_checks.json`](release_gate_checks.json) and
[`negative_controls.json`](negative_controls.json) hold the results.

## What was wrong

On the owner's second machine (Fusion 2705.1.25), `assert_export()` blocked
every export because its triangle fingerprint could not be reproduced. The STL
header is the same (`ATF 15.15.0.0`); the tessellation is not.

- STL export ignores `surfaceDeviation`. For the PINREV2 hub, 0.00403 and
  0.000403 both give 5640 triangles; only `normalDeviation` changes the mesh.
- `TriangleMeshCalculator` ignores all settings and quality presets: a fixed
  1° segment mesh of 47488 triangles.
- The pinned releases came from a build that honoured a size-relative surface
  deviation. High = 5.0 × 10⁻⁵ × bounding-box diagonal (hub 0.0040 mm, distal
  0.0093, proximal 0.0097 chord). The older stand, plate, cover, post and
  wheel-hub files used Medium, 1.6 × 10⁻⁴ × diagonal (0.0125–0.056 mm).

"High" here therefore means 10° segments on small circles and a 0.0125 mm chord
on large ones. Measured on the proximal Ø19.15 bearing seat:

| Export | Segments | Chord | Across flats |
|---|---:|---:|---:|
| Plain High on this machine | 40 | 0.0295 mm | Ø19.091 |
| Pinned release | 70 | 0.0096 mm | Ø19.131 |
| New release standard | 253 | 0.0007 mm | Ø19.149 |

Plain High would print that seat 0.040 mm tighter than the coupon-derived
release, most of a 0.05 mm ladder step. The fingerprint gate blocked that
silently wrong export, but it also blocked every legitimate one.

## What replaced it

| Piece | Rule |
|---|---|
| [`stl_release.py`](../../../stl_release.py) | One standard for every print export: High plus a normal deviation giving a 0.004 mm chord on the largest curved radius, the finest reviewed release. Hub: 1.937°, measured 0.00399 mm. |
| `mesh_fidelity()` | Machine-independent proof against the reviewed B-Rep at its bed pose. Every vertex classifies On the B-Rep. Every face, edge and vertex sample lies within the chord of the mesh. The mesh is closed with the B-Rep's shell count and sits at z = 0. Bed contact, box, volume and area agree within tessellation. New files need a cylinder chord ≤ 0.005 mm. |
| `assert_export()` | Accepts the pinned fingerprint exactly, otherwise requires `mesh_fidelity()`, otherwise blocks. |
| Exporters | A pinned file that still passes fidelity against the current B-Rep is retained, not rewritten. |
| `accept_shapes()`, `accept_released_files()`, `accept_verified_sources()` | The only baseline writers. Each needs a written reason and appends to `review_log`; exporters never call them. |

## Results

- **Pinned files:** all 15 pass fidelity: 0 vertices off the reviewed surface
  and 0 missing B-Rep samples. Their chords are 0.0011–0.0097 mm for the High
  files and 0.0125–0.056 mm for the five Medium fixture files. All are already
  printed; no reprint is implied.
- **Negative controls:** the gate rejects
  - the September 22 Ø4.25 hub mesh (156 vertices off; the socket radii differ
    by only 0.025 mm);
  - the mislabeled Ø16 distal;
  - a coarse export (chord 0.0127 mm);
  - a hub with one root socket filled;
  - a hub exported on the wrong bed face.

  It accepts the release-standard export and the pinned file. The B-Rep
  receiver mutations are still rejected.
- **Dry runs:** both release scripts complete on this machine:
  - ordered-pin: 4 parts in 48.5 s;
  - spring test: 6 parts in 91.4 s.

  Every file passes the gate. The new meshes agree with the pinned files'
  surfaces within the pinned files' own chord.
- **Release folders:** exporting all 15 parts into their real release
  folders retained every pinned file byte for byte.

## Consequences and rejected alternatives

New files are larger because this build refines uniformly: hub 3.1 MB, proximal
4.3 MB, distal 4.0 MB, compared with 0.3–0.5 MB. Holes in them sit closer to
nominal than in High-era files; the flats move outward by at most the old
chord. For the ordered-pin parts that is under 0.02 mm in diameter (the seat
above: 0.018 mm), below one 0.05 mm ladder step. Coupons and parts exported
after this change share one standard on any machine; export a new coupon with
it before transferring a fit.

- *Reproduce the old triangles:* impossible here; no API setting honours a
  surface deviation.
- *Compare meshes with a 0.03 mm tolerance:* accepts a 0.05 mm diameter
  change and has no reference for new geometry.
- *Write STLs from `TriangleMeshCalculator`:* its segments are fixed at 1°
  regardless of settings, and it needs a custom writer.
- *Keep the size-relative chord:* not controllable per circle on this build;
  a fixed 0.004 mm is simpler and never coarser than a reviewed release.
