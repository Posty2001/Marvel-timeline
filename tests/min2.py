import json,re
from playwright.sync_api import sync_playwright
KEY='marvel-ultimate-timeline-watched'
s=open('/home/claude/work/index.html',encoding='utf-8').read()
md=json.loads(re.search(r'id="tesseraMinutesData"[^>]*>(.*?)</script>',s,re.S).group(1))
res=[]
def ok(n,c,x=''): res.append(c); print('PASS' if c else 'FAIL',n,x)
with sync_playwright() as p:
    b=p.chromium.launch()
    def run(ids,url='file:///home/claude/work/index.html'):
        pg=b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(url); pg.evaluate("(s)=>{localStorage.clear();localStorage.setItem('%s',s)}"%KEY,json.dumps({i:True for i in ids})); pg.reload(); pg.wait_for_timeout(900)
        pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true}"); pg.wait_for_timeout(200)
        r=pg.evaluate("()=>({dash:(document.getElementById('dashTimeWatched')||{}).textContent,tes:(document.getElementById('tesseraOre')||{}).textContent})")
        pg.close(); return r,errs
    for ids in (['028'],['130'],['133'],['136'],['028','130','133','136'],[f'{i:03d}' for i in range(1,140)]):
        r,e=run(ids); tot=sum(md.get(str(int(i)),0) for i in ids if i!='133')  # 133 = variante di 089, non conteggiata
        exp='%dh %dm'%(tot//60,tot%60); ore=round(tot/60)
        ok('ids=%s dash=%s atteso=%s tessera=%s (atteso %dh)'%(ids if len(ids)<5 else 'tutti',r['dash'],exp,r['tes'],ore), r['dash']==exp and re.sub(r'\D','',r['tes'] or '')==str(ore) and not e)
print('FAILED' if not all(res) else 'ALL_PASS')
