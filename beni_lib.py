"""Shared geometry + modelling helpers for the Beni Prototype 1 Fusion build.

Coordinate system (assembly / global):
    X = forward (robot fore-aft)
    Y = left  (+Y = left leg outboard)
    Z = up
    Shoulder axis  = global Y axis through the origin.
    Left leg is built at +Y; right leg is mirrored in Phase 10.

All public dimensions in this module are millimetres.  Fusion's internal API
unit is centimetres, so every value handed to the API goes through cm().
"""

import math
import re
import adsk.core
import adsk.fusion

# ----------------------------------------------------------------- constants
A_NOM = 50.0                      # nominal link angle from downward vertical
L1 = 120.0                        # proximal link length
L2 = 120.0                        # distal link length
PHI_EXT = -8.0                    # knee extension stop
PHI_BUMP = 20.0                   # bumper engagement
PHI_DESIGN = 25.0                 # main flexion design point
PHI_STOP = 27.0                   # physical hard stop

RU = 36.0                         # upper cartridge pivot radius from knee
RL = 54.0                         # lower cartridge pivot radius from knee
CART_ANG = 110.0                  # included anchor angle at nominal

WHEEL_OD = 110.0

# --- sagittal skeleton, nominal pose, global frame (Y omitted) -------------
_a = math.radians(A_NOM)
KX = L1 * math.sin(_a)            #  91.9253
KZ = -L1 * math.cos(_a)           # -77.1345
WX = 0.0
WZ = -(L1 + L2) * math.cos(_a)    # -154.2690

# cartridge anchors: bisector of the anchor pair points straight aft (180 deg
# in the knee-local frame, where local x == global X and local y == global Z).
_u_ang = math.radians(180.0 - CART_ANG / 2.0)      # 125 deg
_l_ang = math.radians(180.0 + CART_ANG / 2.0)      # 235 deg
UX = KX + RU * math.cos(_u_ang)   #  71.2764
UZ = KZ + RU * math.sin(_u_ang)   # -47.6455
LX = KX + RL * math.cos(_l_ang)   #  60.9516
LZ = KZ + RL * math.sin(_l_ang)   # -121.3718

# link axis directions in the knee-local frame, degrees measured atan2(z, x)
PROX_DIR = 180.0 - A_NOM + 10.0   # placeholder, see prox_angle()
PROX_ANG = math.degrees(math.atan2(-KZ, -KX))      # K -> shoulder = 140 deg
DIST_ANG = math.degrees(math.atan2(WZ - KZ, WX - KX))  # K -> wheel  = 220 deg

# ----------------------------------------------------------- lateral layout
# FROZEN left-leg lateral stack.  Right leg is mirrored about Y=0 in Phase 10.
SHOULDER_Y = 42.0                 # shoulder motor housing mount face (8xM3 @74 PCD)
SH_PLATE_T = 5.0
SH_PLATE_Y0 = 42.0
SH_PLATE_Y1 = 47.0
SH_PLATE_OD = 96.0
SH_BOLT_PCD = 74.0
SH_BOLT_A0 = 22.6                 # first housing bolt, global XZ angle
SH_OUT_PCD = 25.0                 # output flange 6x M3
SH_OUT_A0 = 30.4
SH_PIN_PCD = 20.4                 # output 3x O4 anti-rotation pins
SH_PIN_A0 = 60.4
SH_OUT_FACE_Y = 45.5
SH_PIN_TIP_Y = 49.0
SH_PILOT_D = 34.0                 # output pilot boss O34, y 44..45
SH_ROTOR_D = 46.0                 # rotating face O46 at y=44

HUB_Y0 = 45.5                     # hub inner face on motor output face
HUB_MID_Y = 51.5                  # hub body -> flange step (8 mm flange)
HUB_Y1 = 59.5                     # hub outboard face == leg inboard face
HUB_BODY_D = 38.0
HUB_FLANGE_D = 56.0
HUB_LINK_PCD = 44.0               # 6x M4 link bolts into hub flange, 7 mm thread
HUB_LINK_A0 = 0.4
HUB_CABLE_R = 21.0                # cable pass-through in hub flange

CAV_R_IN = 20.0                   # cable spiral cavity
CAV_R_OUT = 32.0
CAV_LIP_T = 1.5
CAV_Y0 = 47.0
CAV_Y1 = 51.0                     # lip top, 0.5 mm below hub flange underside
CABLE_D = 3.0
CABLE_COVER_Y0 = 51.5
CABLE_COVER_T = 2.0
CABLE_COVER_R_IN = 30.0           # 2 mm radial gap to the O56 rotating hub flange
CABLE_COVER_R_OUT = 47.0
CABLE_COVER_PCD = 88.0

LEG_Y_IN = 59.5
LEG_W = 30.0

# ---------------------------------------------------------- chassis geometry
# Reverse-engineered from the model on 2026-08-08.  These four parts had no
# builder at all, and build_shoulder_plate() had drifted to an older revision
# of the panel, so build_all() would have silently deleted the chassis joint.
SH_PANEL_X0, SH_PANEL_Z0 = -72.0, -24.0      # side panel outline
SH_PANEL_X1, SH_PANEL_Z1 = 42.0, 72.0
SH_PANEL_WINDOWS = [(-70.0, -6.0, -54.0, 46.0),
                    (-50.0, 50.0, -10.0, 66.0),
                    (-2.0, 50.0, 30.0, 66.0),
                    (22.0, -15.0, 38.0, 35.0)]
# Panel <-> frame bolted joint.  Single source of truth for both parts.
FRAME_BOLTS = [(-60.0, 62.0), (30.0, 62.0), (-60.0, 48.0), (30.0, 48.0),
               (-60.0, -18.0)]
FRAME_T = 4.0
FRAME_FLANGE_Y = 38.0                        # flange inner face; outer at 42
FRAME_FLANGE_RECTS = [(-70.0, -20.0, -56.0, 72.0),
                      (-70.0, 58.0, 40.0, 72.0),
                      (26.0, 36.0, 40.0, 72.0)]
FRAME_WEB_RECTS = [(-70.0, -20.0, -66.0, 4.0),
                   (-70.0, 46.0, -66.0, 72.0),
                   (-70.0, 68.0, -46.0, 72.0),
                   (16.0, 68.0, 40.0, 72.0),
                   (36.0, 36.0, 40.0, 72.0)]
TRAY_X0, TRAY_Z0, TRAY_X1, TRAY_Z1 = -64.0, -16.0, -62.0, 40.0
TRAY_HALF_W = 38.0
# battery moved aft: X was -35..34 (centre -0.5), now -65..4 (centre -30.5)
BATT_X0, BATT_Z0, BATT_X1, BATT_Z1 = -65.0, 42.0, 4.0, 67.0
BATT_HALF_W = 22.5
BATT_MASS_G = 250.0
# compute + IMU + PDB + wiring, previously an unmodelled 120 g BOM line.
# It has to sit AFT of the shoulder motors: both motors are Ø80 cylinders about
# the Y axis spanning |y| = 5..49, so the whole region r < 40 from the shoulder
# axis is motor territory regardless of y.  X <= -42 clears it at every Z.
# Aft face stops 0.5 mm clear of Electronics_Tray (X = -64..-62); top face
# stops 2 mm clear of the battery (Z >= 42).
ELEC_X0, ELEC_Z0, ELEC_X1, ELEC_Z1 = -61.5, 0.0, -44.0, 40.0
ELEC_HALF_W = 25.0
ELEC_MASS_G = 120.0
IMU_X, IMU_Z0, IMU_Z1 = -52.0, 40.0, 41.5   # IMU datum pad, on the top face
IMU_PAD = 12.0
SPIRAL_Y0, SPIRAL_T = 47.2, 3.6
SPIRAL_R_IN, SPIRAL_R_OUT = 20.2, 31.8

LEG_Y_OUT = LEG_Y_IN + LEG_W      # 89.5
ARM_T = 5.0
CH_Y0 = LEG_Y_IN + ARM_T          # 64.5  channel inboard face
CH_Y1 = LEG_Y_OUT - ARM_T         # 84.5  channel outboard face
LEG_Y_MID = (LEG_Y_IN + LEG_Y_OUT) / 2.0   # 74.5  spring centre plane
ROOT_PLATE_T = 8.0                # thickened arm-A root pad for M4 counterbores
ROOT_PLATE_Y1 = LEG_Y_IN + ROOT_PLATE_T    # 67.5
ROOT_DISC_D = 62.0

# --- knee bearing stack (frozen) -------------------------------------------
KNEE_BOSS_D = 26.0                # proximal arm knee boss OD
KNEE_BOSS_A_Y0 = 58.7             # arm A boss, thickened 0.8 mm inboard
KNEE_BOSS_A_Y1 = 64.5
KNEE_BOSS_B_Y0 = 84.5
KNEE_BOSS_B_Y1 = 90.3
# DFM datum: the proximal arm-B outer face is coplanar with its bearing boss.
# The old 89.5 mm arm face left only the O38 boss at Y=90.3 available as a
# bearing-axis-vertical bed contact.  Extending the arm by the existing 0.8 mm
# boss allowance creates a broad face-flat print datum without changing the
# frozen 58.7...90.3 mm knee envelope or any bearing/insert plane.
PROX_PRINT_FACE_Y = KNEE_BOSS_B_Y1
BRG1_Y0, BRG1_Y1 = 58.7, 63.7     # 6800 in arm A
BRG2_Y0, BRG2_Y1 = 85.3, 90.3     # 6800 in arm B
KNEE_LIP_D = 17.0                 # 0.8 mm retaining lip behind each bearing
SLEEVE_Y0, SLEEVE_Y1 = 63.7, 85.3 # steel sleeve O16/O10 x 21.6
DBOSS_Y0, DBOSS_Y1 = 65.0, 84.0   # printed distal knee boss, 19 mm
DBOSS_D = 22.0                    # must clear cartridge envelope at phi = -8
AXLE_Y0, AXLE_Y1 = 58.7, 90.3     # O10 axle journal span
AXLE_FLANGE_D = 15.0
AXLE_FLANGE_T = 3.0
AXLE_FLANGE_Y0 = AXLE_Y0 - AXLE_FLANGE_T   # 55.7
MAG_CARRIER_Y0 = AXLE_Y1          # 90.3
MAG_CARRIER_T = 6.0
MAG_D = 6.0
MAG_T = 2.5
ENC_PCB_Y = 97.8                  # 1.5 mm air gap to magnet face at 96.3

WM_PLATE_Y0 = LEG_Y_IN            # 59.5 distal wheel-end plate inboard face
WM_PLATE_T = 8.0
WM_MOUNT_Y = 67.5                 # wheel motor housing mount face
WM_BOLT_PCD = 47.5
WM_BOLT_A0 = 29.4                 # 6x M2.5, global XZ angle, 60 deg spacing
WM_COVER_D = 41.5                 # clearance hole for motor driver cover
WM_OUT_FACE_Y = 94.5              # wheel motor output flange face
WM_OUT_PCD = 27.0                 # 3x M3
WM_OUT_A0 = -28.7                 # 120 deg spacing
WM_FLANGE_D = 37.0

WHEEL_Y0 = 69.0                   # rim/tyre inboard edge
WHEEL_Y1 = 99.0                   # rim/tyre outboard edge
WHEEL_HUB_Y1 = 100.5
RIM_ID = 58.0
RIM_OD = 96.0
TRACK = 2 * 84.0                  # 168 mm

# ------------------------------------------------------------- hardware sizes
KNEE_AXLE_D = 10.0
KNEE_BRG_OD = 19.0                  # real 6800-2RS hardware envelope
# ABS first-article printed seat selected by the owner on 2026-08-31 from the
# O19.05..O19.25 ladder: firm thumb pressure, square seating, no rock, removable.
# This is process compensation, not a change to the bearing model.  Recalibrate
# before any PA-CF structural release.
ABS_KNEE_BRG_SEAT_D = 19.10
KNEE_BRG_W = 5.0
KNEE_SLEEVE_OD = 16.0
CART_PIN_D = 4.0
ROD_D = 5.0
SPRING_OD = 19.0
SPRING_WIRE = 2.6
SPRING_FREE = 55.0
SPRING_RATE = 10.45


# ------------------------------------------------------------------- helpers
def cm(v):
    return v / 10.0


def p3(x, y, z):
    return adsk.core.Point3D.create(cm(x), cm(y), cm(z))


def v3(x, y, z):
    return adsk.core.Vector3D.create(cm(x), cm(y), cm(z))


def dirv(x, y, z):
    return adsk.core.Vector3D.create(x, y, z)


def app():
    return adsk.core.Application.get()


def design():
    return adsk.fusion.Design.cast(app().activeProduct)


def root():
    return design().rootComponent


_SUFFIX = re.compile(r'\s*\(\d+\)$')


def base_name(s):
    """Component name without Fusion's ' (N)' duplicate suffix."""
    return _SUFFIX.sub('', s)


def cname(occ):
    return base_name(occ.component.name)


def find_occ(name, parent=None):
    """Return the first occurrence whose (base) component name matches."""
    parent = parent or root()
    for i in range(parent.occurrences.count):
        o = parent.occurrences.item(i)
        if base_name(o.component.name) == name:
            return o
    return None


def find_all_occ(name, parent=None):
    """Every occurrence whose (base) component name matches."""
    parent = parent or root()
    out = []
    for i in range(parent.occurrences.count):
        o = parent.occurrences.item(i)
        if base_name(o.component.name) == name:
            out.append(o)
    return out


def rename_components():
    """Strip Fusion's ' (N)' suffixes so the browser and BOM read cleanly."""
    r = root()
    seen = set()
    fixed = 0
    for i in range(r.occurrences.count):
        c = r.occurrences.item(i).component
        b = base_name(c.name)
        if c.name != b and b not in seen:
            try:
                c.name = b
                fixed += 1
            except Exception:
                pass
        seen.add(base_name(c.name))
    return fixed


def new_comp(name, parent=None):
    """Create (or fetch) an empty child component under `parent`."""
    parent = parent or root()
    exist = find_occ(name, parent)
    if exist:
        return exist
    m = adsk.core.Matrix3D.create()
    occ = parent.occurrences.addNewComponent(m)
    occ.component.name = name
    return occ


def drop_comp(name, parent=None):
    """Delete EVERY occurrence whose component base-name matches.

    This used to delete only the first match, via find_occ().  That made every
    builder non-idempotent in two compounding ways: repeated placements piled
    up (57 M3 x 10 screws instead of 14 after one extra build), and because
    new_comp() reuses a surviving component, a second call appended a whole
    fresh body to it -- the 6800 bearing ended up as four stacked copies of
    itself.  A builder must be safe to call twice, so drop_comp has to clear
    the component out completely.
    """
    parent = parent or root()
    n = 0
    for i in range(parent.occurrences.count - 1, -1, -1):
        o = parent.occurrences.item(i)
        if base_name(o.component.name) == name:
            try:
                o.deleteMe()
                n += 1
            except Exception:
                pass
    return n


def mat(ex, ey, ez, t_mm):
    m = adsk.core.Matrix3D.create()
    m.setWithArray([ex[0], ey[0], ez[0], cm(t_mm[0]),
                    ex[1], ey[1], ez[1], cm(t_mm[1]),
                    ex[2], ey[2], ez[2], cm(t_mm[2]),
                    0, 0, 0, 1])
    return m


# ------------------------------------------------------- construction planes
def plane_y(comp, y_mm, name=None):
    """Construction plane parallel to XZ at global Y = y_mm."""
    pl = comp.constructionPlanes
    ipt = pl.createInput()
    ipt.setByOffset(comp.xZConstructionPlane,
                    adsk.core.ValueInput.createByReal(cm(y_mm)))
    p = pl.add(ipt)
    if name:
        p.name = name
    return p


def axis_y(comp, x_mm, z_mm, name=None):
    """Construction axis parallel to global Y through (x, z)."""
    sk = comp.sketches.add(comp.xZConstructionPlane)
    # XZ sketch plane: sketch x -> global X, sketch y -> global -Z
    pt = sk.sketchPoints.add(adsk.core.Point3D.create(cm(x_mm), cm(-z_mm), 0))
    ax = comp.constructionAxes
    ipt = ax.createInput()
    ipt.setByLine(adsk.core.InfiniteLine3D.create(pt.worldGeometry,
                                                 dirv(0, 1, 0)))
    a = ax.add(ipt)
    if name:
        a.name = name
    sk.isVisible = False
    return a


# ------------------------------------------------------------------ sketching
def sk_on_y(comp, y_mm):
    """Sketch on a plane parallel to XZ at global Y = y_mm.

    Sketch coordinates map as:  sketch (u, v) -> global (X=u, Z=-v).
    Use sxz() to convert a global (X, Z) pair into sketch coordinates.
    """
    pl = plane_y(comp, y_mm)
    pl.isLightBulbOn = False
    return comp.sketches.add(pl)


def sxz(x_mm, z_mm):
    """Global (X,Z) -> sketch point on a Y-normal sketch made by sk_on_y."""
    return adsk.core.Point3D.create(cm(x_mm), cm(-z_mm), 0)


def circle(sk, x_mm, z_mm, dia_mm):
    return sk.sketchCurves.sketchCircles.addByCenterRadius(
        sxz(x_mm, z_mm), cm(dia_mm / 2.0))


def circles_polar(sk, cx, cz, pcd, dia, count, start_deg):
    out = []
    for i in range(count):
        a = math.radians(start_deg + i * 360.0 / count)
        out.append(circle(sk, cx + pcd / 2.0 * math.cos(a),
                          cz + pcd / 2.0 * math.sin(a), dia))
    return out


def polyline(sk, pts_xz, closed=True):
    """pts_xz: list of global (X, Z) tuples."""
    lines = sk.sketchCurves.sketchLines
    made = []
    n = len(pts_xz)
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        a = pts_xz[i]
        b = pts_xz[(i + 1) % n]
        made.append(lines.addByTwoPoints(sxz(a[0], a[1]), sxz(b[0], b[1])))
    return made


