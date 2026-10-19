from playwright.sync_api import sync_playwright
from leg_shot import boot
import json,collections
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const out={keys:{},n:0,sample:null,attKeys:{},attSample:null};
      const lis=[...document.querySelectorAll('#tvaArchivesOverlayEl li[id^="char-"]')];out.n=lis.length;
      lis.forEach(li=>{li.querySelectorAll('.detail-row,.comic-box,.read-box,h4,.detail-section').forEach(r=>{const k=(r.querySelector('.detail-k')||r).className+'|'+((r.querySelector('.detail-k')||{}).textContent||'').trim().slice(0,24);out.keys[k]=(out.keys[k]||0)+1})});
      out.sample=lis[10].outerHTML.replace(/\\s+/g,' ').slice(0,3500);
      const at=[...document.querySelectorAll('#tvaArchivesOverlayEl li[id^="att-"]')];
      at.forEach(li=>li.querySelectorAll('.detail-row').forEach(r=>{const k=r.querySelector('.detail-k').textContent.trim();out.attKeys[k]=(out.attKeys[k]||0)+1}));
      out.attSample=at[3].outerHTML.replace(/\\s+/g,' ').slice(0,1800);
      return out}""")
    print(r['n']); print(json.dumps(r['keys'],ensure_ascii=False)); print(r['sample']); print(); print(r['attKeys']); print(r['attSample'])
    b.close()
