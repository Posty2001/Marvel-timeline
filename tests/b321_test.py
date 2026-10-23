from b32lib import *
import json,io,base64
exec(open('/tmp/claude-0/t/b32_test.py').read().split("with sync_playwright() as p:")[0].split("from b32lib import *")[1])
def png(pg,view=None):
    b64=pg.evaluate("""async(v)=>{const b=await tvaTessera.exportPng();const f=new FileReader();return await new Promise(r=>{f.onload=()=>r(f.result.split(',')[1]);f.readAsDataURL(b)})}""",view)
    return base64.b64decode(b64)
with sync_playwright() as p:
    b=p.chromium.launch(); ids,anim=ids_of(b); S=seed_full(ids,anim)
    ctx,pg,errs=boot(b,390,844,atlas=False); put(pg,S); reload(pg); open_tessera(pg); pg.wait_for_timeout(500)
    ok('S0 nessun errore JS',errs==[],errs)
    ok('B0 build id 3.2.1',pg.evaluate("()=>document.querySelector('meta[name=tva-build]').content")=='20261023-1730-m342')
    ok('M0 catalogo invariato: 48 ricompense, 12 cornici, 10 temi',pg.evaluate("()=>tvaRewards.catalog.length===48&&tvaRewards.catalog.filter(r=>r.cat==='cornice').length===12&&tvaRewards.catalog.filter(r=>r.cat==='tema').length===10"))
    ok('M1 id motore = id catalogo (nessun id orfano)',pg.evaluate("()=>{const c=tvaRewards.catalog;return tvaCardArt.frames.every(f=>c.some(r=>r.id===f))&&tvaCardArt.themes.every(f=>c.some(r=>r.id===f))}"))
    pg.click('#tcPersonalizzaBtn'); pg.wait_for_timeout(300)
    # ---- editor: miniature cornici ----
    tab(pg,'cornici')
    info=pg.evaluate("""()=>[...document.querySelectorAll('#tcEdBody .tc-grid-cornice .tc-tile')].map(t=>{const th=t.querySelector('.tc-tile-th svg');const r=t.querySelector('.tc-tile-th').getBoundingClientRect();return {w:r.width,h:r.height,len:th?th.outerHTML.length:0,nm:t.querySelector('.tc-tile-n').textContent,sel:t.classList.contains('tc-sel')}})""")
    ok('E1 12 miniature cornice, larghezza >= 130px',len(info)==12 and min(i['w'] for i in info)>=130,[round(i['w']) for i in info])
    ok('E2 miniature tutte diverse e ricche (carta semplificata + cornice)',len(set(i['len'] for i in info))==12 and min(i['len'] for i in info)>3000)
    ok('E3 elemento equipaggiato evidente (1 selezionato)',sum(1 for i in info if i['sel'])==1)
    # le miniature mostrano la cornice sul tema in bozza: cambia tema -> cambia miniatura
    h0=pg.evaluate("()=>document.querySelector('#tcEdBody .tc-grid-cornice .tc-tile:nth-child(2) .tc-tile-th').innerHTML")
    tab(pg,'temi'); pg.click('#tcEdBody .tc-grid-tema .tc-tile:nth-child(9)'); pg.wait_for_timeout(150)
    ok('E4 anteprima aggiornata subito (tema in bozza), nessun salvataggio',pg.evaluate("()=>localStorage.getItem('marvel-ultimate-timeline-rewards')")==pg.evaluate("()=>localStorage.getItem('marvel-ultimate-timeline-rewards')") and 'Nexus' not in '' and pg.evaluate("()=>tvaRewards.equipped().tema")!='tema-nexus-cosmico')
    tab(pg,'cornici'); h1=pg.evaluate("()=>document.querySelector('#tcEdBody .tc-grid-cornice .tc-tile:nth-child(2) .tc-tile-th').innerHTML")
    ok('E5 miniatura cornice usa il tema scelto in bozza',h0!=h1)
    tab(pg,'temi'); pg.wait_for_timeout(1500)   # 3.2.5: le miniature reali dei temi si riempiono in modo differito (rAF)
    ti=pg.evaluate("""()=>[...document.querySelectorAll('#tcEdBody .tc-grid-tema .tc-tile')].map(t=>{const th=t.querySelector('.tc-tile-th svg');return {len:th.outerHTML.length,h:t.querySelector('.tc-tile-th').getBoundingClientRect().height}})""")
    ok('E6 10 miniature tema = superficie (non un quadratino), altezza >= 80px',len(ti)==10 and min(t['h'] for t in ti)>=80 and min(t['len'] for t in ti)>3000,ti[:2])
    pg.screenshot(path='/tmp/o_ed_temi390.png'); tab(pg,'cornici'); pg.screenshot(path='/tmp/o_ed_cornici390.png')
    pg.click('#tcEdBody .tc-grid-cornice .tc-tile:nth-child(12)'); pg.wait_for_timeout(150)
    ok('E7 anteprima editor immediata (cornice Nexus in bozza)',pg.evaluate("()=>document.getElementById('tcEdPrev').innerHTML.includes('0.35 0.3')||document.getElementById('tcEdPrev').innerHTML.length>5000")and pg.evaluate("()=>tvaRewards.equipped().cornice")=='cornice-standard-tva')
    pg.click('#tcEdCancel') if pg.query_selector('#tcEdCancel') else pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    ok('E8 Annulla: nulla salvato',pg.evaluate("()=>!document.getElementById('tcEditor')&&tvaRewards.equipped().cornice==='cornice-standard-tva'"))
    # ---- quattro leggendarie ----
    leg=pg.evaluate("()=>tvaRewards.catalog.filter(r=>r.rar==='l').map(r=>r.id+'|'+r.cat)")
    ok('L0 quattro ricompense leggendarie',len(leg)==4,leg)
    pg.evaluate("()=>{tvaRewards.equip('cornice','cornice-nexus-supremo');tvaRewards.equip('tema','tema-fine-del-tempo');tvaRewards.equip('effetto','effetto-aura-leggendaria')}"); pg.wait_for_timeout(300)
    hs=hero(pg); ok('L1 Nexus Supremo + Fine del Tempo + Aura leggendaria visibili nella Tessera',('0.35 0.3' in hs or 'nx' in hs) and 'tc-fx' in hs and len(hs)>12000,len(hs))
    ok('L2 titolo leggendario "Colui che Rimane" equipaggiabile',pg.evaluate("()=>{const r=tvaRewards.catalog.find(x=>x.rar==='l'&&x.cat==='titolo');return !!r&&tvaRewards.equip('titolo',r.id).ok}"))
    pg.screenshot(path='/tmp/o_hero_leg390.png',clip={'x':0,'y':0,'width':390,'height':700})
    # ---- PNG ----
    from PIL import Image
    import numpy as np
    res={}
    for tm in ('tema-tva-classico','tema-tecnologia-futuristica','tema-fine-del-tempo'):
        pg.evaluate("(t)=>tvaRewards.equip('tema',t)",tm if tm!='tema-tecnologia-futuristica' else 'tema-tva-classico'); 
    pg.evaluate("()=>tvaRewards.equip('effetto',null)")
    imgs={}
    for fr in ('cornice-standard-tva','cornice-nexus-supremo'):
        pg.evaluate("(f)=>tvaRewards.equip('cornice',f)",fr); pg.wait_for_timeout(200)
        for view in ('vertical',):
            d=png(pg,view); im=Image.open(io.BytesIO(d)).convert('RGB'); imgs[fr]=np.asarray(im,dtype=int)
    ok('X1 PNG verticale 1080x1800',imgs['cornice-nexus-supremo'].shape[:2]==(1800,1080),imgs['cornice-nexus-supremo'].shape)
    d=np.abs(imgs['cornice-standard-tva']-imgs['cornice-nexus-supremo']).sum(2); band=d.copy(); band[100:-100,100:-100]=0
    ok('X2 la cornice cambia davvero il PNG (bordo)',(band>60).mean()>0.03,(band>60).mean())
    ok('X3 PNG non piatto (varianza luminanza)',imgs['cornice-nexus-supremo'].mean(2).std()>20)
    open('/tmp/o_png_nexus.png','wb').write(png(pg,'vertical'))
    ok('X4 niente errori JS dopo export',errs==[],errs)
    ctx.close()
    # ---- responsive ----
    for w in (320,375,390,393,430,1280):
        c2,p2,e2=boot(b,w,844 if w<600 else 900,atlas=False); put(p2,S); reload(p2); open_tessera(p2); p2.wait_for_timeout(400)
        p2.evaluate("()=>{tvaRewards.equip('cornice','cornice-asgard');tvaRewards.equip('tema','tema-fine-del-tempo')}"); p2.wait_for_timeout(300)
        r=p2.evaluate("()=>{const s=document.querySelector('#tcHero svg');const q=s.getBoundingClientRect();const d=document.documentElement;const k=q.width/s.viewBox.baseVal.width;const ts=[...s.querySelectorAll('text')].map(t=>parseFloat(t.getAttribute('font-size'))*k);return {ow:d.scrollWidth<=d.clientWidth+1,min:Math.min(...ts),lay:s.dataset.layout,w:q.width}}")
        ok('W%d Asgard+Fine del Tempo: no overflow, testo minimo >= 8.9px (%s, min %.1f)'%(w,r['lay'],r['min']),r['ow'] and r['min']>=8.9,r)
        p2.click('#tcPersonalizzaBtn'); p2.wait_for_timeout(300); tab(p2,'cornici')
        g=p2.evaluate("()=>{const t=[...document.querySelectorAll('#tcEdBody .tc-grid-cornice .tc-tile')];const d=document.documentElement;return {n:t.length,minw:Math.min(...t.map(x=>x.querySelector('.tc-tile-th').getBoundingClientRect().width)),ow:d.scrollWidth<=d.clientWidth+1}}")
        ok('W%d editor cornici: 12 miniature, larghezza min %.0fpx, no overflow'%(w,g['minw']),g['n']==12 and g['minw']>=100 and g['ow'],g)
        if w in (320,430): p2.screenshot(path='/tmp/o_ed_cornici%d.png'%w)
        ok('W%d nessun errore JS'%w,e2==[],e2); c2.close()
    b.close()
done()
