# Beni-Like Wheeled Biped — Prototype 1 Design Record

> **REVISION 2 — 2026-08-08.** This document describes revision 1 except where
> marked. Ten defects and production gaps were closed after it was written; the
> authoritative record of what changed and why is
> **`beni_prototype1_rev2_changes.md`**, and the numbers that moved are called
> out inline below with a **[REV2]** tag.
>
> **BUILD CONSTRAINT, 2026-08-12.** This record describes Prototype 1 as
> *engineered*, with machined 7075 hubs, a ground double-D knee axle and a
> hardened steel stop arc. **None of those are built that way any more:**
> 3D printed and off-the-shelf parts only, no laser cutting or machining — see
> **[`MANUFACTURING_CONSTRAINTS.md`](MANUFACTURING_CONSTRAINTS.md)**. The
> kinematics, load cases and mass properties below are unaffected and remain the
> reference; the *material and process* callouts are not. §7's knee-stop design is
> superseded in particular — see
> [`beni_single_leg_rig_design_record.md`](beni_single_leg_rig_design_record.md) §8.
>
> The mechanism, kinematics, spring design and load cases in §1–§7 are unchanged
> and were re-verified against the rebuilt model to 0.0000 mm. What changed was
> fastener geometry, the right leg, fillets, the tyre, the chassis builders, and
> the fact that the model now knows its own mass properties.

Companion to `beni_prototype1_fusion_guide_rewritten.md`.
Fusion project: **Biped** → `Beni_Prototype1`
Immutable references: `REF_GIM6010-8`, `REF_GIM4305-10`
Parametric build source: `beni_lib.py` (`build_all()` + `build_mirror()`
reconstructs every modelled part — **[REV2]**, this was not true in revision 1;
four parts had no builder and the side-panel builder had drifted to an older
revision, so running `build_all()` would have destroyed the chassis joint)
Export helpers: `beni_export.py` (STEP, URDF, STL)
Automated audit: `beni_lib.audit_all()` — currently **0 problems**

---

## 1. Guide verification

Every checkpoint table in the guide was recomputed independently before any
geometry was drawn, and the Fusion model was then measured against it.

### 1.1 Knee kinematics (shoulder at nominal)

| φ | vert. compression | guide | fore-aft | guide |
|---:|---:|---:|---:|---:|
| −8° | −12.04 | −12.0 | 11.63 | 11.6 |
| 0° | 0.00 | 0 | 0.00 | 0 |
| +5° | 8.31 | 8.3 | 6.37 | 6.4 |
| +10° | 17.13 | 17.1 | 12.00 | 12.0 |
| +15° | 26.42 | 26.4 | 16.83 | 16.8 |
| +20° | 36.09 | 36.1 | 20.84 | 20.8 |
| +25° | 46.08 | 46.1 | 23.99 | 24.0 |

Shoulder-to-wheel vertical at nominal = **154.269 mm** (guide: ~154.3).

### 1.2 Cartridge geometry and force

| φ | eye-to-eye | guide | moment arm | guide | spring F | guide | wheel F | guide |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| −8° | 77.70 | 77.70 | 22.09 | 22.09 | 30.0 N | 30 | 8.25 N | 8.3 |
| 0° | 74.44 | 74.44 | 24.54 | 24.54 | 64.0 N | 64 | 17.09 N | 17.2 |
| +10° | 69.91 | 69.91 | 27.39 | 27.39 | 111.4 N | — | 29.36 N | 29.4 |
| +20° | 64.90 | 64.90 | 29.95 | 29.95 | 163.8 N | — | 43.50 N | 43.6 |
| +25° | 62.23 | 62.23 | 31.12 | 31.12 | 191.6 N | 192 | 51.44 N | 51.5 |
| +27° | 61.14 | — | 31.56 | — | 203.0 N | — | 54.80 N | — |

Extension→design stroke **15.47 mm** (guide: 15.47). Effective wheel rate
0→+25° = **0.744 N/mm** (guide band 0.71–0.80). Measured model pin-to-pin at
nominal = 74.4431 mm.

### 1.3 Cartridge internal budget

Pin-to-pin dead length **25.57 mm** (11.00 upper + 14.57 lower incl. 2.0 mm of
shims). Spring length = eye-to-eye − 25.57.

| φ | spring length | deflection | force | solid-height margin |
|---:|---:|---:|---:|---:|
| −8° | 52.13 | 2.87 | 30.0 N | 21.45 |
| 0° | 48.87 | 6.13 | 64.0 N | 18.19 |
| +25° | 36.66 | 18.34 | 191.6 N | 5.98 |
| +27° | 35.57 | 19.43 | 203.0 N | **4.89** |

Solid height = 11.8 coils × 2.6 mm = **30.68 mm**. The spring therefore cannot
coil-bind before the +27° metal hard stop, with 4.89 mm to spare.

Rate check: `k = G·d⁴/(8·D³·n) = 79300 × 2.6⁴ / (8 × 16.4³ × 9.8) = 10.48 N/mm`
against the 10.45 N/mm target.

