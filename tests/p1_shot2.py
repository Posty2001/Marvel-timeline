from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,has_touch=True,is_mobile=True); pg=ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(F); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(500)
    pg.add_style_tag(content=":root{--sat:47px !important;--sab:34px !important}")
    pg.evaluate("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(400)
    def sc(n,y=0):
        pg.evaluate(f"()=>{{document.querySelector('.a2-scroll').scrollTop={y}}}"); pg.wait_for_timeout(200); pg.screenshot(path=f'q_{n}.png')
    sc('h_b',900)
    sc('h_c',1700)
    pg.evaluate("()=>document.querySelector('.a2-all').click()"); pg.wait_for_timeout(300); sc('cat1'); sc('cat2',700)
    pg.evaluate("()=>document.querySelector('[data-sez=cosmiche]').click()"); pg.wait_for_timeout(300); sc('soon')
    pg.evaluate("()=>tvaAtlas2.enter()"); 
    pg.evaluate("()=>document.querySelector('[data-tile=personaggi]').click()"); pg.wait_for_timeout(300); sc('pers')
    pg.evaluate("()=>document.querySelector('.a2-back').click()"); pg.wait_for_timeout(500)
    print(pg.evaluate("()=>tvaAtlas2.stato().screen"))
    pg.evaluate("()=>document.querySelector('[data-tile=universi]').click()"); pg.wait_for_timeout(300); sc('uni1')
    pg.evaluate("()=>document.querySelector('.a2-card').click()"); pg.wait_for_timeout(300); sc('dos1'); sc('dos2',900)
    pg.evaluate("()=>document.querySelector('.a2-back').click()"); pg.wait_for_timeout(500)
    pg.evaluate("()=>document.querySelector('.a2-back').click()"); pg.wait_for_timeout(500)
    pg.evaluate("()=>document.querySelector('[data-tile=cronologie]').click()"); pg.wait_for_timeout(300); sc('cron')
    print(errs)
    b.close()
