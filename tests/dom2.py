import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(800)
    pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true}"); pg.wait_for_timeout(500)
    for sid in sys.argv[1:]:
        print('=====',sid)
        print(pg.evaluate("""(sid)=>{const ds=e=>e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(typeof e.className==='string'&&e.className?'.'+e.className.trim().split(/\\s+/).slice(0,3).join('.'):'');
          const root=document.getElementById(sid)||document.querySelector('.'+sid); const o=[];
          for(const e of root.children){ const t=(e.innerText||'').replace(/\\s+/g,' ').slice(0,70); o.push(ds(e)+' cards='+e.querySelectorAll('.card-wrap').length+' | '+t)}
          return o.join('\\n')}""",sid))
    b.close()
