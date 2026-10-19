from playwright.sync_api import sync_playwright
from leg_shot import boot
import json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const I=tvaAtlas2.ext.api.IDX;const names=['First Steps','Thor','Thor: The Dark World','Thor: Ragnarok','Captain America: Civil War','Black Panther','Black Panther: Wakanda Forever','Avengers: Endgame'];
      const out={};for(const n of names){out[n]=Object.values(I.titoli).filter(t=>t.title===n||t.title.toLowerCase().endsWith(n.toLowerCase())).map(t=>[t.id||'',t.title,(t.unis||[]).join(',')])}
      const ch=['char-johnny-storm','char-ben-grimm','char-sue-storm','char-iron-man','char-t-challa-black-panther'].map(i=>[i,!!I.personaggi[i]]);
      const js=Object.keys(I.personaggi).filter(k=>/johnny|storm|torch/.test(k));
      return {out,ch,js,keys:Object.keys(I.titoli).slice(0,2),t0:I.titoli[Object.keys(I.titoli)[0]]}}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)[:3500]); b.close()
