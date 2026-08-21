#!/usr/bin/env python3
"""Analyst-side bridge helper. Plain python3 -- no Fusion, no adsk import.

Two jobs, both things the analyst can do without the CAD:

    python3 fusion_bridge/bridge.py check              # validate request.json
    python3 fusion_bridge/bridge.py read <runid>       # summarise a result

`check` exists so a malformed request is caught here rather than after a
round-trip through a human. `read` refuses to summarise a run whose REF_* guard
failed, because those numbers are computed against displaced geometry.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REQUEST = os.path.join(HERE, 'request.json')
OUTDIR = os.path.join(HERE, 'out')

# Mirror of ops.REGISTRY / ops.MUTATING. Kept here so validation needs no adsk.
KNOWN = {'census', 'mass_report', 'real_clashes', 'checks_44', 'bbox',
         'list_occurrences', 'params', 'set_pose', 'slide_to'}
MUTATING = {'set_pose', 'slide_to'}
DOCUMENTS = {'Beni_Prototype1', 'Beni_SingleLegRig'}
REQUIRED_ARGS = {'bbox': ('occ',), 'set_pose': ('theta', 'phi'),
                 'slide_to': ('dz',)}


def check(path=REQUEST):
    if not os.path.exists(path):
        return ['no request at %s' % path]
    try:
        req = json.load(open(path, encoding='utf-8'))
    except ValueError as exc:
        return ['request is not valid JSON: %s' % exc]

    errs = []
    runid = req.get('runid')
    if not runid:
        errs.append('missing "runid"')
    elif os.path.exists(os.path.join(OUTDIR, '%s.json' % runid)):
        errs.append('runid %r already has a result file -- pick a new one, '
                    'results are an audit trail and must not be overwritten'
                    % runid)

    doc = req.get('document')
    if not doc:
        errs.append('missing "document" -- the wrong-document abort depends on it')
    elif doc not in DOCUMENTS:
        errs.append('document %r is not one of %s' % (doc, sorted(DOCUMENTS)))

    if not req.get('intent'):
        errs.append('missing "intent" -- required so the archive stays readable')

    ops = req.get('ops')
    if not isinstance(ops, list) or not ops:
        errs.append('"ops" must be a non-empty list')
        return errs

    wants_mutation = False
    for i, spec in enumerate(ops):
        if not isinstance(spec, dict) or 'op' not in spec:
            errs.append('ops[%d] must be an object with an "op" key' % i)
            continue
        name = spec['op']
        if name not in KNOWN:
            errs.append('ops[%d]: unknown op %r (whitelist: %s)'
                        % (i, name, ', '.join(sorted(KNOWN))))
            continue
        if name in MUTATING:
            wants_mutation = True
        for a in REQUIRED_ARGS.get(name, ()):
            if a not in (spec.get('args') or {}):
                errs.append('ops[%d] (%s): missing required arg %r'
                            % (i, name, a))

    if wants_mutation and not req.get('confirm_mutate'):
        errs.append('request contains a mutating op but "confirm_mutate" is '
                    'not true -- probe.py will abort')
    if req.get('confirm_mutate') and not wants_mutation:
        errs.append('"confirm_mutate" is set but no op mutates -- drop it')
    return errs


def read(runid):
    path = os.path.join(OUTDIR, '%s.json' % runid)
    if not os.path.exists(path):
        print('no result at %s' % path)
        return 1
    r = json.load(open(path, encoding='utf-8'))

    print('runid    %s' % r.get('runid'))
    print('document %s' % r.get('document'))
    print('intent   %s' % r.get('intent'))

    if r.get('aborted'):
        print('\nABORTED: %s' % r.get('abort_reason'))
        return 2

    for key in ('guard', 'guard_after'):
        g = r.get(key) or {}
        print('\n%-11s %s' % (key, 'OK' if g.get('ok') else 'FAIL'))
        for c in g.get('checks', []):
            print('   %-18s expect Y %s  got %s  %s'
                  % (c.get('occ'), c.get('expect_y'),
                     c.get('got_y', c.get('error')),
                     'ok' if c.get('ok') else 'FAIL'))

    hard_fail = not ((r.get('guard') or {}).get('ok')
                     and (r.get('guard_after') or {}).get('ok'))
    if hard_fail:
        print('\n*** REF_* guard failed. The motor STEP references are '
              'displaced, so every number below was computed against wrong '
              'geometry. Treat this run as NO DATA, not as data with a '
              'caveat. See rig design record 6.2. ***')

    print('\nresults')
    for row in r.get('results', []):
        if row.get('ok'):
            print('   %-18s ok' % row['op'])
        else:
            print('   %-18s FAIL  %s' % (row['op'], row.get('error')))
    return 2 if hard_fail else 0


def main(argv):
    cmd = argv[1] if len(argv) > 1 else 'check'
    if cmd == 'check':
        errs = check()
        if errs:
            print('request INVALID:')
            for e in errs:
                print('   - %s' % e)
            return 1
        print('request valid')
        return 0
    if cmd == 'read':
        if len(argv) < 3:
            print('usage: bridge.py read <runid>')
            return 1
        return read(argv[2])
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
