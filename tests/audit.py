import json
from playwright.sync_api import sync_playwright
U='http://127.0.0.1:8124/index.html'
exec(open('nav_test.py').read().split("def st(pg)")[0].split("JS_STATE=")[0].replace("res=[]; errs=[]",""))
JS_STATE=open('nav_test.py').read().split('JS_STATE="""')[1].split('"""')[0]
out=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    def fresh():
        ctx=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page(); pg.goto(U); pg.wait_for_timeout(1200)
        pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(400)
        pg.evaluate("()=>document.getElementById('appTabAtlante').click()"); pg.wait_for_timeout(600)
        pg.evaluate("()=>{[...document.querySelectorAll('#atlas2 button')].find(x=>/Tutti gli archivi/i.test(x.textContent)).click()}"); pg.wait_for_timeout(500)
        return ctx,pg
    ctx,pg=fresh()
    names=pg.evaluate("()=>[...document.querySelectorAll('#atlas2 .a2-scroll button.a2-lrow')].map(b=>b.querySelector('b').textContent)")
    ctx.close()
    for n in names:
        ctx,pg=fresh()
        pg.evaluate("(n)=>{[...document.querySelectorAll('#atlas2 .a2-scroll button.a2-lrow')].find(b=>b.querySelector('b').textContent===n).click()}",n); pg.wait_for_timeout(900)
        s=pg.evaluate(JS_STATE); out.append((n,'a2' if s['a2'] and not s['ov'] else ('SHELL:'+','.join(s['ov'])+' '+s['title'] if s['shell'] else 'LEGACY-NO-SHELL '+str(s['ov'])),s['tab'],s['menu']))
        ctx.close()
    b.close()
for o in out: print(o)
