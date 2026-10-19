import sys,json
from playwright.sync_api import sync_playwright
f=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium' if False else None) if False else p.chromium.launch()
    pg=b.new_page(); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.goto('file://'+f); pg.wait_for_timeout(1500)
    out={}
    for n in ('084','089','099','139','051','067','102','117','136'):
        out[n]=pg.evaluate("""(n)=>{var d=document.querySelector('#item-'+n+' .dep-map'); if(!d) return null; return {count:d.querySelector('.dep-map-count').textContent,
           cats:Array.from(d.querySelectorAll('.dep-map-cat')).map(c=>[c.querySelector('.dep-map-cat-label').textContent.trim(),Array.from(c.querySelectorAll('.dep-chip')).map(x=>x.textContent.replace(/\\s+/g,' ').trim())])}}""",n)
    # logica di blocco invariata: confronta prerequisitiDuri per tutti i titoli
    out['_hard']=pg.evaluate("""()=>{var r={}; for (var i=0;i<WATCH_ORDER_JS.length;i++){var id=WATCH_ORDER_JS[i].id; r[id]=prerequisitiDuri(id);} return r}""") if False else None
    print(json.dumps(out,ensure_ascii=False,indent=1)); print('ERRORI JS:',errs)
    b.close()
