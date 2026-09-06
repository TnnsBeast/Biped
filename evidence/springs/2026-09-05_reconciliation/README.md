# Spring recommendation and CAD mismatch — 2026-09-05

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
- The owner reports **150 mm free length** and reconfirmed that on September 5.
  That conflicts with the confirmed 50 mm order option. A photograph of the
  actual spring beside a ruler is still needed to distinguish a measurement
  misunderstanding from a wrong-length delivery. Do not infer seller error
  from the order screenshot alone; do not describe this as wrong variant selection.
- Live Fusion inspection found **Ø13.4 spigots**, an **Ø10 washer stack** and
  **Ø13 TPU bumper**. Those have not been adapted to the candidate's stated
  ID9. The earlier suggestion to keep the internal hard stop while changing
  only the spigots/spacer was incomplete.
- The 50 mm alternative needs a verified cartridge package: seats/spigots,
  installed length/preload, compressed-length margin, guide and internal hard
  stop/bumper clearance. No such change is released. This does not establish a
  need to redesign the whole leg, or justify choosing new dimensions by guess.
- A 150 mm spring is not accepted for this cartridge. Do not cut it or force it
  into the assembly. The selected order option is now confirmed; verify the
  physical spring next and resolve any wrong-length delivery before adapting it.
  Do not order another spring solely from the old 55 mm headline. The baseline
  CAD remaining unadapted is an assistant workflow error, not an owner selection error.

See [fusion_geometry.json](fusion_geometry.json) for the live inspection.

## Current work

The owner reports the corrected proximal link is printing. A springless,
supported mock-up with a temporary printed alignment pin is requested, but its
distal link, cartridge eyes and temporary pin have **not been released**.
The owner paused that work to reconcile the spring recommendation. Inspection
candidates are not print files. ABS restrictions remain unchanged: no main
spring preload and no powered or load-bearing use of a printed knee pin.
