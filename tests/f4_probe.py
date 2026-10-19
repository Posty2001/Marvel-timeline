import json,re,collections
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8124/index.html'); pg.wait_for_timeout(2500)
    r=pg.evaluate("""()=>{
      const out={};
      const keysOf=li=>[...li.querySelectorAll('.detail-row > .detail-k')].map(k=>k.textContent.trim());
      const groups={};
      document.querySelectorAll('li.card-wrap[id]').forEach(li=>{const m=/^([a-z]+)-/.exec(li.id); if(!m) return; const g=m[1]; (groups[g]=groups[g]||[]).push(li)});
      for(const g in groups){const L=groups[g]; const cnt={}; let chars=0, tot=0, noText=0; const lens=[];
        L.forEach(li=>{keysOf(li).forEach(k=>cnt[k]=(cnt[k]||0)+1); lens.push(li.textContent.length)});
        lens.sort((a,b)=>a-b);
        out[g]={n:L.length,keys:Object.entries(cnt).sort((a,b)=>b[1]-a[1]).slice(0,22),len_min:lens[0],len_med:lens[Math.floor(lens.length/2)],len_max:lens[lens.length-1]};}
      out.idx={titoli:Object.keys(tvaIdx.titoli).length,personaggi:Object.keys(tvaIdx.personaggi).length,keysT:Object.keys(tvaIdx.titoli[Object.keys(tvaIdx.titoli)[5]]),keysP:Object.keys(tvaIdx.personaggi[Object.keys(tvaIdx.personaggi)[5]])};
      return out}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)[:9000]); print(errs)
