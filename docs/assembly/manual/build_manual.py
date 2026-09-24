"""Lay out the visual manual from Fusion MCP captures; no geometry rendering."""
from pathlib import Path
import json
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
VIEWS=HERE/'views'
DATA=json.loads((VIEWS/'manifest.json').read_text())['frames']
OUT=ROOT/'output/pdf/beni_single_leg_assembly_manual.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
W,H=842,595
INK=HexColor('#26363D'); BLUE=HexColor('#146477'); ORANGE=HexColor('#C15E20')
GREY=HexColor('#65747C'); PALE=HexColor('#ECF4F5'); LINE=HexColor('#CEDBDD')
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
c.setTitle('Beni - Illustrated single-leg assembly manual')
c.setAuthor('Beni project')
PAGES=[]


def txt(x,y,s,size=12,bold=False,color=INK):
    c.setFillColor(color); c.setFont('Helvetica-Bold' if bold else 'Helvetica',size)
    c.drawString(x,y,s)


def para(x,y,s,w=740,size=12,color=INK):
    p=Paragraph(s,ParagraphStyle('p',fontName='Helvetica',fontSize=size,leading=size*1.35,textColor=color))
    _,h=p.wrap(w,1000); p.drawOn(c,x,y-h); return h


def arrow(a,b,color=BLUE,width=2):
    dx,dy=b[0]-a[0],b[1]-a[1]; length=math.hypot(dx,dy)
    if length<4:return
    ux,uy=dx/length,dy/length
    c.setStrokeColor(white);c.setLineWidth(width+2);c.line(*a,*b)
    c.setStrokeColor(color);c.setLineWidth(width);c.line(*a,*b)
    p=c.beginPath();p.moveTo(*b)
    p.lineTo(b[0]-8*ux+3.5*uy,b[1]-8*uy-3.5*ux)
    p.lineTo(b[0]-8*ux-3.5*uy,b[1]-8*uy+3.5*ux);p.close()
    c.setFillColor(color);c.drawPath(p,fill=1,stroke=0)


def badge(x,y,letter):
    c.setFillColor(BLUE);c.setStrokeColor(white);c.setLineWidth(1.2)
    c.circle(x,y,9,fill=1,stroke=1)
    c.setFillColor(white);c.setFont('Helvetica-Bold',10)
    c.drawCentredString(x,y-3.5,letter)


def header(step,title,subtitle):
    if step is not None:
        txt(32,548,f'{step:02}',30,True,BLUE)
        txt(89,551,title,25,True)
    else: txt(32,551,title,27,True)
    para(33,530,subtitle,770,12,GREY)
    PAGES.append(title)


def footer():
    c.setStrokeColor(LINE);c.setLineWidth(.7);c.line(32,30,W-32,30)
    txt(32,16,'BENI  /  ABS SINGLE LEG  /  MOTORS UNPLUGGED',8,True,GREY)
    txt(619,16,'Fusion v30  |  23 Sep 2026',8,False,GREY)
    txt(790,16,str(len(PAGES)),9,True,BLUE)
    c.showPage()


def check(s,detail=''):
    c.setFillColor(PALE);c.roundRect(32,46,778,60,8,fill=1,stroke=0)
    txt(47,85,'CHECK',10,True,BLUE)
    para(105,94,s,688,12)
    if detail:para(105,70,detail,688,10,GREY)


