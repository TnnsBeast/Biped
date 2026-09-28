"""README gallery and assembly-guide images from the live R2A model.

Run through the Fusion MCP with Beni_R2A_SingleLeg active.  Presentation only:
appearances, visibility and temporary occurrence offsets.  Every call restores
the nominal pose and the light-bulb states it found; geometry is not touched
(the release gate's shape signatures ignore appearance).
"""
import math
import os
import time

import adsk.core
import adsk.fusion

import beni_lib as B
import r2a_lib as L

ROOT = os.path.dirname(os.path.realpath(__file__))
README_DIR = os.path.join(ROOT, 'docs', 'readme')
GUIDE_DIR = os.path.join(ROOT, 'docs', 'assembly', 'r2a')

LOOK = {
    'Plastic - Matte (Blue)': ('R2A_Crank_L', 'R2A_Crank_Cap_L', 'R2A_Lever_Cap_L',
                               'R2A_Encoder_Arm_L'),
    'Plastic - Matte (Gray)': ('R2A_Prox_Inboard_L', 'R2A_Prox_Outboard_L'),
    'Plastic - Matte (White)': ('R2A_Distal_Link_L', 'R2A_Knee_Pin_Cap_L',
                                'R2A_Encoder_Bracket_L'),
    'Plastic - Matte (Red)': ('R2A_Knee_Bumper_TPU_In', 'R2A_Knee_Bumper_TPU_Out'),
    'Plastic - Matte (Black)': ('REFERENCE_Cable_Wheel_Distal', 'REFERENCE_Cable_Knee_Loop',
                                'REFERENCE_Cable_Wheel_Proximal', 'REFERENCE_Cable_Encoder',
                                'REFERENCE_Cable_Knee_Actuator'),
    'Plastic - Matte (Green)': ('HW_AS5048A_PCB',),
    'Steel - Satin': ('HW_RodEnd_M5_Upper', 'HW_RodEnd_M5_Lower', 'HW_Rod_M5x86',
                      'HW_JamNut_M5', 'HW_Pin_D5x18_Crank', 'HW_Pin_D5x18_Lever',
                      'HW_DowelPin_D4x10_Crank', 'HW_DowelPin_D4x10_Lever',
                      'HW_DowelPin_D4x10_EncArm', 'HW_DowelPin_D10x35', 'HW_Bearing_6800',
                      'HW_Magnet_D6x2p5_Diametric', 'HW_SHCS_M3x12', 'HW_SHCS_M3x6',
                      'HW_SHCS_M3x10', 'HW_SHCS_M2p5x10'),
}


def _appearance(name):
    libs = adsk.core.Application.get().materialLibraries
    for i in range(libs.count):
        lib = libs.item(i)
        if lib.name != 'Fusion Appearance Library':
            continue
        for k in range(lib.appearances.count):
            a = lib.appearances.item(k)
            if a.name == name:
                return a
    return None


def apply_looks():
    L.assert_r2a_doc()
    n = 0
    for look, names in LOOK.items():
        a = _appearance(look)
        if a is None:
            continue
        for o in L.all_root_occs():
            if B.base_name(o.component.name) in names:
                for b in o.component.bRepBodies:
                    if b.appearance is None or b.appearance.name != look:
                        b.appearance = a
                        n += 1
    return n


def _settle(vp):
    vp.refresh()
    adsk.doEvents()
    time.sleep(0.4)
    vp.refresh()


def camera(eye_dir, target, extents, up=(0.0, 0.0, 1.0)):
    vp = adsk.core.Application.get().activeViewport
    cam = vp.camera
    cam.cameraType = adsk.core.CameraTypes.OrthographicCameraType
    t = adsk.core.Point3D.create(target[0] / 10, target[1] / 10, target[2] / 10)
    n = math.sqrt(sum(c * c for c in eye_dir))
    e = adsk.core.Point3D.create(t.x + 60 * eye_dir[0] / n, t.y + 60 * eye_dir[1] / n,
                                 t.z + 60 * eye_dir[2] / n)
    cam.target = t
    cam.eye = e
    cam.upVector = adsk.core.Vector3D.create(*up)
    cam.viewExtents = extents / 10.0
    cam.isFitView = False
    cam.isSmoothTransition = False
    vp.camera = cam
    _settle(vp)
    return vp


def save(vp, path, w=1600, h=1100):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    opt = adsk.core.SaveImageFileOptions.create(path)
    opt.width, opt.height = w, h
    opt.isAntiAliased = True
    opt.isBackgroundTransparent = True
    if not vp.saveAsImageFileWithOptions(opt):
        raise RuntimeError('image export failed: ' + path)
    return path


