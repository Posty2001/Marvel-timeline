from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,has_touch=True,is_mobile=True); pg=ctx.new_page(); pg.goto(F); pg.wait_for_timeout(1300)
    pg.add_style_tag(content=":root{--sat:47px !important;--sab:34px !important}")
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;tvaAtlas2.openUni('uni-earth-828',true)}"); pg.wait_for_timeout(400)
    pg.evaluate("()=>document.querySelector('.a2-legend').open=true"); pg.wait_for_timeout(200)
    pg.screenshot(path='c_828_a.png')
    pg.evaluate("()=>{document.querySelector('.a2-scroll').scrollTop=620}"); pg.wait_for_timeout(200); pg.screenshot(path='c_828_b.png')
    pg.evaluate("()=>{tvaAtlas2.openUni('uni-earth-199999-mcu',true)}"); pg.wait_for_timeout(300); pg.screenshot(path='c_mcu_a.png')
    b.close()
