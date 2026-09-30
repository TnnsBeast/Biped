"""R2A all-printed, unpowered proof-of-concept (POC) stand-ins.  Fusion MCP only.

Run with `Beni_R2A_SingleLeg` active.  Every entry point that can change the
model calls `r2a_lib.assert_r2a_doc()` first.  The POC reuses the released R2A
article parts unchanged and adds `POC_*` components that share space with the
purchased parts they replace (the `ABS_TEST_*` precedent in
mechanical_spring_test_fusion.py).  Two configurations exist in one document:

  article : every part except POC_*            (the released R2A article)
  poc     : every part except NOT_IN_POC        (owned hardware + prints only)

Stand-ins (all ABS, hand-driven, no load; CLAUDE.md rule 7):
  * mock knee GIM6010-8: stator on the real mount face and Ø74 PCD with M3
    inserts; rotor with the real output interface (6 x M3 inserts on Ø25 PCD,
    three owned Ø4 x 10 dowels as the Ø4 factory pins, 3.5 mm proud); a plain
    printed journal; a knob with a θc pointer over a dial and a lock pin;
  * one-piece printed pushrod inside the modelled rod-end / jam-nut / rod
    envelope, 120.0 mm pin to pin;
  * printed Ø5 clevis-pin stand-ins, 18 mm, retained like the dowels they
    replace (float between the cheek faces);
  * printed plain bushings in the released 6800 seats;
  * printed 2.0 mm washers so the owned M2.5 x 12 engage the wheel motor
    exactly as the article's M2.5 x 10;
  * a knee protractor on the (held) encoder-bracket inserts, read against the
    encoder arm tip; a Ø110 tyre gauge ring on the no-tyre shell; a feeler.

Numbers carry their source in the comment beside them.  DESIGN CHOICE marks a
value chosen here and confirmed only by the POC coupons.

Results are CAD evidence only; none of this is a physical result.
"""
import hashlib
import json
import math
import os
import time

import adsk.core
import adsk.fusion

import beni_lib as B
import rig_lib as R
import r2a_lib as L
import r2a_paths_fusion as RP
import r2a_release_fusion as RF
import mechanical_release_audit_fusion as A
import stl_release as S

ROOT = os.path.dirname(os.path.realpath(__file__))
OUT_DIR = os.path.join(ROOT, 'r2a_poc_stl')
EVIDENCE = os.path.join(ROOT, 'evidence', 'r2a', '2026-09-28_poc')
BASELINE = os.path.join(ROOT, 'r2a_poc_release_baseline.json')
VERIFIED_SOURCES = ['r2a_poc_fusion.py', 'r2a_lib.py', 'r2a_release_fusion.py',
                    'r2a_paths_fusion.py', 'stl_release.py']
LOCK = '/tmp/r2a_poc.lock'

# ============================================================== names
HOUSING = 'POC_Knee_Actuator_Mock_Housing_L'
ROTOR = 'POC_Knee_Actuator_Mock_Rotor_L'
KNOB = 'POC_Knee_Actuator_Mock_Knob_L'
LOCK_PIN = 'POC_Knob_Lock_Pin'
ROTOR_DOWELS = 'POC_DowelPin_D4x10_Rotor'        # owned steel, not printed
KEY_DOWEL = 'POC_DowelPin_D4x10_KnobKey'         # owned steel, not printed
PUSHROD = 'POC_Pushrod_L'
PIN_CRANK = 'POC_Clevis_Pin_Crank'
PIN_LEVER = 'POC_Clevis_Pin_Lever'
BUSHING = 'POC_Knee_Bushing'
WASHER = 'POC_Washer_M2p5_WheelMotor'
PROTRACTOR = 'POC_Knee_Protractor_L'
GAUGE = 'POC_Tyre_Gauge_Ring'
THRUST = 'POC_Eye_Thrust_Washer'
SCREW_M25 = 'POC_SHCS_M2p5x12'                   # owned M2.5 x 12
SCREW_M3 = 'POC_SHCS_M3x10'                      # owned M3 x 10
SET_M25 = 'POC_SHCS_M2p5x12_WheelMotor'
SET_KNOB = 'POC_SHCS_M3x10_Knob'
SET_PROT = 'POC_SHCS_M3x10_Protractor'

# Purchased (or held) parts that the POC configuration leaves out.  The knee
# REF is identified by occurrence (L.knee_ref()), because the shoulder unit is
# the same STEP component and stays in.
NOT_IN_POC = ('HW_RodEnd_M5_Upper', 'HW_RodEnd_M5_Lower', 'HW_Rod_M5x86',
              'HW_JamNut_M5', 'HW_Pin_D5x18_Crank', 'HW_Pin_D5x18_Lever',
              'HW_Bearing_6800', 'R2A_Encoder_Bracket_L', 'HW_AS5048A_PCB',
              'HW_Magnet_D6x2p5_Diametric', 'REFERENCE_Cable_Encoder',
              'REFERENCE_Cable_Knee_Actuator', 'Wheel_Rim_L', 'Wheel_Tyre_L')
NOT_IN_POC_SETS = ('R2A_SHCS_M2p5x10_WheelMotor', 'R2A_SHCS_M3x16_Bracket')
# The lock pin is a loose accessory: it is fitted only while a check point is
# held, and the knob cannot turn with it in, so it is kept out of the sweep and
# checked by its own insertion path at each check point (lock_paths()).
SWEEP_EXCLUDE = (LOCK_PIN,)

# ======================================================= mock actuator
# Interface datums are the real actuator's (design record §2.1, placed by
# r2a_lib): mount face y 91.1, output face y 87.6, pin tips y 84.1, Ø80
# housing to y 116.1, Ø57 cover to y 128.1.
MOUNT_Y = L.ACT_MOUNT_Y                 # 91.1
OUT_Y = L.ACT_OUT_Y                     # 87.6
PIN_TIP_Y = L.ACT_PIN_TIP_Y             # 84.1
HOUSING_Y1 = L.ACT_HOUSING_Y[1]         # 116.1
COVER_Y1 = L.ACT_COVER_Y[1]             # 128.1
HOUSING_D = 80.0                        # §2.1
# Insert receivers: the owner-selected Ø4.5 x 6.0 M3 x 5 pocket (evidence/
# inserts/2026-09-14).  At R37 a Ø4.5 pocket leaves 0.75 mm of wall inside Ø80
# and breaks out of the Ø78 land, so each used position gets a Ø9.0 boss (the
# released inboard half's perimeter insert-boss diameter), 1.5 mm proud of Ø80
# over y 91.1..97.6.  Only the five positions the outboard half uses get one.
INSERT_D = B.M3_INSERT_RECEIVER_D       # 4.5
INSERT_DEPTH = B.FRAME_INSERT_HOLE_DEPTH  # 6.0
INSERT_BOSS_D = 9.0                     # = r2a_lib inboard-half perimeter bosses
INSERT_BOSS_Y1 = MOUNT_Y + 6.5          # 97.6: pocket floor + 0.5
# Rotor and journal.  DESIGN CHOICE - COUPON: 0.60 mm diametral printed
# running clearance (holes print under nominal: Ø19.15 light-presses a Ø19.00
# bearing, Ø10.25 firm-thumb-presses a Ø10.00 pin; the printed-shaft side is
# uncharacterised, so the allowance covers both).
DISC_D = 46.0                           # real rotating-face Ø46 (§2.1)
DISC_Y1 = MOUNT_Y - 0.1                 # 91.0: 0.1 thrust gap, DESIGN CHOICE
JOURNAL_D = 36.0                        # DESIGN CHOICE: clears the Ø25-PCD pockets
JOURNAL_BORE_D = 36.6                   # DESIGN CHOICE - COUPON
SHAFT_Y1 = HOUSING_Y1 + 0.1             # 116.2: 0.1 thrust gap under the knob
BORE_CHAMFER = 0.5                      # entry chamfer at the housing bed face
PILOT_D, PILOT_Y1 = 16.0, SHAFT_Y1 + 3.0     # knob centring spigot
PILOT_BORE_D = 16.6                     # same 0.60 allowance as the journal
KNOB_D = 56.0                           # inside the real Ø57 driver cover
KNOB_Y1 = 128.0                         # 0.1 inside the real y 128.1
KNOB_POCKET_DEPTH = 7.0                 # knob-screw insert pocket from the pilot top
KEY_R = 11.0                            # knob key dowel radius
KEY_SOCKET_D = L.DOWEL_HOLE_D           # 4.25: owner Ø4 x 10 press selection
KEY_SOCKET_DEPTH = 5.0                  # hub retained-socket depth
KEY_SLIP_D = B.ROOT_DOWEL_LINK_SOCKET_D  # 4.30: PINREV2 slip holes
KNOB_SCREW_SEAT_Y = 124.9               # counterbore floor; M3 x 10 engages 4.3
KNOB_CBORE_D = 6.2                      # = crank counterbores
# Output interface on the rotor (build_crank's pattern = the knee REF output)
OUT_SCREW_A = [10.8 + 60.0 * i for i in range(6)]
OUT_PIN_A = [41.0 + 120.0 * i for i in range(3)]
OUT_INSERT_DEPTH = INSERT_DEPTH          # 6.0: M3 x 10 tip 1.0 above the floor
DOWEL_SOCKET_DEPTH = L.DOWEL_LEN - (OUT_Y - PIN_TIP_Y)   # 6.5: 3.5 mm proud
DOWEL_CHAMFER = 0.4                     # DESIGN CHOICE: bed-opening sockets
# Dial.  θc is read at the pointer against ticks on the housing's outboard
# face; seven lock holes sit at the θc of the check-point knee angles.
POINTER_A = L.crank_arm_xz()            # XZ angle of the crank arm at build
LOCK_R, LOCK_HOLE_D, LOCK_DEPTH = 31.0, KEY_SLIP_D, 5.0
LOCK_PIN_D = 3.8                        # DESIGN CHOICE (0.5 in the Ø4.30 holes)
# Check points: >= 5 (guide check b), holes >= 10.7 deg of crank apart so a
# 1.5 mm wall stays between Ø4.30 holes at R31.  A seven-point set (adding
# 65 and 140 deg) put holes 9.0 and 4.5 deg apart; rejected.
CHECK_ALPHAS = (55.0, 80.0, 100.0, 120.0, 145.0)
BOSS_D = 7.2
BLADE = (34.0, 39.5, 1.6)               # pointer blade r0, r1, width
TICK_R = (35.0, 37.0, 39.3)             # long start, short start, end
TICK_W, TICK_DEPTH = 0.8, 0.6
STOP_NOTCH = (1.0, 108.1)               # side notches at the stop θc: width, y0

# ============================================================== pushrod
# Inside the modelled envelope (r2a_lib RE_* / NUT_* / ROD_*).  The whole
# pushrod is 5.0 mm thick, the Y extent of the Ø5 rod (y 73.0..78.0), so its
# faces stay 2.8 mm from the clevis neck-relief floor/ceiling (y 70.2 / 80.8)
# exactly like the article rod.  A first version 8.0 mm thick (the ball width)
# came within 1.30 mm of the crank's relief ceiling at the extension stop and
# 2.46 mm of the lever relief floor at the flexion stop (rectangle corners
# outside the round nut envelope), so it was rejected in favour of this one.
# Two printed Ø11 x 1.5 thrust washers per eye take up the ball width: Ø11 x 8.0
# = the modelled ball, 0.2 mm float each side in the 8.4 gap.
ROD_Y = (L.Y_ROD - L.ROD_D / 2.0, L.Y_ROD + L.ROD_D / 2.0)   # 73.0 .. 78.0
EYE_D = L.RE_EYE_D                                 # 18.0 (housing Ø18 x 6.0)
NECK_W, NECK_L = L.RE_NECK_D, L.RE_H + L.NUT_T     # 9.0, 29.7
ROD_W = L.ROD_D                                    # 5.0
EYE_BORE_D = L.PIN5_HOLE_D                         # 5.15: same hole as the ears
THRUST_D = L.RE_BALL_D                             # 11.0 = modelled ball
THRUST_Y = ((L.GAP[0] + 0.2, ROD_Y[0]), (ROD_Y[1], L.GAP[1] - 0.2))  # 71.5..73.0, 78.0..79.5
# ============================================================ clevis pins
PIN_D = 4.75                            # DESIGN CHOICE - COUPON (Ø5.15 holes)
PIN_LEN = L.PIN5_LEN                    # 18.0: keeps the 2.7 mm engagement
PIN_CHAMFER = 0.4
PIN_Y = (0.5 * (L.Y_CH0 + L.Y_CH1) - PIN_LEN / 2.0,
         0.5 * (L.Y_CH0 + L.Y_CH1) + PIN_LEN / 2.0)   # 65.5 .. 83.5 (article)
# ============================================================== bushings
BUSH_OD = 18.90                          # DESIGN CHOICE - COUPON (Ø19.15 seat)
BUSH_ID = 10.60                          # DESIGN CHOICE - COUPON: +0.30 over the
                                         # Ø10.30 firm-thumb receiver