def slot(sk, ax, az, bx, bz, width):
    """Rounded slot (obround) between two global XZ centres."""
    arcs = sk.sketchCurves.sketchArcs
    lines = sk.sketchCurves.sketchLines
    r = width / 2.0
    dx, dz = bx - ax, bz - az
    ln = math.hypot(dx, dz)
    ux, uz = dx / ln, dz / ln
    nx, nz = -uz, ux
    p1 = (ax + nx * r, az + nz * r)
    p2 = (bx + nx * r, bz + nz * r)
    p3_ = (bx - nx * r, bz - nz * r)
    p4 = (ax - nx * r, az - nz * r)
    lines.addByTwoPoints(sxz(*p1), sxz(*p2))
    arcs.addByThreePoints(sxz(*p2), sxz(bx + ux * r, bz + uz * r), sxz(*p3_))
    lines.addByTwoPoints(sxz(*p3_), sxz(*p4))
    arcs.addByThreePoints(sxz(*p4), sxz(ax - ux * r, az - uz * r), sxz(*p1))


def arc_sector(sk, cx, cz, r_in, r_out, a0_deg, a1_deg):
    """Closed annular sector profile, angles in degrees (a1 > a0, CCW)."""
    arcs = sk.sketchCurves.sketchArcs
    lines = sk.sketchCurves.sketchLines
    a0, a1 = math.radians(a0_deg), math.radians(a1_deg)
    am = (a0 + a1) / 2.0

    def pt(r, a):
        return (cx + r * math.cos(a), cz + r * math.sin(a))
    p_o0, p_o1 = pt(r_out, a0), pt(r_out, a1)
    p_i0, p_i1 = pt(r_in, a0), pt(r_in, a1)
    arcs.addByThreePoints(sxz(*p_o0), sxz(*pt(r_out, am)), sxz(*p_o1))
    lines.addByTwoPoints(sxz(*p_o1), sxz(*p_i1))
    arcs.addByThreePoints(sxz(*p_i1), sxz(*pt(r_in, am)), sxz(*p_i0))
    lines.addByTwoPoints(sxz(*p_i0), sxz(*p_o0))


# ------------------------------------------------------------------ features
_OPS = {
    'new': adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
    'join': adsk.fusion.FeatureOperations.JoinFeatureOperation,
    'cut': adsk.fusion.FeatureOperations.CutFeatureOperation,
    'inter': adsk.fusion.FeatureOperations.IntersectFeatureOperation,
}


def profiles(sk, want=None):
    """Return sketch profiles; `want` may be an index or list of indices."""
    ps = sk.profiles
    if want is None:
        col = adsk.core.ObjectCollection.create()
        for i in range(ps.count):
            col.add(ps.item(i))
        return col
    if isinstance(want, int):
        return ps.item(want)
    col = adsk.core.ObjectCollection.create()
    for i in want:
        col.add(ps.item(i))
    return col


def biggest_profile(sk):
    best, ba = None, -1
    for i in range(sk.profiles.count):
        p = sk.profiles.item(i)
        a = p.areaProperties(adsk.fusion.CalculationAccuracy.LowCalculationAccuracy).area
        if a > ba:
            best, ba = p, a
    return best


def extrude(comp, prof, dist_mm, op='new', start_mm=0.0, taper=0.0,
            symmetric=False, participants=None):
    """Extrude `prof` by dist_mm (signed) along the sketch normal.

    start_mm offsets the extrusion start along the same normal.
    """
    ext = comp.features.extrudeFeatures
    ipt = ext.createInput(prof, _OPS[op])
    if abs(start_mm) > 1e-9:
        st = adsk.fusion.OffsetStartDefinition.create(
            adsk.core.ValueInput.createByReal(cm(start_mm)))
        ipt.startExtent = st
    if symmetric:
        ipt.setSymmetricExtent(adsk.core.ValueInput.createByReal(cm(abs(dist_mm))),
                               True)
    else:
        ipt.setDistanceExtent(False,
                              adsk.core.ValueInput.createByReal(cm(dist_mm)))
    if taper:
        ipt.taperAngle = adsk.core.ValueInput.createByString('%g deg' % taper)
    if op in ('cut', 'inter'):
        # CRITICAL: without an explicit participant list Fusion applies the cut
        # to bodies outside the owning component.  That silently destroyed the
        # tyre and knee axle once; never leave it unset.  participantBodies
        # wants a plain Python list of BRepBody, not an ObjectCollection.
        if participants is None:
            bodies = [comp.bRepBodies.item(i) for i in range(comp.bRepBodies.count)]
        elif hasattr(participants, 'count') and not isinstance(participants, list):
            bodies = [participants.item(i) for i in range(participants.count)]
        else:
            bodies = list(participants)
        if not bodies:
            return None
        ipt.participantBodies = bodies
    elif participants:
        ipt.participantBodies = participants
    return ext.add(ipt)


def revolve(comp, prof, axis, angle_deg=360.0, op='new'):
    rf = comp.features.revolveFeatures
    ipt = rf.createInput(prof, axis, _OPS[op])
    ipt.setAngleExtent(False,
                       adsk.core.ValueInput.createByString('%g deg' % angle_deg))
    return rf.add(ipt)


def fillet_all(comp, body, radius_mm, pred=None):
    """Fillet every edge of `body` accepted by pred(edge)."""
    col = adsk.core.ObjectCollection.create()
    for e in body.edges:
        if pred is None or pred(e):
            col.add(e)
    if col.count == 0:
        return None
    ff = comp.features.filletFeatures
    ipt = ff.createInput()
    ipt.isRollingBallCorner = True
    ipt.edgeSetInputs.addConstantRadiusEdgeSet(
        col, adsk.core.ValueInput.createByReal(cm(radius_mm)), True)
    try:
        return ff.add(ipt)
    except Exception:
        return None


# parts that live on the centre line and must NOT be mirrored
CENTRE_PARTS = ('Chassis_Frame', 'Electronics_Tray', 'Battery_4S2200',
                'Chassis_Electronics')
# Knee_Spring_L is excluded from the mirror for a different reason: it is
# rebuilt on every set_pose(), and rebuild_spring() owns both sides itself.
NO_MIRROR = CENTRE_PARTS + ('Knee_Spring_L',)


def drop_mirror():
    """Delete every mirrored occurrence and the mirror feature itself."""
    r = root()
    n = 0
    for i in range(r.occurrences.count - 1, -1, -1):
        o = r.occurrences.item(i)
        if '(Mirror)' in o.component.name or '(Mirror)' in o.name:
            try:
                o.deleteMe(); n += 1
            except Exception:
                pass
    for f in list(r.features.mirrorFeatures):
        try:
            f.deleteMe()
        except Exception:
            pass
    return n


def build_mirror():
    """Regenerate the right leg as a fresh mirror of the finished left leg.

    THIS MUST RUN AFTER EVERY LEFT-SIDE CHANGE.  The original model mirrored
    once, early, and then kept editing the left leg: Fusion's mirror-to-new-
    component is not associative, so the right leg silently fell three parts
    and two cut features behind.  The right knee ended up with no axle, no
    sleeve and no spring, its proximal link kept none of the O34 hub-access
    bore, and its encoder bracket covered the three knee-stop screws.

    Rebuilding the mirror from scratch at the end of every build is the only
    thing that makes L/R divergence structurally impossible.  Verify with
    audit_lr_parity().
    """
    drop_mirror()
    r = root()
    col = adsk.core.ObjectCollection.create()
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        n = base_name(o.component.name)
        if n in NO_MIRROR:
            continue
        col.add(o)
    if col.count == 0:
        return None
    mf = r.features.mirrorFeatures
    ipt = mf.createInput(col, r.xZConstructionPlane)
    out = mf.add(ipt)
    # rebuild_spring owns both springs, so restore the pair after mirroring
    rebuild_spring(0.0)
    return out


# =========================================================================
#  Audit harness.  Every check here exists because its absence let a real
#  defect through: the fastener checks would have caught three screw faults
#  in the original model, and the parity check would have caught the stale
#  right leg immediately.
# =========================================================================

# Expected occurrence count per part, per side.  Anything else means a builder
# ran twice without clearing, or a placement pattern changed.
EXPECT_COUNT = {
    'HW_SHCS_M3x10': 14,      # 8 housing + 6 output hub
    'HW_SHCS_M3x8': 7,        # 4 cable cover + 3 wheel hub
    'HW_SHCS_M3x6': 3,        # knee stop arc
    'HW_SHCS_M4x10': 12,      # 6 link root + 6 rim
    'HW_SHCS_M2p5x12': 6,     # wheel motor
    'HW_SHCS_M3x16': 2,       # encoder bracket
    'HW_Bearing_6800': 2,
    'Cart_Preload_Shim_L': 4,
    'HW_ClevisPin_D4x32': 2,
}


def audit_counts(verbose=True):
    """Occurrence counts and one-body-per-component.

    Both halves of this check exist because drop_comp() used to delete only the
    first matching occurrence, which made every builder non-idempotent: screws
    accumulated and components silently grew extra stacked bodies.
    """
    r = root()
    cnt, bodies = {}, {}
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        nm = o.component.name
        b = base_name(nm.replace('(Mirror)', ''))
        side = 'R' if '(Mirror)' in nm else 'L'
        cnt[(b, side)] = cnt.get((b, side), 0) + 1
        bodies[nm] = o.component.bRepBodies.count
    problems = []
    for (b, side), n in sorted(cnt.items()):
        if b.startswith('REF_'):
            continue
        e = EXPECT_COUNT.get(b, 1)
        if n != e:
            problems.append('%-28s %s: %d occurrences, expected %d' % (b, side, n, e))
    for nm, n in sorted(bodies.items()):
        if nm.startswith('REF_'):
            continue
        if n != 1:
            problems.append('%-28s has %d bodies, expected 1' % (nm, n))
    if verbose:
        if problems:
            print('  COUNTS: %d PROBLEM(S)' % len(problems))
            for p in problems:
                print('     ' + p)
        else:
            print('  COUNTS: clean (%d part/side entries, 1 body each)' % len(cnt))
    return problems


def audit_lr_parity(verbose=True):
    """Compare every left part against its mirror by volume and face census."""
    r = root()
    left, right = {}, {}
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        nm = o.component.name
        b = base_name(nm.replace('(Mirror)', ''))
        if b in CENTRE_PARTS or b.startswith('REF_'):
            continue
        vol = sum(bd.volume * 1000.0 for bd in o.component.bRepBodies)
        nf = sum(bd.faces.count for bd in o.component.bRepBodies)
        d = right if '(Mirror)' in nm else left
        d.setdefault(b, []).append((round(vol, 3), nf))
    problems = []
    for b in sorted(set(list(left.keys()) + list(right.keys()))):
        L, R = left.get(b, []), right.get(b, [])
        if len(L) != len(R):
            problems.append('%-32s count L=%d R=%d' % (b, len(L), len(R)))
            continue
        for (vl, fl), (vr, fr) in zip(sorted(L), sorted(R)):
            if abs(vl - vr) > 0.01 or fl != fr:
                problems.append('%-32s vol L=%.3f R=%.3f  faces L=%d R=%d'
                                % (b, vl, vr, fl, fr))
    if verbose:
        if problems:
            print('  L/R PARITY: %d PROBLEM(S)' % len(problems))
            for p in problems:
                print('     ' + p)
        else:
            print('  L/R PARITY: clean (%d part families matched)' % len(left))
    return problems


# (screw name -> nominal length mm).  Used by audit_fasteners.
SCREW_LEN = {'HW_SHCS_M2p5x12': (2.5, 12.0), 'HW_SHCS_M3x6': (3.0, 6.0),
             'HW_SHCS_M3x8': (3.0, 8.0), 'HW_SHCS_M3x10': (3.0, 10.0),
             'HW_SHCS_M3x16': (3.0, 16.0), 'HW_SHCS_M4x10': (4.0, 10.0)}


def audit_fasteners(verbose=True):
    """Head-to-head clearance for every screw pair sharing a seat plane.

    An M3 SHCS head is O5.5.  Three knee-stop screws at 20 deg on a 15 mm
    radius put their centres 5.209 mm apart, so the heads overlapped and the
    set could not physically be fitted -- on the fastener set carrying the
    entire hard-stop crash load.  The original driver-access audit modelled 32
    hex-key envelopes and passed, because it only ever asked whether a tool
    could reach a screw, never whether two screws could coexist.
    """
    r = root()
    seats = {}
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        nm = base_name(o.component.name.replace('(Mirror)', ''))
        if nm not in SCREW_LEN:
            continue
        d, _L = SCREW_LEN[nm]
        hd = SHCS[d][0]
        b = bbox_of(o)
        cx, cz = (b[0] + b[1]) / 2.0, (b[4] + b[5]) / 2.0
        key = (nm, '(Mirror)' in o.component.name, round(b[2], 2), round(b[3], 2))
        seats.setdefault(key, []).append((cx, cz, hd))
    problems = []
    for key, pts in seats.items():
        for a in range(len(pts)):
            for bi in range(a + 1, len(pts)):
                x1, z1, h1 = pts[a]
                x2, z2, h2 = pts[bi]
                dist = math.hypot(x1 - x2, z1 - z2)
                need = (h1 + h2) / 2.0
                if dist < need:
                    problems.append(
                        '%s heads overlap by %.2f mm (centres %.3f, need %.2f)'
                        % (key[0], need - dist, dist, need))
    if verbose:
        if problems:
            print('  FASTENER HEAD CLEARANCE: %d PROBLEM(S)' % len(problems))
            for p in sorted(set(problems)):
                print('     ' + p)
        else:
            print('  FASTENER HEAD CLEARANCE: clean')
    return problems


def audit_blind_holes(verbose=True):
    """Insert bore depth vs insert length vs screw reach, stated explicitly.

    Both blind-insert joints in the original model were wrong in the same way:
    the bore was shorter than the 5 mm insert and the screw ran past the bore
    floor, so the insert stood proud and the screw bottomed out before it
    clamped anything.
    """
    rows = [
        ('knee stop arc -> proximal arm B',
         KNEE_BOSS_B_Y1 - STOP_INSERT_DEPTH, KNEE_BOSS_B_Y1, INSERT_LEN,
         STOP_ARC_Y0 + STOP_ARC_T, 6.0, KNEE_BOSS_B_Y0),
        ('encoder bracket -> proximal arm B',
         KNEE_BOSS_B_Y1 - ENC_INSERT_DEPTH, KNEE_BOSS_B_Y1, INSERT_LEN,
         101.9, 16.0, KNEE_BOSS_B_Y0),
        ('cable cover -> M3 inserts',
         CAV_Y0, CAV_Y0 + COVER_INSERT_DEPTH, INSERT_LEN,
         SH_PLATE_Y0, 8.0, None),
    ]
    problems = []
    if verbose:
        print('  %-34s %6s %6s %7s %7s %8s' %
              ('joint', 'bore', 'insert', 'screw', 'clear', 'floor'))
    for (name, y_floor, y_mouth, ilen, y_seat, slen, y_back) in rows:
        depth = abs(y_mouth - y_floor)
        # screw shank travels from its seat toward the bore
        if y_seat > y_mouth:
            y_tip = y_seat - slen
            clear = y_tip - min(y_floor, y_mouth)
        else:
            y_tip = y_seat + slen
            clear = max(y_floor, y_mouth) - y_tip
        floor = ('%.2f' % abs(min(y_floor, y_mouth) - y_back)) if y_back is not None else '-'
        if verbose:
            print('  %-34s %6.2f %6.2f %7.2f %+7.2f %8s'
                  % (name, depth, ilen, slen, clear, floor))
        if depth < ilen - 1e-6:
            problems.append('%s: bore %.2f is shallower than the %.2f insert'
                            % (name, depth, ilen))
        if clear < 0:
            problems.append('%s: screw runs %.2f mm past the bore floor'
                            % (name, -clear))
    if verbose:
        print('  BLIND HOLES: %s' % ('clean' if not problems else
                                     '%d PROBLEM(S)' % len(problems)))
        for p in problems:
            print('     ' + p)
    return problems


def audit_source_parity(verbose=True):
    """Every modelled part must have a builder, and vice versa."""
    built = set()
    for fn in (build_shoulder_plate, build_cable_cover, build_cable_spiral,
               build_shoulder_hub, build_proximal_link, build_distal_link,
               build_knee_hardware, build_cartridge, build_knee_stop,
               build_encoder, build_wheel, build_chassis_frame,
               build_electronics_tray, build_battery, build_electronics_block,
               build_fasteners):
        built.add(fn.__name__)
    r = root()
    present = set()
    for i in range(r.occurrences.count):
        n = base_name(r.occurrences.item(i).component.name.replace('(Mirror)', ''))
        if not n.startswith('REF_'):
            present.add(n)
    known = set(PART_CLASS.keys())
    orphan = sorted(p for p in present if p not in known)
    unused = sorted(k for k in known if k not in present)
    if verbose:
        print('  SOURCE PARITY: %d parts in model, %d classified' % (len(present), len(known)))
        for p in orphan:
            print('     modelled but not in PART_CLASS: %s' % p)
        for u in unused:
            print('     in PART_CLASS but not modelled: %s' % u)
    return orphan


def audit_all():
    print('=' * 74)
    print('BENI PROTOTYPE 1 -- AUTOMATED AUDIT')
    print('=' * 74)
    p = []
    p += audit_counts()
    print()
    p += audit_lr_parity()
    print()
    p += audit_fasteners()
    print()
    p += audit_blind_holes()
    print()
    audit_source_parity()
    print()
    print('TOTAL PROBLEMS: %d' % len(p))
    return p


# Interference pairs that are modelling artifacts or intended contact, not
# defects.  Each is a real overlap in the B-Rep for a reason that is understood;
# anything NOT on this list is a genuine clash.
def _artifact(na, nb, phi):
    """True if this interference pair is a known artifact or designed contact."""
    pair = {base_name(na.replace('(Mirror)', '')),
            base_name(nb.replace('(Mirror)', ''))}
    # a screw shank modelled at nominal diameter inside a tap-drill hole
    if any(n.startswith('HW_SHCS') for n in pair):
        return True
    # the magnet carrier's M4 male stud inside the axle's modelled tap drill
    if pair == {'Knee_Axle_L', 'Knee_Magnet_Carrier_L'}:
        return True
    # the shoulder motor's 3 x O4 output pins rotate WITH the hub in reality,
    # but the supplied STEP is one body so the rotor cannot be separated
    if 'Shoulder_Output_Hub_L' in pair and any('Body' in n or 'MOTOR_PART' in n
                                               or '6010' in n for n in pair):
        return True
    # the PU bumpers are SUPPOSED to be crushed by the stop dowel: the flexion
    # pad from phi = +20 and the extension pad from phi = -6.5
    if 'HW_DowelPin_D6x9' in pair:
        if 'Knee_Bumper_Flex_L' in pair and phi >= 19.9:
            return True
        if 'Knee_Bumper_Ext_L' in pair and phi <= -6.4:
            return True
    return False


