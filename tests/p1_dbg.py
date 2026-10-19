from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,has_touch=True,is_mobile=True); pg=ctx.new_page()
    pg.goto(F); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(500)
    pg.add_style_tag(content=":root{--sat:47px !important;--sab:34px !important}")
    pg.evaluate("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(400)
    print(pg.evaluate("()=>{const a=document.getElementById('atlas2').getBoundingClientRect(),t=document.querySelector('.a2-top').getBoundingClientRect();return [a.top,a.height,t.top,t.height,innerHeight, getComputedStyle(document.documentElement).paddingTop, getComputedStyle(document.body).paddingTop]}"))
    b.close()