def render(name,box=(34,117,592,388),move=(),marks=(),spring=False,inserts=None):
    f=DATA[name];x,y,w,h=box
    b=f['bounds'];pad=16
    left=max(0,b[0]-pad);top=max(0,b[1]-pad)
    right=min(f['width'],b[2]+pad);bottom=min(f['height'],b[3]+pad)
    scale=min(w/(right-left),h/(bottom-top))
    dw,dh=(right-left)*scale,(bottom-top)*scale
    px=x+(w-dw)/2;py=y+(h-dh)/2
    trans=lambda p:(px+(p[0]-left)*scale,py+(bottom-p[1])*scale)
    c.saveState();p=c.beginPath();p.rect(x,y,w,h);c.clipPath(p,stroke=0,fill=0)
    c.drawImage(str(VIEWS/f['file']),px-left*scale,py-(f['height']-bottom)*scale,
                width=f['width']*scale,height=f['height']*scale,mask='auto')
    for prefix in move:
        a=next(a for a in f['arrows'] if a['part'].startswith(prefix))
        a0,a1=trans(a['from']),trans(a['to'])
        # Show the direction in the exploded gap, leaving the hole mouth visible.
        v=(a1[0]-a0[0],a1[1]-a0[1])
        arrow((a0[0]+v[0]*.22,a0[1]+v[1]*.22),(a0[0]+v[0]*.88,a0[1]+v[1]*.88))
    if spring and 'spring_seats' in f['points']:
        p1,p2=map(trans,f['points']['spring_seats'])
        dx,dy=p2[0]-p1[0],p2[1]-p1[1];ln=math.hypot(dx,dy)
        ux,uy=dx/ln,dy/ln;radius=min(14,ln*.13)
        path=c.beginPath();path.moveTo(*p1)
        for i in range(1,25):
            t=i/25;side=radius*(1 if i%2 else -1)
            path.lineTo(p1[0]+dx*t-uy*side,p1[1]+dy*t+ux*side)
        path.lineTo(*p2);c.setStrokeColor(ORANGE);c.setLineWidth(2.6);c.drawPath(path)
    if inserts:
        unique={}
        for hole in f['insert_circles']:
            a=hole['world'];key=(round(a[0],4),round(a[2],4))
            if key not in unique or (a[1]>unique[key]['world'][1]) == (inserts=='out'):
                unique[key]=hole
        for hole in unique.values():
            px1,py1=trans(hole['point']);c.setStrokeColor(BLUE);c.setLineWidth(1.7)
            c.circle(px1,py1,6,fill=0,stroke=1)
    for prefix,letter,ox,oy in marks:
        part=next(v for k,v in f['parts'].items() if k.startswith(prefix))
        px1,py1=trans(part['center']);bx,by=px1+ox,py1+oy
        c.setStrokeColor(BLUE);c.setLineWidth(.8);c.line(px1,py1,bx,by)
        badge(bx,by,letter)
    c.restoreState()
    return trans


def icon(kind,x,y):
    c.setStrokeColor(INK);c.setFillColor(white);c.setLineWidth(1.1)
    if kind in ('screw','pin','insert'):
        if kind=='insert':
            c.roundRect(x,y-5,30,13,2,stroke=1,fill=1)
            for i in range(5):c.line(x+3+i*5,y-4,x+8+i*5,y+7)
        else:
            c.roundRect(x+7,y,39,6,2,stroke=1,fill=1)
            if kind=='screw':
                c.rect(x,y-3,9,12,stroke=1,fill=1)
                for i in range(7):c.line(x+10+i*5,y,x+13+i*5,y+6)
    elif kind=='clevis':
        c.roundRect(x+5,y,44,6,2,stroke=1,fill=1);c.rect(x,y-3,7,12,stroke=1,fill=1)
        c.circle(x+43,y+3,1.7,stroke=1,fill=0)
    elif kind=='bearing':
        for r in (11,8,4):c.circle(x+20,y+3,r,stroke=1,fill=0)
    elif kind=='washer':
        c.ellipse(x+2,y-5,x+27,y+10,stroke=1,fill=1);c.ellipse(x+9,y-1,x+20,y+6,stroke=1,fill=1)
    elif kind=='spring':
        p=c.beginPath();p.moveTo(x,y)
        for i in range(1,13):p.lineTo(x+i*3.5,y+(8 if i%2 else -2))
        c.drawPath(p)


def side(hardware=(),parts=(),note=''):
    x=652;y=483
    if hardware:
        txt(x,y,'HARDWARE',9,True,BLUE);y-=25
        for kind,label,caption in hardware:
            icon(kind,x,y);txt(x+57,y,label,12,True)
            y-=17;para(x,y,caption,153,10,GREY);y-=37
    if parts:
        y-=8;txt(x,y,'IN THIS VIEW',9,True,BLUE);y-=23
        for letter,label in parts:
            badge(x+8,y+3,letter);para(x+25,y+10,label,132,11);y-=35
    if note:
        y-=7;para(x,y,note,153,11,ORANGE)


def step(n,title,subtitle,view,hardware,parts,marks,move,ok,detail='',note='',spring=False):
    header(n,title,subtitle)
    render(view,move=move,marks=marks,spring=spring)
    side(hardware,parts,note);check(ok,detail);footer()


# Cover: picture dominates; short use limits stay with the bench manual.
header(None,'BENI / Single-leg assembly','Illustrated bench manual - current Amazon pins and revised ABS parts')
render('00_overview',(325,85,480,425),marks=[('Proximal_Link','E',-35,10),('Distal_Link','G',-38,0),('RIG_Stand','A',60,0)])
txt(36,471,'BUILD IN THIS ORDER',11,True,BLUE)
for i,(a,b) in enumerate([('01-04','Prepare loose parts'),('05-09','Build the shoulder'),('10-14','Build wheel end and knee'),('15-20','Fit cartridge and retainers'),('21','Hand-test the supported leg')]):
    y=437-i*45;txt(36,y,a,16,True);txt(98,y,b,12)
