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

The owner then tested the indexed Ø19.05–Ø19.25 ABS ladder. The second bore from
the two-hole Ø19.05 index end is Ø19.10. The owner confirmed all four criteria:

- the bearing entered squarely with firm thumb pressure;
- no table or clamp was required;
- there was no noticeable side-to-side rock; and
- the bearing was removable using its exposed edge.

Classification: **Ø19.10 ABS PASS.**

## Disposition

- The real 6800-2RS hardware envelope remains Ø19.00; the selected printed ABS
  seat is Ø19.10. This is process compensation, not a hardware-model change.
- Fusion generated and B-Rep-verified an indexed Ø19.05–Ø19.25 ladder in 0.05 mm
  steps: [`../../../first_article_stl/bearing_fit/ABS_CAL_6800_BORE_LADDER.stl`](../../../first_article_stl/bearing_fit/ABS_CAL_6800_BORE_LADDER.stl).
- At the owner's direction, the actual unloaded ABS proximal-link first article
  replaces a separate depth coupon. Its two bearing insertions are the physical
  assembly rehearsal. PA-CF still requires its own material-specific coupon.
- No photo was supplied for this observation; the record is the owner's verbal
  fit report.
