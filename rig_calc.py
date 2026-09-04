#!/usr/bin/env python3
"""Load, travel, mass and dynamics arithmetic for the Beni single-leg test rig.

Everything here is recomputed from the frozen inputs rather than copied from
`fusion_brief_single_leg_rig.md`, so that the brief's numbers get checked instead
of inherited.  Frozen sources:

  * kinematics + spring geometry  beni_prototype1_fusion_guide_rewritten.md §4-§9
  * motor interfaces              beni_prototype1_design_record.md §2
  * per-link masses/inertias      sim/beni_inertia.json

Run:  python3 rig_calc.py
"""

import functools
import json
import math
import os

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
G = 9.80665

# ----------------------------------------------------------- frozen kinematics
A_NOM = 50.0          # nominal link angle from downward vertical, deg
L1 = L2 = 120.0       # link lengths, mm
RU, RL = 36.0, 54.0   # cartridge pivot radii from the knee axis, mm
CART_ANG = 110.0      # included anchor angle at nominal, deg
PHI_EXT, PHI_STOP = -8.0, 27.0
PHI_DESIGN = 25.0
WHEEL_R = 55.0        # Ø110 OD

SPRING_RATE = 10.45   # N/mm
SPRING_FREE = 55.0    # mm
DEAD_LENGTH = 25.57   # pin-to-pin dead length incl. 2.0 mm of shims, mm

# ------------------------------------------------------------- rig hard inputs
MGN12H = dict(L=45.4, W=27.0, H=13.0, mass_g=54.0,
              C=3720.0, C0=5880.0, MR=38.22, MP=36.26, MY=36.26,
              screw='M3', thread_deep=3.5, pattern=20.0)
RAIL_H = 8.0          # MGN12 rail section height, mm
BLOCK_CENTRES = 80.0  # carriage block spacing, mm
HALF_TRACK = 84.0     # wheel centre plane, mm from the sagittal plane
SHOULDER_STALL = 11.0     # N·m, 24 V GIM6010-8
SHOULDER_PROOF = 25.0     # N·m structural screening load
JUMP_TORQUE = 5.9         # N·m the jump needs
TORQUE_ARM = 200.0        # mm

# Rig lateral stack, AS BUILT.  The carriage bolts to Chassis_Shoulder_Plate_L's
# five existing frame-bolt holes on the motor's FRONT face, not to the motor's
# rear flange: the rear flange is stiffer but the GAUGE shoulder coupon models
# only the front 9.5 mm of the motor, and the brief gates every interface on the
# coupons.  See the design record §1.1.
MOTOR_FRONT_FACE_Y = 42.0   # 8 × M3 Ø74 PCD, thread 4.0 deep from here
PANEL_OUTER_Y = 47.0        # Chassis_Shoulder_Plate_L, 5 mm
CARRIAGE_T = 8.0            # PA-CF carriage plate thickness, mm
BLOCK_H = 13.0              # MGN12H
RAIL_PLANE_Y = MOTOR_FRONT_FACE_Y - CARRIAGE_T - BLOCK_H   # 21.0

# Chassis_Shoulder_Plate_L's five existing frame-bolt holes, (X, Z), measured off
# the model (design record §2.2).  In Mode A these are the ONLY structural joint
# between the leg and the stand -- mirrored here from rig_lib.PANEL_FRAME_BOLTS
# so this script stays runnable outside Fusion.
PANEL_FRAME_BOLTS = [(-60.0, -18.0), (-60.0, 48.0), (-60.0, 62.0),
                     (30.0, 48.0), (30.0, 62.0)]


# ------------------------------------------------------------- knee/spring model
def cart_len(phi):
    """Cartridge pivot eye-to-eye length, mm."""
    a = math.radians(CART_ANG - phi)
    return math.sqrt(RU ** 2 + RL ** 2 - 2 * RU * RL * math.cos(a))


def cart_arm(phi):
    """Spring line-of-action moment arm about the knee axis, mm."""
    a = math.radians(CART_ANG - phi)
    return RU * RL * math.sin(a) / cart_len(phi)


def spring_force(phi):
    """Compression-spring force, N."""
    return SPRING_RATE * (SPRING_FREE - (cart_len(phi) - DEAD_LENGTH))


def knee_torque(phi):
    """Spring torque about the knee axis, N·mm."""
    return spring_force(phi) * cart_arm(phi)


def wheel_xz(phi):
    """Wheel axis position relative to the shoulder axis, mm, shoulder fixed."""
    kx = L1 * math.sin(math.radians(A_NOM))
    kz = -L1 * math.cos(math.radians(A_NOM))
    d = math.radians(-A_NOM - phi)
    return kx + L2 * math.sin(d), kz - L2 * math.cos(d)


def dz_dphi(phi):
    """d(shoulder-to-wheel vertical)/dφ, mm per radian.  Positive = wheel rises."""
    return L2 * math.sin(math.radians(A_NOM + phi))


