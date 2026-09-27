#!/usr/bin/env python3
"""R2A active-knee arithmetic: Beni-style crank-and-pushrod knee drive.

The knee actuator rides on the proximal link, coaxial with the shoulder axis,
and turns a crank inside the proximal-link root.  A rod-end pushrod runs down
the link to a lever on the distal link behind the knee.  The linkage is a
four-bar whose ground link is the proximal link itself, so the knee coordinate
is referenced to the proximal link and is independent of shoulder angle.

Every number in the R2A plan's mechanism section comes from this script.
Inputs are copied verbatim from their sources:

  * link lengths, wheel OD, nominal pose   beni_prototype1_fusion_guide_rewritten.md §4
  * GIM6010-8 geometry                      beni_prototype1_design_record.md §2.1
  * lateral (Y) stack                       beni_prototype1_design_record.md §3
  * REV2 robot mass                         beni_prototype1_design_record.md §14
  * GIM6010-8 electrical data               electronics/03_compute_and_can.md §1.1, §1.4
  * CAN frame times                         electronics/03_compute_and_can.md §2
  * RobStride / EduLite published data      docs/design/active_knee_actuator_trade_study.md
  * PA-CF strength                          beni_rig_no_machining.md §1
  * legacy proof screen (275 N at a wheel)  beni_prototype1_fusion_guide_rewritten.md §11

Values marked ASSUMPTION or DESIGN CHOICE are not facts about hardware.  They
are envelopes or targets that the selected purchased parts and the Fusion
model must meet or replace.

Run:  python3 r2a_calc.py            (add --plot to redraw docs/design/r2a_knee_linkage.png)
"""

import math
import sys

import numpy as np

G = 9.80665

# --------------------------------------------------- legacy frozen kinematics
L1 = L2 = 120.0            # mm, guide §4
WHEEL_R = 55.0             # mm, Ø110 OD, guide §4
A_NOM = 50.0               # deg, proximal +50° / distal -50° from vertical
ALPHA_NOM = 180.0 - 2 * A_NOM   # 80° interior knee angle at the legacy nominal

# --------------------------------------------------- lateral stack, design record §3
Y_LEG_IN, Y_LEG_OUT = 59.5, 89.5        # leg inboard / outboard faces
Y_CHANNEL = (64.5, 84.5)                # former spring channel, 20 mm
Y_TYRE = (69.0, 99.0)                   # rim + tyre
Y_RIM_WEB_OUT = 104.5                   # outboard end of the wheel stack
DISTAL_BOSS_R = 11.0                    # distal knee boss Ø22, y 65…84
Y_ROD_PLANE = 74.5                      # legacy cartridge centre plane, reused for the rod

# --------------------------------------------------- GIM6010-8, design record §2.1
GIM_HOUSING_R = 40.0       # Ø80
GIM_REAR_X = -37.0         # driver-cover rear face, from the housing mount face
GIM_HOUSING_X = (-25.0, -1.0)
GIM_COVER_R = 28.5         # Ø57
GIM_COVER_X = (-37.0, -26.0)
GIM_OUT_FACE_X = 3.5       # output mount face
GIM_PCD_R = 37.0           # 8 × M3 on Ø74 PCD
M3_CLEAR = 3.4             # clearance hole used elsewhere in this project

# --------------------------------------------------- GIM6010-8, electronics/03 §1.1, §1.4
GIM = dict(rated=5.0, stall=11.0, kt=0.47, nl_rpm_24=420.0, nom_rpm_24=120.0,
           mass_bare=0.388, mass_brief=0.500, r_phase=0.42,
           meas_low=4.8, meas_high=9.4, rated_a=10.5, stall_a=23.4)

# --------------------------------------------------- trade study, 2026-09-25 data
CANDIDATES = [
    # name, rated N·m, peak N·m, mass kg, V_min, V_max, protocol family
    ('GIM6010-8 (owned family)', 5.0, 11.0, 0.388, None, None, 'ODrive CANSimple, 500 k default / 1 M max'),
    ('RobStride 05', 1.6, 5.5, 0.191, 15, 60, 'RobStride CAN, 1 M'),
    ('EduLite 05', 1.8, 6.0, 0.242, 15, 60, 'RobStride CAN, 1 M'),
    ('RobStride 00', 5.0, 14.0, 0.310, 24, 60, 'RobStride CAN, 1 M'),
    ('RobStride 01', 6.0, 17.0, 0.380, 24, 48, 'RobStride CAN, 1 M'),
    ('RobStride 02', 6.0, 17.0, 0.405, 24, 60, 'RobStride CAN, 1 M'),
]

BUS_BENCH = 20.0           # V, rig bench bus (electronics/07 Wave 0, blocker B1)
BUS_6S_NOM = 22.2          # V, 6S nominal (electronics/01 §4 power tree)

