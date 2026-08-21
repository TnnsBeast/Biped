# MODE A SNAPSHOT — 2026-08-20, `Beni_SingleLegRig`

First snapshot of the rig document. `snapshots/` previously held two
`Beni_Prototype1` entries and **zero** for `Beni_SingleLegRig`, despite the rig
being the active build in a document with a known corruption hazard
(`beni_single_leg_rig_design_record.md` §6.2 trap 5).

Scope: **rig Mode A**. Shoulder bolted rigid to `RIG_Stand`; the vertical slide,
the ballast and the drop series are `[DEFERRED — MODE B]`, not cancelled — the
Mode B *occurrences* are stripped from the assembly but every builder in
`rig_lib.py` is intact.

**Nothing physical has been built.** Every number here comes from CAD, a vendor
datasheet, or a script.

| file | what it is |
|---|---|
| `Beni_SingleLegRig_ModeA.f3d` | full parametric Fusion archive, 2.5 MB |
| `Beni_SingleLegRig_ModeA.step` | neutral B-Rep of the whole assembly, 3.9 MB |
| `mode_a_metrics.json` | per-occurrence volume / mass / material / bbox / transform, per-component bodies, assembly mass + CoM + inertia, the seven check results, `real_clashes()` and unfiltered `clashes()`, `RIG_Stand` expected-vs-actual, both `REF_*` overall lengths |
| `rig_lib.py`, `rig_export.py`, `rig_calc.py`, `beni_lib.py`, `beni_export.py` | the build + export + calc source as it stood, so the metrics are reproducible |

Governing documents are **not** copied here (rule 5, state one fact once):
scope and CAD handoff `../../fusion_agent_guide_mode_a.md`, as-built
`../../beni_single_leg_rig_design_record.md`, print set `../../rig_stl/README.md`.

A named Fusion **cloud version** was created at the same moment:

> MODE A 2026-08-20: first saved version with RIG_Stand modelled and
> RIG_Stand.stl exported. Mode B occurrences stripped; all seven Mode A checks
> pass (rig_lib.checks_44); ref_assert + placed_assert clean before and after the
> sweeps; RIG_Floor_Plate and RIG_Knee_Bumper_Tube_L STLs re-exported. Snapshot:
> snapshots/2026-08-20_rig-mode-a/.

`sha256`:

```
05c28b05a0a6118e2a1a374198430e6004177c0932816ad4216d80fd8744467e  Beni_SingleLegRig_ModeA.f3d
d2ce489b0b5fa0d792f10d21e8deea7718d337187f6420de2bad41ff544395c2  Beni_SingleLegRig_ModeA.step
9257d4509c32effcfcb3c68f740156de907eff7d07f44c96ef37684f9704949c  mode_a_metrics.json
26100e0c1ce9a7253d0d3611c4984a1c558f3dd1b125a2ee3970d65fb9f2e9d8  ../../rig_stl/RIG_Stand.stl
```

---

## State at snapshot

| | |
|---|---:|
| root occurrences | 76 |
| components | 43 |
| timeline features | 1027 |
| pose | θ = 0.0°, φ = 0.0° |
| assembly mass | **2381.3687 g** |
| CoM | X −15.6330, Y +54.3248, Z −85.7369 mm |
| Iyy about the CoM | 0.0290215 kg·m² |
| `real_clashes()` | 1 pair — the documented step-2 fixture, below |

⚠ **The 2381.3687 g includes 750.00 g of motor** — `REF_GIM6010-8` 500.0000 g
and `REF_GIM4305-10` 250.0000 g — carried by **back-fitted material densities**
(4.4581 and 4.6519 g/cm³ against STEP volumes of 112156.10 and 53741.47 mm³).
Those are **vendor datasheet masses, not weighed hardware and not STEP-derived**;
a STEP carries no density. Conflict **C4 is untouched by this snapshot** and still
needs a scale. Every other mass in the file is material density × CAD volume.