BUSH_CHAMFER = 0.3
# =============================================================== washers
WASHER_T = 2.0      # M2.5 x 12 through 8.0 plate + 2.0 = the article x 10 stack
WASHER_OD, WASHER_ID = 5.6, 2.9
# ============================================================ protractor
PROT_Y = (L.Y_OUT, L.Y_OUT + 6.0)       # 91.1 .. 97.1 on the outboard face
PROT_POSTS = L.enc_insert_xz()          # the held bracket's two inserts
PROT_RING = (40.0, 50.0)                # encoder-arm tip reaches R39.0
PROT_SECTOR = (10.5, 40.0, 152.0)       # r0, XZ a0, a1 (clear of the arm sweep)
PROT_TICK = (39.5, 42.0, 44.0, 46.0)    # start, short end, long end, stop end
DIGIT = (2.6, 4.0, 0.8, 0.9)            # width, height, stroke, gap
PROT_NUM_R = 47.2
ARM_TIP_REL = L.ENC_ARM_REL             # arm centreline at du + 15 deg
# ============================================================ tyre gauge
TYRE_D = B.WHEEL_OD                     # Ø110 at the tyre centre plane
GAUGE_Y = (B.WHEEL_Y0, B.RIM_WEB_Y_B)   # 69.0 .. 104.5 (tyre edge .. drum end)
GAUGE_LIP_T = 1.5
GAUGE_BORE_D = 96.4                     # DESIGN CHOICE - COUPON on the Ø96 drum
GAUGE_LIP_D = 89.0                      # lip on the drum end face r 44.5..48
FEELER = (4.0, 5.0)                     # go steps; design rule >= 5 mm


# ============================================================ small helpers
def _tm():
    return adsk.fusion.TemporaryBRepManager.get()


def _P(x, y, z):
    return adsk.core.Point3D.create(x / 10.0, y / 10.0, z / 10.0)


def ycyl(xz, y0, y1, d):
    return _tm().createCylinderOrCone(_P(xz[0], y0, xz[1]), d / 20.0,
                                      _P(xz[0], y1, xz[1]), d / 20.0)


def ycone(xz, y0, d0, y1, d1):
    return _tm().createCylinderOrCone(_P(xz[0], y0, xz[1]), d0 / 20.0,
                                      _P(xz[0], y1, xz[1]), d1 / 20.0)


def xzbox(c, ang, length, width, y0, y1):
    """Box centred at XZ point c: `length` along XZ angle ang, `width`
    perpendicular in XZ, from y0 to y1."""
    a = math.radians(ang)
    obb = adsk.core.OrientedBoundingBox3D.create(
        _P(c[0], 0.5 * (y0 + y1), c[1]),
        adsk.core.Vector3D.create(math.cos(a), 0, math.sin(a)),
        adsk.core.Vector3D.create(0, 1, 0), length / 10.0, (y1 - y0) / 10.0,
        width / 10.0)
    return _tm().createBox(obb)


def radial_box(c, ang, r0, r1, width, y0, y1):
    m = L.polar(c, 0.5 * (r0 + r1), ang)
    return xzbox(m, ang, r1 - r0, width, y0, y1)


def halfspace(c, ang, left, y0, y1, big=600.0):
    """Everything on the left (CCW) side of the ray from c at ang, or right."""
    n = ang + (90.0 if left else -90.0)
    return xzbox(L.polar(c, big / 2.0, n), ang, big * 2, big, y0, y1)


def _bool(a, b, kind):
    t = {'cut': adsk.fusion.BooleanTypes.DifferenceBooleanType,
         'join': adsk.fusion.BooleanTypes.UnionBooleanType,
         'inter': adsk.fusion.BooleanTypes.IntersectionBooleanType}[kind]
    if not _tm().booleanOperation(a, b, t):
        raise RuntimeError('temporary boolean failed: ' + kind)
    return a


def join(a, *bs):
    for b in bs:
        _bool(a, b, 'join')
    return a


def cut(a, *bs):
    for b in bs:
        _bool(a, b, 'cut')
    return a


def _check_body(body, name, lumps=1):
    if not body.isSolid or body.lumps.count != lumps:
        raise RuntimeError('%s: solid %s, %d lumps (want %d)'
                           % (name, body.isSolid, body.lumps.count, lumps))
    return body


SEGS = {'a': (0, 1, 1 - 0.2, 1), 'd': (0, 1, 0, 0.2), 'g': (0, 1, 0.4, 0.6),
        'f': (0, 0.31, 0.5, 1), 'b': (0.69, 1, 0.5, 1),
        'e': (0, 0.31, 0, 0.5), 'c': (0.69, 1, 0, 0.5)}
DIGITS = {'0': 'abcdef', '1': 'bc', '2': 'abged', '3': 'abgcd', '4': 'fgbc',
          '5': 'afgcd', '6': 'afgedc', '7': 'abc', '8': 'abcdefg', '9': 'abcdfg'}


def numeral_tools(text, centre, phi, y0, y1, digit=DIGIT):
    """Seven-segment engraving tools for `text`, tops pointing radially out
    from `centre` at XZ angle phi, reading correctly from outboard (+Y)."""
    w, h, s, gap = digit
    up = (math.cos(math.radians(phi)), math.sin(math.radians(phi)))
    right = (-up[1], up[0])            # right x up = +Y: not mirrored from +Y
    tot = len(text) * w + (len(text) - 1) * gap
    out = []
    for i, ch in enumerate(text):
        x_left = -tot / 2.0 + i * (w + gap)
        for seg in DIGITS[ch]:
            fx0, fx1, fy0, fy1 = SEGS[seg]
            x0, x1 = x_left + fx0 * w, x_left + fx1 * w
            yy0, yy1 = fy0 * h - h / 2.0, fy1 * h - h / 2.0
            if seg in 'adg':           # horizontal strokes: stroke-high
                ym = 0.5 * (yy0 + yy1)
                yy0, yy1 = ym - s / 2.0, ym + s / 2.0
            else:                      # vertical strokes: stroke-wide
                xm = x0 + s / 2.0 if fx0 == 0 else x1 - s / 2.0
                x0, x1 = xm - s / 2.0, xm + s / 2.0
            xc, yc = 0.5 * (x0 + x1), 0.5 * (yy0 + yy1)
            px = centre[0] + xc * right[0] + yc * up[0]
            pz = centre[1] + xc * right[1] + yc * up[1]
            ang = math.degrees(math.atan2(right[1], right[0]))
            out.append(xzbox((px, pz), ang, x1 - x0, yy1 - yy0, y0, y1))
    return out


def _add(name, body, cls, material=None):
    """Replace component `name` with one base-feature body (r2a_lib pattern)."""
    return L._base_comp(name, body, cls, material)


def _occs_named(name):
    return [o for o in L.all_root_occs() if B.base_name(o.component.name) == name]


def _set_occs(label):
    return [o for o in L.all_root_occs()
            if o.attributes.itemByName('POC', 'set') and
            o.attributes.itemByName('POC', 'set').value == label]


# ===================================================== part geometry (TBM)
def housing_body():
    # Ø80 from the mount face.  The real actuator has a Ø78 land over the first
    # 1.0 mm (§2.1); reproducing it left either a 1.0 mm ledge broken by the
    # bosses (a support face in the bed pose) or a 45 deg cone whose
    # intersection with the bosses tessellates 0.0001 mm off the B-Rep and
    # fails mesh_fidelity().  The nearest other part, a perimeter screw head,
    # is 2.86 mm from the mock (at a boss; evidence poc_measurements.json).
    b = join(ycyl((0, 0), MOUNT_Y, HOUSING_Y1, HOUSING_D),
             *[ycyl(p, MOUNT_Y, INSERT_BOSS_Y1, INSERT_BOSS_D) for p in act_xz()])
    cut(b, ycyl((0, 0), MOUNT_Y - 1.0, HOUSING_Y1 + 1.0, JOURNAL_BORE_D),
        ycone((0, 0), MOUNT_Y - 1.0, JOURNAL_BORE_D + 2 * (BORE_CHAMFER + 1.0),
              MOUNT_Y + BORE_CHAMFER, JOURNAL_BORE_D))
    for p in act_xz():
        cut(b, ycyl(p, MOUNT_Y - 1.0, MOUNT_Y + INSERT_DEPTH, INSERT_D))
    for a in CHECK_ALPHAS:
        cut(b, ycyl(lock_xz(a), HOUSING_Y1 - LOCK_DEPTH, HOUSING_Y1 + 1.0, LOCK_HOLE_D))
    for th in range(40, 141, 5):
        r0 = TICK_R[0] if th % 10 == 0 else TICK_R[1]
        cut(b, radial_box((0, 0), th - 40.0, r0, TICK_R[2], TICK_W,
                          HOUSING_Y1 - TICK_DEPTH, HOUSING_Y1 + 1.0))
    for a in (L.ALPHA_FLEX_STOP, L.ALPHA_EXT_STOP):
        cut(b, radial_box((0, 0), L.solve(a)[2] - 40.0, HOUSING_D / 2.0 - 0.8,
                          HOUSING_D / 2.0 + 1.0, STOP_NOTCH[0], STOP_NOTCH[1],
                          HOUSING_Y1 + 1.0))
    return _check_body(b, HOUSING)


def act_xz():
    return [L.suv(L.ACT_PCD / 2.0, a) for a in L.ACT_SCREW_UV]


def lock_xz(alpha):
    return L.polar((0, 0), LOCK_R, L.solve(alpha)[2] - 40.0)


def rotor_body():
    b = join(ycyl((0, 0), OUT_Y, DISC_Y1, DISC_D),
             ycyl((0, 0), DISC_Y1 - 0.2, SHAFT_Y1, JOURNAL_D),
             ycyl((0, 0), SHAFT_Y1 - 0.2, PILOT_Y1, PILOT_D))
    for a in OUT_SCREW_A:
        cut(b, ycyl(L.polar((0, 0), B.SH_OUT_PCD / 2.0, a), OUT_Y - 1.0,
                    OUT_Y + OUT_INSERT_DEPTH, INSERT_D))
    for a in OUT_PIN_A:
        p = L.polar((0, 0), B.SH_PIN_PCD / 2.0, a)
        cut(b, ycyl(p, OUT_Y - 1.0, OUT_Y + DOWEL_SOCKET_DEPTH, KEY_SOCKET_D),
            ycone(p, OUT_Y - 1.0, KEY_SOCKET_D + 2 * (DOWEL_CHAMFER + 1.0),
                  OUT_Y + DOWEL_CHAMFER, KEY_SOCKET_D))
    cut(b, ycyl((0, 0), PILOT_Y1 - KNOB_POCKET_DEPTH, PILOT_Y1 + 1.0, INSERT_D),
        ycyl(key_xz(), SHAFT_Y1 - KEY_SOCKET_DEPTH, SHAFT_Y1 + 1.0, KEY_SOCKET_D))
    # crank-clocking witness notch, opposite the crank arm, on the disc rim
    notch = L.polar((0, 0), DISC_D / 2.0, POINTER_A + 180.0)
    cut(b, xzbox(notch, POINTER_A + 180.0 + 45.0, 1.4, 1.4, OUT_Y - 1.0, DISC_Y1 + 0.5))
    return _check_body(b, ROTOR)


def key_xz():
    return L.polar((0, 0), KEY_R, POINTER_A + 180.0)


def knob_body():
    ptr = L.polar((0, 0), LOCK_R, POINTER_A)
    b = join(ycyl((0, 0), SHAFT_Y1, KNOB_Y1, KNOB_D),
             ycyl(ptr, SHAFT_Y1, KNOB_Y1, BOSS_D),
             radial_box((0, 0), POINTER_A, LOCK_R, BLADE[1], BLADE[2], SHAFT_Y1, KNOB_Y1))
    cut(b, ycyl((0, 0), SHAFT_Y1 - 1.0, PILOT_Y1 + 0.3, PILOT_BORE_D),
        ycyl(key_xz(), SHAFT_Y1 - 1.0, SHAFT_Y1 + L.DOWEL_LEN - KEY_SOCKET_DEPTH + 0.5,
             KEY_SLIP_D),
        ycyl((0, 0), PILOT_Y1, KNOB_Y1 + 1.0, 3.4),
        ycyl((0, 0), KNOB_SCREW_SEAT_Y, KNOB_Y1 + 1.0, KNOB_CBORE_D),
        ycyl(ptr, SHAFT_Y1 - 1.0, KNOB_Y1 + 1.0, LOCK_HOLE_D))
    return _check_body(b, KNOB)


def lock_pin_body():
    p = L.polar((0, 0), LOCK_R, POINTER_A)          # installed at the build pose
    y0 = HOUSING_Y1 - LOCK_DEPTH + 0.5
    b = join(ycone(p, y0, LOCK_PIN_D - 0.8, y0 + 0.4, LOCK_PIN_D),
             ycyl(p, y0 + 0.4, KNOB_Y1, LOCK_PIN_D),
             ycyl(p, KNOB_Y1, KNOB_Y1 + 2.5, 8.0))
    return _check_body(b, LOCK_PIN)


