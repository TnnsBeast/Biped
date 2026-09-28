"""R2A print release gate. Execute only via the Fusion MCP in Beni_R2A_SingleLeg.

Mirrors the legacy mechanical_release_audit_fusion gate for the R2A parts, with
its own reviewed baseline (r2a_release_baseline.json) so the legacy
mechanical_release_baseline.json is never read for writing or rewritten:

  * dimensional_contracts(): measured native cylinder faces vs expected spans;
  * shape_signature(): every face of every released B-Rep;
  * bed_body(): transient copy at the recorded bed pose (a Y face on Z = 0);
  * print_audit(): every downward-facing face in the bed pose, classified;
  * export(): bed-ready binary STL at stl_release.stl_options();
  * mesh_fidelity(): the machine-independent mesh <-> B-Rep proof.

Exports never update the baseline.  Only accept_shapes(), accept_released_files()
and accept_verified_sources() do, each with a written reason in review_log.
"""
import hashlib
import json
import math
import os
import time

import adsk.core
import adsk.fusion

import beni_lib as B
import rig_lib as R
import stl_release as S
import mechanical_release_audit_fusion as A
import r2a_lib as L

ROOT = os.path.dirname(os.path.realpath(__file__))
BASELINE = os.path.join(ROOT, 'r2a_release_baseline.json')
OUT_DIR = os.path.join(ROOT, 'r2a_stl')
EVIDENCE = os.path.join(ROOT, 'evidence', 'r2a', '2026-09-27_digital_gate')
VERIFIED_SOURCES = ['r2a_lib.py', 'r2a_release_fusion.py', 'stl_release.py']

# component, released file stem, bed side (Y face on the bed), qty, material,
# support policy, release state
PARTS = [
    ('R2A_Prox_Inboard_L', 'R2A_Prox_Inboard_L_ABS_Y59p5_DOWN', 'min', 1, 'ABS',
     'none', 'RELEASED'),
    ('R2A_Prox_Outboard_L', 'R2A_Prox_Outboard_L_ABS_Y91p1_DOWN', 'max', 1, 'ABS',
     'none', 'RELEASED'),
    ('R2A_Crank_L', 'R2A_Crank_L_ABS_OUTPUT_FACE_DOWN', 'max', 1, 'ABS', 'none',
     'RELEASED'),
    ('R2A_Crank_Cap_L', 'R2A_Crank_Cap_L_ABS_OUTER_FACE_DOWN', 'min', 2, 'ABS',
     'none', 'RELEASED'),
    ('R2A_Distal_Link_L', 'R2A_Distal_Link_L_ABS_Y59p5_DOWN', 'min', 1, 'ABS',
     'selective', 'RELEASED'),
    ('R2A_Lever_Cap_L', 'R2A_Lever_Cap_L_ABS_OUTER_FACE_DOWN', 'max', 1, 'ABS',
     'none', 'RELEASED'),
    ('R2A_Encoder_Arm_L', 'R2A_Encoder_Arm_L_ABS_TOP_FACE_DOWN', 'max', 1, 'ABS',
     'none', 'RELEASED'),
    ('R2A_Knee_Pin_Cap_L', 'R2A_Knee_Pin_Cap_L_ABS_OUTER_FACE_DOWN', 'min', 1,
     'ABS', 'none', 'RELEASED'),
    ('R2A_Encoder_Bracket_L', 'R2A_Encoder_Bracket_L_ABS_PLATE_DOWN', 'max', 1,
     'ABS', 'none', 'HOLD: AS5048A adapter-board outline not in the repository'),
]


def _assert_doc():
    L.assert_r2a_doc()


def _occ(name):
    o = B.find_occ(name)
    if o is None:
        raise RuntimeError('R2A part missing: ' + name)
    return o


def cylinders(name):
    rows = []
    for body in _occ(name).component.bRepBodies:
        for face in body.faces:
            g = adsk.core.Cylinder.cast(face.geometry)
            if g:
                bb = face.boundingBox
                rows.append({'d': round(g.radius * 20, 4), 'x': g.origin.x * 10,
                             'z': g.origin.z * 10, 'axis': g.axis.asArray(),
                             'y0': round(bb.minPoint.y * 10, 3), 'y1': round(bb.maxPoint.y * 10, 3)})
    return rows


