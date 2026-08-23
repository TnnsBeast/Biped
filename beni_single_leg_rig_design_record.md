# Beni Single-Leg Test Rig — Design Record

> ### ⚠ AMENDED 2026-08-17 — the build is MODE A ONLY
>
> Scope decision by the project owner: **build Mode A, defer Mode B.** The leg
> bolts to a printed `RIG_Stand` clamped to the bench. There is no rail, no
> carriage, no ballast, no index bar, no mode pin, no drop release, no end
> bumpers, no 2020 base or column. Rationale and the full deleted list are in
> `fusion_brief_single_leg_rig.md`'s header banner and §3. The CAD handoff is
> **[`fusion_agent_guide_mode_a.md`](fusion_agent_guide_mode_a.md)**.
>
> **This record is not superseded.** Almost all of it is about the *leg*, not the
> fixture, and that content is unaffected: §2.2's five-hole panel interface, §2.4's
> coupon analysis, §4's Ø10 dowel-pin knee (the whole recommendation), §6.2's five
> measurement traps, §7's print orientations, §8's knee stop, and every spring and
> force number. What changes:
>
> | Section | Mode A status |
> |---|---|
> | §0 departures **1, 2, 5** | moot — no rail to be 400 mm, no drops to limit, no ballast to budget. **3, 4, 6, 7, 8, 9, 10 all stand.** |
> | §1 "Mode A is Mode B with a pin" | taken to its end: the stand *is* the pin. §1.1's front-face decision **still governs** — it is why the stand's outboard face lands on y = 42.0 |
> | §1.2 parts | eight rows **[DEFERRED — MODE B]**; base + column + carriage collapse into `RIG_Stand` |
> | §2.1 rail length, §2.3's 63.00 mm stack | **[DEFERRED]**. Mode A overhang is **42.00 mm** — the 13.0 block and 8.0 carriage plate leave the stack |
> | §2.3 moment check | **redone for Mode A**, see the note in that section. Yaw 11.00 N·m dominates; pitch 2.30, roll 2.99 |
> | §3 drop series, §3.1 bounce mode | **[DEFERRED — MODE B]**. The 54.8 N force ceiling is **not** deferred — it is a spring property |
> | §5 mass properties, ballast | **[DEFERRED — MODE B]**. Mode A carries 0.8382 kg of leg static, 1.2262–1.3382 kg with the motor |
> | §6 checks | six become four plus a hold-down check; brief §4.4 |
> | §9 purchase list | linear-motion and extrusion sections **deleted**; §9 carries the note |
> | §10 drop stations | **[DEFERRED — MODE B]** in full |
>
> Mode A load set: `rig_calc.mode_a_stand()`. **Step 6, spring characterisation,
> runs in Mode A** (brief §6), so F₀ and k are still measured in this build.

**Answers `fusion_brief_single_leg_rig.md`.** Fusion document: **`Biped → Beni_SingleLegRig`**,
saved as a copy of the verified `Beni_Prototype1` so the master was never touched.

| Deliverable (brief §7) | Where |
|---|---|
| 1. Fusion assembly, ~~both modes~~ **Mode A**, §4.4 checks verified | §1, §6 |
| 2. STLs + per-part print orientation | §7, `rig_stl/README.md` |
| 3. ~~DXF for `Knee_Stop_Arc_L`~~ | §8 — **withdrawn, no laser parts** |
| 4. Purchase list | §9 |
| 5. ~~Mass-properties report~~ **Mode A load report** | §5, `rig_calc.mode_a_stand()` |
| 6. Recommendation on §2.3 | §4 |
| 7. What the rig cannot test | §11 |

Reproduce everything: `rig_lib.py` (builders + checks), `rig_calc.py` (arithmetic),
`rig_export.py` (STL), `stl_inspect.py` (mesh measurement).

**No laser-cut and no machined parts.** Every part is either 3D printed or bought
off the shelf — the project rule, stated authoritatively in
**[`MANUFACTURING_CONSTRAINTS.md`](MANUFACTURING_CONSTRAINTS.md)**. The two steel
parts an earlier revision of this record called for — the `Knee_Stop_Arc_L` plates
and the `RIG_Ballast_Disc` sectors — are replaced in §8 and §5. Their retired DXFs
are kept under `archive/laser/` only in case the two-leg build wants the steel arc
back.

---

## 0. Read this first — ten places this departs from the brief

Each is a number in the brief that did not survive being recomputed, or a
constraint the brief did not have. None is a matter of taste.

| # | Brief says | This build | Why |
|---|---|---|---|
| 1 | MGN12 rail **300 mm**, "231 mm usable travel" | ~~**400 mm**~~ **no rail — [DEFERRED, MODE A build]** | 231 mm is the *one-block* figure. Two MGN12H at 80 mm centres occupy 45.4 + 80 = **125.4 mm** of rail, so 300 mm leaves 150.6 mm after bumpers against a **151.5 mm** stroke requirement — 0.9 mm short before any bumper. 400 mm gives 250.6 mm. §2.1. **Moot in Mode A: nothing travels.** |
| 2 | Passive drop limit **49 mm** | ~~**45 mm** planning limit; **46.3 mm** computed +24° gate crossing~~ **[DEFERRED — MODE B]** | The brief's own step-10 gate is φ_peak < +24°. That is reached at **46.3 mm**, so a 49 mm drop already breaks the gate; 45 mm is the round planning limit just inside it. +25° is at 50.7 mm, the +27° metal stop at **60.0 mm**. §3. **No drops in Mode A — but these are the numbers the two-leg build inherits.** |
| 3 | Peak force **~53 N** | **54.8 N** at the stop, 51.4 N at +25° | Exact integration of the frozen spring curve. §3. **Stands in Mode A** — it is a property of the spring, not of the fixture. |
| 4 | "Print the two GAUGE coupons" resolves C2 and C3 | Resolves **C3 only** | `GAUGE_Shoulder_Motor_Interface.stl` is **9.5 mm long** (y −6…+3.5) — the front face and the output interface, nothing else. It cannot see a 40-vs-44 mm motor. §2.4. **Stands.** |
| 5 | Ballast adjustable for **1.2** / 1.645 / 2.0 kg | ~~**1.2 kg is impossible**~~ **no ballast — [DEFERRED, MODE A build]** | The bare slide is **1607.6 g**. 1.2 kg would need 408 g *removed* and there is nothing left to remove. §5. **Moot in Mode A: the stand carries 0.8382 kg of leg as a static hanging load, which is 3 % of the yaw it is sized by.** |
| 6 | `Chassis_Shoulder_Plate_L` is "Ø96, 8 × M3 on Ø74 PCD" | 120 × 120 panel, Ø48 bore | It is the chassis **side panel**. The Ø74 PCD is the *motor's* pattern, already used by the motor's own screws, so the ~~carriage~~ **stand** bolts to the panel's **five existing frame-bolt holes** instead. §2.2. **Stands — and it is now the stand's primary interface.** |
| 7 | (not mentioned) | Housing screws **M3 × 8**, not M3 × 10 | The inherited model uses M3 × 10 through a 5 mm panel into a **4.0 mm** thread → 5 mm of screw into 4 mm of hole. Bottoms out before it clamps — the same defect class as the two found in design record §7 [REV2]. §9. **Stands.** |
| 8 | `Knee_Stop_Arc_L`, laser-cut 3 mm steel at 45 HRC | **Deleted.** The +27° stop becomes a **compression stack inside the spring cartridge**; a printed plate keeps the −8° stop and a +28° backup | No laser parts. And the steel plate only worked because its slot ends were *conformal*; every printed or bought convex substitute reverts to Hertzian line contact at 1.0–1.8 GPa. §8. **Stands. The −8° stop is live in Mode A; the +27° column is only needed before step 10.** |
| 9 | `Distal_Link_L` "reuse as-is" | **Re-exported** | Adopting §2.3 moves the sleeve's Ø16 bore into the printed link as Ø10. This is the hidden cost of deleting the double-D. §4. **Stands.** |
| 10 | (not mentioned) | The cartridge's usable internal length is **44.570 mm consumed**, not 35.57 | Measured with a probe ring at six knee angles, spread 0.0000 mm. The dead-length build-up (11.00 + 14.57 + 4.0 + 6.0) is 9.0 mm optimistic. Sizing the new stop from the build-up would have put the hard stop at **+10°**. §8. **Stands.** |

