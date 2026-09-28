"""Builders, poses and audits for the R2A active-knee single-leg article.

Execute only through the Fusion MCP, with the separate `Beni_R2A_SingleLeg`
document active.  Every public entry point that can change the model calls
`assert_r2a_doc()` first; the legacy `Beni_SingleLegRig` and `Beni_Prototype1`
documents are never edited.

Conventions follow beni_lib / rig_lib: X forward, Y outboard (+Y), Z up, the
shoulder axis is the global Y axis, millimetres.  The proximal-link frame
(u, v) has u along shoulder S -> knee K and v = beni_lib.PV (+v is the side
away from the folding distal link); XZ angle = (u, v) angle - 40 deg.  The
distal frame (du, dv) is beni_lib.dist_uv(): du along K -> wheel at the build
pose, dv = du + 90 deg.

The build pose is the legacy nominal: shoulder theta = 0 and knee alpha = 80
deg (legacy phi = 80 - alpha).  Every part is modelled in place at that pose and
posed afterwards by composing group transforms onto the captured nominal
transforms (see `r2a_pose`).

Geometry decisions and why they were taken are recorded next to the constants
and in docs/design/active_knee_revision2_plan.md.  Linkage dimensions are the
r2a_calc.py selection; nothing here re-derives them.
"""

import json
import math
import os
import time

import adsk.core
import adsk.fusion

import beni_lib as B
import rig_lib as R

DOC = 'Beni_R2A_SingleLeg'
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

# ----------------------------------------------------------------- guards
def assert_r2a_doc():
    """Abort unless the active document is the R2A copy.  Never bypass."""
    name = adsk.core.Application.get().activeDocument.name
    if name != DOC:
        raise RuntimeError('R2A scripts may only run in %s (active: %s)'
                           % (DOC, name))
    return True


# ====================================================== linkage (r2a_calc.py)
# Selected by r2a_calc.py (crank a, rod b, lever c, lever offset delta).
CRANK_A = 32.0
ROD_B = 120.0
LEVER_C = 30.0
LEVER_DELTA = -12.0          # theta_lever = alpha + delta in the (u, v) frame
BRANCH = 1
L1 = B.L1                    # 120.0 shoulder -> knee
ALPHA_NOM = 80.0             # build pose; legacy phi = 80 - alpha
ALPHA_FLEX_STOP = 51.0
ALPHA_EXT_STOP = 150.0
OVERTRAVEL = 2.0


def uv(u, v):
    return B.prox_uv(u, v)


def uv_inv(x, z):
    return B.prox_inv(x, z)


def knee_uv():
    return (L1, 0.0)


def solve(alpha):
    """Crank-pin C and lever-pin P in (u, v), crank angle (deg), for alpha.

    Scalar copy of r2a_calc.solve_linkage() (same formula, same branch).
    """
    th_l = math.radians(alpha + LEVER_DELTA)
    px = L1 + LEVER_C * math.cos(th_l)
    py = LEVER_C * math.sin(th_l)
    dd = math.hypot(px, py)
    cosg = (CRANK_A ** 2 + dd ** 2 - ROD_B ** 2) / (2 * CRANK_A * dd)
    if abs(cosg) > 1.0:
        raise ValueError('linkage cannot assemble at alpha %.2f' % alpha)
    th_c = math.atan2(py, px) + BRANCH * math.acos(cosg)
    cx, cy = CRANK_A * math.cos(th_c), CRANK_A * math.sin(th_c)
    return (cx, cy), (px, py), math.degrees(th_c)


C0_UV, P0_UV, THC0 = solve(ALPHA_NOM)
C0 = uv(*C0_UV)                       # global XZ of the crank pin, build pose
P0 = uv(*P0_UV)                       # global XZ of the lever pin, build pose
KX, KZ = B.KX, B.KZ


def xz_angle_of_uv(a_deg):
    return a_deg - 40.0


# ============================================================== lateral stack
# Legacy datums inboard of the knee are unchanged (design record §3).  The
# knee stack moves +0.8 mm in Y relative to the legacy rig so that BOTH link
# halves print on one flat bed face each: the inboard half on its y = 59.5 hub
# face, the outboard half on its y = 91.1 actuator face.  Every fit keeps its
# legacy diameter and length (6800 seat Ø19.15 x 5, lip Ø17 x 0.8, receiver
# Ø10.30 x 20.0, 0.8 mm bearing-to-receiver gaps); only positions move.
Y_IN = 59.5                  # leg inboard face = hub outboard face
Y_CH0 = 64.5                 # inboard cheek channel face (root, walls)
Y_CH1 = 84.5                 # outboard cheek channel face = wall tops
Y_OUT = 91.1                 # outboard face = knee-actuator mount face
BRG_A = (59.5, 64.5)
LIP_A = (64.5, 65.3)
RECV = (65.3, 85.3)
DBOSS = (65.8, 84.8)
LIP_B = (85.3, 86.1)
BRG_B = (86.1, 91.1)
KNEE_BOSS_R = 17.5           # proximal knee boss radius in the distal sweep
BRG_SEAT_D = B.ABS_KNEE_BRG_SEAT_D      # 19.15, owner-selected ABS seat
LIP_D = B.KNEE_LIP_D                    # 17.0
RECV_D = B.ABS_KNEE_PIN_BORE_D          # 10.30, owner-selected ABS receiver
PIN_D10_LEN = 35.0

# M4 hub screws: the legacy joint is kept exactly -- M4 x 10 SHCS, head seat
# y 63.3 in a Ø7.5 counterbore, 6.2 mm into the hub's M4 x 8 insert.  The
# heads therefore stand to y 67.3 inside the channel.
M4_SEAT_Y = 63.3
M4_CB_D = 7.5

# Rod plane and clevis ears.  The crank's inboard ear (a separate cap) sits
# 1.0 mm above the M4 head tops; the outboard ears stop 1.1 mm short of the
# outboard cheek face.  The 8.4 mm ball gap accepts a rod-end inner ring up to
# B = 8.0 with 0.2 mm per side.
EAR_IN = (68.3, 71.3)        # crank inboard ear (R2A_Crank_Cap_L)
LEVER_IN = (65.8, 71.3)      # lever inboard ear/arm, integral to the distal
GAP = (71.3, 79.7)
EAR_OUT = (79.7, 83.4)       # crank slab ear / R2A_Lever_Cap_L
Y_ROD = 0.5 * (GAP[0] + GAP[1])          # 75.5
NECK_BAND = (Y_ROD - 5.3, Y_ROD + 5.3)   # neck R4.5 / M5 nut R4.62 + >= 0.68 mm

# Knee actuator (second GIM6010-8, same STEP as REF_GIM6010-8).
ACT_MOUNT_Y = Y_OUT                       # housing mount face
ACT_OUT_Y = ACT_MOUNT_Y - 3.5             # 87.6 output mount face
ACT_PIN_TIP_Y = ACT_MOUNT_Y - 7.0         # 84.1
ACT_HOUSING_Y = (ACT_MOUNT_Y + 1.0, ACT_MOUNT_Y + 25.0)
ACT_COVER_Y = (ACT_MOUNT_Y + 26.0, ACT_MOUNT_Y + 37.0)
# Clocking about the actuator axis, XZ-angle sense.  Puts three of the eight
# Ø74 housing threads inside the crank sweep (left empty) and five outside it,
# with 17.5 deg of margin at both sector edges, and points the driver-cover
# cable notch at the root back wall.  Verified by probing the placed STEP.
ACT_CLOCK = 161.2
ACT_SCREW_UV = (358.6, 178.6, 223.6, 268.6, 313.6)   # (u, v) deg, R37
ACT_SCREW_EMPTY_UV = (43.6, 88.6, 133.6)
ACT_PCD = 74.0

# Crank body (one flat slab on the output face) and pocket in the cheek.
CRANK_SLAB = (EAR_OUT[0], ACT_OUT_Y)      # 79.7 .. 87.6
CRANK_M3_SEAT_Y = ACT_OUT_Y - 5.0         # 82.6, shoulder-hub clamp length
CHEEK_POCKET_FLOOR = 88.4                 # 0.8 mm running gap over the slab
CRANK_HEAD_R = 12.5
CRANK_ARM_HW = 10.0

# Clevis pins and cap dowels.
PIN5_D, PIN5_LEN = 5.0, 18.0
PIN5_HOLE_D = 5.15           # [DESIGN - COUPON] ladder 5.05..5.25 selects
DOWEL_D, DOWEL_LEN = 4.0, 10.0
DOWEL_HOLE_D = 4.25          # owner root-ladder press selection (2026-09-22)
EYE_CLR = 1.0                # eye-to-C-wall radial clearance

# Rod-end design envelope (requirement on the purchased part, not vendor
# data): M5 female, bore Ø5, inner ring B <= 8.0, housing <= 6 wide and
# <= Ø18, neck <= Ø9, pin centre to shank end 27, female thread >= 10 deep.
RE_EYE_D, RE_EYE_W = 18.0, 6.0
RE_BALL_D, RE_BALL_W = 11.0, 8.0
RE_NECK_D, RE_H = 9.0, 27.0
RE_THREAD_DEPTH = 10.0
NUT_AF, NUT_T = 8.0, 2.7     # ISO 4035 M5 thin nut envelope
ROD_D = 5.0
ROD_LEN = ROD_B - 2 * RE_H + 2 * RE_THREAD_DEPTH   # 86.0

# Knee stops: radial faces through the knee axis.
STOP_FLEX_UV = 210.0          # proximal flexion face, (u, v) deg from K
STOP_EXT_UV = 20.0            # proximal extension face
DIST_FLEX_REL = -21.0         # distal faces, degrees from du
DIST_EXT_REL = 50.0
STOP_R0, STOP_R1 = 19.0, 40.0
TPU_D, TPU_INSET, TPU_R = 6.0, 2.0, 30.0   # plug protrudes 1.0 mm

# Proximal outline.
ROOT_R = 50.5                 # +v side and back
ROOT_R_TYRE = 42.0            # tyre side at the flexion stop
BOTTOM_TANGENT_R = 41.0       # bottom edge tangent circle (tyre gap)
KNEE_CHEEK_R = 36.0           # retains the lever pin over its arc
ROOF_V = (44.0, 48.0)
ROOF_U_END = 95.0
BACK_WALL_R = (46.5, 50.5)
FLOOR_T = 4.0
FLOOR_U = (14.0, 86.0)
# Cable duct on the shin (-v) side of the rod, inside the proximal box: floor
# wall below, duct wall above; the wheel cable enters through the inboard
# cheek, the AS5048A cable through the outboard cheek, both leave through a
# notch in the root back wall.
DUCT_WALL_V = (-3.0, -1.0)
DUCT_U = (42.0, 86.0)            # starts clear of the 358.6 deg actuator screw head
DUCT_ENTRY_IN_UV = (80.0, -9.0)
DUCT_ENTRY_OUT_UV = (82.0, -9.0)
DUCT_ENTRY_D = 8.0
DUCT_EXIT_UV_DEG = 222.0          # past the back wall's 215 deg end: no notch
CABLE_Y = (66.5, 83.0)            # usable duct height between M4 heads and M3 heads
# mid-link lightening window in both cheeks (clear of both pins and the duct)
WINDOW_UV = ((46.0, 10.0), (76.0, 10.0), 20.0)   # v 0..20: 1 mm above the duct wall

# Encoder stack.  The Ø10 x 35 knee pin sits flush with bearing B's outer
# face and protrudes 3.4 mm inboard, where R2A_Knee_Pin_Cap_L stops it; the
# encoder arm clears its outboard end by 0.5 mm.
PIN_Y = (BRG_B[1] - PIN_D10_LEN, BRG_B[1])   # 56.1 .. 91.1
PIN_CAP_GAP = 0.5
ENC_ARM_Y = (91.6, 95.4)
ENC_PAD_Y1 = 91.0            # distal outboard pads for the arm (89.5 .. 91.0)
ENC_ARM_PAD_Y0 = ENC_PAD_Y1
MAG_D, MAG_T = 6.1, 2.5
ENC_DIE_GAP = 1.0             # design record §3, legacy air gap


# ================================================================ naming
PART = dict(
    INB='R2A_Prox_Inboard_L', OUTB='R2A_Prox_Outboard_L',
    CRANK='R2A_Crank_L', CRANK_CAP='R2A_Crank_Cap_L',
    DIST='R2A_Distal_Link_L', LEVER_CAP='R2A_Lever_Cap_L',
    TPU='R2A_Knee_Bumper_TPU', ENC_ARM='R2A_Encoder_Arm_L',
    ENC_BRACKET='R2A_Encoder_Bracket_L', PIN_CAP='R2A_Knee_Pin_Cap_L',
    KNEE_REF='REF_GIM6010-8',
)

