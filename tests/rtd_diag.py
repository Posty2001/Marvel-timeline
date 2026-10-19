import json,sys
from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
W='marvel-ultimate-timeline-watched'
RTD=['015','016','041','051','084','089','095','097','099','102','108','112','117','121','123','125']
BK='marvel-ultimate-timeline-missioni-xp-bonus'
N=int(sys.argv[1]); bad=0
with sync_playwright() as p:
    b=p.chromium.launch()
    for it in range(N):
        ctx=b.new_context(viewport={'width':390,'height':844}); pg=ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        seed={W:json.dumps({i:True for i in RTD[:-1]})}
        pg.add_init_script("try{sessionStorage.setItem('__len_at_start',String(localStorage.length));var _r=Storage.prototype.removeItem,_c=Storage.prototype.clear;Storage.prototype.removeItem=function(k){try{sessionStorage.setItem('__rm',(sessionStorage.getItem('__rm')||'')+k+';')}catch(e){};return _r.apply(this,arguments)};Storage.prototype.clear=function(){try{sessionStorage.setItem('__rm',(sessionStorage.getItem('__rm')||'')+'CLEAR;')}catch(e){};return _c.apply(this,arguments)}}catch(e){}");
        pg.add_init_script("if(!localStorage.getItem('__s')){localStorage.setItem('__s','1');"+"".join("localStorage.setItem(%s,%s);"%(json.dumps(k),json.dumps(v)) for k,v in seed.items())+"}")
        pg.goto(F); pg.wait_for_timeout(1300)
        pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=false}"); pg.wait_for_timeout(300)
        pg.evaluate("document.querySelector('.watch-check[data-item=\"125\"]').click()"); pg.wait_for_timeout(600)
        pre=pg.evaluate("Object.keys(localStorage).length"); preb=pg.evaluate("localStorage.getItem(%s)"%json.dumps(BK))
        pg.reload(); pg.wait_for_timeout(1200)
        post=pg.evaluate("({n:Object.keys(localStorage).length,keys:Object.keys(localStorage).slice(0,6),bk:localStorage.getItem(%s),s:localStorage.getItem('__s'),w:(localStorage.getItem(%s)||'').length})"%(json.dumps(BK),json.dumps(W)))
        if post['bk'] is None:
            bad+=1; print('   len_at_start:',pg.evaluate("sessionStorage.getItem('__len_at_start')"),'removeItem/clear visti:',pg.evaluate("sessionStorage.getItem('__rm')"));print('ITER',it,'PERDITA bank dopo reload; prima:',pre,preb is not None,'dopo:',post)
            pg.wait_for_timeout(3000)
            print('   dopo +3s:',pg.evaluate("({n:Object.keys(localStorage).length,bk:localStorage.getItem(%s)})"%json.dumps(BK)))
        ctx.close()
    b.close()
print('iterazioni',N,'perdite',bad)
