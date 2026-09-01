# Beni

<!-- PRINT_QUEUE_START -->
## Print this next — ABS proximal-link first article

**Download:** [ABS proximal link, Ø19.10 bearing bores — print-ready STL](https://raw.githubusercontent.com/TnnsBeast/Biped/main/first_article_stl/assembly_dry_fit/ABS_FA_Proximal_Link_L_D19p10_PRINT_ORIENTED.stl)

**Quantity/material:** 1 × ABS

**Slicer:** import as-is; **do not rotate or “lay on face.”** Use 0.20 mm layers,
4 walls, 5 top/bottom layers, 30% infill, and a brim. Do not add support inside
the bearing bores or internal channels. Expected imported size: **169.39 × 31.60
× 62.00 mm**.

**After printing:** thumb-press one 6800-2RS bearing into each open outside face.
Both must enter square, seat flush, have no rock, and remain removable without a
clamp or retaining compound. Follow the
[full test and acceptance instructions](first_article_stl/assembly_dry_fit/README.md#batch-3--unloaded-abs-proximal-link-bearing-rehearsal).

**Hold:** do not print the distal link yet; the Ø10 h6 knee pin and its DFM and
assembly-path verification still gate that release.
<!-- PRINT_QUEUE_END -->

---

A mostly 3D-printed, two-legged balancing robot with a driven wheel at the end of
each spring-loaded leg. Each side runs from an active rotary shoulder through a
passive knee to a wheel actuator, with a Teensy 4.1 planned as the main
controller.

![Verified shoulder assembly in Fusion](evidence/shoulder_assembly/2026-08-23_plate_sequence/03_final_shoulder_stack.png)

The project is deliberately proving one leg before committing to the full robot.
The active build is a rigid-stand **Mode A single-leg rig** for fit, assembly,
spring characterization, controls bring-up, and unloaded motion. The complete
two-leg Prototype 1 is modeled and audited in Fusion, but has not been built.

## Current phase

| Area | State |
|---|---|
| Mechanical | Mode A rig modeled and verified; ABS fit and assembly articles in progress |
| Hardware | Both Steadywin actuators and the 6800-2RS bearings are in hand |
| Electronics | Architecture documented; nothing wired yet |
| Firmware | Non-energizing Teensy 4.1 Stage 0 scaffold compile-verified |

For the exact current state, next actions, blockers, release gates, and CAD
handoff, start with **[`PROJECT_STATUS.md`](PROJECT_STATUS.md)**.

## Design approach

- **Printed and off-the-shelf parts only.** No machining or laser cutting. See
  [`MANUFACTURING_CONSTRAINTS.md`](MANUFACTURING_CONSTRAINTS.md).
- **ABS first articles before structural PA-CF.** Fits and assembly order are
  rehearsed cheaply before structural material is released.
- **Assembly is verified, not assumed.** Insertion paths, tool access, cable
  routing, service paths, and the physical first article are part of the release
  gate in [`ASSEMBLY_VERIFICATION.md`](ASSEMBLY_VERIFICATION.md).
- **Scripted geometry.** The Fusion models, exports, simulation assets, and audit
  checks are designed to be reproducible.

## Explore the project

| Start here | What you will find |
|---|---|
| [`PROJECT_STATUS.md`](PROJECT_STATUS.md) | Live build status, next work, blockers, CAD warnings, and document map |
| [`beni_prototype1_design_record.md`](beni_prototype1_design_record.md) | Prototype 1 mechanical design and verified CAD data |
| [`beni_single_leg_rig_design_record.md`](beni_single_leg_rig_design_record.md) | Single-leg rig design, checks, mass properties, and purchase list |
| [`electronics/README.md`](electronics/README.md) | Power, compute, CAN, harness, logging, bring-up, and BOM |
| [`firmware/README.md`](firmware/README.md) | Firmware scope and Stage 0 bring-up scaffold |
| [`first_article_stl/README.md`](first_article_stl/README.md) | ABS fit coupons and assembly-rehearsal prints |
| [`web/`](web/) | Browser-based robot pose viewer |
| [`sim/`](sim/) | URDF and inertia exports |
| [`evidence/`](evidence/) | Dated hardware and physical-test evidence |

## Working on Beni

Read [`PROJECT_STATUS.md`](PROJECT_STATUS.md) for the live handoff and
[`CLAUDE.md`](CLAUDE.md) for the engineering rules, canonical sources, and Fusion
failure modes before making changes. CAD inspection, editing, export, and
verification must go through the Fusion integration described there.
