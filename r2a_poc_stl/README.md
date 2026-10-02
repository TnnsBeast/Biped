# R2A proof-of-concept print files — all-printed, unpowered

Released 2026-09-29 from Fusion `Beni_R2A_SingleLeg` by
[`r2a_poc_fusion.py`](../r2a_poc_fusion.py). These are the printed stand-ins
for every purchased R2A part, so the owner can build the complete R2A single
leg from **owned hardware plus prints only** and prove the mechanics by hand
before ordering anything. The build and the demonstration are in the
[POC guide](../docs/assembly/r2a_poc_guide.md).

Every file is bed-ready: **import it unchanged — do not rotate, scale or
mirror it**, and do not compensate holes. Only left-hand parts exist.

**Scope (CLAUDE.md rule 7):** ABS, hand-driven kinematics and fit only. No
power, no spring, no preload, no added mass, no load beyond the leg's own
weight and a gentle hand.

The POC also uses the released article parts **unchanged**
([`r2a_stl/`](../r2a_stl/README.md)): both proximal halves, crank, two crank
caps, distal link, lever cap, encoder arm, knee-pin cap, four TPU plugs and
the article coupons 1–3. `R2A_Encoder_Bracket_L` stays on hold; the POC
protractor uses its two inserts.

Release evidence (contracts, print audit, mesh fidelity, sweep, paths) is in
[`evidence/r2a/2026-09-28_poc/`](../evidence/r2a/2026-09-28_poc/README.md).
Hashes are pinned in [`r2a_poc_release_baseline.json`](../r2a_poc_release_baseline.json)
and checked by `python3 verify_r2a_poc_release.py` (also in CI).

## Slicer profile

The tuned enclosed ABS profile of the article: **0.20 mm layers, 4 walls,
5 top / 5 bottom, 30 % infill.** **No supports on any POC file**: the Fusion
print audit found no face that needs one (bridges ≤ 12 mm over pocket
ceilings, 45° chamfers, one 1.4 mm counterbore ledge). Do not drill, sand,
file or heat-fit a failed fit: record it and stop.

## Print order

**Owner status, reported 2026-10-02:** the complete 23-piece P1 batch is
printed; acceptance tests remain pending.
[Print record](../evidence/r2a/2026-10-02_p1_printed/README.md).

**Batch P1 — coupons first.** Every printed-on-printed fit of the POC is on
these. Coupons cut from a part are cut from its reviewed B-Rep, so they print
the interface on the same build axis as the part (rule 12). Print the article
coupons 1–3 from [`r2a_stl/`](../r2a_stl/README.md) in the same batch.

| # | File | Qty | On the bed | Tests |
|---:|---|---:|---|---|
| P1 | [`POC_Clevis_Pin_D4p75x18_ABS_ON_END.stl`](POC_Clevis_Pin_D4p75x18_ABS_ON_END.stl) | 4 | On end | The pins themselves, in the article's `R2A_COUPON_Pin_Dowel_Ladder` Ø5.15 station |
| P2 | [`POC_COUPON_Rod_Eye_ABS.stl`](POC_COUPON_Rod_Eye_ABS.stl) + [`POC_Eye_Thrust_Washer_D11x1p5_ABS.stl`](POC_Eye_Thrust_Washer_D11x1p5_ABS.stl) | 1 + 6 | Flat / on face | Pushrod eye and two thrust washers in the article's `R2A_COUPON_Crank_Clevis` with a crank cap |
| P3 | [`POC_COUPON_Mock_Rotor_Stub_ABS.stl`](POC_COUPON_Mock_Rotor_Stub_ABS.stl) | 1 | Output face down | Mock output: 3 dowel sockets, 6 M3 insert receivers, journal; with the article's `R2A_COUPON_Crank_Register` |
| P4 | [`POC_COUPON_Mock_Housing_Ring_ABS.stl`](POC_COUPON_Mock_Housing_Ring_ABS.stl) | 1 | Mount face down | Journal bore on the rotor stub, thrust face, 5 insert bosses |
| P5 | [`POC_COUPON_Bushing_Seat_ABS.stl`](POC_COUPON_Bushing_Seat_ABS.stl) + [`POC_Knee_Bushing_OD18p90_ID10p60_ABS_ON_END.stl`](POC_Knee_Bushing_OD18p90_ID10p60_ABS_ON_END.stl) | 1 + 3 | Hub face down / on end | The released Ø19.15 seat and lip (cut from the inboard half) with a printed bushing and the steel Ø10 pin |
| P6 | [`POC_COUPON_Tyre_Gauge_Lip_ABS.stl`](POC_COUPON_Tyre_Gauge_Lip_ABS.stl) | 1 | Lip down | Gauge bore and lip on the owned no-tyre shell |

