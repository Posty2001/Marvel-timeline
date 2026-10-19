from playwright.sync_api import sync_playwright
F='file:///home/claude/work/old_base/index.html'
fails=[]
def chk(c,m):
    if not c: fails.append(m); print('FAIL',m)
with sync_playwright() as p:
    b=p.chromium.launch()
    for vw in [(320,568),(375,667),(390,844)]:
        ctx=b.new_context(viewport={'width':vw[0],'height':vw[1]},is_mobile=True,has_touch=True); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(F); pg.wait_for_timeout(1200)
        pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(400)
        E=pg.evaluate
        # Timeline: schede aperte tramite il router (tab visibile), larghezza documento
        E("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(200)
        bad=[]
        for tid in ['item-001','item-012','item-041','item-084','item-100','item-125','item-133','item-138']:
            E("(t)=>tvaGo('item',t)",tid); pg.wait_for_timeout(700)
            sw=E("""(t)=>{const li=document.getElementById(t);const d=li&&li.querySelector('details');if(d)d.open=true;return Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-document.documentElement.clientWidth}""",tid)
            if sw>0: bad.append((tid,sw))
        print(vw,'timeline overflow',bad); chk(not bad,f'{vw} timeline overflow {bad}')
        E("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(300)
        # titoli header: nessuna parola spezzata (ogni parola entra nella larghezza del titolo)
        res=[]
        for scr in ["tvaAtlas2.ext.api.nav('confronto',{arc:'pot',eid:'|',au:'tutti',aq:''})","tvaAtlas2.ext.api.nav('arch',{arc:'org',eid:null,af:'tutti',aq:'',au:'tutti'})","tvaAtlas2.ext.api.nav('arch',{arc:'cos',eid:null,af:'tutti',aq:'',au:'tutti'})","tvaAtlas2.ext.api.nav('arch',{arc:'spe',eid:null,af:'tutti',aq:'',au:'tutti'})","tvaAtlas2.ext.api.nav('potenza',{arc:'pot',eid:null,af:'tutti',aq:'',au:'tutti'})","tvaGo('arc','org:org-s-h-i-e-l-d')","tvaGo('arc','cos:cos-living-tribunal')","tvaGo('arc','mis:mis-stregoneria')"]:
            E("()=>"+scr); pg.wait_for_timeout(120)
            m=E("""()=>{const b=document.querySelector('.a2-ttl b');const cs=getComputedStyle(b);const W=b.clientWidth;const t=b.textContent;
              const c=document.createElement('canvas').getContext('2d');c.font=cs.fontSize+' '+cs.fontFamily;
              const worst=Math.max(...t.split(/\\s+/).map(w=>c.measureText(w).width));
              const ex=document.querySelector('.a2-exit').getBoundingClientRect();const top=document.querySelector('.a2-top').getBoundingClientRect();
              return {t,W,worst:Math.round(worst),exw:Math.round(ex.width),exr:ex.right<=top.right+0.5,over:document.querySelector('.a2-top').scrollWidth-document.querySelector('.a2-top').clientWidth}}""")
            chk(m['worst']<=m['W']+1,f'{vw} titolo spezzato «{m["t"]}» parola {m["worst"]} > {m["W"]}'); chk(m['exw']>=44,f'{vw} exit {m["exw"]}'); chk(m['over']<=0,f'{vw} header overflow'); chk(m['exr'],f'{vw} exit fuori')
            res.append((m['t'][:14],m['W'],m['worst']))
        print(res)
        # immagini: nessun elemento deformato / nessun overflow nei cataloghi
        for cat in ('org','art','evt','luo','cos','spe','mis'):
            E("(c)=>tvaAtlas2.ext.api.nav('arch',{arc:c,eid:null,af:'tutti',aq:'',au:'tutti'})",cat); pg.wait_for_timeout(100)
            q=E("""()=>{const s=document.querySelector('.a2-scroll');const bad=[...document.querySelectorAll('.a2-cov')].filter(c=>{const r=c.getBoundingClientRect();return Math.abs(r.width-r.height)>0.6||r.width<20}).length;return [s.scrollWidth-s.clientWidth,bad,document.querySelectorAll('.a2-cov').length]}""")
            chk(q[0]<=0 and q[1]==0 and q[2]>0,f'{vw} {cat} cover {q}')
        E("()=>tvaAtlas2.ext.api.nav('personaggi',{pf:'tutti',pq:''})"); pg.wait_for_timeout(200)
        q=E("()=>{const s=document.querySelector('.a2-scroll');const c=[...document.querySelectorAll('.a2-prow .a2-cov')];return [s.scrollWidth-s.clientWidth,c.length,c.filter(x=>{const r=x.getBoundingClientRect();return r.width&&Math.abs(r.width-r.height)>0.6}).length]}")
        chk(q[0]<=0 and q[1]>200 and q[2]==0,f'{vw} personaggi cover {q}')
        E("()=>tvaAtlas2.openHome()"); pg.wait_for_timeout(150)
        q=E("()=>{const s=document.querySelector('.a2-scroll');return [s.scrollWidth-s.clientWidth,document.querySelectorAll('.a2-tile-bg svg,.a2-tile > .a2-bgimg').length]}"); chk(q[0]<=0 and q[1]==4,f'{vw} home decor {q}')
        chk(errs==[],f'{vw} JS {errs}'); ctx.close()
    b.close()
print('FAILS',len(fails),fails)
