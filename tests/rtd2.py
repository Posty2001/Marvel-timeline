from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':800}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1200)
    r=pg.evaluate("""()=>{const p=document.querySelector('#item-136 .dep-map');return [...p.querySelectorAll('.dep-map-cat')].map(c=>[c.querySelector('.dep-map-cat-label').textContent,[...c.querySelectorAll('.dep-chip')].map(x=>x.dataset.num+(x.querySelector('.dep-chip-via')?'*':''))])}""")
    for x in r: print(x)
    print(pg.evaluate("document.querySelector('#item-136 .dep-map-count').textContent"), errs)
    print(pg.evaluate("[...document.querySelectorAll('#rtdList .rtd-item')].map(e=>e.dataset.rtdId+':'+(e.querySelector('.rtd-tier')||{}).textContent).join(' ')"))
    b.close()
