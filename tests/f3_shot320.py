from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':320,'height':568},device_scale_factor=2,has_touch=True,is_mobile=True); pg=ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(F); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(600)
    pg.add_style_tag(content=":root{--sat:47px !important;--sab:34px !important}")
    pg.evaluate("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(300)
    def sc(n,y=0):
        pg.evaluate(f"()=>{{document.querySelector('.a2-scroll').scrollTop={y}}}"); pg.wait_for_timeout(200); pg.screenshot(path=f'f3s_{n}.png')
    N=pg.evaluate
    for cat in ('cos','spe','mis'):
        N("(c)=>tvaAtlas2.ext.api.nav('arch',{arc:c,eid:null,af:'tutti',aq:'',au:'tutti'})",cat); pg.wait_for_timeout(300); sc(cat+'_arch')
    N("()=>tvaGo('arc','cos:cos-galactus')"); pg.wait_for_timeout(300); sc('cos_dos'); sc('cos_dos2',900)
    N("()=>tvaGo('arc','cos:cos-death')"); pg.wait_for_timeout(300); sc('cos_dos3')
    N("()=>tvaGo('arc','spe:spe-kree')"); pg.wait_for_timeout(300); sc('spe_dos')
    N("()=>tvaGo('arc','mis:mis-stregoneria')"); pg.wait_for_timeout(300); sc('mis_dos')
    N("()=>tvaAtlas2.ext.api.nav('potenza',{arc:'pot',eid:null,af:'tutti',aq:'',au:'tutti'})"); pg.wait_for_timeout(300); sc('pot')
    N("()=>tvaGo('arc','pot:char-thanos')"); pg.wait_for_timeout(300); sc('potsc'); sc('potsc2',900)
    N("()=>tvaAtlas2.ext.api.nav('confronto',{arc:'pot',eid:'char-thanos|char-galactus',au:'tutti',aq:''})"); pg.wait_for_timeout(300); sc('cmp'); sc('cmp2',800); sc('cmp3',1700)
    print(errs); b.close()
