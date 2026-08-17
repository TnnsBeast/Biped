# Beni Single-Leg Rig — Eliminating Machined Parts

> ### ⚠ AMENDED 2026-08-12 — the constraint now excludes laser cutting too
>
> This document was written against "no custom machining", and it resolves nine
> of the ten machined families on that basis. Those nine verdicts all stand and
> are built.
>
> The constraint has since been tightened to
> **3D printed and off-the-shelf parts only — no laser cutting either**
> (**[`MANUFACTURING_CONSTRAINTS.md`](MANUFACTURING_CONSTRAINTS.md)**), which
> supersedes the tenth:
>
> - **§2.2 `Knee_Stop_Arc_L` — "the one genuine blocker … Laser-cut it"** is no
>   longer available. Option 1 (laser) and option 2 (two stacked 1.5 mm plates)
>   are both out; option 3 (software-only stops for steps 1–9) was never enough on
>   its own, because step 10 needs a real stop.
> - **What replaced it:** the +27° hard stop moved out of the arc entirely and into
>   the spring cartridge as a **compression column** — a stack of bought M5
>   washers on the existing guide rod, with a printed TPU sleeve around it as the
>   progressive bumper. `RIG_Knee_Stop_Plate_L` (printed) keeps the −8° extension
>   stop, which only carries 75 N, plus a +28° flexion backup.
> - **Why not just substitute a printed or bought part in place:** §2.2's judgement
>   that the arc is not printable was right, and for a sharper reason than impact
>   toughness. The steel slot ends are **conformal** (3.1 mm concave on a Ø6
>   dowel, ~257 MPa at 534 N). Every printed or bought *convex* substitute reverts
>   to Hertzian line contact at **1.0–2.0 GPa**. A compression column sidesteps
>   contact stress altogether.
>
> Full reasoning and the verification sweep:
> **[`beni_single_leg_rig_design_record.md`](beni_single_leg_rig_design_record.md) §8.**
>
> One further correction to §2.3, from building it: the double-D flats' second,
> unstated job is carrying the **encoder's angular reference** out to the magnet.
> Deleting them is still right, but that reference has to be replaced — see the
> design record §4.


**Constraint.** No custom machining. Off-the-shelf where a part must be metal,
3D printed everywhere else. **Companion to `fusion_brief_single_leg_rig.md` §2**
— that brief is the handoff document; this one holds the load arithmetic and the
per-part orientations behind its routing table.

**The correction that matters most.** `machined_parts_spec.md` lists **ten**
machined families, not the four named in the earlier rig plan. Six of them are on
the single-leg critical path. Verdicts below are load-based, not preference.

---

## 1. Print settings — the right levers

**100% infill is not the strongest setting.** For bending, impact and crack
resistance — every load case here — **walls beat infill**:

| Setting | Value | Why |
|---|---|---|
| Perimeters / walls | **5** | Shells carry bending load. This is the main lever. |
| Infill | **40% gyroid** | Past ~40% the returns collapse. 100% adds time and warp, not strength. |
| Layer height | 0.15 mm | Thinner layers = more interlayer bonds per mm of Z |
| Extrusion temp | **top of range** | Layer adhesion is temperature-driven, not infill-driven |
| Cooling | minimal for PA-CF | Fast cooling is the #1 cause of weak Z bonds |

**The real lever is orientation.** PA-CF measures **84–102 MPa in XY but only
26–50 MPa in Z.** Every part below states its orientation, and that decides
whether it survives — not infill percentage.

**Dry the filament.** PA-CF is hygroscopic; wet nylon loses a large fraction of
interlayer strength. Non-negotiable for structural parts.

---

## 2. Verdicts

### 2.1 Print these — the loads work out

**`Shoulder_Output_Hub_L` → print, with one bought insert.**

```
25 N·m proof / 6 × M4 on Ø44 PCD  =  189 N per screw
M4 × 7 thread bearing area 28 mm² →  6.8 MPa
```

6.8 MPa against 84 MPa XY. **The bolted flange is not the problem.** Use M4
heat-set inserts (the spec already buys M3 inserts, §11) rather than tapping PA-CF.