# --------------------------------------------------- mass, design record §14
M_REV2 = 3.3089            # kg, historical REV2 Fusion mass
M_LINKAGE_ALLOW = 0.060    # kg per leg — ASSUMPTION: crank, rod ends, rod, pins,
#                            extra cheek; replace with Fusion mass properties

# --------------------------------------------------- DESIGN CHOICES / ASSUMPTIONS
TYRE_GAP = 5.0             # mm, minimum tyre-to-leg-root clearance at the flex stop
ROOT_WALL = 3.3            # mm, printed wall outside an M3 clearance hole
ROOT_R = GIM_PCD_R + M3_CLEAR / 2 + ROOT_WALL   # outboard cheek radius holding the actuator
ALPHA_EXT_STOP = 150.0     # deg, extension stop: keep 30° from a straight leg
OVERTRAVEL = 2.0           # deg, linkage must stay valid 2° beyond each stop
CRANK_HUB_R = 19.0         # mm, crank hub Ø38 (same body as Shoulder_Output_Hub_L)
ROD_EYE_R = 8.0            # mm, ASSUMPTION: rod-end eye envelope radius (M5 class)
ROD_SHANK_R = 4.5          # mm, ASSUMPTION: jam-nut envelope radius on the rod
CLR = 2.0                  # mm, minimum running clearance
MU_MIN = 40.0              # deg, minimum transmission angle over the working range
MU_MIN_OVERTRAVEL = 35.0   # deg, allowed only in the 2° overtravel into the bumpers
GAMMA_MIN = 15.0           # deg, keep the crank this far from its toggle
ETA = 0.95                 # linkage efficiency, ASSUMPTION
PIN_D = 5.0                # mm, crank / lever pin shoulder diameter
CHEEK_T = 4.0              # mm, each printed clevis cheek at a pin
ROD_MINOR_D = {'M5': 5.0 - 1.0825 * 0.8, 'M6': 6.0 - 1.0825 * 1.0}   # ISO 724 d1
E_STEEL = 200e3            # MPa
PA_CF_XY = (84.0, 102.0)   # MPa, beni_rig_no_machining.md §1
PROOF_WHEEL_N = 275.0      # N at one wheel, guide §11 structural screen
STOP_R = 35.0              # mm, DESIGN CHOICE: knee-stop contact radius
DYN_FACTOR = 1.5           # ASSUMPTION: dynamic factor on actuator stall torque
SELECT_JUMP_FRAC = 0.97    # DESIGN CHOICE: accept 3 % of idealised push-off for compactness
MAX_PIN_ENVELOPE = 40.0    # mm, DESIGN CHOICE: pin + eye envelope from the link line
FRAME_US_1M = (117.0, 135.0)   # typical / worst classical-CAN frame at 1 Mbit


def hr(title):
    print()
    print('=' * 78)
    print(title)
    print('=' * 78)


def leg_d(alpha):
    """Shoulder-to-wheel-axle distance for the equal-link leg, mm."""
    return 2 * L1 * np.sin(np.radians(alpha) / 2)


def alpha_of_d(d):
    return np.degrees(2 * np.arcsin(d / (2 * L1)))


def knee_arm(alpha):
    """Knee torque per newton of radial leg force, mm (= L·cos(α/2))."""
    return L1 * np.cos(np.radians(alpha) / 2)


