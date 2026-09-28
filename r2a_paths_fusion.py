"""R2A assembly-path, tool-access and service-path checks.  Fusion MCP only.

Every step of the R2A assembly sequence is checked as a straight-line path in
Fusion (ASSEMBLY_VERIFICATION.md): the moving parts are copied as temporary
B-Reps at the build pose and translated from their installed position out to
`travel` mm in `step` increments; at every station the overlap with each part
already present at that step must be zero.  Hex-key access is checked the same
way with a key envelope on the screw axis.  Removal is the reverse of each
path, so the same result is the service path.

Results carry the status CAD PATH VERIFIED only.  Physical rehearsal on the
first article is still required.
"""
import json
import math
import os

import adsk.core
import adsk.fusion

import beni_lib as B
import r2a_lib as L

OUT = os.path.join(L.GATE_DIR, 'assembly_paths.json')


def _tm():
    return adsk.fusion.TemporaryBRepManager.get()


def _world(occ):
    """Temporary copies of an occurrence's bodies in world coordinates."""
    out = []
    stack = [occ]
    while stack:
        o = stack.pop()
        for b in o.component.bRepBodies:
            t = _tm().copy(b)
            assert _tm().transform(t, o.transform2)
            out.append(t)
        for i in range(o.childOccurrences.count):
            stack.append(o.childOccurrences.item(i))
    return out


def _occs(names):
    out = []
    for n in names:
        if hasattr(n, 'component'):
            out.append(n)
            continue
        found = [o for o in L.all_root_occs()
                 if B.base_name(o.component.name) == n
                 or (o.attributes.itemByName('R2A', 'set') and
                     o.attributes.itemByName('R2A', 'set').value == n)]
        if not found:
            raise RuntimeError('path check: no occurrence ' + str(n))
        out.extend(found)
    return out


def _overlap(a, b):
    ba, bb = a.boundingBox, b.boundingBox
    for ax in ('x', 'y', 'z'):
        if getattr(ba.maxPoint, ax) <= getattr(bb.minPoint, ax) + 1e-8 or \
           getattr(bb.maxPoint, ax) <= getattr(ba.minPoint, ax) + 1e-8:
            return 0.0
    r = _tm().copy(a)
    try:
        assert _tm().booleanOperation(r, b, adsk.fusion.BooleanTypes.IntersectionBooleanType)
    except Exception:
        return -1.0
    return r.volume * 1000.0


def _shift(body, v):
    r = _tm().copy(body)
    m = adsk.core.Matrix3D.create()
    m.translation = adsk.core.Vector3D.create(v[0] / 10.0, v[1] / 10.0, v[2] / 10.0)
    assert _tm().transform(r, m)
    return r


def linear_path(moving, fixed, vector, travel, step=1.0, eps=0.001):
    """Max overlap (mm3) along the straight path; stations from travel to 0."""
    mv = [b for o in _occs(moving) for b in _world(o)]
    fx = [b for o in _occs(fixed) for b in _world(o)]
    n = int(round(travel / step))
    worst, at = 0.0, None
    for k in range(n + 1):
        # offset slightly along the path itself (out of the seated contact):
        # exactly coincident faces make the temporary Boolean indeterminate
        off = travel - k * step + eps
        v = (vector[0] * off, vector[1] * off, vector[2] * off)
        for a in mv:
            t = _shift(a, v)
            for b in fx:
                ov = _overlap(t, b)
                if ov < 0:     # kernel-indeterminate coincident slice: retry
                    ov = max(_overlap(_shift(t, (0, e, 0)), b) for e in (-0.01, 0.01))
                if ov > worst:
                    worst, at = ov, off
    return {'moving': [getattr(m, 'name', m) for m in moving], 'vector': list(vector), 'travel_mm': travel,
            'step_mm': step, 'max_overlap_mm3': round(worst, 4), 'at_offset_mm': at,
            'clear': worst <= 0.001}


def _screw_axes(label):
    """(head-top point, axis pointing out of the head) for a screw set, or for
    a list of screw occurrences."""
    rows = []
    for o in _occs(label if isinstance(label, list) else [label]):
        m = o.transform2.asArray()
        # screw_comp: head underside at the local origin, head toward local +Y
        yax = (m[1], m[5], m[9])
        org = (m[3] * 10.0, m[7] * 10.0, m[11] * 10.0)
        rows.append((org, yax))
    return rows


