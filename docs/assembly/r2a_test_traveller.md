# R2A test traveller — gates 2 to 4 (ABS single-leg article)

The gates are defined in the [R2A plan](../design/active_knee_revision2_plan.md)
§10; this document is the procedure. Gate 1, the Fusion digital gate, is
closed ([evidence](../../evidence/r2a/2026-09-27_digital_gate/README.md)).
Record every result as a dated observation under `evidence/`, with the log
file for every powered run ([electronics/06](../../electronics/06_logging_and_bringup.md)).
Nothing here has been run.

## Rules for every gate

- **ABS article, self-weight only** (CLAUDE.md rule 7): wheel clear of
  everything, no ground contact, no added mass, no torque arm, no stall, no
  drop. The stand is clamped with the leg overhanging a bench edge
  ([assembly guide §0](r2a_assembly_guide.md#0-before-you-start)).
- **Backdrive only with every actuator lead unplugged.** The brake chopper is
  deferred, so a powered actuator, idle or enabled, must never be moved by hand
  or allowed to fall under gravity. Enable a hold before letting go of a
  powered joint.
- **Stop the gate** at any bind, rod-end play beyond its specification,
  cracked or whitened print, stop bypass, encoder disagreement, unexpected
  current, CAN error, smell or noise. Do not rework a print; record and hold.
- **The wheel stays disconnected.** The CAN protocol of its GDZ34 driver is not confirmed (B2).

### Limits

Chosen for the ABS article (DESIGN CHOICE); the consequences are printed by
`python3 r2a_calc.py` §9 and are copied here:

| Limit | Gate 3 (detached) | Gate 4 (on the leg) |
|---|---|---|
| Bus | 20 V bench supply (B1) | same |
| Supply current limit | 1.0 A (fault limiter) | 1.0 A |
| Knee actuator current limit | **1.0 A** = 0.47 N·m output | **3.0 A** = 1.41 N·m output; the self-weight hold bound is 1.47 A |
| Shoulder actuator | unpowered, CAN disconnected | **3.0 A**; hold bound 1.49 A within 30° of hanging |
| Speed | ≤ 0.078 turn/s at the knee output | knee ≤ 30°/s (output ≤ 0.078 turn/s); shoulder ≤ 0.083 turn/s |
| Range | ±20° of crank about mid-pocket | knee α 54…147° (software limits); shoulder within ±30° of hanging |
| Command rate | ≤ 100 Hz per node | ≤ 100 Hz per node, bus A at 500 kbit/s: 10.8 % worst load |

At the gate 4 knee limit the rod force is ≤ 63 N and a drive into the flexion
stop gives ≤ 44 N at the stop face, against the 761 N design rod force and
347 N stall-into-stop case of the PA-CF design (`r2a_calc.py` §5).

Current and speed limits are set with the vendor configuration tool (or the
CANSimple limit commands 0x00F…0x011 once their payloads are confirmed from the
Steadywin manual) and **read back before the axis is enabled**. The repository
records the command IDs only ([electronics/03 §1.3](../../electronics/03_compute_and_can.md));
no payload layout is guessed.

## Gate 2 — unpowered linkage

Preconditions: the assembly guide complete through step 13; every actuator
lead unplugged; stand clamped at the bench edge.

1. **Knee sweep by hand**, shoulder held hanging. Move the distal link slowly
   from mid-range to the flexion stop and to the extension stop, ten times.
   - Pass: smooth, no catch or grinding; the TPU plugs touch about 1–2° before
     each rigid stop; the rigid faces then meet squarely.
   - Watch the tight running gaps from CAD: crank to the proximal halves
     0.8 mm, distal link to the cheeks 0.5 mm, encoder arm 0.5 mm. No rubbing
     sound, no witness marks.
   - At the extension stop, look for contact between the upper jam nut / rod
     and the crank: CAD clearance there is 1.95 mm, the tightest joint-internal
     gap. Any witness mark fails the gate.
2. **Rod ends.** Each ball has slight end float in its clevis and swivels
   freely through the sweep; no housing or neck touches a clevis ear.
3. **Flexion-stop clearance.** At the flexion stop the wheel shell stands clear
   of the proximal link (CAD tyre gap 5.49 mm).
4. **Shoulder by hand** through ±120° at knee angles near both stops and mid
   range: the three cables stay slack in the service loop, nothing pinches at
   the root exit, the knee-pin cap loop or the duct entries.
5. **After the cycles:** both Ø5 pins still captive, knee pin seated, caps
   seated, no crack or whitening anywhere, perimeter and hub screws still snug.

Pass all five, or stop. The plan's linkage-map check with the AS5048A is
deferred: the encoder bracket is on hold, so the map is checked in gate 4
against the knee actuator's encoder and the stop gaps at the software limits.

## Gate 3 — detached knee drive

Set up on the bench: the knee actuator on the outboard half (assembly steps
2–4) with the crank fitted and the pushrod on its crank pin, lower end free;
the outboard half clamped flat; the shoulder actuator not connected.

1. **Crank pocket ends.** Unplugged, turn the crank by hand from one wall of
   the outboard half's crank pocket to the other; note both ends and leave the
   crank in the middle.
2. **Set the new actuator's CAN node ID to 1**, before it ever shares a bus
   with the shoulder unit (both leave the factory as node 0):
   1. Only the knee actuator on bus A; power at 20 V, 1.0 A limit.
   2. Its heartbeat arrives at CAN ID **0x001** (`(0 << 5) | 0x001`).
   3. Send **Set_Axis_Node_ID (0x006)** to node 0 with the new ID 1, using the
      vendor tool or the payload from the Steadywin manual (**TO CONFIRM**; not
      in the repository).
   4. Send **Save_Configuration (0x01F)** to node 1, CAN ID **0x03F**.
   5. Power-cycle. Pass: heartbeat at **0x021** (`(1 << 5) | 0x001`) and
      nothing at 0x001. Label the actuator "KNEE — node 1".
3. **Configure and read back** the gate 3 limits. Confirm the bus bitrate the
   unit reports.
4. **Encoder test (open item: rotor or output?).** Read the reported output
   position. Power off, unplug, turn the crank by hand about 60° from
   mid-pocket (more than the 45° of output per rotor turn at 8:1, and at least
   10° short of the pocket wall), reconnect and power on. If the reading moved
   by about 60°, the encoder resolves the output across power cycles. Any other
   change, for example about 15° (60° − 45°) or about 120° (8 × 60° modulo
   360°), means it is rotor-referenced and the knee needs a reference at every
   power-up. Record which. Power off, unplug, and turn the crank back to
   mid-pocket by hand.
5. **Enable a position hold** at the present position, then command moves of
   ±5°, ±10° and ±20° of crank about it at ≤ 0.078 turn/s.
   - Pass: the crank moves the commanded way by the commanded amount (by eye
     against the pocket), settles without oscillation, and reported current
     stays well below the 1.0 A limit.
   - Record the sign convention: which command direction flexes the knee
     (θc increases with α; [firmware map](../../firmware/r2a/README.md)).
6. **Stop behaviour:** a zero command, Estop (0x002) and switching the supply
   output off each stop the crank promptly. After an Estop, Clear_Errors
   (0x018) and re-enable work. If the driver offers a CAN-timeout watchdog,
   enable it and confirm that stopping the Teensy's traffic idles the axis.
7. **Phase resistance** with a milliohm meter, if available (open item C7).

Pass 2–6 (7 is a measurement), or stop.

## Gate 4 — wheel-clear single leg

Preconditions: gates 2 and 3 passed; the knee module back on the leg; both
GIM6010-8 on bus A (shoulder node 0, knee node 1) at 500 kbit/s; the wheel
disconnected; the stand clamped at the bench edge.

1. **Knee reference (every power-up until the AS5048A is fitted).** Unplugged,
   press the distal link gently against the **flexion stop** until the rigid
   faces meet over the compressed TPU plugs (Fusion contact α = 51.00°). Hold
   it there, connect and power both actuators, and **enable the knee hold at
   the present position**, then the shoulder hold, before letting go. Record
   the knee reading as the α = 51.00° reference; commands are then
   `θc(α) − θc(51.00°) + reference` from the firmware map. First command:
   α = 54° (the flexion software limit).
2. **Both heartbeats** (0x001 and 0x021), no errors; read back the gate 4
   limits on both axes.
3. **Knee map check.** Command α = 60°, 80°, 100°, 120°, 140° and **147°**
   (the extension software limit) at ≤ 30°/s, pausing at each, then return to
   100°. The map is checked end to end at 147°, 96° of knee from the
   reference: CAD puts the extension TPU plugs 0.57 mm from the distal stop
   face there, and the rigid faces 1.44 mm apart (`r2a_calc.py` §9; the plugs
   engage 1.91° before rigid contact).
   - Pass: at 147° a strip of paper slides between each extension plug and
     the stop face, and the rigid faces are visibly apart. The same holds at
     54° on the flexion side (plug gap 0.57 mm, rigid gap 1.54 mm).
   - Fail: a compressed plug or touching faces (the map, the rod length or the
     reference is off by more than about 1°), a gap of several millimetres,
     held current at the 3.0 A limit, any bind or noise.
4. **Soft limits.** Command 1° past each software limit (53°, 148°): the
   firmware must refuse; the knee stays at 54° / 147°. Nothing in this gate
   drives into a stop under power.
5. **Shoulder.** With the knee holding at 100°, command shoulder moves of ±5°,
   ±15° and ±30° from hanging at ≤ 0.083 turn/s. Pass: correct direction,
   settles, cables slack, current below 3.0 A.
6. **Stops and faults** as gate 3 step 6, now for both axes, with the leg
   supported by hand under the distal link before any stop that idles an axis.
7. **Soak and latency.** The electronics/06 Stage 2 gate asks for a 1-hour
   soak at 1 kHz with no CAN errors and < 8 ms end-to-end latency. Two nodes
   at 1 kHz need bus A at 1 Mbit/s (54.0 % worst; 108.0 % at 500 kbit/s,
   `r2a_calc.py` §6), or one GIM6010-8 per bus with a third CAN Pal. Choose one,
   record it, and run the soak with the leg holding still at α = 100°.

Pass 1–7, or stop. Passing gate 4 does not release any structural, ground,
jump or PA-CF test.
