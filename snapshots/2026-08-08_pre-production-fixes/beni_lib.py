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
KNEE_BRG_OD = 19.0
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
    o = find_occ(name, parent)
    if o:
        o.deleteMe()
        return True
    return False


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
    'HW_SHCS_M3x8': 'STEEL',
    'HW_SHCS_M3x10': 'STEEL',
    'HW_SHCS_M3x14': 'STEEL',
    'HW_SHCS_M4x14': 'STEEL',
    'Chassis_Frame': 'PACF',
    'Chassis_Deck_Top': 'ABS',
    'Chassis_Deck_Bottom': 'ABS',
    'Battery_4S2200': 'ABS',
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


def lozenge(sk, c1, r1, c2, r2, frame=None):
    """Closed tangent-line lozenge between two circles.

    c1, c2 are (u, v) centres in the given frame (or global XZ if frame None),
    r1, r2 their radii.  frame is a function (u, v) -> (X, Z).
    """
    f = frame or (lambda u, v: (u, v))
    d = math.hypot(c2[0] - c1[0], c2[1] - c1[1])
    base = math.atan2(c2[1] - c1[1], c2[0] - c1[0])
    alpha = math.asin(max(-1.0, min(1.0, (r1 - r2) / d)))
    th = math.pi / 2.0 + alpha
    arcs = sk.sketchCurves.sketchArcs
    lines = sk.sketchCurves.sketchLines

    def on(c, r, ang):
        return f(c[0] + r * math.cos(base + ang), c[1] + r * math.sin(base + ang))
    p1u = on(c1, r1, th)
    p2u = on(c2, r2, th)
    p1l = on(c1, r1, -th)
    p2l = on(c2, r2, -th)
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
STOP_BOLT_A = (240.0, 260.0, 280.0)


def pl_ep(u):
    d = 120.0
    al = math.asin((PL_R1 - PL_R2) / d)
    th = math.pi / 2 + al
    p1 = (PL_R1 * math.cos(th), PL_R1 * math.sin(th))
    p2 = (d + PL_R2 * math.cos(th), PL_R2 * math.sin(th))
    t = (u - p1[0]) / (p2[0] - p1[0])
    return p1[1] + t * (p2[1] - p1[1])


def dl_epd(u):
    return 33.96 - 0.07636 * (u - 41.86)


def kpt(r, a_deg):
    """Point at radius r and global XZ angle a_deg measured from the knee."""
    a = math.radians(a_deg)
    return (KX + r * math.cos(a), KZ + r * math.sin(a))


def slot_half_angle():
    return math.degrees(math.asin((STOP_SLOT_W / 2.0) / STOP_R))


def build_proximal_link():
    drop_comp('Proximal_Link_L')
    occ = new_comp('Proximal_Link_L')
    c = occ.component
    sk = sk_on_y(c, LEG_Y_IN)
    lozenge(sk, (0.0, 0.0), PL_R1, (120.0, 0.0), PL_R2, frame=prox_uv)
    e = extrude(c, biggest_profile(sk), LEG_W, 'new')
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

    # root pad and knee boss thickening
    sk = sk_on_y(c, CH_Y0); circle(sk, 0, 0, ROOT_DISC_D)
    extrude(c, sk.profiles.item(0), ROOT_PLATE_Y1 - CH_Y0, 'join')
    sk = sk_on_y(c, KNEE_BOSS_A_Y0); circle(sk, KX, KZ, 2 * PL_R2)
    extrude(c, sk.profiles.item(0), LEG_Y_IN - KNEE_BOSS_A_Y0, 'join')
    sk = sk_on_y(c, LEG_Y_OUT); circle(sk, KX, KZ, 2 * PL_R2)
    extrude(c, sk.profiles.item(0), KNEE_BOSS_B_Y1 - LEG_Y_OUT, 'join')

    # knee bearing pockets + O17 retaining lips
    sk = sk_on_y(c, BRG1_Y0); circle(sk, KX, KZ, KNEE_BRG_OD)
    extrude(c, sk.profiles.item(0), BRG1_Y1 - BRG1_Y0, 'cut')
    sk = sk_on_y(c, BRG2_Y0); circle(sk, KX, KZ, KNEE_BRG_OD)
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
    extrude(c, profiles(sk), LEG_Y_OUT - CH_Y1 + 0.5, 'cut')
    sk = sk_on_y(c, CH_Y1); circle(sk, 0, 0, 34.0)
    extrude(c, sk.profiles.item(0), LEG_Y_OUT - CH_Y1 + 0.5, 'cut')
    # O34 access bore straight through the root pad as well, so a hex key can
    # reach the six M3 output-hub screws without removing the link.
    sk = sk_on_y(c, LEG_Y_IN - 1); circle(sk, 0, 0, 34.0)
    extrude(c, sk.profiles.item(0), ROOT_PLATE_T + 2, 'cut')

    # harness pass-through, aligned with the hub cable hole
    a = math.radians(30.4)
    sk = sk_on_y(c, LEG_Y_IN - 1)
    circle(sk, 21 * math.cos(a), 21 * math.sin(a), 8.0)
    extrude(c, sk.profiles.item(0), ROOT_PLATE_T + 2, 'cut')

    # Steel knee-stop arc: 3x M3 heat-set inserts, blind from the arm-B boss
    # face.  These MUST stay blind -- a through bolt would put its nut inside
    # the spring channel and inside the distal link's knee web.
    sk = sk_on_y(c, KNEE_BOSS_B_Y1 - 4.5)
    for ang in STOP_BOLT_A:
        w = kpt(STOP_BOLT_R, ang); circle(sk, w[0], w[1], 4.0)
    extrude(c, profiles(sk), 4.5, 'cut')

    # 2x M3 heat-set inserts for the knee encoder bracket
    sk = sk_on_y(c, KNEE_BOSS_B_Y1 - 5.0)
    for ang in (60.0, 140.0):
        w = kpt(15.0, ang); circle(sk, w[0], w[1], 4.0)
    extrude(c, profiles(sk), 5.0, 'cut')

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
                'Shoulder_Cable_Cover_L', 'Chassis_Frame', 'Chassis_Deck_Top',
                'Chassis_Deck_Bottom', 'Battery_4S2200', 'Electronics_Tray')
