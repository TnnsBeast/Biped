# Beni Prototype 1 — Machined Parts Specification

> ### ⛔ NOT A SHOPPING LIST — nothing here is machined any more
>
> **3D printed and off-the-shelf parts only. No laser cutting, no machining.**
> See **[`../MANUFACTURING_CONSTRAINTS.md`](../../MANUFACTURING_CONSTRAINTS.md)**.
>
> All **ten** families below have been rerouted. Nine went to printed or bought
> parts in [`../beni_rig_no_machining.md`](../../beni_rig_no_machining.md) §2–§3; the
> tenth, `Knee_Stop_Arc_L`, was deleted and its function moved into the spring
> cartridge — [`../beni_single_leg_rig_design_record.md`](../../beni_single_leg_rig_design_record.md) §8.
>
> | Family | Now |
> |---|---|
> | 1 `Shoulder_Output_Hub_L` | printed + 3 bought Ø4 × 10 dowel pins + M4 inserts |
> | 2 `Wheel_Hub_L` | printed + steel washers + re-torque schedule |
> | 3 `Cart_Upper_Eye_L` | printed, measured, fed back to the spring model |
> | 4 `Cart_Lower_Eye_L` | printed, measured, fed back to the spring model |
> | 5 `Knee_Axle_L` | bought Ø10 h6 hardened ground dowel pin |
> | 6 `Knee_Sleeve_L` | deleted; its bore is printed into `Distal_Link_L` as Ø10 |
> | 7 `Knee_Magnet_Carrier_L` | printed, runout measured on an indicator |
> | 8 `Knee_Stop_Arc_L` | deleted; hard stop is a bought M5 washer column in the cartridge |
> | 9 `Cart_Guide_Rod_L` | bought Ø5 × 50 hardened shaft |
> | 10 `Cart_Preload_Shim_L` | bought Ø19/Ø13.6 × 0.5 shim washers |
>
> **This document is still the authority on the fits, tolerances and load cases**
> those parts have to satisfy, and §12's fit table is still what the printed
> coupon is measured against. Read it as the requirement, not the process.


Companion to `beni_prototype1_bom_and_assembly.md`.
Geometry source: `Biped → Beni_Prototype1`, exported per part to
`manufacturing/step/<Part>.step` (STEP AP214, millimetres, parts at their
assembly coordinates).

**Why this document exists.** Until now these ten part families existed only as
STL, and the H7/H8/h6 fits existed only as prose in the BOM. No shop can quote
or program from that. Everything below is a callout, not a description.

---

## 0. General requirements

| Item | Requirement |
|---|---|
| Units | millimetres |
| Default linear tolerance | ±0.1 unless a fit class or explicit tolerance is given |
| Default angular tolerance | ±0.5° |
| Edges | all sharp edges deburred; **no burrs in any bore or on any slot end** |
| Threads | ISO metric coarse, class 6H |
| Cleanliness | degreased, no cutting fluid residue in blind holes |
| Marking | part number and `L`/`R` where handed, on a non-functional face |

**Handedness.** Nine of the ten families are bodies of revolution whose hole
patterns are rotationally symmetric, so they are **not handed** — order 2 of
each and set the rotation at assembly. The exception is `Knee_Stop_Arc_L`,
which is a flat plate with handed angular features: order **1 LH + 1 RH**,
RH being the mirror image through the plate's own mid-plane.

One caveat on `Shoulder_Output_Hub_L`: it carries three features on a 120°
pattern of which one is a Ø6 harness port and two are Ø11 lightening pockets.
Simplest robust instruction — **drill all three positions as Ø6 ports and
machine all three as Ø11 pockets**, so a single part number serves both sides
and the harness exits through whichever position suits the build.

---

## 1. `Shoulder_Output_Hub_L` — 7075-T6, qty 2

Torque path from the shoulder actuator into the leg. Proof-designed to 25 N·m.

| Feature | Spec |
|---|---|
| Body | Ø38.0 × 6.0, stepping to a Ø56.0 × 8.0 flange (overall 14.0 long) |
| **3 × Ø4.05 H7** (+0.012 / 0) | on **Ø20.4 PCD ±0.02**, through. Locates on the motor's anti-rotation pins — **this is the register, not the Ø34 boss** |
| 6 × Ø3.4 through, c'bore Ø6.2 × 4.0 deep | on Ø25.0 PCD ±0.05. Clamp screws into the motor output |
| 6 × M4 × 7.0 deep, blind | on Ø44.0 PCD ±0.05, in the flange. Proximal-link root joint |
| Ø12.0 central bore | through |
| Ø6.0 harness port | at r = 21.0 (see the handedness note above) |
| 3 × Ø11.0 × 5.5 pockets | at r = 21.0, 120° spacing |
| **Motor mating face** (the Ø38 end) | flatness **0.02**, perpendicular to the Ø4.05 dowel axes within **0.05** |
| Flange face | parallel to the mating face within 0.05 |
| Surface finish | Ra 1.6 general, **Ra 0.8 on the mating face** |

