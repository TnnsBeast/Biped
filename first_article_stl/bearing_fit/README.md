# ABS 6800 bearing-bore calibration

**OWNER UPDATE, 2026-09-02:** Ø19.10 passed and the full-depth face-flat link is
usable, but the owner found it slightly tighter than preferred. Ø19.15, the
third bore from the two-hole index end, retains the bearing with no perceptible
movement at easier thumb pressure and is now the preferred compensation for any
future ABS proximal link. Ø19.00 previously failed as too tight. The real
bearing remains Ø19.00; both larger values are ABS process observations, not a
hardware-model change. Full-depth result:
[`../../evidence/knee_fit/2026-09-02_proximal_link_full_depth/`](../../evidence/knee_fit/2026-09-02_proximal_link_full_depth/).

Print [`ABS_CAL_6800_BORE_LADDER.stl`](ABS_CAL_6800_BORE_LADDER.stl) flat in
the same ABS material and slicer profile intended for the first structural
links. Do not apply a slicer hole-compensation experiment to this file: the CAD
already contains five different trial diameters.

The two small Ø3 index holes identify the Ø19.05 end:

```text
index holes →   Ø19.05   Ø19.10   Ø19.15   Ø19.20   Ø19.25
   •  •            ○        ○        ○        ○        ○
```

Use one real 6800-2RS bearing and test from Ø19.05 toward Ø19.25:

1. Remove only brim/elephant-foot material. Do not sand, drill, ream, heat or
   clamp a trial bore.
2. Keep the bearing square and press with both thumbs over the **outer race**.
3. Stop at the first bore where the bearing enters with firm thumb pressure,
   stays square, and has no perceptible radial rock.
4. Because the coupon is 4 mm thick and the bearing is 5 mm wide, grip the
   exposed edge and pull it back out before trying the next bore.
5. Report the selected nominal diameter and whether insertion was light, firm,
   or still required a tool.

This ladder is diagnostic only. At the owner's direction, the actual unloaded
ABS proximal first article is the full-depth confirmation and physical assembly
rehearsal; an additional depth coupon is not required. PA-CF remains unreleased.

`fusion_manifest.json` is the Fusion-generated dimensional/export record.
