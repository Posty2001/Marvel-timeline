from f4lib import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    ids=pg.evaluate("()=>tvaXref.attori().list.map(a=>a.id)"); ok('C20 49 attori indicizzati',len(ids)==49,len(ids))
    bad=[];ord_=[];empty=[]
    for i in ids:
        pg.evaluate("(c)=>tvaGo('att',c)",i); pg.wait_for_timeout(40)
        r=pg.evaluate("""(i)=>{const b=document.querySelector('.a2-att.a2-dossier'); if(!b) return {no:1}; const e=tvaXref.attori().byId[i];
          const ch=[...b.querySelectorAll('.d4-sec[data-d4sec="film"] [data-go^="item:"]')].map(x=>x.getAttribute('data-go').slice(5));
          const secs=[...b.querySelectorAll('.d4-sec')].map(s=>({n:s.children.length,txt:s.innerText.trim().length}));
          const guide=[...document.querySelectorAll('li.card-wrap[id^="item-"]')].map(l=>l.id);
          return {t:e.titles.length,ch,secs,sorted:e.titles.every((v,k)=>k==0||guide.indexOf(e.titles[k-1])<guide.indexOf(v))}}""",i)
        if r.get('no'): bad.append(i); continue
        if r['t']>1 and not r['ch']: empty.append(i)
        if not r['sorted']: ord_.append(i)
        for s in r['secs']:
            if s['n']<2 or s['txt']<6: empty.append((i,s))
    ok('C21 ogni scheda attore si apre',bad==[],bad)
    ok('C22 filmografia presente se >1 titolo, nessuna sezione vuota',empty==[],empty[:4])
    ok('C23 titoli in ordine di guida',ord_==[],ord_)
    # bidirezionalita' opera <-> attore, opera <-> personaggio
    r=pg.evaluate("""()=>{const bad=[];const AT=tvaXref.attori();
      Object.keys(tvaIdx.titoli).forEach(t=>{ (AT.byTitle[t]||[]).forEach(a=>{ if(AT.byId[a].titles.indexOf(t)===-1) bad.push(['att',t,a]); }); });
      AT.list.forEach(a=>a.titles.forEach(t=>{ if((AT.byTitle[t]||[]).indexOf(a.id)===-1) bad.push(['att2',a.id,t]); }));
      Object.keys(tvaIdx.itemChars).forEach(t=>tvaIdx.itemChars[t].forEach(c=>{ if(tvaIdx.personaggi[c].apps.indexOf(t)===-1) bad.push(['chr',t,c]); }));
      Object.keys(tvaIdx.personaggi).forEach(c=>tvaIdx.personaggi[c].apps.forEach(t=>{ if((tvaIdx.itemChars[t]||[]).indexOf(c)===-1) bad.push(['chr2',c,t]); }));
      return bad.slice(0,6)}""")
    ok('C24 bidirezionalita\' opera<->attore e opera<->personaggio',r==[],r)
    # ricerca per cognome attore porta alla scheda attore
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('search')"); pg.fill('#a2Search','jackman'); pg.wait_for_timeout(400)
    pg.locator('.d4-res-att .a2-chip').first.click(); pg.wait_for_timeout(400)
    ok('C25 ricerca attore -> scheda attore',pg.evaluate("()=>tvaAtlas2.getState().screen")=='attore')
    ok('C26 nessun errore JS',errs==[],errs[:3])
    b.close()
done()
