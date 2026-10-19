import json
from playwright.sync_api import sync_playwright
BASE='file:///home/claude/work/index.baseline.html'; NEW='file:///home/claude/work/index.html'
W='marvel-ultimate-timeline-watched'; B='marvel-ultimate-timeline-badges-earned'; BANK='marvel-ultimate-timeline-missioni-xp-bonus'
res=[]
def ok(n,c,x=''): res.append((n,bool(c))); print('PASS' if c else 'FAIL',n,x)
START="()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true;const h=document.getElementById('homeHub');if(h)h.style.display='none'}"
NEW4=['016','097','108','121']
def run(b,url,seed,pre=None):
    ctx=b.new_context(viewport={'width':390,'height':844}); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url); pg.evaluate("(s)=>{localStorage.clear();for(const k in s)localStorage.setItem(k,s[k])}",seed); pg.reload(); pg.wait_for_timeout(1500); pg.evaluate(START); pg.wait_for_timeout(300)
    return ctx,pg,errs
def info(pg):
    return pg.evaluate("""()=>({xp:(document.getElementById('tesseraXpTotale')||{}).textContent,
      badges:document.getElementById('badgesCount').textContent,
      ess:[...document.getElementById('badge-essenziale').classList],
      rank:(document.getElementById('tesseraRank')||{}).textContent,
      store:localStorage.getItem('marvel-ultimate-timeline-badges-earned'),
      watched:localStorage.getItem('marvel-ultimate-timeline-watched')})""")
