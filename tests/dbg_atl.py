from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':320,'height':568},is_mobile=True,has_touch=True)
    pg=ctx.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(800)
    pg.click('#journeyStartBtn'); pg.wait_for_timeout(2500); pg.click('#onboardingStartBtn'); pg.wait_for_timeout(800)
    pg.click('#appTabAtlante'); pg.wait_for_timeout(1200)
    pg.evaluate("window.scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})"); pg.wait_for_timeout(400)
    print(pg.evaluate("""()=>{const o=document.querySelector('.tva-archives-overlay');const cs=getComputedStyle(o);return {y:scrollY,dh:document.documentElement.scrollHeight,oh:o.getBoundingClientRect().height,ob:o.getBoundingClientRect().bottom,pb:cs.paddingBottom,tb:document.getElementById('appTabbar').getBoundingClientRect().top,vh:innerHeight}}"""))
    pg.screenshot(path='/tmp/claude-0/t/shots/atl_bottom.png')
    print(pg.evaluate("""()=>{const tb=document.getElementById('appTabbar').getBoundingClientRect().top;const out=[];for(const e of document.querySelectorAll('body *')){if(e.closest('.app-tabbar')||e.closest('.sidebar'))continue;const r=e.getBoundingClientRect();if(r.height<2||r.width<2||r.bottom<=0||r.top>=innerHeight)continue;const cs=getComputedStyle(e);if(cs.display==='none'||cs.visibility==='hidden'||cs.position==='fixed')continue;if(e.closest('[hidden]'))continue;if(e.children.length===0&&(e.textContent||'').trim()&&r.bottom>tb)out.push([e.tagName,(e.id||e.className+'').slice(0,40),Math.round(r.top),Math.round(r.bottom),(e.textContent||'').trim().slice(0,20),e.parentElement.className.slice(0,30)]);}return out.slice(0,6)}"""))
