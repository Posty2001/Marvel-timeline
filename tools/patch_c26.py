#!/usr/bin/env python3
"""Patch C2-C6 (idempotente, dopo patch_m342): coerenza modalita' Timeline/backup (C2), versionamento service worker (C3),
contrasto .ud-st-vf e CSP (C4). Non tocca catalogo, progressi, voti, XP, ricompense, Firebase."""
import re
P='/home/claude/work/index.html'; SW='/home/claude/work/sw.js'
BUILD='20261023-1520-c26'
s=open(P,encoding='utf-8').read()
def rep(old,new,marker):
    global s
    if marker in s: return
    assert s.count(old)==1,(old[:70],s.count(old)); s=s.replace(old,new)
# --- C2a: la modalita' salvata 'custom' riapre la vista Personalizzato solo se esiste un ordine (stessa regola della Home)
rep("          var m341c = false; try { m341c = localStorage.getItem('marvelGuideActiveTimelineMode') === 'custom'; } catch(eM341c) {}",
    "          var m341c = false; try { m341c = localStorage.getItem('marvelGuideActiveTimelineMode') === 'custom'; var c26o = atGetCustomOrder(); if (!Array.isArray(c26o) || !c26o.length) m341c = false; /* C26: senza ordine salvato si riparte dal consigliato, come la Home */ } catch(eM341c) {}",
    'C26: senza ordine salvato')
# --- C2b: «Cancella tutto» azzera anche la modalita' attiva locale (l'ordine viene rimosso con PROFILE_OBJ_KEYS)
rep("        localStorage.removeItem('marvel-ultimate-timeline-tessera-photo');   // B3.2: foto personale (solo locale)\n",
    "        localStorage.removeItem('marvel-ultimate-timeline-tessera-photo');   // B3.2: foto personale (solo locale)\n        localStorage.removeItem('marvelGuideActiveTimelineMode');   // C26: modalita' Timeline attiva (solo locale, mai in backup/sync)\n",
    'C26: modalita\' Timeline attiva')
# --- C2c: documentazione nel codice del campo preferredMode
rep("      preferredMode: 'marvel-ultimate-timeline-preferred-mode',\n",
    "      preferredMode: 'marvel-ultimate-timeline-preferred-mode',   /* C26: preferenza DICHIARATA nel quiz (uscita|cronologico); informativa, non governa la Home. Resta nel backup per compatibilita'. La modalita' attiva e' 'marvelGuideActiveTimelineMode' (solo locale) */\n",
    'C26: preferenza DICHIARATA')
# --- C4a: contrasto reale insufficiente (misurato sui pixel: 4.10-4.22) su .ud-st-vf -> >= 4.5
rep(".ud-st-vf { background: rgba(219,119,124,0.12); color: var(--a2-acc); border: 1px dashed var(--a2-acc); }",
    ".ud-st-vf { background: rgba(219,119,124,0.12); color: #EA9195; /* C26: contrasto >= 4.5:1 (era 4.1-4.2) */ border: 1px dashed var(--a2-acc); }",
    'C26: contrasto')

# --- C4c: accessibilita' tastiera del menu laterale (mobile): il drawer chiuso non entra nell'ordine di tabulazione; apri/chiudi con Invio/Spazio/Esc; aria-expanded aggiornato
rep("  #sidebarToggle:checked ~ .sidebar { transform: translateX(0); }\n  #sidebarToggle:checked ~ .sidebar-open-btn { display: none; }\n}",
    "  #sidebarToggle:checked ~ .sidebar { transform: translateX(0); }\n  #sidebarToggle:checked ~ .sidebar-open-btn { display: none; }\n"
    "  /* C26 a11y: il menu chiuso e' fuori schermo E fuori dal focus */\n  .sidebar { visibility: hidden; transition: transform 0.2s, visibility 0s linear 0.2s; }\n"
    "  #sidebarToggle:checked ~ .sidebar, #infoOverlayToggle:checked ~ .sidebar { visibility: visible; transition-delay: 0s; }\n}",
    'C26 a11y: il menu chiuso')
C26JS=("<script>/* C26 a11y */(function(){try{var t=document.getElementById('sidebarToggle');if(!t)return;var o=document.querySelector('.sidebar-open-btn'),c=document.querySelector('.sidebar-close-btn');"
 "function sync(){if(o)o.setAttribute('aria-expanded',t.checked?'true':'false');}"
 "function set(v){t.checked=v;t.dispatchEvent(new Event('change',{bubbles:true}));sync();var f=v?c:o;if(f&&f.focus)try{f.focus();}catch(e){}}"
 "[o,c].forEach(function(el){if(!el)return;el.setAttribute('role','button');el.tabIndex=0;el.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();set(!t.checked);}});});"
 "t.addEventListener('change',sync);document.addEventListener('keydown',function(e){if(e.key==='Escape'&&t.checked)set(false);});sync();}catch(e){}})();</script>\n")