para(36,182,'Both motors unplugged.<br/>Stand clamped to the bench.<br/>Wheel clear of bench and floor.<br/>Keep one hand on the distal side.',270,13)
para(36,95,'23 SEP: Reprint hub + both links (PINREV2).<br/>Root/clevis holes Ø4.30; knee receiver Ø10.30.<br/>No M4 washers in hand: cotters bear on ABS;<br/>inspect both cotter faces after step 21.',285,10,ORANGE)
footer()

# Visual parts key. These IDs stay the same in the exploded drawings.
header(None,'Identify your printed parts','Reprint D, E and G from PINREV2. Keep K and the other current released parts.')
assets=[
 ('D','NEW shoulder hub','ordered_pin_integration/00_fusion_ABS_PINREV2_Shoulder_Output_Hub_D4p15_ROOT_D4p30_PRINT_ORIENTED.png'),
 ('E','NEW proximal link','ordered_pin_integration/00_fusion_ABS_PINREV2_Proximal_Link_D19p15_ROOT_D4p30_CLEVIS_D4p30_PRINT_ORIENTED.png'),
 ('G','NEW distal link','ordered_pin_integration/00_fusion_ABS_PINREV2_Distal_Link_D10p30_D6x10_CLEVIS_D4p30_PRINT_ORIENTED.png'),
 ('K','KEEP stop plate','ordered_pin_integration/00_fusion_ABS_PINREV_Knee_Stop_Plate_15deg_D6x10_CAPTIVE_PRINT_ORIENTED.png'),
 ('L','Upper cartridge eye','mechanical_spring_test/00_fusion_ABS_TEST_Cart_Upper_Eye_50mm_AXIS_UP_PRINT_ORIENTED.png'),
 ('N','Lower cartridge eye','mechanical_spring_test/00_fusion_ABS_TEST_Cart_Lower_Eye_50mm_AXIS_UP_PRINT_ORIENTED.png'),
 ('M','Guide bar','mechanical_spring_test/00_fusion_ABS_TEST_Cart_Guide_Bar_50mm_FLAT_PRINT_ORIENTED.png'),
 ('Q','Knee-pin spacer','mechanical_spring_test/00_fusion_ABS_TEST_Knee_Pin_Outboard_Spacer_PRINT_ORIENTED.png'),
 ('P','Keeper bracket','mechanical_spring_test/00_fusion_ABS_TEST_Knee_Encoder_Bracket_PIN_KEEPER_PRINT_ORIENTED.png'),
 ('R','No-tyre shell','mechanical_spring_test/00_fusion_ABS_TEST_Wheel_Rim_NoTyre_PRINT_ORIENTED.png'),
 ('J','Wheel hub','assembly_dry_fit/00_fusion_ABS_FA_Wheel_Hub_L_OWNED_M4x8_D5p30_PRINT_ORIENTED.png'),
 ('B','Shoulder plate','assembly_dry_fit/00_fusion_ABS_FA_Chassis_Shoulder_Plate_L_M3_INSERTS_PRINT_ORIENTED.png')]
for i,(letter,label,path) in enumerate(assets):
    col,row=i%4,i//4;x=32+col*195;y=367-row*128
    c.drawImage(str(ROOT/'first_article_stl'/path),x+20,y+17,width=150,height=100,preserveAspectRatio=True,anchor='c')
    badge(x+10,y+8,letter);txt(x+25,y+4,label,11,True)
para(35,106,'Also use the current stand (A), cable cover and front post. The stand and plate in hand are the owner-confirmed Ø4.5 M3-receiver prints.',760,11)
para(35,67,'Inboard = toward the stand/body. Outboard = away from the stand. C = GIM6010 shoulder motor; H = GIM4305 wheel motor; F = 6800 bearing.',760,10,GREY)
footer()

