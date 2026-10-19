from playwright.sync_api import sync_playwright
import json,re
F='file:///home/claude/work/old_base/index.html'
res=[]
def ok(n,c,d=''): res.append(c); print('PASS' if c else 'FAIL',n,d)
src=open('/home/claude/work/old_base/index.html',encoding='utf-8').read()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':900}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(F); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{const li=document.getElementById('item-137');const st=li.querySelector('.status-tag');const l8=document.getElementById('item-138').querySelector('.status-tag');
      return {yr:li.querySelector('.yr').textContent,cls:st.className,title:st.title,txt:st.textContent.trim(),cls138:l8.className}}""")
    ok('137: anno "2027", badge Annunciato (stessa classe e titolo di 138)',r['yr']=='2027' and 'status-annunciato' in r['cls'] and r['cls']==r['cls138'] and r['title'].startswith('Progetto annunciato') and 'Annunciato' in r['txt'],r)
    ok('nessun "mar 2027"/"2027-03" fuori da atlasData',not re.search(r'mar 2027|2027-03',re.sub(r'<script type="application/json" id="atlasData">.*?</script>','',src,flags=re.S)))
    r=pg.evaluate("""()=>{return {f:['137','138','027','134','136','139','028','001'].map(i=>[i,titoloDisponibile(i)])}}""") if False else None
    m=re.search(r"var RILASCIO_JS = \{(.*?)\};",src,re.S); R=dict(re.findall(r"'(\d+)':\s*'([^']*)'",m.group(1)))
    ok('RILASCIO_JS: 137 e 138 solo anno, altre date invariate',R['137']=='2027' and R['138']=='2027' and R['027']=='2027-06-18' and R['134']=='2027-01-13' and R['136']=='2026-12-18' and R['139']=='2027-12-17' and R['028']=='non-distribuito',R)
    ok('137 e 138 restano bloccati (non data completa)',all(not re.match(r'^\d{4}-\d{2}-\d{2}$',R[i]) for i in ('137','138')))
    alt=pg.evaluate("()=>JSON.parse(document.getElementById('altTimelineData').textContent).filter(x=>[137,138].includes(x.num)).map(x=>[x.num,x.release])")
    ok('altTimelineData release invariato (null)',alt==[[137,None],[138,None]],alt)
    # tessera
    r=pg.evaluate("""()=>{const ids=JSON.parse(document.getElementById('tesseraCharIdsData').textContent);const sel=document.getElementById('tesseraFavSelect');
      const o=[...sel.options].filter(x=>x.value).map(x=>x.value);const pages=new Set([...document.querySelectorAll('li.card-wrap[id^=char-]')].map(x=>x.id));
      const bad=[];for(const v of o){const el=document.getElementById(ids[v]);if(!el){bad.push([v,'manca']);continue}const g=el.closest('details.letter-group');if(!g)bad.push([v,'senza gruppo'])}
      return {n:o.length,uniq:new Set(o).size,reach:new Set(o.map(v=>ids[v])).size,pages:pages.size,keys:Object.keys(ids).length,jarvis:'Jarvis' in ids,edwin:ids['Edwin Jarvis'],pageJ:!!document.getElementById('char-edwin-jarvis'),orph:Object.keys(ids).filter(k=>!o.includes(k)),bad}}""")
    ok('tessera: 304 opzioni uniche -> 304 pagine distinte = tutte le pagine',r['n']==r['uniq']==r['reach']==r['pages']==304 and not r['bad'],r)
    ok('tessera: nessuna chiave orfana; Jarvis rimossa, Edwin Jarvis e pagina intatti',r['keys']==304 and not r['orph'] and not r['jarvis'] and r['edwin']=='char-edwin-jarvis' and r['pageJ'],(r['keys'],r['orph'],r['jarvis']))
    # navigazione reale: tutte le 304 voci aprono il gruppo-lettera corretto
    out=pg.evaluate("""async()=>{const sel=document.getElementById('tesseraFavSelect'),link=document.getElementById('tesseraFavLink'),ids=JSON.parse(document.getElementById('tesseraCharIdsData').textContent);
      const bad=[];let n=0;for(const o of [...sel.options].filter(x=>x.value)){sel.value=o.value;sel.dispatchEvent(new Event('change'));link.onclick();await new Promise(r=>setTimeout(r,350));
        const el=document.getElementById(ids[o.value]);const g=el.closest('details.letter-group');const d=el.querySelector('details');
        const open=g&&g.hasAttribute('open')&&(!d||d.hasAttribute('open'));const only=document.querySelectorAll('details.letter-group[open]').length===1;
        if(open&&only)n++;else bad.push([o.value,!!open,only])}return {n,bad}}""")
    ok('tessera: tutte le 304 voci aprono gruppo-lettera e scheda corretti (un solo gruppo aperto)',out['n']==304,out['bad'][:8])
    # i link con lettera iniziale corretta continuano a funzionare per le 8 voci corrette
    ok('nessun errore JS',errs==[],errs[:3])
    b.close()
print('TOTALE FALLITI',res.count(False))
