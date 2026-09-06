"""Supported ABS knee mock-up. Run every operation through the Fusion MCP.

The saved rig is the geometric source. These are separate first articles, not
a steel-pin fit, encoder/retention release, or a spring-loaded leg release.
"""
import json
import math
import os
import sys
import struct
import hashlib
from collections import Counter
import adsk.core
import adsk.fusion

ROOT = os.path.dirname(__file__)
sys.path.insert(0, ROOT)
import beni_lib as B
import rig_lib as R
import rig_export as E

WORK = '/tmp/biped-knee-release'
DOC_NAME = 'Beni_Knee_Supported_DryFit'
DISTAL = 'ABS_MOCKUP_Distal_Link_L'
PIN = 'ABS_MOCKUP_Knee_Alignment_Pin_D9p7'
CAP = 'ABS_Spring_Seat_Fit_Cap_D8'

# New mock-up dimensions, deliberately specified here rather than presented
# as physical measurements. The nominal knee bore is 10 and the journal span
# is 31.6 (rig_lib AXLE_Y0/Y1). Clearance is intentional; this is not a gauge.
PIN_D = 9.7
PIN_GRIP_D = 18.0
PIN_GRIP_T = 3.0
PIN_SHAFT_L = 40.0
PIN_LEAD = 0.8
CAP_OD = 20.0           # original cartridge rectangular seat width
CAP_PILOT_D = 8.0       # fit candidate for the owner's nominal ID9 spring
CAP_PILOT_L = 4.0       # original upper eye's locating length
CAP_BASE_T = 2.0        # detached coupon only, not a preload adjustment
CAP_BORE = 5.6          # existing lower guide clearance, not spring acceptance


def tm():
    return adsk.fusion.TemporaryBRepManager.get()


def cylinder(x, z, d, y0, y1, d1=None):
    return tm().createCylinderOrCone(
        adsk.core.Point3D.create(x/10, y0/10, z/10), d/20,
        adsk.core.Point3D.create(x/10, y1/10, z/10), (d if d1 is None else d1)/20)


def boolean(a, b, operation):
    assert tm().booleanOperation(a, b, operation)
    return a


def cut(a, b):
    return boolean(a, b, adsk.fusion.BooleanTypes.DifferenceBooleanType)


def join(a, b):
    return boolean(a, b, adsk.fusion.BooleanTypes.UnionBooleanType)


def overlap(a, b):
    aa, bb = a.boundingBox, b.boundingBox
    if any(getattr(aa.maxPoint, v) <= getattr(bb.minPoint, v)+1e-8 or
           getattr(bb.maxPoint, v) <= getattr(aa.minPoint, v)+1e-8
           for v in ('x','y','z')):
        return 0.0
    return boolean(tm().copy(a), b, adsk.fusion.BooleanTypes.IntersectionBooleanType).volume*1000


def shifted(b, x=0.0, y=0.0, z=0.0):
    result = tm().copy(b)
    m = adsk.core.Matrix3D.create()
    m.translation = adsk.core.Vector3D.create(x/10,y/10,z/10)
    assert tm().transform(result,m)
    return result


def persist(name, body):
    assert not B.find_occ(name), name
    o = B.new_comp(name)
    base = o.component.features.baseFeatures.add()
    base.name = name + '_NativeFusionBRep'
    base.startEdit()
    result = o.component.bRepBodies.add(body, base)
    base.finishEdit()
    assert result and result.isSolid
    result.name = name
    return o


def topology(o):
    b=o.component.bRepBodies.item(0)
    assert o.component.bRepBodies.count == 1 and b.isSolid
    assert b.lumps.count == 1
    assert all(e.faces.count == 2 for e in b.edges)
    return dict(volume_mm3=b.volume*1000, faces=b.faces.count,
                edges=b.edges.count, closed_manifold=True)


def planes(o, direction=-1):
    rows=[]
    for i,f in enumerate(o.component.bRepBodies.item(0).faces):
        ok,n=f.evaluator.getNormalAtPoint(f.pointOnFace)
        assert ok
        if adsk.core.Plane.cast(f.geometry) and n.y*direction>.99999:
            bb=f.boundingBox
            rows.append(dict(index=i,y_mm=f.pointOnFace.y*10,area_mm2=f.area*100,
                             xz_mm=[v*10 for v in [bb.minPoint.x,bb.maxPoint.x,bb.minPoint.z,bb.maxPoint.z]]))
    return rows


