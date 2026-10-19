import re,json
from playwright.sync_api import sync_playwright
def W(f):
    s=open(f,encoding='utf-8').read(); return json.loads(re.search(r'var WATCH_ORDER_JS = (\[.*?\]);',s).group(1))
a,b=W('/home/claude/work/index.baseline.html'),W('/home/claude/work/index.html')
print('stesso ordine:',[e['id'] for e in a]==[e['id'] for e in b],'tag diversi:',[(x['id'],x['tag'],y['tag']) for x,y in zip(a,b) if x['tag']!=y['tag']])
errs=[]
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_page(viewport={'width':390,'height':844})
    pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///mnt/user-data/outputs/index.html'); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true}")
    r=pg.evaluate("""()=>{const out={};
      const c=document.getElementById('char-edwin-jarvis'); out.char=!!c;
      if(c){const rows=[...c.querySelectorAll('.detail-row')].map(r=>r.textContent.replace(/\\s+/g,' ').trim());out.rows=rows.slice(0,4)}
      const c2=document.getElementById('item-043'); out.p043=[...c2.querySelectorAll('.detail-row')].filter(r=>r.textContent.includes('PERSONAGGI')).map(r=>r.textContent.trim());
      const c3=document.getElementById('item-042'); out.p042=[...c3.querySelectorAll('.detail-row')].filter(r=>r.textContent.includes('PERSONAGGI')).map(r=>r.textContent.trim());
      out.idx=[...document.querySelectorAll('[onclick*="char-edwin-jarvis"]')].length;
      return out}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)); print('pageerror:',errs)
