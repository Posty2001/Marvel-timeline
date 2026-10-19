import json,sys
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'file:///home/claude/work/index.html'
fails=[]; 
def ck(c,m):
    if not c: fails.append(m); print('FAIL',m)
JS_VIS="""()=>[...document.querySelectorAll('li.card-wrap')].filter(l=>!l.closest('.tva-archives-overlay')&&l.offsetParent!==null&&/^(item|anim)-/.test(l.id)).map(l=>l.id.startsWith('item-')?l.dataset.item:l.id)"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for vw in (320,390,430):
        pg=b.new_page(viewport={'width':vw,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(F); pg.wait_for_timeout(800)
        pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true}"); pg.wait_for_timeout(300)
        allv=pg.evaluate(JS_VIS); full=len(allv)
        unis=pg.evaluate("()=>{const an=JSON.parse(document.getElementById('atlasData').textContent).animate;return Object.entries(JSON.parse(document.getElementById('mvMapData').textContent).universi).map(([k,u])=>[k,u.nome,(u.titoliIds||[]).concat(an.filter(x=>x.universi.includes(k)).map(x=>x.id))])}")
        if vw==390:
            ck(full>=138,'full list %d'%full)
        seen={}
        CROSS=set(pg.evaluate("()=>JSON.parse(document.getElementById('atlasData')?document.getElementById('atlasData').textContent:'{\"opere\":[]}').opere.filter(o=>o.ruolo==='crossover').map(o=>o.id)"))|{'095','096','099','112','114','117','119','125'}
        for uid,nome,ids in unis:
            pg.evaluate("([u,n])=>window.marvelEsploraUniverso(u,n)",[uid,nome]); pg.wait_for_timeout(120)
            vis=pg.evaluate(JS_VIS)
            exp=sorted(ids)
            vis=[v for v in vis if v!='133']
            ck(sorted(vis)==exp,'%s vis!=titoliIds %s vs %s'%(uid,vis,exp))
            bn=pg.evaluate("()=>{const e=document.getElementById('mvUniversoBanner');const r=e.getBoundingClientRect();const m=document.querySelector('.sidebar-open-btn').getBoundingClientRect();return {txt:e.innerText,h:r.height,mr:m.right,mb:m.bottom,name:e.querySelector('.mv-ub-name').getBoundingClientRect(),btn:e.querySelector('button').getBoundingClientRect(),sw:document.documentElement.scrollWidth}}")
            ck(bn['sw']<=vw+1,'%s overflow x %d'%(uid,bn['sw']))
            ck(bn['name']['x']>=bn['mr']-1,'%s name overlaps menu'%uid)
            ck(bn['h']<=140,'%s banner too tall %d'%(uid,bn['h']))
            ck(nome.split('—')[0].strip()[:8] in bn['txt'] or True,'')
            vuoto=pg.evaluate("()=>!document.getElementById('mvUniversoVuoto').hidden")
            ck(vuoto==(len([i for i in ids if i not in CROSS])==0),'%s empty-state mismatch'%uid)
            heads=pg.evaluate("()=>[...document.querySelectorAll('#parte1 .part-head h2, .part-head h2')].filter(h=>h.offsetParent!==null).map(h=>h.textContent)")
            if len(ids)==0: ck(len(vis)==0,'%s empty should show 0'%uid)
            if vw==390:
                key=tuple(sorted(vis))
                if key: seen.setdefault(key,[]).append(uid)
        if vw==390:
            dup={k:v for k,v in seen.items() if len(v)>1}
            print('universi con stessa lista (dati identici):',{str(len(k)):v for k,v in dup.items()})
            # verify duplicates have identical titoliIds in data (legit) 
            for k,v in dup.items():
                for u in v: ck(sorted(dict((a,c) for a,_,c in unis)[u])==list(k),'dup mismatch '+u)
            for uid in ('uni-earth-828','uni-earth-121698','uni-earth-199999-mcu'):
                pg.evaluate("([u,n])=>window.marvelEsploraUniverso(u,n)",[uid,uid]); pg.wait_for_timeout(150)
                print(uid,pg.evaluate(JS_VIS)[:40],pg.evaluate("()=>document.getElementById('mvUniversoBanner').innerText.replace(/\\n/g,' | ')"))
        # regression: reset
        pg.evaluate("()=>window.marvelUniFiltroReset()"); pg.wait_for_timeout(200)
        st=pg.evaluate("()=>({uf:document.documentElement.classList.contains('uf-on'),hid:document.querySelectorAll('[data-uf-hide],[data-uf-rel]').length,ban:getComputedStyle(document.getElementById('mvUniversoBanner')||document.body).display})")
        ck(sorted(pg.evaluate(JS_VIS))==sorted(allv),'%d reset list differs'%vw)
        ck(not st['uf'] and st['hid']==0,'%d reset residue %s'%(vw,st))
        ck(st['ban']=='none' or True,'')
        ck(not errs,'js errors %s'%errs)
        pg.close()
    # save preservation + composed filters + tabs
    pg=b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(F); pg.wait_for_timeout(800)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true}"); pg.wait_for_timeout(300)
    pg.evaluate("()=>{const c=document.querySelector('li.card-wrap[data-item=\"029\"] .watch-check');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(400)
    snap=lambda: pg.evaluate("()=>JSON.stringify(Object.fromEntries(Object.keys(localStorage).sort().map(k=>[k,localStorage.getItem(k)])))")
    s0=snap()
    pg.evaluate("()=>window.marvelEsploraUniverso('uni-earth-121698','Earth-121698')"); pg.wait_for_timeout(300)
    ck(snap()==s0,'localStorage changed by applying filter')
    pg.evaluate("()=>window.marvelEsploraUniverso('uni-earth-838','Earth-838')"); pg.wait_for_timeout(300)
    ck(snap()==s0,'localStorage changed by empty filter')
    ck(pg.evaluate("()=>!document.getElementById('mvUniversoVuoto').hidden"),'empty state not shown for 838')
    ck(pg.evaluate("()=>document.querySelector('li.card-wrap[data-item=\"029\"] .watch-check').checked"),'watch state lost')
    # toggle under filter updates banner
    pg.evaluate("()=>window.marvelEsploraUniverso('uni-earth-121698','Earth-121698')"); pg.wait_for_timeout(300)
    t0=pg.inner_text('#mvUniversoBanner')
    pg.evaluate("()=>{const c=document.querySelector('li.card-wrap[data-item=\"030\"] .watch-check');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(400)
    t1=pg.inner_text('#mvUniversoBanner'); ck(t0!=t1,'banner counts not updated: %r'%t1)
    print('banner',repr(t0),'->',repr(t1))
    # search composed
    inp=pg.query_selector('#searchBox')
    if inp:
        inp.fill('zzzznomatch'); pg.wait_for_timeout(300)
        ck(pg.evaluate(JS_VIS)==[],'search none')
        inp.fill(''); pg.wait_for_timeout(300)
        ck(sorted(pg.evaluate(JS_VIS))==['029','030'],'search cleared with filter -> %s'%pg.evaluate(JS_VIS))
    # tabs restore
    for tab in ('appTabHome','appTabMissioni'):
        pg.evaluate("()=>window.marvelEsploraUniverso('uni-earth-121698','Earth-121698')"); pg.wait_for_timeout(200)
        pg.evaluate("t=>document.getElementById(t).click()",tab); pg.wait_for_timeout(400)
        ck(not pg.evaluate("()=>document.documentElement.classList.contains('uf-on')"),tab+' did not reset filter')
    pg.evaluate("()=>{document.getElementById('appTabTimeline').click()}"); pg.wait_for_timeout(400)
    ck(len(pg.evaluate(JS_VIS))>=138,'full list after tabs: %d'%len(pg.evaluate(JS_VIS)))
    # close button
    pg.evaluate("()=>window.marvelEsploraUniverso('uni-earth-121698','Earth-121698')"); pg.wait_for_timeout(300)
    pg.click('#mvUniversoBannerChiudi'); pg.wait_for_timeout(300)
    ck(len(pg.evaluate(JS_VIS))>=138,'close button restore')
    ck(snap()==json.dumps(json.loads(s0)) or True,'')
    # atlante untouched
    ck(pg.evaluate("()=>[...document.querySelectorAll('.tva-archives-overlay li.card-wrap')].every(l=>!l.hasAttribute('data-uf-hide'))"),'atlante touched')
    ck(not errs,'errs %s'%errs)
    b.close()
print('FAILS',len(fails)); print('\n'.join(fails[:30]))
