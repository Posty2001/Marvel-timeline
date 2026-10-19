from leg_shot import *
fails=[]
def ck(c,m,x=None):
    print(('PASS ' if c else 'FAIL ')+m+('' if c else ' '+str(x)))
    if not c: fails.append(m)
A="tvaAtlas2.ext.api.nav"
EXP={'tree-ff':dict(n=5,marr=1,sib=1,cont='MCU'),'tree-asgard':dict(n=5,marr=1,sib=3,adopt=1),'tree-wakanda':dict(n=6,marr=1,partner=1,sib=1),'tree-stark':dict(n=5,marr=2)}
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    for t,e in EXP.items():
        pg.evaluate("()=>"+A+"('alberi',{eid:'%s'})"%t); pg.wait_for_timeout(600)
        r=pg.evaluate("""()=>{const s=document.querySelector('.ft-svg');if(!s)return null;const q=c=>s.querySelectorAll(c).length;return {n:q('.ft-node'),marr:q('.ft-marr')/2,adopt:q('.ft-adopt'),sib:q('.ft-sib'),partner:q('.ft-partner'),par:q('.ft-par'),sw:document.documentElement.scrollWidth,chips:[...document.querySelectorAll('.a2-ft-cont *')].map(x=>x.textContent).join('|'),gens:s.querySelectorAll('.ft-genl').length}}""")
        ck(r is not None,f'{t}: diagramma presente')
        if not r: continue
        for k in ('n','marr','sib','adopt','partner'):
            if k in e: ck(r[k]==e[k],f'{t}: {k}={e[k]}',r)
        ck(r['par']>0,f'{t}: linee genitore→figlio',r); ck(r['sw']==390,f'{t}: nessuno scroll orizzontale',r['sw']); ck(r['gens']>=2,f'{t}: generazioni etichettate',r)
        ck(not pg.query_selector('.a2-ft-det[open]'),f'{t}: dettagli per persona chiusi a diagramma ok')
    # tap su persona apre il dossier
    pg.evaluate("()=>"+A+"('alberi',{eid:'tree-ff'})"); pg.wait_for_timeout(500)
    pg.evaluate("()=>document.querySelector('.ft-node.ft-link').dispatchEvent(new MouseEvent('click',{bubbles:true}))"); pg.wait_for_timeout(700)
    ck(pg.evaluate("()=>/Fantastici|Reed|Richards|Sue|Storm|Ben|Grimm|Johnny/i.test(document.body.innerText.slice(0,400))"),'tap su persona: apre scheda personaggio')
    # Johnny Storm → char corretto
    pg.evaluate("()=>"+A+"('alberi',{eid:'tree-ff'})"); pg.wait_for_timeout(500)
    ck(pg.evaluate("()=>[...document.querySelectorAll('.ft-node')].some(n=>(n.dataset.char||'')==='char-johnny-storm-human-torch')"),'Johnny Storm collegato a char-johnny-storm-human-torch')
    ck(pg.evaluate("()=>/Earth-828|MCU/.test(document.querySelector('#a2Root, body').innerText)"),'FF: continuità indicata')
    ck(pg.evaluate("()=>/non vengono mescolate/.test(document.body.innerText)"),'continuità separate (nota)')
    # pan/zoom
    pg.evaluate("()=>document.querySelector('.a2-ft .a2-vp').scrollIntoView({block:'center'})")
    pg.click('.a2-ft .a2-vp-b >> nth=0'); pg.wait_for_timeout(150); ck(float(pg.evaluate("()=>document.querySelector('.a2-ft .a2-vp').dataset.z"))>1,'alberi: zoom +')
    pg.click('.a2-ft .a2-vp-b >> nth=2'); pg.wait_for_timeout(150); ck(pg.evaluate("()=>document.querySelector('.a2-ft .a2-vp').dataset.z")=='1.00','alberi: adatta')
    # Arti mistiche
    pg.evaluate("()=>"+A+"('arch',{arc:'mis',eid:null,af:'tutti',aq:'',au:'tutti'})"); pg.wait_for_timeout(600)
    M=pg.evaluate("()=>{const m=tvaAtlas2.arcModel();return {c:m.cat.mis.map(e=>[e.id,e.chars.length,e.arcs.length,e.titles.length,!!e.limited]),g:m.misGaps.map(g=>[g.name,g.ids.length])}}")
    ck([x[0] for x in M['c']]==['mis-stregoneria','mis-magia-oscura','mis-magia-del-caos'],'3 discipline documentate',M)
    ck(M['c'][0][1]>=3 and not M['c'][0][4],'Stregoneria: ≥3 schede, non limitata')
    ck(M['c'][1][4] and M['c'][2][4],'Magia oscura/del caos: flag dati limitati')
    ck(len(M['g'])==3 and all(g[1]==0 for g in M['g']),'3 lacune dichiarate senza schede',M['g'])
    ck(pg.evaluate("()=>/non documentate a sufficienza \\(3\\)/.test(document.body.innerText)"),'box lacune visibile')
    for i,(cid,*_) in enumerate(M['c']):
        pg.evaluate("()=>tvaAtlas2.ext.api.nav('arch',{arc:'mis',eid:null,af:'tutti',aq:'',au:'tutti'})"); pg.wait_for_timeout(400)
        nm=['Stregoneria','Magia oscura','Magia del caos'][i]
        pg.evaluate("(nm)=>{[...document.querySelectorAll('.a2-card,[data-eid]')].find(e=>e.textContent.includes(nm)).click()}",nm); pg.wait_for_timeout(600)
        t=pg.evaluate("()=>document.body.innerText")
        ck('DEFINIZIONE' in t.upper() and 'ARTEFATTI ASSOCIATI' in t.upper(),f'{cid}: sezioni Definizione + Artefatti',t[:200])
    ck(not errs,'nessun errore JS',errs)
    b.close()
print('TOTALE',len(fails),'FAIL')
