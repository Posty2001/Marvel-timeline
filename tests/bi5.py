import json
from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); pg.goto(F); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{const li=document.getElementById('item-133');const I=tvaIdx.titoli['item-133'];
      return {title:li.querySelector('.title').textContent,rows:[...li.querySelectorAll('.detail-row')].map(r=>(r.querySelector('.detail-k')||{}).textContent+' = '+((r.querySelector('.detail-v')||{}).textContent||'').slice(0,120)),variant:I.variant,unis:I.unis,
       prim:(()=>{const a=JSON.parse(document.getElementById('atlasData').textContent);const ex={};a.opere.filter(o=>o.ruolo==='primario').forEach(o=>{const n=o.universi.length;ex[n]=(ex[n]||0)+1});return ex})(),
       vcount:Object.values(tvaIdx.titoli).filter(t=>t.variant).map(t=>t.id)}}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)); b.close()
