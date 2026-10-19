import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844})
    pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true}"); pg.wait_for_timeout(300)
    for tgt,ty,nm in (('uni-earth-828','uni','E'),('char-peter-parker','char','P'),('att-tom-holland','att','T')):
        pg.evaluate("([a,b,c])=>{window.marvelChiudiOverlay&&0;mvNavigate(a,b,c)}",[tgt,ty,nm]); pg.wait_for_timeout(2500)
        print(tgt,pg.evaluate("""(t)=>{const e=document.getElementById(t);const r=e.getBoundingClientRect();let p=e,cl=[];while(p&&p!==document.body){if(p.tagName==='DETAILS'&&!p.open)cl.push(p.className);p=p.parentElement}
          return [Math.round(r.top),Math.round(r.height),pageYOffset,'closedAncestors',cl]}""",tgt))
        pg.evaluate("()=>{tvaArchivesToggle.checked=false}")
    b.close()
