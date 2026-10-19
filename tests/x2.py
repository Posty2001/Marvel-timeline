import json
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>[...document.querySelectorAll('#sec-1d ~ ul.items:first-of-type li.card-wrap, h3#sec-1d + ul.items li.card-wrap')].map(l=>[l.id,l.dataset.item,(l.textContent.match(/N°(\\d+)/)||[])[1],tvaIdx.titoli[l.id]&&tvaIdx.titoli[l.id].num,l.querySelector('.card-title,.card-head')?.textContent.replace(/\\s+/g,' ').slice(0,60)])""")
    for x in r: print(x)
    print(pg.evaluate("()=>[...document.querySelectorAll('li.card-wrap[data-item]')].filter(l=>{const m=l.textContent.match(/N°(\\d+)/);return m&&m[1]!==l.dataset.item}).map(l=>l.dataset.item+'->'+l.textContent.match(/N°(\\d+)/)[1]).join(' ')"))
    b.close()
