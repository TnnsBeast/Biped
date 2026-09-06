# Spring recommendation and CAD mismatch — 2026-09-05

**Corrected by the owner, 2026-09-06:** the received spring is **50 mm (5 cm)**,
matching the order. The earlier 150 mm / 15 cm report was a typo. There is no
wrong-length delivery or replacement-order hold. [Owner correction](owner_correction.json).

The owner challenged the claim that the purchased spring should have been the
55 mm baseline. Reviewing the earlier conversation confirmed a recommendation
for a different, off-the-shelf candidate. The project records had failed to
preserve that decision and its unfinished CAD work.

## What was recommended

In the task **Assess and refactor project**
(`01a02251-b515-7b42-8599-5f65a8d85cb7`), the assistant initially added yellow
OD18 / ID9 springs in 40, 45 and 50 mm lengths to the AliExpress cart. The later
answer (`item-302`) explicitly recommended keeping only **Yellow / 50 mm /
OD18 mm / ID9 mm**, quantity three. It also stated that the existing Ø13.4
cartridge-eye spigots would need redesign before spring-loaded parts were made.

The candidate listing was
[AliExpress item 3256809413333634](https://www.aliexpress.us/item/3256809413333634.html).
Earlier answers disagreed about its inferred rate: the seller-chart estimate
and comparable branded spring data were not equivalent evidence. None is an
actual measurement or certification of the owner's spring. The final confident
recommendation overstated what was verified.

## What is established now

- The original CAD/BOM baseline is Ø19 OD, Ø2.6 wire, **55 mm free length**.
  Its cartridge dimensions and force table remain baseline calculations,
  not validation of the purchased AliExpress candidate.
- The owner-provided completed-order screenshot on September 5 confirms
  **Yellow, 50 mm, OD18 mm / ID9 mm**, quantity one, from Creamily Official Store.
  It matches the recommended variant. The account/order screenshot is not
  copied into this public repository.
- The owner confirms the received spring is **50 mm free length**. The earlier
  longer-length report is corrected; no ruler photograph or supplier dispute
  is required to resolve it. The owned part matches the recommended order option.
- Live Fusion inspection found **Ø13.4 spigots**, an **Ø10 washer stack** and
  **Ø13 TPU bumper**. Those have not been adapted to the candidate's stated
  ID9. The earlier suggestion to keep the internal hard stop while changing
  only the spigots/spacer was incomplete.
- The 50 mm alternative needs a verified cartridge package: seats/spigots,
  installed length/preload, compressed-length margin, guide and internal hard
  stop/bumper clearance. No such change is released. This does not establish a
  need to redesign the whole leg, or justify choosing new dimensions by guess.
- Keep the owned 50 mm spring; no replacement is required because of length.
  Do not order another spring solely from the old 55 mm headline. The baseline
  CAD remaining unadapted is an assistant workflow error, not an owner selection error.

See [fusion_geometry.json](fusion_geometry.json) for the live inspection.

## Current work

The corrected proximal link is printing. The
[2026-09-06 supported knee mock-up](../../../first_article_stl/knee_mockup/)
now provides a provisional distal link and temporary alignment pin for two
supported links, with the spring cartridge absent. Two optional detached
Ø8-pilot seat caps check the owned spring's ends on the bench, uncompressed.
They are fit coupons, not revised cartridge eyes or preload spacers. Actual
cartridge adaptation remains unfinished. No main-spring preload or powered/
load-bearing use of a printed knee pin is released.
