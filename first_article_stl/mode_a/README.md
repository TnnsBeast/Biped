# Mode A — ABS single-leg fixture prints

The active single-leg integration article remains entirely ABS. These files
support dry assembly and wheel-clear, current-limited commissioning under
self-weight only. They are not structural-load articles.

**Owner update, 2026-09-07:** the corrected front cable post and M3 fit coupon
are printed, together with the cover and wheel hub.
[Completion record](../../evidence/assembly/2026-09-07_small_parts_printed/).
Their physical checks remain pending. Test the M3 insert first, then print
the stand separately; the rear anchor remains optional.

## Stand

![Fusion view of the stand on its released bed face](00_fusion_ABS_FA_RIG_Stand_M3_INSERTS_PRINT_ORIENTED.png)

Print
[`ABS_FA_RIG_Stand_M3_INSERTS_PRINT_ORIENTED.stl`](ABS_FA_RIG_Stand_M3_INSERTS_PRINT_ORIENTED.stl)
exactly as supplied. Its mount face is at `Z=0`; the oriented envelope is
200.0 × 299.3119 × 32.0 mm and needs at least 300 mm on one bed axis. Use no
supports.

The five panel receivers are Ø4.0 × 6.0 blind pockets for approved 5 mm
Voron-style M3 inserts. They open on the bed datum, leave 1.0 mm below the
insert and retain a 6.0 mm printed floor. Coupon the exact owned insert before
installation.

Clamp or bolt the stand to the bench before mounting the leg. Its own weight
cannot react shoulder stall torque. The ABS commissioning scope still forbids
torque-arm, stall/proof, spring, ground-traction and drop testing.

## Cable anchor

`RIG_Cable_Anchor_ModeA.stl` is the optional rear-face strain-relief anchor.
Place either broad face on the bed and install with 2 × M3 × 8 plus washers.

The full receiver release record is
[`../heatset_receiver_release_manifest.json`](../heatset_receiver_release_manifest.json).


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
