import sys,json
from playwright.sync_api import sync_playwright
from leg_shot import boot
from cron3c_test import setcr,hub
VPS=[(320,568),(320,480),(360,640),(375,667),(390,844),(430,932),(844,390),(1024,768),(1280,800)]
F=[];N=[0]
def ok(n,c,d=''):
    N[0]+=1
    if not c: F.append(n); print('FAIL',n,str(d)[:400])
CHECK="""()=>{const out={ov:[],small:[],tap:[],overlapCards:0,sheetOut:null,hs:document.documentElement.scrollWidth>innerWidth+1};
 const sc=document.querySelector('.a2-scroll'); out.scw=sc.scrollWidth-sc.clientWidth;
 const els=[...document.querySelectorAll('.a2-cron *, .cr-ov *')].filter(e=>e.offsetParent!==null||getComputedStyle(e).position==='fixed');
 els.forEach(e=>{ if(e.children.length===0 && e.textContent.trim()){const fs=parseFloat(getComputedStyle(e).fontSize); if(fs<10.9) out.small.push([e.className,e.textContent.trim().slice(0,20),fs]); }
   if(e.matches('button,input,[role=tab]')){const r=e.getBoundingClientRect(); if(r.width>0&&(r.height<43.5||r.width<43.5)) out.tap.push([e.className,e.textContent.trim().slice(0,20),Math.round(r.width),Math.round(r.height)]);}});
 const rects=sel=>[...document.querySelectorAll(sel)].map(e=>e.getBoundingClientRect()).filter(r=>r.width>0);
 const inter=(a,b)=>a.left<b.right-1&&b.left<a.right-1&&a.top<b.bottom-1&&b.top<a.bottom-1;
 for(const sel of ['.cr-cd','.cr-lc']){const R=rects(sel);for(let i=0;i<R.length;i++)for(let j=i+1;j<R.length;j++)if(inter(R[i],R[j]))out.overlapCards++;}
 const sh=document.querySelector('.cr-sheet'); if(sh){const r=sh.getBoundingClientRect();out.sheetOut=[r.left>=-1,r.right<=innerWidth+1,r.top>=0,r.bottom<=innerHeight+1];}
 return out}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for W,H in VPS:
        ctx,pg,errs=boot(b,W,H); hub(pg); ids=pg.evaluate("()=>tvaUniverse.ids()"); mcu=ids[0]; fox=[i for i in ids if '10005' in i][0]
        states=[('hub',None),('uni',dict(mode='uni',uid=mcu,und=True)),('uni-ord-uscita',dict(mode='uni',uid=mcu,ord='uscita')),('uni-vuoto',dict(mode='uni',uid=[i for i in ids if 'legion' in i][0])),
          ('par-uscita',dict(mode='par',pA=mcu,pB=fox,lim=60)),('par-proprie',dict(mode='par',pA=mcu,pB=fox,pm='proprie')),('par-ab',dict(mode='par',pA=mcu,pB=fox,pm='ab')),('exp',dict(mode='exp',q='agents')),('exp-na',dict(mode='exp',fu=['_na'],na=True))]
        for name,kw in states:
            if kw is None: hub(pg); continue
            setcr(pg,**kw); r=pg.evaluate(CHECK); tag=f'{W}x{H} {name}'
            ok(tag+': nessun overflow orizzontale',not r['hs'] and r['scw']<=1,(r['hs'],r['scw']))
            ok(tag+': testi >= 11px',not r['small'],r['small'][:4]); ok(tag+': comandi >= 44px',not r['tap'],r['tap'][:4]); ok(tag+': nessuna sovrapposizione tra card',r['overlapCards']==0,r['overlapCards'])
        for nm,kw,sel in [('sheet-filtri',dict(mode='exp'),'#crFbtn'),('sheet-universo',dict(mode='uni',uid=mcu),'#crUniSel')]:
            setcr(pg,**kw); pg.click(sel); pg.wait_for_timeout(450); r=pg.evaluate(CHECK); tag=f'{W}x{H} {nm}'
            ok(tag+': dentro lo schermo',r['sheetOut'] and all(r['sheetOut']),r['sheetOut']); ok(tag+': comandi >= 44px',not r['tap'],r['tap'][:4]); ok(tag+': testi >= 11px',not r['small'],r['small'][:3])
            vis=pg.evaluate("()=>{const g=document.getElementById('crFgo')||document.querySelector('.cr-opt');const r=g.getBoundingClientRect();return r.bottom<=innerHeight+1&&r.top>=0}"); ok(tag+': comando principale visibile',vis)
            pg.keyboard.press('Escape')
        # reduced motion
        if (W,H)==(390,844):
            pg.emulate_media(reduced_motion='reduce'); setcr(pg,mode='uni',uid=mcu); an=pg.evaluate("()=>[getComputedStyle(document.querySelector('.cr-tl'),'::before').animationName,getComputedStyle(document.querySelector('.cr-ev .cr-cd')).animationName]")
            ok('reduced-motion: nessuna animazione',an==['none','none'],an)
            pg.emulate_media(reduced_motion='no-preference'); setcr(pg,mode='uni',uid=mcu); an=pg.evaluate("()=>getComputedStyle(document.querySelector('.cr-tl'),'::before').animationName")
            ok('motion normale: spina animata (transform/opacity)',an=='cr-draw',an)
            bad=pg.evaluate("()=>{const css=[...document.styleSheets].flatMap(s=>{try{return [...s.cssRules]}catch(e){return []}}).map(r=>r.cssText).join('\\n');const m=css.match(/\\.cr-[^{}]*\\{[^}]*(backdrop-filter|filter:)[^}]*\\}/g);return m}")
            ok('nessun filter/backdrop-filter nelle regole cr-',not bad,bad)
        ok(f'{W}x{H}: nessun errore JS',not errs,errs[:2]); ctx.close()
    b.close()
print('TOTALE',N[0],'FALLITI',len(F))