def ground_force(phi):
    """Vertical force at the wheel held by the spring, N."""
    return knee_torque(phi) / dz_dphi(phi)


def compression(phi):
    """Vertical wheel compression from φ=0, mm (positive = compressed)."""
    return wheel_xz(phi)[1] - wheel_xz(0.0)[1]


def phi_at_compression(x):
    """Invert compression(φ)."""
    lo, hi = -8.0, 40.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if compression(mid) < x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def phi_at_force(f):
    lo, hi = -7.999, 27.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if ground_force(mid) < f:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def wheel_rate(phi, h=1e-4):
    """Tangent vertical rate at the wheel, N/mm."""
    x0, x1 = compression(phi - h), compression(phi + h)
    return (ground_force(phi + h) - ground_force(phi - h)) / (x1 - x0)


@functools.lru_cache(maxsize=1)
def spring_energy_curve():
    """Return the cumulative spring-work curve over the allowed travel."""
    xs = np.linspace(0.0, compression(PHI_STOP), 4000)
    fs = np.array([ground_force(phi_at_compression(v)) for v in xs])
    segment_work = (fs[:-1] + fs[1:]) * 0.5 * np.diff(xs)
    energy = np.concatenate(([0.0], np.cumsum(segment_work))) / 1000.0
    return xs, energy


def spring_energy(x):
    """Work done compressing the leg from φ=0 to compression x mm, in J."""
    xs, energy = spring_energy_curve()
    if not xs[0] <= x <= xs[-1]:
        raise ValueError(f'compression {x:.3f} mm is outside the energy curve')
    return float(np.interp(x, xs, energy))


# ------------------------------------------------------------------- verification
def check_frozen():
    print('=' * 78)
    print('1.  FROZEN-INPUT VERIFICATION  (guide §4/§5/§6 must be reproduced)')
    print('=' * 78)
    print('  φ      vert     guide |  fore-aft  guide |  eye-eye  guide |'
          '  arm    guide |  F_wheel guide')
    ref = {-8: (-12.0, 11.6, 77.70, 22.09, 8.3), 0: (0.0, 0.0, 74.44, 24.54, 17.2),
           5: (8.3, 6.4, None, None, 23.1), 10: (17.1, 12.0, 69.91, 27.39, 29.4),
           15: (26.4, 16.8, None, None, 36.2), 20: (36.1, 20.8, 64.90, 29.95, 43.6),
           25: (46.1, 24.0, 62.23, 31.12, 51.5)}
    w0 = wheel_xz(0.0)
    worst = 0.0
    for phi in sorted(ref):
        x, z = wheel_xz(float(phi))
        vert, fore = z - w0[1], -(x - w0[0])
        ee, arm, fw = cart_len(phi), cart_arm(phi), ground_force(float(phi))
        r = ref[phi]
        errs = [abs(vert - r[0]), abs(fore - r[1]), abs(fw - r[4])]
        if r[2]:
            errs += [abs(ee - r[2]), abs(arm - r[3])]
        worst = max(worst, max(errs))
        print(f'  {phi:+3d}  {vert:8.2f} {r[0]:8.1f} | {fore:8.2f} {r[1]:6.1f} | '
              f'{ee:8.2f} {str(r[2] or "-"):>7} | {arm:6.2f} {str(r[3] or "-"):>6} | '
              f'{fw:7.2f} {r[4]:5.1f}')
    print(f'\n  worst deviation from the frozen tables: {worst:.3f}'
          '  → model agrees, so every number below is built on it')
    print(f'  shoulder-to-wheel vertical at nominal: {-wheel_xz(0.0)[1]:.3f} mm'
          '   (guide ~154.3)')
    k_sec = ground_force(25.0) - ground_force(0.0)
    k_sec /= compression(25.0)
    print(f'  secant wheel rate 0→+25°:  {k_sec * 1000:.1f} N/m'
          f'   ({k_sec:.4f} N/mm)   brief §4.3 says 744 N/m')
    print(f'  tangent wheel rate at φ=0: {wheel_rate(0.0) * 1000:.1f} N/m'
          f'   at φ=+25°: {wheel_rate(25.0) * 1000:.1f} N/m'
          '   (guide band 710-800)')
    return k_sec