def show(hide=(), only=None):
    """Light-bulb set for one frame; returns the states to restore."""
    saved = [(o, o.isLightBulbOn) for o in L.all_root_occs()]
    for o in L.all_root_occs():
        nm = B.base_name(o.component.name)
        tag = o.attributes.itemByName('R2A', 'set')
        names = (nm, tag.value if tag else None)

        def hit(pre):
            # component/set names by prefix; occurrence names ('X:2') exactly
            return o.name == pre or any(n and n.startswith(pre) for n in names)
        if only is not None:
            on = any(hit(p) for p in only)
        else:
            on = not any(hit(p) for p in hide)
        o.isLightBulbOn = on
    return saved


def offset(names, vec):
    """Translate named occurrences (posed transforms) by vec mm; returns undo."""
    undo = []
    for o in L.all_root_occs():
        nm = B.base_name(o.component.name)
        tag = o.attributes.itemByName('R2A', 'set')
        if nm in names or (tag and tag.value in names) or o.name in names:
            m = list(o.transform2.asArray())
            undo.append((o, list(m)))
            m[3] += vec[0] / 10.0
            m[7] += vec[1] / 10.0
            m[11] += vec[2] / 10.0
            o.transform2 = B._as_matrix(m)
    return undo


def unoffset(undo):
    for o, m in undo:
        o.transform2 = B._as_matrix(m)


HIDE_ALWAYS = ('ABS_TEST_Wheel_Rim_NoTyre', 'REFERENCE_Cable')
OUTBOARD_SIDE = ('R2A_Prox_Outboard_L', 'REF_GIM6010-8:2', 'R2A_Encoder_Bracket_L',
                 'HW_AS5048A_PCB', 'R2A_SHCS_M3x16_Bracket', 'R2A_SHCS_M3x10_Actuator',
                 'R2A_SHCS_M3x12_Perimeter', 'R2A_Knee_Bumper_TPU_Out', 'R2A_Encoder_Arm_L',
                 'HW_Magnet_D6x2p5_Diametric', 'R2A_SHCS_M3x10_EncArm', 'Wheel_Rim_L',
                 'Wheel_Tyre_L')


def readme_images(_context=''):
    L.assert_r2a_doc()
    L.capture_nominal(force=True)
    out = []
    vis = show(hide=HIDE_ALWAYS)
    try:
        # 1. hero: the single-leg article on the Mode A stand
        L.r2a_pose(0.0, 80.0)
        vp = camera((0.55, 1.0, 0.45), (20.0, 60.0, -70.0), 420.0)
        out.append(save(vp, os.path.join(README_DIR, 'r2a_leg_iso.png'), 1800, 1200))
        # 2. outboard side view
        vp = camera((0.0, 1.0, 0.0), (35.0, 80.0, -75.0), 360.0)
        out.append(save(vp, os.path.join(README_DIR, 'r2a_leg_outboard.png'), 1600, 1200))
        L.r2a_restore()
        # 3. linkage exposed at three knee angles
        L.restore_bulbs(vis)
        vis = show(hide=HIDE_ALWAYS + OUTBOARD_SIDE + ('RIG_Stand', 'RIG_Cable'))
        for a in (51.0, 80.0, 150.0):
            L.r2a_pose(0.0, a)
            vp = camera((0.0, 1.0, 0.0), (45.0, 80.0, -70.0), 330.0)
            out.append(save(vp, os.path.join(README_DIR, 'r2a_linkage_a%03d.png' % int(a)), 1400, 1400))
        L.r2a_restore()
        # 4. knee and crank close-ups (nominal)
        vp = camera((0.25, 1.0, 0.2), (L.KX + 5.0, 75.0, L.KZ + 10.0), 120.0)
        out.append(save(vp, os.path.join(README_DIR, 'r2a_knee_detail.png'), 1400, 1000))
        vp = camera((0.25, 1.0, 0.2), (8.0, 75.0, 8.0), 130.0)
        out.append(save(vp, os.path.join(README_DIR, 'r2a_crank_detail.png'), 1400, 1000))
    finally:
        L.r2a_restore()
        L.restore_bulbs(vis)
    return out


def _frame(path, only, moves=(), eye=(0.7, 1.0, 0.55), target=(40.0, 80.0, -60.0),
           extents=330.0, pose=80.0):
    vis = show(only=only)
    undo = []
    try:
        L.r2a_pose(0.0, pose)
        for names, vec in moves:
            undo += offset(names, vec)
        vp = camera(eye, target, extents)
        return save(vp, path, 1500, 1100)
    finally:
        unoffset(undo)
        L.r2a_restore()
        L.restore_bulbs(vis)


