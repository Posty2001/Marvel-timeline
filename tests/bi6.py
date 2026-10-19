import json
from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); pg.goto(F); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{const a=JSON.parse(document.getElementById('atlasData').textContent);const out=[];
      a.personaggi.forEach(c=>{(c.continuitaOrigine||[]).forEach(u=>{if(!c.appartenenza.includes(u))out.push(c.id+' origin '+u)})});
      const dub=a.personaggi.filter(c=>(c.dubbio||[]).length).map(c=>[c.id,c.dubbio]);
      const ass=a.personaggi.filter(c=>c.assegnazione).map(c=>[c.id,c.assegnazione]).slice(0,5);
      const prod=a.personaggi.filter(c=>c.produzioneMarvelStudios).length;
      return {outOnly:out,n:out.length,dub:dub.slice(0,10),ndub:dub.length,ass,prod,stato:[...new Set(a.personaggi.map(c=>c.stato))],tipo:[...new Set(a.personaggi.map(c=>c.tipo))],conta:a.personaggi.filter(c=>!c.conta).length}}""")
    print(json.dumps(r,ensure_ascii=False)[:2500]); b.close()
