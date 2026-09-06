"""Ordered assembly/removal and continuous hardware paths via Fusion MCP."""
import json
import os
import runpy
import adsk.core
import adsk.fusion

OUT=os.path.dirname(__file__)


def run(_context: str):
    V=runpy.run_path(os.path.join(OUT,'verify_fusion.py'))
    B,R=V['B'],V['R']
    R.ref_assert(); R.placed_assert()
    tm=adsk.fusion.TemporaryBRepManager.get()
    def bodies(name):
        o=B.find_occ(name)
        return [tm.copy(b) for c in R._occ_tree(o) for b in c.bRepBodies]
    paths=[]
    def path(label,moving,fixed,travel=40,sign=1):
        maximum=0; worst=None
        for i in range(81):
            off=sign*(travel-i*travel/80)
            xf=adsk.core.Matrix3D.create(); xf.translation=adsk.core.Vector3D.create(0,off/10,0)
            value=0
            for b in moving:
                trial=tm.copy(b); assert tm.transform(trial,xf)
                value+=sum(V['intersect'](trial,s) for s in fixed)
            if value>maximum:maximum,worst=value,off
        row=dict(path=label,samples=81,travel_mm=travel,direction_y=sign,
                 max_interference_mm3=maximum,worst_offset_mm=worst)
        paths.append(row); return maximum
    link=bodies('Proximal_Link_L'); hub=bodies('Shoulder_Output_Hub_L')
    plate=bodies('Chassis_Shoulder_Plate_L'); cover=bodies('Shoulder_Cable_Cover_L')
    post=bodies('RIG_Cable_Post_A'); smotor=bodies('REF_GIM6010-8')
    path('link onto completed shoulder; knee subassembly absent',link,hub+plate+cover+post+smotor)
    path('post A onto fitted cover; link absent',post,cover+plate+hub+smotor)
    path('cover onto shoulder; link and post absent',cover,plate+hub+smotor)
    path('wheel rim onto hub and detached wheel motor',bodies('Wheel_Rim_L'),bodies('Wheel_Hub_L')+bodies('REF_GIM4305-10'))
    assert all(p['max_interference_mm3']<.001 for p in paths),paths

    printed=[(o.component.name,tm.copy(b)) for o in B.root().occurrences
             if not o.component.name.startswith(('HW_','REF_','Knee_Spring'))
             and o.component.name not in ('RIG_Torque_Arm','RIG_Scale_Pedestal')
             for b in o.bRepBodies]
    screw_paths=[]
    for o in B.root().occurrences:
        family=B.base_name(o.component.name)
        if family not in B.SCREW_LEN:continue
        d,length=B.SCREW_LEN[family]; hd,hh=B.SHCS[d]
        bb=B.bbox_of(o); x,z=(bb[0]+bb[1])/2,(bb[4]+bb[5])/2
        sign=1 if o.transform2.getCell(1,1)>0 else -1
        edge=bb[3] if sign==1 else bb[2]; seat=edge-sign*hh
        absent=[]
        if family=='HW_SHCS_M3x8' and abs(seat-47)<.001:
            absent=['Shoulder_Cable_Cover_L','RIG_Cable_Post_A','Proximal_Link_L']
        if family=='HW_SHCS_M3x10' and abs(seat-47)<.001:
            absent=['RIG_Cable_Post_A'] # attach panel to stand before post
        if family=='HW_SHCS_M3x6':
            absent=['Knee_Encoder_Bracket_L','Knee_Encoder_PCB_L']
        if family=='HW_SHCS_M2p5x12':
            absent=['RIG_Stand'] # wheel-motor screws on a supported bench subassembly
        probes=[V['cylinder'](x,z,hd,seat,edge+sign*40),
                V['cylinder'](x,z,d,seat-sign*length,seat+sign*40),
                V['cylinder'](x,z,hd,edge,edge+sign*50)]
        collisions={n:vol for n,b in printed if n not in absent
                    if (vol:=sum(V['intersect'](p,b) for p in probes))>.001}
        screw_paths.append(dict(screw=o.name,assembly_order_parts_absent=absent,
                                head_and_driver_envelope_d_mm=hd,continuous_travel_mm=40,
                                collisions_mm3=collisions))
    # Full Ø8 bore open through the post; Ø6 insertion/tie envelope clears
    # the cover on both sides. This is not a terminated-connector claim.
    eye=V['cylinder'](0,52,6,48.5,85.5)
    eye_collisions={n:v for n,b in printed if (v:=V['intersect'](eye,b))>.001}
    report=dict(paths=paths,screw_paths=screw_paths,post_eye_probe_d_mm=6,
                post_eye_y_mm=[48.5,85.5],post_eye_collisions_mm3=eye_collisions,
                service_order='Reverse paths. Remove link before cover and housing screws. Remove post before panel/stand bolts. Fit stop screws before encoder bracket and remove encoder bracket to withdraw them. Install/service wheel housing screws with leg supported off the stand. Heat inserts in bare parts before mating parts cover their mouths.',
                real_harness_gate='Actual tie, connector and bend routing still requires physical rehearsal; no complete wired release.')
    with open(os.path.join(OUT,'ordered_paths.json'),'w') as f:
        json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps({'paths':paths,'screw_count':len(screw_paths),'failures':[r for r in screw_paths if r['collisions_mm3']],'eye_collisions':eye_collisions}))
    assert not eye_collisions
    assert all(not row['collisions_mm3'] for row in screw_paths)
