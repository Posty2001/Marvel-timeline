from leg_shot import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('alberi',{eid:'tree-ff'})"); pg.wait_for_timeout(600)
    print(pg.evaluate("""()=>{const M=tvaFamTree.parse(document.getElementById('tree-ff'),null);const L=tvaFamTree.layout(M);return {par:M.parents.map(r=>r.p.name+'>'+r.c.name),sib:M.sibs.map(s=>s[0].name+'~'+s[1].name),marr:M.marriages.map(s=>s[0].name+'='+s[1].name),units:L.units.map(u=>u.m.map(n=>n.name).join('+')+' w='+u.w+' kids='+u.kids.length+' par='+(u.par?'y':'n'))}}"""))
    b.close()
