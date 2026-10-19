import json,re
from playwright.sync_api import sync_playwright
src=open('data_test.py').read()
JS=re.search(r'JS="""(.*?)"""',src,re.S).group(1).replace('\\\\','\\')
CFG=json.load(open('/home/claude/work/tools/xmen_order.json')); ORD=set(CFG['order'])
with sync_playwright() as p:
    b=p.chromium.launch(); r={}
    for k,u in (('old','file:///tmp/claude-0/t/index.3c.frozen.html'),('new','file:///home/claude/work/index.html')):
        pg=b.new_page(); pg.goto(u); pg.wait_for_timeout(1500); r[k]=pg.evaluate(JS); pg.close()
norm=lambda t:re.sub(r'N(?:°|&deg;)\d{3}','N°#',t)
chg=[i for i in r['old'] if r['old'][i]!=r['new'][i]]
print(len(chg))
cat={'norm_only':[], 'norm_sorted_words':[], 'other':[]}
for i in chg:
    a,b2=r['old'][i],r['new'][i]
    if a[0]!=b2[0]: cat['other'].append(i); continue
    if norm(a[1])==norm(b2[1]): cat['norm_only'].append(i)
    elif sorted(norm(a[1]).split())==sorted(norm(b2[1]).split()): cat['norm_sorted_words'].append(i)
    else: cat['other'].append(i)
for k,v in cat.items(): print(k,len(v),v[:60])
json.dump(cat,open('dt_cat.json','w'))