# hex-key envelope Ø (2.0 / 2.5 / 3 mm keys + margin; DESIGN CHOICE, same
# ratio for M2.5 as for M3 and M4)
KEY_D = {2.5: 3.2, 3.0: 3.9, 4.0: 4.6}
HEAD_H = {2.5: 2.5, 3.0: 3.0, 4.0: 4.0}


def tool_access(label, d, fixed, length=100.0):
    """Hex-key envelope from each head's socket outward along the screw axis."""
    fx = [b for o in _occs(fixed) for b in _world(o)]
    rows = []
    for org, ax in _screw_axes(label):
        top = tuple(org[i] + ax[i] * HEAD_H[d] for i in range(3))
        start = tuple(top[i] - ax[i] * 1.5 for i in range(3))      # 1.5 mm into the socket
        end = tuple(top[i] + ax[i] * length for i in range(3))
        key = _tm().createCylinderOrCone(
            adsk.core.Point3D.create(*(c / 10.0 for c in start)), KEY_D[d] / 20.0,
            adsk.core.Point3D.create(*(c / 10.0 for c in end)), KEY_D[d] / 20.0)
        worst = 0.0
        for b in fx:
            ov = _overlap(key, b)
            worst = max(worst, ov)
        rows.append(round(worst, 4))
    name = label if isinstance(label, str) else '+'.join(o.name for o in label)
    return {'screws': name, 'key_envelope_d_mm': KEY_D[d], 'length_mm': length,
            'max_overlap_mm3_each': rows, 'clear': all(r <= 0.001 for r in rows)}


# ------------------------------------------------------------- the sequence
MODULE = [L.PART['OUTB'], 'HW_Bearing_6800', L.PART['TPU'] + '_Out', 'R2A_SHCS_M3x10_Actuator',
          L.PART['CRANK'], L.PART['CRANK_CAP'], 'HW_DowelPin_D4x10_Crank', 'R2A_SHCS_M3x10_Crank',
          'HW_Pin_D5x18_Crank', 'HW_RodEnd_M5_Upper', 'HW_RodEnd_M5_Lower', 'HW_Rod_M5x86',
          'HW_JamNut_M5', L.PART['DIST'], L.PART['LEVER_CAP'], 'HW_DowelPin_D4x10_Lever',
          'HW_Pin_D5x18_Lever', 'HW_DowelPin_D4x10_EncArm']
ROD = ['HW_RodEnd_M5_Upper', 'HW_RodEnd_M5_Lower', 'HW_Rod_M5x86', 'HW_JamNut_M5']
SHOULDER_STATIC = ['Shoulder_Output_Hub_L', 'HW_DowelPin_D4x10_Root', 'Shoulder_Cable_Cover_L',
                   'Chassis_Shoulder_Plate_L', 'RIG_Stand', 'RIG_Cable_Post_A']


def _bearing(which):
    occ = [o for o in L.all_root_occs() if B.base_name(o.component.name) == 'HW_Bearing_6800']
    occ.sort(key=lambda o: B.bbox_of(o)[2])
    return occ[0] if which == 'A' else occ[1]


