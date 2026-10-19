# Test layout iOS: safe area, tabbar, overflow, zoom. Emula inset (--sat/--sab) e display-mode standalone.
import sys,json
from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
res=[]
def ok(n,c,d=''):
    res.append(bool(c)); print('PASS' if c else 'FAIL',n,d)
# (larghezza, altezza, sat PWA, sab PWA)
DEV=[(320,568,20,0),(375,812,50,34),(390,844,59,34),(430,932,59,34)]
SHOT='--shots' in sys.argv
LEAF_JS="""(sat)=>{
 const out=[]; const vis=(e)=>{const cs=getComputedStyle(e); if(cs.display==='none'||cs.visibility==='hidden'||parseFloat(cs.opacity)===0) return false; let p=e.parentElement; while(p){const c=getComputedStyle(p); if(c.display==='none'||c.visibility==='hidden') return false; p=p.parentElement;} return true;};
 const all=document.querySelectorAll('body *');
 for(const e of all){
   if(e.closest('.app-tabbar')||e.classList.contains('skip-link')||(e.closest('.sidebar')&&!document.getElementById('sidebarToggle').checked)) continue;
   if(document.getElementById('onboardingScreen')&&!document.getElementById('onboardingScreen').hidden&&e.closest('#intro')) continue;
   if(document.getElementById('journeyStarted').checked&&e.closest('#intro')) continue;
   if(e.closest('.lm-art')||(e.closest('.intro-logo')&&document.getElementById('intro').classList.contains('lm-art-ready'))) continue; /* illustrazione a tutto schermo per progetto; titolo solo per screen reader (già nell'illustrazione) */
   if(e.closest('.lm-scene')) continue; /* sfondo decorativo aria-hidden: a tutto schermo per progetto (sotto la safe area) */
   if(!['BUTTON','A','INPUT','SELECT','TEXTAREA','H1','H2','H3','SVG','IMG','LABEL','SUMMARY'].includes(e.tagName.toUpperCase()) && !(e.children.length===0 && (e.textContent||'').trim().length>0)) continue;
   const r=e.getBoundingClientRect(); if(r.width<2||r.height<2) continue;
   if(r.bottom<=0||r.top>=innerHeight) continue;
   if(!vis(e)) continue;
   const cs=getComputedStyle(e); if(cs.position==='absolute'&&e.classList.contains('intro-scanlines')) continue;
   // elemento "coperto" dalla striscia: la sua parte alta sta sotto sat
   if(r.top < sat-0.5 && r.bottom > 0.5){ out.push((e.id||e.className||e.tagName).toString().slice(0,40)+' top='+r.top.toFixed(1)+' txt='+(e.textContent||'').trim().slice(0,24)); }
 }
 return out.slice(0,8);
}"""
def setup(b,w,h,sat,sab,mode):
    ctx=b.new_context(viewport={'width':w,'height':h},is_mobile=True,has_touch=True,device_scale_factor=3)
    pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    cdp=ctx.new_cdp_session(pg)
    feats=[{'name':'display-mode','value':'standalone' if mode=='pwa' else 'browser'}]
    cdp.send('Emulation.setEmulatedMedia',{'features':feats})
    pg.goto(F); pg.wait_for_timeout(900)
    if mode=='pwa':
        pg.add_style_tag(content=':root{--sat:%dpx !important;--sab:%dpx !important}'%(sat,sab))
    else:
        pg.add_style_tag(content=':root{--sat:0px !important;--sab:0px !important}')
    pg.wait_for_timeout(150)
    return ctx,pg,errs
def overflow(pg):
    return pg.evaluate("""()=>{const d=document.documentElement; const o=[]; 
      const ov=document.querySelectorAll('.tessera-overlay,.friends-overlay,.tva-archives-overlay,.multiverse-graph-overlay,.alt-timeline-overlay,.info-overlay,.universe-timeline-overlay,.relationship-graph-overlay,.kang-tva-overlay');
      let bad=[]; ov.forEach(e=>{if(getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>0&&e.scrollWidth>e.clientWidth+0.5) bad.push((e.className+'').slice(0,30)+':'+e.scrollWidth+'>'+e.clientWidth);});
      return {page:d.scrollWidth-d.clientWidth,bad}}""")
