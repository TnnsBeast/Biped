# Miniature pivot — research record, 2026-10-11

Owner scope: $150–250 new parts, excluding printer and owned electronics;
balancing, driving and active crouching first; preserve independent hip, knee
and wheel actuation on both sides. This is a research/planning result, not a
physical observation, Fusion audit, purchase, print release or policy result.

- [Study and decisions](../../../docs/design/miniature_wheeled_biped_study.md)
- [Published inputs and access qualifications](vendor_inputs.json)
- [Numerical source](../../../mini_biped_calc.py)
- [Reproduced output](sizing_output.txt)
- [Unit/geometry/budget checks](../../../test_mini_biped_calc.py)

Product price access differs by site: DFRobot, Pololu and GensTattu were readable live;
Waveshare official shop content was available from indexed search results while
direct fetches returned access errors. Values are displayed USD product prices,
not checked-out delivered quotes. The cost allowances have no supplier quote.
No claim of Amazon stock, delivery date or actuator authenticity is made.

The study's reference comparison distinguishes actual wheel-biped balance,
actual servo-robot RL and proposed capabilities. No third-party CAD or code
was imported. The MINI-1…8 register in the study tracks evidence still needed.

Reproduce from the repository root:

```sh
python3 mini_biped_calc.py
python3 -m unittest -v test_mini_biped_calc.py
```

The calculation uses explicitly assumed geometry/mass and vertical-force
statics, not Fusion measurements or a complete dynamic/structural model.
Its output cannot release an operating envelope. Existing ABS limits and
Fusion-only CAD verification rules remain unchanged.
