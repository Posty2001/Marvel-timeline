from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844})
    pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true}"); pg.wait_for_timeout(300)
    pg.evaluate("()=>mvNavigate('uni-earth-828','uni','E')")
    pg.wait_for_timeout(1500)
    print(pg.evaluate("""()=>{window.scrollTo(0,2700);return [pageYOffset,document.body.scrollHeight,document.documentElement.scrollHeight,innerHeight,getComputedStyle(document.documentElement).overflow,getComputedStyle(document.body).overflow,getComputedStyle(document.body).height]}"""))
    pg.wait_for_timeout(300)
    print(pg.evaluate("()=>[pageYOffset,document.getElementById('uni-earth-828').getBoundingClientRect().top]"))
    pg.evaluate("()=>document.getElementById('uni-earth-828').scrollIntoView({block:'start'})"); pg.wait_for_timeout(300)
    print(pg.evaluate("()=>[pageYOffset,document.getElementById('uni-earth-828').getBoundingClientRect().top]"))
    b.close()
