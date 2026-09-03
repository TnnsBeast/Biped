"""Exports for the Beni single-leg test rig.

Runs inside Fusion against `Beni_SingleLegRig`.  Produces:

  * `rig_stl/*.stl`            every printed rig part, at assembly coordinates
  * `rig_stl/reroute/*.stl`    the formerly-machined parts, now printed

There is no DXF output.  The build has no laser-cut or machined parts: the steel
arc stop was replaced by a compression stack in the spring cartridge and a
printed plate, and the steel ballast sectors by printed pots filled with
off-the-shelf shot.  The retired laser files are kept under `archive_laser/` in
case the two-leg build wants the steel version back.
"""

import json
import math
import os

import adsk.core
import adsk.fusion

import beni_lib as B
import rig_lib as R

ROOT = '/Users/neilchulani/Robots/Biped'
STL_DIR = os.path.join(ROOT, 'rig_stl')
FIRST_ARTICLE_DIR = os.path.join(ROOT, 'first_article_stl', 'mode_a')
ABS_ASSEMBLY_DIR = os.path.join(ROOT, 'first_article_stl',
                                'assembly_dry_fit')
HEATSET_RELEASE_MANIFEST = os.path.join(
    ROOT, 'first_article_stl', 'heatset_receiver_release_manifest.json')
INSERT_FIT_DIR = os.path.join(ROOT, 'first_article_stl', 'insert_fit')

# printed rig parts, with the orientation each one has to be printed in
RIG_PRINT = [
    ('RIG_Stand', 'mount face (y = 42.00) flat on the bed, building inboard. '
                  'Every layer is then an XZ slice, so the dominant 11.00 N.m '
                  'of shoulder yaw -- a couple lying IN the XZ plane -- stays '
                  'in the print plane at 84-102 MPa instead of across the '
                  'layers at 26-50.  No support: the Y thickness only ever '
                  'decreases away from the bed.  Needs a bed >= 300 mm'),
    ('RIG_Carriage', 'plate face flat on the bed; bending stays in the print '
                     'plane and the 8 block-screw counterbores print as pockets'),
    ('RIG_Index_Bar', 'flat on the bed, station holes vertical; the pin bears '
                      'across layers, not along them'),
    ('RIG_Torque_Arm', 'flat on the bed, arm plane parallel to the bed; the '
                       '200 mm bending load is then fully in-plane'),
    ('RIG_Floor_Plate', 'flat on the bed'),
    ('RIG_Cable_Post_A', 'flat on the bed, sector face down'),
    ('RIG_Cable_Post_B', 'flat on the bed'),
    ('RIG_Cable_Anchor_ModeA', 'flat on the bed, either broad face down; '
                               'first article in ABS'),
    ('RIG_Knee_Magnet_Carrier_L', 'bore axis vertical -- this is what holds the '
                                  '0.05 TIR the encoder needs'),
    ('RIG_Knee_Stop_Plate_L', 'flat on the bed; replaces the laser-cut steel arc. '
                              'It keeps the -8 deg extension stop and a +28 deg '
                              'flexion backup only -- the working +27 deg stop is '
                              'the washer stack in the cartridge'),
    ('RIG_Knee_Bumper_Tube_L', 'TPU 95A, bore axis vertical. Sits AROUND the '
                               'washer stack so the two act in parallel'),
    ('RIG_Ballast_Pot', 'open side up, no support; fill with steel shot'),
]

# formerly machined, now printed (beni_rig_no_machining.md §3)
REROUTE_PRINT = [
    ('Shoulder_Output_Hub_L', 'flange face flat on the bed, so torque loads the '
                              'bolt circle in XY and the 3 dowel holes see '
                              'shear ACROSS layers'),
    ('Wheel_Hub_L', 'flat on the bed, register face up'),
    ('Cart_Upper_Eye_L', 'pivot bore axis vertical; printed on its side the eye '
                         'splits along a layer'),
    ('Cart_Lower_Eye_L', 'pivot bore axis vertical'),
    ('Distal_Link_L', 'on edge, link axis vertical -- RE-EXPORTED: its Ø16 '
                      'sleeve bore is now Ø10 (§2.3)'),
]


