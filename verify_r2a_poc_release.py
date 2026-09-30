"""Repository-only integrity gate for the R2A proof-of-concept (POC) print set.

Byte hashing and recorded-audit checks only, like verify_r2a_release.py: it
neither inspects nor edits CAD geometry (that is r2a_poc_fusion.py, run
through the Fusion MCP).  It blocks a released POC file or a Fusion-verified
source that changed without a reviewed baseline entry, and any recorded
contract, print-audit, sweep or assembly-path failure.  It never touches the
R2A article baseline or the legacy baseline.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASELINE = ROOT / 'r2a_poc_release_baseline.json'
EVIDENCE = ROOT / 'evidence/r2a/2026-09-28_poc'
EXPECTED_RELEASED = 17


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    baseline = json.loads(BASELINE.read_text())
    failures = []
    released = {k: v for k, v in baseline['parts'].items()
                if str(v.get('state', '')).startswith('RELEASED')}
    if len(released) != EXPECTED_RELEASED:
        failures.append('Expected %d released POC files, baseline has %d'
                        % (EXPECTED_RELEASED, len(released)))
    for name, row in released.items():
        path = ROOT / row['file']
        if not path.is_file() or digest(path) != row.get('released_sha256'):
            failures.append('Unverified released POC file: ' + name)
        fid = row.get('fidelity') or {}
        if fid.get('open_or_nonmanifold_edges') != 0 or \
                fid.get('vertices_off_reviewed_surface') != 0 or \
                fid.get('brep_samples_not_in_mesh') != 0:
            failures.append('Recorded mesh-fidelity failure: ' + name)
        if row.get('support_policy') != 'none':
            failures.append('POC part released with supports: ' + name)
    listed = {row['file'] for row in baseline['parts'].values()}
    for stl in (ROOT / 'r2a_poc_stl').glob('*.stl'):
        if stl.relative_to(ROOT).as_posix() not in listed:
            failures.append('Print file without a baseline entry: ' + stl.name)
    sources = baseline.get('verified_source_sha256') or {}
    if not sources:
        failures.append('Missing verified POC source hashes')
    for relative, expected in sources.items():
        path = ROOT / relative
        if not path.is_file() or digest(path) != expected:
            failures.append('Fusion re-verification required for changed source: ' + relative)
    audit = json.loads((EVIDENCE / 'release_audit.json').read_text())
    if not all(c['pass'] for c in audit['dimensional_contracts']):
        failures.append('Recorded POC interface failure')
    for name, pa in audit['print_audit'].items():
        if pa['counts'].get('SUPPORT'):
            failures.append('Support face on a no-support POC part: ' + name)
    gate = json.loads((EVIDENCE / 'poc_measurements.json').read_text())
    for config in ('poc', 'article'):
        sw = gate['sweeps'][config]
        if sw['real']:
            failures.append('Real clash recorded in the %s sweep' % config)
    if gate['sweeps']['poc']['poses'] < 140:
        failures.append('POC sweep has fewer than 140 poses')
    paths = json.loads((EVIDENCE / 'assembly_paths.json').read_text())
    for sid, r in paths.items():
        if not r.get('clear'):
            failures.append('Blocked POC assembly path: ' + sid)
    neg = json.loads((EVIDENCE / 'assembly_path_negative_controls.json').read_text())
    for sid, r in neg.items():
        if r.get('clear'):
            failures.append('Negative control not blocked: ' + sid)
    lock = json.loads((EVIDENCE / 'lock_pin_paths.json').read_text())
    if not lock.get('pass'):
        failures.append('Lock-pin check-point paths failed')
    if not gate['rotor_free_turn']['clear']:
        failures.append('Mock rotor does not turn freely in CAD')
    if failures:
        raise SystemExit('\n'.join(failures))
    print('PASS: %d reviewed POC print files, %d contracts, %d-pose POC sweep, %d paths and '
          'Fusion-verified sources match r2a_poc_release_baseline.json'
          % (len(released), len(audit['dimensional_contracts']),
             gate['sweeps']['poc']['poses'], len(paths)))


if __name__ == '__main__':
    main()
