# Mechanical assembly audit and reprint decision — September 23

Scope: all **15 printed parts** in the 21-step ABS mechanical assembly manual.
The owner photographed a steel knee pin visibly loose in the printed distal
receiver. Fusion MCP inspection confirmed a Ø16 hole in v29 and in the
September 22 released mesh despite its D10p30 filename.

Saved and verified in **Beni_SingleLegRig v30**.

[Owner photograph](owner_pin_clearance.jpg).

## Reprint decision

| Printed part | Decision | Reason / required version |
|---|---|---|
| Shoulder output hub | **Reprint** | Owner now requests Ø4.30 root-dowel sockets, +0.05 mm beyond the Ø4.25 ladder selection. Motor-pin passages remain Ø4.15. |
| Proximal link | **Reprint** | Root sockets and clevis-link passages become Ø4.30. Bearing seats remain Ø19.15; five M3 receivers remain Ø4.5. |
| Distal link | **Reprint** | Restore the missing Ø10.30 × 20.0 knee receiver and use Ø4.30 clevis-link passages. Stop socket remains Ø6.2. |
| Captive knee-stop plate | Keep | Current ordered-pin closed-skin version; channel/skin and mounting holes verified. |
| Upper cartridge eye | Keep | Original September 17 released file is correct; Ø4.4 passage and Ø8 spring pilot unchanged. |
| Lower cartridge eye | Keep | Original September 17 file; Ø4.4 passage and Ø8 spring pilot unchanged. |
| Guide bar | Keep | Original September 17 full-length, 3.8 mm square guide file is correct. |
| Outboard D10 spacer | Keep | Original September 17 file; locator and pin-end clearance retained. |
| Keeper bracket | Keep | Original September 17 file; locating and mounting interfaces retained. |
| No-tyre wheel shell | Keep | Original September 17 file; insert-tip reliefs, mounting pattern and service path retained. |
| Wheel hub | Keep | Released Ø5.3 M4 receiver version; motor register and mounting holes verified. |
| Cable cover | Keep | Released M3-clearance version. |
| Front cable post | Keep | Released cover-mount version. |
| Mode A stand | **Conditional keep** | Released Ø4.5 × 6.0 M3 receiver version passes. Owner's physical print revision is still unidentified; replace an older Ø4.0 version. |
| Shoulder plate | **Conditional keep** | Released Ø4.5 M3 receiver version passes. Owner's physical print revision is still unidentified; replace an older Ø4.0 version. |

Download the three **PINREV2** replacements from the
[current print queue](../../../../README.md#current-print--ordered-pin-unpowered-abs-mechanical-article).
The owner clarified that only the root-dowel and clevis-link fits should grow,
by **+0.05 mm**, not +0.10 mm. The bought bearings, D10 knee receiver,
factory motor-pin holes, cartridge eyes and stop-pin socket/channel retain their
previous intended sizes. Ø4.30 is an owner-requested fit candidate, **not a
newly passed coupon result**. Confirm easy hand insertion and withdrawal,
flush root mating faces and no objectionable assembled play. The root screws
capture the dowels; both clevis pins still require their washers and cotters.

## What failed

1. **Missing knee receiver after rebuild.** The original two-leg builder cuts
   Ø16 for a separate sleeve. A later rig conversion adds the printed Ø10.30
   receiver. September 16 and September 21 meshes contain that receiver;
   September 22 commit `56b2507` does not. Rebuilding the distal link had lost
   the conversion, while the export retained a D10p30 name. A clear pin path
   and manifold mesh could both pass despite an oversized bore.
2. **Unscoped revolve cuts.** Live v29 also differed from the retained upper
   eye and guide files. Legacy `Cart_Upper_Eye_L` / `Cart_Lower_Eye_L` revolve
   cuts (timeline 996 and 1012 before correction) affected other components.
   The upper eye's CAD volume was 4465.839353 mm³ instead of 4477.220539;
   the guide was 577.303874 mm³ instead of 804.308000. Restricting those cuts
   to their intended components restored both parts. Fresh Fusion exports
   then exactly matched the previously released eye and guide meshes.
   **Their physical prints do not need replacement for this CAD corruption.**

The corrected link builder now creates its ABS receiver itself whenever it runs
in `Beni_SingleLegRig`; the separate rig conversion is idempotent. Revolve cuts,
like extrude cuts, now explicitly name their participating bodies.

## Evidence and release gate

- `before.json`: live v29 shapes, original mesh hashes, all 15 source/file
  comparisons, and the measured missing-receiver failure before repair.
- `inventory.json`: repaired intended geometry versus the original 15 print
  files, before the owner's new Ø4.30 preference. Nine meshes match exact
  triangle geometry; five older exports use coarser tessellation.
- Older plate/cover/post/wheel-hub meshes pass bidirectional vertex and facet-
  centroid comparisons within 0.03 mm. The stand's coarse large arcs reach
  0.054419 mm, within the documented 0.06 mm mesh-comparison threshold; all
  five fit-critical receiver vertex rings separately measure Ø4.5 over 6.0 mm.
  These thresholds describe mesh approximation, not extra fit allowance.
- `pin_clearance_revision.json`: only the three requested parts change for
  Ø4.30, with independently measured interface diameters and axial spans.
- `rebuild_regression.json`: rebuilding the link preserves its integral
  receiver, repeating the receiver operation changes nothing, and unrelated
  printed shapes stay unchanged.
- `negative_controls.json`: missing, oversized and shortened receiver
  mutations, and the old mislabeled STL, are all rejected. A deliberately
  overlapping revolve cut leaves all 15 printed parts unchanged.

`mechanical_release_audit_fusion.py` checks required parts, measured interface
positions/diameters/depths, and every native face against the independently
reviewed `mechanical_release_baseline.json`. The source geometry check runs
before the active-article exporters and the mechanical audit; bed-oriented
exports also require the reviewed triangle-geometry fingerprint. The motion
audit repeats the shape check afterward to catch incidental edits. Manual
captures require the same gate. Exporters cannot update the baseline.

A deliberate design change requires review of the baseline diff, applicable
coupon/owner-fit evidence, assembly/service paths, print orientation and fresh
mesh evidence in the same commit. A filename, echoed builder constant, mesh
volume or clash-free motion alone is not proof of an interface fit.

Physical final-part acceptance remains open. This audit does not establish the
condition of each physical print, actual pin/bearing fits, insert retention,
spring rate, a wired assembly or permission for ground/structural loads.


Final verification: v30 passes all 32 measured interface contracts, the 24-pose
mechanical sweep, stop proof, insertion/service paths, threaded receivers,
proximal screw seats/access, Ø10.29/10.30/10.31 knee-bore probe bracket, and
selective-support removal. The refreshed exports pass manifold/bed checks and
reviewed native-mesh fingerprints. See `fusion_mechanical_audit.json`,
`fusion_release.json`, `fusion_release_manifest.json` and `final_release.json`.
The 29 manual views and README ABS gallery were recaptured through Fusion MCP.

Before committing/publishing, run `python3 verify_mechanical_release.py`.
The same check runs on GitHub pushes and pull requests, comparing all 15 released
file hashes and verified source hashes. It cannot run Fusion in CI and does not
replace the native geometry, path or physical checks. Exporters stage candidate
meshes and only replace a released file after its geometry/orientation check
passes. The baseline is reviewed evidence, never an auto-generated escape hatch.
