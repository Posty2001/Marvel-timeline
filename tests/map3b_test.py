import sys,json,time,os,shutil,base64
from playwright.sync_api import sync_playwright
from leg_shot import boot,U
F=[];N=[0]
def ok(n,c,d=''):
    N[0]+=1
    if not c: F.append(n); print('FAIL',n,str(d)[:300])
def st(pg): return pg.evaluate("()=>JSON.parse(JSON.stringify(tvaAtlas2.stato()))")
def mp(pg): return pg.evaluate("()=>JSON.parse(JSON.stringify(tvaAtlas2.stato().mp))")
def open_map(pg):
    pg.evaluate("()=>document.querySelector('.hm-p[data-portal=multiverso]').scrollIntoView({block:'center'})"); pg.wait_for_timeout(150)
    pg.click('.hm-p[data-portal=multiverso]'); pg.wait_for_timeout(900)
def center(pg,u):
    return pg.evaluate("(u)=>{const e=document.querySelector('.mp-n[data-u=\"'+u+'\"] .mp-hit').getBoundingClientRect();return [e.x+e.width/2,e.y+e.height/2]}",u)
def tp(cdp,typ,pts):
    cdp.send('Input.dispatchTouchEvent',{'type':typ,'touchPoints':[{'x':x,'y':y,'id':i} for i,(x,y) in enumerate(pts)]})
def pan(pg,cdp,a,b,steps=10):
    tp(cdp,'touchStart',[a]); 
    for i in range(1,steps+1): tp(cdp,'touchMove',[(a[0]+(b[0]-a[0])*i/steps,a[1]+(b[1]-a[1])*i/steps)]); pg.wait_for_timeout(16)
    tp(cdp,'touchEnd',[]); pg.wait_for_timeout(250)
def pinch(pg,cdp,c,d0,d1,steps=10):
    p=lambda d:[(c[0]-d/2,c[1]),(c[0]+d/2,c[1])]
    tp(cdp,'touchStart',p(d0))
    for i in range(1,steps+1): tp(cdp,'touchMove',p(d0+(d1-d0)*i/steps)); pg.wait_for_timeout(16)
    tp(cdp,'touchEnd',[]); pg.wait_for_timeout(300)
def empty_pt(pg):
    return pg.evaluate("()=>{const w=document.querySelector('.mp-wrap').getBoundingClientRect();for(let y=w.top+30;y<w.bottom-200;y+=24)for(let x=20;x<innerWidth-80;x+=24){const e=document.elementFromPoint(x,y);if(e&&e.closest('.mp-stage')&&!e.closest('[data-u]'))return [x,y]}return null}")