def steps():
    kn = L.knee_ref()
    bA, bB = _bearing('A'), _bearing('B')
    module = [kn] + [m for m in MODULE if m != 'HW_Bearing_6800'] + [bB]
    return [
        # id, description, kind, args
        ('B1', 'knee actuator onto the outboard half (from +Y)', 'path',
         dict(moving=[kn], fixed=[L.PART['OUTB'], bB], vector=(0, 1, 0), travel=40)),
        ('B2', 'actuator 5 x M3 x 12 from the channel side', 'path',
         dict(moving=['R2A_SHCS_M3x10_Actuator'], fixed=[L.PART['OUTB'], bB], vector=(0, -1, 0), travel=25)),
        ('B2k', 'hex key to the actuator screws', 'tool',
         dict(label='R2A_SHCS_M3x10_Actuator', d=3.0, fixed=[L.PART['OUTB'], bB, kn])),
        ('B3', 'crank onto the actuator output (from -Y)', 'path',
         dict(moving=[L.PART['CRANK']], fixed=[kn, L.PART['OUTB'], 'R2A_SHCS_M3x10_Actuator'],
              vector=(0, -1, 0), travel=40)),
        ('B4', 'crank 6 x M3 x 10 into the output', 'path',
         dict(moving=['R2A_SHCS_M3x10_Crank'], fixed=[L.PART['CRANK'], L.PART['OUTB']],
              vector=(0, -1, 0), travel=25)),
        ('B4k', 'hex key to the crank screws (crank at build angle)', 'tool',
         dict(label='R2A_SHCS_M3x10_Crank', d=3.0,
              fixed=[L.PART['CRANK'], L.PART['OUTB'], kn, 'R2A_SHCS_M3x10_Actuator'])),
        ('B5', 'pushrod: upper rod end onto the crank ear (cap off)', 'path',
         dict(moving=ROD, fixed=[L.PART['CRANK'], L.PART['OUTB'], kn], vector=(0, -1, 0), travel=20)),
        ('B6', 'crank cap on its two dowels', 'path',
         dict(moving=[L.PART['CRANK_CAP']], fixed=[L.PART['CRANK'], 'HW_DowelPin_D4x10_Crank'] + ROD,
              vector=(0, -1, 0), travel=20)),
        ('B6p', 'crank pin from the inboard side', 'path',
         dict(moving=['HW_Pin_D5x18_Crank'], fixed=[L.PART['CRANK'], L.PART['CRANK_CAP']] + ROD,
              vector=(0, -1, 0), travel=30)),
        ('B7', 'lower rod end into the lever clevis (cap off)', 'path',
         dict(moving=ROD, fixed=[L.PART['DIST']], vector=(0, 1, 0), travel=20)),
        ('B8', 'lever cap on its two dowels', 'path',
         dict(moving=[L.PART['LEVER_CAP']], fixed=[L.PART['DIST'], 'HW_DowelPin_D4x10_Lever'] + ROD,
              vector=(0, 1, 0), travel=20)),
        ('B8p', 'lever pin from the outboard side', 'path',
         dict(moving=['HW_Pin_D5x18_Lever'], fixed=[L.PART['DIST'], L.PART['LEVER_CAP']] + ROD,
              vector=(0, 1, 0), travel=30)),
        ('S1', 'inboard half onto the shoulder hub (from +Y)', 'path',
         dict(moving=[L.PART['INB'], bA, L.PART['TPU'] + '_In'], fixed=SHOULDER_STATIC,
              vector=(0, 1, 0), travel=40)),
        ('S2', 'hub 6 x M4 x 10 from the channel side', 'path',
         dict(moving=['HW_SHCS_M4x10'], fixed=[L.PART['INB'], 'Shoulder_Output_Hub_L', bA],
              vector=(0, 1, 0), travel=25)),
        ('S2k', 'hex key to the hub screws', 'tool',
         dict(label='HW_SHCS_M4x10', d=4.0, fixed=[L.PART['INB'], 'Shoulder_Output_Hub_L', bA,
                                                  'HW_DowelPin_D4x10_Root'])),
        ('S3', 'outboard module onto the inboard half (from +Y)', 'path',
         dict(moving=module, fixed=[L.PART['INB'], bA, L.PART['TPU'] + '_In', 'HW_SHCS_M4x10']
              + SHOULDER_STATIC, vector=(0, 1, 0), travel=60, step=2.0)),
        ('S4', 'perimeter 6 x M3 x 12 from outboard', 'path',
         dict(moving=['R2A_SHCS_M3x12_Perimeter'], fixed=[L.PART['OUTB'], L.PART['INB']],
              vector=(0, 1, 0), travel=25)),
        ('S4k', 'hex key to the perimeter screws', 'tool',
         dict(label='R2A_SHCS_M3x12_Perimeter', d=3.0,
              fixed=[L.PART['OUTB'], L.PART['INB'], kn, L.PART['DIST']])),
        ('S5', 'knee-pin cap on the inboard face', 'path',
         dict(moving=[L.PART['PIN_CAP']], fixed=[L.PART['INB'], bA], vector=(0, -1, 0), travel=25)),
        ('S5k', 'hex key to the pin-cap screws', 'tool',
         dict(label='R2A_SHCS_M3x6_PinCap', d=3.0,
              fixed=[L.PART['INB'], L.PART['PIN_CAP'], L.PART['DIST'], 'RIG_Stand'])),
        ('S6', 'Ø10 knee pin from outboard (also the service path)', 'path',
         dict(moving=['HW_DowelPin_D10x35'], fixed=[L.PART['INB'], L.PART['OUTB'], bA, bB,
                                                     L.PART['DIST'], L.PART['PIN_CAP']],
              vector=(0, 1, 0), travel=45)),
        ('S7', 'encoder arm onto the distal pads', 'path',
         dict(moving=[L.PART['ENC_ARM'], 'HW_Magnet_D6x2p5_Diametric'],
              fixed=[L.PART['DIST'], 'HW_DowelPin_D4x10_EncArm', L.PART['OUTB'], 'HW_DowelPin_D10x35'],
              vector=(0, 1, 0), travel=30)),
        ('S7k', 'hex key to the encoder-arm screws', 'tool',
         dict(label='R2A_SHCS_M3x10_EncArm', d=3.0,
              fixed=[L.PART['ENC_ARM'], L.PART['DIST'], L.PART['OUTB']])),
        ('S8', 'AS5048A board and bracket', 'path',
         dict(moving=[L.PART['ENC_BRACKET'], 'HW_AS5048A_PCB'],
              fixed=[L.PART['OUTB'], L.PART['ENC_ARM'], 'HW_Magnet_D6x2p5_Diametric', L.PART['DIST']],
              vector=(0, 1, 0), travel=30)),
        ('S8k', 'hex key to the bracket screws', 'tool',
         dict(label='R2A_SHCS_M3x16_Bracket', d=3.0,
              fixed=[L.PART['ENC_BRACKET'], L.PART['OUTB'], L.PART['ENC_ARM'], L.PART['DIST']])),
    ] + wheel_steps(module)


