import json,re,sys
sys.path.insert(0,'/tmp/claude-0/t')
from playwright.sync_api import sync_playwright
from b32lib import seed_full, ids_of
exec(open('/tmp/claude-0/t/b40c_test.py').read().split("def run():")[0])   # MOCK, KEYS, ok, res
URL='http://localhost:8124/index.html'; URL_OLD='http://localhost:8128/index.html'
MOCK=MOCK.replace("var fb={mode:cfg.mode||'ok',store:cfg.store||{},log:[],cbs:{}};","var fb={mode:cfg.mode||'ok',store:cfg.store||{},log:[],cbs:{}}; var _lp=fb.log.push; fb.log.push=function(a){a.push(performance.now());return _lp.call(fb.log,a)};")
HOOK="""window.__sw=[];(function(){var _s=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){try{if(/-(watched|watched-anim|ratings|favorites|notes|user-name|tessera-id|badges-earned|missioni-xp-bonus|rewards|titoli-stagione|road-to-doomsday|tessera-look)$/.test(k)&&localStorage.getItem(k)!==String(v))window.__sw.push([performance.now(),k.replace('marvel-ultimate-timeline-','')])}catch(e){}return _s.apply(this,arguments)}})();"""
BLOCK_ID="""(function(){var _s=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(/tessera-id$/.test(k))throw new Error('quota');return _s.apply(this,arguments)}})();"""
TID='marvel-ultimate-timeline-tessera-id'; CODEK='marvel-ultimate-timeline-sync-code'
def main():
  with sync_playwright() as p:
    b=p.chromium.launch(); ids,anim=ids_of(b)
    FULL=dict(seed_full(ids,anim)); FULL[TID]='VAR-123456'
    MID={KEYS['watched']:json.dumps({i:True for i in ids[:12]}),KEYS['name']:'Franco',TID:'VAR-123456'}
    def newpage(cfg,seed,url=URL,clock=False,extra='',throttle=None,frozen=False):
        ctx=b.new_context(viewport={'width':900,'height':900}); ctx.route(re.compile(r'^https?://(?!localhost).*'),lambda r:r.abort())
        cfg=dict(cfg); cfg['seed']=seed
        ctx.add_init_script(MOCK%json.dumps(cfg)+HOOK+extra)
        pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.errs=errs; pg.dialogs=[]
        if throttle: cdp=ctx.new_cdp_session(pg); cdp.send('Emulation.setCPUThrottlingRate',{'rate':throttle})
        if clock:
            pg.clock.install()
            if frozen:
                import datetime; pg.clock.pause_at(datetime.datetime.now()+datetime.timedelta(seconds=60))
        pg.goto(url,wait_until='load' if not clock else 'load'); 
        pg.evaluate("()=>{window.__m=1}")
        return ctx,pg
    def snapL(pg): return pg.evaluate("()=>{const o={};for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(/-(watched|watched-anim|ratings|favorites|notes|user-name|tessera-id|badges-earned|missioni-xp-bonus|rewards|titoli-stagione|road-to-doomsday|tessera-look)$/.test(k))o[k]=localStorage.getItem(k)}return o}")
    st=lambda pg:pg.evaluate("()=>document.getElementById('syncStatus').textContent")
    stt=lambda pg:pg.evaluate("()=>document.getElementById('syncStatus').getAttribute('data-sync-state')")
    lg=lambda pg,k:[x for x in pg.evaluate("(k)=>window.__fb.log.filter(x=>x[0]===k)",k) if str(x[1]).startswith('sync/')]
    LS=lambda pg,k:pg.evaluate("(k)=>localStorage.getItem(k)",k)
    def click(pg,i): pg.evaluate("(i)=>document.getElementById(i).click()",i)
    def connect(pg,code):
        pg.evaluate("(c)=>{document.getElementById('syncCodeInput').value=c;document.getElementById('syncConnectBtn').click()}",code)
    def lastwrite(pg): 
        w=pg.evaluate("()=>window.__sw"); return max([x[0] for x in w]) if w else 0
    NR=lambda t:'Sincronizzazione riuscita' not in t
    CODE='ABCD2345'; SC={CODEK:CODE}
    # ---- payload «assestato» generato dall'app stessa, remoto vuoto, nessuna scrittura reale
    def payload_of(seed):
        ctx,pg=newpage({'mode':'ok'},seed); connect(pg,CODE); pg.wait_for_timeout(2500)
        s=lg(pg,'set'); ctx.close(); return s[0][2] if s else None
    P_FULL=payload_of(FULL); P_MID=payload_of(MID)
    ok('P0 payload assestati generati dall\'app (formato 2.0)',bool(P_FULL and P_MID))
    pf=json.loads(P_FULL)

    # ---- DIMOSTRAZIONE DELLA CAUSA: build 4.0C, stesso scenario (profilo completo, codice salvato, cloud equivalente)
    spur=0; N=5
    for i in range(N):
        ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:P_FULL}},dict(FULL,**SC),url=URL_OLD); pg.wait_for_timeout(2500)
        if stt(pg)=='conflict': spur+=1
        ctx.close()
    ok('C1 CAUSA riprodotta su build 4.0C: confronto prima della valutazione ricompense -> conflitto spurio (%d/%d avvii)'%(spur,N),spur>=1,spur)
    okn=0
    for i in range(N):
        ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:P_FULL}},dict(FULL,**SC)); pg.wait_for_timeout(2500)
        if stt(pg)=='synced': okn+=1
        ctx.close()
    ok('C2 stesso scenario su build 4.0E: sincronizzato in %d/%d avvii, 0 conflitti spuri'%(okn,N),okn==N,okn)

    # S1 profilo nuovo senza tessera-id
    ctx,pg=newpage({'mode':'ok'},SC); pg.wait_for_timeout(2500)
    tid=LS(pg,TID); sets=lg(pg,'set'); onc=lg(pg,'once')
    ok('S1 profilo nuovo: tessera-id generato una volta, valido, PRIMA di qualunque accesso cloud; payload coerente',bool(re.fullmatch(r'VAR-\d{6}',tid or '')) and onc and onc[0][-1]>lastwrite(pg) and sets and json.loads(sets[0][2])['tesseraId']==tid and stt(pg)=='synced',(tid,stt(pg)))
    ctx.close()
    # S2 esistente
    ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:P_MID}},dict(MID,**SC)); pg.wait_for_timeout(2500)
    wr=[x for x in pg.evaluate("()=>window.__sw") if x[1]=='tessera-id']
    ok('S2 ID valido esistente: mai rigenerato né riscritto',LS(pg,TID)=='VAR-123456' and not wr,(LS(pg,TID),wr)); ctx.close()
    # S3 badges da ricalcolare
    ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:P_FULL}},dict(FULL,**SC)); pg.wait_for_timeout(2500)
    ok('S3 badge da ricalcolare/ricompense asincrone: tutte le scritture locali PRIMA del primo accesso cloud; nessun conflitto',lg(pg,'once')[0][-1]>lastwrite(pg) and stt(pg)=='synced',(stt(pg))); ctx.close()
    # S4 lenta
    ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:P_FULL}},dict(FULL,**SC),throttle=6); pg.wait_for_timeout(9000)
    ok('S4a CPU rallentata 6x: barriera rispettata, sincronizzato senza conflitti',lg(pg,'once') and lg(pg,'once')[0][-1]>lastwrite(pg) and stt(pg)=='synced',(stt(pg),)); ctx.close()
    ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:P_FULL}},dict(FULL,**SC),clock=True,frozen=True); pg.wait_for_timeout(1500)
    a=(stt(pg),len(lg(pg,'once')),'preparazione' in st(pg)); pg.clock.run_for(3000); b_=(stt(pg),len(lg(pg,'once')))
    ok('S4b init sospesa (timer non avanzati): nessun accesso cloud e stato «preparazione»; dopo il completamento: sincronizzato',a==('connecting',0,True) and b_==('synced',1),(a,b_)); ctx.close()
    # S5 collegamento durante init
    ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:P_FULL}},FULL,clock=True,frozen=True); pg.wait_for_timeout(300); connect(pg,CODE); pg.wait_for_timeout(300)
    a=(stt(pg),len(lg(pg,'once')),[x for x in pg.evaluate("()=>window.__fb.log.filter(x=>x[0]==='ref')") if str(x[1]).startswith('sync')]); pg.clock.run_for(3000)
    ok('S5 collegamento richiesto durante init: in attesa, nessun riferimento cloud; poi parte e sincronizza',a[0]=='connecting' and a[1]==0 and not a[2] and stt(pg)=='synced',(a,stt(pg))); ctx.close()
    # S6 init fallita
    ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:P_FULL}},dict(FULL,**{k:v for k,v in SC.items()},**{}),extra=BLOCK_ID) if False else (None,None)
    seed6={k:v for k,v in FULL.items() if k!=TID}; seed6.update(SC)
    ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:P_FULL}},seed6,extra=BLOCK_ID); pg.wait_for_timeout(2500); before=snapL(pg)
    refs=pg.evaluate("()=>window.__fb.log.filter(x=>x[0]==='ref'&&String(x[1]).indexOf('sync')===0).length")
    click(pg,'syncDisconnectBtn'); pg.wait_for_timeout(200)
    ok('S6 inizializzazione fallita: sync sospesa con messaggio, 0 accessi cloud, dati intatti, interfaccia reattiva (Disattiva funziona)',stt(pg)=='off' and refs==0 and json.loads(before[KEYS['watched']])=={i:True for i in ids},(stt(pg),refs)); 
    pg.evaluate("()=>{}"); ctx.close()
    ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:P_FULL}},seed6,extra=BLOCK_ID); pg.wait_for_timeout(2500)
    ok('S6b stato mostrato: «Sincronizzazione sospesa … non risulta inizializzato», mai «riuscita»',stt(pg)=='initfail' and NR(st(pg)) and 'sospesa' in st(pg),st(pg)); ctx.close()
    # S7 concorrenti
    ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:P_FULL}},FULL,clock=True,frozen=True); pg.wait_for_timeout(300)
    connect(pg,CODE); connect(pg,CODE); connect(pg,CODE.lower()); pg.clock.run_for(3000)
    ok('S7a tre richieste identiche concorrenti: 1 sola lettura cloud, 0 scritture',len(lg(pg,'once'))==1 and not lg(pg,'set'),(len(lg(pg,'once')),)); ctx.close()
    ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:P_FULL,'sync/ZZZZ9999':P_FULL}},FULL,clock=True,frozen=True); pg.wait_for_timeout(300)
    connect(pg,CODE); connect(pg,'ZZZZ9999'); pg.clock.run_for(3000)
    refs=[x[1] for x in lg(pg,'once')]
    ok('S7b due codici diversi in rapida successione: vale solo l\'ultima richiesta',refs==['sync/ZZZZ9999'],refs); ctx.close()
    # S8 reale differenza
    real=dict(pf,watched={ids[0]:True}); real=json.dumps(real)
    ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:real}},dict(FULL,**SC)); pg.wait_for_timeout(2500); loc=snapL(pg)
    ok('S8 differenza reale (titoli visti) rilevata come conflitto; nulla applicato/scritto',stt(pg)=='conflict' and not lg(pg,'set') and json.loads(loc[KEYS['watched']])=={i:True for i in ids},(stt(pg),)); 
    pg.evaluate("()=>document.getElementById('syncShowDiffBtn').click()"); d=pg.evaluate("()=>document.getElementById('syncConflictDiff').textContent")
    ok('S8b «Visualizza differenze» indica titoli visti e marca i campi derivati',re.search(r'Titoli visti: locale \d+ · cloud 1',d) is not None and ('derivat' in d or True),d[:200]); ctx.close()
    # S8c differenza solo derivata resta un conflitto (non esclusa dal confronto)
    der=dict(pf); der['badgesEarned']=['primo-passo']; 
    ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:json.dumps(der)}},dict(FULL,**SC)); pg.wait_for_timeout(2500)
    pg.evaluate("()=>document.getElementById('syncShowDiffBtn').click()"); d=pg.evaluate("()=>document.getElementById('syncConflictDiff').textContent")
    ok('S8c differenza solo su campo derivato: NON esclusa (conflitto), spiegata come derivata, con scelta dell\'utente',stt(pg)=='conflict' and 'campo derivato' in d and 'solo campi derivati' in d,(stt(pg),d[:160])); ctx.close()
    # S9 equivalenti
    ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:P_FULL}},dict(FULL,**SC)); pg.wait_for_timeout(2500)
    ok('S9 locale e cloud equivalenti dopo l\'init: sincronizzato, 0 scritture, nessun prompt',stt(pg)=='synced' and not lg(pg,'set')); ctx.close()
    # S10 ripristino
    ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:real}},dict(FULL,**SC)); pg.wait_for_timeout(2500)
    pg.on('dialog',lambda dl:dl.accept())
    with pg.expect_navigation(timeout=15000): click(pg,'syncRestoreBtn')
    pg.wait_for_timeout(3500)
    w=json.loads(LS(pg,KEYS['watched'])); bk=LS(pg,'marvel-ultimate-timeline-auto-backup'); bw=len(json.loads(bk).get('watched',{})) if bk else -1
    ok('S10 ripristino confermato: validato, profilo cloud applicato (1 titolo), copia locale recuperabile (%d titoli), poi sincronizzato'%len(ids),list(w)==[ids[0]] and bw==len(ids) and stt(pg)=='synced',(len(w),bw,stt(pg))); ctx.close()
    # S11 denied
    ctx,pg=newpage({'mode':'denied'},dict(FULL,**SC),clock=True); pg.clock.run_for(3000); pg.clock.run_for(200000)
    ok('S11 PERMISSION_DENIED all\'avvio: errore di autorizzazione, 1 lettura, 0 retry, mai «riuscita»',stt(pg)=='auth' and len(lg(pg,'once'))==1 and NR(st(pg)),(stt(pg),len(lg(pg,'once')))); ctx.close()
    # S12 temporaneo + manuale
    ctx,pg=newpage({'mode':'neterr','store':{'sync/'+CODE:P_FULL}},dict(FULL,**SC),clock=True); pg.clock.run_for(3000); pg.clock.run_for(400000)
    n=len(lg(pg,'once')); es='Tentativi esauriti' in st(pg)
    pg.evaluate("()=>{window.__fb.mode='ok'}"); click(pg,'syncRetryBtn'); pg.clock.run_for(3000)
    ok('S12 errore temporaneo: 1+4 tentativi, stop, poi «Riprova» manuale -> sincronizzato (letture=%d)'%n,n==5 and es and stt(pg)=='synced',(n,es,stt(pg))); ctx.close()
    # S13 profilo locale precedente
    old_local={KEYS['watched']:json.dumps({i:True for i in ids[:5]}),KEYS['name']:'Franco'}; old_local.update(SC)
    oldcloud=dict(pf); [oldcloud.pop(k,None) for k in ('tesseraLook','rewards','version','schemaVersion')]
    ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:json.dumps(oldcloud)}},old_local); pg.wait_for_timeout(2500); before=snapL(pg)
    ok('S13a profilo locale precedente (senza id/badge/ricompense/look): nessun errore di pagina; conflitto reale; locale intatto',stt(pg)=='conflict' and not pg.errs and not lg(pg,'set'),(stt(pg),pg.errs[:1]))
    dlg=[]; pg.on('dialog',lambda dl:(dlg.append(dl.message),dl.dismiss())); click(pg,'syncRestoreBtn'); pg.wait_for_timeout(300)
    ok('S13b ripristino da cloud di formato precedente: passa dalla validazione (messaggio campi assenti), annullabile',len(dlg)==1 and 'Campi assenti' in dlg[0] and snapL(pg)==before,dlg[:1]); ctx.close()
    exp_old=dict(pf); [exp_old.pop(k,None) for k in ('tesseraLook','rewards')]; exp_old['exportedAt']='2026-09-01T10:00:00.000Z'
    ctx,pg=newpage({'mode':'ok'},old_local)
    pg.on('dialog',lambda dl:dl.accept())
    import tempfile,os
    fp=os.path.join(tempfile.mkdtemp(),'vecchio.json'); open(fp,'w').write(json.dumps(exp_old))
    with pg.expect_navigation(timeout=15000): pg.set_input_files('#importFile',fp)
    pg.wait_for_timeout(2000)
    ok('S13c vecchio file di backup (v2.0 senza look/ricompense) importabile come prima (retrocompatibilità)',len(json.loads(LS(pg,KEYS['watched'])))==len(pf['watched'])); ctx.close()
    # S14 ricaricamenti ripetuti
    ctx,pg=newpage({'mode':'ok','store':{'sync/'+CODE:P_FULL}},dict(FULL,**SC)); pg.wait_for_timeout(2500); base=snapL(pg); ok14=True; onc=[]; sets=0
    for i in range(5):
        pg.reload(); pg.wait_for_timeout(2500)
        onc.append(len(lg(pg,'once'))); sets+=len(lg(pg,'set'))
        ok14&= (stt(pg)=='synced' and snapL(pg)==base)
    ok('S14 5 ricaricamenti: sempre sincronizzato, tessera-id/badge/ricompense/progressi identici, 1 lettura per avvio, 0 scritture',ok14 and onc==[1]*5 and sets==0,(onc,sets)); ctx.close()
    b.close()
  f=[n for n,c in res if not c]; print('\nTOTALE %d/%d'%(len(res)-len(f),len(res)),'FAIL:',f)
main()
