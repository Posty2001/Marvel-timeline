# Libreria di sola lettura: estrae dal file HTML i dati esistenti (migrazione verso atlasData).
import re,html,json,collections
MCU='uni-earth-199999-mcu'; TVA='uni-tva-fuori-dal-tempo'; WIF='uni-rami-di-what-if'; E828='uni-earth-828'
FOX='uni-earth-10005-fox-verse'; SSU='uni-sony-s-spider-man-universe-ssu'; RAI='uni-earth-96283-raimi-verse'; GAR='uni-earth-120703-garfield-verse'
SVA='uni-spider-verse-sony-animato'; YF='uni-your-friendly-neighborhood-spider-man-verse'
# etichetta (token della riga UNIVERSI) -> (universi certi, universi dubbi)  | 'LEGACY' = da risolvere con le apparizioni documentate
LABELS={
 'MCU':([MCU],[]),'MCU (Netflix)':([MCU],[]),'MCU, Earth-199999':([MCU],[]),'MCU (Special Presentation)':([MCU],[]),
 'MCU (Special Presentation, b/n)':([MCU],[]),'MCU, animata, Fase Sei':([MCU],[]),
 'MCU multiversale':([MCU,WIF],[]),
 'MCU multiversale, tutti gli universi':([],[MCU,WIF]),
 'MCU/TVA':([TVA],[MCU]),
 'MCU, Earth-828':([E828],[MCU]),
 'MCU + Fox-Verse':([MCU,FOX],[]),'MCU + Raimi-Verse + Garfield-Verse':([MCU,RAI,GAR],[]),
 'Fox-Verse':([FOX],[]),'Fox-Verse, Earth-10005':([FOX],[]),
 'SSU':([SSU],[]),"Sony's Spider-Man Universe (SSU)":([SSU],[]),
 'Earth-96283':([RAI],[]),'Earth-96283 (Raimi-Verse)':([RAI],[]),
 'Earth-120703':([GAR],[]),'Earth-120703 (Garfield-Verse)':([GAR],[]),
 'Animato Sony, NON canonico MCU':([SVA],[]),'Animato Sony':([SVA],[]),
 'Animato, continuità propria':([],['uni-x-men-97-verse']),
 'Your Friendly Neighborhood Spider-Man-verse':([YF],[]),
 'Legacy, Universal Pictures, isolato':(['uni-hulk-2003-verse'],[]),
 'Legacy, Sony Pictures Television/Prime Video/MGM+, isolato':(['uni-spider-noir-verse'],[]),
 'Legacy, New Line Cinema, isolato':(['uni-blade-verse'],[]),
 'Legacy, 20th Century Fox, isolato':(['uni-daredevil-elektra-verse'],[]),
 'Legacy, Columbia/Sony, isolato':(['uni-ghost-rider-verse'],[]),
 'Legacy':'LEGACY','Legacy, continuità isolata':'LEGACY','Legacy, stessa continuità':'LEGACY',
 'Legacy, stessa continuità del film precedente':'LEGACY','Legacy, stessa continuità del 2005':'LEGACY',
}
LEGACY_UNI=['uni-fantastic-four-1994','uni-earth-121698','uni-earth-trn123','uni-blade-verse','uni-daredevil-elektra-verse','uni-ghost-rider-verse','uni-spider-noir-verse','uni-hulk-2003-verse']
def load(path):
    s=open(path,encoding='utf-8').read()
    mv=json.loads(re.search(r'<script[^>]*id="mvMapData"[^>]*>(.*?)</script>',s,re.S).group(1))
    fam={}
    for f,v in mv['famiglie'].items():
        for u in v['universi']: fam[u]=f
    works={}
    for m in re.finditer(r'<li class="card-wrap" id="item-(\d+)"([^>]*)>(.*?)</details>\s*</li>',s,re.S):
        a=m.group(2); b=m.group(3)
        du=re.search(r'data-uni="([^"]*)"',a); ty=re.search(r'data-type="([^"]*)"',a); st=re.search(r'data-studio="([^"]*)"',a)
        works[m.group(1)]=dict(id=m.group(1),num=int(m.group(1)),titolo=html.unescape(re.search(r'class="title">(.*?)</span>',b).group(1)),
            tipo=ty.group(1) if ty else None,studio=st.group(1) if st else None,uni=du.group(1).split() if du else [])
    anim={}
    for m in re.finditer(r'<li class="card-wrap" id="(anim-[^"]+)"(.*?)</details>\s*</li>',s,re.S):
        b=m.group(2); u=re.search(r'UNIVERSO</span><span class="detail-v">(.*?)</span>',b); y=re.search(r'class="yr">(.*?)</span>',b)
        anim[m.group(1)]=dict(id=m.group(1),titolo=html.unescape(re.search(r'class="title">(.*?)</span>',b).group(1)),anno=y.group(1) if y else None,
            universoTesto=html.unescape(u.group(1)) if u else None)
    chars={}
    for m in re.finditer(r'<li class="card-wrap" id="(char-[^"]+)"[^>]*>(.*?)</details></li>',s,re.S):
        b=m.group(2)
        g=lambda k:(lambda x:html.unescape(re.sub(r'<[^>]+>','',x.group(1))).strip() if x else None)(re.search(k+r'</span><span class="detail-v">(.*?)</span></div>',b,re.S))
        apps=set()
        for k in ('PRIMA APP.','ULTIMA APP.','ALTRE APP.'):
            v=g(re.escape(k))
            if v: apps.update(re.findall(r'N°(\d{3})',v))
        chars[m.group(1)]=dict(id=m.group(1),nome=html.unescape(re.search(r'class="title">(.*?)</span>',b).group(1)),
            uni=g('UNIVERSI'),prima=g(re.escape('PRIMA APP.')),apps=sorted(apps))
    return s,mv,fam,works,anim,chars
def resolve(ch,works):
    """-> (certi, dubbi, nonrisolti, etichette)"""
    if not ch['uni']: return [],[],[],[]
    et=ch['uni'].split(' · '); cer=[];dub=[];nr=[]
    for t in et:
        r=LABELS.get(t)
        if r is None: nr.append(t); continue
        if r=='LEGACY':
            u=set()
            for n in ch['apps']:
                w=works.get(n)
                if w and len(w['uni'])==1 and w['uni'][0] in LEGACY_UNI: u.add(w['uni'][0])
            if u: cer+=sorted(u)
            else: nr.append(t)
        else:
            cer+=r[0]; dub+=r[1]
    cer=list(dict.fromkeys(cer)); dub=[d for d in dict.fromkeys(dub) if d not in cer]
    return cer,dub,nr,et
