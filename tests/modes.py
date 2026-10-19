import json
from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
res=[]
def ok(n,c,d=''): res.append(bool(c)); print('PASS' if c else 'FAIL',n,d)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':320,'height':700}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(F); pg.wait_for_timeout(1000)
    pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true;const t=document.getElementById('altTimelineToggle');t.checked=true;t.dispatchEvent(new Event('change'))}"); pg.wait_for_timeout(500)
    modes=pg.evaluate("[...document.querySelectorAll('#atModes .at-mode-btn')].map(b=>[b.dataset.mode,b.classList.contains('at-mode-active')])")
    ok('modalità: Consigliato (attiva di default), Uscita, Eventi presenti',modes[0]==['recommended',True] and ['release',False] in modes and ['events',False] in modes,modes)
    def rows(): return pg.evaluate("[...document.querySelectorAll('#atList .at-row')].map(r=>+r.dataset.num)")
    rec=rows(); ok('Consigliato = 138 schede uniche nell\'ordine della guida',len(rec)==138 and len(set(rec))==138 and 133 not in rec)
    ids=pg.evaluate("[...document.querySelectorAll('.watch-check')].map(c=>+c.dataset.item)")
    ok('ordine Consigliato = ordine delle schede nella pagina',rec==ids)
    pg.click('.at-mode-btn[data-mode="release"]'); pg.wait_for_timeout(300); rel=rows()
    ok('Uscita: 138 schede senza duplicati',len(rel)==138 and len(set(rel))==138 and set(rel)==set(rec))
    pg.click('.at-mode-btn[data-mode="events"]'); pg.wait_for_timeout(300); ev=rows()
    ok('Eventi: 138 schede senza duplicati (nessuna card duplicata)',len(ev)==138 and len(set(ev))==138 and set(ev)==set(rec))
    heads=pg.evaluate("[...document.querySelectorAll('#atList .at-group-head')].map(h=>h.textContent)")
    print(heads)
    ok('Eventi: MCU è il primo gruppo e le continuità restano separate',heads[0].startswith('Earth-199999') and len(heads)>=20)
    sub=pg.evaluate("Object.fromEntries([...document.querySelectorAll('#atList .at-row')].map(r=>[r.dataset.num,r.querySelector('.at-row-sub').textContent]))")
    pos={n:i for i,n in enumerate(ev)}
    ok('Fox: First Class(12) < DOFP(13) < Apocalypse(14) < Logan(24)',pos[12]<pos[13]<pos[14]<pos[24],[pos[x] for x in (12,13,14,24)])
    ok('MCU: Cap. America(41)<Agent Carter S1(43)<Captain Marvel(88)<Iron Man(45)<Avengers(51)<Endgame(89)',pos[41]<pos[43]<pos[88]<pos[45]<pos[51]<pos[89])
    ok('Titoli senza data (Doomsday 136, S3 137, X-Men97 S3 138, Secret Wars 139) marcati non determinabile',all('non determinabile' in sub[str(n)] for n in (136,137,138,139)),[sub[str(n)] for n in (136,137)])
    ok('data dibattuta marcata ~ (Hulk 49, Hawkeye 100)',sub['49'].find('~')>=0 and sub['100'].find('~')>=0,(sub['49'][:60],sub['100'][:60]))
    ok('Loki S1 (95) e Terra-838 (102) non inventano anni errati (102 non datato)','non determinabile' in sub['102'] and '2023' in sub['95'])
    ok('periodo Endgame (89) indicato come periodo','periodo' in sub['89'] and '2012' in sub['89'],sub['89'][:80])
    # click riga apre la scheda
    pg.click('#atList .at-row[data-num="24"]'); pg.wait_for_timeout(600)
    ok('click riga Logan apre item-024',pg.evaluate("document.querySelector('#item-024 details.card').open"))
    ok('nessun errore JS',not errs,errs)
    # overflow a 320
    ov=pg.evaluate("[document.documentElement.scrollWidth,innerWidth]")
    ok('nessun overflow orizzontale a 320px',ov[0]<=ov[1],ov)
    b.close()
print('TOTALE',len(res),'FALLITI',[i for i,x in enumerate(res) if not x])