step(1,'Fit the two knee bearings','Work with the loose proximal link before installing inserts.','01_bearings',
 [('bearing','2 x 6800','Use undamaged bearings.'),('pin','1 x D10 x 35','Bought steel knee pin.')],
 [('E','New proximal link'),('F','6800 bearings')],
 [('Proximal_Link','E',0,35),('HW_Bearing_6800 (5):1','F',-28,0),('HW_Bearing_6800 (5):2','F',28,0)],
 ['HW_Bearing_6800 (5):1','HW_Bearing_6800 (5):2'],
 'Both bearings sit square, without rock. Pass the steel pin through each bearing separately.',
 'Press only on the outer bearing race; transfer old bearings only if they come out undamaged.')

header(2,'Insert the new hub and proximal link','Circled holes take inserts. Let each insert cool before starting a screw.')
render('28_hub_inserts',(35,161,368,319),inserts='out')
render('20_prox_inserts',(432,161,368,319),inserts='out')
txt(50,486,'D / SHOULDER HUB',12,True,BLUE);txt(449,486,'E / PROXIMAL LINK',12,True,BLUE)
txt(50,141,'6 x M4 x 8 inserts',15,True);txt(449,141,'5 x M3 inserts',15,True)
txt(50,122,'Enter from the outboard / link face.',11);txt(449,122,'3 stop-plate holes + 2 keeper holes.',11)
check('Inserts are flush, straight and firm after cooling. Keep heat away from the root-dowel sockets.',
      'The distal link, stop plate and cartridge eyes take no heat-set inserts.');footer()

header(3,'Finish the exposed insert receivers','Complete these before closing the motor and fixture joints.')
for name,box,title,count,detail,direction in [
 ('21_wheel_inserts',(35,163,243,322),'J / WHEEL HUB','6 x M4 x 8','Enter from motor face.', 'in'),
 ('27_plate_inserts',(298,163,243,322),'B / SHOULDER PLATE','4 x M3','Enter from outboard face.','out'),
 ('26_stand_inserts',(561,163,243,322),'A / STAND','5 x M3','Enter from plate-mount face.','out')]:
    render(name,box,inserts=direction);txt(box[0]+7,488,title,11,True,BLUE)
    txt(box[0]+7,142,count,14,True);txt(box[0]+7,123,detail,10)
check('Wheel-hub inserts project 2.0 mm on the rim side; shoulder-plate inserts finish flush.',
      'Use a depth-controlled tip. The stand has 6.0 mm pockets for the approved 5 mm M3 inserts.');footer()

step(4,'Seat the three root dowels','Support the detached hub flat. Keep the pin axes straight.','02_hub_dowels',
 [('pin','3 x Ø4 x 10','Bought root dowels.')],[('D','New shoulder hub')],
 [('Shoulder_Output','D',0,-45)],['HW_DowelPin_D4x10_Root'],
 'Seat each dowel 5.0 mm in its blind socket; half of the 10 mm pin stays exposed.',
 'Trial-fit the proximal root by hand now, then remove it for shoulder assembly.',
 note='Stop for whitening, splitting or a cocked pin.')

step(5,'Slide the plate over the bare rotor','View from outboard. The housing stays behind the plate.','03_plate_motor',
 [('screw','8 x M3 x 8','Shoulder housing screws.')],[('C','GIM6010 shoulder motor'),('B','Shoulder plate')],
 [('REF_GIM6010','C',-45,10),('Chassis_Shoulder','B',20,35)],
 ['Chassis_Shoulder','HW_SHCS_M3x8'],
 'Flat plate face against the stationary housing; cable-spiral lip faces outward.',
 'Use M3 x 8 here. M3 x 10 bottoms before this plate is clamped.')

step(6,'Fasten the shoulder to the stand','Clamp or bolt the stand to the bench before adding the leg.','04_stand',
 [('screw','5 x M3 x 10','Plate-to-stand screws.')],[('A','Clamped stand'),('B','Plate + motor from step 05')],
 [('RIG_Stand','A',-55,0),('Chassis_Shoulder','B',20,35)],
 ['Chassis_Shoulder','HW_SHCS_M3x10'],
 'The five plate holes line up with the stand inserts; all screws finger-start.',
 'Keep the motor power and communication leads unplugged.')

step(7,'Route the cable; fit cover and post','Complete this area while you can still reach it.','05_cover',
 [('screw','2 x M3 x 12','Upper post + cover positions.'),('screw','2 x M3 x 10','Lower cover positions.')],
 [('B','Stationary shoulder plate')],[('Shoulder_Cable_Cover','1',20,-30),('RIG_Cable_Post_A','2',15,30)],
 ['Shoulder_Cable_Cover','RIG_Cable_Post_A'],
 '1: Cover closes the cable spiral.  2: Front post sits outside the cover.',
 'Route the real harness first. The printed cover has clearance holes and takes no inserts.')

