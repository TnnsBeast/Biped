"""Fusion builders and exports for ABS fit calibration and assembly articles.

This module is executed *inside Fusion* through the Fusion MCP.  It deliberately
does not open, save, or close documents itself.  The caller must activate
``Beni_Prototype1_TestGauges``, run the relevant builder, and inspect the
returned manifest. Diagnostic coupons and first articles may be built and
exported transiently without saving them into the cloud document.

All public dimensions are millimetres.  Coupons are modelled flat in Fusion's
XY plane with thickness in +Z, so their exported STLs arrive print-ready without
reorientation.  The base coupons reproduce the dimensions of the actual mating
parts.  Any clearance-calibration variant is explicitly named and kept out of
the released structural dimensions until a physical result selects it.
"""

import json
import math
import os
import sys

import adsk.core
import adsk.fusion


WORKSPACE = '/Users/neilchulani/Robots/Biped'
OUT_DIR = os.path.join(WORKSPACE, 'first_article_stl', 'actuator_fit')
PIN_TRIAL_OUT_DIR = os.path.join(OUT_DIR, 'gim6010_pin_trials')
BEARING_TRIAL_OUT_DIR = os.path.join(
    WORKSPACE, 'first_article_stl', 'bearing_fit')
ASSEMBLY_DRY_FIT_OUT_DIR = os.path.join(
    WORKSPACE, 'first_article_stl', 'assembly_dry_fit')
DOCUMENT = 'Beni_Prototype1_TestGauges'

if WORKSPACE not in sys.path:
    sys.path.insert(0, WORKSPACE)
import beni_lib as B

COUPONS = {
    # Chassis_Shoulder_Plate_L interface: O48 rotating-face clearance and the
    # actual eight-hole angle from beni_lib.py, not a nominal clocking guess.
    'ABS_FIT_GIM6010_HOUSING': {
        'od': 84.0, 'thickness': 4.0, 'center_d': 48.0,
        'patterns': [(74.0, 3.4, 8, 22.6)],
        'interface': 'GIM6010-8 housing -> Chassis_Shoulder_Plate_L',
        'hardware': '8 x M3; use two opposite screws for first seating check',
    },
    # Shoulder_Output_Hub_L interface.  The O34 motor boss is explicitly not a
    # usable register; the three O4 pins and six M3 holes are the datum.
    'ABS_FIT_GIM6010_OUTPUT': {
        'od': 40.0, 'thickness': 4.0, 'center_d': 13.2,
        'patterns': [(25.0, 3.4, 6, 30.4), (20.4, 4.05, 3, 60.4)],
        'interface': 'GIM6010-8 output -> Shoulder_Output_Hub_L',
        'hardware': '6 x M3 plus 3 x O4 motor pins',
    },
    # Distal_Link_L interface: actual O41.5 driver-cover clearance and six
    # O2.8 printed clearances for the M2.5 housing screws.
    'ABS_FIT_GIM4305_HOUSING': {
        'od': 58.0, 'thickness': 4.0, 'center_d': 41.5,
        'patterns': [(47.5, 2.8, 6, 29.4)],
        'interface': 'GIM4305-10 housing -> Distal_Link_L',
        'hardware': '6 x M2.5; use two opposite screws for first seating check',
    },
    # Wheel_Hub_L interface: includes the actual printed O37.3 x 0.8 register
    # pocket, plus the three M3 holes.  Pocket is on the +Z (top) face.
    'ABS_FIT_GIM4305_OUTPUT': {
        'od': 44.0, 'thickness': 4.0, 'center_d': 12.0,
        'patterns': [(27.0, 3.4, 3, -28.7)],
        'pocket_d': 37.3, 'pocket_depth': 0.8,
        'interface': 'GIM4305-10 output -> Wheel_Hub_L',
        'hardware': '3 x M3; printed O37.3 x 0.8 register pocket',
    },
}


# ABS-only diagnostic series after the delivered GIM6010's three pins aligned
# with the O4.05 pattern but did not slide into it by hand.  O4.15 is already
# the project's printed slip-bore nominal for bought O4 pins.  The two finer
# steps above it are an experiment, not released structural dimensions.
GIM6010_PIN_TRIALS = (4.15, 4.20, 4.25)


