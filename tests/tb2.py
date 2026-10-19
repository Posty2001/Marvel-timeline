import sys
from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
ok=True
def chk(n,c,d=''):
    global ok
    if not c: ok=False
    print(('PASS ' if c else 'FAIL ')+n,d)
with sync_playwright() as p:
    b=p.chromium.launch()
    for w,h in ((320,568),(375,667),(390,844),(430,932)):
      for sab in (0,34):
        pg=b.new_page(viewport={'width':w,'height':h}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(F); pg.wait_for_timeout(500)
        pg.evaluate("(sab)=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true;document.documentElement.style.setProperty('--sab',sab+'px')}",sab); pg.wait_for_timeout(500)
        T=f'{w}x{h} sab={sab} '
        g=lambda:pg.evaluate("""()=>{const b=document.getElementById('appTabbar'),r=b.getBoundingClientRect(),cs=getComputedStyle(b);
          const tabs=[...b.querySelectorAll('.app-tab')].map(t=>t.getBoundingClientRect());
          return {bottom:r.bottom,top:r.top,left:r.left,right:r.right,h:innerHeight,w:document.documentElement.clientWidth,tf:cs.transform,wc:cs.willChange,bf:cs.backdropFilter,bg:cs.backgroundColor,
            tabBottom:Math.max(...tabs.map(t=>t.bottom)),sh:document.documentElement.scrollHeight,sw:document.documentElement.scrollWidth,n:tabs.length}}""")
        r=g()
        chk(T+'bar bottom == bordo fisico',abs(r['bottom']-r['h'])<0.5,r['bottom'])
        chk(T+'bar larga quanto lo schermo',r['left']==0 and abs(r['right']-r['w'])<0.5)
        chk(T+'icone/testi sopra safe area',r['tabBottom']<=r['h']-sab+0.5,(r['tabBottom'],r['h']-sab))
        chk(T+'nessun transform/will-change/backdrop',r['tf']=='none' and r['wc']=='auto' and r['bf']=='none',(r['tf'],r['wc'],r['bf']))
        chk(T+'sfondo opaco',r['bg'] in('rgb(15, 13, 10)',),r['bg'])
        chk(T+'no overflow orizzontale',r['sw']<=r['w'],(r['sw'],r['w']))
        sh0=r['sh']
        for y in (300,2000,'end'):
            pg.evaluate("(y)=>window.scrollTo({top:y==='end'?document.documentElement.scrollHeight:y,behavior:'instant'})",y); pg.wait_for_timeout(120)
            q=g(); chk(T+f'stabile scroll {y}',abs(q['bottom']-q['h'])<0.5 and q['top']==r['top'])
        # contenuto finale non coperto
        chk(T+'scrollHeight invariato da ::after',g()['sh']==sh0)
        # tastiera
        pg.evaluate("()=>window.scrollTo({top:0,behavior:'instant'})")
        pg.evaluate("()=>{const i=document.createElement('input');i.type='text';i.id='tmpI';document.body.appendChild(i);i.focus()}"); pg.wait_for_timeout(200)
        chk(T+'tastiera: barra nascosta',pg.evaluate("()=>getComputedStyle(document.getElementById('appTabbar')).display")=='none')
        pg.evaluate("()=>document.getElementById('tmpI').blur()"); pg.wait_for_timeout(200)
        chk(T+'blur: barra torna',pg.evaluate("()=>getComputedStyle(document.getElementById('appTabbar')).display")!='none')
        pg.evaluate("()=>{const c=document.createElement('input');c.type='checkbox';c.id='tmpC';document.body.appendChild(c);c.focus()}"); pg.wait_for_timeout(150)
        chk(T+'checkbox non nasconde la barra',pg.evaluate("()=>getComputedStyle(document.getElementById('appTabbar')).display")!='none')
        # pinch (CDP)
        cdp=pg.context.new_cdp_session(pg)
        cdp.send('Emulation.setPageScaleFactor',{'pageScaleFactor':2}); pg.wait_for_timeout(300)
        z=pg.evaluate("""()=>{const v=visualViewport,b=document.getElementById('appTabbar'),r=b.getBoundingClientRect();return {s:v.scale,vb:v.offsetTop+v.height,ox:v.offsetLeft,vw:v.width,z:b.classList.contains('is-zoomed'),tf:getComputedStyle(b).transform}}""")
        print('   zoom info',z)
        chk(T+'pinch: scale rilevata e classe is-zoomed',z['s']>1.5 and z['z'])
        cdp.send('Emulation.setPageScaleFactor',{'pageScaleFactor':1}); pg.wait_for_timeout(300)
        chk(T+'pinch rilasciato: classe rimossa, transform none',pg.evaluate("()=>{const b=document.getElementById('appTabbar');return !b.classList.contains('is-zoomed')&&getComputedStyle(b).transform==='none'}"))
        chk(T+'nessun errore JS',not errs,errs)
        pg.close()
    # >=700
    pg=b.new_page(viewport={'width':820,'height':900}); pg.goto(F); pg.wait_for_timeout(400)
    pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true}"); pg.wait_for_timeout(400)
    r=pg.evaluate("()=>{const r=document.getElementById('appTabbar').getBoundingClientRect();return [r.left,r.right,r.width,r.bottom,innerHeight,innerWidth]}")
    chk('820 centrata 480 e a bordo basso',abs(r[2]-480)<1 and abs((r[0]+r[1])/2-r[5]/2)<1 and abs(r[3]-r[4])<0.5,r)
    b.close()
print('ALL_PASS' if ok else 'SOME_FAIL')
