# Shoulder access correction and assembly audit — 2026-09-05

The owner printed the Ø5.3 M4 shoulder hub and installed its inserts successfully.
The link attached, but a wall obstructed outer fastener access. The exact owner
report is in [owner_report.json](owner_report.json). Keep that hub in service.

## Proximal-link corrections

Fusion inspection found two defects, both in the shoulder end:

- The internal channel wall crossed two of the six M4 head insertion paths.
  The Ø9 access passages now continue from Y67.5 through the outboard arm.
  The Ø7.5 counterbores and Y63.3 screw seats retain their original dimensions.
- The large lightening opening cut away part of one screw seat. Exact solid
  intersection measured a supported fraction of 0.5229817396859231. Moving the
  slot's first centre from proximal u36 to u44 leaves complete seating lands
  under all six Ø7 heads. These are explicit new design dimensions.

The five M3 insert pockets at the knee have clear mouths and complete Ø5.5
design-envelope lands. The six shoulder M4 inserts belong in the **hub**;
the link holes in this area are screw clearances and counterbores.

[Before](link_before.png) · [After](link_after.png) ·
[Initial exact access audit](before.json) · [Original seat support](root_seats_before.json)

The new ABS print uses the owner's already-selected Ø19.15 bearing preference.
Its bearing axes remain vertical on the same outboard face as the successful
face-flat article. No assembly datums, bolt patterns, insert depths or screw
lengths change at the hub/link interface. The shorter lightening opening is
part of the seat correction, not a change to the leg kinematics.

## Adjacent parts and assembly findings

| Part / family | Finding and disposition |
|---|---|
| Shoulder hub | Six Ø5.3 × 8 receivers clear from the detached link face; owner installation PASS. Retain this print. |
| Proximal link | Two obstructed head paths and one incomplete seat corrected. Six continuous head/shank/Ø6 driver paths and full seat lands are release gates in `beni_lib.audit_proximal_access()`. |
| Knee M3 pockets | All five paths and seating envelopes clear. The printed corrected link has failed Ø4.0 pockets; replace it with the Fusion-verified Ø4.5 revision before M3 installation. |
| Shoulder plate / cover | Four insert paths clear; four screws enter outboard. The released plate has owner-selected Ø4.5 receivers. Replace a prior Ø4.0 plate; the cover contains no inserts. Fit housing screws before the cover, and reverse that order for service. |
| Shoulder housing screws | CAD/source updated to the physically accepted M3 × 8; the previous model still showed ×10 despite the owner-observed bottoming. |
| Mode A stand | Five owner-selected Ø4.5 × 6.0 blind M3 receiver paths are open from the detached mount face. The source and bed-ready STL passed Fusion verification. Install inserts before attaching the panel, and attach the panel before fitting post A, which covers one panel-bolt approach. Bench access retains its checked mount-face orientation. |
| Front cable post A | Old post intersected the cover. New flat sector mounts outside the cover on its upper two Ø88 holes. Use two **M3 × 12** in place of those two cover M3 × 10 screws; the other two cover screws stay ×10. The Ø8 cable eye is at Z52, beyond the cover's r47 edge. It is a strain-relief/tie eye; no claim that a terminated connector fits through it. |
| Rear Mode A cable anchor | Separate fixed-harness anchor retained; fit before enclosing the rear wiring. |
| Wheel hub / rim | Six hub insert mouths and six rim protrusion reliefs clear. Heat the hub inserts from its motor face before mounting it; rim screws enter outboard. Rim still has a separate printability hold for the 14 mm inward ledge and retaining flange. Altering those features also affects the tyre interface, so this audit does not release a revised rim. |
| Distal link / wheel motor mount | Modelled screw heads clear. Install/service the rear-facing M2.5 screws with the leg supported off the stand; the stand obstructs their long axial approach. Full distal print release still needs the real Ø10 × 35 pin and its own final printability/path gate. |
| Stop plate / encoder bracket | Modelled screw heads clear; insert depths and screw reach pass. Fit stop screws before the encoder bracket; its Ø5 apertures pass a driver, not the Ø5.5 heads. Remove the bracket to withdraw those screws. Full knee assembly awaits the pin and retention solution. |
| Knee collar / magnet carrier | No heat-set receiver redesign is implied. Existing collar cannot yet retain the ordered pin; do not print it as an accepted retention solution before the delivered pin/end interface is verified. |
| Cartridge eyes, guide rod, shims, bumper | No additional heat-set receivers. Existing motion checks remain geometric only. **Owner correction, 2026-09-06:** the received spring is the ordered 50 mm part; the earlier longer-length report was a typo. Cartridge adaptation to its OD18 / ID9 remains unfinished; see the [spring record](../../springs/2026-09-05_reconciliation/). |
| Tyre | No insert or screw seats. TPU tyre installation/retention is still coupled to the held rim. |
| Chassis frame and remaining two-leg parts | Master receiver/head geometry passes; both corrected legs have matching volume and face counts. Physical build remains deferred. |
| Mode B carriage and fixtures | Absent from the active Fusion article. Source receiver corrections remain deferred and require a rebuilt Fusion audit when Mode B resumes. |
| Torque arm / scale / floor | Alternative/deferred load-test equipment. The torque arm cannot coexist with the proximal link at the same hub. The rigid-floor/contact contradiction remains unresolved for the future loaded procedure. |

