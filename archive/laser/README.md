# ARCHIVED — not part of this build

**The single-leg rig has no laser-cut parts.** These files are retained only
because the two-leg build may want the steel arc stop back, and because
regenerating them took some work. Nothing on this page is an instruction for the
current build: it is a record of an order that was never placed.

**`stop_arc_loops.json` in this directory is the only remaining source for the
`Knee_Stop_Arc_L` profile.** The part no longer exists in the `Beni_SingleLegRig`
document, so if the steel version is ever wanted, the JSON — and the geometry
tabulated below — is where it has to come from. `rig_dxf_build.py` in this
directory still regenerates the DXFs from that JSON and still area-checks them
against the Fusion faces.

What replaced them, in `../beni_single_leg_rig_design_record.md` §8 and §5:

| Retired here | Replaced by |
|---|---|
| `Knee_Stop_Arc_L_inner/outer.dxf`, 1.5 mm steel at 45 HRC | the +27° stop is now **16.571 mm of bought M5 washers** as a compression column on the spring cartridge's guide rod, with a printed TPU sleeve around it as the progressive bumper, plus `RIG_Knee_Stop_Plate_L` (printed) for the −8° stop and a +28° backup |
| `RIG_Ballast_Disc.dxf`, 3 mm steel sectors | `RIG_Ballast_Pot` × 2, printed cups filled with off-the-shelf steel shot |

---

# `Knee_Stop_Arc_L` — the laser order as it stood

At the time, this was held to be the one part in the rig that had to be metal,
and the one part where nothing downstream was compliant: the load path was
dowel → steel slot end → 3 × M3 in shear → printed boss, at **534 N of impact**
(214 N static × 2.5). `beni_rig_no_machining.md` §2.2 was right that PA-CF
delaminates at a sharp slot end and then the leg has no stop — the stop was
therefore moved into the spring cartridge rather than substituted in place.

Uploading these files would not have been machining: ~$15 at SendCutSend or
equivalent, ±0.13 mm on 3 mm steel, no setup fee. The rule that now governs the
build rules out laser cutting regardless.

---

## What would have been ordered

| File | Qty | Material | Notes |
|---|---:|---|---|
| `Knee_Stop_Arc_L_inner.dxf` | 1 | **1.5 mm steel** | slot ends were the metal hard stops |
| `Knee_Stop_Arc_L_outer.dxf` | 1 | **1.5 mm steel** | slot housed the PU bumper blocks |
| `Knee_Stop_Arc_L_nest.dxf` | — | — | both of the above nested 90 mm apart, if the shop preferred one file |
| `RIG_Ballast_Disc.dxf` | 12 | 3 mm steel, plain | would have gone on the same order — see below |

**Hardness:** both plates would have been through-hardened to **45 HRC**, or the
slot ends case-hardened to 50–55 HRC.
**Finish:** slot-end faces **Ra 0.8, no burrs, no radius break** — an impact
contact surface. Everything else deburred.
**Flatness:** 0.05 over the sector.

The two plates stacked to the 3.0 mm the design expected, bolted through the same
3 × Ø3.4 by the three M3 × 6 that held the assembly to the proximal arm-B boss.
Splitting one 3 mm plate into two was necessary because a laser cuts one
through-profile per plate, and the spec's arc slot (`../manufacturing/machined_parts_spec.md`
§8) was **two-level** — so a single plate could not carry two different slot
lengths. The two levels were already two distinct profiles, so the split was
arguably the more natural build:

| Level | Span | Slot | Function |
|---|---|---|---|
| inner | 0 → 1.5 mm | 219.60° … 254.60° | **the metal hard stops** at φ = +27° and −8° |
| outer | 1.5 → 3.0 mm | 206.345° … 264.761° | housed the two replaceable PU blocks |

---

## The 0.3 mm undersize — inner plate only

The inner plate's slot ends **were** the hard stops, so they were dimensioned
short, to be filed to fit on assembly:

| | nominal | as ordered |
|---|---:|---:|
| end 1 | 219.600° | **220.173°** |
| end 2 | 254.600° | **254.027°** |

That is 0.30 mm of arc at the slot's r = 30 centreline, i.e. 0.5730° at each end.
Filing *opens* the slot toward nominal, so the stops would have engaged slightly
early until filed — which is the safe direction.

**The outer plate was cut nominal.** Its ends only located PU blocks; there was
nothing to file to.

---

## Geometry — the surviving record of the profile

All angles in the knee-local frame, 0° along +X, measured about the plate's own
datum (the centre of the r = 35.5 arc).

| Feature | Value |
|---|---|
| Sector | r **11.0 → 35.5**, spanning **200.345° → 302.000°** |
| Slot | r **26.9 → 33.1**, centreline r 30.0, width 6.2 |
| Slot end radius | **3.1** (matches the Ø6 dowel near-conformally) |
| Inner slot | 220.173° → 254.027° (undersized) |
| Outer slot | 206.345° → 264.761°, with steps at 213.669° and 260.531° |
| 3 × Ø3.400 | at **r = 15.000**, at **230° / 260° / 290°** |

Both files were verified after writing: hole positions read back at exactly
r = 15.0000 and 230 / 260 / 290°, and each closed profile's area was
cross-checked against the area Fusion reported for the same face —

| Level | area, DXF | area, Fusion | |
|---|---:|---:|---|
| outer | 802.082 mm² | 802.082 mm² | exact |
| inner | 843.309 mm² | 839.589 mm² | +3.720 = 2 × 0.3 × 6.2, the undersize |

### Handedness

These are the **left-hand** plates. The right-hand part is the mirror image
through the plate's own mid-plane — needed only for the two-leg build, not for
this rig. The profile as written is rotated 180° from the assembly's global XZ
frame, which is a view convention and **not** a mirror: do not flip it.

---

## Why these files are not Fusion's own DXF export

`Sketch.saveAsDXF` after `projectCutEdges` wrote the plate outline about a datum
at (+91.93, +77.13) and the three M3 holes about (−91.93, +77.13) — the **hole
pattern came out mirrored and 183 mm away from the profile.** Cutting that file
would have scrapped the part, and the error is not obvious on a thumbnail.

`../rig_dxf_build.py` instead reads the loop geometry straight off the solid
(`stop_arc_loops.json`, also in this directory) and authors the DXF entity by
entity, with the area cross-check above as the guard. Regenerate with:

```
python3 rig_dxf_build.py
```

---

## `RIG_Ballast_Disc`

A 3 mm steel annular sector, r 42 → 64, spanning 55° → 125°, with 2 × Ø4.5 at
r = 53 (at 70° and 110°). **32.8 g each.** It stacked on four M4 studs on the
carriage's inboard face, in symmetric pairs — the same part served top and bottom,
rotated 180°.

The order was to have been **12**, covering the 2.0 kg run (6 pairs = 394 g); the
mass budget needed only 61 g at 1.645 kg with a 500 g motor, so most were for the
heavy runs, bundled onto an order already being placed. Steps between discs would
have been trimmed with M12 washers (≈7 g) on the same studs.
