from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for F in ('file:///home/claude/work/backups/N4_pre_narrativa.html','file:///home/claude/work/index.html'):
        pg=b.new_page(viewport={'width':320,'height':700}); pg.goto(F); pg.wait_for_timeout(800)
        pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true;for(const i of ['024','089','133']){const e=document.querySelector('#item-'+i+' details.card');if(e){e.open=true;e.querySelectorAll('details').forEach(d=>d.open=true)}}}"); pg.wait_for_timeout(500)
        r=pg.evaluate("()=>{const bad=[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1&&e.offsetParent!==null).slice(0,6).map(e=>(e.id||e.className)+':'+Math.round(e.getBoundingClientRect().right));return [document.documentElement.scrollWidth,bad]}")
        print(F[-22:],r); pg.close()
    b.close()
