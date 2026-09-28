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

  * modelled R2A geometry and volumes      Fusion Beni_R2A_SingleLeg, written by
                                            r2a_lib.write_gate_record() to
                                            evidence/r2a/2026-09-27_digital_gate/
                                            fusion_measurements.json

Values marked ASSUMPTION or DESIGN CHOICE are not facts about hardware.  The
four envelope assumptions of the concept study (rod-end eye R8, jam nut R4.5,
root wall, 60 g linkage allowance) are replaced by the modelled Fusion values
loaded below; the rod-end envelope is a requirement on the purchased part.

Run:  python3 r2a_calc.py            (add --plot to redraw docs/design/r2a_knee_linkage.png)
"""

import json
import math
import os
import sys

import numpy as np

GATE_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'evidence', 'r2a',
                         '2026-09-27_digital_gate', 'fusion_measurements.json')
FUSION = json.load(open(GATE_JSON))

G = 9.80665

# --------------------------------------------------- legacy frozen kinematics
L1 = L2 = 120.0            # mm, guide §4
WHEEL_R = 55.0             # mm, Ø110 OD, guide §4
A_NOM = 50.0               # deg, proximal +50° / distal -50° from vertical
ALPHA_NOM = 180.0 - 2 * A_NOM   # 80° interior knee angle at the legacy nominal

# --------------------------------------------------- lateral stack, design record §3
Y_LEG_IN = 59.5                         # leg inboard face (hub face), design record §3
Y_CHANNEL = (64.5, 84.5)                # former spring channel, 20 mm
Y_TYRE = (69.0, 99.0)                   # rim + tyre
Y_RIM_WEB_OUT = 104.5                   # outboard end of the wheel stack
DISTAL_BOSS_R = 11.0                    # distal knee boss Ø22 (R2A y 65.8…84.8)
# modelled: the outboard half prints on one flat face, so the knee-actuator
# mount face is that face (Fusion; concept value 89.5); the rod plane sits in
# the clevis gap above the M4 hub-screw heads (Fusion; concept value 74.5)
Y_LEG_OUT = FUSION['stack_y_mm']['actuator_mount_face']
Y_ROD_PLANE = FUSION['stack_y_mm']['rod_plane']

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
# Modelled per-leg increment: R2A printed parts in PA-CF + steel hardware at
# its modelled (envelope) volume + TPU plugs, minus the legacy proximal link,
# distal link and encoder bracket they replace.  Densities: beni_lib
# MATERIAL_SPEC (PA-CF 1.15, steel 7.85, TPU 1.20 g/cm3).  No credit is taken
# for the removed spring cartridge or stop parts.
DENSITY = {'PACF': 1.15, 'STEEL': 7.85, 'TPU': 1.20}


def linkage_mass_kg():
    v = FUSION['volumes_mm3']
    add = sum(v[k] * DENSITY[c] for k, c in FUSION['r2a_mass_parts'].items()) / 1e6
    rem = sum(FUSION['legacy_volumes_mm3'].values()) * DENSITY['PACF'] / 1e6
    return add - rem, add, rem


M_LINKAGE = linkage_mass_kg()[0]

# --------------------------------------------------- DESIGN CHOICES / ASSUMPTIONS
TYRE_GAP = 5.0             # mm, minimum tyre-to-leg-root clearance at the flex stop
ROOT_WALL = 3.3            # mm, printed wall outside an M3 clearance hole
ROOT_R = GIM_PCD_R + M3_CLEAR / 2 + ROOT_WALL   # outboard cheek radius holding the actuator
assert abs(ROOT_R - FUSION['outline_mm']['root_r_tyre_side']) < 1e-9   # modelled R42.0
ALPHA_EXT_STOP = 150.0     # deg, extension stop: keep 30° from a straight leg
OVERTRAVEL = 2.0           # deg, linkage must stay valid 2° beyond each stop
CRANK_HUB_R = 19.0         # mm, crank hub Ø38 (same body as Shoulder_Output_Hub_L)
# modelled rod-end design envelope (Fusion stand-in; a purchasing requirement)
ROD_EYE_R = FUSION['rod_end_envelope_mm']['eye_d'] / 2
ROD_SHANK_R = max(FUSION['rod_end_envelope_mm']['neck_d'],
                  FUSION['jam_nut_mm']['across_corners']) / 2
CLR = 2.0                  # mm, minimum running clearance
MU_MIN = 40.0              # deg, minimum transmission angle over the working range
MU_MIN_OVERTRAVEL = 35.0   # deg, allowed only in the 2° overtravel into the bumpers
GAMMA_MIN = 15.0           # deg, keep the crank this far from its toggle
ETA = 0.95                 # linkage efficiency, ASSUMPTION
PIN_D = 5.0                # mm, Ø5 clevis pin
# modelled: worst-case engagement of a floating Ø5 x 18 pin in its thinner ear
CHEEK_T = FUSION['clevis_mm']['min_pin_engagement']
ROD_MINOR_D = {'M5': 5.0 - 1.0825 * 0.8, 'M6': 6.0 - 1.0825 * 1.0}   # ISO 724 d1
E_STEEL = 200e3            # MPa
PA_CF_XY = (84.0, 102.0)   # MPa, beni_rig_no_machining.md §1
PROOF_WHEEL_N = 275.0      # N at one wheel, guide §11 structural screen
# modelled: centroid radius of the smaller radial stop-face overlap
STOP_R = min(0.5 * (r['r0'] + r['r1']) for r in FUSION['stops'].values()
             if isinstance(r, dict) and 'r0' in r)
DYN_FACTOR = 1.5           # ASSUMPTION: dynamic factor on actuator stall torque
SELECT_JUMP_FRAC = 0.97    # DESIGN CHOICE: accept 3 % of idealised push-off for compactness
MAX_PIN_CENTRE = 32.0      # mm, DESIGN CHOICE: pin centres within 32 mm of the link line
MAX_PIN_ENVELOPE = MAX_PIN_CENTRE + ROD_EYE_R   # (the concept's 40 mm with an R8 eye)
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
        m = M_REV2 + 2 * (m_act + M_LINKAGE)
        out[tag] = m
        print(f'  REV2 {M_REV2:.4f} kg + 2 × (knee GIM6010-8 {tag} + {M_LINKAGE * 1000:.0f} g'
              f' linkage) = {m:.3f} kg')
    d, add, rem = linkage_mass_kg()
    print(f'  modelled linkage increment per leg {d * 1000:.0f} g = R2A parts {add * 1000:.0f} g'
          f' - legacy links/bracket {rem * 1000:.0f} g (Fusion volumes; PA-CF, steel, TPU)')
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
          f' bearing on two printed ears at the {CHEEK_T:.1f} mm worst-case pin engagement: {brg:5.1f} MPa'
          f' (PA-CF XY {PA_CF_XY[0]:.0f}–{PA_CF_XY[1]:.0f} MPa; ABS carries no structural load)')
    print(f'  rod-end requirement: static radial rating ≥ 2 × {f_max:.0f} = {2 * f_max:.0f} N')
    arm = (Y_LEG_OUT - GIM_OUT_FACE_X) - Y_ROD_PLANE
    print(f'  crank overhang: rod plane y = {Y_ROD_PLANE} is {arm:.1f} mm inboard of the knee-actuator'
          f' output face → {f_max * arm / 1000:.1f} N·m moment on its output bearing at the design rod force')
    tk = PROOF_WHEEL_N * float(knee_arm(flex)) / 1000
    print(f'  proof screen {PROOF_WHEEL_N:.0f} N at one wheel at the flex stop → knee {tk:.1f} N·m'
          f' → {tk * 1000 / STOP_R:.0f} N at the R{STOP_R:.1f} stop-face centroid (thigh↔shin, not the rod)')
    i = int(np.argmin(np.abs(alphas - flex)))
    print(f'  actuator stall driven into the flex stop: knee {GIM["stall"] * r["n"][i]:.1f} N·m'
          f' → {GIM["stall"] * r["n"][i] * 1000 / STOP_R:.0f} N at the stop')
    st = FUSION['stops']
    print(f'  stop faces: two {st["band_mm"]:.1f} mm bands, radial overlap R{st["flex"]["r0"]:.0f}-{st["flex"]["r1"]:.0f}'
          f' (flexion) / R{st["ext"]["r0"]:.0f}-{st["ext"]["r1"]:.0f} (extension); proof load'
          f' {tk * 1000 / STOP_R:.0f} N on the smaller {2 * st["band_mm"] * (st["ext"]["r1"] - st["ext"]["r0"]):.0f} mm2'
          f' -> {tk * 1000 / STOP_R / (2 * st["band_mm"] * (st["ext"]["r1"] - st["ext"]["r0"])):.1f} MPa')


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


def gate():
    hr('0.  FUSION DIGITAL GATE (modelled values in use)')
    g = FUSION
    print(f"  source: {g['document']} v{g['version']}, {os.path.relpath(GATE_JSON)}")
    e = g['rod_end_envelope_mm']
    print(f"  rod-end design envelope: eye Ø{e['eye_d']:.1f} x {e['eye_w']:.1f}, ball {e['ball_w']:.1f} wide,"
          f" neck Ø{e['neck_d']:.1f}, pin to shank end {e['h']:.1f}; jam nut"
          f" {g['jam_nut_mm']['af']:.1f} AF ({g['jam_nut_mm']['across_corners']:.2f} across corners)")
    print(f"  stop contact: flexion {g['stops']['flex']['contact_deg']:.2f} deg,"
          f" extension {g['stops']['ext']['contact_deg']:.2f} deg (bisected to"
          f" {g['stops']['bisection_tol_deg']:.2f} deg)")
    rows = {r['alpha']: r for r in g['clearances']}
    work = [r for a, r in rows.items() if 51.0 <= a <= 150.0]
    print(f"  tyre to proximal at the flexion stop: {rows[51.0]['tyre_to_proximal_mm']:.2f} mm")
    for key, label in (('rod_to_distal_mm', 'rod/nuts to the distal knee boss'),
                       ('rod_group_to_crank_mm', 'rod group to the crank'),
                       ('rod_group_to_proximal_mm', 'rod group to the proximal halves'),
                       ('crank_to_proximal_mm', 'crank to the proximal halves'),
                       ('encoder_arm_to_proximal_mm', 'encoder arm to the proximal parts')):
        print(f"  min {label:<36s} {min(r[key] for r in work):6.2f} mm (alpha 51..150)")
    print(f"  pin-to-pin in every sampled pose: {min(r['pin_to_pin_mm'] for r in work):.3f}"
          f"..{max(r['pin_to_pin_mm'] for r in work):.3f} mm;"
          f" max |theta_c CAD - solver| = "
          f"{max(abs(r['theta_c_measured_deg'] - r['theta_c_solver_deg']) for r in work):.3f} deg")
    sw = g['sweep']
    print(f"  sweep: {sw['poses']} poses, knee {sw['knee_range']}, shoulder {sw['shoulder_range']};"
          f" real clashes {sw['real_pairs']}")


def stand(flex):
    """Mode A stand with the R2A leg: bench reach and the added static moment.

    Only the distal link and the wheel module can pass below the stand's base
    plane: the knee never gets lower than L1 + the knee cheek below the axis,
    and the knee actuator sits on the axis.  Those parts all lie outboard of the
    leg inboard face, so the stand clamps at a bench edge and the leg overhangs.
    """
    hr('8.  MODE A STAND WITH THE R2A LEG')
    st = FUSION['stand_mm']
    h = -st['base_plane_z']
    y_face = st['outboard_face_y']
    y_leg = FUSION['stack_y_mm']['leg_inboard_face']
    knee_low = L1 + FUSION['outline_mm']['knee_cheek_r']
    print(f'  stand base plane {h:.2f} mm below the shoulder axis; outboard face y = {y_face:.1f}')
    print(f'  lowest point of the knee and everything on the proximal link: {knee_low:.1f} mm'
          f' below the axis (L1 + R{FUSION["outline_mm"]["knee_cheek_r"]:.0f} knee cheek)'
          f' -> always above the bench')
    a_touch = float(alpha_of_d(h - WHEEL_R))
    print(f'  shoulder at 0 (wheel under the axis): tyre reaches the bench plane at alpha ='
          f' {a_touch:.1f} deg')
    for a in (flex, ALPHA_NOM, a_touch, ALPHA_EXT_STOP):
        low = float(leg_d(a)) + WHEEL_R
        print(f'    alpha {a:6.1f} deg: tyre bottom {low:6.1f} mm below the axis,'
              f' {low - h:+6.1f} mm below the bench plane (negative = above it)')
    print(f'  -> the leg must overhang a bench edge.  Every part that can pass below the'
          f' bench plane lies at y >= {y_leg:.1f}, so the bench edge must lie between'
          f' y {y_face:.1f} (stand face fully supported) and y {y_leg - TYRE_GAP:.1f}'
          f' ({TYRE_GAP:.0f} mm from the leg)')
    y_out = FUSION['stack_y_mm']['actuator_cover'][1]
    for tag, m_act in (('bare 388 g', GIM['mass_bare']), ('brief 500 g', GIM['mass_brief'])):
        mom = G * (m_act * (y_out - y_face) + M_LINKAGE * (Y_LEG_OUT - y_face)) / 1000
        print(f'  added static roll moment, knee GIM6010-8 {tag} at <= {y_out - y_face:.1f} mm'
              f' + {M_LINKAGE * 1000:.0f} g linkage at <= {Y_LEG_OUT - y_face:.1f} mm'
              f' outboard of the stand face: <= {mom:.2f} N.m')
    print(f'  against {GIM["stall"]:.2f} N.m shoulder-stall yaw, which already requires the'
          f' stand to be clamped (rig_calc.py mode_a_stand); the knee reaction stays inside'
          f' the leg (stator on the proximal link)')


# ----------------------------------------------------- 9. ABS commissioning
ABS_DENSITY = 1.04          # g/cm3, beni_lib MATERIAL_SPEC 'ABS'
WHEEL_MOTOR_KG = 0.250      # GIM4305-10: ~150 g (electronics/03 §1.2) vs brief 250 g (C4); the larger
# DESIGN CHOICES for the ABS article's powered gates (the test traveller copies these):
LIM_KNEE_DETACHED_A = 1.0   # gate 3: knee actuator driving only the crank and a free rod
LIM_HOLD_MARGIN = 2.0       # gate 4: current limit = this x the self-weight hold bound ...
LIM_STEP_A = 0.5            # ... rounded up to this step
LIM_SHOULDER_DEG = 30.0     # gate 4: shoulder within this of hanging
LIM_SPEED_DPS = 30.0        # gates 3-4: joint speed limit, deg/s at the joint
LIM_CMD_HZ = 100.0          # gates 3-4: command + reply rate per node
DIST_ABS = ('R2A_Distal_Link_L', 'R2A_Lever_Cap_L', 'R2A_Encoder_Arm_L', 'Wheel_Hub_L',
            'ABS_TEST_Wheel_Rim_NoTyre')
DIST_STEEL = ('HW_Pin_D5x18_Lever', 'HW_DowelPin_D4x10_Lever', 'HW_DowelPin_D4x10_EncArm',
              'HW_Magnet_D6x2p5_Diametric', 'HW_SHCS_M4x8', 'HW_SHCS_M3x8', 'R2A_SHCS_M3x10_EncArm',
              'R2A_SHCS_M2p5x10_WheelMotor', 'HW_RodEnd_M5_Upper', 'HW_RodEnd_M5_Lower',
              'HW_Rod_M5x86', 'HW_JamNut_M5')
PROX_ABS = ('R2A_Prox_Inboard_L', 'R2A_Prox_Outboard_L', 'R2A_Crank_L', 'R2A_Crank_Cap_L',
            'R2A_Knee_Pin_Cap_L')
PROX_STEEL = ('HW_Bearing_6800', 'HW_DowelPin_D10x35', 'HW_Pin_D5x18_Crank', 'HW_DowelPin_D4x10_Crank',
              'R2A_SHCS_M3x10_Actuator', 'R2A_SHCS_M3x12_Perimeter', 'R2A_SHCS_M3x10_Crank',
              'R2A_SHCS_M3x6_PinCap', 'HW_SHCS_M4x10')


def _mass(names, density):
    return sum(FUSION['volumes_mm3'][n] for n in names) * density / 1e6


def _ceil_step(x, step):
    return math.ceil(x / step - 1e-9) * step


def commissioning(r, alphas):
    hr('9.  ABS COMMISSIONING LIMITS (test traveller gates 3 and 4)')
    work = (alphas >= 51.0) & (alphas <= ALPHA_EXT_STOP)
    n_min = float(np.min(r['n'][work]))
    m_dist = _mass(DIST_ABS, ABS_DENSITY) + _mass(DIST_STEEL, DENSITY['STEEL']) + WHEEL_MOTOR_KG
    m_prox = _mass(PROX_ABS, ABS_DENSITY) + _mass(PROX_STEEL, DENSITY['STEEL'])
    print(f'  upper bounds from Fusion volumes (ABS {ABS_DENSITY}, steel envelopes, wheel motor'
          f' {WHEEL_MOTOR_KG * 1000:.0f} g; the whole pushrod and every M3 x 8 counted on the distal side):')
    print(f'    distal side {m_dist * 1000:.0f} g, all placed at the wheel centre; proximal side'
          f' {m_prox * 1000:.0f} g, all at the knee; the knee actuator is on the shoulder axis')
    tk = m_dist * G * L2 / 1000
    tc = tk / (ETA * n_min)
    i_k = tc / GIM['kt']
    lim_k = _ceil_step(LIM_HOLD_MARGIN * i_k, LIM_STEP_A)
    print(f'  knee hold, distal link horizontal: <= {tk:.2f} N.m knee -> {tc:.2f} N.m crank'
          f' (N {n_min:.3f}, eta {ETA}) -> {i_k:.2f} A')
    d_max = float(leg_d(ALPHA_EXT_STOP))
    ts = G * (m_prox * L1 + m_dist * d_max) / 1000 * math.sin(math.radians(LIM_SHOULDER_DEG))
    i_s = ts / GIM['kt']
    lim_s = _ceil_step(LIM_HOLD_MARGIN * i_s, LIM_STEP_A)
    print(f'  shoulder hold within {LIM_SHOULDER_DEG:.0f} deg of hanging, leg at the extension stop'
          f' (d {d_max:.1f} mm): <= {ts:.2f} N.m -> {i_s:.2f} A')
    print('  chosen current limits (DESIGN CHOICE, q-axis/phase current as set in the driver):')
    for label, lim in (('gate 3 knee, detached', LIM_KNEE_DETACHED_A),
                       (f'gate 4 knee, {LIM_HOLD_MARGIN:.0f} x hold', lim_k),
                       (f'gate 4 shoulder, {LIM_HOLD_MARGIN:.0f} x hold', lim_s)):
        print(f'    {label:<28s} {lim:4.1f} A = {lim * GIM["kt"]:.2f} N.m output'
              f' ({100 * lim / GIM["rated_a"]:.0f} % of rated {GIM["rated_a"]} A)')
    f_rod = float(np.max(lim_k * GIM['kt'] * r['n'][work] * 1000 / np.abs(r['s'][work])))
    i_f = int(np.argmin(np.abs(alphas - 51.0)))
    f_stop = lim_k * GIM['kt'] * r['n'][i_f] * 1000 / STOP_R
    print(f'  at the gate 4 knee limit: rod force <= {f_rod:.0f} N (design {DYN_FACTOR} x stall case in §5);'
          f' driven into the flexion stop <= {f_stop:.0f} N at R{STOP_R:.1f}')
    sp_c = LIM_SPEED_DPS * float(np.max(r['n'][work]))
    print(f'  speed limit {LIM_SPEED_DPS:.0f} deg/s at each joint: knee crank <= {sp_c:.1f} deg/s'
          f' = {sp_c / 360:.3f} turn/s at the output; shoulder {LIM_SPEED_DPS / 360:.3f} turn/s')
    for rate, scale in (('1 Mbit', 1.0), ('500 kbit', 2.0)):
        typ = 2 * 2 * LIM_CMD_HZ * FRAME_US_1M[0] * scale / 1e4
        worst = 2 * 2 * LIM_CMD_HZ * FRAME_US_1M[1] * scale / 1e4
        print(f'  2 nodes, command + reply at {LIM_CMD_HZ:.0f} Hz on {rate:<8s}: {typ:4.1f} % typical,'
              f' {worst:4.1f} % worst')


def main():
    gate()
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
    stand(flex)
    commissioning(r, alphas)
    if '--plot' in sys.argv:
        import os
        plot(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', 'design',
                          'r2a_knee_linkage.png'), best, alphas, flex)


if __name__ == '__main__':
    main()
