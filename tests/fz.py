from playwright.sync_api import sync_playwright
import sys
with sync_playwright() as p:
    b=p.chromium.launch()
    for pct in (125,150,200):
      for vw in (320,390):
        pg=b.new_page(viewport={'width':vw,'height':844}); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(2500)
        pg.evaluate("(p)=>{document.documentElement.style.fontSize=p+'%'}",pct); pg.wait_for_timeout(300)
        r=pg.evaluate("""()=>{const W=innerWidth;const out=[];for(const e of document.querySelectorAll('#intro .lm-scroll *')){const r=e.getBoundingClientRect();if(e.closest('.lm-scene'))continue;if(r.width>0&&(r.right>W+0.5||r.left<-0.5))out.push((e.id||e.className.baseVal||e.className)+':'+Math.round(r.left)+'..'+Math.round(r.right))}
          const g=[];for(const e of document.querySelectorAll('#intro h1 *,#intro h2 span,.intro-stat-num,.intro-stat-lbl,.lm-ev-name,.lm-portal-t,#icdDoomsday,#icdSecretWars,.intro-tagline,#journeyStartBtn span')){const rg=document.createRange();rg.selectNodeContents(e);const q=rg.getBoundingClientRect();if(q.right>W+0.5||q.left<-0.5)g.push(e.className||e.id)}
          return {sc:document.getElementById('lmScroll').scrollWidth-W,out:out.slice(0,8),glyph:g}}""")
        print(pct,vw,r); pg.close()
