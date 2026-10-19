import sys,json
from playwright.sync_api import sync_playwright
from leg_shot import boot
from cron3c_test import setcr,hub,cs,sc
from map3b_test_helpers import tp,pan
F=[];N=[0]
def ok(n,c,d=''):
    N[0]+=1
    if not c: F.append(n); print('FAIL',n,str(d)[:300])
def tap(pg,cdp,x,y): tp(cdp,'touchStart',[(x,y)]); pg.wait_for_timeout(40); tp(cdp,'touchEnd',[]); pg.wait_for_timeout(350)
def ctr(pg,sel,nth=0):
    return pg.evaluate("([s,n])=>{const e=document.querySelectorAll(s)[n];e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]}",[sel,nth])
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b,390,844); cdp=ctx.new_cdp_session(pg); hub(pg)
    ids=pg.evaluate("()=>tvaUniverse.ids()"); mcu=ids[0]; fox=[i for i in ids if '10005' in i][0]
    ls0=pg.evaluate("()=>JSON.stringify(Object.entries(localStorage).filter(e=>!e[0].startsWith('tvaHomeMiss')))")
    # hub → tap sulla voce
    x,y=ctr(pg,'[data-cr=uni]'); tap(pg,cdp,x,y); ok('tap hub → universo',sc(pg)=='cron' and cs(pg)['mode']=='uni')
    # tab touch
    x,y=ctr(pg,'#crTab-par'); tap(pg,cdp,x,y); ok('tap tab Parallele',cs(pg)['mode']=='par')
    x,y=ctr(pg,'#crTab-exp'); tap(pg,cdp,x,y); ok('tap tab Esplora',cs(pg)['mode']=='exp')
    x,y=ctr(pg,'#crTab-uni'); tap(pg,cdp,x,y); ok('tap tab Universo',cs(pg)['mode']=='uni')
    # scroll verticale con swipe
    setcr(pg,mode='uni',uid=mcu); pg.evaluate("()=>{document.querySelector('.a2-scroll').scrollTop=0}")
    pan(pg,cdp,(200,700),(200,300),12); s1=pg.evaluate("()=>document.querySelector('.a2-scroll').scrollTop"); ok('swipe verticale scorre la cronologia',s1>150,s1)
    pan(pg,cdp,(200,300),(200,700),12); s2=pg.evaluate("()=>document.querySelector('.a2-scroll').scrollTop"); ok('swipe inverso torna indietro',s2<s1,(s1,s2))
    ok('nessun scroll orizzontale indesiderato',pg.evaluate("()=>document.querySelector('.a2-scroll').scrollLeft")==0)
    # selettore universo via touch + scelta
    x,y=ctr(pg,'#crUniSel'); tap(pg,cdp,x,y); ok('tap apre il selettore',pg.evaluate("()=>!!document.querySelector('.cr-sheet')"))
    # scroll nel sheet non muove il body
    pg.evaluate("()=>{document.querySelector('.a2-scroll').scrollTop=0}"); b0=pg.evaluate("()=>document.querySelector('.a2-scroll').scrollTop")
    pan(pg,cdp,(200,650),(200,250),10); sb=pg.evaluate("()=>document.querySelector('.cr-sh-b').scrollTop"); b1=pg.evaluate("()=>document.querySelector('.a2-scroll').scrollTop")
    ok('swipe nel sheet scorre la lista, non la pagina',sb>100 and b1==b0,(sb,b0,b1))
    pan(pg,cdp,(200,60),(200,20),6); ok('swipe sul backdrop non scorre la pagina',pg.evaluate("()=>document.querySelector('.a2-scroll').scrollTop")==b0)
    x,y=ctr(pg,'.cr-opt',3); tap(pg,cdp,x,y); ok('tap su un universo lo seleziona e chiude',cs(pg)['uid']==ids[3] and not pg.evaluate("()=>!!document.querySelector('.cr-sheet')"),cs(pg))
    # tap su backdrop chiude
    x,y=ctr(pg,'#crUniSel'); tap(pg,cdp,x,y); tap(pg,cdp,200,40); ok('tap sul backdrop chiude',not pg.evaluate("()=>!!document.querySelector('.cr-sheet')"))
    # titolo → scheda, nessun click fantasma, back ripristina
    setcr(pg,mode='uni',uid=mcu); pg.evaluate("()=>{document.querySelector('.a2-scroll').scrollTop=900}"); y0=pg.evaluate("()=>document.querySelector('.a2-scroll').scrollTop")
    x,y=ctr(pg,'.cr-ev .cr-t',6); tap(pg,cdp,x,y); pg.wait_for_timeout(500)
    ok('tap sul titolo apre la scheda',not pg.evaluate("()=>document.getElementById('atlas2Toggle').checked"))
    pg.evaluate("()=>tvaBack()"); pg.wait_for_timeout(800)
    ok('Back: schermata, universo e scroll ripristinati',sc(pg)=='cron' and cs(pg)['uid']==mcu and abs(pg.evaluate("()=>document.querySelector('.a2-scroll').scrollTop")-y0)<40,(cs(pg),y0,pg.evaluate("()=>document.querySelector('.a2-scroll').scrollTop")))
    # Mostra altri: scroll preservato
    setcr(pg,mode='uni',uid=mcu,lim=40); pg.evaluate("()=>document.getElementById('crMore').scrollIntoView({block:'center'})"); y1=pg.evaluate("()=>document.querySelector('.a2-scroll').scrollTop")
    x,y=ctr(pg,'#crMore'); y1=pg.evaluate("()=>document.querySelector('.a2-scroll').scrollTop"); tap(pg,cdp,x,y)
    ok('Mostra altri: espande senza saltare',cs(pg)['lim']==80 and abs(pg.evaluate("()=>document.querySelector('.a2-scroll').scrollTop")-y1)<30,(cs(pg)['lim'],y1))
    # chips filtro: scorrimento orizzontale
    setcr(pg,mode='exp',fu=[mcu],fp=['b3'],ft=['serie'],fs=[]); sw=pg.evaluate("()=>{const c=document.querySelector('.cr-fchips.cr-act');return [c.scrollWidth,c.clientWidth]}")
    if sw[0]>sw[1]+4:
        r=pg.evaluate("()=>{const r=document.querySelector('.cr-fchips.cr-act').getBoundingClientRect();return [r.x+r.width-20,r.y+r.height/2]}"); pan(pg,cdp,(r[0],r[1]),(r[0]-200,r[1]),8); ok('swipe orizzontale sui chip filtro',pg.evaluate("()=>document.querySelector('.cr-fchips.cr-act').scrollLeft")>20)
    else: ok('chip filtro entrano nello schermo',True)
    # sheet filtri: tap chip, conteggio, chiusura
    x,y=ctr(pg,'#crFbtn'); tap(pg,cdp,x,y); ok('tap apre i filtri',pg.evaluate("()=>!!document.querySelector('.cr-sheet')"))
    x,y=ctr(pg,'.cr-fg:last-of-type .a2-f'); tap(pg,cdp,x,y); ok('tap su "Solo previste"',cs(pg)['fr']==True)
    x,y=ctr(pg,'#crFgo'); tap(pg,cdp,x,y); ok('tap Mostra risultati chiude',not pg.evaluate("()=>!!document.querySelector('.cr-sheet')"))
    # ricerca con tastiera su touch
    x,y=ctr(pg,'#crQ'); tap(pg,cdp,x,y); pg.keyboard.type('wolv'); pg.wait_for_timeout(300); ok('digitazione nella ricerca',cs(pg)['q']=='wolv')
    # Parallele: swap e modalità
    setcr(pg,mode='par',pA=mcu,pB=fox); x,y=ctr(pg,'#crSwap'); tap(pg,cdp,x,y); ok('tap scambia A/B',cs(pg)['pA']==fox)
    x,y=ctr(pg,'.cr-seg .cr-sg',1); tap(pg,cdp,x,y); ok('tap modalità Corsie proprie',cs(pg)['pm']=='proprie')
    x,y=ctr(pg,'.cr-seg .cr-sg',2); tap(pg,cdp,x,y); ok('tap modalità A | B',cs(pg)['pm']=='ab')
    ls1=pg.evaluate("()=>JSON.stringify(Object.entries(localStorage).filter(e=>!e[0].startsWith('tvaHomeMiss')))"); ok('nessuna scrittura su localStorage',ls0==ls1)
    ok('nessun errore JS',not errs,errs[:3]); b.close()
print('TOTALE',N[0],'FALLITI',len(F),F)
