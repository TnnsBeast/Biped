# R2A single-leg article — ordering guide

Status: **purchasing requirements for the first R2A ABS article, 2026-09-27.**
Nothing here has been ordered. Vendor websites were not reachable from the
design session (proxy 403), so **no vendor part number, price, stock or rating
below has been checked**: each BUY line gives the engineering requirement, the
part type and search terms, and leaves price and link as **TO CONFIRM**. Check
every candidate's drawing against the requirement before ordering; a close
catalogue part is not a substitute unless it meets every line.

Sources for the requirements: the Fusion model `Beni_R2A_SingleLeg`
([digital-gate evidence](../evidence/r2a/2026-09-27_digital_gate/)),
[`r2a_calc.py`](../r2a_calc.py) (loads) and the
[R2A plan](../docs/design/active_knee_revision2_plan.md). Owned stock comes
from the [Mode A workbook](mode_a_procurement_bom_2026-08-21.xlsx), the
[electronics BOM](../electronics/07_bom.md) Wave 0 and the dated
[`evidence/`](../evidence/) records.

Status labels: **BUY** — not owned; **OWNED** — recorded as received;
**OWNED — VERIFY** — recorded as owned or ordered, but the count, receipt or
exact variant is not recorded in the repository.

## 1. Buy list (what to order)

| # | Item | Qty (incl. spares) | Requirement | Search terms | Price / link |
|---:|---|---:|---|---|---|
| 1 | **Steadywin GIM6010-8 actuator** | **1** | Same model and driver variant as the owned shoulder unit (integrated driver, CAN, ODrive-CANSimple firmware, 8:1). Housing 8 × M3 on Ø74, output 6 × M3 on Ø25 + 3 × Ø4 pins: the Fusion knee actuator is the same STEP. Include its power/CAN lead set. | "Steadywin GIM6010-8", "GIM6010-8 CAN" | TO CONFIRM |
| 2 | **M5 female rod end (spherical)** | **4** (2 + 2 spares) | Bore Ø5 for a Ø5 pin; female M5 × 0.8 thread ≥ 10 mm deep; **static radial rating ≥ 1521 N** (2 × the 761 N design rod force, `r2a_calc.py` §5); must fit the modelled envelope: eye OD ≤ 18.0, housing width ≤ 6.0, inner-ring (ball) width 7.6–8.0 (the clevis gap is 8.4), neck ≤ Ø9.0, pin centre to shank end ≤ 27.0 mm. Right-hand thread on both unless item 3 is a LH/RH rod. | "M5 female rod end", "SI5 T/K rod end", "PHS5 rod end", "rod end DIN ISO 12240-4 d=5 female" | TO CONFIRM |
| 3 | **M5 threaded rod, steel** | 1 length ≥ 100 mm | Plain steel or A2 stainless, M5 × 0.8. Cut to **86.0 mm** with a hacksaw (MANUFACTURING_CONSTRAINTS allows cutting bought stock). A true LH/RH turnbuckle rod is optional; with plain RH rod the length is set in 0.4 mm half-turn steps. | "M5 threaded rod 304", "M5 x 0.8 studding" | TO CONFIRM |
| 4 | **M5 thin jam nut** | 4 (2 + 2 spares) | ISO 4035 / DIN 439, 8 mm across flats, ≤ 2.7 mm thick (the Fusion nut envelope). | "ISO 4035 M5", "M5 thin jam nut" | TO CONFIRM |
| 5 | **Ø5 × 18 mm dowel pin, hardened** | 4 (2 + 2 spares) | Ø5.000 nominal, h6 or m6, 18 mm long, chamfered ends (ISO 8734 / DIN 6325 class). One each for the crank and lever clevises. Select the printed hole on the pin ladder coupon first. | "5 x 18 dowel pin hardened", "ISO 8734 5x18" | TO CONFIRM |
| 6 | 6800-2RS bearing | 2 (recommended) | 10 × 19 × 5 mm, sealed. The owned pair is pressed into the retired legacy proximal link; buy a fresh pair rather than pushing those out past their Ø17 retaining lips. | "6800-2RS" | TO CONFIRM |
| 7 | Adafruit CAN Pal, PID 5708 | 1 (recommended) | Not needed for the single-leg gates: both GIM6010-8 share bus A at the default 500 kbit/s and the traveller's 100 Hz command rate loads it to 10.8 % worst (`r2a_calc.py` §9). A 1 kHz loop on one bus needs 1 Mbit/s (54.0 % worst; 108.0 % at 500 kbit/s, §6); the third transceiver keeps the fallback of one GIM6010-8 per bus if 1 Mbit/s is unreliable on the breadboard ([electronics/02](../electronics/02_harness_and_routing.md#8-r2a-single-leg-rig)). | "Adafruit 5708 CAN Pal" | TO CONFIRM |
| 8 | WAGO 221-415 (5-conductor) lever connector | 2 (only if needed) | The owned 2 × 221-413 (3-way) serve PSU + 2 actuators per rail; three actuators need 4 conductors per rail. | "WAGO 221-415" | TO CONFIRM |
| 9 | DIN 988 M5 shim washers 5 × 10 × 0.2 / 0.5 | 10 each (only if needed) | Only if the chosen rod end's inner ring is narrower than 7.6 mm: shim to 8.0 mm. | "DIN 988 5x10x0.2" | TO CONFIRM |
| 10 | M2.5 × 10 socket-head cap screw, ISO 4762 | 6 + spares (buy if not in stock) | Wheel motor to the distal wheel end. Replaces the legacy M2.5 × 12, which through the 8.0 mm plate reaches 1.0 mm past the floor of the motor's Ø2.0 × 3.0 holes in the STEP; × 10 engages 2.0 mm and stops 1.0 mm short ([engagement record](../evidence/r2a/2026-09-27_digital_gate/README.md)). | "M2.5 x 10 socket head cap screw" | TO CONFIRM |