Critical: the dowel holes carry positional load. Ream after drilling; do not
drill to size.

## 2. `Wheel_Hub_L` — 7075-T6, qty 2

| Feature | Spec |
|---|---|
| Body | Ø56.0 × 6.0 |
| **Ø37.3 H8** (+0.039 / 0) **× 0.8 deep** | counterbore register on the motor output flange. The motor's own register is only 1 mm deep, so this is the entire centring feature |
| 3 × Ø3.4 through, c'bore Ø6.5 × 3.0 | on Ø27.0 PCD ±0.05 |
| **6 × M4 × 6.0 deep, BLIND** | on Ø46.0 PCD ±0.05. **Must not break through.** A through-drilled hub put M4 × 14 screws inside the motor's Ø53 bearing gland |
| Ø12.0 central bore | through |
| Register face | perpendicular to the Ø37.3 bore within 0.03 |
| Surface finish | Ra 1.6, Ra 0.8 in the Ø37.3 register |

Torque is carried by friction at the 3 × M3 (≈20 N·m capacity at 3 × 3.4 kN
preload); the register is for centring only.

## 3. `Cart_Upper_Eye_L` — 7075-T6, qty 2

| Feature | Spec |
|---|---|
| Overall width | **19.0 −0.1 / −0.0** — runs in the 20 mm spring channel with 0.5 mm per side |
| Ø4.15 H9 pivot bore | through the 13 mm boss |
| **Ø5.0 H7** rod bore | press fit for the guide rod, ≥6 mm deep |
| Ø13.4 × 4.0 spring spigot | captures the spring's ground end |
| Pivot bore to spigot face | **11.00 ±0.05** — this is the upper half of the 25.57 mm cartridge dead length, and the spring force curve depends on it |

## 4. `Cart_Lower_Eye_L` — 7075-T6, qty 2

| Feature | Spec |
|---|---|
| Overall width | 19.0 −0.1 / −0.0 |
| Ø4.15 H9 pivot bore | through the 13 mm boss |
| Ø5.6 +0.1 rod clearance bore | 8.5 deep, sliding clearance on the Ø5 rod |
| Ø13.4 × 6.0 spring spigot | plus a shim stack seat |
| Pivot bore to spigot face | **14.57 ±0.05** including 2.0 mm of shims |

## 5. `Knee_Axle_L` — steel, qty 2

Ø10 in double shear at the two 6800 bearings.

| Feature | Spec |
|---|---|
| Journal | **Ø10 h6** (0 / −0.009) × 31.6 |
| Flange | Ø15.0 × 3.0 at the inboard end |
| **Double-D across flats** | **8.40 −0.02 / −0.00** over the 21.6 mm sleeve length |
| Thread | M4 × 8 deep, tapped, outboard end |
| Material | 4140 pre-hardened, or through-harden to **40–45 HRC** |
| Journal finish | **Ra 0.4**, cylindricity 0.008 |
| Runout | flats and thread concentric to the journal within 0.03 TIR |

Inserts from the **inboard** side only; the cartridge and stop arc must be off.

## 6. `Knee_Sleeve_L` — steel, qty 2

| Feature | Spec |
|---|---|
| OD | **Ø16 h6** — light press into the printed distal boss. Expect to ream the PA-CF bore; see the fit coupon in `print_stl/README.md` |
| **Double-D bore across flats** | **8.60 +0.05 / +0.00** (0.10 clearance per side on the 8.40 axle) |
| Bore | Ø10.0 +0.05 on the round portion |
| Length | **21.6 ±0.05** |
| Finish | Ra 1.6 |

The key is on the **bore**, not the OD. Cutting the flats on the OD severs the
sleeve into two pieces.

## 7. `Knee_Magnet_Carrier_L` — steel, qty 2

Carries the encoder magnet, so its geometry sets the sensor air gap.

| Feature | Spec |
|---|---|
| Body | Ø15.0 × 6.0 |
| Male stud | M4 × 8 |
| **Magnet pocket** | **Ø6.1 H8 × 2.5 deep**, flat bottom |
| Pocket bottom | perpendicular to the stud axis within **0.02**, concentric within **0.05 TIR** |
| Outboard face | this face sits at y = 96.3; the encoder package face is at 97.3 |

Magnet concentricity is the one thing that degrades the absolute encoder, so
the TIR callout is not optional.

