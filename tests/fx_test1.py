from f4lib import *
def vis(pg): return pg.evaluate("""()=>{const bad=[];const vh=innerHeight,vw=innerWidth;let n=0;
  for(const y of [4,vh*.25,vh*.5,vh*.75,vh-4]){for(const x of [4,vw/2,vw-4]){n++;const e=document.elementFromPoint(x,y);if(!e||!e.closest('#onboardingScreen'))bad.push([Math.round(x),Math.round(y),e&&(e.id||e.className)])}}
  const i=document.getElementById('intro');return {bad:bad,intro:getComputedStyle(i).display,html:document.documentElement.className.includes('tva-onb')}}""")
with sync_playwright() as p:
    b=p.chromium.launch()
    for W,H in [(390,844),(320,568),(430,932)]:
        ctx=b.new_context(viewport={'width':W,'height':H},is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page(); pg.set_default_timeout(8000); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(U); pg.wait_for_timeout(1500)
        t='[%d] '%W
        r=pg.evaluate("()=>({intro:getComputedStyle(document.getElementById('intro')).display,onb:document.getElementById('onboardingScreen').hidden})"); ok(t+'primo accesso: introduzione visibile, onboarding nascosto',r['intro']!='none' and r['onb'],r)
        pg.evaluate("()=>document.getElementById('journeyStartBtn').click()"); pg.wait_for_timeout(300)
        v=vis(pg); ok(t+'step 1: l\'introduzione e\' smontata e solo l\'onboarding e\' visibile',v['intro']=='none' and v['html'] and not v['bad'],v)
        pg.wait_for_timeout(1900); v=vis(pg); ok(t+'step 2 «Registrazione completata»: unica schermata',v['intro']=='none' and not v['bad'],v)
        txt=pg.evaluate("()=>document.getElementById('onboardingStep2').innerText"); ok(t+'testo registrazione presente e nessun «Inizia il viaggio» visibile',('REGISTRAZIONE COMPLETATA' in txt.upper()) and 'Inizia il viaggio' not in pg.evaluate("()=>document.body.innerText"),txt[:60])
        # viewport dinamica: barra Safari che compare/scompare
        for hh in (H-90,H,H-60):
            pg.set_viewport_size({'width':W,'height':hh}); pg.wait_for_timeout(250); v=vis(pg); ok(t+'viewport dinamica %d: ancora unica schermata'%hh,not v['bad'] and v['intro']=='none',v)
        pg.set_viewport_size({'width':W,'height':H})
        bt=pg.evaluate("()=>{const r=document.getElementById('onboardingStartBtn').getBoundingClientRect();return [r.height,r.top,r.bottom,innerHeight]}"); ok(t+'pulsante «Inizia la timeline» raggiungibile e >=44px',bt[0]>=43.5 and bt[1]>=0 and bt[2]<=bt[3],bt)
        pg.touchscreen.tap(W/2,bt[1]+bt[0]/2); pg.wait_for_timeout(700)
        r=pg.evaluate("()=>({j:journeyStarted.checked,onb:document.getElementById('onboardingScreen').hidden,cls:document.documentElement.className.includes('tva-onb'),intro:getComputedStyle(document.getElementById('intro')).display,hub:getComputedStyle(document.getElementById('homeHub')).display,sh:document.documentElement.scrollWidth})")
        ok(t+'«Inizia la timeline» funziona: onboarding chiuso, home hub visibile, intro assente',r['j'] and r['onb'] and not r['cls'] and r['intro']=='none' and r['hub']!='none' and r['sh']<=W+1,r)
        # refresh e accesso successivo
        pg.reload(); pg.wait_for_timeout(1500)
        r=pg.evaluate("()=>({intro:getComputedStyle(document.getElementById('intro')).display,onb:document.getElementById('onboardingScreen').hidden,cls:document.documentElement.className.includes('tva-onb')})"); ok(t+'dopo refresh: solo introduzione, nessun residuo di stato',r['intro']!='none' and r['onb'] and not r['cls'],r)
        pg.evaluate("()=>document.getElementById('journeyStartBtn').click()"); pg.wait_for_timeout(2300); v=vis(pg); ok(t+'accesso successivo: unica schermata',not v['bad'] and v['intro']=='none',v)
        pg.evaluate("()=>document.getElementById('onboardingStartBtn').click()"); pg.wait_for_timeout(500)
        ok(t+'accesso successivo: entra nella home',pg.evaluate("()=>journeyStarted.checked&&getComputedStyle(document.getElementById('homeHub')).display!=='none'"))
        ok(t+'nessun errore JS',errs==[],errs[:2]); ctx.close()
    # reduced motion
    ctx=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,reduced_motion='reduce',service_workers='block'); pg=ctx.new_page(); pg.goto(U); pg.wait_for_timeout(1200)
    pg.evaluate("()=>document.getElementById('journeyStartBtn').click()"); pg.wait_for_timeout(600); v=vis(pg); ok('reduced-motion: unica schermata',not v['bad'] and v['intro']=='none',v)
    # quiz d'ingresso / skip: stessa funzione
    b.close()
done()
