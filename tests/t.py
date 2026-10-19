import json, sys
from playwright.sync_api import sync_playwright
FILE='file:///home/claude/work/index.html'
IDS=['015','016','041','051','084','089','095','097','099','102','108','112','117','121','123','125']
res=[]
def ok(n,c,extra=''): res.append((n,bool(c),extra)); print(('PASS' if c else 'FAIL'),n,extra)
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':390,'height':844})
    pg=ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(FILE); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true;const h=document.getElementById('homeHub');if(h)h.style.display='none';}")
    ok('no pageerror load',not errs,str(errs[:2]))
    ok('card presente',pg.locator('#roadToDoomsday').count()==1)
    ok('16 righe',pg.locator('#rtdList .rtd-item').count()==16)
    ok('frac 0/16',pg.inner_text('#rtdFrac')=='0/16')
    # filtro: 4 schede verdi
    tags=pg.evaluate("""()=>['016','097','108','121'].map(n=>{const w=document.getElementById('item-'+n);return [w.dataset.tag,w.querySelector('.tag').textContent.trim(),w.querySelector('.tag').className]})""")
    ok('4 schede verde',all(t[0]=='verde' and t[1]=='OBBLIGATORIO' and 'tag-verde' in t[2] for t in tags),str(tags))
    cnt=pg.evaluate("()=>[document.querySelectorAll('.card-wrap[data-tag=verde]').length,document.querySelectorAll('.card-wrap[data-item]').length,new Set([...document.querySelectorAll('.card-wrap[data-item]')].map(e=>e.dataset.item)).size]")
    ok('conteggio verdi 49 / 139 schede / no duplicati',cnt==[49,139,139],str(cnt))
    ok('tutte le 16 verdi',pg.evaluate("(ids)=>ids.every(i=>document.getElementById('item-'+i).dataset.tag==='verde')",IDS))
    # XP prima
    def xp(): 
        return pg.evaluate("()=>JSON.parse(localStorage.getItem('marvel-ultimate-timeline-missioni-xp-bonus')||'{\"totale\":0}').totale")
    ok('bank xp 0',xp()==0)
    # segna 15 titoli via stato reale: usa click su checkbox
    for i in IDS[:15]:
        pg.evaluate("(i)=>{const c=document.querySelector('.watch-check[data-item=\"'+i+'\"]');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}));}",i)
    pg.wait_for_timeout(500)
    ok('frac 15/16',pg.inner_text('#rtdFrac')=='15/16',pg.inner_text('#rtdFrac'))
    ok('non completata a 15',not pg.evaluate("()=>document.getElementById('roadToDoomsday').classList.contains('rtd-completa')"))
    xp15=xp(); keys15=pg.evaluate("()=>JSON.parse(localStorage.getItem('marvel-ultimate-timeline-missioni-xp-bonus')).ricompensate.filter(k=>k.indexOf('road-to-doomsday')>-1).length")
    ok('nessun XP road a 15/16',keys15==0,f'xp={xp15}')
    # ultimo
    pg.evaluate("(i)=>{const c=document.querySelector('.watch-check[data-item=\"'+i+'\"]');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}));}",IDS[15])
    pg.wait_for_timeout(500)
    ok('frac 16/16',pg.inner_text('#rtdFrac')=='16/16')
    ok('completata',pg.evaluate("()=>document.getElementById('roadToDoomsday').classList.contains('rtd-completa')"))
    ok('xp +300 esatti',xp()-xp15==300,f'{xp15}->{xp()}')
    XP1=xp()
    ok('chiave ricompensa 1 sola',pg.evaluate("()=>JSON.parse(localStorage.getItem('marvel-ultimate-timeline-missioni-xp-bonus')).ricompensate.filter(k=>k==='road-to-doomsday-v1').length")==1)
    ok('badge visibile',pg.evaluate("()=>!document.getElementById('rtdBadge').hidden"))
    ok('celebrazione mostrata',pg.evaluate("()=>!document.getElementById('missioneCelebrazione').hidden"))
    pg.click('#missioneCelebrazioneChiudi')
    # no ripetizione: uncheck/recheck + reload
    for _ in range(2):
        pg.evaluate("(i)=>{const c=document.querySelector('.watch-check[data-item=\"'+i+'\"]');c.checked=!c.checked;c.dispatchEvent(new Event('change',{bubbles:true}));}",IDS[3])
        pg.wait_for_timeout(300)
    ok('xp invariato dopo toggle',xp()==XP1,str(xp()))
    ok('celebrazione non riaperta',pg.evaluate("()=>document.getElementById('missioneCelebrazione').hidden"))
    pg.reload(); pg.wait_for_timeout(1500)
    ok('xp invariato dopo reload',xp()==XP1,str(xp()))
    ok('celebrazione non riaperta reload',pg.evaluate("()=>document.getElementById('missioneCelebrazione').hidden"))
    pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true;document.getElementById('homeHub').style.display='none'}")
    ok('stato persistito 16/16',pg.inner_text('#rtdFrac')=='16/16')
    # link
    pg.evaluate("()=>{document.getElementById('rtdDetails').open=true}")
    pg.locator('#rtdList .rtd-link[data-rtd-id="121"]').scroll_into_view_if_needed()
    pg.click('#rtdList .rtd-link[data-rtd-id="121"]'); pg.wait_for_timeout(1200)
    r=pg.evaluate("()=>{const t=document.getElementById('item-121');const r=t.getBoundingClientRect();return [t.querySelector('details').open, r.top>=-5 && r.top<844, getComputedStyle(t).display]}")
    ok('link apre scheda 121 e la porta in vista',r[0] and r[1] and r[2]!='none',str(r))
    # tutti i link puntano a schede esistenti
    ok('tutti i link validi',pg.evaluate("()=>[...document.querySelectorAll('.rtd-link')].every(b=>document.getElementById('item-'+b.dataset.rtdId))"))
    # overflow orizzontale
    for w in (320,375,390,430,1280):
        pg.set_viewport_size({'width':w,'height':800}); pg.wait_for_timeout(200)
        ov=pg.evaluate("()=>document.documentElement.scrollWidth-document.documentElement.clientWidth")
        ok(f'no overflow {w}px',ov<=0,str(ov))
    ok('no pageerror finale',not errs,str(errs[:2]))
    pg.screenshot(path='/tmp/claude-0/t/final.png')
    b.close()
print('FAILED:',[r[0] for r in res if not r[1]])