# ABS-only diagnostic ladder after a real 6800-2RS bearing would start in the
# released O19.00 fit coupon only under table/clamp force.  These are trial
# bores, not released structural dimensions.  The 0.05 mm steps bracket the
# expected printer hole compensation without jumping straight to a loose seat.
BEARING_6800_TRIALS = (19.05, 19.10, 19.15, 19.20, 19.25)
BEARING_LADDER_NAME = 'ABS_CAL_6800_BORE_LADDER'
BEARING_LADDER_LENGTH = 170.0
BEARING_LADDER_WIDTH = 32.0
BEARING_LADDER_THICKNESS = 4.0
ABS_PROXIMAL_NAME = 'ABS_FA_Proximal_Link_L_D19p10'
ABS_PROXIMAL_PRINT_NAME = ABS_PROXIMAL_NAME + '_PRINT_ORIENTED'


def _pin_trial_name(pin_d):
    return 'ABS_CAL_GIM6010_OUTPUT_PIN_D' + ('%.2f' % pin_d).replace('.', 'p')


def _pin_trial_spec(pin_d):
    spec = dict(COUPONS['ABS_FIT_GIM6010_OUTPUT'])
    spec['patterns'] = [(25.0, 3.4, 6, 30.4),
                        (20.4, pin_d, 3, 60.4)]
    spec['interface'] = ('ABS-only GIM6010 output-pin clearance calibration; '
                         'not a structural release dimension')
    spec['hardware'] = ('6 x M3 plus 3 x O4 motor pins; trial bore O%.2f' %
                        pin_d)
    spec['pin_trial_d'] = pin_d
    return spec


def _bearing_ladder_spec():
    return {
        'length': BEARING_LADDER_LENGTH,
        'width': BEARING_LADDER_WIDTH,
        'thickness': BEARING_LADDER_THICKNESS,
        'trial_bores': list(BEARING_6800_TRIALS),
        'trial_centers_x': [-64.0, -32.0, 0.0, 32.0, 64.0],
        'index_holes': [(-79.0, -10.0, 3.0), (-79.0, 10.0, 3.0)],
        'interface': ('ABS-only 6800-2RS bearing-bore calibration; '
                      'not a structural release dimension'),
        'orientation': ('two O3 index holes mark the O19.05 end; bores increase '
                        'left-to-right: 19.05, 19.10, 19.15, 19.20, 19.25 mm'),
        'hardware': 'one real 6800-2RS bearing, O19 x 5 mm',
    }


def _cm(mm):
    return mm / 10.0


def _app_design_root():
    app = adsk.core.Application.get()
    doc = app.activeDocument
    if doc is None or doc.name != DOCUMENT:
        raise RuntimeError('activate %s before building coupons; active=%r' %
                           (DOCUMENT, None if doc is None else doc.name))
    design = adsk.fusion.Design.cast(app.activeProduct)
    if design is None:
        raise RuntimeError('active product is not a Fusion design')
    return app, doc, design, design.rootComponent


def _drop_occurrence(root, component_name):
    for i in range(root.occurrences.count - 1, -1, -1):
        occ = root.occurrences.item(i)
        if occ.component.name == component_name:
            occ.deleteMe()


def _new_component(root, name, x_mm, y_mm=0.0):
    transform = adsk.core.Matrix3D.create()
    transform.translation = adsk.core.Vector3D.create(
        _cm(x_mm), _cm(y_mm), 0)
    occ = root.occurrences.addNewComponent(transform)
    occ.component.name = name
    return occ


def _circle(sketch, x_mm, y_mm, diameter_mm):
    return sketch.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(_cm(x_mm), _cm(y_mm), 0),
        _cm(diameter_mm / 2.0))


def _all_profiles(sketch):
    collection = adsk.core.ObjectCollection.create()
    for i in range(sketch.profiles.count):
        collection.add(sketch.profiles.item(i))
    return collection


def _extrude(comp, profiles, distance_mm, operation):
    return comp.features.extrudeFeatures.addSimple(
        profiles,
        adsk.core.ValueInput.createByReal(_cm(distance_mm)),
        operation)


def _cut_circles(comp, center_d, patterns, thickness):
    # Keep every cut in its own sketch.  A single sketch containing all of the
    # circles also contains the large plate-minus-holes profile; blindly
    # extruding every profile would delete the entire coupon.
    circles = [(0.0, 0.0, center_d)]
    for pcd, hole_d, count, start_deg in patterns:
        radius = pcd / 2.0
        for i in range(count):
            angle = math.radians(start_deg + 360.0 * i / count)
            circles.append((radius * math.cos(angle),
                            radius * math.sin(angle), hole_d))
    for x_mm, y_mm, diameter_mm in circles:
        sketch = comp.sketches.add(comp.xYConstructionPlane)
        _circle(sketch, x_mm, y_mm, diameter_mm)
        _extrude(comp, sketch.profiles.item(0), thickness + 0.5,
                 adsk.fusion.FeatureOperations.CutFeatureOperation)


