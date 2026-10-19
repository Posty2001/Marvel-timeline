import re,json
from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
OLD=open('/home/claude/work/backups/N0_pre_ios_xmen.html',encoding='utf-8').read()
NEW=open('/home/claude/work/index.html',encoding='utf-8').read()
res=[]
def ok(n,c,d=''): res.append(bool(c)); print('PASS' if c else 'FAIL',n,d)
def order(s): return re.findall(r'id="item-(\d+)" data-item="\d+" data-tag="(\w+)" data-studio="(\w+)"',s)
o,n=order(OLD),order(NEW)
# AGGIORNATO (ordine di visione X-Men, ott. 2026): atteso = ordine precedente con i 13 titoli Fox nella sequenza editoriale approvata (tools/xmen_order.json)
XO=json.load(open('/home/claude/work/tools/xmen_order.json'))['order']
info={x[0]:x for x in o}; exp=[x for x in o if x[0]!='133']  # 133 = variante di 089 (non titolo autonomo)
fx=[k for k,x in enumerate(exp) if x[0] in XO]; assert fx==list(range(fx[0],fx[0]+13)); exp[fx[0]:fx[0]+13]=[info[i] for i in XO]
ok('138 schede autonome, ordine = precedente con i 13 titoli Fox nella nuova sequenza editoriale (133 Encore ora variante)',len(n)==138 and n==exp)
ok('colore/studio per id invariati',dict((a,(b,c)) for a,b,c in o if a!='133')==dict((a,(b,c)) for a,b,c in n))
ids=[x[0] for x in n]; k=ids.index('022'); ok('sequenza: 021, Deadpool(022), Logan(024), Deadpool 2(023), 025',ids[k-1:k+4]==['021','022','024','023','025'],ids[k-1:k+4])
rec=dict(re.findall(r'id="item-(\d+)"(?:(?!</li>).)*?<span class="rec">N&deg;(\d+)</span>',NEW,re.S))
ok('N° visibile: Deadpool 022, Logan 023, Deadpool 2 024',(rec['022'],rec['024'],rec['023'])==('022','023','024'),rec['022']+rec['024']+rec['023'])
ok('N° visibile = id per tutte le altre schede (fuori dai 13 Fox)',all(rec[x]==x for x in rec if x not in XO))
ok('N° visibili Fox = 012..024 nell\'ordine della sequenza',[rec[i] for i in XO]==['%03d'%v for v in range(12,25)],[rec[i] for i in XO])
ok('N° visibili tutti unici e consecutivi 001..139',sorted(rec.values())==['%03d'%i for i in range(1,140) if i!=133])
title=lambda s,i:re.search(r'id="item-%s".*?class="title">(.*?)</span>'%i,s,re.S).group(1)
ok('id stabili: 022=Deadpool, 023=Deadpool 2, 024=Logan',(title(NEW,'022'),title(NEW,'023'),title(NEW,'024'))==('Deadpool','Deadpool 2','Logan'))
for i in ('022','023','024'):
    blk=lambda s:re.search(r'<li class="card-wrap" id="item-%s".*?</li>'%i,s,re.S).group(0)
    a=re.sub(r'<span class="rec">.*?</span>','',blk(OLD)); b=re.sub(r'<span class="rec">.*?</span>','',blk(NEW))
    b=re.sub(r'</details><details class="sub-group sub-order-why">.*?</details></div>','</details></div>',b,flags=re.S)
    # AGGIORNATO: note editoriali del nuovo ordine (Deadpool precede Logan, Deadpool 2 lo segue)
    b=re.sub(r'\. In questo percorso (?:precede|segue) Logan \(N&deg;\d+\) per scelta editoriale, non per cronologia: vedi &laquo;Perch&eacute; questo ordine&raquo; nella scheda di Logan','',b)
    if i=='024': b=re.sub(r'\. Nel percorso editoriale segue Deadpool e precede Deadpool 2[^<]*','',b)
    ok('scheda %s: contenuto invariato (salvo N° e nota editoriale)'%i,a==b)
ok('nota editoriale su Logan: non cronologica',"non indica precedenza cronologica" in NEW)
# riferimenti N° nelle pagine Atlante: stesse opere di prima
def vis2id(s):
    return {v:k for k,v in re.findall(r'id="item-(\d+)"(?:(?!</li>).)*?<span class="rec">N&deg;(\d+)</span>',s,re.S)}
