"""Build and release the ABS ordered-pin fit ladders through Fusion MCP.

The ladders are generated in a temporary unsaved Fusion document so the saved
``Beni_SingleLegRig`` assembly is never polluted by diagnostic geometry.  Both
coupons print with their pin axes bed-normal, matching the released hub and
link orientations.  The real ordered pins are the go/no-go gauges; no measured
pin diameter is required.
"""

import json
import os

import adsk.core

import beni_lib as B
import rig_lib as R
import rig_export as E
import mechanical_spring_test_fusion as M


ROOT = os.path.dirname(os.path.realpath(__file__))
OUT_DIR = os.path.join(ROOT, 'first_article_stl', 'ordered_pin_fit')
EVIDENCE_DIR = os.path.join(
    ROOT, 'evidence', 'assembly', '2026-09-22_ordered_pin_fit_ladders')

ROOT_NAME = 'ABS_CAL_D4x10_ROOT_BLIND_SOCKET_LADDER'
ROOT_EXPORT = ROOT_NAME + '_PRINT_ORIENTED'
ROOT_TRIALS = (4.05, 4.10, 4.15, 4.20, 4.25)
ROOT_THICKNESS = 8.0
ROOT_SOCKET_DEPTH = 5.0

CLEVIS_NAME = 'ABS_CAL_M4x40_CLEVIS_LINK_LAND_LADDER'
CLEVIS_EXPORT = CLEVIS_NAME + '_PRINT_ORIENTED'
CLEVIS_TRIALS = (4.15, 4.20, 4.25, 4.30, 4.35)
# Fusion inspection of v28 found the restrictive link lands are 5.0, 5.8,
# 8.2 and 9.0 mm long.  The cartridge eyes are already looser at Ø4.4 x 19 mm.
# Reproducing the worst 9.0 mm link land is therefore more faithful than a
# solid 34 mm tube: 34 mm is the retained stack, not continuous bore material.
CLEVIS_LAND_DEPTH = 9.0
CLEVIS_BOSS_D = 14.0

STATION_X = (-48.0, -24.0, 0.0, 24.0, 48.0)
MARKER_D = 2.0
MARKER_XZ = ((-67.0, -4.0), (-61.0, -4.0))


def _bodies(comp):
    return [comp.bRepBodies.item(index)
            for index in range(comp.bRepBodies.count)]


def _cut_circles(comp, y0, y1, rows):
    sketch = B.sk_on_y(comp, y0)
    for x, z, diameter in rows:
        B.circle(sketch, x, z, diameter)
    B.extrude(comp, B.profiles(sketch), y1 - y0, 'cut',
              participants=_bodies(comp))


def _build_root_ladder():
    B.drop_comp(ROOT_NAME)
    occurrence = B.new_comp(ROOT_NAME)
    comp = occurrence.component
    # The 8 mm solid and 5 mm blind depth exactly reproduce the hub flange's
    # root-dowel receiver, including its 3 mm closed floor/bridge.
    R.box(comp, -70.0, 60.0, 0.0, ROOT_THICKNESS, -10.0, 10.0)
    _cut_circles(
        comp, ROOT_THICKNESS, ROOT_THICKNESS - ROOT_SOCKET_DEPTH,
        [(x, 0.0, diameter)
         for x, diameter in zip(STATION_X, ROOT_TRIALS)])
    _cut_circles(
        comp, -0.25, ROOT_THICKNESS + 0.25,
        [(x, z, MARKER_D) for x, z in MARKER_XZ])
    comp.bRepBodies.item(0).name = ROOT_NAME
    return occurrence


def _build_clevis_ladder():
    B.drop_comp(CLEVIS_NAME)
    occurrence = B.new_comp(CLEVIS_NAME)
    comp = occurrence.component
    # A narrow full-height web joins five Ø14 stations.  The stations match
    # the actual integral clevis-boss diameter and the longest continuous link
    # land.  Their pin axes become vertical in the released print orientation.
    R.box(comp, -70.0, 60.0, 0.0, CLEVIS_LAND_DEPTH, -8.0, -4.0)
    R.box(comp, -70.0, -56.0, 0.0, CLEVIS_LAND_DEPTH, -8.0, 4.0,
          op='join', participants=_bodies(comp))
    for x in STATION_X:
        B.cyl_y(comp, None, x, 0.0, CLEVIS_BOSS_D,
                0.0, CLEVIS_LAND_DEPTH, 'join', _bodies(comp))
    _cut_circles(
        comp, -0.25, CLEVIS_LAND_DEPTH + 0.25,
        [(x, 0.0, diameter)
         for x, diameter in zip(STATION_X, CLEVIS_TRIALS)] +
        [(x, z, MARKER_D) for x, z in MARKER_XZ])
    comp.bRepBodies.item(0).name = CLEVIS_NAME
    return occurrence