**The 3 × Ø4.05 dowel register is the problem:**

| Load | Shear per pin | Stress | vs PA-CF ~40–50 MPa |
|---|---:|---:|---|
| 11 N·m stall | 272 N | **28 MPa** | marginal |
| 25 N·m proof | 817 N | **63 MPa** | **fails** |

**Fix: press three Ø4 × 10 hardened dowel pins into the printed hub.** The pins
are off-the-shelf (~$0.30 each), and steel-on-steel against the motor's pins
removes the plastic from the shear path entirely. Print the holes Ø3.9 and ream
to Ø4.05.

- **Orientation: flange face flat on the bed**, so torque loads the bolt circle
  in XY and the dowel holes see shear across layers, not along them.

**`Wheel_Hub_L` → print.**

```
3 × M3 at 3.4 kN preload, µ=0.15, r=13.5 mm  →  20.7 N·m friction capacity
```

Wheel motor peak is ~4–5 N·m, so ~4× margin — but **preload in plastic relaxes by
creep**, which is how a friction joint quietly dies. Two mitigations, use both:

1. **Steel washers under every screw head** to spread bearing load
2. **Re-torque after the first hour of running**, then every ~10 hours

The Ø37.3 H8 register is centring-only and prints fine at 5 walls.

- **Orientation: flat on the bed, register face up.**

**`Knee_Sleeve_L` → substitute, do not print.** An Ø16 OD × Ø10 bore steel
bushing is a stock item. The double-D flats are the hard part; see §2.3 for the
redesign that deletes them.

### 2.2 Do NOT print these — buy or substitute

**`Knee_Stop_Arc_L` → the one genuine blocker.**

```
crash load 534 N on a Ø6 dowel through a 3 mm plate  →  30 MPa bearing
```

30 MPa looks survivable against 84 MPa XY — **but that is the wrong comparison.**
This is the final crash load path with nothing compliant downstream, it is
**impact** loading at 45 HRC hardness for a reason, and it is a repeated
high-cycle event across the whole drop series. PA-CF has no meaningful impact
toughness at a sharp slot end; it will delaminate and then the leg has no stop.

**Three options, in order:**

1. **Laser-cut it.** SendCutSend and equivalents cut 3 mm steel at ±0.13 mm with
   no setup fee — a flat annular sector with two arc slots is exactly what laser
   cutting is for. **This is not machining; it is uploading a DXF for ~$15.**
   Order the slot ends ~0.3 mm undersize and file to fit.
2. **Two stacked 1.5 mm plates** if 3 mm is awkward — the spec's two slot levels
   (inner hard stop, outer bumper channel) are *already* two distinct profiles,
   so a two-plate stack is arguably the more natural build.
3. **Software-only stops for early testing.** Steps 1–9 never approach +27°.
   Only step 10's drop series needs a metal stop. **You can start the rig
   without it** — but do not run a single drop without it fitted.

**`Knee_Axle_L` → buy.** An M10 shoulder bolt or a hardened Ø10 h6 dowel pin plus
a printed retaining collar. **Delete the double-D flats** — see §2.3.

**`Cart_Guide_Rod_L` → buy.** Ø5 mm hardened ground shaft, cut to 50 mm. Sold as
linear-motion shafting; ~$3.

**`Cart_Preload_Shim_L` → buy.** Ø19/Ø13.6 × 0.5 mm shim washers are stock. Or
stack M12 washers and measure.

**`Knee_Magnet_Carrier_L` → print, but check runout.** The 0.05 TIR concentricity
callout is what keeps the absolute encoder honest. Print it, measure it on an
indicator, and if it exceeds ~0.1 mm, glue the magnet into a printed pocket
using the bore as the datum instead of the printed step.

### 2.3 The redesign that deletes the hardest part

**The double-D flats (8.40 −0.02 on the axle, 8.60 +0.05 in the sleeve) are the
single most machining-intensive feature in the whole spec** — a ground flat pair
held to 20 µm, on two mating parts.

