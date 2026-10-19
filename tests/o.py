from playwright.sync_api import sync_playwright
import sys
with sync_playwright() as p:
    b=p.chromium.launch()
    for f in ('index.baseline.html','index.html'):
        pg=b.new_page(viewport={'width':320,'height':800})
        pg.goto('file:///home/claude/work/'+f); pg.wait_for_timeout(1200)
        pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true;document.getElementById('homeHub').style.display='none'}")
        pg.wait_for_timeout(300)
        r=pg.evaluate("""()=>{const W=document.documentElement.clientWidth;const o=[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>W+0.5&&getComputedStyle(e).position!=='fixed'&&e.getBoundingClientRect().width>0).slice(0,5).map(e=>e.tagName+'.'+e.className+'#'+e.id+' '+Math.round(e.getBoundingClientRect().right));return [document.documentElement.scrollWidth-W,o, !!e_in_rtd()]; function e_in_rtd(){return document.querySelector('#roadToDoomsday .rtd-link')}}""")
        print(f,r)
