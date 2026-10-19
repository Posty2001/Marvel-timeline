from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{const M=tvaAtlas2.arcModel();const o={};
      for(const c of ['org','art','evt','luo','cos','spe','mis']) o[c]=M.cat[c].length;
      o.det={};
      for(const c of ['cos','spe','mis']) o.det[c]=M.cat[c].map(e=>[e.id,e.sub,e.titles.length,e.chars.length,e.arcs.length,e.cited.length,(e.byChars||[]).length+'/'+(e.byArcs||[]).length,e.limiti.length]);
      return o}""")
    print(json.dumps(r,ensure_ascii=False)); print(errs[:5]); b.close()
