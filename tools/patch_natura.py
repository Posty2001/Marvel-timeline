import re,json
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
LAB={'principale':'Continuità principale','diramazione':'Diramazione / universo alternativo','autonomo':'Universo autonomo','raggruppamento':'Raggruppamento editoriale','luogo':'Luogo narrativo (non un universo)'}
N={
'uni-earth-199999-mcu':('principale','Linea di riferimento di questa guida.'),
'uni-earth-96283-raimi-verse':('autonomo','Continuità cinematografica propria; ricompare nel MCU come variante in N°099.'),
'uni-earth-120703-garfield-verse':('autonomo','Continuità cinematografica propria; ricompare nel MCU come variante in N°099.'),
'uni-sony-s-spider-man-universe-ssu':('autonomo','Il legame con il MCU/Earth-616 non è mai stato chiarito del tutto.'),
'uni-earth-10005-fox-verse':('autonomo','Continuità propria dei film Fox, non una linea unica e continua.'),
'uni-fantastic-four-1994':('autonomo','Film isolato, senza collegamenti con altri titoli.'),
'uni-earth-121698':('autonomo','Duologia isolata, senza collegamenti con altri titoli della guida.'),
'uni-earth-trn123':('autonomo','Film isolato, senza collegamenti con altri titoli.'),
'uni-blade-verse':('autonomo','Continuità propria della trilogia.'),
'uni-daredevil-elektra-verse':('autonomo','Continuità propria dei due film.'),
'uni-ghost-rider-verse':('autonomo','Continuità propria dei due film.'),
'uni-hulk-2003-verse':('autonomo','Film isolato, senza collegamenti con altri titoli.'),
'uni-spider-noir-verse':('autonomo','Dichiarata non collegata ai film animati Spider-Verse.'),
'uni-spider-verse-sony-animato':('autonomo','Dichiarato non canonico rispetto al MCU live-action.'),
'uni-earth-828':('diramazione','Universo alternativo del multiverso MCU, separato dalla linea principale.'),
'uni-earth-838':('diramazione','Universo alternativo del multiverso MCU, separato dalla linea principale.'),
'uni-rami-di-what-if':('diramazione','Raccoglie linee temporali distinte, ciascuna nata da un evento divergente da Earth-199999: non è una continuità unica.'),
'uni-marvel-zombies-verse':('diramazione','Ramo derivato da What If…? S1, con continuità propria.'),
'uni-your-friendly-neighborhood-spider-man-verse':('diramazione','Linea alternativa del multiverso MCU, distinta dalla principale; i collegamenti con il MCU principale non sono dimostrati dalla scheda.'),
'uni-tva-fuori-dal-tempo':('luogo','Luogo fuori dal multiverso: non è una linea temporale.'),
'uni-x-men-97-verse':('autonomo','Continua X-Men: The Animated Series (1992-97); nessun collegamento confermato con il MCU principale.'),
'uni-marvel-productions-universe-anni-80':('raggruppamento','Raggruppamento editoriale (stesso studio e stesso blocco di programmazione): non è dimostrata una continuità narrativa condivisa.'),
'uni-marvel-productions-universe-anni-90':('autonomo','Universo condiviso con crossover diretto documentato tra le serie.'),
'uni-marvel-animation-universe-2006-2017':('raggruppamento','Etichetta editoriale della guida: riunisce film e serie con cast e linea produttiva comuni. La continuità comune non è dimostrata per ogni opera, quindi non va letta come un\'unica linea narrativa.'),
'uni-continuity-animate-isolate-minori':('raggruppamento','Contenitore editoriale: ogni serie ha una continuità separata e nessun crossover documentato.'),
'uni-legion-verse':('autonomo','Dichiarato separato sia dai film X-Men sia da The Gifted.'),
'uni-the-gifted-verse':('autonomo','Dichiarato separato sia da Legion sia dai film.'),
}
assert len(N)==27
esc=lambda t:t.replace('&','&amp;').replace('<','&lt;')
for uid,(code,nota) in N.items():
    a=s.index('<li class="card-wrap" id="%s"'%uid); b=s.index('</li>',a); blk=s[a:b]
    k=blk.index('<div class="detail-row"><span class="detail-k">COMPARE IN</span>')
    row='<div class="detail-row"><span class="detail-k">NATURA</span><span class="detail-v"><b>%s</b> &mdash; %s</span></div>\n            '%(LAB[code],esc(nota))
    blk=blk[:k]+row+blk[k:]
    s=s[:a]+blk+s[b:]
# atlasData
m=re.search(r'(id="atlasData">)(.*?)(</script>)',s,re.S); at=json.loads(m.group(2))
assert {u['id'] for u in at['universi']}==set(N) and len(at['universi'])==27
for u in at['universi']: u['natura']=N[u['id']][0]; u['naturaNota']=N[u['id']][1]
at['nota_natura']='natura: principale | diramazione | autonomo | raggruppamento (etichetta editoriale, non continuità dimostrata) | luogo. Non modifica universi né conteggi.'
s=s[:m.start(2)]+json.dumps(at,ensure_ascii=False,separators=(',',':'))+s[m.end(2):]
# mvMapData
m=re.search(r'(id="mvMapData">)(.*?)(</script>)',s,re.S); mv=json.loads(m.group(2))
for uid,(code,nota) in N.items():
    if uid in mv['universi']: mv['universi'][uid]['natura']=LAB[code]; mv['universi'][uid]['naturaNota']=nota
    else: print('mancante in mvMap',uid)
s=s[:m.start(2)]+json.dumps(mv)+s[m.end(2):]
# chip nella mappa
old="'</div>' + tipoHtml + atlasHtml + persHtml"
assert s.count(old)==1
s=s.replace(old,"'</div>' + naturaHtml + tipoHtml + atlasHtml + persHtml")
old="    var tipoHtml = '';\n"
assert s.count(old)==1
s=s.replace(old,"""    var naturaHtml = '';
    if (u.natura) {
      var _nEsc = function(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;'); };
      naturaHtml = '<div class="mv-map-tipo-row"><span class="mv-map-tipo-chip" id="mvMapNatura" title="' + _nEsc(u.naturaNota || '') + '">\\uD83E\\uDDED ' + _nEsc(u.natura) + '</span></div>';
    }
    var tipoHtml = '';
""")
open(P,'w',encoding='utf-8').write(s); print('ok')