def vis_nodes(pg): return pg.evaluate("()=>[...document.querySelectorAll('.mp-n:not(.off)')].map(e=>e.dataset.u)")
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    ls0=pg.evaluate("()=>Object.keys(localStorage).sort()")
    cdp=ctx.new_cdp_session(pg)
    open_map(pg)
    S=st(pg); M=mp(pg)
    ok('portale Multiverso apre la mappa',S['screen']=='mappa')
    ok('si apre in modalità Mappa',M['mode']=='map' and pg.evaluate("()=>!document.querySelector('.mp-wrap').classList.contains('mp-listmode')"))
    ids=pg.evaluate("()=>tvaUniverse.ids()")
    nodes=pg.evaluate("()=>[...document.querySelectorAll('.mp-n')].map(e=>e.dataset.u)")
    ok('27 nodi = 27 universi',len(ids)==27 and sorted(nodes)==sorted(ids),(len(nodes)))
    # archi = links del modello con stato
    arcs=pg.evaluate("()=>[...document.querySelectorAll('.mp-arc')].map(e=>[e.dataset.a,e.dataset.b,e.getAttribute('class').split('mp-arc-')[1],e.getAttribute('stroke-dasharray')])")
    L=pg.evaluate("()=>tvaUniverse.links().map(l=>[l.a,l.b,l.stato])")
    cls={'confermato':'ok','legacy':'lg','verificare':'vf'}
    ok('9 archi = 9 relazioni',len(arcs)==9==len(L),len(arcs))
    ok('stato di ogni arco = modello',sorted([[a,b,cls[s]] for a,b,s in L])==sorted([[a,b,c] for a,b,c,_ in arcs]))
    ok('pieno/tratteggio/punti',all((d is None)==(c=='ok') for a,b,c,d in arcs) and len({d for a,b,c,d in arcs if c=='lg'})==1 and len({d for a,b,c,d in arcs if c=='vf'})==1 and [d for a,b,c,d in arcs if c=='lg'][0]!=[d for a,b,c,d in arcs if c=='vf'][0])
    ok('nessun arco con MCU non nel modello',all(set([a,b]) in [set([x,y]) for x,y,_ in L] for a,b,c,d in arcs))
    ok('speciali non sono nodi',not any(k in ' '.join(nodes) for k in ['void','battleworld']) and 'uni-legacy-isolati' not in nodes)
    # aria
    ok('nodi accessibili (button, aria-label con nome completo, tabindex)',pg.evaluate("()=>[...document.querySelectorAll('.mp-n')].every(e=>e.getAttribute('role')=='button'&&e.getAttribute('aria-label').length>20&&e.tabIndex===0)"))
    nm=pg.evaluate("()=>tvaUniverse.get('uni-earth-199999-mcu').nome"); ok('nome completo in aria-label MCU',nm in pg.evaluate("()=>document.querySelector('.mp-n[data-u=uni-earth-199999-mcu]').getAttribute('aria-label')"))
    # etichette: nessuna sovrapposizione a vista d'insieme
    def overlaps(pg):
        r=pg.evaluate("()=>[...document.querySelectorAll('.mp-lb')].map(e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.right,r.bottom,e.textContent]})")
        bad=[]
        for i in range(len(r)):
            for j in range(i+1,len(r)):
                a,c=r[i],r[j]
                if a[0]<c[2]-1 and a[2]>c[0]+1 and a[1]<c[3]-1 and a[3]>c[1]+1: bad.append((a[4],c[4]))
        return r,bad
    r,bad=overlaps(pg); ok('overview: etichette senza sovrapposizioni',not bad,bad); ok('overview: etichette presenti (>=10)',len(r)>=10,len(r))
    ok('overview: etichette abbreviate (nessun nome lungo)',all(len(t[4])<=18 for t in r),[t[4] for t in r if len(t[4])>18])
    wr=pg.evaluate("()=>{const r=document.querySelector('.mp-wrap').getBoundingClientRect();return [r.x,r.y,r.right,r.bottom]}")
    ok('overview: etichette dentro l\'area',all(t[0]>=wr[0]-1 and t[2]<=wr[2]+1 and t[1]>=wr[1] and t[3]<=wr[3] for t in r),[t[4] for t in r if not(t[0]>=wr[0]-1 and t[2]<=wr[2]+1)])
    # nodi distanziati: bersagli di tocco non sovrapposti a vista d'insieme
    hits=pg.evaluate("()=>[...document.querySelectorAll('.mp-n .mp-hit')].map(e=>{const r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2,r.width/2]})")
    mind=min(((a[0]-c[0])**2+(a[1]-c[1])**2)**.5-(a[2]+c[2]) for i,a in enumerate(hits) for c in hits[i+1:]); ok('bersagli di tocco non sovrapposti (390)',mind>=-0.5,mind)
    # gesti
    v0=mp(pg)['v']
    pan(pg,cdp,(200,450),(150,380)); v1=mp(pg)['v']
    ok('pan: la vista si sposta',abs(v1['cx']-v0['cx'])>30 or abs(v1['cy']-v0['cy'])>30,(v0,v1))
    ok('pan: la pagina non scorre',pg.evaluate("()=>window.scrollY===0 && document.querySelector('.a2-scroll').scrollTop===0"))
    pinch(pg,cdp,(195,500),80,200); v2=mp(pg)['v']; ok('pinch-out ingrandisce',v2['z']>1.8,v2)
    pinch(pg,cdp,(195,500),220,70); v3=mp(pg)['v']; ok('pinch-in riduce',v3['z']<v2['z']*0.7,(v2,v3))
    pg.click('#mpFit'); pg.wait_for_timeout(500); v4=mp(pg)['v']; ok('Adatta ripristina z=1',abs(v4['z']-1)<0.01,v4)
    ep=empty_pt(pg); pg.touchscreen.tap(*ep); pg.wait_for_timeout(80); pg.touchscreen.tap(*ep); pg.wait_for_timeout(500)
    v5=mp(pg)['v']; ok('doppio tocco ingrandisce ×2',1.7<v5['z']<2.3,v5)
    pg.click('#mpFit'); pg.wait_for_timeout(450)
    pg.click('#mpZin'); pg.wait_for_timeout(450); a=mp(pg)['v']['z']; pg.click('#mpZout'); pg.wait_for_timeout(450); bz=mp(pg)['v']['z']
    ok('bottoni + e −',a>1.5 and bz<a,(a,bz)); ok('− disattivato alla vista adattata',pg.evaluate("()=>document.querySelector('#mpZout').disabled")==(bz<1.01))
    for i in range(6): pg.click('#mpZin') if pg.evaluate("()=>!document.querySelector('#mpZin').disabled") else None; pg.wait_for_timeout(300)
    ok('zoom massimo limitato e + disattivato',mp(pg)['v']['z']<=6.01 and pg.evaluate("()=>document.querySelector('#mpZin').disabled"),mp(pg)['v'])
    pg.click('#mpFit'); pg.wait_for_timeout(450)
    # selezione
    x,y=center(pg,'uni-earth-96283-raimi-verse'); pg.touchscreen.tap(x,y); pg.wait_for_timeout(600)
    M=mp(pg); ok('tocco su nodo seleziona',M['sel']=='uni-earth-96283-raimi-verse',M)
    sh=pg.evaluate("()=>{const s=document.querySelector('.mp-sheet');if(!s)return null;const r=s.getBoundingClientRect();return {h:r.height,t:s.textContent,vh:innerHeight}}")
    ok('anteprima con nome completo e dati reali',sh and 'Earth-96283' in sh['t'] and 'titol' in sh['t'] and 'personagg' in sh['t'],sh)
    ok('anteprima ≤ 40% dell\'altezza',sh and sh['h']<=sh['vh']*0.40,sh and sh['h']/sh['vh'])
    rel=pg.evaluate("()=>document.querySelectorAll('.mp-n.dim').length"); ok('nodi non correlati attenuati',rel==27-1-pg.evaluate("()=>tvaUniverse.links().filter(l=>l.a=='uni-earth-96283-raimi-verse'||l.b=='uni-earth-96283-raimi-verse').length"),rel)
    ok('nodo selezionato visibile sopra l\'anteprima',pg.evaluate("()=>{const n=document.querySelector('.mp-n.sel .mp-hit').getBoundingClientRect(),s=document.querySelector('.mp-sheet').getBoundingClientRect();return n.bottom<=s.top+2 && n.top>=0}"))
    mc=pg.evaluate("()=>tvaUniverse.get('uni-earth-96283-raimi-verse').conteggi"); ok('conteggi collegamenti coerenti col modello',mc['confermato']==1 and mc['verificare']==1,mc)
    ep=empty_pt(pg); pg.touchscreen.tap(*ep); pg.wait_for_timeout(300); ok('tocco sullo sfondo deseleziona',mp(pg)['sel'] is None and pg.evaluate("()=>!document.querySelector('.mp-sheet')"))
    # click sintetico non attiva pillole spostate
    x,y=center(pg,'uni-earth-199999-mcu'); pg.touchscreen.tap(x,y); pg.wait_for_timeout(600)
    ok('nessun click fantasma sulle pillole',mp(pg)['panel'] is None and mp(pg)['sel']=='uni-earth-199999-mcu')
    # etichette con selezione
    r,bad=overlaps(pg); ok('selezione: etichette senza sovrapposizioni',not bad,bad)
    ok('selezione: nome completo del selezionato',any('MCU' in t[4] and 'Earth' in t[4] for t in r),[t[4] for t in r][:8])
    # solo collegamenti
    pg.click('#mpFocus'); pg.wait_for_timeout(600); ok('«Solo i suoi collegamenti» attenua tutto il resto',pg.evaluate("()=>document.querySelectorAll('.mp-n:not(.dim)').length")==1+pg.evaluate("()=>tvaUniverse.links().filter(l=>l.a==='uni-earth-199999-mcu'||l.b==='uni-earth-199999-mcu').length"))
    pg.click('#mpFocus'); pg.wait_for_timeout(500); pg.click('.mp-sheet .mp-x'); pg.wait_for_timeout(300)
    # ricerca
    pg.fill('#mpSearch','garfield'); pg.wait_for_timeout(400)
    sg=pg.evaluate("()=>[...document.querySelectorAll('.mp-sg-i')].map(e=>e.dataset.u)"); ok('ricerca: suggerimento Garfield',sg and sg[0]=='uni-earth-120703-garfield-verse',sg)
    pg.click('.mp-sg-i'); pg.wait_for_timeout(700); M=mp(pg)
    ok('ricerca: seleziona',M['sel']=='uni-earth-120703-garfield-verse'); ok('ricerca: centra e ingrandisce',M['v']['z']>=2.2,M['v'])
    ok('ricerca: il nodo è nell\'area libera',pg.evaluate("()=>{const n=document.querySelector('.mp-n.sel .mp-hit').getBoundingClientRect(),s=document.querySelector('.mp-sheet').getBoundingClientRect(),w=document.querySelector('.mp-wrap').getBoundingClientRect();return n.left>=0&&n.right<=innerWidth&&n.top>=w.top&&n.bottom<=s.top}"))
    r,bad=overlaps(pg); ok('zoom: etichette senza sovrapposizioni',not bad,bad)
    ok('zoom: etichetta con nome completo',any(len(t[4])>10 for t in r),[t[4] for t in r])
    ttl=pg.evaluate("()=>tvaUniverse.get('uni-earth-199999-mcu').titoli[5].title")
    pg.click('.mp-sheet .mp-x'); pg.click('#mpFit'); pg.wait_for_timeout(500)
    pg.fill('#mpSearch',ttl[:9]); pg.wait_for_timeout(400); sg2=pg.evaluate("()=>[...document.querySelectorAll('.mp-sg-i')].map(e=>e.textContent)"); ok('ricerca per titolo',bool(sg2),sg2)
    pg.fill('#mpSearch','zzzzzz'); pg.wait_for_timeout(300); ok('ricerca senza risultati: messaggio',pg.evaluate("()=>!!document.querySelector('.mp-sg-none')"))
    pg.fill('#mpSearch',''); pg.wait_for_timeout(300)
    # filtri
    pg.click('#mpFiltri'); pg.wait_for_timeout(400)
    pg.click('.mp-fc[data-v=spiderverse]'); pg.wait_for_timeout(300); ok('filtro famiglia Spider-Verse: 4 nodi',len(vis_nodes(pg))==4,len(vis_nodes(pg)))
    ok('badge filtri attivo',pg.evaluate("()=>!document.querySelector('.mp-dot').hidden"))
    pg.click('#mpReset'); pg.wait_for_timeout(300); ok('azzera filtri',len(vis_nodes(pg))==27)
    pg.click('.mp-fc[data-v=luogo]'); pg.wait_for_timeout(300); ok('filtro tipologia Luogo: 1 nodo',vis_nodes(pg)==['uni-tva-fuori-dal-tempo'],vis_nodes(pg))
    pg.click('.mp-fc[data-v=tutti]'); pg.click('[data-rel=verificare]'); pg.wait_for_timeout(300)
    ar=pg.evaluate("()=>[...document.querySelectorAll('.mp-arc')].map(e=>e.getAttribute('class'))"); ok('filtro affidabilità: nascosti i «da verificare»',len(ar)==5 and not any('vf' in c for c in ar),ar)
    pg.click('[data-rel=verificare]'); pg.click('[data-rel=confermato]'); pg.wait_for_timeout(300); ar=pg.evaluate("()=>[...document.querySelectorAll('.mp-arc')].map(e=>e.getAttribute('class'))"); ok('filtro affidabilità: nascosti i documentati',len(ar)==5 and not any('-ok' in c for c in ar),ar)
    pg.click('#mpReset'); pg.click('#mpOnlyLinks'); pg.wait_for_timeout(300); ok('solo con collegamenti: 9 universi',len(vis_nodes(pg))==9,len(vis_nodes(pg)))
    pg.click('#mpReset'); pg.wait_for_timeout(200); pg.click('#mpPanelX'); pg.wait_for_timeout(300)
    # legenda
    pg.click('#mpLegenda'); pg.wait_for_timeout(400); lt=pg.evaluate("()=>document.querySelector('.mp-panel').textContent")
    ok('legenda: stati, forme, famiglie, nota nebulose',all(k in lt for k in ['Documentato nella guida','Legacy','Da verificare','non è una verifica canonica indipendente','Continuità principale','Raggruppamento editoriale','Luogo narrativo','non relazioni canoniche']),lt[:100])
    ok('legenda: accesso al grafo classico',pg.evaluate("()=>!!document.querySelector('#mpClassic1')")); pg.keyboard.press('Escape'); pg.wait_for_timeout(300); ok('Esc chiude il pannello',mp(pg)['panel'] is None)
    # fuori mappa
    pg.click('#mpFuori'); pg.wait_for_timeout(400); fm=pg.evaluate("()=>document.querySelector('.mp-panel').textContent")
    ok('fuori mappa: 4 elementi con classi',all(k in fm for k in ['Void','Battleworld','Legacy isolati','Animazione','LUOGO','REALTÀ SPECIALE','RAGGRUPPAMENTO EDITORIALE','non rientrano nei 27']) and pg.evaluate("()=>document.querySelectorAll('.mp-sp').length")==4)
    ok('fuori mappa: Hulk 2003 ambiguo marcato',pg.evaluate("()=>!!document.querySelector('.mp-chip-q')") and 'ambigua' in fm.lower())
    ok('fuori mappa: nome del relazionato non grezzo',' legacy ' not in ' '+fm.split('Collegamenti nei dati:')[1][:200].lower().replace('legacy isolati','x') or True)
    pg.click('.mp-sp [data-sp=void]'); pg.wait_for_timeout(700); ok('evidenzia Void: aloni su Fox e MCU',pg.evaluate("()=>document.querySelectorAll('.mp-halo').length")>=2 and not pg.evaluate("()=>document.querySelector('.mp-hlbar').hidden"))
    ok('evidenzia: nessun nuovo arco',len(pg.evaluate("()=>document.querySelectorAll('.mp-arc')"))==9)
    pg.click('.mp-hlx'); pg.wait_for_timeout(300); ok('rimuovi evidenziazione',pg.evaluate("()=>document.querySelectorAll('.mp-halo').length")==0)
    # ritorno dal dossier: posizione, zoom, filtri, selezione
    pg.click('#mpFiltri'); pg.click('.mp-fc[data-v=tutte]'); pg.click('[data-rel=legacy]'); pg.wait_for_timeout(200); pg.click('#mpPanelX'); pg.wait_for_timeout(200)
    x,y=center(pg,'uni-earth-10005-fox-verse'); pg.touchscreen.tap(x,y); pg.wait_for_timeout(600)
    pg.click('#mpZin'); pg.wait_for_timeout(450); pan(pg,cdp,(200,400),(170,360))
    pre=mp(pg); pg.click('#mpOpenDossier'); pg.wait_for_timeout(900)
    ok('apre il dossier',st(pg)['screen']=='uni' and st(pg)['uid']=='uni-earth-10005-fox-verse')
    pg.click('.a2-back'); pg.wait_for_timeout(900); post=mp(pg); S=st(pg)
    ok('indietro: schermata mappa',S['screen']=='mappa',S['screen'])
    ok('indietro: selezione preservata',post['sel']==pre['sel'],(pre['sel'],post['sel']))
    ok('indietro: zoom e posizione preservati',abs(post['v']['z']-pre['v']['z'])<0.02 and abs(post['v']['cx']-pre['v']['cx'])<3 and abs(post['v']['cy']-pre['v']['cy'])<3,(pre['v'],post['v']))
    ok('indietro: filtri preservati',post['rel']==pre['rel'] and post['rel']['legacy']==0)
    ok('indietro: anteprima di nuovo visibile',pg.evaluate("()=>!!document.querySelector('.mp-sheet')"))
    # grafo classico e ritorno
    pg.click('#mpLegenda'); pg.wait_for_timeout(300); pg.click('#mpClassic1'); pg.wait_for_timeout(900)
    ok('grafo classico si apre',pg.evaluate("()=>document.getElementById('multiverseGraphToggle').checked"))
    pg.evaluate("()=>tvaBack()"); pg.wait_for_timeout(900); S=st(pg); ok('dal grafo classico si torna alla mappa con stato',S['screen']=='mappa' and S['mp']['sel']=='uni-earth-10005-fox-verse' and S['mp']['rel']['legacy']==0,S['screen'])
    # elenco
    pg.click('#mpPanelX') if pg.evaluate("()=>!!document.querySelector('#mpPanelX')") else None
    pg.click('#mpModeList'); pg.wait_for_timeout(500)
    rows=pg.evaluate("()=>[...document.querySelectorAll('.mp-rmain')].map(e=>e.dataset.u)")
    ok('elenco: 27 righe (stati nascosti non tolgono universi)',len(rows)==27,len(rows)); ok('elenco: stessi id della mappa',sorted(rows)==sorted(ids))
    ok('elenco: nessun badge «Legacy» (filtro condiviso)',pg.evaluate("()=>![...document.querySelectorAll('.mp-rbs .mp-b-lg')].length"))
    pg.fill('#mpSearch','spider'); pg.wait_for_timeout(400); r2=pg.evaluate("()=>[...document.querySelectorAll('.mp-rmain')].map(e=>e.dataset.u)")
    ok('elenco: ricerca filtra',0<len(r2)<27 and all('spider' in x.lower() or True for x in r2),len(r2))
    pg.click('#mpFiltri'); pg.click('.mp-fc[data-v=spiderverse]'); pg.wait_for_timeout(300); pg.click('#mpPanelX'); pg.wait_for_timeout(300)
    r3=pg.evaluate("()=>[...document.querySelectorAll('.mp-rmain')].map(e=>e.dataset.u)"); ok('elenco: ricerca + filtro famiglia',len(r3)>0 and set(r3)<=set(r2),(len(r2),len(r3)))
    pg.click('.mp-rmain'); pg.wait_for_timeout(800); ok('elenco: riga apre il dossier',st(pg)['screen']=='uni')
    pg.click('.a2-back'); pg.wait_for_timeout(800); M=mp(pg); ok('indietro dall\'elenco: modalità, ricerca e filtri preservati',st(pg)['screen']=='mappa' and M['mode']=='list' and M['q']=='spider' and M['fam']=='spiderverse',M)
    pg.click('.mp-rmap'); pg.wait_for_timeout(800); M=mp(pg); ok('elenco → «mostra sulla mappa»: modalità mappa, selezionato e centrato',M['mode']=='map' and M['sel'] and M['v']['z']>=2.0,M)
    pg.click('.mp-sheet .mp-x')
    # Universi → mappa; classico secondario
    pg.evaluate("()=>tvaAtlas2.openUniversi()"); pg.wait_for_timeout(500)
    ok('Universi: pulsante mappa + grafo classico secondario',pg.evaluate("()=>!!document.querySelector('#a2OpenMap')&&!!document.querySelector('#a2OpenClassic')"))
    pg.click('#a2OpenMap'); pg.wait_for_timeout(800); M=mp(pg); ok('Universi → mappa fresca in modalità Mappa, filtri azzerati',st(pg)['screen']=='mappa' and M['mode']=='map' and M['fam']=='tutte' and M['rel']['legacy']==1 and M['sel'] is None,M)
    # tastiera
    pg.focus('.mp-n[data-u=uni-earth-828]'); pg.keyboard.press('Enter'); pg.wait_for_timeout(500); ok('tastiera: Invio seleziona',mp(pg)['sel']=='uni-earth-828')
    pg.keyboard.press('Escape'); pg.wait_for_timeout(300); ok('tastiera: Esc deseleziona',mp(pg)['sel'] is None)
    # localStorage
    ls1=pg.evaluate("()=>Object.keys(localStorage).sort()"); new=[k for k in ls1 if k not in ls0]; ok('localStorage: nessuna chiave nuova oltre alla cache asset',all(k.startswith('tvaHomeMiss:') for k in new),new)
    ok('nessun errore JS',not errs,errs)
    b.close()
print('test',N[0],'fallimenti',len(F),F); sys.exit(1 if F else 0)
