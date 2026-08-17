#!/usr/bin/env python3
"""Run the viewer's kinematics + posing in node, with a stub three.js.

Catches the class of bug that shipped twice: a ReferenceError inside poseSide()
kills posing AND the readout, so the page renders a frozen, half-posed model
with an empty LIVE STATE panel and no error visible to the user.

    python3 web/check.py        # exits non-zero if any pose throws
"""
import os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src', 'viewer.html')

PRELUDE = r'''
function mm(a,b){const o=new Array(16).fill(0);for(let i=0;i<4;i++)for(let j=0;j<4;j++)for(let k=0;k<4;k++)o[i*4+j]+=a[i*4+k]*b[k*4+j];return o;}
class M4{
  constructor(){this.e=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1];}
  set(a){this.e=a.slice();return this;} clone(){return new M4().set(this.e);}
  copy(m){this.e=m.e.slice();return this;}
  makeRotationY(t){const c=Math.cos(t),s=Math.sin(t);return this.set([c,0,s,0,0,1,0,0,-s,0,c,0,0,0,0,1]);}
  makeTranslation(x,y,z){return this.set([1,0,0,x,0,1,0,y,0,0,1,z,0,0,0,1]);}
  makeScale(x,y,z){return this.set([x,0,0,0,0,y,0,0,0,0,z,0,0,0,0,1]);}
  multiply(m){return this.set(mm(this.e,m.e));}
  premultiply(m){return this.set(mm(m.e,this.e));}
  compose(p,q,s){return this.makeTranslation(p.x,p.y,p.z);}
}
class V3{ constructor(x=0,y=0,z=0){this.x=x;this.y=y;this.z=z;}
  set(x,y,z){this.x=x;this.y=y;this.z=z;return this;}
  copy(v){this.x=v.x;this.y=v.y;this.z=v.z;return this;}
  normalize(){const l=Math.hypot(this.x,this.y,this.z)||1;this.x/=l;this.y/=l;this.z/=l;return this;} }
// Everything except Matrix4/Vector3 is a deep permissive stub, so the scene and
// renderer setup runs headless while the real matrix maths is exercised exactly.
const permissive = () => new Proxy(function(){}, {
  get:(t,k)=>{ if(k==='then') return undefined; if(!(k in t)) t[k]=permissive(); return t[k]; },
  set:(t,k,v)=>{ t[k]=v; return true; }, apply:()=>permissive(), construct:()=>permissive() });
const THREE = new Proxy({Matrix4:M4, Vector3:V3}, {get:(t,k)=> (k in t)?t[k]:permissive()});
const OrbitControls = permissive();
const readout = () => {};
globalThis.devicePixelRatio=1; globalThis.innerWidth=1200; globalThis.innerHeight=800;
globalThis.addEventListener=()=>{};
const window={__BENI_GEO__:[], innerWidth:1200, innerHeight:800, devicePixelRatio:1, addEventListener(){}};
const document={getElementById:()=>({textContent:'',innerHTML:'',addEventListener(){},value:0,style:{},appendChild(){}}),
  body:{appendChild(){}}, createElement:()=>({style:{},appendChild(){},getContext:()=>({})})};
'''

EPILOGUE = r'''
let fails=0, first=null;
for(const th of [-185,-140,-90,-35,0,30,90,140,185])
  for(const ph of [-8,-4,0,5,10,12,20,25,27]){
    try{ poseSide('L',th,ph); poseSide('R',th,ph); }
    catch(e){ if(!first) first='theta='+th+' phi='+ph+' -> '+e.message; fails++; }
  }
const n = 9*9;
console.log('poseSide : '+(fails?('FAIL '+fails+'/'+n+'   first: '+first):('ok, '+n+' poses')));
let ufail=null;
try{ update(); }catch(e){ ufail=e.message; }
console.log('update() : '+(ufail?('FAIL -> '+ufail):'ok'));
const need=['static','centre','prox','dist','wheel','cart_up','cart_lo'];
const miss=need.filter(g=>!GROUPS.includes(g));
console.log('groups   : '+(miss.length?('MISSING '+miss.join(',')):GROUPS.join(', ')));
const base=wheelSpin(0,0);
const roll=(t,p)=>+(wheelSpin(t,p)-base).toFixed(1);
console.log('wheel roll: knee+25 '+roll(0,25)+' deg, squat+30 '+roll(30,0)+' deg, jump '+roll(-35,12)+' deg');
if(Math.abs(roll(0,25)) < 5) { console.log('wheel roll: FAIL - wheel barely turns'); process.exit(1); }
process.exit((fails||ufail||miss.length)?1:0);
'''


def main():
    js = re.search(r'<script[^>]*type="module"[^>]*>(.*?)</script>',
                   open(SRC).read(), re.S).group(1)
    lo = js.index('const D = Math.PI/180;')
    hi = js.index('/* ------------------------------------------------'
                  '----------------- readout */')
    body = js[lo:hi]
    # the loader needs a geometry payload we do not have; neuter it
    body = body.replace('(async function load(){', '(async function load(){ if(true) return;')
    with tempfile.NamedTemporaryFile('w', suffix='.mjs', delete=False) as f:
        f.write(PRELUDE + body + EPILOGUE)
        path = f.name
    r = subprocess.run(['node', '--input-type=module'],
                       stdin=open(path), capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0 and r.stderr.strip():
        print(r.stderr.strip()[:800], file=sys.stderr)
    os.unlink(path)
    return r.returncode


if __name__ == '__main__':
    sys.exit(main())
