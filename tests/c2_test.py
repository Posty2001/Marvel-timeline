# C2: coerenza modalita' Timeline / ordine personalizzato / backup (build c26). Server su 127.0.0.1:8124 (cartella work).
import json,tempfile,re
from playwright.sync_api import sync_playwright
U='http://127.0.0.1:8124/index.html'
K='marvelGuideCustomTimelineOrder'; M='marvelGuideActiveTimelineMode'; PM='marvel-ultimate-timeline-preferred-mode'; W='marvel-ultimate-timeline-watched'
fails=[]
def ck(c,m,i=''):
    print(('PASS ' if c else 'FAIL ')+m,'' if c else i)
    if not c: fails.append(m)
with sync_playwright() as p:
    b=p.chromium.launch(); cx=b.new_context(viewport={'width':390,'height':844},accept_downloads=True,service_workers='block'); pg=cx.new_page()
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.on('dialog',lambda d:d.accept())
    def boot():
        pg.goto(U); pg.wait_for_timeout(1000)
        pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(400)
    ls=lambda k:pg.evaluate("(k)=>localStorage.getItem(k)",k)
    setls=lambda k,v:pg.evaluate("([k,v])=>localStorage.setItem(k,v)",[k,v])
    boot()
    ck('Content-Security-Policy' in pg.content(),'CSP presente nel documento')
    # 1 export
    setls(K,json.dumps([5,3,1,2])); setls(M,'custom'); setls(PM,'cronologico'); setls(W,json.dumps({'001':True}))
    with pg.expect_download() as d: pg.evaluate("()=>exportBtn.click()")
    data=json.load(open(d.value.path()))
    ck(data.get('customOrder')==[5,3,1,2],'export: customOrder presente',data.get('customOrder'))
    ck(data.get('preferredMode')=='cronologico','export: preferredMode presente (compatibilita\')',data.get('preferredMode'))
    ck(M not in json.dumps(data) and 'ActiveTimelineMode' not in json.dumps(data),'export: modalita\' attiva NON esportata')
    # 2 cambio modalita' da UI + ricarica
    def open_alt():
        pg.evaluate("()=>{const c=document.getElementById('altTimelineToggle'); if(!c.checked){c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}}"); pg.wait_for_timeout(500)
    def active():
        return pg.evaluate("()=>{const b=document.querySelector('#atModes .at-mode-btn.at-mode-active');return b&&b.dataset.mode}")
    def click_mode(m):
        pg.evaluate("(m)=>document.querySelector('#atModes .at-mode-btn[data-mode=\"'+m+'\"]').click()",m); pg.wait_for_timeout(300)
    open_alt(); ck(active()=='custom','riapertura: modalita\' custom salvata con ordine -> Personalizzato',active())
    click_mode('release'); ck(ls(M)=='standard','mode release -> chiave standard',ls(M))
    click_mode('custom'); ck(ls(M)=='custom','mode custom -> chiave custom',ls(M))
    boot(); open_alt(); ck(active()=='custom','ricarica: resta Personalizzato',active())
    ck(ls(K)==json.dumps([5,3,1,2]),'ricarica: ordine intatto',ls(K))
    # 3 modalita' custom ma ordine vuoto -> consigliato (come la Home)
    setls(K,'[]'); setls(M,'custom'); boot(); open_alt()
    ck(active()=='recommended','custom + ordine vuoto: riapre su Consigliato',active())
    pg.evaluate("()=>window.marvelUpdateHomeHub&&window.marvelUpdateHomeHub()")
    nh=pg.evaluate("()=>{const n=window.marvelHomeNext;return n&&(n.id||n.num||JSON.stringify(n).slice(0,40))}")
    ck(nh is not None,'Home next con ordine vuoto: titolo standard calcolato',nh)
    # 4 import
    def imp(obj):
        f=tempfile.NamedTemporaryFile('w',suffix='.json',delete=False); json.dump(obj,f); f.close()
        pg.set_input_files('#importFile',f.name); pg.wait_for_timeout(1500)
    setls(K,json.dumps([9,8])); setls(M,'custom')
    old=dict(data); old.pop('customOrder'); old.pop('preferredMode')
    boot(); imp(old)
    ck(ls(M)=='custom','import backup vecchio: modalita\' locale intatta',ls(M))
    ck(ls(K)==json.dumps([9,8]),'import backup vecchio senza customOrder: ordine locale intatto',ls(K))
    boot(); imp(data)
    ck(json.loads(ls(K) or 'null')==[5,3,1,2],'import completo: ordine ripristinato',ls(K))
    ck(ls(PM)=='cronologico','import completo: preferredMode ripristinato',ls(PM))
    ck(ls(M)=='custom','import completo: modalita\' locale intatta',ls(M))
    v=dict(data); v['customOrder']=[]; boot(); imp(v); boot(); open_alt()
    ck(ls(K) in (None,'[]'),'import ordine vuoto: ordine azzerato',ls(K))
    ck(active()=='recommended','import ordine vuoto + mode custom: Consigliato',active())
    for lab,val in (('duplicato',[1,1]),('fuori range',[0,5]),('stringa',['3']),('oggetto',{'a':1})):
        setls(K,json.dumps([7,6])); v=dict(data); v['customOrder']=val; boot(); imp(v)
        ck(ls(K)==json.dumps([7,6]),'import invalido '+lab+': nulla scritto',ls(K))
    # 5 reset progresso: ordine e modalita' restano
    setls(K,json.dumps([4,2])); setls(M,'custom'); boot()
    pg.evaluate("()=>{resetBtn.click()}"); pg.wait_for_timeout(200); pg.evaluate("()=>{resetConfirmOk.click()}"); pg.wait_for_timeout(200); pg.evaluate("()=>{resetConfirmOk2.click()}"); pg.wait_for_timeout(500)
    ck(ls(K)==json.dumps([4,2]) and ls(M)=='custom','reset progresso: ordine e modalita\' intatti',(ls(K),ls(M)))
    # 6 reset totale: ordine e modalita' rimossi, auto-backup creato
    boot(); pg.evaluate("()=>{resetAllBtn.click()}"); pg.wait_for_timeout(200); pg.evaluate("()=>resetAllConfirmContinue.click()"); pg.wait_for_timeout(200)
    pg.evaluate("()=>{const i=resetAllConfirmInput;i.value='CANCELLA';i.dispatchEvent(new Event('input',{bubbles:true}))}"); pg.wait_for_timeout(100)
    with pg.expect_navigation(timeout=8000): pg.evaluate("()=>resetAllConfirmOk.click()")
    pg.wait_for_timeout(1200)
    ck(ls(K) is None,'reset totale: ordine rimosso',ls(K))
    ck(ls(M) is None,'reset totale: modalita\' attiva rimossa',ls(M))
    ab=pg.evaluate("()=>Object.keys(localStorage).filter(k=>/auto|backup/i.test(k))")
    ck(len(ab)>0,'reset totale: copia di sicurezza automatica creata',ab)
    ab_txt=pg.evaluate("(k)=>localStorage.getItem(k)",ab[0]) if ab else ''
    ck('[4, 2]' in ab_txt or '[4,2]' in ab_txt,'copia di sicurezza contiene l\'ordine personalizzato')
    ck(not errs,'nessun errore JS',errs[:2])
    b.close()
print('PASS/FAIL', 'FAILS',len(fails),fails)
