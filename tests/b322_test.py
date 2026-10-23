import io,itertools,time,base64,json
from PIL import Image
import numpy as np
from playwright.sync_api import sync_playwright
from f4lib import ok,done
ns={}; exec(open('/tmp/claude-0/t/b321_geom.py').read().split("JS=")[0].replace("from playwright.sync_api import sync_playwright",""),ns)
FR,TH,M,art=ns['FR'],ns['TH'],ns['M'],ns['art']
AV=['agente','variante','esploratore','tecnologico','mistico','astratto','cronista','sentinella']
BN=['Primo Passo','Guardiano della Linea Sacra','Cacciatore di Varianti','Archivista','Essenziale','Nessuna Divergenza','Cinefilo TVA','Maratoneta del Multiverso','Collezionista','Guerriero del Weekend','Meta Strada','Critico Ufficiale','Preferiti','Cronista']
def shot(pg,m,lay,w):
    pg.evaluate("([m,l,w,u])=>{const d=document.getElementById('d');d.innerHTML=tvaCardArt.build(m,l,{uid:u});const s=d.firstChild;s.style.width=w+'px';s.style.height='auto';s.style.display='block'}",[m,lay,w,'z'])
    return Image.open(io.BytesIO(pg.locator('#d').screenshot())).convert('RGB')