def refs(s,v2i):
    out={}
    for m in re.finditer(r'<li class="card-wrap" id="((?:char|att)-[^"]+)".*?\n\s*</li>',s,re.S):
        out[m.group(1)]=sorted({v2i.get(x,x) for x in re.findall(r'N(?:&deg;|°)(\d+)',m.group(0))})
    return out
ro=refs(OLD,{}); rn=refs(NEW,vis2id(NEW))
bad=[k for k in ro if ro[k]!=rn.get(k)]
ok('Atlante: per ogni pagina personaggio/attore le opere citate (per id) sono identiche a prima (%d pagine)'%len(ro),not bad,bad[:4])
# liste ordinate
def ascending(s):
    bad=[]
    for m in re.finditer(r'<span class="detail-v">((?:N&deg;\d+[^<]*?)(?:, N&deg;\d+[^<]*?)+)</span>',s):
        nums=re.findall(r'N&deg;(\d+)',m.group(1))
        if nums!=sorted(nums): bad.append(nums)
    return bad
ok('liste "ALTRE APP." restano in ordine crescente',not ascending(NEW),ascending(NEW)[:3])
# strutture JS
W=json.loads(re.search(r'var WATCH_ORDER_JS = (\[.*?\]);\n',NEW,re.S).group(1)); wi=[x['id'] for x in W]
ok('WATCH_ORDER_JS: stesso ordine delle schede',wi==ids)
ok('DEPENDENCY_MAP: 117 elenca Deadpool, Logan, Deadpool 2 (ordine di visione)','"117": {"ess": ["022", "024", "023", "095"]' in NEW)
ok('prerequisito duro invariato: Deadpool 2 richiede Deadpool',"'023': ['022']" in NEW)
A=json.loads(re.search(r'id="atlasData">(.*?)</script>',NEW,re.S).group(1)); ok('atlasData.opere: stesso ordine',[x['id'] for x in A['opere'] if x['id']!='133']==ids)
T=json.loads(re.search(r'id="altTimelineData">(.*?)</script>',NEW,re.S).group(1)); ok('Timeline alternativa: stesso ordine, 139 titoli unici',['%03d'%x['num'] for x in T]==ids and len({x['num'] for x in T})==138)
ok('ritorno Xavier: Patrick Stewart (N°023 = Logan nella nuova sequenza)',"Patrick Stewart</a> (N°023)" in NEW and "Patrick Stewart (N°023)" in NEW)
# zoom / viewport
vp=re.search(r'<meta name="viewport" content="([^"]*)"',NEW).group(1)
ok('viewport: viewport-fit=cover, nessun blocco dello zoom',('viewport-fit=cover' in vp) and not re.search(r'user-scalable\s*=\s*(no|0)|maximum-scale',vp),vp)
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(F); pg.wait_for_timeout(1200)
    # progressi PRE-ESISTENTI (chiavi per id): Deadpool 2 visto+voto+preferito+nota, Logan visto, Deadpool non visto
    pg.evaluate("""()=>{const S=(k,v)=>localStorage.setItem('marvel-ultimate-timeline-'+k,JSON.stringify(v));
      S('watched',{'012':true,'024':true,'023':true}); S('ratings',{'023':4,'024':5}); S('favorites',{'023':true}); S('notes',{'024':'nota logan','023':'nota dp2'}); S('last-watched',{item:'024'});}""")
    before=pg.evaluate("()=>Object.keys(localStorage).sort().map(k=>k+'='+localStorage.getItem(k))")
    pg.reload(); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true;document.getElementById('homeHub').style.display='none'}")
    st=pg.evaluate("""()=>{const q=(i)=>document.querySelector('#item-'+i);const t=(i)=>q(i).querySelector('.title').textContent.trim();
      return ['022','023','024'].map(i=>({id:i,title:t(i),rec:q(i).querySelector('.rec').textContent.trim(),watched:q(i).querySelector('.watch-check').checked,note:q(i).querySelector('textarea.user-note').value,fav:q(i).querySelector('.fav-star').classList.contains('fav-active')||q(i).querySelector('.fav-star').textContent.trim()==='★',stars:q(i).querySelectorAll('.rating-star.active,.rating-star.filled,.rating-star.rated').length}))}""")
    d={x['id']:x for x in st}
    ok('progressi: Logan(024) visto, Deadpool 2(023) visto, Deadpool(022) NON visto',d['024']['watched'] and d['023']['watched'] and not d['022']['watched'],st)
    ok('note associate alle opere corrette',d['024']['note']=='nota logan' and d['023']['note']=='nota dp2' and d['022']['note']=='')
    ok('preferito su Deadpool 2 soltanto',d['023']['fav'] and not d['022']['fav'] and not d['024']['fav'],[(x['id'],x['fav']) for x in st])
    after=pg.evaluate("()=>Object.keys(localStorage).sort().map(k=>k+'='+localStorage.getItem(k))")
    ok('localStorage non alterato dal caricamento (chiavi di salvataggio intatte)',[x for x in before if 'watched' in x or 'ratings' in x or 'favorites' in x or 'notes' in x]==[x for x in after if 'watched' in x or 'ratings' in x or 'favorites' in x or 'notes' in x])
    # prossimo titolo / continua: azzero e segno fino a 021
    pg.evaluate("""()=>{const S=(k,v)=>localStorage.setItem('marvel-ultimate-timeline-'+k,JSON.stringify(v));const w={};for(let i=1;i<=21;i++)w[('00'+i).slice(-3)]=true;S('watched',w);S('last-watched',{});}""")
    pg.reload(); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=false;}"); pg.wait_for_timeout(600)
    txt=pg.evaluate("()=>{const e=document.getElementById('nextWatchCard')||document.querySelector('.home-hub-continue .next-watch-card');return e?e.textContent.replace(/\\s+/g,' '):''}")
    print('HUB',txt[:300]); ok('Home "Prossimo titolo" dopo 021 = Deadpool, Scheda N°022 (nuova sequenza)',('Deadpool' in txt) and ('Logan' not in txt) and 'N°022' in txt,txt[:120])
    # Timeline alternativa: etichetta N° visibile
    pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true;document.getElementById('altTimelineToggle').checked=true}")
    pg.wait_for_timeout(300); pg.click('.at-mode-btn[data-mode="custom"]'); pg.wait_for_timeout(400)
    sub=pg.evaluate("""()=>{const r=[...document.querySelectorAll('#atList .at-row')].map(e=>e.textContent.replace(/\\s+/g,' ').trim());return r.filter(x=>/Logan|Deadpool/.test(x)&&!/Wolverine/.test(x)).slice(0,3)}""")
    print('AT',pg.evaluate("()=>[...document.querySelectorAll('#atList .at-row')].length"), pg.evaluate("()=>document.getElementById('atList').innerHTML.length"))
    ok('Timeline alternativa mostra Deadpool N°022, Logan N°023, Deadpool 2 N°024',len(sub)==3 and 'N°022' in sub[0] and 'Deadpool' in sub[0] and 'N°023' in sub[1] and 'Logan' in sub[1] and 'N°024' in sub[2] and 'Deadpool 2' in sub[2],sub)
    # click riga Logan apre la scheda giusta
    pg.evaluate("()=>{const r=[...document.querySelectorAll('#atList .at-row')].find(e=>e.getAttribute('data-num')==='24');r.click()}"); pg.wait_for_timeout(600)
    ok('click su Logan nella timeline alternativa apre item-024',pg.evaluate("()=>document.querySelector('#item-024 details.card').open"))
    # ordine personalizzato salvato per id: resta agganciato alle opere
    pg.evaluate("()=>localStorage.setItem('marvelGuideCustomTimelineOrder',JSON.stringify([24,22,23]))"); 
    pg.evaluate("()=>{const i=document.getElementById('spoilerCutoffInput');i.value=22;i.dispatchEvent(new Event('input',{bubbles:true}))}")
    bc=pg.evaluate("()=>['024','022','023','021','025'].map(i=>[i,document.getElementById('item-'+i).classList.contains('beyond-cutoff')])")
    ok('cutoff spoiler #22: Deadpool(N°022) incluso; Logan(N°023), Deadpool 2 e N°025 oltre',bc==[['024',True],['022',False],['023',True],['021',False],['025',True]],bc)
    ok('nessun errore JS',not errs,errs[:2])
    # campi input: font >=16px su touch
    fs=pg.evaluate("""()=>[...document.querySelectorAll('input,select,textarea')].filter(e=>!['checkbox','radio','range','file','hidden','button','submit'].includes(e.type)).map(e=>[e.id||e.className,parseFloat(getComputedStyle(e).fontSize)]).filter(x=>x[1]<16)""")
    ok('tutti i campi di testo/select/textarea >=16px (nessun auto-zoom iOS)',not fs,fs[:6])
    ok('touch-action: manipulation su html e body (niente zoom da doppio tap)',pg.evaluate("()=>getComputedStyle(document.documentElement).touchAction==='manipulation'&&getComputedStyle(document.body).touchAction==='manipulation'"))
    b.close()
print('TOTALE FALLITI',res.count(False),'su',len(res))
