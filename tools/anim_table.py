import atlas_lib as L,csv,collections
s,mv,fam,works,anim,chars=L.load('/home/claude/work/index.html')
MPU80="Marvel Productions Universe (anni '80)"; MPU90="Marvel Productions Universe (anni '90)"; MAU='Marvel Animation Universe (2006-2017)'; MIN='Continuity animate isolate minori'; X97="X-Men '97-verse (continuità animata propria)"
R={
'spiderman81':(MPU80,"La descrizione dell'universo cita la serie; debuttò lo stesso giorno di SMAAF, stesso studio e stile",'Alta'),
'spidermanandhisamazi81':(MPU80,"Citata nella descrizione; andò in onda con The Incredible Hulk (1982) sotto titolo condiviso",'Alta'),
'theincrediblehulk82':(MPU80,"Citata nella descrizione; stesso blocco orario di SMAAF",'Alta'),
'ironman94':(MPU90,"Citata nella descrizione; Robert Hays riprende lo stesso Iron Man in Spider-Man TAS e Hulk (1996)",'Alta'),
'fantasticfour94':(MPU90,"Citata nella descrizione; apparizione del team in Spider-Man TAS con Quinton Flynn",'Alta'),
'spidermantheanimated94':(MPU90,"Citata nella descrizione; crossover documentati con Iron Man e Hulk",'Alta'),
'theincrediblehulk96':(MPU90,"Citata nella descrizione; condivide continuity e attori con Iron Man",'Alta'),
'theavengersearthsmig10':(MAU,"Hulk Vs dichiara universo condiviso con EMH, Wolverine and the X-Men e Thor: Tales of Asgard",'Alta'),
'wolverineandthexmen09':(MAU,"Stessa dichiarazione degli sceneggiatori (scheda Hulk Vs); stesso doppiatore di Hulk in EMH",'Alta'),
'ultimatespiderman12':(MAU,"La scheda dice che condivide continuity con EMH e Wolverine and the X-Men, \"parte dello stesso Marvel Animation Universe\"",'Alta'),
'avengersassemble13':(MAU,"Successore diretto di EMH; condivide continuity con Ultimate Spider-Man",'Alta'),
'hulkandtheagentsofsm13':(MAU,"Guest Spider-Man di Ultimate Spider-Man e Iron Man di Heroes United",'Alta'),
'marvelsspiderman17':(MAU,"Estremo del range 2006-2017 della descrizione; ma la scheda la definisce reboot di Ultimate Spider-Man (possibile continuità separata)",'Media'),
'thesuperherosquadsho09':(MAU,"Inclusa per conteggio (7 serie MAU); unico legame documentato è Steve Blum/Wolverine",'Media'),
'ultimateavengers06':(MAU,"Primo dei Marvel Animated Features; Invincible Iron Man ne conferma il cast",'Alta'),
'ultimateavengers2ris06':(MAU,"Sequel diretto di Ultimate Avengers",'Alta'),
'theinvincibleironman07':(MAU,"Marc Worden riprende Iron Man da Ultimate Avengers 1-2; terzo film della serie MAF",'Alta'),
'doctorstrangethesorc07':(MAU,"Film isolato ma interno alla serie Marvel Animated Features",'Media'),
'nextavengersheroesof08':(MAU,"Uno degli 11 film MAF (conteggio); Tatasciore riprende Hulk",'Media'),
'hulkvs09':(MAU,"Scheda: stesso universo condiviso di EMH, Wolverine and the X-Men e Thor: Tales of Asgard",'Alta'),
'planethulk10':(MAU,"Uno degli 11 film MAF (conteggio); nessun legame esplicito di continuity",'Media'),
'thortalesofasgard11':(MAU,"Citato da Hulk Vs come nello stesso universo condiviso",'Alta'),
'ironmanriseoftechnov13':(MAU,"La scheda lo colloca nell'universo dei film Marvel Animated Features",'Alta'),
'ironmanhulkheroesuni13':(MAU,"Richiamato dalla scheda di Hulk and the Agents of S.M.A.S.H. (Adrian Pasdar)",'Alta'),
'avengersconfidential14':(MAU,"Uno degli 11 film MAF (conteggio); Brian Bloom riprende un ruolo da EMH",'Media'),
'xmentheanimatedserie92':(X97,"La scheda lo definisce diretto predecessore narrativo di X-Men '97, che ne continua la trama; oggi non è in nessun gruppo",'Alta'),
'xmenevolution00':(MIN,"Citata nella descrizione dell'universo (11 serie isolate)",'Media'),
'thespectacularspider08':(MIN,"Citata nella descrizione; solo cameo vocale in Across the Spider-Verse",'Media'),
'ironmanarmoredadvent09':(MIN,"Citata nella descrizione; condivide solo doppiatori con X-Men: Evolution e FF: WGH",'Media'),
'fantasticfourworldsg06':(MIN,"Citata nella descrizione, ma la scheda dice che segue gli eventi del film FF (2005): possibile legame con Earth-121698 (non risolto)",'Bassa'),
'silversurfer98':(MIN,"Citata nella descrizione; la scheda contiene una nota interna di revisione finale",'Media'),
'spidermanunlimited99':(MIN,"Citata nella descrizione; ma alcuni autori la considerano sequel informale di Spider-Man TAS (non risolto)",'Bassa'),
'spiderman67':(MIN,"Citata nella descrizione; nessun collegamento diretto nella scheda",'Media'),
'themarvelsuperheroes66':(MIN,"Citata nella descrizione; nessun collegamento",'Media'),
'fantasticfour67':(MIN,"Citata nella descrizione; nessun collegamento",'Media'),
'spiderwoman79':(MIN,"Citata nella descrizione; solo Paul Soles riprende la voce di Spider-Man in 2 episodi",'Media'),
'spideyandhisamazingf21':(MIN,"Citata nella descrizione; omaggio nel titolo alla serie del 1981, non continuità",'Media'),
}
miss={a[5:] for a in anim}-set(R); extra=set(R)-{a[5:] for a in anim}
print('mancanti',miss,'extra',extra,len(R))
if not miss and not extra:
    rows=[[a,v['titolo'],v['anno'],v['universoTesto'],R[a[5:]][0],R[a[5:]][1],R[a[5:]][2],'NO (solo proposta)'] for a,v in anim.items()]
    rows.sort(key=lambda r:(r[4],r[2]))
    w=csv.writer(open('/mnt/user-data/outputs/schede_animate_proposta_universo.csv','w',encoding='utf-8-sig',newline='')); w.writerow(['ID scheda','Titolo','Anno','Universo attuale (testo scheda)','Universo proposto','Motivazione','Certezza','Applicato']); w.writerows(rows)
    print(collections.Counter((r[4],r[6]) for r in rows))