# Parts of the passive-knee article that R2A removes from its copy.
PASSIVE_PARTS = (
    'Knee_Spring_L', 'REFERENCE_Owned_Spring_Envelope_OD18_ID9_L50',
    'ABS_TEST_Cart_Upper_Eye_50mm', 'ABS_TEST_Cart_Lower_Eye_50mm',
    'ABS_TEST_Cart_Guide_Bar_50mm', 'ABS_TEST_Knee_Stop_Plate_15deg',
    'ABS_TEST_Knee_Pin_Outboard_Spacer', 'Cart_Upper_Eye_L',
    'Cart_Lower_Eye_L', 'Cart_Guide_Rod_L', 'Cart_Preload_Shim_L',
    'HW_ClevisPin_M4x40', 'HW_Washer_M4', 'HW_WasherStack_M5',
    'RIG_Knee_Bumper_Tube_L', 'RIG_Knee_Stop_Plate_L', 'HW_DowelPin_D6x10',
    'RIG_Torque_Arm', 'RIG_Scale_Pedestal', 'RIG_Floor_Plate',
    'Proximal_Link_L',
    'Distal_Link_L', 'Knee_Encoder_Bracket_L', 'Knee_Encoder_PCB_L',
    'HW_Magnet_D6x2p5_Diametric', 'HW_DowelPin_D10x35', 'RIG_Knee_Collar_L',
    'RIG_Knee_Magnet_Carrier_L', 'HW_Bearing_6800',
)
# Individual occurrences of shared screw components that belonged to the
# legacy stop plate and encoder bracket (the component also serves others).
PASSIVE_SCREW_OCCS = ('HW_SHCS_M3x10 (10):17', 'HW_SHCS_M3x10 (10):18',
                      'HW_SHCS_M3x10 (10):19', 'HW_SHCS_M3x16 (10):2',
                      'HW_SHCS_M3x16 (10):3')


# ============================================================ small helpers
def bodies_of(comp):
    return [comp.bRepBodies.item(i) for i in range(comp.bRepBodies.count)]


def tag(occ, cls):
    """Record the R2A pose class on the occurrence (persisted in the doc)."""
    a = occ.attributes.itemByName('R2A', 'pose')
    if a:
        a.value = cls
    else:
        occ.attributes.add('R2A', 'pose', cls)
    return occ


def pose_class(occ):
    a = occ.attributes.itemByName('R2A', 'pose')
    return a.value if a else None


def all_root_occs():
    r = B.root()
    return [r.occurrences.item(i) for i in range(r.occurrences.count)]


def ref_occs():
    """(shoulder, knee) REF_GIM6010-8 occurrences, identified by position."""
    sh = kn = None
    for o in all_root_occs():
        if B.base_name(o.component.name) != 'REF_GIM6010-8':
            continue
        cls = pose_class(o)
        if cls == 'PROX':
            kn = o
        else:
            sh = sh or o
    return sh, kn


def ref_assert(verbose=False):
    """Both legacy REF guards, plus the knee actuator's own Y span."""
    R.ref_assert(verbose=verbose)
    _, kn = ref_occs()
    if kn is not None:
        b = B.bbox_of(kn)
        want = (ACT_PIN_TIP_Y, ACT_COVER_Y[1])
        if abs(b[2] - want[0]) > 0.05 or abs(b[3] - want[1]) > 0.05:
            raise RuntimeError('knee REF displaced: Y %.2f..%.2f want %.2f..%.2f'
                               % (b[2], b[3], want[0], want[1]))
    return True


def guarded(fn, *a, **kw):
    """rig_lib.guarded() plus the knee-REF guard.  Structural work only."""
    assert_r2a_doc()
    out = R.guarded(fn, *a, **kw)
    ref_assert()
    return out


def path_profile(comp, y, segs, start):
    """Closed sketch loop from global XZ segments.

    segs: list of ('L', end) or ('A', mid, end); start is the first point.
    Returns the sketch (single loop expected)."""
    sk = B.sk_on_y(comp, y)
    ln = sk.sketchCurves.sketchLines
    ar = sk.sketchCurves.sketchArcs
    cur = start
    for s in segs:
        if s[0] == 'L':
            ln.addByTwoPoints(B.sxz(*cur), B.sxz(*s[1]))
            cur = s[1]
        else:
            ar.addByThreePoints(B.sxz(*cur), B.sxz(*s[1]), B.sxz(*s[2]))
            cur = s[2]
    return sk


def polar(c, r, a_deg):
    a = math.radians(a_deg)
    return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))


def kuv(r, a_uv):
    """Global XZ of a point r from the knee at (u, v) angle a_uv."""
    return polar((KX, KZ), r, xz_angle_of_uv(a_uv))


def suv(r, a_uv):
    """Global XZ of a point r from the shoulder at (u, v) angle a_uv."""
    return polar((0.0, 0.0), r, xz_angle_of_uv(a_uv))


def dist_xz(r, rel_deg):
    """Global XZ at the build pose of a distal point r from K at du + rel."""
    return polar((KX, KZ), r, 220.0 + rel_deg)


def ext(comp, sk, y0, y1, op='new', prof=None, participants=None):
    """Extrude a sketch made on the plane y = y0 to y1 (y1 may be < y0).

    Cut and intersect default to the owning component's own bodies: the
    beni_lib default already scopes cuts; the explicit list is passed so a
    cut can never reach another component (the September 23 regression)."""
    prof = prof if prof is not None else B.biggest_profile(sk)
    if op in ('cut', 'inter') and participants is None:
        participants = bodies_of(comp)
    return B.extrude(comp, prof, y1 - y0, op=op, participants=participants)


# ================================================================ cleanup
def strip_passive(verbose=True):
    """Delete the passive-knee parts under the transform guard."""
    assert_r2a_doc()

    def work():
        gone = {}
        for nm in PASSIVE_PARTS:
            k = B.drop_comp(nm)
            if k:
                gone[nm] = k
        for occ_name in PASSIVE_SCREW_OCCS:
            for o in all_root_occs():
                if o.name == occ_name:
                    o.deleteMe()
                    gone[occ_name] = 1
        return gone
    gone = R.guarded(work)
    B.capture_nominal(force=True)
    if verbose:
        print(json.dumps(gone))
    return gone


# ======================================================= knee reference motor
def knee_ref_matrix(sh):
    """Top-level transform for the knee REF, composed onto the shoulder REF's.

    The linked STEP carries a child transform, so the placement is expressed
    as a global map G applied to the shoulder occurrence's transform2:
    G = translate(Y 42 + 91.1) . rotate(clock about Y) . rotate(180 about Z).
    A shoulder feature at XZ angle psi lands at 180 - psi + ACT_CLOCK; the
    shoulder mount face (y 42, output +Y) lands at y 91.1 facing -Y."""
    c = math.radians(ACT_CLOCK)
    g = [-math.cos(c), 0.0, -math.sin(c), 0.0,
         0.0, -1.0, 0.0, B.cm(B.SHOULDER_Y + ACT_MOUNT_Y),
         -math.sin(c), 0.0, math.cos(c), 0.0,
         0.0, 0.0, 0.0, 1.0]
    return B._as_matrix(B._mm(g, list(sh.transform2.asArray())))


def add_knee_ref():
    """Second occurrence of the GIM6010-8 STEP, output facing inboard."""
    assert_r2a_doc()
    sh, kn = ref_occs()
    m = knee_ref_matrix(sh)
    if kn is None:
        kn = B.root().occurrences.addExistingComponent(sh.component, m)
        tag(kn, 'PROX')
    else:
        kn.transform2 = m
    return kn


# =========================================================== knee hardware
def build_knee_hardware():
    """Two 6800-2RS envelopes and the owned Ø10 x 35 pin at the R2A stack."""
    assert_r2a_doc()
    B.drop_comp('HW_Bearing_6800')
    o = B.new_comp('HW_Bearing_6800')
    B.ring(o.component, BRG_A[0], B.KNEE_AXLE_D / 2.0, B.KNEE_BRG_OD / 2.0,
           B.KNEE_BRG_W, 'new', cx=KX, cz=KZ).bodies.item(0).name = 'HW_Bearing_6800'
    tag(o, 'PROX')
    m = B.mat((1, 0, 0), (0, 1, 0), (0, 0, 1), (0.0, BRG_B[0] - BRG_A[0], 0.0))
    tag(B.root().occurrences.addExistingComponent(o.component, m), 'PROX')
    B.drop_comp('HW_DowelPin_D10x35')
    o = B.new_comp('HW_DowelPin_D10x35')
    B.cyl_y(o.component, None, KX, KZ, B.KNEE_AXLE_D, PIN_Y[0], PIN_Y[1])
    o.component.bRepBodies.item(0).name = 'HW_DowelPin_D10x35'
    tag(o, 'DIST')
    return True


