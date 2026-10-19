import json,sys
from playwright.sync_api import sync_playwright
from leg_shot import boot
import leg_shot
F=[]
def ok(n,c,x=''):
    print('PASS' if c else 'FAIL',n,'' if c else x)
    if not c: F.append(n)
with sync_playwright() as p:
    b=p.chromium.launch()
    for lab,url in (('new','http://127.0.0.1:8124/index.html'),):
        leg_shot.U=url
        ctx,pg,errs=boot(b)
        pg.evaluate("()=>{const i=document.getElementById('spoilerCutoffInput');i.value='15';i.dispatchEvent(new Event('input',{bubbles:true}));i.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(400)
        r=pg.evaluate("()=>[...document.querySelectorAll('.card-wrap[id^=item-]')].filter(w=>+w.id.slice(5)>=12&&+w.id.slice(5)<=24).map(w=>[w.id.slice(5),w.querySelector('.rec').textContent.replace(/\\D/g,''),w.classList.contains('beyond-cutoff')])")
        print(r)
        ok('soglia spoiler #15: oltre-soglia = schede Fox con N° visibile > 15 (per posizione)',all((int(v)>15)==bc for i,v,bc in r),r)
        ok('soglia #15: First Class, Origins, X-Men, X2 visibili; TLS (N°016) oltre',[i for i,v,bc in r if not bc]==['012','018','015','016'],[i for i,v,bc in r if not bc])
        # filtri per categoria: conteggi X-Men invariati
        c=pg.evaluate("()=>[...document.querySelectorAll('[id^=dashCnt-]')].map(x=>x.id+'='+x.textContent)")
        print(c)
        print(errs); ok('nessun errore JS',not errs,errs)
b.close() if False else None
sys.exit(1 if F else 0)