def screenshot(name, filename, orientation=None):
    o=B.find_occ(name)
    visibility=[(x,x.isLightBulbOn) for x in B.root().occurrences]
    v=adsk.core.Application.get().activeViewport
    for x,_ in visibility:x.isLightBulbOn=(x==o)
    cam=v.camera
    cam.viewOrientation=orientation or adsk.core.ViewOrientations.IsoTopRightViewOrientation
    cam.isFitView=True; v.camera=cam; v.refresh()
    assert v.saveAsImageFile(filename,1600,1200)
    for x,on in visibility:x.isLightBulbOn=on


def create(_context: str):
    app=adsk.core.Application.get()
    assert app.activeDocument.name == 'Beni_SingleLegRig'
    R.ref_assert(); R.placed_assert()
    source=app.activeDocument
    folder=source.dataFile.parentFolder
    original=tm().copy(B.find_occ('Distal_Link_L').component.bRepBodies.item(0))
    bearings=[tm().copy(o.bRepBodies.item(0)) for o in B.find_all_occ('HW_Bearing_6800')]
    doc=app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    doc.name=DOC_NAME
    os.makedirs(WORK,exist_ok=True)
    persist('REFERENCE_Original_Distal', original).isLightBulbOn=False
    for i,b in enumerate(bearings):persist('REFERENCE_Bearing_'+str(i),b).isLightBulbOn=False

    # Omit protruding thrust lands in this supported mock-up. They prevent
    # radial tongue insertion with both bearings already installed. The 19 mm
    # web has 0.5 mm clearance to each proximal arm; no axial clamp is fitted.
    trial=tm().copy(original)
    cut(trial,cylinder(R.KNEE_X,R.KNEE_Z,30,R.SLEEVE_Y0-1,B.DBOSS_Y0))
    cut(trial,cylinder(R.KNEE_X,R.KNEE_Z,30,B.DBOSS_Y1,R.SLEEVE_Y1+1))
    o=persist(DISTAL,trial)
    # Continue the wheel flange's lower ledge to the existing bed plane. The
    # original face outline preserves every aperture; motor-facing Y67.5 stays.
    faces=[]
    for f in o.component.bRepBodies.item(0).faces:
        ok,n=f.evaluator.getNormalAtPoint(f.pointOnFace)
        if adsk.core.Plane.cast(f.geometry) and n.y<-.99999 and abs(f.pointOnFace.y*10-B.CH_Y0)<.001 and f.area*100>100:
            faces.append(f)
    assert len(faces)==1, len(faces)
    features=o.component.features.extrudeFeatures
    ip=features.createInput(faces[0],adsk.fusion.FeatureOperations.JoinFeatureOperation)
    ip.setDistanceExtent(False,adsk.core.ValueInput.createByReal((B.CH_Y0-B.LEG_Y_IN)/10))
    ext=features.add(ip); ext.name='Continue wheel flange to print bed'
    # The face normal controls the extrusion; assert the real result below.
    assert abs(o.component.bRepBodies.item(0).boundingBox.minPoint.y*10-B.LEG_Y_IN)<.001

    pin=cylinder(0,0,PIN_GRIP_D,-PIN_GRIP_T,0)
    join(pin,cylinder(0,0,PIN_D,0,PIN_SHAFT_L-PIN_LEAD))
    join(pin,cylinder(0,0,PIN_D,PIN_SHAFT_L-PIN_LEAD,PIN_SHAFT_L,PIN_D-2*PIN_LEAD))
    persist(PIN,pin).isLightBulbOn=False
    cap=cylinder(0,0,CAP_OD,0,CAP_BASE_T)
    join(cap,cylinder(0,0,CAP_PILOT_D,CAP_BASE_T,CAP_BASE_T+CAP_PILOT_L))
    cut(cap,cylinder(0,0,CAP_BORE,-1,CAP_BASE_T+CAP_PILOT_L+1))
    persist(CAP,cap).isLightBulbOn=False
    ref=B.build_proximal_link(B.ABS_KNEE_BRG_SEAT_D,component_name='REFERENCE_Proximal_Current_ABS')
    ref.isLightBulbOn=False
    print(json.dumps({n:dict(topology=topology(B.find_occ(n)),downward_planes=planes(B.find_occ(n))) for n in [DISTAL,PIN,CAP]}))
    screenshot(DISTAL,os.path.join(WORK,'distal_candidate.png'))
    # Save only after release checks. Folder remains accessible on the source.
    print('Created unsaved '+doc.name+'; source rig unchanged, folder '+folder.name)


