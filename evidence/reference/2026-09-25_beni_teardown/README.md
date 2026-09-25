# Beni teardown evidence — active belt-driven knee

Date reviewed: **2026-09-25**  
Source: [Beni the Camera Robot Goes Under the Knife](https://www.youtube.com/watch?v=Ds3sKpndzTA)

## What is visible

The teardown changes the architecture assumption used for the existing Beni
prototype. The useful sequence is approximately **7:38–8:18**:

- around [**7:38**](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=458s), the opened shoulder/upper-leg mechanism exposes toothed
  transmission parts and belts;
- around [**7:58**](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=478s), two brushless motor bodies are shown on the same joint axis;
- around [**8:03**](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=483s), a toothed belt path is visible inside the upper leg;
- around [**8:08–8:18**](https://www.youtube.com/watch?v=Ds3sKpndzTA&t=488s), the narration identifies an inner motor, a second motor
  arranged concentrically, and a belt reduction that controls the knee.

This is direct evidence that the current Beni mechanism does not rely on an
unactuated compression-spring knee as the project previously assumed. It uses a
remotely actuated knee with motor mass concentrated at the shoulder/body end and
a toothed-belt transmission to the knee.

## What this source does not establish

The video does not provide dimensions, tooth counts, belt profile, reduction
ratio, motor ratings, bearing stack, tension specification, control mapping, or
allowable joint range. It also does not establish that the project can copy the
same packaging with the owned Steadywin actuators. Those values must come from
the project's own requirements, delivered hardware, and Fusion inspection.

The teardown is therefore architecture evidence, not a dimensional source or a
part release.

## Project consequence

The passive spring cartridge and the later fixed-axis cassette proposal are no
longer the target architecture. The current printed ABS assembly remains useful
as fit and assembly evidence, but its spring stays removed and it is not a
powered or jumping article. The replacement direction is defined in
[`active_knee_revision2_plan.md`](../../../docs/design/active_knee_revision2_plan.md).