# ========================================================= proximal outline
def _circle_line_hits(p0, p1, r):
    """Parameters t of |p0 + t (p1 - p0)| = r."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    a = dx * dx + dy * dy
    b = 2 * (p0[0] * dx + p0[1] * dy)
    c = p0[0] ** 2 + p0[1] ** 2 - r * r
    disc = b * b - 4 * a * c
    if disc < 0:
        return []
    s = math.sqrt(disc)
    return sorted(((-b - s) / (2 * a), (-b + s) / (2 * a)))


def prox_outline_uv():
    """Cheek outline in (u, v): list of ('L', pt) / ('A', mid, pt), start pt.

    Root R50.5 on the +v side and back; R42 on the tyre side; bottom edge
    tangent to R41 from the flexion-face end (5 mm tyre gap at the flexion
    stop); flexion face (u, v) 210 deg; knee boss R17.5 through the distal
    sweep; extension face 20 deg; R36 knee cheek retaining the lever pin; top
    edge v = 48 back to the root."""
    k = knee_uv()
    th_a = math.degrees(math.asin(ROOF_V[1] / ROOT_R))
    a = polar((0, 0), ROOT_R, th_a)
    th_b = 262.0
    fend = polar(k, STOP_R1, STOP_FLEX_UV)
    d = math.hypot(*fend)
    psi_q = math.degrees(math.atan2(fend[1], fend[0]))
    psi_t = psi_q - math.degrees(math.acos(BOTTOM_TANGENT_R / d))
    t_pt = polar((0, 0), BOTTOM_TANGENT_R, psi_t)
    ts = _circle_line_hits(fend, t_pt, ROOT_R_TYRE)
    t_i = [t for t in ts if 0.0 < t < 1.0][0]
    ipt = (fend[0] + t_i * (t_pt[0] - fend[0]), fend[1] + t_i * (t_pt[1] - fend[1]))
    th_i = math.degrees(math.atan2(ipt[1], ipt[0])) % 360.0
    th_c = 268.0
    q = (ROOF_U_END, ROOF_V[1])
    qk = math.hypot(q[0] - k[0], q[1] - k[1])
    ang_q = math.degrees(math.atan2(q[1] - k[1], q[0] - k[0]))
    th_j = ang_q - math.degrees(math.acos(KNEE_CHEEK_R / qk))
    segs = [
        ('A', polar((0, 0), ROOT_R, 0.5 * (th_a + th_b)), polar((0, 0), ROOT_R, th_b)),
        ('L', polar((0, 0), ROOT_R_TYRE, th_c)),
        ('A', polar((0, 0), ROOT_R_TYRE, 0.5 * (th_c + th_i)), ipt),
        ('L', fend),
        ('L', polar(k, KNEE_BOSS_R, STOP_FLEX_UV)),
        ('A', polar(k, KNEE_BOSS_R, 0.5 * (STOP_FLEX_UV + STOP_EXT_UV + 360.0)),
         polar(k, KNEE_BOSS_R, STOP_EXT_UV)),
        ('L', polar(k, KNEE_CHEEK_R, STOP_EXT_UV)),
        ('A', polar(k, KNEE_CHEEK_R, 0.5 * (STOP_EXT_UV + th_j)),
         polar(k, KNEE_CHEEK_R, th_j)),
        ('L', q),
        ('L', a),
    ]
    info = dict(th_a=th_a, th_b=th_b, th_i=th_i, th_j=th_j, fend=fend,
                tangent=t_pt, psi_t=psi_t)
    return a, segs, info


def _to_xz(start, segs):
    s = uv(*start)
    out = []
    for g in segs:
        if g[0] == 'L':
            out.append(('L', uv(*g[1])))
        else:
            out.append(('A', uv(*g[1]), uv(*g[2])))
    return s, out


def prox_outline_xz():
    a, segs, _ = prox_outline_uv()
    return _to_xz(a, segs)


def bottom_edge_uv():
    _, _, info = prox_outline_uv()
    return info['tangent'], info['fend']


def _bottom_point(u):
    t_pt, fend = bottom_edge_uv()
    f = (u - t_pt[0]) / (fend[0] - t_pt[0])
    return (t_pt[0] + f * (fend[0] - t_pt[0]), t_pt[1] + f * (fend[1] - t_pt[1]))


def _bottom_normal():
    t_pt, fend = bottom_edge_uv()
    dx, dy = fend[0] - t_pt[0], fend[1] - t_pt[1]
    n = math.hypot(dx, dy)
    return (-dy / n, dx / n)       # inward (+v side)


def tpu_centre_uv(face):
    """Ø6 TPU plug centre, TPU_INSET inside the named stop face."""
    k = knee_uv()
    if face == 'flex':
        p = polar(k, TPU_R, STOP_FLEX_UV)
        return polar(p, TPU_INSET, STOP_FLEX_UV - 90.0)
    p = polar(k, TPU_R, STOP_EXT_UV)
    return polar(p, TPU_INSET, STOP_EXT_UV + 90.0)


# Perimeter screw positions, (u, v): roof, back wall, floor.
def perimeter_screws_uv():
    pts = [(50.0, ROOF_V[1] - 4.5), (80.0, ROOF_V[1] - 4.5),
           polar((0, 0), 46.0, 185.0), polar((0, 0), 46.0, 205.0)]
    n = _bottom_normal()
    for u in (58.0, 70.0):
        p = _bottom_point(u)
        pts.append((p[0] + 4.5 * n[0], p[1] + 4.5 * n[1]))
    return pts


def _sk_poly_uv(comp, y, pts_uv):
    sk = B.sk_on_y(comp, y)
    B.polyline(sk, [uv(*p) for p in pts_uv])
    return sk


def _annular_sector_uv(comp, y, c_uv, r0, r1, a0_uv, a1_uv):
    sk = B.sk_on_y(comp, y)
    c = uv(*c_uv)
    B.arc_sector(sk, c[0], c[1], r0, r1, xz_angle_of_uv(a0_uv), xz_angle_of_uv(a1_uv))
    return sk


def _cheek(comp, y0, y1, op='new'):
    start, segs = prox_outline_xz()
    sk = path_profile(comp, y0, segs, start)
    e = ext(comp, sk, y0, y1, op)
    return e


def _circles(comp, y0, y1, pts_xz, d, op='cut'):
    sk = B.sk_on_y(comp, y0)
    for p in pts_xz:
        B.circle(sk, p[0], p[1], d)
    return ext(comp, sk, y0, y1, op, prof=B.profiles(sk))


def m4_hub_screw_xz():
    return [polar((0, 0), B.HUB_LINK_PCD / 2.0, B.HUB_LINK_A0 + 60.0 * i)
            for i in range(6)]


def root_dowel_xz():
    return [polar((0, 0), B.ROOT_DOWEL_PCD / 2.0, a) for a in B.ROOT_DOWEL_A]


def enc_insert_xz():
    return [B.kpt(15.0, 60.0), B.kpt(15.0, 140.0)]


def pin_cap_insert_xz():
    return [kuv(13.5, 100.0), kuv(13.5, 180.0)]


# ============================================================ inboard half
def build_inboard_half():
    """R2A_Prox_Inboard_L: y 59.5 cheek, walls to 84.5, bearing A, hub joint."""
    assert_r2a_doc()
    name = PART['INB']
    B.drop_comp(name)
    occ = B.new_comp(name)
    c = occ.component
    e = _cheek(c, Y_IN, Y_CH0, 'new')
    e.bodies.item(0).name = name
    sk = B.sk_on_y(c, Y_CH0)
    B.circle(sk, KX, KZ, 2 * KNEE_BOSS_R)
    ext(c, sk, Y_CH0, LIP_A[1], 'join')
    # walls: roof, back wall, floor
    ext(c, _sk_poly_uv(c, Y_CH0, [(17.0, ROOF_V[0]), (ROOF_U_END, ROOF_V[0]),
                                   (ROOF_U_END, ROOF_V[1]), (17.0, ROOF_V[1])]),
        Y_CH0, Y_CH1, 'join')
    ext(c, _annular_sector_uv(c, Y_CH0, (0, 0), BACK_WALL_R[0], BACK_WALL_R[1],
                              62.0, 215.0), Y_CH0, Y_CH1, 'join')
    n = _bottom_normal()
    p0, p1 = _bottom_point(FLOOR_U[0]), _bottom_point(FLOOR_U[1])
    quad = [(p0[0] - 0.3 * n[0], p0[1] - 0.3 * n[1]), (p1[0] - 0.3 * n[0], p1[1] - 0.3 * n[1]),
            (p1[0] + FLOOR_T * n[0], p1[1] + FLOOR_T * n[1]),
            (p0[0] + FLOOR_T * n[0], p0[1] + FLOOR_T * n[1])]
    ext(c, _sk_poly_uv(c, Y_CH0, quad), Y_CH0, Y_CH1, 'join')
    # cable duct wall
    ext(c, _sk_poly_uv(c, Y_CH0, [(DUCT_U[0], DUCT_WALL_V[0]), (DUCT_U[1], DUCT_WALL_V[0]),
                                   (DUCT_U[1], DUCT_WALL_V[1]), (DUCT_U[0], DUCT_WALL_V[1])]),
        Y_CH0, Y_CH1, 'join')
    # screw bosses on the walls
    sk = B.sk_on_y(c, Y_CH0)
    for p in perimeter_screws_uv():
        q = uv(*p)
        B.circle(sk, q[0], q[1], 9.0)
    ext(c, sk, Y_CH0, Y_CH1, 'join', prof=B.profiles(sk))
    # trim anything that grew outside the cheek outline
    _trim_to_outline(c, Y_IN - 1.0, Y_CH1 + 1.0)
    # bearing A seat and lip
    _circles(c, BRG_A[0] - 1.0, BRG_A[1], [(KX, KZ)], BRG_SEAT_D)
    _circles(c, BRG_A[1] - 0.5, LIP_A[1] + 1.0, [(KX, KZ)], LIP_D)
    # hub joint: 6 x M4 clearance + counterbores, 3 x root dowel through-holes
    _circles(c, Y_IN - 1.0, Y_CH0 + 1.0, m4_hub_screw_xz(), 4.3)
    _circles(c, M4_SEAT_Y, Y_CH0 + 1.0, m4_hub_screw_xz(), M4_CB_D)
    _circles(c, Y_IN - 1.0, Y_CH0 + 1.0, root_dowel_xz(), B.ROOT_DOWEL_LINK_SOCKET_D)
    # TPU stop plugs, blind from the inboard (bed) face, 1.0 mm floor
    _circles(c, Y_IN - 1.0, Y_CH0 - 1.0,
             [uv(*tpu_centre_uv('flex')), uv(*tpu_centre_uv('ext'))], TPU_D)
    # knee-pin cap inserts, blind from the bed face, 0.8 mm floor
    _circles(c, Y_IN - 1.0, Y_IN + B.INSERT_LEN, pin_cap_insert_xz(),
             B.M3_INSERT_RECEIVER_D)
    # perimeter M3 insert pockets, blind from the wall tops
    _circles(c, Y_CH1 - B.FRAME_INSERT_HOLE_DEPTH, Y_CH1 + 1.0,
             [uv(*p) for p in perimeter_screws_uv()], B.FRAME_INSERT_D)
    _cable_features(c, Y_IN - 1.0, Y_CH0, DUCT_ENTRY_IN_UV)
    tag(occ, 'PROX')
    return occ


def _trim_to_outline(comp, y0, y1):
    """Intersect every body with the cheek outline prism (scoped)."""
    start, segs = prox_outline_xz()
    sk = path_profile(comp, y0, segs, start)
    ext(comp, sk, y0, y1, 'inter', participants=bodies_of(comp))


# =========================================================== outboard half
def crank_pocket_sector_uv():
    """(u, v) angular range of the crank's swept slab, with margin."""
    lo = solve(ALPHA_FLEX_STOP - OVERTRAVEL)[2]
    hi = solve(ALPHA_EXT_STOP + OVERTRAVEL)[2]
    # arm half-width at the Ø48 bore edge (asin(10/23) = 25.8) and the +100
    # deg cap-dowel boss (31.5) set the two margins; the empty housing
    # threads sit outside with >= 4 deg to spare
    return lo - 28.0, hi + 33.0


def build_outboard_half():
    """R2A_Prox_Outboard_L: 84.5..91.1 cheek, actuator mount, bearing B."""
    assert_r2a_doc()
    name = PART['OUTB']
    B.drop_comp(name)
    occ = B.new_comp(name)
    c = occ.component
    e = _cheek(c, Y_CH1, Y_OUT, 'new')
    e.bodies.item(0).name = name
    # knee recess to the lip face, bearing B seat and lip
    _circles(c, Y_CH1 - 1.0, LIP_B[0], [(KX, KZ)], 2 * KNEE_BOSS_R)
    _circles(c, BRG_B[0], Y_OUT + 1.0, [(KX, KZ)], BRG_SEAT_D)
    _circles(c, LIP_B[0] - 1.0, BRG_B[0] + 0.5, [(KX, KZ)], LIP_D)
    # actuator bore and crank pocket
    _circles(c, Y_CH1 - 1.0, Y_OUT + 1.0, [(0.0, 0.0)], 48.0)
    lo, hi = crank_pocket_sector_uv()
    ext(c, _annular_sector_uv(c, Y_CH1 - 1.0, (0, 0), 23.0, 46.0, lo, hi),
        Y_CH1 - 1.0, CHEEK_POCKET_FLOOR, 'cut')
    # 5 x M3 actuator clearance, 6 x perimeter clearance
    _circles(c, Y_CH1 - 1.0, Y_OUT + 1.0,
             [suv(ACT_PCD / 2.0, a) for a in ACT_SCREW_UV], 3.4)
    _circles(c, Y_CH1 - 1.0, Y_OUT + 1.0,
             [uv(*p) for p in perimeter_screws_uv()], 3.4)
    # encoder bracket inserts and TPU plugs, blind from the bed face
    _circles(c, Y_OUT - B.ENC_INSERT_DEPTH, Y_OUT + 1.0, enc_insert_xz(),
             B.M3_INSERT_RECEIVER_D)
    _circles(c, Y_CH1 + 1.0, Y_OUT + 1.0,
             [uv(*tpu_centre_uv('flex')), uv(*tpu_centre_uv('ext'))], TPU_D)
    _cable_features(c, Y_CH1, Y_OUT + 1.0, DUCT_ENTRY_OUT_UV)
    tag(occ, 'PROX')
    return occ


def _cable_features(c, y0, y1, entry_uv):
    """Mid-link lightening window and a duct entry hole through a cheek."""
    (a0, a1, w) = WINDOW_UV
    p0, p1 = uv(*a0), uv(*a1)
    sk = B.sk_on_y(c, y0); B.slot(sk, p0[0], p0[1], p1[0], p1[1], w)
    ext(c, sk, y0, y1, 'cut')
    _circles(c, y0, y1, [uv(*entry_uv)], DUCT_ENTRY_D)


# ================================================================ crank
FAN_RHO = (5.0, 30.0)        # neck relief starts 1 mm inside the envelope's neck
FAN_HW = RE_NECK_D / 2.0 + 1.0
FAN_MARGIN = 4.0             # deg, rod-end swivel allowance each side
SWEEP = (ALPHA_FLEX_STOP - OVERTRAVEL - 1.0, ALPHA_EXT_STOP + OVERTRAVEL + 1.0)


def _uv_dir(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))


def fan_range(which):
    """XZ direction range of the rod-end neck in the build-pose frame of the
    crank ('crank') or the lever ('lever') over the whole sweep."""
    vals = []
    a = SWEEP[0]
    while a <= SWEEP[1] + 1e-9:
        c, p, thc = solve(a)
        if which == 'crank':
            rel = _uv_dir(c, p) - (thc - THC0)
        else:
            rel = _uv_dir(p, c) - (a - ALPHA_NOM)
        vals.append(rel)
        a += 0.5
    lo = min(vals) - FAN_MARGIN - 40.0
    hi = max(vals) + FAN_MARGIN - 40.0
    return lo, hi


