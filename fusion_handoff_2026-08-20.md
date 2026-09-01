# Fusion handoff — snapshot the rig, export `RIG_Stand`

**Date:** 2026-08-20 · **Document:** `Beni_SingleLegRig` · **Scope:** Mode A
**Runs:** inside Fusion · **Est:** 20–30 min

You are working in `Beni_SingleLegRig`, the active build. `RIG_Stand` was modelled
2026-08-17 (`rig_lib.build_rig_stand()`, line 1633) and all seven Mode A checks
pass, but **the document has never been saved as a snapshot and `RIG_Stand.stl`
has never been exported.** Those two gaps block the physical build. Close them.

Read `CLAUDE.md` and `beni_single_leg_rig_design_record.md` §6.2 before you touch
the model. This document has a *reproducible* corruption hazard and the
bounding-box guard does not catch all of it.

---

## Read this first — the trap

Per `CLAUDE.md` and rig design record §6.2 trap 5:

- **Deleting any occurrence displaces both motor STEP references.** After any
  structural edit `REF_GIM6010-8` must read Y **5.00…49.00** and
  `REF_GIM4305-10` Y **61.50…94.50** (asserted at `rig_lib.py:1793`,
  `fusion_bridge/ops.py:31-32`).
- **`isSuppressed = True` is not a workaround** — not readable on this API build,
  the assignment lands on the Python wrapper silently.
- **The bounding-box guard alone is insufficient.** The same operation also
  resets `HW_WasherStack_M5` and `RIG_Knee_Bumper_Tube_L` to identity, dropping
  them inside the shoulder motor and inventing ~430 mm³ of clashes — while
  `ref_assert()` still passes. Anything placed by assigning `occ.transform2` is
  at risk; screws placed with `addExistingComponent(component, matrix)` are not.
- **It is not only deletes.** `beni_lib._spring_body()` and
  `beni_lib.apply_materials()` both trigger it, and `_spring_body` runs on every
  `rig_set_pose()`.

So: wrap anything that mutates in `rig_lib.guarded(fn)` (line 1902), or
`xf_capture()` (1810) / `xf_restore()` (1825) manually, then assert **both**
`ref_assert()` (1844) **and** `placed_assert()` (1864).

Call `rig_lib.register_pose_classes()` (line 927) before any sweep —
`beni_lib.classify()` only knows the original leg part names and silently returns
`'STATIC'` for the six §2.3/§13 replacement parts.

Use `rig_lib.real_clashes()` (line 815), **never** `beni_lib.interference()` —
the latter falls back to `entity.name`, so everything reads `Body1 ↔ Body2` and a
`'RIG_'` filter matches nothing. Four builds reported zero clashes against 49
real pairs.

---

## Task 1 — verify before you change anything

Establish that the model is currently good. If it is not, **stop and report** —
do not snapshot a displaced model, and do not "fix" it without saying so.

```python
import sys; sys.path.insert(0, '/Users/neilchulani/Fun/Robots/Biped')
import rig_lib
rig_lib.ref_assert()        # REF_GIM6010-8 Y 5.00…49.00, REF_GIM4305-10 Y 61.50…94.50
rig_lib.placed_assert()     # HW_WasherStack_M5, RIG_Knee_Bumper_Tube_L not at identity
rig_lib.checks_44()         # all seven Mode A checks
rig_lib.real_clashes()      # expect clean; report any pair with its volume
```

Report the actual output of all five. A failed `REF_*` guard means **no data, not
caveated data** — every figure computed against displaced geometry is void.

---

## Task 2 — snapshot the document

This is the highest-value item. `snapshots/` has two `Beni_Prototype1` entries
and **zero** for `Beni_SingleLegRig`, despite the rig being the verified active
build in a document with a known corruption hazard.

Create `snapshots/2026-08-20_rig-mode-a/` following the layout of
`snapshots/2026-08-08_post-production-fixes/`:

| File | Notes |
|---|---|
| `Beni_SingleLegRig_ModeA.f3d` | full archive |
| `Beni_SingleLegRig_ModeA.step` | assembly STEP |
| `mode_a_metrics.json` | mass, CoM, inertia; per-part volume/mass; the seven check results; `real_clashes()` output |
| `README.md` | what this snapshot is, what was verified, the exact `rig_lib` calls and their output |

Save the live document too, not just the export.

---

## Task 3 — export `RIG_Stand.stl`

`rig_export.py` already has the entry (`RIG_PRINT[0]`) with the orientation note.
Export to `rig_stl/RIG_Stand.stl`, binary, `MeshRefinementHigh` — matching
`rig_export._stl()`.

Verify against the recorded figures in `rig_stl/README.md` §9 and report both
the expected and actual:

- **499.3 cm³ / 574.2 g** PA-CF
- **200 × 32 × 299.3 mm** (X × Y × Z)
- mount face on **y = 42.00**

If any differs by more than rounding, report the discrepancy — do not adjust the
model to match the document, and do not adjust the document to match the model.

**Print-envelope update, new information as of 2026-08-20:** the printer is a
**Bambu Lab H2S, build volume 340 × 320 × 340 mm** (source: vendor spec, web,
2026-08-20). `RIG_Stand` at 200 × 32 × 299.3 **fits outright in its natural
orientation** — the splice contingency in `rig_stl/README.md` §9 ("split it low
in the column… bolted lap") is not needed and the "no print envelope is stated
anywhere" open item in `PROJECT_STATUS.md` can be closed. Note this in the snapshot
README; leave the §9 edit to the analyst side unless asked.

While you are exporting, also re-export the other Mode A parts if any are stale
relative to the current model — in particular confirm whether
**`RIG_Cable_Post_B`** still needs re-routing (`rig_stl/README.md` flags it as
mounting to the now-deleted Mode B column). If it does, **report it; do not
redesign it.**

---

## Task 4 — one measurement, if cheap

`PROJECT_STATUS.md` lists C2 (shoulder motor 40 vs 44 mm) and C3 (wheel motor 26 vs
33 mm) as open and gating. But `beni_prototype1_design_record.md` §2, titled
"Motor reference audit (measured from the supplied STEP)", already records
**"Overall length | 44.0 mm (x = −37.0 … +7.0)"** (§2.1) and **"Overall length |
33.0 mm (x = −27.0 … +6.0)"** (§2.2) — and the live model's asserted Y-spans are
44.00 and 33.00. No document connects these facts to C2/C3.

If it is cheap, return `op_bbox`-equivalent overall lengths for both `REF_*`
occurrences straight from the model, structurally (a returned value, not printed
prose). That gives a third traceable confirmation and lets the analyst side
downgrade C2/C3 from gating.

Do **not** attempt C4 (masses), C7 (phase R) or C10 (rotor inertia) — a STEP
carries no density or electrical data, and §2 notes the STEP is a single body so
the rotor cannot be separated from the stator. Those need a scale, a milliohm
meter, and a spin-down test.

---

## Deliverables

1. Output of all five Task 1 calls, verbatim.
2. `snapshots/2026-08-20_rig-mode-a/` populated, live document saved.
3. `rig_stl/RIG_Stand.stl`, with expected-vs-actual volume, mass, bbox.
4. `RIG_Cable_Post_B` re-route status.
5. Overall lengths for both `REF_*`, as returned values.
6. Anything that disagreed with a document — **reported, not silently resolved.**

## Rules

- **Never invent, recompute or round an engineering number.** Copy verbatim from
  the source. If two documents disagree, report the contradiction; unresolved
  conflicts go in `PROJECT_STATUS.md`.
- Prefer changing the builder in `rig_lib.py` over hand-editing the model.
- No new machined or laser-cut parts. Printed and off-the-shelf only
  (`MANUFACTURING_CONSTRAINTS.md`).
- Cite returned values, not `stdout`. A number that exists only in printed prose
  is not traceable to CAD.
- If you intend a model write, set `confirm_mutate` yourself; do not ask the
  operator to set it.