def path_search(_context: str):
    assert adsk.core.Application.get().activeDocument.name == DOC_NAME
    distal=B.find_occ(DISTAL).component.bRepBodies.item(0)
    prox=B.find_occ('REFERENCE_Proximal_Current_ABS').component.bRepBodies.item(0)
    bearings=[o.component.bRepBodies.item(0) for o in B.root().occurrences
              if o.component.name.startswith('REFERENCE_Bearing_')]
    print('final overlap',overlap(distal,prox))
    rows=[]
    for angle in range(0,360,15):
        dx,dz=math.cos(math.radians(angle)),math.sin(math.radians(angle))
        maximum=0.0
        for off in range(0,81,2):
            trial=shifted(distal,x=off*dx,z=off*dz)
            vol=sum(overlap(trial,b) for b in [prox]+bearings)
            maximum=max(maximum,vol)
            if maximum>0.01:break
        rows.append(dict(angle_deg=angle,max_interference_mm3=maximum))
    with open(os.path.join(WORK,'path_search.json'),'w') as f:json.dump(rows,f,indent=2)
    print(json.dumps(rows))


def assembly_audit(_context: str):
    assert adsk.core.Application.get().activeDocument.name == DOC_NAME
    distal=B.find_occ(DISTAL).component.bRepBodies.item(0)
    prox=B.find_occ('REFERENCE_Proximal_Current_ABS').component.bRepBodies.item(0)
    bearings=[o.component.bRepBodies.item(0) for o in B.root().occurrences
              if o.component.name.startswith('REFERENCE_Bearing_')]
    fixed=[prox]+bearings
    # Tongue enters radially from +X, with both bearings in place. Motor,
    # cartridge, stop pin/plate, encoder, collar and wiring are absent.
    path=[]
    for i in range(161):
        off=80-i*.5
        trial=shifted(distal,x=off)
        value=sum(overlap(trial,b) for b in fixed)
        assert value<.001,(off,value)
        path.append(dict(offset_x_mm=off,interference_mm3=value))
    pin_probes=[('shaft',cylinder(B.KX,B.KZ,PIN_D,R.AXLE_Y0-80,R.AXLE_Y0+PIN_SHAFT_L)),
                ('grip',cylinder(B.KX,B.KZ,PIN_GRIP_D,R.AXLE_Y0-80-PIN_GRIP_T,R.AXLE_Y0))]
    pin_rows=[]
    for label,p in pin_probes:
        volume=sum(overlap(p,b) for b in fixed+[distal])
        assert volume<.001,(label,volume)
        pin_rows.append(dict(envelope=label,continuous_swept_interference_mm3=volume))
    motion=[]
    for i in range(73):
        phi=-8+i*.5
        trial=tm().copy(distal)
        assert tm().transform(trial,B._as_matrix(B._rot_arr(phi,B.KX,B.KZ)))
        volume=sum(overlap(trial,b) for b in fixed)
        assert volume<.001,(phi,volume)
        motion.append(dict(phi_deg=phi,interference_mm3=volume))
    # Detached spring fit cap: conservative solid annular envelope, not a
    # guessed helix/rate. Slide either spring end onto the candidate pilot.
    cap=B.find_occ(CAP).component.bRepBodies.item(0)
    spring_sweep=cut(cylinder(0,0,18,CAP_BASE_T,CAP_BASE_T+50+40),
                     cylinder(0,0,9,CAP_BASE_T-1,CAP_BASE_T+50+41))
    spring_overlap=overlap(spring_sweep,cap)
    assert spring_overlap<.001
    report=dict(status='CAD PATH VERIFIED; physical rehearsal required',
                distal_radial_insertion=path,pin_continuous_paths=pin_rows,
                sampled_hand_motion=motion,
                spring_cap=dict(spring_od_mm=18,spring_id_mm=9,free_length_mm=50,
                                pilot_d_mm=CAP_PILOT_D,seat_d_mm=CAP_OD,
                                continuous_insertion_interference_mm3=spring_overlap,
                                scope='Detached free spring only; no compression or leg installation'),
                assembly_scope='Both links supported on bench; motors, spring cartridge, stop hardware, encoder, collar and wiring absent. Reverse insertion for removal. Do not lift by the pin or clamp the joint axially.',
                axle_fit='Intentional D9.7 mock-up clearance in nominal D10 bores; not a steel-pin coupon or encoder reference',
                axial_clearance_each_side_mm=(B.CH_Y1-B.CH_Y0-(B.DBOSS_Y1-B.DBOSS_Y0))/2,
                print_geometry={n:dict(topology=topology(B.find_occ(n)),downward_planes=planes(B.find_occ(n))) for n in [DISTAL,PIN,CAP]})
    with open(os.path.join(WORK,'assembly_audit.json'),'w') as f:json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps(dict(radial_path_samples=len(path),pin_paths=pin_rows,
                         hand_motion_samples=len(motion),max_hand_clash_mm3=max(r['interference_mm3'] for r in motion),
                         spring_cap=report['spring_cap'])))