# ----------------------------------------------------------------- 1. envelope
def envelope():
    hr('1.  LATERAL STACK AND THE FLEX-STOP LIMIT')
    y_mount = Y_LEG_OUT
    y_out = y_mount - GIM_OUT_FACE_X
    y_house = (y_mount - GIM_HOUSING_X[1], y_mount - GIM_HOUSING_X[0])
    y_cover = (y_mount - GIM_COVER_X[1], y_mount - GIM_COVER_X[0])
    y_rear = y_mount - GIM_REAR_X
    print(f'  knee actuator mount face on the outboard cheek     y = {y_mount:6.1f}')
    print(f'  output face (inside the cheek bore, facing in)     y = {y_out:6.1f}')
    print(f'  Ø80 housing                                        y = {y_house[0]:.1f} … {y_house[1]:.1f}')
    print(f'  Ø57 driver cover                                   y = {y_cover[0]:.1f} … {y_cover[1]:.1f}')
    print(f'  outermost point of the leg                         y = {y_rear:6.1f}'
          f'   (legacy wheel stack ends at {Y_RIM_WEB_OUT})')
    print(f'  track at the knee actuators                        {2 * y_rear:6.1f} mm'
          f'   (legacy outer width {2 * Y_RIM_WEB_OUT:.1f} mm)')

    rows = [('outboard cheek, R{:.1f}'.format(ROOT_R), ROOT_R, (Y_CHANNEL[1], Y_LEG_OUT)),
            ('Ø80 actuator housing', GIM_HOUSING_R, y_house),
            ('Ø57 driver cover', GIM_COVER_R, y_cover)]
    print('\n  Tyre (R55, y 69…99; stack to 104.5) against parts on the shoulder axis:')
    worst = 0.0
    for nm, r, (y0, y1) in rows:
        overlap = min(y1, Y_RIM_WEB_OUT) - max(y0, Y_TYRE[0])
        if overlap <= 0:
            print(f'    {nm:<26s} no Y overlap — cannot touch the tyre')
            continue
        dmin = WHEEL_R + r + TYRE_GAP
        a = float(alpha_of_d(dmin))
        worst = max(worst, a)
        print(f'    {nm:<26s} {overlap:4.1f} mm Y overlap → d ≥ {dmin:5.1f} mm → α ≥ {a:5.2f}°')
    flex = math.ceil(worst)
    print(f'\n  → flexion stop α = {flex:.0f}° (d = {leg_d(flex):.1f} mm);'
          f' extension stop α = {ALPHA_EXT_STOP:.0f}° (d = {leg_d(ALPHA_EXT_STOP):.1f} mm)')
    print(f'    legacy nominal α = {ALPHA_NOM:.0f}° (d = {leg_d(ALPHA_NOM):.1f} mm); legacy passive'
          f' travel was α 88…53° (φ −8…+27°)')
    print(f'    usable leg-length stroke {leg_d(ALPHA_EXT_STOP) - leg_d(flex):.1f} mm'
          ' (legacy 0→+25° design stroke: 46.1 mm)')
    th_clear = WHEEL_R + 12.0 + 3.0
    print(f'  tyre vs proximal-link underside (12 mm half-depth, 3 mm gap): α ≥'
          f' {math.degrees(math.asin(th_clear / L2)):.1f}° — not governing')
    return flex


# ----------------------------------------------------------- 2. mass and loads
def masses():
    hr('2.  R2A MASS ESTIMATE AND STATIC KNEE LOAD')
    out = {}
    for tag, m_act in (('bare 388 g', GIM['mass_bare']), ('brief 500 g', GIM['mass_brief'])):
        m = M_REV2 + 2 * (m_act + M_LINKAGE_ALLOW)
        out[tag] = m
        print(f'  REV2 {M_REV2:.4f} kg + 2 × (knee GIM6010-8 {tag} + {M_LINKAGE_ALLOW * 1000:.0f} g'
              f' linkage) = {m:.3f} kg')
    print('  (No credit is taken for the removed spring cartridge; C4 is unresolved,'
          ' so both actuator masses are carried.)')
    return out


def static_table(m, flex):
    print(f'\n  Static stance, wheel under the shoulder, per-leg F = m·g/2 = {m * G / 2:.1f} N'
          f' (m = {m:.3f} kg, legs treated as massless — conservative):')
    print('     α°     d mm   knee N·m')
    for a in (flex, 65.0, ALPHA_NOM, 100.0, 120.0, 140.0):
        t = m * G / 2 * knee_arm(a) / 1000
        print(f'   {a:5.1f}  {float(leg_d(a)):7.1f}  {t:8.2f}')


# ----------------------------------------------------------------- 3. linkage
def solve_linkage(alphas, a, b, c, delta, branch):
    """Four-bar in the proximal-link frame: S = (0,0), K = (L1,0).

    The distal link points along 180° + α; the lever is fixed to it at
    θ_l = α + δ, so δ = 180° + (lever offset from the distal-link direction).
    Returns a dict of arrays, or None if the linkage cannot assemble.
    """
    th_l = np.radians(alphas + delta)
    px = L1 + c * np.cos(th_l)
    py = c * np.sin(th_l)
    dd = np.hypot(px, py)
    cosg = (a * a + dd * dd - b * b) / (2 * a * dd)
    if np.any(np.abs(cosg) > 1.0):
        return None
    th_c = np.arctan2(py, px) + branch * np.arccos(cosg)
    cx, cy = a * np.cos(th_c), a * np.sin(th_c)
    ux, uy = (cx - px) / b, (cy - py) / b          # unit P → C
    lx, ly = px - L1, py                           # K → P
    s = lx * uy - ly * ux                          # moment arm of rod tension at K, mm
    mu = np.degrees(np.arcsin(np.clip(np.abs(s) / c, 0, 1)))
    gam = np.abs(cx * (-uy) - cy * (-ux)) / a      # sin(angle crank vs rod)
    th_cu = np.unwrap(th_c)
    n = np.gradient(th_cu, np.radians(alphas))     # dθc/dα
    return dict(th_c=th_cu, cx=cx, cy=cy, px=px, py=py, s=s, mu=mu,
                sin_gam=gam, n=n)