def _wheel():
    """Wheel-module occurrences: motor REF, hub, both rim variants and the
    wheel screws (M2.5 motor, M3 x 8 hub-to-output, M4 x 8 rim-to-hub)."""
    occ = {'motor': [], 'm25': [], 'm3': [], 'm4': []}
    for o in L.all_root_occs():
        n = B.base_name(o.component.name)
        if n == 'REF_GIM4305-10':
            occ['motor'].append(o)
        elif (o.attributes.itemByName('R2A', 'set') and
              o.attributes.itemByName('R2A', 'set').value == 'R2A_SHCS_M2p5x10_WheelMotor'):
            occ['m25'].append(o)
        elif n == 'HW_SHCS_M3x8' and (L.pose_class(o) or '') == 'DIST':
            occ['m3'].append(o)
        elif n == 'HW_SHCS_M4x8':
            occ['m4'].append(o)
    assert len(occ['motor']) == 1 and len(occ['m25']) == 6 and len(occ['m3']) == 3 \
        and len(occ['m4']) == 6, {k: len(v) for k, v in occ.items()}
    return occ


def wheel_steps(module):
    """Legacy order (ordered-pin traveller step 7): motor and hub on the
    detached distal link, the module goes on with them, the no-tyre shell last."""
    w = _wheel()
    mot = w['motor']
    shell = 'ABS_TEST_Wheel_Rim_NoTyre'
    grp = mot + w['m25'] + ['Wheel_Hub_L'] + w['m3']
    leg = [L.PART['INB'], L.PART['OUTB'], L.PART['DIST'], L.knee_ref()]
    return [
        ('W1', 'wheel motor onto the detached distal link (from +Y)', 'path',
         dict(moving=mot, fixed=[L.PART['DIST']], vector=(0, 1, 0), travel=40)),
        ('W1s', 'wheel-motor 6 x M2.5 x 10 from the inboard side', 'path',
         dict(moving=['R2A_SHCS_M2p5x10_WheelMotor'], fixed=[L.PART['DIST']], vector=(0, -1, 0),
              travel=20)),
        ('W1k', 'hex key to the wheel-motor screws (distal link detached)', 'tool',
         dict(label='R2A_SHCS_M2p5x10_WheelMotor', d=2.5, fixed=[L.PART['DIST']] + mot)),
        ('W2', 'wheel hub onto the wheel-motor output (from +Y)', 'path',
         dict(moving=['Wheel_Hub_L'], fixed=[L.PART['DIST']] + mot, vector=(0, 1, 0), travel=30)),
        ('W2k', 'hex key to the 3 x M3 x 8 hub screws', 'tool',
         dict(label=w['m3'], d=3.0, fixed=[L.PART['DIST'], 'Wheel_Hub_L'] + mot)),
        ('S3w', 'outboard module with the wheel motor and hub fitted (from +Y)', 'path',
         dict(moving=module + grp, fixed=[L.PART['INB'], _bearing('A'), L.PART['TPU'] + '_In',
                                           'HW_SHCS_M4x10'] + SHOULDER_STATIC,
              vector=(0, 1, 0), travel=60, step=2.0)),
        ('W3', 'no-tyre wheel shell onto the hub, last (from +Y)', 'path',
         dict(moving=[shell], fixed=leg + ['Wheel_Hub_L'] + mot + w['m3'], vector=(0, 1, 0), travel=40)),
        ('W3k', 'hex key to the 6 x M4 x 8 shell screws', 'tool',
         dict(label='HW_SHCS_M4x8', d=4.0, fixed=leg + [shell, 'Wheel_Hub_L'] + mot)),
    ]