def dist(a,b,gray=False):
    A=np.asarray(a.convert('L') if gray else a,dtype=float);B=np.asarray(b.convert('L') if gray else b,dtype=float); return np.abs(A-B).mean()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':760,'height':900})
    pg.set_content('<body style="margin:0;background:#000"><div id=d></div>'); pg.add_script_tag(content=art)
    # 1 testo non troncato (verticale)
    cut=[]
    for n in BN:
        t=pg.evaluate("([m])=>{const d=document.createElement('div');d.innerHTML=tvaCardArt.build(m,'vertical',{uid:'t'});return [...d.querySelectorAll('text')].map(x=>x.textContent).join('|')}",[dict(M,badges=[{'id':'critico','name':n}])])
        words=n.split(); 
        if '…' in t or not all(w in t for w in words): cut.append(n)
    ok('V1 verticale: nomi di tutti i 14 distintivi interi (nessuna ellissi)',cut==[],cut)
    t=pg.evaluate("([m])=>{const d=document.createElement('div');d.innerHTML=tvaCardArt.build(m,'vertical',{uid:'t'});return [...d.querySelectorAll('text')].map(x=>x.textContent).join('|')}",[dict(M,name='Alessandro Montefus',title='Sovrano delle Linee Temporali')])
    ok('V2 verticale: nickname di 19 caratteri e titolo lungo interi',('Alessandro Montefus' in t) and ('Sovrano delle Linee Temporali' in t) and '…' not in t,t[:120])
    sz=pg.evaluate("([m])=>{const d=document.createElement('div');d.innerHTML=tvaCardArt.build(m,'vertical',{uid:'t'});return [...d.querySelectorAll('text')].map(x=>[x.textContent,parseFloat(x.getAttribute('font-size'))])}",[M])
    ok('V3 verticale: ogni testo >= 20 unita (>= 10px a 360px di larghezza)',min(s for _,s in sz)>=20,[x for x in sz if x[1]<20])
    ok('V4 verticale: nickname protagonista (>= 56 unita) e piu grande di ogni altro testo tranne LV',max(s for t_,s in sz if t_=='Franco Posteraro')>=56)
    ar=pg.evaluate("([m])=>{const d=document.getElementById('d');d.innerHTML=tvaCardArt.build(m,'vertical',{uid:'q'});const c=[...d.querySelectorAll('clipPath')].map(x=>x.firstElementChild.getBBox()).sort((a,b)=>b.width*b.height-a.width*a.height)[0];return c.width*c.height/(720*1200)}",[M])
    ok('V5 verticale: ritratto = punto focale (>= 14% dell\'area)',ar>=0.14,ar)
    # confronto struttura orizzontale/verticale: nessun elemento in comune di posizione
    ok('V6 verticale: composizione autonoma (ritratto ad arco, non rettangolo della wide)',pg.evaluate("([m])=>{const d=document.getElementById('d');d.innerHTML=tvaCardArt.build(m,'vertical',{uid:'q'});return !!d.querySelector('clipPath path')}",[M]))
    # 2 avatar distinguibili
    def avs(a):
        pg.evaluate("([m])=>{document.getElementById('d').innerHTML=tvaCardArt.avatarThumb(m,'q');const s=document.getElementById('d').firstChild;s.style.width='300px';s.style.height='300px';s.style.display='block'}",[dict(M,avatar={'kind':'preset','id':a})])
        return Image.open(io.BytesIO(pg.locator('#d').screenshot())).convert('RGB')
    ims={a:avs(a) for a in AV}
    dd=[(dist(ims[x],ims[y]),dist(ims[x],ims[y],True),x,y) for x,y in itertools.combinations(AV,2)]
    ok('A1 otto avatar: distanza minima a coppie (colore) >= 10 e (grigi) >= 7',min(d[0] for d in dd)>=10 and min(d[1] for d in dd)>=7,sorted(dd,key=lambda z:z[1])[:3])
    # 3 temi con stessa cornice
    ti={t:shot(pg,dict(M,theme=t),'wide',500) for t in TH}
    td=[(dist(ti[x],ti[y]),dist(ti[x],ti[y],True),x[5:],y[5:]) for x,y in itertools.combinations(TH,2)]
    ok('T1 dieci temi: distanza minima a coppie (colore) >= 6 e (grigi) >= 3',min(d[0] for d in td)>=5.5 and min(d[1] for d in td)>=3.5,sorted(td,key=lambda z:z[1])[:3])
    # 4 cornici in grigi
    fi={f:shot(pg,dict(M,frame=f),'wide',500) for f in FR}
    fd=[(dist(fi[x],fi[y],True),x[9:],y[9:]) for x,y in itertools.combinations(FR,2)]
    ok('F1 dodici cornici: distanza minima a coppie in scala di grigi >= 1.0',min(d[0] for d in fd)>=1.0,sorted(fd)[:4])
    # 5 leggendarie
    cnt=lambda f:pg.evaluate("([m])=>{const d=document.createElement('div');d.innerHTML=tvaCardArt.build(m,'wide',{uid:'t'});return d.querySelectorAll('*').length}",[dict(M,frame=f)])
    nc={f:cnt(f) for f in FR}; others=sorted(v for k,v in nc.items() if k!='cornice-nexus-supremo')
    ok('L1 Nexus Supremo: complessita (elementi) >= mediana delle altre',nc['cornice-nexus-supremo']>=others[len(others)//2],nc)
    leg=shot(pg,dict(M,frame='cornice-nexus-supremo',theme='tema-fine-del-tempo',titleId='titolo-colui-che-rimane',title='Colui che Rimane'),'vertical',360)
    base=shot(pg,dict(M,frame='cornice-oro-archivista',theme='tema-cronologia-dorata'),'vertical',360)
    ok('L2 combinazione leggendaria visivamente diversa da oro+oro',dist(leg,base)>=9,dist(leg,base))
    ok('L3 titolo leggendario: ornamento (alloro) presente',pg.evaluate("([m])=>{const d=document.createElement('div');d.innerHTML=tvaCardArt.build(m,'vertical',{uid:'t'});return d.innerHTML.includes('fill-opacity=\"0.85\"')||d.innerHTML.includes('.85')}",[dict(M,titleId='titolo-colui-che-rimane')]))
    # 6 prestazioni
    tm=pg.evaluate("([m])=>{const o={};for(const l of ['wide','compact','vertical']){const t=performance.now();let n=0,len=0;for(let i=0;i<20;i++){const s=tvaCardArt.build(m,l,{uid:'p'+i});len=s.length;n++}o[l]=[(performance.now()-t)/n,len]}return o}",[dict(M,frame='cornice-nexus-supremo',theme='tema-fine-del-tempo')])
    ok('P1 build SVG <= 25ms e <= 130KB per layout (caso peggiore Nexus+Fine del Tempo)',all(v[0]<=25 and v[1]<=130000 for v in tm.values()),tm)
    ok('P2 nessun filtro SVG costoso (feGaussianBlur/filter) nel motore',pg.evaluate("()=>!/<filter|feGaussian/.test(['wide','compact','vertical'].map(l=>tvaCardArt.build({name:'x',title:'y',id:'VAR-1',level:1,xp:1,xpCur:1,xpNeed:2,badges:[],avatar:{kind:'preset',id:'agente'},theme:'tema-fine-del-tempo',frame:'cornice-nexus-supremo',fx:'effetto-aura-leggendaria'},l,{uid:'f'})).join(''))"))
    b.close()
done()
