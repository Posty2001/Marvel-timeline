from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{
      const IDX=tvaAtlas2.ext.api.IDX, out=[];
      const t7=new Set([...document.querySelectorAll('.pyramid-tier-7 .power-chip')].map(a=>a.getAttribute('onclick').match(/'(char-[^']+)'/)[1]));
      const t6=new Set([...document.querySelectorAll('.pyramid-tier-6 .power-chip')].map(a=>a.getAttribute('onclick').match(/'(char-[^']+)'/)[1]));
      Object.keys(IDX.personaggi).forEach(id=>{const c=IDX.personaggi[id];const f={};c.li.querySelectorAll('.detail-row').forEach(r=>{const k=r.querySelector('.detail-k');const v=r.querySelector('.detail-v');if(k&&v)f[k.textContent.trim()]=v.textContent.trim()});
        const txt=(f['POTERI']||'')+' || '+(f['📚 NEI FUMETTI']||'');
        const m=/entit[àa]\\b|celestial|personificazion|essere cosmic|cosmic[oa]\\b|cosmici/i.exec(txt);
        if(m||t7.has(id)) out.push([id,t7.has(id)?7:(t6.has(id)?6:0),m?txt.slice(Math.max(0,m.index-50),m.index+80):'']);});
      return out}""")
    for x in r: print(x)
    b.close()
