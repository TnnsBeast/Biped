# General-gauge M3 station — owner FAIL, 2026-09-14

The owner printed `print_stl/GAUGE_Fit_Coupon.stl` in ABS and reported that the
two smallest holes appeared relevant, but both were too small. The gauge map
shows those as Ø4.05 for the shoulder-output dowel and Ø4.0 for the M3 heat-set
insert. The owner then clarified that the heat-set insert pocket needs to be
wider.

**Result: OWNER FAIL — nominal Ø4.0 is too small for the intended M3 heat-set
insert.** This result applies to the owner's current ABS printer/profile and
the insert intended for the active single-leg article. The exact seller variant
remains unrecorded. No photograph or measured printed diameter was supplied.

The general gauge is not a diameter ladder: it contains only the one Ø4.0 M3
candidate. The dedicated Fusion-generated replacement tests nominal
Ø4.1/4.2/4.3/4.4/4.5 blind pockets at the Mode A stand's 6.0 mm receiver depth:
[`first_article_stl/insert_fit/`](../../../first_article_stl/insert_fit/).

This failure supersedes every affected Ø4.0 print. The later ladder result
selected Ø4.5; Fusion has promoted that diameter and released replacement
stand, shoulder-plate and proximal-link exports. Do not install inserts in the
prior printed Ø4.0 receiver parts.

Machine-readable observation: [`result.json`](result.json).

**Later the same day:** the dedicated ladder selected nominal Ø4.5. See the
[M3 coupon selection](../2026-09-14_m3_coupon_pass/).
