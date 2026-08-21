# ARCHIVED — Prototype 1 Production-Readiness Audit (condensed)

**What this was.** An independent production-readiness audit of the Beni Prototype 1 Fusion model
(`Biped → Beni_Prototype1`), run **2026-08-08**: full context gather across the `Biped` folder plus
direct measurement of the live Fusion document via the Fusion MCP (B-Rep face geometry, body volumes,
per-body centroids, interference analysis, timeline inspection), with every number re-derived from
first principles rather than taken from the existing documents.

**Why it is archived.** It drove **revision 2**. Its findings are closed or superseded and the live
record is [`../beni_prototype1_rev2_changes.md`](../beni_prototype1_rev2_changes.md). The original
full-length findings document has been condensed into **this file**, which keeps only what is unique
to the audit and still true — its model census, its "do not touch" endorsement list, and its forensic
tables.

> ## ⚠ ALL MASS / CoM / INERTIA FIGURES IN THE ORIGINAL AUDIT ARE SUPERSEDED
>
> Do **not** quote the audit's mass properties. In particular, the pitch-bias
> figure of **0.394 N·m is wrong** and is the specific trap this note closes.
>
> | quantity | audit (2026-08-08) — **WRONG** | revision 2 — **current** |
> |---|---:|---:|
> | modelled mass | 3232.2 g | **3290.1 g** (Fusion-reported) |
> | robot total | ≈ 3352 g | — (3290.1 g is the model figure) |
> | CoM X, fore-aft | +11.97 mm | **+6.46 mm** |
> | Iyy (pitch) | 0.0208 kg·m² | **0.02508 kg·m²** |
> | pendulum length | 100.7 mm | **103.7 mm** |
> | standing pitch bias | 0.394 N·m | **0.21 N·m** |
>
> The audit's hand-computed per-body roll-up was replaced by real physical
> materials in the model (`beni_lib.apply_materials()`); mass, CoM and the full
> inertia tensor are now model output, published in `sim/beni.urdf` and
> `sim/beni_inertia.json`. See rev2 §2.

---

## 1. Model census (original §1.3) — verbatim

The only characterisation of the Fusion model's own shape anywhere in the project. Document
`Beni_Prototype1` (project `Biped`, lineage `mrn7U3LF…`) at audit time:

- **156 root occurrences**, **79 components**, **815 timeline entries**
- Feature mix: 217 extrudes, 212 sketches, 212 construction planes, 11 revolves,
  **1 mirror**, 162 occurrence adds
- **31 user parameters** (`L1`, `Ru`, `Rl`, `phi_stop`, `spring_rate`, …)
- 2 external references: `REF_GIM6010-8`, `REF_GIM4305-10`, plus one mirrored
  local copy of each
- **0 joints, 0 as-built joints, 0 rigid groups, 0 snapshots, 0 named views**

Motion is produced by scripted occurrence transforms (`beni_lib.set_pose`), not by Fusion joints.
That is a deliberate, documented choice.

---

## 2. What is solid, and should not be touched (original Part 4) — in full

This endorses *design decisions*, and is distinct from the spec's §17 freeze list, which freezes
*requirements*.

- **The kinematic core is correct and fully verified.** Ru/Rl/110° anchor geometry, the rising moment
  arm, the progressive wheel rate, the 154.269 mm nominal, the wheel directly under the shoulder —
  all reproduce exactly.
- **The spring cannot coil-bind before the metal stop.** 4.89 mm of margin, independently confirmed.
- **The 30 mm leg width is a forced consequence, not a choice**, and the reasoning in design record
  §4.1 is right: the guide's frozen anchor geometry fixes the minimum moment arm at 22.09 mm, which
  mandates a 20 mm clear channel, which leaves 5 mm arms — and a 6800 bearing (Ø19) needs that.
- **Locating the shoulder hub on the three Ø4 anti-rotation pins instead of the Ø34 pilot boss is the
  right call**, and the STEP evidence for it (root fillet blends to Ø36.4) is sound.
- **The clock-spring harness solution is correct** given the motor has no through-bore: r = 20 … 32 ×
  4 mm cavity, ~400 mm of Ø3.0 cable giving ≈ 470° against 370° needed, 27 % margin, strain relief on
  both ends.