Preload is tunable **9.1 N … 30.0 N** at φ=−8° by removing 0–4 × 0.5 mm shims.

---

## 2. Motor reference audit (measured from the supplied STEP)

### 2.1 Steadywin GIM6010-8 — shoulder
Reference datum: **housing mount face at x = 0**, motor axis = x, output toward +x.

| Feature | Value |
|---|---|
| Overall length | 44.0 mm (x = −37.0 … +7.0) |
| Housing OD | Ø80.0, x = −25.0 … −1.0 |
| Rear face | x = −26.0 |
| Driver cover | Ø57.0, x = −37.0 … −26.0, cable exit notch in cover |
| **Housing mount** | **8 × M3 on Ø74.0 PCD**, 45° spacing, ~4.0 mm thread from the front face and ~4.8 mm from the rear, Ø6.0 through-bore between |
| Front mounting land | annulus Ø47 → Ø78 at x = 0 |
| Rotating face | annulus Ø34 → Ø46 at x = +2.0 (0.5 mm gap to the Ø47 housing bore) |
| Output pilot boss | Ø34.0, x = +2.0 … +3.0 — **unusable as a register** (root fillet blends to Ø36.4) |
| **Output mount face** | **x = +3.5**, annulus Ø13 → Ø33, **6 × M3 on Ø25.0 PCD, 5 mm deep** |
| **Anti-rotation pins** | **3 × Ø4.0 on Ø20.4 PCD**, protruding to x = +7.0 (3.5 mm), tip chamfer to Ø3.6, root chamfer Ø4.6 |
| Centre | Ø12/Ø13 blind recess 0.5 mm deep — **solid, no hollow shaft** |

### 2.2 Steadywin GIM4305-10 — wheel
Reference datum: **housing mount face at x = 0**, output toward −x.

| Feature | Value |
|---|---|
| Overall length | 33.0 mm (x = −27.0 … +6.0) |
| Housing OD | Ø53.0, x = −23.0 … −0.5 (Ø54.2 over small ribs) |
| **Housing mount** | **6 × M2.5 on Ø47.5 PCD**, 60° spacing, ~3 mm deep, at x = 0, in two arc lands interrupted by four relief flats |
| Driver cover | Ø40.4, x = 0 … +6.0, retained by 2 × M2 on Ø35 PCD (heads accessible from +x) |
| Bearing gland | Ø53.0, x = −26.0 … −23.0 |
| **Output flange face** | **x = −27.0**, Ø37.0 flange OD, **3 × M3 on Ø27.0 PCD, 4 mm deep**, six kidney lightening pockets |
| Centre | Ø10 mouth → Ø12 → Ø8 blind, 3 mm deep |

---

## 3. Lateral layout (left leg, frozen)

> **The Y datum and every dimension in this table are still authoritative** — other
> documents take these rows as the reference stack, and none of the numbers have
> moved. But four rows describe *parts that no longer exist in that form*, and
> those rows are tagged **[SUPERSEDED]** inline. A superseded row is history: read
> its y-coordinates as real, and its material/process as void. Routing for each is
> in [`MANUFACTURING_CONSTRAINTS.md`](MANUFACTURING_CONSTRAINTS.md).