def _cylinders(occurrence):
    rows = []
    body = occurrence.component.bRepBodies.item(0)
    for index in range(body.faces.count):
        face = body.faces.item(index)
        cylinder = adsk.core.Cylinder.cast(face.geometry)
        if cylinder is None or abs(cylinder.axis.y) < 0.999999:
            continue
        box = face.boundingBox
        rows.append({
            'diameter_mm': round(cylinder.radius * 20.0, 4),
            'y_span_mm': [round(box.minPoint.y * 10.0, 4),
                          round(box.maxPoint.y * 10.0, 4)],
        })
    return sorted(rows, key=lambda row: (row['diameter_mm'],
                                          row['y_span_mm']))


def _audit(occurrence, trials, trial_y_span, expected_bbox):
    topology = M._topology(occurrence)
    box = topology['bbox_mm']
    actual_bbox = [round(box[1] - box[0], 4),
                   round(box[3] - box[2], 4),
                   round(box[5] - box[4], 4)]
    assert all(abs(a - b) <= 0.001
               for a, b in zip(actual_bbox, expected_bbox)), (
                   actual_bbox, expected_bbox)
    cylinders = _cylinders(occurrence)
    for diameter in trials:
        matches = [row for row in cylinders
                   if abs(row['diameter_mm'] - diameter) <= 0.001]
        assert len(matches) == 1, (diameter, matches, cylinders)
        assert all(abs(a - b) <= 0.001
                   for a, b in zip(matches[0]['y_span_mm'], trial_y_span)), (
                       diameter, matches[0], trial_y_span)
    markers = [row for row in cylinders
               if abs(row['diameter_mm'] - MARKER_D) <= 0.001]
    assert len(markers) == 2, markers
    topology['dimensions_mm'] = actual_bbox
    topology['cylindrical_faces'] = cylinders
    return topology


def _capture_socket_face(occurrence, path):
    root = B.root()
    visibility = [(item, item.isLightBulbOn) for item in root.occurrences]
    try:
        for item, _was_on in visibility:
            item.isLightBulbOn = (item == occurrence)
        viewport = adsk.core.Application.get().activeViewport
        camera = viewport.camera
        camera.isSmoothTransition = False
        camera.isPerspective = False
        camera.eye = adsk.core.Point3D.create(-0.5, 15.0, 0.0)
        camera.target = adsk.core.Point3D.create(-0.5, 0.4, 0.0)
        camera.upVector = adsk.core.Vector3D.create(0.0, 0.0, 1.0)
        viewport.camera = camera
        viewport.fit()
        viewport.refresh()
        assert viewport.saveAsImageFile(path, 1600, 900)
    finally:
        for item, was_on in visibility:
            item.isLightBulbOn = was_on
    return path


