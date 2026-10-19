from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844})
    pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;tvaArchivesToggle.checked=true;dbtab_uni=document.getElementById('dbtab-uni');dbtab_uni.checked=true}"); pg.wait_for_timeout(800)
    print(pg.evaluate("""()=>{const o=document.getElementById('tvaArchivesOverlayEl');const r=o.getBoundingClientRect();
      const u=document.getElementById('uni-earth-828').getBoundingClientRect();
      let p=document.getElementById('uni-earth-828'),ch=[];while(p&&p!==document.body){const cs=getComputedStyle(p);ch.push([p.tagName,p.id||p.className.slice(0,25),Math.round(p.getBoundingClientRect().top+pageYOffset),Math.round(p.getBoundingClientRect().height),cs.position,cs.contain,cs.contentVisibility,cs.overflowY]);p=p.parentElement}
      return {ovTop:r.top+pageYOffset,ovH:r.height,uni:u.top+pageYOffset,sh:document.body.scrollHeight,ch}}"""))
    b.close()