def fan_polygon_xz(pc, lo, hi, rho=FAN_RHO, hw=FAN_HW, n=18):
    """Conservative polygon covering every neck strip rotated over [lo, hi]."""
    r0, r1 = rho
    def u(a):
        return (math.cos(math.radians(a)), math.sin(math.radians(a)))
    def pt(r, a, off):
        d = u(a)
        t = (-d[1], d[0])
        return (pc[0] + r * d[0] + off * t[0], pc[1] + r * d[1] + off * t[1])
    pts = [pt(r0, lo, -hw), pt(r1 + hw, lo, -hw)]
    for i in range(n + 1):
        a = lo + (hi - lo) * i / n
        pts.append(pt(r1 + hw, a, 0.0))
    pts += [pt(r1 + hw, hi, hw), pt(r0, hi, hw)]
    for i in range(n, -1, -1):
        a = lo + (hi - lo) * i / n
        pts.append(pt(r0 - 0.01, a, 0.0))
    return pts


def _dowel_xz(pc, arm_xz, rels, rho=14.0):
    return [polar(pc, rho, arm_xz + r) for r in rels]


CRANK_DOWEL_REL = (100.0, 160.0)     # from the crank's outward radial
LEVER_DOWEL_REL = (-100.0, -160.0)   # mirror side on the lever
DOWEL_BOSS_R = 3.75
HEAD_R = 13.0


def crank_arm_xz():
    return xz_angle_of_uv(THC0)


def build_crank():
    """R2A_Crank_L (slab + C-wall) and R2A_Crank_Cap_L (inboard ear)."""
    assert_r2a_doc()
    arm = crank_arm_xz()
    lo, hi = fan_range('crank')
    fan = fan_polygon_xz(C0, lo, hi)
    dowels = _dowel_xz(C0, arm, CRANK_DOWEL_REL)
    # ---- body
    name = PART['CRANK']
    B.drop_comp(name)
    occ = B.new_comp(name)
    c = occ.component
    y0, y1 = CRANK_SLAB
    e = _circles(c, y0, y1, [(0.0, 0.0)], 38.0, 'new')
    e.bodies.item(0).name = name
    t = (-math.sin(math.radians(arm)), math.cos(math.radians(arm)))
    strip = [(t[0] * CRANK_ARM_HW, t[1] * CRANK_ARM_HW),
             (C0[0] + t[0] * CRANK_ARM_HW, C0[1] + t[1] * CRANK_ARM_HW),
             (C0[0] - t[0] * CRANK_ARM_HW, C0[1] - t[1] * CRANK_ARM_HW),
             (-t[0] * CRANK_ARM_HW, -t[1] * CRANK_ARM_HW)]
    sk = B.sk_on_y(c, y0); B.polyline(sk, strip); ext(c, sk, y0, y1, 'join')
    _circles(c, y0, y1, [C0], 2 * HEAD_R, 'join')
    _circles(c, y0, y1, dowels, 2 * DOWEL_BOSS_R, 'join')
    # C-wall (grows from the slab toward the rod plane)
    _circles(c, GAP[0], y0, [C0], 2 * HEAD_R, 'join')
    _circles(c, GAP[0], y0, dowels, 2 * DOWEL_BOSS_R, 'join')
    _circles(c, GAP[0], y0, [C0], RE_EYE_D + 2 * EYE_CLR, 'cut')
    sk = B.sk_on_y(c, GAP[0]); B.polyline(sk, fan)
    ext(c, sk, GAP[0], NECK_BAND[1], 'cut')          # C-wall and slab recess
    # output interface: the printed shoulder hub's, at the knee REF's pattern
    _circles(c, y0 - 1.0, y1 + 1.0, [(0.0, 0.0)], 12.0)
    m3 = [polar((0, 0), B.SH_OUT_PCD / 2.0, 10.8 + 60.0 * i) for i in range(6)]
    pins = [polar((0, 0), B.SH_PIN_PCD / 2.0, 41.0 + 120.0 * i) for i in range(3)]
    _circles(c, y0 - 1.0, y1 + 1.0, m3, 3.4)
    _circles(c, y0 - 1.0, CRANK_M3_SEAT_Y, m3, 6.2)
    _circles(c, y0 - 1.0, y1 + 1.0, pins, B.ABS_SHOULDER_PIN_BORE_D)
    _circles(c, y1 - 0.7, y1 + 1.0, pins, 5.2)
    # clevis pin: blind from the rod plane side, 1.0 mm skin at the output face
    _circles(c, GAP[0] - 1.0, y1 - 1.0, [C0], PIN5_HOLE_D)
    # cap dowel sockets, blind upward from the C-wall face
    _circles(c, GAP[0] - 1.0, GAP[0] + 7.0, dowels, DOWEL_HOLE_D)
    tag(occ, 'CRANK')
    # ---- cap
    cap = PART['CRANK_CAP']
    B.drop_comp(cap)
    oc = B.new_comp(cap)
    cc = oc.component
    e = _circles(cc, EAR_IN[0], EAR_IN[1], [C0], 2 * HEAD_R, 'new')
    e.bodies.item(0).name = cap
    _circles(cc, EAR_IN[0], EAR_IN[1], dowels, 2 * DOWEL_BOSS_R, 'join')
    sk = B.sk_on_y(cc, NECK_BAND[0]); B.polyline(sk, fan)
    ext(cc, sk, NECK_BAND[0], EAR_IN[1] + 1.0, 'cut')
    _circles(cc, EAR_IN[0] - 1.0, EAR_IN[1] + 1.0, [C0], PIN5_HOLE_D)
    _circles(cc, EAR_IN[0] - 1.0, EAR_IN[1] + 1.0, dowels, DOWEL_HOLE_D)
    tag(oc, 'CRANK')
    return occ, oc


# ============================================================ distal link
def dpol(r, rel):
    """(du, dv) of a point r from K at du + rel (distal build frame)."""
    return (r * math.cos(math.radians(rel)), r * math.sin(math.radians(rel)))


def _dxz(p):
    return B.dist_uv(*p)


def _tangent_from(p, c, r, lower=True):
    """Tangent point on circle (c, r) seen from p (distal frame, 2D)."""
    dx, dy = p[0] - c[0], p[1] - c[1]
    d = math.hypot(dx, dy)
    a = math.atan2(dy, dx)
    b = math.acos(r / d)
    t = a + b if lower else a - b
    return (c[0] + r * math.cos(t), c[1] + r * math.sin(t))


def distal_block_segs():
    """Near-knee full-width block with radial stop faces at du-21 and du+50."""
    p1, p2 = dpol(STOP_R0, DIST_FLEX_REL), dpol(STOP_R1, DIST_FLEX_REL)
    p3, p4 = dpol(STOP_R0, DIST_EXT_REL), dpol(STOP_R1, DIST_EXT_REL)
    tw = _tangent_from(p2, (120.0, 0.0), B.DL_WHL_R, lower=False)
    if tw[1] > 0:
        tw = _tangent_from(p2, (120.0, 0.0), B.DL_WHL_R, lower=True)
    pts = [p1, p2, tw, (120.0, 0.0), B.DL_ARM_C, p4, p3]
    segs = [('L', _dxz(q)) for q in pts[1:]]
    segs.append(('A', _dxz(dpol(STOP_R0, 0.5 * (DIST_FLEX_REL + DIST_EXT_REL))),
                 _dxz(p1)))
    return _dxz(p1), segs


def lever_arm_xz():
    return xz_angle_of_uv(ALPHA_NOM + LEVER_DELTA)      # 28 deg


ENC_ARM_REL = 15.0
ENC_INSERTS_D = [dpol(27.0, 0.0), dpol(27.0, 30.0)]
ENC_DOWEL_D = dpol(34.0, ENC_ARM_REL)