def _stl(occ, path, refinement='high'):
    des = B.design()
    em = des.exportManager
    opt = em.createSTLExportOptions(occ, path)
    opt.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh
    opt.isBinaryFormat = True
    em.execute(opt)
    return os.path.getsize(path)


def _export_y_face_down(occ, export_name, out_dir, support_policy,
                        side='max'):
    """Export a bed-ready copy with one Y-normal source face at Z=0.

    The source occurrence is never moved.  The temporary solid and its Fusion
    viewport record are deleted after export, so this is safe in a saved rig.
    """
    if side not in ('min', 'max'):
        raise ValueError("side must be 'min' or 'max'")
    comp = occ.component
    if comp.bRepBodies.count != 1:
        raise RuntimeError('%s must contain exactly one solid body' % comp.name)
    body = comp.bRepBodies.item(0)
    source_y = (body.boundingBox.maxPoint.y if side == 'max'
                else body.boundingBox.minPoint.y)
    normal_sign = 1.0 if side == 'max' else -1.0
    support_area = 0.0
    support_faces = []
    for i in range(body.faces.count):
        face = body.faces.item(i)
        if adsk.core.Plane.cast(face.geometry) is None:
            continue
        ok, normal = face.evaluator.getNormalAtPoint(face.pointOnFace)
        if not ok:
            raise RuntimeError('Fusion face-normal evaluation failed')
        if (normal.y * normal_sign > 0.999999 and
                abs(face.pointOnFace.y - source_y) <= 0.0001):
            support_faces.append(i)
            support_area += face.area
    if not support_faces:
        raise RuntimeError('%s has no planar %simum-Y support face'
                           % (comp.name, side))

    temporary = adsk.fusion.TemporaryBRepManager.get()
    angle = -math.pi / 2.0 if side == 'max' else math.pi / 2.0
    rotation = adsk.core.Matrix3D.create()
    rotation.setToRotation(angle, adsk.core.Vector3D.create(1, 0, 0),
                           adsk.core.Point3D.create(0, 0, 0))
    trial = temporary.copy(body)
    if not temporary.transform(trial, rotation):
        raise RuntimeError('Fusion print-orientation trial failed for %s' % comp.name)
    trial_bb = trial.boundingBox
    transform = adsk.core.Matrix3D.create()
    transform.setToRotation(angle, adsk.core.Vector3D.create(1, 0, 0),
                            adsk.core.Point3D.create(0, 0, 0))
    transform.translation = adsk.core.Vector3D.create(
        0, 0, -trial_bb.minPoint.z)
    transformed = temporary.copy(body)
    if not temporary.transform(transformed, transform):
        raise RuntimeError('Fusion print transform failed for %s' % comp.name)

    root = B.root()
    print_occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    print_occ.component.name = export_name
    base = print_occ.component.features.baseFeatures.add()
    base.name = export_name + '_FusionTransform'
    base.startEdit()
    print_body = print_occ.component.bRepBodies.add(transformed, base)
    base.finishEdit()
    if print_body is None or not print_body.isSolid:
        raise RuntimeError('Fusion could not create oriented solid %s' % export_name)
    print_body.name = export_name

    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, export_name + '.stl')
    image_path = os.path.join(out_dir, '00_fusion_' + export_name + '.png')
    visibility = [(item, item.isLightBulbOn) for item in root.occurrences]
    try:
        for item, _was_on in visibility:
            item.isLightBulbOn = (item == print_occ)
        app = adsk.core.Application.get()
        app.activeViewport.fit()
        app.activeViewport.refresh()
        size = _stl(print_occ, path)
        if not app.activeViewport.saveAsImageFile(image_path, 1600, 1200):
            raise RuntimeError('Fusion screenshot failed for %s' % export_name)
    finally:
        for item, was_on in visibility:
            if item != print_occ:
                item.isLightBulbOn = was_on
        print_occ.deleteMe()
        adsk.core.Application.get().activeViewport.fit()

    return {
        'source_part': comp.name,
        'export_name': export_name,
        'stl': path,
        'stl_bytes': size,
        'fusion_screenshot': image_path,
        'rotation_axis': '+X',
        'rotation_deg': -90.0 if side == 'max' else 90.0,
        'source_support_side': side,
        'source_support_face_y_mm': round(source_y * 10.0, 4),
        'source_support_face_indices': support_faces,
        'support_face_area_mm2': round(support_area * 100.0, 3),
        'oriented_bbox_mm': [
            round((trial_bb.maxPoint.x - trial_bb.minPoint.x) * 10.0, 4),
            round((trial_bb.maxPoint.y - trial_bb.minPoint.y) * 10.0, 4),
            round((trial_bb.maxPoint.z - trial_bb.minPoint.z) * 10.0, 4),
        ],
        'minimum_z_mm': 0.0,
        'support_policy': support_policy,
    }


