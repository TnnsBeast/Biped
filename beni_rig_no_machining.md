# Beni Single-Leg Rig — Print Settings and Load Arithmetic

> ### ⚠ AMENDED 2026-08-12 — every part is now printed or bought
>
> Written against "no custom machining"; the rule is now **3D printed and off-the-shelf only — no
> laser cutting either**, with the authoritative routing table in
> **[`MANUFACTURING_CONSTRAINTS.md`](MANUFACTURING_CONSTRAINTS.md)**. **All ten machined families
> are eliminated; nothing here is laser-cut or machined.**
>
> `Knee_Stop_Arc_L` — once the single genuine blocker — is **deleted**, its +27° stop now a
> compression column of bought M5 washers inside a printed TPU bumper sleeve in the spring
> cartridge, with printed `RIG_Knee_Stop_Plate_L` keeping the −8° stop (75 N) and a +28° backup.
> §2.2 was right that the arc is not printable; the Hertzian numbers for every substitute
> considered, and why a compression column sidesteps contact stress altogether, are in the
> **[design record](beni_single_leg_rig_design_record.md) §8.**

`fusion_brief_single_leg_rig.md` §2 is the handoff document. **This one holds the print settings
with their justifications, and the load arithmetic behind each verdict.**

## 1. Print settings — the right levers

**100% infill is not the strongest setting.** For bending, impact and crack resistance — every
load case here — **walls beat infill**:

| Setting | Value | Why |
|---|---|---|
| Perimeters / walls | **5** | Shells carry bending load. This is the main lever. |
| Infill | **40% gyroid** | Past ~40% the returns collapse. 100% adds time and warp, not strength. |
| Layer height | 0.15 mm | Thinner layers = more interlayer bonds per mm of Z |
| Extrusion temp | **top of range** | Layer adhesion is temperature-driven, not infill-driven |
| Cooling | minimal for PA-CF | Fast cooling is the #1 cause of weak Z bonds |

**The real lever is orientation.** PA-CF measures **84–102 MPa in XY but only 26–50 MPa in Z**, and
that — not infill percentage — decides whether a part survives; per-part orientations are in the
design record §7. And **dry the filament**: PA-CF is hygroscopic, wet nylon loses a large fraction
of interlayer strength, and this is non-negotiable for structural parts.

## 2. The load arithmetic behind the verdicts

### 2.1 The two printed hubs

**`Shoulder_Output_Hub_L` — the flange is fine, the register is not.**

> **[UPDATED 2026-09-04]** The legacy Ø3.3 hub must be replaced by the new
> ABS hub with owner-passed Ø5.3 receivers for M4 × 8 inserts. This historical
> load arithmetic is not an ABS strength release. The six-screw proximal joint
> additionally remains held for screw-loading access; current release status
> is in [ASSEMBLY_VERIFICATION.md](ASSEMBLY_VERIFICATION.md).

```
25 N·m proof / 6 × M4 on Ø44 PCD  =  189 N per screw
M4 × 7 thread bearing area 28 mm² →  6.8 MPa
```

6.8 MPa against 84 MPa XY: **the bolted flange is not the problem.** Use M4 heat-set inserts rather
than tapping PA-CF. The **3 × Ø4.05 dowel register** is:

| Load | Shear per pin | Stress | vs PA-CF ~40–50 MPa |
|---|---:|---:|---|
| 11 N·m stall | 272 N | **28 MPa** | marginal |
| 25 N·m proof | 817 N | **63 MPa** | **fails** |

**Fix: press three Ø4 × 10 hardened dowel pins into the printed hub** (~$0.30 each) —
steel-on-steel against the motor's pins takes the plastic out of the shear path.
The old Ø3.9-and-ream route is prohibited by the project's no-machining rule.
Before PA-CF structural release, print a dedicated PA-CF bore series and select
the smallest as-printed bore that accepts the bought dowels as a true press fit;
if none passes, revise the printed retention geometry rather than drilling or
reaming it. **Orientation: flange face flat on the bed**, so the dowel holes
shear across layers, not along them.

**`Wheel_Hub_L` — a friction joint in plastic.**

```
3 × M3 at 3.4 kN preload, µ=0.15, r=13.5 mm  →  20.7 N·m friction capacity
```