def release(_context: str):
    app = adsk.core.Application.get()
    source_document = app.activeDocument
    assert source_document.name == 'Beni_SingleLegRig'
    source_was_modified = source_document.isModified
    source_version = source_document.dataFile.versionNumber
    R.ref_assert()
    R.placed_assert()
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(EVIDENCE_DIR, exist_ok=True)

    temporary_document = app.documents.add(
        adsk.core.DocumentTypes.FusionDesignDocumentType)
    try:
        root_ladder = _build_root_ladder()
        clevis_ladder = _build_clevis_ladder()
        topology = {
            ROOT_NAME: _audit(
                root_ladder, ROOT_TRIALS,
                [ROOT_THICKNESS - ROOT_SOCKET_DEPTH, ROOT_THICKNESS],
                [130.0, ROOT_THICKNESS, 20.0]),
            CLEVIS_NAME: _audit(
                clevis_ladder, CLEVIS_TRIALS,
                [0.0, CLEVIS_LAND_DEPTH],
                [130.0, CLEVIS_LAND_DEPTH, 15.0]),
        }
        root_socket_image = _capture_socket_face(
            root_ladder,
            os.path.join(OUT_DIR,
                         '01_fusion_' + ROOT_NAME + '_SOCKET_FACE.png'))

        exports = [
            E._export_max_y_face_down(
                root_ladder, ROOT_EXPORT, OUT_DIR,
                'Import unchanged. Broad socket-opening face on bed; pin '
                'axes vertical. No supports. Two Ø2 marker holes identify '
                'the Ø4.05 end.'),
            E._export_max_y_face_down(
                clevis_ladder, CLEVIS_EXPORT, OUT_DIR,
                'Import unchanged. Boss/web face on bed; 9 mm pin passages '
                'vertical. No supports; brim permitted. Two Ø2 marker holes '
                'identify the Ø4.15 end.'),
        ]
        meshes = {}
        for row in exports:
            meshes[row['export_name']] = M._verify_binary_stl(
                row['stl'], topology[row['source_part']]['volume_mm3'])

        manifest = {
            'source_document': source_document.name,
            'source_document_version': source_version,
            'generation_document': 'temporary unsaved Fusion design',
            'status': 'FUSION VERIFIED / DIAGNOSTIC PRINT RELEASE',
            'material_and_profile': ('ABS; same enclosed profile and exact '
                                     'orientation as the final parts'),
            'measurement_policy': ('Use the actual ordered pins as go/no-go '
                                   'gauges; no calipers or pin measurement.'),
            'root_dowel_ladder': {
                'hardware': 'one or more actual Ø4 x 10 cylindrical dowels',
                'trial_diameters_mm': list(ROOT_TRIALS),
                'station_centres_x_mm': list(STATION_X),
                'index': ('two Ø2 holes mark the Ø4.05 end; the closest '
                          'station is Ø4.05 and each station farther away '
                          'increases by 0.05 mm'),
                'receiver_depth_mm': ROOT_SOCKET_DEPTH,
                'closed_floor_mm': ROOT_THICKNESS - ROOT_SOCKET_DEPTH,
                'represents': ('shoulder-hub blind press socket; final link '
                               'slip socket remains deliberately looser'),
                'selection': ('start at Ø4.25 with an actual dowel and move '
                              'toward smaller stations using a fresh dowel as '
                              'needed; select the smallest station that starts '
                              'straight by hand, seats fully with gentle '
                              'smooth-jaw press pressure, stays retained when '
                              'inverted, and causes no whitening or split'),
                'socket_face_image': root_socket_image,
            },
            'clevis_ladder': {
                'hardware': 'one actual M4 x 40 single-hole clevis pin',
                'trial_diameters_mm': list(CLEVIS_TRIALS),
                'station_centres_x_mm': list(STATION_X),
                'index': ('two Ø2 holes mark the Ø4.15 end; the closest '
                          'station is Ø4.15 and each station farther away '
                          'increases by 0.05 mm'),
                'engagement_depth_mm': CLEVIS_LAND_DEPTH,
                'live_link_land_spans_mm': [5.0, 5.8, 8.2, 9.0],
                'cartridge_eye_bore_mm': [4.4, 19.0],
                'selection': ('start at Ø4.35 and move toward smaller '
                              'stations; select the smallest station the pin '
                              'crosses fully with fingertip pressure and '
                              'withdraws by hand without free radial rock'),
            },
            'excluded_D6x10_ladder': {
                'reason': ('the Ø6 x 10 stop pin is captured between a Ø6.2 '
                           'clearance socket and closed plate skin; fit does '
                           'not locate or retain the joint, so a ladder would '
                           'not improve the design'),
            },
            'topology': topology,
            'exports': exports,
            'mesh_verification': meshes,
        }
        for path in (os.path.join(OUT_DIR, 'fusion_manifest.json'),
                     os.path.join(EVIDENCE_DIR,
                                  'fusion_release_manifest.json')):
            with open(path, 'w', encoding='utf-8') as stream:
                json.dump(manifest, stream, indent=2, sort_keys=True)
                stream.write('\n')
    finally:
        temporary_document.close(False)

    source_document.activate()
    assert app.activeDocument == source_document
    assert source_document.isModified == source_was_modified
    R.ref_assert()
    R.placed_assert()
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return manifest
