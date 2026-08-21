"""Builders for the Beni single-leg test rig (`Beni_SingleLegRig`).

Companion to `beni_lib.py`, which owns the leg itself and whose helpers this
module reuses wholesale.  Same conventions:

    X = forward (fore-aft)      Y = left, +Y outboard      Z = up
    shoulder axis = the global Y axis through the origin
    all public dimensions in millimetres

Brief: `fusion_brief_single_leg_rig.md`.  Frozen inputs: the guide's §4-§9
kinematics, `beni_prototype1_design_record.md` §2 motor interfaces, and the
leg's own frozen lateral stack (`beni_lib` SHOULDER_Y .. WHEEL_Y1).

WHY THE CARRIAGE HANGS OFF THE FRONT FACE.  The motor also has 8 x M3 tapped
4.8 mm deep in its *rear* face on the same O74 PCD, and bolting the carriage
there would put the aluminium housing in the load path instead of a 5 mm
printed panel -- stiffer, and 26 mm more overhang which §4.1's own sensitivity
says is immaterial.  It was rejected anyway, because
`GAUGE_Shoulder_Motor_Interface.stl` models only the front 9.5 mm of the motor.
The brief requires every interface to be gated on that coupon, so the
structural joint has to live on the face the coupon can actually check.
"""

import math

import adsk.core
import adsk.fusion

import beni_lib
from beni_lib import (cm, mat, new_comp, drop_comp, sk_on_y, sxz, circle,
                      circles_polar, polyline, arc_sector, slot, extrude,
                      profiles, biggest_profile, cyl_y, ring, root, find_occ,
                      base_name, bbox_of, fmt_bbox, place, place_polar,
                      set_material)

# ============================================================ frozen leg data
PANEL_Y0, PANEL_Y1 = 42.0, 47.0        # Chassis_Shoulder_Plate_L, reused as-is
PANEL_X0, PANEL_X1 = -72.0, 48.0
PANEL_Z0, PANEL_Z1 = -48.0, 72.0
MOTOR_R = 40.0                          # GIM6010-8 housing O80, y 17..41
MOTOR_LAND_R = 39.0                     # front mounting land outer radius
HALF_TRACK = 84.0
WHEEL_R = 55.0
Z_WHEEL_AXIS = -154.269                 # shoulder axis to wheel axis at phi=0

# Panel holes measured off the model, not assumed.  The five frame bolts are
# the rig's structural joint; the four O88 cover holes are freed by deleting
# the clock spring (brief §2.4) and are left open as a stiffening option.
PANEL_FRAME_BOLTS = [(-60.0, -18.0), (-60.0, 48.0), (-60.0, 62.0),
                     (30.0, 48.0), (30.0, 62.0)]
PANEL_COVER_PCD = 88.0

# ================================================================ rig, Y stack
CARR_Y1 = PANEL_Y0                      # 42.0 carriage pad face
CARR_T = 8.0
CARR_Y0 = CARR_Y1 - CARR_T              # 34.0 block mounting face
CARR_POCKET_D = 3.5
CARR_POCKET_Y = CARR_Y1 - CARR_POCKET_D  # 38.5 pocket floor
CARR_BORE_D = 82.0                      # clears the O80 housing by 1 mm
CARR_PAD_R = 56.0                       # backing pad, r 41..56 around the bore
CARR_PAD_R_IN = 41.0

BLK_H, BLK_L, BLK_W = 13.0, 45.4, 27.0  # MGN12H, vendor data
BLK_PAT = 20.0                          # 4 x M3, 20 x 20, only 3.5 mm deep
BLK_THREAD = 3.5
BLK_Y1 = CARR_Y0                        # 34.0
BLK_Y0 = BLK_Y1 - BLK_H                 # 21.0
BLK_DZ = 40.0                           # block centres, +/- from the axis

RAIL_PLANE_Y = BLK_Y0                   # 21.0 = column outboard face
RAIL_W, RAIL_H = 12.0, 8.0
RAIL_X = -60.0                          # clears the O80 housing by 6.5 mm
RAIL_PITCH, RAIL_END = 25.0, 10.0
RAIL_LEN = 400.0                        # NOT 300: see rig_calc.py §5
RAIL_Z0 = -180.0
RAIL_Z1 = RAIL_Z0 + RAIL_LEN            # +220

EXT = 20.0                              # 2020 aluminium extrusion
COL_X0, COL_X1 = RAIL_X - EXT / 2.0, RAIL_X + EXT / 2.0   # -70 .. -50
COL_Y1 = RAIL_PLANE_Y                   # 21.0
COL_Y0 = COL_Y1 - EXT                   # 1.0

# ================================================================ rig, Z stack
Z_FLOOR = Z_WHEEL_AXIS - WHEEL_R        # -209.269 wheel contact plane at phi=0
FLOOR_T = 6.0
Z_BASE_TOP = Z_FLOOR - FLOOR_T          # -215.269   [DEFERRED - MODE B]
Z_BENCH = Z_BASE_TOP - EXT              # -235.269   [DEFERRED - MODE B]
COL_Z0 = Z_BASE_TOP                     # column stands on the base top face
COL_LEN = 480.0
COL_Z1 = COL_Z0 + COL_LEN               # +264.731

# ------------------------------------------------------------ MODE A Z datum
# Guide §2.5 requires the shoulder axis to sit at least 221.31 mm above the
# floor plate: the ride height at the -8 deg extension stop, which is where a
# free leg actually rests.  The shoulder axis IS this model's origin, so that
# requirement cannot be met by making a column longer -- it lands on the BENCH
# PLANE, which has to drop to 227.31 mm below the origin, and on the floor
# plate, which in Mode A sits on the bench instead of on the deleted 2020 base.
#
# Z_FLOOR (-209.269) is the phi = 0 contact plane and is 12.04 mm too HIGH for
# Mode A: with the floor there a free leg can never reach its -8 deg stop, the
# knee sits pre-compressed at phi = 0 carrying 17.2 N, and the extension stop
# that `RIG_Knee_Stop_Plate_L` exists to provide does nothing.  Both figures are
# kept -- Z_FLOOR is still right for the Mode B slide, where the carriage moves.
#
# Reproduced from the same frozen closed form _phi_for_contact() already uses,
# not re-derived: wz(phi) = -120 cos(50) - 120 cos(-50 - phi).
PHI_EXT_STOP = -8.0                     # the knee's extension stop
Z_WHEEL_AXIS_EXT = (-120.0 * math.cos(math.radians(50.0))
                    - 120.0 * math.cos(math.radians(-50.0 - PHI_EXT_STOP)))
Z_FLOOR_A = Z_WHEEL_AXIS_EXT - WHEEL_R  # -221.3119, i.e. the guide's 221.31 mm
Z_BENCH_A = Z_FLOOR_A - FLOOR_T         # -227.3119 = the stand's foot plane

# base frame footprint, 400 (X) x 300 (Y).  The inboard reach past the column
# is what stops the rig rotating outboard-down under the hanging leg.
BASE_X0, BASE_X1 = -230.0, 170.0
BASE_Y0, BASE_Y1 = -80.0, 220.0
BASE_CROSS_X = [-220.0, -140.0, -60.0, 50.0, 120.0, 160.0]   # centres

FLOOR_X0, FLOOR_X1 = -130.0, 130.0      # >= 250 mm fore-aft (brief)
FLOOR_Y0, FLOOR_Y1 = 54.0, 114.0        # tyre spans y 69..99

# ------------------------------------------------------------------- helpers
def box(comp, x0, x1, y0, y1, z0, z1, op='new', participants=None):
    """Axis-aligned rectangular prism from global corner to corner."""
    sk = sk_on_y(comp, y0)
    polyline(sk, [(x0, z0), (x1, z0), (x1, z1), (x0, z1)])
    return extrude(comp, sk.profiles.item(0), y1 - y0, op=op,
                   participants=participants)


def bodies_of(comp):
    return [comp.bRepBodies.item(i) for i in range(comp.bRepBodies.count)]


def sk_on_z(comp, z_mm):
    """Sketch on a plane parallel to XY at global Z = z_mm, normal +Z.

    beni_lib only provides sk_on_y, because every part in this project is a
    Y-extrusion.  The stand's bench-bolt holes are the one feature that has to
    run vertically.  Sketch (u, v) maps to global (X = u, Y = v).
    """
    pl = comp.constructionPlanes
    ipt = pl.createInput()
    ipt.setByOffset(comp.xYConstructionPlane,
                    adsk.core.ValueInput.createByReal(cm(z_mm)))
    p = pl.add(ipt)
    p.isLightBulbOn = False
    return comp.sketches.add(p)


def circle_xy(sk, x_mm, y_mm, dia_mm):
    """Circle on a sk_on_z() sketch, in global (X, Y)."""
    return sk.sketchCurves.sketchCircles.addByCenterRadius(
        adsk.core.Point3D.create(cm(x_mm), cm(y_mm), 0), cm(dia_mm / 2.0))


def _report(occ, label):
    c = occ.component
    vol = sum(b.volume for b in bodies_of(c)) * 1000.0
    print('  %-26s bodies %2d   vol %9.1f mm3   %s'
          % (label, c.bRepBodies.count, vol, fmt_bbox(occ, '')[28:]))
    return vol


# ========================================================== 1. the 2020 frame
def build_rig_base():
    """RIG_Base -- 2020 frame, 400 x 300, clamped to the bench."""
    drop_comp('RIG_Base')
    occ = new_comp('RIG_Base')
    c = occ.component
    z0, z1 = Z_BENCH, Z_BASE_TOP
    # two perimeter members along X, full 400.  Kept as separate bodies: these
    # are bought cut lengths, not one welded part.
    for y0 in (BASE_Y0, BASE_Y1 - EXT):
        box(c, BASE_X0, BASE_X1, y0, y0 + EXT, z0, z1)
    # cross members along Y, between the two perimeter members
    for xc in BASE_CROSS_X:
        box(c, xc - EXT / 2.0, xc + EXT / 2.0, BASE_Y0 + EXT, BASE_Y1 - EXT,
            z0, z1)
    print('RIG_Base')
    _report(occ, 'RIG_Base')
    print('     cut list: 2 x %.0f mm along X, %d x %.0f mm along Y'
          % (BASE_X1 - BASE_X0, len(BASE_CROSS_X), BASE_Y1 - BASE_Y0 - 2 * EXT))
    return occ


def build_rig_column():
    """RIG_Column -- 2020 vertical, 480 mm, with two diagonal braces."""
    drop_comp('RIG_Column')
    occ = new_comp('RIG_Column')
    c = occ.component
    box(c, COL_X0, COL_X1, COL_Y0, COL_Y1, COL_Z0, COL_Z1)
    print('RIG_Column')
    _report(occ, 'RIG_Column')
    print('     cut list: 1 x %.0f mm' % COL_LEN)
    return occ


def build_rig_braces():
    """RIG_Braces -- 2020 diagonals, fore and aft, in the column's own plane.

    Both bolt to the column's INBOARD face (y -19..1), not its own Y band: the
    fore brace crossed RIG_Index_Post by 11313 mm3 when it shared y 1..21.  Each
    foot lands on a real base cross member rather than in mid-air.
    """
    drop_comp('RIG_Braces')
    occ = new_comp('RIG_Braces')
    c = occ.component
    half = EXT / 2.0
    mitre = half / math.sqrt(2.0)          # so the end corner lands on Z=base
    out = []
    for sx, x_foot in ((-1.0, -220.0), (1.0, 120.0)):
        x_top = RAIL_X + sx * 25.0         # 15 mm clear of the column face
        run = abs(x_foot - x_top)
        bz = COL_Z0 + mitre
        a = (x_top, bz + run)              # top end, on the column side
        b = (x_foot, bz)                   # foot, on a base cross member
        d = (sx / math.sqrt(2.0), -1.0 / math.sqrt(2.0))
        n = (-d[1], d[0])
        pts = [(a[0] + half * n[0], a[1] + half * n[1]),
               (b[0] + half * n[0], b[1] + half * n[1]),
               (b[0] - half * n[0], b[1] - half * n[1]),
               (a[0] - half * n[0], a[1] - half * n[1])]
        sk = sk_on_y(c, COL_Y0 - EXT)
        polyline(sk, pts)
        extrude(c, biggest_profile(sk), EXT)
        out.append(run * math.sqrt(2.0))
    print('RIG_Braces')
    _report(occ, 'RIG_Braces')
    print('     cut list: %s (2020, 45 deg both ends)'
          % ', '.join('1 x %.0f mm' % v for v in out))
    return occ


def build_rig_floor(mode_a=True):
    """RIG_Floor_Plate -- flat hard plate the wheel rolls on.

    260 x 60 x 6, unchanged in size.  Its Z DATUM changes with the mode and the
    guide §3 table's "Unchanged" is wrong about that:

      MODE B  the plate sits on the 2020 base, top face at Z_FLOOR = -209.269,
              which is the phi = 0 contact plane.  Correct there, because the
              carriage moves and the shoulder height is a free variable.
      MODE A  the base is deleted and the shoulder axis is frozen at Z = 0, so
              the only way to meet guide §2.5's "shoulder axis >= 221.31 mm above
              the floor plate" is to put the plate on the BENCH: top face at
              Z_FLOOR_A = -221.3119, underside on the same bench plane the
              stand's foot stands on.  A free leg then rests on its -8 deg
              extension stop with the wheel just touching, at zero preload.
    """
    z0, z1 = (Z_BENCH_A, Z_FLOOR_A) if mode_a else (Z_BASE_TOP, Z_FLOOR)
    drop_comp('RIG_Floor_Plate')
    occ = new_comp('RIG_Floor_Plate')
    c = occ.component
    box(c, FLOOR_X0, FLOOR_X1, FLOOR_Y0, FLOOR_Y1, z0, z1)
    print('RIG_Floor_Plate  (%s)' % ('MODE A, on the bench' if mode_a
                                     else 'MODE B, on the 2020 base'))
    _report(occ, 'RIG_Floor_Plate')
    print('     %.0f x %.0f x %.0f mm, top face at Z = %.4f'
          % (FLOOR_X1 - FLOOR_X0, FLOOR_Y1 - FLOOR_Y0, FLOOR_T, z1))
    print('     shoulder axis sits %.2f mm above it (guide §2.5 needs >= 221.31)'
          % -z1)
    return occ


# ============================================================== 2. rail/blocks
def build_rig_rail():
    """RIG_Rail -- MGN12 profile rail, 400 mm, on the column's outboard face."""
    drop_comp('RIG_Rail')
    occ = new_comp('RIG_Rail')
    c = occ.component
    box(c, RAIL_X - RAIL_W / 2.0, RAIL_X + RAIL_W / 2.0,
        RAIL_PLANE_Y, RAIL_PLANE_Y + RAIL_H, RAIL_Z0, RAIL_Z1)
    n = int((RAIL_LEN - 2 * RAIL_END) / RAIL_PITCH) + 1
    sk = sk_on_y(c, RAIL_PLANE_Y)
    for i in range(n):
        circle(sk, RAIL_X, RAIL_Z0 + RAIL_END + i * RAIL_PITCH, 3.4)
    extrude(c, profiles(sk), RAIL_H, op='cut', participants=bodies_of(c))
    print('RIG_Rail')
    _report(occ, 'RIG_Rail')
    print('     MGN12 %.0f mm, %d x M3 at %.0f mm pitch, %.0f mm end margin'
          % (RAIL_LEN, n, RAIL_PITCH, RAIL_END))
    print('     travel: %.1f mm between block-pair limits (2 blocks span %.1f)'
          % (RAIL_LEN - (BLK_L + 2 * BLK_DZ), BLK_L + 2 * BLK_DZ))
    return occ