**Do not order** any spring, cartridge or legacy stop hardware: R2A retires them.

## 2. Owned stock that the R2A article uses

| Item | Qty needed | Status | Evidence / note |
|---|---:|---|---|
| GIM6010-8 (shoulder) | 1 | OWNED | [delivered actuators](../evidence/actuators/2026-08-20_received/) |
| GIM4305-10 (wheel) | 1 | OWNED | same |
| Ø10 × 35 hardened knee pin | 1 | OWNED | [pin result](../evidence/knee_fit/2026-09-15_steel_pin_provisional_shin/); one pin is in the legacy article |
| Ø4 × 10 stainless dowels | 3 root (existing) + **5 new** (2 crank cap, 2 lever cap, 1 encoder arm) | OWNED | 60 received ([order record](../evidence/assembly/2026-09-22_owner_printed_parts_and_pins/)); press fit selected at Ø4.25 on the root ladder |
| M4 × 10 SHCS | 6 | OWNED | legacy hub joint, reused unchanged |
| M3 × 12 SHCS | 6 (perimeter) + spares | OWNED — VERIFY | "assorted metric fasteners in hand" (PROJECT_STATUS 2026-09-20); counts not inventoried |
| M3 × 10 SHCS | 13 (5 knee-actuator housing, 6 crank output, 2 encoder arm) | OWNED — VERIFY | same. The housing screws must be × 10, not × 12: a 5 mm protrusion bottoms in the ~4.0 mm housing thread |
| M3 × 16 SHCS | 2 (encoder bracket) | OWNED — VERIFY | same |
| M3 × 6 SHCS | 2 (knee-pin cap) | OWNED — VERIFY | same |
| M3 × 8 and M4 × 8 SHCS | 3 (wheel hub to wheel output) and 6 (no-tyre shell to wheel hub) | OWNED | legacy wheel module, reused unchanged |
| Voron-style M3 × 5 heat-set inserts (Ø4.5 receiver) | **12** new (6 perimeter, 2 bracket, 2 pin cap, 2 encoder arm) + spares | OWNED — VERIFY | [Ø4.5 selection](../evidence/inserts/2026-09-14_m3_coupon_pass/); count not recorded |
| Kadriick M4 × 8 inserts | 6 (already in the printed hub) | OWNED | hub unchanged |
| Shoulder hub, shoulder plate, cable cover, RIG_Stand, cable post A | 1 each | OWNED (printed) | reused unchanged |
| Wheel hub, no-tyre wheel shell | 1 each | OWNED (printed) | wheel-clear tests only |
| AS5048A adapter kit with AS5000-MD6H-2 diametric magnet, 1 × 8 header | 1 | OWNED — VERIFY | ordered 2026-08-31; receipt not recorded |
| Teensy 4.1 | 1 | OWNED | electronics/07 Wave 0 |
| Adafruit CAN Pal 5708 | 2 | OWNED — VERIFY | ordered 2026-08-31; receipt not recorded |
| WAGO 221-413 | 2 | OWNED — VERIFY | ordered 2026-08-31 |
| Current-limited bench PSU (0–30 V / 5 A) | 1 | OWNED — VERIFY | workbook lists it as "order now" |
| 16–18 AWG stranded wire, CAN twisted pair, 2.5 mm zip ties | as needed | OWNED — VERIFY | workbook "now if missing" |
| ABS filament | ~0.4 kg | OWNED | active article material |
| TPU 95A filament | ~2 g (4 plugs) | OWNED — VERIFY | tyre material in the workbook |

## 3. Why these sizes

- **Rod ends.** Spherical rod ends at both ends make the pushrod a two-force
  member, so the printed crank and lever see no bending from misalignment. The
  1521 N floor is twice the 761 N design rod force (1.5 × 11 N·m stall through
  the linkage at its worst pose). The modelled envelope is what the Fusion
  sweep cleared: a larger eye or a wider neck has not been checked.
- **Plain Ø5 dowels instead of shoulder screws.** The concept listed Ø5
  shoulder screws with nuts, but a head plus a nut does not fit in the 20 mm
  channel between the proximal cheeks. The pins float between the cheek faces
  instead (≥ 2.7 mm engagement in every ear at either end of their float), so
  they need no head, nut or clip and cannot leave the joint while the link is
  assembled. Service is by removing the knee module (crank pin) or the knee pin
  and distal link (lever pin).
- **M5 rod, 86.0 mm.** 120.0 mm pin to pin minus two 27.0 mm rod-end ends plus
  10.0 mm of thread engagement at each end (`r2a_lib.ROD_LEN`). Euler load of
  the M5 rod at 120 mm: 1965 N against 761 N in compression (`r2a_calc.py`).
- **Screws.** Every screw length is the modelled one; grip, engagement and
  tip-to-floor clearance for every set are in the
  [digital-gate record](../evidence/r2a/2026-09-27_digital_gate/README.md).

## 4. Before ordering

1. Confirm the GIM6010-8 variant against the owned unit's label and driver
   (photos in the actuator evidence). The owned unit's protocol and CAN node-ID
   procedure are in [electronics/03](../electronics/03_compute_and_can.md).
2. For the rod end, get the vendor drawing and check every envelope line in
   item 2; record the chosen part and its drawing link in this file.
3. Record price, supplier and lead time here, then place the order yourself.
