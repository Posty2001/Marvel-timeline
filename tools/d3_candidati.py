#!/usr/bin/env python3
"""D3 — elenco (SOLO elenco) dei candidati «stesso individuo» / identita' condivise, con le prove presenti nelle schede.
Nessuna unione, nessun ID modificato, nessuna relazione canonica inventata.
Input: dump JSON delle schede (d3_data.json, prodotto dai test Playwright da tvaIdx/tvaXref/atlasData). Output: CANDIDATI_IDENTITA_D3.md/.csv"""
import json,re,unicodedata,itertools,sys,csv
D=json.load(open(sys.argv[1] if len(sys.argv)>1 else '/tmp/claude-0/t/d3_data.json',encoding='utf-8'))
C={c['id']:c for c in D['chars']}; IDENT=D['ident']; TIT=D['tit']
def norm(s):
    s=unicodedata.normalize('NFD',s); s=''.join(ch for ch in s if unicodedata.category(ch)!='Mn').lower()
    return re.sub(r'[^a-z0-9]+',' ',s).strip()
TITLES={'generale','general','dr','dott','professor','prof','agente','capitano','capitan','re','regina','signor','sir','mr','mrs','miss'}
FILL={'il','la','lo','le','i','gli','the','of','di','de','van','von'}
GENERIC={'spider','man','woman','girl','boy','iron','captain','doctor','black','ant','wasp','lady','king','queen','lord','dark','blue','red','white','green','agents','shield','agente','miss'}
def alias_parts(name):
    base=re.sub(r'\([^)]*\)','',name); out=[norm(p) for p in base.split('/') if norm(p)]
    out+= [norm(x) for x in re.findall(r'\(([^)]*)\)',name) if norm(x)]
    return out
def full(n): return [t for t in n.split() if t not in FILL]
def stripped(n): return [t for t in full(n) if t not in TITLES]
def declared(a,b): return [g['id'] for g in IDENT if a in g.get('pagine',[]) and b in g.get('pagine',[])]
def initials(n): t=stripped(n); return ''.join(x[0] for x in t[:2]) if len(t)>=2 else ''
def motivi(a,b):
    A,B=C[a],C[b]; why=[]; pa=alias_parts(A['name']); pb=alias_parts(B['name'])
    na=norm(re.sub(r'\([^)]*\)','',A['name'])); nb=norm(re.sub(r'\([^)]*\)','',B['name']))
    if na and na==nb: why.append('stesso nome')
    elif set(pa)&set(pb): why.append('alias in comune')
    for x,y in itertools.product(pa,pb):
        if why: break
        for fa,fb in ((full(x),full(y)),(stripped(x),stripped(y))):
            if not fa or not fb: continue
            s,l=(fa,fb) if len(fa)<=len(fb) else (fb,fa)
            if set(s)<=set(l) and any(len(t)>=3 and t not in GENERIC for t in s):
                kind='nome contenuto nell\'altro'
                if len(s)==1 and len(l)>1: kind+=' (solo %s)'%('cognome' if l[-1]==s[0] else 'nome proprio' if l[0]==s[0] else 'una parte del nome')
                why.append(kind); break
    for x,y in ((na,nb),(nb,na)):
        if len(x.replace(' ',''))<=3 and ' ' not in x and x==initials(y) and x: why.append('sigla (%s = iniziali di «%s»)'%(x.upper(),y))
    return why
def given(n): 
    t=stripped(n); return t[0] if len(t)>=2 else None
def ev(a,b):
    A,B=C[a],C[b]; pro=[];con=[];strong=[]
    d=declared(a,b)
    if d: pro.append('dichiarate come stesso individuo in atlasData.identita (%s)'%', '.join(d))
    sa,sb=set(A['apps']),set(B['apps']); sh=sa&sb
    if sh: pro.append('titoli in comune: '+', '.join(TIT[t] for t in sorted(sh)))
    elif A['apps'] and B['apps']: con.append('nessun titolo in comune')
    sat=set(A['att'])&set(B['att'])
    if sat: pro.append('stesso interprete: '+', '.join(sorted(sat)))
    elif A['att'] and B['att']: con.append('interpreti diversi: %s / %s'%(', '.join(A['att']),', '.join(B['att'])))
    ua,ub=set(A['uni']),set(B['uni'])
    if ua&ub: pro.append('universo in comune')
    elif ua and ub: con.append('universi diversi senza sovrapposizione')
    ga,gb=given(norm(re.sub(r'\([^)]*\)','',A['name']).split('/')[0])),given(norm(re.sub(r'\([^)]*\)','',B['name']).split('/')[0]))
    if ga and gb and ga!=gb and not (set(alias_parts(A['name']))&set(alias_parts(B['name']))): strong.append('nomi propri diversi («%s» / «%s»)'%(ga,gb))
    for x,y in ((A,B),(B,A)):
        nm=x['name'].split('/')[0].strip()
        if nm and nm in y['rows']['CORR']: strong.append('la scheda di «%s» cita «%s» tra i correlati (di norma indica due persone distinte)'%(y['name'],x['name']))
    for x in (A,B):
        if x['tipo'] in('variante','aggregata','segnaposto'): con.append('«%s» è una voce di tipo «%s»'%(x['name'],x['tipo']))
    if re.search(r'\bLMD\b|giovane|anziano|piccolo|\be altri\b',A['name']+' '+B['name'],re.I): con.append('il nome indica una versione o un gruppo distinto')
    return pro,con,strong
