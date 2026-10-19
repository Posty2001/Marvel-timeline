import json
from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); pg.goto(F); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{const a=JSON.parse(document.getElementById('atlasData').textContent);
      const c=document.getElementById('char-blade');
      const rows=[...c.querySelectorAll('.detail-row')].map(r=>(r.querySelector('.detail-k')||{}).textContent+' = '+((r.querySelector('.detail-v')||{}).textContent||'').slice(0,100)+' ['+r.querySelectorAll('[data-go]').length+' go]');
      const p=a.personaggi.find(x=>x.id==='char-blade'||x.nome==='Blade');
      const cnt={}; document.querySelectorAll('li[id^="char-"]').forEach(li=>{const has=[...li.querySelectorAll('.detail-k')].map(k=>k.textContent.trim());has.forEach(k=>cnt[k]=(cnt[k]||0)+1)});
      return {rows,p,cnt,keys:Object.keys(a.personaggi[0])}}""")
    print(json.dumps(r,indent=1,ensure_ascii=False)); b.close()
