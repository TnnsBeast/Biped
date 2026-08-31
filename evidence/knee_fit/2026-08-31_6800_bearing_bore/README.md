# 6800-2RS bearing bore — first ABS result

Date: 2026-08-31
Source: owner physical test report in the project task

## Result

The real 6800-2RS bearing does not enter the nominal Ø19.00 bore in the printed
`GAUGE_Fit_Coupon` with thumb pressure. Pushing the coupon against a table can
start the bearing partway; a clamp would probably force it fully in.

Classification: **FAIL — too tight.** The target is a controlled light press,
not a forced interference fit that stores stress in the ABS. The bearing should
not be clamped into this coupon.

## Disposition

- The structural Ø19.00 bearing-seat value remains frozen pending calibration.
- Fusion generated and B-Rep-verified an indexed Ø19.05–Ø19.25 ladder in 0.05 mm
  steps: [`../../../first_article_stl/bearing_fit/ABS_CAL_6800_BORE_LADDER.stl`](../../../first_article_stl/bearing_fit/ABS_CAL_6800_BORE_LADDER.stl).
- The smallest successful ladder bore will be confirmed in a full-depth
  assembly-sim coupon before the proximal link is released.
- No photo was supplied for this observation; the record is the owner's verbal
  fit report.