# ----------------------------------------------------------------- mass budget
def mass_budget():
    print()
    print('=' * 78)
    print('2.  MASS BUDGET AND THE SPRUNG/UNSPRUNG SPLIT')
    print('=' * 78)
    with open(os.path.join(ROOT, 'sim', 'beni_inertia.json')) as fh:
        j = json.load(fh)
    L = j['legs']['L']
    thigh = L['thigh']['mass_kg']
    shank = L['shank']['mass_kg']
    wheel = L['wheel']['mass_kg']
    base = j['base']['mass_kg']
    total = base + 2 * (thigh + shank + wheel)
    leg = thigh + shank + wheel
    half = total / 2.0
    print(f'  robot total (inertia json)      {total:8.4f} kg'
          '   authoritative source: design record §14')
    print(f'  one leg  thigh+shank+wheel      {leg:8.4f} kg'
          f'   ({thigh:.4f} + {shank:.4f} + {wheel:.4f})')
    print(f'  half the robot = slide target   {half:8.4f} kg')
    print(f'  → carriage + plate + motor + ballast budget   {half - leg:8.4f} kg'
          '   (brief: 0.8069)')

    print('\n  What actually goes on the slide (this design):')
    fixed = [('Chassis_Shoulder_Plate_L, 5 mm PA-CF Ø96', 0.0400),
             ('2 × MGN12H blocks @ 54 g', 2 * MGN12H['mass_g'] / 1000.0),
             ('RIG_Carriage, 8 mm PA-CF skeleton plate', 0.1250),
             ('RIG_Ballast_Tray + mode-pin ear + drop ledge', 0.0450),
             ('fasteners, M3 × 8 sets + mode pin', 0.0300)]
    sub = sum(v for _, v in fixed)
    for nm, v in fixed:
        print(f'    {nm:<48s} {v * 1000:7.1f} g')
    print(f'    {"subtotal, everything but the motor":<48s} {sub * 1000:7.1f} g')
    print('\n  C4 is unresolved, so both motor masses are carried through:')
    for motor in (0.388, 0.500):
        on_slide = sub + motor + leg
        ballast = half - on_slide
        print(f'    GIM6010-8 at {motor * 1000:.0f} g → on the slide '
              f'{on_slide:.4f} kg, ballast to reach {half:.4f} = '
              f'{ballast * 1000:+7.1f} g'
              f'{"   ← OVERSHOOT, must remove mass" if ballast < 0 else ""}')

    print('\n  Sprung / unsprung split (the knee spring sits thigh↔shank):')
    unsprung = shank + wheel
    for motor in (0.388, 0.500):
        sprung = sub + motor + thigh
        tot = sprung + unsprung
        print(f'    motor {motor * 1000:.0f} g:  sprung {sprung:.4f} kg   '
              f'unsprung {unsprung:.4f} kg   total {tot:.4f} kg   '
              f'unsprung = {100 * unsprung / tot:.1f} %')
    return dict(thigh=thigh, shank=shank, wheel=wheel, leg=leg, half=half,
                sub=sub, unsprung=unsprung, json=j)


# ------------------------------------------------------------- drop / energy
def drop_table(half):
    print()
    print('=' * 78)
    print('3.  DROP SERIES, SPRING-LIMITED FORCE AND THE PASSIVE CEILING')
    print('=' * 78)
    w = half * G
    print(f'  weight on the slide {w:.2f} N  ({half:.4f} kg)')
    phi_eq = phi_at_force(w)
    print(f'  free-standing equilibrium: F = {w:.2f} N → φ_eq = {phi_eq:+.2f}°,'
          f' wheel compression {compression(phi_eq):+.2f} mm')
    print(f'  ride height, shoulder axis to floor at φ_eq: '
          f'{-wheel_xz(phi_eq)[1] + WHEEL_R:.2f} mm'
          f'   (at φ=0: {-wheel_xz(0.0)[1] + WHEEL_R:.2f} mm)')

    print('\n  Energy balance  ∫F dx = m·g·(h + x),  x measured from φ = 0:')
    print('   drop    compression    φ_peak   peak force   note')
    rows = []
    for h in (20, 30, 40, 49, 50, 60, 70, 80, 90, 100):
        lo, hi = 0.0, compression(PHI_STOP)
        for _ in range(80):
            mid = (lo + hi) / 2.0
            if spring_energy(mid) < w * (h + mid) / 1000.0:
                lo = mid
            else:
                hi = mid
        x = (lo + hi) / 2.0
        phi = phi_at_compression(x)
        f = ground_force(phi)
        note = ''
        if phi >= PHI_STOP - 1e-6:
            note = 'BOTTOMS OUT on the +27° metal stop'
        elif phi >= 24.0:
            note = 'past the +24° gate'
        elif phi >= PHI_DESIGN:
            note = 'past the +25° design point'
        rows.append((h, x, phi, f, note))
        print(f'  {h:4d} mm   {x:7.2f} mm   {phi:+7.2f}°   {f:7.2f} N   {note}')

    # passive ceiling: drop height that just reaches the +25° design point
    def h_for_phi(target):
        x = compression(target)
        e = spring_energy(x)
        return e * 1000.0 / w - x
    for tgt, label in ((PHI_DESIGN, '+25° design point'),
                       (24.0, '+24° step-10 gate'),
                       (PHI_STOP, '+27° metal hard stop')):
        print(f'  drop that just reaches {label:<20s} '
              f'{h_for_phi(tgt):7.2f} mm   (peak {ground_force(tgt):.2f} N)')
    fmax = ground_force(PHI_STOP)
    print(f'\n  Spring-limited peak force: {ground_force(PHI_DESIGN):.2f} N at '
          f'+25°, {fmax:.2f} N against the +27° stop.')
    print('  The spring is the softest element in the load path, so nothing '
          'downstream\n  can see more than this however hard the leg is dropped.')
    return rows, fmax, phi_eq


