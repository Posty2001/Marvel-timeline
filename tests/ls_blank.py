import sys
from playwright.sync_api import sync_playwright
U=sys.argv[1]; N=int(sys.argv[2]); bad=0
with sync_playwright() as p:
    b=p.chromium.launch()
    for it in range(N):
        ctx=b.new_context(); pg=ctx.new_page(); pg.goto(U); pg.wait_for_timeout(200)
        pg.evaluate("localStorage.setItem('a','1')"); pg.wait_for_timeout(1300)
        pg.evaluate("localStorage.setItem('late','1')"); pg.wait_for_timeout(600)
        pg.reload(); pg.wait_for_timeout(300)
        r=pg.evaluate("[localStorage.getItem('a'),localStorage.getItem('late')]")
        if r!=['1','1']: bad+=1; print('ITER',it,'perdita',r)
        ctx.close()
    b.close()
print(U,'iterazioni',N,'perdite',bad)
