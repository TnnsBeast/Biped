# Owner report — spring bows and escapes during knee compression

The owner reports the three PINREV2 parts printed and the article assembled:
“Mostly things work well,” but when compressing the joint the spring compresses
“in a curved motion rather than straight down” and “flies out the side.”

**Physical spring-retention check: FAIL.** Suspend spring-installed motion and
powered commissioning of this assembly until the cause is resolved. Keep motors
unplugged; spring-free inspection may continue with the leg supported.

## Owner clarification — guide disengaged before compression

The owner confirms that with the spring uncompressed the guide bar is not
engaged, and on compression it does not engage every time. The owner also
rejects the loose-guide arrangement as difficult to assemble.

This establishes loss of guide engagement at the starting physical condition.
Intermittent re-entry is consistent with the reported loss of alignment and
spring escape. It does not establish why the guide lacks overlap or whether
the guide, eyes or pilots have sustained damage. The exact knee position,
installed eye orientation and physical guide seating remain unverified.

The existing Fusion audit reports **5.500 mm** guide overlap at the **-8°** stop
with **50.000 mm** installed spring length. The physical observation conflicts
with that intended starting condition if the knee was at the released stop.
Resolve the discrepancy explicitly; do not substitute the nominal overlap for
physical evidence or assume the owner assembled it incorrectly. The audit's
`guide_overlap_mm` is calculated from source parameters at prescribed poses;
it does not demonstrate retention of a loose guide during real assembly.

## Replacement requirements — not a released design

- Guide engagement must persist at full permitted extension and throughout
  compression; no blind re-entry or hand steering during motion.
- The guide must be positively retained against migration or loss during
  installation, handling and extension.
- Assemble the spring and its guidance as a manageable cartridge before
  attaching it to the leg; demonstrate installation and removal without
  simultaneously balancing loose eyes, spring and guide.
- Both eyes must pivot freely, the sliding interface must remain free, and
  the spring must stay seated. Verify guide stiffness and actual spring
  behavior physically as well as the modeled clearances.
- Verify full-extension engagement, full-compression end clearance, stops,
  neighboring-part clearance and service paths through Fusion MCP before
  releasing revised parts. Recheck print orientation and fits.

Simply extending the loose square bar is not an accepted fix: it would not
address retention or assembly ease, and could consume compression clearance.
No replacement dimensions or hardware have been selected. Fusion MCP is not
available in the reporting session; no live CAD inspection or redesign has
been performed. An unloaded photo can help reconcile the existing assembly
with the intended geometry without repeating the spring escape.

This report establishes assembly progress and the failure, not individual
bearing/pin-fit passes or complete assembly acceptance.

The prior [Fusion audit](../2026-09-17_abs_spring_mechanical_test/README.md)
proved modeled clearances, nominal guide overlap and insertion paths. It did
not prove elastic spring stability, printed-guide stiffness or physical spring
capture. No replacement geometry or revised spring test is released by this
report. Any CAD investigation or changed-part verification must use Fusion MCP.
