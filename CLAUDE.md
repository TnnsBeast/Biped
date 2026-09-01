# CLAUDE.md — working rules for the Beni biped project

## What this project is

A Beni-style wheeled biped: **body → active rotary shoulder → proximal link →
passive spring-loaded knee → distal link → driven wheel**, one leg per side. Two
Steadywin actuators per leg (GIM6010-8 shoulder, GIM4305-10 wheel), ABS first
articles followed by PA-CF structural parts, Teensy 4.1 control.

Two Fusion documents exist: `Beni_Prototype1` (the two-leg robot, revision 2,
audits clean) and `Beni_SingleLegRig` (a Save-As copy, the **active build**).
**The rig build is MODE A only** as of 2026-08-17 — shoulder bolted rigid to a
printed stand; the vertical slide, the ballast and the drop series are **deferred,
not cancelled**. `RIG_Stand` **is now modelled** (`rig_lib.build_rig_stand()`,
2026-08-17) and the Mode B occurrences are stripped from the assembly; the CAD
handoff that specifies it is [`fusion_agent_guide_mode_a.md`](fusion_agent_guide_mode_a.md),
and the contradictions found while building it are in `PROJECT_STATUS.md`.
The Mode A document is saved as a named cloud version, the stand STL is exported,
and the snapshot is in `snapshots/2026-08-20_rig-mode-a/`. **Both actuators are in
hand**, with photographs indexed in
`evidence/actuators/2026-08-20_received/`; no printed leg or wiring has yet been
assembled. If you state an engineering figure, trace it to CAD, a vendor source,
a script, or an explicitly identified physical observation.

Start at [`PROJECT_STATUS.md`](PROJECT_STATUS.md) for status and reading order.

## The hard rules

1. **3D printed and off-the-shelf parts only. No laser cutting, no machining.**
   Authoritative: [`MANUFACTURING_CONSTRAINTS.md`](MANUFACTURING_CONSTRAINTS.md).
   Never propose a part that needs a mill, lathe, waterjet or laser. Cutting bought
   stock to length with a hacksaw is fine. If a design problem seems to need a
   machined part, solve it a different way and say why.

2. **Never invent, recompute or round an engineering number.** Copy figures
   verbatim from their source document. If two documents disagree, **report the
   contradiction — do not silently pick one.** Unresolved conflicts are listed in
   `PROJECT_STATUS.md`; add to that list rather than guessing.

3. **The frozen documents.** `beni_prototype1_fusion_guide_rewritten.md` §4–§9 is
   the frozen kinematics and requirements. `beni_prototype1_design_record.md` §2
   (motor interfaces measured from STEP) and §3 (the lateral Y-stack) are the
   datum the whole project is dimensioned against. Do not change any of these
   without demonstrating an actual failure.

4. **Prefer editing bodies over adding banners.** This repo previously accumulated
   documents whose header said "superseded" while the body still instructed the
   reader to laser-cut steel. If a fact is stale, fix it where it is written, or
   mark it inline `[SUPERSEDED]` at the row. A banner alone is not enough.

5. **State one fact once.** Before adding a table or a derivation, check whether it
   already exists elsewhere and link to it instead. The canonical homes are listed
   below.

6. **All Fusion work goes through the Fusion MCP.** This applies to inspection,
   editing, export, and verification. Do not substitute local STEP processing or
   UI automation for a Fusion operation.

7. **ABS first, PA-CF at structural release.** Use ABS for the first mating
   coupons, assembly rehearsal, cable routing, covers, floor-contact parts, and
   unloaded/hand-driven leg work. Do not apply stall torque, spring-test loads,
   drops, or structural proof loads through the ABS load path. ABS print
   compensation does not transfer to PA-CF; repeat the critical coupon before
   releasing PA-CF structural parts.

8. **Keep the public GitHub repository current.** The tracking repository is
   `https://github.com/TnnsBeast/Biped`. When a task materially changes project
   files, finish with one coherent commit and push it to `origin/main` after the
   relevant checks pass, unless the owner says not to. Do not commit generated
   caches, credentials, local account/order screenshots, or unfinished outputs.
   Read-only reviews and research do not require empty commits.

9. **Final-pose clearance is not assembly verification.** Before releasing a
   print or an assembly step, demonstrate the insertion order and full path,
   fastener/tool access, cable path, and service/removal path in Fusion. Then
   rehearse the sequence on the first physical article before structural release.
   Never use fasteners to draw an incompatible print into place. Canonical gate:
   [`ASSEMBLY_VERIFICATION.md`](ASSEMBLY_VERIFICATION.md).