def _pts(name):
    return {r['d'] for r in cylinders(name)}


def contract_table():
    """(part, interface, diameter, expected sorted Y spans, centres or None)."""
    K = [(L.KX, L.KZ)]
    per = [L.uv(*p) for p in L.perimeter_screws_uv()]
    act = [L.suv(L.ACT_PCD / 2.0, a) for a in L.ACT_SCREW_UV]
    crank_m3 = [L.polar((0, 0), B.SH_OUT_PCD / 2.0, 10.8 + 60.0 * i) for i in range(6)]
    crank_pins = [L.polar((0, 0), B.SH_PIN_PCD / 2.0, 41.0 + 120.0 * i) for i in range(3)]
    cd = L._dowel_xz(L.C0, L.crank_arm_xz(), L.CRANK_DOWEL_REL)
    ld = L._dowel_xz(L.P0, L.lever_arm_xz(), L.LEVER_DOWEL_REL)
    enc_d = [L._dxz(p) for p in L.ENC_INSERTS_D]
    enc_dw = [L._dxz(L.ENC_DOWEL_D)]
    tpu = [L.uv(*L.tpu_centre_uv('flex')), L.uv(*L.tpu_centre_uv('ext'))]
    return [
        ('R2A_Prox_Inboard_L', '6800 seat A', L.BRG_SEAT_D, [L.BRG_A], K),
        ('R2A_Prox_Inboard_L', 'bearing lip A', L.LIP_D, [L.LIP_A], K),
        ('R2A_Prox_Inboard_L', 'M4 hub-screw clearance', 4.3, [(59.5, 63.3)] * 6, L.m4_hub_screw_xz()),
        ('R2A_Prox_Inboard_L', 'M4 head counterbores', 7.5, [(63.3, 64.5)] * 6, L.m4_hub_screw_xz()),
        ('R2A_Prox_Inboard_L', 'root dowel slip holes', B.ROOT_DOWEL_LINK_SOCKET_D,
         [(59.5, 64.5)] * 3, L.root_dowel_xz()),
        ('R2A_Prox_Inboard_L', 'TPU plug bores', L.TPU_D, [(59.5, 63.5)] * 2, tpu),
        ('R2A_Prox_Inboard_L', 'pin-cap M3 insert pockets', 4.5, [(59.5, 64.5)] * 2,
         L.pin_cap_insert_xz()),
        ('R2A_Prox_Inboard_L', 'perimeter M3 insert pockets', 4.5, [(78.5, 84.5)] * 6, per),
        ('R2A_Prox_Outboard_L', '6800 seat B', L.BRG_SEAT_D, [L.BRG_B], K),
        ('R2A_Prox_Outboard_L', 'bearing lip B', L.LIP_D, [L.LIP_B], K),
        ('R2A_Prox_Outboard_L', 'actuator M3 clearance', 3.4, [(84.5, 91.1)] * 5, act),
        ('R2A_Prox_Outboard_L', 'perimeter M3 clearance', 3.4, [(84.5, 91.1)] * 6, per),
        ('R2A_Prox_Outboard_L', 'encoder-bracket M3 insert pockets', 4.5, [(86.1, 91.1)] * 2,
         L.enc_insert_xz()),
        ('R2A_Prox_Outboard_L', 'TPU plug bores', L.TPU_D, [(85.5, 91.1)] * 2, tpu),
        ('R2A_Crank_L', 'motor factory-pin passages', B.ABS_SHOULDER_PIN_BORE_D,
         [(79.7, 86.9)] * 3, crank_pins),
        ('R2A_Crank_L', 'motor pin root reliefs', 5.2, [(86.9, 87.6)] * 3, crank_pins),
        ('R2A_Crank_L', 'output M3 clearance', 3.4, [(82.6, 87.6)] * 6, crank_m3),
        ('R2A_Crank_L', 'output M3 head counterbores', 6.2, [(79.7, 82.6)] * 6, crank_m3),
        ('R2A_Crank_L', 'crank pin (blind, 1.0 skin)', L.PIN5_HOLE_D, [(79.7, 86.6)], [L.C0]),
        ('R2A_Crank_L', 'cap dowel sockets', L.DOWEL_HOLE_D, [(71.3, 78.3)] * 2, cd),
        ('R2A_Crank_Cap_L', 'crank pin', L.PIN5_HOLE_D, [(68.3, 71.3)], [L.C0]),
        ('R2A_Crank_Cap_L', 'dowel holes', L.DOWEL_HOLE_D, [(68.3, 71.3)] * 2, cd),
        ('R2A_Distal_Link_L', 'steel knee-pin receiver', L.RECV_D, [L.RECV], K),
        ('R2A_Distal_Link_L', 'lever pin', L.PIN5_HOLE_D, [(65.8, 71.3)], [L.P0]),
        ('R2A_Distal_Link_L', 'lever-cap dowel sockets', L.DOWEL_HOLE_D, [(73.4, 79.7)] * 2, ld),
        ('R2A_Distal_Link_L', 'wheel-motor M2.5 clearance', 2.8, [(59.5, 67.5)] * 6, None),
        ('R2A_Distal_Link_L', 'wheel-motor cover clearance', 41.5, [(59.5, 67.5)], None),
        ('R2A_Distal_Link_L', 'encoder-arm M3 insert pockets', 4.5, [(85.5, 91.0)] * 2, enc_d),
        ('R2A_Distal_Link_L', 'encoder-arm dowel socket', L.DOWEL_HOLE_D, [(86.0, 91.0)], enc_dw),
        ('R2A_Lever_Cap_L', 'lever pin', L.PIN5_HOLE_D, [(79.7, 83.4)], [L.P0]),
        ('R2A_Lever_Cap_L', 'dowel holes', L.DOWEL_HOLE_D, [(79.7, 83.4)] * 2, ld),
        ('R2A_Encoder_Arm_L', 'magnet pocket', L.MAG_D, [L.ENC_MAG], K),
        ('R2A_Encoder_Arm_L', 'M3 clearance', 3.4, [(91.0, 97.3)] * 2, enc_d),
        ('R2A_Encoder_Arm_L', 'dowel slip hole', 4.30, [(91.0, 97.3)], enc_dw),
        ('R2A_Knee_Pin_Cap_L', 'pin pocket', 15.0, [(L.PIN_Y[0] - L.PIN_CAP_GAP, 59.5)], K),
        ('R2A_Knee_Pin_Cap_L', 'M3 clearance', 3.4, [(56.6, 59.5)] * 2, L.pin_cap_insert_xz()),
        ('R2A_Knee_Pin_Cap_L', 'M3 head counterbores', 6.0, [(53.6, 56.6)] * 2, L.pin_cap_insert_xz()),
    ]