def seg_dist(qx, qy, x0, y0, x1, y1):
    vx, vy = x1 - x0, y1 - y0
    t = np.clip(((qx - x0) * vx + (qy - y0) * vy) / (vx * vx + vy * vy), 0, 1)
    return np.hypot(x0 + t * vx - qx, y0 + t * vy - qy)


def rod_clear(r):
    """Clearance of the rod shank from the distal knee boss, which spans the
    whole channel at K.  Near S the only part in the rod's plane is the crank's
    own tip clevis: the Ø38 crank hub sits on the actuator output face,
    outboard of the rod plane (see §1), so it is not a rod obstacle."""
    bx, by = r['px'] - r['cx'], r['py'] - r['cy']
    bl = np.hypot(bx, by)
    f0 = ROD_EYE_R / bl
    x0, y0 = r['cx'] + f0 * bx, r['cy'] + f0 * by
    x1, y1 = r['px'] - f0 * bx, r['py'] - f0 * by
    dk = seg_dist(L1, 0.0, x0, y0, x1, y1) - (DISTAL_BOSS_R + ROD_SHANK_R)
    return dk


def tyre_vs_crank(r, alphas):
    """Smallest tyre-edge clearance to the printed wall around the crank-pin
    sweep, over every knee pose.  The wall encloses every crank-pin position
    the linkage ever uses, so it is tested against the tyre at every α."""
    wx = L1 - L2 * np.cos(np.radians(alphas))
    wy = -L2 * np.sin(np.radians(alphas))
    dx = r['cx'][None, :] - wx[:, None]
    dy = r['cy'][None, :] - wy[:, None]
    return float(np.min(np.hypot(dx, dy))) - (WHEEL_R + ROD_EYE_R + ROOT_WALL)


def feasible(r, alphas, flex):
    if r is None:
        return False
    work = (alphas >= flex) & (alphas <= ALPHA_EXT_STOP)
    if np.any(r['mu'][work] < MU_MIN) or np.any(r['mu'] < MU_MIN_OVERTRAVEL):
        return False
    if np.any(r['sin_gam'] < math.sin(math.radians(GAMMA_MIN))):
        return False
    if np.any(r['n'] <= 0.05) or np.any(np.sign(r['s']) != np.sign(r['s'][0])):
        return False
    if np.any(rod_clear(r) < CLR):
        return False
    if tyre_vs_crank(r, alphas) < TYRE_GAP:
        return False
    # the lever pin stays on the side away from the folding distal link; the
    # crank pin may sit anywhere inside the root (the tyre stays outside it)
    if np.any(r['py'] < CLR):
        return False
    return True


# ----------------------------------------------------------- 4. push-off model
def jump(alphas, n_tab, m, t_lim, bus_v, flex):
    """Vertical push-off from rest at the flex stop + 3° to α = ext stop − 2°.

    Per-leg share m/2 lumped at the shoulder; legs massless (optimistic).
    Knee actuator: linear torque-speed line from stall to no-load speed, capped
    by t_lim.  No-load speed scales linearly with bus voltage (ASSUMPTION).
    """
    ms = m / 2
    w_nl = GIM['nl_rpm_24'] * bus_v / 24.0 * 2 * math.pi / 60
    a0, a1 = flex + 3.0, ALPHA_EXT_STOP - 2.0
    d = float(leg_d(a0)) / 1000
    v = 0.0
    dt = 2e-4
    t = 0.0
    for _ in range(20000):
        al = float(alpha_of_d(d * 1000))
        if al >= a1:
            break
        nn = float(np.interp(al, alphas, n_tab))
        arm = float(knee_arm(al)) / 1000
        ad = v / arm
        wc = nn * ad
        tc = min(t_lim, GIM['stall'] * max(0.0, 1 - wc / w_nl))
        f = ETA * nn * tc / arm
        acc = f / ms - G
        if t == 0.0 and acc <= 0:
            return 0.0, 0.0, 0.0
        v = max(0.0, v + acc * dt)
        d += v * dt
        t += dt
    return v, v * v / (2 * G) * 1000, t * 1000


def landing(alphas, n_tab, m, t_lim, a_touch, flex):
    """Largest free-drop height one pair of legs can stop between α_touch and
    the flex stop at constant actuator torque t_lim (no bumper, no shoulder)."""
    ms = m / 2
    grid = np.linspace(flex, a_touch, 400)
    f = ETA * np.interp(grid, alphas, n_tab) * t_lim / (knee_arm(grid) / 1000)
    dgrid = leg_d(grid) / 1000
    work = float(np.trapezoid(f, dgrid)) if hasattr(np, 'trapezoid') else float(np.trapz(f, dgrid))
    stroke = float(dgrid[-1] - dgrid[0])
    h = (work - ms * G * stroke) / (ms * G)
    return max(0.0, h * 1000), stroke * 1000, float(f.min())