---

## Verification — the exact calls and what they returned

Run inside Fusion against the live document, in this order.

```python
import sys; sys.path.insert(0, '/Users/neilchulani/Fun/Robots/Biped')
import rig_lib
rig_lib.register_pose_classes()   # -> 6
rig_lib.ref_assert()              # -> True
rig_lib.placed_assert()           # -> True
rig_lib.checks_44()               # -> all seven PASS, 69.6 s
rig_lib.real_clashes()            # -> 1 pair, the step-2 fixture
```

### Guards — clean before the sweeps, after the sweeps, and after the save

```
   REF_GIM6010-8    Y    5.00 ..   49.00   want   5.00 ..  49.00   ok
   REF_GIM4305-10   Y   61.50 ..   94.50   want  61.50 ..  94.50   ok
   HW_WasherStack_M5          X   60.42..  72.62 Z   -90.50..  -72.70   placed ok
   RIG_Knee_Bumper_Tube_L     X   58.41..  74.11 Z   -94.43..  -72.49   placed ok
```

`ref_assert()` **and** `placed_assert()` were both run three times — before
`checks_44()`, after its pose sweeps, and after `doc.save()`. All three clean, so
the bounding-box guard and the transform2 guard agree and no figure in this
snapshot was computed against displaced geometry.

### The seven Mode A checks — `rig_lib.checks_44()`, 69.6 s

| check | result |
|---|---|
| 1 knee sweep vs guide §4 | **PASS** — worst deviation **0.043 mm** (limit 0.15) over φ −8…+27 |
| 2 shoulder ±120° | **PASS** — 17 poses at 15° steps, **0** with clashes; wheel clears the Mode A contact plane by +12.04 mm at φ=0 |
| 3 wheel clears the floor plate | **PASS** — 6 φ stations −8…+27, 0 clashes; touches at −8° by design |
| 4 Mode A load report | **PASS** — 5 of 5 insert bores found, centroid X −24.00 / Z +40.40, Σr² 14179 mm², worst r 68.60 mm, worst screw shear 53.2 N stall / 121.0 N proof |
| 5 torque arm clearance | **PASS** — Y bands disjoint by 17.50 mm, so the arm cannot reach the stand at any angle |
| 6 the 42.00 mm overhang | **PASS** — **42.000 mm**, 0.000 mm shim, no `RIG_Stand` interference over 0.01 mm³ |
| 7 hold-down | **PASS** — 4 clamp landings, 2 aft + 2 fore; smallest 720 mm² |

Full printed output is not reproduced here — the returned values are in
`mode_a_metrics.json` under `checks_44` and `checks_44_verdicts`.

### `real_clashes()` — 1 pair, expected

```
   REAL CLASHES: 1
      Proximal_Link_L                  RIG_Torque_Arm                    14634.62 mm3
```

`RIG_Torque_Arm` is a `STEP2_FIXTURE`: it bolts to the hub **in place of** the
proximal link and is only ever fitted with the leg off, so the two genuinely
cannot coexist. Checks 2 and 3 exclude `STEP2_FIXTURES`; bare `real_clashes()`
does not. **Not a defect** — but see the finding below, because `rig_lib`'s own
comment claims this pair is filtered when it is not.

Unfiltered `clashes()` reports 45 pairs; the other 44 are screws inside their own
modelled tap drills, which `_is_artifact()` does filter. Both lists are in the
metrics file.

---

## `RIG_Stand` — expected vs actual

Recorded figures from `../../rig_stl/README.md` §9, measured figures off the live
model at `HighCalculationAccuracy`.

| | recorded §9 | measured | |
|---|---:|---:|---|
| volume | 499.3 cm³ | **499.3082 cm³** | matches |
| mass, PA-CF | 574.2 g | **574.2045 g** | matches (ρ = 1.150000 g/cm³) |
| size X × Y × Z | 200 × 32 × 299.3 mm | **200.0000 × 32.0000 × 299.3119 mm** | matches |
| mount face | y = 42.00 | **y = 42.0000** | matches |
| bodies | one | 1, material `BENI_PACF` | matches |

