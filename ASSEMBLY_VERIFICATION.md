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
On 2026-09-14 the owner selected nominal Ø4.5 on the same-profile M3 ladder.
Fusion promoted that diameter into the active plate, proximal link and stand;
replace prior printed Ø4.0 receiver parts before insert installation.

The 2026-09-03 owned-M4 redesign adds a second explicit path condition. The
M4 × 8 wheel inserts install from the detached hub's motor face, pass through
the 6.0 mm hub, and finish with 2.0 mm projecting outboard. Fusion B-Rep checks
verify that all six projecting Ø5.5 label envelopes enter straight coaxial
Ø6.0 × 2.2 reliefs in `Wheel_Rim_L`; after the six screws are removed, the rim
services straight outboard along the same open paths. The owner-selected
Ø5.3 receiver was promoted through Fusion on 2026-09-04. The hub is an ABS
print release. The final tyre-compatible rim remains held for the separate
printability finding below; the September 17 no-tyre shell is a different,
suspended-test-only part.

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
the new hub's insert installation; on September 7 the owner also confirmed
the corrected link and all six screw seats. See the
[physical result](evidence/assembly/2026-09-07_owner_mockup/) and
[current audit](evidence/assembly/2026-09-05_access_fix/).

**Final tyre-compatible wheel-rim printing remains BLOCKED.** With the broad web face on the bed,
the annular underside at source y = 72 spans r = 30…44: a 14 mm unsupported
inward ledge. The outer retaining flange also has an overhang. The former
no-support claim is withdrawn. A printable solution must preserve the frozen
stack and keep support off the tyre, insert reliefs and mating/service faces.

The shoulder hub’s two Ø11 blind-relief ceilings and motor counterbore
shoulders are controlled bridges. The wheel-hub counterbore shoulders and
stand’s Ø4.5 blind-pocket roofs also bridge. Inspect their undersides on the
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

## 2026-09-06 supported knee mock-up

The [interim batch](first_article_stl/knee_mockup/) is `CAD PATH VERIFIED`
for two detached, supported links. A provisional distal tongue with its thrust
extensions omitted enters the fork radially with both bearings installed;
the temporary Ø9.7 pin then slides through all three bores. No spacers, collar,
spring cartridge, motors or wiring are present. Support removal, radial
insertion, continuous pin envelopes and sampled hand poses are recorded in
the [Fusion evidence](evidence/assembly/2026-09-06_supported_knee_mockup/).
The [September 7 owner report](evidence/assembly/2026-09-07_owner_mockup/)
confirms printing, successful provisional assembly, free supported knee
movement and easy pin removal: `PHYSICAL ASSEMBLY VERIFIED` for the supported
provisional hand fit. The shoulder motor appears attached in the photo; the
report does not expand the detached-link traveller to motor loads or power.
Detailed support-removal quality was not separately reported. Both spring
caps pass their detached, uncompressed fit check. These results do not release
the final distal/steel-pin/retention stack or spring cartridge.

## 2026-09-15 real steel pin in provisional shin

The real-pin gate is now `PHYSICAL FIT FAILED` for the provisional shin bore.
The owner fully inserted one received metal pin through both installed bearings
and the provisional shin, then had to break the printed shin pieces to recover
it. The owner isolated the seizure to the shin's nominal Ø10 bore; the bearings
were snug but were not the cause of the trapped assembly.

Do not repeat the nominal Ø10 bore in another link. The bearing result remains
incomplete until the pin candidates are inserted and removed through each
bearing separately without the printed link. Nominal Ø10.25 passed the initial
19.0 mm coupon under firm thumb pressure, and the owner selected Ø10.30 while
the receiver was expected to span 21.6 mm. Fusion's final service audit found
that copied sleeve span overlapped both bearing pockets, so the saved v26 source
now uses the clear 20.0 mm fork gap with 0.8 mm axial clearance per side.
Printability, support-removal, link/pin insertion and mesh checks pass, and the
bed-ready fit article is released. The first print must still prove firm-thumb
insertion, hand withdrawal, no free spin or rock and acceptable axial play.
Final retention and encoder coupling remain required before powered use. The
controlled September 17 unpowered spring article uses an outboard
spacer/bracket keeper plus hand containment and depends on this physical gate.
[Owner result](evidence/knee_fit/2026-09-15_steel_pin_provisional_shin/) ·
[Fusion release](evidence/knee_fit/2026-09-16_distal_d10p30_release/).

