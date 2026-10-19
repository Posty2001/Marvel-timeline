import json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{const o={};
     ['multiverse-graph-overlay','universe-timeline-overlay','relationship-graph-overlay','kang-tva-overlay','alt-timeline-overlay','tva-archives-overlay','info-overlay'].forEach(c=>{const e=document.querySelector('.'+c);o[c]=e?[e.id,(e.querySelector('h1,h2,.overlay-title,[class*=title]')||{}).textContent,(e.textContent||'').trim().slice(0,90)]:null});
     const ph=[...document.querySelectorAll('.part-head h2')].map(h=>h.textContent.trim());
     const head=[...document.querySelectorAll('.part-head')].find(h=>/Cronologie Tematiche/.test(h.textContent));const ul=head.nextElementSibling;
     o.cronTit=[...ul.querySelectorAll(':scope > li.card-wrap > details > summary .title')].map(t=>t.textContent.trim());
     o.cronLi=[...ul.querySelectorAll(':scope > li.card-wrap')].map(l=>l.id||'-');
     o.parts=ph;
     o.tabsArch=[...document.querySelectorAll('.atlas-tile-tab')].map(t=>[t.dataset.tab,t.textContent.trim().replace(/\\s+/g,' ')]);
     o.art=[...document.querySelectorAll('li[id^="art-"]')].slice(0,3).map(l=>l.id).concat([document.querySelectorAll('li[id^="art-"]').length]);
     o.gemId=[...document.querySelectorAll('li.card-wrap')].filter(l=>/Gemme dell/.test((l.querySelector('.title')||{}).textContent||'')).map(l=>[l.id,l.closest('.tva-archives-overlay')?'arch':'main',(l.querySelector('.title')||{}).textContent]);
     o.hubBtns=[...document.querySelectorAll('.home-hub-nav > *')].map(e=>e.textContent.trim().slice(0,22));
     o.hubChildren=[...document.querySelector('.home-hub-inner').children].map(e=>e.className||e.tagName);
     o.sott=[...new Set(JSON.parse(document.getElementById('atlasData').textContent).personaggi.map(c=>c.sottotipo))];
     o.atlasKeys=Object.keys(JSON.parse(document.getElementById('atlasData').textContent));
     return o}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)[:4500]); b.close()