| y (mm) | Feature |
|---:|---|
| 5 … 16 | shoulder motor driver cover (Ø57) |
| 17 … 41 | shoulder motor housing (Ø80) |
| **42** | **housing mount face** — 8 × M3 @ Ø74 PCD |
| 42 … 47 | `Chassis_Shoulder_Plate_L` (5 mm PA-CF, Ø96) |
| 44 | rotor face (Ø34…Ø46) |
| **45.5** | **output mount face** — 6 × M3 @ Ø25 PCD, 3 × Ø4 pins to y = 49 |
| 45.5 … 51.5 | **[SUPERSEDED]** `Shoulder_Output_Hub_L` body Ø38 (7075-T6) — **now printed**, with 3 bought Ø4 × 10 dowel pins and M4 inserts |
| 47 … 51 | cable spiral cavity, r = 20 … 32 (lip r = 32 … 33.5) |
| 51.5 … 53.5 | `Shoulder_Cable_Cover_L` (2 mm ABS ring, r = 30 … 47) |
| 51.5 … 59.5 | hub flange Ø56, Ø6 cable port at r = 21. **[HOLD 2026-09-02]** Its six Ø44-PCD holes still carry legacy Ø3.3 tapped-metal geometry; the printed hub needs real M4 insert pockets and a reprint. |
| **59.5** | **leg inboard face** |
| 55.7 … 58.7 | knee axle flange Ø15 |
| 58.7 … 64.5 | proximal arm A (5 mm + 0.8 mm knee boss), 6800 bearing at 58.7 … 63.7 |
| 63.7 … 85.3 | **[SUPERSEDED]** knee steel sleeve Ø16/Ø10 (double-D bore) — **`Knee_Sleeve_L` is DELETED**; its Ø16 bore is now printed as Ø10 directly into `Distal_Link_L` |
| 64.5 … 84.5 | **spring channel, 20 mm** — cartridge centred on y = 74.5, Ø19 spring spans 65 … 84 |
| 65 … 84 | distal knee boss Ø22 (19 mm) |
| 84.5 … 90.3 | proximal arm B (5 mm + 0.8 mm knee boss), 6800 bearing at 85.3 … 90.3 |
| **89.5** | **leg outboard face** |
| 90.3 … 93.3 | **[SUPERSEDED]** `Knee_Stop_Arc_L` (3 mm steel, two-level slot) — **DELETED**; the +27° stop is a compression column of bought M5 washers, see `beni_single_leg_rig_design_record.md` §8 |
| 90.3 … 96.3 | `Knee_Magnet_Carrier_L` Ø15, magnet face at 96.3 |
| 97.3 | AS5048A die face — **1.0 mm air gap** |
| 98.3 … 99.9 | encoder PCB; bracket shelf 99.9 … 101.9 |
| 59.5 … 67.5 | distal wheel-end plate (8 mm), Ø41.5 clearance for the motor driver cover |
| **67.5** | **wheel motor mount face** — 6 × M2.5 @ Ø47.5 PCD |
| 61.5 … 67.5 | wheel motor driver cover (Ø40.4) recessed into the plate |
| 68 … 90.5 | wheel motor housing (Ø53) |
| 69 … 99 | rim + tyre, tyre OD Ø110 (**centre y = 84**) |
| **94.5** | wheel motor output flange face |
| 94.5 … 100.5 | **[SUPERSEDED]** `Wheel_Hub_L` (7075-T6, Ø56) — **now printed**, with steel washers and a re-torque schedule |
| 100.5 … 104.5 | rim web, 6 × M4 @ Ø46 PCD into the hub. **[HOLD 2026-09-02]** The printed 6 mm hub still has legacy Ø3.3 tapped-metal bores; the insert/captive-thread scheme is not released. |

**Track = 168 mm.** Nothing rotating crosses y = 53.5, so the chassis is free
to occupy |y| ≤ 47 without ever fouling the leg sweep.

---

## 4. Recorded assumptions and deviations from the guide

1. **Structural leg/knee width is 30 mm, not ~28 mm.** This is forced. The
   guide freezes Ru = 36, Rl = 54, 110° anchor geometry, which fixes the
   spring's minimum moment arm at 22.09 mm (φ = −8°). With the guide's Ø19
   spring that puts the cartridge's outer surface 12.59 mm from the knee axis.
   A 20 mm clear channel is therefore mandatory, and 28 mm total leaves only
   4 mm per arm — not enough for a 6800 (Ø19) bearing seat. 30 mm gives 5 mm
   arms and a 20 mm channel with 0.5 mm spring clearance per side. Everything
   else in the guide's §17 freeze list is preserved exactly.
2. **The shoulder output's Ø34 pilot boss is not used as a register** — its root
   fillet blends out to Ø36.4, leaving under 0.2 mm of usable straight land.
   The hub instead locates on the motor's **3 × Ø4.0 anti-rotation pins** in
   reamed Ø4.05 H7 holes, with the 6 × M3 as the clamp. This is a better
   interface than the 1 mm spigot would have been.
3. **No central cable route exists** — the GIM6010-8 output centre is a 0.5 mm
   blind recess, not a through bore. Guide §8 option 1 therefore fails and
   option 2 is used: a clock-spring harness cavity (r = 20…32, 4 mm tall)
   between the shoulder plate and the rotating hub flange. With Ø3.0 high-flex
   cable and ~400 mm coiled the capacity is `L(1/r_i − 1/r_o) ≈ 8.2 rad ≈ 470°`
   against the 370° requirement — 27 % margin.
4. **Wheel-motor output register is only 1 mm deep**, so `Wheel_Hub_L` centres
   on a Ø37.3 H8 × 0.8 counterbore and takes torque through 3 × M3 on Ø27 PCD
   (friction capacity ≈ 20 N·m at 3 × 3.4 kN preload).
5. **The knee stop arc is fastened with blind M3 heat-set inserts**, not
   through-bolts. A through-bolt at the required radius would put its nut
   inside the spring channel *and* inside the distal link's knee web. Load at
   the inserts is shear (≈ 5 MPa on the insert/plastic interface at the 16 N·m
   impact case), not pull-out.
6. **The spring is modelled as a swept Ø2.6 helical wire body** with the specified
   Ø19 OD and 11.8 total-coil representation. It rebuilds to the cartridge length
   at every knee pose. The earlier annular outer-envelope model established the
   conservative 0.50 mm channel clearance; coil-bind acceptance still comes from
   the specified solid height and the supplier/press check, not spline end detail.
7. **The guide rod guides the spring only for φ ≳ +13°.** The stroke (16.6 mm)
   exceeds the axial room available between the lower eye's rod bore and its
   pivot pin, so the rod withdraws at high extension. This is acceptable: at
   φ ≤ +13° the spring is under 20 % deflection where buckling is not credible,
   and the Ø13.4 seat spigots capture both spring ends at all times.