PROX_NAMES = ('Shoulder_Output_Hub_L', 'Proximal_Link_L', 'HW_Bearing_6800',
              'Knee_Stop_Arc_L', 'Knee_Bumper_Flex_L', 'Knee_Bumper_Ext_L',
              'Knee_Encoder_Bracket_L', 'Knee_Encoder_PCB_L', 'HW_SHCS_M3x16')
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
        return 'DIST' if cz < -120 else 'PROX'
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


def rebuild_spring(phi):
    """Rebuild the spring envelope for knee angle phi."""
    drop_comp('Knee_Spring_L')
    o = new_comp('Knee_Spring_L')
    c = o.component
    d, L = cart_dir(phi)
    s0, s1 = CART_DEAD_U, L - (CART_DEAD - CART_DEAD_U)
    sk = sk_on_y(c, LEG_Y_MID)
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
    revolve(c, biggest_profile(sk), ax, 360.0, 'new').bodies.item(0).name = 'Knee_Spring_L'
    a = appearance('SPRING')
    if a:
        c.bRepBodies.item(0).appearance = a
    return o


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
    drop_comp('Chassis_Shoulder_Plate_L')
    occ = new_comp('Chassis_Shoulder_Plate_L'); c = occ.component
    sk = sk_on_y(c, SH_PLATE_Y0); circle(sk, 0, 0, SH_PLATE_OD)
    extrude(c, biggest_profile(sk), SH_PLATE_T, 'new').bodies.item(0).name = 'Chassis_Shoulder_Plate_L'
    ring(c, CAV_Y0, CAV_R_OUT, CAV_R_OUT + CAV_LIP_T, CAV_Y1 - CAV_Y0, 'join')
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
    return occ


def build_cable_cover():
    drop_comp('Shoulder_Cable_Cover_L')
    occ = new_comp('Shoulder_Cable_Cover_L'); c = occ.component
    ring(c, CABLE_COVER_Y0, CABLE_COVER_R_IN, CABLE_COVER_R_OUT,
         CABLE_COVER_T, 'new').bodies.item(0).name = 'Shoulder_Cable_Cover_L'
    ring(c, CAV_Y0, 41.0, CABLE_COVER_R_OUT, CABLE_COVER_Y0 - CAV_Y0, 'join')
    sk = sk_on_y(c, CAV_Y0)
    circles_polar(sk, 0, 0, CABLE_COVER_PCD, 4.0, 4, 45.0)
    extrude(c, profiles(sk), 4.0, 'cut')
    return occ


