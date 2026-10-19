from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,has_touch=True,is_mobile=True); pg=ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.goto(F); pg.wait_for_timeout(1500)
    pg.add_style_tag(content=":root{--sat:47px !important;--sab:34px !important}")
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(800); pg.screenshot(path='q_home0.png')
    print('entry', pg.evaluate("()=>!!document.getElementById('a2Entry')"))
    pg.evaluate("()=>{const e=document.getElementById('a2Entry'); if(e) e.scrollIntoView({block:'center'})}"); pg.wait_for_timeout(300); pg.screenshot(path='q_home1.png')
    pg.evaluate("()=>document.getElementById('a2Entry').click()"); pg.wait_for_timeout(600)
    print('tabbar display', pg.evaluate("()=>getComputedStyle(document.getElementById('appTabbar')).display"), 'sidebtn', pg.evaluate("()=>getComputedStyle(document.querySelector('.sidebar-open-btn')).display"))
    pg.screenshot(path='q_a2home.png')
    pg.evaluate("()=>{document.querySelector('.a2-scroll').scrollTop=520}"); pg.wait_for_timeout(200); pg.screenshot(path='q_a2home2.png')
    pg.evaluate("()=>{document.querySelector('.a2-all').click()}"); pg.wait_for_timeout(300); pg.screenshot(path='q_cat.png')
    print(errs)
    b.close()