8. **The distal link is single-sided at the wheel.** Nothing may sit inside the
   wheel's swept annulus (r = 44…55 from the wheel axis over y = 69…104.5), so
   the fork terminates and only the 8 mm inboard plate continues to the wheel.
9. **The cartridge separates when unpinned.** The spring is captured between two
   Ø13.4 seat spigots while both pivot pins are fitted; with a pin removed the
   assembly comes apart, which is what makes the spring replaceable.

---

## 5. Load cases and margins

| Case | Load | Checked |
|---|---|---|
| Static | 17.2 N per wheel (φ = 0) | reproduces guide table |
| Knee design point | 51.5 N per wheel (φ = +25°) | reproduces guide table |
| Crash/proof screen | 275 N at one wheel (≈ 8 g) | see below |

- **Shoulder mount:** 8 × M3 into 4 mm of aluminium thread. Thread shear area
  ≈ 22.6 mm² per bolt → 4.5 kN, above the M3 12.9 proof load (3.4 kN), so the
  screw is the weak element by design.
- **Hub → output torque path:** 6 × M3 on Ø25 PCD, friction capacity
  ≈ 6 × 3.4 kN × 0.15 × 12.5 mm = **38 N·m** against the 25 N·m proof-design
  screening load, plus 3 × Ø4 dowel pins as a positive backup.
- **Root joint:** 6 × M4 on Ø44 PCD, 7 mm thread in 7075. Dominant load is the
  14 N·m roll moment from 275 N acting 51 mm outboard → ≈ 412 N peak bolt
  tension.

> **[SUPERSEDED as the governing case]** The two threaded-in-metal margins above —
> "8 × M3 into 4 mm of aluminium thread" and "6 × M4 … 7 mm thread in 7075" — are
> the **as-designed metal** numbers and are retained as such. Both joints are now
> in **printed plastic with heat-set inserts**, so the failure mode is
> insert-to-plastic pull-out, not thread shear in aluminium, and neither figure is
> the governing margin for a build. Do not recompute them here; the printed-joint
> analysis lives in `beni_rig_no_machining.md` §2.1 and
> `beni_single_leg_rig_design_record.md`.

- **Knee axle:** Ø10 in double shear at the 6800 bearings. 275 N gives 1.75 kN
  of bending at 6.4 mm → 22 MPa in the shaft. Bearing pressure on the printed
  distal boss is carried by the Ø16 steel sleeve → 1.4 MPa on PA-CF.
- **Cartridge pivot pins:** Ø4 in double shear at 203 N → 8 MPa; bearing on the
  5 mm PA-CF arms 5 MPa; on the aluminium eye 2.7 MPa.
- **Knee hard stop:** spring torque at +27° = 203 N × 31.56 mm = **6.41 N·m**;
  at the stop-pin radius of 30 mm that is 214 N, taken as 534 N with a 2.5×
  impact factor. Bearing on the printed arm B is 17.8 MPa; the contact is
  hardened Ø6 dowel against a steel slot end with a matching 3.1 mm radius, so
  the metal contact is near-conformal rather than line contact.
- **Spring fatigue:** Wahl-corrected τ at +27° = 597 MPa against ≈ 855 MPa
  static allowable for shot-peened chrome-silicon. Over the 0 → +25° duty cycle
  τ_mean = 376 MPa, τ_alt = 189 MPa against ≈ 280 MPa Goodman allowable —
  infinite life.

**FEA caveat:** none of the above is a substitute for test. For PA-CF parts,
isotropic FEA is not proof; the bench tests in §8 must precede any powered jump.

---

## 6. Landing energy

3.5 kg dropped 100 mm arrives at 1.40 m/s carrying 3.43 J.

Energy the two passive knees can absorb from φ = 0 to the +27° hard stop:
spring force rises 64 → 203 N over 19.43 − 6.13 = 13.30 mm of spring travel, so
per leg `½(64+203) × 13.30 mm = 1.78 J`, and **3.55 J for the pair** — enough
for a 100 mm free drop with essentially no margin.

> **[REV2]** With the model's true mass of **3290.1 g** rather than the 3.5 kg
> design mass, a 100 mm free drop carries **3.23 J** against the pair's
> **3.553 J** (numerically integrated, not trapezoid-approximated), so there is
> **+10 % margin** rather than ≈0 %. The conclusion below is unchanged.

> **[CORRECTION — 2026-08-11]** Both the original and the REV2 energy comparison
> omit the m·g·Δz gravity work done during the ~50 mm of spring compression.
> Including it raises demand to **4.85 J** — a 100 mm free drop **bottoms out**.
> Passive free-drop capacity is **~49 mm** (spring-rate method; see
> `electronics/04_firmware.md` correction 3 and `fusion_brief_single_leg_rig.md`
> §4.3). The conclusion — that the shoulder must participate — is more than
> unchanged; it is stronger.

That is the quantitative reason the guide insists the shoulder participates. The
progressive PU bumper adds ≈ 0.7 J per knee at the very end of travel, and
active shoulder yielding must supply the rest. The design therefore does not
stiffen the main spring to survive the drop, and no oil damper is fitted; the
bumper pocket and the shoulder's ±185° range are the provisions kept open.

