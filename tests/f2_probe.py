from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,has_touch=True,is_mobile=True); pg=ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' and 'TUNNEL' not in m.text else None)
    pg.goto(F); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(600)
    pg.add_style_tag(content=":root{--sat:47px !important;--sab:34px !important}")
    m=pg.evaluate("""()=>{const M=tvaAtlas2.arcModel();const o={};for(const e of M.list){o[e.id]={t:e.titles.length,v:e.vago,u:e.unis.length,m:e.members.map(c=>tvaIdx.personaggi[c].name),l:e.leader.map(c=>tvaIdx.personaggi[c].name),c:e.cited.map(c=>tvaIdx.personaggi[c].name),a:e.arcs}}return o}""")
    for k,v in m.items(): print(k,v)
    print(errs)
    b.close()
