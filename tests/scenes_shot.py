from playwright.sync_api import sync_playwright
import sys
O='/home/claude/outputs/'
VP=[(390,844,'iphone14'),(375,667,'iphoneSE'),(320,568,'iphone5')]
with sync_playwright() as p:
    b=p.chromium.launch()
    for w,h,n in VP:
        ctx=b.new_context(viewport={'width':w,'height':h},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('http://127.0.0.1:8124/index.html'); pg.wait_for_timeout(1800)
        for i in range(4):
            pg.evaluate("(i)=>tvaIntroScenes.go(i)",i); pg.wait_for_timeout(2300)
            pg.screenshot(path=f'{O}intro_scena{i+1}_{n}.png')
        print(n,errs)
        ctx.close()
    b.close()
