"""Fail-closed mechanical-article release checks. Execute only via Fusion MCP.

The reviewed baseline is independent of builders. Ordinary exports cannot update
it. A deliberate design change requires review of the diff, renewed paths and
print-orientation evidence, and an explicit accept_* call in the same commit.

The mesh gate is machine-independent. A bed-ready STL passes when it matches
the pinned triangle fingerprint exactly, or when mesh_fidelity() proves it is
the reviewed B-Rep at its recorded bed pose at the release chord. Fusion builds
tessellate differently, so a fingerprint alone cannot be the fit gate.
"""
import hashlib
import json
import math
import os
import struct
import time
import adsk.core
import adsk.fusion
import beni_lib as B
import rig_lib as R
import mechanical_spring_test_fusion as M
import stl_release as S

ROOT = os.path.dirname(__file__)
BASELINE = os.path.join(ROOT, 'mechanical_release_baseline.json')
EVIDENCE = os.path.join(ROOT, 'evidence/assembly/2026-09-23_mechanical_reprint_audit')
GATE_EVIDENCE = os.path.join(ROOT, 'evidence/assembly/2026-09-24_cross_machine_release_gate')
# Fusion-verified sources pinned by accept_verified_sources(); CI re-hashes them.
VERIFIED_SOURCES = ['beni_lib.py', 'rig_lib.py', 'rig_export.py', 'beni_export.py',
                    'mechanical_spring_test_fusion.py', 'ordered_pin_integration_fusion.py',
                    'mechanical_release_audit_fusion.py', 'distal_first_article_fusion.py',
                    'stl_release.py']
# Source component, released file, bed transform. This is the manual's complete
# fifteen-part printed inventory; purchased hardware is checked by assembly paths.
PARTS = [
 ('RIG_Stand','mode_a/ABS_FA_RIG_Stand_M3_INSERTS_PRINT_ORIENTED.stl','max'),
 ('Chassis_Shoulder_Plate_L','assembly_dry_fit/ABS_FA_Chassis_Shoulder_Plate_L_M3_INSERTS_PRINT_ORIENTED.stl','min'),
 ('Shoulder_Cable_Cover_L','assembly_dry_fit/ABS_FA_Shoulder_Cable_Cover_L_CLEARANCE_PRINT_ORIENTED.stl','max'),
 ('RIG_Cable_Post_A','mode_a/ABS_FA_RIG_Cable_Post_A_COVER_MOUNT_PRINT_ORIENTED.stl','max'),
 ('Shoulder_Output_Hub_L','ordered_pin_integration/ABS_PINREV2_Shoulder_Output_Hub_D4p15_ROOT_D4p30_PRINT_ORIENTED.stl','max'),
 ('Proximal_Link_L','ordered_pin_integration/ABS_PINREV2_Proximal_Link_D19p15_ROOT_D4p30_CLEVIS_D4p30_PRINT_ORIENTED.stl','max'),
 ('Distal_Link_L','ordered_pin_integration/ABS_PINREV2_Distal_Link_D10p30_D6x10_CLEVIS_D4p30_PRINT_ORIENTED.stl','min'),
 (M.STOP,'ordered_pin_integration/ABS_PINREV_Knee_Stop_Plate_15deg_D6x10_CAPTIVE_PRINT_ORIENTED.stl','max'),
 ('Wheel_Hub_L','assembly_dry_fit/ABS_FA_Wheel_Hub_L_OWNED_M4x8_D5p30_PRINT_ORIENTED.stl','max'),
 (M.UPPER,'mechanical_spring_test/ABS_TEST_Cart_Upper_Eye_50mm_AXIS_UP_PRINT_ORIENTED.stl','upper'),
 (M.LOWER,'mechanical_spring_test/ABS_TEST_Cart_Lower_Eye_50mm_AXIS_UP_PRINT_ORIENTED.stl','lower'),
 (M.GUIDE,'mechanical_spring_test/ABS_TEST_Cart_Guide_Bar_50mm_FLAT_PRINT_ORIENTED.stl','max'),
 (M.SPACER,'mechanical_spring_test/ABS_TEST_Knee_Pin_Outboard_Spacer_PRINT_ORIENTED.stl','min'),
 ('Knee_Encoder_Bracket_L','mechanical_spring_test/ABS_TEST_Knee_Encoder_Bracket_PIN_KEEPER_PRINT_ORIENTED.stl','max'),
 (M.RIM,'mechanical_spring_test/ABS_TEST_Wheel_Rim_NoTyre_PRINT_ORIENTED.stl','max'),
]


def _occ(name):
    occ = B.find_occ(name)
    if occ is None:
        raise RuntimeError('Required mechanical part missing: ' + name)
    return occ


