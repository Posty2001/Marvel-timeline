from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); pg.set_default_timeout(8000)
    pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1000)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true}"); pg.wait_for_timeout(300)
    pg.evaluate("()=>document.getElementById('appTabMissioni').click()"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const c=document.querySelector('.tva-mis [data-go]');c.scrollIntoView({block:'center'});}"); pg.wait_for_timeout(400)
    print('before',pg.evaluate("()=>[pageYOffset,document.body.scrollHeight]"))
    g=pg.evaluate("()=>document.querySelector('.tva-mis [data-go]').getAttribute('data-go')")
    pg.evaluate("g=>document.querySelector('.tva-mis [data-go=\"'+g+'\"]').click()",g); pg.wait_for_timeout(1500)
    print('snap',pg.evaluate("()=>JSON.stringify([tvaNavStato().last.an,tvaNavStato().last.y,tvaNavStato().last.tab])"))
    pg.click('#tvaBackBtn')
    for i in range(5):
        pg.wait_for_timeout(500); print(pg.evaluate("()=>[pageYOffset,document.body.scrollHeight,document.querySelector('.tva-mis')?document.querySelector('.tva-mis').getBoundingClientRect().top:null]"))
    b.close()
