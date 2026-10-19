import json,re
from playwright.sync_api import sync_playwright
F='file:///home/claude/work/backups/N7_finale.html'
res=[]
def ok(n,c,d=''): res.append(bool(c)); print('PASS' if c else 'FAIL',n,d)
S=open('/home/claude/work/backups/N7_finale.html',encoding='utf-8').read()
RTD=['015','016','041','051','084','089','095','097','099','102','108','112','117','121','123','125']
W='marvel-ultimate-timeline-watched'
ok('RTD_IDS invariati (16)',"var RTD_IDS = "+str(RTD).replace('"',"'").replace(' ','') in S and "var RTD_XP = 300;" in S and "var RTD_BANK_KEY = 'road-to-doomsday-v1';" in S)
# i 16 coincidono con la lista Countdown ufficiale (15 titoli, Loki S1+S2)
titoli={i:re.search(r'id="item-%s".*?class="title">(.*?)</span>'%i,S,re.S).group(1) for i in RTD}
print(titoli)
with sync_playwright() as p:
    b=p.chromium.launch()
    def page(seed):
        ctx=b.new_context(viewport={'width':390,'height':844}); pg=ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.add_init_script("if(!localStorage.getItem('__s')){localStorage.setItem('__s','1');"+"".join("localStorage.setItem(%s,%s);"%(json.dumps(k),json.dumps(v)) for k,v in seed.items())+"}")
        pg.goto(F); pg.wait_for_timeout(1300)
        pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=false}"); pg.wait_for_timeout(300)
        return ctx,pg,errs
    ctx,pg,errs=page({})
    ok('missione: 16 righe, 0/16',pg.evaluate("document.querySelectorAll('#rtdList .rtd-item').length")==16 and pg.inner_text('#rtdFrac')=='0/16')
    tiers=pg.evaluate("Object.fromEntries([...document.querySelectorAll('#rtdList .rtd-item')].map(e=>[e.dataset.rtdId,(e.querySelector('.rtd-tier')||{}).textContent]))")
    ok('ogni voce della missione ha un livello (Essenz./Consigl.)',all(tiers[i] in ('ESSENZ.','CONSIGL.') for i in RTD),tiers)
    dep=pg.evaluate("""()=>{const p=document.querySelector('#item-136 .dep-map');return {cats:[...p.querySelectorAll('.dep-map-cat')].map(c=>[c.querySelector('.dep-map-cat-label').textContent.split(' ')[1],[...c.querySelectorAll('.dep-chip')].length]),
       rich:p.querySelectorAll('.dep-chip-rich').length,leg:!!p.querySelector('.dep-map-legend'),src:!!p.querySelector('.dep-map-sources'),
       lk:[...p.querySelectorAll('.dep-chip-lk span')].map(x=>x.title).filter((v,i,a)=>a.indexOf(v)===i).sort(), count:p.querySelector('.dep-map-count').textContent}}""")
    print(dep)
    ok('Doomsday: tre livelli presenti (Essenziali/Consigliati/Facoltativi)',[c[0] for c in dep['cats']]==['ESSENZIALI','CONSIGLIATI','FACOLTATIVI'])
    ok('Doomsday: 23 titoli, tutti con motivo e tipo di legame; legenda e fonti presenti',dep['rich']==23 and dep['count']=='0/23' and dep['leg'] and dep['src'])
    ok('tre tipi di legame distinti presenti',dep['lk']==['Confermato ufficialmente','Ipotesi editoriale','Legame narrativo dimostrabile'],dep['lk'])
    # nessun titolo essenziale solo per ipotesi: nelle ess dirette nessuno con solo 'ipo'
    M=json.loads(re.search(r'var DEPENDENCY_MAP_JS = (\{.*?\});',S,re.S).group(1))['136']
    MOT=json.loads(re.search(r'var DEP_MOTIVI_JS = \{"136": (\{.*?\})\};',S,re.S).group(1))
    ok('nessun Essenziale diretto fondato solo su ipotesi editoriale',all(MOT[i]['lk']!=['ipo'] and 'uff' in MOT[i]['lk'] for i in M['ess']))
    ok('voci "ipo" mai Essenziali/Consigliati senza legame ufficiale',all(('uff' in MOT[i]['lk']) for i in M['ess']+M['cons']))
    ok('Wolverine/Deadpool/Spider-Man rumoreggiati non rendono essenziale nulla (117,099 Consigliati)', '117' in M['cons'] and '099' in M['cons'] and '117' not in M['ess'])
    ok('nessun errore JS',not errs,errs); ctx.close()
    # utente che aveva già completato la missione: nessuna doppia assegnazione
    bank=json.dumps({'totale':300,'ricompensate':['road-to-doomsday-v1']})
    seed={W:json.dumps({i:True for i in RTD}),'marvel-ultimate-timeline-road-to-doomsday':json.dumps({'completata':True,'data':'2026-10-10'}),'marvel-ultimate-timeline-missioni-xp-bonus':bank,'marvel-ultimate-timeline-badges-earned':json.dumps(['primo-passo'])}
    ctx,pg,errs=page(seed)
    after=pg.evaluate("({b:localStorage.getItem('marvel-ultimate-timeline-missioni-xp-bonus'),f:localStorage.getItem('marvel-ultimate-timeline-road-to-doomsday')})")
    ok('missione già completata: banca XP e flag invariati (nessun premio doppio)',json.loads(after['b'])==json.loads(bank) and json.loads(after['f'])['completata'] is True,after)
    ok('missione completata: 16/16',pg.inner_text('#rtdFrac')=='16/16')
    ok('nessun errore JS',not errs,errs); ctx.close()
    # completamento nuovo: +300 una sola volta, anche dopo reload
    seed={W:json.dumps({i:True for i in RTD[:-1]})}
    ctx,pg,errs=page(seed)
    pg.evaluate("document.querySelector('.watch-check[data-item=\"125\"]').click()"); pg.wait_for_timeout(600)
    bk=json.loads(pg.evaluate("localStorage.getItem('marvel-ultimate-timeline-missioni-xp-bonus')"))
    ok('completamento: +300 XP una volta',bk['totale']==300 and bk['ricompensate'].count('road-to-doomsday-v1')==1,bk)
    pg.reload(); pg.wait_for_timeout(1200)
    bk2=json.loads(pg.evaluate("localStorage.getItem('marvel-ultimate-timeline-missioni-xp-bonus')"))
    ok('dopo ricarica nessun secondo premio',bk2==bk,bk2)
    ok('nessun errore JS',not errs,errs); ctx.close()
    # universi: natura
    ctx,pg,errs=page({})
    r=pg.evaluate("""()=>{const a=JSON.parse(document.getElementById('atlasData').textContent);const un=a.universi;
      const cards=[...document.querySelectorAll('li.card-wrap[id^="uni-"]')];
      return {n:un.length,nat:un.filter(u=>u.natura).length,cards:cards.length,rows:cards.filter(c=>[...c.querySelectorAll('.detail-k')].some(k=>k.textContent==='NATURA')).length,
        verify:window.mvAtlasVerifica().ok,zombie:un.find(u=>u.id==='uni-marvel-zombies-verse').natura,mau:un.find(u=>u.id==='uni-marvel-animation-universe-2006-2017').natura,
        x97:un.find(u=>u.id==='uni-x-men-97-verse').natura,yfn:un.find(u=>u.id==='uni-your-friendly-neighborhood-spider-man-verse').natura,wi:un.find(u=>u.id==='uni-rami-di-what-if').natura,
        sv:un.find(u=>u.id==='uni-spider-verse-sony-animato').natura,
        kinds:[...new Set(un.map(u=>u.natura))].sort()}}""")
    print(r)
    ok('27 universi invariati, tutti con natura e riga NATURA nella scheda',r['n']==27 and r['nat']==27 and r['rows']==27,r)
    ok('classificazioni: X-Men 97 autonomo; YFN, Zombies, What If diramazioni; Animation Universe raggruppamento editoriale; Spider-Verse animato autonomo',r['x97']=='autonomo' and r['yfn']=='diramazione' and r['zombie']=='diramazione' and r['wi']=='diramazione' and r['mau']=='raggruppamento' and r['sv']=='autonomo')
    ok('mvAtlasVerifica ancora ok (conteggi derivati da atlasData invariati)',r['verify'])
    pg.evaluate("()=>window.marvelEsploraUniverso('uni-marvel-zombies-verse','Z')"); pg.wait_for_timeout(300)
    ok('nessun errore JS',not errs,errs); ctx.close(); b.close()
print('TOTALE',len(res),'FALLITI',[i for i,x in enumerate(res) if not x])
