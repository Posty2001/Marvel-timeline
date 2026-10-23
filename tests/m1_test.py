"""M1 — ordine di visione personalizzato nel profilo (export/import/sync) + retrocompatibilita'."""
import json, os, time
from playwright.sync_api import sync_playwright
URL='file:///home/claude/work/index.html'; D='/tmp/claude-0/t/m1'; os.makedirs(D,exist_ok=True)
K='marvelGuideCustomTimelineOrder'; W='marvel-ultimate-timeline-watched'; N='marvel-ultimate-timeline-notes'
res=[]
def ok(n,c,x=''): res.append(bool(c)); print('PASS' if c else 'FAIL',n,x)
INIT="(function(){var o=window.setTimeout;window.__pend=null;window.setTimeout=function(f,m){if(m===5000)return 0;if(m===1200){window.__pend=f;return 0}return o.apply(window,arguments)}})();"
with sync_playwright() as p:
    b=p.chromium.launch()
    def page(seed=None):
        ctx=b.new_context(viewport={'width':390,'height':844},accept_downloads=True); ctx.add_init_script(INIT)
        pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('dialog',lambda d:d.accept())
        pg.goto(URL)
        if seed is not None:
            pg.evaluate("(d)=>{localStorage.clear();for(const k in d)localStorage.setItem(k,d[k])}",seed); pg.reload()
        pg.wait_for_timeout(1500); return ctx,pg,errs
    def exp(pg):
        with pg.expect_download() as d: pg.evaluate("()=>document.getElementById('exportBtn').click()")
        path=os.path.join(D,'e%d.json'%int(time.time()*1000)); d.value.save_as(path); return path
    def imp(pg,path):
        pg.evaluate("()=>{window.__pend=null}"); pg.set_input_files('#importFile',path); pg.wait_for_timeout(700)
    ORD=[5,2,9,1,3]
    # 1 export con ordine
    c1,p1,e1=page({K:json.dumps(ORD),W:json.dumps({'001':True}),N:json.dumps({'001':'nota'})})
    f1=exp(p1); j1=json.load(open(f1)); ok('1 export contiene customOrder',j1.get('customOrder')==ORD,j1.get('customOrder'))
    # 2 export senza ordine -> {} (come gli altri campi vuoti)
    c2,p2,e2=page({W:json.dumps({'001':True})}); j2=json.load(open(exp(p2))); ok('2 export senza ordine: campo vuoto',j2.get('customOrder')=={},j2.get('customOrder'))
    # 3 import ripristina l'ordine, senza perdere altri dati del file
    c3,p3,e3=page({K:json.dumps([1,2,3]),W:json.dumps({'002':True})}); imp(p3,f1)
    g=p3.evaluate("(k)=>[localStorage.getItem(k[0]),localStorage.getItem(k[1]),localStorage.getItem(k[2])]",[K,W,N])
    ok('3 import: ordine ripristinato',json.loads(g[0])==ORD,g[0]); ok('3b import: titoli visti e note del file presenti','001' in json.loads(g[1]) and json.loads(g[2]).get('001')=='nota',g[1:])
    # 4 vecchio backup (senza campo): l'ordine locale NON viene perso, il resto si sostituisce come sempre
    old={k:v for k,v in j1.items() if k!='customOrder'}; old['watched']={'040':True}; fo=os.path.join(D,'old.json'); json.dump(old,open(fo,'w'))
    c4,p4,e4=page({K:json.dumps(ORD),W:json.dumps({'002':True})}); imp(p4,fo)
    g=p4.evaluate("(k)=>[localStorage.getItem(k[0]),localStorage.getItem(k[1])]",[K,W])
    ok('4 vecchio backup: ordine locale conservato',g[0] is not None and json.loads(g[0])==ORD,g[0]); ok('4b vecchio backup: profilo sostituito (watched del file)',list(json.loads(g[1]))==['040'],g[1])
    # 5 valori non validi respinti senza toccare nulla
    for nm,val in (('stringa','abc'),('duplicati',[1,1]),('non intero',[1.5]),('testo nell elenco',['x']),('troppo lungo',list(range(1,502)))):
        bad=dict(j1); bad['customOrder']=val; fb=os.path.join(D,'bad.json'); json.dump(bad,open(fb,'w'))
        c5,p5,e5=page({K:json.dumps([7,8]),W:json.dumps({'002':True})}); imp(p5,fb)
        g=p5.evaluate("(k)=>[localStorage.getItem(k[0]),localStorage.getItem(k[1])]",[K,W]); ok('5 import rifiutato (%s): nessuna modifica'%nm,g[0] is not None and json.loads(g[0])==[7,8] and list(json.loads(g[1]))==['002'],g); c5.close()
    # 6 ordine vuoto nel file -> rimosso (esplicito)
    emp=dict(j1); emp['customOrder']=[]; fe=os.path.join(D,'emp.json'); json.dump(emp,open(fe,'w'))
    c6,p6,e6=page({K:json.dumps(ORD)}); imp(p6,fe); ok('6 ordine vuoto esplicito: rimosso',p6.evaluate("(k)=>localStorage.getItem(k)",K) is None)
    # 7 ordine personalizzato intatto e leggibile dall'UI (vista custom)
    c7,p7,e7=page({K:json.dumps(ORD)}); ok('7 atGetCustomOrder invariato (chiave originale)',json.loads(p7.evaluate("(k)=>localStorage.getItem(k)",K))==ORD)
    ok('8 nessun errore JS',not (e1+e2+e3+e4+e6+e7),(e1+e3+e4)[:2])
print('TOT',sum(res),'/',len(res))
