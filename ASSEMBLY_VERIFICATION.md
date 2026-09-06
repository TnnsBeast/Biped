# Physical assembly-path verification

An interference-free final CAD pose is necessary, but it is not a build
release. Every released part or subassembly also needs a physically achievable
installation and removal path.

## Required release gate

Before a part is sent to the printer or added to an assembly instruction, record
all of the following:

1. **Order** — the parts and captive hardware that must be installed first.
2. **Insertion path** — the direction and intermediate poses used to reach the
   final CAD pose. Check the full path in Fusion, not only the endpoints.
3. **Fastener and tool access** — screws must be startable and torqueable with
   the surrounding parts present. Screws must not be used to pull a mismatched
   print into place.
4. **Cable path** — connectors, strain relief, and minimum bend space must remain
   installable during the stated sequence.
5. **Service path** — identify what must be removed to replace the part and make
   sure that removal does not require damaging another component.
6. **Physical rehearsal** — for a first article, repeat the sequence with the
   real hardware and record the result before structural release.

Use these status labels in build records:

- `CAD PATH VERIFIED` — Fusion was used to check intermediate poses and tool
  access, but the sequence has not yet been completed on the real hardware.
- `PHYSICAL ASSEMBLY VERIFIED` — the owner completed the sequence with the real
  parts without forcing, destructive rework, or fastener pull-down.
- `BLOCKED` — there is no demonstrated path, required hardware is missing, or a
  physical attempt failed. Do not release downstream parts that depend on it.

For each first-article batch, its local `README.md` is the build traveller: it
must state the exact sequence, current status, and evidence link. The canonical
fastener schedule and full robot assembly order remain in
[`beni_prototype1_bom_and_assembly.md`](beni_prototype1_bom_and_assembly.md).

The first recorded application of this gate is the GIM6010 shoulder stack:
[`evidence/shoulder_assembly/2026-08-23_plate_sequence/`](evidence/shoulder_assembly/2026-08-23_plate_sequence/).

The 2026-09-02 receiver audit added one concrete correction to that stack: the
old cable-cover screws entered from the inboard face and their heads collided
with the stand/chassis volume. The four inserts now live in the shoulder plate,
the cover is a clearance part, and M3 × 10 screws enter from the accessible
outboard face. Fusion verified 1.5 mm screw-tip clearance and zero stand
interference. The pictured insert and screw-direction map is
[`docs/assembly/heatset_receiver_map.md`](docs/assembly/heatset_receiver_map.md).

The 2026-09-03 owned-M4 redesign adds a second explicit path condition. The
M4 × 8 wheel inserts install from the detached hub's motor face, pass through
the 6.0 mm hub, and finish with 2.0 mm projecting outboard. Fusion B-Rep checks
verify that all six projecting Ø5.5 label envelopes enter straight coaxial
Ø6.0 × 2.2 reliefs in `Wheel_Rim_L`; after the six screws are removed, the rim
services straight outboard along the same open paths. The owner-selected
Ø5.3 receiver was promoted through Fusion on 2026-09-04. The hub is an ABS
print release; the rim remains held for the separate printability finding below.

The same rerun found a separate `RIG_Cable_Post_A`/cable-cover overlap. The
2026-09-05 redesign moves the post outside the cover; its eye remains open
beyond the cover edge. Actual harness routing still needs physical rehearsal.

## 2026-09-04 release checks and new blockers

[Fusion B-Rep path and print audit](evidence/inserts/2026-09-04_m4_coupon_pass/fusion_paths_and_print_audit.json)
checks each axial path from +40 mm to the final pose in 0.5 mm steps. The
bare-rotor plate, Ø4.15 ABS hub, cable cover, proximal-link body, wheel hub and
rim body paths have zero intersections; reverse motion provides their removal
path. The wheel’s six M4 screws also have clear insertion paths. The shoulder
hub is released for detached insert installation and unplugged motor fit.

**Historical 2026-09-04 link failure, corrected 2026-09-05:** two M4 × 10
heads hit the internal wall on a straight approach. The current link extends
all six access passages through that wall and shortens the lightening opening
to restore a complete seat under the sixth head. New exact continuous swept
head/shank/driver envelopes and seat-support checks pass. The owner accepted
the new hub's insert installation; the corrected link still needs its own
physical six-screw rehearsal. See the [current audit](evidence/assembly/2026-09-05_access_fix/).

**Wheel-rim printing remains BLOCKED.** With the broad web face on the bed,
the annular underside at source y = 72 spans r = 30…44: a 14 mm unsupported
inward ledge. The outer retaining flange also has an overhang. The former
no-support claim is withdrawn. A printable solution must preserve the frozen
stack and keep support off the tyre, insert reliefs and mating/service faces.

The shoulder hub’s two Ø11 blind-relief ceilings and motor counterbore
shoulders are controlled bridges. The wheel-hub counterbore shoulders and
stand’s Ø4 blind-pocket roofs also bridge. Inspect their undersides on the
first ABS articles; the bores remain vertical and no slicer support is allowed
on their functional surfaces. The full wired/stand article is still gated by
actual harness routing, floor disposition, real knee pin/retention and electronics checks.

## 2026-09-05 access and assembly-order audit

[Ordered Fusion paths](evidence/assembly/2026-09-05_access_fix/ordered_paths.json)
check the link, cover, cable post and rim through 81 poses each. All 49 modelled
screw paths clear with the stated order. These constraints are part of assembly,
not optional workarounds:

- Fit housing screws with the proximal link, cover and post absent.
- Attach the panel to the stand before adding the front cable post.
- Fit knee-stop screws before the encoder bracket; remove the bracket to
  withdraw those screw heads. Its Ø5 access openings are for a driver.
- Fit/service wheel-motor housing screws with the leg supported off the stand.
- Remove the link before removing the cover; reverse the remaining sequence.

[The ABS export report](evidence/assembly/2026-09-05_access_fix/proximal_release.json)
checks both continuous bearing insertion/removal envelopes, full root screw
lands, topology and supporting plane. The front post's Ø6 probe passes its
open Ø8 eye with the cover fitted. The exact iron tip, cable connector, tie and
bend-radius fit remain physical checks; these envelopes do not assert a full
wired or structural release.
