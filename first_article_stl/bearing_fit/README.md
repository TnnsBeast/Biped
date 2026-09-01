# ABS 6800 bearing-bore calibration

**OWNER PASS, 2026-08-31:** Ø19.10 was the smallest/best bore satisfying every
release criterion: firm thumb pressure, square seating, no perceptible radial
rock and removal using the exposed bearing edge. Ø19.00 previously failed as
too tight. The real bearing remains Ø19.00; Ø19.10 is ABS print compensation.

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