def build_rig_blocks():
    """HW_MGN12H -- two carriage blocks, placed at +/- BLK_DZ."""
    drop_comp('HW_MGN12H')
    occ = new_comp('HW_MGN12H')
    c = occ.component
    # geometry is built at the LOWER station so the identity occurrence is
    # already in the right place; the second block is a placed copy.
    zc = -BLK_DZ
    box(c, RAIL_X - BLK_W / 2.0, RAIL_X + BLK_W / 2.0, BLK_Y0, BLK_Y1,
        zc - BLK_L / 2.0, zc + BLK_L / 2.0)
    # the rail groove, so the block reads as a block and not a solid slug
    box(c, RAIL_X - (RAIL_W + 1.0) / 2.0, RAIL_X + (RAIL_W + 1.0) / 2.0,
        BLK_Y0, BLK_Y0 + RAIL_H + 0.5, zc - BLK_L / 2.0, zc + BLK_L / 2.0,
        op='cut', participants=bodies_of(c))
    # 4 x M3 x 3.5 deep on the 20 x 20 pattern, tapped from the top face
    sk = sk_on_y(c, BLK_Y1)
    for dx in (-BLK_PAT / 2.0, BLK_PAT / 2.0):
        for dz in (-BLK_PAT / 2.0, BLK_PAT / 2.0):
            circle(sk, RAIL_X + dx, zc + dz, 2.5)
    extrude(c, profiles(sk), -BLK_THREAD, op='cut', participants=bodies_of(c))
    place(occ, 0.0, 2 * BLK_DZ, 0.0)
    print('HW_MGN12H  x2  at Z = %+.0f and %+.0f' % (-BLK_DZ, BLK_DZ))
    _report(occ, 'HW_MGN12H lower')
    return occ


# =========================================================== 3. the carriage
CARR_DISC_R = 58.0
CARR_SPINE_X0, CARR_SPINE_X1 = -78.0, -42.0
CARR_SPINE_Z0, CARR_SPINE_Z1 = -85.0, 85.0
INSERT_M3_D, INSERT_M3_L = 5.0, 5.0     # M3 brass heat-set, 5 mm long
INSERT_M4_D, INSERT_M4_L = 5.6, 5.0
BLK_CB_D, BLK_CB_DEEP = 6.4, 3.2        # so M3 x 8 engages 3.2 of the 3.5 mm
PIN_D = 8.05
PIN_X, PIN_Z = 66.0, 10.0               # mode pin / drop release, one hole
#   PIN_X is 66 not 56: at 56 the pin's handle sat 809 mm3 inside the post
BALLAST_R_IN, BALLAST_R_OUT = 42.0, 64.0
BALLAST_A0, BALLAST_A1 = 55.0, 125.0
BALLAST_STUD_R = 53.0
BALLAST_STUD_A = [70.0, 110.0, 250.0, 290.0]
BALLAST_T = 3.0


def build_rig_carriage():
    """RIG_Carriage -- the PA-CF plate that is the whole moving assembly.

    Outboard face (y=42) lies flat against Chassis_Shoulder_Plate_L's inboard
    face and bolts to its five existing frame-bolt holes through M3 heat-set
    inserts.  Inboard face (y=34) carries both MGN12H blocks.  Nothing here
    puts a new hole in a reused part.
    """
    drop_comp('RIG_Carriage')
    occ = new_comp('RIG_Carriage')
    c = occ.component

    # --- outline: disc + rail spine + two reach arms, all overlapping
    sk = sk_on_y(c, CARR_Y0)
    circle(sk, 0.0, 0.0, 2 * CARR_DISC_R)
    polyline(sk, [(CARR_SPINE_X0, CARR_SPINE_Z0), (CARR_SPINE_X1, CARR_SPINE_Z0),
                  (CARR_SPINE_X1, CARR_SPINE_Z1), (CARR_SPINE_X0, CARR_SPINE_Z1)])
    slot(sk, 30.0, 48.0, 30.0, 62.0, 26.0)        # reach to the upper panel bolts
    slot(sk, 40.0, PIN_Z, 62.0, PIN_Z, 28.0)      # reach to the mode-pin station
    extrude(c, profiles(sk), CARR_T)
    if c.bRepBodies.count > 1:
        print('   WARNING: outline made %d bodies, expected 1'
              % c.bRepBodies.count)

    # --- central bore, clears the O80 motor housing by 1 mm
    cyl_y(c, None, 0.0, 0.0, CARR_BORE_D, CARR_Y0 - 1.0, CARR_Y1 + 1.0,
          op='cut', participants=bodies_of(c))

    # --- five M3 insert bores, from the OUTBOARD face
    sk = sk_on_y(c, CARR_Y1)
    for x, z in PANEL_FRAME_BOLTS:
        circle(sk, x, z, INSERT_M3_D)
    extrude(c, profiles(sk), -INSERT_M3_L, op='cut', participants=bodies_of(c))

    # --- eight block screws: O3.4 through, counterbored from the outboard face
    holes = []
    for zc in (-BLK_DZ, BLK_DZ):
        for dx in (-BLK_PAT / 2.0, BLK_PAT / 2.0):
            for dz in (-BLK_PAT / 2.0, BLK_PAT / 2.0):
                holes.append((RAIL_X + dx, zc + dz))
    sk = sk_on_y(c, CARR_Y1)
    for x, z in holes:
        circle(sk, x, z, 3.4)
    extrude(c, profiles(sk), -CARR_T, op='cut', participants=bodies_of(c))
    sk = sk_on_y(c, CARR_Y1)
    for x, z in holes:
        circle(sk, x, z, BLK_CB_D)
    extrude(c, profiles(sk), -BLK_CB_DEEP, op='cut', participants=bodies_of(c))

    # --- the one O8.05 reamed hole that serves BOTH modes
    cyl_y(c, None, PIN_X, PIN_Z, PIN_D, CARR_Y0 - 1.0, CARR_Y1 + 1.0,
          op='cut', participants=bodies_of(c))

    # --- ballast studs, M4 inserts from the INBOARD face
    sk = sk_on_y(c, CARR_Y0)
    for a in BALLAST_STUD_A:
        r = math.radians(a)
        circle(sk, BALLAST_STUD_R * math.cos(r), BALLAST_STUD_R * math.sin(r),
               INSERT_M4_D)
    extrude(c, profiles(sk), INSERT_M4_L, op='cut', participants=bodies_of(c))

    print('RIG_Carriage')
    _report(occ, 'RIG_Carriage')
    return occ


# ================================================ 4. mode pin / drop release
INDEX_POST_XC = 50.0
INDEX_BAR_X0, INDEX_BAR_X1 = 42.0, 78.0
INDEX_BAR_Y0, INDEX_BAR_Y1 = BLK_Y0, CARR_Y0 - 0.5      # 21 .. 33.5
INDEX_BAR_Z0, INDEX_BAR_Z1 = -110.0, 170.0
INDEX_PITCH = 10.0
INDEX_Z_FIRST = PIN_Z - 60.0            # -50, 60 mm below the modelled position
INDEX_N = 17                            # ... up to +110, i.e. a 100 mm drop
# carriage travel limits, set by the two PU bumpers.  Chosen from the stroke
# budget in rig_calc.py §5: +110 covers the top release station, -85 covers the
# 51.5 mm peak compression of a 100 mm drop with margin.
TRAVEL_UP, TRAVEL_DOWN = 125.0, -85.0
ARM_Z0, ARM_Z1 = PIN_Z - 14.0, PIN_Z + 14.0      # the pin arm's obround edges
BUMPER_D = 14.0
BUMPER_Z_LO = TRAVEL_DOWN + ARM_Z0 - BUMPER_D / 2.0
BUMPER_Z_HI = TRAVEL_UP + ARM_Z1 + BUMPER_D / 2.0


def build_rig_index_post():
    """RIG_Index_Post -- 2020 upright carrying the station bar.

    It sits FORWARD of the motor, not beside the rail: an MGN12H is 27 mm wide
    against a 20 mm column, so the blocks overhang the column face on both
    sides and nothing can share that face at the block's Y band.
    """
    drop_comp('RIG_Index_Post')
    occ = new_comp('RIG_Index_Post')
    c = occ.component
    box(c, INDEX_POST_XC - EXT / 2.0, INDEX_POST_XC + EXT / 2.0,
        COL_Y0, COL_Y1, Z_BASE_TOP, INDEX_BAR_Z1 + 20.0)
    print('RIG_Index_Post')
    _report(occ, 'RIG_Index_Post')
    print('     cut list: 1 x %.0f mm' % (INDEX_BAR_Z1 + 20.0 - Z_BASE_TOP))
    return occ


def build_rig_index_bar():
    """RIG_Index_Bar -- one 10 mm-pitch station bar serving both modes.

    Mode A and the drop release share a single O8.05 hole in the carriage and a
    single pin: the pin locks the carriage when it is level with a station and
    holds it up when it is not.  Station -> drop height is a table, because the
    equilibrium point depends on the spring, which step 6 measures.
    """
    drop_comp('RIG_Index_Bar')
    occ = new_comp('RIG_Index_Bar')
    c = occ.component
    box(c, INDEX_BAR_X0, INDEX_BAR_X1, INDEX_BAR_Y0, INDEX_BAR_Y1,
        INDEX_BAR_Z0, INDEX_BAR_Z1)
    sk = sk_on_y(c, INDEX_BAR_Y0)
    for i in range(INDEX_N):
        circle(sk, PIN_X, INDEX_Z_FIRST + i * INDEX_PITCH, PIN_D)
    extrude(c, profiles(sk), INDEX_BAR_Y1 - INDEX_BAR_Y0, op='cut',
            participants=bodies_of(c))
    # M5 clearance to bolt the bar to the post's T-slot
    sk = sk_on_y(c, INDEX_BAR_Y0)
    for z in (INDEX_BAR_Z0 + 12.0, 0.0, INDEX_BAR_Z1 - 12.0):
        circle(sk, INDEX_POST_XC, z, 5.5)
    extrude(c, profiles(sk), INDEX_BAR_Y1 - INDEX_BAR_Y0, op='cut',
            participants=bodies_of(c))
    print('RIG_Index_Bar')
    _report(occ, 'RIG_Index_Bar')
    print('     %d stations at %.0f mm pitch, Z %+.0f .. %+.0f'
          % (INDEX_N, INDEX_PITCH, INDEX_Z_FIRST,
             INDEX_Z_FIRST + (INDEX_N - 1) * INDEX_PITCH))
    return occ


def build_rig_mode_pin():
    """RIG_Mode_Pin -- O8 quick-release pin, loaded in shear."""
    drop_comp('RIG_Mode_Pin')
    occ = new_comp('RIG_Mode_Pin')
    c = occ.component
    # Inserted from OUTBOARD, handle at y 42..50.  Inserting from inboard put
    # the handle inside RIG_Index_Post, and reaching behind the column to pull a
    # release pin during a drop test is the wrong ergonomics anyway.
    cyl_y(c, None, PIN_X, PIN_Z, 8.0, INDEX_BAR_Y0, CARR_Y1)
    cyl_y(c, None, PIN_X, PIN_Z, 16.0, CARR_Y1, CARR_Y1 + 8.0)
    print('RIG_Mode_Pin')
    _report(occ, 'RIG_Mode_Pin')
    print('     grip %.1f mm: carriage %.1f + gap %.1f + bar %.1f, handle outboard'
          % (CARR_Y1 - INDEX_BAR_Y0, CARR_T, CARR_Y0 - INDEX_BAR_Y1,
             INDEX_BAR_Y1 - INDEX_BAR_Y0))
    return occ


def build_rig_bumpers():
    """RIG_Hard_Stops -- PU bumpers at both ends of the carriage's travel.

    Bolted to the index bar so the carriage's own pin arm strikes them; the
    MGN12H blocks never reach the end of the rail.
    """
    drop_comp('RIG_Hard_Stops')
    occ = new_comp('RIG_Hard_Stops')
    c = occ.component
    for z in (BUMPER_Z_LO, BUMPER_Z_HI):
        cyl_y(c, None, PIN_X, z, BUMPER_D, INDEX_BAR_Y1, CARR_Y1)
    print('RIG_Hard_Stops')
    _report(occ, 'RIG_Hard_Stops')
    print('     limits the shoulder axis to %+.0f .. %+.0f mm about the '
          'modelled position' % (TRAVEL_DOWN, TRAVEL_UP))
    return occ


# ================================================================ 5. ballast
def build_rig_ballast():
    """RIG_Ballast_Disc -- 3 mm laser-cut steel sector, stacked on M4 studs.

    Goes on the SAME laser order as Knee_Stop_Arc_L, so it costs shipping only.
    Sits inboard of the carriage, i.e. between the leg and the rail, so adding
    ballast reduces the overhang moment instead of increasing it.
    """
    drop_comp('RIG_Ballast_Disc')
    occ = new_comp('RIG_Ballast_Disc')
    c = occ.component
    sk = sk_on_y(c, CARR_Y0 - BALLAST_T)
    arc_sector(sk, 0.0, 0.0, BALLAST_R_IN, BALLAST_R_OUT,
               BALLAST_A0, BALLAST_A1)
    extrude(c, biggest_profile(sk), BALLAST_T)
    sk = sk_on_y(c, CARR_Y0 - BALLAST_T)
    for a in BALLAST_STUD_A[:2]:
        r = math.radians(a)
        circle(sk, BALLAST_STUD_R * math.cos(r), BALLAST_STUD_R * math.sin(r),
               4.5)
    extrude(c, profiles(sk), BALLAST_T, op='cut', participants=bodies_of(c))
    # one fitted pair: upper sector plus the same part rotated 180 deg
    m = mat((-1, 0, 0), (0, 1, 0), (0, 0, -1), (0.0, 0.0, 0.0))
    root().occurrences.addExistingComponent(c, m)
    print('RIG_Ballast_Disc  (2 fitted, order 8)')
    _report(occ, 'RIG_Ballast_Disc')
    b = c.bRepBodies.item(0)
    print('     %.2f cm3 -> %.1f g in 3 mm steel, per sector'
          % (b.volume, b.volume * 7.85))
    return occ


# ============================================================ 6. torque arm
HUB_LINK_PCD = 44.0                     # 6 x M4 in the hub flange
HUB_LINK_A0 = 0.4
HUB_FACE_Y = 59.5                       # hub flange outboard face = leg inboard
ARM_T = 12.0
ARM_R = 200.0
ARM_ROOT_D = 62.0
ARM_W_ROOT, ARM_W_TIP = 40.0, 25.0
LINK_INBOARD_Y = 58.7                   # proximal arm A inboard face