def _cut_top_pocket(comp, diameter, depth, thickness):
    planes = comp.constructionPlanes
    plane_input = planes.createInput()
    plane_input.setByOffset(
        comp.xYConstructionPlane,
        adsk.core.ValueInput.createByReal(_cm(thickness)))
    plane = planes.add(plane_input)
    sketch = comp.sketches.add(plane)
    _circle(sketch, 0, 0, diameter)
    _extrude(comp, sketch.profiles.item(0), -depth,
             adsk.fusion.FeatureOperations.CutFeatureOperation)


def _build_one(root, name, spec, x_mm, y_mm=0.0):
    _drop_occurrence(root, name)
    occ = _new_component(root, name, x_mm, y_mm)
    comp = occ.component

    sketch = comp.sketches.add(comp.xYConstructionPlane)
    _circle(sketch, 0, 0, spec['od'])
    feature = _extrude(comp, sketch.profiles.item(0), spec['thickness'],
                       adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body = feature.bodies.item(0)
    body.name = name

    _cut_circles(comp, spec['center_d'], spec['patterns'], spec['thickness'])
    if 'pocket_d' in spec:
        _cut_top_pocket(comp, spec['pocket_d'], spec['pocket_depth'],
                        spec['thickness'])

    comp.attributes.add('BeniFirstArticle', 'spec',
                        json.dumps(spec, sort_keys=True))
    return occ


def _build_6800_bore_ladder(root, x_mm=0.0, y_mm=-70.0):
    """Build one indexed plate containing five removable 6800 bore trials."""
    spec = _bearing_ladder_spec()
    _drop_occurrence(root, BEARING_LADDER_NAME)
    occ = _new_component(root, BEARING_LADDER_NAME, x_mm, y_mm)
    comp = occ.component

    sketch = comp.sketches.add(comp.xYConstructionPlane)
    half_l = spec['length'] / 2.0
    half_w = spec['width'] / 2.0
    sketch.sketchCurves.sketchLines.addTwoPointRectangle(
        adsk.core.Point3D.create(_cm(-half_l), _cm(-half_w), 0),
        adsk.core.Point3D.create(_cm(half_l), _cm(half_w), 0))
    feature = _extrude(comp, sketch.profiles.item(0), spec['thickness'],
                       adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body = feature.bodies.item(0)
    body.name = BEARING_LADDER_NAME

    for x_center, bore_d in zip(spec['trial_centers_x'],
                                spec['trial_bores']):
        hole_sketch = comp.sketches.add(comp.xYConstructionPlane)
        _circle(hole_sketch, x_center, 0.0, bore_d)
        _extrude(comp, hole_sketch.profiles.item(0),
                 spec['thickness'] + 0.5,
                 adsk.fusion.FeatureOperations.CutFeatureOperation)
    for x_center, y_center, bore_d in spec['index_holes']:
        hole_sketch = comp.sketches.add(comp.xYConstructionPlane)
        _circle(hole_sketch, x_center, y_center, bore_d)
        _extrude(comp, hole_sketch.profiles.item(0),
                 spec['thickness'] + 0.5,
                 adsk.fusion.FeatureOperations.CutFeatureOperation)

    comp.attributes.add('BeniFirstArticle', 'spec',
                        json.dumps(spec, sort_keys=True))
    return occ


def _cylinder_diameters(body):
    values = []
    for face in body.faces:
        cyl = adsk.core.Cylinder.cast(face.geometry)
        if cyl is not None:
            values.append(round(cyl.radius * 20.0, 4))
    values.sort()
    return values


def _measure(occ, spec=None):
    comp = occ.component
    if comp.bRepBodies.count != 1:
        raise RuntimeError('%s has %d bodies, expected 1' %
                           (comp.name, comp.bRepBodies.count))
    body = comp.bRepBodies.item(0)
    if not body.isSolid:
        raise RuntimeError('%s body is not solid' % comp.name)
    bb = body.boundingBox
    size = [round((bb.maxPoint.x - bb.minPoint.x) * 10.0, 4),
            round((bb.maxPoint.y - bb.minPoint.y) * 10.0, 4),
            round((bb.maxPoint.z - bb.minPoint.z) * 10.0, 4)]
    if spec is None:
        spec = COUPONS[comp.name]
    expected = [spec['od'], spec['od'], spec['thickness']]
    if any(abs(a - b) > 0.001 for a, b in zip(size, expected)):
        raise RuntimeError('%s bbox %r != expected %r' %
                           (comp.name, size, expected))
    return {
        'name': comp.name,
        'interface': spec['interface'],
        'hardware': spec['hardware'],
        'bbox_mm': size,
        'volume_cm3': round(body.volume, 4),
        'cylindrical_face_diameters_mm': _cylinder_diameters(body),
        'spec': spec,
    }


def _measure_6800_bore_ladder(occ, spec=None):
    if spec is None:
        spec = _bearing_ladder_spec()
    comp = occ.component
    if comp.bRepBodies.count != 1:
        raise RuntimeError('%s has %d bodies, expected 1' %
                           (comp.name, comp.bRepBodies.count))
    body = comp.bRepBodies.item(0)
    if not body.isSolid:
        raise RuntimeError('%s body is not solid' % comp.name)
    bb = body.boundingBox
    size = [round((bb.maxPoint.x - bb.minPoint.x) * 10.0, 4),
            round((bb.maxPoint.y - bb.minPoint.y) * 10.0, 4),
            round((bb.maxPoint.z - bb.minPoint.z) * 10.0, 4)]
    expected = [spec['length'], spec['width'], spec['thickness']]
    if any(abs(a - b) > 0.001 for a, b in zip(size, expected)):
        raise RuntimeError('%s bbox %r != expected %r' %
                           (comp.name, size, expected))
    cylinders = _cylinder_diameters(body)
    for diameter in list(spec['trial_bores']) + [3.0, 3.0]:
        if not any(abs(actual - diameter) <= 0.001 for actual in cylinders):
            raise RuntimeError('%s missing O%.2f cylindrical face; got %r' %
                               (comp.name, diameter, cylinders))
    return {
        'name': comp.name,
        'interface': spec['interface'],
        'hardware': spec['hardware'],
        'orientation': spec['orientation'],
        'bbox_mm': size,
        'volume_cm3': round(body.volume, 4),
        'cylindrical_face_diameters_mm': cylinders,
        'spec': spec,
    }


def _measure_abs_proximal(occ):
    comp = occ.component
    if comp.bRepBodies.count != 1:
        raise RuntimeError('%s has %d bodies, expected 1' %
                           (comp.name, comp.bRepBodies.count))
    body = comp.bRepBodies.item(0)
    if not body.isSolid:
        raise RuntimeError('%s body is not solid' % comp.name)
    cylinders = _cylinder_diameters(body)
    seat_count = sum(abs(value - B.ABS_KNEE_BRG_SEAT_D) <= 0.001
                     for value in cylinders)
    if seat_count != 2:
        raise RuntimeError('%s has %d O%.2f bearing-seat faces, expected 2; %r' %
                           (comp.name, seat_count,
                            B.ABS_KNEE_BRG_SEAT_D, cylinders))
    bb = body.boundingBox
    return {
        'name': comp.name,
        'bearing_hardware_od_mm': B.KNEE_BRG_OD,
        'abs_bearing_seat_d_mm': B.ABS_KNEE_BRG_SEAT_D,
        'bearing_seat_depth_mm': B.KNEE_BRG_W,
        'retaining_lip_opening_d_mm': B.KNEE_LIP_D,
        'bbox_mm': [
            round((bb.maxPoint.x - bb.minPoint.x) * 10.0, 4),
            round((bb.maxPoint.y - bb.minPoint.y) * 10.0, 4),
            round((bb.maxPoint.z - bb.minPoint.z) * 10.0, 4),
        ],
        'volume_cm3': round(body.volume, 4),
        'bearing_seat_face_count': seat_count,
        'cylindrical_face_diameters_mm': cylinders,
    }


def _bearing_path_occurrence(root, name, y0_mm):
    _drop_occurrence(root, name)
    occ = B.new_comp(name)
    comp = occ.component
    feature = B.ring(comp, y0_mm, B.KNEE_AXLE_D / 2.0,
                     B.KNEE_BRG_OD / 2.0, B.KNEE_BRG_W,
                     'new', cx=B.KX, cz=B.KZ)
    feature.bodies.item(0).name = name
    return occ


def _interference_mm3(design, occ_a, occ_b):
    entities = adsk.core.ObjectCollection.create()
    entities.add(occ_a)
    entities.add(occ_b)
    test_input = design.createInterferenceInput(entities)
    test_input.areCoincidentFacesIncluded = False
    results = design.analyzeInterference(test_input)
    return round(sum(results.item(i).interferenceBody.volume * 1000.0
                     for i in range(results.count)), 6)


def _set_y_offset(occ, offset_mm):
    transform = adsk.core.Matrix3D.create()
    transform.translation = adsk.core.Vector3D.create(0, _cm(offset_mm), 0)
    occ.transform2 = transform


def build_all():
    _app, doc, _design, root = _app_design_root()
    positions = [-135.0, -45.0, 45.0, 135.0]
    occurrences = []
    for (name, spec), x_mm in zip(COUPONS.items(), positions):
        occurrences.append(_build_one(root, name, spec, x_mm))
    manifest = [_measure(occ) for occ in occurrences]
    print(json.dumps({
        'document': doc.name,
        'document_modified': doc.isModified,
        'coupons': manifest,
    }, indent=2, sort_keys=True))
    return occurrences


def build_gim6010_pin_trials():
    """Build the three full-pattern ABS output-pin clearance trials."""
    _app, doc, _design, root = _app_design_root()
    positions = [-50.0, 0.0, 50.0]
    occurrences = []
    manifest = []
    for pin_d, x_mm in zip(GIM6010_PIN_TRIALS, positions):
        name = _pin_trial_name(pin_d)
        spec = _pin_trial_spec(pin_d)
        occ = _build_one(root, name, spec, x_mm, 70.0)
        occurrences.append(occ)
        manifest.append(_measure(occ, spec))
    print(json.dumps({
        'document': doc.name,
        'document_modified': doc.isModified,
        'purpose': 'ABS-only GIM6010 delivered-pin clearance calibration',
        'coupons': manifest,
    }, indent=2, sort_keys=True))
    return occurrences


def build_6800_bore_ladder():
    """Build the indexed ABS 6800 bearing-bore ladder."""
    _app, doc, _design, root = _app_design_root()
    occ = _build_6800_bore_ladder(root)
    manifest = _measure_6800_bore_ladder(occ)
    print(json.dumps({
        'document': doc.name,
        'document_modified': doc.isModified,
        'purpose': 'ABS-only 6800-2RS bearing-bore calibration',
        'coupon': manifest,
    }, indent=2, sort_keys=True))
    return occ


def build_abs_proximal_link():
    """Build the actual ABS proximal first article with the selected seat."""
    _app, doc, _design, root = _app_design_root()
    _drop_occurrence(root, ABS_PROXIMAL_NAME)
    occ = B.build_proximal_link(B.ABS_KNEE_BRG_SEAT_D)
    B.add_fillets(verbose=False)
    occ.component.name = ABS_PROXIMAL_NAME
    occ.component.bRepBodies.item(0).name = ABS_PROXIMAL_NAME
    row = _measure_abs_proximal(occ)
    print(json.dumps({
        'document': doc.name,
        'document_modified': doc.isModified,
        'purpose': 'unloaded ABS proximal-link physical assembly rehearsal',
        'component': row,
    }, indent=2, sort_keys=True))
    return occ


def verify_abs_proximal_bearing_paths():
    """Verify both bearing insertion paths and their reverse service paths."""
    _app, doc, design, root = _app_design_root()
    proximal = None
    for i in range(root.occurrences.count):
        candidate = root.occurrences.item(i)
        if candidate.component.name == ABS_PROXIMAL_NAME:
            proximal = candidate
            break
    if proximal is None:
        raise RuntimeError('missing %s' % ABS_PROXIMAL_NAME)

    paths = []
    cases = (
        ('inboard', 'ABS_PATH_BEARING_INBOARD', B.BRG1_Y0,
         (-12.0, -10.0, -8.0, -6.0, -4.0, -2.0, 0.0)),
        ('outboard', 'ABS_PATH_BEARING_OUTBOARD', B.BRG2_Y0,
         (12.0, 10.0, 8.0, 6.0, 4.0, 2.0, 0.0)),
    )
    for side, name, y0_mm, offsets in cases:
        bearing = _bearing_path_occurrence(root, name, y0_mm)
        samples = []
        for offset in offsets:
            _set_y_offset(bearing, offset)
            clash = _interference_mm3(design, proximal, bearing)
            samples.append({'offset_y_mm': offset,
                            'interference_mm3': clash})
            if clash > 0.001:
                raise RuntimeError('%s bearing path clashes at offset %.2f: '
                                   '%.6f mm3' % (side, offset, clash))
        paths.append({
            'side': side,
            'insertion_direction': '+Y' if side == 'inboard' else '-Y',
            'service_direction': '-Y' if side == 'inboard' else '+Y',
            'samples': samples,
            'max_interference_mm3': max(row['interference_mm3']
                                        for row in samples),
        })
        bearing.deleteMe()

    result = {
        'document': doc.name,
        'status': 'CAD PATH VERIFIED',
        'order': ('press bearings into the detached proximal link before the '
                  'distal link, axle, cartridge, stop arc, encoder, or cables'),
        'fastener_tool_access': ('no fastener is used for seating; press only '
                                 'on the bearing outer race from the open face'),
        'cable_path': 'no cable is present during the detached-link operation',
        'service_path': ('remove the proximal link, then reverse the same open-'
                         'face paths; an internal bearing puller may sacrifice '
                         'the bearing being replaced but no printed part'),
        'paths': paths,
    }
    os.makedirs(ASSEMBLY_DRY_FIT_OUT_DIR, exist_ok=True)
    verification_path = os.path.join(
        ASSEMBLY_DRY_FIT_OUT_DIR,
        'proximal_d19p10_path_verification.json')
    with open(verification_path, 'w', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write('\n')
    result['verification_file'] = verification_path
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def export_all():
    _app, doc, design, root = _app_design_root()
    os.makedirs(OUT_DIR, exist_ok=True)
    manager = design.exportManager
    exported = []
    for name in COUPONS:
        occ = None
        for i in range(root.occurrences.count):
            candidate = root.occurrences.item(i)
            if candidate.component.name == name:
                occ = candidate
                break
        if occ is None:
            raise RuntimeError('missing coupon component %s' % name)
        row = _measure(occ)
        path = os.path.join(OUT_DIR, name + '.stl')
        options = manager.createSTLExportOptions(occ.component, path)
        options.meshRefinement = (
            adsk.fusion.MeshRefinementSettings.MeshRefinementHigh)
        options.isBinaryFormat = True
        if not manager.execute(options):
            raise RuntimeError('STL export failed for %s' % name)
        row['stl'] = path
        row['stl_bytes'] = os.path.getsize(path)
        exported.append(row)

    manifest_path = os.path.join(OUT_DIR, 'fusion_manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as stream:
        json.dump({'document': doc.name, 'coupons': exported}, stream,
                  indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'exported': exported,
                      'manifest': manifest_path}, indent=2, sort_keys=True))
    return exported


def export_gim6010_pin_trials():
    """Export the three ABS pin trials after Fusion B-Rep validation."""
    _app, doc, design, root = _app_design_root()
    os.makedirs(PIN_TRIAL_OUT_DIR, exist_ok=True)
    manager = design.exportManager
    exported = []
    for pin_d in GIM6010_PIN_TRIALS:
        name = _pin_trial_name(pin_d)
        spec = _pin_trial_spec(pin_d)
        occ = None
        for i in range(root.occurrences.count):
            candidate = root.occurrences.item(i)
            if candidate.component.name == name:
                occ = candidate
                break
        if occ is None:
            raise RuntimeError('missing pin-trial component %s' % name)
        row = _measure(occ, spec)
        path = os.path.join(PIN_TRIAL_OUT_DIR, name + '.stl')
        options = manager.createSTLExportOptions(occ.component, path)
        options.meshRefinement = (
            adsk.fusion.MeshRefinementSettings.MeshRefinementHigh)
        options.isBinaryFormat = True
        if not manager.execute(options):
            raise RuntimeError('STL export failed for %s' % name)
        row['stl'] = path
        row['stl_bytes'] = os.path.getsize(path)
        exported.append(row)

    manifest_path = os.path.join(PIN_TRIAL_OUT_DIR,
                                 'fusion_manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as stream:
        json.dump({
            'document': doc.name,
            'purpose': 'ABS-only GIM6010 delivered-pin clearance calibration',
            'coupons': exported,
        }, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'exported': exported,
                      'manifest': manifest_path}, indent=2, sort_keys=True))
    return exported


def export_6800_bore_ladder():
    """Export the ABS bearing-bore ladder after Fusion B-Rep validation."""
    _app, doc, design, root = _app_design_root()
    os.makedirs(BEARING_TRIAL_OUT_DIR, exist_ok=True)
    occ = None
    for i in range(root.occurrences.count):
        candidate = root.occurrences.item(i)
        if candidate.component.name == BEARING_LADDER_NAME:
            occ = candidate
            break
    if occ is None:
        raise RuntimeError('missing bearing-bore ladder component %s' %
                           BEARING_LADDER_NAME)
    row = _measure_6800_bore_ladder(occ)
    path = os.path.join(BEARING_TRIAL_OUT_DIR,
                        BEARING_LADDER_NAME + '.stl')
    options = design.exportManager.createSTLExportOptions(occ.component, path)
    options.meshRefinement = (
        adsk.fusion.MeshRefinementSettings.MeshRefinementHigh)
    options.isBinaryFormat = True
    if not design.exportManager.execute(options):
        raise RuntimeError('STL export failed for %s' % BEARING_LADDER_NAME)
    row['stl'] = path
    row['stl_bytes'] = os.path.getsize(path)

    manifest_path = os.path.join(BEARING_TRIAL_OUT_DIR,
                                 'fusion_manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as stream:
        json.dump({
            'document': doc.name,
            'purpose': 'ABS-only 6800-2RS bearing-bore calibration',
            'coupon': row,
        }, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'exported': row,
                      'manifest': manifest_path}, indent=2, sort_keys=True))
    return row


