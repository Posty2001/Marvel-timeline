P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
def card_span(i):
    a=s.index('<li class="card-wrap" id="item-%s"'%i); return a, s.index('</li>',a)
MK='</details></div>\n      <details class="watch-picker">'
def nota(rows):
    body=''.join('<div class="detail-row "><span class="detail-k">%s</span><span class="detail-v ">%s</span></div>'%(k,v) for k,v in rows)
    return '</details><details class="sub-group sub-order-why">\n          <summary>&#129517; Perch&eacute; questa posizione</summary>\n          <div class="sub-group-body">'+body+'</div>\n        </details></div>\n      <details class="watch-picker">'
N={
'010':[("ORDINE DI USCITA","Kraven the Hunter esce il 13 dicembre 2024, dopo Venom: The Last Dance (25 ottobre 2024)."),("ORDINE CONSIGLIATO QUI","Kraven precede The Last Dance perch&eacute; non ha collegamenti confermati con gli altri film del suo universo, mentre The Last Dance chiude l&rsquo;arco aperto dal crossover con No Way Home. Si possono invertire senza perdere nulla: la modalit&agrave; &laquo;Uscita&raquo; della Timeline alternativa li mostra nell&rsquo;ordine reale.")],
'011':[("ORDINE DI USCITA","Venom: The Last Dance esce il 25 ottobre 2024, prima di Kraven the Hunter (13 dicembre 2024)."),("ORDINE CONSIGLIATO QUI","&Egrave; messo per ultimo tra i film del suo universo perch&eacute; chiude l&rsquo;arco aperto dal crossover con No Way Home (N&deg;099). Non cambia i collegamenti con Kraven, che non ne ha.")],
'130':[("ORDINE DI USCITA","La prima stagione &egrave; uscita a marzo 2024, prima di molti titoli che la precedono in questo elenco."),("ORDINE CONSIGLIATO QUI","Viene dopo i titoli live-action di riferimento perch&eacute; &egrave; FACOLTATIVA e non ha collegamenti confermati con l&rsquo;MCU live-action. &Egrave; una serie animata con continuit&agrave; propria, non un ramo dimostrato del MCU: la sua posizione non indica che i fatti avvengano dopo i titoli vicini.")],
'131':[("ORDINE DI USCITA","La seconda stagione &egrave; uscita il 1 luglio 2026."),("ORDINE CONSIGLIATO QUI","Segue la prima stagione e resta nel blocco dei titoli facoltativi, perch&eacute; non ha collegamenti confermati con l&rsquo;MCU live-action. La vicinanza con altri titoli non indica una continuit&agrave; comune.")],
'134':[("ORDINE DI USCITA","Esce il 13 gennaio 2027, dopo Avengers: Doomsday (18 dicembre 2026), che nella lista la segue."),("ORDINE CONSIGLIATO QUI","La sua posizione rispetto a N&deg;136 non indica una dipendenza: non &egrave; un prerequisito di Doomsday e la serie ha una linea temporale alternativa, distinta da quella del Peter Parker live-action. Prosegue la stagione 1 (N&deg;120).")],
}
for i,rows in N.items():
    a,b=card_span(i); blk=s[a:b]
    mk=MK if blk.count(MK)==1 else '</details></div>\n      \n      <div class="rating-widget"'
    assert blk.count(mk)==1,i
    rep=nota(rows) if mk==MK else nota(rows).replace('\n      <details class="watch-picker">','\n      \n      <div class="rating-widget"')
    s=s[:a]+blk.replace(mk,rep)+s[b:]
# legenda: colonna "Tre ordini"
old='''    <div class="legend-col">
      <h4>Categorie di canone</h4>'''
assert s.count(old)==1
s=s.replace(old,'''    <div class="legend-col">
      <h4>Tre ordini diversi</h4>
      <p class="legend-editorial-note">Consigliato, uscita ed eventi non coincidono. Cambia solo la vista: le schede, i progressi e gli XP restano gli stessi.</p>
      <div class="legend-row"><b>Consigliato</b> l&rsquo;ordine di visione della guida (predefinito)</div>
      <div class="legend-row"><b>Uscita</b> in base alla data di uscita reale</div>
      <div class="legend-row"><b>Eventi</b> per anno di ambientazione, separato per continuit&agrave;; le date incerte sono segnate con ~ (Timeline alternativa)</div>
    </div>
    <div class="legend-col">
      <h4>Categorie di canone</h4>''')
open(P,'w',encoding='utf-8').write(s); print('ok')
