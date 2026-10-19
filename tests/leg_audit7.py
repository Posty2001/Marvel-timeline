from playwright.sync_api import sync_playwright
from leg_shot import boot
import json,re,collections
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const T={};Object.keys(tvaIdx.titoli).forEach(k=>{const e=tvaIdx.titoli[k];if(/^item-\\d{3}$/.test(k))T[k.slice(5)]=e.title});
      const out=[];document.querySelectorAll('#tvaArchivesOverlayEl li[id^="org-"],li[id^="art-"],li[id^="evt-"],li[id^="bat-"],li[id^="pia-"],li[id^="luo-"]').forEach(li=>{
        li.querySelectorAll('.detail-row:not(.tva-row)').forEach(r=>{const k=r.querySelector('.detail-k').textContent.trim();if(k==='COMPARE IN'||k==='TITOLI')out.push([li.id,r.querySelector('.detail-v').textContent.trim()])})});
      return {T,out}}""")
    T=r['T']; 
    def norm(s): return re.sub(r'[^a-z0-9]','',s.lower().replace('&amp;','&').replace('&','and'))
    byn={norm(v):k for k,v in T.items()}
    pairs=[]
    for id,v in r['out']:
        m=re.match(r'^((?:N°\d{3}(?:,\s*)?)+)\s*—\s*(.+)$',v)
        if m:
            nums=re.findall(r'\d{3}',m.group(1)); names=re.split(r',\s*(?=[A-Z])',m.group(2))
            if len(nums)==len(names):
                for n,nm in zip(nums,names):
                    nm=re.sub(r'\s*\(\d{4}\)','',nm).strip()
                    real=byn.get(norm(nm)); pairs.append((id,n,nm,real))
    for p_ in pairs: print(p_, 'delta', (int(p_[3])-int(p_[1])) if p_[3] else None)
    b.close()
