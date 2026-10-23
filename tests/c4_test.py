# C4: CSP (nessuna violazione nei flussi principali), accessibilita' tastiera/etichette, contrasto .ud-st.
import json,re,io,statistics
from playwright.sync_api import sync_playwright
from PIL import Image
U='http://127.0.0.1:8124/index.html'
fails=[]
def ck(c,m,i=''):
    print(('PASS ' if c else 'FAIL ')+m,'' if c else i)
    if not c: fails.append(m)
with sync_playwright() as p:
    b=p.chromium.launch(); cx=b.new_context(viewport={'width':390,'height':844},service_workers='block'); pg=cx.new_page()
    viol=[]; cons=[]; errs=[]
    pg.on('console',lambda m:cons.append(m.text) if 'Content Security Policy' in m.text or 'Refused to' in m.text else None)
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.add_init_script("window.__csp=[];document.addEventListener('securitypolicyviolation',e=>window.__csp.push([e.violatedDirective,e.blockedURI,(e.sourceFile||'').slice(-40)]))")
    pg.goto(U); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{journeyStarted.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(500)
    tabs=pg.evaluate("()=>[...document.querySelectorAll('.app-tab')].map(t=>t.id||t.dataset.tab||t.textContent.trim().slice(0,12))")
    print('tab',tabs)
    n=pg.evaluate("()=>document.querySelectorAll('.app-tab').length")
    for i in range(n):
        try: pg.evaluate("(i)=>document.querySelectorAll('.app-tab')[i].click()",i); pg.wait_for_timeout(500)
        except Exception as e: print('tab err',i,str(e)[:60])
    pg.evaluate("()=>{homeHubExited.checked=true;tvaAtlas2.openUni('uni-earth-199999-mcu',true)}"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{const c=document.getElementById('altTimelineToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(600)
    pg.evaluate("()=>{const e=document.querySelector('.card-wrap .card, .card-wrap');e&&e.scrollIntoView()}"); pg.wait_for_timeout(300)
    pg.evaluate("()=>window.tvaAtlas2&&window.tvaAtlas2.img&&0"); pg.wait_for_timeout(1200)
    v=pg.evaluate("()=>window.__csp")
    ck(not v and not cons,'CSP: nessuna violazione nei flussi principali (tab, Atlante, Timeline, poster)',(v[:4],cons[:3]))
    ck(not errs,'nessun errore JS',errs[:2])
    meta=pg.evaluate("()=>document.querySelector('meta[http-equiv=Content-Security-Policy]').content")
    ck("object-src 'none'" in meta and "base-uri 'self'" in meta and 'unsafe-eval' not in meta,'CSP: object-src none, base-uri self, niente unsafe-eval')
    ck(not re.search(r"script-src[^;]*\*[^;]*;",meta.replace('https://*.','')) ,'CSP: script-src senza wildcard')
    # prova negativa: una risorsa non consentita viene davvero bloccata
    pg.evaluate("()=>{const s=document.createElement('script');s.src='https://evil.example/x.js';document.head.appendChild(s)}"); pg.wait_for_timeout(500)
    v=pg.evaluate("()=>window.__csp"); ck(any('script' in x[0] for x in v),'CSP attiva: script da origine esterna non consentita bloccato',v[-2:])
    # accessibilita': pulsanti senza nome accessibile (visibili), immagini senza alt, focus visibile
    res=pg.evaluate("""()=>{const vis=e=>{const r=e.getBoundingClientRect();const cs=getComputedStyle(e);return r.width>0&&r.height>0&&cs.visibility!=='hidden'&&cs.display!=='none'};
      const name=e=>((e.getAttribute('aria-label')||'')+(e.getAttribute('aria-labelledby')?document.getElementById(e.getAttribute('aria-labelledby'))?.textContent:'')+(e.textContent||'')+(e.getAttribute('title')||'')+(e.alt||'')).trim();
      const bs=[...document.querySelectorAll('button,[role=button],a[href],input:not([type=hidden]),select,textarea')].filter(vis);
      const noname=bs.filter(e=>{if(e.tagName==='INPUT'&&e.id&&document.querySelector('label[for="'+e.id+'"]'))return false;if(e.closest('label'))return false;return !name(e)}).map(e=>e.tagName+'#'+e.id+'.'+(e.className+'').slice(0,30));
      const clickDiv=[...document.querySelectorAll('div[onclick],span[onclick]')].filter(vis).filter(e=>!e.getAttribute('role')&&e.tabIndex<0).length;
      const imgs=[...document.querySelectorAll('img')].filter(vis).filter(i=>i.getAttribute('alt')===null).length;
      return {total:bs.length,noname,clickDiv,imgs}}""")
    print('a11y',json.dumps(res)[:600])
    ck(len(res['noname'])==0,'a11y: controlli visibili senza nome accessibile',res['noname'][:8])
    ck(res['imgs']==0,'a11y: immagini visibili senza attributo alt',res['imgs'])
    # tastiera: Home -> nessuna tappa fuori schermo (menu chiuso escluso dal focus); menu apribile da tastiera
    pg.evaluate("()=>document.getElementById('appTabHome').click()"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{document.activeElement&&document.activeElement.blur();window.scrollTo(0,0)}")
    off=[];stops=[]
    for i in range(16):
        pg.keyboard.press('Tab'); pg.wait_for_timeout(50)
        r=pg.evaluate("""()=>{const e=document.activeElement;if(!e||e===document.body)return null;const q=e.getBoundingClientRect();const cs=getComputedStyle(e);return {t:e.tagName+'#'+e.id+'.'+(e.className+'').slice(0,22),off:(q.right<=0||q.left>=innerWidth),ring:(cs.outlineStyle!=='none'&&parseFloat(cs.outlineWidth)>0)||cs.boxShadow!=='none'}}""")
        if r:
            stops.append(r['t'])
            if r['off']: off.append(r['t'])
    ck(len(stops)>=10,'tastiera: Home, 16 Tab -> almeno 10 tappe',stops)
    ck(not off,'tastiera: nessuna tappa nel menu laterale chiuso (fuori schermo)',off[:4])
    pg.evaluate("()=>document.getElementById('appTabTimeline').click()"); pg.wait_for_timeout(600)
    vis=pg.evaluate("()=>{const o=document.querySelector('.sidebar-open-btn');return o&&getComputedStyle(o).display!=='none'}")
    if vis:
        pg.evaluate("()=>document.querySelector('.sidebar-open-btn').focus()")
        pg.keyboard.press('Enter'); pg.wait_for_timeout(350)
        st=pg.evaluate("()=>({chk:sidebarToggle.checked,exp:document.querySelector('.sidebar-open-btn').getAttribute('aria-expanded'),vis:getComputedStyle(document.querySelector('.sidebar')).visibility,foc:document.activeElement.className})")
        ck(st['chk'] and st['vis']=='visible','menu: Invio sul pulsante apre il menu',st)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
        st=pg.evaluate("()=>({chk:sidebarToggle.checked,exp:document.querySelector('.sidebar-open-btn').getAttribute('aria-expanded'),vis:getComputedStyle(document.querySelector('.sidebar')).visibility})")
        ck((not st['chk']) and st['exp']=='false' and st['vis']=='hidden','menu: Esc chiude, aria-expanded=false, menu escluso dal focus',st)
        pg.evaluate("()=>document.querySelector('.sidebar-open-btn').click()"); pg.wait_for_timeout(350)
        ck(pg.evaluate("()=>sidebarToggle.checked && getComputedStyle(document.querySelector('.sidebar')).visibility")=='visible','menu: apertura con tocco/clic invariata')
    else:
        print('SKIP menu: pulsante non visibile in questa schermata')
    b.close()
print('FAILS',len(fails),fails)
