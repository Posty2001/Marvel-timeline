import json
from playwright.sync_api import sync_playwright
exec(open('xm_close_test.py').read().split("with sync_playwright() as p:")[0])
with sync_playwright() as p:
    br=p.chromium.launch()
    g=[{'name':'G','createdAt':0,'members':[{'name':'Anna','tesseraId':'TVA-TEST-A','watchedIds':['012'],'watchedAnimIds':[]},{'name':'Bruno','tesseraId':'TVA-TEST-B','watchedIds':['012','018'],'watchedAnimIds':[]}]}]
    c,q,e=boot(br,{'marvel-ultimate-timeline-groups':json.dumps(g)})
    print(q.evaluate("()=>[...document.querySelectorAll('[id^=appTab]')].map(x=>x.id)"))
    print(q.evaluate("()=>[!!document.querySelector('.friends-group-card'), document.getElementById('groupsListWrap').innerHTML.slice(0,200), (location.hash)]"))
    print(e)
    q.evaluate("()=>document.getElementById('appTabFriends').click()"); q.wait_for_timeout(400)
    q.evaluate("()=>document.querySelector('.friends-group-card').click()"); q.wait_for_timeout(400)
    print(q.evaluate("()=>[document.getElementById('groupCompareBox').hidden, document.getElementById('groupCompareA').innerHTML.slice(0,120), document.getElementById('groupCompareWrap').innerText]"))