# ---------------------------------------------------------------- 5. synthesis
def synthesise(flex, m):
    hr('3.  CRANK-AND-PUSHROD SYNTHESIS (four-bar, ground = proximal link)')
    alphas = np.arange(flex - OVERTRAVEL, ALPHA_EXT_STOP + OVERTRAVEL + 0.25, 0.5)
    print(f'  valid range checked: α = {alphas[0]:.0f}…{alphas[-1]:.0f}°'
          f'  constraints: μ ≥ {MU_MIN:.0f}°, crank ≥ {GAMMA_MIN:.0f}° from toggle,'
          f' rod ≥ {CLR:.0f} mm from the knee boss,'
          f' tyre ≥ {TYRE_GAP:.0f} mm from the crank-sweep wall')
    best = None
    count = 0
    feas = []
    for a in np.arange(20.0, 44.1, 2.0):
        for c in np.arange(20.0, 40.1, 2.0):
            for b in np.arange(84.0, 156.1, 4.0):
                for delta in np.arange(-60.0, 60.1, 3.0):
                    for branch in (1, -1):
                        r = solve_linkage(alphas, a, b, c, delta, branch)
                        count += 1
                        if not feasible(r, alphas, flex):
                            continue
                        feas.append((a, b, c, delta, branch, r))
    print(f'  {count} candidate geometries, {len(feas)} satisfy every constraint')
    if not feas:
        return alphas, None, None

    scored = []
    for a, b, c, delta, branch, r in feas:
        _, h_low, _ = jump(alphas, r['n'], m, GIM['meas_low'], BUS_6S_NOM, flex)
        f_rod = float(np.max(DYN_FACTOR * GIM['stall'] * r['n'] * 1000 / np.abs(r['s'])))
        depth = float(max(r['py'].max(), r['cy'].max())) + ROD_EYE_R
        scored.append((h_low, a, b, c, delta, branch, r, f_rod, depth))
    scored.sort(key=lambda x: -x[0])
    h_best = scored[0][0]
    print(f'  best idealised push-off (m = {m:.3f} kg, 22.2 V, 4.8 N·m cap): {h_best:.0f} mm CoM rise')
    print('  the ten best, showing how flat the optimum is:')
    print('     rise  crank  rod  lever  δ    N range      rod force  pin envelope')
    for h, a, b, c, delta, branch, r, f_rod, depth in scored[:10]:
        print(f'    {h:5.0f}  {a:4.0f} {b:5.0f} {c:5.0f} {delta:+4.0f}  {r["n"].min():4.2f}–{r["n"].max():4.2f}'
              f'   {f_rod:6.0f} N   {depth:5.1f} mm')
    pool = [x for x in scored if x[0] >= SELECT_JUMP_FRAC * h_best and x[8] <= MAX_PIN_ENVELOPE]
    pool.sort(key=lambda x: (x[7], x[8]))
    print(f'  selection rule: rise ≥ {100 * SELECT_JUMP_FRAC:.0f} % of best, pin envelope ≤'
          f' {MAX_PIN_ENVELOPE:.0f} mm from the link line, then lowest rod force'
          f' ({len(pool)} qualify)')
    best = pool[0][:7]
    return alphas, best, None


def report_linkage(tag, s, alphas, m, flex):
    h_low, a, b, c, delta, branch, r = s
    print(f'\n  {tag}: crank a = {a:.0f} mm, pushrod b = {b:.0f} mm (pin to pin),'
          f' lever c = {c:.0f} mm,')
    off = (delta - 180 + 180) % 360 - 180
    print(f'    lever {off:+.0f}° from the distal-link direction, i.e. {180 - abs(off):.0f}° short of'
          f' straight through the knee (θ_lever = α {delta:+.0f}°), assembly branch {branch:+d}')
    tension = r['s'][0] > 0
    print('    weight-bearing (knee-extension) torque puts the rod in '
          + ('TENSION' if tension else 'COMPRESSION'))
    dk = rod_clear(r)
    crank_range = float(np.degrees(r['th_c'].max() - r['th_c'].min()))
    work = (alphas >= flex) & (alphas <= ALPHA_EXT_STOP)
    print(f'    crank travel {crank_range:.1f}° for {alphas[-1] - alphas[0]:.0f}° of knee;'
          f' min μ {r["mu"][work].min():.1f}° working / {r["mu"].min():.1f}° with overtravel')
    print(f'    rod clearance to the distal boss {dk.min():.1f} mm; tyre to crank-sweep wall'
          f' {tyre_vs_crank(r, alphas):.1f} mm; crank toggle margin'
          f' {math.degrees(math.asin(r["sin_gam"].min())):.1f}°')
    print('     α°   crank θc°  N=dθc/dα   μ°   crank for stance   rod force @ stall×1.5')
    ms_f = m * G / 2
    for al in (flex, 65.0, ALPHA_NOM, 100.0, 120.0, 140.0, ALPHA_EXT_STOP):
        i = int(np.argmin(np.abs(alphas - al)))
        nn = r['n'][i]
        tk = ms_f * knee_arm(al) / 1000
        tc = tk / (ETA * nn)
        f_rod = DYN_FACTOR * GIM['stall'] * nn * 1000 / abs(r['s'][i])
        thc = math.degrees(r['th_c'][i]) % 360
        print(f'   {al:5.1f}  {thc:7.1f}  {nn:8.3f}  {r["mu"][i]:5.1f}  {tc:6.2f} N·m'
              f'          {f_rod:6.0f} N')
    print('    θc is the crank angle from the shoulder→knee line, positive toward the'
          ' side away from the distal link; α is the interior knee angle')
    return r