**Batch P2 — POC parts, after batch P1 passes.** Print the article parts
(batch 2 of [`r2a_stl/`](../r2a_stl/README.md)) alongside.

| File | Qty | On the bed | Bed footprint × height |
|---|---:|---|---|
| [`POC_Knee_Actuator_Mock_Housing_L_ABS_MOUNT_FACE_DOWN.stl`](POC_Knee_Actuator_Mock_Housing_L_ABS_MOUNT_FACE_DOWN.stl) | 1 | Mount face (y 91.1) | 81.4 × 81.4 × 25.0 mm |
| [`POC_Knee_Actuator_Mock_Rotor_L_ABS_OUTPUT_FACE_DOWN.stl`](POC_Knee_Actuator_Mock_Rotor_L_ABS_OUTPUT_FACE_DOWN.stl) | 1 | Output face (y 87.6) | 46.0 × 46.0 × 31.6 mm |
| [`POC_Knee_Actuator_Mock_Knob_L_ABS_OUTER_FACE_DOWN.stl`](POC_Knee_Actuator_Mock_Knob_L_ABS_OUTER_FACE_DOWN.stl) | 1 | Outer face (y 128.0) | 62.8 × 56.0 × 11.8 mm |
| [`POC_Knob_Lock_Pin_ABS_HEAD_DOWN.stl`](POC_Knob_Lock_Pin_ABS_HEAD_DOWN.stl) | 2 | Head down | Ø8 × 18.9 mm |
| [`POC_Pushrod_L_ABS_FLAT.stl`](POC_Pushrod_L_ABS_FLAT.stl) | 1 | Flat, 5.0 mm | 108.5 × 96.8 × 5.0 mm (diagonal on the bed) |
| [`POC_Washer_M2p5_2p0_ABS.stl`](POC_Washer_M2p5_2p0_ABS.stl) | 8 | On face | Ø5.6 × 2.0 mm |
| [`POC_Knee_Protractor_L_ABS_FLAT.stl`](POC_Knee_Protractor_L_ABS_FLAT.stl) | 1 | Flat, 6.0 mm, scale up | 100 × 100 × 6.0 mm |
| [`POC_Tyre_Gauge_Ring_D110_ABS_LIP_DOWN.stl`](POC_Tyre_Gauge_Ring_D110_ABS_LIP_DOWN.stl) | 1 | Lip down | Ø110 × 37.0 mm |
| [`POC_Feeler_4p0_5p0_ABS_FLAT.stl`](POC_Feeler_4p0_5p0_ABS_FLAT.stl) | 1 | Flat | 60 × 12 × 5.0 mm (notched corner = 4.0 end) |

The clevis pins, thrust washers and bushings of batch P1 are the parts: print
the quantities above once and use the ones that passed.

## Design choices the coupons confirm

Every value below is a **design choice**, not a measured fit. The reasoning
starts from the owner's recorded ABS results: printed holes run under nominal
(Ø19.15 light-presses a Ø19.00 bearing, Ø10.25–10.30 firm-thumb-presses the
Ø10.00 steel pin, Ø4.25 presses a Ø4 dowel, Ø4.5 takes the M3 × 5 insert); the
printed-shaft side has no recorded result, so each allowance covers both.

