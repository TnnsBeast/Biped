"""Fusion-side runner for the bridge. Executes fusion_bridge/request.json.

Runs INSIDE Fusion (Scripts and Add-Ins), never in plain python3.

    import sys; sys.path.insert(0, '/Users/neilchulani/Robots/Biped')
    import fusion_bridge.probe as probe
    probe.run()

Contract is fusion_bridge/PROTOCOL.md. Behaviour worth knowing before you run it:

  * The document name in the request is asserted against the open document. A
    mismatch aborts BEFORE any op executes -- this is the cheap guard against
    running a rig request against Beni_Prototype1.
  * The REF_* bounding-box guard runs before and after the ops regardless of
    what was requested. If it fails, every result in the run is suspect.
  * A failing op does not stop the run. It is recorded and the next op proceeds.
  * Mutating ops (pose, slide) require "confirm_mutate": true in the request.
"""

import io
import json
import os
import traceback
import contextlib

import adsk.core

HERE = os.path.dirname(os.path.abspath(__file__))
REQUEST = os.path.join(HERE, 'request.json')
OUTDIR = os.path.join(HERE, 'out')


def _load():
    with open(REQUEST, encoding='utf-8') as fh:
        return json.load(fh)


def _write(payload):
    os.makedirs(OUTDIR, exist_ok=True)
    path = os.path.join(OUTDIR, '%s.json' % payload['runid'])
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)
        fh.write('\n')
    return path


def run(request_path=None):
    app = adsk.core.Application.get()
    ui = app.userInterface

    global REQUEST
    if request_path:
        REQUEST = request_path

    try:
        req = _load()
    except Exception as exc:                              # noqa: BLE001
        ui.messageBox('bridge: cannot read request\n%s' % exc)
        return

    # import late so a syntax error in ops.py surfaces as a readable message
    import importlib
    from fusion_bridge import ops
    importlib.reload(ops)

    ctx = {'app': app, 'ui': ui}
    out = {
        'runid': req.get('runid', 'unnamed'),
        'document': app.activeDocument.name,
        'document_expected': req.get('document'),
        'intent': req.get('intent', ''),
        'aborted': False,
        'guard': None,
        'guard_after': None,
        'results': [],
    }

    # ---- document assert, before anything touches the model
    want = req.get('document')
    if want and app.activeDocument.name != want:
        out['aborted'] = True
        out['abort_reason'] = (
            'request targets %r but the open document is %r -- nothing was run'
            % (want, app.activeDocument.name))
        path = _write(out)
        ui.messageBox('bridge ABORTED (wrong document)\n%s' % path)
        return

    # ---- guard, before
    out['guard'] = ops.guard(ctx)

    # ---- mutation gate
    asked = [o.get('op') for o in req.get('ops', [])]
    mutating = sorted(set(asked) & ops.MUTATING)
    if mutating and not req.get('confirm_mutate'):
        out['aborted'] = True
        out['abort_reason'] = (
            'request contains mutating op(s) %s without "confirm_mutate": true'
            % ', '.join(mutating))
        path = _write(out)
        ui.messageBox('bridge ABORTED (unconfirmed mutation)\n%s' % path)
        return
    out['mutating_ops'] = mutating

    # ---- execute
    for spec in req.get('ops', []):
        name = spec.get('op')
        args = spec.get('args', {}) or {}
        row = {'op': name, 'args': args}
        fn = ops.REGISTRY.get(name)
        if fn is None:
            row.update(ok=False,
                       error='unknown op %r; whitelist is %s'
                             % (name, sorted(ops.REGISTRY)))
            out['results'].append(row)
            continue
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                row['value'] = fn(ctx, args)
            row['ok'] = True
        except Exception as exc:                          # noqa: BLE001
            row['ok'] = False
            row['error'] = '%s: %s' % (type(exc).__name__, exc)
            row['traceback'] = traceback.format_exc()
        row['stdout'] = buf.getvalue()
        out['results'].append(row)

    # ---- guard, after: did our own ops displace anything?
    out['guard_after'] = ops.guard(ctx)

    ok = sum(1 for r in out['results'] if r.get('ok'))
    path = _write(out)
    ui.messageBox(
        'bridge done: %d/%d ops ok\nguard before %s / after %s\n%s'
        % (ok, len(out['results']),
           'OK' if out['guard']['ok'] else 'FAIL',
           'OK' if out['guard_after']['ok'] else 'FAIL',
           path))


def main():
    run()
