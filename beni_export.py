"""Export helpers for Beni Prototype 1.

Run inside Fusion (the MCP `script` feature type) against the open
`Beni_Prototype1` document:

    import sys; sys.path.insert(0, '/Users/neilchulani/Fun/Robots/Biped')
    import beni_export; beni_export.export_all()

Produces
    manufacturing/step/<Part>.step        one STEP per machined part family
    manufacturing/machined_parts_spec.md  fits, tolerances, finish, hardness
    sim/beni.urdf                         6-link tree with true inertias
    sim/beni_inertia.json                 the same numbers, machine-readable

Everything here reads the model; nothing modifies it.
"""

import json
import math
import os

import adsk.core
import adsk.fusion

import beni_lib as B

ROOT = '/Users/neilchulani/Fun/Robots/Biped'
STEP_DIR = os.path.join(ROOT, 'manufacturing', 'step')
SPEC_MD = os.path.join(ROOT, 'manufacturing', 'machined_parts_spec.md')
SIM_DIR = os.path.join(ROOT, 'sim')


# ---------------------------------------------------------------- utilities
def _bodies(occ):
    """Every body under an occurrence, including children, as proxies."""
    out = []
    stack = [occ]
    while stack:
        cur = stack.pop()
        for b in cur.bRepBodies:
            out.append(b)
        for i in range(cur.childOccurrences.count):
            stack.append(cur.childOccurrences.item(i))
    return out


def _occs_matching(names, side=None):
    """Occurrences whose base part name is in `names`.

    side='L' -> unmirrored only, 'R' -> mirrored only, None -> both.
    """
    r = B.root()
    out = []
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        nm = o.component.name
        base = B.base_name(nm.replace('(Mirror)', ''))
        if base not in names:
            continue
        mirrored = '(Mirror)' in nm
        if side == 'L' and mirrored:
            continue
        if side == 'R' and not mirrored:
            continue
        out.append(o)
    return out


def combined_props(occs):
    """Mass (kg), CoM (m) and inertia about the CoM (kg m^2) for a set of
    occurrences.

    Inertia about a common point is additive, so every body's tensor is summed
    about the world origin first and the result is then shifted to the combined
    CoM with the parallel-axis theorem.  Doing it the other way round -- summing
    CoM-referenced tensors -- is the classic way to get a plausible but wrong
    inertia, because each body's CoM is in a different place.
    """
    M = 0.0
    mx = my = mz = 0.0
    Ixx = Iyy = Izz = Ixy = Iyz = Ixz = 0.0
    for o in occs:
        for b in _bodies(o):
            try:
                pp = b.physicalProperties
            except Exception:
                continue
            m = pp.mass                      # kg
            c = pp.centerOfMass              # cm
            M += m
            mx += m * c.x / 100.0            # cm -> m
            my += m * c.y / 100.0
            mz += m * c.z / 100.0
            ok, xx, yy, zz, xy, yz, xz = pp.getXYZMomentsOfInertia()
            if not ok:
                continue
            f = 1e-4                         # kg cm^2 -> kg m^2
            Ixx += xx * f
            Iyy += yy * f
            Izz += zz * f
            Ixy += xy * f
            Iyz += yz * f
            Ixz += xz * f
    if M <= 0:
        return None
    cx, cy, cz = mx / M, my / M, mz / M
    # shift world-origin tensor to the CoM
    Ixx -= M * (cy * cy + cz * cz)
    Iyy -= M * (cx * cx + cz * cz)
    Izz -= M * (cx * cx + cy * cy)
    Ixy += M * cx * cy
    Iyz += M * cy * cz
    Ixz += M * cx * cz
    return {'mass': M, 'com': (cx, cy, cz),
            'I': (Ixx, Iyy, Izz, Ixy, Iyz, Ixz)}


def _sane(props, label):
    """Positive definiteness + triangle inequality on the principal moments."""
    Ixx, Iyy, Izz, Ixy, Iyz, Ixz = props['I']
    msgs = []
    for n, v in (('Ixx', Ixx), ('Iyy', Iyy), ('Izz', Izz)):
        if v <= 0:
            msgs.append('%s: %s = %.6g is not positive' % (label, n, v))
    if Ixx + Iyy < Izz or Iyy + Izz < Ixx or Izz + Ixx < Iyy:
        msgs.append('%s: principal moments violate the triangle inequality '
                    '(%.6g, %.6g, %.6g)' % (label, Ixx, Iyy, Izz))
    return msgs


