from b32lib import *
import json,io,base64,glob
exec(open('/tmp/claude-0/t/b32_test.py').read().split("with sync_playwright() as p:")[0].split("from b32lib import *")[1])
from PIL import Image
import numpy as np
OUT='/home/claude/outputs/sprint_blocco3_2_6/'
IDS=['agente','variante','esploratore','tecnologico','mistico','astratto','cronista','sentinella']
def heroImgs(pg): return pg.evaluate("()=>{const h=document.getElementById('tcHero').innerHTML;return (h.match(/data:image\\/webp/g)||[]).length}")
def setav(pg,i): pg.evaluate("(i)=>{localStorage.setItem('marvel-ultimate-timeline-tessera-look',JSON.stringify({v:1,a:i,ts:Date.now()}))}",i)
with sync_playwright() as p:
    b=p.chromium.launch(); ids,anim=ids_of(b); S=seed_full(ids,anim)
    # ---- file asset
    for n in IDS:
        im=Image.open('/home/claude/work/assets/avatars/%s.webp'%n); sz=len(open('/home/claude/work/assets/avatars/%s.webp'%n,'rb').read())
        ok('A1 asset %s: >=720 px, 4:5, <=120 KB (%d KB)'%(n,sz//1024),im.size[0]>=720 and im.size[1]*4==im.size[0]*5 and sz<=120*1024,(im.size,sz))
    ctx,pg,errs=boot(b,390,844,atlas=False); put(pg,S); setav(pg,'agente'); reload(pg); open_tessera(pg); pg.wait_for_timeout(1200)
    ok('A2 loader: 8 ritratti caricati',sorted(pg.evaluate("()=>tvaCardArt.avatarArt.loaded()"))==sorted(IDS),pg.evaluate("()=>tvaCardArt.avatarArt.loaded()"))
    ok('A3 hero usa il ritratto WebP (agente)',heroImgs(pg)>=1)
    # Cronista -> fallback
    setav(pg,'cronista'); reload(pg); open_tessera(pg); pg.wait_for_timeout(1200)
    ok('A4 Cronista: ritratto WebP',heroImgs(pg)>=1)
    # ---- editor
    setav(pg,'agente'); reload(pg); open_tessera(pg); pg.wait_for_timeout(1000)
    pg.click('#tcPersonalizzaBtn'); pg.wait_for_timeout(400); tab(pg,'avatar')
    tiles=pg.evaluate("()=>[...document.querySelectorAll('#tcEdBody .tc-tile')].map(t=>[t.querySelector('.tc-tile-n')?.textContent,(t.innerHTML.match(/data:image\\/jpeg/g)||[]).length,(t.innerHTML.match(/data:image\\/webp/g)||[]).length,t.innerHTML.length])")
    ok('E1 editor: 8 avatar con miniatura leggera (JPEG 160x200, solo href (3.2.5: xlink omesso nelle miniature leggere), nessun WebP completo nel DOM)',len(tiles)>=8 and sum(1 for t in tiles if t[1]==1)==8 and all(t[2]==0 for t in tiles) and max(t[3] for t in tiles)<40000,tiles)
    pg.evaluate("()=>[...document.querySelectorAll('#tcEdBody .tc-tile')].find(t=>/Variante/.test(t.textContent)).click()"); pg.wait_for_timeout(400)
    ok('E2 anteprima immediata: la hero mostra la bozza (immagine) prima del salvataggio',heroImgs(pg)>=1)
    sv=pg.evaluate("()=>JSON.parse(localStorage.getItem('marvel-ultimate-timeline-tessera-look')||'{}').a")
    ok('E3 bozza NON salvata finche non si preme Salva (look ancora agente)',sv=='agente',sv)
    pg.click('#tcEdCancel'); pg.wait_for_timeout(400)
    ok('E4 Annulla: look invariato',pg.evaluate("()=>JSON.parse(localStorage.getItem('marvel-ultimate-timeline-tessera-look')||'{}').a")=='agente')
    pg.click('#tcPersonalizzaBtn'); pg.wait_for_timeout(400); tab(pg,'avatar')
    pg.evaluate("()=>[...document.querySelectorAll('#tcEdBody .tc-tile')].find(t=>/Sentinella/.test(t.textContent)).click()"); pg.wait_for_timeout(300)
    pg.click('#tcEdSave'); pg.wait_for_timeout(500)
    ok('E5 Salva: look = sentinella',pg.evaluate("()=>JSON.parse(localStorage.getItem('marvel-ultimate-timeline-tessera-look')||'{}').a")=='sentinella')
    reload(pg); open_tessera(pg); pg.wait_for_timeout(1200)
    ok('E6 persistenza dopo ricarica: Sentinella con ritratto',pg.evaluate("()=>JSON.parse(localStorage.getItem('marvel-ultimate-timeline-tessera-look')||'{}').a")=='sentinella' and heroImgs(pg)>=1)
    # ---- verticale + export
    r=pg.evaluate("""async()=>{const svg=tvaTessera.buildSvg('vertical');const w=(svg.match(/data:image\\/webp/g)||[]).length;
      const blob=await tvaTessera.exportPng();const bm=await createImageBitmap(blob);
      const url='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg);const img=await new Promise((ok,ko)=>{const i=new Image();i.onload=()=>ok(i);i.onerror=ko;i.src=url});
      const W=540,H=900;const c=document.createElement('canvas');c.width=W;c.height=H;const x=c.getContext('2d');x.drawImage(img,0,0,W,H);const a=x.getImageData(0,0,W,H).data;
      const c2=document.createElement('canvas');c2.width=W;c2.height=H;const y=c2.getContext('2d');y.drawImage(bm,0,0,W,H);const d=y.getImageData(0,0,W,H).data;let s=0;for(let i=0;i<a.length;i+=4)s+=Math.abs(a[i]-d[i])+Math.abs(a[i+1]-d[i+1])+Math.abs(a[i+2]-d[i+2]);
      const f=new FileReader();const b64=await new Promise(r=>{f.onload=()=>r(f.result.split(',')[1]);f.readAsDataURL(blob)});
      return {w:bm.width,h:bm.height,kb:Math.round(blob.size/1024),imgs:w,diff:s/(W*H*3),b64}}""")
    open(OUT+'esempio_PNG_esportato_sentinella.png','wb').write(base64.b64decode(r['b64']))
    ok('X1 export: 1080x1800 con ritratto incorporato (data URL, nessuna risorsa esterna)',r['w']==1080 and r['h']==1800 and r['imgs']>=1,{k:v for k,v in r.items() if k!='b64'})
    ok('X2 export fedele all anteprima (differenza media per canale < 4)',r['diff']<4,r['diff'])
    ok('X3 peso PNG < 2.5 MB (misurato: %d KB)'%r['kb'],r['kb']<2560,r['kb'])
    print('PNG_KB',r['kb'],'DIFF',round(r['diff'],3))
    ok('X4 nessun errore JS',errs==[],errs); ctx.close()
    # ---- fallback: asset 404 / corrotto
    ctx=b.new_context(viewport={'width':390,'height':844},is_mobile=True,service_workers='block'); pg=ctx.new_page(); errs2=[]; pg.on('pageerror',lambda e:errs2.append(str(e)))
    pg.route('**/assets/avatars/agente.webp',lambda r:r.fulfill(status=404,body='')); pg.route('**/assets/avatars/variante.webp',lambda r:r.fulfill(status=200,content_type='image/webp',body=b'corrotto'))
    pg.route('**/assets/avatars/mistico.webp',lambda r:r.abort())
    pg.goto('http://127.0.0.1:8124/index.html'); pg.wait_for_timeout(1200)
    ld=pg.evaluate("()=>tvaCardArt.avatarArt.loaded()")
    ok('F1 404 / file corrotto / rete interrotta: solo gli asset validi caricati, gli altri in fallback',sorted(ld)==sorted(['esploratore','tecnologico','astratto','cronista','sentinella']),ld)
    ok('F2 nessun errore JS con asset mancanti',errs2==[],errs2); ctx.close()
    # ---- offline con Service Worker (precache)
    ctx=b.new_context(viewport={'width':390,'height':844},is_mobile=True); pg=ctx.new_page(); errs3=[]; pg.on('pageerror',lambda e:errs3.append(str(e)))
    pg.goto('http://127.0.0.1:8124/index.html'); pg.wait_for_timeout(2500)
    sw=pg.evaluate("async()=>{const r=await navigator.serviceWorker.getRegistration();if(!r)return 'noreg';await navigator.serviceWorker.ready;const c=await caches.open('marvel-timeline-cache-'+document.querySelector('meta[name=tva-build]').content);const ks=(await c.keys()).map(k=>new URL(k.url).pathname);return ks.filter(k=>/assets\\/avatars/.test(k))}")
    # C5/C3: la cache e' ora nominata con la build (era 'marvel-timeline-cache-v9'); l'aspettativa (8 ritratti in precache) non cambia
    ok('O1 Service Worker: 8 ritratti nella cache (precache)',isinstance(sw,list) and len(sw)==8,sw)
    ctx.set_offline(True)
    try:
        pg.reload(); pg.wait_for_timeout(2500)
        ld=pg.evaluate("()=>tvaCardArt.avatarArt.loaded()")
        ok('O2 offline: pagina e 8 ritratti disponibili da cache',sorted(ld)==sorted(IDS),ld)
    except Exception as e:
        ok('O2 offline: ricarica non riuscita',False,str(e)[:200])
    ok('O3 nessun errore JS offline',errs3==[],errs3); ctx.close(); b.close()
done()
