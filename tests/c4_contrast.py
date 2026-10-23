# C4: contrasto misurato sui PIXEL (testo reso trasparente per leggere lo sfondo reale) di tutte le pillole .ud-st in tutti gli universi (Atlante 2.0). Soglia WCAG AA 4.5:1.
import sys,io,statistics,re
from playwright.sync_api import sync_playwright
from PIL import Image
F=sys.argv[1] if len(sys.argv)>1 else 'file:///home/claude/work/index.html'
SRC=F.replace('file://','') if F.startswith('file://') else None
def lin(c):
    c/=255; return c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
def L(r,g,b): return 0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b)
IDS=sorted(set(re.findall(r"'(uni-[a-z0-9-]+)'",open('/home/claude/work/index.html').read())))
INFO="""()=>[...document.querySelectorAll('#atlas2 .ud-st')].map(e=>{const cs=getComputedStyle(e);let op=1;for(let x=e;x;x=x.parentElement)op*=parseFloat(getComputedStyle(x).opacity);return {cls:e.className,color:cs.color,op,vis:e.offsetParent!==null}})"""
worst={}
with sync_playwright() as p:
    b=p.chromium.launch(); cx=b.new_context(viewport={'width':390,'height':844},service_workers='block'); pg=cx.new_page(); pg.goto(F); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true}")
    for U in IDS:
        try: pg.evaluate('(u)=>tvaAtlas2.openUni(u,true)',U)
        except Exception: continue
        pg.wait_for_timeout(250)
        pg.evaluate("()=>document.querySelectorAll('#atlas2 details').forEach(d=>d.open=true)"); pg.wait_for_timeout(150)
        infos=pg.evaluate(INFO)
        if not infos: continue
        pg.evaluate("()=>{const s=document.createElement('style');s.id='ztmp';s.textContent='#atlas2 .ud-st{color:transparent !important}';document.head.appendChild(s)}"); pg.wait_for_timeout(80)
        for i,info in enumerate(infos):
            if not info['vis']: continue
            el=pg.locator('#atlas2 .ud-st').nth(i); el.scroll_into_view_if_needed(); pg.wait_for_timeout(40)
            im=Image.open(io.BytesIO(el.screenshot())).convert('RGB'); w,h=im.size
            px=[im.getpixel((x,y)) for x in range(w//4,3*w//4) for y in range(h//3,2*h//3)]
            bg=tuple(int(statistics.median(c[k] for c in px)) for k in range(3))
            m=[float(v) for v in re.findall(r'[\d.]+',info['color'])]; a=(m[3] if len(m)>3 else 1)*info['op']
            fg=tuple(m[k]*a+bg[k]*(1-a) for k in range(3))
            l1,l2=L(*fg),L(*bg); cr=round((max(l1,l2)+0.05)/(min(l1,l2)+0.05),2)
            k=info['cls']
            if k not in worst or cr<worst[k][0]: worst[k]=(cr,bg,U)
        pg.evaluate("()=>document.getElementById('ztmp').remove()")
    b.close()
print('unis',len(IDS))
for k,v in worst.items(): print(('PASS ' if v[0]>=4.5 else 'FAIL ')+'contrasto %s %s (min %.2f, bg %s, %s)'%(k,'>= 4.5:1' if v[0]>=4.5 else '< 4.5:1',v[0],v[1],v[2]))