def build_distal_link():
    """R2A_Distal_Link_L and R2A_Lever_Cap_L."""
    assert_r2a_doc()
    name = PART['DIST']
    B.drop_comp(name)
    occ = B.new_comp(name)
    c = occ.component
    y0, y1 = B.LEG_Y_IN, B.LEG_Y_OUT
    sk = B.sk_on_y(c, y0)
    B.lozenge(sk, B.DL_ARM_C, B.DL_ARM_R, (120.0, 0.0), B.DL_WHL_R, frame=B.dist_uv)
    e = ext(c, sk, y0, y1, 'new')
    e.bodies.item(0).name = name
    start, segs = distal_block_segs()
    ext(c, path_profile(c, y0, segs, start), y0, y1, 'join')
    # legacy U-channel from du = 22
    pts = [(B.DL_CUT_U0, B.dl_epd(B.DL_CUT_U0) - B.DL_WT),
           (132.0, B.dl_epd(132.0) - B.DL_WT), (132.0, -62.0), (B.DL_CUT_U0, -62.0)]
    sk = B.sk_on_y(c, B.CH_Y0); B.polyline(sk, [_dxz(q) for q in pts])
    ext(c, sk, B.CH_Y0, B.CH_Y1, 'cut')
    # knee boss, web sector and receiver ring
    sk = B.sk_on_y(c, DBOSS[0])
    B.lozenge(sk, (0.0, 0.0), B.DBOSS_D / 2.0, B.DL_WEB_C, B.DL_WEB_R, frame=B.dist_uv)
    ext(c, sk, DBOSS[0], DBOSS[1], 'join')
    sk = B.sk_on_y(c, DBOSS[0])
    B.polyline(sk, [(KX, KZ), _dxz(dpol(23.0, DIST_FLEX_REL)),
                    _dxz(dpol(23.0, 14.5)), _dxz(dpol(23.0, DIST_EXT_REL))])
    ext(c, sk, DBOSS[0], DBOSS[1], 'join')
    _circles(c, RECV[0], RECV[1], [(KX, KZ)], 16.0, 'join')
    # lever: arm + head (inboard ear level), C-wall with dowel bosses
    arm = lever_arm_xz()
    t = (-math.sin(math.radians(arm)), math.cos(math.radians(arm)))
    hw = 12.0
    strip = [(KX + t[0] * hw, KZ + t[1] * hw), (P0[0] + t[0] * hw, P0[1] + t[1] * hw),
             (P0[0] - t[0] * hw, P0[1] - t[1] * hw), (KX - t[0] * hw, KZ - t[1] * hw)]
    sk = B.sk_on_y(c, LEVER_IN[0]); B.polyline(sk, strip)
    ext(c, sk, LEVER_IN[0], LEVER_IN[1], 'join')
    _circles(c, LEVER_IN[0], LEVER_IN[1], [P0], 2 * HEAD_R, 'join')
    dowels = _dowel_xz(P0, arm, LEVER_DOWEL_REL)
    # the C-wall's dowel bosses stand on matching bosses (no overhang in print)
    _circles(c, LEVER_IN[0], LEVER_IN[1], dowels, 2 * DOWEL_BOSS_R, 'join')
    _circles(c, GAP[0], GAP[1], [P0], 2 * HEAD_R, 'join')
    _circles(c, GAP[0], GAP[1], dowels, 2 * DOWEL_BOSS_R, 'join')
    _circles(c, GAP[0], GAP[1], [P0], RE_EYE_D + 2 * EYE_CLR, 'cut')
    lo, hi = fan_range('lever')
    fan = fan_polygon_xz(P0, lo, hi)
    sk = B.sk_on_y(c, NECK_BAND[0]); B.polyline(sk, fan)
    ext(c, sk, NECK_BAND[0], GAP[1], 'cut')
    _circles(c, LEVER_IN[0] - 1.0, GAP[0] + 0.5, [P0], PIN5_HOLE_D)
    _circles(c, GAP[1] - 6.3, GAP[1] + 1.0, dowels, DOWEL_HOLE_D)
    # wheel end (legacy)
    _circles(c, B.CH_Y0, B.WM_MOUNT_Y, [(B.WX, B.WZ)], B.WM_PLATE_D, 'join')
    _circles(c, B.WM_MOUNT_Y, y1 + 1.0, [(B.WX, B.WZ)], 112.0)
    _circles(c, y0 - 1.0, B.WM_MOUNT_Y + 2.0, [(B.WX, B.WZ)], B.WM_COVER_D)
    wm = [polar((B.WX, B.WZ), B.WM_BOLT_PCD / 2.0, B.WM_BOLT_A0 + 60.0 * i) for i in range(6)]
    _circles(c, y0 - 1.0, B.WM_MOUNT_Y + 2.0, wm, 2.8)
    lw = [polar((B.WX, B.WZ), 26.0, B.WM_BOLT_A0 + 30.0 + 60.0 * i) for i in range(6)]
    _circles(c, y0 - 1.0, B.WM_MOUNT_Y + 2.0, lw, 9.0)
    for (u0, v0, u1, v1, w) in [(64.0, -6.0, 96.0, -5.0, 16.0),
                                (46.0, 26.0, 94.0, 15.0, 12.0)]:
        sk = B.sk_on_y(c, y0 - 1.0)
        a0, a1 = B.dist_uv(u0, v0), B.dist_uv(u1, v1)
        B.slot(sk, a0[0], a0[1], a1[0], a1[1], w)
        ext(c, sk, y0 - 1.0, y1 + 1.0, 'cut')
    # encoder-arm attachment: 1.5 mm pads on the outboard face (inside the
    # block's angular range), insert pockets 5.5 deep, dowel socket 5.0 deep.
    # Nothing hangs into the U-channel, so its ceiling support slides out.
    att = [_dxz(p) for p in ENC_INSERTS_D + [ENC_DOWEL_D]]
    _circles(c, y1, ENC_PAD_Y1, att, 10.0, 'join')
    _circles(c, ENC_PAD_Y1 - 5.5, ENC_PAD_Y1 + 1.0, att[:2], B.M3_INSERT_RECEIVER_D)
    _circles(c, ENC_PAD_Y1 - 5.0, ENC_PAD_Y1 + 1.0, att[2:], DOWEL_HOLE_D)
    # confine the full-width side plates to du-21 .. du+50 near the knee: the
    # proximal cheeks occupy every other direction at some knee angle
    for band in ((B.LEG_Y_IN - 0.1, B.CH_Y0 + 0.2), (B.CH_Y1 - 0.5, B.LEG_Y_OUT + 0.1)):
        sk = B.sk_on_y(c, band[0])
        pts = [_dxz(dpol(11.0, DIST_EXT_REL)), _dxz(dpol(60.0, DIST_EXT_REL))]
        for i in range(1, 12):
            a = DIST_EXT_REL + (360.0 + DIST_FLEX_REL - DIST_EXT_REL) * i / 12.0
            pts.append(_dxz(dpol(60.0 / math.cos(math.radians(15.0)), a)))
        pts += [_dxz(dpol(60.0, 360.0 + DIST_FLEX_REL)),
                _dxz(dpol(11.0, 360.0 + DIST_FLEX_REL))]
        for i in range(11, 0, -1):
            a = DIST_EXT_REL + (360.0 + DIST_FLEX_REL - DIST_EXT_REL) * i / 12.0
            pts.append(_dxz(dpol(11.0, a)))
        B.polyline(sk, pts)
        ext(c, sk, band[0], band[1], 'cut')
    # wheel-cable tie slots through the inboard side plate (pairs, 6 mm apart)
    for du in (40.0, 52.0):
        for dv in (-5.0, -11.0):
            a0, a1 = B.dist_uv(du - 1.75, dv), B.dist_uv(du + 1.75, dv)
            sk = B.sk_on_y(c, y0 - 1.0); B.slot(sk, a0[0], a0[1], a1[0], a1[1], 2.0)
            ext(c, sk, y0 - 1.0, B.CH_Y0 + 0.5, 'cut')
    # channel-band sliver of the legacy arm circle beyond the extension face
    sk = B.sk_on_y(c, B.CH_Y0 - 0.1)
    B.polyline(sk, [_dxz(dpol(23.0, DIST_EXT_REL)), _dxz(dpol(62.0, DIST_EXT_REL)),
                    _dxz(dpol(62.0, DIST_EXT_REL + 20.0)), _dxz(dpol(23.0, DIST_EXT_REL + 20.0))])
    ext(c, sk, B.CH_Y0 - 0.1, B.CH_Y1 + 0.1, 'cut')
    # knee receiver bore last, through the ring
    _circles(c, RECV[0] - 1.0, RECV[1] + 1.0, [(KX, KZ)], RECV_D)
    tag(occ, 'DIST')
    # ---- lever cap (outboard ear)
    cap = PART['LEVER_CAP']
    B.drop_comp(cap)
    oc = B.new_comp(cap)
    cc = oc.component
    e = _circles(cc, EAR_OUT[0], EAR_OUT[1], [P0], 2 * HEAD_R, 'new')
    e.bodies.item(0).name = cap
    _circles(cc, EAR_OUT[0], EAR_OUT[1], dowels, 2 * DOWEL_BOSS_R, 'join')
    sk = B.sk_on_y(cc, EAR_OUT[0] - 1.0); B.polyline(sk, fan)
    ext(cc, sk, EAR_OUT[0] - 1.0, NECK_BAND[1], 'cut')
    _circles(cc, EAR_OUT[0] - 1.0, EAR_OUT[1] + 1.0, [P0], PIN5_HOLE_D)
    _circles(cc, EAR_OUT[0] - 1.0, EAR_OUT[1] + 1.0, dowels, DOWEL_HOLE_D)
    tag(oc, 'DIST')
    return occ, oc


# ============================================================ hardware
def _tm():
    return adsk.fusion.TemporaryBRepManager.get()


def _p(x, y, z):
    return adsk.core.Point3D.create(x / 10.0, y / 10.0, z / 10.0)


def _cyl(a, b, d):
    """Temporary solid cylinder between global points a and b (mm)."""
    return _tm().createCylinderOrCone(_p(*a), d / 20.0, _p(*b), d / 20.0)


def _union(bodies):
    out = bodies[0]
    for b in bodies[1:]:
        assert _tm().booleanOperation(out, b, adsk.fusion.BooleanTypes.UnionBooleanType)
    return out


def _cut(body, tool):
    assert _tm().booleanOperation(body, tool, adsk.fusion.BooleanTypes.DifferenceBooleanType)
    return body


def _base_comp(name, body, cls, material=None):
    B.drop_comp(name)
    occ = B.new_comp(name)
    c = occ.component
    base = c.features.baseFeatures.add()
    base.startEdit()
    b = c.bRepBodies.add(body, base)
    base.finishEdit()
    c.bRepBodies.item(0).name = name
    if material:
        B.set_material(c, c.bRepBodies.item(0), material)
    tag(occ, cls)
    return occ


def _rod_end_body(pc, toward):
    """M5 female rod-end design envelope at pin centre pc (XZ), neck toward."""
    x, z = pc
    y = Y_ROD
    dx, dz = toward[0] - x, toward[1] - z
    n = math.hypot(dx, dz)
    ux, uz = dx / n, dz / n
    eye = _cyl((x, y - RE_EYE_W / 2, z), (x, y + RE_EYE_W / 2, z), RE_EYE_D)
    ball = _cyl((x, y - RE_BALL_W / 2, z), (x, y + RE_BALL_W / 2, z), RE_BALL_D)
    neck = _cyl((x + 6.0 * ux, y, z + 6.0 * uz), (x + RE_H * ux, y, z + RE_H * uz), RE_NECK_D)
    body = _union([eye, ball, neck])
    _cut(body, _cyl((x, y - 10, z), (x, y + 10, z), PIN5_D))
    _cut(body, _cyl((x + (RE_H - RE_THREAD_DEPTH) * ux, y, z + (RE_H - RE_THREAD_DEPTH) * uz),
                    (x + (RE_H + 1) * ux, y, z + (RE_H + 1) * uz), ROD_D))
    return body


def build_rod():
    """Pushrod group at the build pose: two rod-end envelopes, rod, nuts."""
    assert_r2a_doc()
    x0, z0 = C0
    x1, z1 = P0
    L = math.hypot(x1 - x0, z1 - z0)
    ux, uz = (x1 - x0) / L, (z1 - z0) / L
    y = Y_ROD
    _base_comp('HW_RodEnd_M5_Upper', _rod_end_body(C0, P0), 'ROD', 'Steel')
    _base_comp('HW_RodEnd_M5_Lower', _rod_end_body(P0, C0), 'ROD', 'Steel')
    s0 = RE_H - RE_THREAD_DEPTH
    rod = _cyl((x0 + s0 * ux, y, z0 + s0 * uz), (x0 + (s0 + ROD_LEN) * ux, y,
               z0 + (s0 + ROD_LEN) * uz), ROD_D)
    _base_comp('HW_Rod_M5x86', rod, 'ROD', 'Steel')
    nut_d = NUT_AF / math.cos(math.radians(30.0))
    n1 = _cyl((x0 + RE_H * ux, y, z0 + RE_H * uz),
              (x0 + (RE_H + NUT_T) * ux, y, z0 + (RE_H + NUT_T) * uz), nut_d)
    n2 = _cyl((x1 - RE_H * ux, y, z1 - RE_H * uz),
              (x1 - (RE_H + NUT_T) * ux, y, z1 - (RE_H + NUT_T) * uz), nut_d)
    for b in (n1, n2):
        _cut(b, _cyl((x0 - 500 * ux, y, z0 - 500 * uz), (x0 + 500 * ux, y, z0 + 500 * uz), ROD_D))
    _base_comp('HW_JamNut_M5', _union([n1, n2]), 'ROD', 'Steel')
    return L


def build_pins():
    """Ø5 x 18 clevis pins, cap dowels, TPU stop plugs."""
    assert_r2a_doc()
    ymid = 0.5 * (Y_CH0 + Y_CH1)
    for nm, pc, cls in (('HW_Pin_D5x18_Crank', C0, 'CRANK'),
                        ('HW_Pin_D5x18_Lever', P0, 'DIST')):
        _base_comp(nm, _cyl((pc[0], ymid - PIN5_LEN / 2, pc[1]),
                            (pc[0], ymid + PIN5_LEN / 2, pc[1]), PIN5_D), cls, 'Steel')
    cd = _dowel_xz(C0, crank_arm_xz(), CRANK_DOWEL_REL)
    ld = _dowel_xz(P0, lever_arm_xz(), LEVER_DOWEL_REL)
    b = _union([_cyl((p[0], EAR_IN[0], p[1]), (p[0], EAR_IN[0] + DOWEL_LEN, p[1]), DOWEL_D)
                for p in cd])
    _base_comp('HW_DowelPin_D4x10_Crank', b, 'CRANK', 'Steel')
    b = _union([_cyl((p[0], EAR_OUT[1] - DOWEL_LEN, p[1]), (p[0], EAR_OUT[1], p[1]), DOWEL_D)
                for p in ld])
    _base_comp('HW_DowelPin_D4x10_Lever', b, 'DIST', 'Steel')
    ed = _dxz(ENC_DOWEL_D)
    _base_comp('HW_DowelPin_D4x10_EncArm',
               _cyl((ed[0], ENC_PAD_Y1 - 5.0, ed[1]), (ed[0], ENC_PAD_Y1 + 5.0, ed[1]),
                    DOWEL_D), 'DIST', 'Steel')
    f, x = uv(*tpu_centre_uv('flex')), uv(*tpu_centre_uv('ext'))
    B.drop_comp(PART['TPU'])
    tp = [_cyl((p[0], Y_IN, p[1]), (p[0], Y_CH0 - 1.0, p[1]), TPU_D) for p in (f, x)]
    _base_comp(PART['TPU'] + '_In', _union(tp), 'PROX')
    tp = [_cyl((p[0], Y_CH1 + 1.0, p[1]), (p[0], Y_CH1 + 5.0, p[1]), TPU_D) for p in (f, x)]
    _base_comp(PART['TPU'] + '_Out', _union(tp), 'PROX')
    return True


# ================================================================ encoder
ENC_ARM_PLATE = (ENC_ARM_Y[0], 97.3)      # arm plate; magnet face at 97.3
ENC_MAG = (ENC_ARM_PLATE[1] - MAG_T, ENC_ARM_PLATE[1])
ENC_DIE = (ENC_ARM_PLATE[1] + ENC_DIE_GAP, ENC_ARM_PLATE[1] + ENC_DIE_GAP + 1.0)
ENC_PCB = (ENC_DIE[1], ENC_DIE[1] + 1.6)  # legacy 14 x 14 x 1.6 envelope
ENC_BRACKET_PLATE = (ENC_PCB[1], ENC_PCB[1] + 2.0)