def _cylinders(name):
    rows=[]
    for body in _occ(name).component.bRepBodies:
        for face in body.faces:
            g=adsk.core.Cylinder.cast(face.geometry)
            if g:
                bb=face.boundingBox
                rows.append({'d':g.radius*20, 'x':g.origin.x*10,
                             'z':g.origin.z*10, 'axis':g.axis.asArray(),
                             'y0':bb.minPoint.y*10,'y1':bb.maxPoint.y*10})
    return rows


def dimensional_contracts():
    """Measured faces, never constants echoed as an audit result."""
    results=[]
    def check(name, label, d, spans, centers=None):
        rows=[r for r in _cylinders(name) if abs(r['d']-d)<0.001
              and abs(abs(r['axis'][1])-1)<1e-6
              and (centers is None or any(math.hypot(r['x']-x,r['z']-z)<0.001 for x,z in centers))]
        got=sorted((round(r['y0'],3),round(r['y1'],3)) for r in rows)
        want=sorted(spans)
        results.append({'part':name,'interface':label,'diameter_mm':d,
                        'expected_y_spans_mm':want,'measured_y_spans_mm':got,
                        'pass':got==want})
    root_centers=B._receiver_centres(0,0,44,3,90.4)
    check('Distal_Link_L','steel knee-pin receiver',10.30,[(64.5,84.5)],[(B.KX,B.KZ)])
    check('Proximal_Link_L','6800 seats',19.15,[(58.7,63.7),(85.3,90.3)],[(B.KX,B.KZ)])
    check('Proximal_Link_L','bearing retention lips',17,[(63.7,64.5),(84.5,85.3)],[(B.KX,B.KZ)])
    check('Shoulder_Output_Hub_L','root dowel blind sockets',4.30,[(54.5,59.5)]*3,root_centers)
    check('Proximal_Link_L','root dowel slip sockets',4.30,[(59.5,64.7)]*3,root_centers)
    check('Shoulder_Output_Hub_L','motor factory pin passages',4.15,[(46.2,59.5)]*3)
    check('Shoulder_Output_Hub_L','M4 insert receivers',5.3,[(51.5,59.5)]*6)
    check('Proximal_Link_L','M3 insert receivers',4.5,[(85.3,90.3)]*5)
    check('Proximal_Link_L','upper clevis lands',4.30,[(56.3,64.5),(84.5,90.3)],[(B.UX,B.UZ)])
    check('Distal_Link_L','lower clevis lands',4.30,[(59.5,64.5),(84.5,93.5)],[(B.LX,B.LZ)])
    check('Distal_Link_L','captive stop socket',6.2,[(85,89.5)])
    check('Distal_Link_L','wheel motor mounting screws',2.8,[(59.5,67.5)]*6)
    check('Distal_Link_L','wheel motor cover clearance',41.5,[(59.5,67.5)])
    check('RIG_Stand','M3 insert receivers',4.5,[(36,42)]*5)
    check('Chassis_Shoulder_Plate_L','M3 cover receivers',4.5,[(42,47)]*4)
    check('Shoulder_Cable_Cover_L','M3 clearance',3.4,[(47,53.5)]*4)
    check('RIG_Cable_Post_A','M3 clearance',3.4,[(53.5,55.5)]*2)
    check('RIG_Cable_Post_A','harness eye',8,[(53.5,55.5)])
    check('Wheel_Hub_L','M4 insert receivers',5.3,[(94.5,100.5)]*6)
    check('Wheel_Hub_L','motor register',37.3,[(94.5,95.3)])
    check('Wheel_Hub_L','motor screw clearance',3.4,[(95.3,98)]*3)
    check('Wheel_Hub_L','motor screw counterbores',6.5,[(98,100.5)]*3)
    for n in (M.UPPER,M.LOWER):
        check(n,'clevis eye passage',4.4,[(65,84)])
    check(M.STOP,'mounting holes',3.4,[(90.3,96.1)]*3)
    check(M.STOP,'stop channel depth / closed skin',6.2,[(90.3,95.3)]*25)
    check(M.SPACER,'keeper locator',7.6,[(99.4,101.4)])
    check(M.SPACER,'pin stop body',15,[(94,99.4)])
    check('Knee_Encoder_Bracket_L','locator hole',8,[(99.9,101.9)])
    check('Knee_Encoder_Bracket_L','mounting passages',3.4,[(90.3,101.9)]*2)
    check(M.RIM,'insert tip relief',6,[(100.5,102.7)]*6)
    check(M.RIM,'M4 clearance',4.3,[(102.7,104.5)]*6)
    return results


