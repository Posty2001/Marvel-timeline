import sys
from playwright.sync_api import sync_playwright
F=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':320,'height':568},has_touch=True,is_mobile=True); pg=ctx.new_page(); pg.goto(F); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;['item-125','item-099'].forEach(i=>{const d=document.getElementById(i).querySelector('details');d.open=true})}"); pg.wait_for_timeout(400)
    print(sys.argv[1][-30:],pg.evaluate("""()=>{const o=[];document.querySelectorAll('body *').forEach(e=>{if(e.offsetParent===null)return;const r=e.getBoundingClientRect();if(r.right>321&&r.width>0&&!e.closest('.tva-archives-overlay'))o.push([e.tagName,(e.className||'').toString().slice(0,40),e.id,Math.round(r.right)])});return [document.documentElement.scrollWidth,o.slice(0,8)]}"""))
    b.close()
