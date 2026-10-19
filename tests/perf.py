from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); pg.set_default_timeout(8000)
    pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true}"); pg.wait_for_timeout(300)
    print(pg.evaluate("""()=>{const t=[];for(let i=0;i<5;i++){const a=performance.now();tvaPushNav('x');t.push(Math.round((performance.now()-a)*10)/10)}return t}"""))
    pg.evaluate("()=>tvaGo('uni','uni-earth-828')"); pg.wait_for_timeout(500)
    print(pg.evaluate("""()=>{const a=performance.now();tvaPushNav('x');return performance.now()-a}"""))
    b.close()