Wheel motor peak is ~4–5 N·m, so ~4× margin — but **preload in plastic relaxes by creep**, which is
how a friction joint quietly dies. Use both mitigations: **steel washers under every screw head**,
and **re-torque after the first hour**, then every ~10 hours. **Orientation: flat on the bed,
register face up.**

### 2.2 Why the stop arc could never have been printed

The retired steel arc carried the crash load as bearing on a slot end:

```
crash load 534 N on a Ø6 dowel through a 3 mm plate  →  30 MPa bearing
```

30 MPa looks survivable against 84 MPa XY — **but that is the wrong comparison.** This is the final
crash load path with nothing compliant downstream, it is **impact** loading at 45 HRC hardness for a
reason, and it recurs across the drop series. PA-CF has no meaningful impact toughness at a sharp
slot end; it delaminates and then the leg has no stop.

### 2.3 The double-D flats — deleted, but they had a second job

The flats (8.40 −0.02 axle, 8.60 +0.05 sleeve bore) were the most machining-intensive feature in the
spec, and loads never justified them: the bearings are 10×19×5, the knee oscillates ±35° rather than
rotating, and static knee force peaks near 51 N. **Correction from building it:** beyond keying axle
to sleeve, they also carried the **encoder's angular reference** out to the magnet, so that
reference had to be replaced — a bought Ø10 h6 hardened ground dowel pin for the axle, the sleeve's
bore printed into `Distal_Link_L` as Ø10. Design record **§4**.

### 2.4 Cartridge eyes — the one open question

`Cart_Upper_Eye_L` / `Cart_Lower_Eye_L` carry the **11.00 ±0.05** and **14.57 ±0.05**
pivot-to-spigot dimensions, and **the spring force curve depends directly on them** (spec §3–§4);
they also need a Ø5.0 H7 press fit. Printing them puts a ±0.05 dimension in PA-CF — achievable if
measured and shimmed, and step 6 measures F₀ and k anyway, so a print error is detectable and
correctable. **M5 rod ends** (heim joints) are the obvious off-the-shelf substitute — Ø5 bore,
580–710 kgf static, ~$8 each — **but their centre-to-thread length differs from 11.00/14.57**, so
the cartridge dead length changes and the force curve shifts.

**Recommendation: print them, measure the achieved pivot-to-spigot dimension, and feed the real
number into the spring model** rather than chasing the nominal — and add a threaded adjuster if one
fits, making dead length tunable instead of tolerance-critical. **Orientation: pivot bore axis
vertical** (bore in the XY plane); printed on its side, the eye splits along a layer.

## 3. What printed structure costs you

**Stand and hub compliance reads as false knee deflection**, and printed hubs make it worse.
**Take step 6's spring characterisation as a system measurement, and if the numbers look soft,
suspect the print before the spring.** Also **re-torque everything after the first hour**, then
periodically — creep relaxation in printed joints is the dominant failure mode and it is silent —
and **inspect the printed hub's dowel holes after every load session**, because ovalised holes mean
the dowels are working.

**Amended 2026-08-17 — Mode A changes where the compliance lives.** The 2020
column and `RIG_Carriage` are **[DEFERRED — MODE B]**, so the series stiffness
chain is now shorter but entirely printed: bench → clamps → `RIG_Stand` → motor
front face → leg. Three consequences:

- **The stand is now the softest element in the measurement.** It carries the full
  shoulder yaw reaction (**11.00 N·m stall, 25.00 N·m proof**) at a **42.00 mm**
  overhang. Any deflection there appears as shoulder angle error, not knee error —
  which is a different and more insidious artifact than the old column bending.
  Print it with the load path along the layer *plane*, not across it, and check
  it: push the leg by hand at the wheel and watch the shoulder encoder.
- **Deflection is not the failure mode — tipping is.** 11.00 N·m needs 11.2 kg of
  hold-down at a 100 mm base half-width, 5.6 kg at 200 mm, 3.7 kg at 300 mm; a
  printed stand is ~0.3 kg. **It must be clamped.** Bench clamps are now a
  required purchase, and more of them than the Mode B build needed.
- **No drop session means the hub inspection interval is no longer event-driven.**
  Mode A never impacts the knee, so inspect on a schedule instead — after the
  first hour, then after each step-6 loading run.

## 4. ABS as a first-article material — where it is allowed

