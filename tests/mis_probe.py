from playwright.sync_api import sync_playwright
from leg_shot import boot
import json
TERMS={
 'stregoneria/arti mistiche':r'stregon|arti mistiche|Kamar-Taj|Sorcerer Supreme|Mystic Arts|Maestr[oi] delle Arti',
 'magia oscura':r'magia oscura|dark magic|Darkhold|Chthon|Libro dei Dannati',
 'magia del caos':r'caos|Chaos Magic|Scarlet Witch|Strega Scarlatta',
 'magia runica/rune':r'\brun[ae]|runic|\bRune\b|incantesim',
 'seidr/asgardiana':r'seidr|magia asgardian|magia di Asgard|Asgardian magic|incantatric|Enchantress|\bFrigga\b.*magi',
 'magia dimensionale/portali':r'portal|Sling Ring|Specchio|Mirror Dimension|Dimensione Specchio|dimension',
 'Sorcerer Supreme':r'Sorcerer Supreme|Stregone Supremo|Antica|Ancient One',
 'magia generica':r'\bmagi[ac]|\bmago|\bmaga\b|\bstrega|incanta|sortileg|\bmistic|occult|rituale',
 'necromanzia/Mondo dei Morti':r'necroman|Wanda.*Darkhold|Mondo dei Morti|Scarlet',
 'illusione':r'illusion|Illusion',
 'Vishanti/Agamotto/Cyttorak':r'Vishanti|Agamotto|Cyttorak|Cytorrak|Crimson Bands|Cremisi|Eye of Agamotto|Occhio di Agamotto',
 'Voodoo/Stregoneria Haitiana':r'voodoo|Voodoo|Brother Voodoo',
}
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""(T)=>{const out={};const lis=[...document.querySelectorAll('#tvaArchivesOverlayEl li[id]')].filter(l=>/^(char|art|evt|org|pia|luo|uni)-/.test(l.id));
      for(const [k,re] of Object.entries(T)){const R=new RegExp(re,'i');const hit={};const sam=[];
        for(const l of lis){const pre=l.id.split('-')[0];const rows=[...l.querySelectorAll('.detail-row')].filter(r=>!r.classList.contains('tva-row'));let h=0;
          for(const r of rows){const t=r.innerText.replace(/\\s+/g,' ');const m=t.match(R);if(m&&!h){h=1;if(sam.length<4)sam.push(l.id+': '+t.slice(Math.max(0,m.index-60),m.index+120));}}
          if(h)hit[pre]=(hit[pre]||0)+1;}
        out[k]={hit,sam};}
      return {n:lis.length,out}}""",TERMS)
    print(r['n'])
    for k,v in r['out'].items(): print('\n##',k,v['hit']); [print('   ',s) for s in v['sam']]
    b.close()
