#!/usr/bin/env python3
"""Measure circular features out of an STL mesh.

Written to check `print_stl/GAUGE_*.stl` against
`beni_prototype1_design_record.md` §2 before anything is printed.  The gauges are
mesh exports of revolved/extruded solids, so every cylindrical face leaves its
vertices on a circle in a plane normal to the part axis.  Recovering those
circles recovers the callouts: face positions, ODs, bolt PCDs and hole sizes.

Usage:
    python3 manufacturing/stl_inspect.py print_stl/GAUGE_Shoulder_Motor_Interface.stl --axis y

The part axis defaults to y because every part in this project is modelled at its
assembly coordinates and the shoulder/wheel motor axes are the global Y axis
(`beni_lib` module docstring).
"""

import argparse
import math
import struct
import sys

import numpy as np

AXES = {'x': 0, 'y': 1, 'z': 2}


# --------------------------------------------------------------------- loading
def load_stl(path):
    """Return an (n, 3, 3) array of triangle vertices, mm."""
    with open(path, 'rb') as fh:
        head = fh.read(84)
        fh.seek(0)
        raw = fh.read()

    # An ASCII STL starts with "solid" -- but so can a binary one, so trust the
    # declared triangle count against the actual file length instead.
    n_declared = struct.unpack('<I', head[80:84])[0]
    if len(raw) == 84 + 50 * n_declared:
        tris = np.empty((n_declared, 3, 3), dtype=np.float64)
        for i in range(n_declared):
            off = 84 + 50 * i
            vals = struct.unpack('<12f', raw[off:off + 48])
            tris[i] = np.array(vals[3:12]).reshape(3, 3)
        return tris

    text = raw.decode('ascii', errors='replace')
    verts = [tuple(float(v) for v in line.split()[1:4])
             for line in text.splitlines()
             if line.strip().startswith('vertex')]
    if len(verts) % 3:
        raise ValueError('ASCII STL vertex count is not a multiple of 3')
    return np.array(verts).reshape(-1, 3, 3)


def unique_vertices(tris, tol=1e-4):
    v = tris.reshape(-1, 3)
    keys = np.round(v / tol).astype(np.int64)
    _, idx = np.unique(keys, axis=0, return_index=True)
    return v[np.sort(idx)]


# ------------------------------------------------------------------ clustering
def cluster_1d(values, tol):
    """Single-linkage clustering of a 1-D array. Returns list of index arrays."""
    order = np.argsort(values)
    groups, cur = [], [order[0]]
    for a, b in zip(order[:-1], order[1:]):
        if values[b] - values[a] <= tol:
            cur.append(b)
        else:
            groups.append(np.array(cur))
            cur = [b]
    groups.append(np.array(cur))
    return groups


def cluster_2d(pts, tol):
    """Single-linkage clustering of 2-D points. O(n^2), fine at these sizes."""
    n = len(pts)
    d = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=-1)
    adj = d <= tol
    seen = np.zeros(n, dtype=bool)
    out = []
    for i in range(n):
        if seen[i]:
            continue
        stack, comp = [i], []
        seen[i] = True
        while stack:
            k = stack.pop()
            comp.append(k)
            for j in np.nonzero(adj[k] & ~seen)[0]:
                seen[j] = True
                stack.append(j)
        out.append(np.array(comp))
    return out


def fit_circle(pts):
    """Algebraic circle fit. Returns (cx, cy, r, max residual)."""
    x, y = pts[:, 0], pts[:, 1]
    a = np.column_stack([x, y, np.ones(len(x))])
    b = x ** 2 + y ** 2
    sol, *_ = np.linalg.lstsq(a, b, rcond=None)
    cx, cy = sol[0] / 2.0, sol[1] / 2.0
    r = math.sqrt(max(sol[2] + cx * cx + cy * cy, 0.0))
    resid = np.abs(np.hypot(x - cx, y - cy) - r)
    return cx, cy, r, float(resid.max())


# -------------------------------------------------------------------- reporting
def inspect(path, axis='y', plane_tol=0.05, xy_tol=1.2, min_pts=6):
    tris = load_stl(path)
    v = unique_vertices(tris)
    ax = AXES[axis]
    others = [i for i in range(3) if i != ax]

    print(f'file            {path}')
    print(f'triangles       {len(tris)}')
    print(f'unique vertices {len(v)}')
    lo, hi = v.min(axis=0), v.max(axis=0)
    for i, nm in enumerate('xyz'):
        print(f'bbox {nm}          {lo[i]:9.3f} .. {hi[i]:9.3f}   '
              f'({hi[i] - lo[i]:.3f})')

    a = v[:, ax]
    rad = np.hypot(v[:, others[0]], v[:, others[1]])
    print(f'\nmax radius from {axis} axis   {rad.max():.3f}  '
          f'(implies OD {2 * rad.max():.3f})')

    print(f'\nplanes normal to {axis} (tol {plane_tol} mm), circles fitted per '
          f'plane (link tol {xy_tol} mm, >= {min_pts} pts)')
    print('-' * 78)
    for grp in cluster_1d(a, plane_tol):
        if len(grp) < min_pts:
            continue
        aval = a[grp].mean()
        pts = v[grp][:, others]
        comps = [c for c in cluster_2d(pts, xy_tol) if len(c) >= min_pts]
        if not comps:
            continue
        print(f'\n  {axis} = {aval:9.3f}   ({len(grp)} vertices, '
              f'{len(comps)} feature(s))')
        rows = []
        for c in comps:
            cx, cy, r, res = fit_circle(pts[c])
            rows.append((cx, cy, r, res, len(c)))
        # group features by fitted radius so a bolt pattern reports as one line
        by_r = {}
        for cx, cy, r, res, n in rows:
            key = round(r, 2)
            for k in by_r:
                if abs(k - r) < 0.06:
                    key = k
                    break
            by_r.setdefault(key, []).append((cx, cy, r, res, n))
        for key in sorted(by_r):
            fam = by_r[key]
            rr = np.mean([f[2] for f in fam])
            res = max(f[3] for f in fam)
            pcd = np.mean([math.hypot(f[0], f[1]) for f in fam])
            angs = sorted(round(math.degrees(math.atan2(f[1], f[0])), 2)
                          for f in fam)
            if len(fam) == 1 and pcd < 0.05:
                print(f'      1 x  D{2 * rr:7.3f}  on axis'
                      f'                        fit +-{res:.3f}')
            else:
                sp = ('%.2f' % (angs[1] - angs[0])) if len(angs) > 1 else '-'
                print(f'      {len(fam)} x  D{2 * rr:7.3f}  PCD {2 * pcd:8.3f}'
                      f'  first {angs[0]:8.2f} deg  step {sp:>7}'
                      f'  fit +-{res:.3f}')
    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='+')
    ap.add_argument('--axis', default='y', choices=list(AXES))
    ap.add_argument('--plane-tol', type=float, default=0.05)
    ap.add_argument('--xy-tol', type=float, default=1.2)
    ap.add_argument('--min-pts', type=int, default=6)
    args = ap.parse_args()
    for p in args.paths:
        inspect(p, args.axis, args.plane_tol, args.xy_tol, args.min_pts)
        print('=' * 78)
    return 0


if __name__ == '__main__':
    sys.exit(main())
