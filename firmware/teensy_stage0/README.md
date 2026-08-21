# Teensy 4.1 Stage 0 — bench only, no motors

This scaffold implements the Mode A Stage 0 gate from
[`electronics/06_logging_and_bringup.md`](../../electronics/06_logging_and_bringup.md):

- CAN1 and CAN2 at 500 kbit/s in **internal loopback**;
- BNO085 over SPI, requesting raw gyro and raw accelerometer reports at 1 kHz;
- the Teensy 4.1 onboard microSD at 256 kB/s for 10 minutes;
- fixed 256-byte binary records with sequence and drop counters.

It contains **no actuator IDs, no actuator protocol and no motor command path**.
Do not add one during Stage 0.

## Before connecting anything

1. Leave both actuators disconnected. Power the Teensy by USB only.
2. Verify the BNO085 wiring against `include/beni_stage0.h`: CS 10, INT 9,
   RESET 8, MOSI 11, MISO 12 and SCK 13. Teensy 4.1 GPIO is not 5 V tolerant.
3. Insert a blank/fresh microSD. The firmware creates the first unused file from
   `STG0_00.BIN` through `STG0_99.BIN`; it does not overwrite an old result.
4. Keep `BENI_STAGE0_CAN_INTERNAL_LOOPBACK=1`. The build deliberately fails if
   live-bus transmit is enabled.

## Build and run

```sh
cd firmware/teensy_stage0
pio run
pio run --target upload
pio device monitor
```

At the monitor prompt:

- `s` starts the 10-minute SD gate;
- `x` stops it without granting a pass;
- `?` prints counters.

A valid Stage 0 result ends with `SD gate PASS`, `dropped=0`, matching CAN
transmit/receive counts with `errors=0`, and observed raw gyro plus raw
accelerometer flags in the log. The code requests 1 kHz reports; the achieved
rate still has to be measured on the actual BNO085/Teensy pair. A compile is not
a hardware gate.

## Log record

`Stage0Record` is version 1 and exactly 256 bytes. At 1 kHz that is 256 kB/s.
The first fields are magic `BNI0`, record version, record size, sequence,
microsecond timestamp and status flags, followed by the latest raw IMU sample,
CAN counters and the dropped-record count. Unused bytes are zero and reserved
for later Stage 0 channels; changing the layout requires a new record version.
