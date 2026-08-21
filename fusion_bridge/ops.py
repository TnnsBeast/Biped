"""Whitelisted, read-only Fusion operations for the bridge.

Runs INSIDE Fusion only (imports adsk). Each op takes (ctx, args) and returns a
JSON-serialisable value. Ops must not print for their return value's sake --
printing is captured separately as a diagnostic, never as the citable number.

Every workaround for a documented Fusion trap lives here, once, so that no
future request has to remember it:

  * interference() falls back to entity.name, so occurrence names never resolve
    -> we always go through rig_lib.real_clashes(), which fixes the naming.
  * bounding boxes inflate under rotation (axis-aligned box of the untransformed
    box) -> bbox ops refuse to report on a posed occurrence unless the caller
    passes allow_posed, and say so in the payload.
  * isSuppressed is silently unwritable on this API build -> no op offers it.

Units returned to the analyst are mm / g / kg.m2 / degrees.
"""

import adsk.core
import adsk.fusion

import beni_lib
import rig_lib

# mm tolerance for the REF_* guard. Equality assert, not a range check.
GUARD_TOL = 0.01

# beni_single_leg_rig_design_record.md 6.2
GUARD_SPEC = {
    'REF_GIM6010-8': (5.00, 49.00),
    'REF_GIM4305-10': (61.50, 94.50),
}

# Ops that write to the model. Require "confirm_mutate": true in the request.
MUTATING = {'set_pose', 'slide_to'}


# ------------------------------------------------------------------ helpers
def _occ(name):
    o = beni_lib.find_occ(name)
    if o is None:
        raise KeyError('no occurrence named %r in the root component' % name)
    return o


def _bbox_mm(entity):
    b = entity.boundingBox
    return {
        'x': [b.minPoint.x * 10.0, b.maxPoint.x * 10.0],
        'y': [b.minPoint.y * 10.0, b.maxPoint.y * 10.0],
        'z': [b.minPoint.z * 10.0, b.maxPoint.z * 10.0],
    }


