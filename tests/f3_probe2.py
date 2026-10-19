from playwright.sync_api import sync_playwright
import json
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{const M=tvaAtlas2.arcModel();const n=M.byId['cos-nova'];
      const mo=/magia oscura|Darkhold|Chthon/i;const hits=[];
      M.list.filter(o=>['org','art','evt','luo'].includes(o.cat)).forEach(o=>{if(Object.keys(o.f).some(k=>mo.test(o.f[k])))hits.push(o.id)});
      return {nova:n.byArcs.map(i=>[i,M.byId[i].f.DESCRIZIONE]),death:M.byId['cos-death'].byChars,maestro:M.byId['cos-maestro'].byChars,mo:hits,
      ex:M.byId['mis-stregoneria'].ex.map(x=>x.id+': '+x.txt.slice(0,90)),mut:M.byId['spe-mutanti'].arcs}}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)); b.close()
