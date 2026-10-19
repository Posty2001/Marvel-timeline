P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
def li(i):
    a=s.index('<li class="card-wrap" id="item-%s"'%i); return a, s.index('</li>',a)
note='''</details><details class="sub-group sub-order-why">
          <summary>&#129517; Perch&eacute; questo ordine</summary>
          <div class="sub-group-body"><div class="detail-row "><span class="detail-k">ORDINE DI USCITA</span><span class="detail-v ">Deadpool (2016) &rarr; Logan (2017) &rarr; Deadpool 2 (2018).</span></div><div class="detail-row "><span class="detail-k">ORDINE CONSIGLIATO QUI</span><span class="detail-v ">Logan &rarr; Deadpool &rarr; Deadpool 2. &Egrave; una scelta editoriale di questa guida: chiude prima l&rsquo;arco di Wolverine (Hugh Jackman) e poi porta i due Deadpool, consecutivi, verso Deadpool &amp; Wolverine (N&deg;117), che richiama sia Logan sia i due Deadpool.</span></div><div class="detail-row "><span class="detail-k">CRONOLOGIA INTERNA</span><span class="detail-v ">Non &egrave; la ragione dello spostamento. Logan &egrave; ambientato nel 2029, quindi dopo gli eventi dei due Deadpool nel loro tempo narrativo: qui compare prima solo per il percorso di visione. I film Fox non formano un&rsquo;unica linea del tempo continua (dopo X-Men: Giorni di un futuro passato la continuit&agrave; viene riscritta) e questa guida non sostiene che le varie incarnazioni di Wolverine siano un solo personaggio coerente.</span></div><div class="detail-row "><span class="detail-k">SE PREFERISCI</span><span class="detail-v ">L&rsquo;ordine di uscita &egrave; disponibile nella Timeline alternativa (modalit&agrave; &laquo;Uscita&raquo;). Gli identificativi e i progressi delle schede non cambiano.</span></div></div>
        </details></div>
      <details class="watch-picker">'''
# Logan
a,b=li('024'); blk=s[a:b]; mk='</details></div>\n      <details class="watch-picker">'
assert blk.count(mk)==1
s=s[:a]+blk.replace(mk,note)+s[b:]
# rimandi su Deadpool / Deadpool 2
for i,old in (('022',"Essenziale per Deadpool &amp; Wolverine"),('023',"Introduce Domino e Cable, essenziale per Deadpool &amp; Wolverine")):
    a,b=li(i); blk=s[a:b]; assert blk.count(old)==1
    s=s[:a]+blk.replace(old,old+". In questo percorso segue Logan (N&deg;022) per scelta editoriale, non per cronologia: vedi &laquo;Perch&eacute; questo ordine&raquo; nella scheda di Logan")+s[b:]
open(P,'w',encoding='utf-8').write(s); print('ok')
