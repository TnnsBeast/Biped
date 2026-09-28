"""Repository-only integrity gate for the R2A print release.

Byte hashing only, like verify_mechanical_release.py: it neither inspects nor
edits CAD geometry (that is r2a_release_fusion.py, run through the Fusion MCP).
It blocks a released R2A file, or a Fusion-verified R2A source, that changed
without a reviewed baseline entry, and a recorded interface or print-audit
failure.  It never touches the legacy mechanical_release_baseline.json.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASELINE = ROOT / 'r2a_release_baseline.json'
AUDIT = ROOT / 'evidence/r2a/2026-09-27_digital_gate/release_audit.json'
EXPECTED_RELEASED = 12


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    baseline = json.loads(BASELINE.read_text())
    failures = []
    released = {k: v for k, v in baseline['parts'].items()
                if str(v.get('state', '')).startswith('RELEASED')}
    if len(released) != EXPECTED_RELEASED:
        failures.append('Expected %d released R2A files, baseline has %d'
                        % (EXPECTED_RELEASED, len(released)))
    for name, row in released.items():
        path = ROOT / row['file']
        if not path.is_file() or digest(path) != row.get('released_sha256'):
            failures.append('Unverified released R2A file: ' + name)
        fid = row.get('fidelity') or {}
        if fid.get('open_or_nonmanifold_edges') != 0 or \
                fid.get('vertices_off_reviewed_surface') != 0:
            failures.append('Recorded mesh-fidelity failure: ' + name)
    held = [k for k, v in baseline['parts'].items() if k not in released]
    for name in held:
        f = baseline['parts'][name].get('file')
        if f and (ROOT / f).is_file():
            failures.append('Held part has a print file in the repository: ' + name)
    sources = baseline.get('verified_source_sha256') or {}
    if not sources:
        failures.append('Missing verified R2A source hashes')
    for relative, expected in sources.items():
        path = ROOT / relative
        if not path.is_file() or digest(path) != expected:
            failures.append('Fusion re-verification required for changed source: '
                            + relative)
    audit = json.loads(AUDIT.read_text())
    if not all(c['pass'] for c in audit['dimensional_contracts']):
        failures.append('Recorded R2A interface failure')
    for name, pa in audit['print_audit'].items():
        if pa['counts'].get('SUPPORT') and baseline['parts'][name]['support_policy'] == 'none':
            failures.append('Support face on a no-support part: ' + name)
    for r in audit.get('distal_support_audit', []):
        if r.get('error') or not r.get('clear_removal_paths'):
            failures.append('Support region without a removal path: %s' % r.get('label'))
    if failures:
        raise SystemExit('\n'.join(failures))
    print('PASS: %d reviewed R2A print files, %d contracts and Fusion-verified sources '
          'match r2a_release_baseline.json' % (len(released),
                                               len(audit['dimensional_contracts'])))


if __name__ == '__main__':
    main()