def performance(alphas, best, par, masses_, flex):
    hr('4.  JUMP AND LANDING CAPABILITY WITH A GIM6010-8 KNEE')
    print('  Push-off from rest at the flex stop + 3° to α = ext stop − 2°; legs massless;')
    print('  no-load speed scaled from 420 rpm @ 24 V (ASSUMPTION); torque capped at the')
    print('  two published measurements, 4.8 and 9.4 N·m (electronics/03 §1.4).')
    for tag, s in (('selected linkage', best),):
        r = s[6]
        print(f'\n  {tag}:')
        print('    mass       bus    t_lim   takeoff v   CoM rise   push time')
        for mtag, m in masses_.items():
            for bus in (BUS_BENCH, BUS_6S_NOM):
                for tl in (GIM['meas_low'], GIM['meas_high']):
                    v, h, t = jump(alphas, r['n'], m, tl, bus, flex)
                    print(f'    {m:5.3f} kg  {bus:4.1f} V  {tl:4.1f}   {v:5.2f} m/s'
                          f'   {h:6.0f} mm   {t:5.0f} ms')
        m = max(masses_.values())
        print(f'    landing from α = 140° to the flex stop, m = {m:.3f} kg, constant torque:')
        for tl in (GIM['rated'], GIM['meas_low'], GIM['meas_high']):
            h, stroke, fmin = landing(alphas, r['n'], m, tl, 140.0, flex)
            print(f'      {tl:4.1f} N·m → stops a {h:4.0f} mm free drop over {stroke:.0f} mm'
                  f' (weakest point {fmin:.0f} N per leg vs {m * G / 2:.0f} N weight share)')


# ------------------------------------------------------------- 6. part loads
def part_loads(r, alphas, b, flex):
    hr('5.  PUSHROD, PINS AND STOPS')
    f_max = float(np.max(DYN_FACTOR * GIM['stall'] * r['n'] * 1000 / np.abs(r['s'])))
    print(f'  design rod force = 1.5 × 11 N·m stall through the linkage, worst pose: {f_max:.0f} N')
    for size, d1 in ROD_MINOR_D.items():
        i_m = math.pi * d1 ** 4 / 64
        pcr = math.pi ** 2 * E_STEEL * i_m / b ** 2
        print(f'  {size} threaded rod (d1 {d1:.3f} mm), pin-pin {b:.0f} mm: Euler P_cr = {pcr:6.0f} N'
              f'  → factor {pcr / f_max:4.2f} on the compression (flexion) case')
    tau = f_max / (2 * math.pi * PIN_D ** 2 / 4)
    brg = f_max / (2 * PIN_D * CHEEK_T)
    print(f'  Ø{PIN_D:.0f} pin in double shear: τ = {tau:5.1f} MPa;'
          f' bearing on two {CHEEK_T:.0f} mm printed cheeks: {brg:5.1f} MPa'
          f' (PA-CF XY {PA_CF_XY[0]:.0f}–{PA_CF_XY[1]:.0f} MPa; ABS carries no structural load)')
    print(f'  rod-end requirement: static radial rating ≥ 2 × {f_max:.0f} = {2 * f_max:.0f} N')
    arm = (Y_LEG_OUT - GIM_OUT_FACE_X) - Y_ROD_PLANE
    print(f'  crank overhang: rod plane y = {Y_ROD_PLANE} is {arm:.1f} mm inboard of the knee-actuator'
          f' output face → {f_max * arm / 1000:.1f} N·m moment on its output bearing at the design rod force')
    tk = PROOF_WHEEL_N * float(knee_arm(flex)) / 1000
    print(f'  proof screen {PROOF_WHEEL_N:.0f} N at one wheel at the flex stop → knee {tk:.1f} N·m'
          f' → {tk * 1000 / STOP_R:.0f} N at a R{STOP_R:.0f} stop (carried thigh↔shin, not by the rod)')
    i = int(np.argmin(np.abs(alphas - flex)))
    print(f'  actuator stall driven into the flex stop: knee {GIM["stall"] * r["n"][i]:.1f} N·m'
          f' → {GIM["stall"] * r["n"][i] * 1000 / STOP_R:.0f} N at the stop')


