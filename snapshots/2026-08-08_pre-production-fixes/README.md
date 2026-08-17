# BASELINE SNAPSHOT — 2026-08-08, before production-readiness fixes

State of `Biped → Beni_Prototype1` and this folder immediately before the
Tier 0–3 fix programme described in
`beni_prototype1_production_readiness_findings.md`.

| file | what it is | how to restore |
|---|---|---|
| `Beni_Prototype1_BASELINE.f3d` | full parametric Fusion archive, 4.5 MB | Fusion → Upload, or File → Open, then Save As over the working doc |
| `Beni_Prototype1_BASELINE.step` | neutral B-Rep of the whole assembly, 7.2 MB | opens in anything; geometry only, no timeline |
| `baseline_metrics.json` | every occurrence + component: volume, face/edge/shell/lump counts, bbox, 4×4 transform, material, appearance, cylindrical-face radius census, all 31 user parameters | diff target — `compare_to_baseline.py` uses this |
| `beni_lib.py` | build source as it stood | — |
| `*.md` | all four documents as they stood | — |
| `print_stl_BASELINE/` | the exported STL set as it stood | — |

A named Fusion **cloud version** was also created at the same moment:
> "BASELINE 2026-08-08: state before production-readiness fixes (audit findings doc). Restore point."

Recover it from the Fusion data panel → `Beni_Prototype1` → right-click → Versions.

## Baseline facts, for quick reference

- timeline 815 entries · 156 root occurrences · 79 components · 31 user parameters
- 0 joints, 0 as-built joints, 0 rigid groups, 0 snapshots, 0 named views
- 217 extrudes, 11 revolves, 1 mirror, **0 fillets, 0 chamfers**
- all bodies mis-assigned material "Steel" → Fusion reported mass 8174.2 g
- corrected mass (by hand) 3232.2 g modelled, ≈3352 g with unmodelled electronics
- right leg missing `Knee_Axle_L`, `Knee_Sleeve_L`, `Knee_Spring_L` entirely
- `Proximal_Link_L(Mirror)` 70356.44 mm³ vs left 63093.07 mm³
- `Knee_Encoder_Bracket_L(Mirror)` 2726.12 mm³ vs left 2614.88 mm³