rep("<script>/* M341 */(function(){try{window.addEventListener('storage'", C26JS+"<script>/* M341 */(function(){try{window.addEventListener('storage'", 'C26 a11y */(function')

# --- C4b: Content-Security-Policy (meta). Script/stile inline restano necessari (app a file singolo): la protezione e' sulle ORIGINI.
CSP=("default-src 'self'; script-src 'self' 'unsafe-inline' https://www.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
     "font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: blob: https://image.tmdb.org; "
     "connect-src 'self' https://*.firebaseio.com wss://*.firebaseio.com https://*.firebasedatabase.app wss://*.firebasedatabase.app https://fonts.googleapis.com https://fonts.gstatic.com https://image.tmdb.org; "
     "manifest-src 'self' data:; worker-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'")
if 'Content-Security-Policy' not in s:
    k='<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n'
    assert s.count(k)==1
    s=s.replace(k,k+'<meta http-equiv="Content-Security-Policy" content="%s">\n'%CSP)
s=re.sub(r'(name="tva-build" content=")[^"]*',lambda m:m.group(1)+BUILD,s)
open(P,'w',encoding='utf-8').write(s)
# --- C3: sw.js legato alla build (cache per build, pulizia SOLO delle cache di questa app, index in precache)
w=open(SW,encoding='utf-8').read()
w=re.sub(r"const SW_BUILD = '[^']*';","const SW_BUILD = '%s';"%BUILD,w)
w=re.sub(r"const CACHE_NAME = '[^']*';","const CACHE_NAME = 'marvel-timeline-cache-%s';"%BUILD,w)
if 'CACHE_PREFIX' not in w:
    w=w.replace("const CACHE_NAME","const CACHE_PREFIX = 'marvel-timeline-cache-';   // C26: si cancellano solo le cache di questa app\nconst CACHE_NAME",1)
    old="keys.filter(function (k) { return k !== CACHE_NAME; })"
    assert w.count(old)==1
    w=w.replace(old,"keys.filter(function (k) { return k.indexOf(CACHE_PREFIX) === 0 && k !== CACHE_NAME; })")
    old="caches.open(CACHE_NAME).then(function (cache) { return Promise.all([precacheFonts(cache), precacheAvatars(cache)]); })"
    assert w.count(old)==1
    w=w.replace(old,"caches.open(CACHE_NAME).then(function (cache) { return Promise.all([precacheFonts(cache), precacheAvatars(cache), precacheShell(cache)]); })")
    old="function precacheFonts(cache) {"
    w=w.replace(old,"""/* C26: la pagina della build corrente entra subito in cache: dopo un aggiornamento la guida resta apribile offline anche prima della prima navigazione. */
function precacheShell(cache) {
  return Promise.all(['./', './index.html'].map(function (u) {
    return fetch(new Request(u, { cache: 'no-cache' })).then(function (r) { if (r && r.status === 200) return cache.put(u, r); }).catch(function () { /* offline: nessun errore fatale */ });
  }));
}

"""+old,1)
    old="return caches.match(req).then(function (cached) {"
    assert w.count(old)==1
    w=w.replace(old,"return caches.match(req, { ignoreSearch: req.mode === 'navigate' }).then(function (cached) {   // C26: la navigazione ignora la query")
open(SW,'w',encoding='utf-8').write(w)
# --- C3b: la pagina entra nella cache della build SOLO se la sua build coincide con quella del SW (deploy a meta': sw.js nuovo + index.html vecchio)
w=open(SW,encoding='utf-8').read()
if 'C26b' not in w:
    old="""    return fetch(new Request(u, { cache: 'no-cache' })).then(function (r) { if (r && r.status === 200) return cache.put(u, r); }).catch(function () { /* offline: nessun errore fatale */ });"""
    assert w.count(old)==1
    new="""    return fetch(new Request(u, { cache: 'no-cache' })).then(function (r) {
      if (!r || r.status !== 200) return;
      // C26b: non si salva HTML di una build diversa da SW_BUILD (es. deploy a meta': sw.js nuovo, index.html ancora vecchio)
      return r.clone().text().then(function (t) {
        var m = /name="tva-build"\\s+content="([^"]+)"/.exec(t.slice(0, 8192));
        if (m && m[1] === SW_BUILD) return cache.put(u, r);
      });
    }).catch(function () { /* offline: nessun errore fatale */ });"""
    w=w.replace(old,new)
    open(SW,'w',encoding='utf-8').write(w)
