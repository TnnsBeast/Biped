#!/usr/bin/env python3
"""Author the `Knee_Stop_Arc_L` laser DXFs from the verified Fusion geometry.

Input:  `rig_dxf/stop_arc_loops.json`, dumped straight off the solid by
        `rig_lib`/Fusion, in knee-axis-relative (X, Z) millimetres.
Output: `rig_dxf/Knee_Stop_Arc_L_inner.dxf`, `..._outer.dxf`, `..._nest.dxf`

WHY NOT Fusion's own DXF export.  `Sketch.saveAsDXF` after `projectCutEdges`
wrote the three M3 holes at (-X, -Z) while writing the plate outline at
(+X, -Z) -- the hole pattern came out MIRRORED relative to the profile, about
183 mm away.  Cutting that file scraps the part.  Everything here is built from
explicit numbers instead, and `_area()` cross-checks each closed profile against
the area Fusion reports for the same face.

TWO PLATES, NOT ONE.  `machined_parts_spec.md` §8 asks for a two-level slot in a
single 3 mm plate: the inner level (1.5 mm) whose slot ends ARE the metal hard
stops at phi = +27 and -8, and the outer level (1.5 mm) that houses the PU
bumper blocks.  A laser cuts one through-profile per plate, so this ships as two
1.5 mm plates stacked -- option 2 in `beni_rig_no_machining.md` §2.2.
"""

import json
import math
import os

import ezdxf

ROOT = os.path.dirname(os.path.abspath(__file__))
DXF_DIR = os.path.join(ROOT, 'rig_dxf')
SRC = os.path.join(DXF_DIR, 'stop_arc_loops.json')

# The inner slot's two ends are the metal hard stops.  Order them 0.3 mm short
# so they can be filed to the measured angle on assembly (brief §7 item 3).
UNDERSIZE_MM = 0.3
SLOT_R = 30.0                     # slot centreline radius
SLOT_HALF = 3.1                   # end radius; slot is 6.2 wide
STOP_A0, STOP_A1 = 219.600, 254.600     # nominal, machined_parts_spec §8


def _ang(p, c=(0.0, 0.0)):
    return math.degrees(math.atan2(p[1] - c[1], p[0] - c[0])) % 360.0


def _sweep(a0, a1):
    """Shorter signed sweep from a0 to a1, degrees, +ve = CCW."""
    d = (a1 - a0) % 360.0
    return d if d <= 180.0 else d - 360.0


def _ends(e):
    if e['t'] == 'arcx':
        a, b, _ = _arcx_pts(e)
        return a, b
    return e['a'], e['b']


def _flip(e):
    """Reverse an edge's traversal direction."""
    f = dict(e)
    if e['t'] == 'arcx':
        f['s'], f['e'] = e['e'], e['s']
        f['sw'] = -e['sw']
    else:
        f['a'], f['b'] = e['b'], e['a']
    return f


def _chain(edges, tol=1e-6):
    """Order and orient a loop's edges into one continuous traversal.

    Fusion hands back a BRepLoop's edges in no particular order and with no
    consistent sense -- the inner level's outer loop arrived with its second
    edge starting where the first one started.  Summing a shoelace over that
    order gives a scrambled polygon, which is what put the inner profile
    218 mm2 out.  Chain by endpoint instead of trusting the order.
    """
    if len(edges) == 1:
        return list(edges)
    rest = list(edges)
    out = [rest.pop(0)]
    while rest:
        cur_end = _ends(out[-1])[1]
        for i, e in enumerate(rest):
            a, b = _ends(e)
            if math.dist(a, cur_end) < tol:
                out.append(rest.pop(i))
                break
            if math.dist(b, cur_end) < tol:
                out.append(_flip(rest.pop(i)))
                break
        else:
            raise ValueError('loop does not close: %d edge(s) left' % len(rest))
    if math.dist(_ends(out[-1])[1], _ends(out[0])[0]) > tol:
        raise ValueError('loop end does not meet its start')
    return out


