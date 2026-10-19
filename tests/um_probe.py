from leg_shot import *
import json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("()=>({a:tvaUniverse.audit(),l:tvaUniverse.links().map(x=>[x.a.slice(4,18),x.b.slice(4,18),x.stato,x.tipi.join('/'),x.titoli.join(',')]),s:tvaUniverse.special().map(s=>({id:s.id,c:s.classe,m:s.membri.length,rel:s.relazioni.map(r=>[r.con&&r.con.slice(4,14),r.conSpecial,r.tipo,r.stato,r.titoli.join(',')])}))})")
    print(json.dumps(r['a'])); [print(x) for x in r['l']]; [print(x) for x in r['s']]; print(errs)
    for l in tvaUniverse_links if False else []: pass
    print(pg.evaluate("()=>tvaUniverse.links().filter(x=>x.stato=='verificare').map(x=>x.motivo)"))
