"""Release the ABS Ø10.30 steel-pin-fit distal-link first article.

Run every function in this file through the Fusion MCP with
``Beni_SingleLegRig`` active.  The export is a physical fit and assembly-path
article.  It does not release the unresolved pin retention, encoder carrier,
spring cartridge, powered motion, or structural loading.
"""

from collections import Counter
import hashlib
import json
import math
import os
import struct

import adsk.core
import adsk.fusion

import beni_lib as B
import rig_lib as R
import rig_export as E


ROOT = os.path.dirname(os.path.realpath(__file__))
OUT_DIR = os.path.join(ROOT, 'first_article_stl', 'assembly_dry_fit')
EVIDENCE_DIR = os.path.join(
    ROOT, 'evidence', 'knee_fit', '2026-09-16_distal_d10p30_release')
EXPORT_NAME = 'ABS_FA_Distal_Link_L_D10p30_STEEL_PIN_FIT_PRINT_ORIENTED'


def _tm():
    return adsk.fusion.TemporaryBRepManager.get()


def _occs(prefix):
    return [o for o in B.root().allOccurrences
            if o.component.name.startswith(prefix)]


def _copy_occ(occ):
    return _tm().copy(occ.bRepBodies.item(0))


def _shifted(body, x=0.0, y=0.0, z=0.0):
    result = _tm().copy(body)
    transform = adsk.core.Matrix3D.create()
    transform.translation = adsk.core.Vector3D.create(x / 10.0, y / 10.0,
                                                       z / 10.0)
    assert _tm().transform(result, transform)
    return result


def _overlap(a, b):
    aa, bb = a.boundingBox, b.boundingBox
    if any(getattr(aa.maxPoint, v) <= getattr(bb.minPoint, v) + 1e-8 or
           getattr(bb.maxPoint, v) <= getattr(aa.minPoint, v) + 1e-8
           for v in ('x', 'y', 'z')):
        return 0.0
    result = _tm().copy(a)
    assert _tm().booleanOperation(
        result, b, adsk.fusion.BooleanTypes.IntersectionBooleanType)
    return result.volume * 1000.0


def _cut(a, b):
    assert _tm().booleanOperation(
        a, b, adsk.fusion.BooleanTypes.DifferenceBooleanType)
    return a


def _cylinder(x, z, diameter, y0, y1):
    return _tm().createCylinderOrCone(
        adsk.core.Point3D.create(x / 10.0, y0 / 10.0, z / 10.0),
        diameter / 20.0,
        adsk.core.Point3D.create(x / 10.0, y1 / 10.0, z / 10.0),
        diameter / 20.0)


def _topology(occ):
    assert occ.component.bRepBodies.count == 1
    body = occ.component.bRepBodies.item(0)
    assert body.isSolid and body.lumps.count == 1
    assert all(edge.faces.count == 2 for edge in body.edges)
    return {
        'volume_mm3': body.volume * 1000.0,
        'faces': body.faces.count,
        'edges': body.edges.count,
        'closed_manifold': True,
    }


def _downward_faces(body):
    rows = []
    for index, face in enumerate(body.faces):
        ok, normal = face.evaluator.getNormalAtPoint(face.pointOnFace)
        assert ok
        if not adsk.core.Plane.cast(face.geometry) or normal.y >= -0.999999:
            continue
        bb = face.boundingBox
        rows.append({
            'index': index,
            'y_mm': face.pointOnFace.y * 10.0,
            'area_mm2': face.area * 100.0,
            'bbox_xz_mm': [bb.minPoint.x * 10.0, bb.maxPoint.x * 10.0,
                           bb.minPoint.z * 10.0, bb.maxPoint.z * 10.0],
        })
    return rows