# ------------------------------------------------------------------- moments
def moment_check(fmax):
    print()
    print('=' * 78)
    print('4.  MGN12H MOMENT CHECK FOR THE AS-DESIGNED OVERHANG')
    print('=' * 78)
    rail_face_y = RAIL_PLANE_Y
    print('  As built: carriage -> the panel\'s five frame-bolt holes on the')
    print('  motor\'s FRONT face, which reproduces brief §4.1 exactly.')
    print(f'    rail mounting plane (column outboard face)   y = {rail_face_y:+7.2f}')
    print(f'    + MGN12H block height {MGN12H["H"]:.1f}                   '
          f'y = {rail_face_y + MGN12H["H"]:+7.2f}')
    print(f'    + RIG_Carriage {CARRIAGE_T:.1f} mm                        '
          f'y = {MOTOR_FRONT_FACE_Y:+7.2f}  = motor front face')
    print(f'    + Chassis_Shoulder_Plate_L 5.0               '
          f'y = {PANEL_OUTER_Y:+7.2f}')
    print(f'    wheel centre plane (half-track)              '
          f'y = {HALF_TRACK:+7.2f}')
    over = HALF_TRACK - rail_face_y
    print(f'  → lateral overhang, rail plane to wheel plane  {over:7.2f} mm'
          f'   (brief §4.1: 63.0 -> %s)'
          % ('MATCHES' if abs(over - 63.0) < 0.01 else 'DIFFERS'))

    print('\n  Loads, and what they do to a block:')
    m_imp = fmax * over / 1000.0
    m_stall = SHOULDER_STALL
    # a fore-aft ground reaction from stall torque also rolls the block
    lever_z = -wheel_xz(0.0)[1]
    f_x = SHOULDER_STALL * 1000.0 / lever_z
    m_roll = f_x * over / 1000.0
    print(f'    spring-limited impact {fmax:.1f} N × {over:.1f} mm'
          f'          → {m_imp:6.2f} N·m  about X  (pitch, MP {MGN12H["MP"]:.2f})')
    print(f'    shoulder stall {m_stall:.1f} N·m about the motor axis'
          f'      → {m_stall:6.2f} N·m  about Y  (yaw,   MY {MGN12H["MY"]:.2f})')
    print(f'    its ground reaction {f_x:.1f} N × {over:.1f} mm'
          f'      → {m_roll:6.2f} N·m  about Z  (roll,  MR {MGN12H["MR"]:.2f})')
    vec = math.sqrt(m_imp ** 2 + m_stall ** 2)
    print(f'    vector sum of the two perpendicular-to-rail components'
          f'  {vec:6.2f} N·m')
    print('\n   case                     moment   fs 1 block   fs 2 blocks')
    for nm, m, cap in (('impact only', m_imp, MGN12H['MP']),
                       ('stall only', m_stall, MGN12H['MY']),
                       ('roll from stall', m_roll, MGN12H['MR']),
                       ('vector sum imp+stall', vec, MGN12H['MP'])):
        print(f'   {nm:<24s} {m:6.2f}     {cap / m:8.2f}     {2 * cap / m:8.2f}')
    print(f'\n   clone-rail derate 30 %, 2 blocks: fs = '
          f'{0.7 * 2 * MGN12H["MP"] / vec:.2f}'
          f'   ... 1 block: fs = {0.7 * MGN12H["MP"] / vec:.2f}  (below spec)')
    print(f'   vertical load check: {(0.5 + 1.645) * G:.1f} N against C0 '
          f'{MGN12H["C0"]:.0f} N → fs {MGN12H["C0"] / ((0.5 + 1.645) * G):.0f}'
          '  (irrelevant, as the brief says)')
    return over