def dimensional_contracts():
    results = []
    for part, label, d, spans, centres in contract_table():
        rows = [r for r in cylinders(part) if abs(r['d'] - d) < 0.001
                and abs(abs(r['axis'][1]) - 1) < 1e-6
                and (centres is None or any(math.hypot(r['x'] - x, r['z'] - z) < 0.01
                                            for x, z in centres))]
        got = sorted((round(r['y0'], 2), round(r['y1'], 2)) for r in rows)
        want = sorted((round(a, 2), round(b, 2)) for a, b in spans)
        results.append({'part': part, 'interface': label, 'diameter_mm': d,
                        'expected_y_spans_mm': want, 'measured_y_spans_mm': got,
                        'pass': got == want})
    return results


def shape_signature(name):
    return A.shape_signature(name)


def _side(name):
    for row in PARTS:
        if row[0] == name:
            return row[2]
    raise KeyError(name)


def bed_body(name, side=None, source=None):
    """Transient copy at the recorded bed pose (same map as rig_export)."""
    side = side or _side(name)
    tm = adsk.fusion.TemporaryBRepManager.get()
    body = tm.copy(source if source is not None else _occ(name).component.bRepBodies.item(0))
    m = adsk.core.Matrix3D.create()
    m.setToRotation((-1 if side == 'max' else 1) * math.pi / 2,
                    adsk.core.Vector3D.create(1, 0, 0), adsk.core.Point3D.create(0, 0, 0))
    assert tm.transform(body, m)
    shift = adsk.core.Matrix3D.create()
    shift.translation = adsk.core.Vector3D.create(0, 0, -body.boundingBox.minPoint.z)
    assert tm.transform(body, shift)
    return body