def run_steps(ids=None, path=OUT):
    L.assert_r2a_doc()
    L.ref_assert()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = json.load(open(path)) if os.path.exists(path) else {}
    for sid, desc, kind, args in steps():
        if ids and sid not in ids:
            continue
        if sid in data:
            continue
        if kind == 'path':
            r = linear_path(**args)
        else:
            r = tool_access(**args)
        r['description'] = desc
        r['status'] = 'CAD PATH VERIFIED' if r['clear'] else 'BLOCKED'
        data[sid] = r
        with open(path, 'w') as s:
            json.dump(data, s, indent=1)
    return {k: v['clear'] for k, v in data.items()}


# ------------------------------------------------------ fastener engagement
# Receiving spans (y mouth, y floor of the thread or insert, y floor of the
# pocket or None) and the head side of each screw set.  Actuator threads are
# design record §2.1: housing mount "~4.0 mm thread from the front face" with a
# Ø6.0 through-bore behind it; output "6 x M3 on Ø25.0 PCD, 5 mm deep".  Inserts
# are the 5.0 mm M3 (beni_lib.INSERT_LEN) and the owned 8.0 mm M4 (Kadriick).
ENGAGEMENT = [
    # set, head side, receiving part, mouth y, thread/insert end y, pocket floor y
    ('R2A_SHCS_M3x10_Actuator', -1, 'knee GIM6010-8 housing front thread (~4.0; STEP Ø2.459 y 91.1..95.1)',
     L.ACT_MOUNT_Y, L.ACT_MOUNT_Y + 4.0, L.ACT_MOUNT_Y + 4.0),
    ('R2A_SHCS_M3x10_Crank', -1, 'knee GIM6010-8 output thread (5 mm deep)',
     L.ACT_OUT_Y, L.ACT_OUT_Y + 5.0, L.ACT_OUT_Y + 5.0),
    ('R2A_SHCS_M3x12_Perimeter', +1, 'M3 x 5 insert, inboard-half wall top',
     L.Y_CH1, L.Y_CH1 - B.INSERT_LEN, L.Y_CH1 - 6.0),
    ('R2A_SHCS_M3x16_Bracket', +1, 'M3 x 5 insert, outboard-half outer face',
     L.Y_OUT, L.Y_OUT - B.INSERT_LEN, L.Y_OUT - B.ENC_INSERT_DEPTH),
    ('R2A_SHCS_M3x10_EncArm', +1, 'M3 x 5 insert, distal outboard pads',
     L.ENC_PAD_Y1, L.ENC_PAD_Y1 - B.INSERT_LEN, 85.5),
    ('R2A_SHCS_M3x6_PinCap', -1, 'M3 x 5 insert, inboard-half inboard face',
     L.Y_IN, L.Y_IN + B.INSERT_LEN, L.Y_IN + B.INSERT_LEN),
    ('HW_SHCS_M4x10', +1, 'owned M4 x 8 insert, shoulder hub link face',
     L.Y_IN, L.Y_IN - B.OWNED_M4_INSERT_LEN, None),
    ('R2A_SHCS_M2p5x10_WheelMotor', -1, 'GIM4305-10 housing thread (STEP Ø2.0 x 3.0 blind, y 67.5..70.5)',
     67.5, 70.5, 70.5),
]