step(8,'Fit the rotating shoulder hub','The motor factory pins enter the back of the new hub.','06_hub_motor',
 [('screw','6 x M3 x 10','Hub-to-motor output screws.')],[('D','New hub with root dowels')],
 [('Shoulder_Output','D',25,-25)],['Shoulder_Output','HW_SHCS_M3x10'],
 'Hub reaches the metal output face by hand; the three bought dowels point toward the link.',
 'The three motor factory pins and the three bought root dowels are separate interfaces.')

step(9,'Attach the proximal root','Support the far end of the link throughout this step.','07_root',
 [('screw','6 x M4 x 10','Link-to-hub clamp screws.')],[('D','Rotating shoulder hub'),('E','New proximal link')],
 [('Shoulder_Output','D',-20,35),('Proximal_Link','E',35,-10)],
 ['Proximal_Link','HW_SHCS_M4x10'],
 'Faces meet on all three dowels before tightening. Every screw head sits flat.',
 'The six screws clamp the joint; do not use them to draw an incompatible fit together.')

step(10,'Mount the wheel motor','Detached distal link. View from inboard to show screw entry.','08_wheel_motor',
 [('screw','6 x M2.5 x 12','Enter from the inboard side.')],[('G','New distal link'),('H','GIM4305 wheel motor')],
 [('Distal_Link','G',-20,35),('REF_GIM4305','H',30,-30)],
 ['REF_GIM4305','HW_SHCS_M2p5x12'],
 'The motor seats on the distal wheel ring without screw pull-down.',
 'Keep the motor unplugged; support the loose assembly on the bench.')

step(11,'Fit the wheel output hub','View from outboard. The rim stays off for now.','09_wheel_hub',
 [('screw','3 x M3 x 8','Wheel hub to motor output.')],[('H','Wheel motor'),('J','Prepared wheel hub')],
 [('REF_GIM4305','H',-20,-35),('Wheel_Hub','J',25,20)],
 ['Wheel_Hub','HW_SHCS_M3x8'],
 'Hub seats by hand and all three output screws start freely.',
 'The six rim inserts were installed from the motor face in step 03.')

step(12,'Bring the distal receiver into the fork','The drawing isolates the links; support the fitted wheel motor and hub.','10_knee_entry',
 [],[('E','Proximal fork + bearings'),('G','Distal knee receiver')],
 [('Proximal_Link','E',-20,35),('Distal_Link','G',25,-25)],['Distal_Link'],
 'The distal receiver sits in the gap between the two bearings; all three pin bores align.',
 'Slide in from the open side along the illustrated path. Keep the spring off.')

step(13,'Insert the steel knee pin','View from inboard. The pin travels through bearing - receiver - bearing.','11_knee_pin',
 [('pin','1 x D10 x 35','Bought steel knee pin.')],[('E','Proximal fork'),('G','Distal receiver')],
 [('HW_DowelPin_D10','1',30,18)],['HW_DowelPin_D10'],
 'Firm-thumb insertion, full seating and hand withdrawal; no free spin or radial rock in the receiver.',
 'Prove withdrawal now, before adding the stop, cartridge or keeper. Stop if the pin seizes.')

step(14,'Capture the stop dowel','Fit the dowel first, then close it in with the new stop plate.','12_stop',
 [('pin','1 x Ø6 x 10','Distal blind stop socket.'),('screw','3 x M3 x 10','Stop plate to proximal inserts.')],
 [('K','New closed-skin stop plate')],
 [('HW_DowelPin_D6','1',-20,-22),('ABS_TEST_Knee_Stop','2',0,-35)],
 ['HW_DowelPin_D6','ABS_TEST_Knee_Stop','HW_SHCS_M3x10'],
 'Channel faces the dowel; closed skin faces outboard. Prove both stops with the spring absent.',
 'The plate bolts to the proximal link. Allowed knee range: -8° to +15°. No glue or press fit here.')

step(15,'Place the upper cartridge eye','Keep the supported knee at its -8° extension stop.','13_upper_eye',
 [],[('E','Proximal upper clevis'),('L','Upper cartridge eye')],
 [('ABS_TEST_Cart_Upper','L',-30,-20)],['ABS_TEST_Cart_Upper'],
 'The side pivot passage aligns with the clevis. The raised round spring pilot faces the lower eye.',
 'The round pilot hole carries the guide; the pointed-roof side hole carries the clevis pin.')