def export_abs_proximal_link():
    """Export the Fusion-verified ABS proximal first article."""
    _app, doc, design, root = _app_design_root()
    os.makedirs(ASSEMBLY_DRY_FIT_OUT_DIR, exist_ok=True)
    occ = None
    for i in range(root.occurrences.count):
        candidate = root.occurrences.item(i)
        if candidate.component.name == ABS_PROXIMAL_NAME:
            occ = candidate
            break
    if occ is None:
        raise RuntimeError('missing %s' % ABS_PROXIMAL_NAME)
    row = _measure_abs_proximal(occ)
    path = os.path.join(ASSEMBLY_DRY_FIT_OUT_DIR,
                        ABS_PROXIMAL_NAME + '.stl')
    options = design.exportManager.createSTLExportOptions(occ.component, path)
    options.meshRefinement = (
        adsk.fusion.MeshRefinementSettings.MeshRefinementHigh)
    options.isBinaryFormat = True
    if not design.exportManager.execute(options):
        raise RuntimeError('STL export failed for %s' % ABS_PROXIMAL_NAME)
    row['stl'] = path
    row['stl_bytes'] = os.path.getsize(path)

    manifest_path = os.path.join(ASSEMBLY_DRY_FIT_OUT_DIR,
                                 'proximal_d19p10_fusion_manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as stream:
        json.dump({
            'document': doc.name,
            'purpose': 'unloaded ABS proximal-link physical assembly rehearsal',
            'component': row,
        }, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'exported': row,
                      'manifest': manifest_path}, indent=2, sort_keys=True))
    return row