def _export_max_y_face_down(occ, export_name, out_dir, support_policy):
    return _export_y_face_down(occ, export_name, out_dir, support_policy,
                               side='max')


def _export_min_y_face_down(occ, export_name, out_dir, support_policy):
    return _export_y_face_down(occ, export_name, out_dir, support_policy,
                               side='min')


def export_stls(verbose=True):
    os.makedirs(STL_DIR, exist_ok=True)
    os.makedirs(os.path.join(STL_DIR, 'reroute'), exist_ok=True)
    done, failed = [], []
    for part, note in [(p, '') for p, _n in RIG_PRINT]:
        occ = B.find_occ(part)
        if occ is None:
            failed.append((part, 'not in model'))
            continue
        try:
            done.append((part, _stl(occ, os.path.join(STL_DIR, part + '.stl'))))
        except Exception as e:
            failed.append((part, str(e)[:70]))
    for part, _note in REROUTE_PRINT:
        occ = B.find_occ(part)
        if occ is None:
            failed.append((part, 'not in model'))
            continue
        try:
            done.append(('reroute/' + part,
                         _stl(occ, os.path.join(STL_DIR, 'reroute',
                                                part + '.stl'))))
        except Exception as e:
            failed.append((part, str(e)[:70]))
    if verbose:
        for p, sz in done:
            print('   STL   %-40s %9.1f kB' % (p, sz / 1024.0))
        for p, why in failed:
            print('   FAIL  %-40s %s' % (p, why))
    return done, failed


def export_all():
    print('=== rig STLs ===')
    export_stls()


def export_mode_a_anchor_first_article():
    """Export only the new Mode A cable anchor for the first ABS batch.

    The body is intentionally exported from its validated rig occurrence.  Its
    broad faces are XZ in assembly coordinates, so the slicer must place either
    broad face on the bed (a single 90 degree rotation about X).
    """
    os.makedirs(FIRST_ARTICLE_DIR, exist_ok=True)
    part = 'RIG_Cable_Anchor_ModeA'
    occ = B.find_occ(part)
    if occ is None:
        raise RuntimeError('%s is not in the active rig' % part)
    path = os.path.join(FIRST_ARTICLE_DIR, part + '.stl')
    size = _stl(occ, path)
    bb = B.bbox_of(occ)
    manifest = {
        'document': adsk.core.Application.get().activeDocument.name,
        'part': part,
        'material': 'ABS first article',
        'bbox_mm': [round(bb[1] - bb[0], 4),
                    round(bb[3] - bb[2], 4),
                    round(bb[5] - bb[4], 4)],
        'orientation': 'place either 41.0 x 15.45 mm broad face on bed',
        'hardware': '2 x M3 x 8 SHCS plus washers',
        'stl': path,
        'stl_bytes': size,
    }
    manifest_path = os.path.join(FIRST_ARTICLE_DIR,
                                 'fusion_manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as stream:
        json.dump(manifest, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'exported': manifest,
                      'manifest': manifest_path}, indent=2, sort_keys=True))
    return manifest