def print_audit(name, bridge_max_mm=12.0, lip_max_mm=1.2):
    """Classify every downward-facing face of the bed-pose body.

    bed        : planar, normal -Z, at Z = 0 (the supporting plane)
    lip        : planar ring/overhang no wider than lip_max_mm from its wall
    bridge     : planar ceiling whose smaller in-plane extent <= bridge_max_mm
    SUPPORT    : anything else (needs a slicer support region)
    Non-planar downward faces are reported as SUPPORT.
    """
    body = bed_body(name)
    rows = []
    for f in body.faces:
        ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
        if not ok or n.z > -1e-6:
            continue
        bb = f.boundingBox
        z = f.pointOnFace.z * 10
        dx = (bb.maxPoint.x - bb.minPoint.x) * 10
        dy = (bb.maxPoint.y - bb.minPoint.y) * 10
        planar = adsk.core.Plane.cast(f.geometry) is not None
        area = f.area * 100
        if planar and n.z < -0.999999 and abs(z) < 1e-4:
            cls = 'bed'
        elif planar and n.z < -0.999999:
            # ring/overhang width: area over perimeter of its outer loop
            per = sum(e.length for e in f.loops.item(0).edges) * 10 if f.loops.count else 1.0
            width = area / max(per, 1e-9)
            inner = f.loops.count > 1
            if inner and width <= lip_max_mm:
                cls = 'lip'
            elif min(dx, dy) <= bridge_max_mm:
                cls = 'bridge'
            else:
                cls = 'SUPPORT'
        else:
            cls = 'SUPPORT'
        rows.append({'z_mm': round(z, 3), 'area_mm2': round(area, 2),
                     'extent_mm': [round(dx, 2), round(dy, 2)], 'class': cls,
                     'centre_mm': [round(v * 10, 2) for v in f.pointOnFace.asArray()]})
    counts = {}
    for r in rows:
        counts[r['class']] = counts.get(r['class'], 0) + 1
    bed_area = sum(r['area_mm2'] for r in rows if r['class'] == 'bed')
    return {'part': name, 'side': _side(name), 'bed_contact_mm2': round(bed_area, 2),
            'counts': counts, 'faces': [r for r in rows if r['class'] != 'bed'],
            'height_mm': round(body.boundingBox.maxPoint.z * 10, 3)}


# ================================================================ coupons
# Coupons are cut from the reviewed part B-Reps at export time, so each one
# reproduces the released geometry and print orientation exactly.
COUPONS = [
    # name, source part, bed side, keep-region builder key, qty, purpose
    ('R2A_COUPON_Crank_Register', 'R2A_Crank_L', 'max', 'register', 1,
     'crank-to-output register: 3 factory pins in Ø4.15, 6 x M3 x 10, flat seat'),
    ('R2A_COUPON_Crank_Clevis', 'R2A_Crank_L', 'max', 'clevis', 1,
     'rod-end ball in the 8.4 gap, swivel through the neck relief, Ø5.15 pin, '
     'Ø4.25 cap-dowel press; use with one extra R2A_Crank_Cap_L'),
    ('R2A_COUPON_Pin_Dowel_Ladder', None, 'min', 'ladder', 1,
     'Ø5.05-5.25 clevis-pin passages (3.7 mm plate) and Ø4.20-4.30 dowel press '
     'holes (3.0 mm) and blind top-opening sockets (7.0 mm deep)'),
]
LADDER_PIN = (5.05, 5.10, 5.15, 5.20, 5.25)
LADDER_DOWEL = (4.20, 4.25, 4.30)


def _tm():
    return adsk.fusion.TemporaryBRepManager.get()


def _box(x0, x1, y0, y1, z0, z1):
    c = adsk.core.Point3D.create((x0 + x1) / 20, (y0 + y1) / 20, (z0 + z1) / 20)
    obb = adsk.core.OrientedBoundingBox3D.create(
        c, adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0),
        (x1 - x0) / 10, (y1 - y0) / 10, (z1 - z0) / 10)
    return _tm().createBox(obb)


def _zcyl(x, y, z0, z1, d):
    return _tm().createCylinderOrCone(adsk.core.Point3D.create(x / 10, y / 10, z0 / 10), d / 20,
                                      adsk.core.Point3D.create(x / 10, y / 10, z1 / 10), d / 20)


