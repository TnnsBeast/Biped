# Delivered actuators — photo record, 2026-08-20

These are full-resolution copies of the owner's photographs of the two delivered
Steadywin actuators and the included breakout/accessory wiring. They are retained
inside the project so later agents can inspect the actual connector placement,
cable exits, output faces, and mounting hardware without relying on chat history.

| File | Actuator | View / useful evidence |
|---|---|---|
| `gim6010-8_01_driver-side-overview.jpeg` | GIM6010-8 | Driver-side overview and power leads |
| `gim6010-8_02_driver-labels-and-connectors.jpeg` | GIM6010-8 | Visible `GIM6010-8` marking, driver-board labels, power and communications connectors |
| `gim6010-8_03_output-interface.jpeg` | GIM6010-8 | Output flange, pilot, bolt pattern, and surrounding housing holes |
| `gim4305-10_00_driver-side-overview-with-breakout.jpeg` | GIM4305-10 | Driver-side overview, fixed red/black leads, communications cable, and supplied breakout |
| `gim4305-10_01_driver-side-terminal-breakout.jpeg` | GIM4305-10 | Driver side beside the supplied screw-terminal breakout |
| `gim4305-10_02_driver-side-usbc-breakout.jpeg` | GIM4305-10 | Driver side beside the supplied USB-C breakout |
| `gim4305-10_03_driver-side-connectors.jpeg` | GIM4305-10 | Close view of driver-side communications connector and power leads |
| `gim4305-10_04_output-interface-and-accessories.jpeg` | GIM4305-10 | Output flange, pilot, bolt pattern, and supplied accessory wiring |

The filenames describe what is visible; they are not an electrical pinout. Do
not energise a connector based only on a photograph or PCB silkscreen. Confirm
the delivered controller manual and continuity/polarity first.

## Nominal CAD sources

- `../../../CAD Imports/ascii/GIM6010_8.stp` — nominal manufacturer geometry.
- `../../../CAD Imports/ascii/GIM4305_10.stp` — nominal manufacturer geometry.
- The matching live Fusion references are `REF_GIM6010-8` and
  `REF_GIM4305-10`; all Fusion inspection and design work is performed through
  the Fusion MCP.
- The current nominal axial envelopes are **44.0000 mm** for GIM6010-8 and
  **33.0000 mm** for GIM4305-10, as recorded in the design record and verified
  in the live Fusion assembly.

Read-only Fusion MCP inspection of the native imported motor documents on
2026-08-20 returned these complete B-Rep bounding boxes:

| Fusion document | Nominal B-Rep envelope |
|---|---:|
| `MOTOR_GIM6010-8-DE`, v1 | 44.0000 × 80.0000 × 80.0000 mm |
| `MOTOR_GIM4305-10_GDZ34`, v1 | 33.0000 × 54.1982 × 54.1982 mm |

For the GIM4305-10, the design's cylindrical housing datum remains Ø53 mm; the
slightly larger bounding-box width includes protruding exterior geometry.

STEP geometry is sufficient for nominal design dimensions and mating geometry.
It does not prove the delivered unit's manufacturing tolerance, exact electrical
variant, or the dimensional error of a particular print. With no calipers, close
those uncertainties by printing a negative ABS mating coupon (or the actual ABS
mating part) and treating the real actuator, real fasteners, and real dowels as a
go/no-go fixture. The existing `GAUGE_*_Motor_Interface.stl` files are positive
motor stand-ins and cannot serve as sockets for this check.

## Material decision for the first campaign

The owner's first articles are **ABS**. ABS is appropriate for mating coupons,
assembly rehearsal, cable-routing parts, guards, floor-contact parts, and an
unloaded/hand-driven leg. Do not use an ABS result as PA-CF print compensation,
and do not apply stall torque, spring-characterisation loads, drops, or other
structural proof loads to the ABS load path. Repeat the critical mating coupon in
PA-CF before printing or loading the structural release parts.

## Source mapping and integrity

The repository copies have their embedded camera metadata removed before public
release. The untouched originals are retained locally under the ignored
`.private_evidence/` directory. The original-attachment hashes preserve the
chain of custody; the public-copy hashes verify the files committed here.

| Project file | Original attachment | Original SHA-256 | Public copy SHA-256 |
|---|---|---|---|
| `gim6010-8_01_driver-side-overview.jpeg` | `IMG_0573.jpeg` | `8a23145fe5db88c6c5357ddf999331a8aba1285d6e67b8151836ddccbecc2b9f` | `fdb55f4f749e29f0782c8f7db7bce9fda22d13e05100a8506b4f400e1f81f294` |
| `gim6010-8_02_driver-labels-and-connectors.jpeg` | `IMG_0574.jpeg` | `6b10a510ccade9e8703634876863eb1575750d3a6d591fb74946569c8b857628` | `1f1c1907e5ef0ed421808c2bb6a818a00be635ec8d0ffff7d0a11a3dbcdaa7c6` |
| `gim6010-8_03_output-interface.jpeg` | `IMG_0575.jpeg` | `f30891443b940ed789ed449412ccb8ad767b51c3e408c56fca9e80573144b9a3` | `871e3ec6001641ff051d3ba400459294fb38f85d131a61eeb51f2081631e9f50` |
| `gim4305-10_00_driver-side-overview-with-breakout.jpeg` | `IMG_0576.jpeg` | `020988bfd52f48666508564f6234355547c2616ce93c8108021d5635a160dfba` | `3941e913bec5d6fd90f63ff5de6933e87435d23ca1f372392be1fca6533e64f4` |
| `gim4305-10_01_driver-side-terminal-breakout.jpeg` | `IMG_0577.jpeg` | `153318fa3f84e84fd86c19898cb76a91bdfc611b55a840342a03dadc136a17c7` | `c12664d4bac28936697178675bf5aee5ea9d7ecf20bd8bac37e0e1d6ed2a6759` |
| `gim4305-10_02_driver-side-usbc-breakout.jpeg` | `IMG_0578.jpeg` | `6b698e7a85294e4e5975356b62225d5d2aa4bbb49930af2c1f4c9e7c0c967346` | `0e17c7dea4d061bbbf47b3312285a3d20564703848ec310b92ae883c80075092` |
| `gim4305-10_03_driver-side-connectors.jpeg` | `IMG_0579.jpeg` | `5b5c23591e548ef16693b051f71b8beb060553a9a21c8a5bf701d492861d9664` | `a736c64884bd741dd625700ec4d1d556f5584b713c68fd14e7cf09b54f1d7a0c` |
| `gim4305-10_04_output-interface-and-accessories.jpeg` | `IMG_0580.jpeg` | `421a77a399648ff376712122a5257003dc4d15674c15c046d4b548ad23f7faa2` | `99896947b82a76f39c4b47ac70094412fd933a8911f02c9830b9bab72043a21b` |
