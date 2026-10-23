"""Test integrazione legacy: nessuna esposizione del database classico, schede native, gemme verificate/non confermate, grafici."""
from playwright.sync_api import sync_playwright
from leg_shot import boot
fails=[]
def ck(c,m,x=None):
    print(('PASS ' if c else 'FAIL ')+m+('' if c else ' '+str(x))); 
    if not c: fails.append(m)
S="()=>({a2:atlas2Toggle.checked,classic:tvaArchivesToggle.checked,scr:tvaAtlas2.ext.api.ST.screen,eid:tvaAtlas2.ext.api.ST.eid,sw:document.documentElement.scrollWidth,depth:tvaNavStato().depth})"
def go(pg,fn): pg.evaluate("()=>"+fn); pg.wait_for_timeout(500)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    st=lambda: pg.evaluate(S)
    # --- schede native
    go(pg,"tvaAtlas2.ext.api.nav('personaggi',{pf:'tutti',pq:''})")
    pg.click('#atlas2 .a2-prow >> nth=3'); pg.wait_for_timeout(800); s=st()
    ck(s['scr']=='char' and s['a2'] and not s['classic'],'Personaggi → scheda nativa (non il classico)',s)
    ck(s['sw']==390,'scheda personaggio senza scroll orizzontale',s)
    ck(pg.evaluate("()=>!/archivio classico/i.test(document.getElementById('atlas2').innerText)"),'nessun rimando "archivio classico" nella scheda')
    d0=s['depth']
    ok=pg.evaluate("()=>{const b=document.querySelector('#atlas2 .a2-v .mv-inline-link,#atlas2 .a2-v .tva-chip');if(!b)return false;b.click();return true}"); pg.wait_for_timeout(700)
    if ok:
        s=st(); ck(not s['classic'] and s['a2'],'link correlato resta nell\'Atlante',s)
        pg.evaluate("()=>tvaBack()"); pg.wait_for_timeout(500); s=st(); ck(s['scr']=='char' and s['depth']==d0,'Indietro riporta alla scheda precedente',s)
    # mvNavigateTo (router storico) → moderno
    pg.evaluate("()=>{marvelChiudiOverlay&&0; window.mvNavigateTo && window.mvNavigateTo('char-adam-warlock')}"); pg.wait_for_timeout(700); s=st()
    ck(s['scr']=='char' and not s['classic'],'mvNavigateTo(char) → scheda nativa',s)
    for nm,fn,scr in [('cronologie',"tvaAtlas2.ext.api.nav('chrono',{eid:'chrono-gemme-dell-infinito'})",'chrono'),('alberi',"tvaAtlas2.ext.api.nav('alberi',{eid:'tree-asgard'})",'alberi'),('attori',"tvaAtlas2.ext.api.nav('attori',{eid:null,aq:''})",'attori'),('incursioni',"tvaAtlas2.ext.api.nav('doc',{eid:'inc'})",'doc'),('maratona',"tvaAtlas2.ext.api.nav('doc',{eid:'mar'})",'doc')]:
        go(pg,fn); s=st(); ck(s['scr']==scr and not s['classic'] and s['sw']==390,nm+' nativa, 390px senza scroll orizzontale',s)
        ck(pg.evaluate("()=>document.getElementById('atlas2').innerText.trim().length>150"),nm+' ha contenuto')
    # tutte le cronologie tematiche presenti
    n=pg.evaluate("()=>document.querySelectorAll('#tvaArchivesOverlayEl [id^=chrono-]').length"); go(pg,"tvaAtlas2.ext.api.nav('chrono',{eid:'chrono-gemme-dell-infinito'})")
    tabs=pg.evaluate("()=>document.querySelectorAll('#atlas2 .a2-tabs button,#atlas2 .a2-tabs .a2-chip').length"); ck(tabs>=n>0,'tutte le cronologie tematiche sono raggiungibili (%d/%d)'%(tabs,n))
    na=pg.evaluate("()=>document.querySelectorAll('#tvaArchivesOverlayEl li[id^=att-]').length"); go(pg,"tvaAtlas2.ext.api.nav('attori',{eid:null,aq:''})")
    ck(pg.evaluate("()=>document.querySelectorAll('#atlas2 .a2-prow').length")>=na>0,'tutti gli attori elencati (%d)'%na)
    # attore → ruoli con link ai titoli
    pg.click('#atlas2 .a2-prow >> nth=1'); pg.wait_for_timeout(700); s=st(); ck(s['scr']=='attore' and not s['classic'],'scheda attore nativa',s)
    # --- guardia
    pg.evaluate("()=>{marvelChiudiOverlay();const c=document.getElementById('tvaArchivesToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(600); s=st()
    ck(not s['classic'] and s['a2'],'il toggle classico viene reindirizzato all\'Atlante',s)
    # --- gemme: verificate vs non confermate
    G=pg.evaluate("""()=>{const M=tvaAtlas2.arcModel();const n=id=>id.slice(5);const o={};M.list.filter(e=>/^art-gemma/.test(e.id)||e.id==='art-mjolnir').forEach(e=>o[e.id]={v:e.titles.map(n),u:e.unconf.map(n),why:e.titles.every(t=>!!e.why[t]),dis:e.titles.every(t=>e.unconf.indexOf(t)<0)});return o}""")
    ck(len(G)>=7,'Reliquiario: 6 Gemme + Mjolnir classificati',list(G))
    ck(all(v['why'] and v['dis'] for v in G.values()),'ogni titolo verificato ha la provenienza; nessun titolo è insieme verificato e non confermato')
    mi=G.get('art-gemma-della-mente',{}); ck(set(['051','062','084'])<=set(mi.get('v',[])) and '061' in mi.get('u',[]) and '061' not in mi.get('v',[]),'Gemma della Mente: 051/062/084 verificati, 061 non confermato',mi)
    te=G.get('art-gemma-del-tempo',{}); ck('070' in te.get('v',[]) and '069' in te.get('u',[]) and '069' not in te.get('v',[]),'Gemma del Tempo → Doctor Strange (070) verificato; 069 non confermato',te)
    mj=G.get('art-mjolnir',{}); ck('050' in mj.get('v',[]) and '076' in mj.get('v',[]) and '075' in mj.get('u',[]),'Mjolnir: 050/076 verificati, 075 non confermato',mj)
    go(pg,"tvaAtlas2.openArc('art','art-gemma-del-tempo')")
    ck(pg.evaluate("()=>/non confermat/i.test(document.getElementById('atlas2').innerText)"),'il dossier mostra i riferimenti non confermati separati')
    # --- grafici
    def opent(t):
        pg.evaluate("()=>marvelChiudiOverlay()"); pg.wait_for_timeout(150)
        pg.evaluate("(t)=>{const c=document.getElementById(t);c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}",t); pg.wait_for_timeout(800)
    for t,nm in [('kangTvaGraphToggle','Kang/TVA'),('relationshipGraphToggle','Relazioni'),('multiverseGraphToggle','Multiverso')]:
        opent(t)
        r=pg.evaluate("""()=>{const o=document.querySelector('.kang-tva-overlay,.relationship-graph-overlay,.multiverse-graph-overlay');const ov=[...document.querySelectorAll('.kang-tva-overlay,.relationship-graph-overlay,.multiverse-graph-overlay')].find(x=>x.getClientRects().length);
          return [...ov.querySelectorAll('.a2-vp')].map(v=>{const st=v.querySelector('.a2-vp-stage').getBoundingClientRect(),svg=v.querySelector('svg');const out=[...svg.querySelectorAll('.mg-node circle, .mg-node text')].filter(n=>{const r=n.getBoundingClientRect();return r.width&&(r.left<st.left-1||r.right>st.right+1||r.top<st.top-1||r.bottom>st.bottom+1)}).length;return {z:v.dataset.z,out,w:Math.round(st.width),sw:document.documentElement.scrollWidth}})}""")
        ck(len(r)>=1 and all(x['out']==0 and x['sw']==390 and x['z']=='1.00' for x in r),nm+': vista iniziale intera, centrata, nessun nodo/nome tagliato',r)
    # pan/zoom/tap-vs-drag sul grafo relazioni
    opent('relationshipGraphToggle'); pg.fill('#rgSearchInput','Wanda'); pg.wait_for_timeout(300); pg.click('#rgSearchResults button'); pg.wait_for_timeout(700)
    vb0=pg.evaluate("()=>document.querySelector('#rgSvg').getAttribute('viewBox')")
    pg.evaluate("()=>document.querySelector('.relationship-graph-overlay .a2-vp').scrollIntoView()")
    pg.click('.relationship-graph-overlay .a2-vp-b >> nth=0'); pg.wait_for_timeout(200)
    vb1=pg.evaluate("()=>document.querySelector('#rgSvg').getAttribute('viewBox')"); ck(vb1!=vb0,'zoom + cambia il viewBox',(vb0,vb1))
    pg.evaluate("()=>document.querySelector('.relationship-graph-overlay .a2-vp-stage').scrollIntoView({block:'center',behavior:'instant'})"); pg.wait_for_function("""()=>{const e=document.querySelector('.relationship-graph-overlay .a2-vp-stage');const r=e.getBoundingClientRect(),k=JSON.stringify([r.top,r.left,r.width,r.height]);const ok=window.__stk===k;window.__stk=k;return ok}""",polling=150)  # M1: geometria stabile prima di calcolare il punto di trascinamento
    bx=pg.evaluate("()=>{const r=document.querySelector('.relationship-graph-overlay .a2-vp-stage').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}")
    pg.mouse.move(bx[0],bx[1]); pg.mouse.down(); pg.mouse.move(bx[0]-60,bx[1]-30,steps=6); pg.mouse.up(); pg.wait_for_timeout(200)
    vb2=pg.evaluate("()=>document.querySelector('#rgSvg').getAttribute('viewBox')"); ck(vb2!=vb1,'trascinamento sposta il grafo',(vb1,vb2))
    ck(pg.evaluate("()=>!!document.querySelector('.relationship-graph-overlay')&&relationshipGraphToggle.checked"),'il trascinamento non chiude/naviga')
    pg.click('.relationship-graph-overlay .a2-vp-b >> nth=2'); pg.wait_for_timeout(200)
    ck(pg.evaluate("()=>document.querySelector('.relationship-graph-overlay .a2-vp').dataset.z")=='1.00','pulsante "adatta" ripristina la vista intera')
    # timeline universi: nomi allineati
    opent('universeTimelineToggle'); pg.wait_for_timeout(300)
    d=pg.evaluate("()=>{const r=document.querySelector('.ut-label-row[data-lane=tva]').getBoundingClientRect(),l=document.querySelector('.ut-lane-line[data-lane=tva]').getBoundingClientRect();return Math.abs((r.top+r.height/2)-l.top)}")
    ck(d<1.5,'Timeline Universi: nome riga allineato alla linea (%.1fpx)'%d,d)
    ck(pg.evaluate("()=>document.querySelectorAll('.a2-ut-j').length")>=3,'Timeline Universi: salti rapidi presenti')
    # Back dai grafici torna dove si era (Atlante), mai al classico
    pg.evaluate("()=>tvaBack()"); pg.wait_for_timeout(500); s=st(); ck(not s['classic'],'Back dal grafico non apre il classico',s)
    ck(not errs,'nessun pageerror',errs)
    b.close()
print('TOTALE',len(fails),'FAIL'); 