def build_encoder():
    """Distal-keyed magnet arm, AS5048A bracket, PCB and magnet envelopes.

    The arm bolts to the distal link, so the magnet reads the distal link
    directly and never the (freely turning) Ø10 pin; it also stops the pin
    0.5 mm beyond bearing B.  The bracket keeps the legacy two-post pattern on
    the outboard cheek's kpt(15, 60/140) inserts, outside the arm's sweep."""
    assert_r2a_doc()
    name = PART['ENC_ARM']
    B.drop_comp(name)
    occ = B.new_comp(name)
    c = occ.component
    y0, y1 = ENC_ARM_PLATE
    e = _circles(c, y0, y1, [(KX, KZ)], 14.0, 'new')
    e.bodies.item(0).name = name
    tip = _dxz(dpol(36.0, ENC_ARM_REL))
    a = math.atan2(tip[1] - KZ, tip[0] - KX)
    t = (-math.sin(a), math.cos(a))
    hw = 7.0
    strip = [(KX + t[0] * hw, KZ + t[1] * hw), (tip[0] + t[0] * hw, tip[1] + t[1] * hw),
             (tip[0] - t[0] * hw, tip[1] - t[1] * hw), (KX - t[0] * hw, KZ - t[1] * hw)]
    sk = B.sk_on_y(c, y0); B.polyline(sk, strip); ext(c, sk, y0, y1, 'join')
    att = [_dxz(p) for p in ENC_INSERTS_D + [ENC_DOWEL_D]]
    _circles(c, y0, y1, att, 10.0, 'join')
    _circles(c, ENC_ARM_PAD_Y0, y0, att, 10.0, 'join')
    _circles(c, ENC_MAG[0], y1 + 1.0, [(KX, KZ)], MAG_D)
    _circles(c, ENC_ARM_PAD_Y0 - 1.0, y1 + 1.0, att[:2], 3.4)
    _circles(c, ENC_ARM_PAD_Y0 - 1.0, y1 + 1.0, att[2:], 4.30)
    tag(occ, 'DIST')
    _base_comp('HW_Magnet_D6x2p5_Diametric',
               _cyl((KX, ENC_MAG[0], KZ), (KX, ENC_MAG[1], KZ), 6.0), 'DIST')
    # PCB envelope (beni_lib.build_encoder): 14 x 14 board, 5 x 5 x 1 die
    pcb = _tm().createBox(adsk.core.OrientedBoundingBox3D.create(
        _p(KX, 0.5 * (ENC_PCB[0] + ENC_PCB[1]), KZ), adsk.core.Vector3D.create(1, 0, 0),
        adsk.core.Vector3D.create(0, 0, 1), 1.4, 1.4, (ENC_PCB[1] - ENC_PCB[0]) / 10.0))
    die = _tm().createBox(adsk.core.OrientedBoundingBox3D.create(
        _p(KX, 0.5 * (ENC_DIE[0] + ENC_DIE[1]), KZ), adsk.core.Vector3D.create(1, 0, 0),
        adsk.core.Vector3D.create(0, 0, 1), 0.5, 0.5, 0.1))
    _base_comp('HW_AS5048A_PCB', _union([pcb, die]), 'PROX')
    # bracket: two posts on the legacy inserts, plate over the axis
    bn = PART['ENC_BRACKET']
    B.drop_comp(bn)
    ob = B.new_comp(bn)
    cb = ob.component
    e = _circles(cb, ENC_BRACKET_PLATE[0], ENC_BRACKET_PLATE[1], [(KX, KZ)], 34.0, 'new')
    e.bodies.item(0).name = bn
    _circles(cb, Y_OUT, ENC_BRACKET_PLATE[0], enc_insert_xz(), 9.0, 'join')
    _circles(cb, Y_OUT - 1.0, ENC_BRACKET_PLATE[1] + 1.0, enc_insert_xz(), 3.4)
    _circles(cb, ENC_BRACKET_PLATE[0] - 1.0, ENC_BRACKET_PLATE[1] + 1.0, [(KX, KZ)], 8.0)
    # lead notch from the centre to the plate edge toward the cable route
    a = xz_angle_of_uv(205.0)
    tt = (-math.sin(math.radians(a)), math.cos(math.radians(a)))
    far = polar((KX, KZ), 20.0, a)
    sk = B.sk_on_y(cb, ENC_BRACKET_PLATE[0] - 1.0)
    B.polyline(sk, [(KX + 3 * tt[0], KZ + 3 * tt[1]), (far[0] + 3 * tt[0], far[1] + 3 * tt[1]),
                    (far[0] - 3 * tt[0], far[1] - 3 * tt[1]), (KX - 3 * tt[0], KZ - 3 * tt[1])])
    ext(cb, sk, ENC_BRACKET_PLATE[0] - 1.0, ENC_BRACKET_PLATE[1] + 1.0, 'cut')
    tag(ob, 'PROX')
    # inboard knee-pin cap
    pn = PART['PIN_CAP']
    B.drop_comp(pn)
    op = B.new_comp(pn)
    cp = op.component
    y0 = PIN_Y[0] - PIN_CAP_GAP - 2.0          # 53.6
    e = _circles(cp, y0, Y_IN, [(KX, KZ)], 34.0, 'new')
    e.bodies.item(0).name = pn
    _circles(cp, PIN_Y[0] - PIN_CAP_GAP, Y_IN + 1.0, [(KX, KZ)], 15.0)
    _circles(cp, y0 - 1.0, Y_IN + 1.0, pin_cap_insert_xz(), 3.4)
    _circles(cp, y0 - 1.0, y0 + 3.0, pin_cap_insert_xz(), 6.0)
    tag(op, 'PROX')
    return True


# ============================================================ fasteners
SCREW_SETS = {
    # name: (component, d, L, flip, y_seat, points, class)
}


def screw_sets():
    act = [suv(ACT_PCD / 2.0, a) for a in ACT_SCREW_UV]
    per = [uv(*p) for p in perimeter_screws_uv()]
    crank = [polar((0, 0), B.SH_OUT_PCD / 2.0, 10.8 + 60.0 * i) for i in range(6)]
    arm = [_dxz(p) for p in ENC_INSERTS_D]
    wm = [polar((B.WX, B.WZ), B.WM_BOLT_PCD / 2.0, B.WM_BOLT_A0 + 60.0 * i) for i in range(6)]
    return [
        # M3 x 10, not x 12: 3.4 mm into the ~4.0 mm housing thread.  The
        # delivered-actuator test found a 5.0 mm protrusion bottoms (beni_lib
        # build_hardware: "x10 bottoms before the 5 mm panel clamps"); x 12
        # through the 6.6 mm cheek would protrude 5.4 mm.
        ('R2A_SHCS_M3x10_Actuator', 'HW_SHCS_M3x10', 3.0, 10.0, True, Y_CH1, act, 'PROX'),
        ('R2A_SHCS_M3x12_Perimeter', 'HW_SHCS_M3x12', 3.0, 12.0, False, Y_OUT, per, 'PROX'),
        ('R2A_SHCS_M3x10_Crank', 'HW_SHCS_M3x10', 3.0, 10.0, True, CRANK_M3_SEAT_Y, crank, 'CRANK'),
        ('R2A_SHCS_M3x10_EncArm', 'HW_SHCS_M3x10', 3.0, 10.0, False, ENC_ARM_PLATE[1], arm, 'DIST'),
        ('R2A_SHCS_M3x16_Bracket', 'HW_SHCS_M3x16', 3.0, 16.0, False, ENC_BRACKET_PLATE[1],
         enc_insert_xz(), 'PROX'),
        ('R2A_SHCS_M3x6_PinCap', 'HW_SHCS_M3x6', 3.0, 6.0, True, PIN_Y[0] - PIN_CAP_GAP + 1.0,
         pin_cap_insert_xz(), 'PROX'),
        # wheel motor: the legacy M2.5 x 12 through the 8.0 mm wheel-end plate
        # reaches 1.0 mm past the floor of the STEP's Ø2.0 x 3.0 holes
        # (y 67.5..70.5, measured 2026-09-27); x 10 stops 1.0 mm short of it
        ('R2A_SHCS_M2p5x10_WheelMotor', 'HW_SHCS_M2p5x10', 2.5, 10.0, True, B.LEG_Y_IN, wm, 'DIST'),
    ]


def build_fasteners():
    """Place every R2A screw as addExistingComponent (not transform2) occurrences."""
    assert_r2a_doc()
    placed = {}
    for o in all_root_occs():
        if o.attributes.itemByName('R2A', 'set') or \
                B.base_name(o.component.name) == 'HW_SHCS_M2p5x12':
            o.deleteMe()           # the legacy wheel-motor screws are replaced
    for label, comp, d, L, flip, y, pts, cls in screw_sets():
        master = B.screw_comp(comp, d, L)
        occs = []
        for (x, z) in pts:
            o = B.place(master, x, z, y, flip=flip)
            o.attributes.add('R2A', 'set', label)
            tag(o, cls)
            occs.append(o)
        placed[label] = len(occs)
    # screw_comp leaves its master at the origin: remove it unless placed
    for comp in ('HW_SHCS_M3x12', 'HW_SHCS_M3x6', 'HW_SHCS_M2p5x10'):
        for o in all_root_occs():
            if B.base_name(o.component.name) == comp and o.attributes.itemByName('R2A', 'set') is None:
                o.deleteMe()
    return placed


# ============================================================ classification
WHEEL_PREFIXES = ('Wheel_', 'ABS_TEST_Wheel')


def classify_legacy():
    """Tag every untagged occurrence with its R2A pose class (legacy rules)."""
    assert_r2a_doc()
    n = 0
    for o in all_root_occs():
        if pose_class(o):
            continue
        nm = B.base_name(o.component.name)
        if any(nm.startswith(p) for p in WHEEL_PREFIXES):
            cls = 'DIST'
        else:
            cls = B.classify(o)
            cls = cls if cls in ('STATIC', 'PROX', 'DIST') else 'STATIC'
        tag(o, cls)
        n += 1
    return n


# ================================================================ posing
def rod_frame(alpha):
    c, p, _ = solve(alpha)
    cx, cz = uv(*c)
    px, pz = uv(*p)
    return (cx, cz), math.degrees(math.atan2(pz - cz, px - cx))


_ROD0 = rod_frame(ALPHA_NOM)


def group_matrices(theta, alpha):
    """Row-major 16-arrays (cm) for every pose class."""
    _, _, thc = solve(alpha)
    sh = B._rot_arr(theta, 0.0, 0.0)
    crank = B._rot_arr(-(thc - THC0), 0.0, 0.0)
    dist = B._rot_arr(ALPHA_NOM - alpha, KX, KZ)
    (cx, cz), psi = rod_frame(alpha)
    (c0x, c0z), psi0 = _ROD0
    rod = B._mm(B._trans_arr((cx - c0x, 0.0, cz - c0z)),
                B._rot_arr(-(psi - psi0), c0x, c0z))
    ident = B._trans_arr((0.0, 0.0, 0.0))
    return {'STATIC': ident, 'PROX': sh, 'CRANK': B._mm(sh, crank),
            'ROD': B._mm(sh, rod), 'DIST': B._mm(sh, dist)}


_NOM = {}


def capture_nominal(force=False):
    """Nominal (build-pose) transforms, keyed by entity token."""
    global _NOM
    if _NOM and not force:
        return _NOM
    _NOM = {o.entityToken: list(o.transform2.asArray()) for o in all_root_occs()}
    return _NOM


def r2a_pose(theta, alpha):
    """Pose the leg: shoulder theta (deg, beni_lib sense) and knee alpha."""
    nom = capture_nominal()
    g = group_matrices(theta, alpha)
    for o in all_root_occs():
        cls = pose_class(o) or 'STATIC'
        m0 = nom.get(o.entityToken)
        if m0 is None or cls == 'STATIC':
            continue
        o.transform2 = B._as_matrix(B._mm(g[cls], m0))
    return True


def r2a_restore():
    nom = capture_nominal()
    for o in all_root_occs():
        m0 = nom.get(o.entityToken)
        if m0 is not None:
            o.transform2 = B._as_matrix(m0)
    return True


