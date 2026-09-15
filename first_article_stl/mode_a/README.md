# Mode A — ABS single-leg fixture prints

The active single-leg integration article remains entirely ABS. These files
support dry assembly and wheel-clear, current-limited commissioning under
self-weight only. They are not structural-load articles.

**Owner update, 2026-09-14:** the corrected front cable post, cover, wheel hub,
general fit gauge and dedicated M3 ladder are printed. The gauge's Ø4.0 M3
station failed; the owner selected the ladder's largest, unmarked-end station,
nominal Ø4.5. [Physical selection](../../evidence/inserts/2026-09-14_m3_coupon_pass/).
The stand has been promoted, re-exported and verified through Fusion; the rear
anchor remains optional.

## Stand

![Fusion view of the current stand source on its bed face](00_fusion_ABS_FA_RIG_Stand_M3_INSERTS_PRINT_ORIENTED.png)

**ABS PRINT RELEASE — Ø4.5 M3 receivers.** Fusion verifies five Ø4.5 × 6.0
blind pockets and a clean, closed, bed-ready STL. The print keeps its mount face at `Z=0`; the oriented envelope is
200.0 × 299.3119 × 32.0 mm and needs at least 300 mm on one bed axis. Use no
supports.

The five panel receivers are Ø4.5 × 6.0 blind pockets for 5 mm Voron-style M3
inserts. They open on the bed datum, leave 1.0 mm below the insert and retain a
6.0 mm printed floor.

Clamp or bolt the stand to the bench before mounting the leg. Its own weight
cannot react shoulder stall torque. The ABS commissioning scope still forbids
torque-arm, stall/proof, spring, ground-traction and drop testing.

## Cable anchor

`RIG_Cable_Anchor_ModeA.stl` is the optional rear-face strain-relief anchor.
Place either broad face on the bed and install with 2 × M3 × 8 plus washers.

The current receiver record is
[`../heatset_receiver_release_manifest.json`](../heatset_receiver_release_manifest.json).
It records the Ø4.5 M3 selection and releases the current stand STL.


## Corrected front cable post A — 2026-09-05

The owner has printed one ABS
[`ABS_FA_RIG_Cable_Post_A_COVER_MOUNT_PRINT_ORIENTED.stl`](ABS_FA_RIG_Cable_Post_A_COVER_MOUNT_PRINT_ORIENTED.stl)
as of September 7; cover/post and actual harness fit remain pending. No reprint
is requested. For a replacement, use its supplied broad face down and no
supports. This is a constant 2 mm
section with vertical through holes. Use the same tuned ABS profile as the
other first articles.

It mounts on the outside of the cover, sharing the upper two Ø88 holes. Use
**two M3 × 12**, replacing those two cover M3 × 10 screws; the lower two stay
×10. Fit the panel/stand and housing screws first. The Ø8 eye lies outside the
cover edge and must remain open after assembly. Fit and inspect the actual tie
and harness before attaching the link; both must clear supported hand motion.
This part is distinct from the rear anchor above.

[Assembly paths and remaining gates](../../evidence/assembly/2026-09-05_access_fix/).
