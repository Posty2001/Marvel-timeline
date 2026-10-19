import json,sys
from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); pg.goto(F); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{const a=JSON.parse(document.getElementById('atlasData').textContent);
      const rows=a.universi.map(u=>{const op=a.opere.filter(o=>o.universi.includes(u.id));const ch=a.personaggi.filter(c=>c.appartenenza.includes(u.id));
        const orig=ch.filter(c=>(c.continuitaOrigine||[]).includes(u.id)).length;
        return [u.id.replace('uni-',''),op.filter(o=>o.ruolo==='primario').length,op.filter(o=>o.ruolo==='crossover').length,op.filter(o=>o.ruolo==='variante').length,ch.length,orig]});
      const ff=a.personaggi.filter(c=>['char-reed-richards','char-sue-storm','char-ben-grimm','char-johnny-storm-human-torch','char-galactus','char-franklin-richards'].includes(c.id)).map(c=>[c.id,c.appartenenza,c.continuitaOrigine,c.dubbio,c.assegnazione]);
      const cr=a.opere.filter(o=>o.ruolo!=='primario').map(o=>[o.id,o.ruolo,o.universi.join(','),o.ambientazione]);
      const noOrigin=a.personaggi.filter(c=>!(c.continuitaOrigine||[]).length).length;
      const orMulti=a.personaggi.filter(c=>(c.continuitaOrigine||[]).length>1).length;
      return {rows,ff,cr,noOrigin,orMulti}}""")
    print(json.dumps(r,ensure_ascii=False)); b.close()
