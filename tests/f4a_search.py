from f4lib import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    def S(q): return pg.evaluate("(q)=>{const r=tvaXref.cerca(q);return r.gruppi.map(g=>({t:g.tipo,l:g.lbl,v:g.voci.map(x=>x.name)}))}",q)
    def names(q,t=None):
        r=S(q); out=[]
        for g in r:
            if t is None or g['t']==t: out+=g['v']
        return out
    ok('shield -> S.H.I.E.L.D. (Organizzazioni)',any('S.H.I.E.L.D' in n for n in names('shield','org')),S('shield'))
    ok('S.H.I.E.L.D. con punti -> org',any('S.H.I.E.L.D' in n for n in names('S.H.I.E.L.D.','org')))
    ok('shield trova anche titoli Agents of S.H.I.E.L.D.',any('S.H.I.E.L.D' in n for n in names('shield','tit')),names('shield','tit'))
    ok('jackman -> attore Hugh Jackman',any('Jackman' in n for n in names('jackman','att')),S('jackman'))
    ok('nyong -> Lupita (attori)',any('Nyong' in n for n in names('nyong','att')),S('nyong'))
    ok('realta senza accento = realtà (accenti ignorati)',names('realta')==names('realtà') and any('Realtà' in n for n in names('realta')),(names('realta')[:3],names('realtà')[:3]))
    ok('wakanda trova luoghi/titoli',len(names('wakanda'))>0,S('wakanda'))
    ok('x men = xmen = X-Men',set(names('x men','tit'))==set(names('xmen','tit'))==set(names('X-Men','tit')) and len(names('xmen','tit'))>=10,(len(names('x men','tit')),len(names('xmen','tit'))))
    ok('spiderman = spider-man',set(names('spiderman','tit'))==set(names('spider man','tit')) and len(names('spiderman','tit'))>3)
    ok('deadpool wolverine (senza &) trova D&W',any('Deadpool & Wolverine' in n for n in names('deadpool wolverine','tit')),names('deadpool wolverine','tit'))
    ok('deadpool and wolverine / deadpool e wolverine',any('Deadpool & Wolverine' in n for n in names('deadpool and wolverine','tit')) and any('Deadpool & Wolverine' in n for n in names('deadpool e wolverine','tit')))
    ok('MAIUSCOLE ignorate',names('LOGAN')==names('logan'))
    ok('risultati distinti per tipologia (gruppi separati, nessun mix)',all(len(set(g['t'] for g in [x]))==1 for x in S('loki')) and len(S('loki'))>=2,[g['l'] for g in S('loki')])
    ok('1 carattere = nessun risultato',S('l')==[])
    # regressione: tutto cio' che trovava la vecchia ricerca (sottostringa esatta) e' ancora trovato
    r=pg.evaluate("""()=>{
      const A=tvaAtlas2.ext.api, M=tvaAtlas2.arcModel(); const bad=[]; let nq=0;
      const sets={tit:A.titoliBase().map(e=>[e.id,e.title]),chr:A.personaggiLista().map(c=>[c.id,c.name]),uni:Object.keys(A.UNI).map(u=>[u,A.UNI[u].nome||u]),arc:M.list.map(e=>[e.id,e.name])};
      const queries=new Set();
      Object.values(sets).forEach(l=>l.forEach(([i,n])=>{const w=n.toLowerCase().split(/\\s+/);queries.add(w[0]);if(w[1])queries.add(w.slice(0,2).join(' '));queries.add(n.toLowerCase());}));
      queries.forEach(q=>{ if(q.length<2) return; nq++;
        const R=tvaXref.cerca(q); const got=new Set(); R.gruppi.forEach(g=>g.voci.forEach(v=>got.add(v.t+':'+v.id)));
        sets.tit.forEach(([i,n])=>{ if(n.toLowerCase().indexOf(q)!==-1 && !got.has('tit:'+i)) bad.push(['tit',q,n]); });
        sets.chr.forEach(([i,n])=>{ if(n.toLowerCase().indexOf(q)!==-1 && !got.has('chr:'+i)) bad.push(['chr',q,n]); });
        sets.uni.forEach(([i,n])=>{ if(n.toLowerCase().indexOf(q)!==-1 && !got.has('uni:'+i)) bad.push(['uni',q,n]); });
        sets.arc.forEach(([i,n])=>{ if(n.toLowerCase().indexOf(q)!==-1 && ![...got].some(x=>x.endsWith(':'+i))) bad.push(['arc',q,n]); });
      }); return {nq,bad:bad.slice(0,10),nbad:bad.length}; }""")
    ok('regressione ricerca: nessun risultato vecchio perso (%d query)'%r['nq'],r['nbad']==0,r)
    # UI
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('search')"); pg.wait_for_timeout(300)
    pg.fill('#a2Search','shield'); pg.wait_for_timeout(500)
    txt=pg.evaluate("()=>document.querySelector('.a2-res').innerText")
    ok('UI: gruppi con conteggio e filtri',('Organizzazioni' in txt) and pg.locator('.d4-tf-b').count()>=2,txt[:300])
    pg.screenshot(path='f4_search1.png')
    pg.click('.d4-tf-b:has-text("Organizzazioni")'); pg.wait_for_timeout(300)
    ok('UI: filtro per tipo mostra un solo gruppo',pg.locator('.a2-res .a2-resbox').count()==1)
    ok('UI: bersagli >=44px',pg.evaluate("()=>[...document.querySelectorAll('.d4-tf-b,.a2-res .a2-chip')].every(b=>b.getBoundingClientRect().height>=43.5)"))
    pg.fill('#a2Search','zzzzqq'); pg.wait_for_timeout(400)
    ok('UI: stato vuoto onesto',pg.locator('.a2-empty').count()==1)
    pg.fill('#a2Search','616'); pg.wait_for_timeout(400)
    ok('UI: nota 616 conservata',pg.evaluate("()=>document.querySelector('.a2-res').innerText.includes('Earth-616')"))
    ok('nessun errore JS',errs==[],errs)
    b.close()
done()