def support_audit(_context: str):
    """Check support envelopes and their withdrawal in the detached print.

    Envelopes are native Fusion face extrusions. Their voids reserve the pin
    bore and all actual mating lands; they are inspection geometry, not STLs.
    """
    o=B.find_occ(DISTAL)
    body=o.component.bRepBodies.item(0)
    geometry=tm().copy(body)
    rows=[]
    shown=[]
    for label,y,depth in [('knee_web',65.0,5.2),('open_channel',84.5,19.4)]:
        face=next(f for f in body.faces if adsk.core.Plane.cast(f.geometry)
                  and abs(f.pointOnFace.y*10-y)<.001 and f.area*100>500
                  and f.evaluator.getNormalAtPoint(f.pointOnFace)[1].y<-.99)
        ip=o.component.features.extrudeFeatures.createInput(face,adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        ip.setDistanceExtent(False,adsk.core.ValueInput.createByReal(depth/10))
        ext=o.component.features.extrudeFeatures.add(ip)
        support=shifted(ext.bodies.item(0),y=-.3)
        assert ext.deleteMe()
        body=o.component.bRepBodies.item(0)
        cut(support,geometry)
        # Reserve 0.6 mm lateral separation from print walls. For the knee
        # support, also exclude everything shadowed by the lower arm: those
        # areas already have part material beneath them and are not a route
        # for build-plate supports or downward removal.
        for dx,dz in [(.6,0),(-.6,0),(0,.6),(0,-.6),(.6,.6),(.6,-.6),(-.6,.6),(-.6,-.6)]:
            shifted_geometry=shifted(geometry,x=dx,z=dz)
            if overlap(support,shifted_geometry)>.00001:cut(support,shifted_geometry)
        if label=='knee_web':
            for i in range(1,13):
                shadow=shifted(geometry,y=i*.5)
                if overlap(support,shadow)>.00001:cut(support,shadow)
        for x,z,d in [(B.KX,B.KZ,18),(B.LX,B.LZ,8),(*B.kpt(B.STOP_R,B.STOP_PIN_A0),9)]:
            if overlap(support,cylinder(x,z,d,55,95))>.00001:
                cut(support,cylinder(x,z,d,55,95))
        paths=[]
        directions=[(0,-1,0)] if label=='knee_web' else [(math.cos(math.radians(a)),0,math.sin(math.radians(a))) for a in range(0,360,15)]
        for dx,dy,dz in directions:
            maximum=0
            for i in range(81):
                off=i*.5
                volume=overlap(shifted(support,x=dx*off,y=dy*off,z=dz*off),geometry)
                maximum=max(maximum,volume)
                if maximum>.001:break
            paths.append(dict(direction=[dx,dy,dz],maximum_mm3=maximum))
        clear=[p for p in paths if p['maximum_mm3']<.001]
        assert clear, (label,paths)
        row=dict(label=label,top_y_mm=y-.3,depth_mm=depth,
                 support_volume_mm3=support.volume*1000,clear_removal_paths=clear,
                 samples_each_path=81,step_mm=.5,travel_mm=40,
                 lateral_gap_mm=.6,top_bottom_gap_mm=.3,
                 keepout_diameters_mm=dict(knee=18,cartridge_pivot=8,stop_pin=9))
        rows.append(row)
        shown.append(persist('REFERENCE_Support_'+label,support))
        shown[-1].component.bRepBodies.item(0).appearance=B.appearance('SPRING')
    with open(os.path.join(WORK,'support_audit.json'),'w') as f:json.dump(rows,f,indent=2);f.write('\n')
    print(json.dumps(rows))
    o.component.bRepBodies.item(0).appearance=B.appearance('ABS')
    snapshot_group([DISTAL]+[x.component.name for x in shown],os.path.join(WORK,'support_regions.png'),(-1,-1,1))
    for x in shown:x.isLightBulbOn=False


def snapshot_group(names,filename,eye_direction=(1,1,1)):
    visibility=[(x,x.isLightBulbOn) for x in B.root().occurrences]
    for x,_ in visibility:x.isLightBulbOn=x.component.name in names
    view=adsk.core.Application.get().activeViewport
    bb=B.find_occ(names[0]).boundingBox
    target=adsk.core.Point3D.create((bb.minPoint.x+bb.maxPoint.x)/2,
                                  (bb.minPoint.y+bb.maxPoint.y)/2,
                                  (bb.minPoint.z+bb.maxPoint.z)/2)
    cam=view.camera
    cam.target=target
    cam.eye=adsk.core.Point3D.create(target.x+eye_direction[0]*30,
                                   target.y+eye_direction[1]*30,
                                   target.z+eye_direction[2]*30)
    cam.upVector=adsk.core.Vector3D.create(0,0,1)
    cam.isPerspective=False; cam.isFitView=True
    view.camera=cam; view.refresh()
    assert view.saveAsImageFile(filename,1600,1200)
    for x,on in visibility:x.isLightBulbOn=on


def export_candidates(_context: str):
    assert adsk.core.Application.get().activeDocument.name == DOC_NAME
    exports=[]
    policies={
        DISTAL:'ABS supported dry-fit mock-up only. Source Y59.5 down; all bores vertical. Manual normal supports under raised knee web and upper channel ceiling only, top/bottom gap at least 0.3 mm (0.4 mm for the 0.20 mm layer profile), XY gap 0.6 mm. Protect full D18 around knee, D8 around cartridge pivot and D9 around stop hole. No support in bores or on motor face, bearing lands or other mating/service surfaces. Withdraw web supports downward and channel supports through the open side. Small slot-corner ceiling and excluded hole margins are controlled bridges; inspect undersides and slicer preview.',
        PIN:'ABS, grip flat on bed, shaft vertical. No supports, 0.20 mm layers, 4 walls, 100 percent infill. Intentional clearance alignment pin only; no powered, spring or load-bearing use.',
        CAP:'ABS, broad annular seat base on bed, pilot vertical. No supports. Detached fit coupon for free spring ends only; no spring compression or installation on the leg.'}
    for n in [PIN,DISTAL,CAP]:
        o=B.find_occ(n)
        topology(o)
        for f in o.component.bRepBodies.item(0).faces:
            g=f.geometry
            if adsk.core.Cylinder.cast(g):assert abs(g.axis.y)>.999999
        row=E._export_min_y_face_down(o,n+'_PRINT_ORIENTED',WORK,policies[n])
        row['topology']=topology(o)
        row['quantity']=2 if n==CAP else 1
        exports.append(row)
    pin=shifted(B.find_occ(PIN).component.bRepBodies.item(0),x=B.KX,y=R.AXLE_Y0,z=B.KZ)
    posed=persist('REFERENCE_Inserted_Temporary_Pin',pin)
    posed.component.bRepBodies.item(0).appearance=B.appearance('SPRING')
    names=['REFERENCE_Proximal_Current_ABS',DISTAL,posed.component.name]
    names += [o.component.name for o in B.root().occurrences if o.component.name.startswith('REFERENCE_Bearing_')]
    snapshot_group(names,os.path.join(WORK,'supported_knee_assembly.png'),(-1,-1,1))
    posed.isLightBulbOn=False
    with open(os.path.join(WORK,'exports.json'),'w') as f:json.dump(exports,f,indent=2);f.write('\n')
    print(json.dumps(exports))


def verify_exports(_context: str):
    """Verify exported files inside Fusion, through MCP, without mesh repair."""
    with open(os.path.join(WORK,'exports.json')) as f:exports=json.load(f)
    report=[]
    for row in exports:
        data=open(row['stl'],'rb').read()
        count=struct.unpack_from('<I',data,80)[0]
        assert len(data)==84+count*50
        edges=Counter(); degenerate=0; volume=0; xyz=[]
        for i in range(count):
            values=struct.unpack_from('<12fH',data,84+i*50)
            pts=[tuple(values[3+j*3:6+j*3]) for j in range(3)]
            xyz.extend(pts)
            if len(set(pts))<3:degenerate+=1
            for j in range(3):edges[tuple(sorted((pts[j],pts[(j+1)%3])))]+=1
            a,b,c=pts
            volume+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
        bad=sum(v!=2 for v in edges.values())
        dimensions=[max(p[i] for p in xyz)-min(p[i] for p in xyz) for i in range(3)]
        minimum=min(p[2] for p in xyz)
        ratio=abs(volume-row['topology']['volume_mm3'])/row['topology']['volume_mm3']
        result=dict(file=os.path.basename(row['stl']),triangles=count,nonmanifold_edges=bad,
                    degenerate_triangles=degenerate,minimum_z_mm=minimum,dimensions_mm=dimensions,
                    mesh_volume_mm3=volume,native_volume_relative_error=ratio,
                    sha256=hashlib.sha256(data).hexdigest())
        report.append(result)
        assert bad==0 and degenerate==0 and abs(minimum)<1e-5 and ratio<.002,result
    with open(os.path.join(WORK,'mesh_verification.json'),'w') as f:json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps(report))