| Fit | Values | Wanted |
|---|---|---|
| Clevis pin in the released Ø5.15 holes and in the Ø5.15 pushrod eye | pin Ø4.75 | Free slip; slight play accepted |
| Mock journal | shaft Ø36.0 in bore Ø36.6; thrust gaps 0.1 each side | Turns freely by fingertip, no bind over full turns |
| Knob pilot | Ø16.0 in Ø16.6 | Slides on by hand |
| Knob key and lock | owned Ø4 × 10 dowel pressed in Ø4.25, slip in Ø4.30; lock pin Ø3.8 in Ø4.30 | Press / slip as on the root dowels |
| Mock output pins | owned Ø4 × 10 dowels in Ø4.25 × 6.5 sockets opening at the bed, 0.4 mm entry chamfer; 3.5 mm proud like the factory pins | Firm press, square, no whitening |
| M3 inserts in the mock | Ø4.5 × 6.0 receivers opening at the bed face; housing receivers in Ø9.0 bosses | Flush, square, no bulge into a neighbour |
| Knee bushing | OD 18.90 in the released Ø19.15 seat; bore Ø10.60 on the steel pin | Seats by thumb, does not turn; pin turns freely |
| Tyre gauge | bore Ø96.4 on the Ø96 no-tyre drum | Slides on by hand, stays where put |

## Acceptance tests

By hand, without measuring unless stated. Record each result as a dated
observation in `evidence/`. Stop at the first failure; a failed fit is a
re-release, never a rework.

**P1 — clevis pins.** Each printed pin passes the ladder coupon's **Ø5.15**
station by hand without force; note the smallest station it passes. Slight
play is acceptable for the POC. A pin that does not pass Ø5.15 holds batch P2
for a pin re-release. Also press an owned Ø4 × 10 dowel into the Ø4.25 plate
hole and socket as the article traveller says.

**P2 — pushrod eye.** Press two dowels into `R2A_COUPON_Crank_Clevis`, stack a
thrust washer, the rod-eye coupon and a second washer in the gap, press the
crank cap on and slide a printed pin in from the cap side. The eye swings
through its whole neck relief without touching an ear; the stack has slight
end float (0.2 mm per side in CAD); the pin withdraws by hand.

**P3 + P4 — mock output and journal.** Press three dowels into the rotor
stub's sockets from its output face until they bottom (3.5 mm proud); only
then fit two M3 inserts (the dowels support the 1.9 mm wall between a
receiver and a socket). Fit one or two inserts in the housing ring's bosses.
Stand the ring on the stub:
- it turns freely by fingertip through several full turns, no tight spot;
- the article's crank-register coupon sits flat over the three dowels with
  no rock, and two M3 × 10 into the stub's inserts clamp it before any screw
  bottoms (1.0 mm to the floor in CAD).

**P5 — bushing seat.** A printed bushing enters the coupon's Ø19.15 seat by
thumb pressure until it stops on the Ø17 lip and does not turn by hand. The
steel Ø10 pin passes the bushing and turns freely, with no bind; slight play
is acceptable.

**P6 — tyre gauge lip.** The lip coupon slides onto the owned no-tyre shell's
drum from outboard by hand until the lip meets the drum end, and stays put.

**Batch P2 detached checks:** rotor into the housing turns freely; knob
seats on the pilot over the key; the lock pin drops through the knob boss
into each of the five dial holes; the protractor sits flat on the outboard
half over its two inserts.

## Assembly status

**`CAD PATH VERIFIED`** — 34 of 34 POC insertion, tool and service paths, and
the lock pin at all five check points
([`assembly_paths.json`](../evidence/r2a/2026-09-28_poc/assembly_paths.json)).
**Not physically rehearsed.**