def sweep_check(poses=None, verbose=True):
    """Pose the leg through `poses` and report only genuine interferences.

    Returns a list of (theta, phi, name_a, name_b, volume) for real clashes.
    Bumper crush is reported separately as a positive result -- it is how the
    hard stop is confirmed to engage where it was designed to.
    """
    if poses is None:
        poses = [(0, -8), (0, -6), (0, 0), (0, 5), (0, 10), (0, 15), (0, 20),
                 (0, 22), (0, 25), (0, 27),
                 (-185, 0), (-120, 0), (-60, 0), (30, 0), (60, 0), (120, 0),
                 (185, 0), (-35, 12),
                 (-185, -8), (-185, 27), (185, -8), (185, 27)]
    des = design()
    r = root()
    capture_nominal()
    bad, crush = [], []
    for (th, ph) in poses:
        set_pose(float(th), float(ph))
        col = adsk.core.ObjectCollection.create()
        for i in range(r.occurrences.count):
            col.add(r.occurrences.item(i))
        ipt = des.createInterferenceInput(col)
        ipt.areCoincidentFacesIncluded = False
        res = des.analyzeInterference(ipt)
        n_real = 0
        for i in range(res.count):
            it = res.item(i)
            v = it.interferenceBody.volume * 1000.0
            if v < 0.5:
                continue
            a, b = it.entityOne, it.entityTwo
            na = a.component.name if hasattr(a, 'component') else a.name
            nb = b.component.name if hasattr(b, 'component') else b.name
            if 'HW_DowelPin_D6x9' in (base_name(na.replace('(Mirror)', '')),
                                      base_name(nb.replace('(Mirror)', ''))):
                if _artifact(na, nb, float(ph)):
                    crush.append((th, ph, v))
                    continue
            if _artifact(na, nb, float(ph)):
                continue
            bad.append((th, ph, na, nb, v))
            n_real += 1
        if verbose:
            cr = [c for c in crush if c[0] == th and c[1] == ph]
            note = ''
            if cr:
                note = '   bumper crush %.1f mm3' % sum(c[2] for c in cr)
            print('  theta=%+5d phi=%+4d   real clashes: %d%s' % (th, ph, n_real, note))
    restore_nominal()
    rebuild_spring(0.0)
    design().activateRootComponent()
    if verbose:
        print()
        if bad:
            print('  GENUINE INTERFERENCES: %d' % len(bad))
            for th, ph, na, nb, v in bad:
                print('     theta=%+5d phi=%+4d  %8.2f mm3  %s <-> %s'
                      % (th, ph, v, na, nb))
        else:
            print('  NO GENUINE INTERFERENCES across %d poses' % len(poses))
    return bad


# =========================================================================
#  Physical materials.  Every body in the original model carried the default
#  "Steel", so Fusion reported the robot at 8174 g against a real 3.3 kg and
#  there was no usable CoM or inertia tensor anywhere -- which meant nothing
#  downstream (balance controller, URDF, sim) could be built at all.
#
#  Each entry is either a density in g/cm3, or an exact target mass in grams
#  for bodies that are ENVELOPES rather than true solids.  The envelopes are
#  the honest reason the old hand roll-up was 48 g out: the spring is modelled
#  as its full O19 outer cylinder, which at steel density weighs 51 g against
#  a real 25.3 g spring.  Giving the envelope an effective density makes the
#  assembly mass correct without pretending to model a swept helix.
# =========================================================================
MATERIAL_SPEC = {
    # class   library material         density   target mass (g)  note
    'PACF':   ('Nylon',               1.15,  None, 'PA-CF, printed'),
    'ABS':    ('ABS Plastic',         1.04,  None, 'ABS, printed'),
    'TPU':    ('Rubber',              1.20,  None, 'TPU 95A, printed'),
    'PU':     ('Rubber',              1.20,  None, 'polyurethane ~90A'),
    'ALU':    ('Aluminum',            2.81,  None, '7075-T6'),
    'STEEL':  ('Steel',               7.85,  None, 'steel'),
    'PCB':    ('ABS Plastic',         1.90,  None, 'FR4 assembly'),
    # envelopes / assemblies -- mass is specified, density is derived
    'SPRING': ('Steel',               None,  25.3, 'spring, modelled as its O19 envelope'),
    'BATT':   ('ABS Plastic',         None, 250.0, '4S 2200 mAh pack'),
    'ELEC':   ('ABS Plastic',         None, 120.0, 'compute + IMU + PDB + wiring'),
}
# per-part overrides where the body is an envelope or a bought assembly
MASS_OVERRIDE_G = {
    'HW_Bearing_6800': 6.5,              # solid ring modelled; real 6800-2RS
    'Shoulder_Cable_Spiral_L': 7.0,      # harness envelope, per shoulder
    'Knee_Spring_L': 25.3,
    'HW_Magnet_D6x2p5_Diametric': 0.53,  # NdFeB
    'Knee_Encoder_PCB_L': 2.0,           # AS5048A on a 14 x 14 board
}
# The two motor references are external STEP bodies whose modelled volume is
# not their real mass distribution, so they get an explicit mass each.
MOTOR_MASS_G = {'REF_GIM6010-8': 500.0, 'REF_GIM4305-10': 250.0}

_MAT_CACHE = {}


def _local_material(cls):
    """Get or create a design-local material for a material class.

    Library materials are read-only, so a density override needs a local copy
    (design.materials.addByCopy) whose structural_Density property we can set.
    """
    if cls in _MAT_CACHE:
        return _MAT_CACHE[cls]
    spec = MATERIAL_SPEC.get(cls)
    if spec is None:
        return None
    libname, dens, _mass, note = spec
    des = design()
    want = 'BENI_%s' % cls
    for i in range(des.materials.count):
        m = des.materials.item(i)
        if m.name == want:
            _MAT_CACHE[cls] = m
            return m
    src = None
    libs = app().materialLibraries
    for li in range(libs.count):
        lib = libs.item(li)
        if lib.name != 'Fusion Material Library':
            continue
        for mi in range(lib.materials.count):
            m = lib.materials.item(mi)
            if libname.lower() in m.name.lower():
                src = m
                break
        if src:
            break
    if src is None:
        return None
    local = des.materials.addByCopy(src, want)
    _MAT_CACHE[cls] = local
    return local


def _set_density(mat, g_per_cm3):
    """Set a local material's density in kg/m3 (Fusion's internal unit)."""
    try:
        prop = mat.materialProperties.itemById('structural_Density')
        if prop is None:
            for i in range(mat.materialProperties.count):
                p = mat.materialProperties.item(i)
                if 'density' in p.name.lower():
                    prop = p
                    break
        if prop is None:
            return False
        prop.value = g_per_cm3 * 1000.0
        return True
    except Exception:
        return False


def apply_materials(verbose=False):
    """Give every body a physical material with the right density.

    Bodies whose class or part name specifies a target mass get their own
    local material whose density is derived from the modelled volume, so
    Fusion's reported mass, CoM and inertia are all correct.
    """
    r = root()
    done, skipped = 0, []
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        raw = o.component.name
        part = base_name(raw.replace('(Mirror)', ''))
        if part.startswith('REF_') or part in MOTOR_MASS_G:
            continue
        cls = PART_CLASS.get(part)
        if cls is None:
            skipped.append(part)
            continue
        spec = MATERIAL_SPEC.get(cls)
        if spec is None:
            skipped.append(part)
            continue
        _lib, dens, cls_mass, _note = spec
        for b in o.component.bRepBodies:
            vol_cm3 = b.volume
            target = MASS_OVERRIDE_G.get(part, cls_mass)
            if target is not None and vol_cm3 > 1e-9:
                # this body needs its own density, so give it its own material
                key = 'PART_%s' % part
                if key in _MAT_CACHE:
                    mat = _MAT_CACHE[key]
                else:
                    base = _local_material(cls)
                    if base is None:
                        skipped.append(part)
                        continue
                    des = design()
                    mat = None
                    for k in range(des.materials.count):
                        if des.materials.item(k).name == 'BENI_' + part:
                            mat = des.materials.item(k)
                            break
                    if mat is None:
                        mat = des.materials.addByCopy(base, 'BENI_' + part)
                    _set_density(mat, target / vol_cm3)
                    _MAT_CACHE[key] = mat
                b.material = mat
            else:
                mat = _local_material(cls)
                if mat is None:
                    skipped.append(part)
                    continue
                if dens is not None:
                    _set_density(mat, dens)
                b.material = mat
            done += 1
    # the two motor references: one local material each, density from volume
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        part = base_name(o.component.name.replace('(Mirror)', ''))
        if part not in MOTOR_MASS_G:
            continue
        vol = 0.0
        stack = [o]
        while stack:
            cur = stack.pop()
            for b in cur.bRepBodies:
                vol += b.volume
            for j in range(cur.childOccurrences.count):
                stack.append(cur.childOccurrences.item(j))
        if vol <= 1e-9:
            continue
        des = design()
        want = 'BENI_%s' % part
        mat = None
        for k in range(des.materials.count):
            if des.materials.item(k).name == want:
                mat = des.materials.item(k)
                break
        if mat is None:
            base = _local_material('STEEL')
            if base is None:
                continue
            mat = des.materials.addByCopy(base, want)
        _set_density(mat, MOTOR_MASS_G[part] / vol)
        stack = [o]
        while stack:
            cur = stack.pop()
            for b in cur.bRepBodies:
                b.material = mat
                done += 1
            for j in range(cur.childOccurrences.count):
                stack.append(cur.childOccurrences.item(j))
    if verbose and skipped:
        print('  no material for: %s' % sorted(set(skipped)))
    return done


def mass_report(verbose=True):
    """Fusion's own mass properties, once the materials are right.

    Returns a dict with mass (g), CoM (mm) and the inertia tensor about the
    CoM (kg m2).  This is the handoff to controls: without it there is no
    balance model and no URDF.
    """
    des = design()
    r = des.rootComponent
    acc = adsk.fusion.CalculationAccuracy.HighCalculationAccuracy
    pp = r.getPhysicalProperties(acc)
    m_g = pp.mass * 1000.0
    com = (pp.centerOfMass.x * 10, pp.centerOfMass.y * 10, pp.centerOfMass.z * 10)
    ok, xx, yy, zz, xy, yz, xz = pp.getXYZMomentsOfInertia()
    # Fusion returns kg*cm2 about the world origin; convert and shift to CoM
    f = 1e-4                      # kg cm2 -> kg m2
    Ixx, Iyy, Izz = xx * f, yy * f, zz * f
    Ixy, Iyz, Ixz = xy * f, yz * f, xz * f
    M = pp.mass
    cx, cy, cz = [v / 1000.0 for v in com]     # mm -> m
    Ixx_c = Ixx - M * (cy * cy + cz * cz)
    Iyy_c = Iyy - M * (cx * cx + cz * cz)
    Izz_c = Izz - M * (cx * cx + cy * cy)
    Ixy_c = Ixy + M * cx * cy
    Iyz_c = Iyz + M * cy * cz
    Ixz_c = Ixz + M * cx * cz
    out = {'mass_g': m_g, 'com_mm': com,
           'I_origin': (Ixx, Iyy, Izz, Ixy, Iyz, Ixz),
           'I_com': (Ixx_c, Iyy_c, Izz_c, Ixy_c, Iyz_c, Ixz_c),
           'com_height_above_wheel_mm': com[2] - WZ}
    if verbose:
        print('=== MASS PROPERTIES (from Fusion, materials assigned) ===')
        print('  mass                       %.1f g' % m_g)
        print('  CoM                        X %+.2f   Y %+.2f   Z %+.2f  mm' % com)
        print('  CoM above the wheel axis   %.1f mm' % out['com_height_above_wheel_mm'])
        print('  CoM fore-aft vs wheel      %+.2f mm' % com[0])
        print('  inertia about CoM (kg m2)  Ixx %.5f  Iyy %.5f  Izz %.5f'
              % (Ixx_c, Iyy_c, Izz_c))
        print('                             Ixy %+.6f Iyz %+.6f Ixz %+.6f'
              % (Ixy_c, Iyz_c, Ixz_c))
        L = out['com_height_above_wheel_mm'] / 1000.0
        if L > 0:
            print('  inverted-pendulum tau      %.3f s  (sqrt(L/g))'
                  % math.sqrt(L / 9.81))
    return out


def mass_by_part(verbose=True):
    """Per-part mass roll-up straight out of the model."""
    r = root()
    tot = {}
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        part = base_name(o.component.name.replace('(Mirror)', ''))
        m = 0.0
        stack = [o]
        while stack:
            cur = stack.pop()
            for b in cur.bRepBodies:
                try:
                    m += b.physicalProperties.mass * 1000.0
                except Exception:
                    pass
            for j in range(cur.childOccurrences.count):
                stack.append(cur.childOccurrences.item(j))
        tot[part] = tot.get(part, 0.0) + m
    if verbose:
        print('  %-34s %9s' % ('part (both sides)', 'mass g'))
        for k in sorted(tot, key=lambda k: -tot[k]):
            print('  %-34s %9.1f' % (k, tot[k]))
        print('  %-34s %9.1f' % ('TOTAL', sum(tot.values())))
    return tot


def set_material(comp, body, name):
    """Best-effort physical-material assignment by name substring."""
    try:
        libs = app().materialLibraries
        for li in range(libs.count):
            lib = libs.item(li)
            for mi in range(lib.materials.count):
                m = lib.materials.item(mi)
                if name.lower() in m.name.lower():
                    body.material = m
                    return m.name
    except Exception:
        pass
    return None


# =========================================================================
#  Fillets.  The design was built entirely from sharp-cornered extrusions --
#  0 fillet features in 815 timeline entries -- and FDM PA-CF cracks at sharp
#  re-entrant corners long before the nominal section stress is reached.
#  These are the corners that actually carry load.
# =========================================================================

def _fillet_one(comp, edge, radius_mm):
    """Fillet a single edge.  Returns True on success.

    Per-edge rather than one feature over a collection: a single edge that
    cannot take the radius would otherwise abort the whole set silently.
    """
    col = adsk.core.ObjectCollection.create()
    col.add(edge)
    ff = comp.features.filletFeatures
    ipt = ff.createInput()
    ipt.isRollingBallCorner = True
    ipt.edgeSetInputs.addConstantRadiusEdgeSet(
        col, adsk.core.ValueInput.createByReal(cm(radius_mm)), True)
    try:
        return ff.add(ipt) is not None
    except Exception:
        return False


def _fillet_try(comp, edge, radii):
    """Try each radius in turn, largest first.  Returns the radius used, or 0."""
    for rr in radii:
        if _fillet_one(comp, edge, rr):
            return rr
    return 0.0


def _y_line_edges(body, length_mm, y_lo, y_hi, tol=0.05):
    """Edges that are straight lines parallel to Y, of the given length,
    lying inside [y_lo, y_hi].  These are the corner edges left by a cut that
    ran along Y -- i.e. every channel and window corner."""
    out = []
    for e in body.edges:
        g = e.geometry
        if type(g).__name__ != 'Line3D':
            continue
        a, b = g.startPoint, g.endPoint
        if abs(a.x - b.x) > 1e-6 or abs(a.z - b.z) > 1e-6:
            continue                      # not Y-parallel
        L = abs(b.y - a.y) * 10
        if abs(L - length_mm) > tol:
            continue
        ylo, yhi = min(a.y, b.y) * 10, max(a.y, b.y) * 10
        if ylo < y_lo - tol or yhi > y_hi + tol:
            continue
        out.append(e)
    return out


def _circle_edges(body, radius_mm, y_mm, cx_mm=None, cz_mm=None, tol=0.05):
    """Circular edges of a given radius at a given Y (optionally centred)."""
    out = []
    for e in body.edges:
        g = e.geometry
        if type(g).__name__ != 'Circle3D':
            continue
        if abs(g.radius * 10 - radius_mm) > tol:
            continue
        c = g.center
        if abs(c.y * 10 - y_mm) > tol:
            continue
        if cx_mm is not None and abs(c.x * 10 - cx_mm) > tol:
            continue
        if cz_mm is not None and abs(c.z * 10 - cz_mm) > tol:
            continue
        out.append(e)
    return out


def _edge_key(e):
    """Stable positional key for an edge, so it can be re-found after the body
    has been rebuilt by a previous fillet."""
    p = e.pointOnEdge
    return (round(p.x * 10, 3), round(p.y * 10, 3), round(p.z * 10, 3))