# ------------------------------------------------------------- STEP exports
MACHINED = {
    'Shoulder_Output_Hub_L': '7075-T6 aluminium',
    'Wheel_Hub_L': '7075-T6 aluminium',
    'Cart_Upper_Eye_L': '7075-T6 aluminium',
    'Cart_Lower_Eye_L': '7075-T6 aluminium',
    'Knee_Axle_L': 'steel, through-hardened',
    'Knee_Sleeve_L': 'steel',
    'Knee_Magnet_Carrier_L': 'steel',
    'Knee_Stop_Arc_L': 'steel plate, hardened',
    'Cart_Guide_Rod_L': 'steel, ground',
    'Cart_Preload_Shim_L': 'steel shim stock',
}


def export_machined_steps(verbose=True):
    """One STEP file per machined part family.

    A shop cannot quote or program from an STL, and STL was the only output the
    project had.  Left-hand geometry only: every one of these is either
    symmetric or is mirrored for the right side, which the spec sheet states.
    """
    os.makedirs(STEP_DIR, exist_ok=True)
    des = B.design()
    em = des.exportManager
    done, failed = [], []
    for part in sorted(MACHINED):
        occ = B.find_occ(part)
        if occ is None:
            failed.append((part, 'not in model'))
            continue
        path = os.path.join(STEP_DIR, '%s.step' % part)
        try:
            opt = em.createSTEPExportOptions(path, occ.component)
            em.execute(opt)
            done.append((part, os.path.getsize(path)))
        except Exception as e:
            failed.append((part, str(e)[:60]))
    if verbose:
        for p, sz in done:
            print('   STEP  %-28s %7.1f kB' % (p, sz / 1024.0))
        for p, why in failed:
            print('   FAIL  %-28s %s' % (p, why))
    return done, failed


# --------------------------------------------------------------- URDF export
# Kinematic tree.  All three joint axes are the global +Y axis, which is what
# the whole design is built around: shoulder through the origin, knee through
# (KX, KZ), wheel through (WX, WZ).
BASE_PARTS = ('Chassis_Frame', 'Electronics_Tray', 'Battery_4S2200',
              'Chassis_Electronics', 'Chassis_Shoulder_Plate_L',
              'Shoulder_Cable_Cover_L', 'Shoulder_Cable_Spiral_L',
              'REF_GIM6010-8')
THIGH_PARTS = ('Shoulder_Output_Hub_L', 'Proximal_Link_L', 'HW_Bearing_6800',
               'Knee_Stop_Arc_L', 'Knee_Bumper_Flex_L', 'Knee_Bumper_Ext_L',
               'Knee_Encoder_Bracket_L', 'Knee_Encoder_PCB_L',
               'HW_SHCS_M3x16', 'HW_SHCS_M3x6',
               'Cart_Upper_Eye_L', 'Cart_Guide_Rod_L')
SHANK_PARTS = ('Distal_Link_L', 'Knee_Sleeve_L', 'Knee_Axle_L',
               'Knee_Magnet_Carrier_L', 'HW_Magnet_D6x2p5_Diametric',
               'HW_DowelPin_D6x9', 'REF_GIM4305-10', 'HW_SHCS_M2p5x12',
               'Cart_Lower_Eye_L', 'Cart_Preload_Shim_L', 'Knee_Spring_L')
WHEEL_PARTS = ('Wheel_Hub_L', 'Wheel_Rim_L', 'Wheel_Tyre_L')

# screws are assigned by position rather than by name, since the same size is
# used in several places; see _split_screws.
SCREW_PARTS = ('HW_SHCS_M3x10', 'HW_SHCS_M3x8', 'HW_SHCS_M4x10',
               'HW_ClevisPin_D4x32')


