# Beni mechanical research — evidence, interpretation and remaining questions

Source: [Beni the Camera Robot Goes Under the Knife](https://www.youtube.com/watch?v=Ds3sKpndzTA)

Owner's October 12 reference: [We Cracked Beni Open!](https://www.youtube.com/shorts/p3SAWH4o9yc).
The Short links to the full teardown above; it is not independent corroboration.

| Review | Method |
|---|---|
| 2026-09-25 | First reading; method not recorded. Its readings are corrected below. |
| 2026-09-27 | Frame review. 2160p60 section 5:25–10:25 and full 1080p60 video; stills at 0.5–1 s through 7:00–10:00. Captions returned HTTP 429 and were not read, and the narration was not transcribed. |
| 2026-10-12 | Opened both videos in the browser; exported the full English auto-generated captions after video loading, and inspected paused frames at 7:57, 8:12 and 8:22. Reviewed the additional online sources below. |

Times are YouTube playback time. The 4K section starts at 325 s, so 4K section
time + 325 s = playback time. Frames stay out of this public repository
because the video is third-party; the timestamps below reproduce every
observation.

## October 12 narration check

The presenter identifies an early engineering prototype and qualifies his
explanation as a hobbyist interpretation at
[0:00–0:23](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=0s).
The description discloses Mondo sponsorship. Captions are not engineering drawings.

| Playback time | Captioned explanation — reported, not independently measured |
|---|---|
| [7:51–8:06](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=471s) | The belt drives the hip's outer assembly, supported by a large bearing. |
| [8:06–8:18](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=486s) | The concentric inner motor drives the knee through an unspecified reduction. |
| [8:18–8:37](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=498s) | The presenter calls the mechanism a “spring-loaded linkage” and attributes energy storage to the spring. |

The spring's attachment, force path and parameters are not exposed clearly
enough to distinguish series compliance from parallel assistance.
The transcript and screenshots remain outside the public repository.

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
- The visible belt is the short loop at the hip between a body-fixed small
  motor and the large ring coaxial with the hip; no belt is visible down the thigh.
- The knee has a hip-coaxial crank inside the thigh root, a link along the
  thigh, and a lever on the shin behind the knee axle. A rigid four-bar is an
  idealization until the link's compliance is established.
- Two drives act about each hip axis: the large pancake BLDC and the
  belt-driven ring. The two small body motors are one per leg, not a coaxial
  hip/knee pair.

**Best-supported reading; now consistent with the captioned explanation above.**
The belt stage drives the hip, and the pancake motor rides on the hip assembly
and turns the knee crank. The stator-to-thigh fastening still needs direct evidence.
- The witness line fixes the belt-driven ring to the stator carrier and the
  bearing clamp, so the ring and the stator rotate together.
- The main bearing's outer race was exposed after removal, so it sits in the
  body. The carrier assembly is the part turning in it, and so carries the thigh.
- The alternative puts the thigh on the pancake rotor and the crank on the
  belt-driven carrier. Leg loads would then pass through the small centre
  bearing, which makes it less likely, but it is not excluded. Under it, the
  belt stage drives the knee.
- The October 12 narration check supports this assignment. A fastening view
  would independently establish the mechanical constraints.

**Not established.**
- The compliance topology: the narration reports a spring, but the frame review
  does not establish where it acts or whether the link changes length.
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
- **8:08–8:18, earlier attribution of a belt reduction to the knee** — corrected
  by the October 12 narration check above. The internal knee reduction remains
  unspecified.

## Additional online sources reviewed October 12

These have different evidential roles. Repeated press descriptions do not
constitute additional teardown observations.

| Source | Useful evidence and limits |
|---|---|
| [Developer account's RL engineering write-up](https://www.reddit.com/r/MondoRobotics/comments/1szuepv/our_rl_journey_so_far_what_we_learned_what_broke/) | `u/lanyusea` reports replacing bought prototype actuators with supplier-customized RS485 drives, improving current/torque behavior and communication consistency. Reports position targets into local PD control. The author's follow-up emphasizes predictable latency. These are developer reports, not actuator specifications or a benchmark. |
| [Same account's Beni launch discussion](https://www.reddit.com/r/robotics/comments/1uti96j/im_glad_to_share_the_little_robot_we_designed/) | Connects the engineering account to Beni and links the RL write-up. SDK/framework release is described as future work after shipping; this does not establish available Beni source or hardware drawings. |
| [Mondo product specification](https://www.mondorobotics.com/products/beni-camera-robot) | Published whole-robot weight **1.75 kg** and envelope **21.5 × 18 × 18 cm**. These do not give link lengths, joint torque, gear ratio, spring data or an actuator BOM. Do not scale the miniature from the product envelope. |
| [Mondo development history](https://www.mondorobotics.com/pages/about-us) | Describes successive prototypes and beta units. Treat the opened prototype as a dated configuration; a shared product name does not prove identical internals. |
| [Mondo-Robotics/PMT](https://github.com/Mondo-Robotics/PMT) and [robot-extension documentation](https://github.com/Mondo-Robotics/PMT/blob/main/docs/USAGE.md) | Public training framework with G1 examples; extension documentation says the robot axis ships G1. It is not evidence that Beni CAD, a Beni actuator model or a Beni policy has been published there. |

Searches for Beni/Mondo mechanical drawings, motor specifications and patents
did not identify a usable Beni mechanism disclosure in this pass. This is a
search limit, not evidence that no filing or drawing exists. Unrelated patents
returned for the name Beni were excluded. The Kickstarter page was reachable
but did not expose a usable internal mechanism specification to the reader.

## Mechanical questions that still matter

The following are investigation requirements, not newly inferred Beni facts.

| Question | Evidence needed | Why it changes our design |
|---|---|---|
| What is fixed to the body, thigh, stator and rotor? | Exploded fastening view or independent motion with those four bodies marked | Establishes the actuator coordinate frames and reaction-torque paths. Coaxial appearance alone is insufficient. |
| What is inside the knee reduction? | Opened reducer, tooth counts and output attachment | Determines motor-to-crank ratio, backlash, reflected inertia and backdrivability. A rotating external ring does not identify the internal reducer. |
| Is the spring in series, in parallel, or part of a stop? | Both spring attachments; crank held while shin moves; link-length change versus joint angle | Determines whether motor position uniquely determines knee position, whether a separate output sensor is needed, and how impact reaches the gearbox. |
| What constrains the spring? | Guide, containment, end seats, travel stops and behavior across the stroke | A spring concept without a constrained load path repeats the failure mode of our retired article. |
| Where do transverse loads go? | Bearing supports and spans, shaft retention and structural attachment views | A motor torque rating says nothing about allowable wheel/leg bending loads. |
| What does the linkage do across the stroke? | Joint-centre geometry, branch, stops and transmission Jacobian | Establishes torque/speed conversion and singularities; a four-bar is not a constant reduction. |
| How do wheel and hip cables survive motion? | Harness routing and actual mechanical rotation limits | Large visible joint travel does not prove unlimited rotation or a slip ring. |
| What actuator behavior is reproducible? | Torque/speed/current curves, output sensing, control modes, delays and thermal duty | Determines which behaviors can be simulated and achieved with purchased drives. |

**Compliance distinction, from mechanics:** in a series arrangement, elastic
deflection separates motor-derived angle from output angle. A parallel spring
adds angle-dependent assistance while a rigid drive may retain its position
mapping. A compliant stop acts only at engagement. These alternatives need
different models and sensors; do not select one from the word “spring.”

### Next research deliverable

Before freezing the miniature mechanism, prepare a comparison of the existing
direct-knee proposal with a hip-mounted knee drive using the **same candidate
actuator and task envelope**. Include moving mass/inertia, independently supported
pivots, transmission variation, backlash, wire travel, assembly/service access,
cost and the exact state each encoder measures. Keep hypothetical compliance
separate until its force path is defined. This can proceed from our own
requirements even if Beni's proprietary dimensions remain unavailable.

For a future documentation request, the highest-value items are an exploded
hip/knee drawing, spring-attachment diagram, reducer ratio, output-sensor
location and torque/speed/duty data. No contact with Mondo or the creator was
made during this research.

## Project consequence

Beni's knee is actively driven, with its motor at the hip and body. It is not an
unactuated spring knee, so the passive cartridge and the fixed-axis cassette
stay superseded.

**Correction to the stale September 25 consequence:** R2A already selected a
crank and rigid pushrod on September 27; its former belt-in-link proposal is
superseded. R2A adopts remote knee actuation, not a verified reproduction of
Beni's reduction or compliance. The miniature's direct-knee servo arrangement
is a separate simplified proposal, not a scaled Beni mechanism.

The [miniature study](../../../docs/design/miniature_wheeled_biped_study.md)
tracks that comparison as MINI-9. Its current basket and direct-knee choice
remain provisional pending the comparison; an inexpensive position servo must
not inherit the behavior of a custom Beni drive by assumption.

The teardown is architecture evidence, not a dimensional source or a part
release. R2A values come from the project's own requirements, delivered hardware
and Fusion inspection. The preserved R2A implementation is defined in
[`active_knee_revision2_plan.md`](../../../docs/design/active_knee_revision2_plan.md).
This research changes no CAD, released mesh, material restriction or powered
test envelope. Existing large-build purchasing and print holds remain in force.