def add_fillets(verbose=False):
    """Radius every load-bearing re-entrant corner.  Returns a per-part tally."""
    tally = {}

    def do(part, edges_fn, radii, label):
        occ = find_occ(part)
        if occ is None or occ.component.bRepBodies.count == 0:
            return
        c = occ.component
        # Snapshot the target edges by position first.  A fillet rebuilds the
        # body and invalidates every other edge reference, so the keys -- not
        # the objects -- are what survive between passes.
        keys = [_edge_key(e) for e in edges_fn(c.bRepBodies.item(0))]
        n, used = 0, []
        for k in keys:
            body = c.bRepBodies.item(0)
            match = None
            for e in edges_fn(body):
                if _edge_key(e) == k:
                    match = e
                    break
            if match is None:
                continue                      # already consumed by a neighbour
            got = _fillet_try(c, match, radii)
            if got:
                n += 1
                used.append(got)
        if n:
            key = '%s:%s' % (part, label)
            tally[key] = (n, round(sum(used) / len(used), 2))
            if verbose:
                print('   %-46s %2d edges @ R%.2f avg' % (key, n, tally[key][1]))

    # ---- proximal link -------------------------------------------------
    # the 20 mm spring-channel corners: the classic FDM crack initiator, a
    # sharp slot end in a part loaded in bending
    do('Proximal_Link_L',
       lambda b: _y_line_edges(b, CH_Y1 - CH_Y0, CH_Y0, CH_Y1),
       (2.5, 1.5, 1.0), 'channel corners')
    # root pad step: O62 disc standing 3 mm proud into the channel, and the
    # face the six M4 root bolts clamp against
    do('Proximal_Link_L',
       lambda b: _circle_edges(b, ROOT_DISC_D / 2.0, CH_Y0, 0.0, 0.0),
       (2.0, 1.0, 0.5), 'root pad step')
    # knee bearing-boss roots (0.8 mm steps, so a small radius is all that fits)
    do('Proximal_Link_L',
       lambda b: _circle_edges(b, PL_R2, LEG_Y_IN, KX, KZ),
       (0.5,), 'knee boss A root')
    do('Proximal_Link_L',
       lambda b: _circle_edges(b, PL_R2, LEG_Y_OUT, KX, KZ),
       (0.5,), 'knee boss B root')

    # ---- distal link ---------------------------------------------------
    do('Distal_Link_L',
       lambda b: _y_line_edges(b, CH_Y1 - CH_Y0, CH_Y0, CH_Y1),
       (2.5, 1.5, 1.0), 'channel corners')
    # wheel-end plate root: 8 mm plate stepping off the 5 mm arm, and the
    # single load path from the wheel motor into the leg
    do('Distal_Link_L',
       lambda b: _circle_edges(b, WM_PLATE_D / 2.0, CH_Y0, WX, WZ),
       (2.0, 1.0, 0.5), 'wheel plate root')
    # distal knee boss ends, which carry the O16 steel sleeve press fit
    do('Distal_Link_L',
       lambda b: _circle_edges(b, DBOSS_D / 2.0, DBOSS_Y0, KX, KZ),
       (1.5, 1.0, 0.5), 'knee boss inboard')
    do('Distal_Link_L',
       lambda b: _circle_edges(b, DBOSS_D / 2.0, DBOSS_Y1, KX, KZ),
       (1.5, 1.0, 0.5), 'knee boss outboard')

    # ---- side panel: lightening-window corners -------------------------
    do('Chassis_Shoulder_Plate_L',
       lambda b: _y_line_edges(b, SH_PLATE_T, SH_PLATE_Y0, SH_PLATE_Y0 + SH_PLATE_T),
       (2.0, 1.0), 'window corners')

    # ---- chassis frame: web/flange window corners ----------------------
    do('Chassis_Frame',
       lambda b: _y_line_edges(b, 2 * (FRAME_FLANGE_Y + FRAME_T),
                               -FRAME_FLANGE_Y - FRAME_T, FRAME_FLANGE_Y + FRAME_T),
       (2.0, 1.0), 'web corners')

    return tally


# Appearance names from the Fusion Appearance Library, keyed by our own
# material classes.  Purely cosmetic, but the visual collision checks the
# guide asks for are unreadable with translucent additive-library appearances.
APPEARANCE = {
    'PACF':  'Plastic - Matte (Gray)',
    'ABS':   'Plastic - Matte (White)',
    'ALU':   'Aluminum - Satin',
    'STEEL': 'Steel - Satin',
    'TPU':   'Rubber - Soft',
    'PU':    'Plastic - Matte (Red)',
    'SPRING': 'Plastic - Matte (Blue)',
    'PCB':   'Plastic - Matte (Green)',
    'BATT':  'Plastic - Matte (Black)',
    'ELEC':  'Plastic - Matte (Green)',
}

# Every modelled part -> material class.  Also drives the BOM.
PART_CLASS = {
    'Chassis_Shoulder_Plate_L': 'PACF',
    'Shoulder_Cable_Cover_L': 'ABS',
    'Shoulder_Output_Hub_L': 'ALU',
    'Proximal_Link_L': 'PACF',
    'Distal_Link_L': 'PACF',
    'Knee_Axle_L': 'STEEL',
    'Knee_Sleeve_L': 'STEEL',
    'Knee_Magnet_Carrier_L': 'STEEL',
    'Knee_Stop_Arc_L': 'STEEL',
    'Knee_Bumper_Flex_L': 'PU',
    'Knee_Bumper_Ext_L': 'PU',
    'Knee_Spring_L': 'SPRING',
    'Knee_Encoder_PCB_L': 'PCB',
    'Knee_Encoder_Bracket_L': 'ABS',
    'Cart_Upper_Eye_L': 'ALU',
    'Cart_Lower_Eye_L': 'ALU',
    'Cart_Guide_Rod_L': 'STEEL',
    'Cart_Preload_Shim_L': 'STEEL',
    'Wheel_Hub_L': 'ALU',
    'Wheel_Rim_L': 'PACF',
    'Wheel_Tyre_L': 'TPU',
    'HW_Bearing_6800': 'STEEL',
    'HW_ClevisPin_D4x32': 'STEEL',
    'HW_DowelPin_D6x9': 'STEEL',
    'HW_Magnet_D6x2p5_Diametric': 'STEEL',
    'HW_SHCS_M2p5x12': 'STEEL',
    'HW_SHCS_M3x6': 'STEEL',
    'HW_SHCS_M3x8': 'STEEL',
    'HW_SHCS_M3x10': 'STEEL',
    'HW_SHCS_M3x16': 'STEEL',
    'HW_SHCS_M4x10': 'STEEL',
    'Chassis_Frame': 'PACF',
    'Battery_4S2200': 'BATT',
    'Chassis_Electronics': 'ELEC',
    'Electronics_Tray': 'ABS',
    'Shoulder_Cable_Spiral_L': 'PU',
}

_APP_CACHE = {}


def appearance(key):
    if key in _APP_CACHE:
        return _APP_CACHE[key]
    nm = APPEARANCE.get(key)
    if not nm:
        return None
    libs = app().materialLibraries
    for li in range(libs.count):
        lib = libs.item(li)
        if lib.name != 'Fusion Appearance Library':
            continue
        for ai in range(lib.appearances.count):
            a = lib.appearances.item(ai)
            if a.name == nm:
                _APP_CACHE[key] = a
                return a
    return None


def apply_appearances(verbose=False):
    """Give every modelled body an opaque appearance from its material class."""
    r = root()
    done, miss = 0, []
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        n = base_name(o.component.name)
        cls = PART_CLASS.get(n)
        if cls is None:
            if not n.startswith('REF_'):
                miss.append(n)
            continue
        a = appearance(cls)
        if a is None:
            continue
        for b in o.component.bRepBodies:
            b.appearance = a
            done += 1
    if verbose and miss:
        print('  no material class for: %s' % sorted(set(miss)))
    return done


def cyl_y(comp, name_sk_y, x, z, dia, y0, y1, op='new', participants=None):
    """Convenience: circular extrusion along Y from y0 to y1."""
    sk = sk_on_y(comp, y0)
    circle(sk, x, z, dia)
    return extrude(comp, sk.profiles.item(0), (y1 - y0), op=op,
                   participants=participants)


def ring(comp, y, r_in, r_out, h, op='new', cx=0.0, cz=0.0):
    """Annular extrusion from y, height h, between radii r_in and r_out."""
    sk = sk_on_y(comp, y)
    circle(sk, cx, cz, 2 * r_out)
    circle(sk, cx, cz, 2 * r_in)
    want = math.pi * (r_out ** 2 - r_in ** 2)
    prof, best = None, 1e18
    acc = adsk.fusion.CalculationAccuracy.LowCalculationAccuracy
    for i in range(sk.profiles.count):
        p = sk.profiles.item(i)
        ar = p.areaProperties(acc).area * 100
        if abs(ar - want) < best:
            best, prof = abs(ar - want), p
    return extrude(comp, prof, h, op)


def sk_axial_y(comp, cx_mm, cz_mm, y_lo=-200.0, y_hi=200.0):
    """Sketch + axis for a solid of revolution about the Y line at (cx, cz).

    Returns (sketch, axis, sp) where sp(radius_mm, y_mm) -> a sketch Point3D.
    The profile plane is the YZ plane offset to X = cx, so it contains the
    axis; radius is measured along +Z from the axis.  Point mapping goes
    through modelToSketchSpace rather than an assumed axis convention, so it
    is correct regardless of how Fusion orients the sketch.

    The axis is a CONSTRUCTION LINE inside the sketch, not a ConstructionAxis:
    constructionAxes.add() raises "Environment is not supported" when called
    from a script in the parametric design environment, and revolveFeatures
    accepts a sketch line as the axis anyway.
    """
    pl = comp.constructionPlanes
    ipt = pl.createInput()
    ipt.setByOffset(comp.yZConstructionPlane,
                    adsk.core.ValueInput.createByReal(cm(cx_mm)))
    plane = pl.add(ipt)
    plane.isLightBulbOn = False
    sk = comp.sketches.add(plane)

    def sp(radius_mm, y_mm):
        g = adsk.core.Point3D.create(cm(cx_mm), cm(y_mm), cm(cz_mm + radius_mm))
        return sk.modelToSketchSpace(g)

    ax = sk.sketchCurves.sketchLines.addByTwoPoints(sp(0.0, y_lo), sp(0.0, y_hi))
    ax.isConstruction = True
    return sk, ax, sp


def rev_profile(comp, cx_mm, cz_mm, pts, arcs=(), op='new'):
    """Revolve a closed (radius, y) polygon about the Y axis at (cx, cz).

    pts   : list of (radius_mm, y_mm), traversed in order and closed.
    arcs  : list of (i, radius_mid, y_mid) -- replaces the straight segment
            from pts[i] to pts[i+1] with a 3-point arc through that midpoint.
    """
    sk, ax, sp = sk_axial_y(comp, cx_mm, cz_mm)
    ln = sk.sketchCurves.sketchLines
    ar = sk.sketchCurves.sketchArcs
    arc_at = {i: (r, y) for (i, r, y) in arcs}
    n = len(pts)
    for i in range(n):
        a = pts[i]
        b = pts[(i + 1) % n]
        if i in arc_at:
            m = arc_at[i]
            ar.addByThreePoints(sp(*a), sp(*m), sp(*b))
        else:
            ln.addByTwoPoints(sp(*a), sp(*b))
    return revolve(comp, biggest_profile(sk), ax, 360.0, op)


# --------------------------------------------------------------- knee kinematics
def wheel_at(phi_deg):
    """Global (X, Z) of the wheel axis for knee angle phi (shoulder nominal)."""
    d = math.radians(-A_NOM - phi_deg)
    return (KX + L2 * math.sin(d), KZ - L2 * math.cos(d))


def lower_pivot_at(phi_deg):
    """Global (X, Z) of the lower cartridge pivot for knee angle phi."""
    a = math.radians(180.0 + CART_ANG / 2.0 - phi_deg)
    return (KX + RL * math.cos(a), KZ + RL * math.sin(a))


def cart_len(phi_deg):
    th = math.radians(CART_ANG - phi_deg)
    return math.sqrt(RU ** 2 + RL ** 2 - 2 * RU * RL * math.cos(th))


def cart_arm(phi_deg):
    th = math.radians(CART_ANG - phi_deg)
    return RU * RL * math.sin(th) / cart_len(phi_deg)


def spring_force(phi_deg):
    return 30.0 + SPRING_RATE * (cart_len(PHI_EXT) - cart_len(phi_deg))


def ground_force(phi_deg):
    wx, wz = wheel_at(phi_deg)
    lever = abs(wx - KX)
    return spring_force(phi_deg) * cart_arm(phi_deg) / lever


# ------------------------------------------------------------ link uv frames
# Proximal link frame: origin at the shoulder S, u along S->K, v = fore/up perp.
PU = (math.sin(_a), -math.cos(_a))        # ( 0.76604, -0.64279)
PV = (math.cos(_a), math.sin(_a))         # ( 0.64279,  0.76604)
# Distal link frame (nominal pose): origin at the knee K, u along K->W,
# v chosen so the lower cartridge pivot Lp has v > 0.
DU = (-math.sin(_a), -math.cos(_a))       # (-0.76604, -0.64279)
DV = (math.cos(_a), -math.sin(_a))        # ( 0.64279, -0.76604)


def prox_uv(u, v):
    return (u * PU[0] + v * PV[0], u * PU[1] + v * PV[1])


def prox_inv(x, z):
    return (x * PU[0] + z * PU[1], x * PV[0] + z * PV[1])


def dist_uv(u, v):
    return (KX + u * DU[0] + v * DV[0], KZ + u * DU[1] + v * DV[1])


def dist_inv(x, z):
    dx, dz = x - KX, z - KZ
    return (dx * DU[0] + dz * DU[1], dx * DV[0] + dz * DV[1])


def lozenge_tangent_points(c1, r1, c2, r2, upper=True):
    """Exact external-tangent contact points for two unequal circles.

    The previous sketch helper used ``pi/2 + alpha`` for the upper radius.
    That is the internal/chord-side sign: unequal end circles projected about
    0.61 mm beyond the supposedly straight proximal-link print face.  Using
    ``pi/2 - alpha`` makes the straight segment a true supporting tangent and
    gives the link a deliberate FDM bed datum without adding sacrificial feet.
    """
    dx, dy = c2[0] - c1[0], c2[1] - c1[1]
    d = math.hypot(dx, dy)
    if d <= 0.0 or abs(r1 - r2) >= d:
        raise ValueError('external lozenge tangent requires separate circles')
    base = math.atan2(dy, dx)
    alpha = math.asin(max(-1.0, min(1.0, (r1 - r2) / d)))
    theta = math.pi / 2.0 - alpha
    angle = base + theta if upper else base - theta
    return ((c1[0] + r1 * math.cos(angle),
             c1[1] + r1 * math.sin(angle)),
            (c2[0] + r2 * math.cos(angle),
             c2[1] + r2 * math.sin(angle)))


def lozenge(sk, c1, r1, c2, r2, frame=None):
    """Closed tangent-line lozenge between two circles.

    c1, c2 are (u, v) centres in the given frame (or global XZ if frame None),
    r1, r2 their radii.  frame is a function (u, v) -> (X, Z).
    """
    f = frame or (lambda u, v: (u, v))
    base = math.atan2(c2[1] - c1[1], c2[0] - c1[0])
    arcs = sk.sketchCurves.sketchArcs
    lines = sk.sketchCurves.sketchLines

    def on(c, r, ang):
        return f(c[0] + r * math.cos(base + ang), c[1] + r * math.sin(base + ang))
    p1u_uv, p2u_uv = lozenge_tangent_points(c1, r1, c2, r2, True)
    p1l_uv, p2l_uv = lozenge_tangent_points(c1, r1, c2, r2, False)
    p1u, p2u = f(*p1u_uv), f(*p2u_uv)
    p1l, p2l = f(*p1l_uv), f(*p2l_uv)
    m1 = on(c1, r1, math.pi)
    m2 = on(c2, r2, 0.0)
    lines.addByTwoPoints(sxz(*p1u), sxz(*p2u))
    arcs.addByThreePoints(sxz(*p2u), sxz(*m2), sxz(*p2l))
    lines.addByTwoPoints(sxz(*p2l), sxz(*p1l))
    arcs.addByThreePoints(sxz(*p1l), sxz(*m1), sxz(*p1u))


# ------------------------------------------------------------------ reporting
def bbox_of(entity):
    """(minx,maxx,miny,maxy,minz,maxz) in mm for an occurrence or body."""
    lo = [1e9] * 3
    hi = [-1e9] * 3

    def acc(bb):
        for k, v in enumerate((bb.minPoint.x, bb.minPoint.y, bb.minPoint.z)):
            lo[k] = min(lo[k], v * 10)
        for k, v in enumerate((bb.maxPoint.x, bb.maxPoint.y, bb.maxPoint.z)):
            hi[k] = max(hi[k], v * 10)

    if hasattr(entity, 'bRepBodies'):
        for b in entity.bRepBodies:
            acc(b.boundingBox)
        if hasattr(entity, 'childOccurrences'):
            stack = [entity]
            while stack:
                cur = stack.pop()
                for i in range(cur.childOccurrences.count):
                    c = cur.childOccurrences.item(i)
                    for b in c.bRepBodies:
                        acc(b.boundingBox)
                    stack.append(c)
    else:
        acc(entity.boundingBox)
    return (lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])


def fmt_bbox(entity, label=''):
    b = bbox_of(entity)
    return ('%-28s X[%8.2f,%8.2f] Y[%8.2f,%8.2f] Z[%9.2f,%9.2f]'
            % (label, b[0], b[1], b[2], b[3], b[4], b[5]))


# --------------------------------------------------------------- hardware
# Socket-head cap screw head sizes (ISO 4762): d -> (head_dia, head_height)
SHCS = {2.0: (3.8, 2.0), 2.5: (4.5, 2.5), 3.0: (5.5, 3.0),
        4.0: (7.0, 4.0), 5.0: (8.5, 5.0), 6.0: (10.0, 6.0)}


def screw_comp(name, d, L, kind='shcs'):
    """Create/fetch a screw component modelled along -Y from its origin.

    The component origin sits at the *head underside*; the head grows toward
    +Y and the shank toward -Y.  Place it with a translation to the seat face.
    """
    occ = find_occ(name)
    if occ:
        return occ
    occ = new_comp(name)
    c = occ.component
    hd, hh = SHCS[d]
    if kind == 'nut':
        hd, hh = (d * 1.8, d * 0.85)
    sk = sk_on_y(c, 0.0)
    circle(sk, 0, 0, hd)
    e = extrude(c, sk.profiles.item(0), hh, 'new')
    e.bodies.item(0).name = name
    if kind != 'nut':
        sk = sk_on_y(c, 0.0)
        circle(sk, 0, 0, d)
        extrude(c, sk.profiles.item(0), -L, 'join')
    else:
        sk = sk_on_y(c, -0.5)
        circle(sk, 0, 0, d)
        extrude(c, sk.profiles.item(0), hh + 1.0, 'cut')
    set_material(c, c.bRepBodies.item(0), 'Steel')
    return occ


