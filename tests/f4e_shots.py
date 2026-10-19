from f4lib import *
import os
O='/home/claude/outputs/screenshot_fase4'; os.makedirs(O,exist_ok=True)
S=[('opera_023',"tvaGo('item','item-023')"),('opera_136',"tvaGo('item','item-136')"),('personaggio_xavier',"tvaGo('char','char-charles-xavier')"),
 ('attore',"tvaGo('att',tvaXref.attori().list[0].id)"),('ricerca_shield',"tvaAtlas2.setState({screen:'cerca',q:'shield'})"),('ricerca_xmen',"tvaAtlas2.setState({screen:'cerca',q:'x men'})")]
with sync_playwright() as p:
    b=p.chromium.launch()
    for W,H in [(320,640),(390,844)]:
        ctx=b.new_context(viewport={'width':W,'height':H},is_mobile=True,has_touch=True,service_workers='block',device_scale_factor=2); pg=ctx.new_page(); pg.goto(U); pg.wait_for_timeout(800)
        pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.evaluate("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(500)
        arcs=pg.evaluate("()=>tvaAtlas2.arcModel().list.map(e=>e.cat+':'+e.id)")
        extra=[('arch_'+k,"tvaGo('arc','%s')"%next(a for a in arcs if a.startswith(k+':'))) for k in ('org','evt','luo','art')]
        for n,js in S+extra:
            pg.evaluate("()=>{"+js+"}"); pg.wait_for_timeout(350); pg.screenshot(path='%s/f4_%s_%d.png'%(O,n,W))
        ctx.close()
    b.close()
print(len(os.listdir(O)),'screenshot')
