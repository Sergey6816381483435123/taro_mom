#!/usr/bin/env python3
"""Render every scoped page against a static server; save QA outside the site."""
import argparse,asyncio,json,time
from pathlib import Path
from playwright.async_api import async_playwright
from generate import outputs
WIDTHS=(320,360,375,390,414,768,1024,1440)
async def main(args):
 out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
 routes=list(outputs());report={'ok':False,'base':args.base,'pages':len(routes),'widths':WIDTHS,'checks':[],'errors':[],'http_errors':[],'metrics':{}}
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  context=await browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce')
  page=await context.new_page();page.on('pageerror',lambda e:report['errors'].append(str(e)));page.on('console',lambda m:report['errors'].append(m.text) if m.type=='error' else None)
  page.on('response',lambda r:report['http_errors'].append({'url':r.url,'status':r.status}) if r.status>=400 else None)
  await page.add_init_script("window.labLCP=0;new PerformanceObserver(list=>{for(const e of list.getEntries())window.labLCP=e.startTime}).observe({type:'largest-contentful-paint',buffered:true})")
  async def geometry(label):
   result=await page.evaluate('''()=>{const bad=[];for(const el of document.querySelectorAll('h1,h2,h3,p,.entry-link,.topic-card,.primary-nav,.locale-switch,img,summary')){const r=el.getBoundingClientRect();if(r.width&&r.height&&(r.left < -1 || r.right>innerWidth+1))bad.push(el.tagName+'.'+el.className)}return {overflow:document.documentElement.scrollWidth>innerWidth+1,bad}}''')
   assert not result['overflow'] and not result['bad'],(label,result)
  for index,route in enumerate(routes):
   response=await page.goto(args.base.rstrip('/')+route,wait_until='networkidle');assert response.status==200
   assert await page.locator('h1').count()==1 and await page.locator('.entry-link').count()==6
   await page.evaluate('document.querySelectorAll("details").forEach(e=>e.open=true)')
   for width in WIDTHS:
    await page.set_viewport_size({'width':width,'height':844});await geometry(route+str(width));report['checks'].append({'route':route,'width':width,'mode':'portrait'})
   await page.set_viewport_size({'width':844,'height':390});await geometry(route+'landscape');report['checks'].append({'route':route,'mode':'landscape'})
   await page.set_viewport_size({'width':768,'height':844});await page.evaluate("document.documentElement.style.zoom='2'");await geometry(route+'zoom200');await page.evaluate("document.documentElement.style.zoom=''");report['checks'].append({'route':route,'mode':'200% zoom (CSS layout)'})
   await page.set_viewport_size({'width':320,'height':844});await page.evaluate("document.documentElement.style.fontSize='20px'");await geometry(route+'text125');await page.evaluate("document.documentElement.style.fontSize=''");report['checks'].append({'route':route,'mode':'125% root text'})
   await page.keyboard.press('Tab');assert await page.evaluate("document.activeElement.classList.contains('skip-link')")
   await page.keyboard.press('Enter');assert await page.evaluate("document.activeElement.id==='main-content'")
   assert await page.evaluate("getComputedStyle(document.documentElement).scrollBehavior==='auto'")
   await page.evaluate('document.activeElement.blur()')
   if route in ['/','/ru/','/astro/','/ru/astro/','/astro/natal-chart/','/ru/astro/natalnaya-karta/','/en/three-card-tarot-spread/','/ru/rasklad-taro-na-tri-karty/']:
    for width in [320,390,1440]:
     await page.set_viewport_size({'width':width,'height':900});await page.screenshot(path=str(out/(('en-home' if route=='/' else route.strip('/').replace('/','-'))+'-'+str(width)+'.png')),full_page=True)
   for image in await page.locator('img').all():
    await image.scroll_into_view_if_needed();await image.evaluate('(i)=>i.decode()')
   report['metrics'][route]=await page.evaluate("({lcp_ms:window.labLCP,dom_ms:performance.getEntriesByType('navigation')[0].domContentLoadedEventEnd,html_bytes:performance.getEntriesByType('navigation')[0].decodedBodySize,images:Array.from(document.images).map(i=>({src:i.getAttribute('src'),loaded:i.complete&&i.naturalWidth>0}))})")
   assert all(x['loaded'] for x in report['metrics'][route]['images'])
   print('Checked '+route,flush=True)
  nojs=await browser.new_context(java_script_enabled=False,viewport={'width':320,'height':844});np=await nojs.new_page()
  for route in routes:
   response=await np.goto(args.base.rstrip('/')+route);assert response.status==200 and await np.locator('.entry-link').count()==6 and await np.locator('h1').inner_text();assert await np.locator('#faq p').first.is_visible()
  report['no_javascript_pages']=len(routes)
  await nojs.close();await context.close();await browser.close()
 assert not report['errors'] and not report['http_errors'],report
 report['ok']=True;(out/'browser-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'ok':True,'pages':len(routes),'responsive_cases':len(report['checks']),'no_js_pages':len(routes),'errors':0}))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--base',default='http://127.0.0.1:8765');parser.add_argument('--output',default='/tmp/taro-site-qa');asyncio.run(main(parser.parse_args()))
