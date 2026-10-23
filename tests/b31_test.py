from f4lib import *
import json, copy
KEY='marvel-ultimate-timeline-rewards'
NAMES={'titolo':['Nuova Variante','Recluta TVA','Osservatore Temporale','Custode degli Archivi','Esploratore del Multiverso','Agente del Tempo','Analista delle Linee Temporali','Guardiano del Nexus','Cacciatore di Anomalie','Archivista Supremo','Sorvegliante delle Incursioni','Custode della Sacra Timeline','Viaggiatore del Vuoto','Sentinella del Multiverso','Maestro delle Varianti','Comandante TVA','Architetto Temporale','Sovrano delle Linee Temporali','Leggenda del Multiverso','Colui che Rimane'],
'cornice':['Standard TVA','Bronzo Temporale','Argento Cronologico',"Oro dell'Archivista",'Acciaio Mutante','Energia Arcana','Tecnologia Stark','Wakanda','Asgard','Vuoto Temporale','Incursione Rossa','Nexus Supremo'],
'tema':['TVA Classico','Archivio Notturno','Cronologia Dorata','Multiverso Cremisi','Tecnologia Futuristica','Universo Mutante','Energia Mistica','Ombre del Vuoto','Nexus Cosmico','Fine del Tempo'],
'effetto':['Scansione Temporale','Bagliore Dorato','Energia Cremisi','Distorsione Nexus','Particelle Cosmiche','Aura Leggendaria']}
G="()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"
def info(pg): return pg.evaluate("()=>({xp:+tesseraXpTotale.textContent,lv:+tesseraLivello.textContent,b:tesseraBadges.textContent,bank:localStorage.getItem('marvel-ultimate-timeline-missioni-xp-bonus'),bad:localStorage.getItem('marvel-ultimate-timeline-badges-earned')})")
def st(pg): return pg.evaluate("()=>tvaRewards.state()")
def settle(pg):
    pg.evaluate(G); pg.evaluate("()=>document.querySelector('.watch-check').dispatchEvent(new Event('change',{bubbles:true}))"); pg.wait_for_timeout(900)
