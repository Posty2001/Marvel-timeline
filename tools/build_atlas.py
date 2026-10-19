import atlas_lib as L,json,re,sys,collections
src='/home/claude/work/index.html'
s,mv,fam,works,anim,chars=L.load(src)
CLS={ # Intervento 4: classificazione esplicita, nessuna pagina rimossa
 'char-cast-fox-verse':('segnaposto','elenco-cast-generico'),
 'char-potenzialmente-ogni-personaggio-della-lista':('segnaposto','jolly-generico'),
 'char-tbd':('segnaposto','da-definire'),
 'char-varianti-di-eroi-mcu':('segnaposto','categoria-generica-di-varianti'),
 'char-coulson-lmd':('variante','versione-LMD-di-personaggio-esistente'),
 'char-groot-piccolo':('variante','incarnazione-di-personaggio-esistente'),
 'char-professor-x-terra-838':('variante','variante-multiversale'),
 'char-victor-timely-variante-kang':('variante','variante-di-Kang'),
 'char-xavier-giovane-e-anziano':('aggregata','due-incarnazioni-in-una-pagina'),
 'char-peter-parker-holland-maguire-garfield':('aggregata','tre-incarnazioni-in-una-pagina'),
 'char-kingpin':('personaggio','ambiguo-Spider-Verse-vs-MCU-da-verificare'),
}
PH={'char-cast-fox-verse','char-potenzialmente-ogni-personaggio-della-lista','char-tbd','char-varianti-di-eroi-mcu'}
unis=[dict(id=u,nome=x['nome'],famiglia=fam.get(u)) for u,x in mv['universi'].items()]
import html as _h
_alt={('%03d'%o['num']):o['release'] for o in json.loads(re.search(r'id="altTimelineData">(.*?)</script>',s,re.S).group(1))}
_yr={};_amb={}
for m in re.finditer(r'<li class="card-wrap" id="item-(\d+)"[^>]*>(.*?)</details>\s*</li>',s,re.S):
    y=re.search(r'class="yr">(.*?)</span>',m.group(2)); a=re.search(r'AMBIENTAZIONE</span><span class="detail-v">(.*?)</span>',m.group(2),re.S)
    _yr[m.group(1)]=_h.unescape(y.group(1)) if y else None; _amb[m.group(1)]=_h.unescape(re.sub('<[^>]+>','',a.group(1))) if a else None
def _sig(i):
    ys=set(re.findall(r'\d{4}',_yr[i] or '')); uy=(_alt.get(i) or '')[:4]; ay=set(re.findall(r'\d{4}',_amb[i] or ''))
    if not ys: return 'non-determinabile'
    if uy and uy in ys: return 'uscita'
    if ys&ay: return 'ambientazione'
    return 'altro'
W=[dict(id=w['id'],tipo=w['tipo'],universi=w['uni'],annoCard=_yr[w['id']],ambientazione=_amb[w['id']],uscita=_alt.get(w['id']),significatoAnnoCard=_sig(w['id']),ruolo='primario' if len(w['uni'])==1 else ('crossover' if len(w['uni'])>1 else 'non-classificato')) for w in works.values()]
A=[dict(id=a['id'],universi=[],stato='non-classificato') for a in anim.values()]
C=[]
for k,c in chars.items():
    cer,dub,nr,et=L.resolve(c,works)
    kind,sub=CLS.get(k,('personaggio',None))
    stato='ok' if cer else ('universo-non-assegnato' if not c['uni'] else 'solo-dubbio')
    if k in PH: stato='segnaposto-da-escludere-dai-conteggi'
    C.append(dict(id=k,tipo=kind,sottotipo=sub,conta=(kind!='segnaposto'),appartenenza=cer,dubbio=dub,crossover=[],stato=stato))
