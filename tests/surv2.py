from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    print(pg.evaluate("()=>{const A=JSON.parse(document.getElementById('atlasData').textContent);return Object.keys(A).map(k=>[k,Array.isArray(A[k])?A[k].length:typeof A[k]])}"))
    r=pg.evaluate("""()=>{const o={};['org-s-h-i-e-l-d','org-tva-time-variance-authority','art-gemma-della-mente','art-mjolnir','evt-il-blip','bat-battaglia-di-new-york','luo-wakanda','pia-vormir'].forEach(id=>{const li=document.getElementById(id);o[id]=[...li.querySelectorAll('.detail-row')].map(r=>r.textContent.slice(0,420)+' || html:'+r.querySelector('.detail-v').innerHTML.slice(0,300))});return o}""")
    for k,v in r.items():
        print('==',k)
        for x in v: print('  ',x)
    b.close()