**Departure 11, added 2026-08-17 — the brief's two-mode stand is one mode.** The
brief asks for "one stand with two modes" and this build delivers Mode A only, on a
printed stand rather than a pinned carriage. See the header banner. The lateral
overhang consequently drops from **63.00 mm to 42.00 mm** (§2.3).

---

## 1. Architecture, and the one decision that shaped it

**Mode A is Mode B with a pin through the carriage**, as the brief requires — and
in this build the mode pin and the drop release are literally *the same pin in
the same hole*. A pin through a round hole in the carriage and a station in a
fixed bar constrains the carriage in both directions (Mode A) and holds it up at
a drop height (Mode B). The only difference between the two modes is which
station you use.

### 1.1 Why the carriage hangs off the motor's front face

The GIM6010-8 has 8 × M3 on the Ø74 PCD tapped **from both ends** — 4.0 mm deep
from the front face at y = 42 and 4.8 mm deep from the rear at y = 16, with a
through-bore between (design record §2.1, confirmed against the STEP: the rear
taps measure Ø2.46 from y 16.2 to 21.0).

Bolting the carriage to the **rear** flange is structurally better: the load path
becomes carriage → aluminium housing → front face → rotor → leg, instead of
carriage → 5 mm printed panel → motor. It costs 26 mm of extra overhang, which
the brief's own sensitivity analysis says is immaterial.

**It was rejected anyway.** The brief requires every interface to be gated on the
GAUGE coupons, and the shoulder coupon models only the front 9.5 mm of the motor
(§2.4). Putting the rig's primary structural joint on a face the coupon cannot
check would defeat the gate. The front face it is — and that also keeps the
lateral stack identical to the brief's §4.1, which check 6 then reproduces
exactly.

### 1.2 Parts

**Mode A (2026-08-17):** the `RIG_Stand` column below is the live routing.
`RIG_Base`, `RIG_Column`, `RIG_Braces` and `RIG_Carriage` are replaced by a single
printed `RIG_Stand` whose outboard face is the motor front mount face at y = 42.0
and which is **clamped or bolted to the bench** — it reacts 11.00 N·m of yaw and
cannot be held by dead weight (brief §3).

| Part | What it is | Route | Mode A |
|---|---|---|---|
| `RIG_Stand` | printed stand, carries the panel's five frame-bolt holes, clamped to the bench | **print** + bought clamps | **new — the build** |
| `RIG_Base` | 2020 frame, 400 × 300 | buy extrusion | superseded by `RIG_Stand` |
| `RIG_Column` | 2020 × 480 vertical | buy | superseded by `RIG_Stand` |
| `RIG_Braces` | 2 × 2020 diagonals, 191 + 219 mm | buy | superseded by `RIG_Stand` |
| `RIG_Rail` | **MGN12, 400 mm** + 2 × MGN12H | buy | **[DEFERRED — MODE B]** |
| `RIG_Carriage` | 8 mm PA-CF, 154 × 170 | **print** | **[DEFERRED]** — its five-hole interface moves to `RIG_Stand` |
| `RIG_Index_Post` | 2020 × 405, forward of the motor | buy | **[DEFERRED — MODE B]** |
| `RIG_Index_Bar` | 12.5 mm PA-CF, 17 stations at 10 mm | **print** | **[DEFERRED — MODE B]** |
| `RIG_Mode_Pin` | Ø8 quick-release pin | buy | **[DEFERRED]** — nothing to pin |
| `RIG_Hard_Stops` | 2 × Ø14 PU bumpers | buy | **[DEFERRED — MODE B]** |
| `RIG_Ballast_Pot` × 2 | printed cup, 344 g of shot | **print** + bought shot | **[DEFERRED — MODE B]** |
| `RIG_Knee_Stop_Plate_L` | printed arc, −8° stop + backup | **print** | **keep** — the leg rests on the −8° stop at 8.25 N in every pose |
| `HW_WasherStack_M5` + `RIG_Knee_Bumper_Tube_L` | the +27° hard stop | buy + **print (TPU)** | needed before step 10 only → **[DEFERRED]**, but buy the washers |
| `RIG_Torque_Arm` | 200 mm lever, 12 mm PA-CF | **print** | **keep** — step 2 |
| `RIG_Scale_Pedestal` | 2 × 2020 + shelf | buy | **keep in function**; substitute anything rigid at the right height |
| `RIG_Floor_Plate` | 260 × 60 × 6 | **print** or 6 mm alu | **keep** |
| `RIG_Cable_Post_A/B` | two service-loop anchors | **print** | **keep**, simpler routing |
| `RIG_Knee_Collar_L`, `RIG_Knee_Magnet_Carrier_L` | §2.3 substitutes | **print** | **keep** — knee parts, not fixture |

Reused unchanged: `Proximal_Link_L`, `Wheel_Rim_L`, `Wheel_Tyre_L`,
`Knee_Encoder_Bracket_L`, `Chassis_Shoulder_Plate_L`, the knee bearings, the
cartridge and the spring. Reused **modified**: `Distal_Link_L` (§4). **All of these
are unaffected by the Mode A cut** — every one is a robot part.

---

## 2. Geometry that had to be got right

### 2.1 Rail length — the brief's travel arithmetic is the one-block case

```
two MGN12H at 80 mm centres occupy 45.4 + 80        = 125.4 mm of rail
stroke the experiment needs, about equilibrium:
   highest release station                            +100.0 mm
   peak compression on a 100 mm drop                  − 51.5 mm
                                                      --------
                                                       151.5 mm
   + 12 mm of bumper and crush at each end             175.5 mm

300 mm rail →  174.6 mm block travel → 150.6 usable → SHORT by 0.9 mm
400 mm rail →  274.6 mm block travel → 250.6 usable → OK
```

Travel limits are set by two PU bumpers on the index bar, struck by the
carriage's own pin arm: the shoulder axis is confined to **−85 … +125 mm** about
the modelled position. At both limits the block pair is still fully on the rail
(−147.7 … +187.7 against a rail spanning −180 … +220).

### 2.2 The carriage interface

`Chassis_Shoulder_Plate_L`, measured off the model rather than assumed: a
**120 × 120 × 5** panel (X −72…48, Z −48…72) with a Ø48 central bore, a
Ø64/Ø67 cable-cavity lip standing to y = 51, 8 × Ø3.4 on the Ø74 PCD (the
motor's), 4 × Ø3.4 on a Ø88 PCD (the deleted clock-spring cover's), and
**5 × Ø3.4 frame-bolt holes** at (−60, −18), (−60, 48), (−60, 62), (30, 48),
(30, 62).

Those five are the rig's structural joint — they are what the panel uses to
carry the leg on the real robot, so the rig reproduces the robot's own load path.
Verified in the model: all five carriage insert bores are concentric with the
panel holes, all eight block screws are concentric with the MGN12H taps, and both
mating faces are coincident to **0.000 mm**.

The four Ø88 cover holes are **not** used: any fastener there needs access to the
panel's inboard face, and the carriage is now bolted flat against it. They are
left open as a stiffening option if bench measurement shows the panel is soft.

### 2.3 Moment check, at the as-built overhang

**Mode A first (2026-08-17), because it is the build.** Deleting the rail and the
carriage removes 21.0 mm from the stack, so the stand's outboard face *is* the
motor front mount face:

```
stand outboard face = motor front mount face   y = 42.00
+ Chassis_Shoulder_Plate_L 5.0                 y = 47.00
wheel centre plane                             y = 84.00
                                               --------
Mode A overhang                                  42.00 mm   (67 % of Mode B)
```

