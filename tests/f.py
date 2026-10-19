from playwright.sync_api import sync_playwright
import re
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{const o={};
      o.n=Object.keys(PREREQ_DIRETTI_JS).reduce((a,k)=>a+PREREQ_DIRETTI_JS[k].length,0);o.t=Object.keys(PREREQ_DIRETTI_JS).length;
      o.p74=prerequisitiDuri('074');o.p129=prerequisitiDuri('129');
      o.min131=minutiDaTabella?minutiDaTabella('131'):null;
      const c=document.getElementById('item-131');o.d131=[...c.querySelectorAll('.detail-row')].filter(r=>/DURATA/.test(r.textContent)).map(r=>r.textContent.trim().replace(/\\s+/g,' '));
      o.yr134=document.querySelector('#item-134 .yr').textContent;
      o.jarvis=!!document.getElementById('char-jarvis'); 
      return o}""")
    print(r)
    # navigate link Whitney -> Edwin
    ok=pg.evaluate("""()=>{mvNavigate('char-edwin-jarvis','char','E');const e=document.getElementById('char-edwin-jarvis');return !!e && e.offsetParent!==null}""")
    print('nav edwin',ok)
    pg.evaluate("()=>{mvNavigate('char-whitney-frost','char','W')}"); pg.wait_for_timeout(300)
    links=pg.evaluate("""()=>[...document.querySelectorAll('#char-whitney-frost a.mv-inline-link')].map(a=>a.getAttribute('onclick'))""")
    print(links)
    # test selector with empty profile for 074/129
    print('errs',errs)