def place(comp_occ, x, z, y_seat, flip=False, parent=None):
    """Add another occurrence of comp_occ's component at (x, y_seat, z).

    flip=False -> shank runs toward -Y.  flip=True -> shank runs toward +Y.
    """
    parent = parent or root()
    if flip:
        m = mat((-1, 0, 0), (0, -1, 0), (0, 0, 1), (x, y_seat, z))
    else:
        m = mat((1, 0, 0), (0, 1, 0), (0, 0, 1), (x, y_seat, z))
    return parent.occurrences.addExistingComponent(comp_occ.component, m)


def place_polar(comp_occ, pcd, count, a0, y_seat, flip=False, cx=0.0, cz=0.0,
                parent=None):
    out = []
    for i in range(count):
        a = math.radians(a0 + i * 360.0 / count)
        out.append(place(comp_occ, cx + pcd / 2.0 * math.cos(a),
                         cz + pcd / 2.0 * math.sin(a), y_seat, flip, parent))
    return out


# ------------------------------------------------------ interference checking
def interference(skip_names=(), only_names=None, coincident=False,
                 min_vol_mm3=0.5):
    """Run a whole-assembly interference analysis.

    Returns a list of (nameA, nameB, volume_mm3) sorted worst-first.
    Occurrences whose component name contains any string in skip_names are
    excluded.  Volumes below min_vol_mm3 are treated as touching, not clashing.
    """
    d = design()
    col = adsk.core.ObjectCollection.create()
    r = root()
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        n = o.component.name
        if any(s in n for s in skip_names):
            continue
        if only_names is not None and not any(s in n for s in only_names):
            continue
        col.add(o)
    if col.count < 2:
        return []
    ipt = d.createInterferenceInput(col)
    ipt.areCoincidentFacesIncluded = coincident
    res = d.analyzeInterference(ipt)
    out = []
    if res:
        for i in range(res.count):
            it = res.item(i)
            v = it.interferenceBody.volume * 1000.0   # cm3 -> mm3
            if v < min_vol_mm3:
                continue
            a = it.entityOne
            b = it.entityTwo
            na = a.component.name if hasattr(a, 'component') else a.name
            nb = b.component.name if hasattr(b, 'component') else b.name
            out.append((na, nb, v))
    out.sort(key=lambda t: -t[2])
    return out


def report_interference(label, **kw):
    res = interference(**kw)
    if not res:
        print('  [%s] NO INTERFERENCE' % label)
        return True
    print('  [%s] %d clash(es):' % (label, len(res)))
    for na, nb, v in res[:25]:
        print('     %-30s <-> %-30s  %9.2f mm3' % (na, nb, v))
    return False


def gap(occA_name, occB_name):
    """Minimum distance in mm between two occurrences' bodies."""
    a = find_occ(occA_name)
    b = find_occ(occB_name)
    best = 1e9
    mm = app().measureManager
    for ba in a.bRepBodies:
        for bb in b.bRepBodies:
            r = mm.measureMinimumDistance(ba, bb)
            best = min(best, r.value * 10)
    return best


# ===========================================================================
#  Part builders.  Kept here so a rebuild is one call and every phase uses
#  exactly the same geometry.  All angles below are GLOBAL XZ angles measured
#  from the knee: 140 deg points at the shoulder, 220 deg at the wheel.
# ===========================================================================

# --- proximal link outline -------------------------------------------------
PL_R1 = 31.0          # root half-depth (about the shoulder axis)
PL_R2 = 19.0          # knee boss half-depth
PL_WT = 4.0           # +v / -v wall thickness
PL_WALL_STOP = 72.0   # -v wall dies out at this u
# The through-channel termination cannot end as a zero-radius knife edge: that
# produced a four-face non-manifold B-Rep/STL edge.  R1.0 is the existing
# fallback channel-corner fillet in add_fillets(), expressed as a relief bore.
PL_WALL_RELIEF_D = 2.0
# The O34 root-access bore (R17) and the harness pass-through at R21 were
# exactly tangent when the latter was O8.0 (17 + 4 = 21), creating the second
# non-manifold STL edge.  O8.2 preserves the datum centre while providing
# 0.10 mm nominal overlap and more, not less, cable clearance.
PROX_HARNESS_D = 8.2

# --- distal link outline ---------------------------------------------------
DL_WEB_C = (30.0, 24.0)
DL_WEB_R = 10.0
DL_ARM_C = (36.0, 18.0)
DL_ARM_R = 17.0
DL_WHL_R = 29.0
DL_WT = 4.0
DL_CUT_U0 = 22.0
WM_PLATE_D = 68.0

# --- knee stop -------------------------------------------------------------
STOP_R = 30.0             # stop-pin radius from the knee axis
STOP_PIN_D = 6.0
STOP_SLOT_W = 6.2
STOP_PIN_A0 = 246.6       # pin global XZ angle at phi = 0 (fixed to distal link)
STOP_ARC_Y0 = 90.3        # steel arc plate sits on the proximal arm-B boss face
STOP_ARC_T = 3.0
STOP_BOLT_R = 15.0
# 30 deg spacing, NOT 20.  At r = 15 a 20 deg pitch puts the bolt centres
# 2*15*sin(10) = 5.209 mm apart, and an M3 SHCS head is O5.5 -- the three heads
# physically overlap by 0.29 mm and cannot all be fitted.  30 deg gives
# 2*15*sin(15) = 7.765 mm, a 2.27 mm gap between heads.  Do not tighten this.
STOP_BOLT_A = (230.0, 260.0, 290.0)

# --- blind heat-set insert budget -----------------------------------------
# Every blind insert bore must satisfy:  bore_depth >= insert_len, and the
# screw shank must stop SHORT of the bore floor, or the screw bottoms out
# before it clamps.  Getting this wrong once left the knee hard stop -- the
# final crash load path -- sitting on three proud brass pips and never
# actually torqued down.  arm B is only 5.8 mm thick at the boss
# (y = 84.5 .. 90.3), so the bore is 5.0 and the screw is M3 x 6, giving
# 3.0 mm of thread into a 5.0 mm insert.  That is 1.0 x d, which is fine
# here because the joint is loaded in SHEAR, not pull-out.
INSERT_LEN = 5.0          # M3 brass heat-set insert length
STOP_INSERT_DEPTH = 5.0   # bore depth in the arm-B boss (0.8 mm of floor left)
ENC_INSERT_DEPTH = 5.0    # bore depth for the encoder bracket inserts
COVER_INSERT_DEPTH = 5.0  # bore depth in the cable cover (1.5 mm of floor left)


def pl_ep(u):
    p1, p2 = lozenge_tangent_points(
        (0.0, 0.0), PL_R1, (120.0, 0.0), PL_R2, True)
    t = (u - p1[0]) / (p2[0] - p1[0])
    return p1[1] + t * (p2[1] - p1[1])


def dl_epd(u):
    p1, p2 = lozenge_tangent_points(
        DL_ARM_C, DL_ARM_R, (120.0, 0.0), DL_WHL_R, True)
    t = (u - p1[0]) / (p2[0] - p1[0])
    return p1[1] + t * (p2[1] - p1[1])


def kpt(r, a_deg):
    """Point at radius r and global XZ angle a_deg measured from the knee."""
    a = math.radians(a_deg)
    return (KX + r * math.cos(a), KZ + r * math.sin(a))


def slot_half_angle():
    return math.degrees(math.asin((STOP_SLOT_W / 2.0) / STOP_R))


def build_proximal_link(bearing_seat_d=KNEE_BRG_OD):
    drop_comp('Proximal_Link_L')
    occ = new_comp('Proximal_Link_L')
    c = occ.component
    sk = sk_on_y(c, LEG_Y_IN)
    lozenge(sk, (0.0, 0.0), PL_R1, (120.0, 0.0), PL_R2, frame=prox_uv)
    e = extrude(c, biggest_profile(sk), PROX_PRINT_FACE_Y - LEG_Y_IN, 'new')
    e.bodies.item(0).name = 'Proximal_Link_L'

    # channel: keep a +v wall the whole length, a -v wall only up to u=72
    sk = sk_on_y(c, CH_Y0)
    pts = [(0.0, pl_ep(0.0) - PL_WT), (118.0, pl_ep(118.0) - PL_WT),
           (118.0, pl_ep(118.0) + 6.0), (145.0, pl_ep(118.0) + 6.0),
           (145.0, -46.0), (PL_WALL_STOP, -46.0),
           (PL_WALL_STOP, -(pl_ep(PL_WALL_STOP) - PL_WT))]
    ln = sk.sketchCurves.sketchLines
    arcs = sk.sketchCurves.sketchArcs
    for i in range(len(pts) - 1):
        a = prox_uv(*pts[i]); b = prox_uv(*pts[i + 1])
        ln.addByTwoPoints(sxz(*a), sxz(*b))
    arcs.addByThreePoints(sxz(*prox_uv(*pts[-1])),
                          sxz(*prox_uv(-(PL_R1 - PL_WT), 0.0)),
                          sxz(*prox_uv(*pts[0])))
    extrude(c, biggest_profile(sk), CH_Y1 - CH_Y0, 'cut')
    # Round the wall-to-open-channel transition with the already specified
    # R1.0 fallback instead of leaving a zero-thickness four-face edge.
    relief = prox_uv(PL_WALL_STOP,
                     -(pl_ep(PL_WALL_STOP) - PL_WT))
    sk = sk_on_y(c, CH_Y0)
    circle(sk, relief[0], relief[1], PL_WALL_RELIEF_D)
    extrude(c, sk.profiles.item(0), CH_Y1 - CH_Y0, 'cut')

    # root pad and knee boss thickening
    sk = sk_on_y(c, CH_Y0); circle(sk, 0, 0, ROOT_DISC_D)
    extrude(c, sk.profiles.item(0), ROOT_PLATE_Y1 - CH_Y0, 'join')
    sk = sk_on_y(c, KNEE_BOSS_A_Y0); circle(sk, KX, KZ, 2 * PL_R2)
    extrude(c, sk.profiles.item(0), LEG_Y_IN - KNEE_BOSS_A_Y0, 'join')
    # Arm B already reaches the existing Y=90.3 bearing-boss plane.  The old
    # local 0.8 mm boss step is deliberately absorbed into the full outboard
    # face so the bearing axes can print normal to the bed.

    # knee bearing pockets + O17 retaining lips
    sk = sk_on_y(c, BRG1_Y0); circle(sk, KX, KZ, bearing_seat_d)
    extrude(c, sk.profiles.item(0), BRG1_Y1 - BRG1_Y0, 'cut')
    sk = sk_on_y(c, BRG2_Y0); circle(sk, KX, KZ, bearing_seat_d)
    extrude(c, sk.profiles.item(0), BRG2_Y1 - BRG2_Y0, 'cut')
    sk = sk_on_y(c, BRG1_Y1); circle(sk, KX, KZ, KNEE_LIP_D)
    extrude(c, sk.profiles.item(0), CH_Y0 - BRG1_Y1, 'cut')
    sk = sk_on_y(c, CH_Y1); circle(sk, KX, KZ, KNEE_LIP_D)
    extrude(c, sk.profiles.item(0), BRG2_Y0 - CH_Y1, 'cut')

    # upper cartridge pivot
    sk = sk_on_y(c, KNEE_BOSS_A_Y0 - 1); circle(sk, UX, UZ, 4.15)
    extrude(c, sk.profiles.item(0), (KNEE_BOSS_B_Y1 - KNEE_BOSS_A_Y0) + 2, 'cut')

    # root fasteners: 6x M4 counterbored in arm A, 6x access holes in arm B
    sk = sk_on_y(c, LEG_Y_IN - 1)
    circles_polar(sk, 0, 0, HUB_LINK_PCD, 4.3, 6, HUB_LINK_A0)
    extrude(c, profiles(sk), ROOT_PLATE_T + 2, 'cut')
    sk = sk_on_y(c, 63.3)
    circles_polar(sk, 0, 0, HUB_LINK_PCD, 7.5, 6, HUB_LINK_A0)
    extrude(c, profiles(sk), ROOT_PLATE_Y1 - 63.3 + 0.5, 'cut')
    sk = sk_on_y(c, CH_Y1)
    circles_polar(sk, 0, 0, HUB_LINK_PCD, 9.0, 6, HUB_LINK_A0)
    extrude(c, profiles(sk), PROX_PRINT_FACE_Y - CH_Y1 + 0.5, 'cut')
    sk = sk_on_y(c, CH_Y1); circle(sk, 0, 0, 34.0)
    extrude(c, sk.profiles.item(0), PROX_PRINT_FACE_Y - CH_Y1 + 0.5, 'cut')
    # O34 access bore straight through the root pad as well, so a hex key can
    # reach the six M3 output-hub screws without removing the link.
    sk = sk_on_y(c, LEG_Y_IN - 1); circle(sk, 0, 0, 34.0)
    extrude(c, sk.profiles.item(0), ROOT_PLATE_T + 2, 'cut')

    # harness pass-through, aligned with the hub cable hole
    a = math.radians(30.4)
    sk = sk_on_y(c, LEG_Y_IN - 1)
    circle(sk, HUB_CABLE_R * math.cos(a), HUB_CABLE_R * math.sin(a),
           PROX_HARNESS_D)
    extrude(c, sk.profiles.item(0), ROOT_PLATE_T + 2, 'cut')

    # Steel knee-stop arc: 3x M3 heat-set inserts, blind from the arm-B boss
    # face.  These MUST stay blind -- a through bolt would put its nut inside
    # the spring channel and inside the distal link's knee web.  Depth is
    # STOP_INSERT_DEPTH so the 5 mm insert seats flush; see the note there.
    sk = sk_on_y(c, KNEE_BOSS_B_Y1 - STOP_INSERT_DEPTH)
    for ang in STOP_BOLT_A:
        w = kpt(STOP_BOLT_R, ang); circle(sk, w[0], w[1], 4.0)
    extrude(c, profiles(sk), STOP_INSERT_DEPTH, 'cut')

    # 2x M3 heat-set inserts for the knee encoder bracket
    sk = sk_on_y(c, KNEE_BOSS_B_Y1 - ENC_INSERT_DEPTH)
    for ang in (60.0, 140.0):
        w = kpt(15.0, ang); circle(sk, w[0], w[1], 4.0)
    extrude(c, profiles(sk), ENC_INSERT_DEPTH, 'cut')

    # lightening
    sk = sk_on_y(c, KNEE_BOSS_A_Y0 - 1)
    a1 = prox_uv(36.0, 0.0); a2 = prox_uv(68.0, 0.0)
    slot(sk, a1[0], a1[1], a2[0], a2[1], 34.0)
    extrude(c, biggest_profile(sk), (KNEE_BOSS_B_Y1 - KNEE_BOSS_A_Y0) + 2, 'cut')
    sk = sk_on_y(c, KNEE_BOSS_A_Y0 - 1)
    b1 = prox_uv(76.0, -6.0); b2 = prox_uv(94.0, -6.0)
    slot(sk, b1[0], b1[1], b2[0], b2[1], 16.0)
    extrude(c, biggest_profile(sk), (KNEE_BOSS_B_Y1 - KNEE_BOSS_A_Y0) + 2, 'cut')
    return occ


def build_distal_link():
    drop_comp('Distal_Link_L')
    occ = new_comp('Distal_Link_L')
    c = occ.component
    LPD = dist_inv(LX, LZ)
    sk = sk_on_y(c, LEG_Y_IN)
    lozenge(sk, DL_ARM_C, DL_ARM_R, (120.0, 0.0), DL_WHL_R, frame=dist_uv)
    e = extrude(c, biggest_profile(sk), LEG_W, 'new')
    e.bodies.item(0).name = 'Distal_Link_L'
    sk = sk_on_y(c, LEG_Y_IN)
    p = dist_uv(*LPD); circle(sk, p[0], p[1], 28.0)
    extrude(c, sk.profiles.item(0), LEG_W, 'join')

    sk = sk_on_y(c, CH_Y0)
    pts = [(DL_CUT_U0, dl_epd(DL_CUT_U0) - DL_WT),
           (132.0, dl_epd(132.0) - DL_WT), (132.0, -62.0), (DL_CUT_U0, -62.0)]
    ln = sk.sketchCurves.sketchLines
    for i in range(4):
        a = dist_uv(*pts[i]); b = dist_uv(*pts[(i + 1) % 4])
        ln.addByTwoPoints(sxz(*a), sxz(*b))
    extrude(c, biggest_profile(sk), CH_Y1 - CH_Y0, 'cut')

    sk = sk_on_y(c, DBOSS_Y0)
    lozenge(sk, (0.0, 0.0), DBOSS_D / 2.0, DL_WEB_C, DL_WEB_R, frame=dist_uv)
    extrude(c, biggest_profile(sk), DBOSS_Y1 - DBOSS_Y0, 'join')

    sk = sk_on_y(c, CH_Y0); circle(sk, WX, WZ, WM_PLATE_D)
    extrude(c, sk.profiles.item(0), WM_MOUNT_Y - CH_Y0, 'join')
    # Nothing may sit inside the wheel's swept annulus: the rim/tyre occupies
    # r = 44..55 from the wheel axis over y = 69..104.5, so clear O112.
    sk = sk_on_y(c, WM_MOUNT_Y); circle(sk, WX, WZ, 112.0)
    extrude(c, sk.profiles.item(0), LEG_Y_OUT - WM_MOUNT_Y + 1.0, 'cut')

    sk = sk_on_y(c, DBOSS_Y0 - 1); circle(sk, KX, KZ, KNEE_SLEEVE_OD)
    extrude(c, sk.profiles.item(0), (DBOSS_Y1 - DBOSS_Y0) + 2, 'cut')
    sk = sk_on_y(c, LEG_Y_IN - 1); circle(sk, LX, LZ, 4.15)
    extrude(c, sk.profiles.item(0), LEG_W + 2, 'cut')
    sk = sk_on_y(c, LEG_Y_IN - 1); circle(sk, WX, WZ, WM_COVER_D)
    extrude(c, sk.profiles.item(0), (WM_MOUNT_Y - LEG_Y_IN) + 2, 'cut')
    sk = sk_on_y(c, LEG_Y_IN - 1)
    circles_polar(sk, WX, WZ, WM_BOLT_PCD, 2.8, 6, WM_BOLT_A0)
    extrude(c, profiles(sk), (WM_MOUNT_Y - LEG_Y_IN) + 2, 'cut')

    # O6 H7 stop-pin seat in arm B
    q = kpt(STOP_R, STOP_PIN_A0)
    sk = sk_on_y(c, CH_Y1 - 0.5); circle(sk, q[0], q[1], STOP_PIN_D)
    extrude(c, sk.profiles.item(0), (LEG_Y_OUT - CH_Y1) + 1.0, 'cut')

    for (u0, v0, u1, v1, w) in [(64.0, -6.0, 96.0, -5.0, 16.0),
                                (46.0, 26.0, 94.0, 15.0, 12.0)]:
        sk = sk_on_y(c, LEG_Y_IN - 1)
        a = dist_uv(u0, v0); b = dist_uv(u1, v1)
        slot(sk, a[0], a[1], b[0], b[1], w)
        extrude(c, biggest_profile(sk), LEG_W + 2, 'cut')
    sk = sk_on_y(c, LEG_Y_IN - 1)
    circles_polar(sk, WX, WZ, 52.0, 9.0, 6, WM_BOLT_A0 + 30.0)
    extrude(c, profiles(sk), (WM_MOUNT_Y - LEG_Y_IN) + 2, 'cut')
    return occ


