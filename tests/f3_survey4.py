from playwright.sync_api import sync_playwright
import json,re,collections
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{
      const terms=['Kree','Skrull','Asgardian','Asgard','Celestial','Deviant','Eterni','Chitauri','Xandar','Kronan','Atlantidei','Talokan','Wakand','Sakaar','Ravager','Inumani','Inhuman','Symbiote','simbiot','Mutant','mutant','Vampir','Licantrop','Kamar-Taj','Sanctum','Darkhold','Stregon','Hexe','Sorcerer','Mistic','mistic','Arti Mistiche','magia','Ancient One','Antico','Cabala','Vishanti','Wanda','Scarlet','Chaos Magic','Ghost Rider','Spirito','Titani','Eternals','Elfi','Giganti di Ghiaccio','Jotun','Nova Corps','Guardiani','Collezionista','Skrulls','Krylor','Sovereign','Sovrani','Ravagers','Flora colossus'];
      const out={};
      const all=[...document.querySelectorAll('li[id^=char-],details[id^=char-]')];
      const nonchar=[...document.querySelectorAll('details.card')].filter(c=>!/^char-/.test(c.id));
      terms.forEach(t=>{const re=new RegExp(t,'i');out[t]=[all.filter(c=>re.test(c.innerText)).length,nonchar.filter(c=>re.test(c.innerText)).length]});
      return out}""")
    print(json.dumps(r,ensure_ascii=False)); b.close()
