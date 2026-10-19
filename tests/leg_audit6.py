from playwright.sync_api import sync_playwright
from leg_shot import boot
import json,re,collections
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>[...document.querySelectorAll('#tvaArchivesOverlayEl li[id^="org-"],li[id^="art-"],li[id^="evt-"],li[id^="bat-"],li[id^="pia-"],li[id^="luo-"]')].map(li=>({id:li.id,f:Object.fromEntries([...li.querySelectorAll('.detail-row')].filter(r=>!r.classList.contains('tva-row')).map(r=>[r.querySelector('.detail-k')?.textContent.trim(),r.querySelector('.detail-v')?.textContent.trim()]))}))""")
    fmt=collections.Counter()
    for x in r:
        for k in ('COMPARE IN','TITOLI'):
            v=x['f'].get(k)
            if v: fmt[(x['id'].split('-')[0],k,re.sub(r'\d{3}','NNN',v)[:40])]+=1
    for k,v in sorted(fmt.items(), key=lambda z:-z[1])[:30]: print(v,k)
    for x in r:
        if x['id'] in ('art-mjolnir','org-hydra','evt-il-blip','pia-vormir','luo-wakanda','evt-battaglia-finale-contro-thanos'): print(json.dumps(x,ensure_ascii=False)[:700])
    b.close()