def build_shoulder_hub():
    drop_comp('Shoulder_Output_Hub_L')
    occ = new_comp('Shoulder_Output_Hub_L'); c = occ.component
    sk = sk_on_y(c, HUB_Y0); circle(sk, 0, 0, HUB_BODY_D)
    extrude(c, sk.profiles.item(0), HUB_MID_Y - HUB_Y0, 'new').bodies.item(0).name = 'Shoulder_Output_Hub_L'
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
    circles_polar(sk, 0, 0, SH_PIN_PCD, 4.05, 3, SH_PIN_A0)
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
    ring(c, WHEEL_Y0, 44.0, RIM_OD / 2.0, RIM_WEB_Y_B - WHEEL_Y0, 'join', cx=WX, cz=WZ)
    ring(c, WHEEL_Y0, 30.0, 44.0, 3.0, 'join', cx=WX, cz=WZ)
    sk = sk_on_y(c, RIM_WEB_Y_A - 1)
    circles_polar(sk, WX, WZ, RIM_BOLT_PCD, 4.3, 6, 0.0)
    extrude(c, profiles(sk), (RIM_WEB_Y_B - RIM_WEB_Y_A) + 2, 'cut')
    sk = sk_on_y(c, RIM_WEB_Y_A - 1)
    circles_polar(sk, WX, WZ, 66.0, 14.0, 6, 30.0)
    extrude(c, profiles(sk), (RIM_WEB_Y_B - RIM_WEB_Y_A) + 2, 'cut')

    drop_comp('Wheel_Tyre_L')
    o = new_comp('Wheel_Tyre_L'); c = o.component
    ring(c, WHEEL_Y0, RIM_OD / 2.0, WHEEL_OD / 2.0, WHEEL_Y1 - WHEEL_Y0,
         'new', cx=WX, cz=WZ).bodies.item(0).name = 'Wheel_Tyre_L'


def build_fasteners():
    for nm in ('HW_SHCS_M3x10', 'HW_SHCS_M3x8', 'HW_SHCS_M2p5x12',
               'HW_SHCS_M4x10', 'HW_SHCS_M3x16'):
        drop_comp(nm)
    s = screw_comp('HW_SHCS_M3x10', 3.0, 10.0)
    place_polar(s, SH_BOLT_PCD, 8, SH_BOLT_A0, SH_PLATE_Y1)
    place_polar(s, SH_OUT_PCD, 6, SH_OUT_A0, 50.5)
    place_polar(s, CABLE_COVER_PCD, 4, 45.0, SH_PLATE_Y0, flip=True)
    s4 = screw_comp('HW_SHCS_M4x10', 4.0, 10.0)
    place_polar(s4, HUB_LINK_PCD, 6, HUB_LINK_A0, 63.3)
    place_polar(s4, RIM_BOLT_PCD, 6, 0.0, RIM_WEB_Y_B, cx=WX, cz=WZ)
    s8 = screw_comp('HW_SHCS_M3x8', 3.0, 8.0)
    for ang in STOP_BOLT_A:
        w = kpt(STOP_BOLT_R, ang)
        place(s8, w[0], w[1], STOP_ARC_Y0 + STOP_ARC_T)
    place_polar(s8, WM_OUT_PCD, 3, WM_OUT_A0, WH_HUB_Y_B - 2.5, cx=WX, cz=WZ)
    s25 = screw_comp('HW_SHCS_M2p5x12', 2.5, 12.0)
    place_polar(s25, WM_BOLT_PCD, 6, WM_BOLT_A0, LEG_Y_IN, flip=True, cx=WX, cz=WZ)
    s16 = screw_comp('HW_SHCS_M3x16', 3.0, 16.0)
    for ang in (60.0, 140.0):
        w = kpt(15.0, ang)
        place(s16, w[0], w[1], 101.9)
    # remove the master occurrences that sit at the origin
    r = root()
    for nm in ('HW_SHCS_M3x10', 'HW_SHCS_M3x8', 'HW_SHCS_M2p5x12',
               'HW_SHCS_M4x10', 'HW_SHCS_M3x16'):
        occs = [r.occurrences.item(i) for i in range(r.occurrences.count)
                if base_name(r.occurrences.item(i).component.name) == nm]
        for o in occs:
            t = o.transform2.translation
            if abs(t.x) < 1e-9 and abs(t.y) < 1e-9 and abs(t.z) < 1e-9 and len(occs) > 1:
                o.deleteMe(); break


def build_all(log=None):
    def say(m):
        if log is not None:
            log.append(m)
    build_shoulder_plate();   say('shoulder plate')
    build_cable_cover();      say('cable cover')
    build_shoulder_hub();     say('shoulder output hub')
    build_proximal_link();    say('proximal link')
    build_distal_link();      say('distal link')
    build_knee_hardware();    say('knee axle / sleeve / bearings / magnet')
    build_cartridge();        say('spring cartridge')
    build_knee_stop();        say('knee stops + bumpers')
    build_encoder();          say('knee encoder')
    build_wheel();            say('wheel hub / rim / tyre')
    build_fasteners();        say('fasteners')
    apply_appearances();      say('appearances')
    # new_comp() -> addNewComponent() leaves the last sub-component as the active
    # edit target, and Fusion ghosts everything outside it.  Always hand the
    # edit target back to the root or the whole model renders translucent.
    design().activateRootComponent()
    say('root reactivated')
