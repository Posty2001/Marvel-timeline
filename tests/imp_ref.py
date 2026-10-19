import json
exec(open('imp.py').read().split("with sync_playwright() as p:")[0])
REF='file:///home/claude/work/index.ref_e8f05b99.html'
with sync_playwright() as p:
    b=p.chromium.launch()
    def mk(url,block=True):
        ctx=b.new_context(viewport={'width':390,'height':844},accept_downloads=True); ctx.add_init_script(INIT.replace('__BLOCK__','true')); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('dialog',lambda d:d.accept()); pg.goto(url); return ctx,pg,errs
    ctx,pg,e=mk(REF); fav=pg.evaluate("()=>[...document.querySelectorAll('#tesseraFavSelect option')].map(o=>o.value).filter(Boolean)[0]")
    seed(pg,base_profile(fav)); pg.reload(); pg.wait_for_timeout(1500)
    SA=prof(snap(pg))
    with pg.expect_download() as d: pg.evaluate("()=>document.getElementById('exportBtn').click()")
    path=os.path.join(D,'ref_export.json'); d.value.save_as(path); ctx.close()
    ctx,pg,e2=mk(NEW); seed(pg,base_profile(fav)|{'watched':{'040':True},'userName':'Altro','badgesEarned':['maratoneta']}); pg.reload(); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{window.__holdReload=true;window.__toasts=[]}")
    pg.set_input_files('#importFile',path); pg.wait_for_timeout(600)
    SB=prof(snap(pg)); diff={k:(SA[k],SB[k]) for k in ALLK if SA[k]!=SB[k]}
    ok('export del file di riferimento e8f05b99 reimportato nel file nuovo senza perdite',not diff and any('importato correttamente' in t for t in pg.evaluate("()=>window.__toasts")),str(list(diff.items())[:2]))
    print('errori pagina:',e,e2)