def _is_identity(occ):
    """True if the occurrence carries no rotation (so its bbox is trustworthy)."""
    m = occ.transform2.asArray()
    ident = (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
    return all(abs(a - b) < 1e-9 for a, b in zip(m[:11], ident[:11]))


# -------------------------------------------------------------------- guard
def guard(ctx):
    """Assert both motor STEP references sit where the design record says.

    Runs on every bridge invocation, before and after the ops, regardless of
    what was requested. A failure means the model has displaced its references
    and every other number in the run is computed against wrong geometry.
    """
    checks, ok = [], True
    for name, (y0, y1) in GUARD_SPEC.items():
        row = {'occ': name, 'expect_y': [y0, y1]}
        try:
            bb = _bbox_mm(_occ(name))
            got = bb['y']
            row['got_y'] = got
            row['ok'] = (abs(got[0] - y0) <= GUARD_TOL
                         and abs(got[1] - y1) <= GUARD_TOL)
            if not row['ok']:
                row['note'] = ('displaced -- see rig design record 6.2; '
                               'discard every result in this run')
        except Exception as exc:                       # noqa: BLE001
            row['ok'], row['error'] = False, str(exc)
        ok = ok and row['ok']
        checks.append(row)
    return {'ok': ok, 'tol_mm': GUARD_TOL, 'checks': checks}


# ---------------------------------------------------------------- read ops
def op_census(ctx, args):
    """Cheap structural fingerprint. Diff this across runs to detect drift."""
    des = beni_lib.design()
    r = des.rootComponent
    return {
        'document': ctx['app'].activeDocument.name,
        'root_occurrences': r.occurrences.count,
        'components': des.allComponents.count,
        'timeline_entries': des.timeline.count,
        'parameters': des.userParameters.count,
        'joints': r.joints.count,
        'bodies_at_root': r.bRepBodies.count,
    }


def op_mass_report(ctx, args):
    """Mass, CoM and inertia about the CoM. Materials applied first."""
    rig_lib.register_materials()
    beni_lib.apply_materials(verbose=False)
    return beni_lib.mass_report(verbose=True)


def op_real_clashes(ctx, args):
    """Interference with documented artifacts classified out.

    Never use beni_lib.interference() -- it cannot resolve occurrence names.
    """
    mv = float(args.get('min_vol_mm3', 0.5))
    out = rig_lib.real_clashes(min_vol_mm3=mv, verbose=True)
    return {
        'min_vol_mm3': mv,
        'count': len(out),
        'pairs': [{'a': a, 'b': b, 'vol_mm3': v} for a, b, v in out],
    }


def op_checks_44(ctx, args):
    """The six 4.4 release checks. Returns whatever each check returns."""
    raw = rig_lib.checks_44()
    return {k: _plain(v) for k, v in raw.items()}


def op_bbox(ctx, args):
    """Bounding box of one occurrence, in mm.

    Refuses posed occurrences by default: Fusion reports the axis-aligned box of
    the UNTRANSFORMED box, which inflates under rotation. The box centre does
    transform exactly, so that is reported separately and is always valid.
    """
    occ = _occ(args['occ'])
    bb = _bbox_mm(occ)
    ident = _is_identity(occ)
    centre = {k: (v[0] + v[1]) / 2.0 for k, v in bb.items()}
    out = {'occ': args['occ'], 'centre_mm': centre, 'unrotated': ident}
    if ident or args.get('allow_posed'):
        out['bbox_mm'] = bb
        if not ident:
            out['warning'] = ('occurrence is rotated -- bbox is INFLATED and '
                              'must not be used for a clearance; centre is exact')
    else:
        out['bbox_mm'] = None
        out['warning'] = ('occurrence is rotated; bbox withheld because it '
                          'inflates. Pass allow_posed to see it anyway, or use '
                          'centre_mm, which transforms exactly.')
    return out


def op_list_occurrences(ctx, args):
    """Root occurrence names + component names. For discovering what exists."""
    r = beni_lib.design().rootComponent
    rows = []
    for i in range(r.occurrences.count):
        o = r.occurrences.item(i)
        rows.append({
            'occurrence': o.name,
            'component': o.component.name,
            'base': beni_lib.base_name(o.component.name),
            'bodies': o.component.bRepBodies.count,
            'unrotated': _is_identity(o),
        })
    return {'count': len(rows), 'occurrences': rows}


def op_params(ctx, args):
    """Every user parameter, with expression and evaluated value."""
    ps = beni_lib.design().userParameters
    return {'parameters': [
        {'name': ps.item(i).name,
         'expression': ps.item(i).expression,
         'value': ps.item(i).value,
         'unit': ps.item(i).unit}
        for i in range(ps.count)]}


# ------------------------------------------------------------- mutating ops
def op_set_pose(ctx, args):
    """Pose the rig. MUTATES transform2 on real occurrences."""
    theta, phi = float(args['theta']), float(args['phi'])
    rig_lib.rig_set_pose(theta, phi)
    return {'posed': True, 'theta_deg': theta, 'phi_deg': phi}


def op_slide_to(ctx, args):
    """Mode B travel harness. MUTATES the model."""
    dz = float(args['dz'])
    theta, phi = float(args.get('theta', 0.0)), float(args.get('phi', 0.0))
    rig_lib.slide_to(dz, theta=theta, phi=phi)
    return {'dz_mm': dz, 'theta_deg': theta, 'phi_deg': phi}


def _plain(v):
    """Coerce whatever a check returned into something JSON can hold."""
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    if isinstance(v, dict):
        return {str(k): _plain(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_plain(x) for x in v]
    return repr(v)


REGISTRY = {
    'census': op_census,
    'mass_report': op_mass_report,
    'real_clashes': op_real_clashes,
    'checks_44': op_checks_44,
    'bbox': op_bbox,
    'list_occurrences': op_list_occurrences,
    'params': op_params,
    'set_pose': op_set_pose,
    'slide_to': op_slide_to,
}
