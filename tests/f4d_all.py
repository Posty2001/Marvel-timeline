from f4lib import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    L=pg.evaluate("()=>tvaAtlas2.arcModel().list.map(e=>[e.cat,e.id])")
    ok('D1 voci d\'archivio indicizzate (>=90)',len(L)>=90,len(L))
    bad=[];empty=[];jump=[];skin=[];ov=[];d4bad=[];d4n=0
    for cat,i in L:
        pg.evaluate("(i)=>tvaGo('arc',i)",cat+':'+i); pg.wait_for_timeout(30)
        r=pg.evaluate("""(a)=>{const b=document.querySelector('.a2-dossier'); if(!b||tvaAtlas2.getState().screen!=='dossier') return {no:1};
          const secs=[...b.querySelectorAll(':scope > section.a2-sec:not(.a2-foot)')].map(s=>({id:s.getAttribute('data-d4sec'),n:s.children.length,txt:s.innerText.trim().length}));
          const jb=[...b.querySelectorAll('[data-d4j]')].map(x=>x.getAttribute('data-d4j'));
          const d4=[...b.querySelectorAll('[data-d4sec="nome"] [data-go^="item:"]')].map(x=>x.getAttribute('data-go').slice(5));
          return {secs,jb,sk:b.classList.contains('d4-skin-'+a),d4,ov:document.documentElement.scrollWidth>innerWidth}}""",cat)
        if r.get('no'): bad.append(i); continue
        for s in r['secs']:
            if s['n']<2 or s['txt']<6: empty.append((i,s))
        ids={s['id'] for s in r['secs']}
        for j in r['jb']:
            if j not in ids: jump.append((i,j))
        if not r['sk']: skin.append(i)
        if r['ov']: ov.append(i)
        if r['d4']:
            d4n+=len(r['d4'])
            if cat!='org': d4bad.append((i,'D4 fuori dalle organizzazioni'))
            for t in r['d4']:
                ok_=pg.evaluate("""([o,t])=>{const e=tvaAtlas2.arcModel().byId[o];const n=s=>' '+s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase().replace(/&/g,' and ').replace(/\\./g,'').replace(/[^a-z0-9]+/g,' ').trim()+' ';
                  const title=n(tvaIdx.titoli[t].title);const base=e.name.replace(/\\s*\\([^)]*\\)/g,'');const vs=[base,...base.split('/'),...(e.name.match(/\\(([^)]*)\\)/g)||[]).map(x=>x.slice(1,-1))].map(n).filter(x=>x.trim().length>=4);
                  return vs.some(v=>title.indexOf(v)!==-1) && e.titles.indexOf(t)===-1;}""",[i,t])
                if not ok_: d4bad.append((i,t))
    ok('D2 ogni dossier d\'archivio si apre',bad==[],bad[:5])
    ok('D3 nessuna sezione vuota',empty==[],empty[:5])
    ok('D4 nessun salto senza sezione',jump==[],jump[:5])
    ok('D5 skin per tipo applicata',skin==[],skin[:5])
    ok('D6 nessun overflow orizzontale',ov==[],ov[:5])
    ok('D7 sezione «nome nel titolo»: solo org, solo titoli col nome, mai quelli gia\' confermati',d4bad==[],d4bad[:5])
    print('titoli D4 mostrati:',d4n)
    ok('D8 nessun errore JS',errs==[],errs[:3])
    # D4 etichettata come corrispondenza del titolo
    pg.evaluate("()=>tvaGo('arc','org:org-s-h-i-e-l-d')"); pg.wait_for_timeout(400)
    t=pg.evaluate("()=>document.querySelector('[data-d4sec=\"nome\"]').innerText")
    ok('D9 D4 dichiarata come corrispondenza del titolo, non relazione',('Corrispondenza del titolo' in t) and ('non è un’apparizione' in t or 'Non è un’apparizione' in t),t[-220:])
    b.close()
done()
