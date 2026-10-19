from playwright.sync_api import sync_playwright
import re,json
F='file:///home/claude/work/index.html'
res=[]
def ok(n,c,d=''): res.append(c); print('PASS' if c else 'FAIL',n,d)
src=open('/home/claude/work/index.html',encoding='utf-8').read()
def card(i): return re.search(r'<li class="card-wrap" id="%s".*?</details>\s*</li>'%i,src,re.S).group(0)
for n,t,y in (('012','X-Men: First Class','2011'),('014','X-Men: Apocalypse','2016'),('024','Logan','2017')):
    ok('File locale %s: anno %s'%(t,y),("openLocalVideoFor('%s','film','%s')"%(t,y)) in card('item-'+n))
c=card('item-134'); ok('134: badge Confermato con titolo di data ufficiale',('status-confermato' in c and 'Data ufficiale confermata' in c and '<span class="yr">gen 2027</span>' in c))
R=dict(re.findall(r"'(\d+)':\s*'([^']*)'",re.search(r"var RILASCIO_JS = \{(.*?)\};",src,re.S).group(1))); ok('134: RILASCIO_JS invariato 2027-01-13',R['134']=='2027-01-13')
cx=card('char-charles-xavier'); ok('Charles Xavier: citati McAvoy (N°012) e Stewart (N°024) con link a Stewart',('James McAvoy' in cx and 'Patrick Stewart</a> (N' in cx and "mvNavigate('att-patrick-stewart'" in cx))
ok('Patrick Stewart: ruolo Fox-Verse non su N°012; primo titolo = X-Men (N°014 nella nuova sequenza)',('N&deg;014, Fox-Verse' in card('att-patrick-stewart')) and 'N&deg;012' not in card('att-patrick-stewart'))
A=json.loads(re.search(r'id="atlasData">(.*?)</script>',src,re.S).group(1)); sm=next(c for c in A['personaggi'] if c['id']=='char-spider-man')
ok('atlasData: char-spider-man origine MCU (N°067), non Raimi',sm['continuitaOrigine']==['uni-earth-199999-mcu'])
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1280,'height':800}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.goto(F); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true;document.getElementById('homeHub').style.display='none';document.getElementById('rtdDetails').open=true}")
    for w in (320,340,360,375,380,390):
        pg.set_viewport_size({'width':w,'height':800}); pg.wait_for_timeout(250)
        ov=pg.evaluate("()=>{const s=document.getElementById('jsStatus');if(s)s.style.display='inline';return document.documentElement.scrollWidth-document.documentElement.clientWidth}")
        ok('no overflow %dpx (con jsStatus visibile)'%w,ov<=0,ov)
    ok('nessun errore JS',not errs,errs[:2]); b.close()
print('TOTALE FALLITI',res.count(False))