def pushrod_body():
    c, p = L.C0, L.P0
    ang = math.degrees(math.atan2(p[1] - c[1], p[0] - c[0]))
    ln = math.hypot(p[0] - c[0], p[1] - c[1])
    y0, y1 = ROD_Y
    u = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
    b = join(ycyl(c, y0, y1, EYE_D), ycyl(p, y0, y1, EYE_D),
             xzbox((c[0] + u[0] * NECK_L / 2, c[1] + u[1] * NECK_L / 2), ang, NECK_L,
                   NECK_W, y0, y1),
             xzbox((p[0] - u[0] * NECK_L / 2, p[1] - u[1] * NECK_L / 2), ang, NECK_L,
                   NECK_W, y0, y1),
             xzbox((0.5 * (c[0] + p[0]), 0.5 * (c[1] + p[1])), ang, ln - 2 * NECK_L + 2.0,
                   ROD_W, y0, y1))
    cut(b, ycyl(c, y0 - 1, y1 + 1, EYE_BORE_D), ycyl(p, y0 - 1, y1 + 1, EYE_BORE_D))
    return _check_body(b, PUSHROD)


def pin_body(xz):
    y0, y1 = PIN_Y
    c = PIN_CHAMFER
    b = join(ycone(xz, y0, PIN_D - 2 * c, y0 + c, PIN_D),
             ycyl(xz, y0 + c, y1 - c, PIN_D),
             ycone(xz, y1 - c, PIN_D, y1, PIN_D - 2 * c))
    return _check_body(b, 'pin')


def bushing_body(y0):
    y1 = y0 + B.KNEE_BRG_W
    c = BUSH_CHAMFER
    k = (L.KX, L.KZ)
    b = ycyl(k, y0, y1, BUSH_OD)
    cut(b, ycyl(k, y0 - 1, y1 + 1, BUSH_ID))
    for yf, s in ((y0, 1.0), (y1, -1.0)):          # face, inward direction
        # bore chamfer: 45 deg cone, Ø(ID + 2c) at the face
        cut(b, ycone(k, yf - s * 1.0, BUSH_ID + 2 * (c + 1.0), yf + s * (c + 0.5),
                     BUSH_ID - 1.0))
        # outer chamfer: everything outside a 45 deg cone, Ø(OD - 2c) at the face
        ring = ycyl(k, yf - s * 1.0, yf + s * (c + 0.5), 40.0)
        cut(ring, ycone(k, yf - s * 1.0, BUSH_OD - 2 * (c + 1.0), yf + s * (c + 0.5),
                        BUSH_OD + 1.0))
        cut(b, ring)
    return _check_body(b, BUSHING)


def thrust_washer_body(xz, y0, y1):
    b = ycyl(xz, y0, y1, THRUST_D)
    cut(b, ycyl(xz, y0 - 1, y1 + 1, EYE_BORE_D))
    return _check_body(b, THRUST)


def washer_body(xz):
    b = ycyl(xz, B.LEG_Y_IN - WASHER_T, B.LEG_Y_IN, WASHER_OD)
    cut(b, ycyl(xz, B.LEG_Y_IN - WASHER_T - 1, B.LEG_Y_IN + 1, WASHER_ID))
    return _check_body(b, WASHER)


def wheel_screw_xz():
    return [L.polar((B.WX, B.WZ), B.WM_BOLT_PCD / 2.0, B.WM_BOLT_A0 + 60.0 * i)
            for i in range(6)]


def protractor_body():
    k = (L.KX, L.KZ)
    y0, y1 = PROT_Y
    ring = cut(ycyl(k, y0, y1, 2 * PROT_RING[1]), ycyl(k, y0 - 1, y1 + 1, 2 * PROT_RING[0]))
    sector = cut(ycyl(k, y0, y1, 2 * PROT_RING[1]),
                 ycyl(k, y0 - 1, y1 + 1, 2 * PROT_SECTOR[0]))
    _bool(sector, halfspace(k, PROT_SECTOR[1], True, y0 - 1, y1 + 1), 'inter')
    _bool(sector, halfspace(k, PROT_SECTOR[2], False, y0 - 1, y1 + 1), 'inter')
    b = join(ring, sector)
    for p in PROT_POSTS:
        cut(b, ycyl(p, y0 - 1, y1 + 1, 3.4))
    ye = (y1 - TICK_DEPTH, y1 + 1.0)
    for a in range(45, 156, 5):
        r1 = PROT_TICK[2] if a % 10 == 0 else PROT_TICK[1]
        cut(b, radial_box(k, prot_xz_angle(a), PROT_TICK[0], r1, TICK_W, *ye))
    for a in (L.ALPHA_FLEX_STOP, L.ALPHA_EXT_STOP):
        cut(b, radial_box(k, prot_xz_angle(a), PROT_TICK[0], PROT_TICK[3], TICK_W, *ye))
    # numeral tops point at the knee: with the shoulder near 0 the scale is
    # the lower half of the ring, where outward tops would read upside down
    for a in (60, 80, 100, 120, 140):
        phi = prot_xz_angle(a)
        cut(b, *numeral_tools(str(a), L.polar(k, PROT_NUM_R, phi), phi + 180.0, *ye))
    return _check_body(b, PROTRACTOR)


def prot_xz_angle(alpha):
    """XZ angle (build pose) of the encoder-arm centreline at knee angle alpha:
    du is at XZ 220 at alpha 80 and turns with alpha (r2a_lib.group_matrices)."""
    return 220.0 + ARM_TIP_REL + (alpha - L.ALPHA_NOM)


def gauge_body():
    w = (B.WX, B.WZ)
    y0, y1 = GAUGE_Y
    b = ycyl(w, y0, y1 + GAUGE_LIP_T, TYRE_D)
    cut(b, ycyl(w, y0 - 1, y1, GAUGE_BORE_D), ycyl(w, y1 - 1, y1 + GAUGE_LIP_T + 1, GAUGE_LIP_D))
    return _check_body(b, GAUGE)


def feeler_body():
    """Two-step feeler, built flat in its own frame (bed z = 0), mapped so the
    bed face is the model's min-Y face like the R2A ladder coupon."""
    t4, t5 = FEELER
    b = join(RF._box(0, 30, 0, 12, 0, t4), RF._box(30, 60, 0, 12, 0, t5))
    cut(b, RF._box(-1, 2, -1, 3, -1, 6))                 # corner notch at the 4.0 end
    m = adsk.core.Matrix3D.create()
    m.setToRotation(-math.pi / 2, adsk.core.Vector3D.create(1, 0, 0),
                    adsk.core.Point3D.create(0, 0, 0))
    assert _tm().transform(b, m)
    return _check_body(b, 'POC_Feeler_4p0_5p0')


# ================================================================== build
def _dowel_union(pts, y0):
    return join(*[ycyl(p, y0, y0 + L.DOWEL_LEN, L.DOWEL_D) for p in pts]) if len(pts) > 1 \
        else ycyl(pts[0], y0, y0 + L.DOWEL_LEN, L.DOWEL_D)


def _build_parts():
    _add(HOUSING, housing_body(), 'PROX')
    _add(ROTOR, rotor_body(), 'CRANK')
    _add(KNOB, knob_body(), 'CRANK')
    _add(LOCK_PIN, lock_pin_body(), 'PROX')
    pins = [L.polar((0, 0), B.SH_PIN_PCD / 2.0, a) for a in OUT_PIN_A]
    d = join(*[ycyl(p, PIN_TIP_Y, PIN_TIP_Y + L.DOWEL_LEN, L.DOWEL_D) for p in pins])
    _add(ROTOR_DOWELS, _check_body(d, ROTOR_DOWELS, 3), 'CRANK', 'Steel')
    _add(KEY_DOWEL, ycyl(key_xz(), SHAFT_Y1 - KEY_SOCKET_DEPTH,
                         SHAFT_Y1 - KEY_SOCKET_DEPTH + L.DOWEL_LEN, L.DOWEL_D), 'CRANK', 'Steel')
    _add(PUSHROD, pushrod_body(), 'ROD')
    occ = _add(THRUST, thrust_washer_body(L.C0, *THRUST_Y[0]), 'CRANK')
    for dx, dz, dy, cls in ((0.0, 0.0, THRUST_Y[1][0] - THRUST_Y[0][0], 'CRANK'),
                            (L.P0[0] - L.C0[0], L.P0[1] - L.C0[1], 0.0, 'DIST'),
                            (L.P0[0] - L.C0[0], L.P0[1] - L.C0[1],
                             THRUST_Y[1][0] - THRUST_Y[0][0], 'DIST')):
        m = B.mat((1, 0, 0), (0, 1, 0), (0, 0, 1), (dx, dy, dz))
        L.tag(B.root().occurrences.addExistingComponent(occ.component, m), cls)
    _add(PIN_CRANK, pin_body(L.C0), 'CRANK')
    _add(PIN_LEVER, pin_body(L.P0), 'DIST')
    occ = _add(BUSHING, bushing_body(L.BRG_A[0]), 'PROX')
    m = B.mat((1, 0, 0), (0, 1, 0), (0, 0, 1), (0.0, L.BRG_B[0] - L.BRG_A[0], 0.0))
    L.tag(B.root().occurrences.addExistingComponent(occ.component, m), 'PROX')
    pts = wheel_screw_xz()
    occ = _add(WASHER, washer_body(pts[0]), 'DIST')
    for p in pts[1:]:
        m = B.mat((1, 0, 0), (0, 1, 0), (0, 0, 1), (p[0] - pts[0][0], 0.0, p[1] - pts[0][1]))
        L.tag(B.root().occurrences.addExistingComponent(occ.component, m), 'DIST')
    _add(PROTRACTOR, protractor_body(), 'PROX')
    _add(GAUGE, gauge_body(), 'DIST')
    return True


def _screws():
    """Owned screws as addExistingComponent occurrences (never transform2)."""
    for comp in (SCREW_M25, SCREW_M3):
        B.drop_comp(comp)
    placed = {}
    m25 = B.screw_comp(SCREW_M25, 2.5, 12.0)
    m3 = B.screw_comp(SCREW_M3, 3.0, 10.0)
    rows = [(SET_M25, m25, [(p, B.LEG_Y_IN - WASHER_T, True) for p in wheel_screw_xz()], 'DIST'),
            (SET_KNOB, m3, [((0.0, 0.0), KNOB_SCREW_SEAT_Y, False)], 'CRANK'),
            (SET_PROT, m3, [(p, PROT_Y[1], False) for p in PROT_POSTS], 'PROX')]
    for label, master, pts, cls in rows:
        for (x, z), y, flip in pts:
            o = B.place(master, x, z, y, flip=flip)
            o.attributes.add('POC', 'set', label)
            L.tag(o, cls)
        placed[label] = len(pts)
    # screw_comp leaves its master at the origin: remove the unplaced ones
    for comp in (SCREW_M25, SCREW_M3):
        for o in _occs_named(comp):
            if o.attributes.itemByName('POC', 'set') is None:
                o.deleteMe()
    return placed


def build(_context=''):
    """Build every POC stand-in under the transform guard; article unchanged."""
    L.assert_r2a_doc()
    if os.path.exists(LOCK):
        return 'skipped: lock present'
    open(LOCK, 'w').write(time.strftime('%H:%M:%S'))
    try:
        before = {n: RF.shape_signature(n) for n in ARTICLE_RELEASED}
        L.guarded(_build_parts)
        placed = L.guarded(_screws)
        L.capture_nominal(force=True)
        after = {n: RF.shape_signature(n) for n in ARTICLE_RELEASED}
        changed = [n for n in ARTICLE_RELEASED if before[n] != after[n]]
        if changed:
            raise RuntimeError('article geometry changed: %s' % changed)
        hide_poc()
        return {'placed': placed, 'article_shapes_unchanged': True,
                'extents': placement_record()}
    finally:
        os.remove(LOCK)


ARTICLE_RELEASED = ('R2A_Prox_Inboard_L', 'R2A_Prox_Outboard_L', 'R2A_Crank_L',
                    'R2A_Crank_Cap_L', 'R2A_Distal_Link_L', 'R2A_Lever_Cap_L',
                    'R2A_Encoder_Arm_L', 'R2A_Knee_Pin_Cap_L')


def placement_record():
    """Y extents of every POC occurrence (guards against a silent displacement)."""
    out = {}
    for o in L.all_root_occs():
        nm = B.base_name(o.component.name)
        if nm.startswith('POC_'):
            b = B.bbox_of(o)
            out.setdefault(nm, []).append([round(v, 2) for v in b])
    return out