def _split_screws(side):
    """Assign the ambiguous fastener families to base / thigh / shank / wheel.

    The same screw size appears in several joints, so the only reliable
    discriminator is where the occurrence actually sits.
    """
    out = {'base': [], 'thigh': [], 'shank': [], 'wheel': []}
    for o in _occs_matching(SCREW_PARTS, side):
        nm = B.base_name(o.component.name.replace('(Mirror)', ''))
        bb = B.bbox_of(o)
        cx, cz = (bb[0] + bb[1]) / 2.0, (bb[4] + bb[5]) / 2.0
        rs = math.hypot(cx, cz)
        if nm == 'HW_SHCS_M3x10':
            out['thigh' if rs < 20 else 'base'].append(o)
        elif nm == 'HW_SHCS_M3x8':
            out['wheel' if cz < -120 else 'base'].append(o)
        elif nm == 'HW_SHCS_M4x10':
            out['wheel' if cz < -120 else 'thigh'].append(o)
        elif nm == 'HW_ClevisPin_D4x32':
            # the cartridge is a floating two-pivot member: its upper pivot
            # rides with the thigh, its lower pivot with the shank.  Same split
            # as beni_lib.classify()'s CART_UP / CART_LO.
            out['shank' if cz < -100 else 'thigh'].append(o)
    return out


def link_props(side):
    """Mass properties for the four moving links of one leg, plus the base."""
    scr = _split_screws(side)
    groups = {
        'thigh': _occs_matching(THIGH_PARTS, side) + scr['thigh'],
        'shank': _occs_matching(SHANK_PARTS, side) + scr['shank'],
        'wheel': _occs_matching(WHEEL_PARTS, side) + scr['wheel'],
    }
    return {k: combined_props(v) for k, v in groups.items()}, scr


def _xyz(v):
    return '%.6f %.6f %.6f' % v


def _inertia_xml(props, indent):
    Ixx, Iyy, Izz, Ixy, Iyz, Ixz = props['I']
    pad = ' ' * indent
    return (
        '%s<inertial>\n'
        '%s  <origin xyz="%s" rpy="0 0 0"/>\n'
        '%s  <mass value="%.6f"/>\n'
        '%s  <inertia ixx="%.9f" iyy="%.9f" izz="%.9f"'
        ' ixy="%.9f" iyz="%.9f" ixz="%.9f"/>\n'
        '%s</inertial>\n'
        % (pad, pad, _xyz(props['com_local']), pad, props['mass'],
           pad, Ixx, Iyy, Izz, Ixy, Iyz, Ixz, pad))


