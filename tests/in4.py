from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import io
def run(F,tag):
    with sync_playwright() as p:
        b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844}); pg=ctx.new_page()
        pg.goto(F); pg.wait_for_timeout(1000); pg.click('#journeyStartBtn'); pg.wait_for_timeout(2500)
        pg.add_style_tag(content='*{animation:none!important}')
        pg.wait_for_timeout(300)
        img=Image.open(io.BytesIO(pg.screenshot())).convert('RGB')
        vis=pg.evaluate("(()=>{const o=document.getElementById('onboardingScreen');return o&&!o.hidden})()")
        # utente di ritorno: journeyStarted gia' spuntato -> la pagina parte senza intro?
        ctx2=b.new_context(viewport={'width':390,'height':844}); pg2=ctx2.new_page()
        pg2.add_init_script("localStorage.setItem('marvel-ultimate-timeline-tessera-id',JSON.stringify({}));")
        b.close(); return img,vis
a,va=run('file:///home/claude/work/backups/N10_pre_intro.html','old')
n,vn=run('file:///home/claude/work/index.html','new')
d=ImageChops.difference(a,n).getbbox()
print('onboarding visibile old/new',va,vn,'| differenza pixel onboarding (None = identico):',d)
a2,_=run('file:///home/claude/work/backups/N10_pre_intro.html','old2')
print('baseline old vs old:',ImageChops.difference(a,a2).getbbox())
n.save('/tmp/claude-0/t/onb_new.png'); a.save('/tmp/claude-0/t/onb_old.png')
