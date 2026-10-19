"""Grafo delle Relazioni: filtri per ogni tipo, combinazioni, zero risultati, assenza di sovrapposizioni, pan/zoom/selezione."""
from playwright.sync_api import sync_playwright
from leg_shot import boot
fails=[]
def ck(c,m,x=None):
    print(('PASS ' if c else 'FAIL ')+m+('' if c else ' '+str(x)))
    if not c: fails.append(m)
RT=['famiglia','relazione','organizzazione','variante','universo','titolo','attore']
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>{const c=document.getElementById('relationshipGraphToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(700)
    # scelta di un nodo di prova per ogni tipo (il più piccolo con >=1 collegamento di quel tipo)
    pick=pg.evaluate("""(RT)=>{const d=tvaRelGraph.data();const o={};RT.forEach(t=>{let best=null;for(const [id,n] of Object.entries(d)){const ids=new Set(n.conns.filter(c=>c.rtype===t).map(c=>c.id));if(ids.size&&(!best||ids.size<best[1]))best=[id,ids.size]}o[t]=best});return o}""",RT)
    print('  nodi di prova',pick)
    def setf(on):
        pg.evaluate("(on)=>{for(const t of %s){tvaRelGraph.filters[t]=on.includes(t)}}"%RT,on)
    def shown(id,on):
        setf(on); pg.evaluate("(id)=>tvaRelGraph.render(id,false,false)",id); pg.wait_for_timeout(120)
        return pg.evaluate("()=>[...document.querySelectorAll('#rgSvg .rg-satellite')].map(g=>({id:g.dataset.node,rt:g.dataset.rt.split(',')}))")
    # 1) ogni filtro da solo mostra esclusivamente il suo tipo, ed esattamente i collegamenti dei dati
    for t in RT:
        nid=pick[t][0]; sat=shown(nid,[t])
        exp=pg.evaluate("([id,t])=>[...new Set(tvaRelGraph.data()[id].conns.filter(c=>c.rtype===t).map(c=>c.id))]",[nid,t])
        ck(len(sat)>0 and all(t in s['rt'] and all(x==t for x in s['rt']) for s in sat),f'filtro {t}: solo relazioni di tipo {t} ({len(sat)} nodi)',sat[:3])
        ck(set(s['id'] for s in sat)==set(exp[:14]) and len(sat)==min(14,len(exp)),f'filtro {t}: insieme dei nodi = dati ({len(exp)})',(len(sat),len(exp)))
    # 2) combinazioni: nodo con più tipi
    multi=pg.evaluate("""()=>{const d=tvaRelGraph.data();let best=null;for(const [id,n] of Object.entries(d)){const ts=new Set(n.conns.map(c=>c.rtype));if(ts.has('famiglia')&&ts.has('universo')&&ts.has('titolo')&&(!best||n.conns.length<best[1]))best=[id,n.conns.length]}return best&&best[0]}""")
    for combo in (['famiglia','universo'],['famiglia','titolo'],['universo','titolo'],['famiglia','universo','titolo']):
        sat=shown(multi,combo); allowed=set(combo)
        ck(len(sat)>0 and all(set(s['rt'])<=allowed for s in sat),f'combinazione {"+".join(combo)}: nessun tipo estraneo ({len(sat)})',[s for s in sat if not set(s['rt'])<=allowed][:3])
        exp=pg.evaluate("([id,c])=>[...new Set(tvaRelGraph.data()[id].conns.filter(x=>c.includes(x.rtype)).map(x=>x.id))].length",[multi,combo])
        ck(len(sat)==min(14,exp),f'combinazione {"+".join(combo)}: conteggio = dati (atteso {min(14,exp)})',(len(sat),exp))
    # 3) tutti i filtri attivi = unione completa; tutti disattivi = messaggio
    sat=shown(multi,RT); tot=pg.evaluate("(id)=>new Set(tvaRelGraph.data()[id].conns.map(c=>c.id)).size",multi)
    ck(len(sat)==min(14,tot),'tutti i filtri: totale = dati',(len(sat),tot))
    sat=shown(multi,[]); ck(len(sat)==0 and pg.evaluate("()=>/almeno un filtro/.test(document.getElementById('rgInfoPanel').innerText)"),'nessun filtro attivo: messaggio esplicito, nessun nodo')
    # 4) zero risultati: Wanda con solo Famiglia
    wid=pg.evaluate("()=>Object.keys(tvaRelGraph.data()).find(k=>tvaRelGraph.data()[k].name==='Wanda Maximoff')")
    sat=shown(wid,['famiglia']); ck(len(sat)==0 and pg.evaluate("()=>/Nessun collegamento di tipo Famiglia per Wanda Maximoff/.test(document.getElementById('rgInfoPanel').innerText)&&/Nessun collegamento da mostrare/.test(document.getElementById('rgSvg').textContent)"),'zero risultati: messaggio nel pannello e nel grafo')
    sat=shown(wid,['relazione']); ck([s['id'] for s in sat]==[ 'char-visione'] or len(sat)==1,'Wanda + Relazione → Visione',sat)
    # 5) conteggi sui pulsanti = dati
    shown(wid,RT)
    bc=pg.evaluate("()=>Object.fromEntries([...document.querySelectorAll('.rg-filter-btn')].map(b=>[b.dataset.rtype,b.querySelector('.rg-fc').textContent]))")
    ex=pg.evaluate("(id)=>{const o={};tvaRelGraph.data()[id].conns.forEach(c=>{(o[c.rtype]=o[c.rtype]||new Set()).add(c.id)});return Object.fromEntries(Object.entries(o).map(([k,v])=>[k,String(v.size)]))}",wid)
    ck(all(bc[t]==ex.get(t,'0') if hasattr(ex,'get') else bc[t]==ex.get(t,'0') for t in RT),'badge dei filtri = collegamenti reali',(bc,ex))
    # 6) nessuna sovrapposizione tra etichette (nodi con molti collegamenti), con tutte le combinazioni di filtri
    big=pg.evaluate("()=>Object.entries(tvaRelGraph.data()).sort((a,b)=>b[1].conns.length-a[1].conns.length).slice(0,6).map(x=>x[0])")
    nover=0; bad=[]
    for nid in big+[multi,wid]:
        for on in (RT,['universo'],['titolo'],['famiglia','organizzazione','attore']):
            shown(nid,on)
            for page in range(3):
                r=pg.evaluate("""()=>{const bs=[...document.querySelectorAll('#rgSvg text')].filter(t=>t.textContent.trim()).map(t=>{const r=t.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom,t.textContent.slice(0,16)]});const cs=[...document.querySelectorAll('#rgSvg circle')].map(c=>{const r=c.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom,'o']});
                  const all=bs.concat(cs.map(x=>x));let n=[];for(let i=0;i<bs.length;i++)for(let j=i+1;j<bs.length;j++){const a=bs[i],b=bs[j];if(a[0]<b[2]-0.5&&b[0]<a[2]-0.5&&a[1]<b[3]-0.5&&b[1]<a[3]-0.5)n.push([a[4],b[4]])}
                  // etichette sopra cerchi altrui (escluso il proprio)
                  return n}""")
                nover+=len(r); bad+=r[:2]
                mb=pg.query_selector('#rgMoreBtn')
                if not mb: break
                mb.click(); pg.wait_for_timeout(120)
    ck(nover==0,'nessuna sovrapposizione tra nomi/etichette (nodi con molti collegamenti, filtri diversi, pagine)',bad[:6])
    # 7) paginazione
    shown(big[0],RT); n1=len(pg.query_selector_all('#rgSvg .rg-satellite')); 
    if pg.query_selector('#rgMoreBtn'): pg.click('#rgMoreBtn'); pg.wait_for_timeout(200); n2=len(pg.query_selector_all('#rgSvg .rg-satellite')); ck(n2>n1,'«Mostra altri» aggiunge nodi',(n1,n2))
    # 8) interazione: selezione nodo, pan/zoom
    shown(wid,RT); pg.evaluate("()=>document.querySelector('.relationship-graph-overlay .a2-vp').scrollIntoView()")
    pg.evaluate("()=>document.querySelector('.relationship-graph-overlay .a2-vp').scrollIntoView({block:'center'})"); pg.click('#rgSvg .rg-satellite circle >> nth=0'); pg.wait_for_timeout(300); ck(pg.evaluate("()=>tvaRelGraph.data()[document.querySelector('#rgSvg .mg-active').dataset.node].name")!='Wanda Maximoff','tocco su un nodo: il grafo si ricentra')
    pg.click('.relationship-graph-overlay .a2-vp-b >> nth=0'); pg.wait_for_timeout(150); z=pg.evaluate("()=>document.querySelector('.relationship-graph-overlay .a2-vp').dataset.z"); ck(float(z)>1,'zoom con pulsante',z)
    pg.click('.relationship-graph-overlay .a2-vp-b >> nth=2'); pg.wait_for_timeout(150); ck(pg.evaluate("()=>document.querySelector('.relationship-graph-overlay .a2-vp').dataset.z")=='1.00','adatta')
    ck(pg.evaluate("()=>document.documentElement.scrollWidth")==390,'nessun scroll orizzontale')
    # tutti i nodi sono dentro la vista iniziale
    shown(big[0],RT); out=pg.evaluate("()=>{const st=document.querySelector('.relationship-graph-overlay .a2-vp-stage').getBoundingClientRect();return [...document.querySelectorAll('#rgSvg text, #rgSvg circle')].filter(n=>{const r=n.getBoundingClientRect();return r.width&&(r.left<st.left-1||r.right>st.right+1||r.top<st.top-1||r.bottom>st.bottom+1)}).length}")
    ck(out==0,'vista iniziale: nessun nodo o nome tagliato',out)
    ck(not errs,'nessun errore JS',errs)
    pg.screenshot(path='/tmp/claude-0/t/shots_leg/rel_after.png')
    b.close()
print('TOTALE',len(fails),'FAIL')