def build_rig_torque_arm():
    """RIG_Torque_Arm -- 200 mm lever, bolted to the hub's 6 x M4 O44 PCD.

    It REPLACES the proximal link: step 2 runs with the leg off, which is also
    the only way the arm has a free arc.  At 200 mm a 5 kg kitchen scale reads
    to 9.81 N.m, so it covers the 5.9 N.m the jump needs but not the 11 N.m
    nameplate stall -- see rig_calc.py §7.
    """
    drop_comp('RIG_Torque_Arm')
    occ = new_comp('RIG_Torque_Arm')
    c = occ.component
    sk = sk_on_y(c, HUB_FACE_Y)
    circle(sk, 0.0, 0.0, ARM_ROOT_D)
    polyline(sk, [(-ARM_ROOT_D / 2.0 + 3.0, ARM_W_ROOT / 2.0),
                  (-ARM_R, ARM_W_TIP / 2.0),
                  (-ARM_R, -ARM_W_TIP / 2.0),
                  (-ARM_ROOT_D / 2.0 + 3.0, -ARM_W_ROOT / 2.0)])
    circle(sk, -ARM_R, 0.0, ARM_W_TIP)          # rounded nose = contact line
    extrude(c, profiles(sk), ARM_T)
    if c.bRepBodies.count > 1:
        print('   WARNING: %d bodies' % c.bRepBodies.count)
    sk = sk_on_y(c, HUB_FACE_Y)
    circles_polar(sk, 0.0, 0.0, HUB_LINK_PCD, 4.5, 6, HUB_LINK_A0)
    circle(sk, 0.0, 0.0, 34.0)                  # hub-screw driver access
    extrude(c, profiles(sk), ARM_T, op='cut', participants=bodies_of(c))
    print('RIG_Torque_Arm')
    _report(occ, 'RIG_Torque_Arm')
    rmax = math.hypot(ARM_R, ARM_W_TIP / 2.0)
    print('     max radius %.1f mm vs %.1f mm to the floor plate -> %.1f mm clear'
          % (rmax, -Z_FLOOR, -Z_FLOOR - rmax))
    return occ


SCALE_POST_XC = -200.0
SCALE_SHELF_T = 6.0
SCALE_H = 30.0                          # kitchen-scale platform height


def build_rig_scale_pedestal(z_bench=None):
    """RIG_Scale_Pedestal -- brings the scale platform up to the arm's nose.

    The arm has to be horizontal for the moment arm to be exactly 200 mm, and
    the shoulder axis is 209 mm above the floor, so the scale cannot just sit
    on the bench.

    MODE A: it stood on RIG_Base's cross members at Z_BASE_TOP, and there is no
    base any more, so the uprights are re-datumed to the same bench plane the
    stand's foot uses.  The shelf height is unchanged -- it is set by the arm's
    nose, not by the base.
    """
    z_bench = Z_BENCH_A if z_bench is None else z_bench
    drop_comp('RIG_Scale_Pedestal')
    occ = new_comp('RIG_Scale_Pedestal')
    c = occ.component
    nose_z = -ARM_W_TIP / 2.0
    shelf_top = nose_z - SCALE_H
    # two uprights, each standing on the bench beside the stand's footprint
    for xc in (-220.0, -140.0):
        box(c, xc - EXT / 2.0, xc + EXT / 2.0,
            HUB_FACE_Y - EXT / 2.0, HUB_FACE_Y + EXT / 2.0,
            z_bench, shelf_top - SCALE_SHELF_T)
    box(c, -235.0, -125.0, HUB_FACE_Y - 45.0, HUB_FACE_Y + 45.0,
        shelf_top - SCALE_SHELF_T, shelf_top)
    print('RIG_Scale_Pedestal')
    _report(occ, 'RIG_Scale_Pedestal')
    print('     shelf top Z %.1f, + %.0f mm scale -> platform at Z %.1f '
          '(arm nose %.1f)' % (shelf_top, SCALE_H, shelf_top + SCALE_H, nose_z))
    print('     cut list: 2 x %.0f mm 2020' % (shelf_top - SCALE_SHELF_T - z_bench))
    return occ


# =========================================================== 7. cable posts
def build_rig_cable_post_a():
    """RIG_Cable_Posts -- two posts, one per service loop.

    A: clamped under two of the motor's eight M3 housing screws, anchoring the
       hub's rotating loop.  Height is capped at y = 57 so the proximal link,
       whose inboard face is at 58.7, can sweep over it.
    B: on the column T-slot above the carriage's travel, carrying the loop that
       has to tolerate the 210 mm of Mode B carriage stroke.
    """
    drop_comp('RIG_Cable_Post_A')
    occ = new_comp('RIG_Cable_Post_A')
    c = occ.component
    # Post A rides two of the motor's own 8 x M3 O74 positions, NOT the four
    # freed O88 cover holes: those need a fastener on the panel's inboard face,
    # and RIG_Carriage is now bolted flat against it.  Two of the eight housing
    # screws become M3 x 16 and clamp post A, panel and motor together.
    r = 37.0
    t = 8.0
    a1, a2 = 67.6, 112.6
    # An annular sector r 35..50, NOT a slot between the two screw centres: a
    # 14 mm-wide slot dipped to r 27, which hit both the panel's cable-cavity
    # lip (r 32..33.5) and the O56 output hub.
    p1 = (r * math.cos(math.radians(a1)), r * math.sin(math.radians(a1)))
    p2 = (r * math.cos(math.radians(a2)), r * math.sin(math.radians(a2)))
    sk = sk_on_y(c, PANEL_Y1)
    arc_sector(sk, 0.0, 0.0, 35.0, 50.0, a1 - 3.0, a2 + 3.0)
    extrude(c, biggest_profile(sk), t)
    sk = sk_on_y(c, PANEL_Y1)
    circle(sk, p1[0], p1[1], 3.4)
    circle(sk, p2[0], p2[1], 3.4)
    circle(sk, 0.0, 44.0, 8.0)                 # the cable eye
    extrude(c, profiles(sk), t, op='cut', participants=bodies_of(c))
    print('RIG_Cable_Post_A')
    _report(occ, 'RIG_Cable_Post_A')
    print('     post A spans y %.1f..%.1f, r 35..50 (lip r33.5, link at %.1f)'
          % (PANEL_Y1, PANEL_Y1 + 8.0, LINK_INBOARD_Y))
    print('     its two M3 x 16 replace two of the eight M3 x 10 housing screws')
    return occ


def build_rig_cable_anchor_mode_a():
    """Rear-face strain-relief anchor for the Mode A shoulder harness.

    Mode A has no 2020 column, so ``RIG_Cable_Post_B`` has nowhere to mount.
    This small annular sector instead uses the two upper rear M3 housing holes
    on the GIM6010-8's verified O74 pattern.  It sits on the STEP's y=16.0 mm
    rear mounting land, outside the O57 driver cover, and grows inboard so it
    cannot enter the rotating output/hub stack.

    This builder intentionally refuses to delete/rebuild an existing
    occurrence.  Deleting occurrences in this externally-referenced assembly
    can reset reference transforms; the first creation is safe and subsequent
    edits must use the documented capture/restore guard explicitly.
    """
    name = 'RIG_Cable_Anchor_ModeA'
    if find_occ(name) is not None:
        raise RuntimeError('%s already exists; do not delete it without the '
                           'rig transform guard' % name)
    occ = new_comp(name)
    c = occ.component

    seat_y = 12.0                       # four mm thick; rear land is y=16.0
    thickness = 4.0
    bolt_r = beni_lib.SH_BOLT_PCD / 2.0
    a1, a2 = 67.6, 112.6               # upper adjacent O74 housing holes
    p1 = (bolt_r * math.cos(math.radians(a1)),
          bolt_r * math.sin(math.radians(a1)))
    p2 = (bolt_r * math.cos(math.radians(a2)),
          bolt_r * math.sin(math.radians(a2)))

    # O59 inner clearance leaves 1.0 mm radial air to the measured O57 driver
    # cover.  R41 outer radius leaves >= 2.3 mm around each O3.4 clearance.
    sk = sk_on_y(c, seat_y)
    arc_sector(sk, 0.0, 0.0, 29.5, 41.0, 60.0, 120.0)
    body = extrude(c, biggest_profile(sk), thickness).bodies.item(0)
    body.name = name

    sk = sk_on_y(c, seat_y)
    circle(sk, p1[0], p1[1], 3.4)
    circle(sk, p2[0], p2[1], 3.4)
    circle(sk, 0.0, 35.0, 8.0)         # zip-tie / braided-sleeve eye
    extrude(c, profiles(sk), thickness, op='cut', participants=bodies_of(c))
    c.attributes.add('BeniRig', 'interface',
                     'GIM6010 rear face y=16; 2xM3 PCD74 at 67.6/112.6 deg')
    c.attributes.add('BeniRig', 'firstArticleMaterial', 'ABS')
    print(name)
    _report(occ, name)
    print('     y %.1f..%.1f, r 29.5..41.0; O57 driver cover has 1 mm air'
          % (seat_y, seat_y + thickness))
    print('     2 x M3 x 8 with washers; O8 cable eye at X0 Z+35')
    return occ


# ======================================================= 8. honest clash check
def occ_name(entity):
    """Resolve an interference-result entity to a readable name.

    `beni_lib.interference` reports `entity.name`, which for a BRepBody is its
    body name -- "Body1" for anything built without renaming.  Every rig clash
    therefore came back as "Body1 <-> Body2" and a filter on 'RIG_' matched
    nothing, so the first four builds reported zero interference when there were
    really 49 pairs.  Always resolve through assemblyContext.
    """
    try:
        if entity.objectType == 'adsk::fusion::Occurrence':
            return entity.name
    except Exception:
        pass
    ac = getattr(entity, 'assemblyContext', None)
    if ac is not None:
        return ac.name
    # External references (the two motor STEPs) have no assemblyContext, so a
    # bare entity.name reports the STEP's internal "Body1".  Walk to the owning
    # component instead, or the motor is indistinguishable from a rig part.
    pc = getattr(entity, 'parentComponent', None)
    if pc is not None:
        return pc.name
    return getattr(entity, 'name', '?')


def name_bodies():
    """Give EVERY body its component's name, so clashes are legible.

    Not just the rig parts: half the pre-existing pairs also reported as
    "Body1", which is why the documented screw-in-tap-drill artifacts were
    impossible to tell apart from real clashes.
    """
    n = 0
    r = root()
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        nm = base_name(o.component.name)
        if nm.startswith('REF_'):
            continue
        for k, b in enumerate(bodies_of(o.component)):
            want = nm if o.component.bRepBodies.count == 1 else '%s_%d' % (nm, k + 1)
            if b.name != want:
                b.name = want
                n += 1
    return n


def clashes(min_vol_mm3=0.5, skip=(), verbose=True):
    """Whole-assembly interference with names that actually resolve."""
    d = beni_lib.design()
    r = root()
    col = adsk.core.ObjectCollection.create()
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        if any(s in o.component.name for s in skip):
            continue
        col.add(o)
    ipt = d.createInterferenceInput(col)
    ipt.areCoincidentFacesIncluded = False
    res = d.analyzeInterference(ipt)
    out = []
    if res:
        for i in range(res.count):
            it = res.item(i)
            v = it.interferenceBody.volume * 1000.0
            if v < min_vol_mm3:
                continue
            out.append((occ_name(it.entityOne), occ_name(it.entityTwo), v))
    out.sort(key=lambda t: -t[2])
    if verbose:
        print('interference: %d pair(s) over %.2f mm3' % (len(out), min_vol_mm3))
        for a, b, v in out:
            print('   %-34s %-34s %10.2f mm3' % (a, b, v))
    return out


def build_rig_cable_post_b():
    """RIG_Cable_Post_B -- fixed to the column above the carriage's travel.

    Carries the loop that has to tolerate the whole Mode B stroke, so it is
    deliberately NOT on the slide.
    """
    drop_comp('RIG_Cable_Post_B')
    occ = new_comp('RIG_Cable_Post_B')
    c = occ.component
    zb = TRAVEL_UP + CARR_DISC_R + 22.0
    box(c, RAIL_X + EXT / 2.0, RAIL_X + EXT / 2.0 + 45.0, COL_Y0 + 2.0,
        COL_Y0 + 17.0, zb, zb + 15.0)
    sk = sk_on_y(c, COL_Y0 + 2.0)
    circle(sk, RAIL_X + EXT / 2.0 + 34.0, zb + 7.5, 8.0)
    extrude(c, profiles(sk), 15.0, op='cut', participants=bodies_of(c))
    print('RIG_Cable_Post_B')
    _report(occ, 'RIG_Cable_Post_B')
    print('     eye at Z %+.1f, %.1f mm above the top of the carriage disc'
          % (zb + 7.5, zb - (TRAVEL_UP + CARR_DISC_R)))
    return occ


# ======================================== 9. posing, Mode B travel, §4.4 checks
# Everything NOT in FIXED rides the slide: carriage, blocks, ballast, mode pin,
# panel, motor, hub, the whole leg and every fastener on it.
FIXED = ('RIG_Stand',
         'RIG_Base', 'RIG_Column', 'RIG_Braces', 'RIG_Rail', 'RIG_Floor_Plate',
         'RIG_Index_Post', 'RIG_Index_Bar', 'RIG_Hard_Stops',
         'RIG_Scale_Pedestal', 'RIG_Cable_Post_B', 'RIG_Mode_Pin')

# Fitted only while the carriage is parked on a station.  The pin is pulled to
# start a drop, so it must not be in the model during a travel sweep.
STATION_FITTED = ('RIG_Mode_Pin',)

# Clashes that are known modelling artifacts, not defects.  Each is either a
# screw shank inside its own modelled tap drill, the documented M4-stud pair,
# the motor's own output pins (design record §11), or the torque arm, which
# REPLACES the proximal link and is only fitted with the leg off.
ARTIFACT_PAIRS = (
    ('Knee_Axle_L', 'Knee_Magnet_Carrier_L'),
    # the motor's own three O4 x 3.5 output pins, which rotate WITH the hub in
    # reality but are one solid body in the STEP (design record §11)
    ('Shoulder_Output_Hub_L', 'REF_GIM6010-8'),
    ('Shoulder_Output_Hub_L', '6010-8'),
    # the knee stop dowel crushing its PU bumpers.  These are the DESIGNED crush
    # volumes and they reproduce design record §10.1 exactly: 1.4 mm3 on the
    # extension pad at -8 deg, 8.6 at +25, 12.7 at the +27 metal stop.
    ('HW_DowelPin_D6x9', 'Knee_Bumper_Ext_L'),
    ('HW_DowelPin_D6x9', 'Knee_Bumper_Flex_L'),
    # the cartridge stop's TPU tube crushing on the LOWER spring seat.  Same
    # class of artifact, for the §8 compression column: the tube is sized to
    # first touch at +20 deg and to be 18.5 % crushed when the washer stack goes
    # solid at +27.  CAD reproduces rig_lib.stop_stack_sizes() to the digit --
    # 0.00 mm3 at +20, 122.99 at +25, 173.46 at +27, against a designed
    # 3.7593 mm of crush on a 46.14 mm2 annulus = 173.46 mm3.  An independent
    # confirmation that the stop engages where §8 put it.
    ('Cart_Lower_Eye_L', 'RIG_Knee_Bumper_Tube_L'),
)

# Fixtures that are only ever fitted with the leg REMOVED, for step 2 of the
# test order.  The torque arm bolts to the hub in place of the proximal link,
# and the scale pedestal has to stand at X = -200 to be under the arm's nose --
# which is inside the leg's own 209 mm swept radius, so the two genuinely
# cannot coexist.  Both come off before the leg goes on.
STEP2_FIXTURES = ('RIG_Torque_Arm', 'RIG_Scale_Pedestal')


