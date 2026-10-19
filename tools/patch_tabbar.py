import re,sys
p='/home/claude/work/index.html'
s=open(p,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:60],s.count(old))
    s=s.replace(old,new)
# 1) tabbar base: niente transform/will-change; sfondo pieno fino al bordo fisico
rep("""  background: rgba(15,13,10,0.95); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border-top: 1px solid rgba(239,228,201,0.14);
  box-shadow: 0 -2px 12px rgba(0,0,0,0.25);
  transform: translateZ(0); -webkit-transform: translateZ(0); will-change: transform;
}""","""  background: #0f0d0a;
  border-top: 1px solid rgba(239,228,201,0.14);
  box-shadow: 0 -2px 12px rgba(0,0,0,0.25);
  /* NIENTE transform / will-change / backdrop-filter qui: su iOS creano un livello compositing separato la cui
     posizione puo' non coincidere con il bordo fisico (barra staccata o con striscia vuota sotto). Lo sfondo e'
     opaco, quindi il blur non serviva. Il padding-bottom (safe area) e' DENTRO l'altezza della barra:
     lo sfondo arriva al bordo fisico, icone/testi restano sopra l'indicatore Home. */
}
/* Prolungamento opaco sotto il bordo: copre qualsiasi interstizio durante l'animazione della toolbar di Safari
   o il rimbalzo di overscroll. Un elemento fixed non contribuisce all'overflow scrollabile della pagina. */
.app-tabbar::after {
  content: ""; position: absolute; left: 0; right: 0; top: 100%; height: 160px; background: #0f0d0a; pointer-events: none;
}
/* Tastiera aperta (campo di testo a fuoco): la barra non resta sospesa sopra la tastiera. Nessun preventDefault. */
html.kb-open .app-tabbar { display: none; }
/* Pinch-zoom attivo (solo iPhone, <700px): la barra viene riportata, via visualViewport, sul bordo basso VISIBILE
   e alla dimensione reale. Applicato solo mentre scale>1; a scala 1 non c'e' alcun transform. */
.app-tabbar.is-zoomed {
  transform-origin: 0 100%;
  transform: translate(var(--vv-x, 0px), var(--vv-y, 0px)) scale(var(--vv-s, 1));
}""")
rep("""    max-width: 480px; left: 50%; transform: translateX(-50%); border-radius: 16px 16px 0 0;""",
    """    max-width: 480px; left: 0; right: 0; margin: 0 auto; border-radius: 16px 16px 0 0;""")
# 2) overflow a 320px
rep(".filter-btns { display: flex; gap: 0.4rem; }",".filter-btns { display: flex; flex-wrap: wrap; gap: 0.4rem; }")
# 3) JS passivo
js="""<script>
/* Barra inferiore: stabilita' su iOS. SOLO listener passivi, nessun preventDefault, nessun blocco del pinch. */
(function(){
  var bar=document.getElementById('appTabbar'); if(!bar) return;
  var root=document.documentElement, vv=window.visualViewport, raf=0;
  function upd(){
    raf=0;
    var s=vv?vv.scale:1, W=root.clientWidth;
    if(vv && s>1.02 && W<700){
      var H=root.clientHeight;
      bar.style.setProperty('--vv-s',(1/s).toFixed(4));
      bar.style.setProperty('--vv-x',vv.offsetLeft.toFixed(1)+'px');
      bar.style.setProperty('--vv-y',(vv.offsetTop+vv.height-H).toFixed(1)+'px');
      bar.classList.add('is-zoomed');
    } else if(bar.classList.contains('is-zoomed')){
      bar.classList.remove('is-zoomed');
      bar.style.removeProperty('--vv-s'); bar.style.removeProperty('--vv-x'); bar.style.removeProperty('--vv-y');
    }
  }
  function sched(){ if(!raf) raf=requestAnimationFrame(upd); }
  if(vv){ vv.addEventListener('resize',sched,{passive:true}); vv.addEventListener('scroll',sched,{passive:true}); }
  function isText(e){
    if(!e||!e.tagName) return false;
    var t=e.tagName;
    if(t==='TEXTAREA'||t==='SELECT') return true;
    if(t==='INPUT'){ return !/^(checkbox|radio|range|button|submit|reset|file|hidden|image|color)$/i.test(e.type||'text'); }
    return !!e.isContentEditable;
  }
  document.addEventListener('focusin',function(ev){ if(isText(ev.target)) root.classList.add('kb-open'); },{passive:true});
  document.addEventListener('focusout',function(){ setTimeout(function(){ if(!isText(document.activeElement)) root.classList.remove('kb-open'); },60); },{passive:true});
  upd();
})();
</script>
</body>"""
assert s.count("</body>")==1
s=s.replace("</body>",js)
open(p,'w',encoding='utf-8').write(s)
print('ok')
