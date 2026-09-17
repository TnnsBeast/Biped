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

**Coupon result: OWNER SELECTED 19.0 MM CANDIDATE — nominal Ø10.25.** The first
Fusion inspection assumed that the integrated printed receiver would copy the
deleted steel sleeve's 21.6 mm span. The owner therefore made the production
selection conservatively relative to the 19.0 mm coupon.

## Production selection — 2026-09-16

The owner judged that the initially assumed extra 2.6 mm of receiver length
would not materially change the fit and directed the production ABS bore to
**Ø10.30**, one 0.05 mm step above the firm-thumb Ø10.25 coupon result. This
closes the ABS bore-size gate by owner engineering choice without another
coupon print.

The subsequent Fusion service-path audit found that a 21.6 mm printed receiver
extends 0.8 mm into each bearing pocket and cannot be inserted into or removed
from the assembled fork. The released v26 design retains the conservative
Ø10.30 bore but confines it to the clear 20.0 mm fork gap. Fusion printability,
support-removal, link/pin insertion and mesh checks pass. See the
[release evidence](../2026-09-16_distal_d10p30_release/).

The first printed link must still confirm firm thumb insertion and hand removal
with no free spin or rock, plus acceptable axial play, before spring-loaded or
powered use. Pin retention and encoder coupling remain held, and the ABS result
does not transfer to PA-CF.

No separate spin, rock, withdrawal, printed-diameter or pin-diameter result was
supplied. This is ABS process evidence and does not change the nominal Ø10 pin
or bearing envelope. Repeat the coupon for PA-CF. See
[`result.json`](result.json) for the machine-readable report and the source
verification record in
[`source_selection_fusion_verification.json`](source_selection_fusion_verification.json)
for the saved Fusion build check.

## Disposition

1. Inspect the recovered pin for an end burr or scoring. Do not abrade its
   ground journal to tune the fit.
2. Test that pin, and then the other received candidates, through each loose or
   independently accessible 6800 bearing with no printed link present. Record
   whether controlled thumb pressure inserts and removes each pin.
3. Use nominal Ø10.30 for the active 20.0 mm ABS distal-link receiver. The
   [21.6 mm full-span ladder](../../../first_article_stl/knee_pin_fit/) remains
   available as a conservative diagnostic if the first link is unexpectedly tight.
4. Print the [released distal fit article](../../../first_article_stl/assembly_dry_fit/ABS_FA_Distal_Link_L_D10p30_STEEL_PIN_FIT_PRINT_ORIENTED.stl)
   and record insertion, withdrawal, spin, rock and axial play. Pin retention
   and encoder coupling remain held.

The earlier supported mock-up result remains valid evidence for the loose Ø9.7
printed alignment-pin assembly only. It does not transfer to the real steel pin.

The exact printed 19.0 mm artifact and its Fusion/mesh records are preserved in
this directory as `ABS_CAL_KNEE_PIN_BORE_LADDER_19MM_PRINTED.stl`,
`initial_19mm_fusion_manifest.json` and
`initial_19mm_mesh_verification.json`.