# --- regole definitive di classificazione (approvate) ---
INC={'char-xavier-giovane-e-anziano':dict(sottotipo='incarnazioni-stesso-individuo',identita='singola',inc=[dict(id='giovane',universi=[L.FOX]),dict(id='anziano',universi=[L.FOX])]),
     'char-peter-parker-holland-maguire-garfield':dict(sottotipo='incarnazioni-in-universi-distinti',identita='per-universo',inc=[dict(id='holland',universi=[L.MCU]),dict(id='maguire',universi=[L.RAI]),dict(id='garfield',universi=[L.GAR])])}
OVR={}
# char-spider-man: il N°001 nella riga PRIMA APP. è un rimando alla pagina Peter Parker, non un'apparizione; prima apparizione MCU = N°067 (Civil War)
PRIMA_OVR={'char-spider-man':'067'}
# --- regole di appartenenza approvate (4 categorie distinte) ---
X97='uni-x-men-97-verse'; E838='uni-earth-838'; X97W=set(mv['universi'][X97]['titoliIds'])
RULE_NOTE={}
for c in C:
    ch=chars[c['id']]; toks=(ch['uni'] or '').split(' · ') if ch['uni'] else []
    coll=[]; prima=re.findall(r'N°(\d{3})',ch['prima'] or '')
    if c['id'] in PRIMA_OVR: prima=[PRIMA_OVR[c['id']]]
    c['continuitaOrigine']=works[prima[0]]['uni'] if prima and prima[0] in works else None
    c['produzioneMarvelStudios']=any(works[n]['studio']=='mcu' for n in ch['apps'] if n in works and not (c['id']=='char-spider-man' and n=='001'))
    # TVA e Earth-828: universo proprio; il collegamento al multiverso MCU resta narrativo, non appartenenza
    if any(t in ('MCU/TVA','MCU, Earth-828') for t in toks):
        coll+=[dict(universo=L.MCU,tipo='narrativo',origine=t) for t in toks if t in ('MCU/TVA','MCU, Earth-828')]
        c['dubbio']=[d for d in c['dubbio'] if d!=L.MCU]
    # X-Men '97: continuita' animata propria, solo se la pagina ha apparizioni documentate nella serie
    if 'Animato, continuità propria' in toks and c['id']!='char-tbd':
        if set(ch['apps'])&X97W:
            c['appartenenza']=list(dict.fromkeys(c['appartenenza']+[X97])); c['dubbio']=[d for d in c['dubbio'] if d!=X97]
    c['collegamentiMultiversoMCU']=coll
PAGE_RULES={
 'char-professor-x-terra-838':dict(appartenenza=[E838],dubbio=[],collegamentiMultiversoMCU=[dict(universo=L.MCU,tipo='narrativo',opera='102',origine='MCU multiversale')],nota='Appartiene a Earth-838; collegamento narrativo con Doctor Strange in the Multiverse of Madness (N°102), non appartenenza MCU.'),
 'char-steve-rogers-capitan-america':dict(appartenenza=[L.MCU],dubbio=[],nota='Etichetta "tutti gli universi" non assegna What If: serve l\'incarnazione specifica (non indicata nella pagina).',stato='incarnazione-non-specificata'),
}
for c in C:
    if c['id'] in PAGE_RULES: c.update(PAGE_RULES[c['id']])
for c in C:
    if c['id'] in INC:
        d=INC[c['id']]; c['sottotipo']=d['sottotipo']; c['identita']=d['identita']; c['incarnazioni']=d['inc']
        for _i in c['incarnazioni']: _i.setdefault('stato','verificata')
        assert sorted(set(u for i in d['inc'] for u in i['universi']))==sorted(c['appartenenza']),c['id']
    if c['id'] in OVR: c.update(OVR[c['id']]); c['override']=True