def shape_signature(name):
    """All faces, including planar lands and non-Y spring pilots/guide features."""
    bodies=[]
    for body in _occ(name).component.bRepBodies:
        faces=[]
        for f in body.faces:
            bb=f.boundingBox
            row=[f.geometry.objectType,round(f.area*100,4),
                 [round(v*10,4) for v in f.centroid.asArray()],
                 [round(v*10,4) for v in bb.minPoint.asArray()+bb.maxPoint.asArray()]]
            g=adsk.core.Cylinder.cast(f.geometry)
            if g: row += [round(g.radius*20,4),[round(v,6) for v in g.axis.asArray()]]
            faces.append(row)
        bodies.append({'volume_mm3':round(body.volume*1000,4),
                       'faces':sorted(faces,key=lambda r:json.dumps(r)),
                       'solid':body.isSolid,'lumps':body.lumps.count})
    return bodies


def assert_part(name):
    """Called before any active-article STL export; no bypass on file names."""
    if adsk.core.Application.get().activeDocument.name!='Beni_SingleLegRig':
        return
    if name not in {r[0] for r in PARTS}:
        return
    rows=[r for r in dimensional_contracts() if r['part']==name]
    bad=[r for r in rows if not r['pass']]
    if bad: raise RuntimeError('Mechanical interface contract failed: '+json.dumps(bad))
    baseline=json.load(open(BASELINE))
    actual=shape_signature(name)
    if actual!=baseline['parts'][name]['shape']:
        raise RuntimeError('Unreviewed geometry change blocks export: '+name)


def assert_all():
    for name,_,_ in PARTS: assert_part(name)
    return dimensional_contracts()


def mesh_signature(path):
    data=open(path,'rb').read()
    count=struct.unpack_from('<I',data,80)[0]
    assert len(data)==84+50*count
    triangles=[]
    for i in range(count):
        v=struct.unpack_from('<12fH',data,84+50*i)
        triangles.append(sorted(tuple(round(x,3) for x in v[j:j+3]) for j in (3,6,9)))
    return {'sha256':hashlib.sha256(data).hexdigest(), 'triangles':count,
            'geometry_sha256':hashlib.sha256(json.dumps(sorted(triangles),separators=(',',':')).encode()).hexdigest()}


def export_comparison_mesh(name, side, path):
    """Native Fusion export at the recorded bed orientation; no local mesh CAD."""
    _export_body(bed_body(name, side), path)


def _export_body(body, path, options=None):
    """Export a transient body through a temporary occurrence; run guarded."""
    temp=B.root().occurrences.addNewComponent(adsk.core.Matrix3D.create())
    temp.component.name='AUDIT_TRANSIENT'
    try:
        base=temp.component.features.baseFeatures.add();base.startEdit()
        temp.component.bRepBodies.add(body,base);base.finishEdit()
        em=B.design().exportManager
        opt=(options or S.stl_options)(em,temp,path,temp.component.bRepBodies)
        assert em.execute(opt)
    finally:
        temp.deleteMe()


def _side(name):
    for part,_,side in PARTS:
        if part==name:return side
    raise KeyError('Not a release part: '+name)


def bed_body(name, side=None, source=None):
    """Transient copy of the reviewed B-Rep (or source) at its recorded bed transform."""
    side=side or _side(name)
    tm=adsk.fusion.TemporaryBRepManager.get()
    body=tm.copy(source if source is not None else _occ(name).component.bRepBodies.item(0))
    matrix=adsk.core.Matrix3D.create()
    if side in ('upper','lower'):
        (ax,az),_=B.cart_dir(0)
        if side=='lower': ax,az=-ax,-az
        matrix.setWithArray([-az,0,ax,0, 0,1,0,0, ax,0,az,0, 0,0,0,1])
    else:
        matrix.setToRotation((-1 if side=='max' else 1)*math.pi/2,
            adsk.core.Vector3D.create(1,0,0),adsk.core.Point3D.create(0,0,0))
    assert tm.transform(body,matrix)
    shift=adsk.core.Matrix3D.create()
    shift.translation=adsk.core.Vector3D.create(0,0,-body.boundingBox.minPoint.z)
    assert tm.transform(body,shift)
    return body


def _triangle_grid(tris, tolerance, cell=5.0):
    grid={}
    for idx,t in enumerate(tris):
        lo=[math.floor((min(v[i] for v in t)-tolerance)/cell) for i in range(3)]
        hi=[math.floor((max(v[i] for v in t)+tolerance)/cell) for i in range(3)]
        for x in range(lo[0],hi[0]+1):
            for y in range(lo[1],hi[1]+1):
                for z in range(lo[2],hi[2]+1):grid.setdefault((x,y,z),[]).append(idx)
    return grid


