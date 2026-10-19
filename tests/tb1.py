from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':320,'height':760}); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(500)
    pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true}"); pg.wait_for_timeout(400)
    print(pg.evaluate("""()=>{const out=[];for(const sel of ['.toc-n','#studioBtns']){let e=document.querySelector(sel);const ch=[];while(e&&e!==document.documentElement){const cs=getComputedStyle(e);ch.push((e.id||e.className||e.tagName).toString().slice(0,30)+'|'+cs.position+'|ov:'+cs.overflowX+'|tf:'+(cs.transform!=='none')+'|r:'+Math.round(e.getBoundingClientRect().right)+'|w:'+Math.round(e.getBoundingClientRect().width));e=e.parentElement}out.push(ch)}return out}"""))
    b.close()
