from playwright.sync_api import sync_playwright
import sys
F=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':320,'height':568},is_mobile=True,has_touch=True); pg=ctx.new_page()
    pg.goto(F); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(400)
    pg.evaluate("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(200)
    pg.evaluate("()=>tvaGo('item','item-125')"); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{const li=document.getElementById('item-125');const d=li.querySelector('details');if(d)d.open=true;
      const out=[];const W=document.documentElement.clientWidth;
      document.querySelectorAll('#item-125 *').forEach(e=>{const r=e.getBoundingClientRect();if(r.right>W+0.5&&r.width>0)out.push([e.tagName,e.className&&String(e.className).slice(0,30),Math.round(r.right)])});
      return {sw:document.documentElement.scrollWidth,cw:W,bs:document.body.scrollWidth,out:out.slice(0,6),ow:getComputedStyle(document.documentElement).overflowX}}""")
    print(r); b.close()