# ------------------------------------------------------------ 7. electronics
def electronics(r, alphas, m):
    hr('6.  ELECTRICAL AND CAN CONSEQUENCES')
    i = int(np.argmin(np.abs(alphas - ALPHA_NOM)))
    tc = m * G / 2 * knee_arm(ALPHA_NOM) / 1000 / (ETA * r['n'][i])
    ia = tc / GIM['kt']
    print(f'  standing at α = {ALPHA_NOM:.0f}°: knee crank {tc:.2f} N·m → {ia:.1f} A'
          f' ({100 * ia / GIM["rated_a"]:.0f} % of rated {GIM["rated_a"]} A),'
          f' copper ≈ {ia * ia * GIM["r_phase"]:.1f} W per knee (R [UNVERIFIED])')
    for nodes in (2, 3):
        frames = 2 * nodes
        for rate, scale in (('1 Mbit', 1.0), ('500 kbit', 2.0)):
            typ = frames * FRAME_US_1M[0] * scale / 10
            worst = frames * FRAME_US_1M[1] * scale / 10
            print(f'  {nodes} nodes, command + reply at 1 kHz on {rate:<8s}: {typ:5.1f} % typical,'
                  f' {worst:5.1f} % worst')


def candidates_table(static_knee, jump_knee):
    hr('7.  ACTUATOR SCREEN AT A 1:1-CLASS LINKAGE')
    print(f'  required: stance ≈ {static_knee:.2f} N·m continuous at α = {ALPHA_NOM:.0f}°;'
          f' one full robot weight per leg (1 g net push) at the crouch ≈ {jump_knee:.1f} N·m;')
    print(f'  must run on the {BUS_BENCH:.0f} V bench bus.  Stance/rated is at the knee, before the'
          ' 0.87–0.94 linkage ratio.')
    print('  candidate                   rated  peak   stance/rated  20 V bus   protocol')
    for nm, rated, peak, mass, vmin, vmax, proto in CANDIDATES:
        ok_v = 'yes' if (vmin is None or vmin <= BUS_BENCH) else f'no (≥{vmin} V)'
        print(f'  {nm:<26s} {rated:5.1f} {peak:5.1f}   {100 * static_knee / rated:6.0f} %'
              f'      {ok_v:<10s} {proto}')


# ------------------------------------------------------------------ 8. figure
SURFACE, INK, INK2, MUTED, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#b9b8b2', '#e6e5e0'
DRIVE = '#2a78d6'          # categorical slot 1; validated against SURFACE


