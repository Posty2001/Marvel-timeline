from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844},has_touch=True,is_mobile=True); pg=ctx.new_page(); pg.goto(F); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;tvaAtlas2.openHome()}"); pg.wait_for_timeout(300)
    print(pg.evaluate("""()=>{const sc=document.querySelector('.a2-scroll');const o=[];document.querySelectorAll('#atlas2 *').forEach(e=>{const r=e.getBoundingClientRect();if(r.right>innerWidth+0.5&&r.width>0)o.push([e.tagName,e.className&&e.className.baseVal===undefined?e.className:'svg',Math.round(r.right)])});return [sc.scrollWidth,sc.clientWidth,o.slice(0,8)]}"""))
    b.close()
