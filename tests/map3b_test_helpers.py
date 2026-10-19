import sys,json,time,os,shutil,base64
from playwright.sync_api import sync_playwright
from leg_shot import boot,U
F=[];N=[0]
def ok(n,c,d=''):
    N[0]+=1
    if not c: F.append(n); print('FAIL',n,str(d)[:300])
def st(pg): return pg.evaluate("()=>JSON.parse(JSON.stringify(tvaAtlas2.stato()))")
def mp(pg): return pg.evaluate("()=>JSON.parse(JSON.stringify(tvaAtlas2.stato().mp))")
def open_map(pg):
    pg.evaluate("()=>document.querySelector('.hm-p[data-portal=multiverso]').scrollIntoView({block:'center'})"); pg.wait_for_timeout(150)
    pg.click('.hm-p[data-portal=multiverso]'); pg.wait_for_timeout(900)
def center(pg,u):
    return pg.evaluate("(u)=>{const e=document.querySelector('.mp-n[data-u=\"'+u+'\"] .mp-hit').getBoundingClientRect();return [e.x+e.width/2,e.y+e.height/2]}",u)
def tp(cdp,typ,pts):
    cdp.send('Input.dispatchTouchEvent',{'type':typ,'touchPoints':[{'x':x,'y':y,'id':i} for i,(x,y) in enumerate(pts)]})
def pan(pg,cdp,a,b,steps=10):
    tp(cdp,'touchStart',[a]); 
    for i in range(1,steps+1): tp(cdp,'touchMove',[(a[0]+(b[0]-a[0])*i/steps,a[1]+(b[1]-a[1])*i/steps)]); pg.wait_for_timeout(16)
    tp(cdp,'touchEnd',[]); pg.wait_for_timeout(250)
def pinch(pg,cdp,c,d0,d1,steps=10):
    p=lambda d:[(c[0]-d/2,c[1]),(c[0]+d/2,c[1])]
    tp(cdp,'touchStart',p(d0))
    for i in range(1,steps+1): tp(cdp,'touchMove',p(d0+(d1-d0)*i/steps)); pg.wait_for_timeout(16)
    tp(cdp,'touchEnd',[]); pg.wait_for_timeout(300)
def empty_pt(pg):
    return pg.evaluate("()=>{const w=document.querySelector('.mp-wrap').getBoundingClientRect();for(let y=w.top+30;y<w.bottom-200;y+=24)for(let x=20;x<innerWidth-80;x+=24){const e=document.elementFromPoint(x,y);if(e&&e.closest('.mp-stage')&&!e.closest('[data-u]'))return [x,y]}return null}")
def vis_nodes(pg): return pg.evaluate("()=>[...document.querySelectorAll('.mp-n:not(.off)')].map(e=>e.dataset.u)")