## 2026-09-17 unpowered spring-mechanical article

The [local traveller](first_article_stl/mechanical_spring_test/) is `CAD PATH
VERIFIED` for the complete supported single-leg sequence. Fusion sampled every
integer knee pose from -8° through +15°, found zero link/cartridge/spring-envelope
interference, and proved contact at both stops by 0.5° of overtravel. It also
verified radial insertion for both eyes, axial insertion for the guide and
spring, both clevis-pin paths, the steel knee-pin path and 40 mm wheel-shell
service travel. All seven exported meshes are closed manifolds on their stated
support planes.

The test remains `PHYSICAL ASSEMBLY PENDING`. Its Ø4 × 32 clevis-pin, Ø6 × 9
stop-dowel, and original stop-plate instructions are superseded by the
September 21 ordered-pin release below. The cartridge eyes, guide, D10 spacer,
bracket keeper, and no-tyre wheel shell remain current.

## 2026-09-21 ordered-pin integration

The [ordered-pin traveller](first_article_stl/ordered_pin_integration/) is `CAD
PATH VERIFIED` for the purchased Ø4 × 10, M4 × 40, and Ø6 × 10 pin families.
The new shoulder hub and proximal root use three face-locating dowels with a
press side, slip side, and screw-clamped axial capture. Both cartridge pivots
use integral Ø14 lands that make a 34.0 mm retained stack; one ISO 7089 M4
washer separates each printed land from its supplied cotter, with 0.4 mm
conservative clearance to the retaining-hole edge. The stop dowel is captured
between a blind distal socket and a closed 0.8 mm stop-plate skin, with 0.3 mm
axial clearance and no glue or press-fit dependency.

Fusion preserved the accepted proximal and distal print datums, passed both
40 mm clevis insertion paths, all 24 allowed knee poses, and positive stop
contact at 0.5° of overtravel. All four replacement meshes are closed
manifolds on their stated bed planes. [Numeric release evidence](evidence/assembly/2026-09-21_ordered_pin_integration/).

The release remains `PHYSICAL ASSEMBLY PENDING`: when the order arrives,
visually inspect it and complete the traveller's hand-fit checks. Do not ask
the owner to measure the pins and do not compensate a failed interface by
drilling, filing, hammering, or screw pull-down. Clamp the stand, unplug both
motors, keep the wheel clear, contain the distal side by hand, install the
spring at the -8° stop, and move slowly no farther than +15°. This procedure
observes self-weight equilibrium; it does not validate spring rate, solid
height, ground contact, structural load, or powered motion.

## 2026-09-22 ordered-pin fit ladders

The two [ordered-pin fit ladders](first_article_stl/ordered_pin_fit/) are
`FUSION VERIFIED / PHYSICAL SELECTION PENDING`. They precede the large
ordered-pin hub and link prints and use the real pins directly; no measurement
is part of the gate.

The root ladder reproduces the hub's bed-facing 5.0 mm blind socket and 3.0 mm
closed floor at Ø4.05…4.25 in 0.05 mm steps. Its accepted station must start
straight, seat fully with gentle controlled press pressure, remain retained
when inverted, and produce no whitening or split. The link side remains an
intentional slip fit.

The clevis ladder reproduces the Ø14 boss and the longest restrictive link
land at 9.0 mm, with Ø4.15…4.35 passages in 0.05 mm steps. Fusion read the live
link-land spans as 5.0, 5.8, 8.2, and 9.0 mm; the intervening cartridge-eye
passages are already Ø4.4 × 19 mm. The accepted station is the smallest one
that takes the real M4 × 40 pin with fingertip pressure, permits hand
withdrawal, and has no free radial rock. A continuous 34 mm coupon was rejected
because that dimension is the retained stack, not continuous bore material,
and would bias the result loose.

The Ø6 × 10 stop pin remains excluded from fit calibration because its Ø6.2
socket is deliberately loose and the closed stop-plate skin provides axial
capture. After the two Ø4 results are reported, update/confirm the Fusion
source and bed-ready hub/link exports before those large parts are printed.