# ===========================================================================
#  Motion checking.  The leg is posed by transforming occurrence groups rather
#  than by driving joints: it is deterministic, and it lets the spring body be
#  rebuilt at each knee angle so the cartridge envelope is honest.
# ===========================================================================

STATIC_NAMES = ('REF_GIM6010-8', 'Chassis_Shoulder_Plate_L',
                'Shoulder_Cable_Cover_L', 'Chassis_Frame',
                'Battery_4S2200', 'Electronics_Tray', 'Chassis_Electronics')
PROX_NAMES = ('Shoulder_Output_Hub_L', 'Proximal_Link_L', 'HW_Bearing_6800',
              'Knee_Stop_Arc_L', 'Knee_Bumper_Flex_L', 'Knee_Bumper_Ext_L',
              'Knee_Encoder_Bracket_L', 'Knee_Encoder_PCB_L', 'HW_SHCS_M3x16',
              'HW_SHCS_M3x6')
DIST_NAMES = ('Distal_Link_L', 'Knee_Sleeve_L', 'Knee_Axle_L',
              'Knee_Magnet_Carrier_L', 'HW_Magnet_D6x2p5_Diametric',
              'HW_DowelPin_D6x9', 'REF_GIM4305-10', 'Wheel_Hub_L',
              'Wheel_Rim_L', 'Wheel_Tyre_L', 'HW_SHCS_M2p5x12')
CART_UP_NAMES = ('Cart_Upper_Eye_L', 'Cart_Guide_Rod_L')
CART_LO_NAMES = ('Cart_Lower_Eye_L', 'Cart_Preload_Shim_L')

CART_DEAD = 25.57          # pin-to-pin length not taken by the spring
CART_DEAD_U = 11.0         # upper pin to spring upper face


def classify(occ):
    """Return 'STATIC' | 'PROX' | 'DIST' | 'CART_UP' | 'CART_LO' | 'SPRING'.

    Mirrored (right-leg) occurrences are treated as STATIC: the right leg is the
    geometric mirror of the left, so sweeping the left leg against the chassis
    proves both.  Posing them with left-leg matrices would be wrong.
    """
    if '(Mirror)' in occ.component.name or '(Mirror)' in occ.name:
        return 'STATIC'
    n = cname(occ)
    if n in STATIC_NAMES:
        return 'STATIC'
    if n in PROX_NAMES:
        return 'PROX'
    if n in DIST_NAMES:
        return 'DIST'
    if n in CART_UP_NAMES:
        return 'CART_UP'
    if n in CART_LO_NAMES:
        return 'CART_LO'
    if n == 'Knee_Spring_L':
        return 'SPRING'
    b = bbox_of(occ)
    cx, cy, cz = (b[0] + b[1]) / 2, (b[2] + b[3]) / 2, (b[4] + b[5]) / 2
    rs = math.hypot(cx, cz)
    if n == 'HW_SHCS_M3x10':
        return 'PROX' if rs < 20 else 'STATIC'
    if n == 'HW_SHCS_M4x10':
        return 'DIST' if cz < -120 else 'PROX'
    if n == 'HW_SHCS_M3x8':
        # wheel-hub screws are DIST; the four cable-cover screws sit on the
        # shoulder plate, which is STATIC.
        return 'DIST' if cz < -120 else 'STATIC'
    if n == 'HW_ClevisPin_D4x32':
        return 'CART_LO' if cz < -100 else 'CART_UP'
    return 'STATIC'


def snapshot_transforms():
    """Record every occurrence's FULL nominal transform.

    Storing only the translation is wrong: the two motor references carry a
    rotation of their own, and discarding it re-orients them.
    """
    r = root()
    out = []
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        out.append((o, classify(o), list(o.transform2.asArray())))
    return out


def _mm(a, b):
    """4x4 row-major 16-array multiply: returns a . b"""
    out = [0.0] * 16
    for i in range(4):
        for j in range(4):
            out[i * 4 + j] = sum(a[i * 4 + k] * b[k * 4 + j] for k in range(4))
    return out


def _rot_arr(a_deg, ox_mm, oz_mm):
    """Rotation about +Y by a_deg through (ox, oz), as a 16-array in cm."""
    a = math.radians(a_deg)
    ca, sa = math.cos(a), math.sin(a)
    ox, oz = cm(ox_mm), cm(oz_mm)
    cxx = ox - ox * ca - oz * sa
    czz = oz + ox * sa - oz * ca
    return [ca, 0.0, sa, cxx,
            0.0, 1.0, 0.0, 0.0,
            -sa, 0.0, ca, czz,
            0.0, 0.0, 0.0, 1.0]


def _trans_arr(t_mm):
    return [1.0, 0.0, 0.0, cm(t_mm[0]),
            0.0, 1.0, 0.0, cm(t_mm[1]),
            0.0, 0.0, 1.0, cm(t_mm[2]),
            0.0, 0.0, 0.0, 1.0]


def _as_matrix(arr):
    m = adsk.core.Matrix3D.create()
    m.setWithArray(arr)
    return m


def _rmat(a_deg, ox, oz, t_mm):
    """Rotation about +Y by a_deg through (ox, oz), composed with translate t."""
    a = math.radians(a_deg)
    ca, sa = math.cos(a), math.sin(a)
    cxx = ox - ox * ca - oz * sa
    czz = oz + ox * sa - oz * ca
    tx, ty, tz = t_mm
    nx = tx * ca + tz * sa + cxx
    nz = -tx * sa + tz * ca + czz
    m = adsk.core.Matrix3D.create()
    m.setWithArray([ca, 0.0, sa, cm(nx),
                    0.0, 1.0, 0.0, cm(ty),
                    -sa, 0.0, ca, cm(nz),
                    0.0, 0.0, 0.0, 1.0])
    return m


def _tmat(t_mm):
    m = adsk.core.Matrix3D.create()
    m.setWithArray([1, 0, 0, cm(t_mm[0]), 0, 1, 0, cm(t_mm[1]),
                    0, 0, 1, cm(t_mm[2]), 0, 0, 0, 1])
    return m


def cart_dir(phi):
    lx, lz = lower_pivot_at(phi)
    L = math.hypot(lx - UX, lz - UZ)
    return ((lx - UX) / L, (lz - UZ) / L), L


def _spring_body(name, phi, y_mid):
    """Build one spring envelope, revolved about the cartridge axis at y_mid."""
    drop_comp(name)
    o = new_comp(name)
    c = o.component
    d, L = cart_dir(phi)
    s0, s1 = CART_DEAD_U, L - (CART_DEAD - CART_DEAD_U)
    sk = sk_on_y(c, y_mid)
    ax = sk.sketchCurves.sketchLines.addByTwoPoints(
        sxz(UX - 25 * d[0], UZ - 25 * d[1]),
        sxz(UX + (L + 25) * d[0], UZ + (L + 25) * d[1]))
    ax.isConstruction = True
    p = (-d[1], d[0])
    ri, ro = (SPRING_OD - 2 * SPRING_WIRE) / 2.0, SPRING_OD / 2.0

    def SP(s, rr):
        return (UX + s * d[0] + rr * p[0], UZ + s * d[1] + rr * p[1])
    pts = [SP(s0, ri), SP(s1, ri), SP(s1, ro), SP(s0, ro)]
    ln = sk.sketchCurves.sketchLines
    for i in range(4):
        ln.addByTwoPoints(sxz(*pts[i]), sxz(*pts[(i + 1) % 4]))
    revolve(c, biggest_profile(sk), ax, 360.0, 'new').bodies.item(0).name = name
    b = c.bRepBodies.item(0)
    a = appearance('SPRING')
    if a:
        b.appearance = a
    # Re-apply the physical material.  A freshly built body defaults to steel,
    # which for this ENVELOPE means 51 g instead of the real 25.3 g spring --
    # so skipping this silently adds 26 g per leg to the mass properties.
    try:
        mat = None
        des = design()
        for k in range(des.materials.count):
            if des.materials.item(k).name == 'BENI_Knee_Spring_L':
                mat = des.materials.item(k)
                break
        if mat is None:
            base = _local_material('SPRING')
            if base is not None:
                mat = des.materials.addByCopy(base, 'BENI_Knee_Spring_L')
                _set_density(mat, MASS_OVERRIDE_G['Knee_Spring_L'] / b.volume)
        if mat is not None:
            b.material = mat
    except Exception:
        pass
    return o


def rebuild_spring(phi, phi_mirror=0.0):
    """Rebuild BOTH spring envelopes.

    Both, not one.  This function is called by set_pose(), so if it only built
    the left spring then merely *posing* the model deleted the right leg's
    spring and left the assembly asymmetric -- which is exactly how the right
    leg lost parts in the first place.  Knee_Spring_L is therefore excluded
    from build_mirror() and owned entirely here.

    phi_mirror defaults to 0 and is deliberately NOT phi.  Mirrored occurrences
    are treated as STATIC by classify(), so during a left-leg sweep the right
    leg stays at nominal -- and a right spring built for the left leg's knee
    angle is the wrong length for the un-posed right cartridge and reads as a
    ~300 mm3 interference on the right leg.  Pass phi_mirror explicitly only if
    the right leg is genuinely being posed as well.
    """
    left = _spring_body('Knee_Spring_L', phi, LEG_Y_MID)
    _spring_body('Knee_Spring_L(Mirror)', phi_mirror, -LEG_Y_MID)
    return left


def pose(snap, theta, phi):
    """Place the leg at shoulder angle theta and knee angle phi (degrees).

    Every group matrix is composed onto the occurrence's stored nominal
    transform, so occurrences that carry their own rotation survive.
    """
    d0, L0 = cart_dir(0.0)
    d1, Lp_ = cart_dir(phi)
    psi0 = math.degrees(math.atan2(d0[1], d0[0]))
    psi1 = math.degrees(math.atan2(d1[1], d1[0]))
    dpsi = psi1 - psi0
    dL = Lp_ - L0
    Sh = _rot_arr(theta, 0.0, 0.0)
    Kn = _rot_arr(phi, KX, KZ)
    Cu = _rot_arr(-dpsi, UX, UZ)
    Cl = _mm(_trans_arr((dL * d1[0], 0.0, dL * d1[1])), Cu)
    G = {'PROX': Sh,
         'DIST': _mm(Sh, Kn),
         'CART_UP': _mm(Sh, Cu),
         'CART_LO': _mm(Sh, Cl),
         'SPRING': Sh}
    for o, cls, m0 in snap:
        g = G.get(cls)
        if g is None:
            continue
        o.transform2 = _as_matrix(_mm(g, m0))


_NOMINAL = {}


def capture_nominal(force=False):
    """Cache every occurrence's nominal transform, keyed by entity token.

    pose() must always compose from the NOMINAL state.  Reading the current
    transforms instead compounds successive poses, which silently corrupts the
    assembly (and any snapshot taken from it).
    """
    global _NOMINAL
    if _NOMINAL and not force:
        return _NOMINAL
    r = root()
    _NOMINAL = {}
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        _NOMINAL[o.entityToken] = list(o.transform2.asArray())
    return _NOMINAL


def nominal_snapshot():
    """Build a pose() snapshot list from the cached nominal transforms."""
    nom = capture_nominal()
    r = root()
    out = []
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        m0 = nom.get(o.entityToken)
        if m0 is None:
            m0 = list(o.transform2.asArray())
            nom[o.entityToken] = m0
        out.append((o, classify(o), m0))
    return out


def restore_nominal():
    nom = capture_nominal()
    r = root()
    n = 0
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        m0 = nom.get(o.entityToken)
        if m0 is not None:
            o.transform2 = _as_matrix(m0)
            n += 1
    return n


def set_pose(theta, phi):
    """Rebuild the spring for phi, then pose the whole leg from nominal.

    Order matters: rebuild_spring() adds a feature, and a parametric recompute
    reverts every un-snapshotted occurrence transform.  Build first, pose after.
    """
    capture_nominal()
    rebuild_spring(phi)
    snap = nominal_snapshot()
    pose(snap, theta, phi)
    return snap


def _relocate(m, t_mm):
    a = m.asArray()
    out = list(a)
    out[3] = cm(t_mm[0]); out[7] = cm(t_mm[1]); out[11] = cm(t_mm[2])
    n = adsk.core.Matrix3D.create()
    n.setWithArray(out)
    return n


def _compose_shoulder(theta, k):
    """Apply the shoulder rotation on top of an already-built matrix k."""
    a = math.radians(theta)
    ca, sa = math.cos(a), math.sin(a)
    ka = k.asArray()
    R = [[ka[0], ka[1], ka[2]], [ka[4], ka[5], ka[6]], [ka[8], ka[9], ka[10]]]
    t = [ka[3] * 10, ka[7] * 10, ka[11] * 10]
    S = [[ca, 0, sa], [0, 1, 0], [-sa, 0, ca]]
    RR = [[sum(S[i][q] * R[q][j] for q in range(3)) for j in range(3)]
          for i in range(3)]
    tt = [sum(S[i][q] * t[q] for q in range(3)) for i in range(3)]
    m = adsk.core.Matrix3D.create()
    m.setWithArray([RR[0][0], RR[0][1], RR[0][2], cm(tt[0]),
                    RR[1][0], RR[1][1], RR[1][2], cm(tt[1]),
                    RR[2][0], RR[2][1], RR[2][2], cm(tt[2]),
                    0, 0, 0, 1])
    return m


# ===========================================================================
#  Full-design builders.  build_all() reconstructs every modelled part from
#  scratch in a fixed order, so the design is reproducible from source.
# ===========================================================================

def build_shoulder_plate():
    """Left chassis side panel + shoulder motor interface.

    This is a rectangular lightened panel, not the bare O96 disc the first
    version of this function made.  The panel carries the motor interface at
    the origin, the harness cavity lip, and the bolted joint to Chassis_Frame.
    """
    drop_comp('Chassis_Shoulder_Plate_L')
    occ = new_comp('Chassis_Shoulder_Plate_L'); c = occ.component
    # panel outline, then the O96 lobe around the motor
    sk = sk_on_y(c, SH_PLATE_Y0)
    polyline(sk, [(SH_PANEL_X0, SH_PANEL_Z0), (SH_PANEL_X1, SH_PANEL_Z0),
                  (SH_PANEL_X1, SH_PANEL_Z1), (SH_PANEL_X0, SH_PANEL_Z1)])
    extrude(c, biggest_profile(sk), SH_PLATE_T, 'new').bodies.item(0).name = 'Chassis_Shoulder_Plate_L'
    sk = sk_on_y(c, SH_PLATE_Y0); circle(sk, 0, 0, SH_PLATE_OD)
    extrude(c, sk.profiles.item(0), SH_PLATE_T, 'join')
    # harness cavity lip
    ring(c, CAV_Y0, CAV_R_OUT, CAV_R_OUT + CAV_LIP_T, CAV_Y1 - CAV_Y0, 'join')
    # motor bore, housing bolts, harness grommet, cable-cover bolts
    sk = sk_on_y(c, SH_PLATE_Y0 - 1); circle(sk, 0, 0, 48.0)
    extrude(c, sk.profiles.item(0), SH_PLATE_T + 2, 'cut')
    sk = sk_on_y(c, SH_PLATE_Y0 - 1)
    circles_polar(sk, 0, 0, SH_BOLT_PCD, 3.4, 8, SH_BOLT_A0)
    extrude(c, profiles(sk), SH_PLATE_T + 2, 'cut')
    a = math.radians(200)
    sk = sk_on_y(c, SH_PLATE_Y0 - 1)
    circle(sk, 29 * math.cos(a), 29 * math.sin(a), 7.0)
    extrude(c, sk.profiles.item(0), SH_PLATE_T + 2, 'cut')
    sk = sk_on_y(c, SH_PLATE_Y0 - 1)
    circles_polar(sk, 0, 0, CABLE_COVER_PCD, 3.4, 4, 45.0)
    extrude(c, profiles(sk), SH_PLATE_T + 2, 'cut')
    # joint to Chassis_Frame.  FRAME_BOLTS is the single source of truth for
    # this pattern -- the panel used to carry a sixth hole at (+30, -18) with
    # no matching boss on the frame.  Giving the frame a front-lower leg to
    # reach it would have cost 19-29 g against a 148 g mass margin, and the
    # pattern is nowhere near load-limited (the worst bolt sees 82 N at the
    # 25 N.m proof torque), so the orphan hole is deleted instead.
    sk = sk_on_y(c, SH_PLATE_Y0 - 1)
    for (bx, bz) in FRAME_BOLTS:
        circle(sk, bx, bz, 3.4)
    extrude(c, profiles(sk), SH_PLATE_T + 2, 'cut')
    # lightening windows
    sk = sk_on_y(c, SH_PLATE_Y0 - 1)
    for (x0, z0, x1, z1) in SH_PANEL_WINDOWS:
        polyline(sk, [(x0, z0), (x1, z0), (x1, z1), (x0, z1)])
    extrude(c, profiles(sk), SH_PLATE_T + 2, 'cut')
    return occ


