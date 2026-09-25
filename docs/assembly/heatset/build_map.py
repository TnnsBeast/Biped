"""SVG documentation overlays on unchanged Fusion MCP captures (no CAD operations)."""
from pathlib import Path
import base64
import json
from html import escape

HERE = Path(__file__).resolve().parent
VIEWS = HERE.parent / 'manual/views'
MANIFEST = json.loads((VIEWS / 'manifest.json').read_text())
BLUE, ORANGE = '#086bba', '#b74c0b'
SPECS = [
    ('shoulder_hub', '28_hub_inserts', 'Shoulder hub', '6 × M4 inserts · 8 mm long', 6, 'out',
     ['FACE SHOWN: LINK SIDE', 'Insert from this face.', 'Finish flush at both ends.', '', 'Only the six circled outer', 'holes receive inserts.', '', 'Inner screw holes and three', 'root-dowel sockets stay clear.']),
    ('proximal_link', '20_prox_inserts', 'Proximal link — knee end', '5 × M3 inserts · 5 mm long', 5, 'out',
     ['FACE SHOWN: OUTBOARD', 'Insert from this face.', 'All five finish flush.', '', '1–2: keeper / encoder bracket', '3–5: knee stop plate', '', 'No inserts at the shoulder end.']),
    ('shoulder_plate', '27_plate_inserts', 'Shoulder plate', '4 × M3 inserts · 5 mm long', 4, 'out',
     ['FACE SHOWN: COVER SIDE', 'Insert from this face.', 'Finish flush through the plate.', '', 'Four circled holes around the', 'motor opening hold the cover.', '', 'The cable cover itself takes', 'no inserts. Other plate holes', 'remain clear.']),
    ('stand', '26_stand_inserts', 'Mode A stand', '5 × M3 inserts · 5 mm long', 5, 'out',
     ['FACE SHOWN: PLATE MOUNT', 'Insert from this face.', 'All five finish flush.', '', 'Four holes at the top, plus', 'one beside the motor opening.', '', 'Do not put inserts in the', 'bench-mounting base holes.']),
    ('wheel_hub', '21_wheel_inserts', 'Wheel hub', '6 × M4 inserts · 8 mm long', 6, 'in',
     ['FACE SHOWN: MOTOR SIDE', 'Insert from this face.', 'Finish flush on the motor side.', '', 'The opposite / shell side has', '2.0 mm of brass projecting.', 'Do not make both ends flush.', '', 'The three inner motor screw', 'holes remain clear.']),
]


def build(spec):
    slug, key, title, subtitle, count, side, notes = spec
    frame = MANIFEST['frames'][key]
    unique = {}
    for hole in frame['insert_circles']:
        w = hole['world']; axis = (round(w[0], 4), round(w[2], 4))
        if axis not in unique or ((w[1] > unique[axis]['world'][1]) == (side == 'out')):
            unique[axis] = hole
    holes = sorted(unique.values(), key=lambda h: (h['point'][1], h['point'][0]))
    assert len(holes) == count, (key, len(holes))
    # Proximal labels: upper pair are bracket receivers; lower trio are stop receivers.
    if slug == 'proximal_link':
        holes = sorted(holes[:2], key=lambda h: h['point'][0]) + sorted(holes[2:], key=lambda h: h['point'][0])
    raw = base64.b64encode((VIEWS / frame['file']).read_bytes()).decode()
    uri = 'data:image/png;base64,' + raw
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="900" viewBox="0 0 1200 900">',
             f'<title>{escape(title)} heat-set insert locations</title>',
             '<desc>Numbered circles mark only insert receivers on an existing Fusion MCP capture. Labels are documentation overlays.</desc>',
             '<rect width="1200" height="900" fill="white"/>',
             '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#20313d}.title{font-size:32px;font-weight:700}.note{font-size:21px}.small{font-size:17px}</style>']
    def text(x, y, value, cls='note', color=None):
        parts.append(f'<text x="{x}" y="{y}" class="{cls}"' + (f' style="fill:{color}"' if color else '') + f'>{escape(value)}</text>')
    text(40, 52, title, 'title'); text(40, 88, subtitle)
    text(40, 123, 'NUMBERED RINGS = INSERTS     •     Match the face shown before heating.', 'small', BLUE)
    bounds = [frame['bounds'][0]-8, frame['bounds'][1]-8,
              frame['bounds'][2]+8, frame['bounds'][3]+8]
    if slug == 'proximal_link': bounds = [865, 595, 1150, 850]
    x0,y0,x1,y1 = bounds
    scale = min(660/(x1-x0), 610/(y1-y0))
    tx,ty = 75+(660-(x1-x0)*scale)/2, 165+(610-(y1-y0)*scale)/2
    def pic(bounds, x,y,w,h):
        a,b,c,d = bounds
        parts.append(f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{a} {b} {c-a} {d-b}"><image width="{frame["width"]}" height="{frame["height"]}" xlink:href="{uri}"/></svg>')
    pic(bounds,tx,ty,(x1-x0)*scale,(y1-y0)*scale)
    for i,hole in enumerate(holes,1):
        hx,hy = hole['point']; x,y = tx+(hx-x0)*scale, ty+(hy-y0)*scale
        # Labels sit away from holes, with a leader terminating at each ring.
        if slug == 'stand':
            dx = -58 if hx < 1350 else 58
            dy = -12 if hy < 75 else (18 if hy < 150 else 0)
            r=12
        elif slug == 'proximal_link':
            dx = -60 if i in (1,3) else (60 if i in (2,5) else 0)
            dy = -40 if i < 3 else 55
            r=31
        else:
            dx = -53 if hx < 1335 else 53; dy = -25 if hy < 430 else 25; r=23
        color = ORANGE if slug == 'proximal_link' and i >= 3 else BLUE
        parts += [f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" fill-opacity="0.10" stroke="{color}" stroke-width="4"/>',
                  f'<path d="M{x+dx} {y+dy} L{x} {y}" stroke="{color}" stroke-width="2"/>',
                  f'<circle cx="{x+dx}" cy="{y+dy}" r="17" fill="{color}"/>',
                  f'<text x="{x+dx}" y="{y+dy+7}" text-anchor="middle" style="font-size:20px;font-weight:700;fill:white">{i}</text>']
    ny=208
    if slug == 'proximal_link':
        text(800,185,'Whole part: knee at lower left','small')
        pic(frame['bounds'],805,200,320,290)
        ny=532
    for line in notes:
        text(795,ny,line,'note',BLUE if line.startswith('FACE') else None); ny+=31
    text(40,841,'Existing Fusion MCP capture · Beni_SingleLegRig v30 / PINREV2 · circles from recorded receiver coordinates','small')
    text(40,871,'Location guide only. Use the receiver map for fit checks and installation depth.','small')
    parts.append('</svg>')
    (HERE / (slug+'.svg')).write_text('\n'.join(parts)+'\n')

for spec in SPECS:
    build(spec)
print('Built five SVG maps: 26 receiver callouts from the Fusion capture manifest.')
