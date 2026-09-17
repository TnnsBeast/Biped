# Steel knee pin in the provisional ABS shin — owner result

Date: 2026-09-15  
Source: owner physical test report in the project task

## Result

The bought metal knee pins have arrived. Their count, listing tolerance and
measured diameter have not yet been recorded. The owner inserted one pin through
both installed 6800-2RS bearings and the provisional ABS distal/shin link until
it was fully seated.

- The pin is **snug in the bearings**, but the owner determined that the bearing
  fit was not what trapped the assembly. A separate one-bearing-at-a-time
  thumb-pressure/removal test has not yet been reported.
- The pin was **seized in the provisional shin's nominal Ø10 printed bore** and
  could not be withdrawn by hand.
- The owner recovered the metal pin by breaking the provisional printed shin
  pieces. The provisional shin is therefore destroyed and cannot be reused.
- No photograph, pin measurement, extraction-force measurement or post-removal
  bearing inspection was supplied with this report.

Classification:

- **Nominal Ø10, 19 mm-deep provisional ABS shin bore: FAIL — excessive
  interference.** Do not repeat it in another full link.
- **Pin through the two installed bearings: INCOMPLETE.** “Snug” is not yet the
  required separate hand-fit/removal result, and the bought pin's h6 claim
  remains unverified.

## Initial ladder result — 2026-09-16

The owner printed the initial ABS ladder and selected the largest, unmarked-end
station: nominal **Ø10.25**. The received pin passes through its full 19.0 mm
station using firm thumb pressure. That is the intended feel for the
shin-to-pin angular reference: deliberate hand force, with no hammer or clamp,
and no free slip reported.

**Result: OWNER SELECTED 19.0 MM CANDIDATE — nominal Ø10.25.** Fusion inspection
then found that the production receiver actually spans 21.6 mm because it
includes the two 1.3 mm thrust lands. The initial ladder therefore did not
reproduce the whole press length. It establishes Ø10.25 as the lower end of a
corrected full-span ladder, not as a final production release.

No separate spin, rock, withdrawal, printed-diameter or pin-diameter result was
supplied. This is ABS process evidence and does not change the nominal Ø10 pin
or bearing envelope. Repeat the coupon for PA-CF. See
[`result.json`](result.json) for the machine-readable report and
[`source_candidate_fusion_verification.json`](source_candidate_fusion_verification.json)
for the transient source-build check.

## Disposition

1. Inspect the recovered pin for an end burr or scoring. Do not abrade its
   ground journal to tune the fit.
2. Test that pin, and then the other received candidates, through each loose or
   independently accessible 6800 bearing with no printed link present. Record
   whether controlled thumb pressure inserts and removes each pin.
3. Print the corrected [21.6 mm full-span ladder](../../../first_article_stl/knee_pin_fit/),
   which now starts at Ø10.25 and continues to Ø10.45 in 0.05 mm steps. Select
   the smallest removable light press.
4. Keep the final `Distal_Link_L`, pin retention and encoder coupling on hold
   until the full-span bore is selected and the print, insertion and service
   paths are verified in Fusion.

The earlier supported mock-up result remains valid evidence for the loose Ø9.7
printed alignment-pin assembly only. It does not transfer to the real steel pin.

The exact printed 19.0 mm artifact and its Fusion/mesh records are preserved in
this directory as `ABS_CAL_KNEE_PIN_BORE_LADDER_19MM_PRINTED.stl`,
`initial_19mm_fusion_manifest.json` and
`initial_19mm_mesh_verification.json`.
