from f4lib import *
import json
def tab(pg,n): pg.evaluate("(n)=>document.getElementById(n).click()",n); pg.wait_for_timeout(500)
def vis(pg,sel): return pg.evaluate("(s)=>{const e=document.querySelector(s);return !!e&&e.getClientRects().length>0}",sel)
with sync_playwright() as p:
    b=p.chromium.launch()
    for W,H in [(320,568),(375,812),(390,844),(393,852)]:
        ctx,pg,errs=boot(b,W,H,atlas=False)
        pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(300)
        # 1 barra: sei voci, Centrale TVA
        labs=pg.evaluate("()=>[...document.querySelectorAll('#appTabbar .app-tab')].map(t=>[t.id,t.getAttribute('data-tab'),t.textContent.replace(/\\s+/g,' ').trim(),t.getAttribute('aria-label')])")
        ok('%d barra: 6 voci, ordine e id invariati'%W,[l[0] for l in labs]==['appTabHome','appTabTimeline','appTabAtlante','appTabMissioni','appTabTessera','appTabFriends'],labs)
        ok('%d barra: «Centrale TVA» al posto di Missioni'%W,labs[3][2]=='CENTRALE TVA' and labs[3][3]=='Centrale TVA' and not any('MISSIONI' in l[2] for l in labs),labs[3])
        geo=pg.evaluate("()=>[...document.querySelectorAll('#appTabbar .app-tab')].map(t=>{const r=t.getBoundingClientRect(),l=t.querySelector('.app-tab-lbl').getBoundingClientRect();return [r.left,r.right,l.left,l.right,t.querySelector('.app-tab-lbl').scrollWidth>t.querySelector('.app-tab-lbl').clientWidth+1]}).map(x=>x)")
        ok('%d barra: etichette dentro la propria voce'%W,all(g[2]>=g[0]-0.5 and g[3]<=g[1]+0.5 for g in geo),geo)
        bar=pg.evaluate("()=>{const r=document.getElementById('appTabbar').getBoundingClientRect();return [r.top,r.height,innerHeight]}")
        ok('%d barra: altezza ragionevole (%dpx)'%(W,bar[1]),bar[1]<=84,bar)
        # 2 Timeline: vista
        tab(pg,'appTabTimeline'); pg.evaluate("()=>window.scrollTo({top:0,behavior:'instant'})"); pg.wait_for_timeout(300)
        ok('%d Timeline: nascosti dashboard/database/bollettino/footer/foot-mark'%W,not any(vis(pg,s) for s in ('#dashboard','#database','.bollettino-box','footer.closing','.foot-mark')))
        ok('%d Timeline: visibili cover, indice, controlli, capitoli'%W,all(vis(pg,s) for s in ('#cover','#indice','.controlbar','#cap0','#parte1','#parte2','#parte3','#parte4','#serieanimate')))
        pos=pg.evaluate("()=>{const t=s=>document.querySelector(s).getBoundingClientRect().top+scrollY;return [t('#cover'),t('#indice'),t('.controlbar'),t('#cap0')]}")
        ok('%d Timeline: indice subito dopo la copertina, prima di controlli e capitoli'%W,pos[0]<pos[1]<pos[2]<pos[3] and pos[1]<420,pos)
        n=pg.evaluate("()=>[document.querySelectorAll('li.card-wrap[id^=\"item-\"]:not([data-variant-of])').length,document.querySelectorAll('li.card-wrap[id^=\"item-\"]').length,document.querySelectorAll('#cap0 details.card').length]")
        ok('%d DOM intatto: schede/varianti/Cap.0 (%s)'%(W,n),n[2]==5 and n[1]>=139,n)
        # fondo Timeline: niente footer; ultimo contenuto non coperto dalla barra
        pg.evaluate("()=>window.scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})"); pg.wait_for_timeout(300)
        r=pg.evaluate("()=>{const bt=document.getElementById('appTabbar').getBoundingClientRect().top;const vis=[...document.querySelectorAll('a,button,summary,input')].filter(e=>{const r=e.getBoundingClientRect();return r.height>0&&r.width>0&&!e.closest('#appTabbar')&&r.top<innerHeight&&r.bottom>0&&getComputedStyle(e).visibility!=='hidden'});const lastB=Math.max(...[...document.querySelectorAll('.back-top, .part:last-of-type li.card-wrap:last-child')].map(e=>e.getBoundingClientRect().bottom));return {bt,lastB,sh:document.documentElement.scrollHeight}}")
        ok('%d Timeline fondo: ultimo contenuto sopra la barra'%W,r['lastB']<=r['bt']+1,r)
        # 3 Centrale TVA
        tab(pg,'appTabMissioni'); pg.wait_for_timeout(500)
        ok('%d Centrale [B2: intenzionale] dashboard e bollettino (in Panoramica) visibili, database/Atlante fuori dalla Centrale; capitoli nascosti'%W,all(vis(pg,s) for s in ('#dashboard','.bollettino-box')) and not vis(pg,'#database') and not any(vis(pg,s) for s in ('#cap0','#parte1','#parte2','#cover','#indice')))
        ok('%d Centrale [B2: intenzionale] strumenti di gestione raggiungibili in Operazioni'%W,pg.evaluate("()=>{document.getElementById('cenTab-operazioni').click();return !!document.querySelector('#exportBtn').getClientRects().length&&!!document.querySelector('#markAllBtn').getClientRects().length}"))
        ok('%d Centrale: missioni popolate'%W,pg.evaluate("()=>!!document.getElementById('dashMissioniBadge')&&/\\d+\\/\\d+/.test(document.getElementById('dashMissioniBadge').textContent)"),pg.evaluate("()=>document.getElementById('dashMissioniBadge').textContent"))
        pg.evaluate("()=>window.scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})"); pg.wait_for_timeout(300)
        # ritorno
        tab(pg,'appTabTimeline'); ok('%d Timeline di nuovo: dashboard nascosta'%W,not vis(pg,'#dashboard') and vis(pg,'#cap0'))
        # link #dashboard (barra laterale) -> Centrale; ricerca/hub -> Timeline
        pg.evaluate("()=>document.querySelector('a[href=\"#dashboard\"]').click()"); pg.wait_for_timeout(300); ok('%d link #dashboard apre la Centrale'%W,vis(pg,'#dashboard') and not vis(pg,'#cap0'))
        pg.evaluate("()=>document.getElementById('item-005').scrollIntoView()"); pg.wait_for_timeout(300); ok('%d scroll a un titolo dalla Centrale riporta alla Timeline'%W,vis(pg,'#item-005'))
        pg.evaluate("()=>document.getElementById('dashboard').scrollIntoView()"); pg.wait_for_timeout(300); ok('%d scroll alla dashboard dalla Timeline apre la Centrale'%W,vis(pg,'#dashboard'))
        tab(pg,'appTabTimeline')
        # 4 card: stelle sotto il titolo, senza riquadro
        pg.evaluate("()=>{const c=document.querySelector('#item-001 details.card');c.open=true;document.getElementById('item-001').scrollIntoView({block:'start',behavior:'instant'})}"); pg.wait_for_timeout(400)
        g=pg.evaluate("""()=>{const c=document.querySelector('#item-001 details.card'),sm=c.querySelector('summary').getBoundingClientRect(),w=c.querySelector('.rw2'),wr=w.getBoundingClientRect(),cs=getComputedStyle(w),pn=c.querySelector('.detail-panel'),fr=pn.querySelector('.detail-row').getBoundingClientRect();const lab=w.querySelector('.rw-label'),lr=lab.getBoundingClientRect();return {gapTitle:wr.top-sm.bottom,firstChild:pn.firstElementChild===w,border:[cs.borderTopWidth,cs.borderLeftWidth,cs.backgroundImage,cs.backgroundColor],labelVisible:lr.width>2&&lr.height>2,beforeInfo:wr.bottom<=fr.top+1,aria:w.querySelector('.rw-stars').getAttribute('aria-labelledby')===lab.id,labTxt:lab.textContent}}""")
        ok('%d card: stelle subito sotto il titolo, prima dei dettagli'%W,g['firstChild'] and g['gapTitle']<20 and g['beforeInfo'],g)
        ok('%d card: nessun riquadro «La tua valutazione» visibile (etichetta solo per screen reader)'%W,not g['labelVisible'] and g['border'][0]=='0px' and g['border'][1]=='0px' and g['border'][2]=='none' and g['border'][3]=='rgba(0, 0, 0, 0)' and g['aria'],g)
        dr=pg.evaluate("()=>{const rows=[...document.querySelectorAll('#item-001 .detail-panel > .detail-row')].slice(0,2).map(r=>r.getBoundingClientRect());return rows.length==2?rows[1].top-rows[0].bottom:null}")
        ok('%d card: spaziatura righe dettaglio ridotta (%s px)'%(W,dr),dr is not None and dr<=8,dr)
        subs=pg.evaluate("()=>[...document.querySelectorAll('#item-001 details.sub-group > summary')].map(s=>s.textContent.trim())")
        ok('%d card: sezioni espandibili %s'%(W,subs),len(subs)==4,subs)
        wr=pg.evaluate("()=>{const w=document.querySelector('#item-001 .rw2').getBoundingClientRect(),c=document.querySelector('#item-001 details.card').getBoundingClientRect();return [w.left>=c.left-1,w.right<=c.right+1,document.documentElement.scrollWidth-innerWidth]}")
        ok('%d card: widget dentro la scheda, no overflow x'%W,wr[0] and wr[1] and wr[2]<=1,wr)
        # titoli gruppo
        sh=pg.evaluate("()=>{const h=document.getElementById('sec-1a'),s=h.querySelector('.sec-sub'),a=h.getBoundingClientRect(),r=s.getBoundingClientRect();const lines=h.getClientRects().length;return {hh:a.height,right:r.right<=a.right+1,sameRow:Math.abs(r.top-a.top)<10,disp:getComputedStyle(h).display,ov:document.documentElement.scrollWidth-innerWidth}}")
        ok('%d titolo gruppo: flex-wrap, id non spezzato, nessun overflow'%W,sh['disp']=='flex' and sh['right'] and sh['ov']<=1,sh)
        ok('%d nessun errore JS'%W,not errs,errs[:2])
        ctx.close()
    b.close()
done()
