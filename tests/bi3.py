import json,sys
from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); pg.goto(F); pg.wait_for_timeout(1500)
    r=pg.evaluate("""(uid)=>{const a=JSON.parse(document.getElementById('atlasData').textContent);const mv=JSON.parse(document.getElementById('mvMapData').textContent);
      const u=mv.universi[uid]; const au=a.universi.find(x=>x.id===uid);
      const op=a.opere.filter(o=>o.universi.includes(uid));
      const ch=a.personaggi.filter(c=>c.appartenenza.includes(uid));
      return {mv:u,au,opere:op.map(o=>[o.id,o.ruolo,o.ambientazione,o.universi.join(','),o.note||'']),nch:ch.length,
        origin:ch.filter(c=>(c.continuitaOrigine||[]).includes(uid)).map(c=>c.id),
        notOrigin:ch.filter(c=>!(c.continuitaOrigine||[]).includes(uid)).map(c=>c.id).slice(0,30),
        keysOpera:Object.keys(a.opere[0]),nota:a.nota}}""", sys.argv[1])
    print(json.dumps(r,indent=1,ensure_ascii=False)[:6000]); b.close()