## 8. `Knee_Stop_Arc_L` — steel plate, hardened, qty 1 LH + 1 RH

**This is the final crash load path.** Dowel → slot end → 3 × M3 in shear →
printed boss. Nothing downstream of it is compliant.

| Feature | Spec |
|---|---|
| Plate | **3.0 ±0.05** thick, annular sector r = 11.0 → 35.5 |
| Inner slot level (y 0 → 1.5) | arc slot r = 26.9 → 33.1, **ends at 219.60° and 254.60° ±0.1°** — these are the metal hard stops at φ = +27° and −8° |
| Slot end radius | **3.10 +0.05** to match the Ø6 dowel near-conformally |
| Outer slot level (y 1.5 → 3.0) | arc slot r = 26.9 → 33.1, 206.34° → 264.76°, houses the PU bumpers, open-ended |
| 3 × Ø3.4 | at r = 15.0, at **230°, 260°, 290° ±0.1°** |
| Hardness | through-harden **45 HRC**, or case-harden the slot ends to **50–55 HRC** |
| **Slot end faces** | **Ra 0.8, no burrs, no radius break** — impact contact surface |
| Flatness | 0.05 over the sector |

Angles are measured in the knee-local frame with 0° along +X; the load case is
534 N at r = 30 (214 N static × 2.5 impact).

The bolt circle changed from 20° to **30° spacing**: at 20° the three M3 SHCS
heads sat 5.209 mm apart against a Ø5.5 head and physically overlapped.

## 9. `Cart_Guide_Rod_L` — steel, ground, qty 2

| Feature | Spec |
|---|---|
| Length | 50.0 ±0.2 |
| Press end (6 mm) | **Ø5 n6** (+0.016 / +0.008) into the upper eye's Ø5.0 H7 |
| Remainder | Ø5.0 h9, sliding in the lower eye's Ø5.6 bore |
| Finish | Ra 0.4, straightness 0.05 over the length |
| Ends | chamfer 0.5 × 45° both ends |

The rod guides the spring only for φ ≳ +13°; it withdraws at high extension by
design, which is acceptable because the Ø13.4 spigots capture both spring ends
at all times.

## 10. `Cart_Preload_Shim_L` — steel shim stock, qty 8 fitted + 8 spare

| Feature | Spec |
|---|---|
| OD / ID | Ø19.0 / Ø13.6 |
| Thickness | **0.50 ±0.02** |
| Flatness | 0.02 |

Preload is tuned by removing 0–4 shims per cartridge, which moves the φ = −8°
force from 30.0 N down to 9.1 N.

---

## 11. Purchased items these parts mate to

| Item | Spec | Note |
|---|---|---|
| Knee bearing | 6800-2RS, 10 × 19 × 5, sealed | qty 4 |
| Knee stop dowel | **Ø6 × 9 hardened dowel, h6** | qty 2, press into the distal arm B |
| Cartridge pivot pin | Ø4 × 32 clevis pin + E-clip DIN 6799-4 | qty 4 |
| Main spring | Ø19 OD × 2.6 wire × 55 free × ~9.8 active coils, closed & ground, **chrome-silicon ASTM A877/A877M**, shot-peened + preset, **10.45 N/mm ±5 %** | qty 2. Confirm the achieved solid height — the design has only 4.89 mm of margin above it at the +27° stop |
| Heat-set insert | M3 brass, **5.0 long** | qty 10. Bores are now 5.0 deep; install with a depth-stopped tip, the blind floor is 0.8 mm |
| Encoder magnet | Ø6 × 2.5 **diametric** NdFeB | qty 2 |
| Encoder | AS5048A or AS5047-class, 14 × 14 PCB | qty 2 |

---

## 12. Fit summary — verify against the printed coupon first

`print_stl/GAUGE_Fit_Coupon.stl` carries all six critical bores. Print it in
PA-CF and measure before committing to any machining, because two of these
fits land in printed plastic rather than metal:

| Fit | Male | Female | Class |
|---|---|---|---|
| Bearing in proximal arm | 6800 OD Ø19 | **printed** Ø19 | light press |
| Sleeve in distal boss | Ø16 h6 steel | **printed** Ø16 | light press |
| Axle in sleeve | 8.40 flats | 8.60 flats | 0.10/side clearance |
| Axle in bearing | Ø10 h6 | 6800 bore Ø10 | slip |
| Hub on motor pins | motor Ø4.0 | Ø4.05 H7 | slip, located |
| Wheel hub on flange | motor Ø37.0 | Ø37.3 H8 | centring only |
| Rod in upper eye | Ø5 n6 | Ø5.0 H7 | press |
| Stop dowel in arm B | Ø6 h6 | **printed** Ø6 | light press |
