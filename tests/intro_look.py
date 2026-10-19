from playwright.sync_api import sync_playwright
import sys
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page()
    pg.goto('http://127.0.0.1:8124/index.html'); pg.wait_for_timeout(1800)
    pg.screenshot(path='/tmp/claude-0/t/shots_leg/intro_now.png')
    b.close()