def _cylinder_chord_mm(body, verts, tris):
    """Largest rim-chord sagitta over every cylindrical face of the B-Rep.

    Only curved-wall facets are measured: all three vertices lie on the
    cylinder at more than one axial station, and the centroid is off the
    reviewed surface. Planar faces that meet a cylinder along its straight
    edges also have all vertices on it, but their centroids classify On.
    """
    on=adsk.fusion.PointContainment.PointOnPointContainment
    worst=0.0
    for face in body.faces:
        g=adsk.core.Cylinder.cast(face.geometry)
        if not g:continue
        o=[c*10 for c in g.origin.asArray()];a=list(g.axis.asArray())
        n=math.sqrt(sum(c*c for c in a));a=[c/n for c in a];r=g.radius*10
        ref=[1.0,0,0] if abs(a[0])<0.9 else [0,1.0,0]
        dot=sum(ref[i]*a[i] for i in range(3))
        e1=[ref[i]-dot*a[i] for i in range(3)];n=math.sqrt(sum(c*c for c in e1));e1=[c/n for c in e1]
        e2=[a[1]*e1[2]-a[2]*e1[1],a[2]*e1[0]-a[0]*e1[2],a[0]*e1[1]-a[1]*e1[0]]
        bb=face.boundingBox
        lo=[c*10-0.01 for c in bb.minPoint.asArray()];hi=[c*10+0.01 for c in bb.maxPoint.asArray()]
        station={}
        for i,v in enumerate(verts):
            if not all(lo[k]<=v[k]<=hi[k] for k in range(3)):continue
            d=[v[k]-o[k] for k in range(3)];t=sum(d[k]*a[k] for k in range(3))
            rad=[d[k]-t*a[k] for k in range(3)]
            if abs(math.sqrt(sum(c*c for c in rad))-r)>0.002:continue
            station[i]=(t,math.atan2(sum(rad[k]*e2[k] for k in range(3)),sum(rad[k]*e1[k] for k in range(3))))
        for tri in tris:
            if not all(i in station for i in tri):continue
            ts=[station[i][0] for i in tri]
            if max(ts)-min(ts)<=0.005:continue
            c=[sum(verts[i][k] for i in tri)/30.0 for k in range(3)]
            if body.pointContainment(adsk.core.Point3D.create(*c))==on:continue
            for p,q in ((tri[0],tri[1]),(tri[1],tri[2]),(tri[2],tri[0])):
                if abs(station[p][0]-station[q][0])>0.005:continue
                span=abs(station[p][1]-station[q][1])
                span=min(span,2*math.pi-span)
                worst=max(worst,r*(1-math.cos(span/2)))
    return worst


