# ABS proximal link — full-depth bearing result

Date: 2026-09-02
Source: owner physical test report in the project task

## Result

The face-flat
`ABS_FA_Proximal_Link_L_D19p10_PRINT_ORIENTED.stl` article printed successfully
and accepted both real 6800-2RS bearings. The owner reports that the bearings fit
properly, but the Ø19.10 full-depth seats are slightly tighter than preferred.
The existing link remains usable and does not need to be reprinted.

The owner re-evaluated the indexed Ø19.05–Ø19.25 ladder. The third bore from the
two-hole Ø19.05 index end is Ø19.15. It accepts the bearing with easier thumb
pressure while retaining no perceptible movement.

Classification:

- **Ø19.10 full-depth ABS link: PASS, usable, tighter than preferred.**
- **Ø19.15 ladder bore: preferred future ABS process compensation.**

No photograph was supplied for this observation. The record is the owner's
verbal fit report.

## Source-default verification

After changing the future-ABS source default to Ø19.15, a transient Fusion MCP
build on 2026-09-02 verified one solid body, exactly two Ø19.15 bearing-seat
faces, a native envelope of 141.9253 × 31.6000 × 127.1345 mm, and the retained
face-flat print transform with both bearing axes along +Z and minimum Z = 0.
No STL or replacement component was saved. The clean Fusion documents were
restored after the check.

## Disposition

- Keep the installed bearings in the existing Ø19.10 ABS link for the unloaded
  single-leg integration article.
- Do not generate or print a replacement proximal link solely for this change.
- Any future ABS proximal-link export uses Ø19.15 with the same face-flat,
  bearing-axes-vertical orientation and support prohibition.
- The real bearing reference remains Ø19.00. Recalibrate the bearing seat in
  PA-CF immediately before the later two-leg structural build; no ABS
  compensation transfers to PA-CF.
