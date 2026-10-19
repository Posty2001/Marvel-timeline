import json
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const c={},ex=[];Object.entries(tvaIdx.titoli).forEach(([k,t])=>{c[t.kind]=(c[t.kind]||0)+1;if(t.kind!=='item'&&t.kind!=='anim')ex.push(k+'|'+t.title+'|'+t.num)});return {c,ex,n:Object.keys(tvaIdx.titoli).length}}""")
    print(json.dumps(r,ensure_ascii=False)); b.close()
