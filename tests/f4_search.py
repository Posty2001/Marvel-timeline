from leg_shot import *
import json,re
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    for q in ['jackman','Hugh Jackman','ragnarok','dottor stranamore','nyong','wakanda','Sokovia','citta','città','thanos','vibranio','s.h.i.e.l.d','shield','mjolnir','asgard']:
        pg.evaluate("(q)=>{tvaAtlas2.setState({screen:'search',sq:q});tvaAtlas2.onOpen()}",q); pg.wait_for_timeout(250)
        r=pg.evaluate("()=>[...document.querySelectorAll('.a2-resbox h3')].map(x=>x.textContent.trim())")
        print(repr(q),r)
    A=json.loads(re.search(r'<script[^>]*id="atlasData"[^>]*>(.*?)</script>',open('/home/claude/work/index.html',encoding='utf-8').read(),re.S).group(1))
    print([ (i['id'],i['pagine']) for i in A['identita']])