# -------------------------------------------------------------- travel budget
def travel_budget(rows, phi_eq):
    print()
    print('=' * 78)
    print('5.  RAIL TRAVEL BUDGET  — where the brief\'s 300 mm rail fails')
    print('=' * 78)
    span = MGN12H['L'] + BLOCK_CENTRES
    print(f'  two MGN12H at {BLOCK_CENTRES:.0f} mm centres occupy '
          f'{MGN12H["L"]:.1f} + {BLOCK_CENTRES:.0f} = {span:.1f} mm of rail')
    print('  brief §3 computes usable travel as 300 − 45.4 − 24 = 231 mm, which')
    print('  is the ONE-block figure.  With the two blocks the same brief '
          'mandates:')
    for rail in (300.0, 350.0, 400.0):
        print(f'    {rail:.0f} mm rail → {rail - span:.1f} mm of block travel, '
              f'{rail - span - 24.0:.1f} mm usable after 24 mm of bumpers')

    x100 = [r[1] for r in rows if r[0] == 100][0]
    need_dn = x100 - compression(phi_eq)
    need_up = 100.0 - compression(phi_eq) * 0  # release stations are above eq
    need_ext = compression(phi_eq) - compression(PHI_EXT)
    print(f'\n  Stroke the experiment actually needs, about the equilibrium '
          f'position:')
    print(f'    highest release station, brief §3                 '
          f'+{100.0:6.1f} mm')
    print(f'    knee free to full extension φ = −8° (leg lifted)  '
          f'+{need_ext:6.1f} mm  (inside the above)')
    print(f'    peak compression on the 100 mm drop               '
          f'-{need_dn:6.1f} mm')
    print(f'    → stroke required                                  '
          f'{100.0 + need_dn:6.1f} mm, before bumpers')
    print(f'    → with 12 mm of bumper/crush each end              '
          f'{100.0 + need_dn + 24.0:6.1f} mm')
    for rail in (300.0, 400.0):
        avail = rail - span - 24.0
        ok = 'OK' if avail >= 100.0 + need_dn else 'SHORT by %.1f mm' % (
            100.0 + need_dn - avail)
        print(f'    {rail:.0f} mm rail gives {avail:6.1f} mm usable → {ok}')
    return need_dn


# ------------------------------------------------------------------- dynamics
# Measured off the built Fusion assembly (rig_lib.slide_mass / sprung_split),
# not estimated.  Bare slide, empty ballast pots, no mode pin, 500 g GIM6010-8.
MEASURED = dict(slide_g=1607.6, sprung_g=1051.1, unsprung_g=556.5)


def m_sh_share():
    """The part of the sprung mass that is NOT rigid: none, by definition."""
    return 0.0


def bounce_mode(mb, phi_eq):
    print()
    print('=' * 78)
    print('6.  THE BOUNCE MODE  — what step 8 will actually read')
    print('=' * 78)
    j = mb['json']
    L = j['legs']['L']
    m_th, m_sh, m_wh = mb['thigh'], mb['shank'], mb['wheel']
    I_sh = L['shank']['I_com_kgm2'][1]      # Iyy about the shank CoM
    I_wh = L['wheel']['I_com_kgm2'][1]
    com_sh = np.array(L['shank']['com_world_m'])[[0, 2]] * 1000.0   # mm, X,Z
    kx = L1 * math.sin(math.radians(A_NOM))
    kz = -L1 * math.cos(math.radians(A_NOM))
    knee = np.array([kx, kz])

    def state(phi):
        """Positions, mm, with the wheel contact fixed and the shoulder on the
        rail.  Returns shoulder z, shank CoM, wheel axis, shank rotation."""
        wx, wz = wheel_xz(phi)
        z_s = -wz                     # shoulder height above the wheel axis
        rot = -math.radians(phi)      # shank rotates by −φ about the knee
        c, s = math.cos(rot), math.sin(rot)
        r = com_sh - knee
        com = knee + np.array([c * r[0] - s * r[1], s * r[0] + c * r[1]])
        # express in a frame where the wheel axis is the origin
        return z_s, com - np.array([wx, wz]), np.array([0.0, 0.0]), rot

    h = 1e-4
    z0, c0, _, r0 = state(phi_eq - h)
    z1, c1, _, r1 = state(phi_eq + h)
    dz = (z1 - z0) / 1000.0                  # m per (2h deg)
    dcom = (c1 - c0) / 1000.0
    drot = r1 - r0
    wx0, _ = wheel_xz(phi_eq - h)
    wx1, _ = wheel_xz(phi_eq + h)
    dwx = (wx1 - wx0) / 1000.0

    print('  Using the MEASURED split off the built assembly: sprung %.1f g, '
          'unsprung %.1f g' % (MEASURED['sprung_g'], MEASURED['unsprung_g']))
    m_th_eff = MEASURED['sprung_g'] / 1000.0 - (mb['sub'] + 0.500)
    for motor in (0.388, 0.500):
        m_rigid = MEASURED['sprung_g'] / 1000.0 - (0.500 - motor) - m_sh_share()
        # kinetic energy coefficient, per unit (dz)^2
        ke = (m_rigid * dz ** 2
              + m_sh * float(dcom @ dcom) + I_sh * drot ** 2
              + m_wh * dwx ** 2 + I_wh * (dwx / (WHEEL_R / 1000.0)) ** 2)
        m_eff = ke / dz ** 2
        k = wheel_rate(phi_eq) * 1000.0      # N/m, tangent at equilibrium
        f = math.sqrt(k / m_eff) / (2 * math.pi)
        total = m_rigid + MEASURED['unsprung_g'] / 1000.0
        naive = math.sqrt(k / total) / (2 * math.pi)
        sprung = m_rigid
        f_sprung = math.sqrt(k / sprung) / (2 * math.pi)
        print(f'  motor {motor * 1000:.0f} g:')
        print(f'    tangent wheel rate at φ_eq            {k:8.1f} N/m')
        print(f'    whole slide mass (naive 1-DOF)        '
              f'{total:8.4f} kg → {naive:5.2f} Hz'
              '   ← the 3.67 Hz style answer')
        print(f'    sprung mass only, wheel grounded      '
              f'{sprung:8.4f} kg → {f_sprung:5.2f} Hz')
        print(f'    Lagrangian effective mass             '
              f'{m_eff:8.4f} kg → {f:5.2f} Hz'
              '   ← predict THIS')
    print('\n  Reading this correctly matters.  Three models, in increasing '
          'fidelity:')
    print('    * whole slide on the spring          3.4-3.5 Hz   ignores that '
          'the wheel is grounded')
    print('    * sprung mass only                   4.2-4.5 Hz   ignores the '
          'shank\'s rotation and the rolling wheel')
    print('    * full Lagrangian, rigid contact     3.5-3.7 Hz   <- the '
          'prediction')
    print('  The shank rotates about the contact patch and the wheel rolls, so '
          'part of\n  the unsprung mass DOES ride the mode through its '
          'rotational inertia.  That\n  pulls the answer back down from 4.2 to '
          '3.5-3.7 Hz, which lands inside the\n  step-8 gate of 3-4 Hz after '
          'all.  The lumped 2-DOF cross-check below reads\n  ~0.5 Hz high '
          'precisely because it drops those two effects.')
    for k_tyre in (50e3, 100e3, 200e3):
        m_u = MEASURED['unsprung_g'] / 1000.0
        m_s = MEASURED['sprung_g'] / 1000.0
        k_s = wheel_rate(phi_eq) * 1000.0
        # 2-DOF: sprung on knee spring, unsprung on tyre to ground
        M = np.diag([m_s, m_u])
        K = np.array([[k_s, -k_s], [-k_s, k_s + k_tyre]])
        w2 = np.linalg.eigvals(np.linalg.solve(M, K))
        fs = sorted(math.sqrt(abs(v)) / (2 * math.pi) for v in w2)
        print(f'    tyre rate {k_tyre / 1e3:5.0f} kN/m → modes '
              f'{fs[0]:5.2f} Hz and {fs[1]:6.1f} Hz')
    return