- **The ±185° sweep is clean by construction as well as by test** — the Y-separation argument (all
  chassis within |y| ≤ 51, leg's inboard-most part is a body of revolution) makes the clearance
  rotation-invariant.
- **Assembly and disassembly logic is genuinely well thought through.** Spring changes with one
  clevis pin. Wheel motor removable with the leg assembled. Axle insertable only from inboard, and
  the sequence respects it.
- **`print_stl/` is exemplary de-risking.** The fit coupon and motor gauges let the whole knee and
  shoulder stack be dry-assembled before any motor or any metal arrives.
- **The web viewer is a real asset**, and `web/check.py` — headless-testing the posing maths in node
  with a stubbed three.js — is the right instinct. It passes: 81/81 poses, `update()` ok, all 7
  groups present.

---

## 3. Forensic detail more precise than its rev2 summary

### 3.1 The six chassis-mount hole coordinates (original §3.5)

The model's `Chassis_Shoulder_Plate_L` carried **6 chassis-mount Ø3.4 holes** on a rectangular grid
at (X, Z) = **(+30, −18), (+30, +48), (+30, +62), (−60, −18), (−60, +48), (−60, +62)**, spanning
y = 42 … 47. `build_shoulder_plate()` created **none of them** — it only cut 8 × Ø3.4 at PCD 74,
4 × Ø3.4 at PCD 88, the Ø7 grommet and the Ø48 bore. `build_all()` would therefore have rebuilt the
plate without its chassis interface, silently disconnecting the two legs from the frame while leaving
`Chassis_Frame` in place with its 10 unmatched Ø3.4 holes.

### 3.2 Full interference table (original §3.8)

Whole-assembly analysis, coincident faces excluded, threshold 0.5 mm³:
**89 pairs, of which 88 are screw-shank-in-tap-drill modelling artifacts.**

| pair (L+R merged) | count | total mm³ | max mm³ | verdict |
|---|---:|---:|---:|---|
| motor body ↔ M3×10 | 28 | 400.72 | 16.35 | artifact (screw in motor's tapped hole) |
| M4×10 ↔ `Shoulder_Output_Hub_L` | 12 | 298.60 | 24.88 | artifact |
| M4×10 ↔ `Wheel_Hub_L` | 12 | 288.96 | 24.08 | artifact |
| motor body ↔ M2.5×12 | 12 | 122.52 | 10.21 | artifact |
| motor body ↔ M3×8 | 6 | 76.87 | 12.81 | artifact |
| M3×10 ↔ `Shoulder_Cable_Cover_L` | 8 | 56.55 | 7.07 | **real — §3.4, screw 1.0 mm past bore** |
| `Knee_Axle_L` ↔ `Knee_Magnet_Carrier_L` | 1 | 32.11 | 32.11 | artifact (M4 stud in tap drill), documented |
| M3×8 ↔ `Proximal_Link_L` | 6 | 21.21 | 3.53 | **real — §3.4, screw 0.5 mm past bore** |
| M3×8 ↔ M3×8 | 4 | 4.12 | 1.03 | **real — §3.3, screw heads collide** |

Closed-form confirmation of each artifact flagged as real:

- Cable-cover screws: 7.07 mm³ = π × 1.5² × 1.0 → 1.0 mm past the insert bore.
- Proximal-link stop screws: 3.53 mm³ = π × 1.5² × 0.5 → 0.5 mm past the bore floor (Ø4.0 bore,
  y = 85.80 … 90.30 = 4.50 mm deep, against a 5.00 mm insert).
- Screw-head collision: `STOP_BOLT_A = (240°, 260°, 280°)` at `STOP_BOLT_R = 15.0` mm gives 5.209 mm
  centres for adjacent pairs against a Ø5.50 M3 SHCS head → 0.29 mm overlap; Fusion reported 4
  clashes at 1.03 mm³ each, and the closed-form lens area for two Ø5.5 circles at 5.209 mm centres ×
  3.0 mm head height = 1.02 mm³ — exact match.

The audit's own conclusion: the design record's "interference clear" claim held for the *structure*,
but that audit was run with screws filtered out — and filtering the screws is exactly what hid the
three real defects.

### 3.3 Derivation of the 48 g spring-envelope delta (original §3.1)

The BOM's 3304 g figure was close and essentially sound — the 48 g delta was because `Knee_Spring_L`
is modelled as its full outer *envelope* at steel density (**51.4 g modelled vs 25.3 g real
spring**), which over-counts by ~26 g per leg, offset by right-leg parts missing from the model.

---

## 4. Finding and recommendation disposition

| # | Finding (one line) | Disposition |
|---|---|---|
| 3.1 | No physical materials; no CoM or inertia | CLOSED — rev2 §2 |
| 3.2 | Right leg an incomplete copy (3 parts missing, 2 stale) | CLOSED — rev2 §3 |
| 3.3 | Three knee-stop screw heads physically collide | CLOSED — rev2 §4.1 |
| 3.4 | Blind insert bores too shallow; screws bottom out | CLOSED — rev2 §4.2 |
| 3.5 | `build_all()` would break the model | CLOSED — rev2 §5 |
| 3.6 | Zero fillets in the whole design | CLOSED — rev2 §6 |
| 3.7 | Tyre has no retention and no crown | CLOSED — rev2 §7 |
| 3.8 | Interference audit hid three real defects behind a screw filter | CLOSED — rev2 §8 |
| 3.9 | No STEP, no drawings, no tolerances for machined parts | CLOSED — rev2 §9 (and moot: no machined parts) |
| 3.10 | Electronics and harness are placeholders; no IMU datum | OPEN — partly fixed, rev2 §10 |
| 3.11 | Actuator sizing never checked against the duty cycle | OPEN — quantified not closed, rev2 §11 |
| 3.12 | Items blocked on outside information | OPEN — rev2 §11 |

Finding bodies are not reproduced here; rev2 has them. Of the 16 recommendations, 9 are done, and
two are void:

- **Recommendation 7** (STEP 214 exports, dimensioned drawings, tolerance, hardness and material-cert
  callouts for the "10 machined parts") is **FORBIDDEN** under the project's hard rule — *3D printed
  and off-the-shelf parts only, no laser cutting, no machining*
  ([`../MANUFACTURING_CONSTRAINTS.md`](../MANUFACTURING_CONSTRAINTS.md)). There are no machined
  parts; all ten families are printed, bought or deleted.
- **Recommendation 13** (add real Fusion joints with limits) was **deliberately REJECTED** in
  rev2 §12.
