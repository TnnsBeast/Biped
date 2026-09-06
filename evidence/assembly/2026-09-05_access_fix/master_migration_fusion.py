"""Guarded saved-master migration; run with Beni_Prototype1 via Fusion MCP."""
import importlib
import json
import os
import runpy
import sys
import adsk.core

ROOT='/Users/neilchulani/Robots/Biped'
OUT=os.path.dirname(__file__)
sys.path.insert(0,ROOT)
import beni_lib as B
import rig_lib as R


def migrate_housing():
    master=B.find_occ('HW_SHCS_M3x8')
    old=[]
    for o in B.root().occurrences:
        if B.base_name(o.component.name)=='HW_SHCS_M3x10':
            bb=B.bbox_of(o);x,z=(bb[0]+bb[1])/2,(bb[4]+bb[5])/2
            if abs(bb[3]-50)<.001 and abs((x*x+z*z)**.5-37)<.001:old.append(o)
    assert len(old) in (0,8)
    for o in old:
        B.root().occurrences.addExistingComponent(master.component,o.transform2)
        assert o.deleteMe()


def run(_context: str):
    assert adsk.core.Application.get().activeDocument.name=='Beni_Prototype1'
    importlib.reload(B);importlib.reload(R)
    R.ref_assert(); R.placed_assert()
    R.guarded(B.drop_mirror)
    p=B.find_occ('Proximal_Link_L')
    if not any(s.name=='Root_M4_Continuous_Access' for s in p.component.sketches):
        R.guarded(B.clear_proximal_root_access,p.component)
    R.guarded(B.repair_proximal_root_seat_land,p.component)
    R.guarded(migrate_housing)
    R.guarded(B.build_mirror)
    problems=B.audit_all()
    assert not problems,problems
    V=runpy.run_path(os.path.join(OUT,'verify_fusion.py'))
    report=V['snapshot']('master_after')
    assert not any(row['collisions_mm3'] for row in report['screw_heads'])
    assert not report['head_spacing_problems']
    assert all(v<.001 for row in report['receiver_access'] for v in row['interference_mm3'])
    assert all(abs(v['supported_fraction']-1)<1e-6 for row in report['receiver_access'] for v in row['mouth_lands'])
    for o in B.root().occurrences:
        o.isLightBulbOn=True
        for s in o.component.sketches:s.isLightBulbOn=False
    import rig_export as E
    E._stl(B.find_occ('Proximal_Link_L'),os.path.join(ROOT,'print_stl/Proximal_Link_L.stl'))
    runpy.run_path(os.path.join(ROOT,'readme_images_fusion.py'))['run'](_context)
    R.ref_assert();R.placed_assert()
    assert adsk.core.Application.get().activeDocument.save('Correct proximal M4 head access and seating lands; match accepted shoulder housing screws; regenerate right leg')
    doc=adsk.core.Application.get().activeDocument
    record=dict(document=doc.name,audit_problems=problems,saved=not doc.isModified,
                version=doc.dataFile.versionNumber)
    with open(os.path.join(OUT,'master_save.json'),'w') as f:json.dump(record,f,indent=2)
    print(json.dumps(record))
