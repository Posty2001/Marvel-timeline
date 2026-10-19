from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page()
    pg.route("**/living-multiverse.webp",lambda r:r.abort()); pg.goto('http://127.0.0.1:8124/index.html'); pg.wait_for_timeout(3500)
    print(pg.evaluate("()=>{const r=e=>{const x=e.getBoundingClientRect();return [x.left,x.top,x.width,x.height].map(Math.round)};return {logo:r(document.querySelector('.intro-logo')),btn:r(document.getElementById('journeyStartBtn')),h:r(document.querySelector('.lm-act1'))}}"))
    pg.screenshot(path='/tmp/claude-0/t/shots_leg/fallback.png'); b.close()
