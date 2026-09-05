"""Run via Fusion MCP with Beni_SingleLegRig active; writes B-Rep evidence."""
import json
import math
import os
import sys

import adsk.core
import adsk.fusion

ROOT = '/Users/neilchulani/Robots/Biped'
OUT = os.path.join(ROOT, 'evidence/inserts/2026-09-04_m4_coupon_pass')
sys.path.insert(0, ROOT)
import beni_lib as B
import rig_lib as R


def run(_context: str):
    app = adsk.core.Application.get()
    assert app.activeDocument.name == 'Beni_SingleLegRig'
    R.ref_assert()
    R.placed_assert()
    saved = R.xf_capture()
    temporary = adsk.fusion.TemporaryBRepManager.get()

    def bodies(name):
        occ = B.find_occ(name)
        assert occ is not None, name
        return [temporary.copy(body) for child in R._occ_tree(occ)
                for body in child.bRepBodies]

    def intersection(a, b):
        aa, bb = a.boundingBox, b.boundingBox
        if any(getattr(aa.maxPoint, axis) <= getattr(bb.minPoint, axis) + 1e-8
               or getattr(bb.maxPoint, axis) <= getattr(aa.minPoint, axis) + 1e-8
               for axis in ('x', 'y', 'z')):
            return 0.0
        trial = temporary.copy(a)
        assert temporary.booleanOperation(
            trial, b, adsk.fusion.BooleanTypes.IntersectionBooleanType)
        return trial.volume * 1000.0

    def cylinder(x, z, diameter, y0, y1):
        return temporary.createCylinderOrCone(
            adsk.core.Point3D.create(x / 10, y0 / 10, z / 10), diameter / 20,
            adsk.core.Point3D.create(x / 10, y1 / 10, z / 10), diameter / 20)

    paths = []

    def path(label, moving, stationary, travel=40.0, step=0.5):
        maximum, worst = 0.0, None
        count = round(travel / step) + 1
        for index in range(count):
            offset = travel - index * step
            transform = adsk.core.Matrix3D.create()
            transform.translation = adsk.core.Vector3D.create(0, offset / 10, 0)
            volume = 0.0
            for body in moving:
                trial = temporary.copy(body)
                assert temporary.transform(trial, transform)
                volume += sum(intersection(trial, other) for other in stationary)
            if volume > maximum:
                maximum, worst = volume, offset
        row = {'path': label, 'direction': '-Y insertion / +Y removal',
               'start_offset_mm': travel, 'end_offset_mm': 0.0,
               'step_mm': step, 'sample_count': count,
               'max_interference_mm3': maximum, 'worst_offset_mm': worst}
        paths.append(row)
        print(json.dumps(row))
        return maximum

    transient = R.guarded(
        B.build_shoulder_hub, pin_bore_d=4.15,
        component_name='VERIFY_ABS_M4_D5p30_SHOULDER')
    try:
        sh = bodies('VERIFY_ABS_M4_D5p30_SHOULDER')
        plate = bodies('Chassis_Shoulder_Plate_L')
        cover = bodies('Shoulder_Cable_Cover_L')
        link = bodies('Proximal_Link_L')
        smotor = bodies('REF_GIM6010-8')
        wheel = bodies('Wheel_Hub_L')
        rim = bodies('Wheel_Rim_L')
        wmotor = bodies('REF_GIM4305-10')
        path('shoulder plate over bare rotor; hub absent', plate, smotor)
        path('ABS shoulder hub after plate; cover and link absent', sh, plate + smotor)
        path('cable cover; hub fitted and link absent', cover, sh + plate + smotor)
        path('supported proximal link onto assembled shoulder', link, sh + plate + cover + smotor)
        path('wheel hub onto detached wheel motor; rim absent', wheel, wmotor)
        path('wheel rim onto hub and detached wheel motor', rim, wheel + wmotor)

        tips = [cylinder(x, z, B.OWNED_M4_INSERT_D1,
                         B.WH_HUB_Y_B, B.WHEEL_INSERT_OUTBOARD_Y)
                for x, z in B._receiver_centres(B.WX, B.WZ, B.RIM_BOLT_PCD, 6, 0)]
        path('rim reliefs over the six projecting insert tips', rim, tips)

        # Sweep the actual CAD screw envelopes from their open outboard side.
        for family, surroundings in [
                ('HW_SHCS_M4x10', link + sh + plate + cover + smotor),
                ('HW_SHCS_M4x8', rim + wheel + wmotor)]:
            screws = [o for o in B.root().occurrences
                      if B.base_name(o.component.name) == family]
            assert len(screws) == 6, (family, len(screws))
            path(family + ' six screw insertion paths',
                 [temporary.copy(b) for o in screws for b in o.bRepBodies],
                 surroundings)

        # Driver access is separate from screw-head insertion. The M4 probe
        # is a Ø3.5 circular envelope; larger driver shanks are not covered.
        access = []
        for family, size, surroundings in [
                ('HW_SHCS_M4x10', 4.0, link + sh + plate + cover),
                ('HW_SHCS_M4x8', 4.0, rim + wheel),
                ('HW_SHCS_M3x10', 3.0, link + sh + plate + cover)]:
            screws = [o for o in B.root().occurrences
                      if B.base_name(o.component.name) == family]
            if family == 'HW_SHCS_M3x10':
                screws = [o for o in screws if abs(B.bbox_of(o)[3] - 53.5) < 0.01]
            probes = []
            for o in screws:
                bb = B.bbox_of(o)
                diameter = 3.5 if size == 4.0 else B.SHCS[size][0]
                probe = cylinder((bb[0] + bb[1]) / 2, (bb[4] + bb[5]) / 2,
                                 diameter, bb[3], bb[3] + 50.0)
                probes.append(sum(intersection(probe, b) for b in surroundings))
            access.append({'screw_family': family, 'probe_diameter_mm': diameter,
                           'count': len(probes), 'interference_mm3': probes})

        # All planar faces directed toward the bed are enumerated. Internal
        # ceilings need controlled bridging; a broad one-sided rim ledge fails.
        face_audit = {}
        for name in ['VERIFY_ABS_M4_D5p30_SHOULDER', 'Wheel_Hub_L',
                     'Wheel_Rim_L', 'Chassis_Shoulder_Plate_L',
                     'Shoulder_Cable_Cover_L', 'RIG_Stand']:
            body = B.find_occ(name).component.bRepBodies.item(0)
            sign = -1 if name == 'Chassis_Shoulder_Plate_L' else 1
            bed = body.boundingBox.maxPoint.y if sign == 1 else body.boundingBox.minPoint.y
            faces = []
            for index, face in enumerate(body.faces):
                if adsk.core.Plane.cast(face.geometry) is None:
                    continue
                ok, normal = face.evaluator.getNormalAtPoint(face.pointOnFace)
                assert ok
                if normal.y * sign > 0.999999:
                    faces.append({'face': index, 'y_mm': face.pointOnFace.y * 10,
                                  'height_above_bed_mm': (bed - face.pointOnFace.y) * sign * 10,
                                  'area_mm2': face.area * 100})
            face_audit[name] = faces

        report = {'document': app.activeDocument.name, 'source': 'Fusion MCP / exact B-Rep',
                  'paths': paths, 'driver_access': access, 'bed_facing_planar_faces': face_audit,
                  'cable_scope': 'detached, unplugged dry fits; route harness in open shoulder spiral before hub/link; complete wired article remains blocked by cable post A',
                  'wheel_rim_print_status': 'HOLD: y=72 annular underside from r=30 to r=44 is a 14 mm unsupported inward ledge; outer retaining flange also needs an overhang solution',
                  'shoulder_link_assembly_status': 'BLOCKED: two screw heads cannot follow the straight axial path; alternate loading path not verified. Retain the physical link pending a detached screw-loading rehearsal.',
                  'physical_rehearsal': 'required after printing; coupon pass is not subassembly acceptance'}
        with open(os.path.join(OUT, 'fusion_paths_and_print_audit.json'), 'w') as stream:
            json.dump(report, stream, indent=2)
            stream.write('\n')
        # Preserve the failed root-screw path as a blocker, not a passing path.
        assert all(p['max_interference_mm3'] < 0.01 for p in paths
                   if p['path'] != 'HW_SHCS_M4x10 six screw insertion paths'), paths
        assert all(v < 0.01 for row in access for v in row['interference_mm3']), access
    finally:
        transient.deleteMe()
        B.design().computeAll()
        adsk.doEvents()
        R.xf_restore(saved)
    R.ref_assert()
    R.placed_assert()
