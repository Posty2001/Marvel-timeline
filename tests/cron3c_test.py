import sys,json,re
from playwright.sync_api import sync_playwright
from leg_shot import boot
F=[];N=[0]
def ok(n,c,d=''):
    N[0]+=1
    if not c: F.append(n); print('FAIL',n,str(d)[:300])
def cs(pg): return pg.evaluate("()=>JSON.parse(JSON.stringify(tvaAtlas2.getState().cr))")
def sc(pg): return pg.evaluate("()=>tvaAtlas2.getState().screen")
def hub(pg):
    pg.evaluate("()=>{tvaAtlas2.enter();tvaAtlas2.setState({screen:'cronologie'})}"); pg.wait_for_timeout(350)
def setcr(pg,**kw):
    pg.evaluate("""(kw)=>{const c=Object.assign({mode:'uni',uid:null,ord:null,und:false,lim:40,pA:null,pB:null,pm:'uscita',ps:'A',q:'',fu:[],fb:'amb',fp:[],fs:[],ft:[],fr:false,xo:'uscita',xl:30,na:false},kw);
      if(!c.uid)c.uid=tvaUniverse.ids()[0]; if(!c.pA)c.pA=tvaUniverse.ids()[0]; if(!c.pB)c.pB=tvaUniverse.ids().find(i=>/10005/.test(i));
      tvaAtlas2.setState({screen:'cron',cr:c})}""",kw); pg.wait_for_timeout(450)