def _abs_proximal_print_transform(occ):
    """Return the exact Fusion transform for the largest supporting side face.

    The proximal link is modelled in assembly coordinates.  Its native STL has
    no useful XY-bed datum, even though the solid has a large planar tangent
    face.  Restrict the search to side faces (normal Y ~= 0), require the face
    plane to support the entire solid, then put the largest qualifying face on
    Z=0.  This preserves the one-piece link and keeps the fork channel open
    sideways without adding sacrificial geometry.
    """
    comp = occ.component
    if comp.bRepBodies.count != 1:
        raise RuntimeError('%s has %d bodies, expected 1' %
                           (comp.name, comp.bRepBodies.count))
    body = comp.bRepBodies.item(0)
    temporary = adsk.fusion.TemporaryBRepManager.get()
    candidates = []
    for i in range(body.faces.count):
        face = body.faces.item(i)
        if adsk.core.Plane.cast(face.geometry) is None:
            continue
        ok, normal = face.evaluator.getNormalAtPoint(face.pointOnFace)
        if not ok or abs(normal.y) > 1e-6:
            continue
        angle = math.atan2(normal.x, -normal.z)
        rotation = adsk.core.Matrix3D.create()
        rotation.setToRotation(
            angle, adsk.core.Vector3D.create(0, 1, 0),
            adsk.core.Point3D.create(0, 0, 0))
        trial_body = temporary.copy(body)
        if not temporary.transform(trial_body, rotation):
            raise RuntimeError('Fusion candidate transform failed for face %d' %
                               i)
        point = face.pointOnFace
        cosine, sine = math.cos(angle), math.sin(angle)
        face_z = -sine * point.x + cosine * point.z
        min_z = trial_body.boundingBox.minPoint.z
        # Exact B-Rep bounding boxes include circular extrema that a vertex-only
        # test misses.  The old pseudo-tangent failed here by 0.608 mm.
        if abs(face_z - min_z) <= 0.001:  # 0.01 mm
            candidates.append((face.area, i, normal, angle, trial_body))
    if not candidates:
        raise RuntimeError('%s has no supporting planar side face' % comp.name)
    area_cm2, face_index, normal, angle, trial_body = max(
        candidates, key=lambda row: row[0])
    trial_bb = trial_body.boundingBox
    min_z = trial_bb.minPoint.z
    matrix = adsk.core.Matrix3D.create()
    matrix.setToRotation(angle, adsk.core.Vector3D.create(0, 1, 0),
                         adsk.core.Point3D.create(0, 0, 0))
    matrix.translation = adsk.core.Vector3D.create(0, 0, -min_z)
    return matrix, {
        'method': 'largest Fusion-verified supporting planar side face',
        'rotation_axis': '+Y',
        'rotation_deg': round(math.degrees(angle), 6),
        'support_face_index': face_index,
        'support_face_area_mm2': round(area_cm2 * 100.0, 3),
        'support_face_normal_native': [round(normal.x, 8),
                                       round(normal.y, 8),
                                       round(normal.z, 8)],
        'oriented_bbox_mm': [
            round((trial_bb.maxPoint.x - trial_bb.minPoint.x) * 10.0, 4),
            round((trial_bb.maxPoint.y - trial_bb.minPoint.y) * 10.0, 4),
            round((trial_bb.maxPoint.z - trial_bb.minPoint.z) * 10.0, 4),
        ],
        'minimum_z_mm': 0.0,
        'channel': 'open sideways; no trapped internal support',
    }


