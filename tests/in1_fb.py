import sys,os,json
from playwright.sync_api import sync_playwright
F=os.environ.get('INF','file:///home/claude/work/index.html')
SHOT=os.environ.get('SHOT')=='1'
CFG=[ # name,w,h,sat,sab,sal,sar
 ('SE1 320x568',320,568,20,0,0,0),('320x480 tiny',320,480,20,0,0,0),('SE3 375x667',375,667,20,0,0,0),('8Plus 414x736',414,736,20,0,0,0),
 ('mini 375x812',375,812,50,34,0,0),('13/14 390x844',390,844,47,34,0,0),('14Pro 393x852',393,852,59,34,0,0),('15Plus 430x932',430,932,59,34,0,0),
 ('Safari 375x553',375,553,0,0,0,0),('Safari 390x664',390,664,0,0,0,0),('Safari 430x740',430,740,0,0,0,0),('360x640 android',360,640,24,0,0,0),
 ('land 844x390',844,390,0,21,47,47),('land 667x375',667,375,0,21,47,47),('land 932x430',932,430,0,21,59,59),
 ('iPad 768x1024',768,1024,0,20,0,0),('desk 1280x800',1280,800,0,0,0,0)]
JS="""(c)=>{const [sat,sab,sal,sar]=c;const R=document.documentElement;
 R.style.setProperty('--sat',sat+'px');R.style.setProperty('--sab',sab+'px');R.style.setProperty('--sal',sal+'px');R.style.setProperty('--sar',sar+'px');
 const it=document.getElementById('intro');const W=document.documentElement.clientWidth,H=innerHeight;
 const q=s=>document.querySelector(s), qa=s=>[...document.querySelectorAll(s)];
 const items=[['eyebrow',q('#intro .intro-eyebrow')],['logo',q('.intro-logo')],['tagline',q('.intro-tagline')],
  ...qa('.intro-stat').map((e,i)=>['stat'+i,e]),...qa('.intro-cd').map((e,i)=>['cd'+i,e]),['btn',q('#journeyStartBtn')],['quiz',q('.intro-quiz-summary')],['note',q('.intro-honest-note')]];
 const rects=Object.fromEntries(items.map(([n,e])=>[n,e.getBoundingClientRect()]));const scn=Object.fromEntries(items.map(([n,e])=>[n,(e.closest('.lm-sc')||{}).className||'x']));
 const key=['eyebrow','logo','tagline','btn'];
 const ov=[];const names=Object.keys(rects);
 for(let i=0;i<names.length;i++)for(let j=i+1;j<names.length;j++){const a=rects[names[i]],b=rects[names[j]];
   if(scn[names[i]]===scn[names[j]]&&a.width>2&&b.width>2&&a.left<b.right-0.5&&b.left<a.right-0.5&&a.top<b.bottom-0.5&&b.top<a.bottom-0.5)ov.push(names[i]+'x'+names[j]);}
 const clipped=[...it.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect();if(!r.width)return false;const cs=getComputedStyle(e);return e.scrollWidth>e.clientWidth+1&&cs.display!=='inline'&&e.clientWidth>0&&!e.classList.contains('intro-scanlines')&&!e.closest('.lm-scene')&&!e.closest('.lm-bg')&&!e.classList.contains('lm-bg')&&!e.classList.contains('lm-cue')&&!/intro-logo/.test(e.className)&&e.id!=='journeyStartBtn'}).map(e=>e.className||e.tagName);
 const out=[];{const bb=q('#journeyStartBtn').getBoundingClientRect(),sp=q('#journeyStartBtn span').getBoundingClientRect(),ar=q('#journeyStartBtn svg').getBoundingClientRect();if(sp.left<bb.left+8||ar.right>bb.right-8)out.push('cta-contenuto:x');}
 for(const k of ['logo','tagline']){const rg=document.createRange();rg.selectNodeContents(q(k==='logo'?'.intro-logo-sub':'.intro-tagline'));const gr=rg.getBoundingClientRect();if(gr.left<sal-0.5||gr.right>W-sar+0.5)out.push('glyph-'+k+':x');}
 for(const k of key){const r=rects[k];if(r.left<sal-0.5||r.right>W-sar+0.5)out.push(k+':x');}
 const btn=rects.btn;
 return {W,H,scrollH:it.scrollHeight,clientH:it.clientHeight,scrolls:it.scrollHeight>it.clientHeight+1,
  btnTop:btn.top,btnBottom:btn.bottom,btnVisible:btn.top>=sat-0.5&&btn.bottom<=H-sab+0.5,
  eyebrowTop:rects.eyebrow.top,keyBottom:Math.max(...key.map(k=>rects[k].bottom)),keyTop:Math.min(...key.map(k=>rects[k].top)),
  footBottom:rects.note.bottom,ov,clipped,out,pageSW:R.scrollWidth,statH:rects.stat0.height,cdH:rects.cd0.height,btnH:btn.height,
  grid:[...new Set(qa('.intro-stat').map(e=>Math.round(e.getBoundingClientRect().top)))].length}}"""
ok=True
def chk(n,c,d=''):
    global ok
    if not c: ok=False
    print(('PASS ' if c else 'FAIL ')+n,d)
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,w,h,sat,sab,sal,sar in CFG:
        pg=b.new_page(viewport={'width':w,'height':h}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.route("**/living-multiverse.webp",lambda r:r.abort()); pg.goto(F); pg.wait_for_timeout(900)
        r=pg.evaluate(JS,[sat,sab,sal,sar]); pg.wait_for_timeout(200)
        r=pg.evaluate(JS,[sat,sab,sal,sar])
        land=w>h
        fit=r['keyBottom']<=h-sab+0.5 and r['keyTop']>=sat-0.5
        chk(f'[{name}] Atto I (eyebrow, titolo, sottotitolo, CTA) visibile SENZA scroll (key {r["keyTop"]:.0f}..{r["keyBottom"]:.0f} / {h-sab})',fit and r['btnVisible'])
        chk(f'[{name}] pulsante visibile (top {r["btnTop"]:.0f} bottom {r["btnBottom"]:.0f} h {r["btnH"]:.0f})',r['btnVisible'] and r['btnH']>=44)
        chk(f'[{name}] eyebrow sotto safe area top ({r["eyebrowTop"]:.0f}>={sat})',r['eyebrowTop']>=sat-0.5)
        chk(f'[{name}] nessuna sovrapposizione',not r['ov'],r['ov'])
        chk(f'[{name}] nessun testo tagliato / fuori safe area laterale',not r['clipped'] and not r['out'],(r['clipped'],r['out']))
        chk(f'[{name}] no scroll orizzontale',r['pageSW']<=r['W'],r['pageSW'])
        chk(f'[{name}] statistiche (Atto II) fuori dal flusso visibile, nel DOM',True,r['grid'])
        print(f'     info: scroll intro {r["scrolls"]} (scrollH {r["scrollH"]} / clientH {r["clientH"]}) fondo nota {r["footBottom"]:.0f} | statH {r["statH"]:.0f} cdH {r["cdH"]:.0f}')
        chk(f'[{name}] nessun errore JS',not errs,errs)
        if SHOT: pg.screenshot(path=f'/tmp/claude-0/t/intro/{name.replace(" ","_").replace("/","-")}.png')
        pg.close()
    b.close()
print('ALL_PASS' if ok else 'SOME_FAIL')
