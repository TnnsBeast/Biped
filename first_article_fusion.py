"""Fusion builders and exports for the ABS actuator-fit coupon sets.

This module is executed *inside Fusion* through the Fusion MCP.  It deliberately
does not open, save, or close documents itself.  The caller must activate
``Beni_Prototype1_TestGauges``, run :func:`build_all`, inspect the returned
manifest.  Diagnostic coupons may be built and exported transiently without
saving them into the cloud document.

All public dimensions are millimetres.  Coupons are modelled flat in Fusion's
XY plane with thickness in +Z, so their exported STLs arrive print-ready without
reorientation.  The base coupons reproduce the dimensions of the actual mating
parts.  Any clearance-calibration variant is explicitly named and kept out of
the released structural dimensions until a physical result selects it.
"""

import json
import math
import os

import adsk.core
import adsk.fusion


WORKSPACE = '/Users/neilchulani/Robots/Biped'
OUT_DIR = os.path.join(WORKSPACE, 'first_article_stl', 'actuator_fit')
PIN_TRIAL_OUT_DIR = os.path.join(OUT_DIR, 'gim6010_pin_trials')
BEARING_TRIAL_OUT_DIR = os.path.join(
    WORKSPACE, 'first_article_stl', 'bearing_fit')
DOCUMENT = 'Beni_Prototype1_TestGauges'

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