# ====================================================== configurations
def poc_set():
    kn = L.knee_ref().entityToken
    out = []
    for o in L.all_root_occs():
        nm = B.base_name(o.component.name)
        tag = o.attributes.itemByName('R2A', 'set')
        if o.entityToken == kn or nm in NOT_IN_POC or (tag and tag.value in NOT_IN_POC_SETS):
            continue
        out.append(o)
    return out


def article_set():
    return [o for o in L.all_root_occs() if not B.base_name(o.component.name).startswith('POC_')]


def show_config(which='article'):
    """Light bulbs for one configuration; returns the states to restore."""
    keep = {o.entityToken for o in (poc_set() if which == 'poc' else article_set())}
    saved = [(o, o.isLightBulbOn) for o in L.all_root_occs()]
    for o in L.all_root_occs():
        o.isLightBulbOn = o.entityToken in keep
    return saved


def hide_poc():
    """The saved document shows the article: POC parts hidden, nothing else touched."""
    n = 0
    for o in L.all_root_occs():
        if B.base_name(o.component.name).startswith('POC_'):
            o.isLightBulbOn = False
            n += 1
    return n


# ======================================================= classification
def classify(a, b, v, alpha):
    """r2a_lib.classify_pair plus the one POC artifact class."""
    cls = L.classify_pair(a, b, v, alpha)
    if cls:
        return cls
    na, nb = L._base(a), L._base(b)
    if (na.startswith('POC_SHCS') and L._is_ref(nb)) or (nb.startswith('POC_SHCS') and L._is_ref(na)):
        if v <= L.THREAD_ARTIFACT_MM3:
            return 'screw in modelled STEP thread'
    return None


def _clashes(occs, min_mm3):
    d = B.design()
    col = adsk.core.ObjectCollection.create()
    for o in occs:
        col.add(o)
    ipt = d.createInterferenceInput(col)
    ipt.areCoincidentFacesIncluded = False
    res = d.analyzeInterference(ipt)
    out = []
    if res:
        for i in range(res.count):
            it = res.item(i)
            v = it.interferenceBody.volume * 1000.0
            if v >= min_mm3:
                out.append((R.occ_name(it.entityOne), R.occ_name(it.entityTwo), v))
    return out


def sweep_poses():
    """The digital gate's 140 poses: knee 49..152 deg at shoulder 0, shoulder
    -120..+120 deg in 20 deg steps at knee 51/100/150 deg."""
    poses = [(0.0, float(a)) for a in range(49, 153)]
    for th in range(-120, 121, 20):
        for a in (51.0, 100.0, 150.0):
            if (float(th), a) not in poses:
                poses.append((float(th), a))
    return poses


def sweep(config, poses, path, min_mm3=0.01):
    """Interference over one configuration's occurrences, classified, appended
    to `path`.  Every occurrence is forced visible first (linked REFs drop out
    of analyzeInterference when hidden)."""
    L.assert_r2a_doc()
    L.ref_assert()
    L.capture_nominal(force=True)
    L._REF_NAMES = L.ref_body_names()
    occs = poc_set() if config == 'poc' else article_set()
    occs = [o for o in occs if B.base_name(o.component.name) not in SWEEP_EXCLUDE]
    saved = L.all_visible()
    data = json.load(open(path)) if os.path.exists(path) else {}
    try:
        for th, al in poses:
            key = '%.1f,%.1f' % (th, al)
            if key in data:
                continue
            L.r2a_pose(th, al)
            try:
                raw = _clashes(occs, min_mm3)
            finally:
                L.r2a_restore()
            data[key] = [{'a': a, 'b': b, 'mm3': round(v, 3),
                          'class': classify(a, b, v, al) or 'REAL'} for a, b, v in raw]
            with open(path, 'w') as s:
                json.dump(data, s)
    finally:
        L.restore_bulbs(saved)
    L.ref_assert()
    return len(data)


def sweep_summary(path):
    data = json.load(open(path))
    classes, real = {}, []
    for key, rows in data.items():
        for r in rows:
            classes[r['class']] = classes.get(r['class'], 0) + 1
            if r['class'] == 'REAL':
                real.append([key, r['a'], r['b'], r['mm3']])
    return {'poses': len(data), 'classes': classes, 'real': real}


# ========================================================= measurements
def _names(o):
    return B.base_name(o.component.name)


def _dist(a_names, b_names):
    return round(L.min_dist(list(a_names), list(b_names)), 3)


MOCK = (HOUSING, ROTOR, KNOB, ROTOR_DOWELS, KEY_DOWEL)


def measurements(alphas=(51.0, 55.0, 65.0, 80.0, 100.0, 120.0, 140.0, 145.0, 150.0)):
    """POC clearances at the article's sampled knee angles (theta = 0)."""
    L.assert_r2a_doc()
    L.ref_assert()
    L.capture_nominal(force=True)
    P = L.PART
    rows = []
    try:
        for a in alphas:
            L.r2a_pose(0.0, a)
            c = _pin_axis(PIN_CRANK)
            p = _pin_axis(PIN_LEVER)
            cu = L.uv_inv(*c)
            rows.append({
                'alpha': a,
                'pin_to_pin_mm': round(math.hypot(c[0] - p[0], c[1] - p[1]), 4),
                'theta_c_measured_deg': round(math.degrees(math.atan2(cu[1], cu[0])), 3),
                'theta_c_solver_deg': round(L.solve(a)[2], 3),
                'tyre_gauge_to_proximal_mm': _dist([GAUGE], [P['INB'], P['OUTB'],
                    'Shoulder_Output_Hub_L', P['CRANK']] + list(MOCK) + [PROTRACTOR]),
                'pushrod_rod_to_distal_mm': _dist_body(pushrod_segment('rod_and_nuts'), [P['DIST']]),
                'pushrod_group_to_crank_mm': _dist_body(pushrod_segment('without_upper_end'),
                                                        [P['CRANK'], P['CRANK_CAP']]),
                'pushrod_group_to_lever_mm': _dist_body(pushrod_segment('without_lower_end'),
                                                        [P['DIST'], P['LEVER_CAP']]),
                'thrust_washer_to_clevis_ears_mm': _dist([THRUST], [P['CRANK'], P['CRANK_CAP'],
                                                                   P['DIST'], P['LEVER_CAP']]),
                'pushrod_eye_to_thrust_washer_mm': _dist([PUSHROD], [THRUST]),
                'pushrod_to_proximal_mm': _dist([PUSHROD, THRUST], [P['INB'], P['OUTB'],
                                                                    'HW_SHCS_M4x10']),
                'crank_to_proximal_mm': _dist([P['CRANK'], P['CRANK_CAP'], 'HW_DowelPin_D4x10_Crank'],
                                              [P['INB'], P['OUTB'], 'HW_SHCS_M4x10',
                                               'R2A_SHCS_M3x10_Actuator']),
                'mock_rotor_to_proximal_mm': _dist([ROTOR, ROTOR_DOWELS], [P['OUTB'], HOUSING]),
                'knob_to_housing_mm': _dist([KNOB, KEY_DOWEL], [HOUSING]),
                'distal_to_proximal_mm': _dist([P['DIST'], P['LEVER_CAP']], [P['INB'], P['OUTB']]),
                'encoder_arm_to_protractor_mm': _dist([P['ENC_ARM']], [PROTRACTOR] + _set_occs(SET_PROT)),
                'distal_to_protractor_mm': _dist([P['DIST'], PIN_LEVER, PUSHROD], [PROTRACTOR]),
                'wheel_washers_heads_to_cable_mm': _dist([WASHER] + _set_occs(SET_M25),
                    ['REFERENCE_Cable_Wheel_Distal', 'REFERENCE_Cable_Knee_Loop']),
                'mock_to_tyre_gauge_mm': _dist(list(MOCK), [GAUGE]),
            })
    finally:
        L.r2a_restore()
    L.ref_assert()
    return rows


# Pushrod segments that match the article's rod-group definitions
# (r2a_lib.gate_measurements): 'rod + nuts' = 27..93 mm from the crank pin
# (outside both 27 mm rod-end envelopes); 'rod group to crank' adds the lower
# end; 'rod group to lever' adds the upper end.
SEGMENTS = {'rod_and_nuts': (L.RE_H, L.ROD_B - L.RE_H),
            'without_upper_end': (L.RE_H, L.ROD_B + EYE_D),
            'without_lower_end': (-EYE_D, L.ROD_B - L.RE_H)}


def pushrod_segment(key):
    """Temporary world-space copy of the pushrod cut to a SEGMENTS span."""
    s0, s1 = SEGMENTS[key]
    body = RP._world(_occs_named(PUSHROD)[0])[0]
    c, p = _pin_axis(PIN_CRANK), _pin_axis(PIN_LEVER)
    ang = math.degrees(math.atan2(p[1] - c[1], p[0] - c[0]))
    u = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
    mid = (c[0] + u[0] * 0.5 * (s0 + s1), c[1] + u[1] * 0.5 * (s0 + s1))
    return _bool(body, xzbox(mid, ang, s1 - s0, 60.0, 50.0, 100.0), 'inter')


def _dist_body(body, names):
    mm = adsk.core.Application.get().measureManager
    best = None
    for n in names:
        for o in (L.find_all(n) if isinstance(n, str) else [n]):
            for ob in L.occ_bodies(o):
                v = mm.measureMinimumDistance(body, ob).value * 10.0
                best = v if best is None else min(best, v)
    return round(best, 3)


def _pin_axis(name):
    o = _occs_named(name)[0]
    for b in L.occ_bodies(o):
        for f in b.faces:
            g = adsk.core.Cylinder.cast(f.geometry)
            if g and abs(g.radius * 20.0 - PIN_D) < 1e-6:
                return (g.origin.x * 10.0, g.origin.z * 10.0)
    raise RuntimeError('pin axis not found: ' + name)


def rotor_free_turn(step=15.0):
    """Detached mock: the rotor, knob, dowels and knob screw turned through a
    full revolution about Y must never touch the housing (journal 0.30 mm
    radial, thrust faces 0.1 mm)."""
    L.assert_r2a_doc()
    hs = [b for o in _occs_named(HOUSING) for b in RP._world(o)]
    mv = [b for n in (ROTOR, KNOB, ROTOR_DOWELS, KEY_DOWEL) for o in _occs_named(n)
          for b in RP._world(o)] + [b for o in _set_occs(SET_KNOB) for b in RP._world(o)]
    worst = 0.0
    a = 0.0
    while a < 360.0 - 1e-9:
        m = adsk.core.Matrix3D.create()
        m.setToRotation(math.radians(a), adsk.core.Vector3D.create(0, 1, 0),
                        adsk.core.Point3D.create(0, 0, 0))
        for body in mv:
            t = _tm().copy(body)
            assert _tm().transform(t, m)
            for h in hs:
                worst = max(worst, RP._overlap(t, h))
        a += step
    mm = adsk.core.Application.get().measureManager
    radial = mm.measureMinimumDistance(_occs_named(ROTOR)[0].bRepBodies.item(0),
                                       _occs_named(HOUSING)[0].bRepBodies.item(0)).value * 10
    return {'step_deg': step, 'max_overlap_mm3': round(worst, 4), 'clear': worst <= 0.001,
            'rotor_to_housing_min_mm': round(radial, 3)}


# ========================================================== assembly paths
def _mods(n):
    return _occs_named(n)


def poc_module():
    """The POC knee module (assembly-guide step 10 with the stand-ins)."""
    P = L.PART
    names = [P['OUTB'], P['TPU'] + '_Out', P['CRANK'], P['CRANK_CAP'], 'HW_DowelPin_D4x10_Crank',
             PIN_CRANK, PUSHROD, P['DIST'], P['LEVER_CAP'], 'HW_DowelPin_D4x10_Lever', PIN_LEVER,
             'HW_DowelPin_D4x10_EncArm'] + list(MOCK)
    occs = [o for n in names for o in _mods(n)]
    occs += [o for o in L.all_root_occs() if o.attributes.itemByName('R2A', 'set') and
             o.attributes.itemByName('R2A', 'set').value in ('R2A_SHCS_M3x10_Actuator',
                                                             'R2A_SHCS_M3x10_Crank')]
    occs += _set_occs(SET_KNOB) + [bushing('B')] + _mods(THRUST)
    return occs


def thrust(end, side):
    """Thrust washer at the crank ('C') or lever ('P') eye, inboard ('in') or
    outboard ('out') of it."""
    c = L.C0 if end == 'C' else L.P0
    want = THRUST_Y[0] if side == 'in' else THRUST_Y[1]
    for o in _mods(THRUST):
        b = B.bbox_of(o)
        if abs(0.5 * (b[0] + b[1]) - c[0]) < 0.5 and abs(0.5 * (b[4] + b[5]) - c[1]) < 0.5 \
                and abs(0.5 * (b[2] + b[3]) - 0.5 * sum(want)) < 0.2:
            return o
    raise RuntimeError('thrust washer not found: %s %s' % (end, side))


