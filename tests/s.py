from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for w,h,n in ((390,844,'m'),(1280,900,'d')):
        pg=b.new_page(viewport={'width':w,'height':h})
        pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1200)
        pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true;document.getElementById('homeHub').style.display='none';document.getElementById('rtdDetails').open=true}")
        for i in ['015','016','041','051','084']:
            pg.evaluate("(i)=>{const c=document.querySelector('.watch-check[data-item=\"'+i+'\"]');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}));}",i)
        pg.wait_for_timeout(500)
        pg.evaluate("()=>{const c=document.getElementById('missioneCelebrazione');if(c)c.hidden=true;document.querySelectorAll('.lv-toast-msg').forEach(e=>e.remove())}")
        pg.locator('#roadToDoomsday').scroll_into_view_if_needed()
        pg.locator('#roadToDoomsday').screenshot(path=f'rtd_{n}.png')