| Load | Moment | axis |
|---|---:|---|
| spring-limited wheel force 54.80 N × 42.00 mm | **2.30** | X, pitch |
| **shoulder stall 11 N·m** | **11.00** | **Y, yaw — dominant** |
| its ground reaction 71.3 N × 42.00 mm | **2.99** | Z, roll |
| vector sum of yaw + roll | **11.40** | — |
| proof screen at the hub | **25.00** | Y, yaw |

There is no bearing-block factor of safety to quote because there is no bearing
block: the load goes into a printed part and into the bench clamp. **Yaw dominates
by 4×**, so the stand's job is torsional, not vertical — and it must be **clamped,
not weighted** (11 N·m needs 11.2 kg of stand at 100 mm base half-width, still
3.7 kg at 300 mm, against a ~0.3 kg print). Recompute with
`rig_calc.mode_a_stand()`.

⚠ **This is the number to re-verify in CAD.** If anything lands between the stand
and the motor's front face, the 42.00 mm grows and all four moments scale with it
linearly (brief §4.4 check 6).

**Mode B, [DEFERRED] — retained for the restart.** The stack-up reproduced the
brief exactly:

```
rail mounting plane (column outboard face)   y = 21.00
+ MGN12H block 13.0                          y = 34.00
+ RIG_Carriage 8.0                           y = 42.00
+ Chassis_Shoulder_Plate_L 5.0               y = 47.00
wheel centre plane                           y = 84.00
                                             --------
overhang                                       63.00 mm   (brief §4.1: 63.00)
```

| Load | Moment | axis | fs, 1 block | fs, 2 blocks |
|---|---:|---|---:|---:|
| spring-limited impact 54.8 N × 63 mm | 3.45 | X, pitch | 10.50 | 21.01 |
| shoulder stall 11 N·m | 11.00 | Y, yaw | 3.30 | 6.59 |
| its ground reaction 71.3 N × 63 mm | 4.49 | Z, roll | 8.51 | 17.02 |
| vector sum of the two ⟂-to-rail | 11.53 | — | **3.15** | **6.29** |

Two blocks, as the brief requires. With the clone-rail 30 % derate the two-block
case still sits at **fs 4.40**; one block would be 2.20, below spec. **None of
this is bought in the Mode A build.**

### 2.4 What the GAUGE coupons actually resolve

Measured out of the STLs with `stl_inspect.py`:

| | `GAUGE_Shoulder_Motor_Interface.stl` | `GAUGE_Wheel_Motor_Interface.stl` |
|---|---|---|
| Envelope | Ø78 × **9.5** (y −6 … +3.5) | Ø53 × **33.0** (y −27 … +6) |
| Patterns | 8 × Ø2.5 @ Ø74.000, step 45.00°, first 22.6° ✓ · 6 × Ø2.5 @ Ø25.000, step 60° ✓ · 3 × Ø4.050 @ Ø20.400, step 120° ✓ · Ø12 centre · Ø34 pilot at y +3.0 · output face +3.5 ✓ | 6 × Ø2.0 @ Ø47.500, step 60° ✓ · 3 × Ø2.5 @ Ø27.000, step 120° ✓ · Ø12 centre |
| Agrees with design record §2 | **yes, every feature** | **yes, every feature** |
| Resolves C3 (wheel 26 vs 33) | — | **yes** — it is full length, hold it against the motor |
| Resolves C2 (shoulder 40 vs 44) | **NO** — it stops 3.5 mm past the mount face | — |

**Both coupons are correct and worth printing.** But C2 is not a coupon test: it
needs a caliper across the real motor, which is already test #3 in the brief's
order ("weigh and caliper both motors").

**What C2 actually threatens in this design: nothing structural.** Every rig
interface is referenced to the motor's *front* mount face at y = 42, which is the
datum the coupon does check. A 40 mm motor is 4 mm shorter *behind* that face, so
it changes only how much air sits between the motor's rear and the column — and
that gap is 5 mm of clearance, not a fit. The one thing to re-check on a 40 mm
motor is that the rear housing still clears the MGN12H blocks, which sit at
r ≥ 46.5 against a Ø80 housing: 6.5 mm of margin, and a shorter motor can only
increase it.

---

## 3. Drop series and the force ceiling

> **[DEFERRED — MODE B] as a test programme (2026-08-17).** The Mode A build runs
> no drops, so the table below is not executed. **It is not deleted, for two
> reasons:** the force ceiling in it is what makes Mode A safe to design against a
> flat 54.8 N, and the two-leg build inherits this table as its landing prediction.
> The one Mode-A-live number is the last block of this section: 54.8 N.
>
> Mode A's own force/angle table — known masses on the wheel, which *is* run, as
> step 6 — is in brief §6 and `rig_calc.mode_a_stand()`.

Exact integration of the frozen spring curve, `∫F dx = m·g·(h + x)`, m = 1.6451 kg:

| Drop | Compression | φ_peak | Peak force | |
|---:|---:|---:|---:|---|
| 20 mm | 28.67 | +16.18° | 37.8 N | |
| 30 mm | 35.33 | +19.61° | 42.9 N | bumper engaged |
| 40 mm | 40.90 | +22.43° | 47.3 N | |
| **46.3 mm** | **43.8** | **+24.00°** | **49.8 N** | **the step-10 gate** |
| 49 mm | 45.32 | +24.62° | 50.8 N | past the gate |
| 50.7 mm | 46.08 | +25.00° | 51.4 N | design point |
| **60.0 mm** | **50.14** | **+27.00°** | **54.8 N** | **bottoms on metal** |
| 100 mm | — | +27° | 54.8 N | bottoms out |

**This is the single source for the rig's passive drop limit, and it is a pair of
numbers: 46.3 mm is the computed +24° gate crossing; 45 mm is the planning limit
used everywhere else in this project** (the round number just below the crossing,
so the drop stations in §10 sit inside the gate with margin). The brief's 49 mm is
superseded: the brief's own gate is φ_peak < +24°, and 49 mm exceeds it. The
brief's conclusion is otherwise confirmed and strengthened: a 100 mm free drop
bottoms the knee out, and it does so from 60 mm upward.

Free-standing equilibrium: F = 16.13 N → **φ_eq = −0.84°**, ride height
**210.60 mm** (209.27 at φ = 0). Because equilibrium depends on the spring as
built, the drop stations are given as a Z table, not as fixed drop heights — see
§10.

**Peak force is spring-limited at 54.8 N.** Nothing downstream of the knee can
ever see more, however hard the leg is dropped, because the spring is the softest
element in the load path and it reaches metal at +27°. **This paragraph is live in
Mode A** — it is the reason `RIG_Stand` is designed against 54.80 N of wheel force
(2.30 N·m of pitch at 42 mm) and not against a guessed impact load.

### 3.1 The bounce mode — what step 8 will read

> **[DEFERRED — MODE B].** Step 8 is not run in this build; there is no sprung
> mass to pluck. The prediction below is retained as the model the two-leg build
> will test, and as the reason not to be surprised later: **a pluck reading other
> than 3.67 Hz is not a build error.**

Three models, increasing fidelity, at the measured masses:

| Model | m_eff | f |
|---|---:|---:|
| whole slide on the spring | 1.61 kg | 3.37 Hz |
| sprung mass only, wheel grounded | 1.05 kg | 4.16 Hz |
| **full Lagrangian, rigid contact, rolling wheel** | **1.49 kg** | **3.49 Hz** |

With a 388 g motor the Lagrangian figure is **3.63 Hz**. The shank rotates about
the contact patch and the wheel rolls, so part of the unsprung mass *does* ride
the mode through its rotational inertia — which pulls the answer back down from
4.2 Hz and lands it inside the brief's 3–4 Hz gate after all.

So: **predict 3.5–3.65 Hz.** The brief is right that the 1-DOF identity behind
"3.67 Hz exactly" is invalid, but the correct answer happens to land in the same
place, and the step-8 gate does not need widening. A tangent rate of 719.7 N/m at
equilibrium is the number to compare against step 6's measurement.

---

## 4. Recommendation on §2.3 — delete the double-D flats

**Adopt it, in a modified form. Implemented in the model.**

### The proposal's premise is incomplete