10. **Keep the active print queue at the top of `README.md`.** Whenever a verified
    repository change makes a new or revised part ready for the owner to print,
    update the `PRINT_QUEUE_START` / `PRINT_QUEUE_END` block immediately after the
    README title before pushing. Put a direct raw-GitHub STL download in the first
    few lines and state quantity, material, required import orientation, concise
    slicer constraints, and the physical acceptance test. Replace stale print
    links rather than accumulating a history there, and identify any closely
    related parts still on hold. If nothing is released, the block must say so
    explicitly; a ready-to-print file must never be discoverable only in a
    subdirectory document.

11. **Keep the README CAD gallery current.** When a verified model change affects
    the full robot, leg, or knee views shown on the project homepage, run
    `readme_images_fusion.py` through the Fusion MCP and commit the refreshed
    `docs/readme/` images with the model change. Do not substitute concept art or
    locally rendered STEP/STL images for the live Fusion model.

## Where each fact lives — link, don't copy

| Fact | Canonical home |
|---|---|
| Active owner print/download queue | `README.md`, first section between `PRINT_QUEUE_START` and `PRINT_QUEUE_END` |
| Current build status, next work, and unresolved engineering issues | `PROJECT_STATUS.md` |
| The manufacturing rule and the ten-part routing table | `MANUFACTURING_CONSTRAINTS.md` |
| PA-CF print settings + per-setting reasoning | `beni_rig_no_machining.md` §1 |
| **Where ABS is allowed instead of PA-CF** | `beni_rig_no_machining.md` §4 |
| Motor interface geometry (from STEP) | `beni_prototype1_design_record.md` §2 |
| Delivered actuator photographs and visible connector arrangement | `evidence/actuators/2026-08-20_received/` |
| Lateral Y-stack | `beni_prototype1_design_record.md` §3 |
| Robot mass properties / CoM / inertia | `beni_prototype1_design_record.md` §14 |
| Fastener schedule, assembly sequence, torques | `beni_prototype1_bom_and_assembly.md` §7, §9 |
| Physical assembly-path release gate and status labels | `ASSEMBLY_VERIFICATION.md` |
| Revision-2 defects and the Fusion scripting traps | `beni_prototype1_rev2_changes.md` |
| Rig as-built, checks, mass, purchase list | `beni_single_leg_rig_design_record.md` |
| **Mode A scope decision + CAD handoff** | `fusion_agent_guide_mode_a.md` |
| **Mode A load set** (42.00 mm overhang, the four moments, tipping table, step-6 mass/φ table) | `rig_calc.py` → `mode_a_stand()`, written up in `fusion_brief_single_leg_rig.md` §4.1 |
| **Fusion measurement traps** | `beni_single_leg_rig_design_record.md` §6.2 |
| Knee hard-stop redesign + Hertzian reasoning | `beni_single_leg_rig_design_record.md` §8 |
| Coordinate frame, free-space map, spring table | `electronics/00_mechanical_datum.md` |
| Blocker/conflict register (B1, C1–C10, CR-1…10) | `electronics/05_open_questions.md` |
| Rig electronics shopping list | `electronics/07_bom.md` Wave 0 |
| Rig mechanical shopping list | `beni_single_leg_rig_design_record.md` §9 |
| Reading the live CAD without Fusion access | `fusion_bridge/PROTOCOL.md` |

## Conventions that bite

- **Chirality.** Only left-hand (`_L`) parts are modelled and exported. Mirror in
  the slicer. Fusion reports a mirrored occurrence under its *source* occurrence's
  `name` while the component carries the `(Mirror)` suffix — **trust the clash
  volume's bounding box, not the names.**
- **Conflict shorthand.** B1 / C2 / C3 / C4 are referenced across many files and
  defined in `electronics/05_open_questions.md`. Do not renumber them.
- **Two build targets, different numbers.** `electronics/01`–`06` describe the
  two-leg robot; the rig is a Teensy 4.1 on a 20 V bench supply with no pack, no
  BMS, no PCB, no satellite nodes, no clock springs. A figure that is right for one
  may be wrong for the other — scope it explicitly rather than overwriting it. The
  passive drop limit is the standing example: **45 mm planning limit / 46.3 mm
  computed +24° gate crossing** for the rig, ~49 mm for the two-leg 1-DOF model.