def _support_envelope(occ, label, y_mm, minimum_area_mm2, maximum_area_mm2,
                      depth_mm,
                      removal_directions):
    """Build, test, and delete one native-Fusion selective-support envelope."""
    body = occ.component.bRepBodies.item(0)
    candidates = []
    for face in body.faces:
        ok, normal = face.evaluator.getNormalAtPoint(face.pointOnFace)
        if (ok and adsk.core.Plane.cast(face.geometry) and
                normal.y < -0.999999 and
                abs(face.pointOnFace.y * 10.0 - y_mm) < 0.001 and
                minimum_area_mm2 <= face.area * 100.0 <= maximum_area_mm2):
            candidates.append(face)
    if len(candidates) != 1:
        raise RuntimeError('%s support face selection returned %d faces' %
                           (label, len(candidates)))
    face = candidates[0]
    source_area = face.area * 100.0
    geometry = _tm().copy(body)
    ext_input = occ.component.features.extrudeFeatures.createInput(
        face, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext_input.setDistanceExtent(
        False, adsk.core.ValueInput.createByReal(depth_mm / 10.0))
    feature = occ.component.features.extrudeFeatures.add(ext_input)
    support = _shifted(feature.bodies.item(0), y=-0.4)
    assert feature.deleteMe()
    body = occ.component.bRepBodies.item(0)
    if _overlap(support, geometry) > 0.00001:
        _cut(support, geometry)

    # Reserve the same 0.6 mm XY separation used by the accepted supported
    # mock-up.  The knee receiver gets an explicit bore keepout as well.
    for dx, dz in ((0.6, 0), (-0.6, 0), (0, 0.6), (0, -0.6),
                   (0.6, 0.6), (0.6, -0.6), (-0.6, 0.6), (-0.6, -0.6)):
        shifted_geometry = _shifted(geometry, x=dx, z=dz)
        if _overlap(support, shifted_geometry) > 0.00001:
            _cut(support, shifted_geometry)
    if label in ('knee_receiver_land', 'knee_web', 'wheel_end'):
        # Remove every column shadowed by material closer to the build plate.
        # Those regions need no slicer support and would make a downward
        # withdrawal test report a false trapped-support collision.
        for step in range(1, int(math.ceil(depth_mm / 0.5)) + 2):
            shadow = _shifted(geometry, y=step * 0.5)
            if _overlap(support, shadow) > 0.00001:
                _cut(support, shadow)
    keepout = _cylinder(B.KX, B.KZ, 11.0, B.LEG_Y_IN - 2.0,
                        B.LEG_Y_OUT + 2.0)
    if _overlap(support, keepout) > 0.00001:
        _cut(support, keepout)

    paths = []
    for dx, dy, dz in removal_directions:
        maximum = 0.0
        for step in range(81):
            moved = _shifted(support, x=dx * step * 0.5,
                             y=dy * step * 0.5,
                             z=dz * step * 0.5)
            maximum = max(maximum, _overlap(moved, geometry))
            if maximum > 0.001:
                break
        paths.append({'direction': [dx, dy, dz],
                      'maximum_interference_mm3': maximum})
    clear = [row for row in paths
             if row['maximum_interference_mm3'] <= 0.001]
    if not clear:
        raise RuntimeError('%s has no support-removal path' % label)
    return {
        'label': label,
        'source_face_y_mm': y_mm,
        'source_face_area_mm2': source_area,
        'support_volume_mm3': support.volume * 1000.0,
        'top_bottom_gap_mm': 0.4,
        'lateral_gap_mm': 0.6,
        'knee_bore_keepout_diameter_mm': 11.0,
        'clear_removal_paths': clear,
        'travel_checked_mm': 40.0,
    }


def _verify_binary_stl(path, native_volume_mm3):
    data = open(path, 'rb').read()
    triangles = struct.unpack_from('<I', data, 80)[0]
    assert len(data) == 84 + triangles * 50
    edges = Counter()
    degenerate = 0
    volume = 0.0
    points = []
    for index in range(triangles):
        values = struct.unpack_from('<12fH', data, 84 + index * 50)
        tri = [tuple(values[3 + i * 3:6 + i * 3]) for i in range(3)]
        points.extend(tri)
        if len(set(tri)) < 3:
            degenerate += 1
        for i in range(3):
            edges[tuple(sorted((tri[i], tri[(i + 1) % 3])))] += 1
        a, b, c = tri
        volume += (a[0] * (b[1] * c[2] - b[2] * c[1]) +
                   a[1] * (b[2] * c[0] - b[0] * c[2]) +
                   a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0
    result = {
        'file': path,
        'triangles': triangles,
        'nonmanifold_edges': sum(count != 2 for count in edges.values()),
        'degenerate_triangles': degenerate,
        'minimum_z_mm': min(p[2] for p in points),
        'dimensions_mm': [max(p[i] for p in points) - min(p[i] for p in points)
                          for i in range(3)],
        'mesh_volume_mm3': volume,
        'native_volume_relative_error':
            abs(volume - native_volume_mm3) / native_volume_mm3,
        'sha256': hashlib.sha256(data).hexdigest(),
    }
    assert result['nonmanifold_edges'] == 0
    assert result['degenerate_triangles'] == 0
    assert abs(result['minimum_z_mm']) < 0.00001
    assert result['native_volume_relative_error'] < 0.002
    return result


def release(_context=''):
    app = adsk.core.Application.get()
    assert app.activeDocument.name == 'Beni_SingleLegRig'
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    R.ref_assert()
    R.placed_assert()

    distal_occ = B.find_occ('Distal_Link_L')
    proximal_occ = B.find_occ('Proximal_Link_L')
    bearing_occs = _occs('HW_Bearing_6800')
    assert distal_occ and proximal_occ and len(bearing_occs) == 2
    topology = _topology(distal_occ)
    distal = _copy_occ(distal_occ)
    fixed = [_copy_occ(proximal_occ)] + [_copy_occ(o) for o in bearing_occs]

    radial_path = []
    for step in range(241):
        offset = 120.0 - step * 0.5
        trial = _shifted(distal, x=offset)
        interference = sum(_overlap(trial, body) for body in fixed)
        assert interference <= 0.001, (offset, interference)
        radial_path.append({'offset_x_mm': offset,
                            'interference_mm3': interference})

    pin = _cylinder(B.KX, B.KZ, 10.0, R.AXLE_Y0,
                    R.AXLE_Y0 + R.PIN_LEN)
    pin_path = []
    for step in range(101):
        offset = -50.0 + step * 0.5
        trial = _shifted(pin, y=offset)
        interference = sum(_overlap(trial, body)
                           for body in fixed + [distal])
        assert interference <= 0.001, (offset, interference)
        pin_path.append({'offset_y_mm': offset,
                         'interference_mm3': interference})

    bore_bracket = {}
    for diameter in (10.29, 10.30, 10.31):
        probe = _cylinder(B.KX, B.KZ, diameter,
                          R.PRINTED_RECEIVER_Y0,
                          R.PRINTED_RECEIVER_Y1)
        bore_bracket[str(diameter)] = _overlap(distal, probe)
    assert bore_bracket['10.29'] <= 0.001
    assert bore_bracket['10.3'] <= 0.02
    assert bore_bracket['10.31'] > 3.0

    downward = _downward_faces(distal_occ.component.bRepBodies.item(0))
    saved_transforms = R.xf_capture()
    lateral = [(math.cos(math.radians(angle)), 0.0,
                math.sin(math.radians(angle)))
               for angle in range(0, 360, 15)]
    supports = [
        _support_envelope(distal_occ, 'knee_receiver_land', 64.5, 100.0, 200.0,
                          5.2, [(0.0, -1.0, 0.0)]),
        _support_envelope(distal_occ, 'knee_web', 65.0, 800.0, 1000.0,
                          5.2, [(0.0, -1.0, 0.0)]),
        _support_envelope(distal_occ, 'wheel_end', 64.5, 600.0, 700.0,
                          5.2, [(0.0, -1.0, 0.0)]),
        _support_envelope(distal_occ, 'open_channel', 84.5, 900.0, 1100.0,
                          19.4, lateral),
    ]
    B.design().computeAll()
    adsk.doEvents()
    R.xf_restore(saved_transforms)
    R.replace_cart_stops()
    R.ref_assert()
    R.placed_assert()

    support_policy = (
        'ABS steel-pin fit first article. Import unchanged; broad inboard '
        'source face down, making the Ø10.30 bore bed-normal like its coupon. '
        'Use painted/manual normal supports only under the Ø16 knee receiver '
        'land, raised knee web, wheel-end underside and open channel ceiling. '
        'For a 0.20 mm layer profile use at least 0.4 mm top/bottom support '
        'distance and 0.6 mm XY distance. Block support from the entire knee '
        'bore, cartridge and stop bores, motor cover opening, motor screw holes '
        'and motor mounting face. Remove lower supports toward the bed and the '
        'channel support through its open side. Inspect all supported surfaces. '
        'Fit/assembly article only: no spring, powered motion, ground contact '
        'or structural load; pin retention and encoder coupling remain held.')
    saved_transforms = R.xf_capture()
    export = E._export_min_y_face_down(
        distal_occ, EXPORT_NAME, OUT_DIR, support_policy)
    B.design().computeAll()
    adsk.doEvents()
    R.xf_restore(saved_transforms)
    R.replace_cart_stops()
    R.ref_assert()
    R.placed_assert()
    mesh = _verify_binary_stl(export['stl'], topology['volume_mm3'])

    audit = {
        'document': app.activeDocument.name,
        'status': 'ABS STEEL-PIN FIT ARTICLE RELEASE; retention still held',
        'source': {
            'part': 'Distal_Link_L',
            'bore_diameter_mm': B.ABS_KNEE_PIN_BORE_D,
            'receiver_y_mm': [R.PRINTED_RECEIVER_Y0,
                              R.PRINTED_RECEIVER_Y1],
            'receiver_span_mm': R.PRINTED_RECEIVER_Y1 - R.PRINTED_RECEIVER_Y0,
            'bearing_inner_faces_y_mm': [R.SLEEVE_Y0, R.SLEEVE_Y1],
            'axial_clearance_each_side_mm':
                R.PRINTED_RECEIVER_Y0 - R.SLEEVE_Y0,
            'topology': topology,
            'downward_faces': downward,
        },
        'bore_overlap_bracket_mm3': bore_bracket,
        'assembly_path': {
            'description': ('detached distal link translates from +X into the '
                            'supported proximal fork with both bearings '
                            'already installed; reverse for service'),
            'samples': radial_path,
            'maximum_interference_mm3':
                max(row['interference_mm3'] for row in radial_path),
        },
        'pin_path': {
            'description': 'Ø10 nominal pin enters from the inboard -Y side',
            'samples': pin_path,
            'maximum_interference_mm3':
                max(row['interference_mm3'] for row in pin_path),
        },
        'selective_support_audit': supports,
        'export': export,
        'mesh_verification': mesh,
        'physical_acceptance': [
            'support both links; keep motors and spring disconnected',
            'distal link enters and leaves the bearing-installed fork along +X',
            'steel pin inserts fully with firm thumb pressure and withdraws by hand',
            'no free pin spin or perceptible radial rock in the printed receiver',
            '0.8 mm nominal axial clearance per side is checked for excessive play',
            'do not power or load the joint; retention and encoder coupling are unreleased',
        ],
    }
    path = os.path.join(EVIDENCE_DIR, 'fusion_release.json')
    with open(path, 'w', encoding='utf-8') as stream:
        json.dump(audit, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({
        'status': audit['status'],
        'bore_diameter_mm': B.ABS_KNEE_PIN_BORE_D,
        'receiver_span_mm': audit['source']['receiver_span_mm'],
        'axial_clearance_each_side_mm':
            audit['source']['axial_clearance_each_side_mm'],
        'assembly_path_samples': len(radial_path),
        'assembly_path_max_interference_mm3':
            audit['assembly_path']['maximum_interference_mm3'],
        'pin_path_samples': len(pin_path),
        'pin_path_max_interference_mm3':
            audit['pin_path']['maximum_interference_mm3'],
        'selective_support_regions': [row['label'] for row in supports],
        'stl': export['stl'],
        'mesh': mesh,
        'evidence': path,
        'guards': 'PASS',
    }, indent=2, sort_keys=True))
    return audit
