from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{
      const cards=[...document.querySelectorAll('details.card')];
      const byPre={};cards.forEach(c=>{const id=(c.closest('[id]')||{}).id||c.id||'';const p=id.replace(/-.*/,'');byPre[p]=(byPre[p]||0)+1});
      const find=re=>cards.filter(c=>re.test((c.querySelector('.title')||{}).textContent||'')).map(c=>[(c.id||c.parentElement.id),(c.querySelector('.title')||{}).textContent.trim().slice(0,70)]);
      const IDX=tvaAtlas2.ext.api.IDX;
      return {byPre,total:cards.length,fort:find(/forte|manca|potere|poteri|cosmic|entit|specie|razz|civilt|magi|mistic|arcan|stregon/i),
        persKeys:Object.keys(IDX),
        pk:Object.fromEntries(Object.entries(IDX).map(([k,v])=>[k,typeof v+":"+(Array.isArray(v)?v.length:Object.keys(v||{}).slice(0,8).join(","))]))}}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)[:3500]); b.close()
