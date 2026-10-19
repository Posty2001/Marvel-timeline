from f4lib import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    ids=pg.evaluate("()=>Object.keys(tvaIdx.personaggi)")
    ok('C1 304 personaggi',len(ids)==304,len(ids))
    bad=[];empty=[];jump=[];lost=[];order=[];ov=[];single=0
    for cid in ids:
        pg.evaluate("(c)=>tvaGo('char',c)",cid); pg.wait_for_timeout(30)
        r=pg.evaluate("""(cid)=>{const b=document.querySelector('.d4-char'); if(!b) return {no:1};
          const secs=[...b.querySelectorAll('.d4-sec')].map(s=>({id:s.getAttribute('data-d4sec'),n:s.children.length,txt:s.innerText.trim().length}));
          const jb=[...b.querySelectorAll('[data-d4j]')].map(x=>x.getAttribute('data-d4j'));
          const apps=[...b.querySelectorAll('.d4-app')].map(x=>x.getAttribute('data-go').slice(5));
          // N° citati nelle righe APP. della scheda originale
          const li=tvaIdx.personaggi[cid].li; const rows=[...li.querySelectorAll('.detail-row')].filter(r=>/APP\\./.test(r.querySelector('.detail-k').textContent));
          const want=new Set(); rows.forEach(r=>{const re=/N°(\\d{3})/g;let m;while((m=re.exec(r.textContent))){const id=marvelIdDaNumeroVisibile(m[1]);if(tvaIdx.titoli['item-'+id])want.add('item-'+id)}});
          const guide=[...document.querySelectorAll('li.card-wrap[id^="item-"]')].map(l=>l.id);
          const idxs=apps.map(a=>guide.indexOf(a));
          return {secs,jb,apps,want:[...want],sorted:idxs.every((v,i)=>i==0||idxs[i-1]<v),ov:document.documentElement.scrollWidth>innerWidth}}""",cid)
        if r.get('no'): bad.append(cid); continue
        for s in r['secs']:
            if s['n']<2 or s['txt']<6: empty.append((cid,s))
        secids={s['id'] for s in r['secs']}
        for j in r['jb']:
            if j not in secids: jump.append((cid,j))
        miss=[w for w in r['want'] if w not in r['apps']]
        if miss: lost.append((cid,miss))
        if not r['sorted']: order.append(cid)
        if r['ov']: ov.append(cid)
        if len(r['apps'])<=1: single+=1
    ok('C2 ogni personaggio apre il dossier senza errori',bad==[],bad[:5])
    ok('C3 nessuna sezione vuota',empty==[],empty[:5])
    ok('C4 nessun tab/salto senza contenuto',jump==[],jump[:5])
    ok('C5 nessuna apparizione persa rispetto alle righe PRIMA/ULTIMA/ALTRE APP.',lost==[],lost[:5])
    ok('C6 percorso in ordine di guida',order==[],order[:5])
    ok('C7 nessun overflow orizzontale',ov==[],ov[:5])
    print('personaggi con <=1 apparizione:',single)
    ok('C8 nessun errore JS',errs==[],errs[:3])
    b.close()
done()
