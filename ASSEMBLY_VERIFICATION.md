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
