<script>
/* TVA — verifica versione caricata + diagnostica layout (?debugLayout=1).
   - Normale: nessun pannello, nessuna modifica al layout. Solo un controllo di versione (vedi checkNormale).
   - Debug: ?debugLayout=1 (persistente con ?debugLayout=0 per spegnere) oppure, in PWA standalone dove non c'e'
     barra indirizzi, 5 tocchi rapidi sulla barra inferiore. Il pannello e' figlio di <html> (non di <body>:
     le regole "#toggle:checked ~ *" lo nasconderebbero), position:fixed, non influisce sul layout.
   - Nessun listener non passivo, nessun preventDefault, nessuna scrittura su localStorage/IndexedDB dei salvataggi:
     l'unica chiave scritta e' 'tva-debug-layout' (fuori dal prefisso dei salvataggi). */
(function(){
  'use strict';
  var meta=document.querySelector('meta[name="tva-build"]');
  var BUILD=meta?meta.getAttribute('content'):'?';
  var FLAG='tva-debug-layout', root=document.documentElement;
  function lsGet(k){ try{ return localStorage.getItem(k); }catch(e){ return null; } }
  function lsSet(k,v){ try{ localStorage.setItem(k,v); }catch(e){} }
  function lsDel(k){ try{ localStorage.removeItem(k); }catch(e){} }
  function parseBuild(t){ var m=/name="tva-build"\s+content="([^"]+)"/.exec(t||''); return m?m[1]:null; }
  function isHttp(){ return /^https?:$/.test(location.protocol); }

  /* ---- lettura dei primi ~8 KB di un URL (il meta build e' in testa al file): niente scarico di 3 MB ---- */
  function readHead(url,useCache){
    var ctrl=('AbortController' in window)?new AbortController():null;
    var o={headers:{Range:'bytes=0-8191'}}; if(!useCache) o.cache='no-store'; if(ctrl) o.signal=ctrl.signal;
    return fetch(url,o).then(function(r){
      if(!r.body||!r.body.getReader||typeof TextDecoder==='undefined') return r.text().then(function(t){ return t.slice(0,8192); });
      var rd=r.body.getReader(), dec=new TextDecoder(), acc='';
      function pump(){ return rd.read().then(function(x){
        if(x.done) return acc;
        acc+=dec.decode(x.value,{stream:true});
        if(acc.length>=8192){ try{ rd.cancel(); }catch(e){} if(ctrl){ try{ ctrl.abort(); }catch(e){} } return acc; }
        return pump();
      }); }
      return pump();
    });
  }
  function netBuild(){ return readHead(location.pathname+location.search,false).then(parseBuild); }

  /* ---- controllo normale: se la rete ha una build diversa da quella caricata, riavvia UNA volta (per build) ---- */
  function checkNormale(){
    if(!isHttp()||navigator.onLine===false) return;
    netBuild().then(function(nb){
      if(!nb||nb===BUILD) return;
      var key='tva-build-reload', done=null;
      try{ done=sessionStorage.getItem(key); }catch(e){}
      if(done===nb) return;                                   /* gia' tentato: nessun loop */
      try{ sessionStorage.setItem(key,nb); }catch(e){ return; } /* senza anti-loop non ricarico */
      var go=function(){ location.reload(); };
      if(navigator.serviceWorker&&navigator.serviceWorker.getRegistration){
        navigator.serviceWorker.getRegistration().then(function(r){ return r&&r.update(); }).catch(function(){}).then(go);
      } else go();
    }).catch(function(){});
  }
  function schedNormale(){ setTimeout(checkNormale,1500); }
  if(document.readyState==='complete') schedNormale(); else window.addEventListener('load',schedNormale,{once:true});

  /* ---- attivazione ---- */
  var mm=/[?&]debugLayout=(\d)/.exec(location.search);
  if(mm){ if(mm[1]==='1') lsSet(FLAG,'1'); else lsDel(FLAG); }
  var active=mm?mm[1]==='1':lsGet(FLAG)==='1';
  var bar=document.getElementById('appTabbar');
  var taps=[];
  if(bar){
    bar.addEventListener('click',function(){
      var n=Date.now(); taps.push(n); taps=taps.filter(function(t){ return n-t<2500; });
      if(taps.length>=5){ taps=[]; if(panel){ chiudi(); } else { lsSet(FLAG,'1'); apri(); } }
    },{passive:true});
  }

  var panel=null, pre=null, timer=0, probes=null, mark=null, asyncInfo={}, vvLog=[];
  function mk(tag,css,txt){ var e=document.createElement(tag); if(css) e.style.cssText=css; if(txt) e.textContent=txt; return e; }
  function px(n){ return (Math.round(n*10)/10)+''; }

  function apri(){
    if(panel) return;
    panel=mk('div','position:fixed;left:2px;right:2px;top:calc(env(safe-area-inset-top,0px) + 2px);max-height:58vh;overflow:auto;'+
      'z-index:2147483000;background:rgba(0,0,0,.88);color:#7CFC00;font:10px/1.3 ui-monospace,Menlo,monospace;padding:4px;'+
      'border:1px solid #7CFC00;border-radius:4px;box-sizing:border-box;-webkit-text-size-adjust:100%;');
    panel.id='tvaDbgPanel';
    var row=mk('div','display:flex;gap:4px;flex-wrap:wrap;margin-bottom:4px;');
    function btn(label,fn){ var b=mk('button','font:10px ui-monospace,Menlo,monospace;color:#000;background:#7CFC00;border:0;border-radius:3px;padding:5px 7px;',label); b.type='button'; b.addEventListener('click',fn,{passive:true}); row.appendChild(b); return b; }
    btn('COPIA',function(){ copia(); });
    btn('RICONTROLLA',function(){ asyncInfo={}; carica(); });
    var zb=btn('ZOOMFIX',function(){ var z=window.__tvaTabbar; if(z){ z.setZoomFix(!z.zoomFix); } zb.textContent='ZOOMFIX '+(z&&z.zoomFix?'ON':'OFF'); });
    zb.textContent='ZOOMFIX '+((window.__tvaTabbar&&window.__tvaTabbar.zoomFix)?'ON':'OFF');
    btn('CHIUDI',function(){ chiudi(); });
    pre=mk('pre','margin:0;white-space:pre-wrap;word-break:break-all;font:inherit;');
    panel.appendChild(row); panel.appendChild(pre);
    probes=mk('div','position:fixed;left:0;top:0;width:0;height:0;visibility:hidden;pointer-events:none;'+
      'padding:env(safe-area-inset-top,0px) env(safe-area-inset-right,0px) env(safe-area-inset-bottom,0px) env(safe-area-inset-left,0px);');
    probes.id='tvaDbgProbe';
    var h1=mk('div','position:fixed;left:0;top:0;width:0;visibility:hidden;height:100vh;');
    var h2=mk('div','position:fixed;left:0;top:0;width:0;visibility:hidden;height:100dvh;');
    var h3=mk('div','position:fixed;left:0;top:0;width:0;visibility:hidden;height:-webkit-fill-available;');
    probes.h=[h1,h2,h3];
    /* marcatori: rosso = bordo basso del layout viewport (dove si ancora bottom:0); ciano = bordo basso del visual viewport;
       riquadro magenta = rettangolo reale della tabbar */
    var red=mk('div','position:fixed;left:0;right:0;bottom:0;height:3px;background:#f00;z-index:2147483001;pointer-events:none;');
    var cy=mk('div','position:fixed;left:0;right:0;top:0;height:3px;background:#0ff;z-index:2147483001;pointer-events:none;');
    var box=mk('div','position:fixed;border:2px dashed #f0f;box-sizing:border-box;z-index:2147483001;pointer-events:none;');
    mark=[red,cy,box];
    [panel,probes,h1,h2,h3,red,cy,box].forEach(function(e){ root.appendChild(e); });
    if(window.visualViewport){
      var onvv=function(){ var v=window.visualViewport,b=document.getElementById('appTabbar');
        vvLog.push('vv scale='+v.scale.toFixed(2)+' off='+px(v.offsetLeft)+','+px(v.offsetTop)+' bar.tf='+(b?getComputedStyle(b).transform:'-'));
        if(vvLog.length>4) vvLog.shift(); aggiorna(); };
      panel._onvv=onvv;
      window.visualViewport.addEventListener('resize',onvv,{passive:true});
      window.visualViewport.addEventListener('scroll',onvv,{passive:true});
    }
    window.addEventListener('scroll',aggiorna,{passive:true});
    window.addEventListener('resize',aggiorna,{passive:true});
    window.addEventListener('pageshow',aggiorna,{passive:true});
    timer=setInterval(aggiorna,1000);
    carica(); aggiorna();
  }
  function chiudi(){
    lsDel(FLAG);
    clearInterval(timer);
    if(window.visualViewport&&panel&&panel._onvv){ window.visualViewport.removeEventListener('resize',panel._onvv); window.visualViewport.removeEventListener('scroll',panel._onvv); }
    window.removeEventListener('scroll',aggiorna); window.removeEventListener('resize',aggiorna); window.removeEventListener('pageshow',aggiorna);
    [panel,probes].concat(probes?probes.h:[]).concat(mark||[]).forEach(function(e){ if(e&&e.parentNode) e.parentNode.removeChild(e); });
    panel=pre=probes=mark=null;
  }

  /* ---- misure asincrone: rete, cache, service worker ---- */
  function askSW(w){
    return new Promise(function(res){
      if(!w){ res(null); return; }
      var done=false, t=setTimeout(function(){ if(!done){ done=true; res(null); } },1500);
      try{
        var ch=new MessageChannel();
        ch.port1.onmessage=function(e){ if(!done){ done=true; clearTimeout(t); res(e.data); } };
        w.postMessage({type:'tva-get-version'},[ch.port2]);
      }catch(e){ clearTimeout(t); res(null); }
    });
  }
  function carica(){
    var a=asyncInfo;
    if(!isHttp()){ a.rete='n/d (file:// o altro schema)'; return; }
    netBuild().then(function(b){ a.rete=b||'non trovata'; }).catch(function(e){ a.rete='errore '+e; });
    if('caches' in window){
      caches.keys().then(function(k){ a.cacheKeys=k.join(', ')||'(nessuna)'; }).catch(function(){ a.cacheKeys='errore'; });
      caches.match(location.href.split('#')[0]).then(function(r){
        if(!r){ a.cacheHtml='non in cache'; return; }
        var rd=r.clone().body&&r.clone().body.getReader?r.clone().body.getReader():null;
        if(!rd) return r.clone().text().then(function(t){ a.cacheHtml=parseBuild(t.slice(0,8192))||'build assente'; });
        var dec=new TextDecoder(), acc='';
        (function pump(){ rd.read().then(function(x){ if(x.done||acc.length>=8192){ try{ rd.cancel(); }catch(e){} a.cacheHtml=parseBuild(acc)||'build assente'; return; } acc+=dec.decode(x.value,{stream:true}); pump(); }); })();
      }).catch(function(){ a.cacheHtml='errore'; });
    } else a.cacheKeys='Cache API assente';
    if('serviceWorker' in navigator){
      var c=navigator.serviceWorker.controller;
      a.ctrl=c?(c.state+' '+c.scriptURL.split('/').pop()):'NESSUN controller (pagina non controllata dal SW)';
      navigator.serviceWorker.getRegistration().then(function(reg){
        a.reg=reg?('active='+(reg.active?reg.active.state:'no')+' waiting='+(!!reg.waiting)+' installing='+(!!reg.installing)):'nessuna registrazione';
        return askSW(c||(reg&&reg.active));
      }).then(function(v){ a.swRun=v?(v.swBuild+' / '+v.cache):'nessuna risposta (SW precedente alla v8 o non attivo)'; }).catch(function(){ a.swRun='errore'; });
      fetch('./sw.js',{cache:'no-store'}).then(function(r){ return r.text(); }).then(function(t){
        var m1=/SW_BUILD\s*=\s*'([^']+)'/.exec(t), m2=/CACHE_NAME\s*=\s*'([^']+)'/.exec(t);
        a.swServito=(m1?m1[1]:'?')+' / '+(m2?m2[1]:'?');
      }).catch(function(){ a.swServito='errore'; });
    } else a.ctrl='serviceWorker non supportato';
  }

  function rapporto(){
    var v=window.visualViewport, b=document.getElementById('appTabbar'), L=[];
    var r=b?b.getBoundingClientRect():null, cs=b?getComputedStyle(b):null;
    var pp=probes?getComputedStyle(probes):null;
    var sat=pp?pp.paddingTop:'?', sar=pp?pp.paddingRight:'?', sab=pp?pp.paddingBottom:'?', sal=pp?pp.paddingLeft:'?';
    var ch=root.clientHeight, ih=window.innerHeight;
    var ua=(/OS (\d+[_\d]*)/.exec(navigator.userAgent)||[])[1];
    L.push('BUILD html in esecuzione: '+BUILD);
    L.push('BUILD html da rete:       '+(asyncInfo.rete||'...'));
    L.push('BUILD html in cache SW:   '+(asyncInfo.cacheHtml||'...'));
    L.push('SW in esecuzione: '+(asyncInfo.swRun||'...'));
    L.push('sw.js servito:    '+(asyncInfo.swServito||'...'));
    L.push('controller: '+(asyncInfo.ctrl||'...')+' | '+(asyncInfo.reg||'...'));
    L.push('cache: '+(asyncInfo.cacheKeys||'...'));
    L.push('--- modo ---');
    L.push('display-mode standalone: '+matchMedia('(display-mode: standalone)').matches+' | navigator.standalone: '+navigator.standalone+' | iOS '+(ua||'?').replace(/_/g,'.'));
    L.push('--- viewport (px CSS) ---');
    L.push('innerWidth x innerHeight:      '+window.innerWidth+' x '+ih);
    L.push('documentElement.clientWidth x clientHeight: '+root.clientWidth+' x '+ch);
    L.push('outerHeight: '+window.outerHeight+' | screen: '+screen.width+' x '+screen.height+' | availHeight: '+screen.availHeight+' | dpr '+window.devicePixelRatio);
    if(v) L.push('visualViewport: '+px(v.width)+' x '+px(v.height)+' | offsetTop '+px(v.offsetTop)+' | offsetLeft '+px(v.offsetLeft)+' | pageTop '+px(v.pageTop)+' | scale '+v.scale.toFixed(3));
    else L.push('visualViewport: assente');
    if(probes){ var hs=probes.h.map(function(e){ return e.offsetHeight; }); L.push('100vh='+hs[0]+'  100dvh='+hs[1]+'  fill-available='+hs[2]); }
    L.push('--- safe area (misurata con env()) ---');
    L.push('top '+sat+' | right '+sar+' | bottom '+sab+' | left '+sal+' | --sab='+getComputedStyle(root).getPropertyValue('--sab').trim());
    L.push('--- tabbar ---');
    if(r){
      L.push('rect: top '+px(r.top)+' bottom '+px(r.bottom)+' height '+px(r.height)+' left '+px(r.left)+' width '+px(r.width));
      L.push('GAP bottom vs innerHeight: '+px(ih-r.bottom)+' | vs clientHeight: '+px(ch-r.bottom)+(v?' | vs visual bottom: '+px(v.offsetTop+v.height-r.bottom):''));
      var tabs=[].slice.call(b.querySelectorAll('.app-tab')).map(function(t){ return t.getBoundingClientRect().bottom; });
      var tb=Math.max.apply(null,tabs);
      L.push('fondo icone/testi: '+px(tb)+' | spazio sotto le icone fino a clientHeight: '+px(ch-tb)+' (safe bottom '+sab+')');
      L.push('css: position '+cs.position+' bottom '+cs.bottom+' height '+cs.height+' padding-bottom '+cs.paddingBottom+' display '+cs.display);
      L.push('css: transform '+cs.transform+' | will-change '+cs.willChange+' | backdrop '+(cs.backdropFilter||cs.webkitBackdropFilter)+' | bg '+cs.backgroundColor);
      L.push('classi: '+b.className+' | html: '+root.className);
      if(mark){ mark[0].style.bottom='0px'; mark[1].style.top=(v?(v.offsetTop+v.height-3):(ch-3))+'px';
        mark[2].style.left=r.left+'px'; mark[2].style.top=r.top+'px'; mark[2].style.width=r.width+'px'; mark[2].style.height=r.height+'px'; }
    } else L.push('tabbar assente');
    L.push('--- documento ---');
    L.push('scrollY '+px(window.scrollY)+' | scrollHeight '+root.scrollHeight+' | scrollWidth '+root.scrollWidth+' | body padding-bottom '+getComputedStyle(document.body).paddingBottom);
    L.push('html bg '+getComputedStyle(root).backgroundColor+' | body bg '+getComputedStyle(document.body).backgroundColor);
    if(vvLog.length){ L.push('--- ultimi eventi pinch ---'); vvLog.forEach(function(x){ L.push(x); }); }
    L.push('legenda marcatori: ROSSO = bordo basso layout viewport (bottom:0); CIANO = bordo basso visual viewport; MAGENTA tratteggiato = rettangolo tabbar');
    return L.join('\n');
  }
  function aggiorna(){ if(pre) pre.textContent=rapporto(); }
  function copia(){
    var t=rapporto();
    if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(t).catch(function(){}); return; }
    var ta=mk('textarea','position:fixed;left:0;top:0;opacity:0;'); ta.value=t; root.appendChild(ta); ta.select();
    try{ document.execCommand('copy'); }catch(e){} root.removeChild(ta);
  }
  window.__tvaDiag={build:BUILD,apri:apri,chiudi:chiudi,rapporto:rapporto,netBuild:netBuild};
  if(active) apri();
})();
</script>
</body>
