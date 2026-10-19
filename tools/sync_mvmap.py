# M4: allinea mvMapData.personaggi ai conteggi derivati da atlasData (pagine conteggiabili). Idempotente.
import re,json
p='/home/claude/work/index.html'; s=open(p,encoding='utf-8').read()
m=re.search(r'(<script type="application/json" id="mvMapData">)(.*?)(</script>)',s,re.S); mv=json.loads(m.group(2))
assert json.dumps(mv)==m.group(2),'roundtrip mvMapData'
A=json.loads(re.search(r'id="atlasData">(.*?)</script>',s,re.S).group(1)); pu=A['conteggi']['pagine_per_universo']
ch=[]
for u,x in mv['universi'].items():
    n=pu[u]['pagine']
    if x['personaggi']!=n: ch.append((u,x['personaggi'],n)); x['personaggi']=n
s=s[:m.start(2)]+json.dumps(mv)+s[m.end(2):]
old_c="""  // Come si contano i numeri: 'personaggi' = pagine personaggio UNICHE (id char-...) che nella riga
  // UNIVERSI hanno almeno un'etichetta di quell'universo (un personaggio in piu' universi e' contato in
  // ciascuno, quindi la somma tra universi supera i 304 personaggi totali). 'varianti' = le pagine con
  // etichetta 'MCU multiversale', gia' incluse nei 'personaggi' dell'MCU. Verifica 207 MCU: 304 pagine."""
new_c="""  // Come si contano i numeri: 'personaggi' = PAGINE personaggio conteggiabili (id char-..., segnaposto esclusi)
  // con appartenenza certa a quell'universo, derivate da atlasData (un personaggio in piu' universi e' contato
  // in ciascuno, quindi la somma tra universi supera le 300 pagine conteggiabili). Pagine, incarnazioni e schede
  // animate sono quantita' distinte e non si sommano. 'varianti' = valore dichiarato (non verificato) di varianti
  // identificate, distinto dalle pagine di variante e dalle apparizioni multiverso. Il valore salvato qui e' una
  // copia di sicurezza: a runtime prevale atlasData (ATLAS_COUNTS_ENABLED) e mvAtlasVerifica() ne controlla l'allineamento."""
if old_c in s: s=s.replace(old_c,new_c)
else: print('commento gia aggiornato o non trovato')
open(p,'w',encoding='utf-8').write(s)
print(len(ch),'universi aggiornati:',[(u[4:28],a,b) for u,a,b in ch])
