# Beni Prototype 1 — fit coupons and first articles

> ### ⚠ Superseded in places by the single-leg rig build
>
> **3D printed and off-the-shelf parts only, no laser cutting or machining** —
> see [`../MANUFACTURING_CONSTRAINTS.md`](../MANUFACTURING_CONSTRAINTS.md).
>
> - **`Distal_Link_L.stl` is superseded** by
>   [`../rig_stl/reroute/Distal_Link_L.stl`](../rig_stl/reroute/Distal_Link_L.stl).
>   The steel knee sleeve is deleted and its Ø16 bore is now printed into the link
>   as Ø10. **That rig file is currently on DFM hold** pending the real Ø10 h6
>   knee-pin gate and a post-tangent-fix bed-ready Fusion re-export; do not print
>   either legacy distal file yet.
> - **`check_prints/` is obsolete** — it existed to dry-fit before ordering
>   machining. Use [`../rig_stl/reroute/`](../rig_stl/reroute/) instead.
> - The **`GAUGE_*` coupons below are still exactly right** and were re-measured
>   against the design record feature by feature. Note that the shoulder coupon is
>   only **9.5 mm long** and therefore cannot report the delivered motor's exact
>   overall length. The STEP model supplies the 44.0000 mm nominal dimension;
>   use the real motor and ABS mating article as a functional go/no-go.
>
> Everything else on this page stands. What to print for the rig:
> [`../rig_stl/README.md`](../rig_stl/README.md).


Everything here is exported straight from the verified Fusion assembly
(`Beni_Prototype1`) at High mesh refinement. All STLs are in millimetres and sit
at their assembly coordinates, not centred on the origin — every slicer will
drop them to the bed and centre them for you.

Chiral parts are exported **left-hand only**. Mirror in the slicer for the
right-hand part; there is no separate `_R` file.

> **Revision 2 — 2026-08-08.** Re-exported from the corrected model. The links
> and side panels now carry fillets at every load-bearing re-entrant corner, the
> rim has a tyre bead groove and an inboard retaining flange, and the tyre has a
> crowned tread. Two screw lengths changed — see the hardware list at the bottom.
> Details in [`../beni_prototype1_rev2_changes.md`](../beni_prototype1_rev2_changes.md).

---

## Print in this order

### 1. `GAUGE_Fit_Coupon.stl` — print this first, before anything else
14 cm³, ~25 min. Print the first one in ABS for the ABS first-article campaign,
then repeat it in PA-CF before releasing structural PA-CF parts.

A 26 × 92 × 8 bar with six through-bores, one for every critical fit in the
robot:

| bore | what it is | target fit |
|---:|---|---|
| Ø19.0 | 6800 bearing seat, proximal arms | light press — bearing enters with thumb pressure, no rock |
| Ø16.0 | **was** the steel knee sleeve's seat in the distal boss — **that bore is now Ø10**, printed straight into `Distal_Link_L`, because `Knee_Sleeve_L` is deleted. Measure it as a general large-bore check only | light press |
| Ø10.0 | knee axle bore — the fit that now matters, on a bought Ø10 h6 × 35 mm dowel pin | light press, not a loose slip — this press is the rig's angular reference |
| Ø6.0 | knee-stop dowel seat | light press |
| Ø4.05 | shoulder-output dowel | slip |
| Ø4.0 | M3 heat-set insert bore | insert seats flush without splitting the wall |

With no calipers, test the bores using the real matching bearings, dowels,
fasteners, and inserts. Record which nominal feature produces the required fit
and use that to set the ABS profile's **hole / X-Y size compensation**. The
result is specific to the material, printer, orientation, and profile; do not
reuse ABS compensation for PA-CF.

For the active Mode A first article, the immediate go/no-go checks are Ø19 with
the real 6800-2RS bearing and Ø10 with the real h6 knee pin. The Ø16 bore is a
superseded sleeve check; Ø6 and Ø4.0 support later stop/insert work; and the
Ø4.05 shoulder-output result has already been superseded for this ABS profile
by the owner-tested Ø4.15 hub.

**Physical result, 2026-08-31:** the real 6800-2RS bearing does not enter the
nominal Ø19.00 bore with thumb pressure. It starts only under table/clamp force,
so this is a **FAIL**, not permission to clamp it home. The owner then printed the indexed
[`ABS_CAL_6800_BORE_LADDER.stl`](../first_article_stl/bearing_fit/ABS_CAL_6800_BORE_LADDER.stl)
whose two small holes mark the Ø19.05 end; the five main bores are Ø19.05,
Ø19.10, Ø19.15, Ø19.20 and Ø19.25 moving away from those markers. Test from
smallest to largest. **Ø19.10 PASSed**: firm thumb pressure, square seating, no
perceptible rock and removal by the exposed edge. The actual unloaded ABS
proximal first article with Ø19.10 seats is now the full-depth confirmation and
physical rehearsal; no extra coupon is required. This does not release the
PA-CF part, whose critical fit must be recalibrated in PA-CF.

**This one print de-risks every other print.** Don't skip it — the Ø19 bearing
seats and the Ø10 knee-axle bore are the two fits that will otherwise waste a
whole link.

