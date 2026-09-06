"""Repair/check shared screw pose classification through Fusion MCP."""
import importlib
import json
import math
import os
import runpy
import sys
import adsk.core

ROOT='/Users/neilchulani/Robots/Biped'
OUT=os.path.dirname(__file__)
sys.path.insert(0,ROOT)
import beni_lib as B
import rig_lib as R


def run(_context: str):
    app=adsk.core.Application.get()
    assert app.activeDocument.name=='Beni_SingleLegRig'
    importlib.reload(B); importlib.reload(R)
    R.register_pose_classes(); R.ref_assert(); R.placed_assert()
    screws=[o for o in B.root().occurrences
            if B.base_name(o.component.name)=='HW_SHCS_M3x8']
    wheel=sorted([o for o in screws if B.bbox_of(o)[3]>90],key=lambda o:o.name)
    housing=[o for o in screws if B.bbox_of(o)[3]<90]
    assert len(wheel)==3 and len(housing)==8
    centres=B._receiver_centres(B.WX,B.WZ,B.WM_OUT_PCD,3,B.WM_OUT_A0)
    saved=R.xf_capture()
    # Intentional wheel repairs replace those three entries in the guard.
    targets={o.entityToken:list(B._tmat((x,B.WH_HUB_Y_B-2.5,z)).asArray())
             for o,(x,z) in zip(wheel,centres)}
    corrected=[(o,targets.get(o.entityToken,arr)) for o,arr in saved]
    R.xf_restore(corrected)
    B.design().computeAll(); adsk.doEvents(); R.xf_restore(corrected)
    nominal=R.xf_capture()
    rows=[]
    try:
        # Only the three shared-family wheel screws need regression coverage;
        # the complete joint geometry sweep is in rig_motion_checks.json.
        for angle in (-120,120,0):
            for o,(x,z) in zip(wheel,centres):
                xf=adsk.core.Matrix3D.create()
                xf.setToRotation(math.radians(angle),adsk.core.Vector3D.create(0,1,0),
                                 adsk.core.Point3D.create(0,0,0))
                p=adsk.core.Point3D.create(x/10,(B.WH_HUB_Y_B-2.5)/10,z/10)
                p.transformBy(xf)
                o.transform2=B._tmat((p.x*10,p.y*10,p.z*10))
            wheel_classes=[B.classify(o) for o in wheel]
            housing_classes=[B.classify(o) for o in housing]
            rows.append(dict(shoulder_deg=angle,wheel_classes=wheel_classes,
                             housing_classes=housing_classes))
            assert wheel_classes==['DIST']*3 and housing_classes==['STATIC']*8
    finally:
        R.xf_restore(nominal)
    R.ref_assert(); R.placed_assert()
    with open(os.path.join(OUT,'wheel_pose_classification.json'),'w') as f:
        json.dump(dict(method='Actual Fusion occurrence transforms at shoulder extremes; restoration to source datums',
                       poses=rows),f,indent=2)
    V=runpy.run_path(os.path.join(OUT,'verify_fusion.py'))
    report=V['snapshot']('rig_after')
    assert not report['head_spacing_problems']
    # The load-test torque arm is an alternative to the attached leg.
    assert not any(set(row['collisions_mm3'])-{'RIG_Torque_Arm'}
                   for row in report['screw_heads'])
    runpy.run_path(os.path.join(OUT,'paths_fusion.py'))['run'](_context)
    R.ref_assert();R.placed_assert()
    assert app.activeDocument.save('Correct M4 assembly access and cable post; match M3x8 housing screws and keep wheel screws rigidly attached during poses')
    record=dict(document=app.activeDocument.name,saved=not app.activeDocument.isModified,
                version=app.activeDocument.dataFile.versionNumber)
    with open(os.path.join(OUT,'rig_save.json'),'w') as f:json.dump(record,f,indent=2)
    print(json.dumps(record))