def guide_images(ids=None):
    """Exploded views for docs/assembly/r2a_assembly_guide.md."""
    L.assert_r2a_doc()
    L.capture_nominal(force=True)
    kn = 'REF_GIM6010-8:2'
    OB, IB = 'HW_Bearing_6800 (5):2', 'HW_Bearing_6800 (5):1'
    # shoulder housing (M3x8 :2-:9), stand/plate/cover (M3x10 :8-:16) and
    # hub-to-output (M3x10 :2-:7) screws; the rest belong to moving groups
    STATIC_SCREWS = tuple(['HW_SHCS_M3x8 (10):%d' % i for i in range(2, 10)]
                          + ['HW_SHCS_M3x10 (10):%d' % i for i in range(2, 17)])
    frames = [
        ('A01_outboard_half', ('R2A_Prox_Outboard_L', OB, 'R2A_Knee_Bumper_TPU_Out'),
         [((OB,), (0, 25, 0)), (('R2A_Knee_Bumper_TPU_Out',), (0, 20, 0))],
         (0.5, 1.0, 0.6), (45.0, 90.0, -40.0), 260.0),
        ('A02_knee_actuator', ('R2A_Prox_Outboard_L', OB, 'R2A_Knee_Bumper_TPU_Out',
                               kn, 'R2A_SHCS_M3x10_Actuator'),
         [((kn,), (0, 45, 0)), (('R2A_SHCS_M3x10_Actuator',), (0, -25, 0))],
         (0.8, -0.9, 0.8), (10.0, 95.0, -10.0), 240.0),
        ('A03_crank', ('R2A_Prox_Outboard_L', kn, 'R2A_SHCS_M3x10_Actuator', 'R2A_Crank_L',
                       'R2A_SHCS_M3x10_Crank'),
         [(('R2A_Crank_L',), (0, -35, 0)), (('R2A_SHCS_M3x10_Crank',), (0, -60, 0))],
         (0.6, -1.0, 0.5), (0.0, 80.0, 0.0), 220.0),
        ('A04_pushrod', ('HW_RodEnd_M5', 'HW_Rod_M5x86', 'HW_JamNut_M5'), [],
         (0.0, -1.0, 0.0), (60.0, 75.0, -20.0), 170.0),
        ('A05_upper_rod_end', ('R2A_Prox_Outboard_L', kn, 'R2A_Crank_L', 'R2A_Crank_Cap_L',
                               'HW_DowelPin_D4x10_Crank', 'HW_Pin_D5x18_Crank', 'HW_RodEnd_M5',
                               'HW_Rod_M5x86', 'HW_JamNut_M5'),
         [(('R2A_Crank_Cap_L',), (0, -20, 0)), (('HW_DowelPin_D4x10_Crank',), (0, -10, 0)),
          (('HW_Pin_D5x18_Crank',), (0, -38, 0))],
         (0.6, -1.0, 0.5), (30.0, 75.0, 10.0), 170.0),
        ('A06_distal_lever', ('R2A_Distal_Link_L', 'R2A_Lever_Cap_L', 'HW_DowelPin_D4x10_Lever',
                              'HW_Pin_D5x18_Lever', 'HW_RodEnd_M5_Lower', 'HW_Rod_M5x86',
                              'HW_JamNut_M5'),
         [(('R2A_Lever_Cap_L',), (0, 20, 0)), (('HW_DowelPin_D4x10_Lever',), (0, 10, 0)),
          (('HW_Pin_D5x18_Lever',), (0, 38, 0))],
         (0.6, 1.0, 0.5), (L.P0[0], 80.0, L.P0[1] - 30.0), 190.0),
        ('A07_inboard_half', ('R2A_Prox_Inboard_L', IB, 'R2A_Knee_Bumper_TPU_In',
                              'Shoulder_Output_Hub_L', 'HW_DowelPin_D4x10_Root', 'HW_SHCS_M4x10',
                              'REF_GIM6010-8:1', 'Chassis_Shoulder_Plate_L', 'Shoulder_Cable_Cover_L',
                              'RIG_Stand', 'RIG_Cable_Post_A', 'RIG_Cable_Anchor_ModeA',
                              'HW_SHCS_M3x12_PostA') + STATIC_SCREWS,
         [(('R2A_Prox_Inboard_L', 'R2A_Knee_Bumper_TPU_In', IB), (0, 45, 0)),
          (('HW_SHCS_M4x10',), (0, 75, 0))],
         (0.7, 1.0, 0.5), (20.0, 60.0, -50.0), 380.0),
        ('A08_module', None,
         [(tuple(['R2A_Prox_Outboard_L', kn, 'R2A_SHCS_M3x10_Actuator', 'R2A_Crank_L',
                  'R2A_Crank_Cap_L', 'HW_DowelPin_D4x10_Crank', 'R2A_SHCS_M3x10_Crank',
                  'HW_Pin_D5x18_Crank', 'HW_RodEnd_M5_Upper', 'HW_RodEnd_M5_Lower', 'HW_Rod_M5x86',
                  'HW_JamNut_M5', 'R2A_Distal_Link_L', 'R2A_Lever_Cap_L', 'HW_DowelPin_D4x10_Lever',
                  'HW_Pin_D5x18_Lever', 'R2A_Knee_Bumper_TPU_Out', 'HW_DowelPin_D4x10_EncArm', OB,
                  'R2A_SHCS_M3x10_Crank', 'REF_GIM4305-10:1', 'Wheel_Hub_L', 'Wheel_Rim_L',
                  'Wheel_Tyre_L', 'HW_SHCS_M4x8', 'HW_SHCS_M3x8 (10):10', 'HW_SHCS_M3x8 (10):11',
                  'HW_SHCS_M3x8 (10):12', 'R2A_SHCS_M2p5x10_WheelMotor']),
           (0, 70, 0))],
         (0.7, 1.0, 0.5), (40.0, 90.0, -60.0), 420.0),
        ('A09_pin_and_screws', None,
         [(('R2A_SHCS_M3x12_Perimeter',), (0, 30, 0)), (('HW_DowelPin_D10x35',), (0, 50, 0)),
          (('R2A_Knee_Pin_Cap_L', 'R2A_SHCS_M3x6_PinCap'), (0, -25, 0))],
         (0.7, 1.0, 0.5), (60.0, 80.0, -60.0), 330.0),
        ('A10_encoder', None,
         [(('R2A_Encoder_Arm_L', 'HW_Magnet_D6x2p5_Diametric', 'R2A_SHCS_M3x10_EncArm'), (0, 25, 0)),
          (('R2A_Encoder_Bracket_L', 'HW_AS5048A_PCB', 'R2A_SHCS_M3x16_Bracket'), (0, 50, 0))],
         (0.6, 1.0, 0.45), (L.KX, 95.0, L.KZ), 150.0),
        ('A11_cables', None, [], (0.5, 1.0, 0.6), (20.0, 70.0, -70.0), 420.0),
        ('S01_service', None,
         [(('R2A_Encoder_Arm_L', 'HW_Magnet_D6x2p5_Diametric', 'R2A_SHCS_M3x10_EncArm',
            'R2A_Encoder_Bracket_L', 'HW_AS5048A_PCB', 'R2A_SHCS_M3x16_Bracket'), (0, 110, 0)),
          (('HW_DowelPin_D10x35',), (0, 55, 0)),
          (tuple(['R2A_Prox_Outboard_L', kn, 'R2A_SHCS_M3x10_Actuator', 'R2A_Crank_L',
                  'R2A_Crank_Cap_L', 'HW_DowelPin_D4x10_Crank', 'R2A_SHCS_M3x10_Crank',
                  'HW_Pin_D5x18_Crank', 'HW_RodEnd_M5_Upper', 'HW_RodEnd_M5_Lower', 'HW_Rod_M5x86',
                  'HW_JamNut_M5', 'R2A_Distal_Link_L', 'R2A_Lever_Cap_L', 'HW_DowelPin_D4x10_Lever',
                  'HW_Pin_D5x18_Lever', 'R2A_Knee_Bumper_TPU_Out', 'HW_DowelPin_D4x10_EncArm', OB,
                  'R2A_SHCS_M3x12_Perimeter', 'REF_GIM4305-10:1', 'Wheel_Hub_L', 'Wheel_Rim_L',
                  'Wheel_Tyre_L', 'HW_SHCS_M4x8', 'HW_SHCS_M3x8 (10):10', 'HW_SHCS_M3x8 (10):11',
                  'HW_SHCS_M3x8 (10):12', 'R2A_SHCS_M2p5x10_WheelMotor']), (0, 45, 0))],
         (0.7, 1.0, 0.5), (40.0, 100.0, -60.0), 440.0),
    ]
    out = []
    everything = tuple(B.base_name(o.component.name) for o in L.all_root_occs()
                       if B.base_name(o.component.name) not in HIDE_ALWAYS
                       and not B.base_name(o.component.name).startswith('REFERENCE_Cable'))
    for fid, only, moves, eye, target, ext in frames:
        if ids and fid not in ids:
            continue
        sel = only if only is not None else everything
        if fid == 'A11_cables':
            sel = everything + ('REFERENCE_Cable',)
        out.append(_frame(os.path.join(GUIDE_DIR, fid + '.png'), sel, moves, eye, target, ext))
    return out
