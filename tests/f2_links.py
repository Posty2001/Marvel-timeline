from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
fails=[]
def chk(c,m):
    if not c: fails.append(m); print('FAIL',m)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True); pg=ctx.new_page()
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(F); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(400)
    pg.evaluate("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(200)
    S="()=>{const s=tvaAtlas2.getState();return [s.screen,s.eid||s.uid||s.cid||'',atlas2Toggle.checked]}"
    # dossier -> ogni tipo di link -> Indietro -> stesso dossier
    for arc,eid in [('org','org-s-h-i-e-l-d'),('art','art-gemma-dell-anima'),('evt',None),('luo',None)]:
        if eid is None:
            eid=pg.evaluate("(c)=>tvaAtlas2.arcModel().cat[c][0].id",arc)
        pg.evaluate("()=>tvaAtlas2.openHome()")
        pg.evaluate("([c,i])=>tvaGo('arc',c+':'+i)",[arc,eid]); pg.wait_for_timeout(200)
        base=pg.evaluate(S)
        # elenco dei bottoni-link del dossier
        links=pg.evaluate("()=>[...document.querySelectorAll('.a2-scroll button')].map((b,i)=>[i,b.textContent.trim().slice(0,30),b.className]).filter(x=>!/a2-back|a2-search|a2-app/.test(x[2]))")
        tested=0
        for i,t,c in links:
            pg.evaluate("(i)=>document.querySelectorAll('.a2-scroll button')[i].click()",i); pg.wait_for_timeout(350)
            now=pg.evaluate(S)
            if now!=base:
                tested+=1
                # Indietro (chip globale se Atlante chiuso, altrimenti header)
                pg.evaluate("()=>{const t=document.getElementById('tvaBackBtn');if(!atlas2Toggle.checked&&t)t.click();else document.querySelector('.a2-back').click()}"); pg.wait_for_timeout(500)
                back=pg.evaluate(S)
                chk(back==base,f'{eid} link "{t}" back {back} != {base}')
                if tested>=6: break
        chk(tested>=1,f'{eid} nessun link testato ({len(links)} bottoni)')
        print(eid,'link testati',tested)
    # chip schede classiche
    n=pg.evaluate("()=>document.querySelectorAll('.tva-chip[data-go^=\"arc:\"]').length")
    print('chip arc: nelle schede classiche',n); chk(n>0,'nessun chip arc')
    pg.evaluate("()=>tvaAtlas2.exit()"); pg.wait_for_timeout(300)
    # click del primo chip su una scheda classica: apre dossier; Indietro torna alla scheda classica
    r=pg.evaluate("""()=>{const c=document.querySelector('.tva-chip[data-go^="arc:org:"],.tva-chip[data-go^="arc:art:"],.tva-chip[data-go^="arc:evt:"],.tva-chip[data-go^="arc:luo:"]');const d=c.closest('details');if(d)d.open=true;c.scrollIntoView();c.click();return c.dataset.go}""")
    pg.wait_for_timeout(500)
    s=pg.evaluate(S); print(r,s); chk(s[0]=='dossier' and s[2],'chip -> dossier')
    pg.evaluate("()=>{const t=document.getElementById('tvaBackBtn');if(!atlas2Toggle.checked&&t)t.click();else document.querySelector('.a2-back').click()}"); pg.wait_for_timeout(600)
    s=pg.evaluate("()=>[atlas2Toggle.checked,tvaNavStato().depth]"); print('dopo back',s); chk(s[0]==False,'back dal dossier-chip torna alla scheda classica')
    # sezione archivi nel dossier universo
    pg.evaluate("()=>tvaAtlas2.enter()"); pg.evaluate("()=>tvaAtlas2.openUni('uni-earth-199999-mcu')"); pg.wait_for_timeout(300)
    t=pg.evaluate("()=>document.querySelector('.a2-scroll').innerText.toLowerCase().includes('archivi nei suoi titoli')"); chk(t,'uniExtra')
    chk(errs==[],f'errori {errs}')
    b.close()
print('FAILS',len(fails),fails)
