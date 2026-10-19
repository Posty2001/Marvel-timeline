from leg_shot import *
import base64
F=[0]
def ok(n,c,x=''):
    print(('PASS ' if c else 'FAIL ')+n,x); F[0]+= 0 if c else 1
PNG=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==')
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    # asset assente: emblema procedurale, nessun img
    pg.evaluate("()=>tvaAtlas2.openUni('uni-earth-10005-fox-verse')"); pg.wait_for_timeout(500)
    ok('senza asset: ambiente procedurale',pg.evaluate("()=>!!document.querySelector('.ud-bg.ud-bg-proc svg')and !document.querySelector('.ud-bg-img')") if False else pg.evaluate("()=>!!document.querySelector('.ud-bg.ud-bg-proc svg') && !document.querySelector('.ud-bg-img')"))
    # asset presente (finto, solo test): viene caricato senza modificare codice
    ctx2=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,service_workers='block'); q=ctx2.new_page(); e2=[]; q.on('pageerror',lambda e:e2.append(str(e)))
    q.route('**/assets/images/tva/uni_fox.webp',lambda r:r.fulfill(status=200,content_type='image/png',body=PNG))
    q.goto(U); q.wait_for_timeout(1000); q.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); q.wait_for_timeout(400); q.click('#appTabAtlante'); q.wait_for_timeout(500)
    q.evaluate("()=>tvaAtlas2.openUni('uni-earth-10005-fox-verse')"); q.wait_for_timeout(700)
    ok('con asset: immagine di famiglia caricata',q.evaluate("()=>!!document.querySelector('.ud-bg.hm-has-img .ud-bg-img')"))
    ok('con asset: testo ancora HTML leggibile (h2 presente)',q.evaluate("()=>!!document.querySelector('.ud-hero h2')"))
    # rotta con stesso asset anche per altri universi della famiglia: Fox ha un solo universo; legacy: asset assente -> procedurale
    q.evaluate("()=>tvaAtlas2.openUni('uni-blade-verse')"); q.wait_for_timeout(500)
    ok('universo di altra famiglia senza asset: fallback',q.evaluate("()=>!!document.querySelector('.ud-bg-proc')"))
    ok('nessun errore',not e2 and not errs,e2+errs); q.screenshot(path='/tmp/claude-0/t/d3a_img_fox.png')
    print('FAILS',F[0]); b.close()
