from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':320,'height':568},is_mobile=True,has_touch=True)
    pg=ctx.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(800)
    pg.click('#journeyStartBtn'); pg.wait_for_timeout(2500); pg.click('#onboardingStartBtn'); pg.wait_for_timeout(800)
    print(pg.evaluate("""()=>{const h=document.getElementById('homeHub');const cs=getComputedStyle(h);const bs=[...document.querySelectorAll('.home-hub-btn')];return {hubH:h.getBoundingClientRect().height,pos:cs.position,pad:cs.padding,docH:document.documentElement.scrollHeight,bodyH:document.body.scrollHeight,bodyPad:getComputedStyle(document.body).paddingBottom,last:bs[bs.length-1].getBoundingClientRect().bottom,tb:document.getElementById('appTabbar').getBoundingClientRect().top,vh:innerHeight}}"""))
    pg.evaluate("()=>window.scrollTo(0,99999)"); pg.wait_for_timeout(300)
    print(pg.evaluate("""()=>{const bs=[...document.querySelectorAll('.home-hub-btn')];return {y:scrollY,last:bs[bs.length-1].getBoundingClientRect().bottom,tb:document.getElementById('appTabbar').getBoundingClientRect().top}}"""))
