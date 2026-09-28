# Beni

![R2A single leg on the Mode A stand, rendered from the live Fusion model](docs/readme/r2a_leg_iso.png)

A mostly 3D-printed wheeled biped. **Active-Knee Revision 2 (R2A)** gives each
leg three actuators: the shoulder GIM6010-8, a second GIM6010-8 coaxial with
the shoulder that drives the knee through a Beni-style crank and pushrod, and
the GIM4305-10 wheel. The single-leg ABS article is designed, CAD-verified and
released for printing; nothing about it has been built or tested yet.

**[Current status](PROJECT_STATUS.md)** · **[R2A plan](docs/design/active_knee_revision2_plan.md)** · **[Print files](r2a_stl/README.md)** · **[Ordering guide](procurement/r2a_ordering_guide.md)** · **[Assembly guide](docs/assembly/r2a_assembly_guide.md)** · **[Test traveller](docs/assembly/r2a_test_traveller.md)** · **[CAD evidence](evidence/r2a/2026-09-27_digital_gate/README.md)** · **[Electronics](electronics/README.md)** · **[Firmware](firmware/README.md)**

## Where R2A stands

- **CAD:** Fusion `Beni_R2A_SingleLeg` holds the complete leg. A 140-pose
  sweep of knee and shoulder shows no real clash; 33 insertion, tool and
  service paths are `CAD PATH VERIFIED`; stops at α 51° / 150° are measured.
- **Linkage:** crank 32 mm, pushrod 120 mm, lever 30 mm; knee range α 51…150°,
  a 128.5 mm leg-length stroke ([`r2a_calc.py`](r2a_calc.py)).
- **Print:** three fit coupons first, then nine article parts, all ABS except
  four TPU stop plugs. One part, the AS5048A bracket, is on hold.
- **Buy:** one knee GIM6010-8, M5 rod ends, rod and jam nuts, Ø5 × 18 pins,
  and a few small items. Prices and vendors are not confirmed.
- **Not yet done:** printing, the physical assembly rehearsal and the three
  test gates. No physical result exists for any R2A part.

## The R2A leg

| On the stand, outboard | Knee | Crank on the knee actuator |
|:---:|:---:|:---:|
| <img src="docs/readme/r2a_leg_outboard.png" alt="R2A leg from outboard on the Mode A stand" width="420"> | <img src="docs/readme/r2a_knee_detail.png" alt="Knee: lever cap, lower rod end and knee pin" width="420"> | <img src="docs/readme/r2a_crank_detail.png" alt="Crank on the knee actuator output inside the proximal link" width="420"> |

The linkage at the flexion stop, the build pose and the extension stop, seen
from outboard with the outboard half and knee actuator hidden:

| α = 51° | α = 80° | α = 150° |
|:---:|:---:|:---:|
| <img src="docs/readme/r2a_linkage_a051.png" alt="Linkage at the flexion stop" width="380"> | <img src="docs/readme/r2a_linkage_a080.png" alt="Linkage at the build pose" width="380"> | <img src="docs/readme/r2a_linkage_a150.png" alt="Linkage at the extension stop" width="380"> |

The images are exported from the live Fusion model by
[`r2a_images_fusion.py`](r2a_images_fusion.py) through the Fusion MCP. Refresh
them only after a verified model change.

## Why the knee changed

The legacy passive knee used an axial compression spring. On the printed ABS
article the spring bowed, twisted and escaped sideways
([failure record](evidence/assembly/2026-09-24_spring_escape/)). A frame review
of a public Beni teardown showed its knee driven from the hip through a crank
and link ([evidence](evidence/reference/2026-09-25_beni_teardown/)). R2A copies
that: the knee actuator's weight stays on the shoulder axis, the knee angle is
referenced to the proximal link, and the proven shoulder, knee-pin and wheel
interfaces carry over.

## Legacy passive-knee baseline