`beni_rig_no_machining.md` §2.3 says the flats' "only job is to key the axle to
the sleeve so they rotate together". They have a second job that is not stated:
the distal tongue is **buried between the two proximal arms** (arm A y 58.7…64.5,
channel 64.5…84.5, arm B 84.5…90.3), so the axle is the *only* load path from the
distal link out to the magnet at y 96.3. **The key also carries the absolute
encoder's angular reference** — the rig's primary instrument. Delete the key
without replacing that reference and the encoder stops tracking the knee.

### What to build instead

| Item | Decision |
|---|---|
| Axle | **Hardened Ø10 h6 ground dowel pin, 35 mm.** NOT a shoulder bolt: a shoulder screw's shoulder is h9/h11, which rattles in the 6800's Ø10 bore, and knee-angle noise is measurement error on this rig. A ground dowel holds the fit for ~$2. |
| Sleeve | **Deleted.** Its Ø16 bore becomes **Ø10 printed directly into the distal boss** — a light press, which is the same fit class the sleeve itself used. |
| Angular reference | The press of the pin into the printed boss. Torque to be carried is two 6800 seals' drag, order **0.002 N·m**; a light press on Ø10 × 21.6 holds ~100× that. |
| Retention | `RIG_Knee_Collar_L`, printed, Ø15 × 3, M3 set screw + retaining compound, replacing the axle's Ø15 flange. |
| Magnet | `RIG_Knee_Magnet_Carrier_L`, printed, Ø10 bore 3.5 deep pressed on the pin's 3.4 mm protrusion, Ø6.1 pocket 2.5 deep. The magnet **bottoms on the pin's own ground end face** — the best datum available. |

### Arithmetic

```
bearing pressure on the printed distal boss, 275 N proof over 21.6 mm:
   Ø16 steel sleeve, as designed        0.80 MPa
   Ø10 pin direct in printed PA-CF      1.27 MPa      against 84 MPa XY
Ø10 pin in bending, 275 N at 6.4 mm     18 MPa
pin length: Ø10 × 35 from y 58.7 → 93.7, 3.4 mm proud of arm B at 90.3
            carrier bore needs 3.5, magnet pocket 2.5 → fits in 6.0 mm
```

Kinematics after the change were re-verified: the knee sweep still reproduces
guide §4 to **0.043 mm** worst case.

### What it costs

- **`Distal_Link_L` is no longer "reuse as-is"** and must be re-printed. Its
  volume goes 45.0 → 47.6 cm³, exactly the 2646 mm³ of the printed-in sleeve.
- Deletes **two** machined families (`Knee_Axle_L`, `Knee_Sleeve_L`), converts
  `Knee_Magnet_Carrier_L` from steel to printed, and buys one dowel pin.
- **Saves 26.4 g on the slide**, which matters given §5.
- The 0.05 TIR concentricity callout now lands in a printed part. **Measure it on
  an indicator; if it exceeds ~0.1 mm, bond the magnet into the pocket using the
  Ø10 bore as the datum** rather than trusting the printed step.

**Keep the keyed version on the shelf for the two-leg build.** Nothing here
argues against it; the rig simply cannot have it without a machine shop.

---

## 5. Mass properties

> **Mode A (2026-08-17).** The slide roll-up below is **[DEFERRED — MODE B]**:
> there is no slide, no block, no carriage and no ballast to weigh, and no 1.645 kg
> target to hit. **The Mode A load report replaces it** — the stand carries a
> *static hanging* load, not a sprung mass:
>
> | Mode A | kg | N |
> |---|---:|---:|
> | one leg: thigh + shank + wheel | 0.8382 | 8.22 |
> | + GIM6010-8 at 388 g (C4 optimistic) | 1.2262 | 12.03 |
> | + GIM6010-8 at 500 g (C4 pessimistic) | 1.3382 | 13.12 |
>
> That is **3 % of the 11.00 N·m yaw** the stand is actually sized by (§2.3), which
> is why **C4 stops being a rig-design risk in Mode A** — the 112 g spread changes
> nothing structural. Weigh the motors anyway; the two-leg mass budget still turns
> on it. Source: `rig_calc.mode_a_stand()`.
>
> The per-part masses in the table below remain the authoritative part weights.

Measured off the built assembly, materials assigned, **not estimated**. The model
carries the pessimistic C4 figure of 500 g for the GIM6010-8.

| On the slide | g |
|---|---:|
| REF_GIM6010-8 (C4: 388–500, model uses 500) | 500.0 |
| REF_GIM4305-10 wheel motor | 250.0 |
| 2 × MGN12H block | 108.0 |
| `RIG_Carriage` | 103.7 |
| `Wheel_Tyre_L` 80.1 · `Wheel_Rim_L` 77.2 | 157.3 |
| `Proximal_Link_L` 72.5 · `Distal_Link_L` 54.8 | 127.3 |
| `Shoulder_Output_Hub_L` | 58.5 |
| `Chassis_Shoulder_Plate_L` | 46.3 |
| `Wheel_Hub_L` 35.6 · knee + cartridge + fasteners | ~232.8 |
| 2 × `RIG_Ballast_Pot` shell (empty) | 31.8 |
| `RIG_Knee_Stop_Plate_L` 2.9 · `HW_WasherStack_M5` 7.3 · TPU tube 1.1 | 11.3 |
| **Bare slide, empty pots, no mode pin** | **1607.6** |

| | g |
|---|---:|
| Target, half of 3.2901 kg | 1645.1 |
| **Shot to reach it, 500 g motor** | **+37.5** |
| **Shot to reach it, 388 g motor** | **+149.5** |

**It fits — but only just.** With a 500 g motor there is 38 g of headroom; the
brief's warning that the rig might exceed 1.645 kg with zero ballast was very
nearly right. Deleting the steel arc stop gave back 19 g, which is most of what
the printed pots cost.

**The 1.2 kg run in the brief is not achievable.** The bare slide is 1607.6 g and
there is nothing left to remove. Runs of 1.645 and 2.0 kg are.

### Sprung / unsprung

| | g | % |
|---|---:|---:|
| Sprung — carriage, motor, panel, hub, thigh | **1051.1** | 65.4 |
| Unsprung — shank, wheel motor, wheel | **556.5** | **34.6** |

**The sprung mass is the number that matters.** The real robot's per-leg sprung
mass is (3290.1 − 2 × 618.4) / 2 = **1026.7 g**; the rig sits at 1051.1 g with
empty pots, 2.4 % high, and lands on it once the shot goes in the pots (which are
above the spring). The match is structural rather than lucky: the leg and the
target total come from the same frozen mass roll-up. That is why the bounce-mode
prediction in §3.1 transfers to the robot.

