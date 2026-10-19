from f4lib import *
def home(b,W,H):
    ctx=b.new_context(viewport={'width':W,'height':H},is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page(); pg.set_default_timeout(8000); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(U); pg.wait_for_timeout(1200)
    pg.evaluate("()=>document.getElementById('journeyStartBtn').click()"); pg.wait_for_timeout(2200); pg.evaluate("()=>document.getElementById('onboardingStartBtn').click()"); pg.wait_for_timeout(600)
    return ctx,pg,errs
ST="()=>{const s=tvaAtlas2.getState();return {a2:atlas2Toggle.checked,g:multiverseGraphToggle.checked,screen:s.screen,hub:getComputedStyle(document.getElementById('homeHub')).display,d:tvaNavStato().depth}}"
with sync_playwright() as p:
    b=p.chromium.launch()
    for W,H in [(390,844),(320,568)]:
        t='[%d] '%W
        ctx,pg,errs=home(b,W,H)
        ok(t+'Home: il pulsante non e\' piu\' un collegamento al vecchio grafo',pg.evaluate("()=>{const e=document.getElementById('homeHubMapBtn');return !!e&&e.tagName==='BUTTON'&&!document.querySelector('#homeHub label[for=multiverseGraphToggle]')}"))
        pg.touchscreen.tap(*pg.evaluate("()=>{const r=document.getElementById('homeHubMapBtn').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}")); pg.wait_for_timeout(900)
        s=pg.evaluate(ST); ok(t+'«Esplora il Multiverso» apre la Mappa 3B (non il grafo classico)',s['a2'] and s['screen']=='mappa' and not s['g'],s)
        ok(t+'la mappa e\' disegnata (nodi)',pg.evaluate("()=>document.querySelectorAll('#atlas2 svg g, #atlas2 .mp-node, #atlas2 [data-uid]').length")>10)
        # ritorno
        pg.evaluate("()=>{const b=document.querySelector('.a2-back');b&&b.click()}"); pg.wait_for_timeout(700)
        s=pg.evaluate(ST); print('  dopo Indietro:',s)
        ok(t+'Indietro dalla mappa: torna alla Home (non resta in Atlante)',not s['a2'] and s['hub']!='none',s)
        # mappa -> grafo classico -> ritorno alla mappa
        pg.evaluate("()=>document.getElementById('homeHubMapBtn').click()"); pg.wait_for_timeout(800)
        pg.evaluate("()=>{[...document.querySelectorAll('#atlas2 button')].find(x=>/Legenda/.test(x.textContent)).click()}"); pg.wait_for_timeout(500)
        ok(t+'Mappa: il grafo classico e\' raggiungibile come opzione secondaria',pg.evaluate("()=>!!(document.getElementById('mpClassic1')||document.getElementById('mpClassic2'))"))
        pg.evaluate("()=>(document.getElementById('mpClassic1')||document.getElementById('mpClassic2')).click()"); pg.wait_for_timeout(900)
        s=pg.evaluate(ST); ok(t+'Mappa -> «Apri il grafo classico» apre il grafo classico',s['g'],s)
        ok(t+'grafo classico: titolo e contenuto visibili',pg.evaluate("()=>{const o=document.querySelector('.multiverse-graph-overlay');return getComputedStyle(o).display!=='none'&&o.getBoundingClientRect().height>200&&!!o.querySelector('#mvMapWrap')}"))
        pg.evaluate("()=>{const b=document.getElementById('tvaBackBtn');(b&&b.offsetParent!==null?b:document.querySelector('.a2-back')).click()}"); pg.wait_for_timeout(900)
        s=pg.evaluate(ST); print('  dopo Indietro dal grafo:',s)
        ok(t+'Indietro dal grafo classico: torna alla Mappa di provenienza',(not s['g']) and s['a2'] and s['screen']=='mappa',s)
        pg.evaluate("()=>{const b=document.querySelector('.a2-back');b&&b.click()}"); pg.wait_for_timeout(700)
        # Atlante -> Universi -> Grafo classico
        pg.evaluate("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(600); pg.evaluate("()=>tvaAtlas2.openUniversi()"); pg.wait_for_timeout(600)
        has=pg.evaluate("()=>!!document.getElementById('a2OpenClassic')"); ok(t+'Universi: «Grafo classico» presente',has)
        pg.evaluate("()=>document.getElementById('a2OpenClassic').click()"); pg.wait_for_timeout(900)
        s=pg.evaluate(ST); ok(t+'Universi -> Grafo classico aperto',s['g'],s)
        pg.evaluate("()=>{const b=document.getElementById('tvaBackBtn');(b&&b.offsetParent!==null?b:document.querySelector('.a2-back')).click()}"); pg.wait_for_timeout(900)
        s=pg.evaluate(ST); ok(t+'Indietro: torna agli Universi',(not s['g']) and s['a2'] and s['screen']=='universi',s)
        # guida: card
        pg.evaluate("()=>{atlas2Toggle.checked&&tvaAtlas2.exit&&tvaAtlas2.exit()}"); pg.wait_for_timeout(500)
        ok(t+'Scheda guida: Mappa primaria + Grafo classico secondario',pg.evaluate("()=>!!document.getElementById('guideMapBtn')&&!!document.querySelector('label.mg-open-btn[for=multiverseGraphToggle]')"))
        ok(t+'nessun errore JS',errs==[],errs[:3]); ctx.close()
    b.close()
done()
