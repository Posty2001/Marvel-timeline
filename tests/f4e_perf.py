from f4lib import *
import statistics,sys
import f4lib
for name,url in [('3C-baseline','http://127.0.0.1:8124/index.xmen.frozen.html'),('Fase4','http://127.0.0.1:8124/index.html')]:
    f4lib.U=url
    with sync_playwright() as p:
        b=p.chromium.launch(); ctx,pg,errs=boot(b)
        cdp=ctx.new_cdp_session(pg); cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
        chars=pg.evaluate("()=>Object.keys(tvaIdx.personaggi).filter((_,i)=>i%12==0)")
        t=pg.evaluate("""(a)=>a.map(x=>{const t=performance.now();tvaGo('char',x);return performance.now()-t})""",chars)
        print(name,'char med %.1f p95 %.1f'%(statistics.median(t),sorted(t)[int(len(t)*.95)-1]))
        b.close()