def livello(pro,con,strong,decl):
    if decl: return 'dichiarato dalla guida'
    if strong: return 'probabili persone distinte'
    sameact=any(p.startswith('stesso interprete') for p in pro); sht=any(p.startswith('titoli in comune') for p in pro)
    if sameact and sht: return 'forte (stesso interprete e titoli in comune)'
    if sameact or (sht and any(p=='universo in comune' for p in pro)): return 'possibile'
    return 'debole (solo somiglianza del nome)'
cand={}
for a,b in itertools.combinations(C,2):
    w=motivi(a,b)
    if w: cand[(a,b)]=w
par={}
def f(x):
    while par.get(x,x)!=x: x=par[x]
    return x
res=[]
for (a,b),w in cand.items():
    pro,con,strong=ev(a,b); lv=livello(pro,con,strong,bool(declared(a,b))); res.append((a,b,w,pro,con,strong,lv))
principali=[r for r in res if not r[6].startswith('probabili')]
for a,b,*_ in principali: par[f(a)]=f(b)
groups={}
for r in principali: groups.setdefault(f(r[0]),[]).append(r)
RANK={'dichiarato':0,'forte':1,'possibile':2,'debole':3}
def rk(l): return RANK[l.split(' ')[0]]
md=[];rows=[];order=0
for g,lst in sorted(groups.items(),key=lambda kv:(min(rk(r[6]) for r in kv[1]),-len(kv[1]))):
    order+=1; members=sorted({x for r in lst for x in (r[0],r[1])})
    md.append('### %d. %s'%(order,' · '.join(C[m]['name'] for m in members)))
    md.append('Pagine: '+', '.join('`%s`'%m for m in members)+'\n')
    for a,b,w,pro,con,strong,lv in sorted(lst,key=lambda r:rk(r[6])):
        md.append('- **%s ↔ %s** — confronto per: %s. **Livello: %s.**'%(C[a]['name'],C[b]['name'],', '.join(w),lv))
        for p in pro: md.append('  - a favore: '+p)
        for c in con: md.append('  - contro: '+c)
        rows.append([order,a,b,C[a]['name'],C[b]['name'],'; '.join(w),lv,' | '.join(pro),' | '.join(con)])
    md.append('')
dist=[r for r in res if r[6].startswith('probabili')]
if dist:
    md.append('## Appendice — nomi simili ma probabili persone o versioni distinte\n')
    md.append('Non sono candidati: le schede stesse indicano che si tratta di persone diverse (nomi propri diversi, scheda che cita l\'altra tra i correlati). Riportati per trasparenza.\n')
    for a,b,w,pro,con,strong,lv in sorted(dist,key=lambda r:(C[r[0]]['name'],C[r[1]]['name'])):
        md.append('- %s ↔ %s — %s'%(C[a]['name'],C[b]['name'],'; '.join(strong)))
        rows.append(['A',a,b,C[a]['name'],C[b]['name'],'; '.join(w),lv,'','; '.join(strong+con)])
hdr=['# D3 — Candidati «stesso individuo» / identità condivise\n',
 'Documento di **sola proposta**. Nessun personaggio è stato unito, nessun ID modificato, nessuna relazione canonica creata. L\'elenco nasce dalla somiglianza dei nomi delle pagine; le «prove» sono dati già scritti nelle schede (titoli in comune, interpreti, universi, correlati). La decisione se due pagine siano la stessa persona è tua.\n',
 'Livelli: **dichiarato dalla guida** (già in `atlasData.identita`) · **forte** (stesso interprete e titoli in comune) · **possibile** · **debole** (solo nome simile) · **probabili persone distinte** (in appendice).\n',
 'Una scheda che ne cita un\'altra tra i **correlati** è trattata come indizio di persone distinte; titoli o prima apparizione in comune non bastano a provare l\'identità (due personaggi diversi compaiono spesso nello stesso film).\n',
 'Gruppi candidati: %d · confronti nell\'elenco: %d · in appendice (probabili distinti): %d\n'%(order,len(rows)-len(dist),len(dist))]
open('/home/claude/outputs/CANDIDATI_IDENTITA_D3.md','w',encoding='utf-8').write('\n'.join(hdr+md)+'\n')
with open('/home/claude/outputs/CANDIDATI_IDENTITA_D3.csv','w',encoding='utf-8',newline='') as fh:
    w=csv.writer(fh); w.writerow(['gruppo','id_a','id_b','nome_a','nome_b','confronto_per','livello','a_favore','contro']); w.writerows(rows)
from collections import Counter
print(order,len(rows)-len(dist),len(dist),Counter(r[6].split(' ')[0] for r in principali))
