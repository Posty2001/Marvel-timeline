from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); pg.set_default_timeout(8000)
    pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true}"); pg.wait_for_timeout(300)
    pg.evaluate("()=>document.getElementById('item-125').scrollIntoView({block:'start'})"); pg.wait_for_timeout(300)
    print('y0',pg.evaluate("()=>[pageYOffset,document.body.scrollHeight,document.getElementById('item-125').getBoundingClientRect().top]"))
    pg.evaluate("()=>tvaGo('uni','uni-earth-828')"); pg.wait_for_timeout(1200)
    print('atl',pg.evaluate("()=>[tvaNavStato().last.y,JSON.stringify(tvaNavStato().last.an)]"))
    pg.evaluate("()=>tvaBack()"); 
    for i in range(6):
        pg.wait_for_timeout(500); print(pg.evaluate("()=>[pageYOffset,document.body.scrollHeight,document.getElementById('item-125').getBoundingClientRect().top]"))
    b.close()