def bushing(which):
    occ = _mods(BUSHING)
    occ.sort(key=lambda o: B.bbox_of(o)[2])
    return occ[0] if which == 'A' else occ[1]


def path_steps():
    P = L.PART
    bA, bB = bushing('A'), bushing('B')
    mock = [o for n in MOCK for o in _mods(n)] + _set_occs(SET_KNOB)
    hous = _mods(HOUSING)
    w = RP._wheel()
    mot = w['motor']
    shell = 'ABS_TEST_Wheel_Rim_NoTyre'
    module = poc_module()
    wheel = mot + _set_occs(SET_M25) + _mods(WASHER) + ['Wheel_Hub_L'] + w['m3']
    act = 'R2A_SHCS_M3x10_Actuator'
    return [
        ('M0', 'three Ø4 x 10 output dowels into the detached rotor (from -Y)', 'path',
         dict(moving=_mods(ROTOR_DOWELS), fixed=_mods(ROTOR), vector=(0, -1, 0), travel=15)),
        ('M1', 'rotor into the housing from the mount face (from -Y)', 'path',
         dict(moving=_mods(ROTOR) + _mods(ROTOR_DOWELS), fixed=hous, vector=(0, -1, 0), travel=40)),
        ('M2', 'key dowel into the rotor end face (from +Y)', 'path',
         dict(moving=_mods(KEY_DOWEL), fixed=_mods(ROTOR) + hous, vector=(0, 1, 0), travel=15)),
        ('M3', 'knob onto the pilot and key (from +Y)', 'path',
         dict(moving=_mods(KNOB), fixed=_mods(ROTOR) + _mods(KEY_DOWEL) + hous, vector=(0, 1, 0),
              travel=20)),
        ('M3s', 'knob M3 x 10 into the rotor insert (from +Y)', 'path',
         dict(moving=_set_occs(SET_KNOB), fixed=_mods(KNOB) + _mods(ROTOR), vector=(0, 1, 0),
              travel=20)),
        ('M3k', 'hex key to the knob screw', 'tool',
         dict(label=_set_occs(SET_KNOB), d=3.0, fixed=_mods(KNOB) + _mods(ROTOR) + hous)),
        ('A2', 'bushing B into the outboard half from its outer face (from +Y)', 'path',
         dict(moving=[bB], fixed=[P['OUTB']], vector=(0, 1, 0), travel=15)),
        ('B1', 'mock actuator onto the outboard half (from +Y)', 'path',
         dict(moving=mock, fixed=[P['OUTB'], bB], vector=(0, 1, 0), travel=40)),
        ('B2', 'five M3 x 10 from the channel side into the mock inserts', 'path',
         dict(moving=[act], fixed=[P['OUTB'], bB] + hous, vector=(0, -1, 0), travel=25)),
        ('B2k', 'hex key to the mock mount screws', 'tool',
         dict(label=act, d=3.0, fixed=[P['OUTB'], bB] + mock)),
        ('B3', 'crank onto the rotor output over the three dowels (from -Y)', 'path',
         dict(moving=[P['CRANK']], fixed=mock + [P['OUTB'], act], vector=(0, -1, 0), travel=40)),
        ('B4', 'crank six M3 x 10 into the rotor inserts', 'path',
         dict(moving=['R2A_SHCS_M3x10_Crank'], fixed=[P['CRANK'], P['OUTB']] + mock,
              vector=(0, -1, 0), travel=25)),
        ('B4k', 'hex key to the crank screws (crank at its build angle)', 'tool',
         dict(label='R2A_SHCS_M3x10_Crank', d=3.0, fixed=[P['CRANK'], P['OUTB'], act] + mock)),
        ('B5a', 'outboard thrust washer onto the crank ear face (from -Y)', 'path',
         dict(moving=[thrust('C', 'out')], fixed=[P['CRANK'], P['OUTB']] + mock, vector=(0, -1, 0),
              travel=20)),
        ('B5', 'pushrod upper eye into the crank ear, cap off (from -Y)', 'path',
         dict(moving=[PUSHROD], fixed=[P['CRANK'], P['OUTB'], thrust('C', 'out')] + mock,
              vector=(0, -1, 0), travel=20)),
        ('B5b', 'inboard thrust washer onto the upper eye (from -Y)', 'path',
         dict(moving=[thrust('C', 'in')], fixed=[P['CRANK'], PUSHROD, thrust('C', 'out')],
              vector=(0, -1, 0), travel=20)),
        ('B6', 'crank cap on its two dowels', 'path',
         dict(moving=[P['CRANK_CAP']], fixed=[P['CRANK'], 'HW_DowelPin_D4x10_Crank', PUSHROD,
                                              thrust('C', 'in')], vector=(0, -1, 0), travel=20)),
        ('B6p', 'printed crank pin from the inboard side through cap, washers and eye', 'path',
         dict(moving=[PIN_CRANK], fixed=[P['CRANK'], P['CRANK_CAP'], PUSHROD, thrust('C', 'in'),
                                         thrust('C', 'out')], vector=(0, -1, 0), travel=30)),
        ('W1s', 'owned M2.5 x 12 with printed 2.0 washers into the wheel motor (from -Y)', 'path',
         # as the article's W1s: the motor's STEP holes are solid modelled threads,
         # so the screw depth is checked by fastener_engagement(), not by this path
         dict(moving=_set_occs(SET_M25) + _mods(WASHER), fixed=[P['DIST']], vector=(0, -1, 0),
              travel=20)),
        ('W1k', 'hex key to the wheel-motor screws (distal link detached)', 'tool',
         dict(label=_set_occs(SET_M25), d=2.5, fixed=[P['DIST']] + mot + _mods(WASHER))),
        ('B7a', 'inboard thrust washer onto the lever inboard ear (from +Y)', 'path',
         dict(moving=[thrust('P', 'in')], fixed=[P['DIST']], vector=(0, 1, 0), travel=20)),
        ('B7', 'pushrod lower eye into the lever clevis, cap off (from +Y)', 'path',
         dict(moving=[PUSHROD], fixed=[P['DIST'], thrust('P', 'in')], vector=(0, 1, 0), travel=20)),
        ('B7b', 'outboard thrust washer onto the lower eye (from +Y)', 'path',
         dict(moving=[thrust('P', 'out')], fixed=[P['DIST'], PUSHROD, thrust('P', 'in')],
              vector=(0, 1, 0), travel=20)),
        ('B8', 'lever cap on its two dowels', 'path',
         dict(moving=[P['LEVER_CAP']], fixed=[P['DIST'], 'HW_DowelPin_D4x10_Lever', PUSHROD,
                                              thrust('P', 'out')], vector=(0, 1, 0), travel=20)),
        ('B8p', 'printed lever pin from the outboard side through cap, washers and eye', 'path',
         dict(moving=[PIN_LEVER], fixed=[P['DIST'], P['LEVER_CAP'], PUSHROD, thrust('P', 'in'),
                                         thrust('P', 'out')], vector=(0, 1, 0), travel=30)),
        ('A1', 'bushing A into the inboard half from its hub face (from -Y)', 'path',
         dict(moving=[bA], fixed=[P['INB']], vector=(0, -1, 0), travel=15)),
        ('S1', 'inboard half with bushing A onto the shoulder hub (from +Y)', 'path',
         dict(moving=[P['INB'], bA, P['TPU'] + '_In'], fixed=RP.SHOULDER_STATIC, vector=(0, 1, 0),
              travel=40)),
        ('S3w', 'POC knee module with wheel motor and hub onto the inboard half (from +Y)', 'path',
         dict(moving=module + wheel, fixed=[P['INB'], bA, P['TPU'] + '_In', 'HW_SHCS_M4x10']
              + RP.SHOULDER_STATIC, vector=(0, 1, 0), travel=60, step=2.0)),
        ('S4k', 'hex key to the perimeter screws with the mock fitted', 'tool',
         dict(label='R2A_SHCS_M3x12_Perimeter', d=3.0,
              fixed=[P['OUTB'], P['INB'], P['DIST']] + mock)),
        ('S6', 'Ø10 knee pin from outboard through both bushings (also service)', 'path',
         dict(moving=['HW_DowelPin_D10x35'], fixed=[P['INB'], P['OUTB'], bA, bB, P['DIST'],
                                                     P['PIN_CAP']], vector=(0, 1, 0), travel=45)),
        ('P1', 'protractor onto the outboard face over the encoder arm (from +Y)', 'path',
         dict(moving=[PROTRACTOR], fixed=[P['OUTB'], P['ENC_ARM'], P['DIST'], 'HW_DowelPin_D10x35',
                                           'R2A_SHCS_M3x10_EncArm'], vector=(0, 1, 0), travel=30)),
        ('P1s', 'protractor two M3 x 10 into the bracket inserts (from +Y)', 'path',
         dict(moving=_set_occs(SET_PROT), fixed=[PROTRACTOR, P['OUTB']], vector=(0, 1, 0), travel=25)),
        ('P1k', 'hex key to the protractor screws', 'tool',
         dict(label=_set_occs(SET_PROT), d=3.0, fixed=[PROTRACTOR, P['OUTB'], P['ENC_ARM'],
                                                        P['DIST']])),
        ('G1', 'tyre gauge over the no-tyre shell, last (from +Y)', 'path',
         dict(moving=[GAUGE], fixed=[shell, 'Wheel_Hub_L', P['DIST'], P['OUTB']] + mot + w['m4'] + mock,
              vector=(0, 1, 0), travel=45)),
    ]


def run_paths(ids=None, path=None):
    L.assert_r2a_doc()
    L.ref_assert()
    path = path or os.path.join(EVIDENCE, 'assembly_paths.json')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = json.load(open(path)) if os.path.exists(path) else {}
    for sid, desc, kind, args in path_steps():
        if (ids and sid not in ids) or sid in data:
            continue
        r = RP.linear_path(**args) if kind == 'path' else RP.tool_access(**args)
        r['moving'] = [getattr(m, 'name', m) for m in args.get('moving', [])] or r.get('moving')
        r['description'] = desc
        r['status'] = 'CAD PATH VERIFIED' if r['clear'] else 'BLOCKED'
        data[sid] = r
        with open(path, 'w') as s:
            json.dump(data, s, indent=1)
    return {k: v['clear'] for k, v in data.items()}


def lock_paths(path=None, offset_deg=3.0):
    """At each check point the lock pin drops from +Y through the knob boss
    into its dial hole with zero overlap; `offset_deg` of knee away from a
    check point it must be blocked (negative control)."""
    L.assert_r2a_doc()
    L.capture_nominal(force=True)
    path = path or os.path.join(EVIDENCE, 'lock_pin_paths.json')
    out = {}
    lp = _mods(LOCK_PIN)[0]
    fixed = _mods(HOUSING) + _mods(KNOB)
    nom = list(lp.transform2.asArray())
    try:
        for a in CHECK_ALPHAS:
            for label, al in (('check', a), ('negative', a + offset_deg)):
                L.r2a_pose(0.0, al)
                # the pin stays in the housing frame; turn it to the hole of `a`
                d = L.solve(a)[2] - L.THC0
                m = B._mm(B._rot_arr(-d, 0.0, 0.0), L.capture_nominal()[lp.entityToken])
                m = B._mm(L.group_matrices(0.0, al)['PROX'], m)
                lp.transform2 = B._as_matrix(m)
                r = RP.linear_path([lp], fixed, (0, 1, 0), 20.0, step=1.0)
                out['%s_%g' % (label, al)] = {'alpha_pose': al, 'hole_alpha': a,
                                              'theta_c_deg': round(L.solve(a)[2], 3),
                                              'max_overlap_mm3': r['max_overlap_mm3'],
                                              'clear': r['clear']}
    finally:
        L.r2a_restore()
        lp.transform2 = B._as_matrix(nom)
    ok = all(v['clear'] for k, v in out.items() if k.startswith('check')) and \
        not any(v['clear'] for k, v in out.items() if k.startswith('negative'))
    out['pass'] = ok
    with open(path, 'w') as s:
        json.dump(out, s, indent=1)
    return ok


def negative_controls(path=None):
    P = L.PART
    path = path or os.path.join(EVIDENCE, 'assembly_path_negative_controls.json')
    out = {
        'rotor_into_housing_from_plus_y': RP.linear_path(_mods(ROTOR), _mods(HOUSING), (0, 1, 0), 10),
        'pushrod_through_crank_slab': RP.linear_path([PUSHROD], [P['CRANK']], (0, 1, 0), 10),
        'module_minus_y_into_inboard': RP.linear_path([P['OUTB']] + _mods(HOUSING), [P['INB']],
                                                      (0, -1, 0), 5),
        'bushing_b_past_its_lip': RP.linear_path([bushing('B')], [P['OUTB']], (0, -1, 0), 3),
    }
    with open(path, 'w') as s:
        json.dump(out, s, indent=1)
    return {k: v['clear'] for k, v in out.items()}