def export_abs_shoulder_hub_first_article(pin_bore_d=4.15):
    """Build/export the ABS-only shoulder hub selected by the pin coupon.

    This creates a separately named transient component so the released
    Ø4.05 master hub remains untouched.  Both native-coordinate and bed-ready
    outputs are exported, then the transient component is deleted.
    """
    if abs(pin_bore_d - 4.15) > 1e-6:
        raise ValueError('only the owner-tested Ø4.15 ABS variant is released')
    os.makedirs(ABS_ASSEMBLY_DIR, exist_ok=True)
    name = 'ABS_FA_Shoulder_Output_Hub_L_D4p15'
    occ = R.guarded(B.build_shoulder_hub,
                    pin_bore_d=pin_bore_d,
                    component_name=name)
    if occ.component.bRepBodies.count != 1:
        raise RuntimeError('%s must contain exactly one solid body' % name)

    # Recover exact analytic cylinder diameters from the B-Rep, rather than
    # treating the STL or Fusion's display bounding box as authoritative.
    diameters = []
    body = occ.component.bRepBodies.item(0)
    for face in body.faces:
        geo = face.geometry
        if geo.objectType.endswith('Cylinder'):
            diameters.append(round(geo.radius * 20.0, 5))
    pin_faces = sum(abs(d - pin_bore_d) <= 1e-4 for d in diameters)
    if pin_faces != 3:
        raise RuntimeError('expected 3 Ø%.2f cylinder faces, found %d: %s'
                           % (pin_bore_d, pin_faces, sorted(diameters)))
    centres = B._receiver_centres(0.0, 0.0, B.HUB_LINK_PCD, 6,
                                  B.HUB_LINK_A0)
    insert_spans = B._receiver_face_spans(occ, B.HUB_LINK_INSERT_D, centres)
    expected_span = (round(B.HUB_Y1 - B.HUB_LINK_INSERT_HOLE_DEPTH, 3),
                     round(B.HUB_Y1, 3))
    found_spans = sorted((round(a, 3), round(b, 3))
                         for a, b in insert_spans.values())
    if (len(insert_spans) != 6 or
            any(span != expected_span for span in found_spans)):
        raise RuntimeError('expected 6 Ø%.1f insert pockets at Y %s, found %s'
                           % (B.HUB_LINK_INSERT_D, expected_span, found_spans))

    path = os.path.join(ABS_ASSEMBLY_DIR, name + '.stl')
    size = _stl(occ, path)
    bb = B.bbox_of(occ)
    manifest = {
        'document': adsk.core.Application.get().activeDocument.name,
        'part': name,
        'purpose': 'unloaded ABS shoulder assembly and interface dry-fit',
        'material_release': 'ABS first article only; not PA-CF structural data',
        'source_geometry': ('Shoulder_Output_Hub_L with pin bores overridden; '
                            'six M4 heat-set receivers retained'),
        'pin_bores_mm': pin_bore_d,
        'pin_bore_count_brep': pin_faces,
        'pin_pcd_mm': B.SH_PIN_PCD,
        'pin_start_angle_deg': B.SH_PIN_A0,
        'link_insert_family': 'PSM Sonic-Lok SL-B-M4-5.8',
        'link_insert_count': 6,
        'link_insert_length_mm': B.HUB_LINK_INSERT_LEN,
        'link_insert_hole_diameter_mm': B.HUB_LINK_INSERT_D,
        'link_insert_hole_depth_mm': B.HUB_LINK_INSERT_HOLE_DEPTH,
        'link_insert_hole_y_span_mm': list(expected_span),
        'link_fastener': '6 x M4 x 10 SHCS',
        'nominal_envelope_mm': [B.HUB_FLANGE_D,
                                B.HUB_Y1 - B.HUB_Y0,
                                B.HUB_FLANGE_D],
        'fusion_bbox_mm': [round(bb[1] - bb[0], 4),
                           round(bb[3] - bb[2], 4),
                           round(bb[5] - bb[4], 4)],
        'orientation': ('use the supplied PRINT_ORIENTED STL; Ø56 outboard '
                        'flange face is at Z=0'),
        'restriction': 'no actuator torque, backdrive, spring, stand, or load',
        'stl': path,
        'stl_bytes': size,
    }
    # Keep a Fusion-authored visual record with only the transient article
    # visible, then export a separately transformed bed-ready solid.
    root = B.root()
    visibility = []
    for item in root.occurrences:
        visibility.append((item, item.isLightBulbOn))
        item.isLightBulbOn = (item == occ)
    adsk.core.Application.get().activeViewport.fit()
    image_path = os.path.join(ABS_ASSEMBLY_DIR,
                              '00_fusion_abs_shoulder_hub_d4p15.png')
    adsk.core.Application.get().activeViewport.saveAsImageFile(
        image_path, 1600, 1200)
    for item, was_on in visibility:
        item.isLightBulbOn = was_on

    oriented = _export_max_y_face_down(
        occ, name + '_PRINT_ORIENTED', ABS_ASSEMBLY_DIR,
        ('No supports. Six M4 insert pockets, three dowel-pin bores, six motor '
         'holes and the centre bore are vertical; the body contracts away '
         'from the Ø56 bed face.'))
    manifest['print_oriented'] = oriented
    manifest_path = os.path.join(ABS_ASSEMBLY_DIR,
                                 'fusion_manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as stream:
        json.dump(manifest, stream, indent=2, sort_keys=True)
        stream.write('\n')
    occ.deleteMe()

    print(json.dumps({'exported': manifest,
                      'manifest': manifest_path,
                      'image': image_path}, indent=2, sort_keys=True))
    return manifest


def export_abs_m4_insert_coupon():
    """Export a three-size ABS ladder for the specified short PSM M4 inserts.

    The nominal Ø5.6 comes from the manufacturer.  The adjacent ±0.1 mm
    stations identify the achieved printer/profile fit without scaling a part.
    All three reproduce the shoulder's 7.2 mm blind-hole depth and 0.8 mm
    floor; the same diameter result governs the wheel's through receivers.
    """
    os.makedirs(INSERT_FIT_DIR, exist_ok=True)
    name = 'ABS_CAL_PSM_SL_M4_INSERT_POCKET_LADDER'

    def build():
        B.drop_comp(name)
        occ = B.new_comp(name)
        comp = occ.component
        R.box(comp, -18.0, 18.0, 0.0, 8.0, -8.0, 8.0,
              op='new').bodies.item(0).name = name
        sketch = R.sk_on_y(comp, 8.0)
        for x, diameter in zip((-12.0, 0.0, 12.0), (5.5, 5.6, 5.7)):
            R.circle(sketch, x, 0.0, diameter)
        R.extrude(comp, R.profiles(sketch), -7.2, op='cut',
                  participants=R.bodies_of(comp))
        # One small through marker identifies the Ø5.5 end after the print is
        # removed from the bed; sizes then increase toward the unmarked end.
        sketch = R.sk_on_y(comp, -1.0)
        R.circle(sketch, -15.0, -5.0, 2.0)
        R.extrude(comp, sketch.profiles.item(0), 10.0, op='cut',
                  participants=R.bodies_of(comp))
        return occ

    R.replace_cart_stops()
    occ = R.guarded(build)
    expected = [(-12.0, 5.5), (0.0, 5.6), (12.0, 5.7)]
    measured = []
    for index, (x, diameter) in enumerate(expected):
        spans = B._receiver_face_spans(occ, diameter, [(x, 0.0)])
        found = sorted((round(a, 3), round(b, 3))
                       for a, b in spans.values())
        if found != [(0.8, 8.0)]:
            raise RuntimeError('coupon Ø%.1f pocket span is %s' %
                               (diameter, found))
        measured.append({'diameter_mm': diameter,
                         'station_from_marked_end': index + 1,
                         'distance_from_first_station_mm': index * 12.0,
                         'local_x_mm': x,
                         'depth_mm': 7.2,
                         'floor_mm': 0.8})

    oriented = _export_min_y_face_down(
        occ, name + '_PRINT_ORIENTED', INSERT_FIT_DIR,
        ('No supports. The 36 x 16 mm full face is the bed datum; all three '
         'blind insert pockets open upward. The Ø2 marker identifies the '
         'Ø5.5 end, and pocket size increases toward the unmarked end.'))
    manifest = {
        'document': adsk.core.Application.get().activeDocument.name,
        'part': name,
        'material': 'same ABS profile as the single-leg articles',
        'insert_families': ['PSM Sonic-Lok SL-B-M4-4.8',
                            'PSM Sonic-Lok SL-B-M4-5.8'],
        'stations': measured,
        'selection_rule': ('smallest pocket that accepts a perpendicular '
                           'heat-set without splitting and resists hand '
                           'spin/pull after cooling'),
        'orientation': oriented,
    }
    manifest_path = os.path.join(INSERT_FIT_DIR,
                                 'm4_insert_coupon_manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as stream:
        json.dump(manifest, stream, indent=2, sort_keys=True)
        stream.write('\n')
    occ.deleteMe()
    R.replace_cart_stops()
    print(json.dumps({'manifest': manifest_path, 'coupon': manifest},
                     indent=2, sort_keys=True))
    return manifest


def export_heatset_receiver_release_articles():
    """Export corrected active receivers and their mating cable cover.

    The physical Ø19.10 proximal link is intentionally absent: its five M3
    pockets are already correct, so regenerating it would create a needless
    reprint.  The wheel hub is exported now but remains procurement-gated on
    the specified short M4 insert.
    """
    problems = R.check8_threaded_receivers()
    if problems:
        raise RuntimeError('threaded-receiver release audit failed: %s' % problems)

    stand = B.find_occ('RIG_Stand')
    wheel = B.find_occ('Wheel_Hub_L')
    plate = B.find_occ('Chassis_Shoulder_Plate_L')
    cover = B.find_occ('Shoulder_Cable_Cover_L')
    if any(item is None for item in (stand, wheel, plate, cover)):
        raise RuntimeError('stand, wheel hub, shoulder plate and cover required')

    os.makedirs(STL_DIR, exist_ok=True)
    os.makedirs(os.path.join(STL_DIR, 'reroute'), exist_ok=True)
    native = {
        'RIG_Stand': os.path.join(STL_DIR, 'RIG_Stand.stl'),
        'Wheel_Hub_L': os.path.join(STL_DIR, 'reroute', 'Wheel_Hub_L.stl'),
    }
    for name, path in native.items():
        _stl(B.find_occ(name), path)

    stand_oriented = _export_max_y_face_down(
        stand, 'ABS_FA_RIG_Stand_M3_INSERTS_PRINT_ORIENTED',
        FIRST_ARTICLE_DIR,
        ('No supports. The mount face is the bed datum; all five M3 insert '
         'pockets are vertical and the Y thickness only decreases away from '
         'the bed. Requires a bed with at least 300 mm in one axis.'))
    wheel_oriented = _export_max_y_face_down(
        wheel, 'ABS_FA_Wheel_Hub_L_M4_INSERTS_PRINT_ORIENTED',
        ABS_ASSEMBLY_DIR,
        ('No supports. The rim mating face is the bed datum; six M4 insert '
         'bores and all motor holes are vertical, and the Ø37.3 register '
         'pocket faces upward.'))
    plate_oriented = _export_min_y_face_down(
        plate, 'ABS_FA_Chassis_Shoulder_Plate_L_M3_INSERTS_PRINT_ORIENTED',
        ABS_ASSEMBLY_DIR,
        ('No supports. The full inboard panel face is the bed datum; the four '
         'M3 cable-cover insert bores and all clearance holes are vertical. '
         'Install cable-cover inserts from the opposite, outboard face.'))
    cover_oriented = _export_max_y_face_down(
        cover, 'ABS_FA_Shoulder_Cable_Cover_L_CLEARANCE_PRINT_ORIENTED',
        ABS_ASSEMBLY_DIR,
        ('No supports. The broad outboard annulus is the bed datum; all four '
         'M3 clearance holes are vertical. This removable part has no inserts.'))
    # Fusion can re-evaluate transform-placed cartridge stop bodies after the
    # temporary orientation components are deleted.  Restore those known
    # transforms before the guarded transient shoulder build asserts them.
    R.replace_cart_stops()
    shoulder = export_abs_shoulder_hub_first_article(pin_bore_d=4.15)

    manifest = {
        'document': adsk.core.Application.get().activeDocument.name,
        'material_scope': ('ABS complete single-leg integration article; '
                           'PA-CF deferred to the two-leg build'),
        'physical_coupon_gates': {
            'M3': ('existing Ø4.0 ABS pocket coupon with the exact '
                   'owner-supplied Voron-style insert'),
            'M4': os.path.join(
                INSERT_FIT_DIR,
                'ABS_CAL_PSM_SL_M4_INSERT_POCKET_LADDER_PRINT_ORIENTED.stl'),
        },
        'RIG_Stand': {
            'receiver': '5 x owner-supplied Voron-style M3 x 5.0',
            'hole': 'Ø4.0 x 6.0 blind, 6.0 mm printed floor',
            'native_stl': native['RIG_Stand'],
            'print_oriented': stand_oriented,
        },
        'Wheel_Hub_L': {
            'receiver': '6 x PSM Sonic-Lok SL-B-M4-4.8 (not currently owned)',
            'hole': 'Ø5.6 through the 6.0 mm hub',
            'fastener': '6 x M4 x 8 SHCS through the 4.0 mm rim web',
            'thread_engagement_mm': 4.0,
            'screw_clearance_to_motor_face_mm': 2.0,
            'native_stl': native['Wheel_Hub_L'],
            'print_oriented': wheel_oriented,
        },
        'Chassis_Shoulder_Plate_L': {
            'receiver': '4 x owner-supplied Voron-style M3 x 5.0',
            'hole': 'Ø4.0 through the 5.0 mm plate',
            'fastener': ('4 x M3 x 10 SHCS, installed from the accessible '
                         'outboard cable-cover face'),
            'thread_engagement_mm': 3.5,
            'screw_clearance_to_inboard_face_mm': 1.5,
            'print_oriented': plate_oriented,
        },
        'Shoulder_Cable_Cover_L': {
            'receiver': 'none; clearance part',
            'hole': '4 x Ø3.4 through',
            'print_oriented': cover_oriented,
        },
        'Shoulder_Output_Hub_L': shoulder,
        'reprint_decision': {
            'required': ['ABS_FA_Shoulder_Output_Hub_L_D4p15'],
            'retain': ['physical ABS Proximal_Link_L D19.10 with bearings'],
            'not_previously_printed_use_new_files': [
                'RIG_Stand', 'Wheel_Hub_L', 'Chassis_Shoulder_Plate_L',
                'Shoulder_Cable_Cover_L'],
        },
    }
    with open(HEATSET_RELEASE_MANIFEST, 'w', encoding='utf-8') as stream:
        json.dump(manifest, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'manifest': HEATSET_RELEASE_MANIFEST,
                      'release': manifest}, indent=2, sort_keys=True))
    return manifest