def plot(path, best, alphas, flex):
    """Schematic of the selected linkage at three poses plus its two curves."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    _, a, b, c, delta, branch, r = best
    fig = plt.figure(figsize=(12, 8.6), dpi=150, facecolor=SURFACE)
    gs = fig.add_gridspec(2, 6, height_ratios=[1.35, 1.0], hspace=0.32, wspace=0.9)
    poses = [(flex, 'flexion stop'), (ALPHA_NOM, 'legacy nominal'), (ALPHA_EXT_STOP, 'extension stop')]
    for k, (al, name) in enumerate(poses):
        ax = fig.add_subplot(gs[0, 2 * k:2 * k + 2])
        ax.set_facecolor(SURFACE)
        i = int(np.argmin(np.abs(alphas - al)))
        A = math.radians((180.0 - al) / 2)
        u = np.array([math.sin(A), -math.cos(A)])
        v = np.array([math.cos(A), math.sin(A)])
        S = np.zeros(2)
        K = L1 * u
        W = K + L2 * (-math.cos(math.radians(al)) * u - math.sin(math.radians(al)) * v)
        th_c = r['th_c'][i]
        th_l = math.radians(al + delta)
        C = a * (math.cos(th_c) * u + math.sin(th_c) * v)
        P = K + c * (math.cos(th_l) * u + math.sin(th_l) * v)
        ground = W[1] - WHEEL_R
        ax.axhline(ground, color=MUTED, lw=1)
        ax.add_patch(plt.Circle(W, WHEEL_R, fill=False, ec=MUTED, lw=2))
        ax.add_patch(plt.Circle(S, ROOT_R, fill=False, ec=MUTED, lw=1, ls=(0, (4, 3))))
        ax.plot(*zip(S, K), color=INK2, lw=6, solid_capstyle='round')
        ax.plot(*zip(K, W), color=INK2, lw=6, solid_capstyle='round')
        ax.plot(*zip(S, C), color=DRIVE, lw=3, solid_capstyle='round')
        ax.plot(*zip(C, P), color=DRIVE, lw=2)
        ax.plot(*zip(K, P), color=DRIVE, lw=3, solid_capstyle='round')
        for q, col in ((S, INK), (K, INK), (W, INK2), (C, DRIVE), (P, DRIVE)):
            ax.add_patch(plt.Circle(q, 3.2, color=SURFACE, ec=col, lw=1.8, zorder=5))
        ax.text(S[0] - 6, S[1] + 6, 'shoulder', ha='right', va='bottom', fontsize=8, color=INK2)
        ax.text(K[0] + 6, K[1] - 2, 'knee', ha='left', va='top', fontsize=8, color=INK2)
        mid = (C + P) / 2
        if k == 1:
            ax.text(mid[0] + 8, mid[1] + 6, 'pushrod', fontsize=8, color=INK2)
            ax.text(C[0] - 4, C[1] + 6, 'crank', ha='right', fontsize=8, color=INK2)
            ax.text(P[0] + 5, P[1] + 5, 'lever', fontsize=8, color=INK2)
            ax.text(S[0] + ROOT_R * 0.72, S[1] + ROOT_R * 0.72, f'R{ROOT_R:.0f} root /\nØ80 actuator',
                    fontsize=7, color=INK2, ha='left', va='bottom')
        ax.set_title(f'{name}\nα = {al:.0f}°, shoulder–axle {float(leg_d(al)):.0f} mm',
                     fontsize=10, color=INK, loc='left')
        ax.set_aspect('equal')
        ax.set_xlim(-95, 175)
        ax.set_ylim(-300, 70)
        ax.axis('off')

    work = (alphas >= flex) & (alphas <= ALPHA_EXT_STOP)
    for j, (key, title, unit) in enumerate(
            (('n', 'Crank-to-knee ratio N = dθc/dα', ''),
             ('mu', 'Transmission angle μ', '°'))):
        ax = fig.add_subplot(gs[1, 3 * j:3 * j + 3])
        ax.set_facecolor(SURFACE)
        y = r[key]
        ax.axvspan(alphas[0], flex, color=GRID, lw=0)
        ax.axvspan(ALPHA_EXT_STOP, alphas[-1], color=GRID, lw=0)
        ax.plot(alphas, y, color=DRIVE, lw=2)
        if key == 'mu':
            ax.axhline(MU_MIN, color=INK2, lw=1, ls=(0, (4, 3)))
            ax.text(88, MU_MIN + 2, f'{MU_MIN:.0f}° design floor', fontsize=8, color=INK2)
            ax.set_ylim(30, 100)
        else:
            ax.set_ylim(0.8, 1.0)
        ax.set_title(title, fontsize=10, color=INK, loc='left')
        ax.set_xlabel('interior knee angle α (°)   shaded: 2° overtravel into the stops',
                      fontsize=8, color=INK2)
        ax.tick_params(colors=INK2, labelsize=8)
        for sp in ('top', 'right'):
            ax.spines[sp].set_visible(False)
        for sp in ('left', 'bottom'):
            ax.spines[sp].set_color(MUTED)
        ax.grid(axis='y', color=GRID, lw=0.8)
        ax.set_axisbelow(True)
    fig.suptitle('R2A knee drive — crank on the shoulder axis, pushrod to a lever behind the knee'
                 '  (schematic from r2a_calc.py; not CAD)', fontsize=11, color=INK, x=0.02, ha='left')
    fig.savefig(path, facecolor=SURFACE, bbox_inches='tight')
    print(f'\n  wrote {path}')


def main():
    flex = envelope()
    ms = masses()
    m_hi = max(ms.values())
    static_table(m_hi, flex)
    alphas, best, par = synthesise(flex, m_hi)
    r = report_linkage('SELECTED', best, alphas, m_hi, flex)
    performance(alphas, best, par, ms, flex)
    part_loads(r, alphas, best[2], flex)
    electronics(r, alphas, m_hi)
    static_knee = m_hi * G / 2 * knee_arm(ALPHA_NOM) / 1000
    jump_knee = m_hi * G * 1.0 * knee_arm(flex + 3.0) / 1000
    candidates_table(static_knee, jump_knee)
    if '--plot' in sys.argv:
        import os
        plot(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', 'design',
                          'r2a_knee_linkage.png'), best, alphas, flex)


if __name__ == '__main__':
    main()
