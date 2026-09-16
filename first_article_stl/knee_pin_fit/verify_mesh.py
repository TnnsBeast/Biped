"""Verify the Fusion-exported knee-pin bore ladder STL."""

import hashlib
import json
import math
import os
import struct
from collections import Counter


HERE = os.path.dirname(os.path.abspath(__file__))
STL = os.path.join(
    HERE, 'ABS_CAL_KNEE_PIN_BORE_LADDER_PRINT_ORIENTED.stl')
MANIFEST = os.path.join(HERE, 'fusion_manifest.json')
OUTPUT = os.path.join(HERE, 'mesh_verification.json')


def inspect(path):
    data = open(path, 'rb').read()
    if len(data) < 84:
        raise RuntimeError('truncated STL')
    count = struct.unpack_from('<I', data, 80)[0]
    if len(data) != 84 + count * 50:
        raise RuntimeError('binary STL length mismatch')

    edges = Counter()
    vertices = set()
    degenerate = 0
    volume = 0.0
    for index in range(count):
        row = struct.unpack_from('<12fH', data, 84 + index * 50)
        tri = tuple(tuple(float(value) for value in row[start:start + 3])
                    for start in (3, 6, 9))
        vertices.update(tri)
        for edge in range(3):
            edges[tuple(sorted((tri[edge], tri[(edge + 1) % 3])))] += 1
        a, b, c = tri
        cross = ((b[1] - a[1]) * (c[2] - a[2]) -
                 (b[2] - a[2]) * (c[1] - a[1]),
                 (b[2] - a[2]) * (c[0] - a[0]) -
                 (b[0] - a[0]) * (c[2] - a[2]),
                 (b[0] - a[0]) * (c[1] - a[1]) -
                 (b[1] - a[1]) * (c[0] - a[0]))
        if math.sqrt(sum(value * value for value in cross)) <= 1e-9:
            degenerate += 1
        volume += (
            a[0] * (b[1] * c[2] - b[2] * c[1])
            + a[1] * (b[2] * c[0] - b[0] * c[2])
            + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6.0

    minimum = [min(vertex[axis] for vertex in vertices) for axis in range(3)]
    maximum = [max(vertex[axis] for vertex in vertices) for axis in range(3)]
    return {
        'file': os.path.basename(path),
        'bytes': len(data),
        'sha256': hashlib.sha256(data).hexdigest(),
        'facets': count,
        'unique_vertices': len(vertices),
        'edge_incidence_errors':
            dict(Counter(value for value in edges.values() if value != 2)),
        'degenerate_facets': degenerate,
        'minimum_mm': minimum,
        'maximum_mm': maximum,
        'envelope_mm': [maximum[i] - minimum[i] for i in range(3)],
        'mesh_volume_mm3': abs(volume),
    }


def main():
    manifest = json.load(open(MANIFEST, encoding='utf-8'))
    coupon = manifest['coupon']
    row = inspect(STL)
    expected_envelope = coupon['bbox_mm']
    expected_volume = coupon['volume_cm3'] * 1000.0
    if row['edge_incidence_errors'] or row['degenerate_facets']:
        raise RuntimeError('STL is not a clean closed manifold: %r' % row)
    if abs(row['minimum_mm'][2]) >= 0.001:
        raise RuntimeError('STL does not sit at Z=0: %r' % row)
    if any(abs(actual - expected) >= 0.05 for actual, expected in
           zip(row['envelope_mm'], expected_envelope)):
        raise RuntimeError('STL envelope mismatch: %r' % row)
    relative_error = abs(row['mesh_volume_mm3'] - expected_volume) / expected_volume
    if relative_error >= 0.002:
        raise RuntimeError('STL volume mismatch: %r' % row)
    row.update({
        'fusion_brep_envelope_mm': expected_envelope,
        'fusion_brep_volume_mm3': expected_volume,
        'volume_relative_error': relative_error,
        'bed_datum_z_mm': 0.0,
        'status': 'PASS',
    })
    with open(OUTPUT, 'w', encoding='utf-8') as stream:
        json.dump(row, stream, indent=2, sort_keys=True)
        stream.write('\n')
    print(json.dumps(row, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()

