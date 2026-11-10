#!/usr/bin/env python3
"""Validate the complete 20-language static site without network or writes."""
import hashlib,html,json,re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
from xml.etree import ElementTree as ET
from generate import ROOT,BASE,ENTRIES,OLD_ROUTES,ASTRO_ROUTES,REVISION,LOCALES,outputs,alternates,path
class Page(HTMLParser):
 def __init__(self,raw):
  super().__init__(convert_charrefs=True);self.tags=[];self.feed(raw)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
 def all(self,tag,**attrs):return [d for t,d in self.tags if t==tag and all(d.get(k)==v for k,v in attrs.items())]
 def one(self,tag,**attrs):
  found=self.all(tag,**attrs);assert len(found)==1,(tag,attrs,len(found));return found[0]
def target(url):
 p=unquote(urlsplit(url).path);return ROOT/p.lstrip('/')/('index.html' if p.endswith('/') else '')
def leaves(value,prefix=()):
 if isinstance(value,dict):
  for k,v in value.items():yield from leaves(v,prefix+(k,))
 elif isinstance(value,list):
  for i,v in enumerate(value):yield from leaves(v,prefix+(i,))
 else:yield prefix,value
def validate_content(data,code,reference):
 actual,expected=dict(leaves(data)),dict(leaves(reference));assert actual.keys()==expected.keys(),('Structure',code)
 assert data['revision']==REVISION['id']
 assert data['ui']['brand']==('Тарошенька' if code=='ru' else 'Tarot')
 if code!='ru':assert all('Tarot' in value for value in (data['pages']['home']['title'],data['ui']['entity_description'],data['ui']['entry_labels'][0])),('Brand spelling',code)
 for key in (*OLD_ROUTES,*ASTRO_ROUTES):assert data['pages'][key].get('related',[])==reference['pages'][key].get('related',[])
 for field,text in actual.items():
  assert isinstance(text,str) and text.strip(),(code,field,'Empty')
  if code!='ru':assert not re.search(r'Taroshenka|Тарошенька',text,re.I),(code,field,'Old brand')
  if code!='en' and field[0]!='revision' and 'related' not in field and len(re.findall(r'[A-Za-z]{2,}',expected[field]))>=5:assert text!=expected[field],(code,field,'Untranslated English')
  if code!='en':
   for term in ('Daily Card','Card Advice','Yes or No','Our Relationship','New Love','What Do They Feel?','Will They Return?','Near Future','My Next Step','How the Situation Develops','Work & Finances','Celtic Cross','Wheel of Fortune'):
    assert term not in text,(code,field,'Untranslated feature name: '+term)
  if code=='be':assert not re.search('[ИиЩщЇїЄєҐґ]',text),(code,field,'Non-Belarusian letters')
 return len(actual)
