from playwright.sync_api import sync_playwright
import json,re
F='file:///home/claude/work/index.html'
res=[]
def ok(n,c,d=''): res.append(c); print('PASS' if c else 'FAIL',n,d)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if (m.type=='error' and 'ERR_TUNNEL' not in m.text) else None)
    pg.goto(F); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{const d=JSON.parse(document.getElementById('mvMapData').textContent);const U=d.universi;
      const g=id=>document.getElementById('item-'+id).getAttribute('data-uni');
      return {u120:g('120'),u134:g('134'),u125:g('125'),n:Object.keys(U).length,mcu:U['uni-earth-199999-mcu'],nu:U['uni-your-friendly-neighborhood-spider-man-verse'],fam:d.famiglie.animazione.universi,
       card:!!document.getElementById('uni-your-friendly-neighborhood-spider-man-verse'),
       cardsUni:[...document.querySelectorAll('.card-wrap[id^=uni-]')].length,
       anim:/MCU \\(animata\\)/.test(document.documentElement.innerHTML)}}""")
    ok('data-uni 120/134',r['u120']==r['u134']=='uni-your-friendly-neighborhood-spider-man-verse',(r['u120'],r['u134']))
    ok('125 multi-uni invariato',r['u125']=='uni-earth-199999-mcu uni-earth-828')
    ok('27 universi (26 + FF 1994), card Atlante presente, nessuna etichetta MCU (animata)',r['n']==27 and r['card'] and r['cardsUni']==27 and not r['anim'],(r['n'],r['cardsUni']))
    m=r['mcu']; ids=m['titoliIds']
    ok('MCU: ids senza 120/134, titoli=len, serie/film',('120' not in ids) and ('134' not in ids) and m['titoli']==len(ids)==93 and m['serie']==53 and m['film']==40 and m['serie']+m['film']==93,(m['titoli'],m['serie'],m['film'],m['personaggi']))
    nu=r['nu']; ok('nuovo universo',nu['titoliIds']==['120','134'] and nu['titoli']==2 and nu['serie']==2 and nu['personaggi']==3 and 'animazione' and True)
    ok('famiglia animazione include il nuovo',r['fam'][1]=='uni-your-friendly-neighborhood-spider-man-verse',r['fam'])
    # tutti i titoli di ogni universo hanno data-uni coerente
    bad=pg.evaluate("""()=>{const d=JSON.parse(document.getElementById('mvMapData').textContent).universi;const out=[];
      for(const [u,x] of Object.entries(d)){for(const id of x.titoliIds||[]){const a=(document.getElementById('item-'+id).getAttribute('data-uni')||'').split(' ');if(!a.includes(u))out.push([u,id])}}
      document.querySelectorAll('[data-uni][data-item]:not([data-variant-of])').forEach(li=>{li.getAttribute('data-uni').split(' ').forEach(u=>{if(!(d[u]&&(d[u].titoliIds||[]).includes(li.dataset.item)))out.push(['rev',u,li.dataset.item])})});return out}""")
    ok('data-uni <-> titoliIds coerenti (entrambe le direzioni)',bad==[],bad[:6])
    # Esplora universo
    pg.evaluate("()=>window.marvelEsploraUniverso('uni-your-friendly-neighborhood-spider-man-verse','YFNS')"); pg.wait_for_timeout(500)
    vis=pg.evaluate("()=>[...document.querySelectorAll('li.card-wrap[data-item]')].filter(l=>l.style.display!=='none').map(l=>l.dataset.item)")
    ok('Esplora nuovo universo mostra 120,134',vis==['120','134'],vis)
    pg.evaluate("()=>window.marvelEsploraUniverso('uni-earth-199999-mcu','MCU')"); pg.wait_for_timeout(500)
    vis=pg.evaluate("()=>[...document.querySelectorAll('li.card-wrap[data-item]')].filter(l=>l.style.display!=='none').map(l=>l.dataset.item)")
    ok('Esplora MCU: 93 autonomi (+ variante Encore), senza 120/134',len([v for v in vis if v!='133'])==93 and '120' not in vis and '134' not in vis,len(vis))
    for uid,exp in (('uni-fantastic-four-1994',['028']),('uni-earth-121698',['029','030']),('uni-earth-trn123',['031']),('uni-earth-828',['125'])):
        pg.evaluate("(u)=>window.marvelEsploraUniverso(u,u)",uid); pg.wait_for_timeout(400)
        vis=pg.evaluate("()=>[...document.querySelectorAll('li.card-wrap[data-item]')].filter(l=>l.style.display!=='none').map(l=>l.dataset.item)")
        ok('Esplora %s separato: %s'%(uid,exp),vis==exp,vis)
    # calendario
    cal=pg.evaluate("""()=>{const o=document.documentElement.innerHTML;return {rel:/"release": "2027-01-13"/.test(o)}}""")
    ok('release 134 nei dati',cal['rel'])
    ok('no errori JS',errs==[],errs[:3])
    b.close()
# calendario reale: apri vista
print('ALL' if all(res) else 'FAILED')