# ===== Fase F (approvata): incarnazioni FF, identita', assegnazioni da proposta, metriche separate, stati opera/data, animate Alta =====
import csv
CD={c['id']:c for c in C}
FFU=['uni-fantastic-four-1994','uni-earth-121698','uni-earth-trn123','uni-earth-828']
FFNAME={'uni-fantastic-four-1994':'ff-1994','uni-earth-121698':'ff-2005-2007','uni-earth-trn123':'ff-2015','uni-earth-828':'earth-828'}
for k in ('char-reed-richards','char-sue-storm','char-johnny-storm-human-torch','char-ben-grimm','char-victor-von-doom'):
    c=CD[k]; inc=[]
    for u in FFU:
        op=[n for n in chars[k]['apps'] if n in works and (works[n]['uni']==[u] or (u==L.E828 and u in works[n]['uni']))]
        if op: inc.append(dict(id=FFNAME[u],universi=[u],opere=op,stato='verificata'))
    assert all(set(i['universi'])<=set(c['appartenenza']) for i in inc),k
    if k=='char-reed-richards': inc.append(dict(id='n102-multiverso-838',universi=[],opere=['102'],stato='non-verificato',nota='Apparizione N°102 (Earth-838): incarnazione non verificata, non registrata come appartenenza.'))
    if k=='char-johnny-storm-human-torch': inc.append(dict(id='n117-etichetta-mcu-fox',universi=[],opere=['117'],stato='non-verificato',nota='Etichetta di pagina "MCU + Fox-Verse" per N°117: incarnazione non verificata.'))
    c['sottotipo']='personaggio-con-incarnazioni-per-continuita'; c['identita']='per-universo'; c['incarnazioni']=inc
    c['incarnazioniNota']='Elenco da apparizioni documentate; le voci con stato non-verificato non sono conteggiate.'
CD['char-silver-surfer']['nota']='La pagina copre solo N°030; il Surfer di Fantastic Four: First Steps (Earth-828) non è verificato e non è registrato.'
CD['char-silver-surfer']['incarnazioni']=[dict(id='ff-2005-2007',universi=['uni-earth-121698'],opere=['030'],stato='verificata'),dict(id='first-steps',universi=[],opere=['125'],stato='non-verificato')]
# assegnazioni approvate da proposta (UNIVERSI della pagina invariato: nessuna modifica UI)
MAU='uni-marvel-animation-universe-2006-2017'; MP80="uni-marvel-productions-universe-anni-80"
BASE_NOTA='Appartenenza per raggruppamento definito dalla guida (gli undici film Marvel Animated Features del Marvel Animation Universe), non prova di continuità narrativa condivisa con le altre opere. Nessun collegamento narrativo registrato.'
ASS={'char-a-bomb':(MAU,'Hulk and the Agents of S.M.A.S.H. (certezza Alta)','Alta'),'char-skaar':(MAU,'Hulk and the Agents of S.M.A.S.H. (certezza Alta)','Alta'),
     'char-firestar-angelica-jones':(MP80,"Spider-Man and His Amazing Friends (1981), universo descritto come tale (Alta)",'Alta'),
     'char-james-rogers':(MAU,'Next Avengers: Heroes of Tomorrow, uno degli 11 film MAF (raggruppamento definito dalla guida, certezza Media)','Media'),
     'char-torunn':(MAU,'Next Avengers: Heroes of Tomorrow, uno degli 11 film MAF (raggruppamento definito dalla guida, certezza Media)','Media')}
for k,(u,mot,cz) in ASS.items():
    c=CD[k]; assert not c['appartenenza']; c['appartenenza']=[u]; c['stato']='assegnazione-da-proposta-approvata'
    c['assegnazione']=dict(fonte='proposta approvata (non riportata nella riga UNIVERSI della pagina)',motivazione=mot,certezza=cz)
    if k in ('char-james-rogers','char-torunn'): c['assegnazione'].update(base='definizione-universo',nota=BASE_NOTA)