def mesh_fidelity(name, path, chord_gate_mm=S.CHORD_GATE_MM):
    """Prove path is a closed tessellation of the reviewed B-Rep at its bed pose.

    Mesh to B-Rep: every vertex must classify On the reviewed surface; a 0.025 mm
    radius change classifies Outside. B-Rep to mesh: every face, edge and vertex
    sample must lie within the chord of the mesh. Volume, area, bed contact and
    box must agree within the measured tessellation. chord_gate_mm=None audits a
    pinned file without imposing the release resolution.
    """
    body=bed_body(name)
    raw=_mesh_triangles(path)
    index={};tris=[]
    for t in raw:tris.append(tuple(index.setdefault(v,len(index)) for v in t))
    verts=[None]*len(index)
    for v,i in index.items():verts[i]=v
    failures=[];metrics={'triangles':len(tris),'vertices':len(verts)}
    edges={};degenerate=0
    for t in tris:
        if len(set(t))<3:degenerate+=1
        for p,q in ((t[0],t[1]),(t[1],t[2]),(t[2],t[0])):
            k=(min(p,q),max(p,q));edges[k]=edges.get(k,0)+1
    parent=list(range(len(verts)))
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    for t in tris:
        for p,q in ((t[0],t[1]),(t[1],t[2])):
            rp,rq=find(p),find(q)
            if rp!=rq:parent[rp]=rq
    metrics.update(open_or_nonmanifold_edges=sum(1 for c in edges.values() if c!=2),
                   degenerate_triangles=degenerate,
                   shells=len({find(i) for i in range(len(verts))}),lumps=body.lumps.count)
    if metrics['open_or_nonmanifold_edges'] or degenerate:failures.append('mesh is not a closed manifold')
    if metrics['shells']!=metrics['lumps']:failures.append('shell count differs from B-Rep lumps')
    on=adsk.fusion.PointContainment.PointOnPointContainment
    off=[v for v in verts if body.pointContainment(adsk.core.Point3D.create(v[0]/10,v[1]/10,v[2]/10))!=on]
    metrics['vertices_off_reviewed_surface']=len(off)
    if off:failures.append('%d vertices are not on the reviewed B-Rep, e.g. %s'%(len(off),[tuple(round(c,3) for c in v) for v in off[:3]]))
    chord=_cylinder_chord_mm(body,verts,tris)
    metrics['max_cylinder_chord_mm']=round(chord,5)
    if chord_gate_mm is not None and chord>chord_gate_mm:
        failures.append('chord %.4f mm exceeds the %.4f mm release standard'%(chord,chord_gate_mm))
    allowance=max(chord,chord_gate_mm or 0.0)+0.001
    volume=area=bed=0.0
    for p,q,r in raw:
        u=[q[i]-p[i] for i in range(3)];w=[r[i]-p[i] for i in range(3)]
        c=(u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0])
        area+=math.sqrt(sum(x*x for x in c))/2
        volume+=(p[0]*(q[1]*r[2]-q[2]*r[1])-p[1]*(q[0]*r[2]-q[2]*r[0])+p[2]*(q[0]*r[1]-q[1]*r[0]))/6
        if max(abs(p[2]),abs(q[2]),abs(r[2]))<1e-4 and c[2]<0:bed+=-c[2]/2
    curved=bed_brep=0.0
    for f in body.faces:
        if not adsk.core.Plane.cast(f.geometry):
            curved+=f.area*100;continue
        ok,normal=f.evaluator.getNormalAtPoint(f.pointOnFace)
        if ok and normal.z<-0.999999 and abs(f.pointOnFace.z)<1e-6:bed_brep+=f.area*100
    metrics.update(mesh_volume_mm3=round(volume,3),brep_volume_mm3=round(body.volume*1000,3),
                   mesh_area_mm2=round(area,3),brep_area_mm2=round(body.area*100,3),
                   bed_contact_mesh_mm2=round(bed,3),bed_contact_brep_mm2=round(bed_brep,3))
    if abs(volume-body.volume*1000)>allowance*curved+0.05:failures.append('volume differs beyond tessellation')
    if abs(area-body.area*100)>0.002*body.area*100+0.05:failures.append('surface area differs beyond tessellation')
    if bed_brep<=0 or abs(bed-bed_brep)>0.01*bed_brep+0.05:failures.append('bed contact face differs')
    zmin=min(v[2] for v in verts);metrics['mesh_min_z_mm']=zmin
    if abs(zmin)>1e-4:failures.append('mesh does not sit on the bed at z=0')
    bb=body.boundingBox
    box=[max(abs(min(v[k] for v in verts)-bb.minPoint.asArray()[k]*10),
             abs(max(v[k] for v in verts)-bb.maxPoint.asArray()[k]*10)) for k in range(3)]
    metrics['box_deviation_mm']=[round(x,4) for x in box]
    if max(box)>allowance:failures.append('bed-pose bounding box differs')
    grid=_triangle_grid(raw,allowance)
    samples=[]
    for f in body.faces:samples.append(('face',f.pointOnFace))
    for e in body.edges:samples.append(('edge',e.pointOnEdge))
    for v in body.vertices:samples.append(('vertex',v.geometry))
    missing=[]
    for kind,pt in samples:
        p=(pt.x*10,pt.y*10,pt.z*10)
        cand=grid.get(tuple(math.floor(c/5.0) for c in p),[])
        d2=min((_distance2(p,*raw[i]) for i in cand),default=float('inf'))
        if d2>allowance*allowance:missing.append((kind,tuple(round(c,3) for c in p)))
    metrics['brep_samples']=len(samples);metrics['brep_samples_not_in_mesh']=len(missing)
    if missing:failures.append('%d B-Rep samples are missing from the mesh, e.g. %s'%(len(missing),missing[:3]))
    return {'part':name,'file':os.path.relpath(path,ROOT) if path.startswith(ROOT) else path,
            'chord_gate_mm':chord_gate_mm,'pass':not failures,'failures':failures,'metrics':metrics}


def audit_inventory(_context=''):
    os.makedirs(EVIDENCE,exist_ok=True)
    R.ref_assert();R.placed_assert()
    rows={}
    for name,relative,side in PARTS:
        path=os.path.join(ROOT,'first_article_stl',relative)
        candidate='/tmp/biped-audit-'+name+'.stl'
        R.guarded(export_comparison_mesh,name,side,candidate)
        released=mesh_signature(path);fresh=mesh_signature(candidate)
        rows[name]={'file':'first_article_stl/'+relative,'released':released,
                    'fresh_fusion_export':fresh,
                    'exact_geometry_match':released['geometry_sha256']==fresh['geometry_sha256'],
                    'shape':shape_signature(name)}
    report={'document':adsk.core.Application.get().activeDocument.name,
            'version':adsk.core.Application.get().activeDocument.dataFile.versionNumber,
            'dimensional_contracts':dimensional_contracts(),'parts':rows}
    with open(os.path.join(EVIDENCE,'inventory.json'),'w') as s:json.dump(report,s,indent=2)
    print(json.dumps({'parts':{k:v['exact_geometry_match'] for k,v in rows.items()},
                      'failed_interfaces':[r for r in report['dimensional_contracts'] if not r['pass']]}))


