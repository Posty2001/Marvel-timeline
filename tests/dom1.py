from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(800)
    pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true}"); pg.wait_for_timeout(500)
    print(pg.evaluate("""()=>{
      const o=[];const ds=e=>e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(e.className&&typeof e.className==='string'?'.'+e.className.trim().split(/\\s+/).slice(0,3).join('.'):'');
      for(const e of document.body.children){ if(e.tagName==='SCRIPT'||e.tagName==='INPUT'||e.tagName==='STYLE')continue;
        const r=e.getBoundingClientRect();
        o.push(ds(e)+' | display='+getComputedStyle(e).display+' | cards='+e.querySelectorAll('.card-wrap').length+' | h='+Math.round(r.height)); }
      return o.join('\\n')}"""))
    b.close()