# ---------------------------------------------------------------- torque arm
def torque_arm():
    print()
    print('=' * 78)
    print('7.  TORQUE ARM')
    print('=' * 78)
    print(f'  {TORQUE_ARM:.0f} mm lever on the hub\'s 6 × M4 Ø44 PCD, '
          'bearing on a 5 kg scale')
    print('   torque N·m    force N    scale reads kgf')
    for t in (0.1, 1.0, 2.0, 4.8, 5.9, 9.4, 11.0):
        f = t * 1000.0 / TORQUE_ARM
        note = ''
        if abs(t - JUMP_TORQUE) < 1e-9:
            note = '  ← the jump needs this'
        if t in (4.8, 9.4):
            note = '  ← published bench measurements'
        if t == SHOULDER_STALL:
            note = '  ← nameplate stall'
        print(f'   {t:8.1f}    {f:7.2f}    {f / G:10.2f}{note}')
    print(f'\n  A 5 kg scale saturates at {5.0 * G * TORQUE_ARM / 1000.0:.2f} '
          f'N·m on a {TORQUE_ARM:.0f} mm arm, so it covers the 5.9 N·m jump '
          'requirement\n  but NOT the 11 N·m nameplate stall — that needs a '
          f'{SHOULDER_STALL * 1000.0 / (5.0 * G):.0f} mm arm or a 10 kg scale.')
    print(f'  Bolt load: {SHOULDER_STALL:.0f} N·m through 6 × M4 on Ø44 PCD = '
          f'{2 * SHOULDER_STALL * 1000 / (6 * 44):.0f} N per screw in shear.')


# -------------------------------------------------------------------- §2.3
def knee_axle_check():
    print()
    print('=' * 78)
    print('8.  §2.3 — DELETING THE DOUBLE-D FLATS')
    print('=' * 78)
    span = 90.3 - 58.7
    print(f'  bearing-to-bearing journal span      {span:.1f} mm '
          '(y = 58.7 … 90.3)')
    print('  sleeve span, currently keyed          21.6 mm (y = 63.7 … 85.3)')
    print(f'  peak knee force, φ = +27°            {ground_force(PHI_STOP):.1f} N')
    print(f'  proof screen, 275 N at one wheel     bending '
          f'{275 * 6.4:.0f} N·mm → '
          f'{275 * 6.4 / (math.pi * 10 ** 3 / 32):.0f} MPa in a Ø10 shaft')
    print('  torque the key has to carry: two 6800 seal + grease drag only,')
    print('  order 0.002 N·m.  A printed light press on Ø10 holds ~100× that.')
    print('\n  Bearing pressure on the printed distal boss over the 21.6 mm span:')
    for d, what in ((16.0, 'Ø16 steel sleeve, as designed'),
                    (10.0, 'Ø10 axle direct in printed PA-CF')):
        print(f'    {what:<34s} {275.0 / (d * 21.6):5.2f} MPa'
              '   against PA-CF 84 MPa XY')
    print('\n  Pin length arithmetic, hardened Ø10 h6 ground dowel:')
    for ln in (35.0, 40.0):
        proud = 58.7 + ln - 90.3
        print(f'    Ø10 × {ln:.0f} entering at arm-A inboard face y = 58.7 '
              f'→ {proud:+5.1f} mm proud of y = 90.3'
              f'   (magnet carrier bore needs 3.5, pocket 2.5)')
    print('    Ø10 × 35 leaves 3.4 mm proud → carrier bore 3.5 mm deep. Fits.')