def _mesh_triangles(path):
    data=open(path,'rb').read()
    return [[tuple(r[j:j+3]) for j in (3,6,9)]
            for r in (struct.unpack_from('<12fH',data,84+50*i)
                      for i in range(struct.unpack_from('<I',data,80)[0]))]


def _distance2(p,a,b,c):
    # Closest point on a triangle, including its edges and vertices.
    sub=lambda x,y:tuple(x[i]-y[i] for i in range(3))
    dot=lambda x,y:sum(x[i]*y[i] for i in range(3))
    ab,ac,ap=sub(b,a),sub(c,a),sub(p,a)
    d1,d2=dot(ab,ap),dot(ac,ap)
    if d1<=0 and d2<=0:return dot(ap,ap)
    bp=sub(p,b);d3,d4=dot(ab,bp),dot(ac,bp)
    if d3>=0 and d4<=d3:return dot(bp,bp)
    vc=d1*d4-d3*d2
    if vc<=0 and d1>=0 and d3<=0:
        t=d1/(d1-d3);q=tuple(a[i]+t*ab[i] for i in range(3))
    else:
        cp=sub(p,c);d5,d6=dot(ab,cp),dot(ac,cp)
        if d6>=0 and d5<=d6:return dot(cp,cp)
        vb=d5*d2-d1*d6
        if vb<=0 and d2>=0 and d6<=0:
            t=d2/(d2-d6);q=tuple(a[i]+t*ac[i] for i in range(3))
        else:
            va=d3*d6-d5*d4
            if va<=0 and d4-d3>=0 and d5-d6>=0:
                t=(d4-d3)/((d4-d3)+(d5-d6));q=tuple(b[i]+t*(c[i]-b[i]) for i in range(3))
            else:
                den=va+vb+vc
                if abs(den)<1e-20:return min(dot(ap,ap),dot(bp,bp),dot(cp,cp))
                v,w=vb/den,vc/den
                q=tuple(a[i]+ab[i]*v+ac[i]*w for i in range(3))
    delta=sub(p,q);return dot(delta,delta)


def compare_mesh_surfaces(first,second,tolerance=.03):
    """Bidirectional vertices + face-centroid sampling; tolerance is tessellation
    QA in mm, not an allowance added to any fit dimension. Exact native faces
    independently own the fit dimensions. Full triangle identity is preferred.
    """
    meshes=[_mesh_triangles(p) for p in (first,second)]
    results=[]
    for src,dst in (meshes,meshes[::-1]):
        grid={};cell=5.0
        for idx,t in enumerate(dst):
            lo=[math.floor((min(v[i] for v in t)-tolerance)/cell) for i in range(3)]
            hi=[math.floor((max(v[i] for v in t)+tolerance)/cell) for i in range(3)]
            for x in range(lo[0],hi[0]+1):
                for y in range(lo[1],hi[1]+1):
                    for z in range(lo[2],hi[2]+1):grid.setdefault((x,y,z),[]).append(idx)
        points=set(v for t in src for v in t)
        points.update(tuple(sum(v[i] for v in t)/3 for i in range(3)) for t in src)
        worst=0;bad=0;worst_point=None
        for p in points:
            indices=grid.get(tuple(math.floor(v/cell) for v in p),[])
            d2=min((_distance2(p,*dst[i]) for i in indices),default=float('inf'))
            if d2>tolerance*tolerance:bad+=1
            if d2>worst:worst=d2;worst_point=p
        results.append({'samples':len(points),'outside_tolerance':bad,'worst_point_mm':worst_point,
                        'maximum_sample_distance_mm':math.sqrt(worst) if math.isfinite(worst) else None})
    return {'tolerance_mm':tolerance,'directions':results,
            'pass':all(r['outside_tolerance']==0 for r in results)}


def assert_export(name,path):
    """Gate a staged bed-ready mesh; never updates the baseline.

    Exact: the triangle fingerprint equals the pinned release. Otherwise the
    mesh must pass mesh_fidelity() at the release chord. assert_part() has
    already proved the B-Rep equals the reviewed shape.
    """
    if name not in {r[0] for r in PARTS}:return
    if adsk.core.Application.get().activeDocument.name!='Beni_SingleLegRig':return
    baseline=json.load(open(BASELINE))['parts'][name]
    actual=mesh_signature(path)
    if actual['geometry_sha256']==baseline['fresh_fusion_export']['geometry_sha256']:
        return dict(actual,gate='exact pinned tessellation')
    report=mesh_fidelity(name,path)
    if not report['pass']:
        raise RuntimeError('Exported mesh/orientation differs from reviewed Fusion geometry: %s %s'
                           %(name,json.dumps(report['failures'])))
    return dict(actual,gate='B-Rep fidelity',fidelity=report['metrics'])