def _boolean(a, b, kind):
    t = {'cut': adsk.fusion.BooleanTypes.DifferenceBooleanType,
         'join': adsk.fusion.BooleanTypes.UnionBooleanType,
         'inter': adsk.fusion.BooleanTypes.IntersectionBooleanType}[kind]
    assert _tm().booleanOperation(a, b, t)
    return a


def coupon_source(key):
    """Model-space B-Rep of a coupon (before the bed transform)."""
    tm = _tm()
    if key == 'register':
        body = tm.copy(_occ('R2A_Crank_L').component.bRepBodies.item(0))
        keep = L._cyl((0, L.CRANK_SLAB[0], 0), (0, L.CRANK_SLAB[1] + 1, 0), 39.0)
        return _boolean(body, keep, 'inter')
    if key == 'clevis':
        body = tm.copy(_occ('R2A_Crank_L').component.bRepBodies.item(0))
        x, z = L.C0
        keep = L._cyl((x, L.GAP[0] - 1, z), (x, L.CRANK_SLAB[1] + 1, z), 2 * 19.0)
        return _boolean(body, keep, 'inter')
    if key == 'ladder':
        # built flat in its own frame, bed face at z = 0 (then mapped to Y)
        plate = _box(0, 64, 0, 14, 0, 3.7)
        for i, d in enumerate(LADDER_PIN):
            _boolean(plate, _zcyl(8 + 12 * i, 7, -1, 5, d), 'cut')
        press = _box(0, 40, 14, 30, 0, 3.0)
        for i, d in enumerate(LADDER_DOWEL):
            _boolean(press, _zcyl(8 + 12 * i, 23, -1, 5, d), 'cut')
        block = _box(0, 40, 30, 44, 0, 8.4)
        for i, d in enumerate(LADDER_DOWEL):
            _boolean(block, _zcyl(8 + 12 * i, 38, 8.4 - 7.0, 9.4, d), 'cut')
        _boolean(plate, press, 'join')
        _boolean(plate, block, 'join')
        _boolean(plate, _box(0, 2.0, 0, 30, -1, 2.0), 'cut')       # marker at Ø5.05 / Ø4.20 end
        # map the flat frame so the bed face is the model's min-Y face
        m = adsk.core.Matrix3D.create()
        m.setToRotation(-math.pi / 2, adsk.core.Vector3D.create(1, 0, 0),
                        adsk.core.Point3D.create(0, 0, 0))
        assert tm.transform(plate, m)
        return plate
    raise KeyError(key)


def coupon_bed_body(name):
    row = [c for c in COUPONS if c[0] == name][0]
    return bed_body(None, side=row[2], source=coupon_source(row[3]))


# ================================================================= export
def part_bed_body(name):
    if name in [c[0] for c in COUPONS]:
        return coupon_bed_body(name)
    if name == 'R2A_Knee_Bumper_TPU':
        return tpu_plug_body(TPU_PLUG_LEN)
    return bed_body(name)


def _mesh_triangles(path):
    return A._mesh_triangles(path)


