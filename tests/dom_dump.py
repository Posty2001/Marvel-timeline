from playwright.sync_api import sync_playwright
import sys
JS="""(sel)=>{const root=document.querySelector(sel);if(!root)return 'NONE';
function d(e,dep){let s='  '.repeat(dep)+e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(e.className&&typeof e.className==='string'?'.'+e.className.trim().split(/\\s+/).join('.'):'');
 const t=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(' ').slice(0,40); if(t) s+='  «'+t+'»'; let out=s+'\\n';
 if(dep<4) for(const c of e.children){ if(['SCRIPT','STYLE','SVG','PATH'].includes(c.tagName.toUpperCase()))continue; out+=d(c,dep+1)} return out}
return d(root,0)}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_context(viewport={'width':390,'height':844},service_workers='block').new_page(); pg.goto('http://127.0.0.1:8124/index.html'); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(600)
    for sel in sys.argv[1:]:
        print('=====',sel); print(pg.evaluate(JS,sel)[:6000])
    b.close()
