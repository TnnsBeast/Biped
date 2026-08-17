#!/usr/bin/env python3
"""Pack the exported STLs into a single self-contained viewer page.

Reads   web/models/*.stl  + web/models/manifest.json
Writes  web/index.html    (no server, no external assets except the three.js CDN)

Packed blob layout, little-endian:
    u32 nVerts | u32 nIndices | f32 xyz * nVerts | u32 index * nIndices
then gzip, then base64.
"""
import base64
import gzip
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, 'models')
TEMPLATE = os.path.join(HERE, 'src', 'viewer.html')
OUT = os.path.join(HERE, 'index.html')

# draw order: big static shells first so the legs read on top
GROUP_ORDER = ['static', 'centre', 'prox', 'dist', 'wheel', 'cart_up', 'cart_lo']


def pack_stl(path):
    """Binary STL -> (packed bytes, triangle count, vertex count)."""
    raw = open(path, 'rb').read()
    ntri = struct.unpack('<I', raw[80:84])[0]
    vmap, verts, idx = {}, [], []
    off = 84
    for _ in range(ntri):
        for v in range(3):
            key = raw[off + 12 + v * 12: off + 24 + v * 12]
            j = vmap.get(key)
            if j is None:
                j = len(verts)
                vmap[key] = j
                verts.append(key)
            idx.append(j)
        off += 50
    blob = (struct.pack('<II', len(verts), len(idx))
            + b''.join(verts)
            + struct.pack('<%dI' % len(idx), *idx))
    return blob, ntri, len(verts)


def main():
    manifest = json.load(open(os.path.join(MODELS, 'manifest.json')))
    manifest.sort(key=lambda m: (GROUP_ORDER.index(m['group'])
                                 if m['group'] in GROUP_ORDER else 99,
                                 m['material']))
    out, tris, raw_total, gz_total = [], 0, 0, 0
    for m in manifest:
        p = os.path.join(MODELS, m['file'])
        if not os.path.exists(p):
            print('  MISSING %s' % m['file'], file=sys.stderr)
            continue
        blob, ntri, nv = pack_stl(p)
        gz = gzip.compress(blob, 9)
        tris += ntri
        raw_total += os.path.getsize(p)
        gz_total += len(gz)
        out.append({'group': m['group'], 'material': m['material'],
                    'parts': m['parts'],
                    'b64': base64.b64encode(gz).decode('ascii')})
        print('  %-24s %6d tris  %5d verts  %7d B gz' % (m['file'], ntri, nv, len(gz)))

    data = json.dumps(out, separators=(',', ':'))
    html = open(TEMPLATE).read().replace('__GEO__', data)
    open(OUT, 'w').write(html)

    print()
    print('%d meshes, %d triangles' % (len(out), tris))
    print('stl on disk %.2f MB  ->  embedded %.2f MB  ->  index.html %.2f MB'
          % (raw_total / 1048576, gz_total / 1048576, len(html) / 1048576))
    print('wrote %s' % OUT)


if __name__ == '__main__':
    main()
