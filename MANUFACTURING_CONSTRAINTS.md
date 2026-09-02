# Manufacturing constraints

**Authoritative. Read before adding any part to any build in this project.**

Stated by the project owner, 2026-08-12.

---

## The rule

> **3D printed parts and off-the-shelf parts only.**
> **No laser cutting. No machining.**

A manifold STL is not by itself a printable release. Print-axis dimensional
control and support-removal requirements are governed by `CLAUDE.md` hard rule
12.

"Off the shelf" means a catalogue item you can order and fit as-is: fasteners,
dowel pins, washers, shims, bearings, linear rail and blocks, aluminium
extrusion, springs, magnets. Cutting bought stock to length with a hacksaw is
fine. Anything that needs a mill, a lathe, a waterjet or a laser is not.

## What this rules out

| Not allowed | Was used for |
|---|---|
| Laser-cut sheet | `Knee_Stop_Arc_L`, `RIG_Ballast_Disc` |
| Milled / turned parts | the ten families in `archive/manufacturing/machined_parts_spec.md` |
| Ground flats, keyed features, reamed precision bores in metal | `Knee_Axle_L`'s double-D, `Knee_Sleeve_L` |

## Where each affected part went

For the single-leg rig, every one of these is resolved. Nothing is outstanding.

| Part | Was | Now | Where it is written up |
|---|---|---|---|
| `Shoulder_Output_Hub_L` | 7075 machined | **printed** + 3 bought Ø4 × 10 dowel pins + M4 inserts | `beni_rig_no_machining.md` §2.1 |
| `Wheel_Hub_L` | 7075 machined | **printed** + steel washers + a re-torque schedule | `beni_rig_no_machining.md` §2.1 |
| `Cart_Upper_Eye_L`, `Cart_Lower_Eye_L` | 7075 machined | **printed**, measured, real dimension fed back to the spring model | `beni_rig_no_machining.md` §2.4 |
| `Knee_Magnet_Carrier_L` | steel | **printed**, runout measured on an indicator | rig design record §4 |
| `Knee_Axle_L` | 4140 ground, double-D | **bought** Ø10 h6 hardened ground dowel pin | rig design record §4 |
| `Knee_Sleeve_L` | steel, double-D bore | **deleted** — its Ø16 bore is printed into `Distal_Link_L` as Ø10 | rig design record §4 |
| `Cart_Guide_Rod_L` | ground steel | **bought** Ø5 × 50 hardened shaft | rig design record §9 |
| `Cart_Preload_Shim_L` | shim stock | **bought** Ø19/Ø13.6 × 0.5 shim washers | rig design record §9 |
| **`Knee_Stop_Arc_L`** | **laser-cut 3 mm steel, 45 HRC** | **deleted.** The +27° hard stop is now a **compression column of bought M5 washers** inside the spring cartridge, with a printed TPU sleeve as the progressive bumper; `RIG_Knee_Stop_Plate_L` (printed) keeps the −8° stop and a +28° backup | **rig design record §8** |
| **`RIG_Ballast_Disc`** | **laser-cut 3 mm steel** | **`RIG_Ballast_Pot` × 2**, printed cups filled with off-the-shelf steel shot — **now [DEFERRED — MODE B] (2026-08-17): the Mode A build has no vertical slide, so there is nothing to ballast. The substitution stands if Mode B is ever built; the shot need not be bought now** | **rig design record §5** |

**Amended 2026-08-17 — the rig build is Mode A only.** This does not change any
substitution above; it changes only what has to be printed *now*. Deferred with
Mode B: `RIG_Rail`, `RIG_Blocks`, `RIG_Carriage`, `RIG_Index_Post`,
`RIG_Index_Bar`, `RIG_Mode_Pin`, `RIG_Bumpers`, `RIG_Ballast_Pot`. Added:
**`RIG_Stand`**, printed, which reacts the shoulder's own 11.00 N·m stall / 25.00
N·m proof yaw torque at a **42.00 mm** overhang and therefore **must be clamped to
the bench, not weighted** — see `fusion_agent_guide_mode_a.md`. The stand is fully
inside this constraint: printed part plus bought bench clamps, no machining, no
laser cutting.

## The one place this cost real margin

Everything above is a lateral move or an improvement except the knee hard stop.

The steel arc worked because its slot ends were **conformal** — a 3.1 mm *concave*
radius bearing on a Ø6 dowel, about 257 MPa at the 534 N crash load. Nothing
printed or off-the-shelf reproduces a concave 3.1 mm steel face, and every convex
substitute reverts to Hertzian line contact at **1.0–2.0 GPa**. That is why the
stop was moved into the spring cartridge as a compression column instead of being
substituted in place: a column has no contact-stress problem at all.

What it costs, honestly:

- the working stop is **inside the cartridge and not inspectable** without pulling
  a clevis pin;
- it reacts through two **printed** spigot faces at 9.9 MPa rather than a hardened
  steel slot end — a factor of 8 below the material, but plastic where there used
  to be steel in the final crash path;
- its engagement angle depends on the printed eyes' achieved dead length, so it
  must be **set by measurement after step 6**, not from a drawing.

Full reasoning, the Hertzian numbers for every substitute considered, and the
verification sweep: `beni_single_leg_rig_design_record.md` §8.

## Scope

The constraint governs **what gets built**. It does not invalidate the design
records that describe the two-leg robot as originally engineered:

- `archive/manufacturing/machined_parts_spec.md` still correctly specifies the ten
  machined families **as they were designed**. It is not a shopping list for the
  rig build — see its own banner.
- `beni_prototype1_design_record.md` and `beni_prototype1_bom_and_assembly.md`
  describe Prototype 1 with machined hubs and axles. That is history, and the
  mass and load numbers in them are still the reference.

If the two-leg build later gets access to a shop or a laser, the retired steel
arc files are preserved under `archive/laser/`.