# livello identita' distinto dalle pagine (ID pagine invariati)
IDENT=[dict(id='charles-xavier',nome='Charles Xavier (Fox-Verse)',universo=L.FOX,pagine=['char-charles-xavier','char-xavier','char-xavier-giovane-e-anziano'],nota='Tre pagine, stesso individuo nel Fox-Verse (copertura sovrapposta su N°013; ordine delle timeline prima/dopo Days of Future Past non verificato). char-charles-xavier ora cita entrambi gli interpreti: James McAvoy (N°012) e Patrick Stewart (N°024). Professor X di Earth-838 è un\'identità distinta (char-professor-x-terra-838).',verifica='verificata'),
       dict(id='peter-parker-mcu',nome='Peter Parker (MCU, Holland)',universo=L.MCU,pagine=['char-peter-parker','char-peter-parker-holland-maguire-garfield','char-spider-man'],verifica='verificata; char-spider-man: prima apparizione nel ruolo MCU = N°067 (Civil War), la pagina rimanda alla voce Peter Parker; il N°001 nella sua riga PRIMA APP. è solo un rimando'),
       dict(id='peter-parker-raimi',nome='Peter Parker (Raimi-Verse, Maguire)',universo=L.RAI,pagine=['char-peter-parker','char-peter-parker-holland-maguire-garfield'],verifica='verificata'),
       dict(id='peter-parker-garfield',nome='Peter Parker (Garfield-Verse)',universo=L.GAR,pagine=['char-peter-parker','char-peter-parker-holland-maguire-garfield'],verifica='verificata'),
       dict(id='peter-parker-ynfsm',nome='Peter Parker (Your Friendly Neighborhood Spider-Man-verse)',universo=L.YF,pagine=['char-peter-parker'],verifica='verificata')]
for i in IDENT:
    for pg in i['pagine']: assert pg in CD,pg
    for pg in i['pagine']: CD[pg].setdefault('identitaIds',[]).append(i['id'])
# animate: solo certezza Alta
UN={mv['universi'][u]['nome']:u for u in mv['universi']}
UN["X-Men '97-verse (continuità animata propria)"]='uni-x-men-97-verse'
for r in csv.DictReader(open('/mnt/user-data/outputs/schede_animate_proposta_universo.csv',encoding='utf-8-sig')):
    a=next(x for x in A if x['id']==r['ID scheda'])
    if r['Certezza']=='Alta':
        a['universi']=[UN[r['Universo proposto']]]; a['stato']='classificata-proposta-approvata'; a['certezza']='Alta'; a['motivazione']=r['Motivazione']
    else:
        a['propostaNonApplicata']=dict(universo=UN[r['Universo proposto']],certezza=r['Certezza'])
_na=next(x for x in A if x['id']=='anim-nextavengersheroesof08')
_na.pop('propostaNonApplicata',None)
_na.update(universi=[MAU],stato='classificata-proposta-approvata',certezza='Media',base='definizione-universo',motivazione='Uno degli undici film Marvel Animated Features citati dalla descrizione del Marvel Animation Universe',nota=BASE_NOTA)
# stati opera / data (nessuna data inventata; badge e RILASCIO_JS invariati)
def _prec(v):
    if not v: return None
    if v=='non-distribuito': return 'non-distribuito'
    return {4:'anno',7:'mese',10:'giorno'}.get(len(v),'altro')
for w in W:
    w['precisioneUscita']=_prec(w['uscita'])
WD={w['id']:w for w in W}
WD['137'].update(statoOpera='rinnovo-ufficiale-riportato-dalla-stampa',statoData='non-ufficiale',badgeScheda='annunciato',annoRiportato='2027',nota='Scheda allineata a "2027" con badge Annunciato. Il mese marzo 2027 compare solo come stima della stampa (SuperHeroHype, IBT UK), non come data ufficiale. Nessuna data inventata; RILASCIO_JS = 2027 (titolo bloccato come prima).')
WD['134'].update(statoData='data-confermata',dataUfficiale='2027-01-13',nota='Data annunciata da Marvel Animation al New York Comic Con (ott 2026) e riportata dalla pagina Disney+; la scheda ora mostra il badge Confermato. RILASCIO_JS invariato.')
WD['138'].update(statoData='anno-ufficiale',annoUfficiale='2027',nota='Anno 2027 dichiarato da Brad Winderbaum (JoBlo, 7 ago 2026); giorno e mese non annunciati.')

