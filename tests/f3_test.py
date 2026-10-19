from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
fails=[]
def chk(c,m):
    if not c: fails.append(m); print('FAIL',m)
CAT={'cos':26,'spe':8,'mis':1}
with sync_playwright() as p:
    b=p.chromium.launch()
    for vw in [(390,844),(320,568),(844,390)]:
        ctx=b.new_context(viewport={'width':vw[0],'height':vw[1]},is_mobile=True,has_touch=True); pg=ctx.new_page()
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(F); pg.wait_for_timeout(1200)
        pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(400)
        pg.evaluate("()=>tvaAtlas2.enter()"); print('==',vw)
        E=pg.evaluate
        OV="()=>{const s=document.querySelector('.a2-scroll');return [s.scrollWidth-s.clientWidth,s.innerText.length]}"
        S="()=>{const s=tvaAtlas2.getState();return [s.screen,s.eid||'',atlas2Toggle.checked]}"
        # 1) cataloghi dal catalogo TVA (voce reale) e dossier
        for k,cat in (('cosmiche','cos'),('specie','spe'),('arti','mis')):
            E("()=>tvaAtlas2.openHome()"); E("()=>document.querySelector('.a2-all').click()"); pg.wait_for_timeout(150)
            E("(k)=>document.querySelector('[data-sez='+k+']').click()",k); pg.wait_for_timeout(250)
            st=E("()=>tvaAtlas2.getState()"); chk(st['screen']=='arch' and st['arc']==cat,f'{k} apre archivio {st["screen"]}')
            n=E("()=>document.querySelectorAll('.a2-arcard').length"); chk(n==CAT[cat],f'{cat} schede {n}')
            o=E(OV); chk(o[0]<=0,f'{cat} overflow {o[0]}')
            ids=E("(c)=>tvaAtlas2.arcModel().cat[c].map(e=>e.id)",cat)
            for i in ids:
                E("([c,i])=>tvaGo('arc',c+':'+i)",[cat,i]); pg.wait_for_timeout(30)
                chk(E("()=>tvaAtlas2.getState().screen")=='dossier',f'{i} dossier')
                o=E(OV); chk(o[0]<=0,f'{i} overflow {o[0]}'); chk(o[1]>80,f'{i} vuoto')
            # archivio -> scheda -> Indietro
            E("(c)=>tvaAtlas2.ext.api.nav('arch',{arc:c,eid:null,af:'tutti',aq:'',au:'tutti'})",cat); pg.wait_for_timeout(100)
            E("()=>document.querySelector('.a2-arcard').click()"); pg.wait_for_timeout(120); E("()=>tvaBack()"); pg.wait_for_timeout(150)
            chk(E("()=>tvaAtlas2.getState().screen")=='arch',f'{cat} back')
            # ricerca e filtro
            E("(c)=>{const i=document.getElementById('a2ArcSearch');i.value='zzzz';i.dispatchEvent(new Event('input',{bubbles:true}))}",cat); pg.wait_for_timeout(350)
            chk(E("()=>document.querySelectorAll('.a2-arcard').length")==0,f'{cat} ricerca vuota')
            E("()=>{const i=document.getElementById('a2ArcSearch');i.value='';i.dispatchEvent(new Event('input',{bubbles:true}))}"); pg.wait_for_timeout(350)
            fs=E("()=>[...document.querySelectorAll('.a2-filters')[0]?.children||[]].length")
            if fs>2 and CAT[cat]>1:
                E("()=>document.querySelectorAll('.a2-filters')[0].children[1].click()"); pg.wait_for_timeout(100)
                m=E("()=>document.querySelectorAll('.a2-arcard').length"); chk(0<m<CAT[cat],f'{cat} filtro {m}')
        # 2) Potenza
        E("()=>tvaAtlas2.openHome()"); E("()=>document.querySelectorAll('.a2-feat')[1].click()"); pg.wait_for_timeout(250)
        chk(E("()=>tvaAtlas2.getState().screen")=='potenza','potenza da home')
        chk(E("()=>document.querySelectorAll('.a2-tier-h').length")==7,'7 fasce')
        chk(E("()=>document.querySelectorAll('[data-pot]').length")==159,'159 personaggi')
        o=E(OV); chk(o[0]<=0,f'potenza overflow {o[0]}')
        E("()=>document.querySelectorAll('.a2-filters .a2-f')[1].click()"); pg.wait_for_timeout(100)
        chk(E("()=>document.querySelectorAll('[data-pot]').length")==11,'filtro fascia 7 = 11')
        E("()=>{const i=document.getElementById('a2PotSearch');i.value='thanos';i.dispatchEvent(new Event('input',{bubbles:true}))}"); pg.wait_for_timeout(350)
        chk(E("()=>document.querySelectorAll('[data-pot]').length")==1,'ricerca thanos')
        ok=E("""()=>{let bad=[];for(const id of Object.keys(tvaAtlas2.ext.api.IDX.personaggi)){if(tvaAtlas2.potTier(id)==null)continue;
          tvaGo('arc','pot:'+id);const s=document.querySelector('.a2-scroll');if(tvaAtlas2.getState().screen!=='potscheda'||s.scrollWidth-s.clientWidth>0||s.innerText.length<120)bad.push(id)}return bad}""")
        chk(ok==[],f'potschede difettose {ok[:5]}')
        # potscheda -> Indietro -> potenza con filtro/ricerca conservati
        E("()=>tvaAtlas2.ext.api.nav('potenza',{arc:'pot',eid:null,af:'7',aq:'',au:'tutti'})"); pg.wait_for_timeout(100)
        E("()=>document.querySelector('[data-pot]').click()"); pg.wait_for_timeout(150); E("()=>tvaBack()"); pg.wait_for_timeout(150)
        chk(E("()=>[tvaAtlas2.getState().screen,tvaAtlas2.getState().af]")==['potenza','7'],'back potenza conserva filtro')
        # 3) Confronto: scelta tramite picker
        E("()=>tvaAtlas2.ext.api.nav('confronto',{arc:'pot',eid:'|',au:'A',aq:''})"); pg.wait_for_timeout(150)
        E("()=>document.querySelector('[data-pick=char-thanos]').click()"); pg.wait_for_timeout(120)
        E("()=>document.querySelectorAll('.a2-slot-b')[1].click()"); pg.wait_for_timeout(120)
        E("()=>document.querySelector('[data-pick=char-the-watcher]').click()"); pg.wait_for_timeout(150)
        t=E("()=>document.querySelector('.a2-scroll').innerText")
        chk('Lettura TVA'.lower() in t.lower() and 'Nessun risultato ipotetico' in t,'confronto lettura TVA')
        chk('vincitore' not in t.lower().replace('non indica un vincitore','') ,'nessun vincitore dichiarato')
        o=E(OV); chk(o[0]<=0,f'confronto overflow {o[0]}')
        # stessa persona non selezionabile come altra
        E("()=>document.querySelectorAll('.a2-slot-b')[0].click()"); pg.wait_for_timeout(100)
        chk(E("()=>!document.querySelector('[data-pick=char-the-watcher]')"),'picker esclude l’altro slot')
        # 4) catalogo: voce Classifica dei Poteri
        E("()=>tvaAtlas2.openHome()"); E("()=>document.querySelector('.a2-all').click()"); pg.wait_for_timeout(150)
        E("()=>document.querySelector('[data-sez=poteri]').click()"); pg.wait_for_timeout(200)
        chk(E("()=>tvaAtlas2.getState().screen")=='potenza','catalogo -> potenza')
        # 5) chip nelle schede classiche
        n1=E("()=>document.querySelectorAll('.tva-chip[data-go^=\"arc:pot:\"]').length"); chk(n1>100,f'chip potenza {n1}')
        n2=E("()=>[...document.querySelectorAll('.tva-row .detail-k')].filter(k=>/ENTITÀ, SPECIE E ARTI/.test(k.textContent)).length"); chk(n2>5,f'righe entità/specie {n2}')
        E("()=>tvaAtlas2.exit()"); pg.wait_for_timeout(200)
        r=E("""()=>{const c=document.querySelector('#char-thanos .tva-chip[data-go^="arc:pot:"]');const d=c.closest('details');if(d)d.open=true;c.click();return tvaAtlas2.getState().screen}""")
        pg.wait_for_timeout(300); chk(E(S)[0]=='potscheda' and E(S)[2],'chip -> scheda potenza')
        E("()=>{const t=document.getElementById('tvaBackBtn');if(!atlas2Toggle.checked&&t)t.click();else document.querySelector('.a2-back').click()}"); pg.wait_for_timeout(500)
        chk(not E("()=>atlas2Toggle.checked"),'back dalla scheda potenza alla scheda classica')
        # ricerca globale
        E("()=>tvaAtlas2.enter()"); E("()=>tvaAtlas2.openHome()"); pg.fill('#a2HomeSearch','galactus'); pg.wait_for_timeout(500)
        chk(E("()=>[...document.querySelectorAll('.a2-resbox')].some(x=>x.innerText.includes('Galactus')) && [...document.querySelectorAll('.a2-resbox h3')].some(h=>/Schede degli archivi/i.test(h.textContent))"),'ricerca globale galactus')
        pg.fill('#a2HomeSearch','kree'); pg.wait_for_timeout(500); chk(E("()=>[...document.querySelectorAll('.a2-resbox')].some(x=>/Schede degli archivi/i.test(x.innerText)&&x.innerText.includes('Kree'))"),'ricerca globale kree')
        chk(errs==[],f'errori JS {errs}'); ctx.close()
    b.close()
print('FAILS',len(fails),fails)
