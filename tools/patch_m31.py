#!/usr/bin/env python3
"""Blocco M3.1 (idempotente, dopo patch_m3): locandine TMDB. Priorita': immagine personalizzata autorizzata -> TMDB -> emblema. Nessuna chiave nel codice."""
import re,json
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
man=json.load(open('/home/claude/work/assets/images/catalog/tmdb_map.json',encoding='utf-8'))
voci={k:v for k,v in man.get('voci',{}).items() if re.match(r'^/[A-Za-z0-9_-]+\.(jpg|png)$',v.get('p',''))}
blob='<script type="application/json" id="tmdbMap">'+json.dumps({'voci':voci},sort_keys=True,ensure_ascii=False,separators=(',',':'))+'</script>'
LOAD="""<script>/* M31 TMDB */(function(){try{var w=window,B='https://image.tmdb.org/t/p/',map={};try{map=JSON.parse(document.getElementById('tmdbMap').textContent).voci||{};}catch(e){}
function off(){try{return w.localStorage.getItem('tvaTmdbOff')==='1';}catch(e){return false;}}
w.tvaTmdb={base:B,count:function(){return Object.keys(map).length;},
poster:function(num,size){var e=map[num];if(!e||!e.p||off()||w.navigator.onLine===false)return null;var a=size==='thumb'?['w154','w342',154,231]:['w342','w500',342,513];
return{src:B+a[0]+e.p,srcset:B+a[0]+e.p+' 1x, '+B+a[1]+e.p+' 2x',w:a[2],h:a[3],kind:e.t,season:e.s||null};}};}catch(e){}})();</script>"""
s=re.sub(r'\n?<script type="application/json" id="tmdbMap">.*?</script>\s*<script>/\* M31 TMDB.*?</script>','',s,flags=re.S)
k=s.index('id="imageManifest">'); k=s.index('</script>',s.index('M3 loader',k))+9
s=s[:k]+blob+LOAD+s[k:]
# nuovo m3Poster: custom -> TMDB -> emblema
a=s.index('    function m3Poster(hero, art, id, titolo) {'); b=s.index('    function renderOpera() {')
NEW="""    function m3Poster(hero, art, id, titolo) {   /* priorita': locandina personalizzata (licence + verified:true) -> TMDB -> emblema */
      try {
        var t = IDX.titoli[id], M = window.TVA_IMG_MANIFEST || {}, num = t && (t.num || id), m = t && M[(t.kind === 'anim' ? 'anim:' : 'item:') + num];
        var custom = !!(m && m.src && m.licence && m.verified === true), T = window.tvaTmdb && t && t.kind !== 'anim' ? window.tvaTmdb.poster(num, 'hero') : null;
        if (!custom && !T) return;
        var im = new Image(); im.className = 'm3-poster'; im.alt = 'Locandina: ' + titolo; im.loading = 'eager'; im.decoding = 'async'; im.referrerPolicy = 'no-referrer';
        function useT() { im.width = T.w; im.height = T.h; im.setAttribute('data-src', 'tmdb'); im.srcset = T.srcset; im.sizes = '(max-width:480px) 46vw, 168px'; im.src = T.src; }
        im.onload = function () { art.style.display = 'none'; if (im.getAttribute('data-src') === 'tmdb') m3Attr(hero); };
        im.onerror = function () { if (custom && T && im.getAttribute('data-src') !== 'tmdb') { custom = false; useT(); } else im.remove(); };
        hero.insertBefore(im, art);
        if (custom) { im.width = m.w || 200; im.height = m.h || 300; im.src = m.src; } else useT();
      } catch (e) { }
    }
    function m3Attr(hero) {   /* attribuzione TMDB richiesta dai termini d'uso */
      if (hero.querySelector('.m3-tmdb')) return;
      var p = document.createElement('p'); p.className = 'm3-tmdb';
      var a = document.createElement('a'); a.href = 'https://www.themoviedb.org/'; a.target = '_blank'; a.rel = 'noopener noreferrer'; a.textContent = 'TMDB';
      p.appendChild(document.createTextNode('Locandina: ')); p.appendChild(a); p.appendChild(document.createTextNode(' — This product uses the TMDB API but is not endorsed or certified by TMDB.'));
      hero.appendChild(p);
    }
"""
s=s[:a]+NEW+s[b:]
# scheda Timeline: miniatura alla prima apertura (solo se esiste locandina)
TL="""<script>/* M31 timeline thumbs */(function(){try{document.addEventListener('toggle',function(ev){var d=ev.target;if(!d||!d.open||!d.classList||!d.classList.contains('card'))return;var li=d.closest&&d.closest('.card-wrap');if(!li||li.__m3t)return;li.__m3t=1;var num=li.getAttribute('data-item'),pn=d.querySelector('.detail-panel');if(!pn)return;
var M=window.TVA_IMG_MANIFEST||{},m=M['item:'+num],ok=m&&m.src&&m.licence&&m.verified===true,T=window.tvaTmdb&&window.tvaTmdb.poster(num,'thumb');if(!ok&&!T)return;
var im=new Image();im.className='m3-tl';im.alt='';im.loading='lazy';im.decoding='async';im.referrerPolicy='no-referrer';im.width=92;im.height=138;
im.onerror=function(){if(ok&&T&&im.getAttribute('data-src')!=='tmdb'){ok=false;im.setAttribute('data-src','tmdb');im.srcset=T.srcset;im.src=T.src;}else im.remove();};
if(ok){im.src=m.src;}else{im.setAttribute('data-src','tmdb');im.srcset=T.srcset;im.src=T.src;}pn.insertBefore(im,pn.firstChild);},true);}catch(e){}})();</script>"""
s=re.sub(r'<script>/\* M31 timeline thumbs.*?</script>','',s,flags=re.S)
s=s.replace('</body>',TL+'</body>',1) if s.count('</body>')==1 else s
CSS="/* M31-CSS */\n.m3-tmdb{font-size:.6875rem;line-height:1.4;opacity:.75;margin:.5rem 0 0}.m3-tmdb a{color:inherit;text-decoration:underline}\n.m3-tl{display:block;width:92px;height:138px;object-fit:contain;border-radius:6px;margin:0 0 .5rem}\n"
if '/* M31-CSS */' not in s:
    k=s.index('</style>'); s=s[:k]+CSS+s[k:]
s=re.sub(r'(name="tva-build" content=")[^"]*',lambda m:m.group(1)+'20261023-1300-m31d',s)
open(P,'w',encoding='utf-8').write(s)
