from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{
      const ch=[...document.querySelectorAll('details.card[id^=char-],li[id^=char-]')];
      const h={};ch.forEach(c=>c.querySelectorAll('.detail-k').forEach(k=>{const t=k.textContent.trim();h[t]=(h[t]||0)+1}));
      const ex=document.getElementById('char-ajak')||ch[0];
      const sample=ex?ex.innerText.slice(0,900):'';
      const t=txt=>[...document.querySelectorAll('details.card')].find(c=>(c.querySelector('.title')||{}).textContent.trim().startsWith(txt));
      return {n:ch.length,h,sample,
        forte:(t('Chi è più forte?')||{}).innerText?.slice(0,3500),
        manca:(t('Chi manca')||{}).innerText?.slice(0,2500),
        ruolo:(t('Il ruolo delle entit')||{}).innerText?.slice(0,1800)}}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)); b.close()