def pinned_release_current(name, path):
    """True when path is the pinned release and still matches the reviewed B-Rep.

    Exporters keep such a file instead of rewriting it, so an unchanged part
    produces no churn on a machine whose tessellation differs.
    """
    row=json.load(open(BASELINE))['parts'].get(name)
    if row is None or not os.path.exists(path):return False
    if os.path.realpath(path)!=os.path.realpath(os.path.join(ROOT,row['file'])):return False
    if hashlib.sha256(open(path,'rb').read()).hexdigest()!=row['released_sha256']:return False
    return mesh_fidelity(name,path,chord_gate_mm=None)['pass']


def _write_baseline(baseline, action, names, reason):
    if not reason or len(reason.strip())<12:
        raise ValueError('A deliberate baseline change needs a written review reason')
    baseline.setdefault('review_log',[]).append(
        {'date':time.strftime('%Y-%m-%d'),'action':action,'parts':names,'reason':reason.strip()})
    with open(BASELINE,'w') as stream:json.dump(baseline,stream,indent=2)


def accept_shapes(names, reason):
    """Deliberate review step: live B-Rep shapes become the reviewed baseline.

    Update the dimensional contracts first for an intended interface change;
    every contract of each named part must pass. Never called by exporters.
    """
    assert adsk.core.Application.get().activeDocument.name=='Beni_SingleLegRig'
    baseline=json.load(open(BASELINE));contracts=dimensional_contracts();changes={}
    for name in names:
        bad=[c for c in contracts if c['part']==name and not c['pass']]
        if bad:raise RuntimeError('Contracts fail; fix geometry or contracts first: '+json.dumps(bad))
        old=baseline['parts'][name]['shape'];new=shape_signature(name)
        baseline['parts'][name]['shape']=new
        changes[name]={'volume_mm3':[[b['volume_mm3'] for b in old],[b['volume_mm3'] for b in new]],
                       'faces':[[len(b['faces']) for b in old],[len(b['faces']) for b in new]]}
    _write_baseline(baseline,'accept_shapes',names,reason)
    return changes


def accept_released_files(names, reason):
    """Deliberate review step: pin release files that pass mesh_fidelity()."""
    assert adsk.core.Application.get().activeDocument.name=='Beni_SingleLegRig'
    baseline=json.load(open(BASELINE));pinned={}
    for name in names:
        assert_part(name)
        row=baseline['parts'][name];path=os.path.join(ROOT,row['file'])
        report=mesh_fidelity(name,path)
        if not report['pass']:raise RuntimeError('Release file fails fidelity: '+json.dumps(report))
        signature=mesh_signature(path)
        row['released_sha256']=signature['sha256']
        row['fresh_fusion_export']={k:signature[k] for k in ('sha256','triangles','geometry_sha256')}
        row['fidelity']=report['metrics'];pinned[name]=signature['sha256']
    _write_baseline(baseline,'accept_released_files',names,reason)
    return pinned


def accept_verified_sources(reason):
    """Deliberate review step: pin source hashes after Fusion verification.

    Run only after the changed sources were exercised in Fusion; assert_all()
    must pass with the modules imported from these exact files.
    """
    assert adsk.core.Application.get().activeDocument.name=='Beni_SingleLegRig'
    assert_all()
    baseline=json.load(open(BASELINE))
    baseline['verified_source_sha256']={s:hashlib.sha256(open(os.path.join(ROOT,s),'rb').read()).hexdigest()
                                        for s in VERIFIED_SOURCES}
    _write_baseline(baseline,'accept_verified_sources',VERIFIED_SOURCES,reason)
    return baseline['verified_source_sha256']