# ---------------------------------------------------- fastener engagement
ENGAGEMENT = [
    # (set or occurrence list key, head side, receiving, mouth, thread end, pocket floor)
    ('R2A_SHCS_M3x10_Actuator', -1, 'M3 x 5 insert, mock housing (Ø4.5 x 6.0)',
     MOUNT_Y, MOUNT_Y + B.INSERT_LEN, MOUNT_Y + INSERT_DEPTH),
    ('R2A_SHCS_M3x10_Crank', -1, 'M3 x 5 insert, mock rotor output (Ø4.5 x 6.0)',
     OUT_Y, OUT_Y + B.INSERT_LEN, OUT_Y + OUT_INSERT_DEPTH),
    (SET_KNOB, +1, 'M3 x 5 insert, rotor pilot (Ø4.5 x 7.0)',
     PILOT_Y1, PILOT_Y1 - B.INSERT_LEN, PILOT_Y1 - KNOB_POCKET_DEPTH),
    (SET_PROT, +1, 'M3 x 5 insert, outboard-half bracket position',
     L.Y_OUT, L.Y_OUT - B.INSERT_LEN, L.Y_OUT - B.ENC_INSERT_DEPTH),
    (SET_M25, -1, 'GIM4305-10 housing thread (STEP Ø2.0 x 3.0 blind, y 67.5..70.5)',
     67.5, 70.5, 70.5),
]


def fastener_engagement(path=None):
    """RP.fastener_engagement's method for the POC screw sets (planar end
    faces of the modelled screws; head height = d)."""
    L.assert_r2a_doc()
    rows = []
    for name, side, recv, mouth, end, floor in ENGAGEMENT:
        occs = _set_occs(name) or RP._occs([name])
        spans = sorted({RP._y_faces(o) for o in occs})
        if len(spans) != 1:
            raise RuntimeError('%s: screws disagree in Y: %s' % (name, spans))
        y0, y1 = spans[0]
        d = 2.5 if 'M2p5' in name else 3.0
        seat, tip = (y1 - d, y0) if side > 0 else (y0 + d, y1)
        lo, hi = sorted((mouth, end))
        eng = max(0.0, min(max(seat, tip), hi) - max(min(seat, tip), lo))
        rows.append({'set': name, 'count': len(occs), 'screw_y_mm': [y0, y1],
                     'head_bearing_y_mm': round(seat, 3), 'tip_y_mm': round(tip, 3),
                     'receiving': recv, 'engagement_mm': round(eng, 3),
                     'tip_to_floor_mm': round(abs(tip - floor), 3)})
    if path:
        with open(path, 'w') as s:
            json.dump(rows, s, indent=1)
    return rows


# ================================================================ release
# (component or builder key, released stem, bed side, qty, material, purpose)
PARTS = [
    (HOUSING, 'POC_Knee_Actuator_Mock_Housing_L_ABS_MOUNT_FACE_DOWN', 'min', 1, 'ABS'),
    (ROTOR, 'POC_Knee_Actuator_Mock_Rotor_L_ABS_OUTPUT_FACE_DOWN', 'min', 1, 'ABS'),
    (KNOB, 'POC_Knee_Actuator_Mock_Knob_L_ABS_OUTER_FACE_DOWN', 'max', 1, 'ABS'),
    (LOCK_PIN, 'POC_Knob_Lock_Pin_ABS_HEAD_DOWN', 'max', 2, 'ABS'),
    (PUSHROD, 'POC_Pushrod_L_ABS_FLAT', 'min', 1, 'ABS'),
    (PIN_CRANK, 'POC_Clevis_Pin_D4p75x18_ABS_ON_END', 'min', 4, 'ABS'),
    (THRUST, 'POC_Eye_Thrust_Washer_D11x1p5_ABS', 'min', 6, 'ABS'),
    (BUSHING, 'POC_Knee_Bushing_OD18p90_ID10p60_ABS_ON_END', 'min', 3, 'ABS'),
    (WASHER, 'POC_Washer_M2p5_2p0_ABS', 'min', 8, 'ABS'),
    (PROTRACTOR, 'POC_Knee_Protractor_L_ABS_FLAT', 'min', 1, 'ABS'),
    (GAUGE, 'POC_Tyre_Gauge_Ring_D110_ABS_LIP_DOWN', 'max', 1, 'ABS'),
]
TOOLS = [('POC_Feeler_4p0_5p0', 'POC_Feeler_4p0_5p0_ABS_FLAT', 'min', 1, 'ABS')]
COUPONS = [
    # name, source, bed side, qty, keep region
    ('POC_COUPON_Rod_Eye', PUSHROD, 'min', 1, 'rod_eye'),
    ('POC_COUPON_Mock_Housing_Ring', HOUSING, 'min', 1, 'housing_ring'),
    ('POC_COUPON_Mock_Rotor_Stub', ROTOR, 'min', 1, 'rotor_stub'),
    ('POC_COUPON_Bushing_Seat', 'R2A_Prox_Inboard_L', 'min', 1, 'bushing_seat'),
    ('POC_COUPON_Tyre_Gauge_Lip', GAUGE, 'max', 1, 'gauge_lip'),
]


def _source_body(name):
    return _tm().copy(_occs_named(name)[0].component.bRepBodies.item(0))


def coupon_source(key):
    if key == 'rod_eye':
        c, p = L.C0, L.P0
        ang = math.degrees(math.atan2(p[1] - c[1], p[0] - c[0]))
        u = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
        keep = xzbox((c[0] + u[0] * 14.0, c[1] + u[1] * 14.0), ang, 48.0, 22.0,
                     ROD_Y[0] - 1, ROD_Y[1] + 1)
        return _bool(_source_body(PUSHROD), keep, 'inter')
    if key == 'housing_ring':
        return _bool(_source_body(HOUSING), ycyl((0, 0), MOUNT_Y - 1, INSERT_BOSS_Y1, 100), 'inter')
    if key == 'rotor_stub':
        return _bool(_source_body(ROTOR), ycyl((0, 0), OUT_Y - 1, MOUNT_Y + INSERT_DEPTH, 60), 'inter')
    if key == 'bushing_seat':
        return _bool(_source_body('R2A_Prox_Inboard_L'),
                     ycyl((L.KX, L.KZ), L.Y_IN - 1, L.LIP_A[1], 34.0), 'inter')
    if key == 'gauge_lip':
        return _bool(_source_body(GAUGE), ycyl((B.WX, B.WZ), GAUGE_Y[1] - 5.5,
                                                GAUGE_Y[1] + GAUGE_LIP_T + 1, 120), 'inter')
    raise KeyError(key)


def release_rows():
    rows = [(n, s, side, q, m, 'part') for n, s, side, q, m in PARTS]
    rows += [(n, s, side, q, m, 'tool') for n, s, side, q, m in TOOLS]
    rows += [(n, n + '_ABS', side, q, 'ABS', 'coupon') for n, _, side, q, _ in COUPONS]
    return rows


def model_body(name):
    """Model-space B-Rep of a released row (before the bed transform)."""
    for n, src, side, q, key in COUPONS:
        if n == name:
            return coupon_source(key)
    if name == TOOLS[0][0]:
        return feeler_body()
    return _source_body(name)


def bed_body(name):
    side = [r[2] for r in release_rows() if r[0] == name][0]
    return RF.bed_body(None, side=side, source=model_body(name))


def body_signature(name):
    return RF.body_signature(model_body(name))


def print_audit(name, bridge_max_mm=12.0, lip_max_mm=1.2, overhang_deg=45.0):
    """Every downward face of the bed-pose body, classified as in
    r2a_release_fusion.print_audit, plus 'self-supporting' for a non-planar
    face whose every sampled normal is within overhang_deg of horizontal
    (45 deg chamfers and cones)."""
    body = bed_body(name)
    zmin = -math.cos(math.radians(90.0 - overhang_deg)) - 1e-4
    rows = []
    for f in body.faces:
        ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
        planar = adsk.core.Plane.cast(f.geometry) is not None
        if planar and (not ok or n.z > -1e-6):
            continue
        z = f.pointOnFace.z * 10
        bb = f.boundingBox
        dx = (bb.maxPoint.x - bb.minPoint.x) * 10
        dy = (bb.maxPoint.y - bb.minPoint.y) * 10
        area = f.area * 100
        if planar:
            if n.z < -0.999999 and abs(z) < 1e-4:
                cls = 'bed'
            elif n.z < -0.999999:
                per = sum(e.length for e in f.loops.item(0).edges) * 10 if f.loops.count else 1.0
                width = area / max(per, 1e-9)
                if f.loops.count > 1 and width <= lip_max_mm:
                    cls = 'lip'
                elif min(dx, dy) <= bridge_max_mm:
                    cls = 'bridge'
                else:
                    cls = 'SUPPORT'
            elif n.z >= zmin:
                cls = 'self-supporting'
            else:
                cls = 'SUPPORT'
        else:
            ev = f.evaluator
            rng = ev.parametricRange()
            if isinstance(rng, tuple):
                rng = rng[-1]
            worst = 1.0
            down = False
            for i in range(9):
                for j in range(9):
                    u = rng.minPoint.x + (rng.maxPoint.x - rng.minPoint.x) * (i + 0.5) / 9
                    v = rng.minPoint.y + (rng.maxPoint.y - rng.minPoint.y) * (j + 0.5) / 9
                    p2 = adsk.core.Point2D.create(u, v)
                    if not ev.isParameterOnFace(p2):
                        continue
                    okn, nn = ev.getNormalAtParameter(p2)
                    if okn:
                        worst = min(worst, nn.z)
                        down = down or nn.z < -1e-6
            if not down:
                continue
            cls = 'self-supporting' if worst >= zmin else 'SUPPORT'
        rows.append({'z_mm': round(z, 3), 'area_mm2': round(area, 2),
                     'extent_mm': [round(dx, 2), round(dy, 2)], 'class': cls,
                     'geometry': f.geometry.objectType.split('::')[-1]})
    counts = {}
    for r in rows:
        counts[r['class']] = counts.get(r['class'], 0) + 1
    bed_area = sum(r['area_mm2'] for r in rows if r['class'] == 'bed')
    bb = body.boundingBox
    return {'part': name, 'bed_contact_mm2': round(bed_area, 2), 'counts': counts,
            'faces': [r for r in rows if r['class'] != 'bed'],
            'bed_footprint_mm': [round((bb.maxPoint.x - bb.minPoint.x) * 10, 1),
                                 round((bb.maxPoint.y - bb.minPoint.y) * 10, 1)],
            'height_mm': round(bb.maxPoint.z * 10, 3)}