def _area(edges):
    """Signed area of a closed loop of lines and arcs, mm^2."""
    a = 0.0
    if edges and edges[0]['t'] == 'circle':
        return math.pi * edges[0]['r'] ** 2
    edges = _chain(edges)
    for e in edges:
        if e['t'] == 'arcx':
            p, q, _sw = _arcx_pts(e)
        else:
            p, q = e['a'], e['b']
        a += p[0] * q[1] - q[0] * p[1]
    a /= 2.0
    for e in edges:
        if e['t'] == 'arc':
            c, r = e['c'], e['r']
            s = math.radians(_sweep(_ang(e['a'], c), _ang(e['b'], c)))
            a += (r ** 2 / 2.0) * (s - math.sin(s))
        elif e['t'] == 'arcx':
            _p, _q, sw = _arcx_pts(e)
            s = math.radians(sw)
            a += (e['r'] ** 2 / 2.0) * (s - math.sin(s))
    return a


def _pt(rr, ang):
    t = math.radians(ang)
    return [rr * math.cos(t), rr * math.sin(t)]


def slot_loop(a0, a1, r=SLOT_R, half=SLOT_HALF):
    """Arc slot as four CCW arcs given by explicit angles.

    The end caps sweep exactly 180 deg, so inferring their direction from their
    two endpoints is ambiguous -- both candidate semicircles have the same
    endpoints, and picking the wrong one turns the cap inside out.  Each cap is
    therefore stated as an explicit CCW start/end pair: the cap at a0 runs from
    a0+180 to a0, which is the half that bulges AWAY from the slot.
    """
    #      centre        radius  traversal from -> to      signed sweep
    return [
        {'t': 'arcx', 'c': _pt(r, a0), 'r': half,
         's': a0 + 180.0, 'e': a0, 'sw': 180.0},
        {'t': 'arcx', 'c': [0.0, 0.0], 'r': r + half,
         's': a0, 'e': a1, 'sw': a1 - a0},
        {'t': 'arcx', 'c': _pt(r, a1), 'r': half,
         's': a1, 'e': a1 + 180.0, 'sw': 180.0},
        {'t': 'arcx', 'c': [0.0, 0.0], 'r': r - half,
         's': a1, 'e': a0, 'sw': -(a1 - a0)},
    ]


def _arcx_pts(e):
    """Traversal start/end points of an explicit arc, and its signed sweep.

    The sweep is carried explicitly rather than inferred: the traversal
    direction round the loop and the DXF's always-CCW start/end pair are two
    different things, and deriving one from the other silently picked the
    325 deg complement of a 35 deg arc.
    """
    p = _pt(e['r'], e['s'])
    q = _pt(e['r'], e['e'])
    a = [e['c'][0] + p[0], e['c'][1] + p[1]]
    b = [e['c'][0] + q[0], e['c'][1] + q[1]]
    return a, b, e['sw']


def _emit(msp, edges):
    for e in edges:
        if e['t'] == 'circle':
            msp.add_circle(center=e['c'], radius=e['r'])
        elif e['t'] == 'line':
            msp.add_line(e['a'], e['b'])
        elif e['t'] == 'arcx':
            s_, e_ = (e['s'], e['e']) if e['sw'] >= 0 else (e['e'], e['s'])
            msp.add_arc(center=e['c'], radius=e['r'],
                        start_angle=s_ % 360.0, end_angle=e_ % 360.0)
        elif e['t'] == 'arc':
            c = e['c']
            a0, a1 = _ang(e['a'], c), _ang(e['b'], c)
            if _sweep(a0, a1) >= 0:          # DXF arcs always run CCW
                msp.add_arc(center=c, radius=e['r'],
                            start_angle=a0, end_angle=a1)
            else:
                msp.add_arc(center=c, radius=e['r'],
                            start_angle=a1, end_angle=a0)


