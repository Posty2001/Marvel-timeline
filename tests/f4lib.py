import json,sys
from playwright.sync_api import sync_playwright
U='http://127.0.0.1:8124/index.html'
FAIL=[]; PASS=[0]
def ok(n,c,i=''):
    if c: PASS[0]+=1; print('PASS',n)
    else: FAIL.append(n); print('FAIL',n,str(i)[:300])
def boot(b,w=390,h=844,url=U,seed=None,atlas=True,dsf=1):
    ctx=b.new_context(viewport={'width':w,'height':h},device_scale_factor=dsf,is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page(); pg.set_default_timeout(8000)
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    if seed: ctx.add_init_script("(()=>{const s=JSON.parse(%s);for(const k in s){localStorage.setItem(k,s[k]);}})()"%json.dumps(json.dumps(seed)))
    pg.goto(url); pg.wait_for_timeout(900)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(300)
    if atlas: pg.evaluate("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(500)
    return ctx,pg,errs
def done():
    print('\nPASS',PASS[0],'FAIL',len(FAIL),FAIL); sys.exit(1 if FAIL else 0)