def mesh_fidelity(name, path, chord_gate_mm=S.CHORD_GATE_MM):
    """The r2a_release_fusion.mesh_fidelity() checks, with this row's bed body."""
    body = bed_body(name)
    raw = A._mesh_triangles(path)
    index, tris = {}, []
    for t in raw:
        tris.append(tuple(index.setdefault(v, len(index)) for v in t))
    verts = [None] * len(index)
    for v, i in index.items():
        verts[i] = v
    failures, metrics = [], {'triangles': len(tris), 'vertices': len(verts)}
    edges, degenerate = {}, 0
    for t in tris:
        if len(set(t)) < 3:
            degenerate += 1
        for p, q in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])):
            k = (min(p, q), max(p, q))
            edges[k] = edges.get(k, 0) + 1
    parent = list(range(len(verts)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for t in tris:
        for p, q in ((t[0], t[1]), (t[1], t[2])):
            rp, rq = find(p), find(q)
            if rp != rq:
                parent[rp] = rq
    metrics.update(open_or_nonmanifold_edges=sum(1 for c in edges.values() if c != 2),
                   degenerate_triangles=degenerate,
                   shells=len({find(i) for i in range(len(verts))}), lumps=body.lumps.count)
    if metrics['open_or_nonmanifold_edges'] or degenerate:
        failures.append('mesh is not a closed manifold')
    if metrics['shells'] != metrics['lumps']:
        failures.append('shell count differs from B-Rep lumps')
    on = adsk.fusion.PointContainment.PointOnPointContainment
    off = [v for v in verts if body.pointContainment(
        adsk.core.Point3D.create(v[0] / 10, v[1] / 10, v[2] / 10)) != on]
    metrics['vertices_off_reviewed_surface'] = len(off)
    if off:
        failures.append('%d vertices are not on the reviewed B-Rep' % len(off))
    chord = A._cylinder_chord_mm(body, verts, tris)
    metrics['max_cylinder_chord_mm'] = round(chord, 5)
    if chord_gate_mm is not None and chord > chord_gate_mm:
        failures.append('chord %.4f mm exceeds %.4f mm' % (chord, chord_gate_mm))
    allowance = max(chord, chord_gate_mm or 0.0) + 0.001
    volume = area = bed = 0.0
    for p, q, r in raw:
        u = [q[i] - p[i] for i in range(3)]
        w = [r[i] - p[i] for i in range(3)]
        c = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
        area += math.sqrt(sum(x * x for x in c)) / 2
        volume += (p[0] * (q[1] * r[2] - q[2] * r[1]) - p[1] * (q[0] * r[2] - q[2] * r[0])
                   + p[2] * (q[0] * r[1] - q[1] * r[0])) / 6
        if max(abs(p[2]), abs(q[2]), abs(r[2])) < 1e-4 and c[2] < 0:
            bed += -c[2] / 2
    curved = bed_brep = 0.0
    for f in body.faces:
        if not adsk.core.Plane.cast(f.geometry):
            curved += f.area * 100
            continue
        ok, normal = f.evaluator.getNormalAtPoint(f.pointOnFace)
        if ok and normal.z < -0.999999 and abs(f.pointOnFace.z) < 1e-6:
            bed_brep += f.area * 100
    metrics.update(mesh_volume_mm3=round(volume, 3), brep_volume_mm3=round(body.volume * 1000, 3),
                   mesh_area_mm2=round(area, 3), brep_area_mm2=round(body.area * 100, 3),
                   bed_contact_mesh_mm2=round(bed, 3), bed_contact_brep_mm2=round(bed_brep, 3))
    if abs(volume - body.volume * 1000) > allowance * curved + 0.05:
        failures.append('volume differs beyond tessellation')
    if abs(area - body.area * 100) > 0.002 * body.area * 100 + 0.05:
        failures.append('surface area differs beyond tessellation')
    if bed_brep <= 0 or abs(bed - bed_brep) > 0.01 * bed_brep + 0.05:
        failures.append('bed contact face differs')
    zmin = min(v[2] for v in verts)
    metrics['mesh_min_z_mm'] = zmin
    if abs(zmin) > 1e-4:
        failures.append('mesh does not sit on the bed at z=0')
    bb = body.boundingBox
    box = [max(abs(min(v[k] for v in verts) - bb.minPoint.asArray()[k] * 10),
               abs(max(v[k] for v in verts) - bb.maxPoint.asArray()[k] * 10)) for k in range(3)]
    metrics['box_deviation_mm'] = [round(x, 4) for x in box]
    if max(box) > allowance:
        failures.append('bed-pose bounding box differs')
    grid = A._triangle_grid(raw, allowance)
    samples = [f.pointOnFace for f in body.faces] + [e.pointOnEdge for e in body.edges] + \
        [v.geometry for v in body.vertices]
    missing = 0
    for pt in samples:
        p = (pt.x * 10, pt.y * 10, pt.z * 10)
        cand = grid.get(tuple(math.floor(c / 5.0) for c in p), [])
        d2 = min((A._distance2(p, *raw[i]) for i in cand), default=float('inf'))
        if d2 > allowance * allowance:
            missing += 1
    metrics['brep_samples'] = len(samples)
    metrics['brep_samples_not_in_mesh'] = missing
    if missing:
        failures.append('%d B-Rep samples are missing from the mesh' % missing)
    return {'part': name, 'pass': not failures, 'failures': failures, 'metrics': metrics}


# -------------------------------------------------------------- contracts
def contract_table():
    K = [(L.KX, L.KZ)]
    O = [(0.0, 0.0)]
    locks = [lock_xz(a) for a in CHECK_ALPHAS]
    screws = [L.polar((0, 0), B.SH_OUT_PCD / 2.0, a) for a in OUT_SCREW_A]
    pins = [L.polar((0, 0), B.SH_PIN_PCD / 2.0, a) for a in OUT_PIN_A]
    ptr = [L.polar((0, 0), LOCK_R, POINTER_A)]
    c = BUSH_CHAMFER
    return [
        (HOUSING, 'journal bore', JOURNAL_BORE_D, [(MOUNT_Y + BORE_CHAMFER, HOUSING_Y1)], O),
        (HOUSING, 'mount M3 insert receivers', INSERT_D, [(MOUNT_Y, MOUNT_Y + INSERT_DEPTH)] * 5,
         act_xz()),
        (HOUSING, 'dial lock holes', LOCK_HOLE_D, [(HOUSING_Y1 - LOCK_DEPTH, HOUSING_Y1)] * len(CHECK_ALPHAS), locks),
        (ROTOR, 'output rotating disc', DISC_D, [(OUT_Y, DISC_Y1)], O),
        (ROTOR, 'journal', JOURNAL_D, [(DISC_Y1, SHAFT_Y1)], O),
        (ROTOR, 'knob pilot', PILOT_D, [(SHAFT_Y1, PILOT_Y1)], O),
        (ROTOR, 'output M3 insert receivers', INSERT_D, [(OUT_Y, OUT_Y + OUT_INSERT_DEPTH)] * 6, screws),
        (ROTOR, 'factory-pin dowel sockets', KEY_SOCKET_D,
         [(OUT_Y + DOWEL_CHAMFER, OUT_Y + DOWEL_SOCKET_DEPTH)] * 3, pins),
        (ROTOR, 'knob-screw insert receiver', INSERT_D, [(PILOT_Y1 - KNOB_POCKET_DEPTH, PILOT_Y1)], O),
        (ROTOR, 'knob key dowel socket', KEY_SOCKET_D, [(SHAFT_Y1 - KEY_SOCKET_DEPTH, SHAFT_Y1)],
         [key_xz()]),
        (KNOB, 'pilot bore', PILOT_BORE_D, [(SHAFT_Y1, PILOT_Y1 + 0.3)], O),
        (KNOB, 'key dowel slip hole', KEY_SLIP_D,
         [(SHAFT_Y1, SHAFT_Y1 + L.DOWEL_LEN - KEY_SOCKET_DEPTH + 0.5)], [key_xz()]),
        (KNOB, 'screw clearance', 3.4, [(PILOT_Y1 + 0.3, KNOB_SCREW_SEAT_Y)], O),
        (KNOB, 'screw counterbore', KNOB_CBORE_D, [(KNOB_SCREW_SEAT_Y, KNOB_Y1)], O),
        (KNOB, 'lock boss hole', LOCK_HOLE_D, [(SHAFT_Y1, KNOB_Y1)], ptr),
        (LOCK_PIN, 'shank', LOCK_PIN_D, [(HOUSING_Y1 - LOCK_DEPTH + 0.9, KNOB_Y1)], ptr),
        (PUSHROD, 'eye bores', EYE_BORE_D, [ROD_Y, ROD_Y], [L.C0, L.P0]),
        (PUSHROD, 'eye outer', EYE_D, [ROD_Y, ROD_Y], [L.C0, L.P0]),
        (THRUST, 'bore', EYE_BORE_D, [THRUST_Y[0]], [L.C0]),
        (THRUST, 'outer', THRUST_D, [THRUST_Y[0]], [L.C0]),
        (PIN_CRANK, 'pin', PIN_D, [(PIN_Y[0] + PIN_CHAMFER, PIN_Y[1] - PIN_CHAMFER)], [L.C0]),
        (PIN_LEVER, 'pin', PIN_D, [(PIN_Y[0] + PIN_CHAMFER, PIN_Y[1] - PIN_CHAMFER)], [L.P0]),
        (BUSHING, 'outer', BUSH_OD, [(L.BRG_A[0] + c, L.BRG_A[1] - c)], K),
        (BUSHING, 'bore', BUSH_ID, [(L.BRG_A[0] + c, L.BRG_A[1] - c)], K),
        (WASHER, 'bore', WASHER_ID, [(B.LEG_Y_IN - WASHER_T, B.LEG_Y_IN)], None),
        (WASHER, 'outer', WASHER_OD, [(B.LEG_Y_IN - WASHER_T, B.LEG_Y_IN)], None),
        (PROTRACTOR, 'M3 clearance on the bracket inserts', 3.4, [PROT_Y] * 2, PROT_POSTS),
        (PROTRACTOR, 'ring inner edge', 2 * PROT_RING[0], [PROT_Y], K),
        (GAUGE, 'tyre OD', TYRE_D, [(GAUGE_Y[0], GAUGE_Y[1] + GAUGE_LIP_T)], [(B.WX, B.WZ)]),
        (GAUGE, 'bore on the no-tyre drum', GAUGE_BORE_D, [GAUGE_Y], [(B.WX, B.WZ)]),
        (GAUGE, 'lip bore', GAUGE_LIP_D, [(GAUGE_Y[1], GAUGE_Y[1] + GAUGE_LIP_T)], [(B.WX, B.WZ)]),
    ]


def dimensional_contracts():
    out = []
    for part, label, d, spans, centres in contract_table():
        rows = [r for r in RF.cylinders(part) if abs(r['d'] - d) < 0.001
                and abs(abs(r['axis'][1]) - 1) < 1e-6
                and (centres is None or any(math.hypot(r['x'] - x, r['z'] - z) < 0.01
                                            for x, z in centres))]
        got = sorted((round(r['y0'], 2), round(r['y1'], 2)) for r in rows)
        want = sorted((round(a, 2), round(b, 2)) for a, b in spans)
        out.append({'part': part, 'interface': label, 'diameter_mm': d,
                    'expected_y_spans_mm': want, 'measured_y_spans_mm': got,
                    'pass': got == want})
    # pushrod pin-to-pin from the two eye-bore axes
    ax = [(r['x'], r['z']) for r in RF.cylinders(PUSHROD) if abs(r['d'] - EYE_BORE_D) < 0.001]
    ptp = math.hypot(ax[0][0] - ax[1][0], ax[0][1] - ax[1][1]) if len(ax) == 2 else None
    out.append({'part': PUSHROD, 'interface': 'pin to pin', 'expected_mm': L.ROD_B,
                'measured_mm': round(ptp, 4) if ptp else None,
                'pass': ptp is not None and abs(ptp - L.ROD_B) < 0.001})
    return out


# ---------------------------------------------------- baseline & export
def load_baseline():
    if os.path.exists(BASELINE):
        return json.load(open(BASELINE))
    return {'document': L.DOC, 'parts': {}, 'verified_source_sha256': {}, 'review_log': []}


def _write_baseline(baseline, action, names, reason):
    if not reason or len(reason.strip()) < 12:
        raise ValueError('A deliberate baseline change needs a written review reason')
    baseline.setdefault('review_log', []).append(
        {'date': time.strftime('%Y-%m-%d'), 'action': action, 'parts': names,
         'reason': reason.strip()})
    with open(BASELINE, 'w') as s:
        json.dump(baseline, s, indent=1)


def _contract_parts():
    return {c[0] for c in contract_table()}


def accept_shapes(names, reason):
    L.assert_r2a_doc()
    contracts = dimensional_contracts()
    baseline = load_baseline()
    rows = {r[0]: r for r in release_rows()}
    for name in names:
        src = name
        for n, s, side, q, key in COUPONS:
            if n == name:
                src = s
        bad = [c for c in contracts if c['part'] == src and not c['pass']]
        if src.startswith('R2A_'):
            bad += [c for c in RF.dimensional_contracts() if c['part'] == src and not c['pass']]
        if bad:
            raise RuntimeError('Contracts fail: ' + json.dumps(bad))
        audit = print_audit(name)
        if audit['counts'].get('SUPPORT'):
            raise RuntimeError('support face in bed pose: %s %s' % (name, audit['counts']))
        r = rows[name]
        baseline['parts'].setdefault(name, {}).update(
            {'file': 'r2a_poc_stl/%s.stl' % r[1], 'qty': r[3], 'material': r[4],
             'bed_side': r[2], 'kind': r[5], 'support_policy': 'none', 'state': 'RELEASED',
             'shape': body_signature(name)})
    _write_baseline(baseline, 'accept_shapes', names, reason)
    return len(names)


def assert_shape(name):
    row = load_baseline()['parts'].get(name)
    if row is None or row.get('shape') != body_signature(name):
        raise RuntimeError('Unreviewed POC geometry blocks export: ' + name)


def _sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def _export_to(name, path):
    A._export_body(bed_body(name), path)


def release(out_dir=None, names=None):
    """Export every reviewed row; a directory argument makes a dry run.
    Never updates the baseline."""
    L.assert_r2a_doc()
    target = out_dir or OUT_DIR
    os.makedirs(target, exist_ok=True)
    report = {}
    base = load_baseline()['parts']
    for r in release_rows():
        name = r[0]
        if names and name not in names:
            continue
        assert_shape(name)
        staged = os.path.join(target, r[1] + '.pending.stl')
        final = os.path.join(target, r[1] + '.stl')
        L.guarded(_export_to, name, staged)
        fid = mesh_fidelity(name, staged)
        if not fid['pass']:
            os.remove(staged)
            raise RuntimeError('mesh fidelity failed: %s %s' % (name, fid['failures']))
        keep = os.path.exists(final) and base.get(name, {}).get('released_sha256') == _sha(final) \
            and mesh_fidelity(name, final, chord_gate_mm=None)['pass']
        if keep:
            os.remove(staged)
            report[name] = {'file': final, 'release_file': 'retained'}
        else:
            os.replace(staged, final)
            report[name] = {'file': final, 'release_file': 'written', 'fidelity': fid['metrics']}
    return report


def accept_released_files(names, reason):
    L.assert_r2a_doc()
    baseline = load_baseline()
    for name in names:
        assert_shape(name)
        row = baseline['parts'][name]
        path = os.path.join(ROOT, row['file'])
        fid = mesh_fidelity(name, path)
        if not fid['pass']:
            raise RuntimeError('fidelity: ' + json.dumps(fid))
        sig = A.mesh_signature(path)
        row['released_sha256'] = sig['sha256']
        row['fresh_fusion_export'] = {k: sig[k] for k in ('sha256', 'triangles', 'geometry_sha256')}
        row['fidelity'] = fid['metrics']
    _write_baseline(baseline, 'accept_released_files', names, reason)
    return len(names)


def accept_verified_sources(reason):
    L.assert_r2a_doc()
    baseline = load_baseline()
    baseline['verified_source_sha256'] = {s: _sha(os.path.join(ROOT, s)) for s in VERIFIED_SOURCES}
    _write_baseline(baseline, 'accept_verified_sources', VERIFIED_SOURCES, reason)
    return baseline['verified_source_sha256']


def audit(path=None):
    """Contracts and print audit for every release row -> release_audit.json."""
    L.assert_r2a_doc()
    path = path or os.path.join(EVIDENCE, 'release_audit.json')
    rec = {'document': L.DOC, 'written': time.strftime('%Y-%m-%d %H:%M'),
           'dimensional_contracts': dimensional_contracts(),
           'print_audit': {r[0]: print_audit(r[0]) for r in release_rows()}}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as s:
        json.dump(rec, s, indent=1)
    return {'contracts_pass': all(c['pass'] for c in rec['dimensional_contracts']),
            'support_faces': {k: v['counts'].get('SUPPORT', 0) for k, v in rec['print_audit'].items()}}


# ================================================================ records
def design_values():
    """The design clearances r2a_calc.py §10 reads (one source: this module)."""
    p0, p1 = PROT_POSTS
    return {
        'pin_d': PIN_D, 'pin_len': PIN_LEN, 'clevis_hole_d': L.PIN5_HOLE_D,
        'eye_bore_d': EYE_BORE_D, 'journal_d': JOURNAL_D, 'journal_bore_d': JOURNAL_BORE_D,
        'thrust_gaps': [round(MOUNT_Y - DISC_Y1, 3), round(SHAFT_Y1 - HOUSING_Y1, 3)],
        'pilot_d': PILOT_D, 'pilot_bore_d': PILOT_BORE_D,
        'bushing_od': BUSH_OD, 'bushing_id': BUSH_ID, 'bearing_seat_d': L.BRG_SEAT_D,
        'knee_pin_d': B.KNEE_AXLE_D, 'lock_r': LOCK_R, 'lock_hole_d': LOCK_HOLE_D,
        'lock_pin_d': LOCK_PIN_D, 'protractor_hole_d': 3.4, 'screw_d': 3.0,
        'post_spacing': round(math.hypot(p0[0] - p1[0], p0[1] - p1[1]), 3),
        'arm_dowel_hole_d': 4.30, 'dowel_d': L.DOWEL_D,
        'arm_dowel_r': round(math.hypot(*L.ENC_DOWEL_D), 3),
        'arm_tip_r': round(math.hypot(*L.ENC_DOWEL_D) + 5.0, 3),
        'gauge_bore_d': GAUGE_BORE_D, 'gauge_od': TYRE_D, 'washer_t': WASHER_T,
        'insert_boss_d': INSERT_BOSS_D, 'housing_d': HOUSING_D,
        'rod_section_mm': [ROD_W, ROD_Y[1] - ROD_Y[0]], 'neck_section_mm': [NECK_W, ROD_Y[1] - ROD_Y[0]],
    }


def write_record(measured=None, extra=None):
    """Write evidence/r2a/2026-09-28_poc/poc_measurements.json."""
    L.assert_r2a_doc()
    doc = adsk.core.Application.get().activeDocument
    rec = {'document': doc.name, 'version': doc.dataFile.versionNumber,
           'written': time.strftime('%Y-%m-%d %H:%M'), 'design_mm': design_values(),
           'check_alphas': list(CHECK_ALPHAS),
           'lock_theta_c_deg': {str(a): round(L.solve(a)[2], 3) for a in CHECK_ALPHAS},
           'stop_theta_c_deg': {str(a): round(L.solve(a)[2], 3)
                                for a in (L.ALPHA_FLEX_STOP, L.ALPHA_EXT_STOP)}}
    if measured:
        rec['clearances'] = measured
        keys = [k for k in measured[0] if k.endswith('_mm') and k != 'pin_to_pin_mm']
        work = [r for r in measured if L.ALPHA_FLEX_STOP <= r['alpha'] <= L.ALPHA_EXT_STOP]
        rec['clearance_min_mm'] = {k: min(r[k] for r in work) for k in keys}
    if extra:
        rec.update(extra)
    os.makedirs(EVIDENCE, exist_ok=True)
    with open(os.path.join(EVIDENCE, 'poc_measurements.json'), 'w') as s:
        json.dump(rec, s, indent=1)
    return rec


# ================================================================= images
GUIDE_DIR = os.path.join(ROOT, 'docs', 'assembly', 'r2a_poc')
LOOK_CANDIDATES = ('Plastic - Matte (Orange)', 'Plastic - Glossy (Orange)',
                   'Plastic - Matte (Yellow)', 'Plastic - Glossy (Yellow)')
LOOK = {
    'POC': (HOUSING, ROTOR, KNOB, LOCK_PIN, PUSHROD, PIN_CRANK, PIN_LEVER, THRUST,
                                 BUSHING, WASHER, PROTRACTOR, GAUGE),
}


def apply_looks():
    """POC occurrences get one appearance (presentation only; shape
    signatures ignore appearance).

    Two traps (2026-09-29): a body appearance on a base-feature body reverts
    at the next recompute (so the look is set on the occurrence, which
    persists), and design.computeAll() -- run inside every rig_lib.guarded()
    call -- displaces the knee REF's transform2 until it is rewritten.  The
    knee REF is therefore recomposed from the shoulder REF and asserted."""
    L.assert_r2a_doc()
    import r2a_images_fusion as I
    a = None
    for cand in LOOK_CANDIDATES:
        a = a or I._appearance(cand)
    n = 0
    if a is not None:
        for o in L.all_root_occs():
            if B.base_name(o.component.name) in LOOK['POC']:
                if o.appearance is None or o.appearance.name != a.name:
                    o.appearance = a
                    n += 1
    L.add_knee_ref()
    L.ref_assert()
    return n


def _frame(path, occs, moves=(), eye=(0.7, 1.0, 0.55), target=(40.0, 80.0, -60.0),
           extents=330.0, pose=(0.0, 80.0), size=(1500, 1100)):
    import r2a_images_fusion as I
    keep = {o.entityToken for o in occs}
    saved = [(o, o.isLightBulbOn) for o in L.all_root_occs()]
    undo = []
    try:
        for o in L.all_root_occs():
            o.isLightBulbOn = o.entityToken in keep
        L.r2a_pose(*pose)
        for names, vec in moves:
            undo += _offset(names, vec)
        vp = I.camera(eye, target, extents)
        return I.save(vp, path, *size)
    finally:
        for o, m in undo:
            o.transform2 = B._as_matrix(m)
        L.r2a_restore()
        L.restore_bulbs(saved)


def _offset(items, vec):
    toks = {i.entityToken for i in items if hasattr(i, 'entityToken')}
    names = {i for i in items if isinstance(i, str)}
    undo = []
    for o in L.all_root_occs():
        nm = B.base_name(o.component.name)
        t1 = o.attributes.itemByName('R2A', 'set')
        t2 = o.attributes.itemByName('POC', 'set')
        if o.entityToken in toks or nm in names or (t1 and t1.value in names) or \
                (t2 and t2.value in names):
            m = list(o.transform2.asArray())
            undo.append((o, list(m)))
            m[3] += vec[0] / 10.0
            m[7] += vec[1] / 10.0
            m[11] += vec[2] / 10.0
            o.transform2 = B._as_matrix(m)
    return undo


def images(ids=None):
    """POC guide images from the live model (presentation only)."""
    L.assert_r2a_doc()
    L.capture_nominal(force=True)
    P = L.PART
    poc = [o for o in poc_set()]
    no_cable = [o for o in poc if not B.base_name(o.component.name).startswith('REFERENCE_Cable')
                and B.base_name(o.component.name) != LOCK_PIN]
    mock = [o for n in MOCK + (LOCK_PIN,) for o in _mods(n)] + _set_occs(SET_KNOB)
    out = []
    frames = [
        ('P00_poc_leg', no_cable, [], (0.55, 1.0, 0.45), (20.0, 60.0, -70.0), 420.0, (0.0, 80.0)),
        ('P01_mock_actuator', mock, [(( KNOB, KEY_DOWEL, SET_KNOB, LOCK_PIN), (0, 30, 0)),
                                     ((ROTOR, ROTOR_DOWELS), (0, -30, 0))],
         (0.8, 0.6, 0.7), (0.0, 100.0, 0.0), 180.0, (0.0, 80.0)),
        ('P02_dial', mock, [], (0.35, 1.0, 0.45), (0.0, 116.0, 0.0), 105.0, (0.0, 80.0)),
        ('P03_mock_on_outboard_half', [o for o in no_cable if B.base_name(o.component.name) in
                                       (P['OUTB'], P['CRANK'], BUSHING) + MOCK] +
         _set_occs(SET_KNOB) + [o for o in no_cable if o.attributes.itemByName('R2A', 'set') and
                                o.attributes.itemByName('R2A', 'set').value in
                                ('R2A_SHCS_M3x10_Actuator', 'R2A_SHCS_M3x10_Crank')],
         [((P['CRANK'], 'R2A_SHCS_M3x10_Crank'), (0, -30, 0))],
         (0.6, -1.0, 0.5), (0.0, 85.0, 0.0), 230.0, (0.0, 80.0)),
        ('P04_pushrod_and_pins', [o for o in no_cable if B.base_name(o.component.name) in
                                  (PUSHROD, PIN_CRANK, PIN_LEVER)], [],
         (0.0, -1.0, 0.0), (60.0, 75.0, -20.0), 170.0, (0.0, 80.0)),
        ('P05_linkage_a051', [o for o in no_cable if B.base_name(o.component.name) not in
                              (P['OUTB'], 'RIG_Stand', 'RIG_Cable_Post_A', 'RIG_Cable_Anchor_ModeA',
                               GAUGE, PROTRACTOR) + MOCK + (LOCK_PIN,)
                              and not (o.attributes.itemByName('POC', 'set') and
                                       o.attributes.itemByName('POC', 'set').value == SET_PROT)
                              and not (o.attributes.itemByName('R2A', 'set') and
                                       o.attributes.itemByName('R2A', 'set').value in
                                       ('R2A_SHCS_M3x10_Actuator', 'R2A_SHCS_M3x12_Perimeter'))],
         [], (0.0, 1.0, 0.0), (45.0, 80.0, -70.0), 330.0, (0.0, 51.0)),
        ('P06_protractor', no_cable, [], (0.3, 1.0, 0.35), (L.KX, 94.0, L.KZ), 125.0, (0.0, 80.0)),
        ('P07_flexion_stop_gauge', no_cable, [], (0.0, 1.0, 0.25), (35.0, 80.0, -40.0), 260.0,
         (0.0, 51.0)),
        ('P08_extension_stop', no_cable, [], (0.0, 1.0, 0.0), (60.0, 80.0, -120.0), 380.0,
         (0.0, 150.0)),
        ('P09_wheel_screws', [o for o in no_cable if B.base_name(o.component.name) in
                              (P['DIST'], WASHER, SCREW_M25, 'REF_GIM4305-10')],
         [((WASHER, SET_M25), (0, -15, 0))], (0.6, -1.0, 0.4), (B.WX, 60.0, B.WZ), 150.0,
         (0.0, 80.0)),
        ('P10_service', no_cable, [(tuple(poc_module()) + tuple(
            [o for o in no_cable if B.base_name(o.component.name) in
             ('REF_GIM4305-10', 'Wheel_Hub_L', 'ABS_TEST_Wheel_Rim_NoTyre', GAUGE, WASHER)]) +
            tuple(_set_occs(SET_M25)), (0, 45, 0)),
            ((PROTRACTOR, SET_PROT, P['ENC_ARM'], 'R2A_SHCS_M3x10_EncArm'), (0, 110, 0)),
            (('HW_DowelPin_D10x35',), (0, 60, 0))],
         (0.7, 1.0, 0.5), (40.0, 100.0, -60.0), 460.0, (0.0, 80.0)),
    ]
    for fid, occs, moves, eye, target, ext, pose in frames:
        if ids and fid not in ids:
            continue
        out.append(_frame(os.path.join(GUIDE_DIR, fid + '.png'), occs, moves, eye, target, ext, pose))
    return out
