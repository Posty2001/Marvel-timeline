from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,has_touch=True,is_mobile=True); pg=ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(F); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(600)
    pg.add_style_tag(content=":root{--sat:47px !important;--sab:34px !important}")
    pg.evaluate("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(300)
    def sc(n,y=0):
        pg.evaluate(f"()=>{{document.querySelector('.a2-scroll').scrollTop={y}}}"); pg.wait_for_timeout(200); pg.screenshot(path=f'f2_{n}.png')
    for cat in ('org','art','evt','luo'):
        pg.evaluate("()=>tvaAtlas2.openHome()"); pg.evaluate("()=>document.querySelector('.a2-all').click()"); pg.wait_for_timeout(200)
        pg.evaluate("(c)=>{const k={org:'organizzazioni',art:'artefatti',evt:'eventi',luo:'luoghi'}[c];document.querySelector('[data-sez='+k+']').click()}",cat); pg.wait_for_timeout(300); sc(cat+'_arch')
    pg.evaluate("()=>document.querySelector('[data-arc=org-tva-time-variance-authority]').click()") if False else None
    pg.evaluate("()=>tvaGo('arc','org:org-s-h-i-e-l-d')"); pg.wait_for_timeout(400); sc('dos_org'); sc('dos_org2',800)
    pg.evaluate("()=>tvaAtlas2.openHome()"); pg.evaluate("()=>document.querySelector('.a2-feat').click()"); pg.wait_for_timeout(300); sc('rel')
    pg.evaluate("()=>document.querySelector('[data-gem]').click()"); pg.wait_for_timeout(200); sc('rel2',400)
    print(errs)
    b.close()
