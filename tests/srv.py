import http.server,re,sys,threading,json,os
ROOT='/tmp/claude-0/t/srv'
STATE={'full':0,'range':0,'rangeBuild':None,'log':[]}
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def do_GET(self):
        path=self.path.split('?')[0]
        if path=='/__state':
            b=json.dumps(STATE).encode(); self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(b))); self.end_headers(); self.wfile.write(b); return
        if path=='/__setrange':
            STATE['rangeBuild']=self.path.split('=')[1] if '=' in self.path else None; STATE['full']=0; STATE['range']=0; self.send_response(200); self.end_headers(); self.wfile.write(b'ok'); return
        f={'/':'index.html','/index.html':'index.html','/sw.js':'sw.js'}.get(path)
        if not f: self.send_response(404); self.end_headers(); return
        data=open(os.path.join(ROOT,f),'rb').read()
        ctype='text/html; charset=utf-8' if f.endswith('html') else 'application/javascript'
        rng=self.headers.get('Range')
        if rng and f=='index.html':
            STATE['range']+=1
            if STATE['rangeBuild']:
                data=re.sub(rb'name="tva-build" content="[^"]+"',b'name="tva-build" content="'+STATE['rangeBuild'].encode()+b'"',data,count=1)
            part=data[:8192]
            self.send_response(206); self.send_header('Content-Type',ctype); self.send_header('Content-Range','bytes 0-%d/%d'%(len(part)-1,len(data))); self.send_header('Content-Length',str(len(part))); self.end_headers(); self.wfile.write(part); return
        if f=='index.html': STATE['full']+=1
        self.send_response(200); self.send_header('Content-Type',ctype); self.send_header('Content-Length',str(len(data))); self.send_header('Cache-Control','public, max-age=3600'); self.end_headers(); self.wfile.write(data)
http.server.ThreadingHTTPServer(('127.0.0.1',8765),H).serve_forever()
