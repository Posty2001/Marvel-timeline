from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{
      const out={};
      document.querySelectorAll('#tvaArchivesOverlayEl [id]').forEach(e=>{const m=e.id.match(/^([a-z]+)-/);if(m&&e.tagName==='LI'){out[m[1]]=(out[m[1]]||0)+1}});
      return out}""")
    print(r)
    # ids per prefix + keys
    r=pg.evaluate("""()=>{
      const res={};
      document.querySelectorAll('#tvaArchivesOverlayEl li[id]').forEach(li=>{
        const m=li.id.match(/^([a-z]+)-/); if(!m)return; const k=m[1];
        if(!['org','art','evt','bat','pia','luo','uni'].includes(k))return;
        const rows=[...li.querySelectorAll('.detail-row')].map(r=>(r.querySelector('.detail-k')||{}).textContent);
        (res[k]=res[k]||[]).push([li.id,(li.querySelector('.title')||{}).textContent,rows.join('|')]);
      });
      return res}""")
    for k,v in r.items():
        print('==',k,len(v))
        for x in v[:20]: print(x)
    b.close()
