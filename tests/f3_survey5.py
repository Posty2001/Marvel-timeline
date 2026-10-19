from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{
      const m=[...document.querySelectorAll('details.card')].find(c=>c.innerText.includes('Chi manca ancora'));
      const subs=[...m.querySelectorAll('details.sub-group')].map(s=>{const sm=s.querySelector('summary').textContent.trim();
        const tiers=[...s.querySelectorAll('.cosmic-tier')].map(t=>[t.querySelector('h4').textContent.trim(),[...t.querySelectorAll('.cosmic-card-name')].map(x=>x.textContent.trim())]);
        const other=s.querySelector('.sub-group-body').innerText.slice(0,500);
        return {sm,tiers,other:tiers.length?'':other}});
      const cap=[...document.querySelectorAll('details.card')].filter(c=>/^cap0|^item-0|^char|^uni|^org|^art|^att|^pia|^luo|^evt|^bat|^cronologie|^p4|^anim/.test(c.id)===false).map(c=>(c.querySelector('.title')||{}).textContent.trim().slice(0,70));
      return {subs,cap}}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)); b.close()