`rig_stl/RIG_Stand.stl` — binary, `MeshRefinementHigh`, 2372 triangles, 115.9 kB.
Mesh bbox reproduces the B-Rep bbox to **0.0000 mm** on all six faces. Mesh
volume 499.4071 cm³ is **+0.020 %** on the B-Rep, which is chordal tessellation
of the nine bores and counterbores (chords cut into the hole walls, so a mesh of
a holed solid reads slightly heavy) — not a geometry difference.

**Print envelope — closed.** The printer is a **Bambu Lab H2S, 340 × 320 × 340 mm**
(vendor spec, web, 2026-08-20). At 200 × 32 × 299.3 the stand **fits outright in
its natural orientation**, mount face flat on the bed. The §9 splice contingency
("split it low in the column… bolted lap") is **not needed**, and the "no build
envelope is stated anywhere" open item in `../../README.md` can be closed. The
§9 edit itself is left to the analyst side.

---

## STL set

Every printed rig part and every `reroute/` part was compared against the live
model — mesh bbox and mesh volume vs B-Rep bbox and volume.

| file | action |
|---|---|
| `RIG_Stand.stl` | **NEW** — first export. The gap this handoff existed to close. |
| `RIG_Floor_Plate.stl` | **RE-EXPORTED** — was 12.0429 mm stale in Z. The old file sat at Z −215.269…−209.269, the Mode B datum; Mode A drops the bench plane to Z −227.3119 (`Z_FLOOR_A`) so the shoulder axis clears the guide §2.5 minimum of 221.31 mm. Geometry unchanged, 260 × 60 × 6 mm, 93.6000 cm³. |
| `RIG_Knee_Bumper_Tube_L.stl` | re-exported, **byte-identical** to the committed file. Not stale. See the note below. |
| `RIG_Torque_Arm`, `RIG_Cable_Post_A`, `RIG_Knee_Collar_L`, `RIG_Knee_Magnet_Carrier_L`, `RIG_Knee_Stop_Plate_L` | current, no action |
| `reroute/` — all five | current, no action (worst bbox delta 0.01 mm, worst volume delta 0.03 %) |
| `RIG_Carriage`, `RIG_Index_Bar`, `RIG_Ballast_Pot`, `RIG_Cable_Post_B` | not in the model — Mode B, stripped. Files left in place; the builders are intact. |

⚠ **`RIG_Knee_Bumper_Tube_L` cannot be staleness-checked by bbox.** It is one of
the two parts positioned by assigning `occ.transform2`
(`rig_lib.PLACED_BY_TRANSFORM`), so its component geometry is built at the origin
and the occurrence transform places it. `createSTLExportOptions(occ, …)` exports
the **component-local** geometry, so the STL is a Ø13 × 20.33 mm tube on the Y
axis while the model bbox is the assembly-space AABB of that tube *rotated* onto
the cartridge axis (15.69 × 13.00 × 21.94 mm). Comparing the two reads as an
88 mm displacement and looks exactly like the trap-5 corruption signature. It is
not — the re-export hashes identical to the committed file and the volumes agree
to 0.057 %. Every other printed part is built at assembly coordinates, so for
those the bbox comparison is valid.

---

## Findings — reported, not resolved

Four disagreements between a document and the model. **None was silently fixed.**
Per rule 2 they belong in `../../README.md`'s conflict register; adding them
there is the analyst side's call.

1. **`rig_stl/README.md` §9 bench-bolt positions are wrong for the built part.**
   §9 says "4 × M6 bench-bolt holes at **X = ±88 and ±26**". The builder is
   `rig_lib.py:1625`, `STAND_BOLT_X = (-88.0, -26.0, 34.0, 88.0)`, and check 7
   measures the model at **X −88, −26, +34, +88**. The set is asymmetric: the
   fore-inboard bolt is at **+34, not +26**. The builder is authoritative for the
   printed part; §9's symmetric description is not what will come off the bed.