def wide(pg):
    return pg.evaluate("""()=>{const W=innerWidth;const out=[];for(const e of document.querySelectorAll('body *')){if(e.closest('.app-tabbar')||e.classList.contains('skip-link')||(e.closest('.sidebar')&&!document.getElementById('sidebarToggle').checked))continue;const r=e.getBoundingClientRect();if(r.width<2||r.height<2||r.bottom<=0||r.top>=innerHeight)continue;const cs=getComputedStyle(e);if(cs.display==='none'||cs.visibility==='hidden')continue;if(e.closest('[hidden]'))continue;if(e.closest('.intro-scanlines'))continue;if(r.right>W+1||r.left<-1){let p=e.parentElement,clipped=false;while(p&&p!==document.body){const c=getComputedStyle(p);if(['hidden','auto','scroll','clip'].includes(c.overflowX)){const pr=p.getBoundingClientRect();if(pr.right<=W+1&&pr.left>=-1){clipped=true;break;}}p=p.parentElement;}if(!clipped)out.push((e.id||(e.className+'')||e.tagName).slice(0,36)+' ['+Math.round(r.left)+','+Math.round(r.right)+']');}}return out.slice(0,6);}""")
for (w,h,sat,sab) in DEV:
  for mode in ('safari','pwa'):
    S=sat if mode=='pwa' else 0; B=sab if mode=='pwa' else 0
    tag='%dpx %s'%(w,mode)
    with sync_playwright() as p:
        b=p.chromium.launch(); ctx,pg,errs=setup(b,w,h,sat,sab,mode)
        # --- schermata iniziale
        ok('[%s] intro: nessun elemento sotto la safe area'%tag, not pg.evaluate(LEAF_JS,S), pg.evaluate(LEAF_JS,S))
        ov=overflow(pg); ok('[%s] intro: no scroll orizzontale'%tag, ov['page']<=0 and not ov['bad'], ov)
        if SHOT: pg.screenshot(path='/tmp/claude-0/t/shots/%d_%s_intro.png'%(w,mode))
        # logo: top >= sat
        lt=pg.evaluate("()=>document.querySelector('.intro-eyebrow').getBoundingClientRect().top"); ok('[%s] intro: eyebrow sotto la safe area'%tag, lt>=S, round(lt,1))
        pg.click('#journeyStartBtn'); pg.wait_for_timeout(500)
        lv=pg.evaluate(LEAF_JS,S); ok('[%s] onboarding(1): nessun elemento sotto la safe area'%tag, not lv, lv)
        pg.wait_for_timeout(2000)
        lv=pg.evaluate(LEAF_JS,S); ok('[%s] onboarding(2): nessun elemento sotto la safe area'%tag, not lv, lv)
        ov=overflow(pg); ok('[%s] onboarding: no scroll orizzontale'%tag, ov['page']<=0 and not ov['bad'], ov)
        if SHOT: pg.screenshot(path='/tmp/claude-0/t/shots/%d_%s_onb.png'%(w,mode))
        pg.click('#onboardingStartBtn'); pg.wait_for_timeout(900)
        pg.wait_for_timeout(300)
        pg.evaluate("()=>window.scrollTo({top:0,behavior:\x27instant\x27})"); pg.wait_for_timeout(200)
        # --- HOME
        lv=pg.evaluate(LEAF_JS,S); ok('[%s] home: nessun elemento sotto la safe area'%tag, not lv, lv)
        gr=pg.evaluate("()=>{const e=document.getElementById('homeHubHello');return e?e.getBoundingClientRect().top:-1}"); ok('[%s] home: saluto sotto la safe area'%tag, gr>=S, round(gr,1))
        ov=overflow(pg); wd=wide(pg); ok('[%s] home: no scroll orizzontale'%tag, ov['page']<=0 and not wd, [ov,wd])
        if SHOT: pg.screenshot(path='/tmp/claude-0/t/shots/%d_%s_home.png'%(w,mode))
        # fondo home: ultimo pulsante non coperto dalla barra
        pg.evaluate("()=>window.scrollTo({top:document.documentElement.scrollHeight,behavior:\x27instant\x27})"); pg.wait_for_timeout(250)
        cov=pg.evaluate("""()=>{const tb=document.getElementById('appTabbar').getBoundingClientRect().top;const bs=[...document.querySelectorAll('.home-hub-btn')].filter(e=>e.getBoundingClientRect().height>0);const last=bs[bs.length-1].getBoundingClientRect().bottom;return [last,tb]}""")
        ok('[%s] home: ultimo pulsante non coperto dalla barra'%tag, cov[0]<=cov[1]+0.5, cov)
        # --- barra inferiore
        g=pg.evaluate("""()=>{const t=document.getElementById('appTabbar');const r=t.getBoundingClientRect();const tabs=[...t.querySelectorAll('.app-tab')].map(e=>{const q=e.getBoundingClientRect();const l=e.querySelector('.app-tab-lbl');return {w:q.width,h:q.height,lw:l.scrollWidth,cw:e.clientWidth,fs:parseFloat(getComputedStyle(l).fontSize)}});return {bottom:r.bottom,h:r.height,left:r.left,right:r.right,vh:innerHeight,vw:innerWidth,tabs}}""")
        ok('[%s] barra: ancorata al bordo inferiore'%tag, abs(g['bottom']-g['vh'])<0.6, g['bottom'])
        exp=3.25*16+B; ok('[%s] barra: altezza = 52px + inset (%d)'%(tag,B), abs(g['h']-exp)<0.6, g['h'])
        ok('[%s] barra: larga tutto lo schermo'%tag, g['left']<=0.5 and abs(g['right']-g['vw'])<0.6)
        ok('[%s] barra: 6 sezioni'%tag, len(g['tabs'])==6)
        ws=[t['w'] for t in g['tabs']]; ok('[%s] barra: sezioni di larghezza uguale (±1px)'%tag, max(ws)-min(ws)<=1.01, ws)
        ok('[%s] barra: target tocco >=44px'%tag, all(t['h']>=44 and t['w']>=44 for t in g['tabs']), [(round(t['w']),round(t['h'])) for t in g['tabs']])
        ok('[%s] barra: etichette non troncate'%tag, all(t['lw']<=t['cw']+0.5 for t in g['tabs']), [(t['lw'],t['cw']) for t in g['tabs']])
        ok('[%s] barra: etichette >=9.5px'%tag, all(t['fs']>=9.5 for t in g['tabs']), [t['fs'] for t in g['tabs']])
        if SHOT: pg.screenshot(path='/tmp/claude-0/t/shots/%d_%s_bar.png'%(w,mode))
        # --- tab: timeline, missioni, atlante, tessera, friends
        for tab in ('Timeline','Missioni','Atlante','Tessera','Friends','Home'):
            pg.click('#appTab'+tab); pg.wait_for_timeout(1500)
            if tab in ('Timeline','Missioni'):
                tid='parte1' if tab=='Timeline' else 'dashboard'
                t=pg.evaluate("(id)=>document.getElementById(id).getBoundingClientRect().top",tid)
                ok('[%s] %s: inizio sezione sotto la safe area (top=%.0f, sat=%d)'%(tag,tab,t,S), t>=S-0.5, round(t,1))
            else:
                pg.evaluate('window.scrollTo({top:0,behavior:\x27instant\x27})'); pg.wait_for_timeout(200)
                lv=pg.evaluate(LEAF_JS,S); ok('[%s] %s: nessun elemento sotto la safe area'%(tag,tab), not lv, lv)
            ov=overflow(pg); wd=wide(pg); ok('[%s] %s: no scroll orizzontale'%(tag,tab), ov['page']<=0 and not ov['bad'] and not wd, [ov,wd])
            if SHOT: pg.screenshot(path='/tmp/claude-0/t/shots/%d_%s_%s.png'%(w,mode,tab))
            if tab=='Atlante':
                # Fase 1: l'Atlante e' immersivo, la barra inferiore dell'app e il menu circolare sono nascosti per scelta
                im=pg.evaluate("()=>({bar:getComputedStyle(document.getElementById('appTabbar')).display,ham:getComputedStyle(document.querySelector('.sidebar-open-btn')).display,top:document.querySelector('.a2-top').getBoundingClientRect().top,pt:parseFloat(getComputedStyle(document.querySelector('.a2-top')).paddingTop),bb:(()=>{const s=document.querySelector('.a2-scroll');return parseFloat(getComputedStyle(s).paddingBottom)})()})")
                ok('[%s] Atlante: immersivo, barra app e menu nascosti, header e fondo con safe area'%tag, im['bar']=='none' and im['ham']=='none' and im['top']==0 and im['pt']>=S-0.5 and im['bb']>=0, im)
                pg.evaluate("()=>tvaAtlas2.exit()"); pg.wait_for_timeout(600)
            if tab in ('Timeline','Missioni','Tessera','Friends'):
                pg.evaluate('window.scrollTo({top:document.documentElement.scrollHeight,behavior:\x27instant\x27})'); pg.wait_for_timeout(300)
                cv=pg.evaluate("""()=>{const tb=document.getElementById('appTabbar').getBoundingClientRect().top;let m=0;for(const e of document.body.children){const cs=getComputedStyle(e);if(cs.display==='none'||cs.position==='fixed'||cs.position==='absolute'||e.tagName==='SCRIPT'||e.tagName==='STYLE'||e.tagName==='INPUT')continue;const r=e.getBoundingClientRect();if(r.height<2)continue;if(r.bottom>m)m=r.bottom;}return [m,tb]}""")
                ok('[%s] %s: fondo contenuto non coperto dalla barra'%(tag,tab), cv[0]<=cv[1]+0.5, cv)
        ok('[%s] nessun errore JS'%tag, not errs, errs[:2])
        b.close()
print('TOTALE FALLITI',res.count(False),'su',len(res))