Their only job is to key the axle to the sleeve so they rotate together.

**Replace the keyed axle+sleeve with a plain Ø10 shoulder bolt running directly
in the two 6800 bearings, and let the printed distal boss carry the anti-rotation
duty via a simple pin or a D-flat printed into the plastic.** The knee sees
±35° of oscillation, not continuous rotation, so a keyed steel interface is
over-engineered for this rig. Loads are modest — the bearings are 10×19×5 and the
static knee force peaks near 51 N (`fusion_brief_single_leg_rig.md` §4.3).

**This deletes two machined parts and buys one bolt.** Flag it to the fusion
agent as a design question rather than treating it as settled — it changes the
knee joint's construction, and the two-leg build may want the keyed version back.

### 2.4 Cartridge eyes — the one open question

`Cart_Upper_Eye_L` / `Cart_Lower_Eye_L` carry the **11.00 ±0.05** and
**14.57 ±0.05** pivot-to-spigot dimensions, and **the spring force curve depends
directly on them** (spec §3–§4). They also need a Ø5.0 H7 press fit.

- **Printing them** puts a ±0.05 dimension in PA-CF. Achievable *if* measured and
  shimmed after printing, but the tolerance is what sets your force curve — and
  step 6 measures F₀ and k anyway, so a print error is detectable and correctable.
- **M5 rod ends** (heim joints) are the obvious off-the-shelf substitute: Ø5 bore,
  580–710 kgf static, ~$8 each. **But their centre-to-thread length differs from
  11.00/14.57**, so the cartridge dead length changes and the force curve shifts.

**Recommendation: print them, measure the achieved pivot-to-spigot dimension, and
feed the real number into the spring model** rather than chasing the nominal. Add
a threaded adjuster if the fusion agent can fit one — then dead length becomes
tunable instead of tolerance-critical.

- **Orientation: pivot bore axis vertical** (bore in the XY plane), so the eye
  loads the layers in-plane. Printed on its side, the eye splits along a layer.

---

## 3. Net result

| Part | Was | Now |
|---|---|---|
| `Shoulder_Output_Hub_L` | 7075 machined | **Print** + 3 bought dowels + M4 inserts |
| `Wheel_Hub_L` | 7075 machined | **Print** + steel washers, re-torque |
| `Cart_Upper/Lower_Eye_L` | 7075 machined | **Print**, measure, feed back to model |
| `Knee_Magnet_Carrier_L` | steel | **Print**, verify runout |
| `Knee_Axle_L` | 4140 ground | **Buy** shoulder bolt (flats deleted, §2.3) |
| `Knee_Sleeve_L` | steel | **Deleted** by §2.3 |
| `Cart_Guide_Rod_L` | ground steel | **Buy** Ø5 linear shaft |
| `Cart_Preload_Shim_L` | shim stock | **Buy** shim washers |
| `Knee_Stop_Arc_L` | 45 HRC steel | **Laser-cut, ~$15.** Not printable. |

**Nine of ten eliminated. One laser-cut flat plate remains**, and it is a DXF
upload rather than a machining job.

**Bought hardware to add:** 3 × Ø4 × 10 dowel pins, M4 heat-set inserts, M10
shoulder bolt, Ø5 × 50 hardened shaft, shim washer assortment, steel washers.
Roughly $30 all in.

---

## 4. What this costs you

Printed structure is **not** equivalent to 7075. Three consequences to accept:

1. **Re-torque everything after the first hour**, then periodically. Creep
   relaxation in printed joints is the dominant failure mode, and it is silent.
2. **Column and carriage compliance reads as false knee deflection.** The fusion
   brief already flags this; printed hubs make it worse. **Take step 6's spring
   characterisation as a system measurement**, and if the numbers look soft,
   suspect the print before the spring.
3. **Inspect the printed hub's dowel holes after every drop session.** Ovalised
   holes mean the dowels are working — catch it before the register is gone.

**None of this compromises the rig's purpose.** Steps 1–9 are actuator and spring
characterisation at modest loads. Only step 10 approaches the design limits, and
that is exactly where the one bought steel part sits.
