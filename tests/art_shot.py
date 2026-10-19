from playwright.sync_api import sync_playwright
U='http://127.0.0.1:8124/index.html'
with sync_playwright() as p:
    b=p.chromium.launch()
    for vw,dpr in [((390,844),2),((430,932),2),((320,568),2),((375,667),2)]:
        ctx=b.new_context(viewport={'width':vw[0],'height':vw[1]},device_scale_factor=dpr,is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(U); pg.wait_for_timeout(2500)
        t=f'{vw[0]}x{vw[1]}'
        pg.screenshot(path=f'art_{t}.png')
        r=pg.evaluate("""()=>{const q=s=>document.querySelector(s);const b=q('#journeyStartBtn').getBoundingClientRect();const i=q('.lm-art-img').getBoundingClientRect();
        return {ready:q('#intro').classList.contains('lm-art-ready'),btn:[b.x,b.y,b.width,b.height].map(Math.round),img:[i.x,i.y,i.width,i.height].map(Math.round),sw:document.documentElement.scrollWidth,
        btnY_pct:((b.y+b.height/2-i.y)/i.height*100).toFixed(2),btnX_pct:((b.x+b.width/2-i.x)/i.width*100).toFixed(2)}}""")
        print(t,r,errs)
    b.close()