def _y_faces(occ):
    """Exact Y extent from the planar end faces (occurrence boxes carry a
    0.01 mm tolerance pad)."""
    ys = []
    for b in occ.component.bRepBodies:
        pb = b.createForAssemblyContext(occ)
        for f in pb.faces:
            pl = adsk.core.Plane.cast(f.geometry)
            if pl and abs(abs(pl.normal.y) - 1.0) < 1e-9:
                ys.append(f.pointOnFace.y * 10)
    return round(min(ys), 3), round(max(ys), 3)


def fastener_engagement(path=None):
    """Thread engagement and tip-to-floor clearance for every R2A screw set,
    from the planar end faces of the modelled screw occurrences.  Head height =
    d (ISO 4762)."""
    L.assert_r2a_doc()
    rows = []
    for name, side, recv, mouth, end, floor in ENGAGEMENT:
        occs = _occs([name])
        spans = sorted({_y_faces(o) for o in occs})
        if len(spans) != 1:
            raise RuntimeError('%s: screws disagree in Y: %s' % (name, spans))
        y0, y1 = spans[0]
        d = 4.0 if 'M4' in name else (2.5 if 'M2p5' in name else 3.0)
        if side > 0:           # head outboard, shank points -Y
            seat, tip = y1 - d, y0
        else:
            seat, tip = y0 + d, y1
        lo, hi = sorted((mouth, end))
        eng = max(0.0, min(max(seat, tip), hi) - max(min(seat, tip), lo))
        row = {'set': name, 'count': len(occs), 'screw_y_mm': [y0, y1],
               'head_bearing_y_mm': round(seat, 3), 'tip_y_mm': round(tip, 3),
               'grip_mm': round(abs(mouth - seat), 3), 'receiving': recv,
               'engagement_mm': round(eng, 3)}
        if floor is not None:
            row['tip_to_floor_mm'] = round((tip - floor) * (1 if side > 0 else -1), 3)
        rows.append(row)
    if path:
        with open(path, 'w') as s:
            json.dump(rows, s, indent=1)
    return rows


NEG_OUT = os.path.join(L.GATE_DIR, 'assembly_path_negative_controls.json')


def negative_controls(path=NEG_OUT):
    """Deliberately wrong moves that must report BLOCKED; proves the checks see
    the parts they claim to."""
    kn = L.knee_ref()
    out = {
        'crank_into_actuator': linear_path([L.PART['CRANK']], [kn], (0, 1, 0), 10),
        'pin_into_cap': linear_path(['HW_DowelPin_D10x35'], [L.PART['PIN_CAP']], (0, -1, 0), 10),
        'module_minus_y': linear_path([L.PART['OUTB']], [L.PART['INB']], (0, -1, 0), 5),
        # the actuator screws must go in before the halves close (B2 before S3)
        'key_after_halves_closed': tool_access('R2A_SHCS_M3x10_Actuator', 3.0,
                                               [L.PART['OUTB'], L.PART['INB']]),
    }
    # informational, expected CLEAR: the five used housing holes lie outside
    # the crank sweep, so the crank never blocks their key path
    out['info_key_with_crank_fitted'] = tool_access('R2A_SHCS_M3x10_Actuator', 3.0,
                                                    [L.PART['OUTB'], L.PART['CRANK'],
                                                     L.PART['CRANK_CAP']])
    with open(path, 'w') as s:
        json.dump(out, s, indent=1)
    return {k: v['clear'] for k, v in out.items()}
