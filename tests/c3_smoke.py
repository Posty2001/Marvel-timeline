import json,sys
from playwright.sync_api import sync_playwright
from leg_shot import boot
W=int(sys.argv[1]) if len(sys.argv)>1 else 390; H=int(sys.argv[2]) if len(sys.argv)>2 else 844
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b,W,H)
    pg.evaluate("()=>{tvaAtlas2.enter();tvaAtlas2.setState({screen:'cronologie'})}"); pg.wait_for_timeout(500)
    pg.screenshot(path=f'/tmp/claude-0/t/c3_hub_{W}.png')
    for mode,extra in [('uni',{}),('par',{}),('exp',{'q':'agents'})]:
        st={'screen':'cron','cr':dict({'mode':mode,'uid':None},**extra)}
        r=pg.evaluate("""(m)=>{const c=tvaAtlas2.getState().cr; return Object.keys(c).length}""",0)
        pg.evaluate("(m)=>{const base=tvaTime.state()||{}; }",0)
        pg.evaluate("""([mode,extra])=>{ tvaAtlas2.setState({screen:'cron',cr:Object.assign({mode:'uni',uid:null,ord:null,und:false,lim:40,pA:null,pB:null,pm:'uscita',ps:'A',q:'',fu:[],fb:'amb',fp:[],fs:[],ft:[],fr:false,xo:'uscita',xl:30,na:false},extra,{mode:mode})}) }""",[mode,extra])
        pg.wait_for_timeout(700)
        pg.screenshot(path=f'/tmp/claude-0/t/c3_{mode}_{W}.png')
    print(errs[:5]); b.close()