Owner decision 2026-09-02: complete the single-leg integration article in ABS
and defer PA-CF to the later two-leg structural build. The split remains by
**test load**, not merely by part name. ABS may be used for fit, complete
mechanical assembly, cable routing, hand-driven kinematics, and wheel-clear,
current-limited motor/electronics commissioning under self-weight only. It may
not carry a torque-arm load, stall torque, main-spring preload or
characterisation load, ground traction, a drop, a proof load, or any
human-adjacent load.

| Property | PA-CF (design basis) | Printed ABS |
|---|---:|---:|
| Tensile, XY | 84–102 MPa | ~20–22 MPa |
| Tensile, Z | 26–50 MPa | ~11–19 MPa |
| Young's modulus | — | ~1.8 GPa |

ABS is roughly **4× weaker in XY** with a proportionally similar Z penalty, and
notably softer. Published FDM ABS figures: 20.6 MPa at 0° vs 10.8 MPa at 90°/Z in one
P430 study; 22.4 → 19.0 MPa with modulus 1.81 → 1.78 GPa in another; general FDM
guidance puts Z as low as 4–5× below XY where interlayer bonding is poor. **Ranges,
not a datum** — do not dimension anything against these.

**Allowed in ABS.** `RIG_Floor_Plate` (for assembly geometry only — ground
traction is deferred; watch warp over 260 mm), `RIG_Cable_Post_A/B`,
`RIG_Scale_Pedestal` (compression block under the scale), `Knee_Encoder_Bracket_L`
(already specified ABS), and **any first-article geometry check** — dry-fitting the
knee stack, confirming the five insert bores line up with the panel, checking the
re-routed `RIG_Cable_Post_B` clears the wheel, and operating both motors slowly
with current limits while the wheel is clear and the structure carries no load
beyond self-weight. Cheap ABS is the right material for that work and derisks the
CAD before PA-CF is committed.

**Not allowed to carry measurement or proof loads in ABS, with the reason each
one fails:** The same geometries may still be printed in ABS for dry assembly,
clearance, fastener-access, and unloaded kinematic checks.

- **`RIG_Stand`** — the decisive one. It is not that it breaks; it is that per §3 the
  stand is *already* the softest element in the measurement chain, and ABS at
  ~1.8 GPa makes it softer. Its deflection appears as **shoulder angle error**, so an
  ABS stand characterises the fixture instead of the actuator, and it does so
  silently — plausible numbers, wrong ones.
- **`Shoulder_Output_Hub_L`** — the three-dowel register already sees 28 MPa at
  11 N·m stall and 63 MPa at 25 N·m proof against PA-CF's ~40–50 MPa shear (§2.1). In
  ABS that fails at **stall**, not just at the proof screen. The bought steel dowel
  pins remain mandatory either way.
- **`Wheel_Hub_L`** — a friction joint held by bolt preload, and preload in plastic
  dies by creep (§2.1). ABS creeps faster. Failure mode is quiet slip, which corrupts
  every wheel-torque reading rather than announcing itself.
- **`RIG_Torque_Arm`** — a 200 mm lever in pure bending that *is* the torque
  instrument. Arm flex reads directly as torque error, and step 2's whole purpose is
  resolving the 4.8 / 9.4 N·m published measurements against the 11 N·m rating.
- **`Cart_Upper_Eye_L` / `Cart_Lower_Eye_L`** — carry the 11.00 ±0.05 and
  14.57 ±0.05 pivot-to-spigot dimensions that set the spring force curve (§2.4).

**Print `GAUGE_Fit_Coupon` in ABS for the ABS campaign.** It gives the ABS
profile's hole/X-Y compensation using real bearings, dowels, fasteners and
inserts. The two existing `GAUGE_*_Motor_Interface` files are positive motor
stand-ins; they do not accept the delivered actuators. For a direct motor
go/no-go, design a negative mating coupon in Fusion or print the actual mating
part in ABS. ABS and PA-CF differ in shrinkage and hole error, so the ABS result
does not transfer: repeat the critical fit and negative mating coupons in PA-CF
immediately before the later two-leg structural prints.

⚠ **Heat-set insert data does not transfer either.** The M3 insert's grip is already
the unverified weak link in the stand's five-bolt joint (`fusion_agent_guide_mode_a.md`
§2.3). If the pull test on a scrap boss gets done, do it in **PA-CF** — an ABS result
says nothing about the built joint.
