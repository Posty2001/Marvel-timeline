from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{
      const f=[...document.querySelectorAll('details.card')].find(c=>(c.querySelector('.title')||{}).textContent.trim()==='Chi è più forte?');
      const IDX=tvaAtlas2.ext.api.IDX;
      const th=document.getElementById('char-thanos');
      const rows={};th.querySelectorAll('.detail-row').forEach(r=>rows[r.querySelector('.detail-k').textContent.trim()]=r.querySelector('.detail-v').textContent.trim().slice(0,400));
      const sample=Object.keys(IDX.personaggi).slice(0,1).map(k=>[k,Object.keys(IDX.personaggi[k])]);
            return {html:f.innerHTML.slice(0,2600),rows,sample,apps:IDX.personaggi['char-thanos'].apps}}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)); b.close()
