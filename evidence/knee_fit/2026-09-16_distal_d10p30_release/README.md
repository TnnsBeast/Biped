# Ø10.30 ABS distal-link steel-pin fit release

Date: 2026-09-16
Fusion document: `Beni_SingleLegRig` v26

## Result

The shin/distal link is released as an **ABS steel-pin fit and physical
assembly-path article**. Its bed-ready STL is:

[`../../../first_article_stl/assembly_dry_fit/ABS_FA_Distal_Link_L_D10p30_STEEL_PIN_FIT_PRINT_ORIENTED.stl`](../../../first_article_stl/assembly_dry_fit/ABS_FA_Distal_Link_L_D10p30_STEEL_PIN_FIT_PRINT_ORIENTED.stl)

The bore is Ø10.30 over a 20.0 mm printed receiver. Fusion found and corrected
an assembly defect before export: the earlier 21.6 mm integrated receiver
copied the deleted steel sleeve's span, extending 0.8 mm into both bearing
pockets. It had zero interference in its final pose but no insertion or removal
path. Confining the printed receiver to the clear 64.5–84.5 mm fork gap leaves
0.8 mm axial clearance to each bearing and restores serviceability.

## Fusion verification

- One closed solid body, 48,470.860 mm³.
- Exact cylindrical bore radius 5.15 mm over y = 64.5–84.5 mm.
- 241 sampled +X assembly/service poses over 120 mm: zero interference with
  the proximal link and both installed bearing envelopes.
- 101 sampled inboard steel-pin insertion poses: zero modeled interference.
- Four selective-support envelopes have verified removal paths: knee receiver
  land, knee web, wheel-end underside and open channel.
- Exported STL: 5,990 triangles, zero nonmanifold edges, zero degenerate
  triangles, z-min 0, native/mesh volume error 0.0134%.
- Mode A checks 1–8 passed on the corrected geometry before the v25 save.
  Knee-sweep deviation remains 0.043 mm; 17 shoulder poses have zero clashes.
- The v26 rerun increased the modeled/specified support separation to 0.4 mm;
  all four support-removal paths still pass and the source geometry and STL hash
  are unchanged.
- Reference motor and cartridge-transform guards passed before and after
  export. The saved document was re-read after save and remains unmodified.

Machine-readable records: [`fusion_release.json`](fusion_release.json),
[`saved_fusion_document.json`](saved_fusion_document.json), and
[`mode_a_checks_summary.json`](mode_a_checks_summary.json).

## Print policy

Import the supplied STL unchanged with the broad inboard face down. Use the
same enclosed ABS process as the coupon. Paint normal supports only under the
knee receiver land, raised knee web, wheel-end underside and open channel
ceiling. At 0.20 mm layers, use at least 0.4 mm top/bottom separation and
0.6 mm XY separation. Block support from all bores, the motor opening and
mounting interfaces. The complete slicer and removal instructions are in the
[assembly-dry-fit traveller](../../../first_article_stl/assembly_dry_fit/README.md).

## Physical acceptance owed

1. Support both links; keep the motors and spring disconnected.
2. Install both bearings in the proximal link, then insert the detached shin
   along the verified straight path. Reverse the path once to prove service.
3. Insert the recovered steel pin from the inboard side using thumb pressure.
4. Confirm full insertion and hand withdrawal, with no hammer or clamp.
5. Confirm no free spin or perceptible radial rock in the printed receiver.
6. Check the 0.8 mm nominal clearance on each side for unacceptable axial play.

The pin count, listing tolerance and separate pin-through-each-bearing results
remain unrecorded.

## Hold that remains

This release does not make the knee ready for powered use. The existing
`RIG_Knee_Collar_L` cannot retain the pin, and the magnet carrier/encoder
coupling still needs its own release. Keep the spring off the leg and perform
no powered motion, ground contact or structural loading with this article.