with sync_playwright() as p:
    b=p.chromium.launch()
    # ids verdi
    ctx,pg,_=run(b,NEW,{})
    verdi=pg.evaluate("()=>[...document.querySelectorAll('.card-wrap[data-tag=verde]')].map(e=>e.dataset.item)"); ctx.close()
    old45=[i for i in verdi if i not in NEW4]; ok('45 vecchi verdi',len(old45)==45,len(old45))
    seedA={W:json.dumps({i:True for i in old45})}
    # baseline: chi aveva Essenziale
    cb,pb,_=run(b,BASE,seedA); ib=info(pb); cb.close()
    ok('baseline: Essenziale sbloccato prima',('badge-unlocked' in ib['ess']),str(ib['ess']))
    # nuova versione
    cn,pn,errs=run(b,NEW,seedA); inn=info(pn)
    ok('nuova: Essenziale resta sbloccato (storico)', 'badge-unlocked' in inn['ess'] and 'badge-storico' in inn['ess'],str(inn['ess']))
    ok('nuova: conteggio badge = baseline',inn['badges']==ib['badges'],f"{ib['badges']} vs {inn['badges']}")
    ok('nuova: XP identici a baseline',inn['xp']==ib['xp'],f"{ib['xp']} vs {inn['xp']}")
    ok('nuova: rango identico',inn['rank']==ib['rank'])
    ok('storico salvato contiene essenziale','essenziale' in json.loads(inn['store']))
    ok('progressi salvati invariati',json.loads(inn['watched'])==json.loads(seedA[W]))
    # prossimo titolo: ora punta a una delle 4 nuove (requisito attuale)
    nx=pn.evaluate("()=>document.getElementById('nextWatchCard').textContent"); print('  next:',nx[:80])
    # chip detail
    pn.evaluate("()=>document.getElementById('badge-essenziale').click()"); pn.wait_for_timeout(100)
    ok('dettaglio chip indica storico','storico' in pn.evaluate("()=>document.getElementById('badgesHint').textContent"))
    # reload persistenza
    pn.reload(); pn.wait_for_timeout(1500); pn.evaluate(START); i2=info(pn)
    ok('dopo reload ancora storico',('badge-storico' in i2['ess']) and i2['badges']==inn['badges'])
    # guardo le 4 nuove -> soddisfatto, niente piu' storico
    for i in NEW4: pn.evaluate("(i)=>{const c=document.querySelector('.watch-check[data-item=\"'+i+'\"]');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}",i)
    pn.wait_for_timeout(400); i3=info(pn)
    ok('con 49/49 verdi: unlocked senza storico','badge-unlocked' in i3['ess'] and 'badge-storico' not in i3['ess'],str(i3['ess']))
    # tolgo una verde: resta sbloccato (storico) e conteggio stabile
    pn.evaluate("()=>{const c=document.querySelector('.watch-check[data-item=\"015\"]');c.checked=false;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pn.wait_for_timeout(300); i4=info(pn)
    ok('togliendo una verde il badge resta',('badge-unlocked' in i4['ess']) and ('badge-storico' in i4['ess']))
    # reset spunte azzera
    pn.evaluate("()=>{document.getElementById('resetConfirmOverlay').style.display='flex'}")
    pn.evaluate("()=>{const f=window.__r;}")
    errs_before=len(errs)
    cn.close()
    # utente nuovo: nessun badge essenziale
    c0,p0,e0=run(b,NEW,{}); i0=info(p0); ok('utente nuovo: Essenziale bloccato','badge-locked' in i0['ess'] and i0['badges'].startswith('0/'),i0['badges']); 
    ok('utente nuovo: storico vuoto',json.loads(i0['store'])==[])
    # reset spunte via doReset: simula conferma
    p0.evaluate("(ids)=>{ids.forEach(i=>{const c=document.querySelector('.watch-check[data-item=\"'+i+'\"]');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))})}",verdi[:3]); p0.wait_for_timeout(300)
    ok('primo-passo sbloccato',json.loads(info(p0)['store'])==['primo-passo'] or 'primo-passo' in json.loads(info(p0)['store']))
    # trova e invoca reset: bottoni
    clicked=p0.evaluate("""()=>{const o=document.getElementById('resetConfirmOk2')||document.getElementById('resetConfirmOk');if(!o)return 'noOk';o.click();return 'ok'}"""); p0.wait_for_timeout(500)
    ir=info(p0); print('  reset click:',clicked, ir['badges'], ir['store'])
    ok('reset spunte azzera storico e badge', ir['store'] in (None,'null') or json.loads(ir['store'])==[] or ir['badges'].startswith('0/'),str((ir['badges'],ir['store'])))
    c0.close()
    # missioni gia' completate mantengono premi
    bank={'totale':800,'ricompensate':['2026-W38-settimanale','2026-W38-tematica','road-to-doomsday-v1']}
    seedM={W:json.dumps({i:True for i in verdi[:20]}),BANK:json.dumps(bank),'marvel-ultimate-timeline-stagione-festeggiata':'0','marvel-ultimate-timeline-road-to-doomsday':json.dumps({'completata':True})}
    cm,pm,em=run(b,NEW,seedM)
    bk=pm.evaluate("()=>JSON.parse(localStorage.getItem('"+BANK+"'))")
    ok('banco XP invariato',bk['totale']==800 and bk['ricompensate']==bank['ricompensate'],str(bk))
    ok('Road to Doomsday completata ma senza re-award',pm.evaluate("()=>document.getElementById('roadToDoomsday').classList.contains('rtd-completa')") and pm.evaluate("()=>document.getElementById('missioneCelebrazione').hidden"))
    # chiave bank persa ma flag presente: nessun re-award
    bank2={'totale':800,'ricompensate':['x']}; seedM[BANK]=json.dumps(bank2)
    cm.close(); cm,pm,em=run(b,NEW,seedM)
    ok('flag dedicato: niente ri-assegnazione anche se il registro non ha la chiave',pm.evaluate("()=>JSON.parse(localStorage.getItem('"+BANK+"')).totale")==800)
    # tutte e 16 viste, nessun flag, chiave bank presente (backup vecchio): nessun XP doppio
    ids16=['015','016','041','051','084','089','095','097','099','102','108','112','117','121','123','125']
    seedD={W:json.dumps({i:True for i in ids16}),BANK:json.dumps({'totale':300,'ricompensate':['road-to-doomsday-v1']})}
    cm.close(); cm,pm,em=run(b,NEW,seedD)
    ok('chiave in registro senza flag: XP non raddoppiati',pm.evaluate("()=>JSON.parse(localStorage.getItem('"+BANK+"')).totale")==300 and pm.evaluate("()=>document.getElementById('missioneCelebrazione').hidden"))
    # filtri
    cf,pf,ef=run(b,NEW,{})
    pf.evaluate("()=>document.querySelector('.filter-btn[data-tag=verde]').click()"); pf.wait_for_timeout(300)
    r=pf.evaluate("""()=>{const vis=t=>[...document.querySelectorAll('.card-wrap[data-tag='+t+']')].filter(e=>e.offsetParent!==null).length;return {verde:vis('verde'),blu:vis('blu'),giallo:vis('giallo'),rosso:vis('rosso'),btnOff:document.querySelector('.filter-btn[data-tag=verde]').classList.contains('off')}}""")
    blu=pf.evaluate("()=>document.querySelectorAll('.card-wrap[data-tag=blu]').length")
    ok('filtro: spegnere OBBLIGATORIO nasconde tutte le 49 e lascia le altre',r['verde']==0 and r['blu']==blu and r['btnOff'],str(r))
    pf.evaluate("()=>document.querySelector('.filter-btn[data-tag=verde]').click()"); pf.wait_for_timeout(300)
    r=pf.evaluate("""()=>[...document.querySelectorAll('.card-wrap[data-tag=verde]')].filter(e=>e.offsetParent!==null).length""")
    ok('filtro: riaccendere mostra 49 OBBLIGATORIO',r==49,str(r))
    pf.evaluate("()=>{document.querySelector('.filter-btn[data-tag=blu]').click();document.querySelector('.filter-btn[data-tag=giallo]').click();document.querySelector('.filter-btn[data-tag=rosso]').click()}"); pf.wait_for_timeout(300)
    solo=pf.evaluate("()=>[...document.querySelectorAll('.card-wrap[data-tag]')].filter(e=>e.offsetParent!==null).map(e=>e.dataset.item)")
    ok('solo OBBLIGATORIO: contiene 016,097,108,121',all(i in solo for i in NEW4) and len(solo)==49,str(len(solo)))
    cf.close()
print('FAILED:',[n for n,c in res if not c])