def build_chassis_frame():
    """Centre cage tying the two side panels together.

    Two 4 mm flanges at y = +/-38..42 (each three rectangles), five 4 mm webs
    spanning the full 84 mm between them, and the 5+5 panel bolt holes.
    """
    drop_comp('Chassis_Frame')
    occ = new_comp('Chassis_Frame'); c = occ.component
    first = True
    for y0 in (FRAME_FLANGE_Y, -FRAME_FLANGE_Y - FRAME_T):
        for (x0, z0, x1, z1) in FRAME_FLANGE_RECTS:
            sk = sk_on_y(c, y0)
            polyline(sk, [(x0, z0), (x1, z0), (x1, z1), (x0, z1)])
            e = extrude(c, biggest_profile(sk), FRAME_T, 'new' if first else 'join')
            if first:
                e.bodies.item(0).name = 'Chassis_Frame'
                first = False
    # webs span flange to flange, which is what merges the two sides into one lump
    for (x0, z0, x1, z1) in FRAME_WEB_RECTS:
        sk = sk_on_y(c, -FRAME_FLANGE_Y - FRAME_T)
        polyline(sk, [(x0, z0), (x1, z0), (x1, z1), (x0, z1)])
        extrude(c, biggest_profile(sk), 2 * (FRAME_FLANGE_Y + FRAME_T), 'join')
    for y0 in (FRAME_FLANGE_Y - 1.0, -FRAME_FLANGE_Y - FRAME_T - 1.0):
        sk = sk_on_y(c, y0)
        for (bx, bz) in FRAME_BOLTS:
            circle(sk, bx, bz, 3.4)
        extrude(c, profiles(sk), FRAME_T + 2.0, 'cut')
    return occ


def build_electronics_tray():
    drop_comp('Electronics_Tray')
    occ = new_comp('Electronics_Tray'); c = occ.component
    sk = sk_on_y(c, -TRAY_HALF_W)
    polyline(sk, [(TRAY_X0, TRAY_Z0), (TRAY_X1, TRAY_Z0),
                  (TRAY_X1, TRAY_Z1), (TRAY_X0, TRAY_Z1)])
    extrude(c, biggest_profile(sk), 2 * TRAY_HALF_W,
            'new').bodies.item(0).name = 'Electronics_Tray'
    return occ


def build_battery():
    """4S 2200 mAh pack envelope, 250 g, as far aft as the cage allows.

    Moved aft from a centre of X = -0.5 to X = -30.5.  It cannot null the
    +12 mm forward CoM offset on its own -- that offset is inherent to the
    bent-leg geometry, not to the pack position (see the design record) -- but
    30 mm of pack travel is 2.2 mm of CoM and it is free.
    """
    drop_comp('Battery_4S2200')
    occ = new_comp('Battery_4S2200'); c = occ.component
    sk = sk_on_y(c, -BATT_HALF_W)
    polyline(sk, [(BATT_X0, BATT_Z0), (BATT_X1, BATT_Z0),
                  (BATT_X1, BATT_Z1), (BATT_X0, BATT_Z1)])
    extrude(c, biggest_profile(sk), 2 * BATT_HALF_W,
            'new').bodies.item(0).name = 'Battery_4S2200'
    return occ


def build_electronics_block():
    """Compute + IMU + power distribution + wiring envelope, 120 g.

    Previously this was a bare 120 g line in the BOM with no location, which
    meant the robot's CoM and inertia could not be computed at all.  Modelling
    it as a block with a stated mass and an explicit IMU datum face is what
    makes the mass properties real.
    """
    drop_comp('Chassis_Electronics')
    occ = new_comp('Chassis_Electronics'); c = occ.component
    sk = sk_on_y(c, -ELEC_HALF_W)
    polyline(sk, [(ELEC_X0, ELEC_Z0), (ELEC_X1, ELEC_Z0),
                  (ELEC_X1, ELEC_Z1), (ELEC_X0, ELEC_Z1)])
    extrude(c, biggest_profile(sk), 2 * ELEC_HALF_W,
            'new').bodies.item(0).name = 'Chassis_Electronics'
    # IMU datum: a 12 x 12 pad standing 1.5 mm proud of the block's top face,
    # centred in Y, axes aligned to the robot frame (X fwd, Y left, Z up).
    # This is the reference the CoM and inertia in mass_report() are stated
    # against, so it has to be a real face in the model, not a note.
    sk = sk_on_y(c, -IMU_PAD / 2.0)
    polyline(sk, [(IMU_X - IMU_PAD / 2.0, IMU_Z0), (IMU_X + IMU_PAD / 2.0, IMU_Z0),
                  (IMU_X + IMU_PAD / 2.0, IMU_Z1), (IMU_X - IMU_PAD / 2.0, IMU_Z1)])
    extrude(c, biggest_profile(sk), IMU_PAD, 'join')
    return occ


def build_cable_spiral():
    """Harness clock-spring envelope: r = 20.2 .. 31.8 x 3.6 mm at y = 47.2."""
    drop_comp('Shoulder_Cable_Spiral_L')
    occ = new_comp('Shoulder_Cable_Spiral_L'); c = occ.component
    ring(c, SPIRAL_Y0, SPIRAL_R_IN, SPIRAL_R_OUT, SPIRAL_T,
         'new').bodies.item(0).name = 'Shoulder_Cable_Spiral_L'
    return occ


def build_cable_cover():
    drop_comp('Shoulder_Cable_Cover_L')
    occ = new_comp('Shoulder_Cable_Cover_L'); c = occ.component
    ring(c, CABLE_COVER_Y0, CABLE_COVER_R_IN, CABLE_COVER_R_OUT,
         CABLE_COVER_T, 'new').bodies.item(0).name = 'Shoulder_Cable_Cover_L'
    ring(c, CAV_Y0, 41.0, CABLE_COVER_R_OUT, CABLE_COVER_Y0 - CAV_Y0, 'join')
    sk = sk_on_y(c, CAV_Y0)
    circles_polar(sk, 0, 0, CABLE_COVER_PCD, 4.0, 4, 45.0)
    extrude(c, profiles(sk), COVER_INSERT_DEPTH, 'cut')
    return occ


def build_shoulder_hub(pin_bore_d=4.05,
                       component_name='Shoulder_Output_Hub_L'):
    """Build the shoulder output hub.

    ``pin_bore_d`` and ``component_name`` exist so material/profile fit trials
    can be generated without changing the released nominal hub.  The ordinary
    assembly build still uses the manufacturer-derived Ø4.05 geometry and the
    canonical ``Shoulder_Output_Hub_L`` name.
    """
    drop_comp(component_name)
    occ = new_comp(component_name); c = occ.component
    sk = sk_on_y(c, HUB_Y0); circle(sk, 0, 0, HUB_BODY_D)
    extrude(c, sk.profiles.item(0), HUB_MID_Y - HUB_Y0, 'new').bodies.item(0).name = component_name
    sk = sk_on_y(c, HUB_MID_Y); circle(sk, 0, 0, HUB_FLANGE_D)
    extrude(c, sk.profiles.item(0), HUB_Y1 - HUB_MID_Y, 'join')
    sk = sk_on_y(c, HUB_Y0 - 1); circle(sk, 0, 0, 12.0)
    extrude(c, sk.profiles.item(0), (HUB_Y1 - HUB_Y0) + 2, 'cut')
    sk = sk_on_y(c, HUB_Y0 - 1)
    circles_polar(sk, 0, 0, SH_OUT_PCD, 3.4, 6, SH_OUT_A0)
    extrude(c, profiles(sk), (HUB_Y1 - HUB_Y0) + 2, 'cut')
    sk = sk_on_y(c, 50.5)
    circles_polar(sk, 0, 0, SH_OUT_PCD, 6.2, 6, SH_OUT_A0)
    extrude(c, profiles(sk), HUB_Y1 - 50.5 + 1, 'cut')
    sk = sk_on_y(c, HUB_Y0 - 1)
    circles_polar(sk, 0, 0, SH_PIN_PCD, pin_bore_d, 3, SH_PIN_A0)
    extrude(c, profiles(sk), (HUB_Y1 - HUB_Y0) + 2, 'cut')
    sk = sk_on_y(c, HUB_Y0)
    circles_polar(sk, 0, 0, SH_PIN_PCD, 5.2, 3, SH_PIN_A0)
    extrude(c, profiles(sk), 0.7, 'cut')
    sk = sk_on_y(c, 52.5)
    circles_polar(sk, 0, 0, HUB_LINK_PCD, 3.3, 6, HUB_LINK_A0)
    extrude(c, profiles(sk), HUB_Y1 - 52.5, 'cut')
    a = math.radians(30.4)
    sk = sk_on_y(c, HUB_MID_Y - 1)
    circle(sk, HUB_CABLE_R * math.cos(a), HUB_CABLE_R * math.sin(a), 6.0)
    extrude(c, sk.profiles.item(0), (HUB_Y1 - HUB_MID_Y) + 2, 'cut')
    for ang_deg in (150.4, 270.4):
        ang = math.radians(ang_deg)
        sk = sk_on_y(c, 54.0)
        circle(sk, 21 * math.cos(ang), 21 * math.sin(ang), 11.0)
        extrude(c, sk.profiles.item(0), 5.5, 'cut')
    return occ


def build_knee_hardware():
    drop_comp('HW_Bearing_6800')
    o = new_comp('HW_Bearing_6800'); c = o.component
    ring(c, BRG1_Y0, KNEE_AXLE_D / 2.0, KNEE_BRG_OD / 2.0, KNEE_BRG_W,
         'new', cx=KX, cz=KZ).bodies.item(0).name = 'HW_Bearing_6800'
    m = mat((1, 0, 0), (0, 1, 0), (0, 0, 1), (0.0, BRG2_Y0 - BRG1_Y0, 0.0))
    root().occurrences.addExistingComponent(c, m)

    drop_comp('Knee_Sleeve_L')
    o = new_comp('Knee_Sleeve_L'); c = o.component
    ring(c, SLEEVE_Y0, KNEE_AXLE_D / 2.0, KNEE_SLEEVE_OD / 2.0,
         SLEEVE_Y1 - SLEEVE_Y0, 'new', cx=KX, cz=KZ).bodies.item(0).name = 'Knee_Sleeve_L'
    # Double-D BORE, 8.6 across flats: fill the two lens-shaped slivers between
    # the O10 bore and the chords at x = KX +/- 4.30.  Filling (not cutting) is
    # what makes this a keyed bore -- cutting the OD would split the sleeve.
    for sgn in (1, -1):
        sk = sk_on_y(c, SLEEVE_Y0)
        pts = [(KX + sgn * 4.30, KZ - 2.75), (KX + sgn * 5.30, KZ - 2.75),
               (KX + sgn * 5.30, KZ + 2.75), (KX + sgn * 4.30, KZ + 2.75)]
        ln = sk.sketchCurves.sketchLines
        for i in range(4):
            ln.addByTwoPoints(sxz(*pts[i]), sxz(*pts[(i + 1) % 4]))
        extrude(c, biggest_profile(sk), SLEEVE_Y1 - SLEEVE_Y0, 'join')

    drop_comp('Knee_Axle_L')
    o = new_comp('Knee_Axle_L'); c = o.component
    sk = sk_on_y(c, AXLE_FLANGE_Y0); circle(sk, KX, KZ, AXLE_FLANGE_D)
    extrude(c, sk.profiles.item(0), AXLE_FLANGE_T, 'new').bodies.item(0).name = 'Knee_Axle_L'
    sk = sk_on_y(c, AXLE_Y0); circle(sk, KX, KZ, KNEE_AXLE_D)
    extrude(c, sk.profiles.item(0), AXLE_Y1 - AXLE_Y0, 'join')
    for sgn in (1, -1):
        sk = sk_on_y(c, SLEEVE_Y0)
        pts = [(KX + sgn * 4.20, KZ - 9), (KX + sgn * 9, KZ - 9),
               (KX + sgn * 9, KZ + 9), (KX + sgn * 4.20, KZ + 9)]
        ln = sk.sketchCurves.sketchLines
        for i in range(4):
            ln.addByTwoPoints(sxz(*pts[i]), sxz(*pts[(i + 1) % 4]))
        extrude(c, biggest_profile(sk), SLEEVE_Y1 - SLEEVE_Y0, 'cut')
    sk = sk_on_y(c, AXLE_Y1 - 8.0); circle(sk, KX, KZ, 3.3)
    extrude(c, sk.profiles.item(0), 8.0, 'cut')

    drop_comp('Knee_Magnet_Carrier_L')
    o = new_comp('Knee_Magnet_Carrier_L'); c = o.component
    sk = sk_on_y(c, MAG_CARRIER_Y0); circle(sk, KX, KZ, AXLE_FLANGE_D)
    extrude(c, sk.profiles.item(0), MAG_CARRIER_T, 'new').bodies.item(0).name = 'Knee_Magnet_Carrier_L'
    sk = sk_on_y(c, MAG_CARRIER_Y0 - 8.0); circle(sk, KX, KZ, 4.0)
    extrude(c, sk.profiles.item(0), 8.0, 'join')
    sk = sk_on_y(c, MAG_CARRIER_Y0 + MAG_CARRIER_T - MAG_T)
    circle(sk, KX, KZ, MAG_D + 0.1)
    extrude(c, sk.profiles.item(0), MAG_T + 0.1, 'cut')

    drop_comp('HW_Magnet_D6x2p5_Diametric')
    o = new_comp('HW_Magnet_D6x2p5_Diametric'); c = o.component
    sk = sk_on_y(c, MAG_CARRIER_Y0 + MAG_CARRIER_T - MAG_T)
    circle(sk, KX, KZ, MAG_D)
    extrude(c, sk.profiles.item(0), MAG_T, 'new').bodies.item(0).name = 'HW_Magnet_D6x2p5_Diametric'


def build_cartridge():
    L0 = cart_len(0.0)
    d = ((LX - UX) / L0, (LZ - UZ) / L0)
    p = (-d[1], d[0])
    sp_end = L0 - (CART_DEAD - CART_DEAD_U)
    seat_lo = sp_end + 2.0
    y0 = LEG_Y_MID - 9.5

    def SP(s, rr):
        return (UX + s * d[0] + rr * p[0], UZ + s * d[1] + rr * p[1])

    def rev_ring(comp, s0, s1, r_in, r_out, op='new'):
        sk = sk_on_y(comp, LEG_Y_MID)
        ax = sk.sketchCurves.sketchLines.addByTwoPoints(
            sxz(*SP(-25.0, 0.0)), sxz(*SP(L0 + 25.0, 0.0)))
        ax.isConstruction = True
        pts = [SP(s0, r_in), SP(s1, r_in), SP(s1, r_out), SP(s0, r_out)]
        ln = sk.sketchCurves.sketchLines
        for i in range(4):
            ln.addByTwoPoints(sxz(*pts[i]), sxz(*pts[(i + 1) % 4]))
        return revolve(comp, biggest_profile(sk), ax, 360.0, op)

    def rect(comp, s0, s1, w, h, op):
        sk = sk_on_y(comp, y0)
        q = [SP(s0, -w / 2), SP(s1, -w / 2), SP(s1, w / 2), SP(s0, w / 2)]
        ln = sk.sketchCurves.sketchLines
        for i in range(4):
            ln.addByTwoPoints(sxz(*q[i]), sxz(*q[(i + 1) % 4]))
        return extrude(comp, biggest_profile(sk), h, op)

    drop_comp('Cart_Upper_Eye_L')
    o = new_comp('Cart_Upper_Eye_L'); c = o.component
    sk = sk_on_y(c, y0)
    a = SP(0.0, 0.0); b = SP(2.0, 0.0)
    slot(sk, a[0], a[1], b[0], b[1], 13.0)
    extrude(c, biggest_profile(sk), 19.0, 'new').bodies.item(0).name = 'Cart_Upper_Eye_L'
    rect(c, 2.0, CART_DEAD_U, 20.0, 19.0, 'join')
    rev_ring(c, CART_DEAD_U, CART_DEAD_U + 4.0, 0.0, 13.4 / 2.0, 'join')
    rev_ring(c, 4.0, CART_DEAD_U + 4.5, 0.0, 2.5, 'cut')
    sk = sk_on_y(c, y0 - 1); circle(sk, UX, UZ, 4.15)
    extrude(c, sk.profiles.item(0), 21.0, 'cut')

    drop_comp('Cart_Lower_Eye_L')
    o = new_comp('Cart_Lower_Eye_L'); c = o.component
    sk = sk_on_y(c, y0)
    a = SP(L0, 0.0); b = SP(L0 - 2.0, 0.0)
    slot(sk, a[0], a[1], b[0], b[1], 13.0)
    extrude(c, biggest_profile(sk), 19.0, 'new').bodies.item(0).name = 'Cart_Lower_Eye_L'
    rect(c, seat_lo, L0 - 2.0, 20.0, 19.0, 'join')
    rev_ring(c, seat_lo - 6.0, seat_lo, 0.0, 13.4 / 2.0, 'join')
    rev_ring(c, seat_lo - 6.5, seat_lo + 8.5, 0.0, 2.8, 'cut')
    sk = sk_on_y(c, y0 - 1); circle(sk, LX, LZ, 4.15)
    extrude(c, sk.profiles.item(0), 21.0, 'cut')

    drop_comp('Cart_Guide_Rod_L')
    o = new_comp('Cart_Guide_Rod_L'); c = o.component
    rev_ring(c, 4.0, 54.0, 0.0, ROD_D / 2.0, 'new').bodies.item(0).name = 'Cart_Guide_Rod_L'

    drop_comp('Cart_Preload_Shim_L')
    o = new_comp('Cart_Preload_Shim_L'); c = o.component
    rev_ring(c, sp_end, sp_end + 0.5, 6.8, 9.5, 'new').bodies.item(0).name = 'Cart_Preload_Shim_L'
    for k in range(1, 4):
        off = k * 0.5
        m = mat((1, 0, 0), (0, 1, 0), (0, 0, 1), (d[0] * off, 0.0, d[1] * off))
        root().occurrences.addExistingComponent(c, m)

    drop_comp('HW_ClevisPin_D4x32')
    o = new_comp('HW_ClevisPin_D4x32'); c = o.component
    sk = sk_on_y(c, LEG_Y_IN - 2.0); circle(sk, UX, UZ, 7.5)
    extrude(c, sk.profiles.item(0), 2.0, 'new').bodies.item(0).name = 'HW_ClevisPin_D4x32'
    sk = sk_on_y(c, LEG_Y_IN); circle(sk, UX, UZ, CART_PIN_D)
    extrude(c, sk.profiles.item(0), 31.5, 'join')
    root().occurrences.addExistingComponent(
        c, mat((1, 0, 0), (0, 1, 0), (0, 0, 1), (LX - UX, 0.0, LZ - UZ)))
    rebuild_spring(0.0)


