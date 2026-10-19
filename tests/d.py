from playwright.sync_api import sync_playwright
IDS=['015','016','041','051','084','089','095','097','099','102','108','112','117','121','123','125']
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844})
    pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true;document.getElementById('homeHub').style.display='none'}")
    for i in IDS:
        pg.evaluate("(i)=>{const c=document.querySelector('.watch-check[data-item=\"'+i+'\"]');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}));}",i)
    pg.wait_for_timeout(600)
    print(pg.evaluate("""()=>{const p=document.getElementById('missioneCelebrazione');const cs=getComputedStyle(p);const bt=document.getElementById('missioneCelebrazioneChiudi');
      let chain=[];let e=p;while(e&&e!==document.body){chain.push(e.tagName+'#'+e.id+':'+getComputedStyle(e).display);e=e.parentElement}
      return {hidden:p.hidden,display:cs.display,vis:cs.visibility,rect:JSON.stringify(p.getBoundingClientRect()),btn:JSON.stringify(bt.getBoundingClientRect()),chain:chain.slice(0,6),titolo:document.getElementById('missioneCelebrazioneTitolo').textContent}}"""))
    pg.screenshot(path='d.png')