def build():
    with open(SRC) as fh:
        src = json.load(fh)

    # the inner level's slot loop is regenerated so the undersize is exact
    half_deg = math.degrees(UNDERSIZE_MM / SLOT_R)
    a0, a1 = STOP_A0 + half_deg, STOP_A1 - half_deg
    print('inner slot ends: nominal %.3f / %.3f deg  ->  ordered %.3f / %.3f'
          % (STOP_A0, STOP_A1, a0, a1))
    print('  = %.2f mm short at each end, %.4f deg at r = %.1f'
          % (UNDERSIZE_MM, half_deg, SLOT_R))

    made = []
    for lvl in ('inner', 'outer'):
        loops = src[lvl]['loops']
        out = []
        for lp in loops:
            eds = lp['edges']
            is_slot = (not lp['outer'] and eds[0]['t'] != 'circle')
            if lvl == 'inner' and is_slot:
                out.append(slot_loop(a0, a1))
            else:
                out.append(eds)
        doc = ezdxf.new('R2010', setup=True)
        doc.header['$INSUNITS'] = 4                      # millimetres
        msp = doc.modelspace()
        for eds in out:
            _emit(msp, eds)
        path = os.path.join(DXF_DIR, 'Knee_Stop_Arc_L_%s.dxf' % lvl)
        doc.saveas(path)

        net = 0.0
        for lp, eds in zip(loops, out):
            ar = abs(_area(eds))
            net += ar if lp['outer'] else -ar
        made.append((lvl, path, net, src[lvl]['area_mm2'], len(out)))

    print()
    print('%-6s %-40s %10s %10s %6s' % ('level', 'file', 'area', 'Fusion', 'loops'))
    for lvl, path, net, ref, n in made:
        d = net - ref
        note = 'matches' if abs(d) < 0.01 else '%+.3f (the undersize)' % d
        print('%-6s %-40s %10.3f %10.3f %6d   %s'
              % (lvl, os.path.basename(path), net, ref, n, note))

    # one nested file, both plates side by side, for a single upload
    doc = ezdxf.new('R2010', setup=True)
    doc.header['$INSUNITS'] = 4
    msp = doc.modelspace()
    for i, lvl in enumerate(('inner', 'outer')):
        dx = i * 90.0
        loops = src[lvl]['loops']
        for lp in loops:
            eds = lp['edges']
            if lvl == 'inner' and not lp['outer'] and eds[0]['t'] != 'circle':
                eds = slot_loop(a0, a1)
            sh = []
            for e in eds:
                e2 = dict(e)
                for k in ('a', 'b', 'c'):
                    if k in e2:
                        e2[k] = [e2[k][0] + dx, e2[k][1]]
                sh.append(e2)
            del e2
            _emit(msp, sh)
    nest = os.path.join(DXF_DIR, 'Knee_Stop_Arc_L_nest.dxf')
    doc.saveas(nest)
    print('\nnested both plates -> %s' % os.path.basename(nest))
    return made




# --------------------------------------------------------- RIG_Ballast_Disc
# Mirrors rig_lib's constants; goes on the same laser order as the stop arc.
BAL_R_IN, BAL_R_OUT = 42.0, 64.0
BAL_A0, BAL_A1 = 55.0, 125.0
BAL_STUD_R = 53.0
BAL_STUD_A = (70.0, 110.0)
BAL_STUD_D = 4.5
BAL_T = 3.0
STEEL_DENSITY = 7.85e-3          # g/mm^3


def build_ballast():
    """One annular-sector ballast plate.  The same part serves top and bottom,
    rotated 180 deg, so there is one part number and one DXF."""
    edges = [
        {'t': 'arcx', 'c': [0.0, 0.0], 'r': BAL_R_OUT,
         's': BAL_A0, 'e': BAL_A1, 'sw': BAL_A1 - BAL_A0},
        {'t': 'line', 'a': _pt(BAL_R_OUT, BAL_A1), 'b': _pt(BAL_R_IN, BAL_A1)},
        {'t': 'arcx', 'c': [0.0, 0.0], 'r': BAL_R_IN,
         's': BAL_A1, 'e': BAL_A0, 'sw': -(BAL_A1 - BAL_A0)},
        {'t': 'line', 'a': _pt(BAL_R_IN, BAL_A0), 'b': _pt(BAL_R_OUT, BAL_A0)},
    ]
    holes = [{'t': 'circle', 'c': _pt(BAL_STUD_R, a), 'r': BAL_STUD_D / 2.0}
             for a in BAL_STUD_A]

    doc = ezdxf.new('R2010', setup=True)
    doc.header['$INSUNITS'] = 4
    msp = doc.modelspace()
    _emit(msp, edges)
    _emit(msp, holes)
    path = os.path.join(DXF_DIR, 'RIG_Ballast_Disc.dxf')
    doc.saveas(path)

    net = abs(_area(edges)) - sum(math.pi * h['r'] ** 2 for h in holes)
    g = net * BAL_T * STEEL_DENSITY
    print('\nRIG_Ballast_Disc.dxf   r %.0f..%.0f, %.0f..%.0f deg, 2 x D%.1f at r %.0f'
          % (BAL_R_IN, BAL_R_OUT, BAL_A0, BAL_A1, BAL_STUD_D, BAL_STUD_R))
    print('   area %.2f mm2 x %.1f mm steel = %.1f g each   (rig_lib says 32.8)'
          % (net, BAL_T, g))
    return path, g


if __name__ == '__main__':
    build()
    build_ballast()
