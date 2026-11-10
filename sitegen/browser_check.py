#!/usr/bin/env python3
"""Check every generated page locally; keep browser evidence outside the site."""
import argparse,asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
from generate import LOCALES,OLD_ROUTES,ASTRO_ROUTES,path
WIDTHS=(320,360,375,390,414,768,1024,1440)

async def main(args):
 out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
 codes=args.locales.split(',') if args.locales else [x['code'] for x in LOCALES]
 assert set(codes)<={x['code'] for x in LOCALES}
 routes=[(code,key,path(code,key)) for code in codes for key in (*OLD_ROUTES,*ASTRO_ROUTES)]
 report={'ok':False,'base':args.base,'pages':len(routes),'widths':WIDTHS,'checks':[],'errors':[],'http_errors':[],'images':{},'no_javascript_pages':0,'lab_initial_metrics':{}}
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  context=await browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce')
  page=await context.new_page();page.on('pageerror',lambda e:report['errors'].append(str(e)));page.on('console',lambda m:report['errors'].append(m.text) if m.type=='error' else None)
  page.on('response',lambda r:report['http_errors'].append({'url':r.url,'status':r.status}) if r.status>=400 else None)
  await page.add_init_script("window.labLCP=0;window.labCLS=0;new PerformanceObserver(l=>l.getEntries().forEach(e=>window.labLCP=e.startTime)).observe({type:'largest-contentful-paint',buffered:true});new PerformanceObserver(l=>l.getEntries().forEach(e=>{if(!e.hadRecentInput)window.labCLS+=e.value})).observe({type:'layout-shift',buffered:true})")
  async def geometry(label):
   result=await page.evaluate('''()=>{const bad=[];for(const el of document.querySelectorAll('h1,h2,h3,p,.entry-link,.topic-card,.primary-nav,.locale-switch,img,summary,.locale-menu')){if(!el.checkVisibility())continue;const r=el.getBoundingClientRect();if(r.width&&r.height&&(r.left < -1 || r.right>innerWidth+1))bad.push(el.tagName+'.'+el.className)}return {overflow:document.documentElement.scrollWidth>innerWidth+1,bad}}''')
   assert not result['overflow'] and not result['bad'],(label,result)
  try:
   for index,(code,key,route) in enumerate(routes):
    await page.set_viewport_size({'width':390,'height':844})
    response=await page.goto(args.base.rstrip('/')+route,wait_until='load');assert response.status==200
    await page.evaluate('document.fonts.ready')
    await page.evaluate('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
    report['lab_initial_metrics'][route]=await page.evaluate("({lcp_ms:window.labLCP,cls:window.labCLS,html_bytes:performance.getEntriesByType('navigation')[0].decodedBodySize})")
    assert await page.locator('h1').count()==1 and await page.locator('.entry-link').count()==6
    await page.keyboard.press('Tab');assert await page.evaluate("document.activeElement.classList.contains('skip-link')"),route+' skip focus'
    await page.keyboard.press('Enter');assert await page.evaluate("document.activeElement.id==='main-content'"),route+' main focus'
    assert await page.evaluate("getComputedStyle(document.documentElement).scrollBehavior==='auto'")
    await page.evaluate('document.activeElement.blur();window.scrollTo(0,0)')
    for width in WIDTHS:
     await page.set_viewport_size({'width':width,'height':844});await geometry(route+str(width))
     await page.locator('.locale-switch summary').click();assert await page.locator('.locale-menu').is_visible();await geometry(route+' menu '+str(width))
     assert await page.locator('.locale-menu a').count()==20
     await page.locator('.locale-switch summary').click();report['checks'].append({'route':route,'width':width,'mode':'portrait+language-menu'})
    await page.set_viewport_size({'width':844,'height':390});await geometry(route+'landscape');report['checks'].append({'route':route,'mode':'landscape'})
    await page.set_viewport_size({'width':768,'height':844});await page.evaluate("document.documentElement.style.zoom='2'");await geometry(route+'zoom200');await page.evaluate("document.documentElement.style.zoom=''");report['checks'].append({'route':route,'mode':'200% zoom (CSS layout)'})
    await page.set_viewport_size({'width':320,'height':844});await page.evaluate("document.documentElement.style.fontSize='20px'");await geometry(route+'text125');await page.evaluate("document.documentElement.style.fontSize=''");report['checks'].append({'route':route,'mode':'125% root text'})
    if key=='home':
     await page.set_viewport_size({'width':390,'height':844});await page.screenshot(path=str(out/f'{code}-home-390.png'),full_page=True);await page.screenshot(path=str(out/f'{code}-home-top-390.png'))
     await page.locator('.locale-switch summary').focus();await page.keyboard.press('Enter');assert await page.locator('.locale-menu').is_visible()
     await page.keyboard.press('Tab');assert await page.evaluate("document.activeElement.closest('.locale-menu')!==null")
     await page.keyboard.press('Shift+Tab');await page.keyboard.press('Enter');assert not await page.locator('.locale-menu').is_visible()
    if code in ('en','ru','ar','fa','ko','hi') and key in ('astro','natal'):
     await page.set_viewport_size({'width':320 if key=='astro' else 1440,'height':900});await page.screenshot(path=str(out/f'{code}-{key}.png'))
    for image in await page.locator('img').all():
     await image.scroll_into_view_if_needed();await image.evaluate('(i)=>i.decode()')
    report['images'][route]=await page.evaluate("Array.from(document.images).map(i=>({src:i.getAttribute('src'),loaded:i.complete&&i.naturalWidth>0}))")
    assert all(x['loaded'] for x in report['images'][route])
    if key=='home' and code in ('en','ru','ar','hi'):
     await page.set_viewport_size({'width':1440,'height':900});await page.evaluate('window.scrollTo(0,0)');await page.mouse.move(0,0)
     links=page.locator('.hero .entry-link')
     normal=await links.evaluate_all("es=>es.map(e=>{const s=getComputedStyle(e);return [s.backgroundColor,s.backgroundImage,s.color,s.borderColor,s.boxShadow]})")
     assert normal[0]==normal[1]==normal[2],(route,'CTA defaults differ',normal)
     for i in range(3):
      await links.nth(i).hover();assert await links.nth(i).evaluate("e=>getComputedStyle(e).backgroundImage")!='none'
     await page.mouse.move(0,0);await links.first.focus();await page.keyboard.press('Shift+Tab');await page.keyboard.press('Tab');assert await links.first.evaluate("e=>getComputedStyle(e).outlineStyle")!='none'
     await page.evaluate('document.activeElement.blur()')
    if (index+1)%12==0:print('Checked '+code+' (12 pages)',flush=True)
   nojs=await browser.new_context(java_script_enabled=False,viewport={'width':320,'height':844});np=await nojs.new_page()
   for code,key,route in routes:
    response=await np.goto(args.base.rstrip('/')+route,wait_until='load');assert response.status==200 and await np.locator('.entry-link').count()==6 and await np.locator('h1').inner_text();assert await np.locator('#faq p').first.is_visible()
    await np.locator('.locale-switch summary').click();assert await np.locator('.locale-menu a').count()==20 and await np.locator('.locale-menu').is_visible()
    report['no_javascript_pages']+=1
   await nojs.close();assert not report['errors'] and not report['http_errors'],report['errors']+report['http_errors'];report['ok']=True
  except Exception as error:
   report['failure']=str(error);await page.screenshot(path=str(out/'failure.png'),full_page=True);raise
  finally:
   (out/'browser-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');await context.close();await browser.close()
 print(json.dumps({'ok':True,'pages':len(routes),'responsive_cases':len(report['checks']),'no_js_pages':report['no_javascript_pages'],'errors':0}))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--base',default='http://127.0.0.1:8765');parser.add_argument('--output',default='/tmp/taro-site-qa');parser.add_argument('--locales');asyncio.run(main(parser.parse_args()))