def regression_tests(_context=''):
    """Deliberately wrong B-Reps and mislabeled mesh must be rejected."""
    from types import SimpleNamespace
    import subprocess
    import tempfile
    import distal_first_article_fusion as D
    results={}
    original_occ=_occ
    actual=original_occ('Distal_Link_L')
    for label,diameter,y0,y1 in [('missing_receiver',16,64.5,84.5),
                                ('oversized_receiver',10.5,64.5,84.5),
                                ('short_receiver',16,83.5,84.5)]:
        damaged=M._tm().copy(actual.component.bRepBodies.item(0))
        cutter=D._cylinder(B.KX,B.KZ,diameter,y0,y1)
        assert M._tm().booleanOperation(damaged,cutter,adsk.fusion.BooleanTypes.DifferenceBooleanType)
        globals()['_occ']=lambda name: SimpleNamespace(component=SimpleNamespace(bRepBodies=[damaged])) if name=='Distal_Link_L' else original_occ(name)
        try:
            assert_part('Distal_Link_L')
        except RuntimeError:
            results[label]='REJECTED'
        else:
            raise AssertionError('Bad receiver escaped export guard: '+label)
        finally:
            globals()['_occ']=original_occ
    historical = subprocess.check_output(['git', 'show',
        '56b2507:first_article_stl/ordered_pin_integration/ABS_PINREV_Distal_Link_D10p30_D6x10_M4x40_PRINT_ORIENTED.stl'], cwd=ROOT)
    bad_path = os.path.join(tempfile.gettempdir(), 'biped-bad-sept22-distal.stl')
    with open(bad_path, 'wb') as stream: stream.write(historical)
    try:
        assert_export('Distal_Link_L',bad_path)
    except RuntimeError:
        results['mislabeled_D10p30_mesh']='REJECTED'
    else:
        raise AssertionError('Historical Ø16 mesh escaped export guard')
    before={name:shape_signature(name) for name,_,_ in PARTS}
    def scoped_revolve():
        length,direction,normal,point=M._cart_geometry()
        o=B.new_comp('AUDIT_REVOLVE_SCOPE')
        try:
            M._revolved_ring(o.component,point,length,0,15,0,12,'new')
            M._revolved_ring(o.component,point,length,0,15,0,2.5,'cut')
        finally:
            o.deleteMe()
    R.guarded(scoped_revolve)
    assert all(shape_signature(n)==s for n,s in before.items())
    results['overlapping_revolve_cut']='ALL 15 PRINTED PARTS UNCHANGED'
    results.update(R.guarded(_fidelity_controls))
    out_dir=_context or GATE_EVIDENCE
    os.makedirs(out_dir,exist_ok=True)
    with open(os.path.join(out_dir,'negative_controls.json'),'w') as s:json.dump(results,s,indent=2)
    print(json.dumps(results))


def _fidelity_controls():
    """Wrong meshes must fail mesh_fidelity(); the release-standard export must pass."""
    import subprocess
    import tempfile
    import distal_first_article_fusion as D
    tmp=tempfile.gettempdir();hub='Shoulder_Output_Hub_L';results={}
    def expect_reject(label,name,path):
        try:assert_export(name,path)
        except RuntimeError as error:results[label]='REJECTED: '+str(error)[:160];return
        raise AssertionError('Wrong mesh escaped the release gate: '+label)
    old=os.path.join(tmp,'biped-control-sept22-hub.stl')
    with open(old,'wb') as stream:stream.write(subprocess.check_output(['git','show',
        '56b2507:first_article_stl/ordered_pin_integration/ABS_PINREV_Shoulder_Output_Hub_D4p15_ROOT_D4x10_PRINT_ORIENTED.stl'],cwd=ROOT))
    expect_reject('sept22_hub_D4p25_sockets',hub,old)
    def low(em,geometry,path,bodies):
        options=em.createSTLExportOptions(geometry,path)
        options.meshRefinement=adsk.fusion.MeshRefinementSettings.MeshRefinementLow
        options.isBinaryFormat=True
        return options
    coarse=os.path.join(tmp,'biped-control-low-hub.stl')
    _export_body(bed_body(hub),coarse,low)
    expect_reject('coarse_low_preset_export',hub,coarse)
    source=M._tm().copy(_occ(hub).component.bRepBodies.item(0))
    x,z=B._receiver_centres(0,0,44,3,90.4)[0]
    plug=D._cylinder(x,z,B.ROOT_DOWEL_HUB_SOCKET_D+0.02,B.HUB_Y1-B.ROOT_DOWEL_HUB_DEPTH,B.HUB_Y1)
    assert M._tm().booleanOperation(source,plug,adsk.fusion.BooleanTypes.UnionBooleanType)
    filled=os.path.join(tmp,'biped-control-filled-socket-hub.stl')
    _export_body(bed_body(hub,source=source),filled)
    expect_reject('one_root_socket_filled',hub,filled)
    flipped=os.path.join(tmp,'biped-control-wrong-bed-face-hub.stl')
    _export_body(bed_body(hub,side='min'),flipped)
    expect_reject('wrong_bed_face',hub,flipped)
    good=os.path.join(tmp,'biped-control-release-standard-hub.stl')
    _export_body(bed_body(hub),good)
    gate=assert_export(hub,good)
    results['release_standard_export']={'accepted':gate['gate'],'triangles':gate['triangles'],
        'max_cylinder_chord_mm':(gate.get('fidelity') or {}).get('max_cylinder_chord_mm')}
    pinned=os.path.join(ROOT,json.load(open(BASELINE))['parts'][hub]['file'])
    results['pinned_release_file']={'accepted':assert_export(hub,pinned)['gate'],
                                    'retained_by_exporters':pinned_release_current(hub,pinned)}
    return results
