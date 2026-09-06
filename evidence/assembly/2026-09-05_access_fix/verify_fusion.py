"""Exact solid-envelope assembly checks. Execute only through Fusion MCP."""
import json
import math
import os
import sys
import adsk.core
import adsk.fusion

ROOT = '/Users/neilchulani/Robots/Biped'
OUT = os.path.dirname(__file__)
sys.path.insert(0, ROOT)
import beni_lib as B
import rig_lib as R


def intersect(a, b):
    tm = adsk.fusion.TemporaryBRepManager.get()
    aa, bb = a.boundingBox, b.boundingBox
    if any(getattr(aa.maxPoint, v) <= getattr(bb.minPoint, v) + 1e-8 or
           getattr(bb.maxPoint, v) <= getattr(aa.minPoint, v) + 1e-8
           for v in ('x', 'y', 'z')):
        return 0.0
    trial = tm.copy(a)
    assert tm.booleanOperation(trial, b, adsk.fusion.BooleanTypes.IntersectionBooleanType)
    return trial.volume * 1000


def cylinder(x, z, d, y0, y1):
    return adsk.fusion.TemporaryBRepManager.get().createCylinderOrCone(
        adsk.core.Point3D.create(x / 10, y0 / 10, z / 10), d / 20,
        adsk.core.Point3D.create(x / 10, y1 / 10, z / 10), d / 20)


def receiver_access():
    # Probe diameters are design clearance envelopes, not measured iron tips.
    specs = [
        ('Shoulder_Output_Hub_L', B._receiver_centres(0, 0, B.HUB_LINK_PCD, 6, B.HUB_LINK_A0), 59.5, 1, 5.5),
        ('Wheel_Hub_L', B._receiver_centres(B.WX, B.WZ, B.RIM_BOLT_PCD, 6, 0), 94.5, -1, 5.5),
        ('Chassis_Shoulder_Plate_L', B._receiver_centres(0, 0, B.CABLE_COVER_PCD, 4, 45), B.SH_PLATE_Y1, 1, 5.5),
        ('Proximal_Link_L', [B.kpt(B.STOP_BOLT_R, a) for a in B.STOP_BOLT_A] + [B.kpt(15, a) for a in (60, 140)], 90.3, 1, 5.5),
    ]
    # Discover stand/frame receiver axes from the actual cylindrical faces.
    for name in ('RIG_Stand', 'Chassis_Frame'):
        occ = B.find_occ(name)
        if occ is None:
            continue
        groups = {}
        for face in occ.component.bRepBodies.item(0).faces:
            g = adsk.core.Cylinder.cast(face.geometry)
            if not g or abs(g.axis.y) < .999999 or abs(g.radius * 20 - 4) > .001:
                continue
            bb = face.boundingBox
            lo, hi = bb.minPoint.y * 10, bb.maxPoint.y * 10
            if abs(hi-lo-6) > .001:
                continue
            sign = 1 if hi > 0 else -1
            groups.setdefault((hi if sign == 1 else lo, sign), []).append((g.origin.x*10, g.origin.z*10))
        for (mouth, sign), centres in groups.items():
            specs.append((name, centres, mouth, sign, 5.5))
    rows = []
    for name, centres, mouth, sign, d in specs:
        occ = B.find_occ(name)
        bodies = list(occ.component.bRepBodies)
        volumes = [sum(intersect(cylinder(x,z,d,mouth+sign*.001,mouth+sign*30), b) for b in bodies) for x,z in centres]
        tm=adsk.fusion.TemporaryBRepManager.get()
        pocket_d=5.3 if name in ('Shoulder_Output_Hub_L','Wheel_Hub_L') else 4.0
        lands=[]
        for x,z in centres:
            land=cylinder(x,z,d,mouth-sign*.2,mouth)
            assert tm.booleanOperation(land,cylinder(x,z,pocket_d,mouth-sign*.2,mouth),adsk.fusion.BooleanTypes.DifferenceBooleanType)
            expected=land.volume*1000
            actual=sum(intersect(land,b) for b in bodies)
            lands.append(dict(expected_volume_mm3=expected,actual_volume_mm3=actual,supported_fraction=actual/expected))
        rows.append(dict(part=name, count=len(centres), mouth_y_mm=mouth,
                         direction_y=sign, clearance_probe_d_mm=d,
                         continuous_travel_mm=30, interference_mm3=volumes, mouth_lands=lands))
    return rows