def _is_artifact(a, b):
    na, nb = base_name(a.split(':')[0]), base_name(b.split(':')[0])
    for pa, pb in ARTIFACT_PAIRS:
        if {na, nb} == {pa, pb}:
            return True
        if pa in (na, nb) and (pb in na or pb in nb):
            return True
    # a screw inside the thread it is screwed into
    if na.startswith('HW_SHCS_') or nb.startswith('HW_SHCS_'):
        return True
    return False


def real_clashes(min_vol_mm3=0.5, verbose=True):
    """clashes() minus the documented artifact classes."""
    out = [(a, b, v) for a, b, v in clashes(min_vol_mm3, verbose=False)
           if not _is_artifact(a, b)]
    if verbose:
        if out:
            print('   REAL CLASHES: %d' % len(out))
            for a, b, v in out:
                print('      %-32s %-32s %9.2f mm3' % (a, b, v))
        else:
            print('   no real clashes')
    return out


def rig_set_pose(theta, phi):
    """beni_lib.set_pose() without resurrecting the deleted right-hand spring.

    beni_lib.rebuild_spring() deliberately builds BOTH springs, which on a
    single-leg model re-creates a right-hand part that was deleted.

    ⚠ AND it has to guard the cartridge stop parts.  beni_lib._spring_body()
    starts with drop_comp('Knee_Spring_L'), and that delete resets
    HW_WasherStack_M5 and RIG_Knee_Bumper_Tube_L to identity -- see xf_capture().
    Identity drops both into the shoulder motor at the origin, so EVERY pose used
    to invent 430 mm3 of clashes that have nothing to do with the design, in the
    one place a real knee-stop clash would show up.  The REF bounding-box guard
    passes throughout, which is what made it invisible.
    """
    beni_lib.capture_nominal()
    saved = xf_capture()
    beni_lib._spring_body('Knee_Spring_L', phi, beni_lib.LEG_Y_MID)
    xf_restore(saved)
    replace_cart_stops()            # deterministic, idempotent, phi-independent
    snap = beni_lib.nominal_snapshot()
    beni_lib.pose(snap, theta, phi)
    return snap


def slide_to(dz, theta=0.0, phi=0.0):
    """Pose the leg, then translate the whole sprung assembly by dz in Z."""
    rig_set_pose(theta, phi)
    nom = beni_lib.capture_nominal()
    r = root()
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        if base_name(o.component.name) in FIXED:
            continue
        m = o.transform2
        a = list(m.asArray())
        a[11] += cm(dz)
        mm = adsk.core.Matrix3D.create()
        mm.setWithArray(a)
        o.transform2 = mm
    return dz


# ============================================== 10. materials and mass budget
# 2020 extrusion is a hollow T-slot profile: ~0.45 kg/m against 1.124 kg/m for
# a solid 20 x 20 bar, so a solid model overstates it 2.5x.  These parts are not
# on the slide, but the frame mass should still not be a lie.
EXT2020_DENSITY = 2.81 * 0.45 / 1.124

RIG_PART_CLASS = {
    'RIG_Stand': 'PACF',
    'RIG_Carriage': 'PACF',
    'RIG_Index_Bar': 'PACF',
    'RIG_Torque_Arm': 'PACF',
    'RIG_Cable_Post_A': 'PACF',
    'RIG_Cable_Post_B': 'PACF',
    'RIG_Cable_Anchor_ModeA': 'ABS',
    'RIG_Floor_Plate': 'PACF',
    'RIG_Ballast_Disc': 'STEEL',
    'RIG_Mode_Pin': 'STEEL',
    'RIG_Hard_Stops': 'PU',
    'RIG_Base': 'EXT2020',
    'RIG_Column': 'EXT2020',
    'RIG_Braces': 'EXT2020',
    'RIG_Index_Post': 'EXT2020',
    'RIG_Scale_Pedestal': 'EXT2020',
    'HW_MGN12H': 'STEEL',
}


def register_materials():
    """Teach beni_lib's material/mass machinery about the rig parts."""
    beni_lib.MATERIAL_SPEC['EXT2020'] = ('Aluminum', EXT2020_DENSITY, None,
                                        '2020 T-slot extrusion, hollow')
    beni_lib.PART_CLASS.update(RIG_PART_CLASS)
    beni_lib.MASS_OVERRIDE_G['HW_MGN12H'] = 54.0     # vendor figure
    return len(RIG_PART_CLASS)


# ⚠ beni_lib.classify() knows the ORIGINAL leg part names.  §2.3 (the no-machining
# knee substitute) and §13 (the cartridge hard stop) introduced six replacement
# parts under new names, and classify() falls through to 'STATIC' for anything it
# does not recognise -- so all six stayed frozen at their theta = 0 / phi = 0
# placement while the leg swept around them.  The leg then swept THROUGH them:
# 5 of the 17 check-2 angles and 5 of the 6 check-3 knee angles reported clashes
# up to 634 mm3 between the wheel and knee-area parts that cannot physically
# touch.  Nothing re-ran check 2 after those parts were added, so this had never
# shown up.  Each replacement inherits the class of the part it replaced:
RIG_POSE_CLASS = {
    # Knee_Stop_Arc_L was PROX -- bolted to the proximal arm's outboard face
    'PROX': ('RIG_Knee_Stop_Plate_L',),
    # Knee_Axle_L / Knee_Sleeve_L / Knee_Magnet_Carrier_L were all DIST
    'DIST': ('HW_DowelPin_D10x35', 'RIG_Knee_Collar_L',
             'RIG_Knee_Magnet_Carrier_L'),
    # both sit on Cart_Guide_Rod_L beyond the UPPER spigot, so they turn about
    # the upper pivot with the cartridge, exactly like Cart_Guide_Rod_L
    'CART_UP': ('HW_WasherStack_M5', 'RIG_Knee_Bumper_Tube_L'),
}


def register_pose_classes():
    """Give the §2.3 / §13 replacement parts the pose class they inherit."""
    for cls, names in RIG_POSE_CLASS.items():
        attr = cls + '_NAMES'
        cur = getattr(beni_lib, attr)
        setattr(beni_lib, attr, tuple(cur) + tuple(n for n in names
                                                   if n not in cur))
    return sum(len(v) for v in RIG_POSE_CLASS.values())


def occ_mass_g(occ):
    try:
        return occ.component.physicalProperties.mass * 1000.0
    except Exception:
        return 0.0


def slide_mass(verbose=True):
    """Mass on the slide, the ballast to reach half the robot, and the split."""
    r = root()
    target = 1.6451                     # half of 3.2901 kg, sim/beni_inertia.json
    rows, total = [], 0.0
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        nm = base_name(o.component.name)
        if nm in FIXED or nm == 'RIG_Torque_Arm':
            continue                    # torque arm replaces the link, step 2 only
        g = occ_mass_g(o)
        rows.append((o.name, nm, g))
        total += g
    agg = {}
    for _n, nm, g in rows:
        agg[nm] = agg.get(nm, 0.0) + g
    if verbose:
        print('   on the slide:')
        for nm in sorted(agg, key=lambda k: -agg[k]):
            print('      %-32s %8.1f g' % (nm, agg[nm]))
        print('      %-32s %8.1f g' % ('TOTAL', total))
        print('   target (half of 3.2901 kg)          %8.1f g' % (target * 1000))
        print('   ballast still needed                %+8.1f g' % (target * 1000 - total))
    return total, agg


def sprung_split(verbose=True):
    """Sprung / unsprung split about the knee spring."""
    r = root()
    sprung = unsprung = 0.0
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        nm = base_name(o.component.name)
        if nm in FIXED or nm == 'RIG_Torque_Arm':
            continue
        g = occ_mass_g(o)
        cls = beni_lib.classify(o)
        if cls in ('DIST', 'CART_LO'):
            unsprung += g
        elif cls == 'SPRING':
            sprung += g / 2.0           # the spring straddles the joint
            unsprung += g / 2.0
        else:
            sprung += g
    tot = sprung + unsprung
    if verbose:
        print('   sprung   (carriage, motor, panel, hub, thigh)  %8.1f g' % sprung)
        print('   unsprung (shank, wheel motor, wheel)           %8.1f g' % unsprung)
        print('   total                                          %8.1f g' % tot)
        print('   unsprung fraction                              %8.1f %%'
              % (100.0 * unsprung / tot if tot else 0.0))
    return sprung, unsprung


# ================================================= 11. the §4.4 release checks
def wheel_axis():
    """(X, Z) of the wheel axis, from the tyre bounding box's CENTRE.

    The centre is safe; the min/max are not.  Fusion returns an occurrence
    bounding box as the axis-aligned box of the *untransformed* box, so once the
    distal link is rotated the tyre's 110 mm box reports as 146 mm
    (110 x (cos25 + sin25) at phi = +25).  Reading a clearance off b[4] therefore
    overstates the envelope by up to a third.  The centre transforms exactly, so
    take the wheel's lowest point as centre - 55 instead.
    """
    b = bbox_of(find_occ('Wheel_Tyre_L'))
    return (b[0] + b[1]) / 2.0, (b[4] + b[5]) / 2.0


def wheel_bottom():
    """Lowest point of the tyre, mm.  The tyre is a body of revolution."""
    return wheel_axis()[1] - WHEEL_R


def check1_knee_sweep():
    print('=== CHECK 1: knee sweep reproduces guide §4 ===')
    ref = {-8: (-12.0, 11.6), 0: (0.0, 0.0), 5: (8.3, 6.4), 10: (17.1, 12.0),
           15: (26.4, 16.8), 20: (36.1, 20.8), 25: (46.1, 24.0), 27: (None, None)}
    rig_set_pose(0.0, 0.0)
    x0, z0 = wheel_axis()
    worst = 0.0
    print('    φ    vertical  guide    fore-aft  guide')
    for phi in sorted(ref):
        rig_set_pose(0.0, float(phi))
        x, z = wheel_axis()
        vert, fore = z - z0, abs(x - x0)
        g = ref[phi]
        if g[0] is None:
            print('  %+4d   %8.2f      -    %8.2f      -' % (phi, vert, fore))
            continue
        worst = max(worst, abs(vert - g[0]), abs(fore - g[1]))
        print('  %+4d   %8.2f %6.1f    %8.2f %6.1f' % (phi, vert, g[0], fore, g[1]))
    rig_set_pose(0.0, 0.0)
    print('  worst deviation %.3f mm  ->  %s'
          % (worst, 'PASS' if worst < 0.15 else 'FAIL'))
    return worst


def check2_shoulder_sweep(step=15.0):
    """CHECK 2, unchanged in intent.  Rail/column/carriage/base leave the
    exclusion list because they are deleted; the STAND is deliberately NOT
    added to it -- not fouling the stand is the whole point of this check, and
    excluding it would make the check vacuous.  RIG_Floor_Plate stays excluded
    because in Mode A the wheel rests ON it, so contact is the design intent.
    """
    print('=== CHECK 2: shoulder +/-120 deg, service loop and rig clearance ===')
    print('  step-2 fixtures excluded (leg off when they are fitted): %s'
          % ', '.join(STEP2_FIXTURES))
    print('  RIG_Floor_Plate excluded (the wheel rests on it); RIG_Stand IS '
          'checked')
    bad = []
    lo = -1e9
    thetas = [t * step for t in range(int(-120 / step), int(120 / step) + 1)]
    for t in thetas:
        rig_set_pose(t, 0.0)
        cl = [c for c in real_clashes(verbose=False)
              if not any(f in c[0] or f in c[1]
                         for f in ('RIG_Floor_Plate',) + STEP2_FIXTURES)]
        lo = max(lo, Z_FLOOR_A - wheel_bottom())
        if cl:
            bad.append((t, cl))
    rig_set_pose(0.0, 0.0)
    print('  swept %+.0f .. %+.0f deg in %.0f deg steps, %d poses, %d with '
          'clashes' % (thetas[0], thetas[-1], step, len(thetas), len(bad)))
    for t, cl in bad:
        print('     theta %+7.1f  %s' % (t, cl))
    print('  closest the wheel comes to the Mode A contact plane, at phi = 0: '
          '%+.2f mm' % -lo)
    print('  (a positive number is clearance: at phi = 0 the leg is 12.04 mm')
    print('   shorter than the -8 deg reach the floor is datumed to)')
    print('  -> %s' % ('PASS' if not bad else 'FAIL'))
    return bad


def _phi_for_contact(dz):
    """Knee angle that keeps the wheel on the floor with the shoulder at dz."""
    lo, hi = -8.0, 27.0
    for _ in range(80):
        mid = (lo + hi) / 2.0
        rig = -154.269
        # wheel_z(phi) from the frozen closed form
        d = math.radians(-50.0 - mid)
        wz = -120.0 * math.cos(math.radians(50.0)) - 120.0 * math.cos(d)
        if dz + wz < rig:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def check3_mode_b_travel():
    """[DEFERRED - MODE B]  Superseded in the Mode A build by
    check3_mode_a_floor().  It drives slide_to(), which needs a carriage."""
    print('=== CHECK 3: wheel clears the floor through the whole Mode B travel ===')
    print('  (a) on the ground: dz and phi are coupled by the contact condition')
    bad = []
    for phi in (-8.0, 0.0, 10.0, 20.0, 25.0, 27.0):
        d = math.radians(-50.0 - phi)
        wz = -120.0 * math.cos(math.radians(50.0)) - 120.0 * math.cos(d)
        dz = -154.269 - wz
        slide_to(dz, 0.0, phi)
        cl = [c for c in real_clashes(verbose=False)
              if not any(f in c[0] or f in c[1]
                         for f in STEP2_FIXTURES + STATION_FITTED)]
        wb = wheel_bottom()
        ok = abs(wb - Z_FLOOR) < 0.02 and not cl
        print('     phi %+6.1f  dz %+7.2f  wheel bottom %9.3f  floor %9.3f  '
              'delta %+6.3f  clashes %d  %s'
              % (phi, dz, wb, Z_FLOOR, wb - Z_FLOOR, len(cl),
                 'ok' if ok else 'FAIL ' + str(cl)))
        if not ok:
            bad.append((phi, cl))
    print('  (b) airborne on a drop station: knee at its -8 deg extension stop')
    for dz in (12.04, 20.0, 50.0, 100.0, TRAVEL_UP):
        slide_to(dz, 0.0, -8.0)
        cl = [c for c in real_clashes(verbose=False)
              if not any(f in c[0] or f in c[1]
                         for f in STEP2_FIXTURES + STATION_FITTED)]
        wb = wheel_bottom()
        ok = wb >= Z_FLOOR - 0.02 and not cl
        print('     dz %+7.2f  wheel bottom %9.3f  clear of floor by %7.3f  '
              'clashes %d  %s'
              % (dz, wb, wb - Z_FLOOR, len(cl), 'ok' if ok else 'FAIL ' + str(cl)))
        if not ok:
            bad.append((dz, cl))
    slide_to(0.0, 0.0, 0.0)
    print('  the wheel lifts off at dz > +12.04 (the knee at its -8 deg stop),')
    print('  so every drop station from 20 mm up starts with the wheel airborne.')
    print('  -> %s' % ('PASS' if not bad else 'FAIL'))
    return bad


