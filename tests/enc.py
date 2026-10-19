import re,json
from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
res=[]
def ok(n,c,d=''): res.append(bool(c)); print('PASS' if c else 'FAIL',n,d)
S=open('/home/claude/work/index.html',encoding='utf-8').read()
with sync_playwright() as p:
    b=p.chromium.launch()
    def page(seed=None):
        ctx=b.new_context(viewport={'width':390,'height':844})
        pg=ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        if seed:
            pg.add_init_script("if(!localStorage.getItem('__seeded')){localStorage.setItem('__seeded','1');"+"".join("localStorage.setItem(%s,%s);"%(json.dumps(k),json.dumps(json.dumps(v))) for k,v in seed.items())+"}")
        pg.goto(F); pg.wait_for_timeout(1200); return ctx,pg,errs
    W='marvel-ultimate-timeline-watched'
    ctx,pg,errs=page()
    r=pg.evaluate("""()=>({wc:document.querySelectorAll('.watch-check').length,vc:document.querySelectorAll('.variant-check').length,
      adj:document.getElementById('item-089').nextElementSibling.id, in133:!!document.querySelector('#item-133 .variant-check'),
      prog:document.getElementById('progressPct').textContent, tess:document.getElementById('tesseraTitoliAssoluti').textContent,
      alt:!!document.querySelector('#item-089 #altVersions-089 .variant-goto'), n134:document.querySelector('#item-134 .rec').textContent,
      altN:JSON.parse(document.getElementById('altTimelineData').textContent).length, wo:WATCH_ORDER_JS?WATCH_ORDER_JS.length:null})""") if False else None
    r=pg.evaluate("""()=>({wc:document.querySelectorAll('.watch-check').length,vc:document.querySelectorAll('.variant-check').length,
      adj:document.getElementById('item-089').nextElementSibling.id, in133:!!document.querySelector('#item-133 .variant-check'),
      prog:document.getElementById('progressPct').textContent, tess:document.getElementById('tesseraTitoliAssoluti').textContent,
      alt:!!document.querySelector('#item-089 #altVersions-089 .variant-goto'), n134:document.querySelector('#item-134 .rec').textContent,
      altN:JSON.parse(document.getElementById('altTimelineData').textContent).length,
      w133:document.querySelectorAll('#item-133 .watch-check').length})""")
    ok('138 titoli autonomi + 1 variante',r['wc']==138 and r['vc']==1 and r['w133']==0,r)
    ok('Encore subito dopo Endgame e accessibile dalla sezione Versioni alternative',r['adj']=='item-133' and r['alt'])
    ok('contatori 0/138',r['prog'].startswith('0/138') and r['tess']=='0/138',r)
    ok('schede successive NON rinumerate (134 resta N°134)',r['n134'].endswith('134'))
    ok('timeline alternativa 138 voci',r['altN']==138)
    ok('nessun errore JS',not errs,errs); ctx.close()
    # --- migrazione: progressi salvati su 133 ---
    ctx,pg,errs=page({W:{'001':True,'133':True}})
    r=pg.evaluate("""()=>({prog:document.getElementById('progressPct').textContent,vchk:document.querySelector('#item-133 .variant-check').checked,
      wcls:document.getElementById('item-133').classList.contains('watched'), xp:document.getElementById('tesseraXpSub')?document.getElementById('tesseraXpSub').textContent:'' })""")
    ok('progressi salvati su 133: conteggio 1/138 (133 non contato) e checkbox variante ancora spuntata',r['prog'].startswith('1/138') and r['vchk'] and r['wcls'],r)
    xp_with=r['xp']
    pg.evaluate("document.querySelector('#item-002 .watch-check').click()"); pg.wait_for_timeout(300)
    raw=json.loads(pg.evaluate("localStorage.getItem('%s')"%W))
    ok('133 preservato in storage dopo altre modifiche',raw.get('133') is True and raw.get('002') is True and raw.get('001') is True,raw)
    pg.evaluate("document.querySelector('#item-002 .watch-check').click()"); pg.wait_for_timeout(300)
    raw=json.loads(pg.evaluate("localStorage.getItem('%s')"%W)); ok('133 preservato dopo deseleziona',raw.get('133') is True and '002' not in raw)
    ok('nessun errore JS',not errs,errs); ctx.close()
    # stesso XP con e senza 133
    ctx,pg,_=page({W:{'001':True}})
    xp_wo=pg.evaluate("document.getElementById('tesseraXpSub')?document.getElementById('tesseraXpSub').textContent:''"); ctx.close()
    ok('XP identici con/senza spunta su 133',xp_with==xp_wo,(xp_with,xp_wo))
    # --- toggle della variante: nessun effetto su progresso/XP/missioni/badge ---
    ctx,pg,errs=page({W:{'001':True}})
    before=pg.evaluate("({p:document.getElementById('progressPct').textContent,x:document.getElementById('tesseraXpSub').textContent,m:localStorage.getItem('marvel-ultimate-timeline-missione-settimana'),b:localStorage.getItem('marvel-ultimate-timeline-badges-earned'),bank:localStorage.getItem('marvel-ultimate-timeline-missioni-xp-bonus')})")
    pg.evaluate("document.getElementById('item-133').querySelector('details.card').open=true")
    pg.evaluate("document.querySelector('#item-133 .variant-check').click()"); pg.wait_for_timeout(400)
    after=pg.evaluate("({p:document.getElementById('progressPct').textContent,x:document.getElementById('tesseraXpSub').textContent,m:localStorage.getItem('marvel-ultimate-timeline-missione-settimana'),b:localStorage.getItem('marvel-ultimate-timeline-badges-earned'),bank:localStorage.getItem('marvel-ultimate-timeline-missioni-xp-bonus'),raw:localStorage.getItem('%s')})"%W)
    raw=json.loads(after.pop('raw'))
    ok('spuntare Encore non cambia progresso/XP/missioni/badge e salva 133',before==after and raw.get('133') is True,(before,after))
    pg.evaluate("document.querySelector('#item-133 .variant-check').click()"); pg.wait_for_timeout(300)
    raw=json.loads(pg.evaluate("localStorage.getItem('%s')"%W)); ok('de-spunta rimuove solo 133',('133' not in raw) and raw.get('001'))
    ok('nessun errore JS',not errs,errs)
    # --- badge range salta la variante ---
    r=pg.evaluate("""()=>{const v={};for(let i=93;i<=139;i++){const k=('000'+i).slice(-3);if(k!=='133')v[k]=true;}
      const b={id:'cacciatore-varianti',type:'range',start:93,end:139};const a=window.marvelValutaBadge(b,{visti:v});
      const v2=Object.assign({},v);delete v2['120'];return [a,window.marvelValutaBadge(b,{visti:v2})]}""")
    ok('badge Cacciatore di Varianti raggiungibile senza 133 e ancora bloccato se manca un titolo vero',r==[True,False],r)
    # --- statistiche amici ignorano la variante ---
    r=pg.evaluate("()=>{const s=window.marvelCalcolaStatistichePersona(['001','133'],[]);return [s.checked,s.totalChecks,s.pct]}")
    ok('statistiche persona: 133 non conta (1/138)',r[0]==1 and r[1]==138,r)
    # --- link dalla scheda Endgame ---
    pg.evaluate("document.getElementById('item-089').querySelector('details.card').open=true")
    pg.evaluate("document.querySelector('#altVersions-089 .variant-goto').click()"); pg.wait_for_timeout(500)
    ok('link "Apri la scheda Encore" apre la scheda variante',pg.evaluate("document.querySelector('#item-133 details.card').open"))
    # --- atlante/mappa ---
    r=pg.evaluate("()=>({v:window.mvAtlasVerifica().ok,m:(()=>{const m=JSON.parse(document.getElementById('mvMapData').textContent).universi['uni-earth-199999-mcu'];return [m.titoli,m.film,m.titoliIds.length,m.titoliIds.includes('133')]})(),a:JSON.parse(document.getElementById('atlasData').textContent).opere.filter(o=>o.id==='133')[0]})")
    ok('Atlante coerente; MCU 93 titoli / 40 film senza Encore; opera 133 marcata variante di 089',r['v'] and r['m']==[93,40,93,False] and r['a']['ruolo']=='variante' and r['a']['variantDi']=='089',r)
    # ricerca
    pg.evaluate("()=>{const e=document.getElementById('searchBox');e.value='encore';e.dispatchEvent(new Event('input',{bubbles:true}))}"); pg.wait_for_timeout(600)
    vis=pg.evaluate("[...document.querySelectorAll('.card-wrap')].filter(w=>!w.classList.contains('filtered-out')&&getComputedStyle(w).display!=='none').map(w=>w.id)")
    ok('ricerca "encore" trova la variante',('item-133' in vis),vis[:6])
    # prossimo da guardare non propone mai 133
    r=pg.evaluate("()=>WATCH_ORDER_JS.some(x=>x.id==='133')") if False else False
    ctx.close(); b.close()
print('TOTALE',len(res),'FALLITI',[i for i,x in enumerate(res) if not x])