This audit does not certify that every stage of the complete robot can already
be built or powered. Missing hardware, the rim printability problem, knee-pin
retention, cable routing with the actual harness, and electronics gates remain
explicit holds. Only self-weight, wheel-clear, current-limited operation may
eventually use the complete ABS article after those gates close.

## Verified saved models and files

- [Rig final audit](rig_after.json): 26 receiver mouths have clear continuous
  installation envelopes and complete mouth lands. The six link screw seats
  are complete; blind-depth and head-spacing checks pass. The report retains
  the expected intersections with the alternative torque arm, which cannot
  be fitted alongside the leg.
- [Ordered assembly/removal paths](ordered_paths.json): four mating-part paths
  each pass 81 sampled positions over 40 mm travel. All 49 screws pass continuous
  swept head, shank and driver-envelope checks in the stated assembly order.
  The cable eye passes its Ø6 tie-access envelope.
- [Motion geometry](rig_motion_checks.json): the 17 shoulder poses from −120°
  to +120° pass the existing stand/part clash check, which excludes screws,
  the floor and alternative load-test fixtures. Knee wheel-axis deviation from
  the reference table is 0.042865894902575974 mm, below the 0.15 mm gate.
  These are CAD checks, not permission to load or power the ABS article.
- A separate final hardware audit caught a [wheel-screw pose regression](rig_pose_regression.json):
  the old classification depended on current Z position and changed as the
  wheel rotated. Classification now uses the invariant Y seat. The three
  screws were restored to their source datums; [actual occurrence checks at
  both shoulder extremes](wheel_pose_classification.json) pass, followed by
  the final nominal head-spacing and all 49 ordered hardware-path checks above.
- [Master final audit](master_after.json) and [save record](master_save.json):
  `Beni_Prototype1` v16 saved at this access-fix milestone, `audit_all()` reports zero problems, 33 mirrored
  families match. The canonical link STL and all four README Fusion views
  were refreshed. [Rig save record](rig_save.json): `Beni_SingleLegRig` v18 saved
  at this milestone. The later Ø4.5 M3 promotion is saved as rig v23 and master
  v18 in the [September 14 receiver record](../../inserts/2026-09-14_m3_coupon_pass/).
- [Proximal release](proximal_release.json), [post release](post_a_release.json)
  and [exported mesh checks](export_artifact_checks.json): both new bed-ready
  STLs are closed, have no degenerate facets, and sit at Z0. The link's two
  Ø19.15 × 5 bearing seats also pass continuous insertion/removal envelopes.

[Corrected cable-post assembly in Fusion](shoulder_stack_after.png).

## Reproduction and acceptance

Run the Python files in this directory **through Fusion MCP**, never in local
Python as a substitute for Fusion. `verify_fusion.py` writes exact B-Rep
envelope evidence; `release_fusion.py` builds the ABS variant from the source,
checks bearing insertion/removal, head paths, seat support, solid topology and
bed faces, then exports a bed-ready STL. Historical failed reports are retained.

Use the same enclosed ABS profile as the passing coupons: 0.20 mm layers,
4 walls, 5 top/bottom layers, 30% infill, no scaling or hole compensation.
Import the supplied orientation unchanged and disable supports. The existing
20 mm channel and root-pad ceilings require controlled bridging; inspect the
slicer preview and printed undersides, bearing lips and counterbore floors.

Before putting the replacement link on the hub, all six M4 × 10 heads must
pass through their access holes and rest flat without force. Install bearings
from their two open faces using pressure on the outer races; both must sit
square and have no perceptible rock. Reuse old bearings only if they can be
removed without damage. Install the five M3 inserts only in the new Ø4.5
revision while the knee is open; do not use the prior printed Ø4.0 pockets.
Support the knee end, attach the link to the accepted hub, finger-start all six
screws, and confirm each head clamps flat without drawing the print into place.
Repeat removal once. Record the physical result before any powered step.