# ============================================================ viewing
def set_view(eye_dir=(0.0, 1.0, 0.0), target=(40.0, 80.0, -80.0), extents=320.0,
             up=(0.0, 0.0, 1.0), hide_prefixes=(), show_only=None):
    """Orthographic camera looking at target (mm) from eye_dir; returns the
    original light-bulb states so the caller can restore them."""
    app = adsk.core.Application.get()
    vp = app.activeViewport
    cam = vp.camera
    cam.cameraType = adsk.core.CameraTypes.OrthographicCameraType
    t = adsk.core.Point3D.create(target[0] / 10, target[1] / 10, target[2] / 10)
    e = adsk.core.Point3D.create(t.x + eye_dir[0] * 50, t.y + eye_dir[1] * 50,
                                 t.z + eye_dir[2] * 50)
    cam.target = t
    cam.eye = e
    cam.upVector = adsk.core.Vector3D.create(*up)
    cam.viewExtents = extents / 10.0
    cam.isFitView = False
    cam.isSmoothTransition = False
    vp.camera = cam
    saved = [(o, o.isLightBulbOn) for o in all_root_occs()]
    for o in all_root_occs():
        nm = B.base_name(o.component.name)
        if show_only is not None:
            o.isLightBulbOn = any(nm.startswith(p) for p in show_only)
        elif any(nm.startswith(p) for p in hide_prefixes):
            o.isLightBulbOn = False
    vp.refresh()
    adsk.doEvents()
    return saved


def restore_bulbs(saved):
    for o, s in saved:
        try:
            o.isLightBulbOn = s
        except Exception:
            pass


# ======================================================= clash classification
WHEEL_ALTERNATIVES = {'Wheel_Rim_L', 'Wheel_Tyre_L', 'ABS_TEST_Wheel_Rim_NoTyre'}
REF_TOKENS = ('6010-8', '4305', 'REF_GIM', 'MOTOR_GIM')
# The motor's three Ø4 x 3.5 output pins are one solid with the STEP housing,
# so a part fixed to a rotating output sees them as a static interference
# whenever it is rotated off its build pose (design record §11).
PIN_ARTIFACT_MM3 = 3 * math.pi * 2.0 ** 2 * 3.5 + 1.0
THREAD_ARTIFACT_MM3 = 40.0
# An output screw turns with the hub; rotated off the build pose its Ø3 shank
# sits in the STEP's static output flange: pi/4 x 3^2 x 6.0 mm + 1.
ROT_SCREW_ARTIFACT_MM3 = math.pi / 4 * 9.0 * 6.0 + 1.0


def _base(n):
    return B.base_name(n.split(':')[0])


_REF_NAMES = set()


def ref_body_names():
    """Names the interference reporter can return for a motor STEP body: the
    REF occurrences, every child occurrence and component in their trees."""
    names = set()
    for o in all_root_occs():
        if B.base_name(o.component.name).startswith('REF_'):
            stack = [o]
            while stack:
                cur = stack.pop()
                names.add(B.base_name(cur.name.split(':')[0]))
                names.add(B.base_name(cur.component.name))
                for i in range(cur.childOccurrences.count):
                    stack.append(cur.childOccurrences.item(i))
    return names


def _is_ref(n):
    return any(t in n for t in REF_TOKENS) or _base(n) in _REF_NAMES


def classify_pair(a, b, v, alpha):
    na, nb = _base(a), _base(b)
    s = {na, nb}
    if s <= WHEEL_ALTERNATIVES:
        return 'alternative wheel parts'
    if na.startswith('REFERENCE_Cable') and nb.startswith('REFERENCE_Cable'):
        return 'cable envelope segments joined by construction'
    if (na.startswith('HW_SHCS') and _is_ref(nb)) or (nb.startswith('HW_SHCS') and _is_ref(na)):
        if v <= THREAD_ARTIFACT_MM3:
            return 'screw in modelled STEP thread'
    rot_screw = ('R2A_SHCS_M3x10_Crank', 'HW_SHCS_M3x10')
    if (_is_ref(na) and nb in rot_screw) or (_is_ref(nb) and na in rot_screw):
        if v <= ROT_SCREW_ARTIFACT_MM3:
            return 'output screw in static STEP output flange'
    if (_is_ref(na) and nb in (PART['CRANK'], 'Shoulder_Output_Hub_L')) or \
       (_is_ref(nb) and na in (PART['CRANK'], 'Shoulder_Output_Hub_L')):
        if v <= PIN_ARTIFACT_MM3:
            return 'static STEP output pins vs rotating hub'
    if any(n.startswith(PART['TPU']) for n in s) and PART['DIST'] in s:
        if alpha <= ALPHA_FLEX_STOP + 3.0 or alpha >= ALPHA_EXT_STOP - 3.0:
            return 'TPU bumper designed crush'
    if PART['DIST'] in s and (PART['INB'] in s or PART['OUTB'] in s):
        if alpha < ALPHA_FLEX_STOP - 1e-6 or alpha > ALPHA_EXT_STOP + 1e-6:
            return 'rigid stop engaged beyond the stop angle'
    return None


def pose_clashes(theta, alpha, min_mm3=0.01):
    """Pose, run whole-assembly interference, classify, restore."""
    global _REF_NAMES
    _REF_NAMES = ref_body_names()
    r2a_pose(theta, alpha)
    try:
        raw = R.clashes(min_mm3, verbose=False)
    finally:
        r2a_restore()
    rows = []
    for a, b, v in raw:
        cls = classify_pair(a, b, v, alpha)
        rows.append({'a': a, 'b': b, 'mm3': round(v, 3), 'class': cls or 'REAL'})
    return rows


def remove_legacy_duplicate_cover_screws():
    """The two upper cover positions carry the cable post's M3 x 12 screws;
    the legacy rig also kept M3 x 10 cover screws there (108.6 mm3 overlap)."""
    assert_r2a_doc()
    posts = [B.bbox_of(o) for o in all_root_occs()
             if B.base_name(o.component.name) == 'HW_SHCS_M3x12_PostA']
    gone = []
    for o in all_root_occs():
        if B.base_name(o.component.name) != 'HW_SHCS_M3x10':
            continue
        b = B.bbox_of(o)
        for p in posts:
            if abs((b[0] + b[1]) - (p[0] + p[1])) < 0.2 and abs((b[4] + b[5]) - (p[4] + p[5])) < 0.2:
                gone.append(o.name)
                o.deleteMe()
                break
    return gone


def all_visible():
    """Turn every root occurrence on; returns the previous states.

    TRAP (2026-09-27): a hidden *linked* occurrence -- the three motor STEP
    references -- drops out of Design.analyzeInterference while hidden ordinary
    occurrences stay in.  A sweep run after an inspection view had hidden the
    REFs silently stopped checking the motors.  Every sweep therefore forces
    all occurrences visible and restores the view afterwards."""
    saved = [(o, o.isLightBulbOn) for o in all_root_occs()]
    for o, on in saved:
        if not on:
            o.isLightBulbOn = True
    return saved


def sweep_chunk(poses, path, min_mm3=0.01):
    """Append pose_clashes() results for (theta, alpha) poses to a JSON file."""
    assert_r2a_doc()
    ref_assert()
    capture_nominal(force=True)
    saved = all_visible()
    data = json.load(open(path)) if os.path.exists(path) else {}
    try:
        for th, al in poses:
            key = '%.1f,%.1f' % (th, al)
            if key in data:
                continue
            data[key] = pose_clashes(th, al, min_mm3)
            with open(path, 'w') as s:
                json.dump(data, s)
    finally:
        restore_bulbs(saved)
    ref_assert()
    return len(data)


# ============================================================ measurements
def occ_bodies(o):
    out, stack = [], [o]
    while stack:
        cur = stack.pop()
        for b in cur.bRepBodies:
            out.append(b)
        for i in range(cur.childOccurrences.count):
            stack.append(cur.childOccurrences.item(i))
    return out


def find_all(name):
    return [o for o in all_root_occs() if B.base_name(o.component.name) == name]


def min_dist(names_a, names_b):
    """Minimum B-Rep distance (mm) between two named occurrence groups."""
    mm = adsk.core.Application.get().measureManager
    best = None
    for na in names_a:
        for oa in find_all(na) if not hasattr(na, 'bRepBodies') else [na]:
            for ba in occ_bodies(oa):
                for nb in names_b:
                    for ob in find_all(nb) if not hasattr(nb, 'bRepBodies') else [nb]:
                        for bb in occ_bodies(ob):
                            v = mm.measureMinimumDistance(ba, bb).value * 10.0
                            best = v if best is None else min(best, v)
    return best


def pin_axis_xz(name):
    """Global XZ of the Ø5 pin's cylinder axis in its current pose."""
    o = find_all(name)[0]
    for b in occ_bodies(o):
        for f in b.faces:
            g = adsk.core.Cylinder.cast(f.geometry)
            if g and abs(g.radius * 20.0 - PIN5_D) < 1e-6:
                return (g.origin.x * 10.0, g.origin.z * 10.0)
    raise RuntimeError('pin axis not found: ' + name)


def knee_ref():
    return ref_occs()[1]


ROD_PARTS = ('HW_Rod_M5x86', 'HW_JamNut_M5', 'HW_RodEnd_M5_Upper', 'HW_RodEnd_M5_Lower')


def gate_measurements(alphas=(51.0, 55.0, 65.0, 80.0, 100.0, 120.0, 140.0, 145.0, 150.0)):
    """Clearances and closure at the sampled knee angles (theta = 0)."""
    assert_r2a_doc()
    ref_assert()
    capture_nominal(force=True)
    kr = knee_ref()
    rows = []
    try:
        for a in alphas:
            r2a_pose(0.0, a)
            c = pin_axis_xz('HW_Pin_D5x18_Crank')
            p = pin_axis_xz('HW_Pin_D5x18_Lever')
            cu = uv_inv(*c)
            row = {
                'alpha': a,
                'pin_to_pin_mm': round(math.hypot(c[0] - p[0], c[1] - p[1]), 4),
                'theta_c_measured_deg': round(math.degrees(math.atan2(cu[1], cu[0])), 3),
                'theta_c_solver_deg': round(solve(a)[2], 3),
                'tyre_to_proximal_mm': round(min_dist(['Wheel_Tyre_L'],
                    [PART['INB'], PART['OUTB'], kr, 'Shoulder_Output_Hub_L',
                     PART['CRANK']]), 3),
                'rod_to_distal_mm': round(min_dist(['HW_Rod_M5x86', 'HW_JamNut_M5'],
                                                   [PART['DIST']]), 3),
                'rod_group_to_proximal_mm': round(min_dist(list(ROD_PARTS),
                    [PART['INB'], PART['OUTB'], 'HW_SHCS_M4x10']), 3),
                'rod_group_to_crank_mm': round(min_dist(['HW_Rod_M5x86', 'HW_JamNut_M5',
                    'HW_RodEnd_M5_Lower'], [PART['CRANK'], PART['CRANK_CAP']]), 3),
                'rod_group_to_lever_mm': round(min_dist(['HW_Rod_M5x86', 'HW_JamNut_M5',
                    'HW_RodEnd_M5_Upper'], [PART['DIST'], PART['LEVER_CAP']]), 3),
                'upper_rod_end_to_crank_mm': round(min_dist(['HW_RodEnd_M5_Upper'],
                    [PART['CRANK'], PART['CRANK_CAP']]), 3),
                'lower_rod_end_to_lever_mm': round(min_dist(['HW_RodEnd_M5_Lower'],
                    [PART['DIST'], PART['LEVER_CAP']]), 3),
                'crank_to_proximal_mm': round(min_dist([PART['CRANK'], PART['CRANK_CAP'],
                    'HW_DowelPin_D4x10_Crank'], [PART['INB'], PART['OUTB'],
                    'HW_SHCS_M4x10', 'R2A_SHCS_M3x10_Actuator']), 3),
                'distal_to_proximal_mm': round(min_dist([PART['DIST'], PART['LEVER_CAP']],
                    [PART['INB'], PART['OUTB']]), 3),
                'encoder_arm_to_proximal_mm': round(min_dist([PART['ENC_ARM']],
                    [PART['OUTB'], PART['ENC_BRACKET'], 'HW_AS5048A_PCB',
                     'R2A_SHCS_M3x16_Bracket', 'HW_DowelPin_D10x35']), 3),
            }
            rows.append(row)
    finally:
        r2a_restore()
    ref_assert()
    return rows


