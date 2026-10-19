from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    print(pg.evaluate("""()=>{const T=Object.values(tvaIdx.titoli);const k={};T.forEach(e=>{const key=e.kind+'|'+(e.variant?'v':'b');k[key]=(k[key]||0)+1});return [k,document.querySelectorAll('.stat-num,.hub-stat-num').length]}"""))
    print(pg.evaluate("()=>[...document.querySelectorAll('#homeHub *')].filter(e=>/^\\d+$/.test(e.textContent.trim())&&e.children.length==0).slice(0,6).map(e=>[e.className,e.textContent])"))
    b.close()
