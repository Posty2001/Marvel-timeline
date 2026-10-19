import json
from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
W='marvel-ultimate-timeline-watched'
res=[]
def ok(n,c,d=''): res.append(bool(c)); print('PASS' if c else 'FAIL',n,d)
with sync_playwright() as p:
    b=p.chromium.launch()
    def page(seed):
        ctx=b.new_context(viewport={'width':390,'height':844}); pg=ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.add_init_script("if(!localStorage.getItem('__s')){localStorage.setItem('__s','1');"+"".join("localStorage.setItem(%s,%s);"%(json.dumps(k),json.dumps(v)) for k,v in seed.items())+"}")
        pg.goto(F); pg.wait_for_timeout(1200); return ctx,pg,errs
    ctx,pg,errs=page({W:json.dumps({'133':True,'001':True})})
    r=pg.evaluate("""()=>({st:document.querySelector('[data-variant-state="133"]').textContent,
      m:document.querySelector('.watch-check[data-item="089"]').checked,p:document.getElementById('progressPct').textContent,raw:localStorage.getItem('%s')})"""%W)
    ok('Versioni alternative mostra il completamento precedente di 133',r['st'].startswith('✓'),r['st'])
    ok('Endgame (089) non modificato; progresso 1/138; salvataggio intatto',(not r['m']) and r['p'].startswith('1/138') and json.loads(r['raw'])=={'133':True,'001':True},r)
    pg.evaluate("document.querySelector('#item-133 .variant-check').click()"); pg.wait_for_timeout(300)
    r=pg.evaluate("({st:document.querySelector('[data-variant-state=\"133\"]').textContent,m:document.querySelector('.watch-check[data-item=\"089\"]').checked,p:document.getElementById('progressPct').textContent})")
    ok('de-spunta variante: stato aggiornato, 089 e progresso invariati',r['st'].startswith('Versione Encore non') and not r['m'] and r['p'].startswith('1/138'),r)
    ok('nessun errore JS',not errs,errs); ctx.close()
    ctx,pg,errs=page({W:json.dumps({'089':True})})
    r=pg.evaluate("({st:document.querySelector('[data-variant-state=\"133\"]').textContent,v:document.querySelector('#item-133 .variant-check').checked,m:document.querySelector('.watch-check[data-item=\"089\"]').checked})")
    ok('089 visto e Encore non segnata: la variante non si spunta da sola',r['m'] and not r['v'] and r['st'].startswith('Versione Encore non'),r); ctx.close()
    ctx,pg,errs=page({})
    r=pg.evaluate("""()=>({note:document.querySelector('#roadToDoomsday .rtd-note').textContent,tier:document.querySelector('#rtdList .rtd-tier').title,
      off:document.querySelectorAll('#item-136 .dep-chip-off').length,chips:document.querySelectorAll('#item-136 .dep-chip').length,
      leg:document.querySelector('#item-136 .dep-map-legend').textContent,
      offIds:[...document.querySelectorAll('#item-136 .dep-chip')].filter(c=>c.querySelector('.dep-chip-off')).map(c=>c.dataset.num).sort()})""")
    ok('RTD: watchlist ufficiale distinta dalle classificazioni editoriali TVA Archive',('watchlist ufficiale' in r['note']) and ('classificazioni editoriali di TVA Archive' in r['note']) and 'TVA Archive' in r['tier'],r['note'][:90])
    ok('Doomsday: 📋 solo sui 16 titoli della lista Marvel (23 voci totali)',r['off']==16 and r['chips']==23 and r['offIds']==sorted(['015','016','041','051','084','089','095','097','099','102','108','112','117','121','123','125']),r['offIds'])
    ok('legenda: lista Marvel vs livelli editoriali',('classificazioni editoriali di TVA Archive' in r['leg']) and ('watchlist ufficiale' in r['leg']))
    v=pg.evaluate("document.querySelector('#item-135 .yr').textContent+'|'+!!document.querySelector('#item-135 .status-tag')")
    ok('Vision Quest: 13 ott 2026 (USA), già uscita, nessun badge Confermato',v=='13 ott 2026 (USA), già uscita|false',v)
    ok('nessun errore JS',not errs,errs); ctx.close(); b.close()
print('TOTALE',len(res),'FALLITI',[i for i,x in enumerate(res) if not x])