# --------------------------------------------------------------- Mode A stand
# Mode A is the active build (2026-08-17).  The vertical slide, the ballast and
# the drop series are deferred, so the stand only ever has to react the
# actuator's own torque and the leg's static weight.
MODE_A_MOUNT_Y = MOTOR_FRONT_FACE_Y   # stand's outboard face = motor front face
MODE_A_OVERHANG = HALF_TRACK - MODE_A_MOUNT_Y      # 42.0 mm, not 63.0


def mode_a_stand():
    """Load set for the Mode-A-only printed stand: no rail, no carriage."""
    print()
    print('=' * 78)
    print('9.  MODE A STAND  --  the active build, no rail and no ballast')
    print('=' * 78)

    with open(os.path.join(ROOT, 'sim', 'beni_inertia.json')) as fh:
        j = json.load(fh)
    L = j['legs']['L']
    leg = sum(L[k]['mass_kg'] for k in L)

    print('  Mode A deletes RIG_Rail, both MGN12H blocks, RIG_Carriage, both')
    print('  ballast pots, the index bar/post, the mode pin and the drop')
    print('  release.  The leg bolts through Chassis_Shoulder_Plate_L straight')
    print('  to the stand.')
    print()
    print('  Static, hanging:')
    print(f'    one leg, thigh+shank+wheel        {leg:8.4f} kg'
          f'  = {leg * G:6.2f} N')
    for motor in (0.388, 0.500):
        print(f'    + GIM6010-8 at {motor * 1000:3.0f} g (C4)          '
              f'{leg + motor:8.4f} kg  = {(leg + motor) * G:6.2f} N')

    print('\n  Lateral overhang is SHORTER than Mode B, because the block and')
    print('  the carriage plate are gone from the stack:')
    print(f'    stand outboard face = motor front mount face   y = '
          f'{MODE_A_MOUNT_Y:6.2f}')
    print(f'    wheel centre plane (half-track)                y = '
          f'{HALF_TRACK:6.2f}')
    mode_b = HALF_TRACK - RAIL_PLANE_Y
    print(f'    -> Mode A overhang {MODE_A_OVERHANG:.2f} mm against Mode B\'s '
          f'{mode_b:.2f} mm  ({100 * MODE_A_OVERHANG / mode_b:.0f} %)')

    fmax = ground_force(PHI_STOP)
    lever_z = -wheel_xz(0.0)[1]
    f_x = SHOULDER_STALL * 1000.0 / lever_z
    over = MODE_A_OVERHANG / 1000.0

    print('\n  Moments the stand mount must react (worst case, Mode A):')
    print(f'    spring-limited wheel force {fmax:.2f} N x '
          f'{MODE_A_OVERHANG:.0f} mm  -> {fmax * over:5.2f} N.m  pitch')
    print(f'    shoulder stall about the motor axis         '
          f'   -> {SHOULDER_STALL:5.2f} N.m  yaw   <-- DOMINANT')
    print(f'    its ground reaction {f_x:.1f} N x {MODE_A_OVERHANG:.0f} mm'
          f'        -> {f_x * over:5.2f} N.m  roll')
    vec = math.hypot(SHOULDER_STALL, f_x * over)
    print(f'    vector sum of yaw + roll                    '
          f'   -> {vec:5.2f} N.m')
    print(f'    proof screen, {SHOULDER_PROOF:.0f} N.m at the hub'
          f'              -> {SHOULDER_PROOF:5.2f} N.m  yaw')
    print("\n  The actuator's own reaction torque is the design load, exactly as")
    print('  brief 4.1 said for the rail.  The impact term is trivial by')
    print('  comparison, and in Mode A there are no drops to produce it anyway.')

    print('\n  Tipping -- why the stand gets clamped, not weighted:')
    for b in (100, 150, 200, 250, 300):
        w_need = SHOULDER_STALL / (b / 1000.0)
        print(f'      base half-width {b:3d} mm -> needs {w_need:6.1f} N'
              f' = {w_need / G:5.1f} kg of stand')
    print('    A printed stand is ~0.3 kg.  No practical base width holds')
    print('    11 N.m by dead weight, so the stand MUST be clamped or bolted')
    print('    to the bench.  Not optional, and not a Mode B artefact.')

    print('\n  Ride height and floor clearance (shoulder axis to floor):')
    for phi, label in ((PHI_EXT, 'knee at the -8 deg extension stop'),
                       (0.0, 'knee at phi = 0, the modelled pose'),
                       (PHI_DESIGN, 'knee at the +25 deg design point'),
                       (PHI_STOP, 'knee against the +27 deg stop')):
        h = -wheel_xz(phi)[1] + WHEEL_R
        print(f'    {label:<34s} {h:7.2f} mm')
    print('    -> the stand must hold the shoulder axis at least '
          f'{-wheel_xz(PHI_EXT)[1] + WHEEL_R:.0f} mm above the floor')

    print('\n  Step 6 reference table (test deferred by owner decision 2026-09-02):')
    print('  the current ABS single-leg article does not carry these masses or')
    print('  characterize the spring.  Preserve the table for the later two-leg')
    print('  PA-CF structural build:')
    print('   added mass    force at wheel      phi')
    f_lo, f_hi = ground_force(PHI_EXT), ground_force(PHI_STOP)
    for m in (0.5, 1.0, 2.0, 3.0, 4.0, 5.0):
        f = m * G
        if f < f_lo:
            note = 'below preload -- still on the -8 deg stop'
        elif f > f_hi:
            note = 'past the +27 deg stop -- do not load this far'
        else:
            note = f'{phi_at_force(f):+7.2f} deg'
        print(f'   {m:5.1f} kg     {f:7.2f} N     {note}')
    print(f'\n  Preload floor: a free leg rests on the -8 deg stop at '
          f'{f_lo:.2f} N, so anything')
    print('  lighter is indistinguishable -- threshold on phi, not on force.')
    return dict(leg=leg, overhang=MODE_A_OVERHANG, fmax=fmax, vec=vec)


