"""M2 — coerenza dati: anni di uscita, ambientazioni conservate, VisionQuest, id/progressi invariati."""
import re,json
from playwright.sync_api import sync_playwright
NEW=open('/home/claude/work/index.html',encoding='utf-8').read(); OLD=open('/tmp/index.pre_m2.html',encoding='utf-8').read()
res=[]
def ok(n,c,x=''): res.append(bool(c)); print('PASS' if c else 'FAIL',n,x)
J=lambda s,i:json.loads(re.search(r'id="%s">(.*?)</script>'%i,s,re.S).group(1))
alt={'%03d'%x['num']:x for x in J(NEW,'altTimelineData')}; cy=J(NEW,'cmpYearData'); atl=J(NEW,'atlasData'); op={o['id']:o for o in atl['opere']}
ids=lambda s:re.findall(r'<li class="card-wrap" id="item-(\d+)"',s)
ok('1 stessi 138 id scheda nello stesso ordine',ids(NEW)==ids(OLD) and len(ids(NEW))==138)
ok('2 altTimelineData: stessi num/ordine, solo 135 modificato',[(x['num'],x['release']) for x in J(OLD,'altTimelineData') if x['num']!=135]==[(x['num'],x['release']) for x in J(NEW,'altTimelineData') if x['num']!=135])
ok('3 cmpYearData = anno di uscita per tutti i titoli con data',all(cy['item-'+n]==x['release'][:4] for n,x in alt.items() if x['release']))
ok('4 cmpYearData: nessuna chiave persa',set(J(OLD,'cmpYearData'))<=set(cy))
ok('5 atlas.uscita = altTimeline.release per tutti',all(op[n]['uscita']==x['release'] for n,x in alt.items()))
T=['041','042','043','044','045','046','047','059','069','077','078','088','089','090','093','094','100','125']
def card(s,n): return re.search(r'<li class="card-wrap" id="item-%s".*?</li>'%n,s,re.S).group(0)
yr=lambda t:re.search(r'class="yr">(.*?)<',t).group(1)
amb=lambda t:re.sub(r'<[^>]+>','',re.search(r'AMBIENTAZIONE</[^>]+>\s*<[^>]+>(.*?)<',t,re.S).group(1)).strip()
ok('6 anno scheda = anno di uscita (18 schede)',all(yr(card(NEW,n))==alt[n]['release'][:4] for n in T),[ (n,yr(card(NEW,n))) for n in T if yr(card(NEW,n))!=alt[n]['release'][:4]])
ok('7 ambientazione conservata (la vecchia info non e\' persa)',all(amb(card(OLD,n)) in amb(card(NEW,n)) for n in T) and all(re.sub(r'\D','',yr(card(OLD,n)))[:4] in amb(card(NEW,n)) or n not in('059','090') for n in T))
ok('8 atlas coerente con scheda (annoCard=anno, significato=uscita)',all(op[n]['annoCard']==alt[n]['release'][:4] and op[n]['significatoAnnoCard']=='uscita' for n in T))
ok('9 altre schede invariate',all(card(OLD,n)==card(NEW,n) for n in ids(NEW) if n not in T+['135']))
v=card(NEW,'135'); ok('10 VisionQuest: titolo, data 14 ott, ricerca per entrambe le grafie','>VisionQuest<' in v and '14 ott 2026' in v and 'visionquest vision quest' in v and alt['135']['release']=='2026-10-14' and op['135']['uscita']=='2026-10-14')
bo=J(NEW,'bollettinoOTD'); ok('11 Bollettino coerente (10-14)',any(x.get('mmdd')=='10-14' and x['titolo']=='VisionQuest' for x in bo))
ok('12 ordine editoriale/dipendenze invariati',re.search(r'var DEPENDENCY_MAP_JS = .*',NEW).group(0)==re.search(r'var DEPENDENCY_MAP_JS = .*',OLD).group(0) and 'var PREREQ_DIRETTI_JS' in NEW)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8124/index.html'); pg.evaluate("()=>{localStorage.setItem('marvel-ultimate-timeline-watched',JSON.stringify({'135':true,'058':true}));localStorage.setItem('marvel-ultimate-timeline-ratings',JSON.stringify({'058':4.5}));localStorage.setItem('marvelGuideCustomTimelineOrder','[5,2,9]')}"); pg.reload(); pg.wait_for_timeout(1500)
    g=pg.evaluate("()=>[localStorage.getItem('marvel-ultimate-timeline-watched'),localStorage.getItem('marvel-ultimate-timeline-ratings'),localStorage.getItem('marvelGuideCustomTimelineOrder'),document.getElementById('item-135').querySelector('.watch-check').checked,document.getElementById('item-058').querySelector('.watch-check').checked]")
    ok('13 progressi, voti e ordine personalizzato intatti',json.loads(g[0])=={'135':True,'058':True} and json.loads(g[1])=={'058':4.5} and g[2]=='[5,2,9]' and g[3] and g[4],g)
    r=pg.evaluate("()=>{try{if(typeof rtdCostruisciLista==='function')rtdCostruisciLista()}catch(e){};return [...document.querySelectorAll('#rtdList .rtd-item')].map(e=>e.dataset.rtdId+':'+(e.querySelector('.rtd-y')||{}).textContent)}")
    exp={n:alt[n]['release'][:4] for n in ('041','045','059','069','088')}
    got=dict(x.split(':') for x in r if x.split(':')[0] in exp)
    ok('14 Road to Doomsday: anni di uscita (non piu\' ambientazioni)',len(r)>=16 and len(got)>=1 and all(got.get(k)==v for k,v in exp.items() if k in got) and all(re.fullmatch(r'\d{4}|',x.split(':')[1]) for x in r),(len(r),got))
    def pick(inp,q):
        pg.evaluate("(a)=>{const i=document.getElementById(a[0]);i.value=a[1];i.dispatchEvent(new Event('input',{bubbles:true}))}",[inp,q]); pg.wait_for_timeout(400)
        pg.evaluate("(a)=>{const r=[...document.querySelectorAll('#'+a+' .us-result')][0];r&&r.click()}",'cmpResultsA' if inp=='cmpInputA' else 'cmpResultsB'); pg.wait_for_timeout(250)
    pick('cmpInputA','Guardians of the Galaxy Vol. 2'); pick('cmpInputB','Luke Cage S1')
    row=pg.evaluate("()=>[...document.querySelectorAll('.cmp-table tbody tr')].slice(0,4).map(r=>[...r.cells].map(c=>c.textContent))")
    ok('16 Confronto: ANNO DI USCITA corretto (GotG Vol.2=2017, Luke Cage S1=2016) e ambientazione separata',row and row[0]==['ANNO DI USCITA','2017','2016'] and row[3][0]=='AMBIENTAZIONE',row)
    ok('15 nessun errore JS',not errs,errs[:2])
print('TOT',sum(res),'/',len(res))
