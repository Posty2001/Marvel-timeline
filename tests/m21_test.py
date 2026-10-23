"""M2.1 — periodo narrativo, posizione cronologica, ordini e progressi invariati."""
import re,json
from playwright.sync_api import sync_playwright
NEW=open('/home/claude/work/index.html',encoding='utf-8').read(); OLD=open('/tmp/index.pre_m21.html',encoding='utf-8').read()
res=[]
def ok(n,c,x=''): res.append(bool(c)); print('PASS' if c else 'FAIL',n,x)
J=lambda s,i:json.loads(re.search(r'id="%s">(.*?)</script>'%i,s,re.S).group(1))
ids=lambda s:re.findall(r'<li class="card-wrap" id="item-(\d+)"',s)
card=lambda s,n:re.search(r'<li class="card-wrap" id="item-%s".*?</li>'%n,s,re.S).group(0)
AMB=['075','090','093','094','095','097','098','099','100','101','103','104','105','108','109','110','111']
POS=['095','096','093','094','097','098','102','100','101','108','105','103','104','106','107','109','110','111']
on={o['id']:o for o in J(NEW,'atlasData')['opere']}; oo={o['id']:o for o in J(OLD,'atlasData')['opere']}
ok('1 id e ordine schede invariati',ids(NEW)==ids(OLD))
ok('2 altTimeline, cmpYear, dipendenze invariati',J(NEW,'altTimelineData')==J(OLD,'altTimelineData') and J(NEW,'cmpYearData')==J(OLD,'cmpYearData') and re.search(r'var DEPENDENCY_MAP_JS = .*',NEW).group(0)==re.search(r'var DEPENDENCY_MAP_JS = .*',OLD).group(0))
ok('3 atlante: solo ambientazione/posizioneDisney cambiano',all({k:v for k,v in on[n].items() if k not in('ambientazione','posizioneDisney','notaContinuita')}=={k:v for k,v in oo[n].items() if k!='ambientazione'} for n in on))
ok('4 uscita e anno scheda (separati) invariati',all(on[n]['uscita']==oo[n]['uscita'] and on[n]['annoCard']==oo[n]['annoCard'] for n in on))
amb=lambda t:re.sub(r'<[^>]+>','',re.search(r'AMBIENTAZIONE</[^>]+>\s*<[^>]+>(.*?)<',t,re.S).group(1)).replace('&amp;','&').strip()
ok('5 card = atlante per le 17 ambientazioni',all(amb(card(NEW,n))==on[n]['ambientazione'] for n in AMB))
yrs=lambda t:re.findall(r'\b(?:19|20)\d\d\b',t)
ok('6 nessun anno inventato: cifre solo in 100 (2024, indicazione produzione) e 098 (5000 a.C.)',all((not yrs(on[n]['ambientazione'])) or n=='100' for n in AMB) and yrs(on['100']['ambientazione'])==['2024'],[ (n,yrs(on[n]['ambientazione'])) for n in AMB if yrs(on[n]['ambientazione'])])
ok('7 le 8 post-Endgame senza anno non sostenuto',all('anno non ufficiale' in on[n]['ambientazione'] or n=='099' for n in ('097','098','101','103','104','105','108')) and 'anno non ufficiale' in on['099']['ambientazione'])
pos=lambda t:re.search(r'POSIZIONE CRONOLOGICA</span><span class="detail-v">(.*?)<',t)
ok('8 posizione cronologica Disney+ (18 schede, n. coerente con la lista ufficiale)',all(pos(card(NEW,n)) and ('n. %d su 18'%(k+1)) in pos(card(NEW,n)).group(1) and on[n]['posizioneDisney']['n']==k+1 for k,n in enumerate(POS)) and not pos(card(NEW,'099')))
ok('9 altre schede invariate',all(card(NEW,n)==card(OLD,n) for n in ids(NEW) if n not in set(AMB)|set(POS)))
ok('10 Road to Doomsday e liste invariate',re.search(r'var RTD_IDS = .*',NEW).group(0)==re.search(r'var RTD_IDS = .*',OLD).group(0) if 'var RTD_IDS' in NEW else True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://localhost:8124/index.html'); pg.evaluate("()=>{localStorage.setItem('marvel-ultimate-timeline-watched',JSON.stringify({'097':true,'100':true}));localStorage.setItem('marvel-ultimate-timeline-ratings',JSON.stringify({'100':4}));localStorage.setItem('marvelGuideCustomTimelineOrder','[5,2,9]')}"); pg.reload(); pg.wait_for_timeout(1500)
    g=pg.evaluate("()=>[localStorage.getItem('marvel-ultimate-timeline-watched'),localStorage.getItem('marvel-ultimate-timeline-ratings'),localStorage.getItem('marvelGuideCustomTimelineOrder')]")
    ok('11 progressi, voti, ordine personalizzato intatti',json.loads(g[0])=={'097':True,'100':True} and json.loads(g[1])=={'100':4} and g[2]=='[5,2,9]',g)
    y=pg.evaluate("()=>{const U=window.tvaUniverse;return ['100','097','075','110','089'].map(n=>[n,U.annoAmbientazione(U.ambientazione(n)).y])}")
    ok('12 Cronologie: Hawkeye=2024 (produzione), le altre senza anno, Endgame con anno',dict(y).get('100')==2024 and all(dict(y)[k] is None for k in ('097','075','110')) and dict(y)['089'] is not None,y)
    pg.evaluate("()=>tvaAtlas2.ext.api.openChrono&&tvaAtlas2.ext.api.openChrono()"); pg.wait_for_timeout(800)
    ok('13 Cronologie si apre senza errori',not errs,errs[:2])
    # Confronto: ambientazione e posizione separate
    def pick(inp,q,box):
        pg.evaluate("(a)=>{const i=document.getElementById(a[0]);i.value=a[1];i.dispatchEvent(new Event('input',{bubbles:true}))}",[inp,q]); pg.wait_for_timeout(400)
        pg.evaluate("(a)=>{const r=document.querySelector('#'+a+' .us-result');r&&r.click()}",box); pg.wait_for_timeout(250)
    pick('cmpInputA','Shang-Chi','cmpResultsA'); pick('cmpInputB','Hawkeye','cmpResultsB')
    row=pg.evaluate("()=>[...document.querySelectorAll('.cmp-table tbody tr')].slice(0,4).map(r=>[...r.cells].map(c=>c.textContent.slice(0,60)))")
    ok('14 Confronto: ANNO DI USCITA e AMBIENTAZIONE distinti',row[0][1:]==['2021','2021'] and 'post-Endgame' in row[3][1] and 'Natale 2024' in row[3][2],row)
    ok('15 nessun errore JS',not errs,errs[:2])
print('TOT',sum(res),'/',len(res))
