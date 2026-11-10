#!/usr/bin/env python3
"""Capture the real app with fail-closed local fixtures and Rider–Waite cards."""
import argparse,asyncio,hashlib,html,json,mimetypes
from pathlib import Path
from urllib.parse import urlsplit
from PIL import Image
from playwright.async_api import async_playwright

SITE=Path(__file__).resolve().parents[1]
BOT=Path('/opt/stacks/bots/Taro')
CARDS=('00_the_fool','01_the_magician','17_the_star')
DECK=BOT/'decks/rider_waite_classic'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

async def main(args):
 frontend=Path(args.frontend).resolve();inventory=json.loads(Path(args.inventory).read_text())['languages']
 locales=json.loads((SITE/'sitegen/locales.json').read_text());codes=args.locales.split(',') if args.locales else [x['code'] for x in locales]
 assert set(codes)<={x['code'] for x in locales}
 out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
 manifest_path=SITE/'sitegen/product-images.json'
 report={'source':'Real published r76 frontend with fully intercepted demonstration API; no real account, generation or API writes',
         'frontend':{str(p.relative_to(frontend)):sha(p) for p in frontend.rglob('*') if p.is_file() and (p.name=='index.html' or p.relative_to(frontend).parts[0]=='assets')},
         'deck':'rider_waite_classic','card_assets':[{'file':str((DECK/(c+'.jpg')).relative_to(BOT)),'sha256':sha(DECK/(c+'.jpg'))} for c in CARDS],
         'images':[],'errors':[],'real_network_requests':0,'request_counts':[],
         'service_workers':'block','websockets':'block','demo_hashes':{}}
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  try:
   for code in codes:
    content=json.loads((SITE/f'sitegen/content/{code}.json').read_text());demo=content['demo'];data=inventory[code]
    report['demo_hashes'][code]=hashlib.sha256(json.dumps(demo,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
    labels={**data['labels'],**json.loads((BOT/f'go/internal/modules/webapp/app/locales/{code}.json').read_text())}
    context=await browser.new_context(viewport={'width':390,'height':580},device_scale_factor=2,reduced_motion='reduce',service_workers='block')
    observed=[];intercepted=set()
    context.on('request',lambda request:observed.append(request))
    async def block_websocket(ws):
     report['errors'].append('Blocked unexpected WebSocket');await ws.close()
    await context.route_web_socket('**/*',block_websocket)
    await context.add_init_script("localStorage.setItem('taro-theme','dark')")
    async def handle(route):
     request=route.request;u=urlsplit(request.url);path=u.path
     intercepted.add(id(request))
     if u.hostname=='telegram.org' and path.startswith('/js/'):
      await route.fulfill(body='window.Telegram={WebApp:{ready(){},expand(){}}};',content_type='application/javascript');return
     if u.hostname!='app.taro.mom':report['errors'].append('Unexpected host '+str(u.hostname));await route.abort();return
     if path=='/' and request.method=='GET':await route.fulfill(body=(frontend/'index.html').read_bytes(),content_type='text/html');return
     if path.startswith('/assets/') and request.method=='GET':
      target=(frontend/path.lstrip('/')).resolve();assert target.is_relative_to(frontend) and target.is_file()
      await route.fulfill(body=target.read_bytes(),content_type=mimetypes.guess_type(target.name)[0] or 'application/octet-stream');return
     if path.startswith('/demo/') and request.method=='GET':
      name=Path(path).name;assert name in {c+'.jpg' for c in CARDS};target=DECK/name
      await route.fulfill(body=target.read_bytes(),content_type='image/jpeg');return
     if path.startswith('/web/api/v1/'):
      endpoint=path.removeprefix('/web/api/v1')
      if endpoint=='/activity' and request.method=='POST':value={'ok':True}
      elif request.method!='GET':report['errors'].append('Blocked API write '+endpoint);await route.abort();return
      elif endpoint=='/localization':value={'language':code,'languages':[{'code':code,'name':next(x['nativeLabel'] for x in locales if x['code']==code)}],'labels':labels}
      elif endpoint=='/bootstrap':
       user=dict(id=100,name=demo['name'],language=code,credits=5,premium_until=None,deck='rider_waite_classic',birth_date=None,birth_time='',birth_place='',birth_place_name='',clock_zone='UTC',clock_place='',clock_place_name='',reading_context='',reminders_enabled=False,allow_reversed=False,revision='demo',show_card_canon=False)
       value=dict(user=user,is_admin=False,languages=[{'code':code,'name':next(x['nativeLabel'] for x in locales if x['code']==code)}],labels=labels,features=data['features'],decks=data['decks'],support_url='',csrf_token='demo')
      elif endpoint=='/operations/demo':
       answer='<p><b>'+html.escape(demo['answer_title'])+'</b></p><p>'+html.escape(demo['answer'])+'</p>'
       value=dict(id='demo',status='ready',feature='spread_3cards',title=demo['reading_title'],question=demo['question'],cards=[dict(index=i,position_code=str(i),position_label=demo['positions'][i],name=demo['card_names'][i],image_url='https://app.taro.mom/demo/'+CARDS[i]+'.jpg',revealed=True,reversed=False) for i in range(3)],layout=dict(kind='three',width=600,height=350,slots=[dict(index=i,x=150+i*150,y=160) for i in range(3)]),answer_html=answer)
      elif endpoint=='/operations/quote':value={'action':'run','price':1}
      elif endpoint=='/auth/email/status':value={'enabled':False}
      elif endpoint in ('/journal/history','/journal'):value={'items':[]}
      else:report['errors'].append('Unexpected API '+endpoint);await route.abort();return
      await route.fulfill(json=value);return
     report['errors'].append('Blocked path '+path);await route.abort()
    await context.route('**/*',handle)
    page=await context.new_page();page.set_default_timeout(10000)
    page.on('pageerror',lambda e:report['errors'].append(str(e)))
    for kind in ('tarot','card','astro'):
     if kind in ('tarot','card'):
      await page.goto('https://app.taro.mom/?page=tarot&operation=demo',wait_until='networkidle');await page.locator('.reading-card').first.wait_for()
      if kind=='card':await page.locator('.reading-card').last.click();await page.locator('.card-viewer[open] img').wait_for()
     else:
      await page.goto('https://app.taro.mom/?page=astro',wait_until='networkidle');await page.locator('[data-feature-id="astro_natal"]').wait_for()
     await page.evaluate('document.fonts.ready')
     for image in await page.locator('img').all():await image.evaluate('(i)=>i.decode()')
     assert await page.locator('html').get_attribute('lang')==code
     if kind in ('tarot','astro'):
      selector='.operation-heading' if kind=='tarot' else '.directory-heading'
      await page.locator(selector).evaluate('(el)=>window.scrollTo(0,el.getBoundingClientRect().top+scrollY-16)')
     png=out/f'{code}-{kind}.png';await page.screenshot(path=str(png))
     target=SITE/f'images/en/app-{kind}-{code}.webp';Image.open(png).convert('RGB').save(target,'WEBP',quality=86,method=6)
     report['images'].append({'file':str(target.relative_to(SITE)),'width':780,'height':1160,'bytes':target.stat().st_size,'sha256':sha(target),'language':code,'view':kind})
    await context.close()
    escaped=[r for r in observed if id(r) not in intercepted]
    report['real_network_requests']+=len(escaped)
    report['request_counts'].append({'language':code,'observed':len(observed),'intercepted':len(intercepted),'unintercepted':len(escaped)})
    if escaped:report['errors'].append('Unintercepted requests for '+code)
    print('Captured '+code,flush=True)
  finally:
   await browser.close();(out/'capture-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 assert not report['errors'],report['errors']
 if args.locales:
  (out/'provenance-partial.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 else:manifest_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'ok':True,'images':len(report['images']),'deck':report['deck']}))

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--frontend',required=True);parser.add_argument('--inventory',required=True);parser.add_argument('--output',required=True);parser.add_argument('--locales');asyncio.run(main(parser.parse_args()))
