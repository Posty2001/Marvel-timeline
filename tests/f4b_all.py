from f4lib import *
import json,re
h=open('/home/claude/work/index.html',encoding='utf-8').read()
ATL=json.loads(re.search(r'<script[^>]*id="atlasData"[^>]*>(.*?)</script>',h,re.S).group(1))
OP={o['id']:o for o in ATL['opere']}
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    ids=pg.evaluate("()=>Object.keys(tvaIdx.titoli)")
    ok('B20 tutti i titoli indicizzati (139 item + 37 anim + p4)',len([i for i in ids if i.startswith('item-')])==139 and len([i for i in ids if i.startswith('anim-')])==37,len(ids))
    bad=[];empty=[];axes=[];nav=[]
    for i in ids:
        pg.evaluate("(i)=>tvaGo('item',i)",i); pg.wait_for_timeout(35)
        r=pg.evaluate("""()=>{const b=document.querySelector('.a2-opera'); if(!b) return {no:1};
          const secs=[...b.querySelectorAll('.d4-sec')].map(s=>({id:s.getAttribute('data-d4sec'),n:s.children.length,txt:s.innerText.trim().length}));
          return {secs,h:b.querySelector('h2').innerText,ax:[...b.querySelectorAll('.d4-ax-v')].map(x=>x.innerText),title:document.querySelector('#item-023')&&0,
            chips:[...b.querySelectorAll('[data-go]')].map(x=>x.getAttribute('data-go')),ov:document.documentElement.scrollWidth>innerWidth}}""")
        if r.get('no'): bad.append(i); continue
        for s in r['secs']:
            if s['n']<2 or s['txt']<8: empty.append((i,s))
        if r['ov']: bad.append(('overflowX',i))
        # chip validi
        for c in r['chips']:
            k,_,v=c.partition(':')
            if k=='item' and v not in ids: bad.append(('chip',i,c))
        if i.startswith('item-'):
            m=OP.get(i[5:])
            if m:
                exp=m['ambientazione']; got=r['ax'][2] if len(r['ax'])>2 else None
                if got!=exp: axes.append((i,'ambi',got,exp))
    ok('B21 ogni titolo apre un Dossier Opera (nessun fallimento/overflow/chip rotto)',bad==[],bad[:6])
    ok('B22 nessuna sezione vuota',empty==[],empty[:6])
    ok('B23 ambientazione = atlasData per tutte le opere',axes==[],axes[:5])
    # assi uscita/guida
    r=pg.evaluate("""()=>{const bad=[];const M=['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre'];
      Object.keys(tvaIdx.titoli).filter(k=>/^item-\\d{3}$/.test(k)&&!tvaIdx.titoli[k].variant).forEach(k=>{const o=tvaXref.opera(k);const e=tvaIdx.titoli[k];
        const vis=marvelNumeroVisibile(e.num); if(o.guida.vis!==vis) bad.push(['vis',k,o.guida.vis,vis]);
        const rec=e.li.querySelector('.rec').textContent.replace(/\\D/g,''); if(rec!==vis) bad.push(['rec',k,rec,vis]);
        });
      return bad.slice(0,8)}""")
    ok('B24 N° visibile e posizione = helper della guida per tutti i 138 titoli',r==[],r)
    # prima/dopo = ordine DOM
    r=pg.evaluate("""()=>{const dom=[...document.querySelectorAll('li.card-wrap[id^="item-"]')].filter(l=>!l.classList.contains('card-variant')).map(l=>l.id);const bad=[];
      dom.forEach((id,i)=>{const o=tvaXref.opera(id);if(o.guida.prec!==(dom[i-1]||null))bad.push(['prec',id]);if(o.guida.succ!==(dom[i+1]||null))bad.push(['succ',id]);});return {n:dom.length,bad:bad.slice(0,6)}}""")
    ok('B25 prima/dopo = ordine del documento (guida) per tutti',r['bad']==[] and r['n']==138,r)
    # ordine uscita / ambientazione invariati: gli assi sono letti, non riordinano nulla
    ok('B26 nessun errore JS',errs==[],errs[:3])
    b.close()
done()
