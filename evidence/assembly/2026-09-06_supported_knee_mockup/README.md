# Supported knee mock-up release — 2026-09-06

The owner requested an interim assembly while the steel knee pin is in
transit. The [print and bench traveller](../../../first_article_stl/knee_mockup/)
is the canonical procedure for this batch. All design, inspection, exports,
screenshots and mesh verification used the Fusion MCP.

## Scope and geometry

- One provisional ABS distal link, one Ø9.7 alignment pin and two detached
  spring-seat fit caps. No extra inserts or fasteners are required.
- Both links stay supported, motors and spring cartridge absent. The caps
  check the owned OD18 / ID9 × 50 spring off the leg with no compression.
- The saved rig's native distal body supplied the geometry. The wheel flange's
  Y64.5 underside was extended to the existing Y59.5 bed plane without changing
  the motor-facing Y67.5 datum or its apertures.
- The original Ø16 thrust extensions at Y63.7…65 and Y84…85.3 were removed from
  this mock-up. They need supports on bearing-contact faces and prevent radial
  entry with both bearings already installed. Separate spacers would retain
  the latter obstruction, so none is installed. The native 19 mm tongue stays
  between Y65…84, within the fork's Y64.5…84.5 channel.
- The temporary pin's Ø9.7 shaft, Ø18 × 3 grip, 40 mm shaft length and 0.8 mm
  tapered lead are explicit new mock-up dimensions in the script, not measured
  hardware or a steel-pin tolerance. The caps' Ø8 × 4 pilots, Ø20 × 2 bases and
  Ø5.6 through bores are detached fit-coupon dimensions, not a preload redesign.

The complete rig and master cartridge geometry remain baseline. This batch
does not close steel-pin fit, thrust retention, encoder coupling, cartridge
adaptation, spring rate, wheel-rim printing or powered assembly gates.

## Verification

[assembly_audit.json](assembly_audit.json) records:

- Zero intersection at 161 radial tongue insertion/removal positions over
  80 mm, with the current ABS proximal-link geometry and both bearings present.
- Zero intersection for continuous swept shaft and grip insertion envelopes.
- Zero intersection in 73 hand-pose samples from −8° to +28° at 0.5° increments.
  These are sampled geometric checks, not a continuous motion proof or physical
  travel-stop release. The owner procedure uses small supported hand movements.
- Zero interference when the conservative OD18 / ID9 annular spring envelope
  slides onto the detached Ø8 cap pilot. This does not measure the spring rate.
- One solid, one lump and two adjacent faces on every B-Rep edge for each part.

[support_audit.json](support_audit.json) records native face-extruded support
envelopes with 0.6 mm wall separation, protected hole/land regions, and clear
withdrawal paths. Each path uses 81 positions over 40 mm. The knee-web support
withdraws toward −Y; the channel support exits through its open side at
directions 150° or 165° in the source XZ plane. The raised surfaces are identified
in the geometry report; the small slot-corner ceiling remains a controlled
bridge. All curved distal faces are cylinders parallel to the print axis.

[exports.json](exports.json) proves an exact bed plane and vertical bores in
each exported orientation. [mesh_verification.json](mesh_verification.json)
records hashes, bounding boxes, zero degenerate triangles and zero open or
non-manifold edges. Binary STLs were checked inside Fusion via MCP, without
mesh repair. The [September 7 owner report](../2026-09-07_owner_mockup/)
confirms printing, successful provisional assembly, free supported movement,
easy pin removal and detached cap fit. Detailed support-removal quality was
not separately reported; final steel-pin/retention release remains open.

## Reproduce

With `Beni_SingleLegRig` active, execute
[`knee_mockup_fusion.py`](../../../knee_mockup_fusion.py) through Fusion MCP.
It copies native geometry into the separate `Beni_Knee_Supported_DryFit`
document, builds the mock-up, audits paths, exports candidates under
`/tmp/biped-knee-release`, and verifies their meshes. It then exports a native
Fusion archive and queues its upload through Fusion's API. After upload,
open the returned DataFile through MCP and call `record_saved` to compare the
reopened native part volumes/topology with the release audit. Do not re-upload
while an upload is pending. Inspection support bodies
are labelled `REFERENCE_` and are not print parts. The source rig's reference
placements are rechecked before recording the saved document.

The released files are copied to the traveller directory only after visual
review. [Fusion save record](fusion_document.json): `Beni_Knee_Supported_DryFit`
v1 was reopened from its completed cloud upload and matched all three parts.
The source rig was saved at v21 after inspection, with its original distal
geometry and reference placements unchanged. The master remains v16.
