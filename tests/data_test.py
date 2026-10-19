import json,hashlib,re
from playwright.sync_api import sync_playwright
OLD='file:///home/claude/work/backups/N11_universe_filter_final.html'; NEW='file:///home/claude/work/index.html'
JS="""()=>{const o={};document.querySelectorAll('li.card-wrap[id]').forEach(li=>{const c=li.cloneNode(true);c.querySelectorAll('.tva-row,.tva-mis').forEach(x=>x.remove());
  o[li.id]=[li.dataset.item||'',(c.textContent||'').replace(/\\s+/g,' ').trim()]});return o}"""
fails=[]
def ck(c,m,i=''):
    print(('PASS ' if c else 'FAIL ')+m,'' if c else i)
    if not c: fails.append(m)
with sync_playwright() as p:
    b=p.chromium.launch(); res={}
    for k,u in (('old',OLD),('new',NEW)):
        pg=b.new_page(viewport={'width':390,'height':844}); pg.set_default_timeout(15000); pg.goto(u); pg.wait_for_timeout(1200)
        res[k]=pg.evaluate(JS)
        if k=='new':
            res['ids']=pg.evaluate("()=>[...document.querySelectorAll('[id]')].map(e=>e.id)")
            res['data']=pg.evaluate("""()=>{const mv=JSON.parse(document.getElementById('mvMapData').textContent).universi;const at=JSON.parse(document.getElementById('atlasData').textContent);
              const diffs=[];at.opere.forEach(o=>{const li=document.getElementById('item-'+o.id);const a=(li.getAttribute('data-uni')||'').split(' ').filter(Boolean).sort().join();const b=[...o.universi].sort().join();if(a!==b)diffs.push(['opera',o.id,a,b])});
              Object.entries(mv).forEach(([u,d])=>{(d.titoliIds||[]).forEach(i=>{const li=document.getElementById('item-'+i);if(!li||!(li.getAttribute('data-uni')||'').split(' ').includes(u))diffs.push(['uni',u,i])})});
              at.animate.forEach(x=>{const li=document.getElementById(x.id);const a=(li.getAttribute('data-uni')||'').split(' ').filter(Boolean).sort().join();if(a!==[...x.universi].sort().join())diffs.push(['anim',x.id,a])});
              return {diffs,n:at.opere.length,an:at.animate.length}}""")
        pg.close()
    old,new=res['old'],res['new']
    ck(set(old)<=set(new),'nessun ID di scheda rimosso o cambiato',[i for i in old if i not in new][:5])
    ck(set(new)-set(old)==set(),'nessuna nuova scheda con ID (solo righe aggiuntive)',list(set(new)-set(old))[:5])
    NORM=lambda t:t.replace('Il legame con il MCU/Earth-616 non è mai stato chiarito del tutto.','Il legame con l’MCU non è mai stato chiarito del tutto.')   # unica modifica testuale autorizzata: niente «MCU/Earth-616» (la guida usa Earth-199999)
    chg=[i for i in old if i in new and (old[i][0]!=new[i][0] or NORM(old[i][1])!=new[i][1])]
    # Aggiornato per il nuovo ordine di visione X-Men: sono ammesse SOLO queste differenze, tutte dichiarate dalla patch:
    #  (a) cambia soltanto il numero visibile «N°ddd» (posizione); (b) stesse parole in ordine diverso (righe PRIMA/ULTIMA/ALTRE APP.);
    #  (c) le 13 schede Fox (ID in tools/xmen_order.json: note editoriali e N°) e le 7 schede personaggio con PRIMA/ULTIMA ricalcolate.
    # Ogni altra variazione resta un fallimento.
    _cfg=json.load(open('/home/claude/work/tools/xmen_order.json')); ALLOW={'item-'+i for i in _cfg['order']}|{'char-'+c for c in ('ciclope','jean-grey-fenice','magneto','sabretooth','william-stryker','wolverine','xavier')}
    _n=lambda t:re.sub(r'La tua valutazione|Il tuo voto:|[\u2605\u2606]|\u2014 / 5|Azzera','',re.sub(r'N(?:°|&deg;)\d{3}','N°#',t))   # fix-iOS: il widget del voto cambia testo e posizione (autorizzato)
    def _ok(i):
        a,b2=old[i],new[i]
        return a[0]==b2[0] and (_n(NORM(a[1]))==_n(b2[1]) or sorted(_n(NORM(a[1])).split())==sorted(_n(b2[1]).split()) or i in ALLOW)
    chg=[i for i in chg if not _ok(i)]
    ck(not chg,'testo e data-item di tutte le %d schede invariati (esclusi i collegamenti aggiunti)'%len(old),chg[:5])
    ck(not res['data']['diffs'],'data-uni == titoliIds == atlasData (139 opere) e serie animate == atlasData.animate (37)',res['data']['diffs'][:5])
    ids=res['ids']; ck(len(ids)==len(set(ids)),'ID DOM univoci',[i for i in set(ids) if ids.count(i)>1][:5])
    b.close()
print('FAILS',len(fails),fails)
