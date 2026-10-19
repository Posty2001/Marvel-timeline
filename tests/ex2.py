import json,collections
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{const A=JSON.parse(document.getElementById('atlasData').textContent);
     const pre={};document.querySelectorAll('.tva-archives-overlay li.card-wrap[id]').forEach(l=>{const k=l.id.split('-')[0];pre[k]=(pre[k]||0)+1});
     const tipo={};A.personaggi.forEach(c=>{const k=c.tipo+'|'+c.conta;tipo[k]=(tipo[k]||0)+1});
     const nc=A.personaggi.filter(c=>c.conta===false||c.tipo!=='personaggio').map(c=>c.id).slice(0,12);
     const varN=A.personaggi.filter(c=>/variant/.test(c.sottotipo||'')).length;
     const toggles=[...document.querySelectorAll('input[id$="Toggle"]')].map(i=>i.id);
     return {pre,tipo,nc,varN,toggles,items:Object.values(tvaIdx.titoli).filter(t=>t.kind==='item'&&!t.variant).length,anim:Object.values(tvaIdx.titoli).filter(t=>t.kind==='anim').length}}""")
    print(json.dumps(r,ensure_ascii=False)); b.close()