### 2. The two positive motor stand-ins
These reproduce the motor envelopes for checking mating CAD when no motor is
available. They are not negative sockets and cannot be test-fitted onto the
delivered motors. Now that the motors are in hand, they are optional: design a
small negative ABS mating coupon in Fusion, or print the actual mating part in
ABS, for the physical go/no-go.

- **`GAUGE_Shoulder_Motor_Interface.stl`** (31 cm³, Ø78 × 10)
  Replicates the GIM6010-8's mating geometry exactly as measured from the STEP:
  the Ø78 front face, **8 × Ø2.5 pilots on the Ø74 PCD** (tap M3), the Ø46 rotor
  step, the Ø34 pilot boss, the output face 3.5 mm proud with **6 × Ø2.5 pilots
  on the Ø25 PCD** and **3 × Ø4.05 dowel holes on the Ø20.4 PCD**.
  Press three Ø4 × 8 steel dowels into those holes and you have a working
  stand-in for the motor's anti-rotation pins.

- **`GAUGE_Wheel_Motor_Interface.stl`** (31 cm³, Ø53 × 33)
  Replicates the GIM4305-10: the full Ø53 × 33 envelope, **6 × Ø2.0 pilots on
  the Ø47.5 PCD** (tap M2.5), the Ø40.4 driver-cover boss, the bearing gland,
  and the output flange Ø37 at the far end with **3 × Ø2.5 on the Ø27 PCD**.
  Note it is the *full length* on purpose — use it to confirm the wheel drum
  clears the motor and that the driver cover nests in the distal plate's Ø41.5
  pocket.

### 3. `check_prints/` — obsolete
Its premise was "print these in PLA before ordering any machining." **There is no
machining.** Print the real printed parts instead:
[`../rig_stl/reroute/`](../rig_stl/reroute/).

### 4. Structural PA-CF parts — only after step 1
Print one of each first and dry-fit before committing to the second set.
The four files are `Chassis_Shoulder_Plate_L.stl`, `Distal_Link_L.stl`
(**use `../rig_stl/reroute/Distal_Link_L.stl` instead** — see the banner),
`Proximal_Link_L.stl` and `Chassis_Frame.stl`. **Orientations, footprints and the
rationale for each are in the BOM `§1`** —
[`../beni_prototype1_bom_and_assembly.md`](../beni_prototype1_bom_and_assembly.md).
Don't re-derive them here.

"On edge" matters for the links: it puts primary bending loads in the print
plane and makes the 20 mm spring channel a through-slot, so nothing needs
internal support. Every part in this design is single-shell — there are no
enclosed cavities anywhere, so no print should ever need trapped support.

Print the structural parts at **high infill** (≥ 60 %, 4+ walls). The mass
figures in the BOM assume the modelled section is actually realised; a
lightly-infilled 5 mm knee arm is not the part that was analysed.

### 5. Wheel and covers — last, nothing depends on them
| file | material | note |
|---|---|---|
| `Wheel_Rim_L.stl` | PA-CF | web face down, drum prints up |
| `Wheel_Tyre_L.stl` | TPU 95A | Ø110 × 30; stretches onto the Ø96 rim seat |
| `Shoulder_Cable_Cover_L.stl` | ABS | 4 × M3 heat-set inserts |
| `Knee_Encoder_Bracket_L.stl` | ABS | 2 × M3 heat-set inserts |
| `Electronics_Tray.stl` | ABS | flat panel |

---

## What the first-article campaign validates

- Every bore fit and the slicer compensation (step 1).
- Both motor bolt patterns and the output-side dowel/screw patterns (step 2).
- The spring cartridge in the 20 mm channel, both pivot pins, and that removing
  one clevis pin frees the spring.
- Driver access to all 32 audited screws.
- That the wheel drum clears the wheel motor and the distal plate.

## What you cannot validate yet

- Actual spring rate and preload — needs the real spring on a press.
- Anything load-bearing. PLA stand-ins prove geometry, not strength.
- Motor bolt-thread engagement depth, and the exact GIM6010-8 variant, bus
  voltage and driver configuration (still to confirm with the supplier).
- Harness bend radius in the shoulder clock-spring cavity — needs the real
  Ø3.0 high-flex cable.

## Hardware worth ordering now so it's on the bench for the dry fit

4 × 6800-2RS bearings · 4 × Ø4 × 32 clevis pins + E-clips · 3 × Ø4 × 8 dowels
per shoulder gauge · 10 × M3 brass heat-set inserts (**5 mm long** — the bores are
5.0 mm deep with a 0.8 mm blind floor, so use a depth-stopped tip) · M3/M4/M2.5
SHCS assortment · 4 × Ø22/Ø16.5 × 0.5 PTFE thrust washers.

Screw lengths: **cable cover is M3 × 8**, not M3 × 10 — a revision-2 fix, and that
joint is still real. The knee-stop screws (M3 × 6 at 30° spacing) went with the
deleted stop arc; the reasoning for both is in
[`../beni_prototype1_rev2_changes.md`](../beni_prototype1_rev2_changes.md) §4.