(`sim/beni_inertia.json` splits shank + wheel at 618.4 g; Fusion's
classification puts 556.5 g below the spring. The 62 g difference is knee
hardware that the URDF assigns to the shank link and the rig assigns to the
proximal side. Use 556.5 g for the rig's own dynamics.)

### Ballast provision — printed pots, off-the-shelf fill

`RIG_Ballast_Pot` × 2 — printed PA-CF cups on the carriage's inboard face,
r 40…66, 70° of arc, 30 mm deep, 2 mm walls, **15.9 g of shell each**, bolted to
two of the four existing M4 stud positions. Between them they hold **73.2 cm³**,
which is **≈344 g of steel shot** at a realistic 4.7 g/cm³ packed density.

Fill with whatever dense granulate is to hand — steel shot, airgun BBs, a jar of
M4 nuts, lead-free shot — and set the mass on a kitchen scale. That gives about
**1 g of granularity** instead of the 32.8 g steps a cut steel plate gave, which
matters because the trim needed is only 36.6 g.

The pots span |X| ≤ 37.9, so they pass between the column (X ≤ −50) and the index
post (X ≥ 40) and can run inboard past the rail plane to y = 4 without fouling
anything, including the motor's Ø57 driver cover (they start at r = 40).

| Run | Fill needed | |
|---|---:|---|
| **1.645 kg, 500 g motor** | **+37.5 g** | ~8 cm³, a spoonful |
| 1.645 kg, 388 g motor | +149.5 g | 32 cm³ |
| 2.0 kg | +392.4 g | 84 cm³ — **48 g over the 344 g capacity**, so deepen the pots or add M12 washers on the spare two studs |
| 1.2 kg | −408 g | **not achievable** |

Ballast sits *inboard* of the carriage, between the leg and the rail, so adding
it reduces the overhang moment rather than increasing it.

---

## 6. The §4.4 checks

All six run from `rig_lib.checks_44()`.

> **Mode A (2026-08-17).** These six checks were run and passed against the
> two-mode assembly and stay on the record. For the Mode A stand, brief §4.4 is
> re-scoped to **four checks plus a new hold-down check**, and the mapping is:
>
> | Was | Mode A |
> |---|---|
> | 1 knee sweep | **unchanged, and still the first thing to reproduce** |
> | 2 shoulder ±120° service loop | **unchanged in intent**; the obstacle list is now the stand and the wheel, no rail/column/carriage |
> | 3 wheel clears floor through Mode B travel | **replaced** by: wheel clears the floor at every knee angle −8°…+27° with the stand at its designed height. The coupling below is what makes that check trivial in Mode A — the wheel is *on* the floor and the stand does not move |
> | 4 sprung/unsprung mass | **[DEFERRED — MODE B]**; do the §5 Mode A load report instead |
> | 5 torque arm cannot hit the column | **unchanged in intent** — cannot hit the *stand*. Re-run it, the Y bands are different |
> | 6 re-verify the 63 mm stack-up | **replaced** by: verify the **42.00 mm** Mode A overhang (§2.3) |
> | — | **new 7: prove the hold-down.** 11.00 N·m of yaw cannot be resisted by dead weight; the CAD must show the clamp or bench-bolt path |
>
> `rig_lib.check3_mode_b_travel()` and the `slide_to()` harness it uses have no
> Mode A equivalent and are **[DEFERRED]**.

| # | Check | Result |
|---|---|---|
| 1 | Knee sweep −8 → +27 reproduces guide §4 | **PASS** — worst deviation **0.043 mm**; +25° gives 46.08 vertical / 23.99 fore-aft against 46.1 / 24.0 |
| 2 | Shoulder ±120°, service loop clear of rail, column, carriage, wheel | **PASS** — 17 angles at 15° steps, **zero** clashes |
| 3 | Wheel clears the floor through the whole Mode B travel | **PASS** — see below. **[DEFERRED — MODE B]** |
| 4 | Mass properties incl. sprung/unsprung | **done**, §5. **[DEFERRED — MODE B]** |
| 5 | Torque arm cannot hit the column | **PASS** — Y bands disjoint by 38.5 mm, so it cannot at *any* angle. **Re-run against the stand** |
| 6 | Re-verify the 63 mm stack-up | **PASS** — 63.00 mm, matches. **Mode A: verify 42.00 mm instead** |

**Check 3 needs stating properly, because dz and φ are not independent.** In
Mode B the wheel stays on the floor, so the carriage height and the knee angle
are coupled by the contact condition. Along that path:

| φ | carriage dz | wheel bottom vs floor | clashes |
|---:|---:|---:|---:|
| −8° | +12.04 | 0.000 | 0 |
| 0° | 0.00 | 0.000 | 0 |
| +10° | −17.13 | 0.000 | 0 |
| +20° | −36.09 | 0.000 | 0 |
| +25° | −46.08 | 0.000 | 0 |
| +27° | −50.14 | 0.000 | 0 |

and airborne on a station, knee at its −8° stop: the wheel **lifts off at
dz > +12.04 mm**, so every station from 20 mm up starts with the wheel clear
(7.96 mm at 20, 112.96 mm at the top bumper), zero clashes throughout.

**Check 5, in full.** The arm cannot reach the column at any angle because their
Y bands are disjoint (arm 59.5…71.5, column 1…21). Its maximum radius is
200.4 mm against 209.3 mm to the floor, so it clears the floor at every angle by
8.9 mm. It reaches the scale shelf **8.6° below horizontal**, which is the
intended bearing contact — and staying within ±8° of horizontal also keeps the
cos(α) error on the 200 mm arm under 1 %.

### 6.1 Interference: one clash, and it is intentional

`RIG_Torque_Arm ↔ Proximal_Link_L`, 14 635 mm³. **The torque arm replaces the
proximal link** on the hub's 6 × M4 Ø44 PCD — step 2 runs with the leg off. It
and `RIG_Scale_Pedestal` are hidden in the assembled state and excluded from the
sweeps as step-2 fixtures.

> **Re-measured 2026-08-17 on the Mode A assembly.** Still one real clash, still
> 14 634.62 mm³, still that pair — **but only after fixing three things this
> section had silently been passing over.** `real_clashes()` was reporting five,
> and the four extra were artifacts of the model, not of the design:
>
> 1. **Six post-§2.3/§13 parts were being posed as `STATIC`.** `beni_lib.classify()`
>    knows the *original* leg part names and falls through to `'STATIC'` for
>    anything else, so `RIG_Knee_Stop_Plate_L`, `HW_DowelPin_D10x35`,
>    `RIG_Knee_Collar_L`, `RIG_Knee_Magnet_Carrier_L`, `HW_WasherStack_M5` and
>    `RIG_Knee_Bumper_Tube_L` stayed frozen at θ = 0 / φ = 0 while the leg swept
>    around them. The leg then swept **through** them: 5 of the 17 check-2 angles
>    and 5 of the 6 check-3 knee angles reported clashes up to 634 mm³ between the
>    wheel and knee-area parts that cannot physically touch. Nothing had re-run
>    check 2 after those parts were added. Fixed by `rig_lib.register_pose_classes()`
>    — each replacement inherits the class of the part it replaced.
> 2. **`Cart_Lower_Eye_L ↔ RIG_Knee_Bumper_Tube_L` is a designed crush volume**,
>    the §8 compression column's TPU tube bearing on the lower spring seat. It
>    reproduces `rig_lib.stop_stack_sizes()` to the digit — **0.00 mm³ at +20°,
>    122.99 at +25°, 173.46 at the +27° stop**, against a designed 3.7593 mm of
>    crush on a 46.14 mm² annulus = 173.46 mm³. Now in `ARTIFACT_PAIRS`, and the
>    same kind of independent confirmation the PU-bumper volumes give for §10.1.
> 3. See §6.2 trap 5 — the transform guard was incomplete.

The pedestal genuinely cannot coexist with the leg: it must stand at X = −200 to
sit under the arm's nose, and that is inside the leg's own 209 mm swept radius.
**With the pedestal fitted, keep the shoulder within −120…+25°** (measured: clean
at +25°, clashes at +30°).

Everything else that the analysis reports is a documented artifact, and
`rig_lib.real_clashes()` classifies each one: screw shanks inside their own
modelled tap drills, the motor's three Ø4 output pins rotating with the hub
(design record §11), and the knee stop dowel crushing its PU bumpers — the last
of which reproduces design record §10.1 **exactly** (1.4 mm³ at −8°, 8.6 at +25°,
12.7 at the +27° stop), which is a useful independent confirmation that the
bumpers still engage where they were designed to after the §2.3 rebuild.

### 6.2 Five measurement traps found while checking

Recorded because each one silently produced a *passing* result that was wrong,
which is the failure mode this project's design record keeps warning about.

1. **`beni_lib.interference()` reports unresolvable names.** It falls back to
   `entity.name`, which for any body built without renaming is `"Body1"`. Every
   rig clash therefore came back as `Body1 ↔ Body2`, a filter on `'RIG_'` matched
   nothing, and the first four builds reported **zero interference when there
   were 49 pairs** — including a 11 313 mm³ brace-through-post collision.
   `rig_lib.occ_name()` resolves through `assemblyContext`, then
   `parentComponent` for external references.
2. **Fusion's occurrence bounding box inflates under rotation.** It is the
   axis-aligned box of the *untransformed* box, so at φ = +25° the Ø110 tyre
   reports as **146.2 mm** tall (110 × (cos 25 + sin 25)). Any clearance read off
   `bbox` min/max for a rotated part is overstated by up to a third. The box
   *centre* transforms exactly, so `wheel_bottom()` takes centre − 55.
3. **`Sketch.saveAsDXF` after `projectCutEdges` mirrored the hole pattern.** It
   wrote the plate outline at (+X, −Z) and the three M3 holes at (−X, −Z) — 183 mm
   apart. That bit while the stop arc was still a laser part; it no longer affects
   any deliverable, but it is recorded because Fusion's DXF export cannot be
   trusted without an independent area check (see `archive/laser/`).
4. **The spring cartridge's internal length is 9.0 mm shorter than its own
   dimension chain implies** (§8). Deriving it instead of measuring it would have
   put the knee's hard stop at +10°.
5. **Deleting *any* occurrence displaces both motor references.** Removing one
   stray M3 screw re-resolved the two external STEP references: `REF_GIM6010-8`
   grew from Y 5…49 to Y 5…75 and the wheel motor moved 140 mm, inventing clashes
   that had nothing to do with the design. This is the hazard `beni_prototype1_`
   `design_record.md` §12 warns about, reached by a different route, and it is
   **reproducible** in `Beni_SingleLegRig` — it fired twice on the same delete.

   Two dead ends worth recording. `occurrence.isSuppressed = True` is **not** a
   fix: that property is not readable on this API build, so the assignment lands
   silently on the Python wrapper and changes nothing in the model — it looked
   like it had worked. And `beni_lib.build_fasteners()` deletes its own origin
   master occurrences the same way, so the operation is house style and cannot
   simply be banned.

   **What works:** capture `transform2.asArray()` for both `REF_*` occurrences
   *and every child occurrence in their trees* (7 transforms), do the delete, then
   write the transforms back and assert the bounding boxes match. Undo also
   recovers it cleanly if you catch it. **Re-check the two REF bounding boxes
   after any structural edit** — `REF_GIM6010-8` must read Y 5.00…49.00 and
   `REF_GIM4305-10` Y 61.50…94.50.

   > ⚠ **[AMENDED 2026-08-17 — the 7-transform recipe above is INCOMPLETE, and
   > the bounding-box guard passes anyway.]** Stripping the Mode B occurrences
   > displaced 2 of those 7 exactly as documented — **and also reset
   > `HW_WasherStack_M5` and `RIG_Knee_Bumper_Tube_L` to identity**, which dropped
   > both into the shoulder motor at the origin and invented four clashes totalling
   > 430 mm³. Both REF boxes read correct throughout, so this is one more trap that
   > produces a *passing* wrong answer.
   >
   > The distinction that predicts which occurrences are at risk: those two are the
   > only parts positioned by assigning `occ.transform2` to an occurrence created
   > by `addNewComponent(identity)` (`rig_lib._place_on_cart`). Every screw, which
   > `place()` creates with `addExistingComponent(component, matrix)`, survived —
   > 18 of 20 spot checks unchanged to 0.05 mm. **So capture every occurrence, not
   > just the REF trees:** `rig_lib.xf_capture()` / `xf_restore()`, then
   > `ref_assert()` *and* `placed_assert()`.
   >
   > ⚠ And it is not only deletes you have to guard. **`beni_lib._spring_body()`
   > and `beni_lib.apply_materials()` both trigger it**, and `_spring_body` is
   > called by `rig_set_pose()` — so *every pose in every sweep* used to drop the
   > two cartridge stop parts into the motor, in the one place a real knee-stop
   > clash would show up. `rig_set_pose()` now guards and re-places them, and
   > `checks_44()` repairs and asserts before the first pose.

---

## 7. Printed parts

Full table and settings in `rig_stl/README.md`. Orientation is the strength
lever, not infill: **5 walls · 40 % gyroid · 0.15 mm layers · top-of-range temp ·
minimal cooling · dried filament**, per `beni_rig_no_machining.md` §1.

| Part | cm³ | g | Orientation |
|---|---:|---:|---|
| `RIG_Stand` | 499.3 | 574.2 | **mount face (y = 42.00) flat on the bed, building inboard** — every layer is then an XZ slice, so the dominant 11.00 N·m of shoulder yaw (a couple lying *in* the XZ plane) stays in the print plane at 84–102 MPa instead of across the layers at 26–50. Y thickness only decreases away from the bed, so no support. ⚠ 200 × 32 × 299.3 needs a bed ≥ 300 mm |
| `RIG_Carriage` | 90.2 | 103.7 | plate face flat on the bed |
| `RIG_Index_Bar` | 114.3 | 131.4 | flat, station holes vertical |
| `RIG_Torque_Arm` | 93.6 | 107.6 | flat, arm plane on the bed |
| `RIG_Floor_Plate` | 93.6 | 107.6 | flat |
| `RIG_Cable_Post_A` | 4.0 | 4.6 | flat, sector face down |
| `RIG_Cable_Post_B` | 9.4 | 10.8 | flat |
| `RIG_Knee_Collar_L` | 0.3 | 0.3 | bore axis vertical |
| `RIG_Knee_Magnet_Carrier_L` | 0.7 | 0.8 | bore axis vertical — this holds the encoder TIR |
| `Shoulder_Output_Hub_L` | 20.8 | 58.5 | **flange flat on the bed**, so the dowel holes shear across layers |
| `Wheel_Hub_L` | 12.7 | 35.6 | flat, register face up |
| `Cart_Upper_Eye_L` / `Cart_Lower_Eye_L` | 5.3 / 6.0 | 14.8 / 16.9 | **pivot bore axis vertical** |
| `RIG_Knee_Stop_Plate_L` | 2.5 | 2.9 | flat on the bed |
| `RIG_Knee_Bumper_Tube_L` | 0.9 | 1.1 | **TPU 95A**, bore axis vertical |
| `RIG_Ballast_Pot` × 2 | 13.8 | 15.9 ea | open side up, no support |
| `Distal_Link_L` | 47.6 | 54.8 | on edge, link axis vertical — **re-exported, §4** |

Two printed parts carry consequences the brief already flagged:

- **`Shoulder_Output_Hub_L` needs its three Ø4 × 10 hardened dowel pins.** The
  printed register alone sees 63 MPa at the 25 N·m proof load against PA-CF's
  ~40–50 MPa shear. The pins are not optional. The former Ø3.9-and-ream route
  is retired because machining is prohibited; PA-CF structural release waits
  for an as-printed bore coupon that gives a true press fit to the bought pins.
  If no bore works, revise the printed retention geometry rather than drilling
  or reaming the hub.
- **`Wheel_Hub_L` needs a steel washer under every screw head**, and the
  re-torque schedule: after the first hour, then every ~10 hours. Its 20.7 N·m
  friction capacity is a preload joint in plastic, and preload in plastic creeps.

---

## 8. The knee hard stop, without a laser

`Knee_Stop_Arc_L` is deleted. This is the one place where "no laser-cut parts"
has a real engineering consequence, so here is the whole reasoning.

### Why the steel plate could not just be printed or substituted

The plate worked because its slot ends are **conformal**: a 3.1 mm *concave*
radius bearing on the Ø6 dowel, which is very nearly line-on-line. At the 534 N
crash load that is about **257 MPa** of Hertzian contact — comfortable for
hardened steel.

Nothing printed or off-the-shelf reproduces a concave 3.1 mm steel face, and
every convex substitute reverts to line contact:

| Substitute | Contact length | p_max |
|---|---:|---:|
| Ø6 dowel on a Ø6 pin | 3.2 mm | **2021 MPa** |
| Ø6 dowel on a Ø10 pin | 3.2 mm | **1808 MPa** |
| Ø6 dowel on a Ø10 pin | 10 mm | 1023 MPa |
| Ø6 dowel on a printed slot end | 3.2 mm | plastic yields locally |

The 10 mm case is the only tolerable stress, and it is not buildable: it needs
the dowel cantilevered 8.3 mm out of a 5 mm press in PA-CF, and the moment alone
puts **177 MPa** of bearing into an 84 MPa wall.

### So the stop moves into the spring cartridge

The +27° stop becomes a **compression column on the guide rod, inside the
spring** — which has no contact-stress problem at all, because the load is
carried as a short steel column through the cartridge's own, already-verified
load path: seat spigots → printed eyes → Ø4 pivot pins, which the spring already
loads to 203 N continuously.

```
clear axial space on the rod, between the two spring seats
   at +20 deg    20.330 mm      <- TPU tube first touches here
   at +27 deg    16.571 mm      <- steel goes solid here
                 --------
   window         3.759 mm
```

| Element | Spec | Why |
|---|---|---|
| `HW_WasherStack_M5` | **16.571 mm** of M5 plain washers (Ø10/Ø5.3 × 1.0), trimmed with DIN 988 M5 shim washers | The metal stop. 9.5 MPa in the steel; 9.9 MPa bearing on the printed spigot face |
| `RIG_Knee_Bumper_Tube_L` | printed **TPU 95A**, Ø13.0/Ø10.5 × **20.330 mm** | The progressive bumper. Crushes 3.759 mm = 18 % at the stop |

**The two act in parallel, not in series** — the TPU tube is a sleeve *around*
the washer stack, both bearing on the same two seat faces. Stacking them end to
end was the first thing I built and it is wrong: the steel can then never go
solid, and the "hard stop" is only as hard as a crushed elastomer. The original
design did the same thing a different way, by putting the PU in a separate slot
*level* from the metal slot end.

Verified in the model, by sweeping the knee and measuring the real gaps:

| φ | steel gap | TPU gap | |
|---:|---:|---:|---|
| 0° | 13.303 | 9.543 | free |
| +18° | 4.796 | 1.037 | free |
| **+20°** | 3.759 | **0.000** | **TPU in contact, steel still clear** |
| +25° | 1.094 | 0.000 | crushing |
| **+27°** | **0.000** | 0.000 | **steel solid — hard stop** |

One 1.0 mm washer moves the stop by **1.83°**, so the stack is bulked out with
1.0 mm washers and trimmed with 0.2/0.3/0.5 mm shim washers. **Set it after step
6**, from the measured spring — which is the right sequencing anyway, because
steps 1–9 never approach +27° and the brief already says the rig can start
without a stop fitted.

### A measurement that would have wrecked this

The clear space is **not** what the dead-length build-up says. Measured with a
probe ring at six knee angles:

```
clear space  =  cart_len(phi) - 44.570        spread over six poses: 0.0000 mm
build-up predicts  11.00 + 14.57 + 4.0 + 6.0  = 35.57 mm consumed
the solid actually consumes                     44.570 mm
```

That is a **9.0 mm** error. Sizing the washer stack from the build-up would have
put the hard stop at **+10°** instead of +27° — the knee would have hit metal in
normal operation, on the first spring-characterisation run. Anything fitted inside
that spring has to be measured, not derived.

### What the printed plate still does

`RIG_Knee_Stop_Plate_L` — printed PA-CF, 3 mm, same annular sector as the steel
part (r 11 → 35.5, 200.345° → 302.000°), bolting to the **same three existing M3
inserts** in the proximal arm-B boss with the same M3 × 6. It keeps two jobs:

- **the −8° extension stop.** This carries only the spring's own 30 N preload
  (75 N with a 2.5× impact factor) and the slot end is a printed *conformal*
  3.1 mm radius, so it is **3.9 MPa** on an 84 MPa wall. Verified: the dowel is
  free to −8.0° and arrested at −9°.
- **a +28° flexion backup**, one degree past the cartridge stop, so the knee is
  never completely unrestrained. Verified free to +28.0°, arrested at +29°. It is
  a backup only: at the full 534 N it would mark, and it exists to catch a
  missing or mis-shimmed washer stack, not to be the working stop.

`HW_DowelPin_D6x9` is retained unchanged as the moving element.

### What this costs

- The working hard stop is now **inside the cartridge and not inspectable**
  without pulling one clevis pin and opening the cartridge. The original could be
  eyeballed. Add a cartridge strip to the periodic re-torque routine.
- The stop angle depends on the printed eyes' achieved dead length, so it must be
  **set by measurement, not by drawing** — see the 9.0 mm finding above.
- The stop reacts through two printed spigot faces at 9.9 MPa rather than through
  a hardened slot end. That is a factor of 8 below the material, but it is plastic
  in the final crash path where there used to be steel. If the drop series ever
  runs past the +24° gate repeatedly, inspect the spigot faces for bedding-in.

## 9. Purchase list

**This is the rig's *mechanical* half only.** The electronics half is
`electronics/07_bom.md` **Wave 0**. The two lists together are the complete rig
shopping list.

> **Mode A (2026-08-17) — what you no longer buy.** The two sections immediately
> below, **Linear motion** and **Extrusion**, are **[DEFERRED — MODE B] in full**:
> no MGN12 rail, no blocks, no rail screws or T-nuts, no block screws, no 2020
> extrusion, no corner brackets, no index post. Also deleted from the hardware
> table: the **Ø8 quick-release pin**, both **Ø14 PU bumpers**, the **~150 g of
> steel shot**, the **20 M12 ballast washers**, the **4 M4 threaded studs**, and
> **4 of the 10 M4 inserts** (the ballast studs; the 6 hub-root ones stay).
> **Still buy the bench clamps** — the stand needs them more than the base did, and
> for a different reason (11.00 N·m of yaw, §2.3, not walking under drop loads).
>
> Everything else stands, because everything else is the leg. Note especially:
> **keep the 20 M5 plain washers and the shim washers.** The +27° stack they build
> is deferred with step 10, but they cost a few dollars and `RIG_Knee_Stop_Plate_L`'s
> −8° stop is a different part — do not conflate them.
>
> Electronics deletions for Mode A (brake resistor, comparator, MOSFET, diode,
> divider, heatsink): `electronics/07_bom.md` Wave 0.

### Linear motion
**[DEFERRED — MODE B]. Nothing in this table is bought for the Mode A build.**

| Item | Qty | Note |
|---|---:|---|
| MGN12 rail, **400 mm** | 1 | **not 300 mm** — §2.1 |
| MGN12H block | **2** | §2.3; one block is fs 2.20 derated |
| M3 × 8 SHCS + M3 T-nuts, for the rail | 16 + 16 | 25 mm pitch, 10 mm end margin |
| **M3 × 8** SHCS, carriage → block | 8 | **≤ plate + 3.0 mm.** 3.2 mm counterbore gives 3.2 mm engagement in a 3.5 mm thread |

### Extrusion (2020, ~2.9 m plus the pedestal)
**[DEFERRED — MODE B]** except the bench clamps and, if you want it, the pedestal.
The stand is printed; the scale pedestal for step 2 can be any rigid object at the
right height.

| Cut | Qty |
|---|---:|
| 400 mm (base, along X) | 2 |
| 260 mm (base cross members) | 6 |
| 480 mm (column) | 1 |
| 405 mm (index post) | 1 |
| 219 / 191 mm (braces, 45° both ends) | 1 each |
| 167 mm (scale pedestal) | 2 |
| Corner brackets, T-nuts, M5 × 10 | ~40 sets |
| **Bench clamps** | 2 | **KEEP — Mode A needs these.** The brief is right that it walks otherwise, and the stand additionally cannot be held by dead weight at all (§2.3) |

### Fasteners and hardware
| Item | Qty | Note |
|---|---:|---|
| **M3 × 8** SHCS, motor housing → panel | 8 | **NOT M3 × 10** — the thread is 4.0 mm deep in a 5 mm panel; ×10 bottoms out. Departure 7 |
| M3 × 16 SHCS, cable post A + panel + motor | 2 | replaces two of the eight above |
| M3 brass heat-set inserts, 5.0 long | 10 | 5 carriage, spares |
| M4 heat-set inserts, **5.8 long** | 6 + ~~4~~ | hub root joint ~~+ ballast studs~~; an 8 mm insert breaks through the 8 mm flange. **Mode A: 6 only** |
| M4 threaded stud, 30 mm | ~~4~~ | ballast. **[DEFERRED — MODE B]** |
| **Ø4 × 10 hardened dowel pin** | 3 | the output hub's register. Not optional |
| **Ø10 h6 hardened ground dowel, 35 mm** | 1 | knee axle, §4 |
| Ø6 × 9 hardened dowel, h6 | 1 | knee stop, moving element |
| **M5 plain washer**, Ø10/Ø5.3 × 1.0 | 20 | the +27° hard-stop stack, §8 |
| **M5 shim washer** DIN 988, 0.2 / 0.3 / 0.5 mm | 10 ea | trimming the stack to 16.571 mm |
| Ø5 hardened ground shaft, cut 50 mm | 1 | cartridge guide rod |
| Ø8 quick-release pin, 20 mm grip | ~~1~~ | mode pin / drop release. **[DEFERRED — MODE B]** |
| Ø19/Ø13.6 × 0.5 shim washers | 8 + 8 | cartridge preload |
| M3 steel washers | 6 | under every wheel-hub head |
| M12 washers (~7 g) | ~~20~~ | ballast trim. **[DEFERRED — MODE B]** |
| 6800-2RS bearing | 2 | |
| Ø4 × 32 clevis pin + E-clip DIN 6799-4 | 2 | |
| Ø6 × 2.5 diametric NdFeB magnet | 1 | **the AS5048A adapter kit already bundles an AS5000-MD6H-2 diametric magnet** — check the kit before buying this separately. A plain axial fridge magnet does **not** work; it must be diametrically magnetised |
| PU bumper, Ø14 | ~~2~~ | rail travel stops. **[DEFERRED — MODE B]** |
| **Steel shot / airgun BBs / M4 nuts** | ~~~150 g~~ | ballast fill, §5. **[DEFERRED — MODE B]** |
| Main spring, Ø19 × 2.6 × 55, chrome-silicon A877 | 1 | 10.45 N/mm ±5 %. **A228 music wire is acceptable for early prototypes** — A877 is required only for high-cycle fatigue life |

### Nothing to laser-cut and nothing to machine
Every part is printed or bought. The retired steel-arc DXFs are under
`archive/laser/` if the two-leg build wants them.

### Instruments
5 kg kitchen scale · dial indicator (the 0.05 TIR on the printed magnet carrier)
· pin gauges · milliohm meter · feeler gauges. ~~**The kitchen scale is also how
the ballast is set** — weigh the shot into the pots.~~ **Mode A: the scale is for
the torque arm (step 2) and for weighing the known masses in step 6.** Add
**calibrated masses up to ~5 kg** for step 6 — anything whose weight you know:
water bottles on a kitchen scale will do, and 5.0 kg reaches +23.53°, just under
the +27° stop. **Do not exceed it** (§3's ceiling).

---

## 10. Drop stations

> **[DEFERRED — MODE B] in full (2026-08-17).** There is no index bar, no drop
> release and no carriage, so there are no stations. Retained because the *method*
> below is the one the two-leg build must use, and because its reasoning is a live
> warning for Mode A's step 6: **equilibrium depends on F₀ and k as built, so
> nothing may be indexed off the spec spring.**

17 stations at 10 mm pitch in `RIG_Index_Bar`, Z = **−50 … +110**, all on
X = 66. The carriage's single Ø8.05 hole sits at (66, 10) at the modelled
position.

**Stations are given as Z, not as drop heights, on purpose.** Drop height is
measured from free-standing equilibrium, and equilibrium depends on F₀ and k as
built — which is exactly what step 6 measures and what the brief says not to
trust from the spec. After step 6:

```
drop height h at station Z  =  Z − 10 − (measured equilibrium offset)
```

At the spec spring (F₀ giving φ_eq = −0.84°, equilibrium 1.33 mm above the
modelled position), station Z = +11.33 is h = 0 and each station up is +10 mm.
**Stop at h ≈ 45 mm** until the landing controller is live — the planning limit
just inside the +24° gate, which is computed to be crossed at 46.3 mm (§3).

---

## 11. What this rig cannot test

- **Balance and pitch dynamics.** One leg on a ~~vertical slide~~ **fixed stand**
  has no free body and no pitch degree of freedom.
- **Jumping.** Takeoff needs both legs and a body that can leave the ground.
- **Yaw.** No second wheel, no differential.
- **The two-leg scissor stance.**
- **The clock spring.** Deleted for this build (brief §2.4): the harness routes
  externally through the hub's existing Ø6.0 port at r = 21.0 with a loose
  service loop, and the rig is limited to ±120° in software. **The clock spring
  therefore gets no validation here.** It remains the highest-risk mechanical
  item in the project and it moves to the two-leg build, still carrying its
  CR-2 / 500 mm / 5 % wrap-margin design unproven.
- **Anything about the right leg.** Deleted.
- **Absolute spring rate against the spec.** The rig measures F₀ and k as built;
  it cannot tell you the spec was achievable.

**Added by the Mode A decision, 2026-08-17 — four more, and this list now has two
items on it as serious as the clock spring:**

- **The leg bounce mode and the sprung/unsprung split.** No sprung mass, no pluck
  test (steps 8, §3.1). The 3.49–3.63 Hz prediction reaches the two-leg build
  unmeasured.
- **Active shoulder damping.** Step 9 needs something to damp. The ζ → 0.3 target
  is untested.
- **The φ_peak vs drop-height curve, and therefore `A_MAX` in the hard-stop CBF.**
  Steps 10–11. The firmware's landing controller ships against a computed table
  (§3), not a measured one. **This is the second high-risk item carried into the
  two-leg build.**
- **Whether a 100 mm drop bottoms the knee out.** Computed twice, both say yes;
  now confirmed by neither.

**What Mode A does still test, and it is the thing that matters most:** step 6
measures F₀ and k as built, and every number above is *computed from that curve*.
A measured spring turns the deferred items from guesses into predictions.

It also cannot, by construction, test the two step-2 fixtures against the leg —
the torque arm replaces the proximal link and the scale pedestal stands inside
the leg's swept radius (§6.1).

---

## 12. Still open, and gating the build

- **B1 — wheel-driver max bus voltage.** Run at 20 V until Steadywin answers.
- **C2 — shoulder motor length, 40 vs 44 mm.** Not resolvable from the GAUGE
  coupon (§2.4); caliper the motor. No structural consequence in this design.
- **C3 — wheel motor length, 26 vs 33 mm.** Hold the wheel coupon against the
  real motor; it is full length.
- **C4 — actuator masses, 388/150 vs 500/250 g.** ~~Decides whether ballast is
  61 g or 173 g.~~ **In Mode A it decides nothing structural** — the 112 g spread
  is 1 % of the stand's design load (§5). Weigh them anyway: the two-leg mass
  budget and the ballast figure for a later Mode B both turn on it.
- **Rear-flange thread depth.** Recorded as "~4.8 mm" and measured in the STEP as
  4.8, but the STEP is a simplified body and shows a Ø6 counterbore over the
  first 2.3 mm. Not used by this design — noted only because it would matter if
  the rear-mount option in §1.1 is ever revisited.
- **TPU bumper stiffness.** The flexion bumper is now a printed TPU 95A tube
  crushing 18 % rather than a PU block crushing 49 %, so it is a stiffer, shorter
  approach to the stop. Its rate is a bench-tuning item: reprint at a different
  wall count or swap to a softer filament if step 10 shows the approach is harsh.
- **Creep.** Re-torque everything after the first hour, then periodically, and
  **inspect the printed hub's dowel holes for ovalisation after every drop
  session.**
- **Panel stiffness.** The leg hangs off five M3 in a 5 mm printed panel — the
  robot's own load path, but if step 6 reads soft, suspect the panel before the
  spring and use the four free Ø88 holes for a stiffening ring (§2.2).
- **The hard stop is now plastic-backed, not steel-backed** (§8). It is a factor
  of 8 below the material limit, but it is the one place where dropping the laser
  part cost real margin. If the drop series repeatedly exceeds the +24° gate,
  inspect the cartridge spigot faces.
