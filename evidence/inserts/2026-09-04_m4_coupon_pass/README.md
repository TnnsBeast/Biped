# Owned M4 × 8 ABS coupon — owner PASS, 2026-09-04

The owner reported that the largest hole in the released five-hole M4 ladder
worked. This identifies the nominal **Ø5.3 mm** station. In a follow-up, the
owner confirmed: “Yes, all those checks passed” for square/flush installation,
no splitting or bulging, no spin with a finger-started M4 screw, and resistance
to a firm hand pull after complete cooling.

This is an owner-reported fit/retention result, not a measured pull-out strength
or a new photograph. The insert is the owned Kadriick **M4 × 8** family. The
owner elected to retain M4 at both hubs. Machine-readable observation:
[`result.json`](result.json).

Use this diameter only with the same ABS profile and vertical bore axis as the
coupon. Repeat critical coupons before the later PA-CF structural build.
The canonical receiver map is
[`MANUFACTURING_CONSTRAINTS.md`](../../../MANUFACTURING_CONSTRAINTS.md#threaded-interfaces-in-printed-parts).

## Fusion results and print scope

- [Receiver promotion](fusion_promotion.json): both documents, six Ø5.3
  shoulder and six Ø5.3 wheel receivers; master audit reports zero problems.
- [Assembly paths and print audit](fusion_paths_and_print_audit.json): body
  paths clear, two root screw heads blocked on the straight loading path, and
  wheel-rim overhangs unresolved. The verifier is [verify_fusion.py](verify_fusion.py),
  executed only through Fusion MCP.
- [Release checks](release_checks.json): saved-document status and verified
  bed-ready mesh topology/checksums for the two hubs and unchanged M3 parts.

The corrected shoulder hub is released for detached insert installation and
unplugged motor fit. The link joint, rim print and complete wired fixture are
not released by the successful insert audit. Keep the physical proximal link
and bearings pending the detached screw-loading rehearsal.
