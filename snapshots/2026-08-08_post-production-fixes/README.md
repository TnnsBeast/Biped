# REV2 SNAPSHOT — 2026-08-08, after production-readiness fixes

State of `Biped → Beni_Prototype1` and this folder after the fix programme in
`beni_prototype1_rev2_changes.md`.

Compare against `../2026-08-08_pre-production-fixes/`.

| file | what it is |
|---|---|
| `Beni_Prototype1_REV2.f3d` | full parametric Fusion archive, 5.0 MB |
| `Beni_Prototype1_REV2.step` | neutral B-Rep of the whole assembly, 7.4 MB |
| `rev2_metrics.json` | every occurrence + component: volume, face/edge/shell/lump counts, transform, **material**, appearance, cylindrical-face radius census, plus assembly mass / CoM / inertia and all 36 user parameters |
| `beni_lib.py`, `beni_export.py` | build + export source |
| `*.md` | all five documents |
| `manufacturing/` | 10 machined-part STEPs + the spec sheet |
| `sim/` | URDF + inertia JSON |
| `print_stl_REV2/` | re-exported print set |

A named Fusion **cloud version** was created at the same moment:
> "REV2 2026-08-08: production-readiness fixes -- L/R parity restored, fastener defects fixed, fillets added, tyre retention, chassis builders, physical materials + true mass properties."

## Headline deltas vs baseline

| | baseline | REV2 |
|---|---:|---:|
| Fusion-reported mass | 8174.2 g | **3290.1 g** |
| CoM known? | no | **yes** — X +6.46, Y −0.00, Z −50.57 mm |
| Inertia tensor known? | no | **yes** — Iyy 0.02508 kg·m² |
| Fillets | 0 | **41** |
| Right-leg parts missing | 3 | **0** |
| Unfittable fastener sets | 1 | **0** |
| Screws bottoming out | 2 joints | **0** |
| Parts with no builder | 4 | **0** |
| Machined-part STEP / drawings | none | **10 STEP + spec sheet** |
| URDF | none | **6-link, mass closure exact** |
| Automated audit problems | (no harness) | **0 of 5 checks** |
