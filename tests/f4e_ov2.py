from f4lib import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>tvaGo('item','item-136')"); pg.wait_for_timeout(300)
    print(pg.evaluate("""()=>{const e=[...document.querySelectorAll('.a2-scroll small')].find(x=>x.getBoundingClientRect().right>391);let o=[],n=e;for(let i=0;i<4&&n;i++,n=n.parentElement){const c=getComputedStyle(n);o.push(n.tagName+'.'+n.className+' ws='+c.whiteSpace+' disp='+c.display+' ov='+c.overflowX+' w='+Math.round(n.getBoundingClientRect().width))}return [e.outerHTML.slice(0,300),o]}"""))
    b.close()
