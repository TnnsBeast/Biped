"""Check the actual Fusion-exported STL artifacts, invoked through Fusion MCP."""
import collections
import hashlib
import json
import os
import struct

OUT=os.path.dirname(__file__)


def run(_context: str):
    rows=[]
    for report_name in ('proximal_release.json','post_a_release.json'):
        with open(os.path.join(OUT,report_name)) as f:report=json.load(f)
        path=report['print_export']['stl']
        with open(path,'rb') as f:data=f.read()
        count=struct.unpack_from('<I',data,80)[0]
        assert len(data)==84+50*count
        edges=collections.Counter(); vertices=set(); degenerate=0
        for i in range(count):
            values=struct.unpack_from('<12f',data,84+50*i)
            tri=[tuple(round(values[3+3*j+k],6) for k in range(3)) for j in range(3)]
            if len(set(tri))<3:degenerate+=1
            vertices.update(tri)
            for j in range(3):edges[tuple(sorted((tri[j],tri[(j+1)%3])))]+=1
        bad=collections.Counter(n for n in edges.values() if n!=2)
        minimum=[min(v[k] for v in vertices) for k in range(3)]
        maximum=[max(v[k] for v in vertices) for k in range(3)]
        assert not bad and not degenerate,(path,bad,degenerate)
        assert abs(minimum[2])<.001
        envelope=[maximum[k]-minimum[k] for k in range(3)]
        assert all(abs(a-b)<.02 for a,b in zip(envelope,report['print_export']['oriented_bbox_mm']))
        rows.append(dict(stl=path,facets=count,vertices=len(vertices),edge_incidence_errors=dict(bad),
                         degenerate_facets=degenerate,min_z_mm=minimum[2],envelope_mm=envelope,
                         sha256=hashlib.sha256(data).hexdigest(),source='Fusion MCP verification of the actual Fusion export'))
    with open(os.path.join(OUT,'export_artifact_checks.json'),'w') as f:
        json.dump(rows,f,indent=2);f.write('\n')
    print(json.dumps(rows))