---

## 7. Knee stop design

> ### ⚠ SUPERSEDED FOR BUILDING — the whole of §7
> `Knee_Stop_Arc_L` was laser-cut 3 mm steel and is **DELETED**. The +27° hard stop
> is now a **compression column of bought M5 washers** inside the spring cartridge,
> with a printed TPU sleeve as the progressive bumper; a printed
> `RIG_Knee_Stop_Plate_L` keeps the −8° stop and a +28° backup. The authoritative
> design, the Hertzian contact-stress reasoning for every substitute considered,
> and the verification sweep are in
> [`beni_single_leg_rig_design_record.md`](beni_single_leg_rig_design_record.md) §8.
> Everything below is the as-engineered steel-arc design, kept for its angles,
> radii and load path only.

Two-level arc slot in a 3 mm steel plate (`Knee_Stop_Arc_L`) bolted to the
proximal arm-B boss, with a Ø6 hardened dowel pressed into the distal arm B at
r = 30 mm from the knee axis.

| Level | y span | Slot arc | Function |
|---|---|---|---|
| inner | 90.3 … 91.8 | 213.67° … 260.53° | **metal hard stops** at φ = +27° and φ = −8° |
| outer | 91.8 … 93.3 | 206.34° … 264.76° | houses the two replaceable PU blocks |

- Flexion bumper: 7.5 mm PU block, face at 220.67° → first contact at
  **φ = +20.0°**, crushed 3.67 mm (49 %) exactly as the pin reaches the steel
  face at +27°.
- Extension bumper: 3.0 mm PU block, face at 259.03° → first contact at
  **φ = −6.5°**, crushed 0.79 mm (26 %) at the −8° metal stop.

Both bumpers sit in open-ended bays and are replaceable without disturbing the
bearing stack. The final crash load path is dowel → steel slot end → 3 M3 in
shear → printed boss; no thin printed tab is ever the last line of defence.

> **[REV2] Two fastener defects in this joint were found and fixed:** the three M3
> screw heads overlapped and could not be fitted (now **30° spacing**, the arc
> plate grew 12° of sector, 2164 → 2463 mm³, +2.3 g each), and the blind insert
> bore was shallower than its insert so the screw bottomed out before clamping
> (now a **5.0 mm bore with M3 × 6**). Both are why `audit_fasteners()` and
> `audit_blind_holes()` exist. **Full account, with all the arithmetic:**
> [`beni_prototype1_rev2_changes.md`](beni_prototype1_rev2_changes.md) §4.

---

## 8. Recommended test sequence (before any powered jump)

1. **Print-order dry fit** — shoulder plate, hub, proximal link, distal link.
   Check the 3 × Ø4 pin holes engage the motor pins with no rock.
2. **Knee stack build** — press the bearings, fit the sleeve, insert the axle,
   torque the magnet carrier. Confirm free rotation and < 0.1 mm axial float.
3. **Static knee sweep by hand**, −8° to +27°, encoder logged. Confirm the
   encoder reads monotonically and the stops engage at the modelled angles.
4. **Spring rate verification** on a press: measure force at 6.13 mm and
   18.34 mm of deflection; expect 64 N and 192 N ±5 %. Adjust preload shims to
   land 17.2 N at the wheel with the leg at nominal.
5. **Static load test** — 17.2 N, then 51.5 N, then 275 N applied at one wheel
   through realistic worst-case directions. Inspect the knee boss, the stop
   arc's insert bosses and the wheel-end plate for permanent set.
6. **Low-energy drop tests** — 20 mm, then 50 mm, then 100 mm, unpowered, with
   the shoulder free to yield. Log knee angle. Do not proceed to a powered jump
   until the +27° stop is confirmed never to be reached at 100 mm.
7. **Cable spiral endurance** — 500 cycles of ±185° at the shoulder, then
   inspect the harness for insulation damage at both strain reliefs.

---

## 9. Items still needing outside confirmation

- **Exact GIM6010-8 variant and driver.** The guide's stale 9 N·m/25 N·m figures
  are not used. Current published variants are roughly 5 N·m rated / 11 N·m
  stall at 24 V and 4.6–5.4 N·m rated / 17.2–17.9 N·m stall at 48 V. The
  structure is proof-designed to 25 N·m regardless, but the *bus voltage,
  driver firmware and CAN/absolute-encoder configuration must be confirmed with
  the supplier* before jump tuning.
- **Spring supplier confirmation.** Ø19 OD × 2.6 mm wire × 55 mm free × ~9.8
  active coils, closed and ground ends, chrome-silicon to ASTM A877/A877M,
  shot-peened and preset. Confirm the achievable rate tolerance (±5 % assumed)
  and the actual solid height.
- **PU bumper compound.** 7.5 mm and 3.0 mm blocks at ~90 A assumed. The crush
  fraction (49 % on the flexion bumper) is at the upper end of sensible for
  polyurethane and is a bench-test tuning item.