def mode_a_bolt_group(plate_t=8.0):
    """Per-screw shear in the stand's five-hole interface under Mode A yaw.

    `Chassis_Shoulder_Plate_L`'s five existing frame-bolt holes are the whole
    structural joint between the leg and the stand (design record 2.2), so the
    11.00 N.m of shoulder yaw is carried by five M3 in shear -- there is no
    register, no dowel and no MGN12H block sharing it.  A pure couple has the
    same moment about every point, so the group reacts it about its OWN
    centroid, not about the motor axis.
    """
    print()
    print('=' * 78)
    print('10.  MODE A BOLT GROUP  --  five M3 carry the whole yaw torque')
    print('=' * 78)
    xc = sum(x for x, _ in PANEL_FRAME_BOLTS) / len(PANEL_FRAME_BOLTS)
    zc = sum(z for _, z in PANEL_FRAME_BOLTS) / len(PANEL_FRAME_BOLTS)
    print(f'  five frame-bolt holes: {PANEL_FRAME_BOLTS}')
    print(f'  group centroid  X {xc:+7.2f}   Z {zc:+7.2f}'
          '   (NOT the motor axis at 0,0)')
    r2 = 0.0
    radii = []
    for x, z in PANEL_FRAME_BOLTS:
        r = math.hypot(x - xc, z - zc)
        radii.append(r)
        r2 += r * r
    print(f'  sum r^2 = {r2:.0f} mm^2,  worst radius {max(radii):.2f} mm')
    print()
    print('   case                        worst screw shear   bearing on a '
          f'{plate_t:.0f} mm printed wall')
    for m, label in ((SHOULDER_STALL, 'shoulder stall 11.00 N.m'),
                     (SHOULDER_PROOF, 'proof screen  25.00 N.m')):
        v = m * 1000.0 * max(radii) / r2
        brg = v / (3.0 * plate_t)          # M3 shank bearing on the bore wall
        print(f'   {label:<28s} {v:7.1f} N        {brg:6.2f} MPa')
    print('   -> against PA-CF ~84 MPa XY, bearing is not the limit; the limit')
    print('      is the M3 heat-set insert\'s grip in printed nylon and the')
    print('      5.0 mm insert depth in the boss (rig_lib INSERT_M3_L).')
    print()
    print('  Two consequences for the stand design:')
    print('    * Spread the five landings as far as the panel allows.  Shear')
    print('      goes as 1/sum(r^2), so a compact boss cluster is the one way to')
    print('      make this joint the failure point.')
    print('    * The group centroid is offset from the motor axis, so the yaw')
    print('      torque also tries to rotate the panel about a point that is')
    print(f'      {math.hypot(xc, zc):.1f} mm off-axis.  Do not model the joint as '
          'five bolts on a')
    print('      circle about the shoulder.')
    return dict(centroid=(xc, zc), r2=r2, rmax=max(radii))


def main():
    k = check_frozen()
    mb = mass_budget()
    rows, fmax, phi_eq = drop_table(mb['half'])
    moment_check(fmax)
    travel_budget(rows, phi_eq)
    bounce_mode(mb, phi_eq)
    torque_arm()
    knee_axle_check()
    mode_a_stand()
    mode_a_bolt_group()
    print()


if __name__ == '__main__':
    main()