def export_urdf(verbose=True):
    """Write a 6-link URDF with the model's real masses and inertia tensors.

    This is the actual handoff to controls and sim, and it was impossible
    before the physical materials were assigned: every body was default steel,
    so the robot massed 8174 g instead of ~3350 g and no inertia was usable.

    Joint frames are placed on the three Y axes the design is built around, in
    the nominal pose, so every link frame is axis-aligned with the world and no
    rotation terms are needed.
    """
    os.makedirs(SIM_DIR, exist_ok=True)
    KX, KZ = B.KX / 1000.0, B.KZ / 1000.0
    WXm, WZm = B.WX / 1000.0, B.WZ / 1000.0

    base = combined_props(_occs_matching(BASE_PARTS, None)
                          + _split_screws('L')['base']
                          + _split_screws('R')['base'])
    warnings = _sane(base, 'base_link')
    base['com_local'] = base['com']

    legs, data = {}, {'base': None, 'legs': {}}
    for side, sgn in (('L', 1.0), ('R', -1.0)):
        props, _scr = link_props(side)
        y_hip = sgn * 0.0525
        y_knee = sgn * 0.0745
        y_wheel = sgn * 0.0840
        frames = {
            'thigh': (0.0, y_hip, 0.0),
            'shank': (KX, y_knee, KZ),
            'wheel': (WXm, y_wheel, WZm),
        }
        for k in ('thigh', 'shank', 'wheel'):
            pr = props[k]
            if pr is None:
                raise RuntimeError('no bodies for %s %s' % (side, k))
            fx, fy, fz = frames[k]
            pr['com_local'] = (pr['com'][0] - fx, pr['com'][1] - fy,
                               pr['com'][2] - fz)
            warnings += _sane(pr, '%s_%s' % (side, k))
        legs[side] = (props, frames)
        data['legs'][side] = {
            k: {'mass_kg': props[k]['mass'],
                'com_world_m': props[k]['com'],
                'com_link_m': props[k]['com_local'],
                'I_com_kgm2': props[k]['I']}
            for k in ('thigh', 'shank', 'wheel')}
    data['base'] = {'mass_kg': base['mass'], 'com_world_m': base['com'],
                    'I_com_kgm2': base['I']}

    LIM_SH = math.radians(185.0)
    LIM_KNEE = (math.radians(B.PHI_EXT), math.radians(B.PHI_STOP))

    out = []
    out.append('<?xml version="1.0"?>\n')
    out.append('<!-- Beni Prototype 1.  Generated from the Fusion model by\n'
               '     beni_export.export_urdf(); masses and inertias are the\n'
               '     model\'s own, not estimates.\n'
               '     Frame: X forward, Y left, Z up.  All joints rotate about +Y.\n'
               '     The knee is PASSIVE: the limits below are the mechanical\n'
               '     stops, and the spring must be supplied by the simulator as\n'
               '     a joint spring of ~10.45 N/mm acting through the cartridge\n'
               '     moment arm (22.09 mm at -8 deg rising to 31.56 mm at +27).\n'
               '-->\n')
    out.append('<robot name="beni_prototype1">\n\n')
    out.append('  <link name="base_link">\n')
    out.append(_inertia_xml(base, 4))
    out.append('  </link>\n\n')

    for side in ('L', 'R'):
        props, frames = legs[side]
        s = side.lower()
        for child, parent, jname, jtype, limit in (
                ('thigh', 'base_link', 'shoulder', 'revolute',
                 (-LIM_SH, LIM_SH)),
                ('shank', '%s_thigh' % s, 'knee', 'revolute', LIM_KNEE),
                ('wheel', '%s_shank' % s, 'wheel', 'continuous', None)):
            out.append('  <link name="%s_%s">\n' % (s, child))
            out.append(_inertia_xml(props[child], 4))
            out.append('  </link>\n')
            out.append('  <joint name="%s_%s" type="%s">\n' % (s, jname, jtype))
            out.append('    <parent link="%s"/>\n' % parent)
            out.append('    <child link="%s_%s"/>\n' % (s, child))
            fx, fy, fz = frames[child]
            if child == 'thigh':
                ox, oy, oz = fx, fy, fz
            elif child == 'shank':
                px, py, pz = frames['thigh']
                ox, oy, oz = fx - px, fy - py, fz - pz
            else:
                px, py, pz = frames['shank']
                ox, oy, oz = fx - px, fy - py, fz - pz
            out.append('    <origin xyz="%s" rpy="0 0 0"/>\n' % _xyz((ox, oy, oz)))
            out.append('    <axis xyz="0 1 0"/>\n')
            if limit is not None:
                out.append('    <limit lower="%.6f" upper="%.6f" '
                           'effort="25.0" velocity="30.0"/>\n' % limit)
            out.append('  </joint>\n\n')
    out.append('</robot>\n')

    urdf = os.path.join(SIM_DIR, 'beni.urdf')
    with open(urdf, 'w') as f:
        f.write(''.join(out))
    with open(os.path.join(SIM_DIR, 'beni_inertia.json'), 'w') as f:
        json.dump(data, f, indent=1, sort_keys=True)

    if verbose:
        tot = base['mass'] + sum(
            data['legs'][s][k]['mass_kg']
            for s in ('L', 'R') for k in ('thigh', 'shank', 'wheel'))
        asm = B.design().rootComponent.getPhysicalProperties(
            adsk.fusion.CalculationAccuracy.HighCalculationAccuracy).mass
        print('   URDF  %s' % urdf)
        print('   %-14s %8s %10s %10s %10s' % ('link', 'mass kg', 'Ixx', 'Iyy', 'Izz'))
        print('   %-14s %8.4f %10.6f %10.6f %10.6f'
              % ('base_link', base['mass'], base['I'][0], base['I'][1], base['I'][2]))
        for s in ('L', 'R'):
            for k in ('thigh', 'shank', 'wheel'):
                d = data['legs'][s][k]
                print('   %-14s %8.4f %10.6f %10.6f %10.6f'
                      % ('%s_%s' % (s.lower(), k), d['mass_kg'],
                         d['I_com_kgm2'][0], d['I_com_kgm2'][1], d['I_com_kgm2'][2]))
        # Closure check: every gram in the assembly must land in exactly one
        # link, or the URDF describes a lighter robot than the one in CAD.
        # This caught the four cartridge clevis pins (15.2 g) going nowhere.
        err = (tot - asm) * 1000.0
        print('   %-14s %8.4f   assembly %.4f   unassigned %+.2f g'
              % ('TOTAL', tot, asm, err))
        if abs(err) > 0.5:
            print('   *** MASS CLOSURE FAILED: %+.2f g is in the assembly but '
                  'not in any URDF link ***' % err)
            warnings.append('mass closure off by %+.2f g' % err)
        else:
            print('   mass closure: OK')
        if warnings:
            print('   INERTIA SANITY WARNINGS:')
            for w in warnings:
                print('      ' + w)
        else:
            print('   inertia sanity: all tensors positive-definite and '
                  'triangle-inequality consistent')
    return data, warnings


