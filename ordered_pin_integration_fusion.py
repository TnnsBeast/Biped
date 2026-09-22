"""Fusion-authored release for the 2026-09-21 ordered pin integration.

Run only through the Fusion MCP with ``Beni_SingleLegRig`` active.  This does
not accept unreceived hardware.  It exports the four printed parts whose
geometry now deliberately uses the seller-listed dimensions, while preserving
the hand-fit gate when the order arrives.
"""

import json
import os

import adsk.core

import beni_lib as B
import rig_lib as R
import rig_export as E
import mechanical_spring_test_fusion as M


ROOT = os.path.dirname(os.path.realpath(__file__))
OUT_DIR = os.path.join(ROOT, 'first_article_stl', 'ordered_pin_integration')
EVIDENCE_DIR = os.path.join(
    ROOT, 'evidence', 'assembly', '2026-09-21_ordered_pin_integration')


def _round(value):
    return round(float(value), 6)


def release(_context: str):
    app = adsk.core.Application.get()
    assert app.activeDocument.name == 'Beni_SingleLegRig'
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    R.replace_cart_stops()
    R.ref_assert()
    R.placed_assert()
    B.capture_nominal(force=True)

    parts = [
        ('Shoulder_Output_Hub_L',
         'ABS_PINREV_Shoulder_Output_Hub_D4p15_ROOT_D4x10_PRINT_ORIENTED',
         E._export_max_y_face_down,
         'Ø56 outboard flange face on bed. No supports. The three Ø4.05 x '
         '5.0 root-dowel sockets are vertical 4 mm bridges; inspect their '
         'ceilings before installing pins or inserts.'),
        ('Proximal_Link_L',
         'ABS_PINREV_Proximal_Link_D19p15_ROOT_D4x10_M4x40_PRINT_ORIENTED',
         E._export_max_y_face_down,
         'Verified broad y=90.3 outboard face on bed. No supports in bearing '
         'seats, root sockets, clevis bore or the 20 mm channel. The M4x40 '
         'upper-clevis land grows away from the bed on the inboard side.'),
        ('Distal_Link_L',
         'ABS_PINREV_Distal_Link_D10p30_D6x10_M4x40_PRINT_ORIENTED',
         E._export_min_y_face_down,
         'Verified broad y=59.5 inboard face on bed. Retain the released '
         'selective-support policy under the knee receiver land, raised web, '
         'wheel-end underside and open channel ceiling. Block support from '
         'all fit bores. The lower-clevis land grows away from the bed.'),
        (M.STOP,
         'ABS_PINREV_Knee_Stop_Plate_15deg_D6x10_CAPTIVE_PRINT_ORIENTED',
         E._export_max_y_face_down,
         'Closed 0.8 mm outboard skin on bed; the 5.0 mm pin channel opens '
         'upward. No supports. Inspect the skin and all three M3 holes.'),
    ]

    exports = []
    meshes = {}
    topology = {}
    for source, export_name, exporter, policy in parts:
        occurrence = B.find_occ(source)
        assert occurrence is not None
        topology[source] = M._topology(occurrence)
        row = R.guarded(exporter, occurrence, export_name, OUT_DIR, policy)
        exports.append(row)
        meshes[export_name] = M._verify_binary_stl(
            row['stl'], topology[source]['volume_mm3'])

    assembly_image = os.path.join(
        EVIDENCE_DIR, '00_fusion_ordered_pin_integration_phi_0.png')
    M._assembly_image(0.0, assembly_image)
    R.replace_cart_stops()
    B.capture_nominal(force=True)
    R.ref_assert()
    R.placed_assert()

    conservative_cotter_edge = (
        B.CLEVIS_PIN_HOLE_DATUM - B.CLEVIS_PIN_HOLE_D / 2.0
        - B.CLEVIS_RETAINED_STACK - B.CLEVIS_WASHER_T)
    stop_cap_clearance = (
        R.STOP_PLATE_Y0 + R.STOP_SLOT_DEPTH
        - (B.STOP_PIN_SOCKET_Y0 + B.STOP_PIN_LEN))
    manifest = {
        'document': app.activeDocument.name,
        'status': ('FUSION VERIFIED / PRINT RELEASE; ordered metal hardware '
                   'still requires visual inspection and hand fit on arrival'),
        'scope': ('unpowered, clamped, wheel-clear, hand-contained ABS '
                  'mechanical assembly only'),
        'design_decisions': {
            'M4x40_clevis_pins': {
                'quantity': 2,
                'shaft_mm': [B.CLEVIS_PIN_D, B.CLEVIS_PIN_SHAFT_LEN],
                'seller_drawing_hole_mm': [B.CLEVIS_PIN_HOLE_D,
                                            B.CLEVIS_PIN_HOLE_DATUM],
                'printed_stack_mm': B.CLEVIS_RETAINED_STACK,
                'washer': '2 x ISO 7089 M4, 4.3 x 9 x 0.8 mm',
                'conservative_washer_to_hole_edge_clearance_mm':
                    _round(conservative_cotter_edge),
                'upper_land': ('Ø14 integral inboard boss; verified proximal '
                               'outboard print plane unchanged'),
                'lower_land': ('Ø14 integral outboard boss; verified distal '
                               'inboard print plane unchanged'),
                'cotter_orientation': ('rotate each clevis pin so its supplied '
                                       'cotter lies radially away from the knee'),
            },
            'D6x10_stop_dowel': {
                'quantity': 1,
                'distal_socket_mm': [B.STOP_PIN_SOCKET_D,
                                     B.STOP_PIN_SOCKET_DEPTH],
                'distal_socket_floor_mm':
                    _round(B.STOP_PIN_SOCKET_Y0 - B.CH_Y1),
                'plate_channel_depth_mm': R.STOP_SLOT_DEPTH,
                'plate_outer_skin_mm': _round(R.STOP_OUTER_SKIN),
                'pin_end_cap_clearance_mm': _round(stop_cap_clearance),
                'retention': ('captured between printed floor and stop-plate '
                              'skin; no adhesive or press fit required'),
                'stop_fasteners': '3 x M3 x 10 SHCS into existing M3 inserts',
            },
            'D4x10_shoulder_root_dowels': {
                'quantity': 3,
                'pcd_mm': B.ROOT_DOWEL_PCD,
                'angles_deg': list(B.ROOT_DOWEL_A),
                'hub_press_socket_mm': [B.ROOT_DOWEL_HUB_SOCKET_D,
                                        B.ROOT_DOWEL_HUB_DEPTH],
                'link_slip_socket_mm': [B.ROOT_DOWEL_LINK_SOCKET_D,
                                        B.ROOT_DOWEL_LINK_DEPTH],
                'axial_bottom_clearance_mm': _round(
                    B.ROOT_DOWEL_LINK_DEPTH
                    - (B.ROOT_DOWEL_LEN - B.ROOT_DOWEL_HUB_DEPTH)),
                'retention': ('press in hub, slip in link, axially captive '
                              'after the six M4 screws clamp the faces'),
            },
        },
        'unchanged_gates': [
            'The ordered pins are not accepted until visually undamaged and '
            'they enter the released receivers by hand; no measurement is required.',
            'The D10 knee-pin spacer/bracket remains test-only and final D10 '
            'retention plus encoder coupling remain open.',
            'ABS is released only for the supported unpowered test. Repeat '
            'same-orientation fit coupons before the later PA-CF build.',
        ],
        'topology': topology,
        'exports': exports,
        'mesh_verification': meshes,
        'assembly_image': assembly_image,
        'mechanical_audit': os.path.join(
            M.EVIDENCE_DIR, 'fusion_mechanical_audit.json'),
    }
    for path in (os.path.join(OUT_DIR, 'fusion_manifest.json'),
                 os.path.join(EVIDENCE_DIR, 'fusion_release_manifest.json')):
        with open(path, 'w', encoding='utf-8') as stream:
            json.dump(manifest, stream, indent=2, sort_keys=True)
            stream.write('\n')
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return manifest