def main():
 assert len(LOCALES)==20 and set(REVISION['locales'])=={x['code'] for x in LOCALES}
 generated=outputs();assert len(generated)==240
 legacy=json.loads((ROOT/'sitegen/legacy-integrity.json').read_text())
 for name,digest in legacy.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,'Protected file changed: '+name
 assert (ROOT/'CNAME').read_text().strip()=='taro.mom'
 assert 'https://taro.mom/sitemap.xml' in (ROOT/'robots.txt').read_text()
 reference=json.loads((ROOT/'sitegen/content/en.json').read_text());documents={r:Page(s) for r,s in generated.items()}
 symbols={x.attrib['id'] for x in ET.parse(ROOT/'sitegen/assets/icons.svg').findall('.//{http://www.w3.org/2000/svg}symbol')}
 links=images=strings=0
 for loc in LOCALES:
  code=loc['code'];data=json.loads((ROOT/f'sitegen/content/{code}.json').read_text());strings+=validate_content(data,code,reference);titles=set();descriptions=set()
  for key in (*OLD_ROUTES,*ASTRO_ROUTES):
   route=path(code,key);raw=generated[route];p=documents[route];assert target(route).read_text()==raw,'Stale '+route
   assert p.one('html')['lang']==loc['hreflang'] and p.one('html')['dir']==loc['dir'] and len(p.all('h1'))==1
   assert p.one('link',rel='canonical')['href']==BASE+route
   actual={(x['hreflang'],x['href']) for x in p.all('link',rel='alternate')};assert actual==set(alternates(key)) and len(actual)==21
   assert route!='/en/' and BASE+'/en/' not in {u for _,u in actual}
   assert p.one('meta',property='og:url')['content']==BASE+route and p.one('meta',property='og:locale')['content']==loc['ogLocale']
   title=data['pages'][key]['title'];description=p.one('meta',name='description')['content'];assert title not in titles and description not in descriptions,(code,key,'Repeated metadata');titles.add(title);descriptions.add(description)
   assert not p.all('meta',name='keywords') and not p.all('form')
   assert all('noindex' not in x.get('content','').lower() for x in p.all('meta',name='robots'))
   assert len(p.all('script'))==1 and p.one('script')['type']=='application/ld+json'
   graph=json.loads(raw.split('<script type="application/ld+json">')[1].split('</script>')[0])['@graph'];assert [x['@type'] for x in graph]==['WebSite','SoftwareApplication','WebPage']
   assert graph[0]['name']==graph[1]['name']==data['ui']['brand'] and graph[2]['inLanguage']==loc['hreflang']
   for node in graph[1:]:assert tuple(x['target'] for x in node['potentialAction'])==ENTRIES
   assert data['ui']['disclaimer'] in html.unescape(raw) and '{{' not in raw
   entry=[x for x in p.all('a') if 'entry-link' in x.get('class','').split()];assert tuple(x['href'] for x in entry)==ENTRIES*2
   localized=[x for x in p.all('a') if 'hreflang' in x];assert len(localized)==40
   assert {(x['hreflang'],x['href']) for x in localized}=={(l['hreflang'],path(l['code'],key)) for l in LOCALES}
   for x in p.all('a'):
    href=x.get('href','');assert href and not href.startswith(('javascript:','http:'))
    if x.get('target')=='_blank':assert set(x.get('rel','').split())>={'noopener','noreferrer'}
    u=urlsplit(href)
    if not u.netloc and u.path:
     assert href.startswith('/') and target(href).is_file(),'Missing link '+href
     if u.fragment:assert any(d.get('id')==u.fragment for _,d in Page(target(href).read_text()).tags),'Missing anchor '+href
    elif not u.netloc and u.fragment:assert any(d.get('id')==u.fragment for _,d in p.tags)
    links+=1
   for tag,attrs in p.tags:
    for attribute in ('src','srcset'):
     if attribute in attrs:assert attrs[attribute].startswith('/') and target(attrs[attribute]).is_file(),'Missing asset '+attrs[attribute]
    if tag=='use':
     u=urlsplit(attrs['href']);assert u.path=='/sitegen/assets/icons.svg' and u.fragment in symbols
    if tag=='svg':assert attrs.get('aria-hidden')=='true' and attrs.get('focusable')=='false'
    if tag=='img':assert int(attrs['width'])>0 and int(attrs['height'])>0 and 'alt' in attrs;images+=1
   for x in p.all('link',rel='stylesheet')+p.all('link',rel='icon')+p.all('link',rel='manifest'):assert target(x['href']).is_file()
 ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'};rows=ET.parse(ROOT/'sitemap.xml').getroot();index={r.findtext('s:loc',namespaces=ns):r for r in rows};assert len(index)==len(rows)==240 and set(index)=={BASE+r for r in generated}
 for loc in LOCALES:
  for key in (*OLD_ROUTES,*ASTRO_ROUTES):
   row=index[BASE+path(loc['code'],key)];assert row.findtext('s:lastmod',namespaces=ns)==REVISION['updated'];assert {(x.attrib['hreflang'],x.attrib['href']) for x in row.findall('x:link',ns)}==set(alternates(key))
 manifest=json.loads((ROOT/'manifest.json').read_text());assert manifest['short_name']=='Tarot'
 for icon in manifest['icons']:assert target(icon['src']).is_file()
 provenance=json.loads((ROOT/'sitegen/product-images.json').read_text());assert len(provenance['images'])==60 and provenance['deck']=='rider_waite_classic'
 assert {(a['language'],a['view']) for a in provenance['images']}=={(x['code'],v) for x in LOCALES for v in ('tarot','card','astro')}
 for asset in provenance['images']:assert hashlib.sha256((ROOT/asset['file']).read_bytes()).hexdigest()==asset['sha256'] and asset['width']==780 and asset['height']==1160
 assert not provenance['errors']
 assert provenance['service_workers']==provenance['websockets']=='block' and provenance['real_network_requests']==0
 assert len(provenance['request_counts'])==20 and all(x['observed']==x['intercepted']>0 and x['unintercepted']==0 for x in provenance['request_counts'])
 assert {x['language'] for x in provenance['request_counts']}=={x['code'] for x in LOCALES}
 for loc in LOCALES:
  demo=json.loads((ROOT/f'sitegen/content/{loc["code"]}.json').read_text())['demo']
  assert provenance['demo_hashes'][loc['code']]==hashlib.sha256(json.dumps(demo,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'Stale screenshot demo: '+loc['code']
 print(json.dumps({'ok':True,'pages':len(generated),'languages':len(LOCALES),'strings':strings,'protected_files':len(legacy),'links':links,'images':images,'sitemap_urls':len(index)},ensure_ascii=False))
if __name__=='__main__':main()