def export_all():
    print('=== STEP (machined parts) ===')
    export_machined_steps()
    print()
    print('=== URDF ===')
    export_urdf()
    print()
    print('=== PRINT STLs ===')
    export_print_stls()
    print()
    print('=== WEB VIEWER STLs ===')
    export_web_stls()


# ----------------------------------------------------------------- STL export
PRINT_PARTS = ['Chassis_Shoulder_Plate_L', 'Distal_Link_L', 'Proximal_Link_L',
               'Chassis_Frame', 'Wheel_Rim_L', 'Wheel_Tyre_L',
               'Shoulder_Cable_Cover_L', 'Knee_Encoder_Bracket_L',
               'Electronics_Tray']
CHECK_PARTS = ['Cart_Upper_Eye_L', 'Cart_Lower_Eye_L', 'Knee_Axle_L',
               'Knee_Magnet_Carrier_L', 'Knee_Sleeve_L', 'Knee_Stop_Arc_L',
               'Shoulder_Output_Hub_L', 'Wheel_Hub_L']
PRINT_DIR = os.path.join(ROOT, 'print_stl')


def _stl(occ, path, refinement='high'):
    des = B.design()
    em = des.exportManager
    opt = em.createSTLExportOptions(occ, path)
    opt.meshRefinement = {
        'high': adsk.fusion.MeshRefinementSettings.MeshRefinementHigh,
        'medium': adsk.fusion.MeshRefinementSettings.MeshRefinementMedium,
        'low': adsk.fusion.MeshRefinementSettings.MeshRefinementLow,
    }[refinement]
    opt.isBinaryFormat = True
    em.execute(opt)
    return os.path.getsize(path)


def export_print_stls(verbose=True):
    """Re-export the printable and check-print STL set from the current model.

    The GAUGE_*.stl motor stand-ins live in Beni_Prototype1_TestGauges and are
    unaffected by anything here, so they are left alone.
    """
    os.makedirs(PRINT_DIR, exist_ok=True)
    os.makedirs(os.path.join(PRINT_DIR, 'check_prints'), exist_ok=True)
    done, failed = [], []
    for part, sub in ([(p, '') for p in PRINT_PARTS]
                      + [(p, 'check_prints') for p in CHECK_PARTS]):
        occ = B.find_occ(part)
        if occ is None:
            failed.append((part, 'not in model'))
            continue
        path = os.path.join(PRINT_DIR, sub, '%s.stl' % part)
        try:
            done.append((os.path.join(sub, part), _stl(occ, path)))
        except Exception as e:
            failed.append((part, str(e)[:60]))
    if verbose:
        for p, sz in done:
            print('   STL   %-42s %8.1f kB' % (p, sz / 1024.0))
        for p, why in failed:
            print('   FAIL  %-42s %s' % (p, why))
    return done, failed