def export_abs_proximal_link_print_oriented():
    """Export a bed-ready occurrence without changing assembly geometry."""
    app, doc, design, root = _app_design_root()
    os.makedirs(ASSEMBLY_DRY_FIT_OUT_DIR, exist_ok=True)
    occ = None
    for i in range(root.occurrences.count):
        candidate = root.occurrences.item(i)
        if candidate.component.name == ABS_PROXIMAL_NAME:
            occ = candidate
            break
    if occ is None:
        raise RuntimeError('missing %s' % ABS_PROXIMAL_NAME)

    row = _measure_abs_proximal(occ)
    transform, orientation = _abs_proximal_print_transform(occ)
    _drop_occurrence(root, ABS_PROXIMAL_PRINT_NAME)
    print_occ = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    print_occ.component.name = ABS_PROXIMAL_PRINT_NAME
    temporary = adsk.fusion.TemporaryBRepManager.get()
    transformed_body = temporary.copy(occ.component.bRepBodies.item(0))
    if not temporary.transform(transformed_body, transform):
        raise RuntimeError('Fusion B-Rep transform failed for %s' %
                           ABS_PROXIMAL_PRINT_NAME)
    base_feature = print_occ.component.features.baseFeatures.add()
    base_feature.name = ABS_PROXIMAL_PRINT_NAME + '_FusionTransform'
    base_feature.startEdit()
    print_body = print_occ.component.bRepBodies.add(transformed_body,
                                                    base_feature)
    base_feature.finishEdit()
    if print_body is None or not print_body.isSolid:
        raise RuntimeError('Fusion could not create oriented solid %s' %
                           ABS_PROXIMAL_PRINT_NAME)
    print_body.name = ABS_PROXIMAL_PRINT_NAME
    visibility = [(root.occurrences.item(i),
                   root.occurrences.item(i).isLightBulbOn)
                  for i in range(root.occurrences.count)]
    try:
        for candidate, _was_visible in visibility:
            candidate.isLightBulbOn = candidate == print_occ
        app.activeViewport.fit()
        app.activeViewport.refresh()

        path = os.path.join(ASSEMBLY_DRY_FIT_OUT_DIR,
                            ABS_PROXIMAL_PRINT_NAME + '.stl')
        options = design.exportManager.createSTLExportOptions(
            print_occ.component, path)
        options.meshRefinement = (
            adsk.fusion.MeshRefinementSettings.MeshRefinementHigh)
        options.isBinaryFormat = True
        if not design.exportManager.execute(options):
            raise RuntimeError('STL export failed for %s' %
                               ABS_PROXIMAL_PRINT_NAME)

        image_path = os.path.join(
            ASSEMBLY_DRY_FIT_OUT_DIR,
            '00_fusion_abs_proximal_d19p10_print_oriented.png')
        if not app.activeViewport.saveAsImageFile(image_path, 1600, 1000):
            raise RuntimeError('Fusion screenshot failed for %s' %
                               ABS_PROXIMAL_PRINT_NAME)
    finally:
        for candidate, was_visible in visibility:
            if candidate != print_occ:
                candidate.isLightBulbOn = was_visible
        print_occ.deleteMe()
        app.activeViewport.fit()
        app.activeViewport.refresh()

    row['print_orientation'] = orientation
    row['stl'] = path
    row['stl_bytes'] = os.path.getsize(path)
    row['fusion_screenshot'] = image_path
    manifest_path = os.path.join(
        ASSEMBLY_DRY_FIT_OUT_DIR,
        'proximal_d19p10_print_orientation_manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as stream:
        json.dump({
            'document': doc.name,
            'purpose': ('bed-ready ABS proximal-link physical assembly '
                        'rehearsal; assembly geometry unchanged'),
            'component': row,
        }, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps({'exported': row, 'manifest': manifest_path},
                     indent=2, sort_keys=True))
    return row
