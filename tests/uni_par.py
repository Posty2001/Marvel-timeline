from playwright.sync_api import sync_playwright
from leg_shot import boot
import json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const A=tvaAtlas2;const norm=s=>s.toLowerCase().replace(/[^a-z0-9à-ù]+/g,' ').trim();const out={};
      const ids=[...document.querySelectorAll('#tvaArchivesOverlayEl li[id^="uni-"]')].map(l=>l.id);
      for(const id of ids){const li=document.getElementById(id);const rows=[...li.querySelectorAll('.detail-row')].map(r=>({k:(r.querySelector('.detail-k')||{}).textContent.trim(),v:(r.querySelector('.detail-v')||{}).textContent.replace(/\\s+/g,' ').trim()}));
        A.openUni(id); const t=norm(document.getElementById('atlas2').textContent);
        rows.forEach(r=>{ if(!r.v) return; const toks=norm(r.v).split(' ').filter(w=>w.length>3); const hit=toks.filter(w=>t.includes(w)).length; const ratio=toks.length?hit/toks.length:1; if(ratio<0.8){(out[r.k]=out[r.k]||[]).push([id,ratio.toFixed(2),r.v.slice(0,90)])} });}
      return {n:ids.length,miss:Object.fromEntries(Object.entries(out).map(([k,v])=>[k,[v.length,v.slice(0,2)]]))}}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)); print(errs)
    b.close()
