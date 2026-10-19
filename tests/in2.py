import os,json
from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
exec(open('/tmp/claude-0/t/in1.py').read().split("ok=True")[0].split("CFG=")[0].replace("SHOT=","SHOT0="))
JS=open('/tmp/claude-0/t/in1.py').read().split('JS="""')[1].split('"""')[0]
fails=[];total=0;needscroll=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); pg.goto(F); pg.wait_for_timeout(800)
    for w in (320,340,360,375,390,393,414,430):
        for h in (480,520,568,600,640,667,700,736,780,812,844,852,896,932):
            pg.set_viewport_size({'width':w,'height':h}); pg.wait_for_timeout(60)
            sat,sab=(20,0) if h<740 else ((50,34) if h<830 else (59,34))
            r=pg.evaluate(JS,[sat,sab,0,0]); total+=1
            fit=r['keyBottom']<=h-sab+0.5 and r['keyTop']>=sat-0.5
            bad=[]
            if not fit: needscroll.append((w,h,round(r['keyBottom']),h-sab))
            if r['ov']: bad.append(('ov',r['ov']))
            if r['clipped'] or r['out']: bad.append(('clip',r['clipped'],r['out']))
            if r['pageSW']>r['W']: bad.append('hscroll')
            if r['eyebrowTop']<sat-0.5: bad.append('eyebrow')
            if bad: fails.append((w,h,bad))
    # testo ingrandito: fallback con scroll
    pg.set_viewport_size({'width':390,'height':844})
    for pct in (125,150,200):
        pg.evaluate("(p)=>{document.documentElement.style.fontSize=p+'%'}",pct); pg.wait_for_timeout(100)
        r=pg.evaluate(JS,[47,34,0,0])
        pg.evaluate("()=>{document.getElementById('journeyStartBtn').scrollIntoView({block:'center',behavior:'instant'})}"); pg.wait_for_timeout(100)
        v=pg.evaluate("()=>{const r=document.getElementById('journeyStartBtn').getBoundingClientRect();return [r.top,r.bottom,innerHeight,getComputedStyle(document.getElementById('intro')).overflowY]}")
        print(f'testo {pct}%: scroll necessario={r["scrolls"]} | dopo scroll bottone visibile={v[0]>=0 and v[1]<=v[2]} | overflow-y={v[3]} | sovrapposizioni={r["ov"]} tagliati={r["clipped"]}')
    pg.evaluate("document.documentElement.style.fontSize=''")
    b.close()
print('combinazioni testate:',total,'| con difetti (sovrapposizioni/tagli/overflow orizz.):',len(fails))
for f in fails[:15]: print('  DIFETTO',f)
print('combinazioni in cui il blocco richiesto NON entra senza scroll (ripiego scroll):',len(needscroll))
for n in needscroll: print('  ',n)