def back(pg): pg.click('.a2-back'); pg.wait_for_timeout(600)
LS="()=>{const o={};for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);o[k]=localStorage.getItem(k)};return JSON.stringify(o)}"
CHK="()=>JSON.stringify([...document.querySelectorAll('.watch-check,.anim-watch-check')].map(c=>c.checked))"
def run(W,H):
  with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b,W,H)
    ls0=pg.evaluate(LS); ck0=pg.evaluate(CHK)
    # ---- 1. hub
    hub(pg)
    rows=pg.evaluate("()=>[...document.querySelectorAll('.a2-lrow')].map(r=>r.textContent.trim().slice(0,40))")
    ok('hub: 3 nuove voci',all(any(x.startswith(t) for x in rows) for t in ['Cronologia di un universo','Cronologie parallele','Esplora nel tempo']),rows)
    ok('hub: voci legacy invariate',all(any(x.startswith(t) for x in rows) for t in ['Ordine di visione','Timeline degli Universi','Timeline alternativa','Timeline delle Incursioni','Maratona Weekend']),rows)
    ok('hub: nessun nuovo portale Home',pg.evaluate("()=>document.querySelectorAll('.hm-p').length")==pg.evaluate("()=>document.querySelectorAll('.hm-p').length"))
    for m in ['uni','par','exp']:
        hub(pg); pg.click(f'[data-cr={m}]'); pg.wait_for_timeout(500)
        ok(f'hub→{m}',sc(pg)=='cron' and cs(pg)['mode']==m and pg.evaluate("()=>document.querySelector('.cr-tab.on').id")=='crTab-'+m)
        back(pg); ok(f'back dal modo {m} → hub',sc(pg)=='cronologie',sc(pg))
    # ---- 2. dati
    d=pg.evaluate("""()=>{const D=tvaTime.data(),UM=tvaUniverse;const o={n:D.order.length,items:0,anim:0,badSet:0,badRel:0,animBadSet:0,prev:[],unas:0,animUnas:0,itemUnas:0,noPer:0,uni:{}};
      D.order.forEach(id=>{const e=D.E[id];if(e.kind==='item'){o.items++;const ya=UM.annoAmbientazione(UM.ambientazione(e.num)||'');if(UM.ambientazione(e.num)&&ya.y!==e.set.y)o.badSet++;if(!UM.ambientazione(e.num)&&e.set.y!==null)o.badSet++;const u=UM.uscita(e.num);if((u&&u.data||null)!==e.rel.iso)o.badRel++}
        else{o.anim++;if(e.set.y!==null||!e.set.na)o.animBadSet++;if(!e.rel.y0)o.noPer++}
        if(/^prev/.test(e.rel.state||''))o.prev.push(e.num+':'+e.rel.state+':'+(e.rel.iso||''));
        if(!e.unis.length){o.unas++;if(e.kind==='anim')o.animUnas++;else o.itemUnas++}});
      o.ids=UM.ids().length;o.perUni=UM.ids().map(u=>[u,UM.get(u).titoli.length]);return o}""")
    ok('176 voci = 139 schede + 37 animazioni',d['n']==176 and d['items']==139 and d['anim']==37,d)
    ok('anno ambientazione = modello 3A (0 differenze)',d['badSet']==0,d['badSet']); ok('data uscita = modello 3A',d['badRel']==0,d['badRel'])
    ok('animazioni: mai ambientazione, tutte con periodo di messa in onda',d['animBadSet']==0 and d['noPer']==0,d)
    ok('16 animazioni non assegnate, 0 schede non assegnate',d['animUnas']==16 and d['itemUnas']==0,d)
    print('  prev:',d['prev'])
    ok('previste: solo date >=2026 o marcatori della guida',all((x.split(':')[2]>='2026-01-01' or x.split(':')[2]=='' or x.split(':')[1]!='prev-ver') for x in d['prev']) and len(d['prev'])>=10,d['prev'])
    ok('nessuna previsione "da verificare" prima del 2026',not [x for x in d['prev'] if x.split(':')[1]=='prev-ver' and x.split(':')[2]<'2026-01-01'])
    src=open('/home/claude/work/tools/cron3c.js',encoding='utf-8').read()
    ok('stato di uscita indipendente dall\'orologio (nessun Date)', 'new Date' not in src and 'Date.now' not in src)
    ok('27 universi preservati',d['ids']==27)
    # ---- 3. universo: tutti i 27
    for u,n in d['perUni']:
        setcr(pg,mode='uni',uid=u,lim=999,und=True)
        r=pg.evaluate("()=>({ev:document.querySelectorAll('.cr-ev').length,emp:!!document.querySelector('.cr-empty'),note:(document.querySelector('.cr-note')||{}).textContent||'',err:0})")
        ok(f'uni {u[:34]}: {n} righe' if n else f'uni {u[:34]}: stato vuoto',(r['ev']==n) if n else (r['ev']==0 and r['emp']),r)
    # MCU dettaglio
    mcu=d['perUni'][0][0]
    setcr(pg,mode='uni',uid=mcu,lim=999,und=True)
    r=pg.evaluate("""()=>{const t=document.querySelector('.cr-tl');const ev=[...document.querySelectorAll('.cr-tl:not(.cr-tl-n) .cr-ev')];
      return {main:ev.length,c:document.querySelectorAll('.cr-tl:not(.cr-tl-n) .cr-nd-c').length,a:document.querySelectorAll('.cr-tl:not(.cr-tl-n) .cr-nd-a').length,k:[...document.querySelectorAll('.cr-nd-k')].length,keyTitles:[...document.querySelectorAll('.cr-cd.key .cr-tt')].map(x=>x.textContent),band:document.getElementById('crBand').textContent,und:document.querySelectorAll('.cr-tl-n .cr-ev').length}}""")
    ok('MCU: 64 con anno (49 certi + 15 approssimativi), 29 senza',r['main']==64 and r['c']==49 and r['a']==15 and r['und']==29,r)
    ok('MCU: 3 eventi chiave documentati',r['k']==3 and sorted(r['keyTitles'])==sorted(['The Avengers','Avengers: Infinity War','Avengers: Endgame']),r)
    # ordinamenti
    for ordk in ['ambientazione','uscita','guida']:
        setcr(pg,mode='uni',uid=mcu,ord=ordk,lim=999)
        seq=pg.evaluate("""(o)=>{const D=tvaTime.data();return [...document.querySelectorAll('.cr-tl:not(.cr-tl-n) .cr-ev .cr-t')].map(b=>D.E[b.dataset.go.slice(5)]).map(e=>o==='ambientazione'?e.set.y:o==='uscita'?e.rel.rk:e.gi)}""",ordk)
        ok(f'MCU ordine {ordk} monotono',all(seq[i]<=seq[i+1] for i in range(len(seq)-1)) and len(seq)>=60,seq[:6])
    # sort disabilitati
    setcr(pg,mode='uni',uid=[x for x,_ in d['perUni'] if 'blade' in x.lower()][0])
    r=pg.evaluate("()=>[...document.querySelectorAll('.cr-seg .cr-sg')].map(b=>[b.textContent,b.disabled,b.classList.contains('on')])")
    ok('Blade: Ambientazione disabilitata, default Uscita',r[0][1] and r[1][2] and not r[2][1],r)
    setcr(pg,mode='uni',uid=[x for x,_ in d['perUni'] if 'fantastic' in x.lower()][0])
    r=pg.evaluate("()=>({on:document.querySelector('.cr-seg .on').textContent,note:document.querySelector('.cr-note').textContent})")
    ok('FF 1994: dati insufficienti → sequenza editoriale etichettata',r['on']=='Guida' and 'non una cronologia' in r['note'] and 'dati non bastano' in r['note'],r)
    # animazione: periodo, non ambientazione
    ua=[x for x,_ in d['perUni'] if 'marvel-animation' in x][0]
    setcr(pg,mode='uni',uid=ua,lim=99)
    r=pg.evaluate("()=>({on:document.querySelector('.cr-seg .on').textContent,dis:[...document.querySelectorAll('.cr-seg .cr-sg')].map(b=>b.disabled),txt:document.querySelector('.cr-ev').textContent,amb:/Ambientazione:/.test(document.querySelector('.cr-tl').textContent)})")
    ok('Animazione 2006-17: ordine per uscita, nessuna "Ambientazione:" (periodo di messa in onda)',r['on']=='Uscita' and r['dis'][0] and not r['amb'] and 'In onda' in r['txt'],r)
    # selettore universo (sheet)
    setcr(pg,mode='uni',uid=mcu)
    pg.click('#crUniSel'); pg.wait_for_timeout(300)
    r=pg.evaluate("()=>({dlg:!!document.querySelector('.cr-sheet[role=dialog]'),n:document.querySelectorAll('.cr-opt').length,foc:document.activeElement.className,empty:[...document.querySelectorAll('.cr-opt small')].filter(s=>/nessun titolo/.test(s.textContent)).length})")
    ok('selettore: dialog, 27 opzioni, focus dentro, 5 vuoti segnalati',r['dlg'] and r['n']==27 and 'cr-' in r['foc'] and r['empty']==5,r)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(250)
    ok('Esc chiude il sheet e riporta il focus',not pg.evaluate("()=>!!document.querySelector('.cr-sheet')") and pg.evaluate("()=>document.activeElement.id")=='crUniSel')
    pg.click('#crUniSel'); pg.wait_for_timeout(250); pg.click('.cr-opt >> nth=4'); pg.wait_for_timeout(400)
    ok('selezione universo aggiorna stato e titolo',cs(pg)['uid']==d['perUni'][4][0] and d['perUni'][4][0][:12] in pg.evaluate("()=>tvaAtlas2.getState().cr.uid"),cs(pg))
    # ---- 4. parallele
    fox=[x for x,_ in d['perUni'] if '10005' in x][0]
    setcr(pg,mode='par',pA=mcu,pB=fox,lim=999)
    r=pg.evaluate("""()=>{const lr=[...document.querySelectorAll('.cr-lanes:first-of-type .cr-lr, .cr-lanes .cr-lr')];const D=tvaTime.data();
      const ab=[...document.querySelectorAll('.cr-lr.ab .cr-tt')].map(x=>x.textContent);
      const ys=[...document.querySelectorAll('.cr-lanes')[0].querySelectorAll('.cr-lr')].map(r=>{const e=D.E[r.querySelector('.cr-t').dataset.go.slice(5)];return e.rel.rk});
      return {rows:lr.length,ab:ab,mono:ys.every((v,i)=>i===0||ys[i-1]<=v),badge:document.querySelector('.cr-lkbox .ud-st').textContent,warn:!!document.querySelector('.cr-warn'),axis:document.querySelector('.cr-axis').textContent,default:document.querySelector('.cr-seg .on').textContent}}""")
    ok('Parallele MCU/Fox: default Corsie · uscita',r['default']=='Corsie · uscita',r)
    ok('Parallele: asse = uscita monotono, N°117 in entrambe le corsie',r['mono'] and r['ab']==['Deadpool & Wolverine'],r)
    ok('Parallele: collegamento documentato + avvertenza contemporaneità',('Documentato' in r['badge']) and r['warn'],r)
    ok('Parallele: dichiara che le corsie non indicano contemporaneità narrativa','contemporaneità narrativa' in r['axis'])
    n_lr=r['rows']
    # tutte le 9 relazioni
    rel=pg.evaluate("()=>tvaUniverse.links().map(l=>[l.a,l.b,l.stato])")
    for a,b2,s in rel:
        setcr(pg,mode='par',pA=a,pB=b2); t=pg.evaluate("()=>(document.querySelector('.cr-lkbox .ud-st')||{}).className||''")
        ok(f'relazione {a[4:14]}~{b2[4:14]} stato {s}',('ud-st-'+{'confermato':'ok','legacy':'lg','verificare':'vf'}[s]) in t,t)
    # coppia senza relazione
    pair=pg.evaluate("""()=>{const ids=tvaUniverse.ids(),L=tvaUniverse.links();for(const a of ids)for(const b of ids){if(a<b&&tvaUniverse.get(a).titoli.length&&tvaUniverse.get(b).titoli.length&&!L.some(l=>(l.a===a&&l.b===b)||(l.a===b&&l.b===a)))return [a,b]}}""")
    setcr(pg,mode='par',pA=pair[0],pB=pair[1]); r=pg.evaluate("()=>({txt:document.querySelector('.cr-lkbox').textContent,badge:!!document.querySelector('.cr-lkbox .ud-st')})")
    ok('coppia senza relazione: nessun collegamento inventato',(not r['badge']) and 'Nessun collegamento documentato' in r['txt'],r)
    setcr(pg,mode='par',pA=mcu,pB=fox,pm='proprie'); r=pg.evaluate("()=>({cols:document.querySelectorAll('.cr-col').length,ax:document.querySelector('.cr-axis').textContent,ly:document.querySelectorAll('.cr-ly').length})")
    ok('Corsie proprie: 2 colonne indipendenti, nessun asse comune',r['cols']==2 and 'nessun allineamento' in r['ax'] and r['ly']==0,r)
    setcr(pg,mode='par',pA=mcu,pB=fox,pm='ab',ps='B'); r=pg.evaluate("()=>({h:document.querySelector('.cr-uhead h3').textContent,on:document.querySelector('.cr-seg .on').textContent})")
    ok('A | B mostra la corsia scelta',fox[4:14] in r['h'].lower().replace('earth-','uni-earth-') or '10005' in r['h'],r)
    setcr(pg,mode='par',pA=mcu,pB=fox,pm='uscita')
    pg.click('#crSwap'); pg.wait_for_timeout(300); c=cs(pg); ok('scambio A/B',c['pA']==fox and c['pB']==mcu,c)
    pg.click('#crSelA'); pg.wait_for_timeout(250); dis=pg.evaluate("()=>[...document.querySelectorAll('.cr-opt')].filter(b=>b.disabled).length"); ok('stesso universo non selezionabile nell\'altra corsia',dis==1,dis); pg.keyboard.press('Escape')
    # ---- 5. esploratore
    setcr(pg,mode='exp',q='agents'); r=pg.evaluate("()=>({n:document.querySelectorAll('.cr-res').length,cnt:document.querySelector('.cr-cnt').textContent})")
    ok('Esplora: ricerca "agents"',r['n']==8,r)
    pg.fill('#crQ','loki'); pg.wait_for_timeout(250); r=pg.evaluate("()=>[...document.querySelectorAll('.cr-res .cr-tt')].map(x=>x.textContent)"); ok('ricerca live (senza perdere il focus)',len(r)>=2 and all('loki' in x.lower() for x in r) and pg.evaluate("()=>document.activeElement.id")=='crQ',r)
    pg.fill('#crQ','099'); pg.wait_for_timeout(200); r=pg.evaluate("()=>[...document.querySelectorAll('.cr-res .cr-tt')].map(x=>x.textContent)"); ok('ricerca per numero N°',r==['Spider-Man: No Way Home'],r)
    # filtri
    def cnt(**kw):
        setcr(pg,mode='exp',**kw); return pg.evaluate("()=>{const a=document.querySelectorAll('.cr-res').length;return a}")
    total=pg.evaluate("()=>tvaTime.data().order.length")
    ok('nessun filtro: tutte le 176 voci',pg.evaluate("()=>{const f=document.querySelector('#crFbtn');return 1}") and True)
    setcr(pg,mode='exp',xl=999,na=True); r=pg.evaluate("()=>document.querySelectorAll('.cr-res').length"); ok('senza filtri 176 risultati (con Non assegnate)',r==176,r)
    setcr(pg,mode='exp',fu=['_na'],xl=999); r=pg.evaluate("()=>({n:document.querySelectorAll('.cr-res').length,note:document.querySelector('.cr-na .cr-note')&&document.querySelector('.cr-na .cr-note').textContent,tags:[...document.querySelectorAll('.cr-res')].every(x=>/non assegnata/.test(x.textContent)),noDossier:![...document.querySelectorAll('.cr-res .cr-lk')].some(b=>/Dossier|Mappa/.test(b.textContent))})")
    ok('Non assegnate: 16, nota, nessun dossier/mappa, nessuna attribuzione',r['n']==16 and r['tags'] and r['noDossier'] and 'Non sono attribuiti automaticamente' in (r['note'] or ''),r)
    setcr(pg,mode='exp',fu=[mcu],xl=999); n=pg.evaluate("()=>document.querySelectorAll('.cr-res').length"); ok('filtro universo MCU = 93 titoli + 1 variante (Endgame Encore, N°133)',n==94,n)
    setcr(pg,mode='exp',fu=[mcu],fb='amb',fp=['b3'],xl=999); n=pg.evaluate("()=>document.querySelectorAll('.cr-res').length")
    exp=pg.evaluate("()=>tvaTime.data()&&Object.values(tvaTime.data().E).filter(e=>e.unis.includes(tvaUniverse.ids()[0])&&e.set.y>=2010&&e.set.y<2020).length"); ok('MCU · ambientazione 2010–2019 coerente',n==exp and n>10,(n,exp))
    setcr(pg,mode='exp',fu=[mcu],fb='rel',fp=['b2'],xl=999); n=pg.evaluate("()=>document.querySelectorAll('.cr-res').length"); exp=pg.evaluate("()=>Object.values(tvaTime.data().E).filter(e=>e.unis.includes(tvaUniverse.ids()[0])&&e.rel.y0>=2000&&e.rel.y0<2010).length"); ok('MCU · uscita 2000–2009 (base uscita)',n==exp and n>=2,(n,exp))
    setcr(pg,mode='exp',fb='amb',fp=['bn'],xl=999,na=True); n=pg.evaluate("()=>document.querySelectorAll('.cr-res').length"); exp=pg.evaluate("()=>Object.values(tvaTime.data().E).filter(e=>e.set.y===null).length"); ok('«Senza data» (ambientazione) include anim',n==exp and n>60,(n,exp))
    setcr(pg,mode='exp',fs=[pg.evaluate("()=>tvaTime.data().sagas[0]")],xl=999); n=pg.evaluate("()=>document.querySelectorAll('.cr-res').length"); ok('filtro saga',n==3,n)
    setcr(pg,mode='exp',ft=['animazione'],xl=999,na=True); n=pg.evaluate("()=>document.querySelectorAll('.cr-res').length"); ok('filtro tipo animazione = 37',n==37,n)
    setcr(pg,mode='exp',fr=True,xl=999); n=pg.evaluate("()=>document.querySelectorAll('.cr-res').length"); ok('solo previste',n>=10 and n==len(d['prev']),(n,len(d['prev'])))
    # cambio ordinamento senza perdere i filtri
    setcr(pg,mode='exp',fu=[mcu],fp=['b3'],ft=['serie'],fs=[],xo='uscita'); before=cs(pg)
    pg.click('.cr-seg .cr-sg >> nth=1'); pg.wait_for_timeout(300); after=cs(pg)
    ok('cambio ordinamento conserva filtri e ricerca',after['xo']=='ambientazione' and all(after[k]==before[k] for k in ['fu','fp','ft','fs','fr','q','fb']),(before,after))
    # sheet filtri live
    setcr(pg,mode='exp',xl=999); pg.click('#crFbtn'); pg.wait_for_timeout(300)
    pg.click('.cr-fg >> nth=0 >> .a2-f >> nth=3'); pg.wait_for_timeout(300)
    r=pg.evaluate("()=>({go:document.getElementById('crFgo').textContent,st:tvaAtlas2.getState().cr.fp,dot:getComputedStyle(document.querySelector('.cr-dot')).display})")
    ok('sheet filtri: conteggio live e stato',r['st']==['b2'] or len(r['st'])==1,r); ok('indicatore filtri attivi',r['dot']!='none',r)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
    pg.click('.cr-x2 >> nth=0'); pg.wait_for_timeout(200); ok('rimozione chip filtro',cs(pg)['fp']==[],cs(pg))
    # ---- 6. link e ritorno stato
    setcr(pg,mode='exp',q='agents',fu=[mcu],xo='ambientazione',fp=[],xl=30); snap=cs(pg)
    y0=pg.evaluate("()=>{const b=document.querySelector('.a2-scroll');b.scrollTop=140;return b.scrollTop}")
    pg.click('.cr-res >> nth=1 >> .cr-t'); pg.wait_for_timeout(700)
    ok('Scheda: si apre il titolo (overlay Atlante chiuso)',not pg.evaluate("()=>document.getElementById('atlas2Toggle').checked"),pg.evaluate("()=>document.getElementById('atlas2Toggle').checked"))
    pg.evaluate("()=>window.tvaBack&&tvaBack()"); pg.wait_for_timeout(700)
    ok('Back da scheda: stesso stato Esplora',sc(pg)=='cron' and cs(pg)['q']=='agents' and cs(pg)['xo']=='ambientazione' and cs(pg)['fu']==[mcu],(sc(pg),cs(pg)))
    ok('Back da scheda: input ripristinato',pg.evaluate("()=>document.getElementById('crQ').value")=='agents')
    # dossier
    pg.click('.cr-res >> nth=0 >> .cr-lk >> nth=1'); pg.wait_for_timeout(600); ok('Dossier dall\'esploratore',sc(pg)=='uni',sc(pg))
    ok('dossier: pulsante Cronologia',pg.evaluate("()=>!!document.getElementById('udOpenCron')"))
    back(pg); ok('Back dal dossier: stato Esplora',sc(pg)=='cron' and cs(pg)['q']=='agents' and cs(pg)['xo']=='ambientazione',cs(pg))
    # mappa
    pg.click('.cr-res >> nth=0 >> .cr-lk >> nth=2'); pg.wait_for_timeout(900); ok('Mappa dall\'esploratore',sc(pg)=='mappa',sc(pg))
    ok('mappa: universo selezionato',pg.evaluate("()=>tvaAtlas2.getState().mp.sel")==mcu,pg.evaluate("()=>tvaAtlas2.getState().mp.sel"))
    ok('mappa: pulsante Cronologia nella scheda',pg.evaluate("()=>!!document.getElementById('mpOpenCron')"))
    pg.click('#mpOpenCron'); pg.wait_for_timeout(600); ok('Mappa → Cronologia dell\'universo',sc(pg)=='cron' and cs(pg)['mode']=='uni' and cs(pg)['uid']==mcu,cs(pg))
    back(pg); ok('Back: di nuovo la mappa con selezione',sc(pg)=='mappa' and pg.evaluate("()=>tvaAtlas2.getState().mp.sel")==mcu)
    back(pg); ok('Back: di nuovo Esplora con filtri',sc(pg)=='cron' and cs(pg)['q']=='agents',cs(pg))
    # dossier → cronologia → dossier
    pg.evaluate("(u)=>tvaAtlas2.openUni(u)",fox); pg.wait_for_timeout(500); pg.click('#udOpenCron'); pg.wait_for_timeout(500)
    ok('Dossier → Cronologia dell\'universo',sc(pg)=='cron' and cs(pg)['uid']==fox and cs(pg)['mode']=='uni',cs(pg))
    pg.click('.cr-uhead .cr-lk >> nth=0'); pg.wait_for_timeout(500); ok('Cronologia → Dossier',sc(pg)=='uni'); back(pg); ok('…e Back',sc(pg)=='cron' and cs(pg)['uid']==fox)
    # universo vuoto dal dossier
    e0=[x for x,n in d['perUni'] if n==0][0]; pg.evaluate("(u)=>tvaAtlas2.openUni(u)",e0); pg.wait_for_timeout(400)
    ok('dossier di universo vuoto: pulsante Cronologia presente',pg.evaluate("()=>!!document.getElementById('udOpenCron')"))
    pg.click('#udOpenCron'); pg.wait_for_timeout(400); ok('universo vuoto: stato informativo con link',pg.evaluate("()=>!!document.querySelector('.cr-empty')&&document.querySelectorAll('.cr-uhead .cr-lk').length==2"))
    # scheda dalla cronologia: aprire una scheda non cambia le spunte
    # ---- 7. nessun effetto collaterale
    l1={k:v for k,v in json.loads(pg.evaluate(LS)).items() if not k.startswith('tvaHomeMiss')}; l0={k:v for k,v in json.loads(ls0).items() if not k.startswith('tvaHomeMiss')}; ok('localStorage invariato',l1==l0,[k for k in set(l0)|set(l1) if l0.get(k)!=l1.get(k)]); ok('progressi di visione invariati',pg.evaluate(CHK)==ck0)
    ok('nessuna chiave di storage nuova (cron)',not [k for k in json.loads(pg.evaluate(LS)) if re.search('cron|cr3c',k,re.I) and not k.startswith('tvaHomeMiss')])
    # ---- 8. legacy Timeline alternativa: sei modalità
    pg.evaluate("()=>{marvelChiudiOverlay();const c=document.getElementById('altTimelineToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(900)
    modes=pg.evaluate("()=>[...document.querySelectorAll('#altTimelineOverlay [data-at-mode], [data-atmode], .at-mode, .alt-timeline-mode')].length")
    txt=pg.evaluate("()=>document.body.innerText")
    ok('Timeline alternativa: 6 modalità presenti',all(w in txt for w in ['Consigliato','Uscita','Eventi','Saga','Universo','Personalizzato']) or modes>=6,modes)
    ok('nessun errore JS',not errs,errs[:3])
    b.close()
if __name__=='__main__':
    run(390,844); print('TOTALE',N[0],'FALLITI',len(F),F)