def record_saved(_context: str):
    app=adsk.core.Application.get()
    doc=app.activeDocument
    assert doc.name==DOC_NAME and doc.isSaved and not doc.isModified
    with open(os.path.join(WORK,'assembly_audit.json')) as f:audit=json.load(f)
    verified={}
    for name in [DISTAL,PIN,CAP]:
        actual=topology(B.find_occ(name))
        expected=audit['print_geometry'][name]['topology']
        assert abs(actual['volume_mm3']-expected['volume_mm3'])<.000001
        assert actual['faces']==expected['faces'] and actual['edges']==expected['edges']
        verified[name]=actual
    rig=next(d for d in app.documents if d.name=='Beni_SingleLegRig')
    saved=dict(document=doc.name,file_id=doc.dataFile.id,version=doc.dataFile.versionNumber,
               source_rig=rig.name,source_rig_version=rig.dataFile.versionNumber,
               source_rig_modified=rig.isModified,
               save_method='Native Fusion archive export, upload, open and re-inspection',
               reopened_native_geometry_matches_release=True,verified_parts=verified)
    rig.activate();R.ref_assert();R.placed_assert()
    assert not rig.isModified
    doc.activate()
    with open(os.path.join(WORK,'fusion_document.json'),'w') as f:json.dump(saved,f,indent=2);f.write('\n')
    print(json.dumps(saved))


def save_verified(_context: str):
    """Export a native archive and queue its upload through Fusion MCP.

    Direct saveAs returned True without producing a saved document in this
    session, so success is established by opening and inspecting the uploaded
    archive. Do not repeat upload while its DataFileFuture is pending.
    """
    global archive_upload_future
    app=adsk.core.Application.get()
    assert app.activeDocument.name==DOC_NAME
    for filename in ['assembly_audit.json','support_audit.json','mesh_verification.json']:
        assert os.path.isfile(os.path.join(WORK,filename))
    archive=os.path.join(WORK,DOC_NAME+'.f3d')
    manager=B.design().exportManager
    assert manager.execute(manager.createFusionArchiveExportOptions(archive))
    rig=next(d for d in app.documents if d.name=='Beni_SingleLegRig')
    archive_upload_future=rig.dataFile.parentFolder.uploadFile(archive)
    assert archive_upload_future
    print('Archive upload queued. Wait for completion, open its dataFile through Fusion MCP, compare native part topology, then call record_saved.')


def run(_context: str):
    create(_context)
    assembly_audit(_context)
    support_audit(_context)
    export_candidates(_context)
    verify_exports(_context)
    save_verified(_context)