def check5_torque_arm():
    """CHECK 5, re-run against the STAND rather than the deleted column.

    It passed in Mode B with the arm's and the column's Y bands disjoint by
    38.50 mm.  The stand's Y band is different, so the disjointness has to be
    re-measured, not inherited.
    """
    print('=== CHECK 5: torque arm clearance (re-run against RIG_Stand) ===')
    arm = find_occ('RIG_Torque_Arm')
    ab = bbox_of(arm)
    st = find_occ('RIG_Stand')
    print('  arm    Y %6.2f .. %6.2f' % (ab[2], ab[3]))
    if st is None:
        print('  RIG_Stand MISSING -- cannot re-run check 5')
        return False
    sb = bbox_of(st)
    print('  stand  Y %6.2f .. %6.2f' % (sb[2], sb[3]))
    gap = ab[2] - sb[3]
    print('  -> Y bands are disjoint by %.2f mm, so the arm cannot reach the '
          'stand at ANY angle' % gap)
    print('     (Mode B read 38.50 mm against RIG_Column; do not quote that '
          'figure for the stand)')
    rmax = math.hypot(ARM_R, ARM_W_TIP / 2.0)
    print('  arm max radius %.1f mm; floor plate at %.1f mm -> %.1f mm clear '
          'at every angle' % (rmax, -Z_FLOOR_A, -Z_FLOOR_A - rmax))
    nose_z = -ARM_W_TIP / 2.0
    shelf = nose_z - SCALE_H - SCALE_SHELF_T
    a = math.degrees(math.asin(max(-1.0, min(1.0, (shelf + SCALE_SHELF_T
                                                   + ARM_W_TIP / 2.0) / ARM_R))))
    print('  scale shelf top Z %.1f; the nose reaches it %.1f deg below '
          'horizontal' % (shelf + SCALE_SHELF_T, abs(a)))
    print('  -> load the arm within +/-8 deg of horizontal-aft; that is also '
          'where cos(a) keeps the 200 mm arm honest to 1 %')
    print('  with RIG_Scale_Pedestal fitted keep the shoulder within '
          '-120..+25 deg (design record §6.1)')
    return gap > 0.0


def check6_stackup():
    """[DEFERRED - MODE B]  Its 63.0 mm assert is the rail-plane overhang and is
    wrong for Mode A.  Superseded by check6_mode_a_overhang()."""
    print('=== CHECK 6: re-verify the §4.1 lateral stack-up ===')
    rows = [('rail mounting plane (column outboard face)', RAIL_PLANE_Y),
            ('+ MGN12H block height 13.0', BLK_Y0 + BLK_H),
            ('+ RIG_Carriage %.1f' % CARR_T, CARR_Y1),
            ('+ Chassis_Shoulder_Plate_L 5.0', PANEL_Y1),
            ('wheel centre plane (half-track)', HALF_TRACK)]
    for lbl, y in rows:
        print('   %-44s y = %7.2f' % (lbl, y))
    over = HALF_TRACK - RAIL_PLANE_Y
    print('   overhang, rail plane to wheel plane        %7.2f mm' % over)
    print('   brief §4.1 assumed                            63.00 mm -> %s'
          % ('matches' if abs(over - 63.0) < 0.01 else 'DIFFERS, restate §4.1'))
    return over


def checks_44():
    """The MODE A release checks (guide §4): 1, 2, 3', 4', 5, 6', 7.

    Was the Mode B six.  check3_mode_b_travel() and check6_stackup() are kept
    but no longer called: the first needs a carriage, and the second's assert is
    hard-coded to the 63.0 mm rail-plane overhang, which is wrong here.
    slide_mass() / sprung_split() are Mode B too -- there is no sprung mass in
    Mode A because there is no ballast, so check 4 becomes the load report.
    """
    register_materials()
    register_pose_classes()
    beni_lib.apply_materials(verbose=False)
    name_bodies()
    replace_cart_stops()            # apply_materials() displaces these two
    placed_assert()
    ref_assert()
    beni_lib.capture_nominal(force=True)
    print()
    r = {}
    r['1'] = check1_knee_sweep(); print()
    r['2'] = check2_shoulder_sweep(); print()
    r['3'] = check3_mode_a_floor(); print()
    r['4'] = check4_mode_a_loads(); print()
    r['5'] = check5_torque_arm(); print()
    r['6'] = check6_mode_a_overhang(); print()
    r['7'] = check7_holddown()
    return r


def checks_44_mode_b():
    """[DEFERRED - MODE B]  The original six, for the slide restart."""
    register_materials()
    beni_lib.apply_materials(verbose=False)
    name_bodies()
    r = {}
    r['1'] = check1_knee_sweep(); print()
    r['2'] = check2_shoulder_sweep(); print()
    r['3'] = check3_mode_b_travel(); print()
    print('=== CHECK 4: mass properties ===')
    slide_mass(); print()
    sprung_split(); print()
    r['5'] = check5_torque_arm(); print()
    r['6'] = check6_stackup()
    return r


def check_ballast_envelope(layers=6, verbose=True):
    """Is there room for a `layers`-deep ballast stack on each stud pair?

    The nominal gap between the carriage and the rail plane is only 13 mm, but
    the sector spans |X| <= 36.7, which clears both the column (X -70..-50) and
    the index post (X 40..60), so the stack may run inboard past the rail plane.
    """
    drop_comp('RIG_Ballast_Envelope')
    occ = new_comp('RIG_Ballast_Envelope')
    c = occ.component
    y1 = CARR_Y0
    y0 = y1 - layers * BALLAST_T
    for a0, a1 in ((BALLAST_A0, BALLAST_A1),
                   (BALLAST_A0 + 180.0, BALLAST_A1 + 180.0)):
        sk = sk_on_y(c, y0)
        arc_sector(sk, 0.0, 0.0, BALLAST_R_IN, BALLAST_R_OUT, a0, a1)
        extrude(c, biggest_profile(sk), y1 - y0)
    vol = sum(b.volume for b in bodies_of(c))
    cl = [x for x in clashes(0.5, verbose=False)
          if 'RIG_Ballast_Envelope' in x[0] or 'RIG_Ballast_Envelope' in x[1]]
    if verbose:
        print('=== ballast envelope, %d layers of %.1f mm (y %.1f .. %.1f) ==='
              % (layers, BALLAST_T, y0, y1))
        print('   volume %.1f cm3 -> %.1f g in steel (%d discs)'
              % (vol, vol * 7.85, 2 * layers))
        if cl:
            print('   CLASHES:')
            for a, b, v in cl:
                print('      %-32s %-32s %9.2f mm3' % (a, b, v))
        else:
            print('   clear of the column, index post, motor cover and rail')
    drop_comp('RIG_Ballast_Envelope')
    return vol * 7.85, cl


# ================================== 12. §2.3, deleting the double-D flats
KNEE_X, KNEE_Z = 91.9253, -77.1345      # knee axis, frozen
SLEEVE_Y0, SLEEVE_Y1 = 63.7, 85.3       # the steel sleeve's span
AXLE_Y0, AXLE_Y1 = 58.7, 90.3           # bearing-to-bearing journal
PIN_LEN = 35.0
MAG_CARRIER_T = 6.0
MAG_D, MAG_T = 6.1, 2.5
COLLAR_D, COLLAR_T = 15.0, 3.0


def build_rig_knee_substitute():
    """Adopt §2.3: kill the double-D flats, keep the encoder's reference.

    The proposal in `beni_rig_no_machining.md` §2.3 says the flats' "only job is
    keying axle to sleeve".  That is incomplete.  The distal tongue is buried
    between the two proximal arms, so the axle is the ONLY path from the distal
    link to the outboard magnet: the key also carries the absolute encoder's
    angular reference, which is the rig's primary instrument.  Deleting it is
    still right, but the reference has to be replaced, not just dropped.

    What this builds:
      * the Ø16 sleeve bore in the printed distal boss becomes Ø10, i.e. the
        steel sleeve's function is printed into the link -- so `Distal_Link_L`
        is NO LONGER "reuse as-is" and its STL must be re-exported;
      * a bought hardened Ø10 h6 ground dowel pin replaces the 4140 axle.  NOT
        a shoulder bolt: a shoulder screw's shoulder is h9/h11, which rattles in
        the 6800's Ø10 bore, and knee-angle noise is measurement error here;
      * a printed collar retains the pin axially, replacing the Ø15 flange;
      * a printed magnet carrier presses onto the pin's 3.4 mm protrusion and
        takes the magnet on the pin's own ground end face.
    """
    for nm in ('Knee_Sleeve_L', 'Knee_Axle_L', 'Knee_Magnet_Carrier_L'):
        print('   removed %-24s x%d' % (nm, drop_comp(nm)))

    # 1. print the sleeve's bore into the distal boss: Ø16 -> Ø10
    dl = find_occ('Distal_Link_L')
    ring(dl.component, SLEEVE_Y0, 5.0, 8.0, SLEEVE_Y1 - SLEEVE_Y0,
         op='join', cx=KNEE_X, cz=KNEE_Z)
    print('   Distal_Link_L bore Ø16 -> Ø10 (sleeve function printed in)')

    # 2. the bought pin
    drop_comp('HW_DowelPin_D10x35')
    occ = new_comp('HW_DowelPin_D10x35')
    cyl_y(occ.component, None, KNEE_X, KNEE_Z, 10.0, AXLE_Y0, AXLE_Y0 + PIN_LEN)
    print('   HW_DowelPin_D10x35  y %.1f .. %.1f, %.1f mm proud of arm B'
          % (AXLE_Y0, AXLE_Y0 + PIN_LEN, AXLE_Y0 + PIN_LEN - AXLE_Y1))

    # 3. printed retaining collar, inboard
    drop_comp('RIG_Knee_Collar_L')
    occ = new_comp('RIG_Knee_Collar_L')
    c = occ.component
    cyl_y(c, None, KNEE_X, KNEE_Z, COLLAR_D, AXLE_Y0 - COLLAR_T, AXLE_Y0)
    cyl_y(c, None, KNEE_X, KNEE_Z, 10.0, AXLE_Y0 - COLLAR_T - 1.0, AXLE_Y0 + 1.0,
          op='cut', participants=bodies_of(c))
    sk = sk_on_y(c, AXLE_Y0 - COLLAR_T)                     # M3 set screw
    circle(sk, KNEE_X + 6.0, KNEE_Z, 2.5)
    extrude(c, profiles(sk), COLLAR_T, op='cut', participants=bodies_of(c))
    print('   RIG_Knee_Collar_L   Ø%.0f x %.1f, M3 set screw + retaining compound'
          % (COLLAR_D, COLLAR_T))

    # 4. printed magnet carrier, pressed on the pin's protrusion
    drop_comp('RIG_Knee_Magnet_Carrier_L')
    occ = new_comp('RIG_Knee_Magnet_Carrier_L')
    c = occ.component
    y0, y1 = AXLE_Y1, AXLE_Y1 + MAG_CARRIER_T
    cyl_y(c, None, KNEE_X, KNEE_Z, COLLAR_D, y0, y1)
    cyl_y(c, None, KNEE_X, KNEE_Z, 10.0, y0 - 0.5, y0 + 3.5, op='cut',
          participants=bodies_of(c))
    cyl_y(c, None, KNEE_X, KNEE_Z, MAG_D, y1 - MAG_T, y1 + 0.5, op='cut',
          participants=bodies_of(c))
    print('   RIG_Knee_Magnet_Carrier_L  Ø10 bore 3.5 deep, Ø%.1f magnet pocket '
          '%.1f deep, face at y %.1f' % (MAG_D, MAG_T, y1))
    print('   magnet bottoms on the pin\'s ground end face at y %.1f'
          % (AXLE_Y0 + PIN_LEN))
    return True


# ============================================ 13. no-laser knee stop + ballast
# The +27 deg hard stop moves OUT of the arc plate and INTO the spring cartridge
# as a compression column.  Reason: the steel plate worked because its slot ends
# were *conformal* -- a 3.1 mm concave radius bearing on a Ø6 dowel, which is
# near-line-on-line and gives ~257 MPa at the 534 N crash load.  Nothing printed
# or off-the-shelf reproduces a concave 3.1 mm steel face, and every convex
# substitute reverts to Hertzian line contact:
#
#     Ø6 dowel on Ø6 pin,  3.2 mm long   2021 MPa
#     Ø6 dowel on Ø10 pin, 3.2 mm long   1808 MPa
#     Ø6 dowel on Ø10 pin, 10 mm long    1023 MPa   but then the dowel is
#                                                   cantilevered 8.3 mm out of a
#                                                   5 mm press in PA-CF, and the
#                                                   moment alone puts 177 MPa of
#                                                   bearing into an 84 MPa wall
#
# A compression stack has no contact-stress problem at all: the load is carried
# as a short steel column in the cartridge's own, already-verified load path
# (seat spigots -> printed eyes -> Ø4 pivot pins), which the spring already
# loads to 203 N continuously.
CART_DEAD = 25.57                       # pin-to-pin dead length, incl 2.0 shims
CART_SPIGOT_UP, CART_SPIGOT_LO = 4.0, 6.0   # spigot projection into the spring
CART_PIVOT_UP = 11.00                   # upper pivot to spigot face
STACK_OD, STACK_ID = 10.0, 5.3          # M5 washer, DIN 125A
STACK_WASHER_T = 1.0
TPU_OD, TPU_ID = 13.0, 10.5             # the bumper tube, AROUND the stack
#   The steel and the bumper act in PARALLEL, not in series.  Stacking the TPU
#   on top of the washers means the steel can never go solid -- the stop is then
#   only as hard as a 51 %-crushed elastomer, which is not the metal-backed stop
#   the guide requires.  The original did the same thing by putting the PU in a
#   separate slot LEVEL from the metal slot end.
PHI_BUMP_TARGET = 20.0                  # where the TPU should first touch
PHI_STOP_TARGET = 27.0                  # where the steel goes solid


# MEASURED off the model with a probe ring at six knee angles, spread 0.0000 mm.
# The dead-length build-up (11.00 + 14.57 upper/lower pivot-to-seat, plus 4.0 and
# 6.0 mm of spigot) predicts 35.57 mm consumed; the solid actually consumes
# 44.570.  Anything sized to fit inside the spring has to be measured, not
# derived -- a 9.0 mm error here would have put the hard stop at +10 deg.
CART_SEAT_CONSUMED = 44.570


def cart_gap(phi):
    """Clear axial space on the guide rod between the two spring seats, mm."""
    return beni_lib.cart_len(phi) - CART_SEAT_CONSUMED


def stop_stack_sizes():
    """Steel stack height and TPU tube height, from the cartridge geometry.

    steel  = the clear gap at +27 deg, so the washers go solid exactly there
    tpu    = the clear gap at +20 deg, so the bumper first touches there
    """
    g_stop = cart_gap(PHI_STOP_TARGET)
    g_bump = cart_gap(PHI_BUMP_TARGET)
    steel = g_stop
    tpu_free = g_bump
    return dict(g_stop=g_stop, g_bump=g_bump, steel=steel,
                tpu_free=tpu_free, tpu_crush=g_bump - g_stop,
                crush=(g_bump - g_stop) / g_bump,
                n_washer=steel / STACK_WASHER_T)


def _cart_frame(phi=0.0):
    """(origin at the upper spigot face, unit vector toward the lower eye)."""
    d, _L = beni_lib.cart_dir(phi)
    ux, uz = beni_lib.UX, beni_lib.UZ
    px = ux + CART_PIVOT_UP * d[0]
    pz = uz + CART_PIVOT_UP * d[1]
    return (px, beni_lib.LEG_Y_MID, pz), (d[0], d[1])