The legacy Fusion documents `Beni_Prototype1` and `Beni_SingleLegRig` are
preserved unchanged, and the assembled legacy ABS article stays spring-free
and unpowered as fit and failure evidence. Its design records, assembly
manuals and archived print files start from
[`PROJECT_STATUS.md`](PROJECT_STATUS.md#legacy-single-leg-rig--physical-evidence-baseline);
the legacy CAD views are in [`docs/readme/`](docs/readme/).

---

<!-- PRINT_QUEUE_START -->
## Current print queue — R2A single-leg ABS article

Automatically maintained convenience section for the active build. Branch
`r2a-active-knee`, released 2026-09-27. Import every file **unchanged**: it is
already in its print orientation. Profile: enclosed ABS, 0.20 mm layers,
4 walls, 5 top / 5 bottom, 30 % infill; no hole compensation.

**Print the three coupons first** and test them on the real hardware before
anything else:

1. [Pin and dowel ladder](https://raw.githubusercontent.com/TnnsBeast/Biped/r2a-active-knee/r2a_stl/R2A_COUPON_Pin_Dowel_Ladder_ABS.stl) — 1 × ABS, flat, no supports. Pass: a Ø5 × 18 pin slides through the Ø5.15 hole by hand with no rock; a Ø4 × 10 dowel presses into the Ø4.25 holes without splitting and stays in.
2. [Crank register coupon](https://raw.githubusercontent.com/TnnsBeast/Biped/r2a-active-knee/r2a_stl/R2A_COUPON_Crank_Register_ABS.stl) — 1 × ABS, output face down, no supports. Pass on the knee GIM6010-8: sits flat over the three factory pins with no rock, and six M3 × 10 clamp it before any screw bottoms.
3. [Crank clevis coupon](https://raw.githubusercontent.com/TnnsBeast/Biped/r2a-active-knee/r2a_stl/R2A_COUPON_Crank_Clevis_ABS.stl) + [crank cap](https://raw.githubusercontent.com/TnnsBeast/Biped/r2a-active-knee/r2a_stl/R2A_Crank_Cap_L_ABS_OUTER_FACE_DOWN.stl) — 1 × ABS each, no supports. Pass with a purchased rod end: the ball floats slightly in its gap and swivels freely; the Ø5 pin slides in and out by hand.

**Then the article**, after the coupons pass — 1 × ABS each unless stated:

| File | Supports |
|---|---|
| [Proximal inboard half](https://raw.githubusercontent.com/TnnsBeast/Biped/r2a-active-knee/r2a_stl/R2A_Prox_Inboard_L_ABS_Y59p5_DOWN.stl) | None |
| [Proximal outboard half](https://raw.githubusercontent.com/TnnsBeast/Biped/r2a-active-knee/r2a_stl/R2A_Prox_Outboard_L_ABS_Y91p1_DOWN.stl) | None |
| [Crank](https://raw.githubusercontent.com/TnnsBeast/Biped/r2a-active-knee/r2a_stl/R2A_Crank_L_ABS_OUTPUT_FACE_DOWN.stl) | None |
| [Crank cap](https://raw.githubusercontent.com/TnnsBeast/Biped/r2a-active-knee/r2a_stl/R2A_Crank_Cap_L_ABS_OUTER_FACE_DOWN.stl) (the second of two) | None |
| [Distal link](https://raw.githubusercontent.com/TnnsBeast/Biped/r2a-active-knee/r2a_stl/R2A_Distal_Link_L_ABS_Y59p5_DOWN.stl) | **Painted only** under the knee webs (6.3 mm), receiver annulus (5.8 mm), wheel-end underside (5.0 mm) and open-channel ceiling (25.0 mm); ≥ 0.4 mm Z and 0.6 mm XY gap; none in any bore, the motor opening or the motor face |
| [Lever cap](https://raw.githubusercontent.com/TnnsBeast/Biped/r2a-active-knee/r2a_stl/R2A_Lever_Cap_L_ABS_OUTER_FACE_DOWN.stl) | None |
| [Encoder arm](https://raw.githubusercontent.com/TnnsBeast/Biped/r2a-active-knee/r2a_stl/R2A_Encoder_Arm_L_ABS_TOP_FACE_DOWN.stl) | None |
| [Knee-pin cap](https://raw.githubusercontent.com/TnnsBeast/Biped/r2a-active-knee/r2a_stl/R2A_Knee_Pin_Cap_L_ABS_OUTER_FACE_DOWN.stl) | None |
| [TPU stop plug](https://raw.githubusercontent.com/TnnsBeast/Biped/r2a-active-knee/r2a_stl/R2A_Knee_Bumper_TPU95A_D6x4.stl) — **4 × TPU 95A**, on end, 100 % infill | None |

Acceptance, by hand: each 6800-2RS seats squarely by thumb with no rock; the
steel Ø10 pin enters the distal receiver by firm thumb pressure and withdraws
by hand; the halves meet at the wall tops without force. Full tests:
[print traveller](r2a_stl/README.md#acceptance-tests).

**On hold:** `R2A_Encoder_Bracket_L`, until the AS5048A adapter-board outline
is known. **Retired:** every legacy spring, cartridge, stop-plate and link
print. Reused as printed: shoulder hub, shoulder plate, cable cover, stand,
cable post, wheel hub and no-tyre shell.
<!-- PRINT_QUEUE_END -->
