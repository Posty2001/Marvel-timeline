p='/home/claude/work/index.html'
s=open(p,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1,(old[:50],s.count(old)); s=s.replace(old,new)
rep('<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n',
    '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n<meta name="tva-build" content="20261017-1100-tabbar-diag1">\n')
rep("var root=document.documentElement, vv=window.visualViewport, raf=0;","var root=document.documentElement, vv=window.visualViewport, raf=0, zoomFix=true;")
rep("if(vv && s>1.02 && W<700){","if(vv && zoomFix && s>1.02 && W<700){")
rep("  upd();\n})();\n</script>\n</body>","  upd();\n  window.__tvaTabbar={get zoomFix(){ return zoomFix; }, setZoomFix:function(v){ zoomFix=!!v; upd(); }};\n})();\n</script>\n</body>")
d=open('/home/claude/work/tools/diag.js',encoding='utf-8').read()
assert s.count('</body>')==1
s=s.replace('</body>',d.rstrip('\n').replace('</body>','')+'</body>')
open(p,'w',encoding='utf-8').write(s); print('ok')