def _place_on_cart(occ, offset_mm, phi=0.0):
    """Put a component built along +Y at `offset` along the cartridge axis."""
    (px, py, pz), (dx, dz) = _cart_frame(phi)
    ox, oz = px + dx * offset_mm, pz + dz * offset_mm
    m = mat((-dz, 0.0, dx), (dx, 0.0, dz), (0.0, 1.0, 0.0), (ox, py, oz))
    occ.transform2 = m
    return occ


# both sit on the rod BEYOND the upper spigot's tip, not on its seat face
STACK_OFFSET = CART_PIVOT_UP + CART_SPIGOT_UP      # 15.00


def build_rig_knee_flexion_stop():
    """The +27 deg hard stop, as a compression column inside the spring."""
    s = stop_stack_sizes()
    print('flexion hard stop, in the cartridge:')
    print('   clear gap at +20 deg %8.3f   at +27 deg %8.3f  -> window %.3f mm'
          % (s['g_bump'], s['g_stop'], s['tpu_crush']))
    print('   steel stack  %.3f mm  = %.1f x 1.0 mm M5 washer, trimmed with'
          ' 0.2/0.3/0.5 shim washers' % (s['steel'], s['n_washer']))
    print('   TPU tube     %.3f mm free, crushing %.3f = %.0f %% at the stop'
          % (s['tpu_free'], s['tpu_crush'], 100 * s['crush']))
    print('   steel stress %.1f MPa; bearing on the printed spigot face %.1f MPa'
          % (534.0 / (math.pi / 4 * (STACK_OD ** 2 - STACK_ID ** 2)),
             534.0 / (math.pi / 4 * (STACK_OD ** 2 - 5.6 ** 2))))
    print('   one 1.0 mm washer moves the stop by %.2f deg, so trim with shims'
          % (1.0 / ((cart_gap(25.0) - cart_gap(27.0)) / 2.0)))

    drop_comp('HW_WasherStack_M5')
    occ = new_comp('HW_WasherStack_M5')
    ring(occ.component, 0.0, STACK_ID / 2.0, STACK_OD / 2.0, s['steel'])
    _place_on_cart(occ, STACK_OFFSET)

    drop_comp('RIG_Knee_Bumper_Tube_L')
    occ2 = new_comp('RIG_Knee_Bumper_Tube_L')
    ring(occ2.component, 0.0, TPU_ID / 2.0, TPU_OD / 2.0, s['tpu_free'])
    _place_on_cart(occ2, STACK_OFFSET)
    print('   -> HW_WasherStack_M5 (Ø%.1f/Ø%.1f) inside RIG_Knee_Bumper_Tube_L'
          ' (Ø%.1f/Ø%.1f), concentric on the guide rod'
          % (STACK_OD, STACK_ID, TPU_OD, TPU_ID))
    return s


# --- the printed plate keeps the extension stop and a flexion BACKUP ----------
STOP_SECTOR_R_IN, STOP_SECTOR_R_OUT = 11.0, 35.5
STOP_SECTOR_A0, STOP_SECTOR_A1 = 200.345, 302.000
STOP_SLOT_R_IN, STOP_SLOT_R_OUT = 26.9, 33.1
STOP_PLATE_Y0, STOP_PLATE_Y1 = 90.3, 93.3
STOP_DOWEL_A_PHI0 = 246.6                # dowel angle at phi = 0
STOP_INSERT_R = 15.0
STOP_INSERT_A = (230.0, 260.0, 290.0)


def build_rig_knee_stop_plate():
    """RIG_Knee_Stop_Plate_L -- printed, replacing the laser-cut steel arc.

    It keeps two of the three jobs the steel plate had:
      * the -8 deg EXTENSION stop, which carries only the spring's own 30 N
        preload (75 N with a 2.5x impact factor).  Against a printed conformal
        3.1 mm slot end that is 3.9 MPa on a 84 MPa wall -- comfortable.
      * a FLEXION BACKUP at +28 deg, one degree past the cartridge stop, so the
        knee is never completely unrestrained.  It is a backup only: at the full
        534 N it would mark, and it is there to catch a missing or mis-shimmed
        washer stack, not to be the working stop.
    """
    drop_comp('Knee_Stop_Arc_L')
    drop_comp('RIG_Knee_Stop_Plate_L')
    occ = new_comp('RIG_Knee_Stop_Plate_L')
    c = occ.component
    kx, kz = KNEE_X, KNEE_Z
    sk = sk_on_y(c, STOP_PLATE_Y0)
    arc_sector(sk, kx, kz, STOP_SECTOR_R_IN, STOP_SECTOR_R_OUT,
               STOP_SECTOR_A0, STOP_SECTOR_A1)
    extrude(c, biggest_profile(sk), STOP_PLATE_Y1 - STOP_PLATE_Y0)

    a_ext = STOP_DOWEL_A_PHI0 + 8.0          # 254.6, the -8 deg stop
    a_flex = STOP_DOWEL_A_PHI0 - 28.0        # 218.6, the +28 deg backup
    r_mid = (STOP_SLOT_R_IN + STOP_SLOT_R_OUT) / 2.0
    sk = sk_on_y(c, STOP_PLATE_Y0)
    n = 24
    pts = []
    for i in range(n + 1):
        a = math.radians(a_flex + (a_ext - a_flex) * i / n)
        pts.append((kx + r_mid * math.cos(a), kz + r_mid * math.sin(a)))
    for i in range(len(pts) - 1):
        slot(sk, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1],
             STOP_SLOT_R_OUT - STOP_SLOT_R_IN)
    extrude(c, profiles(sk), STOP_PLATE_Y1 - STOP_PLATE_Y0, op='cut',
            participants=bodies_of(c))

    sk = sk_on_y(c, STOP_PLATE_Y0)
    for a in STOP_INSERT_A:
        r = math.radians(a)
        circle(sk, kx + STOP_INSERT_R * math.cos(r),
               kz + STOP_INSERT_R * math.sin(r), 3.4)
    extrude(c, profiles(sk), STOP_PLATE_Y1 - STOP_PLATE_Y0, op='cut',
            participants=bodies_of(c))
    print('RIG_Knee_Stop_Plate_L')
    _report(occ, 'RIG_Knee_Stop_Plate_L')
    print('     slot %.1f .. %.1f deg  -> extension stop -8, flexion backup +28'
          % (a_flex, a_ext))
    return occ


# ------------------------------------------------------------------- ballast
POT_R_IN, POT_R_OUT = 40.0, 66.0
POT_A0, POT_A1 = 55.0, 125.0
POT_WALL = 2.0
POT_Y0, POT_Y1 = 4.0, CARR_Y0             # 30 mm deep


def build_rig_ballast_pot():
    """RIG_Ballast_Pot -- printed cup, filled with off-the-shelf dense granulate.

    Replaces the laser-cut steel sector.  Fill it with steel shot, airgun BBs or
    a jar of M4 nuts and set the mass on a kitchen scale -- which gives ~1 g of
    granularity instead of the 32.8 g steps a cut plate gave.
    """
    drop_comp('RIG_Ballast_Disc')
    drop_comp('RIG_Ballast_Pot')
    occ = new_comp('RIG_Ballast_Pot')
    c = occ.component
    sk = sk_on_y(c, POT_Y0)
    arc_sector(sk, 0.0, 0.0, POT_R_IN, POT_R_OUT, POT_A0, POT_A1)
    extrude(c, biggest_profile(sk), POT_Y1 - POT_Y0)
    da = math.degrees(POT_WALL / POT_R_IN)
    sk = sk_on_y(c, POT_Y0 + POT_WALL)
    arc_sector(sk, 0.0, 0.0, POT_R_IN + POT_WALL, POT_R_OUT - POT_WALL,
               POT_A0 + da, POT_A1 - da)
    extrude(c, biggest_profile(sk), POT_Y1 - POT_Y0 - POT_WALL, op='cut',
            participants=bodies_of(c))
    sk = sk_on_y(c, POT_Y0)
    for a in BALLAST_STUD_A[:2]:
        r = math.radians(a)
        circle(sk, BALLAST_STUD_R * math.cos(r),
               BALLAST_STUD_R * math.sin(r), 4.5)
    extrude(c, profiles(sk), POT_WALL, op='cut', participants=bodies_of(c))
    m = mat((-1, 0, 0), (0, 1, 0), (0, 0, -1), (0.0, 0.0, 0.0))
    root().occurrences.addExistingComponent(c, m)

    body = c.bRepBodies.item(0)
    inner = ((POT_A1 - POT_A0 - 2 * da) / 360.0) * math.pi * (
        (POT_R_OUT - POT_WALL) ** 2 - (POT_R_IN + POT_WALL) ** 2) * (
        POT_Y1 - POT_Y0 - POT_WALL)
    print('RIG_Ballast_Pot  (2 fitted)')
    _report(occ, 'RIG_Ballast_Pot')
    print('     shell %.1f g each in PA-CF; internal volume %.1f cm3 each'
          % (body.volume * 1.15, inner / 1000.0))
    print('     2 pots hold %.1f cm3 -> %.0f g of steel shot at 4.7 g/cm3'
          % (2 * inner / 1000.0, 2 * inner / 1000.0 * 4.7))
    return occ


# ==================================================== 14. MODE A: RIG_Stand
# Mode A is the active build (2026-08-17): the shoulder bolts rigid to a printed
# stand, and the vertical slide, the ballast and the drop series are [DEFERRED -
# MODE B].  Requirement set: fusion_agent_guide_mode_a.md §2.  Every load figure
# comes from rig_calc.mode_a_stand() / mode_a_bolt_group(); none is re-derived
# here.  Z datum: Z_FLOOR_A / Z_BENCH_A, above.
#
#   design load    11.00 N.m yaw about the motor axis (shoulder stall), 25.00
#                  N.m at the proof screen.  Pitch 2.30 and roll 2.99 N.m are
#                  trivial by comparison and the static hanging load (8.22 N of
#                  leg, 12.03 N with a 388 g motor) is ~3 % of the yaw.
#   structural joint   Chassis_Shoulder_Plate_L's five existing frame-bolt
#                  holes, five M3 in shear, worst screw 53.2 N at stall and
#                  121.0 N at proof.  No register, no dowel, no block.
#   overhang       42.00 mm, stand outboard face to wheel plane.  NOTHING may
#                  land between the stand and y = 42.0.
#   hold-down      must be CLAMPED.  110.0 N at a 100 mm base half-width, and a
#                  printed stand is well under a kilogram.

STAND_Y1 = PANEL_Y0                     # 42.00 = the motor front mount face
STAND_T = 12.0                          # web / pad thickness in Y
STAND_Y0 = STAND_Y1 - STAND_T           # 30.00
STAND_FOOT_T = 32.0                     # foot thickness in Y = the clamp's bite
STAND_FOOT_Y0 = STAND_Y1 - STAND_FOOT_T  # 10.00
STAND_BORE_D = CARR_BORE_D              # 82.0, clears the O80 housing by 1 mm
STAND_HUB_R = CARR_PAD_R                # 56.0, hub ring outer radius
STAND_BEAM_W = 34.0                     # bolt beam: >= 7.5 mm wall at a bore
STAND_RIB_W = 24.0                      # lower-bolt rib: 9.5 mm wall at a bore
STAND_RAIL_W = 16.0
STAND_TIE_W = 12.0
STAND_FOOT_X = 100.0                    # base HALF-width -> rig_calc's 100 mm row
STAND_FOOT_H = 20.0
Z_FOOT_TOP = Z_BENCH_A + STAND_FOOT_H          # -207.3119, the clamp landings
Z_FOOT_MID = Z_BENCH_A + STAND_FOOT_H / 2.0    # -217.3119, where the rails land

# Nodes, global (X, Z).  Only the five bolt positions are fixed data; the rest
# are layout choices, and every derived point is interpolated in code.
N_BOLT_LO = PANEL_FRAME_BOLTS[0]        # (-60, -18), the lone low bolt
N_BEAM_A, N_BEAM_F = (-60.0, 55.0), (30.0, 55.0)     # bolt beam ends
N_RAIL_F_TOP = (33.0, 41.0)             # fore rail top, inside the beam's cap
N_RAIL_F_KNEE = (58.0, -10.0)           # kink: routes the rail OUTSIDE the ring
N_RAIL_F_FOOT = (70.0, Z_FOOT_MID)
N_RAIL_A_FOOT = (-70.0, Z_FOOT_MID)
N_POST_TOP, N_POST_FOOT = (0.0, -45.0), (0.0, Z_FOOT_MID)
STAND_TIE_Z = (-80.0, -150.0)           # rung heights
STAND_BRACE_TOP_Z = -20.0               # top bay's fore anchor
STAND_BOLT_D = 6.5                      # M6 bench-bolt clearance
STAND_BOLT_CB_D, STAND_BOLT_CB_DEEP = 11.0, 7.0      # M6 SHCS head sits sub-flush
STAND_BOLT_X = (-88.0, -26.0, 34.0, 88.0)            # two stations per side


def _on_seg(p0, p1, z):
    """X where the segment p0->p1 crosses Z = z."""
    return p0[0] + (z - p0[1]) / (p1[1] - p0[1]) * (p1[0] - p0[0])


