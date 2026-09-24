# Assembly manual sources and reproduction

The [bench guide](../ordered_pin_picture_guide.md) and
[printable PDF](../../../output/pdf/beni_single_leg_assembly_manual.pdf) contain
23 pages: a cover, printed-parts key and 21 illustrated operations.

## Drawing provenance

The 29 images in `views/` were captured from the corrected live `Beni_SingleLegRig` v30
through the Fusion MCP using `assembly_manual_fusion.py`. Only reversible
occurrence transforms, visibility and camera settings were used. The manifest
records projected part positions, insertion arrows and insert receivers;
restoration checks passed for transforms, visibility, occurrence/timeline counts
and motor guards. The September 23 images follow the verified PINREV2 correction; capture
itself changes no manufacturing geometry. The source version is in the manifest.
Exploded distances are illustration spacing, not engineering dimensions.

The parts key reuses the released native Fusion print-orientation images. The
four ordered-pin images were recaptured on September 23 from a fixed iso
camera; the exporter had inherited a near edge-on view from the manual capture.
The orange spring is a schematic between the CAD spring seats, not a drawing
of the purchased spring's coils. Cotters are described but not modelled; use
the supplied retainers. Drawings do not establish physical assembly acceptance.

The sequence and engineering values follow the
[ordered-pin traveller](../../../first_article_stl/ordered_pin_integration/README.md),
[spring-mechanical release](../../../evidence/assembly/2026-09-17_abs_spring_mechanical_test/README.md),
[ordered-pin release](../../../evidence/assembly/2026-09-21_ordered_pin_integration/README.md)
and [actual-pin selection](../../../evidence/assembly/2026-09-22_ordered_pin_fit_ladders/README.md).

## Reproduction and checks

Run `assembly_manual_fusion.py` only through Fusion MCP with the active corrected
single-leg rig. Its `run('')` captures all views; a comma-separated frame list
selects particular views. The model state is restored in `finally`.

Then, from the repository root with ReportLab and Poppler available:

```sh
python3 docs/assembly/manual/build_manual.py
pdftoppm -r 110 -png output/pdf/beni_single_leg_assembly_manual.pdf docs/assembly/manual/pages/step
```

Without Poppler, render the same 110 dpi pages with PyMuPDF
(`page.get_pixmap(dpi=110)`, saved as `pages/step-NN.png`). The September 23
gallery was rendered this way; it draws the PDF's Helvetica-Bold headings as
bold, where the earlier Poppler render substituted a regular face.

All 23 rendered pages were visually reviewed for clipping, readable labels,
arrows and assembly orientation. `pages/` is the published image gallery,
not temporary QA output. Physical bearing/pin checks, cotter retention, stop
behavior and the hand-contained sweep remain owner assembly gates.
