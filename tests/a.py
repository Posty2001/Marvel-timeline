from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    f=lambda: pg.evaluate("()=>[document.querySelectorAll('[id=\"depCount-099\"]').length, document.querySelectorAll('.dep-panel, .dep-map, [class*=dep-]').length]")
    print('load',f())
    for i in range(3):
        pg.evaluate("()=>{const c=document.querySelector('.watch-check[data-item=\"00%d\"]');c.checked=!c.checked;c.dispatchEvent(new Event('change',{bubbles:true}))}"%(i+1)); pg.wait_for_timeout(200)
        print('dopo spunta',i+1,f())