def root_access(occ=None):
    body = (occ or B.find_occ('Proximal_Link_L')).component.bRepBodies.item(0)
    rows = []
    for i,(x,z) in enumerate(B._receiver_centres(0,0,B.HUB_LINK_PCD,6,B.HUB_LINK_A0)):
        # Continuous swept volume, from screw seat to 40 mm beyond the link.
        head = cylinder(x,z,7,63.3,134.3)
        shaft = cylinder(x,z,4,53.3,130.3)
        tool = cylinder(x,z,6,67.3,140.3)
        rows.append(dict(index=i, centre_xz_mm=[x,z],
                         head_path_mm3=intersect(head,body),
                         shank_path_mm3=intersect(shaft,body),
                         driver_d6_path_mm3=intersect(tool,body),
                         final_head_mm3=intersect(cylinder(x,z,7,63.3,67.3),body)))
    return rows


def root_seat_lands(occ=None):
    body=(occ or B.find_occ('Proximal_Link_L')).component.bRepBodies.item(0)
    tm=adsk.fusion.TemporaryBRepManager.get()
    rows=[]
    for i,(x,z) in enumerate(B._receiver_centres(0,0,B.HUB_LINK_PCD,6,B.HUB_LINK_A0)):
        ring=cylinder(x,z,7,63.1,63.3)
        assert tm.booleanOperation(ring,cylinder(x,z,4.3,63.1,63.3),adsk.fusion.BooleanTypes.DifferenceBooleanType)
        full=ring.volume*1000
        actual=intersect(ring,body)
        rows.append(dict(index=i,expected_land_volume_mm3=full,actual_land_volume_mm3=actual,
                         supported_fraction=actual/full))
    return rows


def screw_head_audit():
    """All modelled screw heads against every printed part at the saved pose.

    Retain clashes with alternative fixtures as findings; do not hide them.
    This is a final-seat census, supplemented by ordered path checks.
    """
    tm = adsk.fusion.TemporaryBRepManager.get()
    printed = [(o.component.name, tm.copy(b)) for o in B.root().occurrences
               if not o.component.name.startswith(('HW_', 'REF_', 'Knee_Spring'))
               for b in o.bRepBodies]
    rows = []
    for o in B.root().occurrences:
        name = B.base_name(o.component.name)
        if name not in B.SCREW_LEN:
            continue
        d, length = B.SCREW_LEN[name]
        hd, hh = B.SHCS[d]
        bb = B.bbox_of(o)
        x,z = (bb[0]+bb[1])/2,(bb[4]+bb[5])/2
        sign = 1 if o.transform2.getCell(1,1) > 0 else -1
        edge = bb[3] if sign == 1 else bb[2]
        seat = edge - sign*hh
        probe = cylinder(x,z,hd,seat,edge)
        clashes = {n:v for n,b in printed if (v:=intersect(probe,b)) > .001}
        rows.append(dict(screw=o.name, centre_xz_mm=[x,z], seat_y_mm=seat,
                         head_d_mm=hd, head_height_mm=hh, collisions_mm3=clashes))
    return rows


def snapshot(label):
    R.ref_assert(); R.placed_assert()
    report = dict(document=adsk.core.Application.get().activeDocument.name,
                  method='Fusion MCP; exact temporary B-Rep solid intersections',
                  receiver_access=receiver_access(), root_access=root_access(),
                  root_seat_lands=root_seat_lands(),
                  screw_heads=screw_head_audit(),
                  receiver_geometry_problems=B.audit_threaded_receivers(),
                  blind_depth_problems=B.audit_blind_holes(),
                  head_spacing_problems=B.audit_fasteners())
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT,label+'.json'),'w') as f:
        json.dump(report,f,indent=2); f.write('\n')
    print(json.dumps({'report':label+'.json', 'root_access':report['root_access'],
                      'receiver_count':sum(r['count'] for r in report['receiver_access']),
                      'screw_count':len(report['screw_heads']),
                      'head_collisions':[r for r in report['screw_heads'] if r['collisions_mm3']]}))
    return report


def run(_context: str):
    snapshot('before')
