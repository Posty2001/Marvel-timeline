from playwright.sync_api import sync_playwright
import re,json
s=open('/home/claude/work/index.html',encoding='utf-8').read()
md=json.loads(re.search(r'id="tesseraMinutesData"[^>]*>(.*?)</script>',s,re.S).group(1))
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{const out={};document.querySelectorAll('.card-wrap[id^=item-]').forEach(n=>{const id=n.id.replace('item-','');let d=null;n.querySelectorAll('.detail-row').forEach(r=>{const k=r.querySelector('.detail-k'),v=r.querySelector('.detail-v');if(k&&v&&k.textContent.indexOf('DURATA')!==-1)d=v.textContent.trim()});out[id]=d});return out}""")
    def parse(t):
        if not t or re.search(r'TBD|non ancora uscito|mai distribuito',t,re.I): return None
        m=re.search(r'(\d+)\s*episodi[^\d]*(\d+)\s*min',t)
        if m: return int(m[1])*int(m[2])
        m=re.search(r'(\d+)\s*min',t)
        return int(m[1]) if m else None
    diff=[(k,r[k],parse(r[k]),md.get(str(int(k)))) for k in r if (parse(r[k]) or 0)!=(md.get(str(int(k))) or 0)]
    print(len(diff)); [print(d) for d in diff]