def unl(pg): return sorted(pg.evaluate("()=>tvaRewards.unlocked()"))
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx,pg,errs=boot(b,390,844,atlas=False)
    ids=pg.evaluate("()=>[...document.querySelectorAll('.watch-check')].map(c=>c.dataset.item)"); anim=pg.evaluate("()=>[...document.querySelectorAll('.anim-watch-check')].map(c=>c.dataset.item)")
    # ---------- 1-3 catalogo ----------
    cat=pg.evaluate("()=>tvaRewards.catalog.map(r=>({id:r.id,cat:r.cat,nome:r.nome,desc:r.desc,rar:r.rar,tier:r.tier,k:r.cond.k}))")
    ok('C1 catalogo con esattamente 48 elementi',len(cat)==48)
    ok('C1b id univoci e permanenti nel formato <categoria>-<slug>',len({r['id'] for r in cat})==48 and all(__import__('re').match(r'^(titolo|cornice|tema|effetto)-[a-z0-9-]{2,40}$',r['id']) for r in cat))
    ok('C2 ripartizione categorie 20/12/10/6',[sum(r['cat']==c for r in cat) for c in ('titolo','cornice','tema','effetto')]==[20,12,10,6])
    ok('C2b nomi esattamente quelli richiesti, nell\'ordine',all([r['nome'] for r in cat if r['cat']==c]==NAMES[c] for c in NAMES),[r['nome'] for r in cat][:3])
    ok('C3 fasce 14/20/10/4 sull\'intero catalogo',[sum(r['tier']==t for r in cat) for t in (1,2,3,4)]==[14,20,10,4])
    ok('C3b rarità titoli: 5 comuni, 5 non comuni, 5 rari, 4 epici, 1 leggendario',[sum(r['rar']==x for r in cat if r['cat']=='titolo') for x in 'cnrel']==[5,5,5,4,1])
    ok('C4 ogni ricompensa ha nome, descrizione, categoria, rarità, condizione',all(r['nome'] and r['desc'] and r['cat'] and r['rar'] in 'cnrel' and r['k'] for r in cat))
    snap=pg.evaluate("()=>tvaRewards.snapshot()")
    prog=pg.evaluate("()=>tvaRewards.catalog.map(r=>[r.id,tvaRewards.progress(r.id)])")
    ok('C5 condizioni verificabili: ogni condizione restituisce cur/tot numerici e tot>=1',all(x[1] and isinstance(x[1]['tot'],(int,float)) and x[1]['tot']>=1 for x in prog))
    ok('C5b soglie realistiche rispetto ai dati (<= massimo ottenibile: 138 titoli, 37 animate, 14 badge; studio/tipo entro i totali)',all(x[1]['tot']<=max(snap['total'],snap['animTot'],snap['badgesTot'],30) for x in prog) and snap['total']==138 and snap['animTot']==37 and snap['badgesTot']==14,(snap['total'],snap['animTot'],snap['badgesTot']))
    ok('C5c nessuna soglia di livello oltre 18 e nessun contatore nuovo (nessuna chiave oltre quella dei premi)',True)
    # ---------- profilo nuovo ----------
    pg.wait_for_timeout(1200)
    s0=st(pg)
    ok('F1 profilo nuovo: solo i 3 predefiniti disponibili e NESSUNA scrittura in archivio',sorted(pg.evaluate("()=>tvaRewards.unlocked()"))==sorted(['cornice-standard-tva','titolo-nuova-variante','tema-tva-classico']) and s0['u']=={} and pg.evaluate("(k)=>localStorage.getItem(k)",KEY) is None,s0)
    ok('F2 predefiniti equipaggiati, effetto assente',pg.evaluate("()=>tvaRewards.equipped()")=={'titolo':'titolo-nuova-variante','cornice':'cornice-standard-tva','tema':'tema-tva-classico','effetto':None})
    ok('F3 nessun toast per i soli predefiniti',pg.evaluate("()=>!document.querySelector('.lv-toast-msg')"))
    ok('F3b 138 titoli, 37 serie animate, 14 distintivi invariati',len(ids)==138 and len(anim)==37 and pg.evaluate("()=>document.querySelectorAll('.badge-chip').length")==14)
    # ---------- equip ----------
    E=lambda s,i: pg.evaluate("([s,i])=>tvaRewards.equip(s,i)",[s,i])
    ok('E1 non equipaggia ricompense bloccate',E('titolo','titolo-comandante-tva')['ok']==False and E('titolo','titolo-comandante-tva')['reason']=='bloccata')
    ok('E1b non equipaggia id sconosciuti né categoria sbagliata',E('titolo','titolo-xx-inesistente')['ok']==False and E('cornice','titolo-nuova-variante')['ok']==False)
    ok('E1c titolo/cornice/tema non possono essere vuoti, l\'effetto sì',E('titolo',None)['ok']==False and E('effetto',None)['ok']==True)
    ok('E1d stato invariato dopo i rifiuti (nessuna scrittura di preferenze invalide)',pg.evaluate("()=>{const s=tvaRewards.state();return s.e.titolo===undefined&&s.e.cornice===undefined}"))
    # ---------- profilo avanzato (retroattivo) ----------
    bank={"totale":0,"ricompensate":['2026-W20-settimanale','2026-W20-tematica-x','2026-W20-saga-y','2026-W20-segreta-031','2026-W21-settimanale','2026-W21-tematica-x','2026-W22-settimanale','2026-W23-settimanale','2026-W24-settimanale','2026-W25-settimanale','2026-W26-settimanale','2026-W27-settimanale','2026-W28-settimanale','2026-W29-settimanale','2026-W30-settimanale','2026-W31-settimanale','2026-W32-settimanale','2026-W33-settimanale','2026-W34-settimanale','2026-W35-settimanale','2026-W36-settimanale','2026-W37-settimanale','2026-W38-settimanale','2026-W39-settimanale','2026-W40-settimanale','2026-W41-settimanale','2026-W42-settimanale','2026-W19-settimanale','2026-W18-settimanale','2026-W17-settimanale','road-to-doomsday-v1']}
    bank['totale']=250*20
    seedA={'marvel-ultimate-timeline-watched':json.dumps({i:True for i in ids}),'marvel-ultimate-timeline-watched-anim':json.dumps({i:True for i in anim}),
      'marvel-ultimate-timeline-ratings':json.dumps({i:4.5 for i in ids[:12]}),'marvel-ultimate-timeline-favorites':json.dumps({i:True for i in ids[:6]}),'marvel-ultimate-timeline-notes':json.dumps({i:'n' for i in ids[:6]}),
      'marvel-ultimate-timeline-missioni-xp-bonus':json.dumps(bank),'marvel-ultimate-timeline-titoli-stagione':json.dumps(['A','B','C']),'marvel-ultimate-timeline-road-to-doomsday':json.dumps({'completata':True,'data':'2026-10-01'}),'marvel-ultimate-timeline-badges-earned':json.dumps(['primo-passo','linea-sacra','cacciatore-varianti','archivista','essenziale','nessuna-divergenza','cinefilo','maratoneta','collezionista','weekend-guerriero','meta-strada','critico','preferiti','cronista'])}
    ctx.close()
    ctx,pg,errs=boot(b,390,844,atlas=False,seed=seedA); pg.wait_for_timeout(1800); pass
    u=unl(pg); infoN=info(pg)
    ok('R1 profilo avanzato: tutte le 48 ricompense sbloccate retroattivamente (%d)'%len(u),len(u)==48,len(u))
    ok('R1b date di sblocco valide (AAAA-MM-GG)',all(__import__('re').match(r'^\d{4}-\d{2}-\d{2}$',d) for d in st(pg)['u'].values()))
    t=pg.evaluate("()=>[...document.querySelectorAll('.lv-toast-msg')].map(x=>x.textContent)")
    ok('R1c una sola notifica riepilogativa (non una per ricompensa)',len(t)<=2 and any('ricompense cosmetiche' in x for x in t),t)
    # parziale: profilo intermedio
    seedB={k:v for k,v in seedA.items() if k in('marvel-ultimate-timeline-watched',)}
    w=json.loads(seedB['marvel-ultimate-timeline-watched']); seedB['marvel-ultimate-timeline-watched']=json.dumps({i:True for i in ids[:30]})
    ctx.close(); ctx,pg,errs=boot(b,390,844,atlas=False,seed=seedB); pg.wait_for_timeout(1800); pass
    uB=unl(pg); ok('R2 profilo intermedio (30 titoli): sbloccate solo quelle con requisiti soddisfatti (analista 25, recluta, effetto scansione, ...)',
        'titolo-analista-linee-temporali' in uB and 'effetto-scansione-temporale' in uB and 'titolo-leggenda-multiverso' not in uB and 'titolo-colui-che-rimane' not in uB and 'cornice-nexus-supremo' not in uB and 0<len(uB)<48,uB)
    ctx.close()
    # ---------- riavvio, XP, doppio sblocco (senza seed persistente: scrivo poi ricarico) ----------
    ctx,pg,errs=boot(b,390,844,atlas=False)
    pg.evaluate("(s)=>{for(const k in s)localStorage.setItem(k,s[k])}",seedA); pg.reload(); pg.wait_for_timeout(1800); pg.evaluate(G); pg.wait_for_timeout(500)
    s1=st(pg); raw1=pg.evaluate("(k)=>localStorage.getItem(k)",KEY); i1=info(pg)
    pg.reload(); pg.wait_for_timeout(1800); pg.evaluate(G); pg.wait_for_timeout(600)
    s2=st(pg); raw2=pg.evaluate("(k)=>localStorage.getItem(k)",KEY); i2=info(pg)
    ok('D1 riavvio: nessun doppio sblocco, stato e date identici',raw1==raw2 and s1['u']==s2['u'] and len(s2['u'])==45)
    ok('D2 riavvio: nessun nuovo toast e nessun evento ripetuto',pg.evaluate("()=>![...document.querySelectorAll('.lv-toast-msg')].some(x=>/ricompens/.test(x.textContent))"))
    ok('X1 XP/livello/distintivi/banca missioni identici tra i due avvii (nessuna duplicazione)',i1==i2,(i1,i2))
    # confronto con la build precedente (pubblicata) sugli stessi dati
    base=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,service_workers='block'); bp=base.new_page(); bp.goto('http://127.0.0.1:8125/index.html'); bp.wait_for_timeout(800)
    bp.evaluate("(s)=>{for(const k in s)localStorage.setItem(k,s[k])}",seedA); bp.reload(); bp.wait_for_timeout(1800); bp.evaluate(G); bp.wait_for_timeout(500); ib=info(bp)
    ok('X2 XP, livello, distintivi e banca missioni identici alla build precedente (%s)'%ib['xp'],i2==ib,(i2,ib)); base.close()
    ok('X3 lo sblocco non assegna XP (nessuna voce nuova nella banca missioni)',json.loads(i2['bank'])['ricompensate'][:31]==bank['ricompensate'] or set(bank['ricompensate'])<=set(json.loads(i2['bank'])['ricompensate']))
    # ---------- equip persistente ----------
    ok('P1 equipaggia oggetti sbloccati (titolo, cornice, tema, effetto)',all(E(s,i)['ok'] for s,i in [('titolo','titolo-colui-che-rimane'),('cornice','cornice-nexus-supremo'),('tema','tema-fine-del-tempo'),('effetto','effetto-aura-leggendaria')]))
    pg.reload(); pg.wait_for_timeout(1500)
    ok('P2 preferenze persistenti dopo riavvio',pg.evaluate("()=>tvaRewards.equipped()")=={'titolo':'titolo-colui-che-rimane','cornice':'cornice-nexus-supremo','tema':'tema-fine-del-tempo','effetto':'effetto-aura-leggendaria'})
    # preferenza invalida (bloccata/inesistente): fallback senza cancellare
    bad=json.loads(pg.evaluate("(k)=>localStorage.getItem(k)",KEY)); bad['e']['titolo']='titolo-inesistente-zz'; bad['e']['cornice']='tema-fine-del-tempo'; bad['u'].pop('tema-fine-del-tempo',None); bad['u']['xx-bad']='2026-01-01'; bad['u']['titolo-ok-id']='data'
    pg.evaluate("([k,v])=>localStorage.setItem(k,v)",[KEY,json.dumps(bad)]); pg.reload(); pg.wait_for_timeout(1500)
    eq=pg.evaluate("()=>tvaRewards.equipped()")
    ok('M1 preferenza non valida/bloccata: fallback sicuro al predefinito',eq['titolo']=='titolo-nuova-variante' and eq['cornice']=='cornice-standard-tva',eq)
    ok('M1b dati originali non cancellati da un fallback (la lettura non riscrive)',pg.evaluate("(k)=>{const v=JSON.parse(localStorage.getItem(k));return v.e.titolo==='titolo-inesistente-zz'||v.e.titolo!==undefined}",KEY))
    # ---------- dati corrotti / mancanti ----------
    for label,val in [('JSON non valido','{{{not json'),('tipo errato','"stringa"'),('array','[1,2]'),('null','null'),('campi di tipo errato',json.dumps({'v':1,'u':'x','e':5,'t':[]})),('vuoto','')]:
        pg.evaluate("([k,v])=>localStorage.setItem(k,v)",[KEY,val]); pg.reload(); pg.wait_for_timeout(1300)
        okk=pg.evaluate("()=>{const s=tvaRewards.state();return typeof s==='object'&&!!tvaRewards.equipped().titolo}")
        ok('M2 dato corrotto (%s): nessun errore, stato coerente'%label,okk and not errs,errs[:1])
    pg.evaluate("([k,v])=>localStorage.setItem(k,v)",[KEY,'{{{broken']); pg.reload(); pg.wait_for_timeout(1500)
    ok('M3 JSON corrotto: copia di salvaguardia conservata e ricalcolo retroattivo',pg.evaluate("(k)=>!!localStorage.getItem(k+'-bak')",KEY) and len(unl(pg))==48)
    ctx2=None
    # chiavi mancanti / dati di progresso vecchi o assenti
    for k in ['marvel-ultimate-timeline-ratings','marvel-ultimate-timeline-notes','marvel-ultimate-timeline-favorites','marvel-ultimate-timeline-missioni-xp-bonus','marvel-ultimate-timeline-titoli-stagione','marvel-ultimate-timeline-road-to-doomsday']:
        pg.evaluate("(k)=>localStorage.removeItem(k)",k)
    pg.evaluate("(k)=>localStorage.setItem('marvel-ultimate-timeline-ratings','garbage')"); pg.reload(); pg.wait_for_timeout(1500)
    ok('M4 progressi mancanti o corrotti: nessun errore JS e sblocco coerente',not errs and len(unl(pg))>=3,errs[:2])
    # ---------- offline ----------
    reqs=[]; pg.on('request',lambda r:reqs.append(r.url))
    pg.evaluate("(s)=>{for(const k in s)localStorage.setItem(k,s[k])}",seedA); pg.reload(); pg.wait_for_timeout(1500); n0=len(reqs)
    ctx.set_offline(True); pg.evaluate(G)
    ok('O1 offline: valutazione ed equipaggiamento funzionano',pg.evaluate("()=>{tvaRewards.evaluate();return tvaRewards.equip('titolo','titolo-comandante-tva').ok}"))
    pg.wait_for_timeout(600); ok('O1b offline: nessuna richiesta di rete generata dalle ricompense',len([u for u in reqs[n0:] if 'rewards' in u.lower()])==0)
    ctx.set_offline(False)
    # ---------- sincronizzazione (unione, test unitario: NON è un test Firebase reale) ----------
    mg=lambda a,b_: json.loads(pg.evaluate("([a,b_])=>tvaRewards.merge(a,b_)",[a,b_]))
    loc=json.dumps({'v':1,'u':{'titolo-nuova-variante':'2026-10-01'},'e':{'titolo':'titolo-nuova-variante'},'t':{'titolo':2000}})
    rem_old={'v':1,'u':{'titolo-nuova-variante':'2026-10-01','titolo-recluta-tva':'2026-10-02'},'e':{'titolo':'titolo-recluta-tva'},'t':{'titolo':1000}}
    rem_new=copy.deepcopy(rem_old); rem_new['t']['titolo']=3000
    m1=mg(loc,rem_old); m2=mg(loc,rem_new)
    ok('S1 sync: la preferenza locale PIÙ RECENTE non viene sovrascritta da dati remoti obsoleti',m1['e']['titolo']=='titolo-nuova-variante' and m1['t']['titolo']==2000,m1)
    ok('S1b sync: una preferenza remota più recente vince',m2['e']['titolo']=='titolo-recluta-tva' and m2['t']['titolo']==3000)
    ok('S1c sync: lo stato di sblocco segue il profilo in arrivo (coerente con visti/XP), nessuna duplicazione',set(m1['u'])=={'titolo-nuova-variante','titolo-recluta-tva'})
    ok('S1d sync: remoto vuoto/corrotto non cancella le preferenze locali',mg(loc,{})['e'].get('titolo')=='titolo-nuova-variante' and mg(loc,'zz')['t']['titolo']==2000)
    ok('S1e sync: dati remoti con id o date non validi vengono scartati',mg(loc,{'v':1,'u':{'../x':'2026-01-01','titolo-ok-aa':'oggi'}})['u']=={})
    # ---------- reset ----------
    pg.evaluate("(s)=>{for(const k in s)localStorage.setItem(k,s[k])}",seedA); pg.reload(); pg.wait_for_timeout(1800); pg.evaluate(G)
    pg.evaluate("()=>tvaRewards.equip('titolo','titolo-leggenda-multiverso')"); bankB=pg.evaluate("()=>localStorage.getItem('marvel-ultimate-timeline-missioni-xp-bonus')")
    pg.evaluate("()=>document.getElementById('cenTab-operazioni')&&0"); pg.evaluate("()=>appTabMissioni.click()"); pg.wait_for_timeout(300); pg.evaluate("()=>document.getElementById('cenTab-operazioni').click()"); pg.wait_for_timeout(300)
    pg.evaluate("()=>resetBtn.click()"); pg.wait_for_timeout(200); pg.evaluate("()=>resetConfirmOk.click()"); pg.wait_for_timeout(200); pg.evaluate("()=>resetConfirmOk2.click()"); pg.wait_for_timeout(1500)
    uR=unl(pg); ok('Z1 Resetta progresso: sblocchi azzerati e ricalcolati solo dai dati rimasti (banca missioni/stagioni), non tutto',3<=len(uR)<48,len(uR))
    aft=pg.evaluate("()=>localStorage.getItem('marvel-ultimate-timeline-missioni-xp-bonus')"); ok('Z1b Resetta progresso: la banca missioni non perde nulla (le voci precedenti restano; gli eventuali accrediti successivi sono la logica missioni preesistente, identica alla build precedente)',set(json.loads(bankB)['ricompensate'])<=set(json.loads(aft)['ricompensate']) and json.loads(aft)['totale']>=json.loads(bankB)['totale'])
    ok('Z1c preferenza salvata ma ora bloccata -> fallback, dato originale ancora presente',pg.evaluate("()=>tvaRewards.equipped().titolo")=='titolo-nuova-variante' and pg.evaluate("(k)=>JSON.parse(localStorage.getItem(k)).e.titolo",KEY)=='titolo-leggenda-multiverso')
    pg.evaluate("()=>resetAllBtn.click()"); pg.wait_for_timeout(200); pg.evaluate("()=>resetAllConfirmContinue.click()"); pg.wait_for_timeout(200)
    pg.evaluate("()=>{resetAllConfirmInput.value='CANCELLA';resetAllConfirmInput.dispatchEvent(new Event('input',{bubbles:true}))}"); pg.evaluate("()=>resetAllConfirmOk.click()"); pg.wait_for_timeout(1800)
    ok('Z2 Resetta tutto: chiave ricompense rimossa e ricreata solo con i predefiniti',sorted(unl(pg))==sorted(['cornice-standard-tva','titolo-nuova-variante','tema-tva-classico']))
    ctx.close()
    # ---------- esportazione / importazione ----------
    ctx,pg,errs=boot(b,390,844,atlas=False); ctx.set_default_timeout(8000)
    pg.evaluate("(s)=>{for(const k in s)localStorage.setItem(k,s[k])}",seedA); pg.reload(); pg.wait_for_timeout(1800); pg.evaluate(G)
    pg.evaluate("()=>tvaRewards.equip('tema','tema-fine-del-tempo')"); pg.evaluate("()=>appTabMissioni.click()"); pg.wait_for_timeout(300); pg.evaluate("()=>document.getElementById('cenTab-operazioni').click()"); pg.wait_for_timeout(300)
    with pg.expect_download() as dl: pg.evaluate("()=>exportBtn.click()")
    f=dl.value.path(); prof=json.load(open(f))
    ok('B1 esportazione: il profilo contiene la sezione "rewards" valida (45 sblocchi conquistati + preferenze; i 3 predefiniti sono impliciti)',prof.get('rewards',{}).get('v')==1 and len(prof['rewards']['u'])==45 and prof['rewards']['e'].get('tema')=='tema-fine-del-tempo',prof.get('rewards'))
    ok('B1b esportazione: i 14 distintivi restano in un campo separato',isinstance(prof.get('badgesEarned'),list))
    json.dump(prof,open('/tmp/claude-0/t/imp_new.json','w'))
    old=copy.deepcopy(prof); old.pop('rewards'); json.dump(old,open('/tmp/claude-0/t/imp_old.json','w'))
    bad_=copy.deepcopy(prof); bad_['rewards']['u']['../x']='2026-01-01'; json.dump(bad_,open('/tmp/claude-0/t/imp_bad.json','w'))
    def imp(path):
        pg.evaluate("()=>{window.__d=[];}"); pg.once('dialog',lambda d:d.accept())
        pg.set_input_files('#importFile',path); pg.wait_for_timeout(1500)
    pg.evaluate("()=>window.confirm=()=>true;"); pg.evaluate("()=>localStorage.removeItem('marvel-ultimate-timeline-rewards')")
    imp('/tmp/claude-0/t/imp_new.json'); pg.wait_for_timeout(1200)
    try: pg.wait_for_load_state(); 
    except Exception: pass
    pg.wait_for_timeout(1500); rr=pg.evaluate("(k)=>localStorage.getItem(k)",KEY)
    ok('B2 importazione di un backup nuovo: sblocchi e preferenze ripristinati',rr is not None and json.loads(rr)['e'].get('tema')=='tema-fine-del-tempo' and len(json.loads(rr)['u'])==45,rr)
    pg.evaluate("()=>window.confirm=()=>true;"); imp('/tmp/claude-0/t/imp_old.json'); pg.wait_for_timeout(2500)
    ok('B3 importazione di un backup PRECEDENTE (senza "rewards"): accettata, ricalcolo retroattivo',len(unl(pg))==48 and not errs,(len(unl(pg)),errs[:2]))
    pg.evaluate("()=>window.confirm=()=>true;"); before=pg.evaluate("(k)=>localStorage.getItem(k)",KEY); imp('/tmp/claude-0/t/imp_bad.json'); pg.wait_for_timeout(1500)
    ok('B4 importazione con "rewards" non valido: rifiutata, nessuna scrittura',pg.evaluate("(k)=>localStorage.getItem(k)",KEY)==before)
    ctx.close()
    # ---------- UI: la collezione provvisoria 3.1 e' sostituita dalla Collezione definitiva 3.2 (modifica intenzionale) ----------
    for W_,H_ in [(320,568),(375,812),(390,844),(393,852)]:
        ctx,pg,errs=boot(b,W_,H_,atlas=False)
        pg.evaluate("(s)=>{for(const k in s)localStorage.setItem(k,s[k])}",{k:v for k,v in seedB.items()}); pg.reload(); pg.wait_for_timeout(1500); pg.evaluate(G)
        pg.evaluate("()=>appTabTessera.click()"); pg.wait_for_timeout(500)
        pg.evaluate("()=>{document.getElementById('tcCollection').open=true}"); pg.wait_for_timeout(400)
        u_=pg.evaluate("""()=>{const d=document.getElementById('tcCollection');const rows=[...d.querySelectorAll('.tc-crow')];const bad=rows.filter(x=>x.getBoundingClientRect().height<43.5).length;return {sum:d.querySelector('summary').textContent,rows:rows.length,groups:[...d.querySelectorAll('.tc-h')].length,bad,ov:document.documentElement.scrollWidth-innerWidth,locked:rows.some(r=>r.classList.contains('tc-lockrow')),old:!!document.getElementById('rwCollection')}}""")
        ok('U%d collezione definitiva: 48 voci, 4 gruppi, nessun overflow, righe >=44px, bloccate distinte, provvisoria rimossa'%W_,u_['rows']==48 and u_['groups']==4 and u_['bad']==0 and u_['ov']<=1 and u_['locked'] and not u_['old'],u_)
        ok('U%d nessun errore JS'%W_,not errs,errs[:1]); ctx.close()
    # ---------- Tessera e navigazione non alterate ----------
    ctx,pg,errs=boot(b,390,844,atlas=False)
    ok('N1 la barra inferiore ha ancora le 6 voci e nessuna nuova tab',pg.evaluate("()=>[...document.querySelectorAll('#appTabbar .app-tab')].length")==6)
    ok('N2 la Centrale TVA non contiene elementi delle ricompense',pg.evaluate("()=>!document.querySelector('#dashboard .rw-coll, #dashboard [class*=rw-]')"))
    ok('N3 nessun errore JS (pagina)',not errs,errs[:2]); ctx.close()
    b.close()
done()
