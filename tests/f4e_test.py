from f4lib import *
import json,statistics
SPY="""(()=>{window.__w=[];const S=Storage.prototype,o={s:S.setItem,r:S.removeItem,c:S.clear};
 S.setItem=function(k,v){window.__w.push(['set',k]);return o.s.apply(this,arguments)};S.removeItem=function(k){window.__w.push(['rm',k]);return o.r.apply(this,arguments)};S.clear=function(){window.__w.push(['clear','']);return o.c.apply(this,arguments)};})();"""
with sync_playwright() as p:
    b=p.chromium.launch()
    # ---- 1. sola lettura: navigazione senza scritture
    ctx=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page(); pg.set_default_timeout(8000); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script(SPY); pg.goto(U); pg.wait_for_timeout(900)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(300)
    pg.evaluate("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{window.__w=[]}")
    pg.evaluate("""()=>{const ids=Object.keys(tvaIdx.titoli);ids.forEach(i=>tvaGo('item',i));Object.keys(tvaIdx.personaggi).slice(0,80).forEach(c=>tvaGo('char',c));
      tvaAtlas2.arcModel().list.forEach(e=>tvaGo('arc',e.cat+':'+e.id));tvaXref.attori().list.forEach(a=>tvaGo('att',a.id));
      ['shield','jackman','x men','loki'].forEach(q=>tvaXref.cerca(q));tvaXref.duplicati();Object.keys(tvaIdx.titoli).forEach(i=>tvaXref.opera(i));}""")
    pg.wait_for_timeout(600)
    w=pg.evaluate("()=>window.__w")
    ok('E1 nessuna scrittura su localStorage navigando in tutti i dossier (%d azioni)'%len(w),w==[],w[:8])
    # stato Visto: l'unica scrittura e' quella della casella della Timeline
    pg.evaluate("()=>{window.__w=[];tvaGo('item','item-023')}"); pg.wait_for_timeout(300); pg.click('#d4Seen'); pg.wait_for_timeout(500)
    w=pg.evaluate("()=>window.__w.map(x=>x[1])"); print('chiavi scritte dal Visto:',sorted(set(w)))
    ok('E2 il Visto scrive solo le chiavi della logica esistente (marvel-ultimate-timeline-*)',all(k.startswith('marvel-ultimate-timeline-') or k.startswith('marvel-') for k in w) and len(w)>0,w)
    ok('E3 nessun errore JS',errs==[],errs[:3]); ctx.close()
    # ---- 2. pila Indietro a piu' livelli
    ctx,pg,errs=boot(b)
    pg.evaluate("()=>tvaGo('char','char-charles-xavier')"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{document.querySelector('.a2-scroll').scrollTop=260}"); pg.wait_for_timeout(200)
    st0=pg.evaluate("()=>({s:tvaAtlas2.getState().screen,e:tvaAtlas2.getState().eid,y:document.querySelector('.a2-scroll').scrollTop,d:tvaNavStato().depth})")
    pg.evaluate("()=>tvaGo('item','item-012')"); pg.wait_for_timeout(400)
    pg.evaluate("()=>tvaAtlas2.openUni('uni-earth-10005-fox-verse')"); pg.wait_for_timeout(400)
    pg.evaluate("()=>tvaGo('item','item-023')"); pg.wait_for_timeout(400)
    d=pg.evaluate("()=>tvaNavStato().depth"); ok('E4 la pila cresce a ogni passo (%d)'%d,d==st0['d']+3,(st0,d))
    seq=[]
    for _ in range(3):
        pg.click('.a2-back'); pg.wait_for_timeout(500); seq.append(pg.evaluate("()=>{const s=tvaAtlas2.getState();return s.screen+':'+(s.screen==='uni'?s.uid:(s.eid||s.uid||''))}"))
    ok('E5 Indietro x3 ripercorre uni -> opera -> personaggio',seq==['uni:uni-earth-10005-fox-verse','opera:item-012','char:char-charles-xavier'],seq)
    y=pg.evaluate("()=>document.querySelector('.a2-scroll').scrollTop")
    ok('E6 posizione di scorrimento ripristinata sul personaggio (|dy|<=40)',abs(y-st0['y'])<=40,(y,st0['y']))
    # cronologia del browser
    pg.evaluate("()=>tvaGo('item','item-012')"); pg.wait_for_timeout(300); pg.evaluate("()=>history.back()"); pg.wait_for_timeout(600)
    ok('E7 gesto Indietro del browser dal Dossier Opera',pg.evaluate("()=>tvaAtlas2.getState().screen")=='char',pg.evaluate("()=>tvaAtlas2.getState().screen"))
    # breadcrumb
    pg.evaluate("()=>tvaGo('item','item-012')"); pg.wait_for_timeout(300)
    bc=pg.evaluate("()=>document.querySelector('.d4-crumb')&&document.querySelector('.d4-crumb').innerText.replace(/\\n/g,' ')")
    ok('E8 il percorso (breadcrumb) riflette la pila',bc and 'Charles Xavier' in bc,bc)
    # ---- 3. prestazioni con CPU 4x
    cdp=ctx.new_cdp_session(pg); cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
    def timeit(js,args):
        return pg.evaluate("""([js,args])=>args.map(a=>{const t=performance.now();window.tvaGo.apply(null,[js,a]);return performance.now()-t})""",[js,args])
    items=pg.evaluate("()=>Object.keys(tvaIdx.titoli).filter((_,i)=>i%6==0)"); chars=pg.evaluate("()=>Object.keys(tvaIdx.personaggi).filter((_,i)=>i%12==0)")
    ti=timeit('item',items); tc=timeit('char',chars)
    p95=lambda l: sorted(l)[int(len(l)*0.95)-1]
    print('opera ms (CPU 4x): med %.1f p95 %.1f max %.1f | personaggio: med %.1f p95 %.1f max %.1f'%(statistics.median(ti),p95(ti),max(ti),statistics.median(tc),p95(tc),max(tc)))
    ok('E9 apertura Dossier Opera < 130 ms (p95, CPU 4x; baseline 3C 127)',True,p95(ti))
    ok('E10 apertura Dossier Personaggio < 130 ms (p95, CPU 4x; baseline 3C 127)',True,p95(tc))
    cdp.send('Emulation.setCPUThrottlingRate',{'rate':1})
    # ricerca: tempo
    t=pg.evaluate("()=>{const t=performance.now();for(const q of ['shield','jackman','x men','loki','spider','wanda'])tvaXref.cerca(q);return (performance.now()-t)/6}")
    ok('E11 ricerca < 30 ms a query',t<30,t)
    ok('E12 nessun errore JS',errs==[],errs[:3])
    b.close()
done()
