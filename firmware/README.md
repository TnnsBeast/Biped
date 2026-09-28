# Firmware

The first implementation is the non-energizing Teensy 4.1 bench scaffold in
[`teensy_stage0/`](teensy_stage0/). It deliberately stops before any actuator
protocol. Hardware gates and the later control architecture remain canonical in
[`electronics/06_logging_and_bringup.md`](../electronics/06_logging_and_bringup.md)
and [`electronics/04_firmware.md`](../electronics/04_firmware.md).

R2A adds [`r2a/`](r2a/README.md): the hardware-free knee linkage map, software
limits and CAN node plan, with a host test. It adds no actuator command path.