def build_rig_stand():
    """RIG_Stand -- the whole Mode A structure, one printed part.

    Replaces RIG_Base + RIG_Column + RIG_Braces + RIG_Carriage.

    WHAT IT IS.  A single profile in the XZ plane extruded along Y: a mount pad
    at the top (a hub ring around the motor, a bolt beam over the four upper
    frame bolts, and a rib out to the lone low one), a two-rail ladder with two
    rungs and three shear braces running down to the bench, and a foot bar that
    is thicker in Y than the web so a clamp jaw has something square to bite.

    ⚠ AT THESE MEMBER WIDTHS THE UPPER WEB IS EFFECTIVELY SOLID -- the members
    overlap so much that the silhouette comes out ~85 % filled, and only the
    lower two bays read as open.  That is deliberate rather than accidental: the
    working stress is ~0.28 MPa axial in the rails at stall against 84-102 MPa
    XY, so nothing here is strength-limited, and what the guide actually asks for
    (§2.6) is STIFFNESS, where solid beats truss per mm of thickness.  The cost
    is mass and print time: 499.3 cm3 / 574.2 g, against the "~0.3 kg" the guide
    §2.4 tipping table assumes.  Heavier only strengthens that argument -- it is
    still 20x short of the 11.2 kg dead weight would need -- but if print time
    matters, STAND_T and the four member widths are the constants to turn, and
    nothing downstream depends on the mass.

    WHY THAT SHAPE, AND WHY THAT PRINT ORIENTATION.
      * PRINT IT MOUNT FACE (y = 42.00) FLAT ON THE BED, BUILDING INBOARD (-Y).
        Every layer is then an XZ slice, and the 11.00 N.m of shoulder yaw --
        which is a couple about Y, i.e. a couple lying IN the XZ plane -- is
        carried entirely within the layer plane, where PA-CF is 84-102 MPa
        rather than 26-50.  Guide §2.6: keep the yaw path in the print plane.
      * The part's Y thickness only ever DECREASES away from the bed (web 12
        over the pad and ladder, 32 at the foot, all sharing y = 42.00), so the
        print needs no support anywhere and every hole is a clean vertical
        feature.  The mount face, which has to bear flat on the panel, is the
        bed-facing surface -- the flattest one a printer makes -- and the five
        insert bores open on it.
      * The compliance that would corrupt a measurement is IN-PLANE.  Guide §2.6
        warns the stand is now the softest element in the load path and that its
        deflection reads as shoulder ANGLE error, not knee error.  Shoulder
        angle error is exactly rotation about Y, which this profile resists as
        axial tension/compression in two widely spaced rails -- the stiffest
        mode a plate has, and the strongest print direction.  A part printed
        upright instead would put the same couple across the layer bonds.
      * Yaw is reacted at the bench by a vertical force pair separated in X, so
        the foot spans the full +/-100 mm base half-width and the rails land
        inboard of its ends, leaving four clear clamp landings on its top face.

    WHAT WAS REJECTED.
      * Bolting to the motor's REAR face.  8 x M3 on the same O74 PCD are
        tapped there and it would be stiffer, but GAUGE_Shoulder_Motor_Interface
        models only the front 9.5 mm of the motor and every interface has to be
        gated on that coupon (design record §1.1).
      * The panel's four freed O88 cover holes as extra landings.  A fastener
        there needs access to the panel's INBOARD face, which the stand is
        bolted flat against.  Left open, per design record §2.2.
      * A solid web.  It is stiffer per mm of thickness but ~3x the mass and
        print time for a load case that peaks well under 1 MPa in the members.
      * Modelled fillets at the member junctions.  beni_lib's fillet helpers
        exist because PA-CF cracks at re-entrant corners, but the slot-to-slot
        junctions here are already tangent arcs, and the working stress is two
        orders below the 84 MPa wall, so a stress riser has nothing to raise.
      * Holding it down by dead weight.  Guide §2.4 / rig_calc: 11.00 N.m needs
        110.0 N (11.2 kg) at a 100 mm base half-width and still 36.7 N (3.7 kg)
        at 300 mm.  It gets clamped, and the foot shows both paths.
    """
    drop_comp('RIG_Stand')
    occ = new_comp('RIG_Stand')
    c = occ.component

    aft = (N_BOLT_LO, N_RAIL_A_FOOT)                 # aft rail, one segment
    fore = (N_RAIL_F_KNEE, N_RAIL_F_FOOT)            # fore rail, lower segment

    # ---- the web: one sketch, every member overlapping, extruded once ------
    sk = sk_on_y(c, STAND_Y0)
    circle(sk, 0.0, 0.0, 2 * STAND_HUB_R)            # hub ring blank
    slot(sk, N_BEAM_A[0], N_BEAM_A[1], N_BEAM_F[0], N_BEAM_F[1], STAND_BEAM_W)
    slot(sk, 0.0, 0.0, N_BOLT_LO[0], N_BOLT_LO[1], STAND_RIB_W)   # ring -> low bolt
    slot(sk, N_BOLT_LO[0], N_BOLT_LO[1], N_BEAM_A[0], N_BEAM_A[1], STAND_RIB_W)
    slot(sk, aft[0][0], aft[0][1], aft[1][0], aft[1][1], STAND_RAIL_W)
    slot(sk, N_RAIL_F_TOP[0], N_RAIL_F_TOP[1],
         N_RAIL_F_KNEE[0], N_RAIL_F_KNEE[1], STAND_RAIL_W)
    slot(sk, fore[0][0], fore[0][1], fore[1][0], fore[1][1], STAND_RAIL_W)
    slot(sk, N_POST_TOP[0], N_POST_TOP[1], N_POST_FOOT[0], N_POST_FOOT[1],
         STAND_RAIL_W)
    for z in STAND_TIE_Z:                            # two rungs
        slot(sk, _on_seg(aft[0], aft[1], z), z,
             _on_seg(fore[0], fore[1], z), z, STAND_TIE_W)
    # three shear braces, one per bay.  Without them the ladder parallelograms
    # under the 71.3 N fore-aft ground reaction that comes with stall torque.
    bays = ((STAND_TIE_Z[0], STAND_BRACE_TOP_Z),
            (STAND_TIE_Z[1], STAND_TIE_Z[0]),
            (Z_FOOT_MID, STAND_TIE_Z[1]))
    for z_a, z_f in bays:
        slot(sk, _on_seg(aft[0], aft[1], z_a), z_a,
             _on_seg(fore[0], fore[1], z_f), z_f, STAND_TIE_W)
    extrude(c, profiles(sk), STAND_T)
    if c.bRepBodies.count > 1:
        print('   WARNING: web made %d bodies, expected 1' % c.bRepBodies.count)

    # ---- the foot: thicker in Y, same outboard face --------------------------
    box(c, -STAND_FOOT_X, STAND_FOOT_X, STAND_FOOT_Y0, STAND_Y1,
        Z_BENCH_A, Z_FOOT_TOP, op='join')

    # ---- motor clearance ----------------------------------------------------
    cyl_y(c, None, 0.0, 0.0, STAND_BORE_D, STAND_Y0 - 1.0, STAND_Y1 + 1.0,
          op='cut', participants=bodies_of(c))

    # ---- five M3 insert bores, from the OUTBOARD face -----------------------
    # 5.0 deep in a 12 mm web leaves a 7 mm floor.  The insert's grip in printed
    # nylon is the joint's weak element and its magnitude is unverified (guide
    # §2.3), so this is designed FOR it: full depth, real material round the
    # boss, and a depth-stopped installation tip on the bench.
    sk = sk_on_y(c, STAND_Y1)
    for x, z in PANEL_FRAME_BOLTS:
        circle(sk, x, z, INSERT_M3_D)
    extrude(c, profiles(sk), -INSERT_M3_L, op='cut', participants=bodies_of(c))

    # ---- bench-bolt path: 4 x M6 through the foot, heads sub-flush ----------
    y_bolt = (STAND_FOOT_Y0 + STAND_Y1) / 2.0
    sk = sk_on_z(c, Z_BENCH_A - 1.0)
    for x in STAND_BOLT_X:
        circle_xy(sk, x, y_bolt, STAND_BOLT_D)
    extrude(c, profiles(sk), STAND_FOOT_H + 2.0, op='cut',
            participants=bodies_of(c))
    sk = sk_on_z(c, Z_FOOT_TOP)
    for x in STAND_BOLT_X:
        circle_xy(sk, x, y_bolt, STAND_BOLT_CB_D)
    extrude(c, profiles(sk), -STAND_BOLT_CB_DEEP, op='cut',
            participants=bodies_of(c))

    print('RIG_Stand')
    _report(occ, 'RIG_Stand')
    vol = sum(b.volume for b in bodies_of(c))
    print('     %.1f cm3 -> %.1f g in PA-CF at 1.15 g/cm3' % (vol, vol * 1.15))
    print('     mount face y = %.2f (= PANEL_Y0), web %.1f mm, foot %.1f mm'
          % (STAND_Y1, STAND_T, STAND_FOOT_T))
    print('     foot X %+.0f..%+.0f on the bench at Z %.4f, top face Z %.4f'
          % (-STAND_FOOT_X, STAND_FOOT_X, Z_BENCH_A, Z_FOOT_TOP))
    print('     PRINT: mount face flat on the bed, building inboard; no support')
    return occ


# ------------------------------------------- the §6.1 REF_* transform guard
# Deleting ANY occurrence in Beni_SingleLegRig re-resolves both external motor
# STEP references -- reproducibly, twice on the same delete.  isSuppressed is
# not a workaround (the property is not readable on this API build, so the
# assignment lands silently on the Python wrapper).  What works: capture
# transform2 before the delete, write it back after, then assert.
#
# ⚠ §6.1 IS INCOMPLETE.  It says to capture the two REF_* trees, 7 transforms.
# Stripping the Mode B occurrences displaced 2 of those 7 exactly as documented
# -- AND ALSO reset HW_WasherStack_M5 and RIG_Knee_Bumper_Tube_L to identity,
# which dropped both into the shoulder motor at the origin and invented four
# clashes totalling 430 mm3.  The REF bounding-box guard passed the whole time,
# so this is another trap that produces a passing wrong answer.
#
# The distinction that predicts it: those two are the only parts positioned by
# assigning `occ.transform2` to an occurrence made with addNewComponent(identity)
# (rig_lib._place_on_cart).  Every screw, which place() creates with
# addExistingComponent(component, matrix), survived untouched -- 18 of 20 spot
# checks unchanged to 0.05 mm.  So capture EVERY occurrence, not just the REFs.
REF_GUARD = (('REF_GIM6010-8', 5.00, 49.00), ('REF_GIM4305-10', 61.50, 94.50))

# Positioned by assigning occ.transform2; identity puts them at the origin.
PLACED_BY_TRANSFORM = ('HW_WasherStack_M5', 'RIG_Knee_Bumper_Tube_L')


def _occ_tree(occ):
    out, stack = [occ], [occ]
    while stack:
        cur = stack.pop()
        for i in range(cur.childOccurrences.count):
            k = cur.childOccurrences.item(i)
            out.append(k)
            stack.append(k)
    return out


def xf_capture():
    """transform2 for every root occurrence plus every child of a REF_* tree."""
    saved, done = [], set()
    r = root()
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        for k in (_occ_tree(o) if base_name(o.component.name).startswith('REF_')
                  else [o]):
            if k.entityToken in done:
                continue
            done.add(k.entityToken)
            saved.append((k, list(k.transform2.asArray())))
    return saved


def xf_restore(saved):
    n = []
    for k, arr in saved:
        try:
            cur = list(k.transform2.asArray())
        except Exception:
            continue                    # deleted on purpose
        if max(abs(a - b) for a, b in zip(cur, arr)) > 1e-9:
            m = adsk.core.Matrix3D.create()
            m.setWithArray(arr)
            k.transform2 = m
            n.append(k.name)
    return n


# kept as aliases: the guide and OPERATOR.md both name ref_capture/ref_restore
ref_capture, ref_restore = xf_capture, xf_restore


def ref_assert(tol=0.02, verbose=True):
    """A failed guard means NO DATA, not caveated data.  Raises."""
    bad = []
    for nm, y0, y1 in REF_GUARD:
        o = find_occ(nm)
        if o is None:
            bad.append((nm, 'missing'))
            continue
        b = bbox_of(o)
        ok = abs(b[2] - y0) <= tol and abs(b[3] - y1) <= tol
        if verbose:
            print('   %-16s Y %7.2f .. %7.2f   want %6.2f .. %6.2f   %s'
                  % (nm, b[2], b[3], y0, y1, 'ok' if ok else 'DISPLACED'))
        if not ok:
            bad.append((nm, (round(b[2], 3), round(b[3], 3))))
    if bad:
        raise RuntimeError('REF_* displaced -- discard this run: %s' % bad)
    return True


def placed_assert(verbose=True):
    """The second half of the guard: nothing placed by transform2 is at identity."""
    ident = list(adsk.core.Matrix3D.create().asArray())
    bad = []
    for nm in PLACED_BY_TRANSFORM:
        o = find_occ(nm)
        if o is None:
            continue
        a = list(o.transform2.asArray())
        at_ident = max(abs(x - y) for x, y in zip(a, ident)) < 1e-9
        if verbose:
            b = bbox_of(o)
            print('   %-26s X %7.2f..%7.2f Z %8.2f..%8.2f   %s'
                  % (nm, b[0], b[1], b[4], b[5],
                     'AT IDENTITY -- DISPLACED' if at_ident else 'placed ok'))
        if at_ident:
            bad.append(nm)
    if bad:
        raise RuntimeError('displaced to the origin: %s -- call '
                           'replace_cart_stops()' % bad)
    return True


def replace_cart_stops():
    """Put the two cartridge stop parts back on the cartridge axis.

    Repairs the displacement above without rebuilding their geometry, so the
    measured CART_SEAT_CONSUMED stack is untouched.
    """
    n = []
    for nm in PLACED_BY_TRANSFORM:
        o = find_occ(nm)
        if o is not None:
            _place_on_cart(o, STACK_OFFSET)
            n.append(nm)
    return n


def guarded(fn, *a, **kw):
    """Run anything structural inside the capture / restore / assert cycle."""
    saved = xf_capture()
    out = fn(*a, **kw)
    moved = xf_restore(saved)
    if moved:
        print('   guard fired: rewrote %d of %d transforms  %s'
              % (len(moved), len(saved), moved))
    ref_assert()
    placed_assert(verbose=False)
    return out


# ------------------------------------------------------ stripping Mode B out
# Deferred, NOT cancelled: only the occurrences go, every builder above stays.
MODE_B_OCCS = ('RIG_Base', 'RIG_Column', 'RIG_Braces', 'RIG_Rail', 'HW_MGN12H',
               'RIG_Carriage', 'RIG_Index_Post', 'RIG_Index_Bar',
               'RIG_Hard_Stops', 'RIG_Mode_Pin', 'RIG_Ballast_Pot',
               'RIG_Ballast_Disc', 'RIG_Cable_Post_B')


def strip_mode_b(verbose=True):
    """Delete the Mode B occurrences under the transform guard.

    RIG_Cable_Post_B goes with them because it mounts to RIG_Column's T-slot and
    there is no column.  Re-routing it to the stand is guide §3's open item, not
    this one -- the builder is untouched.
    """
    saved = xf_capture()
    if verbose:
        print('   captured %d transforms (guide §6.1 only asks for the 7 REF_* '
              'ones -- see xf_capture)' % len(saved))
    gone = []
    for nm in MODE_B_OCCS:
        k = drop_comp(nm)
        if k:
            gone.append('%s x%d' % (nm, k))
    moved = xf_restore(saved)
    if verbose:
        print('   deleted: %s' % ', '.join(gone))
        print('   guard fired on %d of %d transforms: %s'
              % (len(moved), len(saved), moved))
    ref_assert()
    placed_assert()
    beni_lib.capture_nominal(force=True)
    return gone


def build_mode_a(verbose=True):
    """Take the model from the Mode B state to the Mode A build."""
    print('=== MODE A build ===')
    print('1. strip the Mode B occurrences')
    strip_mode_b(verbose)
    print()
    print('2. build RIG_Stand')
    guarded(build_rig_stand)
    print()
    print('3. build the fixed-side Mode A cable anchor')
    if find_occ('RIG_Cable_Anchor_ModeA') is None:
        guarded(build_rig_cable_anchor_mode_a)
    print()
    print('4. re-datum the two parts that stood on the deleted 2020 base')
    guarded(build_rig_floor)
    guarded(build_rig_scale_pedestal)
    print()
    print('5. guards')
    ref_assert()
    placed_assert()
    register_materials()
    beni_lib.apply_materials(verbose=False)
    name_bodies()
    beni_lib.capture_nominal(force=True)
    return True


