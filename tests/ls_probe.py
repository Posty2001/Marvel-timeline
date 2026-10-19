import sys
from playwright.sync_api import sync_playwright
U=sys.argv[1]; N=int(sys.argv[2]); bad=0; badlate=0
with sync_playwright() as p:
    b=p.chromium.launch()
    for it in range(N):
        ctx=b.new_context(viewport={'width':390,'height':844}); pg=ctx.new_page(); pg.goto(U); pg.wait_for_timeout(1600)
        pg.evaluate("localStorage.setItem('probe_a','1')"); pg.wait_for_timeout(600)
        pg.reload(); pg.wait_for_timeout(1200)
        r=pg.evaluate("localStorage.getItem('probe_a')")
        if r!='1': bad+=1; print('ITER',it,'probe perso',r)
        ctx.close()
    b.close()
print(U,'iterazioni',N,'probe persi',bad)
