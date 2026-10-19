from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
fails=[]
def chk(c,m):
    if not c: fails.append(m); print('FAIL',m)
CAT={'org':17,'art':16,'evt':7,'luo':16}
with sync_playwright() as p:
    b=p.chromium.launch()
    for vw in [(390,844),(320,568),(844,390)]:
        ctx=b.new_context(viewport={'width':vw[0],'height':vw[1]},is_mobile=True,has_touch=True); pg=ctx.new_page()
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(F); pg.wait_for_timeout(1200)
        pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(400)
        pg.evaluate("()=>tvaAtlas2.enter()")
        print('==',vw)
        for cat,n in CAT.items():
            pg.evaluate("(c)=>tvaGo('filter','x')" ,cat) if False else None
            pg.evaluate("()=>tvaAtlas2.openHome()")
            pg.evaluate("(c)=>tvaAtlas2.openArc(c,null)",cat) if False else None
            ids=pg.evaluate("(c)=>tvaAtlas2.arcModel().cat[c].map(e=>e.id)",cat)
            chk(len(ids)==n,f'{cat} count {len(ids)}')
            # open archive through the catalog
            pg.evaluate("(c)=>{tvaAtlas2.ext.api.nav('arch',{arc:c,eid:null,af:'tutti',aq:'',au:'tutti'})}",cat); pg.wait_for_timeout(120)
            cards=pg.evaluate("()=>document.querySelectorAll('.a2-arcard').length")
            chk(cards==n,f'{cat} cards {cards}')
            ov=pg.evaluate("()=>{const s=document.querySelector('.a2-scroll');return s.scrollWidth-s.clientWidth}")
            chk(ov<=0,f'{cat} arch overflow {ov}')
            for i in ids:
                pg.evaluate("([c,i])=>tvaGo('arc',c+':'+i)",[cat,i]); pg.wait_for_timeout(40)
                st=pg.evaluate("()=>tvaAtlas2.getState()")
                chk(st['screen']=='dossier' and st['eid']==Cid if False else st['screen']=='dossier',f'{i} dossier {st["screen"]}')
                o=pg.evaluate("()=>{const s=document.querySelector('.a2-scroll');return [s.scrollWidth-s.clientWidth,s.innerText.length]}")
                chk(o[0]<=0,f'{i} overflow {o[0]}'); chk(o[1]>80,f'{i} vuoto')
            # flusso reale: archivio -> scheda (click) -> Indietro -> archivio
            pg.evaluate("(c)=>{tvaAtlas2.ext.api.nav('arch',{arc:c,eid:null,af:'tutti',aq:'',au:'tutti'})}",cat); pg.wait_for_timeout(100)
            pg.evaluate("()=>document.querySelector('.a2-arcard').click()"); pg.wait_for_timeout(150)
            chk(pg.evaluate("()=>tvaAtlas2.getState().screen")=='dossier',f'{cat} click card')
            pg.evaluate("()=>tvaBack()"); pg.wait_for_timeout(150)
            chk(pg.evaluate("()=>tvaAtlas2.getState().screen")=='arch',f'{cat} back to arch')
        # links: dossier -> title -> back
        pg.evaluate("()=>tvaGo('arc','org:org-s-h-i-e-l-d')"); pg.wait_for_timeout(100)
        for sel,k in [('.a2-dossier [data-go^=item]','item'),('.a2-dossier [data-go^=char]','char')]:
            pass
        n=pg.evaluate("()=>{const c=[...document.querySelectorAll('.a2-scroll button,.a2-scroll a')].filter(x=>/Fury|Coulson|Captain|Agents/i.test(x.textContent));return c.length}")
        chk(n>0,'link elementi nel dossier SHIELD')
        # Reliquiario
        pg.evaluate("()=>tvaAtlas2.ext.api.nav('reliquiario',{arc:'art',eid:null})"); pg.wait_for_timeout(150)
        g=pg.evaluate("()=>document.querySelectorAll('[data-gem]').length"); chk(g>=7,f'reliquiario gemme {g}')
        pg.evaluate("()=>document.querySelector('[data-gem]').click()"); pg.wait_for_timeout(100)
        chk(pg.evaluate("()=>document.querySelector('.a2-rel-panel')!==null"),'panel reliquiario')
        # exit to app
        pg.evaluate("()=>tvaAtlas2.exit()"); pg.wait_for_timeout(150)
        chk(not pg.evaluate("()=>atlas2Toggle.checked"),'uscita')
        chk(errs==[],f'JS errors {errs}')
        ctx.close()
    b.close()
print('FAILS',len(fails),fails)
