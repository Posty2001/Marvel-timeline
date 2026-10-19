import json,re
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{
 const M=tvaAtlas2.arcModel? tvaAtlas2.arcModel():null; const o={has:!!M};
 if(M){o.keys=Object.keys(M); const cats=M.cats||M.categorie||null; o.catkeys=cats?Object.keys(cats):null;
  const evt=(M.byCat&&M.byCat.evt)||(cats&&cats.evt&&cats.evt.items)||[]; o.evt_n=evt.length; o.evt0=evt[0]?JSON.stringify(evt[0]).slice(0,500):null; o.evt_keys=evt[0]?Object.keys(evt[0]):null;}
 const UM=tvaUniverse; o.multi=UM.ids().map(id=>UM.get(id)).reduce((a,g)=>{g.crossover.forEach(t=>a[t.id]=(a[t.id]||[]).concat(g.nome));return a},{});
 const ms=UM.get('uni-earth-199999-mcu'); o.eventiMCU=ms.eventiChiave; o.mvEv=JSON.parse(document.getElementById('mvMapData').textContent).universi['uni-earth-199999-mcu'].eventi;
 o.mvKeys=Object.keys(JSON.parse(document.getElementById('mvMapData').textContent)); 
 return o}""")
    print(json.dumps(r,ensure_ascii=False)[:3500]); b.close()