2. **§9's second clamp landing is 11.5 mm longer than the model's.** §9 records
   the four landings as X −100…−77.5, **−43.5…−8**, +8…+61.5, +77.5…+100.
   Check 7, probing point containment on the solid at 0.5 mm steps, measures
   X −100…−77.5, **−32.0…−8.5**, +8.5…+61.0, +77.5…+100. The first and fourth
   agree exactly; the third differs by one probe step at each end (immaterial);
   the second's aft end differs by **11.5 mm**, so that landing is 23.5 mm long,
   not 35.5 mm. It still exceeds the 20 mm minimum and check 7 still passes 2 aft
   + 2 fore, so nothing structural turns on it — but the number is wrong.

3. **`rig_lib.ARTIFACT_PAIRS` claims to filter the torque arm and does not.** The
   comment at `rig_lib.py:770-772` lists "or the torque arm, which REPLACES the
   proximal link and is only fitted with the leg off" among the documented
   artifact classes, but no `('Proximal_Link_L', 'RIG_Torque_Arm')` pair is in the
   tuple and `_is_artifact()` does not special-case it. The checks compensate by
   filtering `STEP2_FIXTURES` themselves, so no check is wrong — but bare
   `real_clashes()` reports a 14634.62 mm³ pair that the code's own comment says
   is filtered, which is the sort of passing-wrong-answer this file is otherwise
   careful about.

4. **Guide §2.4's stand mass assumption is superseded by the built part.**
   Check 4 reports it: §2.4 assumes "a printed stand is ~0.3 kg" for the tipping
   table; the modelled stand is **574.2045 g**. This makes §2.4's conclusion
   *stronger* (dead weight is still nowhere near the 11.2 kg that 11.00 N·m needs
   at a 100 mm base half-width), so no argument breaks. §9 already carries the
   correct 0.574 kg. Also noted by check 4: `rig_calc` quotes 2.22 / 5.04 MPa
   bearing on an 8 mm wall, while the built web is 12 mm, giving 1.48 / 3.36 MPa —
   the built part is less stressed than the calc reports.

Not attempted, per the handoff: **C4** (motor masses), **C7** (phase R), **C10**
(rotor inertia). A STEP carries no density and no electrical data, and design
record §2 notes the STEP is a single body so the rotor cannot be separated from
the stator. Those need a scale, a milliohm meter and a spin-down test.

---

## C2 / C3 — third traceable confirmation

`README.md` lists C2 (shoulder motor 40 vs 44 mm) and C3 (wheel motor 26 vs
33 mm) as open and gating. Overall lengths returned straight off the live model,
along each motor's own axis, which is the global Y axis:

| occurrence | Y span | overall length | design record §2 |
|---|---|---:|---|
| `REF_GIM6010-8` | 5.0000 … 49.0000 | **44.0000 mm** | §2.1 "44.0 mm (x = −37.0 … +7.0)" |
| `REF_GIM4305-10` | 61.5000 … 94.5000 | **33.0000 mm** | §2.2 "33.0 mm (x = −27.0 … +6.0)" |

Both agree with §2 exactly, so **44 mm and 33 mm now have three independent
traceable sources**: the supplied STEP as audited in §2, the asserted `REF_*`
guard spans, and this direct measurement. The 40 mm and 26 mm figures in C2/C3
are not supported by any of them. Downgrading C2/C3 from gating is the analyst
side's call — this snapshot only supplies the measurement.

Measured with `beni_lib.bbox_of()`, which accumulates per-body bounding boxes,
**not** `occurrence.boundingBox` — the latter inflates under rotation (§6.2
trap 3) and reads 4.98…49.01 / 61.48…94.51 on these same two occurrences.
