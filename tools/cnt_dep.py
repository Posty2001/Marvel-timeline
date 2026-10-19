import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for f in sys.argv[1:]:
        pg=b.new_page(); pg.goto('file://'+f); pg.wait_for_timeout(1200)
        print(f.split('/')[-1],pg.evaluate("()=>{var r={};document.querySelectorAll('[class*=dep-]').forEach(e=>e.className.split(/\\s+/).forEach(c=>{if(c.indexOf('dep-')===0)r[c]=(r[c]||0)+1}));r._tot=document.querySelectorAll('[class*=dep-]').length;return r}"))
        pg.close()