- **Three scopes now, not two: two-leg / rig Mode A / rig Mode B.** Mark deferred
  material `[DEFERRED — MODE B]` inline at the row (rule 4 applies — a banner alone
  is not enough) and never delete it, because Mode B is deferred rather than
  cancelled. Two figures that are easy to cross-wire: the lateral overhang is
  **42.00 mm in Mode A** and 63.00 mm in the Mode B stack, and the sprung mass
  1.645 kg is **Mode B only** — Mode A has no ballast, which is why conflict C4
  decides nothing structural in the rig. **Rig step 6 runs in Mode A**, so the
  measured spring F₀ and k are not forfeited by the deferral.
- **`beni_lib.interference()` cannot be trusted** — it falls back to `entity.name`,
  so everything reads `Body1 ↔ Body2` and a `'RIG_'` filter matches nothing. Four
  builds reported zero clashes against 49 real pairs. Use `rig_lib.real_clashes()`.
- **Fusion bounding boxes inflate under rotation** (axis-aligned box of the
  untransformed box). The box *centre* transforms exactly. Never read a clearance
  off `bbox` min/max for a rotated part.

## Editing the Fusion models

⚠ **In `Beni_SingleLegRig`, deleting any occurrence displaces both motor STEP
references.** `isSuppressed = True` is not a workaround — the property is not
readable on this API build, so the assignment lands on the Python wrapper silently.
Capture `transform2` for both `REF_*` occurrences and every child in their trees,
delete, then write them back and assert the bounding boxes. After any structural
edit: `REF_GIM6010-8` must read Y 5.00…49.00, `REF_GIM4305-10` Y 61.50…94.50.

⚠ **That 7-transform recipe is not enough, and the bounding-box guard passes
anyway.** The same delete also resets `HW_WasherStack_M5` and
`RIG_Knee_Bumper_Tube_L` to identity, dropping both inside the shoulder motor and
inventing 430 mm³ of clashes. Anything placed by assigning `occ.transform2` is at
risk; screws placed with `addExistingComponent(component, matrix)` are not. And it
is not only deletes — **`beni_lib._spring_body()` and `beni_lib.apply_materials()`
both trigger it**, and `_spring_body` runs on every `rig_set_pose()`. Use
`rig_lib.guarded(fn)` / `xf_capture()` + `xf_restore()`, then `ref_assert()` **and**
`placed_assert()`. Full write-up: `beni_single_leg_rig_design_record.md` §6.2 trap 5.

⚠ **`beni_lib.classify()` only knows the original leg part names** and silently
returns `'STATIC'` for anything else, so the six §2.3/§13 replacement parts stayed
frozen while the leg swept through them. Call `rig_lib.register_pose_classes()`
before any sweep.

Geometry is scripted so the models stay reproducible. Prefer changing the builder
in `beni_lib.py` / `rig_lib.py` over hand-editing the model, and re-run the audits:

```python
import rig_lib; rig_lib.checks_44(); rig_lib.real_clashes()
```
```
python3 rig_calc.py     # recomputes every number in the rig design record
```

`rig_calc.py` and `stl_inspect.py` run in plain `python3`; everything else runs
only inside Fusion.

## If you cannot reach Fusion

Most agents working in this repo cannot. STLs and STEP files are not a substitute
— they carry no mass properties, no materials, no interference, no poses.

Use the bridge: write a request naming ops from a fixed whitelist, have an
operator with Fusion open run it, read the JSON back. Protocol and op list:
`fusion_bridge/PROTOCOL.md`. Operator side: `fusion_bridge/OPERATOR.md`.

```
python3 fusion_bridge/bridge.py check          # validate before handing over
python3 fusion_bridge/bridge.py read <runid>   # after the operator runs it
```

Three rules when consuming a bridge result:

1. **A failed `REF_*` guard means no data, not caveated data.** Both motor
   bounding boxes are asserted on every run. If either misses, the model has
   displaced its STEP references and every figure in that file — mass, clashes,
   clearances — was computed against wrong geometry. Discard the run.
2. **Cite `value`, never `stdout`.** `stdout` is captured for diagnosis because
   most `rig_lib` functions report by printing. A number that only exists in
   prose is not traceable to CAD; ask for an op that returns it structurally.
3. **Never ask the operator to set `confirm_mutate`.** Set it in the request
   yourself when you intend a model write, or accept the abort.


## House style for documents

Terse, engineering-first, no narrative padding. Numbers carry their units and their
derivation. When a design decision was made, record **why**, and record what was
rejected and why it lost — the rejected-alternative reasoning in this repo has
repeatedly turned out to be the most valuable content in it. Do not write audit
transcripts ("checked pose −185, clear; −150, clear…") — state the result and the
sweep bounds.
