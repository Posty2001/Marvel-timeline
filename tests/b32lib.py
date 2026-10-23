from f4lib import *
import json
BADGES=['primo-passo','linea-sacra','cacciatore-varianti','archivista','essenziale','nessuna-divergenza','cinefilo','maratoneta','collezionista','weekend-guerriero','meta-strada','critico','preferiti','cronista']
def ids_of(b):
    ctx,pg,e=boot(b,390,844,atlas=False)
    ids=pg.evaluate("()=>[...document.querySelectorAll('.watch-check')].map(c=>c.dataset.item)"); anim=pg.evaluate("()=>[...document.querySelectorAll('.anim-watch-check')].map(c=>c.dataset.item)"); ctx.close(); return ids,anim
def seed_full(ids,anim,name='Franco'):
    bank={"totale":5000,"ricompensate":['2026-W%d-%s'%(w,k) for w in range(20,30) for k in ('settimanale','tematica-x','saga-y','segreta-031')]+['road-to-doomsday-v1']}
    return {'marvel-ultimate-timeline-watched':json.dumps({i:True for i in ids}),'marvel-ultimate-timeline-watched-anim':json.dumps({i:True for i in anim}),
      'marvel-ultimate-timeline-ratings':json.dumps({i:4.5 for i in ids[:12]}),'marvel-ultimate-timeline-favorites':json.dumps({i:True for i in ids[:6]}),'marvel-ultimate-timeline-notes':json.dumps({i:'n' for i in ids[:6]}),
      'marvel-ultimate-timeline-missioni-xp-bonus':json.dumps(bank),'marvel-ultimate-timeline-titoli-stagione':json.dumps(['A','B','C']),'marvel-ultimate-timeline-road-to-doomsday':json.dumps({'completata':True,'data':'2026-10-01'}),
      'marvel-ultimate-timeline-badges-earned':json.dumps(BADGES),'marvel-ultimate-timeline-user-name':name}
def seed_mid(ids,n=30,name='Franco'):
    return {'marvel-ultimate-timeline-watched':json.dumps({i:True for i in ids[:n]}),'marvel-ultimate-timeline-user-name':name}
def open_tessera(pg):
    pg.evaluate("()=>{const c=document.getElementById('tesseraToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(700)
