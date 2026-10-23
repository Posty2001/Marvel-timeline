#!/usr/bin/env python3
"""Blocco M3 (idempotente, dopo patch_m21): Cronologie post-Endgame senza anno, Homecoming (incongruenza di continuita'), registro immagini ID->file."""
import re,json,os
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
def rep(old,new,must=1):
    global s
    if new in s and old not in s: return
    assert s.count(old)==must,(old[:60],s.count(old))
    s=s.replace(old,new)
# --- 1. Homecoming: la didascalia "otto anni dopo" e' un'incongruenza di continuita', non un riferimento cronologico ---
OLD='New York, otto anni dopo la battaglia di New York (cartello sullo schermo; anno non univoco)'
NEW='New York, dopo la battaglia di New York (post-Avengers; anno non determinabile)'
NOTA='La didascalia «otto anni dopo» mostrata nel film è un’incongruenza di continuità con il resto del MCU: non è un riferimento cronologico affidabile e non viene usata per datare il titolo.'
if OLD in s:
    s=s.replace(OLD,NEW)
j=re.search(r'(<script type="application/json" id="atlasData">)(.*?)(</script>)',s,re.S); atl=json.loads(j.group(2))
for o in atl['opere']:
    if o['id']=='075': o['ambientazione']=NEW; o['notaContinuita']=NOTA
s=s[:j.start(2)]+json.dumps(atl,separators=(',',':'),ensure_ascii=False)+s[j.end(2):]
m=re.search(r'<li class="card-wrap" id="item-075".*?</li>',s,re.S); t=m.group(0)
if 'NOTA DI CONTINUIT' not in t:
    i=t.index('AMBIENTAZIONE'); e=t.index('</div>',i)+6
    t=t[:e]+'<div class="detail-row lvl-light"><span class="detail-k">NOTA DI CONTINUITÀ</span><span class="detail-v">'+NOTA+'</span></div>'+t[e:]
    s=s[:m.start()]+t+s[m.end():]
# --- 2. Cronologie: titoli post-Endgame senza anno ufficiale, ordinati per posizione Disney+ (ordine, non data) ---
rep("e.tipo = op.tipo || null; e.ruolo = op.ruolo || null;","e.tipo = op.tipo || null; e.pos = op.posizioneDisney || null; e.ruolo = op.ruolo || null;")
rep("no.sort(cmpG); return { lista: has, senza: no };","no.sort(ord === 'ambientazione' ? function (x, y) { var px = x.pos ? x.pos.n : 1e9, py = y.pos ? y.pos.n : 1e9; return px - py || cmpG(x, y); } : cmpG); return { lista: has, senza: no };")
rep("if (s.raw) return 'Ambientazione: ' + crCut(s.raw, 50) + ' (senza anno)';","if (s.raw) return 'Ambientazione: ' + crCut(s.raw, 50) + (e.pos ? ' · pos. ' + e.pos.n + '/' + e.pos.su + ' timeline Disney+ (ordine)' : ' (senza anno)');")
rep(": crTag('n', 'senza anno'));\n      } else t.appendChild(crTag('n', 'periodo di messa in onda'));",": (e.pos ? crTag('a', 'post-Endgame · pos. ' + e.pos.n + '/' + e.pos.su) : crTag('n', 'senza anno')));\n      } else t.appendChild(crTag('n', 'periodo di messa in onda'));")
rep("(e.set.y !== null ? 'Amb. ' + e.set.lab : 'senza anno')","(e.set.y !== null ? 'Amb. ' + e.set.lab : (e.pos ? 'post-Endgame · pos. ' + e.pos.n : 'senza anno'))")
# --- 3. Dossier Opera: posizione Disney+ sotto l'ambientazione + locandina da registro ---
HELP="""    var M3A = null;
    function m3Pos(t) { try { if (!M3A) { M3A = {}; JSON.parse(document.getElementById('atlasData').textContent).opere.forEach(function (o) { M3A[o.id] = o; }); } var o = M3A[t && t.num]; return o && o.posizioneDisney ? ' · posizione ' + o.posizioneDisney.n + ' di ' + o.posizioneDisney.su + ' tra i titoli post-Endgame (timeline Disney+: ordine, non data)' : ''; } catch (e) { return ''; } }
    function m3Poster(hero, art, id, titolo) {   /* locandina registrata in TVA_IMG_MANIFEST['item:<ID>'] (solo voci con licenza e verified:true); senza file resta l'emblema */
      try {
        var t = IDX.titoli[id], M = window.TVA_IMG_MANIFEST || {}, m = t && M[(t.kind === 'anim' ? 'anim:' : 'item:') + (t.num || id)];
        if (!m || !m.src || !m.licence || m.verified !== true) return;
        var im = new Image(); im.className = 'm3-poster'; im.alt = 'Locandina: ' + titolo; im.width = m.w || 200; im.height = m.h || 300; im.loading = 'eager'; im.decoding = 'async';
        im.onload = function () { art.style.display = 'none'; }; im.onerror = function () { im.remove(); }; im.src = m.src; hero.insertBefore(im, art);
      } catch (e) { }
    }
    function renderOpera() {"""
if "var M3A = null;" not in s: rep("    function renderOpera() {",HELP)
rep("hero.appendChild(opArt(op.tipo === 'Serie' || op.kind === 'anim' ? 'serie' : 'film'));","var m3art = opArt(op.tipo === 'Serie' || op.kind === 'anim' ? 'serie' : 'film'); hero.appendChild(m3art); m3Poster(hero, m3art, id, op.titolo);")
rep("op.ambientazione ? 'luogo o epoca della storia' : null","op.ambientazione ? 'luogo o epoca della storia' + m3Pos(IDX.titoli[id]) : null")
# --- 4. Registro immagini: blob + loader (nessuna immagine scelta: voci vuote finche' l'utente non le registra) ---
man=json.load(open('/home/claude/work/assets/images/catalog/manifest.json',encoding='utf-8'))
blob='<script type="application/json" id="imageManifest">'+json.dumps(man,sort_keys=True,ensure_ascii=False,separators=(',',':'))+'</script>'
LOAD="""<script>/* M3 loader registro immagini */(function(){try{var w=window,m=w.TVA_IMG_MANIFEST=w.TVA_IMG_MANIFEST||{},d=JSON.parse(document.getElementById('imageManifest').textContent).voci||{};Object.keys(d).forEach(function(k){var v=d[k];if(v&&v.src&&v.licence&&v.verified===true&&!m[k])m[k]=v;});}catch(e){}})();</script>"""
s=re.sub(r'\n?<script type="application/json" id="imageManifest">.*?</script>\s*<script>/\* M3 loader.*?</script>','',s,flags=re.S)
mm=re.search(r'<meta name="tva-build"[^>]*>',s); s=s[:mm.end()]+'\n'+blob+LOAD+s[mm.end():]
CSS="/* M3-CSS */\n.m3-poster{display:block;width:min(46%,168px);height:auto;aspect-ratio:2/3;object-fit:cover;border-radius:10px;margin:0 0 .6rem;border:1px solid rgba(210,177,132,.4)}\n"
if '/* M3-CSS */' not in s:
    k=s.index('</style>'); s=s[:k]+CSS+s[k:]
s=s.replace('20261023-0600-m21','20261023-1000-m3')
open(P,'w',encoding='utf-8').write(s)