def stop_contact(lo, hi, flex=True, tol=0.01):
    """Bisect the knee angle where the rigid links first overlap."""
    assert_r2a_doc()
    capture_nominal(force=True)
    mm = adsk.core.Application.get().measureManager

    def overlap(a):
        r2a_pose(0.0, a)
        d = min_dist([PART['DIST']], [PART['INB'], PART['OUTB']])
        return d <= 1e-4
    try:
        # flex: overlap below the stop; ext: overlap above it
        while hi - lo > tol:
            mid = 0.5 * (lo + hi)
            ov = overlap(mid)
            if flex:
                lo, hi = (lo, mid) if not ov else (mid, hi)
            else:
                lo, hi = (mid, hi) if not ov else (lo, mid)
        return 0.5 * (lo + hi)
    finally:
        r2a_restore()


PRINTED = ('INB', 'OUTB', 'CRANK', 'CRANK_CAP', 'DIST', 'LEVER_CAP', 'ENC_ARM',
           'ENC_BRACKET', 'PIN_CAP')


def part_volumes():
    """Native B-Rep volumes (mm3) of every R2A part and R2A hardware group."""
    out = {}
    for o in all_root_occs():
        nm = B.base_name(o.component.name)
        v = sum(b.volume * 1000.0 for b in o.component.bRepBodies)
        key = nm
        a = o.attributes.itemByName('R2A', 'set')
        if a:
            key = a.value
        out.setdefault(key, [0, 0.0])
        out[key][0] += 1
        out[key][1] += v
    return {k: {'count': c, 'volume_mm3': round(v, 1)} for k, (c, v) in sorted(out.items())}


# ================================================================ cables
CABLE_D = 6.0
ENC_CABLE_D = 3.5       # 6 x AWG28 SPI lead envelope (AS5048A kit wiring TBD)
ENC_CABLE_UV = 205.0


def _tube(points, d=CABLE_D):
    """Union of cylinders (and joint spheres) through global (x, y, z) points."""
    parts = []
    for a, b in zip(points[:-1], points[1:]):
        parts.append(_cyl(a, b, d))
    for p in points[1:-1]:
        parts.append(_tm().createSphere(_p(*p), d / 20.0))
    return _union(parts)


def _xyz(xz, y):
    return (xz[0], y, xz[1])


def build_cables():
    """Reference cable envelopes (not printed): wheel, encoder, knee actuator.

    The knee crossing is a free loop; its reserve is an annulus around the pin
    cap on the inboard side.  The service loop from the root exit to the
    stand anchor is flexible and is a physical routing check."""
    assert_r2a_doc()
    yin = 55.5
    ymid = 0.5 * (CABLE_Y[0] + CABLE_Y[1])
    # wheel cable on the distal inboard face (distal-fixed)
    w1 = [_xyz(B.dist_uv(120.0, 0.0), 57.0), _xyz(B.dist_uv(100.0, -8.0), yin),
          _xyz(B.dist_uv(46.0, -8.0), yin), _xyz(B.dist_uv(32.0, -9.0), yin)]
    _base_comp('REFERENCE_Cable_Wheel_Distal', _tube(w1), 'DIST')
    # free-loop reserve around the pin cap
    ring = _cut(_cyl((KX, yin - 3.0, KZ), (KX, yin + 3.0, KZ), 60.0),
                _cyl((KX, yin - 4.0, KZ), (KX, yin + 4.0, KZ), 38.0))
    _base_comp('REFERENCE_Cable_Knee_Loop', ring, 'PROX')
    # proximal: loop -> inboard entry -> duct -> root -> back-wall exit
    ex = polar((0, 0), 55.0, DUCT_EXIT_UV_DEG)
    ex_in = polar((0, 0), BACK_WALL_R[0] - 3.0, DUCT_EXIT_UV_DEG)
    w2 = [_xyz(kuv(28.0, 204.0), yin), _xyz(uv(*DUCT_ENTRY_IN_UV), yin),
          _xyz(uv(*DUCT_ENTRY_IN_UV), ymid), _xyz(uv(30.0, -9.0), ymid),
          _xyz(uv(0.0, -14.0), ymid), _xyz(uv(*ex_in), ymid), _xyz(uv(*ex), ymid)]
    _base_comp('REFERENCE_Cable_Wheel_Proximal', _tube(w2), 'PROX')
    # AS5048A cable: PCB edge -> outboard face -> outboard entry -> duct
    # leaves the board through the bracket-plate notch, drops to the face at
    # R22 (between the post at 180 deg and the arm's sweep from 218 deg)
    yt = ENC_BRACKET_PLATE[1] + 2.0
    ye = ENC_ARM_PLATE[1] - 2.5
    e = [_xyz((KX, KZ), yt), _xyz(kuv(22.0, ENC_CABLE_UV), yt),
         _xyz(kuv(22.0, ENC_CABLE_UV), ye), _xyz(kuv(34.0, ENC_CABLE_UV), ye),
         _xyz(uv(*DUCT_ENTRY_OUT_UV), ye), _xyz(uv(*DUCT_ENTRY_OUT_UV), ymid + 2.0),
         _xyz(uv(48.0, -8.0), ymid + 2.0)]
    _base_comp('REFERENCE_Cable_Encoder', _tube(e, ENC_CABLE_D), 'PROX')
    # knee-actuator cable: cover notch -> over the housing -> round the root
    notch = polar((0, 0), 30.0, 72.0)
    out = [polar((0, 0), 55.0, a) for a in (72.0, 110.0, 150.0, xz_angle_of_uv(DUCT_EXIT_UV_DEG))]
    ya = ACT_COVER_Y[0] + 5.0
    k = [_xyz(notch, ya), _xyz(out[0], ya), _xyz(out[0], 95.0)]
    k += [_xyz(p, 95.0) for p in out[1:]] + [_xyz(out[-1], ymid)]
    _base_comp('REFERENCE_Cable_Knee_Actuator', _tube(k), 'PROX')
    return True


# ============================================================ gate record
GATE_DIR = os.path.join(ROOT_DIR, 'evidence', 'r2a', '2026-09-27_digital_gate')
LEGACY_VOLUMES_MM3 = {
    # native B-Rep volumes in Beni_SingleLegRig v31, read from this document's
    # Save-As copy before any edit (R2A version 1 inventory, 2026-09-27)
    'Proximal_Link_L': 69736.8, 'Distal_Link_L': 49003.8,
    'Knee_Encoder_Bracket_L': 2614.9,
}
R2A_MASS_PARTS = {
    PART['INB']: 'PACF', PART['OUTB']: 'PACF', PART['CRANK']: 'PACF',
    PART['CRANK_CAP']: 'PACF', PART['DIST']: 'PACF', PART['LEVER_CAP']: 'PACF',
    PART['ENC_ARM']: 'PACF', PART['ENC_BRACKET']: 'PACF', PART['PIN_CAP']: 'PACF',
    PART['TPU'] + '_In': 'TPU', PART['TPU'] + '_Out': 'TPU', 'HW_RodEnd_M5_Upper': 'STEEL', 'HW_RodEnd_M5_Lower': 'STEEL',
    'HW_Rod_M5x86': 'STEEL', 'HW_JamNut_M5': 'STEEL', 'HW_Pin_D5x18_Crank': 'STEEL',
    'HW_Pin_D5x18_Lever': 'STEEL', 'HW_DowelPin_D4x10_Crank': 'STEEL',
    'HW_DowelPin_D4x10_Lever': 'STEEL', 'HW_DowelPin_D4x10_EncArm': 'STEEL',
    'R2A_SHCS_M3x10_Actuator': 'STEEL', 'R2A_SHCS_M3x12_Perimeter': 'STEEL',
    'R2A_SHCS_M3x10_Crank': 'STEEL', 'R2A_SHCS_M3x10_EncArm': 'STEEL',
    'R2A_SHCS_M3x16_Bracket': 'STEEL', 'R2A_SHCS_M3x6_PinCap': 'STEEL',
}


def write_gate_record(clearances, stops, sweep, extra=None):
    """Write the Fusion-measured values r2a_calc.py consumes."""
    assert_r2a_doc()
    doc = adsk.core.Application.get().activeDocument
    vols = {k: v['volume_mm3'] for k, v in part_volumes().items()}
    rec = {
        'document': doc.name, 'version': doc.dataFile.versionNumber,
        'written': time.strftime('%Y-%m-%d %H:%M'),
        'linkage_mm': {'crank': CRANK_A, 'rod': ROD_B, 'lever': LEVER_C,
                       'lever_offset_deg': LEVER_DELTA, 'theta_c_build_deg': THC0},
        'rod_end_envelope_mm': {'eye_d': RE_EYE_D, 'eye_w': RE_EYE_W, 'ball_d': RE_BALL_D,
                                'ball_w': RE_BALL_W, 'neck_d': RE_NECK_D, 'h': RE_H,
                                'thread_depth': RE_THREAD_DEPTH, 'bore': PIN5_D},
        'jam_nut_mm': {'af': NUT_AF, 't': NUT_T,
                       'across_corners': round(NUT_AF / math.cos(math.radians(30.0)), 3)},
        'rod_mm': {'d': ROD_D, 'length': ROD_LEN},
        'stack_y_mm': {'leg_inboard_face': Y_IN, 'channel': [Y_CH0, Y_CH1],
                       'actuator_mount_face': ACT_MOUNT_Y, 'actuator_output_face': ACT_OUT_Y,
                       'actuator_housing': list(ACT_HOUSING_Y), 'actuator_cover': list(ACT_COVER_Y),
                       'rod_plane': Y_ROD, 'ball_gap': list(GAP), 'crank_cap': list(EAR_IN),
                       'crank_slab': list(CRANK_SLAB), 'lever_inboard_ear': list(LEVER_IN),
                       'lever_cap': list(EAR_OUT), 'bearing_a': list(BRG_A), 'bearing_b': list(BRG_B),
                       'receiver': list(RECV), 'knee_pin': list(PIN_Y),
                       'magnet_face': ENC_ARM_PLATE[1], 'as5048a_die': list(ENC_DIE)},
        'outline_mm': {'root_r': ROOT_R, 'root_r_tyre_side': ROOT_R_TYRE,
                       'bottom_edge_tangent_r': BOTTOM_TANGENT_R, 'knee_cheek_r': KNEE_CHEEK_R,
                       'knee_boss_r': KNEE_BOSS_R, 'roof_v': list(ROOF_V),
                       'back_wall_r': list(BACK_WALL_R)},
        'clevis_mm': {'ear_thickness': {'crank_cap': EAR_IN[1] - EAR_IN[0],
                                        'crank_slab_at_pin': CRANK_SLAB[1] - 1.0 - CRANK_SLAB[0],
                                        'lever_inboard': LEVER_IN[1] - LEVER_IN[0],
                                        'lever_cap': EAR_OUT[1] - EAR_OUT[0]},
                      'ball_gap': GAP[1] - GAP[0], 'pin': [PIN5_D, PIN5_LEN],
                      'pin_hole_d': PIN5_HOLE_D,
                      # a floating Ø5 x 18 pin: lever pin between the cheek faces;
                      # crank pin between the inboard face and its blind bottom
                      'min_pin_engagement': round(min(
                          (Y_CH0 + PIN5_LEN) - EAR_OUT[0],
                          LEVER_IN[1] - (Y_CH1 - PIN5_LEN),
                          EAR_IN[1] - ((CRANK_SLAB[1] - 1.0) - PIN5_LEN)), 3)},
        'stops': {'flex': {'contact_deg': stops['flex'], 'r0': STOP_R0, 'r1': STOP_R1,
                           'face_uv_deg': STOP_FLEX_UV},
                  'ext': {'contact_deg': stops['ext'], 'r0': STOP_R0, 'r1': KNEE_CHEEK_R,
                          'face_uv_deg': STOP_EXT_UV},
                  'band_mm': 5.0, 'bisection_tol_deg': 0.01,
                  'tpu_plug': {'d': TPU_D, 'protrusion': TPU_D / 2 - TPU_INSET, 'r': TPU_R}},
        'clearances': clearances,
        'sweep': sweep,
        'volumes_mm3': vols,
        'legacy_volumes_mm3': LEGACY_VOLUMES_MM3,
        'r2a_mass_parts': R2A_MASS_PARTS,
        'linkage_map': [{'alpha': a, 'theta_c_deg': round(solve(a)[2], 3)}
                        for a in (49, 51, 55, 60, 65, 70, 80, 90, 100, 110, 120, 130, 140,
                                  145, 150, 152)],
    }
    if extra:
        rec.update(extra)
    os.makedirs(GATE_DIR, exist_ok=True)
    with open(os.path.join(GATE_DIR, 'fusion_measurements.json'), 'w') as s:
        json.dump(rec, s, indent=1)
    return rec