step(16,'Pin the upper eye','View from inboard. Add the washer and supplied cotter on the outboard end.','14_upper_pin',
 [('clevis','1 x M4 x 40','Head stays inboard.'),('washer','1 x M4 washer','ISO 7089 steel washer.')],
 [('L','Upper cartridge eye')],[('HW_ClevisPin','1',30,18),('HW_Washer','2',-28,20)],
 ['HW_ClevisPin','HW_Washer'],
 'Pin passes by hand. Washer rests on the printed outboard face; supplied cotter is fully seated.',
 'Orient the cotter radially away from the knee. No loose printed spacers.',
 note='Retention order: pin head / printed joint / steel washer / supplied cotter.')

header(17,'Guide first, then spring','Cartridge close-up with the surrounding links hidden. Keep the knee at -8°.')
render('25_eye_guide',(40,128,360,361),move=['ABS_TEST_Cart_Guide'],
       marks=[('ABS_TEST_Cart_Upper','L',-30,0),('ABS_TEST_Cart_Guide','M',30,0)])
render('24_cartridge',(434,128,360,361),move=['ABS_TEST_Cart_Lower'],spring=True,
       marks=[('ABS_TEST_Cart_Lower','N',30,0)])
txt(45,489,'1 / GUIDE INTO ROUND PILOT HOLE',11,True,BLUE)
txt(438,489,'2 / SPRING OVER GUIDE; LOWER EYE FOLLOWS',11,True,BLUE)
check('Both raised pilots face the spring. The lower eye slides freely on the guide.',
      'Use the owned OD18 / ID9 / 50 mm spring. Orange spring symbol is schematic.');footer()

step(18,'Pin the lower cartridge eye','Bring the lower eye into the distal clevis with the knee still at -8°.','16_lower_eye',
 [('clevis','1 x M4 x 40','Enter inboard to outboard.'),('washer','1 x M4 washer','Then the supplied cotter.')],
 [('G','Distal lower clevis'),('N','Lower cartridge eye')],
 [('ABS_TEST_Cart_Lower','N',-28,15)],['ABS_TEST_Cart_Lower','HW_ClevisPin_M4x40:2','HW_Washer_M4:2'],
 'The lower pin passes with fingertip pressure. Washer and cotter are on the outboard end.',
 'Stop if more than slight hand compression is needed; do not pull the eye in with a pin or clamp.',
 note='Turn the cotter radially away from the knee. Seat it fully without reshaping it.',spring=True)

step(19,'Fit the outboard knee-pin keeper','The cartridge is hidden in this close-up for visibility.','17_keeper',
 [('screw','2 x M3 x 16','Bracket to proximal inserts.')],[('Q','Knee-pin spacer'),('P','Keeper bracket')],
 [('ABS_TEST_Knee_Pin','Q',0,-30),('Knee_Encoder_Bracket','P',10,30)],
 ['ABS_TEST_Knee_Pin','Knee_Encoder_Bracket','HW_SHCS_M3x16'],
 'The spacer locator enters the bracket center hole; the bracket sits on its two mounting positions.',
 'This limits outboard travel only. Keep hand control of the distal side to prevent inboard escape.')

step(20,'Attach the no-tyre shell','The wheel assembly remains suspended throughout this test.','18_shell',
 [('screw','6 x M4 x 8','Shell to wheel-hub inserts.')],[('J','Wheel output hub'),('R','No-tyre test shell')],
 [('Wheel_Hub','J',-25,30),('ABS_TEST_Wheel_Rim','R',25,-30)],
 ['ABS_TEST_Wheel_Rim','HW_SHCS_M4x8'],
 'Shell seats without force; all six screws start freely. Leave the TPU tyre off.',
 'Do not place the test shell on the bench or floor.')

header(21,'Check motion by hand','Stand clamped. Both motors unplugged. Wheel clear. One hand contains the distal side.')
render('19_final',(43,145,350,344),spring=True)
render('22_flex',(449,145,350,344),spring=True)
txt(66,480,'-8° / EXTENSION STOP',12,True,BLUE)
txt(473,480,'+15° / FLEXION STOP',12,True,BLUE)
txt(247,126,'-8°     0°     +5°     +10°     +15°',17,True)
check('Move slowly between the stops. Observe smooth movement and the settle / return tendency.',
      'Stop for cracks, binding, coil contact, guide escape, moving pins, loose cotters or stop bypass.');footer()

c.save()
(HERE/'page_titles.json').write_text(json.dumps(PAGES,indent=2)+'\n')
print(json.dumps({'pdf':str(OUT),'pages':len(PAGES)}))
