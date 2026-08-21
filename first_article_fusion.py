"""Fusion builders and exports for the ABS actuator-fit coupon set.

This module is executed *inside Fusion* through the Fusion MCP.  It deliberately
does not open, save, or close documents itself.  The caller must activate
``Beni_Prototype1_TestGauges``, run :func:`build_all`, inspect the returned
manifest, and only then save the cloud document.

All public dimensions are millimetres.  Coupons are modelled flat in Fusion's
XY plane with thickness in +Z, so their exported STLs arrive print-ready without
reorientation.  They reproduce the dimensions of the actual mating parts, not
extra clearance invented for a gauge.
"""

import json
import math
import os

import adsk.core
import adsk.fusion


WORKSPACE = '/Users/neilchulani/Robots/Biped'
OUT_DIR = os.path.join(WORKSPACE, 'first_article_stl', 'actuator_fit')
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


def _new_component(root, name, x_mm):
    transform = adsk.core.Matrix3D.create()
    transform.translation = adsk.core.Vector3D.create(_cm(x_mm), 0, 0)
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


def _build_one(root, name, spec, x_mm):
    _drop_occurrence(root, name)
    occ = _new_component(root, name, x_mm)
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


def _cylinder_diameters(body):
    values = []
    for face in body.faces:
        cyl = adsk.core.Cylinder.cast(face.geometry)
        if cyl is not None:
            values.append(round(cyl.radius * 20.0, 4))
    values.sort()
    return values


def _measure(occ):
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