- **PA-CF print parameters.** All mass figures assume 1.15 g/cm³ solid-equivalent.
  Wall count and infill for the links must be set so the modelled section is
  actually achieved, particularly the 5 mm arms at the knee.

---

## 10. Verification results

### 10.1 Knee sweep, shoulder at 0° (spring rebuilt at every angle)

**Clean across 11 knee angles, −8° through +27°.** The bumpers engage exactly
where they were designed to: nothing at +20° (first contact, 0 mm³), progressive
crush to +27° (12.7 mm³), and the extension pad only at −8° (1.4 mm³).

### 10.2 Shoulder sweep, −185° … +185°

**Clean across 35 shoulder poses** — 13 angles at knee φ = 0° and 11 each at
φ = −8° and φ = +27°. Whole-assembly checks (every body, both legs, chassis) at
the six corner poses (θ = −185/0/+185 × φ = −8/+27) are also clear.

**Why the sweep is clean by construction as well as by test:** all chassis
geometry lies within |y| ≤ 51 mm; the leg's inboard-most part is the output hub
at y ≥ 45.5 (Ø56 → r ≤ 28, running inside the panel's Ø48 bore); the next leg
part is the knee axle flange at y ≥ 55.7, which sits at r = 120 mm from the
shoulder axis where no chassis geometry reaches. Only the hub shares a y-band
with the chassis, and both are bodies of revolution there — so that clearance is
rotation-invariant.

### 10.3 Minimum clearances (mm)

| pair | φ = −8 | φ = 0 | φ = +27 | note |
|---|---:|---:|---:|---|
| spring ↔ proximal link | 0.50 | 0.50 | 0.50 | designed channel clearance |
| spring ↔ distal link | 0.50 | 0.50 | 0.50 | designed channel clearance |
| spring ↔ knee sleeve | 4.59 | 7.04 | 14.06 | worst case is full extension |
| proximal ↔ distal link | 0.50 | 0.50 | 0.50 | thrust-washer gap at the knee |
| upper eye ↔ proximal link | 0.50 | 0.50 | 0.50 | |
| lower eye ↔ distal link | 0.50 | 0.50 | 0.50 | |
| guide rod ↔ lower eye | 5.14 | 1.90 | 0.30 | 0.30 = the Ø5/Ø5.6 sliding fit |
| stop arc ↔ distal link | 0.80 | 0.80 | 0.80 | axial gap, plate to arm B |
| encoder die ↔ magnet | 1.00 | 1.00 | 1.00 | **the design air gap** |

> **[REV2]** The last row is the magnet-to-**package-face** clearance, not the
> die gap. The AS5048A is a TSSOP-14 ≈1.0 mm thick with the die near mid-package,
> so the true **magnet-to-die gap is ≈1.5 mm** — inside the AMS operating window
> for a Ø6 × 2.5 diametric magnet. No geometry changed; the claim was mislabelled.

| pose-independent | mm |
|---|---:|
| hub ↔ chassis side panel | 4.03 |
| hub ↔ cable cover | 2.00 |
| tyre ↔ distal link | 1.00 (radial, Ø110 tyre in the Ø112 relief) |
| knee axle flange ↔ side panel | 65.08 |
| distal link ↔ chassis frame | 113.73 |

### 10.4 Robot envelope

| | mm |
|---|---:|
| overall length (X) | 183 |
| overall width (Y) | 217 |
| overall height (Z) | 281 |
| **track** | **168** |
| ride height, shoulder axis to ground | 209.3 |

The shoulder-squat position (θ = +30°, knee held at 0°) drops the body 20.7 mm
relative to the wheel while the wheel travels 77.1 mm fore-aft — exactly the
mechanism the guide describes, with no deep static knee fold.

---

## 11. Defects found and fixed during the audits

Fourteen real defects were found across the two audit rounds — by automated
checks, not by eye — and all are fixed in the model and in `beni_lib.py`. They
ranged from cut features leaking across components, unreachable screws, nuts
landing inside the spring channel and rim bolts entering the wheel motor's
bearing gland, to a right leg that was never a complete copy, builders that
corrupted the assembly every time it was posed, a tyre with no retention, and
every body carrying the default "Steel". Three of the later seven were *hidden by
the way the earlier audits were run*: the interference sweep was executed with
screws filtered out, and the driver-access audit only ever asked whether a tool
could reach a screw, never whether two screws could coexist. **The authoritative
per-defect account, with the arithmetic and the fix for each, is
[`beni_prototype1_rev2_changes.md`](beni_prototype1_rev2_changes.md) §1–§8**;
reproducing it here would only let the two copies drift. Five new automated
checks were added so each class cannot recur — `audit_counts`,
`audit_lr_parity`, `audit_fasteners`, `audit_blind_holes`,
`audit_source_parity`.

### Automated audit results, revision 2

`audit_all()` reports **0 problems**.

- **Counts:** clean — 72 part/side entries, exactly one body each; all are single
  solid bodies, one shell and one lump each, so no enclosed voids (no trapped
  support), no disjoint lumps, no duplicate solids.
- **L/R parity:** clean — 32 part families matched by volume and face census.
- **Fastener head clearance:** clean.
- **Blind holes:** clean — every bore ≥ its insert, every screw clear of the floor.
- **Source parity:** 36 parts in the model, 36 classified, no orphans.
- **Driver access:** 32 hex-key access envelopes (Ø3.0–3.4, 30–45 mm reach)
  modelled for every screw serviceable on the complete robot. **Zero
  obstructions remain.**
- **Interference:** 72 pairs, of which **70 are screw-shank-in-tap-drill
  artifacts** and 2 are the documented M4-stud artifact. No structural clashes;
  clear at nominal and at every pose listed in §10.
- **Fillets:** 41, where there were previously none anywhere in the design.
- **Kinematics:** wheel axis matches closed form to **0.0000 mm** at
  (θ,φ) = (0,0), (0,+25), (0,−8), (−35,+12), (+185,0) after the full rebuild.

### Known modelling artifacts, not defects

- `Shoulder_Output_Hub_L` ↔ shoulder motor, 132 mm³ at any non-zero shoulder
  angle. This is exactly the volume of the motor's three Ø4 × 3.5 output pins.
  The pins rotate *with* the hub in reality; the STEP is a single body so the
  rotor cannot be separated from the stator.
- `Knee_Axle_L` ↔ `Knee_Magnet_Carrier_L`, 32.1 mm³ — the M4 stud inside the
  modelled tap drill. Screw/tapped-hole pairs generally show this.

---

## 12. Named motion positions

All ten required positions were built and verified: the wheel-axis position in
each matched the closed-form kinematics to **0.000 mm**.

| name | shoulder θ | knee φ | wheel axis (X, Z) |
|---|---:|---:|---|
| 01 Nominal stand | 0° | 0° | (0.00, −154.27) |
| 02 Shoulder squat | +30° | 0° | (−77.13, −133.60) |
| 03 Knee extension | 0° | −8° | (11.63, −166.31) |
| 04 Knee 10° compression | 0° | +10° | (−12.00, −137.13) |
| 05 Knee 20° bumper engage | 0° | +20° | (−20.84, −118.18) |
| 06 Knee 25° design point | 0° | +25° | (−23.99, −108.19) |
| 07 Knee 27° hard stop | 0° | +27° | (−25.00, −104.13) |
| 08 Jump-drive pose | −35° | +12° | (65.06, −117.38) |
| 09 Self-right sweep | +185° | 0° | (13.45, 153.68) |
| 10 Self-right sweep | −185° | 0° | (−13.45, 153.68) |

**They are not shipped as Fusion snapshots, and that is deliberate.** Rolling the
timeline back onto a snapshot makes this document resolve the two inserted motor
references to a stale version (the shoulder body reappears 26 mm out of position —
the difference between the original STEP datum and the re-datumed reference). The
leg and chassis geometry in every snapshot was correct — the wheel checked to
0.000 mm in all ten — but shipping a file whose rolled-back states contain
misplaced motors would be worse than shipping none. The proper fix is to break the
two external references (`Occurrence.breakLink()`) and re-create the snapshots;
that was not done because the mirror feature takes those occurrences as inputs and
the risk of corrupting the verified assembly outweighed the benefit.

Instead the positions are reproducible on demand:

```python
import sys; sys.path.insert(0, '/Users/neilchulani/Fun/Robots/Biped')
import beni_lib; from beni_lib import *
set_pose(theta_deg, phi_deg)      # e.g. set_pose(0.0, 25.0)
```

`set_pose()` rebuilds the helical spring body for the knee angle, then poses the
whole leg from a cached nominal state. It is the same function used for every
sweep in §10.

---

## 13. Acceptance checklist (guide §15)

> Two rows below cite deleted hardware — the "Ø16 steel sleeve" (now a Ø10 bore
> printed into `Distal_Link_L`) and the "dowel → steel slot end" load path (now a
> compression column of bought M5 washers). Both requirements are still met, by
> the substitutes in `beni_single_leg_rig_design_record.md` §4 and §8.

| requirement | status |
|---|---|
| full 360° shoulder sweep physically possible | **yes** — −185…+185 verified at φ = −8, 0, +27; clean by Y-separation as well |
| shoulder wiring survives the full sweep | **yes** — clock-spring cavity r = 20…32 × 4 mm, ~400 mm of Ø3.0 cable gives 430° against 370° needed; envelope modelled and unobstructed |
| nominal wheel axis directly below the shoulder | **yes** — (0.00, −154.269) |
| Fusion reproduces the knee kinematic checkpoints | **yes** — all seven rows to ±0.02 mm |
| Fusion reproduces the spring eye-to-eye checkpoints | **yes** — measured pin-to-pin 74.4431 at nominal, 61.141 at +27° |
| passive knee is a real revolute joint with real spring hardware | **yes** — 2 × 6800, Ø10 keyed axle, Ø16 steel sleeve, real spring/rod/seats/shims |
| spring cannot escape or coil-bind before the hard stop | **yes** — 4.89 mm above solid height at +27°; both ends captured on Ø13.4 spigots |
| knee bearings/axle physically assemblable | **yes** — sequence in the BOM document; axle inserts from inboard after the bearings and sleeve |
| spring cartridge can be replaced | **yes** — one clevis pin, no need to disturb the bearing stack, shoulder or wheel |
| bumper and hard stop have real load paths | **yes** — dowel → steel slot end → 3 × M3 shear → printed boss; PU in open-ended bays |
| knee encoder physically fits and can be wired | **yes** — AS5048A at a 1.00 mm air gap, bracket on 2 inserts, cable slot through the shelf |
| wheel motor and connectors removable | **yes** — 6 × M2.5 from inboard; the motor's own cover screws stay accessible |
| every screw has tool access | **yes** — 32 access envelopes modelled, zero obstructions |
| every nut/washer/spacer has an installation path | **HOLD** — the spring channel has no trapped nuts, but the printed shoulder hub, wheel hub, Mode A stand, future chassis frame and deferred carriage threaded interfaces failed the 2026-09-02 insert audit; see `MANUFACTURING_CONSTRAINTS.md` |
| every printed part has an explicit viable print orientation | **yes** — BOM document §1–3 |
| no inaccessible support required | **yes** — every part is single-shell, so there are no enclosed cavities |
| one-leg assembly passes all collision sweeps before duplication | **yes** — §10.1/10.2 were run on the single leg first |
| complete robot passes all shoulder/knee collision combinations | **yes** — §10.2 |
| PA-CF used for primary load paths | **yes** — links, side panels, wheel rim, chassis frame |
| structural proof cases reviewed | **yes** — §5, with the FEA caveat |
| BOM and assembly sequence complete | **yes** — separate document |

**Two items are qualified rather than clean:**

- Named positions are delivered as a reproducible API plus a verification table
  rather than as Fusion snapshots (§12).
- The mass roll-up lands at ≈ 3.30 kg against the 3.5 kg design mass, leaving
  ≈ 200 g of margin. That is real but thin, and the reduction targets are listed
  in the BOM document §8.

---

## 14. [REV2] Mass properties

Revision 1 had none: every body carried the default "Steel", Fusion reported the
robot at **8174.2 g**, and there was no centre of mass or inertia tensor anywhere
in the project. Nothing downstream — balance controller, URDF, simulation —
could be built from it.

| | value |
|---|---:|
| Mass (from Fusion, materials assigned) | **3290.1 g** |
| Design mass | 3500 g |
| Margin | **≈ 210 g (6.0 %)** |
| CoM X, fore-aft from the shoulder axis | **+6.46 mm** |
| CoM Y, lateral | **−0.00 mm** |
| CoM Z | −50.57 mm |
| **CoM height above the wheel axis** | **103.7 mm** |
| Ixx about CoM (roll) | 0.03214 kg·m² |
| **Iyy about CoM (pitch — governs balance)** | **0.02508 kg·m²** |
| Izz about CoM (yaw) | 0.01706 kg·m² |
| Ixz about CoM | +0.002759 kg·m² |
| Inverted-pendulum time constant √(L/g) | 0.103 s |

The helical spring and three simplified bought-assembly/presentation bodies carry
a derived density so the assembly mass remains exact: the spring at 25.3 g, the
harness spiral at 7 g, and the battery and electronics blocks at 250 g and 120 g.
They are listed in `beni_lib.MASS_OVERRIDE_G`; left and right spring materials are
recalibrated independently when their posed lengths differ.

**CoM Y = −0.00 mm is now a standing symmetry check.** Any part missing from one
leg shows up in it immediately — it is how the missing right-hand spring
(§11 [REV2] item 11) was caught.

**The +6.46 mm fore-aft offset is inherent, not a defect.** The two links and the
knee hardware sit around X = +45…+92 while both wheels and both shoulder motors
sit at X = 0. Moving the battery aft (centre X = −0.5 → −30.5) and placing the
electronics block at X = −52 took it from +11.97 mm to +6.46 mm; nulling it
entirely would need ≈89 mm of travel on the whole 450 g chassis group, which does
not exist in a 110 mm frame. In service it is a **0.21 N·m standing bias**
(0.11 N·m per wheel) and it means the equilibrium stance sits a few degrees off
the nominal pose. That is a controller trim term.

Per-link masses and full inertia tensors for all six moving links:
`sim/beni.urdf` and `sim/beni_inertia.json`. The exporter asserts mass closure —
every gram in the assembly must land in exactly one link.

## 15. [REV2] Why there are still no Fusion joints

Live Fusion joints were deliberately not added — they constrain occurrence
transforms and so cannot coexist with the scripted posing (`beni_lib.set_pose()`)
that every sweep and clearance table in §10 runs on. Full reasoning and what was
provided instead (URDF limits, `web/index.html`, Fusion user parameters):
[`beni_prototype1_rev2_changes.md`](beni_prototype1_rev2_changes.md) §12.