def build_knee_stop():
    half = slot_half_angle()
    a_flex = STOP_PIN_A0 - PHI_STOP
    a_ext = STOP_PIN_A0 - PHI_EXT
    e_flex = a_flex - half
    e_ext = a_ext + half
    bf = (STOP_PIN_A0 - PHI_BUMP) - half
    be = (STOP_PIN_A0 + 6.5) + half
    df = math.degrees(7.5 / STOP_R)
    de = math.degrees(3.0 / STOP_R)
    r0, r1 = STOP_R - STOP_SLOT_W / 2.0, STOP_R + STOP_SLOT_W / 2.0
    MID = STOP_ARC_Y0 + 1.5

    drop_comp('Knee_Stop_Arc_L')
    o = new_comp('Knee_Stop_Arc_L'); c = o.component
    sk = sk_on_y(c, STOP_ARC_Y0)
    arc_sector(sk, KX, KZ, 11.0, 35.5, bf - df - 6.0, max(STOP_BOLT_A) + 12.0)
    extrude(c, biggest_profile(sk), STOP_ARC_T, 'new').bodies.item(0).name = 'Knee_Stop_Arc_L'
    sk = sk_on_y(c, STOP_ARC_Y0 - 1)
    arc_sector(sk, KX, KZ, r0, r1, a_flex, a_ext)
    p1 = kpt(STOP_R, a_flex); p2 = kpt(STOP_R, a_ext)
    circle(sk, p1[0], p1[1], STOP_SLOT_W)
    circle(sk, p2[0], p2[1], STOP_SLOT_W)
    extrude(c, profiles(sk), STOP_ARC_T + 2, 'cut')
    sk = sk_on_y(c, MID)
    arc_sector(sk, KX, KZ, r0, r1, bf - df, e_flex)
    extrude(c, biggest_profile(sk), (STOP_ARC_Y0 + STOP_ARC_T) - MID + 0.5, 'cut')
    sk = sk_on_y(c, MID)
    arc_sector(sk, KX, KZ, r0, r1, e_ext, be + de)
    extrude(c, biggest_profile(sk), (STOP_ARC_Y0 + STOP_ARC_T) - MID + 0.5, 'cut')
    sk = sk_on_y(c, STOP_ARC_Y0 - 1)
    for ang in STOP_BOLT_A:
        w = kpt(STOP_BOLT_R, ang); circle(sk, w[0], w[1], 3.4)
    extrude(c, profiles(sk), STOP_ARC_T + 2, 'cut')

    drop_comp('HW_DowelPin_D6x9')
    o = new_comp('HW_DowelPin_D6x9'); c = o.component
    q = kpt(STOP_R, STOP_PIN_A0)
    sk = sk_on_y(c, CH_Y1); circle(sk, q[0], q[1], STOP_PIN_D)
    extrude(c, sk.profiles.item(0), 9.0, 'new').bodies.item(0).name = 'HW_DowelPin_D6x9'

    for nm, a0, a1 in (('Knee_Bumper_Flex_L', bf - df + 0.4, bf - 0.4),
                       ('Knee_Bumper_Ext_L', be + 0.4, be + de - 0.4)):
        drop_comp(nm)
        oo = new_comp(nm); cc = oo.component
        sk = sk_on_y(cc, MID)
        arc_sector(sk, KX, KZ, 28.6, 31.4, a0, a1)
        extrude(cc, biggest_profile(sk), 1.4, 'new').bodies.item(0).name = nm


def build_encoder():
    drop_comp('Knee_Encoder_PCB_L')
    o = new_comp('Knee_Encoder_PCB_L'); c = o.component
    sk = sk_on_y(c, 98.3)
    pts = [(KX - 7, KZ - 7), (KX + 7, KZ - 7), (KX + 7, KZ + 7), (KX - 7, KZ + 7)]
    ln = sk.sketchCurves.sketchLines
    for i in range(4):
        ln.addByTwoPoints(sxz(*pts[i]), sxz(*pts[(i + 1) % 4]))
    extrude(c, biggest_profile(sk), 1.6, 'new').bodies.item(0).name = 'Knee_Encoder_PCB_L'
    sk = sk_on_y(c, 97.3)
    pts = [(KX - 2.5, KZ - 2.5), (KX + 2.5, KZ - 2.5), (KX + 2.5, KZ + 2.5), (KX - 2.5, KZ + 2.5)]
    ln = sk.sketchCurves.sketchLines
    for i in range(4):
        ln.addByTwoPoints(sxz(*pts[i]), sxz(*pts[(i + 1) % 4]))
    extrude(c, biggest_profile(sk), 1.0, 'join')

    drop_comp('Knee_Encoder_Bracket_L')
    o = new_comp('Knee_Encoder_Bracket_L'); c = o.component
    sk = sk_on_y(c, 99.9); circle(sk, KX, KZ, 34.0)
    extrude(c, biggest_profile(sk), 2.0, 'new').bodies.item(0).name = 'Knee_Encoder_Bracket_L'
    for ang in (60.0, 140.0):
        w = kpt(15.0, ang)
        sk = sk_on_y(c, KNEE_BOSS_B_Y1); circle(sk, w[0], w[1], 9.0)
        extrude(c, sk.profiles.item(0), 99.9 - KNEE_BOSS_B_Y1, 'join')
    for ang in (60.0, 140.0):
        w = kpt(15.0, ang)
        sk = sk_on_y(c, KNEE_BOSS_B_Y1); circle(sk, w[0], w[1], 3.4)
        extrude(c, sk.profiles.item(0), 99.9 - KNEE_BOSS_B_Y1 + 2.5, 'cut')
    sk = sk_on_y(c, 99.9); circle(sk, KX, KZ, 8.0)
    extrude(c, sk.profiles.item(0), 2.5, 'cut')
    # driver clearance over the three knee-stop screws
    sk = sk_on_y(c, 99.9)
    for ang in STOP_BOLT_A:
        w = kpt(STOP_BOLT_R, ang); circle(sk, w[0], w[1], 5.0)
    extrude(c, profiles(sk), 2.5, 'cut')


WH_HUB_Y_A, WH_HUB_Y_B = 94.5, 100.5
RIM_BOLT_PCD = 46.0
RIM_WEB_Y_A, RIM_WEB_Y_B = 100.5, 104.5

# --- tyre retention (added; the tyre used to be a plain annulus) -----------
# As modelled the tyre ID was exactly the rim seat OD, so there was no press
# fit, no bead, and no axial lip: a smooth TPU ring on a smooth PA-CF drum
# that would spin under braking and walk off inboard.  Three fixes:
#   1. a bead groove in the drum with a matching rib in the tyre  -> torque
#      and axial lock that does not depend on friction at all;
#   2. an inboard flange the tyre butts against  -> it cannot walk off;
#   3. a crowned tread  -> a contact patch instead of a 30 mm line, so the
#      machine tolerates camber and the contact point is estimable.
# The tyre is modelled in its INSTALLED (stretched) state at ID O96 so it does
# not read as a permanent interference in every future audit.  The free-state
# ID is O94 -- 2 mm of stretch -- and that is what the BOM orders.
RIM_Y0 = 68.0             # drum inboard edge (was 69.0; 1 mm added for the flange)
RIM_FLANGE_OD = 104.0     # inboard retaining flange, r = 52
RIM_FLANGE_Y0 = 68.0
RIM_FLANGE_Y1 = 69.0
RIM_GROOVE_R = 46.5       # bead groove floor radius (1.5 mm deep in the drum)
RIM_GROOVE_Y0 = 82.5      # 3 mm wide, centred on the tyre centre plane y = 84
RIM_GROOVE_Y1 = 85.5
TYRE_ID = 96.0            # installed / modelled
TYRE_FREE_ID = 94.0       # free state -- BOM callout, 2 mm stretch
TYRE_CROWN_DROP = 0.75    # OD drop from centre to each edge -> R approx 150 mm


def build_wheel():
    drop_comp('Wheel_Hub_L')
    o = new_comp('Wheel_Hub_L'); c = o.component
    sk = sk_on_y(c, WH_HUB_Y_A); circle(sk, WX, WZ, 56.0)
    extrude(c, sk.profiles.item(0), WH_HUB_Y_B - WH_HUB_Y_A, 'new').bodies.item(0).name = 'Wheel_Hub_L'
    sk = sk_on_y(c, WH_HUB_Y_A); circle(sk, WX, WZ, 37.3)
    extrude(c, sk.profiles.item(0), 0.8, 'cut')
    sk = sk_on_y(c, WH_HUB_Y_A - 1)
    circles_polar(sk, WX, WZ, WM_OUT_PCD, 3.4, 3, WM_OUT_A0)
    extrude(c, profiles(sk), (WH_HUB_Y_B - WH_HUB_Y_A) + 2, 'cut')
    sk = sk_on_y(c, WH_HUB_Y_B - 2.5)
    circles_polar(sk, WX, WZ, WM_OUT_PCD, 6.5, 3, WM_OUT_A0)
    extrude(c, profiles(sk), 3.0, 'cut')
    sk = sk_on_y(c, WH_HUB_Y_B - 6.0)
    circles_polar(sk, WX, WZ, RIM_BOLT_PCD, 3.3, 6, 0.0)
    extrude(c, profiles(sk), 6.0, 'cut')
    sk = sk_on_y(c, WH_HUB_Y_A - 1); circle(sk, WX, WZ, 12.0)
    extrude(c, sk.profiles.item(0), (WH_HUB_Y_B - WH_HUB_Y_A) + 2, 'cut')

    drop_comp('Wheel_Rim_L')
    o = new_comp('Wheel_Rim_L'); c = o.component
    ring(c, RIM_WEB_Y_A, 20.0, 45.0, RIM_WEB_Y_B - RIM_WEB_Y_A, 'new',
         cx=WX, cz=WZ).bodies.item(0).name = 'Wheel_Rim_L'
    # drum now starts at RIM_Y0 so the inboard flange shares its O96 face
    # rather than meeting it on an edge (which would be non-manifold).
    ring(c, RIM_Y0, 44.0, RIM_OD / 2.0, RIM_WEB_Y_B - RIM_Y0, 'join', cx=WX, cz=WZ)
    ring(c, WHEEL_Y0, 30.0, 44.0, 3.0, 'join', cx=WX, cz=WZ)
    # inboard retaining flange.  It has to live outboard of y = 67.5, because
    # that is where the distal link's O112 relief starts -- inboard of it the
    # fork arms are still full section out to r ~ 84 from the wheel axis.
    ring(c, RIM_FLANGE_Y0, RIM_OD / 2.0, RIM_FLANGE_OD / 2.0,
         RIM_FLANGE_Y1 - RIM_FLANGE_Y0, 'join', cx=WX, cz=WZ)
    # bead groove
    ring(c, RIM_GROOVE_Y0, RIM_GROOVE_R, RIM_OD / 2.0 + 0.01,
         RIM_GROOVE_Y1 - RIM_GROOVE_Y0, 'cut', cx=WX, cz=WZ)
    sk = sk_on_y(c, RIM_WEB_Y_A - 1)
    circles_polar(sk, WX, WZ, RIM_BOLT_PCD, 4.3, 6, 0.0)
    extrude(c, profiles(sk), (RIM_WEB_Y_B - RIM_WEB_Y_A) + 2, 'cut')
    sk = sk_on_y(c, RIM_WEB_Y_A - 1)
    circles_polar(sk, WX, WZ, 66.0, 14.0, 6, 30.0)
    extrude(c, profiles(sk), (RIM_WEB_Y_B - RIM_WEB_Y_A) + 2, 'cut')

    drop_comp('Wheel_Tyre_L')
    o = new_comp('Wheel_Tyre_L'); c = o.component
    ri = TYRE_ID / 2.0                       # 48.0, installed
    rg = RIM_GROOVE_R                        # 46.5, the rib crest
    ro = WHEEL_OD / 2.0                      # 55.0 at the centre plane
    re = ro - TYRE_CROWN_DROP                # 54.25 at each edge
    y0, y1 = WHEEL_Y0, WHEEL_Y1              # 69.0 .. 99.0
    ym = (y0 + y1) / 2.0                     # 84.0
    pts = [(ri, y0), (ri, RIM_GROOVE_Y0), (rg, RIM_GROOVE_Y0),
           (rg, RIM_GROOVE_Y1), (ri, RIM_GROOVE_Y1), (ri, y1),
           (re, y1), (re, y0)]
    # segment 6 is the tread: arc from (re, y1) to (re, y0) via (ro, ym)
    rev_profile(c, WX, WZ, pts, arcs=[(6, ro, ym)],
                op='new').bodies.item(0).name = 'Wheel_Tyre_L'


def build_fasteners():
    for nm in ('HW_SHCS_M3x6', 'HW_SHCS_M3x10', 'HW_SHCS_M3x8',
               'HW_SHCS_M2p5x12', 'HW_SHCS_M4x10', 'HW_SHCS_M3x16'):
        drop_comp(nm)
    s = screw_comp('HW_SHCS_M3x10', 3.0, 10.0)
    place_polar(s, SH_BOLT_PCD, 8, SH_BOLT_A0, SH_PLATE_Y1)
    place_polar(s, SH_OUT_PCD, 6, SH_OUT_A0, 50.5)
    s4 = screw_comp('HW_SHCS_M4x10', 4.0, 10.0)
    place_polar(s4, HUB_LINK_PCD, 6, HUB_LINK_A0, 63.3)
    place_polar(s4, RIM_BOLT_PCD, 6, 0.0, RIM_WEB_Y_B, cx=WX, cz=WZ)
    s8 = screw_comp('HW_SHCS_M3x8', 3.0, 8.0)
    # cable cover: 5 mm through the plate + 3 mm into a 5 mm insert whose bore
    # runs y = 47 .. 52.  An M3 x 10 here overshot the bore floor by 1.0 mm.
    place_polar(s8, CABLE_COVER_PCD, 4, 45.0, SH_PLATE_Y0, flip=True)
    place_polar(s8, WM_OUT_PCD, 3, WM_OUT_A0, WH_HUB_Y_B - 2.5, cx=WX, cz=WZ)
    # knee stop arc: 3 mm of steel plate + 3 mm into a 5 mm insert.  An M3 x 8
    # here reached 0.5 mm past the bore floor and bottomed out before clamping.
    s6 = screw_comp('HW_SHCS_M3x6', 3.0, 6.0)
    for ang in STOP_BOLT_A:
        w = kpt(STOP_BOLT_R, ang)
        place(s6, w[0], w[1], STOP_ARC_Y0 + STOP_ARC_T)
    s25 = screw_comp('HW_SHCS_M2p5x12', 2.5, 12.0)
    place_polar(s25, WM_BOLT_PCD, 6, WM_BOLT_A0, LEG_Y_IN, flip=True, cx=WX, cz=WZ)
    s16 = screw_comp('HW_SHCS_M3x16', 3.0, 16.0)
    for ang in (60.0, 140.0):
        w = kpt(15.0, ang)
        place(s16, w[0], w[1], 101.9)
    # remove the master occurrences that sit at the origin
    r = root()
    for nm in ('HW_SHCS_M3x6', 'HW_SHCS_M3x10', 'HW_SHCS_M3x8',
               'HW_SHCS_M2p5x12', 'HW_SHCS_M4x10', 'HW_SHCS_M3x16'):
        occs = [r.occurrences.item(i) for i in range(r.occurrences.count)
                if base_name(r.occurrences.item(i).component.name) == nm]
        for o in occs:
            t = o.transform2.translation
            if abs(t.x) < 1e-9 and abs(t.y) < 1e-9 and abs(t.z) < 1e-9 and len(occs) > 1:
                o.deleteMe(); break


def build_all(log=None):
    """Reconstruct every modelled part of the LEFT leg and the centre chassis.

    This really does mean every part now.  Chassis_Frame, Electronics_Tray,
    Battery_4S2200 and Shoulder_Cable_Spiral_L used to exist only in the model
    with no builder, and build_shoulder_plate() had drifted to an older panel
    revision, so calling build_all() would silently delete the panel-to-frame
    joint and leave the frame orphaned.  Verified against the model by
    audit_source_parity().

    Call build_mirror() afterwards to regenerate the right leg.
    """
    def say(m):
        if log is not None:
            log.append(m)
    build_shoulder_plate();     say('shoulder side panel')
    build_cable_cover();        say('cable cover')
    build_cable_spiral();       say('harness spiral envelope')
    build_shoulder_hub();       say('shoulder output hub')
    build_proximal_link();      say('proximal link')
    build_distal_link();        say('distal link')
    build_knee_hardware();      say('knee axle / sleeve / bearings / magnet')
    build_cartridge();          say('spring cartridge')
    build_knee_stop();          say('knee stops + bumpers')
    build_encoder();            say('knee encoder')
    build_wheel();              say('wheel hub / rim / tyre')
    build_chassis_frame();      say('chassis frame')
    build_electronics_tray();   say('electronics tray')
    build_battery();            say('battery')
    build_electronics_block();  say('electronics block + IMU datum')
    build_fasteners();          say('fasteners')
    add_fillets();              say('fillets')
    apply_appearances();        say('appearances')
    # new_comp() -> addNewComponent() leaves the last sub-component as the active
    # edit target, and Fusion ghosts everything outside it.  Always hand the
    # edit target back to the root or the whole model renders translucent.
    design().activateRootComponent()
    say('root reactivated')