def mesh_fidelity(name, path, chord_gate_mm=S.CHORD_GATE_MM):
    """A.mesh_fidelity() logic against the R2A bed body (see that docstring)."""
    body = part_bed_body(name)
    raw = _mesh_triangles(path)
    index = {}; tris = []
    for t in raw:
        tris.append(tuple(index.setdefault(v, len(index)) for v in t))
    verts = [None] * len(index)
    for v, i in index.items():
        verts[i] = v
    failures = []; metrics = {'triangles': len(tris), 'vertices': len(verts)}
    edges = {}; degenerate = 0
    for t in tris:
        if len(set(t)) < 3:
            degenerate += 1
        for p, q in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            k = (min(p, q), max(p, q)); edges[k] = edges.get(k, 0) + 1
    parent = list(range(len(verts)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for t in tris:
        for p, q in ((t[0], t[1]), (t[1], t[2])):
            rp, rq = find(p), find(q)
            if rp != rq:
                parent[rp] = rq
    metrics.update(open_or_nonmanifold_edges=sum(1 for c in edges.values() if c != 2),
                   degenerate_triangles=degenerate,
                   shells=len({find(i) for i in range(len(verts))}), lumps=body.lumps.count)
    if metrics['open_or_nonmanifold_edges'] or degenerate:
        failures.append('mesh is not a closed manifold')
    if metrics['shells'] != metrics['lumps']:
        failures.append('shell count differs from B-Rep lumps')
    on = adsk.fusion.PointContainment.PointOnPointContainment
    off = [v for v in verts if body.pointContainment(adsk.core.Point3D.create(v[0] / 10, v[1] / 10, v[2] / 10)) != on]
    metrics['vertices_off_reviewed_surface'] = len(off)
    if off:
        failures.append('%d vertices are not on the reviewed B-Rep' % len(off))
    chord = A._cylinder_chord_mm(body, verts, tris)
    metrics['max_cylinder_chord_mm'] = round(chord, 5)
    if chord_gate_mm is not None and chord > chord_gate_mm:
        failures.append('chord %.4f mm exceeds %.4f mm' % (chord, chord_gate_mm))
    allowance = max(chord, chord_gate_mm or 0.0) + 0.001
    volume = area = bed = 0.0
    for p, q, r in raw:
        u = [q[i] - p[i] for i in range(3)]; w = [r[i] - p[i] for i in range(3)]
        c = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
        area += math.sqrt(sum(x * x for x in c)) / 2
        volume += (p[0] * (q[1] * r[2] - q[2] * r[1]) - p[1] * (q[0] * r[2] - q[2] * r[0])
                   + p[2] * (q[0] * r[1] - q[1] * r[0])) / 6
        if max(abs(p[2]), abs(q[2]), abs(r[2])) < 1e-4 and c[2] < 0:
            bed += -c[2] / 2
    curved = bed_brep = 0.0
    for f in body.faces:
        if not adsk.core.Plane.cast(f.geometry):
            curved += f.area * 100; continue
        ok, normal = f.evaluator.getNormalAtPoint(f.pointOnFace)
        if ok and normal.z < -0.999999 and abs(f.pointOnFace.z) < 1e-6:
            bed_brep += f.area * 100
    metrics.update(mesh_volume_mm3=round(volume, 3), brep_volume_mm3=round(body.volume * 1000, 3),
                   mesh_area_mm2=round(area, 3), brep_area_mm2=round(body.area * 100, 3),
                   bed_contact_mesh_mm2=round(bed, 3), bed_contact_brep_mm2=round(bed_brep, 3))
    if abs(volume - body.volume * 1000) > allowance * curved + 0.05:
        failures.append('volume differs beyond tessellation')
    if abs(area - body.area * 100) > 0.002 * body.area * 100 + 0.05:
        failures.append('surface area differs beyond tessellation')
    if bed_brep <= 0 or abs(bed - bed_brep) > 0.01 * bed_brep + 0.05:
        failures.append('bed contact face differs')
    zmin = min(v[2] for v in verts); metrics['mesh_min_z_mm'] = zmin
    if abs(zmin) > 1e-4:
        failures.append('mesh does not sit on the bed at z=0')
    bb = body.boundingBox
    box = [max(abs(min(v[k] for v in verts) - bb.minPoint.asArray()[k] * 10),
               abs(max(v[k] for v in verts) - bb.maxPoint.asArray()[k] * 10)) for k in range(3)]
    metrics['box_deviation_mm'] = [round(x, 4) for x in box]
    if max(box) > allowance:
        failures.append('bed-pose bounding box differs')
    grid = A._triangle_grid(raw, allowance)
    samples = [('face', f.pointOnFace) for f in body.faces]
    samples += [('edge', e.pointOnEdge) for e in body.edges]
    samples += [('vertex', v.geometry) for v in body.vertices]
    missing = 0
    for kind, pt in samples:
        p = (pt.x * 10, pt.y * 10, pt.z * 10)
        cand = grid.get(tuple(math.floor(c / 5.0) for c in p), [])
        d2 = min((A._distance2(p, *raw[i]) for i in cand), default=float('inf'))
        if d2 > allowance * allowance:
            missing += 1
    metrics['brep_samples'] = len(samples); metrics['brep_samples_not_in_mesh'] = missing
    if missing:
        failures.append('%d B-Rep samples are missing from the mesh' % missing)
    return {'part': name, 'file': os.path.relpath(path, ROOT) if path.startswith(ROOT) else path,
            'pass': not failures, 'failures': failures, 'metrics': metrics}


def body_signature(body):
    faces = []
    for f in body.faces:
        bb = f.boundingBox
        row = [f.geometry.objectType, round(f.area * 100, 4),
               [round(v * 10, 4) for v in f.centroid.asArray()],
               [round(v * 10, 4) for v in bb.minPoint.asArray() + bb.maxPoint.asArray()]]
        g = adsk.core.Cylinder.cast(f.geometry)
        if g:
            row += [round(g.radius * 20, 4), [round(v, 6) for v in g.axis.asArray()]]
        faces.append(row)
    return [{'volume_mm3': round(body.volume * 1000, 4),
             'faces': sorted(faces, key=lambda r: json.dumps(r)),
             'solid': body.isSolid, 'lumps': body.lumps.count}]


def release_rows():
    rows = [(p[0], p[1], p[3], p[4], p[5], p[6]) for p in PARTS]
    rows += [(c[0], c[0] + '_ABS', c[4], 'ABS', 'none', 'RELEASED') for c in COUPONS]
    rows.append(('R2A_Knee_Bumper_TPU', 'R2A_Knee_Bumper_TPU95A_D6x4', 4, 'TPU 95A', 'none',
                 'RELEASED'))
    return rows


def tpu_plug_body(length):
    """One Ø6 bumper plug standing on its end (flat frame, bed at z = 0)."""
    return _zcyl(0.0, 0.0, 0.0, length, L.TPU_D)


def _shape(name):
    if name in [c[0] for c in COUPONS]:
        return body_signature(coupon_bed_body(name))
    if name == 'R2A_Knee_Bumper_TPU':
        return body_signature(tpu_plug_body(TPU_PLUG_LEN))
    return shape_signature(name)


TPU_PLUG_LEN = 4.0     # one length for all four plugs (bores 4.0 inboard, 5.6 outboard)


def export_part(name, out_dir):
    """Write <stem>.stl from the bed-pose B-Rep; returns path.  Run guarded."""
    stem = [r[1] for r in release_rows() if r[0] == name][0]
    path = os.path.join(out_dir, stem + '.stl')
    if name == 'R2A_Knee_Bumper_TPU':
        body = tpu_plug_body(TPU_PLUG_LEN)
    else:
        body = part_bed_body(name)
    A._export_body(body, path)
    return path


def load_baseline():
    if os.path.exists(BASELINE):
        return json.load(open(BASELINE))
    return {'document': L.DOC, 'parts': {}, 'verified_source_sha256': {}, 'review_log': []}


def _write_baseline(baseline, action, names, reason):
    if not reason or len(reason.strip()) < 12:
        raise ValueError('A deliberate baseline change needs a written review reason')
    baseline.setdefault('review_log', []).append(
        {'date': time.strftime('%Y-%m-%d'), 'action': action, 'parts': names,
         'reason': reason.strip()})
    with open(BASELINE, 'w') as s:
        json.dump(baseline, s, indent=1)


def accept_shapes(names, reason):
    """Review step: every contract of each named part must pass first."""
    _assert_doc()
    contracts = dimensional_contracts()
    baseline = load_baseline()
    rows = {r[0]: r for r in release_rows()}
    for name in names:
        bad = [c for c in contracts if c['part'] == name and not c['pass']]
        if bad:
            raise RuntimeError('Contracts fail: ' + json.dumps(bad))
        entry = baseline['parts'].setdefault(name, {})
        r = rows[name]
        entry.update({'file': 'r2a_stl/%s.stl' % r[1], 'qty': r[2], 'material': r[3],
                      'support_policy': r[4], 'state': r[5], 'shape': _shape(name)})
    _write_baseline(baseline, 'accept_shapes', names, reason)
    return len(names)


def assert_shape(name):
    baseline = load_baseline()
    row = baseline['parts'].get(name)
    if row is None or row.get('shape') != _shape(name):
        raise RuntimeError('Unreviewed R2A geometry blocks export: ' + name)
    bad = [c for c in dimensional_contracts() if c['part'] == name and not c['pass']]
    if bad:
        raise RuntimeError('R2A contract failed: ' + json.dumps(bad))


def release(out_dir=None, names=None):
    """Export every released row after the reviewed-shape gate; dry run if a
    directory is given.  Never updates the baseline."""
    _assert_doc()
    target = out_dir or OUT_DIR
    os.makedirs(target, exist_ok=True)
    report = {}
    for r in release_rows():
        name = r[0]
        if names and name not in names:
            continue
        if not r[5].startswith('RELEASED'):
            report[name] = {'state': r[5]}
            continue
        assert_shape(name)
        staged = os.path.join(target, r[1] + '.pending.stl')
        final = os.path.join(target, r[1] + '.stl')
        L.guarded(_export_to, name, staged)
        fid = mesh_fidelity(name, staged)
        if not fid['pass']:
            os.remove(staged)
            raise RuntimeError('mesh fidelity failed: %s %s' % (name, fid['failures']))
        keep = False
        base = load_baseline()['parts'].get(name, {})
        if os.path.exists(final) and base.get('released_sha256') == _sha(final):
            keep = mesh_fidelity(name, final, chord_gate_mm=None)['pass']
        if keep:
            os.remove(staged)
            report[name] = {'file': final, 'release_file': 'retained'}
        else:
            os.replace(staged, final)
            report[name] = {'file': final, 'release_file': 'written', 'fidelity': fid['metrics']}
    return report


def _export_to(name, path):
    body = tpu_plug_body(TPU_PLUG_LEN) if name == 'R2A_Knee_Bumper_TPU' else part_bed_body(name)
    A._export_body(body, path)


def _sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def accept_released_files(names, reason):
    """Review step: pin release files that pass mesh_fidelity()."""
    _assert_doc()
    baseline = load_baseline()
    for name in names:
        assert_shape(name)
        row = baseline['parts'][name]
        path = os.path.join(ROOT, row['file'])
        fid = mesh_fidelity(name, path)
        if not fid['pass']:
            raise RuntimeError('fidelity: ' + json.dumps(fid))
        sig = A.mesh_signature(path)
        row['released_sha256'] = sig['sha256']
        row['fresh_fusion_export'] = {k: sig[k] for k in ('sha256', 'triangles', 'geometry_sha256')}
        row['fidelity'] = fid['metrics']
    _write_baseline(baseline, 'accept_released_files', names, reason)
    return len(names)


def accept_verified_sources(reason):
    _assert_doc()
    baseline = load_baseline()
    baseline['verified_source_sha256'] = {s: _sha(os.path.join(ROOT, s)) for s in VERIFIED_SOURCES}
    _write_baseline(baseline, 'accept_verified_sources', VERIFIED_SOURCES, reason)
    return baseline['verified_source_sha256']


# ================================================= distal selective supports
# (face Y, min area, max area, support depth to the next surface below, label)
DISTAL_SUPPORTS = [
    (65.8, 1000.0, 1500.0, 6.3, 'knee_web'),
    (65.8, 250.0, 400.0, 6.3, 'knee_web'),       # lever ear and arm
    (65.3, 100.0, 140.0, 5.8, 'knee_receiver_land'),
    (84.5, 1100.0, 1300.0, 19.4, 'open_channel'),
    (64.5, 550.0, 650.0, 5.0, 'wheel_end'),
]
# (0, -1, 0) = straight off the part toward the (removed) bed; the lateral
# directions cover the open -dv side of the U-channel.
REMOVAL_DIRS = [(0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1),
                (0.7071, 0, 0.7071), (0.7071, 0, -0.7071),
                (-0.7071, 0, 0.7071), (-0.7071, 0, -0.7071),
                (-0.643, 0, 0.766)]
LATERAL = [(math.cos(math.radians(a)), 0.0, math.sin(math.radians(a))) for a in range(0, 360, 15)]


def distal_support_audit():
    """Selective-support envelopes and straight removal paths (legacy method:
    distal_first_article_fusion._support_envelope, 0.4 mm top/bottom and 0.6 mm
    lateral gaps, Ø11 knee-bore keep-out).  Run inside L.guarded()."""
    import distal_first_article_fusion as D
    occ = _occ('R2A_Distal_Link_L')
    rows = []
    for y, amin, amax, depth, label in DISTAL_SUPPORTS:
        dirs = LATERAL if label == 'open_channel' else REMOVAL_DIRS
        try:
            r = D._support_envelope(occ, label, y, amin, amax, depth, dirs)
            r['face_y_mm'] = y
        except RuntimeError as e:
            r = {'label': label, 'face_y_mm': y, 'error': str(e)}
        rows.append(r)
    return rows