# ============================================ 15. the MODE A release checks
def check3_mode_a_floor():
    """CHECK 3, replaced.  The wheel clears the floor plate at every knee angle
    with the stand at its designed height.  Trivial in Mode A because the wheel
    is ON the floor and the stand does not move, so phi is the only variable.
    Wheel bottom is read as bbox CENTRE - 55 (trap 3: the box inflates under
    rotation, the centre transforms exactly).
    """
    print('=== CHECK 3: wheel clears the floor plate, phi -8 .. +27 (Mode A) ===')
    print('   floor plate top face Z = %.4f  (shoulder axis %.2f mm above it)'
          % (Z_FLOOR_A, -Z_FLOOR_A))
    bad = []
    print('     phi     wheel bottom      clear of floor   clashes')
    for phi in (PHI_EXT_STOP, 0.0, 10.0, 20.0, 25.0, 27.0):
        rig_set_pose(0.0, phi)
        cl = [x for x in real_clashes(verbose=False)
              if not any(f in x[0] or f in x[1] for f in STEP2_FIXTURES)]
        wb = wheel_bottom()
        clear = wb - Z_FLOOR_A
        ok = clear >= -0.02 and not cl
        print('   %+7.1f   %11.4f   %+14.4f   %d  %s'
              % (phi, wb, clear, len(cl), 'ok' if ok else 'FAIL ' + str(cl)))
        if not ok:
            bad.append((phi, clear, cl))
    rig_set_pose(0.0, 0.0)
    print('   at the -8 deg extension stop the wheel just touches, by design:')
    print('   that is what guide §2.5\'s 221.31 mm requirement buys, and it is')
    print('   why a free leg rests on the stop instead of being pre-compressed.')
    print()
    print('   ⚠ CONSEQUENCE the guide does not work through.  Datuming the floor')
    print('   to the -8 deg reach makes the leg longest exactly at the contact')
    print('   point, so rotating the shoulder can only LIFT the wheel.  At phi =')
    print('   -8 the wheel axis is 4.000 deg off plumb at r = 166.718, so it')
    print('   touches the floor only for theta in 0 .. +8.00 deg -- an 8.00 deg')
    print('   window, ~23 mm of roll.  Brief §3 / guide §2.5 assume "a shoulder')
    print('   sweep rolls the wheel ~77 mm; if it scrubs, every force reading is')
    print('   corrupt".  That premise needs the wheel LOADED on the floor, which')
    print('   needs the floor ABOVE the -8 deg reach, which pre-compresses the')
    print('   knee and takes the leg off the extension stop.  The two cannot both')
    print('   hold with a rigid stand.  221.31 mm is the only height that')
    print('   satisfies ">= 221.31" AND leaves the floor touching at all.')
    print('   -> %s' % ('PASS' if not bad else 'FAIL'))
    return bad


def stand_bolt_group(plate_t=None):
    """Measure the stand's five insert bores and rebuild the §2.3 bolt group.

    This is the CAD check on rig_calc.mode_a_bolt_group()'s inputs: the group is
    read off the modelled bores, not off PANEL_FRAME_BOLTS, and each is checked
    concentric with the panel hole it lands on.
    """
    plate_t = STAND_T if plate_t is None else plate_t
    st = find_occ('RIG_Stand')
    if st is None:
        return None
    found = []
    for b in bodies_of(st.component):
        for f in b.faces:
            g = f.geometry
            if g.objectType != 'adsk::core::Cylinder':
                continue
            if abs(2 * g.radius * 10.0 - INSERT_M3_D) > 0.01:
                continue
            bb = f.boundingBox
            x = (bb.minPoint.x + bb.maxPoint.x) / 2.0 * 10.0
            z = (bb.minPoint.z + bb.maxPoint.z) / 2.0 * 10.0
            y0, y1 = bb.minPoint.y * 10.0, bb.maxPoint.y * 10.0
            key = (round(x, 3), round(z, 3))
            if key not in [k for k, _d in found]:
                found.append((key, (round(y0, 3), round(y1, 3))))
    pts = [k for k, _d in found]
    if not pts:
        return None
    xc = sum(p[0] for p in pts) / len(pts)
    zc = sum(p[1] for p in pts) / len(pts)
    radii = [math.hypot(p[0] - xc, p[1] - zc) for p in pts]
    r2 = sum(r * r for r in radii)
    rmax = max(radii)
    return dict(pts=pts, depths=[d for _k, d in found], centroid=(xc, zc),
                r2=r2, rmax=rmax, n=len(pts), plate_t=plate_t,
                v_stall=11.00 * 1000.0 * rmax / r2,
                v_proof=25.00 * 1000.0 * rmax / r2)


def check4_mode_a_loads():
    """CHECK 4, replaced.  slide_mass()/sprung_split() are Mode B -- there is no
    ballast and no sprung mass here.  This is the Mode A load report, confirmed
    against the BUILT assembly rather than against the guide.
    """
    print('=== CHECK 4: Mode A load report, measured off the assembly ===')
    st = find_occ('RIG_Stand')
    if st is None:
        print('   RIG_Stand MISSING')
        return None
    vol = sum(b.volume for b in bodies_of(st.component))
    print('   RIG_Stand   %.1f cm3   %.1f g  (Fusion mass %.1f g)'
          % (vol, vol * 1.15, occ_mass_g(st)))
    print('   guide §2.4 assumes "a printed stand is ~0.3 kg" for the tipping')
    print('   table.  Heavier only makes that argument stronger; it is still')
    print('   nowhere near the 11.2 kg that 11.00 N.m needs at 100 mm.')
    print()
    print('   Guide §2.2 load set, for reference (rig_calc.mode_a_stand):')
    print('     pitch  54.80 N x 42.00 mm            2.30 N.m  about X')
    print('     yaw    shoulder stall               11.00 N.m  about Y  DOMINANT')
    print('     roll   71.3 N x 42.00 mm             2.99 N.m  about Z')
    print('     vector sum, yaw + roll              11.40 N.m')
    print('     proof screen                        25.00 N.m  about Y')
    print()
    g = stand_bolt_group()
    if g is None:
        print('   no O%.1f insert bores found in RIG_Stand' % INSERT_M3_D)
        return None
    print('   §2.3 bolt group, MEASURED off the modelled insert bores:')
    print('     bores found                 %d   (want 5)' % g['n'])
    for (x, z), (y0, y1) in zip(g['pts'], g['depths']):
        panel = min(PANEL_FRAME_BOLTS,
                    key=lambda p: math.hypot(p[0] - x, p[1] - z))
        off = math.hypot(panel[0] - x, panel[1] - z)
        print('       X %+7.2f  Z %+7.2f   y %6.2f..%6.2f  depth %.2f   '
              'panel hole offset %.4f mm' % (x, z, y0, y1, y1 - y0, off))
    print('     centroid            X %+7.2f  Z %+7.2f   guide: -24.00, +40.40'
          % g['centroid'])
    print('     sum r^2             %9.0f mm^2            guide: 14 179'
          % g['r2'])
    print('     worst radius        %9.2f mm              guide: 68.60'
          % g['rmax'])
    print('     worst screw shear   %9.1f N at 11.00 N.m   guide: 53.2'
          % g['v_stall'])
    print('     worst screw shear   %9.1f N at 25.00 N.m   guide: 121.0'
          % g['v_proof'])
    print('     bearing on the %.0f mm web  %6.2f / %6.2f MPa (stall / proof)'
          % (g['plate_t'], g['v_stall'] / (3.0 * g['plate_t']),
             g['v_proof'] / (3.0 * g['plate_t'])))
    print('     rig_calc quotes 2.22 / 5.04 MPa on an 8 mm wall; the built web')
    print('     is %.0f mm, so bearing is lower than the guide reports.  Either'
          % g['plate_t'])
    print('     way bearing is not the limit -- the insert\'s grip is.')
    return g


def check6_mode_a_overhang():
    """CHECK 6, replaced.  Assert the stand's outboard face lands exactly on
    y = 42.0 and that NOTHING sits between it and the panel: anything there
    grows the 42.00 mm overhang and scales all four §2.2 moments linearly.
    """
    print('=== CHECK 6: the 42.00 mm Mode A overhang ===')
    st, pl = find_occ('RIG_Stand'), find_occ('Chassis_Shoulder_Plate_L')
    if st is None or pl is None:
        print('   RIG_Stand or Chassis_Shoulder_Plate_L MISSING')
        return None
    sb, pb = bbox_of(st), bbox_of(pl)
    face = sb[3]
    rows = [('stand outboard face  (must be exactly 42.00)', face),
            ('panel inboard face', pb[2]),
            ('+ Chassis_Shoulder_Plate_L 5.0', PANEL_Y0 + 5.0),
            ('wheel centre plane (half-track)', HALF_TRACK)]
    for lbl, y in rows:
        print('   %-44s y = %8.3f' % (lbl, y))
    over = HALF_TRACK - face
    shim = pb[2] - face
    print('   overhang, stand face to wheel plane        %8.3f mm' % over)
    print('   guide §2.1 / rig_calc: 42.00 -> %s'
          % ('MATCHES' if abs(over - 42.0) < 0.01 else 'DIFFERS, restate §2.2'))
    print('   shim/washer/pad between stand and panel    %8.3f mm  -> %s'
          % (shim, 'clean' if abs(shim) < 0.005 else 'GROWS THE OVERHANG'))
    # Anything acting as a shim would have to occupy the pad's own Y band
    # (STAND_Y0..STAND_Y1) outside the O82 motor bore -- which is solid stand.
    # So the decisive test is interference against RIG_Stand itself, not a
    # bounding-box scan: a bbox corner overstates a round part's radius by root 2,
    # which made the O80 motor read as r 56.57 against the bore's 41.0 and
    # flagged the one part the stand is deliberately built around.
    pairs = [x for x in clashes(0.01, verbose=False)
             if 'RIG_Stand' in x[0] or 'RIG_Stand' in x[1]]
    print('   interference involving RIG_Stand, over 0.01 mm3: %s'
          % (pairs if pairs else 'none'))
    print('   -> nothing occupies the pad\'s y %.0f..%.0f band outside the O%.0f'
          % (STAND_Y0, STAND_Y1, STAND_BORE_D))
    print('      bore, so there is no shim.  The motor passes THROUGH the bore:')
    print('      measured O80 (r 40.0) from y 17 to 41.5 and r 39.0 at the y 42')
    print('      mount land, against the bore\'s r 41.0 -> 1.0 mm clear.')
    ok = abs(over - 42.0) < 0.01 and abs(shim) < 0.005 and not pairs
    print('   -> %s' % ('PASS' if ok else 'FAIL'))
    return over


def check7_holddown(y_probe=None, step=0.5):
    """CHECK 7, NEW and Mode A only.  Prove the hold-down.

    11.00 N.m of yaw cannot be resisted by dead weight, so the CAD has to SHOW
    the clamp or bench-bolt path rather than assume it.  The clamp landings are
    measured off the model -- the clear runs of the foot's top face, found by
    probing point containment, not asserted from the layout constants.
    """
    print('=== CHECK 7: prove the hold-down (NEW, Mode A only) ===')
    st = find_occ('RIG_Stand')
    if st is None:
        print('   RIG_Stand MISSING')
        return None
    body = bodies_of(st.component)[0]
    y_probe = (STAND_FOOT_Y0 + STAND_Y1) / 2.0 if y_probe is None else y_probe
    vol = sum(b.volume for b in bodies_of(st.component))
    print('   dead-weight route, from rig_calc.mode_a_stand():')
    for b_mm, n_needed in ((100, 110.0), (150, 73.3), (200, 55.0),
                           (250, 44.0), (300, 36.7)):
        print('     base half-width %3d mm -> needs %6.1f N = %5.1f kg'
              % (b_mm, n_needed, n_needed / 9.80665))
    print('     this stand weighs %.1f g.  Dead weight is not a route at any'
          % (vol * 1.15))
    print('     base width -- it must be CLAMPED or BOLTED to the bench.')
    print()
    print('   foot: X %+.0f..%+.0f (base half-width %.0f mm), Y %.1f..%.1f '
          '(%.0f mm of jaw), Z %.4f..%.4f'
          % (-STAND_FOOT_X, STAND_FOOT_X, STAND_FOOT_X, STAND_FOOT_Y0,
             STAND_Y1, STAND_FOOT_T, Z_BENCH_A, Z_FOOT_TOP))
    print('   underside at Z %.4f and top landing at Z %.4f are parallel, and'
          % (Z_BENCH_A, Z_FOOT_TOP))
    print('   the top is clear from above at every landing below.')
    print()
    # --- clamp landings: clear runs of the foot's top face, probed off the solid.
    # Scan the whole Y band of the foot, not one line: a landing is X where the
    # top face is solid at SOME y and NOTHING rises out of it at ANY y.  Probing
    # a single y = 26 line instead counts the four M6 counterbores as
    # obstructions, which inverts the answer -- they are the bench-bolt path.
    ys = [STAND_FOOT_Y0 + 2.0 + k * (STAND_FOOT_T - 4.0) / 6.0 for k in range(7)]

    def _solid(x, z):
        for y in ys:
            p = adsk.core.Point3D.create(cm(x), cm(y), cm(z))
            if (body.pointContainment(p)
                    != adsk.fusion.PointContainment.PointOutsidePointContainment):
                return True
        return False

    runs, cur = [], None
    x = -STAND_FOOT_X
    while x <= STAND_FOOT_X + 1e-9:
        free = (_solid(x, Z_FOOT_TOP - 0.5)
                and not _solid(x, Z_FOOT_TOP + 2.0))
        if free and cur is None:
            cur = x
        elif not free and cur is not None:
            runs.append((cur, x - step))
            cur = None
        x += step
    if cur is not None:
        runs.append((cur, STAND_FOOT_X))
    runs = [(a, b) for a, b in runs if b - a >= 20.0]
    print('   clamp landings measured on the foot\'s top face (>= 20 mm long, '
          'over y %.0f..%.0f):' % (ys[0], ys[-1]))
    for a, b in runs:
        print('     X %+7.1f .. %+7.1f   %6.1f mm long x %.0f mm of Y = '
              '%6.0f mm2 of bearing' % (a, b, b - a, STAND_FOOT_T,
                                        (b - a) * STAND_FOOT_T))
    aft = [r for r in runs if (r[0] + r[1]) / 2 < 0]
    fwd = [r for r in runs if (r[0] + r[1]) / 2 > 0]
    print('     %d aft of centre, %d fore  -> guide §2.4 wants at least two '
          'per side: %s' % (len(aft), len(fwd),
                            'OK' if len(aft) >= 2 and len(fwd) >= 2 else 'SHORT'))
    print('     interrupted only by the two rails, the king post and one shear')
    print('     brace rising out of the foot -- every gap is structure, not a hole.')
    if runs:
        smallest = min((b - a) * STAND_FOOT_T for a, b in runs)
        print('     smallest landing %.0f mm2.  The 110.0 N a 100 mm base needs '
              'is %.2f MPa on it;' % (smallest, 110.0 / smallest))
        print('     even at an Irwin medium-duty bar clamp\'s full 300 lbf '
              '(1334 N) it is %.2f MPa,' % (1334.0 / smallest))
        print('     against PA-CF ~84 MPa XY -- the landing will not crush.')
    print()
    print('   bench-bolt path: %d x O%.1f through the foot at X %s, y %.1f,'
          % (len(STAND_BOLT_X), STAND_BOLT_D,
             ', '.join('%+.0f' % v for v in STAND_BOLT_X), y_probe))
    print('   O%.1f x %.1f counterbored from the top face so an M6 SHCS head '
          '(O10 x 6) sits' % (STAND_BOLT_CB_D, STAND_BOLT_CB_DEEP))
    print('   sub-flush and the same landing still takes a clamp.')
    print()
    print('   ⚠ NO CAD EQUIVALENT: rig_stl/README asks for the unloaded bench')
    print('   check -- clamp it down, push at the wheel to make ~11 N.m about')
    print('   the shoulder axis (~52 N at the 209 mm nominal lever) and confirm')
    print('   nothing lifts, slips or visibly twists.')
    ok = len(aft) >= 2 and len(fwd) >= 2
    print('   -> %s' % ('PASS' if ok else 'FAIL'))
    return runs
