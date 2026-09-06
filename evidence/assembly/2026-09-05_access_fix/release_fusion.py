"""Reproduce the ABS access-fix articles via Fusion MCP, active rig document."""
import importlib
import json
import os
import runpy
import sys
import adsk.core
import adsk.fusion

ROOT = '/Users/neilchulani/Robots/Biped'
OUT = os.path.dirname(__file__)
sys.path.insert(0, ROOT)
import beni_lib as B
import rig_lib as R
import rig_export as E


def face_audit(occ):
    body = occ.component.bRepBodies.item(0)
    assert body.isSolid and occ.component.bRepBodies.count == 1
    assert all(e.faces.count == 2 for e in body.edges), 'non-manifold B-Rep edge'
    rows=[]
    for i,face in enumerate(body.faces):
        if adsk.core.Plane.cast(face.geometry) is None:
            continue
        ok,n=face.evaluator.getNormalAtPoint(face.pointOnFace)
        assert ok
        if n.y>.999999:
            rows.append(dict(face=i,y_mm=face.pointOnFace.y*10,
                             height_mm=(body.boundingBox.maxPoint.y-face.pointOnFace.y)*10,
                             area_mm2=face.area*100))
    return dict(volume_mm3=body.volume*1000,faces=body.faces.count,
                edges=body.edges.count,closed_manifold=True,bed_facing_planes=rows)


def run(_context: str):
    assert adsk.core.Application.get().activeDocument.name == 'Beni_SingleLegRig'
    importlib.reload(B); importlib.reload(R); importlib.reload(E)
    R.ref_assert(); R.placed_assert()
    V=runpy.run_path(os.path.join(OUT,'verify_fusion.py'))
    name='ABS_FA_Proximal_Link_L_D19p15_M4_ACCESS_FIXED'
    occ=R.guarded(B.build_proximal_link, B.ABS_KNEE_BRG_SEAT_D, component_name=name)
    try:
        R.guarded(B.add_fillets, only=[name], proximal_name=name)
        access=V['root_access'](occ)
        lands=V['root_seat_lands'](occ)
        assert all(abs(row['supported_fraction']-1)<1e-6 for row in lands), lands
        assert all(row[k]<.001 for row in access for k in ('head_path_mm3','shank_path_mm3','driver_d6_path_mm3','final_head_mm3')), access
        body=occ.component.bRepBodies.item(0)
        spans=B._receiver_face_spans(occ,19.15,[(B.KX,B.KZ)])
        cylinders=[f for f in body.faces if (g:=adsk.core.Cylinder.cast(f.geometry)) and abs(g.radius*20-19.15)<.001]
        assert len(cylinders)==2
        assert all(abs((f.boundingBox.maxPoint.y-f.boundingBox.minPoint.y)*10-5)<.001 for f in cylinders)
        tm=adsk.fusion.TemporaryBRepManager.get()
        bearing_paths=[]
        for side,y0,y1 in [('inboard',28.7,63.7),('outboard',85.3,120.3)]:
            probe=V['cylinder'](B.KX,B.KZ,19,y0,y1)
            assert tm.booleanOperation(probe,V['cylinder'](B.KX,B.KZ,10,y0,y1),adsk.fusion.BooleanTypes.DifferenceBooleanType)
            vol=V['intersect'](probe,body)
            assert vol<.001
            bearing_paths.append(dict(side=side,continuous_swept_ring_y_mm=[y0,y1],interference_mm3=vol))
        report=dict(source_builder='beni_lib.build_proximal_link + targeted add_fillets',
                    bearing_seat_d_mm=19.15,bearing_depth_mm=5,root_access=access,root_seat_lands=lands,
                    bearing_insertion_and_removal=bearing_paths,topology_and_print=face_audit(occ))
        v=adsk.core.Application.get().activeViewport
        cam=v.camera; cam.viewOrientation=adsk.core.ViewOrientations.IsoTopRightViewOrientation; cam.isFitView=True; v.camera=cam
        report['print_export']=R.guarded(E._export_max_y_face_down,occ,name+'_PRINT_ORIENTED',E.ABS_ASSEMBLY_DIR,
            'No supports. Same vertical bearing/insert axes as passed ABS coupons. Outboard arm face Y90.3 down. Existing 20 mm channel and root-pad ceilings are controlled bridges; inspect undersides and Ø17 retention lips. Access cuts run vertically. Shorter lightening slot retains the six screw seats and increases the bed footprint; maximum channel width remains 20 mm. Inspect slicer bridge preview before printing.')
        report['release']='ABS dry assembly only; physical six-screw seating and new full-depth bearing rehearsal required'
        with open(os.path.join(OUT,'proximal_release.json'),'w') as f:
            json.dump(report,f,indent=2); f.write('\n')
        print(json.dumps(report))
    finally:
        R.guarded(occ.deleteMe)
    R.guarded(R.build_rig_cable_post_a)
    R.guarded(R.fit_cable_post_a_fasteners)
    post=B.find_occ('RIG_Cable_Post_A')
    post_report=face_audit(post)
    post_report['print_export']=R.guarded(E._export_max_y_face_down,post,
        'ABS_FA_RIG_Cable_Post_A_COVER_MOUNT_PRINT_ORIENTED',os.path.join(ROOT,'first_article_stl/mode_a'),
        'No supports; constant 2 mm section, all through holes vertical, either broad face supports the whole part. Use supplied orientation.')
    with open(os.path.join(OUT,'post_a_release.json'),'w') as f:
        json.dump(post_report,f,indent=2); f.write('\n')
    print(json.dumps(post_report))
    R.ref_assert(); R.placed_assert()
