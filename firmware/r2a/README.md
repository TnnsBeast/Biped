# R2A firmware support — knee linkage map, limits and CAN node plan

Header-only and hardware-free. Nothing here commands an actuator; it is the
tested arithmetic that the later Stage 2 firmware will include. The
non-energizing [`teensy_stage0/`](../teensy_stage0/) scaffold is unchanged and
still contains no actuator protocol.

| File | What it is |
|---|---|
| [`r2a_knee_linkage.h`](r2a_knee_linkage.h) | Closed-form crank angle θc(α), table lookup, inverse by bisection, knee→crank torque through N = dθc/dα, soft limits, stop angles, CAN node IDs and the CANSimple command IDs recorded in [electronics/03 §1.3](../../electronics/03_compute_and_can.md). |
| [`r2a_knee_linkage_table.h`](r2a_knee_linkage_table.h) | Generated: α 48…153° in 1° steps with θc, N and μ. Do not edit. |
| [`gen_linkage_table.py`](gen_linkage_table.py) | Regenerates the table from `r2a_calc.solve_linkage()` and the Fusion stop angles in the [digital-gate record](../../evidence/r2a/2026-09-27_digital_gate/fusion_measurements.json). |
| [`test_linkage.cpp`](test_linkage.cpp) | Host test: 120 mm rod closure at every row, inverse round trip, table against closed form, soft limits outside the bumper band, build-pose θc against Fusion (69.403°). The CAN IDs are compile-time `static_assert`s in the header. |

```sh
python3 firmware/r2a/gen_linkage_table.py
g++ -std=c++17 -Wall -Wextra -o /tmp/r2a_test firmware/r2a/test_linkage.cpp && /tmp/r2a_test
```

**The map is the CAD map.** Fusion measured θc at 11 knee angles equal to the
solver to 0.001° with pin-to-pin 120.000 mm in every pose, so the table needs
no CAD correction. Its zero is geometric: firmware must still find the
actuator's encoder offset against it (below).

**Limits.** Rigid stops at α 51.00° / 150.00° (Fusion contact). The TPU plugs
start to compress about 1–2° before each stop, so the software limits are
α 54° / 147°. Powered test limits (current, speed, range, command rate) are in
the [test traveller](../../docs/assembly/r2a_test_traveller.md), from
`r2a_calc.py` §9.

**CAN plan, bus A.** Shoulder GIM6010-8 stays at the factory default node 0;
the knee GIM6010-8 becomes node 1 before it joins the bus, so its heartbeat is
`(1 << 5) | 0x001 = 0x021`. The procedure is in the traveller. Bus B carries
the wheel SDC101, whose protocol is still unpublished (B2).

**Not implemented, and why.** No payload packer: the Set_Axis_Node_ID,
Set_Axis_State, limit-setting and MIT (0x008) payloads and scalings are not
recorded in the repository (B3), and nothing is guessed. No homing: whether the
GIM6010-8 encoder reads the rotor or the output is still open, so the
AS5048A (bracket on hold) or a known stop contact must supply the absolute
knee reference.
