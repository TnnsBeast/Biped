"""Verify the Ø4.5 Fusion sources and the three promoted ABS STL exports.

Run only through the Fusion MCP with ``Beni_SingleLegRig`` active.  The B-Rep
checks establish the receiver diameters and depths; the binary-STL checks bind
those verified Fusion exports to hashes and validate their printable meshes.
"""
import hashlib
import json
import math
import os
import struct
import sys
from collections import Counter

import adsk.core


OUT = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.abspath(os.path.join(OUT, '..', '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import beni_lib as B
import rig_lib as R


def _mesh(path):
    data = open(path, 'rb').read()
    if len(data) < 84:
        raise RuntimeError('truncated binary STL: %s' % path)
    facets = struct.unpack_from('<I', data, 80)[0]
    if len(data) != 84 + facets * 50:
        raise RuntimeError('binary STL length mismatch: %s' % path)

    vertices = set()
    edges = Counter()
    degenerate = 0
    signed_volume = 0.0
    for index in range(facets):
        row = struct.unpack_from('<12fH', data, 84 + index * 50)
        tri = tuple(tuple(float(value) for value in row[start:start + 3])
                    for start in (3, 6, 9))
        vertices.update(tri)
        for edge in range(3):
            edges[tuple(sorted((tri[edge], tri[(edge + 1) % 3])))] += 1
        a, b, c = tri
        cross = ((b[1] - a[1]) * (c[2] - a[2]) -
                 (b[2] - a[2]) * (c[1] - a[1]),
                 (b[2] - a[2]) * (c[0] - a[0]) -
                 (b[0] - a[0]) * (c[2] - a[2]),
                 (b[0] - a[0]) * (c[1] - a[1]) -
                 (b[1] - a[1]) * (c[0] - a[0]))
        if math.sqrt(sum(value * value for value in cross)) <= 1e-9:
            degenerate += 1
        signed_volume += (
            a[0] * (b[1] * c[2] - b[2] * c[1])
            + a[1] * (b[2] * c[0] - b[0] * c[2])
            + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0

    incidence = Counter(count for count in edges.values() if count != 2)
    minimum = [min(vertex[axis] for vertex in vertices) for axis in range(3)]
    maximum = [max(vertex[axis] for vertex in vertices) for axis in range(3)]
    return {
        'path': os.path.relpath(path, ROOT),
        'bytes': len(data),
        'sha256': hashlib.sha256(data).hexdigest(),
        'facets': facets,
        'vertices': len(vertices),
        'edge_incidence_errors': dict(incidence),
        'degenerate_facets': degenerate,
        'minimum_mm': minimum,
        'maximum_mm': maximum,
        'envelope_mm': [maximum[i] - minimum[i] for i in range(3)],
        'mesh_volume_mm3': abs(signed_volume),
    }


def _check_mesh(path, expected_envelope, expected_volume, require_z0=True):
    row = _mesh(path)
    if row['edge_incidence_errors'] or row['degenerate_facets']:
        raise RuntimeError('STL is not a clean closed manifold: %s' % row)
    if require_z0 and abs(row['minimum_mm'][2]) >= 0.001:
        raise RuntimeError('STL is not seated at Z=0: %s' % row)
    # Fusion's high-refinement tessellation can stop a few hundredths short
    # of an analytic circular extremum even though the B-Rep box is exact.
    if any(abs(actual - expected) >= 0.05 for actual, expected in
           zip(row['envelope_mm'], expected_envelope)):
        raise RuntimeError('STL envelope mismatch: %s' % row)
    relative_error = abs(row['mesh_volume_mm3'] - expected_volume) / expected_volume
    if relative_error >= 0.002:
        raise RuntimeError('STL volume mismatch: %s' % row)
    row['expected_envelope_mm'] = expected_envelope
    row['fusion_brep_volume_mm3'] = expected_volume
    row['volume_relative_error'] = relative_error
    row['bed_datum_required'] = require_z0
    row['status'] = 'PASS'
    return row


def _volume(occ):
    return sum(body.volume * 1000.0 for body in occ.component.bRepBodies)


def run(_context: str):
    app = adsk.core.Application.get()
    if app.activeDocument.name != 'Beni_SingleLegRig':
        raise RuntimeError('Beni_SingleLegRig must be active')

    plate = B.find_occ('Chassis_Shoulder_Plate_L')
    proximal = B.find_occ('Proximal_Link_L')
    stand = B.find_occ('RIG_Stand')
    if not all((plate, proximal, stand)):
        raise RuntimeError('plate, proximal link and stand must exist')

    specs = {
        'Chassis_Shoulder_Plate_L': (
            plate, B._receiver_centres(0.0, 0.0, B.CABLE_COVER_PCD, 4, 45.0),
            4, (B.SH_PLATE_Y0, B.SH_PLATE_Y1)),
        'Proximal_Link_L': (
            proximal,
            ([B.kpt(B.STOP_BOLT_R, angle) for angle in B.STOP_BOLT_A] +
             [B.kpt(15.0, angle) for angle in (60.0, 140.0)]),
            5, (B.KNEE_BOSS_B_Y1 - B.INSERT_LEN, B.KNEE_BOSS_B_Y1)),
        'RIG_Stand': (
            stand, R.PANEL_FRAME_BOLTS, 5,
            (R.STAND_Y1 - R.INSERT_M3_HOLE_DEPTH, R.STAND_Y1)),
    }
    sources = {}
    for name, (occ, centres, expected_count, expected_span) in specs.items():
        spans = B._receiver_face_spans(occ, B.M3_INSERT_RECEIVER_D, centres)
        got = sorted((round(y0, 3), round(y1, 3))
                     for y0, y1 in spans.values())
        want = tuple(round(value, 3) for value in expected_span)
        if len(spans) != expected_count or any(span != want for span in got):
            raise RuntimeError('%s receiver mismatch: %s' % (name, got))
        sources[name] = {
            'nominal_diameter_mm': B.M3_INSERT_RECEIVER_D,
            'receiver_count': len(spans),
            'receiver_spans_mm': got,
            'status': 'PASS',
        }

    access_report_path = os.path.join(
        ROOT, 'evidence', 'assembly', '2026-09-05_access_fix',
        'proximal_release.json')
    with open(access_report_path, encoding='utf-8') as stream:
        access_report = json.load(stream)
    if (access_report['m3_receiver_diameter_mm'] != B.M3_INSERT_RECEIVER_D or
            access_report['m3_receiver_count'] != 5):
        raise RuntimeError('corrected proximal release does not use Ø4.5')

    meshes = {
        'RIG_Stand_native_assembly_coordinates': _check_mesh(
            os.path.join(ROOT, 'rig_stl', 'RIG_Stand.stl'),
            [200.0, 32.0, 299.3119], _volume(stand), require_z0=False),
        'RIG_Stand': _check_mesh(
            os.path.join(ROOT, 'first_article_stl', 'mode_a',
                         'ABS_FA_RIG_Stand_M3_INSERTS_PRINT_ORIENTED.stl'),
            [200.0, 299.3119, 32.0], _volume(stand)),
        'Chassis_Shoulder_Plate_L': _check_mesh(
            os.path.join(ROOT, 'first_article_stl', 'assembly_dry_fit',
                         'ABS_FA_Chassis_Shoulder_Plate_L_M3_INSERTS_PRINT_ORIENTED.stl'),
            [120.0, 120.0, 9.0], _volume(plate)),
        'Proximal_Link_L_D19p15_M4_ACCESS_FIXED': _check_mesh(
            os.path.join(ROOT, 'first_article_stl', 'assembly_dry_fit',
                         'ABS_FA_Proximal_Link_L_D19p15_M4_ACCESS_FIXED_PRINT_ORIENTED.stl'),
            [141.9253, 127.1345, 31.6],
            access_report['topology_and_print']['volume_mm3']),
    }

    result = {
        'status': 'PASS',
        'document': app.activeDocument.name,
        'physical_selection': os.path.relpath(
            os.path.join(OUT, 'result.json'), ROOT),
        'fusion_source_checks': sources,
        'stl_checks': meshes,
        'protected_occurrences': {
            'reference_guard': R.ref_assert(verbose=False),
            'placed_guard': R.placed_assert(verbose=False),
        },
        'verification_method': (
            'Fusion MCP B-Rep receiver inspection plus binary STL manifold, '
            'bed-datum, envelope, volume and SHA-256 checks'),
    }
    path = os.path.join(OUT, 'fusion_release_verification.json')
    with open(path, 'w', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'verification': path, 'result': result}, sort_keys=True))