cont=[c for c in C if c['conta']]
def _per(u): 
    m=[c for c in cont if u in c['appartenenza']]
    return dict(pagine=len(m),di_cui_varianti_autonome=sum(c['tipo']=='variante' for c in m),di_cui_aggregate=sum(c['tipo']=='aggregata' for c in m),di_cui_ordinarie=sum(c['tipo']=='personaggio' for c in m))
CNT=dict(nota='Quantità distinte, non sommabili tra loro né chiamabili semplicemente "personaggi".',
  pagine_uniche=len(C),pagine_conteggiabili=len(cont),pagine_segnaposto_escluse=len(C)-len(cont),
  varianti_con_pagina_autonoma=sum(c['tipo']=='variante' for c in cont),pagine_aggregate=sum(c['tipo']=='aggregata' for c in cont),
  pagine_ordinarie=sum(c['tipo']=='personaggio' for c in cont),
  pagine_conteggiabili_senza_universo=sum(1 for c in cont if not c['appartenenza']),
  incarnazioni=dict(nota='Tre quantità distinte, non sommabili: pagine con incarnazioni (pagine), incarnazioni (verificate / non verificate, conteggio per coppia pagina+id) e identità narrative (livello identita).',
    pagine_con_incarnazioni=sum(1 for c in cont if c.get('incarnazioni')),
    incarnazioni_verificate=sum(1 for c in cont for i in c.get('incarnazioni',[]) if i['stato']=='verificata'),
    incarnazioni_non_verificate=sum(1 for c in cont for i in c.get('incarnazioni',[]) if i['stato']!='verificata'),
    identita_narrative=len(IDENT)),
  metriche_varianti_per_universo={u['id']:dict(varianti_identificate_dichiarate=mv['universi'][u['id']].get('varianti'),pagine_autonome_di_variante=sum(1 for c in cont if c['tipo']=='variante' and u['id'] in c['appartenenza']),pagine_con_apparizioni_multiverso=sum(1 for c in cont if u['id'] in c['appartenenza'] and any(t in ('MCU multiversale','MCU multiversale, tutti gli universi') for t in (chars[c['id']]['uni'] or '').split(' · '))),pagine_con_collegamento_multiverso_mcu=sum(1 for c in cont if u['id']==L.MCU and c['collegamentiMultiversoMCU'])) for u in unis},
  nota_metriche_varianti='Tre misure distinte e NON sommabili: varianti identificate (valore dichiarato in mvMapData, non verificato), pagine autonome di variante, pagine con apparizioni multiverso. pagine_con_collegamento_multiverso_mcu (TVA/Earth-828) è un collegamento narrativo, non appartenenza MCU.',
  identita=dict(totale=len(IDENT),nota='Livello identità distinto dalle pagine (stesso individuo su più pagine; più incarnazioni su una pagina).'),
  schede_animate_classificate=sum(1 for a in A if a['universi']),schede_animate_totali=len(A),
  pagine_per_universo={u['id']:_per(u['id']) for u in unis})
AD=dict(versione=3,identita=IDENT,conteggi=CNT,sola_lettura=True,nota='Fonte strutturata in migrazione: non usata a runtime. appartenenza=universi certi da UNIVERSI; dubbio=etichetta ambigua; crossover non ancora distinto nei dati esistenti.',universi=unis,opere=W,animate=A,personaggi=C)
json.dump(AD,open('/home/claude/work/tools/atlasData.json','w'),ensure_ascii=False,separators=(',',':'))
blob='<script type="application/json" id="atlasData">'+json.dumps(AD,ensure_ascii=False,separators=(',',':'))+'</script>'
if 'id="atlasData"' in s: s=re.sub(r'<script type="application/json" id="atlasData">.*?</script>',lambda m:blob,s,flags=re.S)
else:
    m=re.search(r'(<script[^>]*id="mvMapData"[^>]*>.*?</script>)',s,re.S); s=s[:m.end()]+'\n'+blob+s[m.end():]
open(src,'w',encoding='utf-8').write(s)
print(len(blob),collections.Counter(c['tipo'] for c in C),collections.Counter(c['stato'] for c in C))
