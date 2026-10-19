from f4lib import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>tvaGo('item','item-136')"); pg.wait_for_timeout(300)
    print(pg.evaluate("""()=>{const sc=document.querySelector('.a2-scroll');const W=sc.clientWidth;return [W,sc.scrollWidth,[...sc.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>W+1).slice(0,6).map(e=>e.tagName+'.'+e.className+' '+Math.round(e.getBoundingClientRect().right)+' '+(e.innerText||'').slice(0,40))]}"""))
    print(pg.evaluate("()=>tvaXref.opera('item-136').titolo"))
    # stesso su baseline
    b.close()
