# Beni teardown evidence — actively driven knee, crank-and-link knee drive, belt stage at the hip

Source: [Beni the Camera Robot Goes Under the Knife](https://www.youtube.com/watch?v=Ds3sKpndzTA)

| Review | Method |
|---|---|
| 2026-09-25 | First reading; method not recorded. Its readings are corrected below. |
| 2026-09-27 | Frame review. 2160p60 section 5:25–10:25 and full 1080p60 video; stills at 0.5–1 s through 7:00–10:00. Captions returned HTTP 429 and were not read, and the narration was not transcribed. |

Times are YouTube playback time. The 4K section starts at 325 s, so 4K section
time + 325 s = playback time. Frames stay out of this public repository
because the video is third-party; the timestamps below reproduce every
observation.

## Observations (2026-09-27 frame review)

Each leg is the mirror of the other.

| Time | Visible |
|---|---|
| [7:55–7:57](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=475s) | A white body-side housing, retained by two screws, holds a motor end with a PCB and a small steel toothed pulley. A black toothed belt wraps that pulley and a large toothed ring coaxial with the hip. |
| [7:57](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=477s) (477.3 s) | Belt marking, read verbatim: **`GUL-TZ® 2M-210-6`**. |
| [7:58–8:01](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=478s) | A central body bracket, moulded "2", holds two small outrunner BLDC motors back to back on one lateral axis. Each motor has a PCB and a steel toothed pulley at its outboard end, and a twisted four-conductor cable. |
| [8:02–8:04](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=482s), again [8:30](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=510s) | The belt spans the body-side housing pulley and the ring at the hip end of the thigh. It is outside the thigh. |
| [8:05](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=485s), [8:38](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=518s) | Hip stack, inboard to outboard: a white spoked carrier holding a wound stator, with a centre ball bearing and shaft; the white toothed ring; a steel clamp ring with socket screws; a large thin-section ball bearing, its outer race exposed once the leg is out of the body; the thigh housing. At 8:38 one painted witness line crosses the carrier, the toothed ring and the steel clamp ring. |
| [8:06](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=486s) | Both hip stacks in the opened body with belts on the rings. Second belt marking: `104 GK23 B` / `105 GK23 B`, also legible at 9:29. |
| [8:08](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=488s) | Two heavier conductors (red, black) and two thin ones (blue, green) leave the carrier face near the axis. |
| [8:10–8:14](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=490s) | With the leg off the robot, the shin swings freely by hand, and the knee link body moves along the thigh with it. |
| [8:15–8:18](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=495s) | The access window at the hip end of the thigh shows a black crank coaxial with the hip. A pin on the crank is retained by a Torx screw, and a white link leaves the pin along the thigh. The crank angle changes relative to the thigh as the leg moves. |
| [8:33](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=513s) | Knee pin with a round cap. The shin ends in a round housing with a grey hub flange: three holes and a centre boss, tyre removed. |
| [9:15–9:25](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=555s) | Parts layout: two white box modules (battery packs by appearance), two body-shell halves, the head/torso, the central two-motor bracket, two legs with hip stacks, two belts (one per leg), the main PCB, flex cables and a remote. No other small motor is laid out. |
| [9:25–9:29](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=565s) | The link ends in an eye pinned by a screw and washer to a lever tab on the shin, offset from the knee axle. The knee axle shows a hex nut and washer in a knee window, and the wheel cable passes through the same window. |

## Interpretation

**Established.**
- No belt runs along the thigh. Each leg's only belt is the short loop at the
  hip between a body-fixed small motor and the large ring coaxial with the hip.
- The knee is driven through a four-bar: a hip-coaxial crank inside the thigh
  root, a link along the thigh, and a lever on the shin behind the knee axle.
- Two drives act about each hip axis: the large pancake BLDC and the
  belt-driven ring. The two small body motors are one per leg, not a coaxial
  hip/knee pair.

**Best-supported reading, not settled.** The belt stage drives the hip, and the
pancake motor rides on the hip assembly and turns the knee crank.
- The witness line fixes the belt-driven ring to the stator carrier and the
  bearing clamp, so the ring and the stator rotate together.
- The main bearing's outer race was exposed after removal, so it sits in the
  body. The carrier assembly is the part turning in it, and so carries the thigh.
- The alternative puts the thigh on the pancake rotor and the crank on the
  belt-driven carrier. Leg loads would then pass through the small centre
  bearing, which makes it less likely, but it is not excluded. Under it, the
  belt stage drives the knee.
- To settle it, check the narration at 8:08–8:18, or find a view showing what
  the thigh is fastened to.

**Not established.**
- Whether the link is rigid or compliant.
- All dimensions, tooth counts, ratios, motor ratings, bearing part numbers,
  joint ranges and belt tension.
- `2M-210-6` has the common profile–pitch-length–width form. Confirm it
  against a vendor listing before treating it as a dimension.

## Corrections to the 2026-09-25 reading

- **7:58, "two brushless motor bodies on the same joint axis"** — this is the
  central body bracket: one small motor per leg, on a lateral axis offset from
  the hips. Only the pancake motor lies on a hip axis.
- **8:03, "toothed belt path inside the upper leg"** — the belt is at the hip,
  between the body-fixed motor and the hip ring. No belt reaches the knee.
- **8:08–8:18, narration "a belt reduction that controls the knee"** — not
  re-verified. The frames show a crank-and-link knee drive. The narration's
  statement holds only under the alternative reading above.

## Project consequence

Beni's knee is actively driven, with its motor at the hip and body. It is not an
unactuated spring knee, so the passive cartridge and the fixed-axis cassette
stay superseded.

R2A's synchronous belt in the proximal link is a project design choice, not the
mechanism Beni uses. The comparison with a crank-and-link knee is an open
decision listed in [`PROJECT_STATUS.md`](../../../PROJECT_STATUS.md). The
teardown is architecture evidence, not a dimensional source or a part release;
R2A values come from the project's own requirements, delivered hardware and
Fusion inspection. The replacement direction is defined in
[`active_knee_revision2_plan.md`](../../../docs/design/active_knee_revision2_plan.md).
