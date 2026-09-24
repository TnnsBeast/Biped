"""Repository-only integrity gate; geometry verification itself uses Fusion MCP.

A source or released-file change without a reviewed Fusion baseline is blocked.
This performs byte hashing only; it neither inspects nor edits CAD geometry.
"""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    baseline=json.loads((ROOT/'mechanical_release_baseline.json').read_text())
    failures=[]
    if len(baseline['parts'])!=15:
        failures.append('Expected all 15 manual print parts')
    for name,row in baseline['parts'].items():
        path=ROOT/row['file']
        if not path.is_file() or digest(path)!=row['released_sha256']:
            failures.append('Unverified released file: '+name)
    if not baseline.get('verified_source_sha256'):
        failures.append('Missing verified source hashes')
    for relative,expected in baseline.get('verified_source_sha256',{}).items():
        path=ROOT/relative
        if not path.is_file() or digest(path)!=expected:
            failures.append('Fusion re-verification required for changed source: '+relative)
    report=json.loads((ROOT/'evidence/assembly/2026-09-23_mechanical_reprint_audit/final_release.json').read_text())
    if not all(r['pass'] for r in report['dimensional_contracts']):
        failures.append('Recorded interface failure')
    if failures:
        raise SystemExit('\n'.join(failures))
    print('PASS: 15 reviewed print files and Fusion-verified sources match release baseline')

if __name__=='__main__':main()
