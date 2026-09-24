"""Capture assembly-manual views through Fusion MCP; restore all model state.

Only visibility, cameras and reversible occurrence transforms are used. Exploded
offsets are illustration spacing, never new manufacturing dimensions.
"""
import json
import math
import os
import sys
import time
import adsk.core
import adsk.fusion

ROOT = os.path.dirname(os.path.realpath(__file__))
OUT = os.path.join(ROOT, 'docs', 'assembly', 'manual', 'views')
sys.path.insert(0, ROOT)
import beni_lib as B
import rig_lib as R
import mechanical_spring_test_fusion as M


def center(o):
    b = o.boundingBox
    return [(getattr(b.minPoint, k) + getattr(b.maxPoint, k)) / 2
            for k in ('x', 'y', 'z')]


def run(_context: str):
    app = adsk.core.Application.get()
    assert app.activeDocument.name == 'Beni_SingleLegRig'
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    vp = app.activeViewport
    original_camera, original_style = vp.camera, vp.visualStyle
    occurrences = list(root.occurrences)
    bulbs = [(o, o.isLightBulbOn) for o in root.allOccurrences]
    transforms = R.xf_capture()
    counts = (root.occurrences.count, design.timeline.count)
    R.ref_assert()
    R.placed_assert()
    M._register_pose_classes()
    nominal = [(o, B.classify(o), list(o.transform2.asArray())) for o in occurrences]
    groups = {}
    for o in occurrences:
        groups.setdefault(o.component.name, []).append(o)
    g = lambda name: groups.get(name, [])
    plate = g('Chassis_Shoulder_Plate_L')
    stand = g('RIG_Stand')
    smotor = g('REF_GIM6010-8')
    wmotor = g('REF_GIM4305-10')
    hub = g('Shoulder_Output_Hub_L')
    prox = g('Proximal_Link_L')
    distal = g('Distal_Link_L')
    bearings = g('HW_Bearing_6800 (5)')
    dowels = g('HW_DowelPin_D4x10_Root')
    pin = g('HW_DowelPin_D10x35')
    stop = g(M.STOP)
    stop_pin = g('HW_DowelPin_D6x10')
    upper, lower, guide = g(M.UPPER), g(M.LOWER), g(M.GUIDE)
    clevis = sorted(g('HW_ClevisPin_M4x40'), key=lambda o:center(o)[2], reverse=True)
    washers = sorted(g('HW_Washer_M4'), key=lambda o:center(o)[2], reverse=True)
    bracket, spacer = g('Knee_Encoder_Bracket_L'), g(M.SPACER)
    whub, rim = g('Wheel_Hub_L'), g(M.RIM)
    cover, post = g('Shoulder_Cable_Cover_L'), g('RIG_Cable_Post_A')
    s3x10 = g('HW_SHCS_M3x10 (10)')
    s3x8 = g('HW_SHCS_M3x8 (10)')
    shoulder_screws = [o for o in s3x8 if center(o)[2] > -5]
    hub_screws = [o for o in s3x10 if abs(center(o)[0]) < 2 and abs(center(o)[2]) < 2]
    stand_screws = [o for o in s3x10 if center(o)[1] < 4.5]
    stop_screws = [o for o in s3x10 if center(o)[2] < -5]
    cover_screws = [o for o in s3x10 if center(o)[2] < 0 and center(o)[1] == 5.0]
    cover_screws += g('HW_SHCS_M3x12_PostA (1)')
    root_screws = g('HW_SHCS_M4x10 (10)')
    wheel_screws = g('HW_SHCS_M2p5x12 (10)')
    whub_screws = [o for o in s3x8 if center(o)[2] < -5]
    bracket_screws = g('HW_SHCS_M3x16 (10)')
    rim_screws = g('HW_SHCS_M4x8 (2)')
    os.makedirs(OUT, exist_ok=True)
    manifest = {'document': app.activeDocument.name, 'source_version': 29,
                'illustration_only': True, 'frames': {}}
    wanted=set(_context.split(',')) if _context else set()
    manifest_path=os.path.join(OUT,'manifest.json')
    if wanted and os.path.exists(manifest_path):
        with open(manifest_path) as f:
            manifest=json.load(f)
    outboard = (2.5, 1.3, 1.0)
    inboard = (-2.5, -1.3, 1.0)
    shoulder = smotor + plate + cover + post + hub + dowels
    leg = shoulder + prox + distal + bearings + wmotor + whub + pin + stop + stop_pin

    def frame(name, show, offsets=(), view=outboard, pose=0, focus=None, span=None):
        if wanted and name not in wanted:
            return
        R.xf_restore(transforms)
        if pose:
            B.pose(nominal, 0, pose)
        selected = {o.entityToken for o in show}
        for o in occurrences:
            o.isLightBulbOn = o.entityToken in selected
        arrows = []
        for items, delta in offsets:
            for o in items:
                target = center(o)
                tr = o.transform2
                p = tr.translation
                tr.translation = adsk.core.Vector3D.create(
                    p.x + delta[0], p.y + delta[1], p.z + delta[2])
                o.transform2 = tr
                arrows.append({'part':o.name, 'from':center(o), 'to':target})
        vp.visualStyle = adsk.core.VisualStyles.WireframeWithVisibleEdgesOnlyVisualStyle
        cam = vp.camera
        cam.cameraType = adsk.core.CameraTypes.OrthographicCameraType
        target = focus or [sum(center(o)[i] for o in show)/len(show) for i in range(3)]
        cam.target = adsk.core.Point3D.create(*target)
        cam.eye = adsk.core.Point3D.create(*[target[i]+view[i]*50 for i in range(3)])
        cam.upVector = adsk.core.Vector3D.create(0,0,1)
        cam.isSmoothTransition = False
        cam.isFitView = focus is None
        if span:
            cam.setExtents(span * vp.width / vp.height, span)
        vp.camera = cam
        if focus is None:
            vp.fit()
        vp.refresh()
        adsk.doEvents()
        time.sleep(0.15)
        vp.refresh()
        project = lambda xyz: list(vp.modelToViewSpace(adsk.core.Point3D.create(*xyz)).asArray())
        imagepath = os.path.join(OUT, name+'.png')
        opts = adsk.core.SaveImageFileOptions.create(imagepath)
        opts.width, opts.height = vp.width, vp.height
        opts.isBackgroundTransparent = True
        opts.isAntiAliased = True
        assert vp.saveAsImageFileWithOptions(opts)
        projected = []
        parts = {}
        for o in show:
            b=o.boundingBox
            pts=[project((x,y,z)) for x in (b.minPoint.x,b.maxPoint.x)
                 for y in (b.minPoint.y,b.maxPoint.y) for z in (b.minPoint.z,b.maxPoint.z)]
            projected += pts
            parts[o.name]={'center':project(center(o)), 'bbox':pts}
        for a in arrows:
            a['from'],a['to']=project(a['from']),project(a['to'])
        bounds=[min(p[0] for p in projected),min(p[1] for p in projected),
                max(p[0] for p in projected),max(p[1] for p in projected)]
        if focus:
            bounds=[vp.width/2-vp.height*.85,0,vp.width/2+vp.height*.85,vp.height]
        circles=[]
        for o in show:
            if o.component.name not in ('Shoulder_Output_Hub_L','Proximal_Link_L','Wheel_Hub_L',
                                       'Chassis_Shoulder_Plate_L','RIG_Stand'):
                continue
            for body in o.bRepBodies:
                for edge in body.edges:
                    circle=adsk.core.Circle3D.cast(edge.geometry)
                    if circle and (abs(circle.radius-.265)<.001 or abs(circle.radius-.225)<.001):
                        circles.append({'part':o.name,'radius_cm':circle.radius,
                                        'world':circle.center.asArray(),'point':project(circle.center.asArray())})
        points={}
        if pose:
            # Frozen upper spring-seat datum and owned spring free length, in mm.
            direction,length = B.cart_dir(pose)
            seat=(B.UX+direction[0]*M.UPPER_SEAT_S, B.LEG_Y_MID,
                  B.UZ+direction[1]*M.UPPER_SEAT_S)
            installed_length = length - M.TEST_DEAD
            end=(seat[0]+direction[0]*installed_length, seat[1],
                 seat[2]+direction[1]*installed_length)
            points['spring_seats']=[project(tuple(v/10 for v in seat)),project(tuple(v/10 for v in end))]
        manifest['frames'][name]={'file':name+'.png','width':vp.width,'height':vp.height,
                                 'bounds':bounds,'parts':parts,'arrows':arrows,
                                 'insert_circles':circles,'points':points,'knee_pose_deg':pose}
        print('Captured '+name)

    try:
        frame('00_overview',leg+stand+upper+lower+guide+clevis+washers+bracket+spacer+rim,view=(.85,2.2,.75))
        frame('01_bearings',prox+bearings,[(bearings[:1],(0,-4,0)),(bearings[1:],(0,4,0))])
        frame('02_hub_dowels',hub+dowels,[(dowels,(0,2.0,0))],view=(.6,2,.7))
        frame('03_plate_motor',smotor+plate+shoulder_screws,
              [(plate,(0,6,0)),(shoulder_screws,(0,10,0))])
        frame('04_stand',stand+smotor+plate+stand_screws,
              [(smotor+plate,(0,6,0)),(stand_screws,(0,9,0))])
        frame('05_cover',smotor+plate+cover+post+cover_screws,
              [(cover,(0,3,0)),(post,(0,6,0)),(cover_screws,(0,8,0))])
        frame('06_hub_motor',smotor+plate+cover+hub+dowels+hub_screws,
              [(hub+dowels,(0,5,0)),(hub_screws,(0,8,0))])
        frame('07_root',shoulder+prox+root_screws,
              [(prox,(0,6,0)),(root_screws,(0,9,0))])
        frame('08_wheel_motor',distal+wmotor+wheel_screws,
              [(wmotor,(0,4,0)),(wheel_screws,(0,-4,0))],view=inboard)
        frame('09_wheel_hub',distal+wmotor+whub+whub_screws,
              [(whub,(0,4,0)),(whub_screws,(0,6,0))])
        frame('10_knee_entry',prox+bearings+distal,[(distal,(5,0,0))])
        frame('11_knee_pin',prox+bearings+distal+pin,[(pin,(0,-5,0))],view=inboard,
              focus=(9,5,-8),span=12)
        frame('12_stop',prox+bearings+distal+pin+stop_pin+stop+stop_screws,
              [(stop_pin,(0,2,0)),(stop,(0,6,0)),(stop_screws,(0,8,0))],
              focus=(9,11,-8.5),span=13)
        frame('13_upper_eye',prox+upper,
              [(upper,(-2.0,0,-2.0))],pose=-8,view=(-2.5,1.3,.75),
              focus=(7,7.5,-5),span=10)
        frame('14_upper_pin',prox+upper+clevis[:1]+washers[:1],
              [(clevis[:1],(0,-4,0)),(washers[:1],(0,2,0))],view=inboard,pose=-8,
              focus=(7,6.5,-5),span=10)
        cart_direction,_ = B.cart_dir(-8)
        frame('15_guide',prox+upper+guide,
              [(guide,(4*cart_direction[0],0,4*cart_direction[1]))],pose=-8,
              view=(-2.5,1.3,.75))
        frame('16_lower_eye',prox+distal+upper+guide+lower+clevis+washers,
              [(lower,(-math.sqrt(3),0,1)),(clevis[1:],(0,-4,0)),(washers[1:],(0,2,0))],pose=-8,
              view=(-2.5,1.3,.75),focus=(6.5,7.5,-10),span=12)
        frame('17_keeper',prox+distal+bearings+pin+stop+stop_pin+bracket+spacer+bracket_screws,
              [(spacer,(0,2,0)),(bracket,(0,4,0)),(bracket_screws,(0,6,0))],
              focus=(9,11,-8),span=12)
        frame('18_shell',distal+wmotor+whub+rim+rim_screws,
              [(rim,(0,4,0)),(rim_screws,(0,7,0))])
        frame('19_final',leg+stand+upper+lower+guide+clevis+washers+bracket+spacer+rim,
              pose=-8,view=(.3,3,.3))
        frame('20_prox_inserts',prox,view=(0,3,.1))
        frame('21_wheel_inserts',whub,view=(.5,-2,.5))
        frame('22_flex',leg+stand+upper+lower+guide+clevis+washers+bracket+spacer+rim,
              pose=15,view=(.3,3,.3))
        frame('23_spring',prox+distal+upper+guide,pose=-8,
              view=(-2.5,1.3,.75),focus=(6.5,7.5,-8),span=14)
        frame('24_cartridge',upper+guide+lower,
              [(lower,(4*cart_direction[0],0,4*cart_direction[1]))],
              pose=-8,view=(-2.5,1.3,.75))
        frame('25_eye_guide',upper+guide,
              [(guide,(4*cart_direction[0],0,4*cart_direction[1]))],
              pose=-8,view=(-2.5,1.3,.75))
        frame('26_stand_inserts',stand,view=(0,3,.1))
        frame('27_plate_inserts',plate,view=(0,3,.1))
        frame('28_hub_inserts',hub,view=(0,3,.1))
    finally:
        R.xf_restore(transforms)
        for o,on in bulbs:
            o.isLightBulbOn=on
        vp.visualStyle=original_style
        vp.camera=original_camera
        vp.refresh()
    assert counts == (root.occurrences.count, design.timeline.count)
    assert all(max(abs(a-b) for a,b in zip(arr,o.transform2.asArray()))<1e-8 for o,arr in transforms)
    assert all(o.isLightBulbOn == on for o,on in bulbs)
    R.ref_assert()
    R.placed_assert()
    manifest['restoration']={'transforms':True,'visibility':True,'counts':True,'motor_guards':True}
    with open(os.path.join(OUT,'manifest.json'),'w') as f:
        json.dump(manifest,f,indent=2)
    print(json.dumps({'frames':len(manifest['frames']),'restored':True,'output':OUT}))
