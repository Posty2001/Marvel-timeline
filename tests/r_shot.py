from playwright.sync_api import sync_playwright
import sys
F='file:///home/claude/work/index.html'
W=int(sys.argv[1]) if len(sys.argv)>1 else 390; H=int(sys.argv[2]) if len(sys.argv)>2 else 844; tag=sys.argv[3] if len(sys.argv)>3 else 'r'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':W,'height':H},device_scale_factor=2,has_touch=True,is_mobile=True); pg=ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(F); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(500)
    pg.add_style_tag(content=":root{--sat:47px !important;--sab:34px !important}")
    pg.evaluate("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(400)
    N=pg.evaluate
    def sc(n,y=0):
        N(f"()=>{{document.querySelector('.a2-scroll').scrollTop={y}}}"); pg.wait_for_timeout(200); pg.screenshot(path=f'{tag}_{n}.png')
    sc('home'); sc('home2',700)
    N("()=>tvaGo('arc','art:art-gemma-dell-anima')"); pg.wait_for_timeout(300); sc('dos')
    N("()=>tvaAtlas2.ext.api.nav('confronto',{arc:'pot',eid:'|',au:'tutti',aq:''})"); pg.wait_for_timeout(300); sc('cmp')
    print(errs); b.close()