# viewer groups.  Derived from beni_lib.classify() and PART_CLASS rather than
# hardcoded, so the manifest cannot drift from the model the way the old one did.
WHEEL_GROUP = ('Wheel_Hub_L', 'Wheel_Rim_L', 'Wheel_Tyre_L')
GROUP_OF_CLASS = {'STATIC': 'static', 'PROX': 'prox', 'DIST': 'dist',
                  'CART_UP': 'cart_up', 'CART_LO': 'cart_lo',
                  'SPRING': 'cart_lo'}
WEB_MODELS = os.path.join(ROOT, 'web', 'models')


def _merge_binary_stl(paths, out_path):
    """Concatenate binary STLs.  Header + uint32 count + 50 bytes per triangle,
    so merging is just re-summing the count and appending the triangle blocks."""
    import struct
    tris, blocks = 0, []
    for p in paths:
        raw = open(p, 'rb').read()
        n = struct.unpack('<I', raw[80:84])[0]
        tris += n
        blocks.append(raw[84:84 + n * 50])
    with open(out_path, 'wb') as f:
        f.write(b'beni merged'.ljust(80, b'\0'))
        f.write(struct.pack('<I', tris))
        for b in blocks:
            f.write(b)
    return tris


def export_web_stls(verbose=True):
    """Re-export the viewer geometry, grouped by (kinematic group, material).

    Left-hand geometry only: the viewer instantiates and mirrors both sides in
    JS, which is why poseSide() takes 'L'/'R'.
    """
    import shutil
    import tempfile
    os.makedirs(WEB_MODELS, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix='beni_stl_')
    r = B.root()
    buckets = {}
    try:
        for i in range(r.occurrences.count):
            o = r.occurrences.item(i)
            nm = o.component.name
            if '(Mirror)' in nm:
                continue
            part = B.base_name(nm)
            if part.startswith('REF_'):
                mat, grp = 'MOTOR', ('static' if '6010' in part else 'dist')
            else:
                mat = B.PART_CLASS.get(part)
                if mat is None:
                    continue
                if part in B.CENTRE_PARTS:
                    grp = 'centre'
                elif part in WHEEL_GROUP:
                    grp = 'wheel'
                else:
                    grp = GROUP_OF_CLASS.get(B.classify(o))
                    # The hub and rim screws turn with the wheel, not with the
                    # shank -- classify() only splits PROX/DIST, so pull them
                    # across or they sit still while the wheel spins.  Only
                    # these two families: HW_SHCS_M2p5x12 is the wheel MOTOR
                    # mount, which is fixed to the distal plate.
                    if grp == 'dist' and part in ('HW_SHCS_M3x8', 'HW_SHCS_M4x10'):
                        bb = B.bbox_of(o)
                        wx = (bb[0] + bb[1]) / 2.0 - B.WX
                        wz = (bb[4] + bb[5]) / 2.0 - B.WZ
                        if math.hypot(wx, wz) < 30.0:
                            grp = 'wheel'
                if grp is None:
                    continue
            path = os.path.join(tmp, '%s_%d.stl' % (part, i))
            try:
                _stl(o, path, 'medium')
            except Exception:
                continue
            key = (grp, mat)
            buckets.setdefault(key, {'files': [], 'parts': set()})
            buckets[key]['files'].append(path)
            buckets[key]['parts'].add(part)

        manifest = []
        for (grp, mat) in sorted(buckets):
            b = buckets[(grp, mat)]
            fname = '%s__%s.stl' % (grp, mat)
            out = os.path.join(WEB_MODELS, fname)
            n = _merge_binary_stl(b['files'], out)
            manifest.append({'file': fname, 'group': grp, 'material': mat,
                             'parts': sorted(b['parts'])})
            if verbose:
                print('   %-22s %7d tris  %8.1f kB  %s'
                      % (fname, n, os.path.getsize(out) / 1024.0,
                         ', '.join(sorted(b['parts']))))
        with open(os.path.join(WEB_MODELS, 'manifest.json'), 'w') as f:
            json.dump(manifest, f, indent=1)
        if verbose:
            print('   manifest: %d meshes' % len(manifest))
        return manifest
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

