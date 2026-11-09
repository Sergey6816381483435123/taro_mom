#!/usr/bin/env python3
"""Validate the scoped static revision; no network, writes or dependencies."""
import hashlib,json,sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
from xml.etree import ElementTree as ET
from generate import ROOT,BASE,ENTRIES,OLD_ROUTES,ASTRO_ROUTES,REVISION,outputs,alternates,path
class Page(HTMLParser):
 def __init__(self,raw):
  super().__init__(convert_charrefs=True);self.tags=[];self.feed(raw)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
 def all(self,tag,**attrs):return [d for t,d in self.tags if t==tag and all(d.get(k)==v for k,v in attrs.items())]
 def one(self,tag,**attrs):
  found=self.all(tag,**attrs);assert len(found)==1,(tag,attrs,len(found));return found[0]
def target(url):
 p=unquote(urlsplit(url).path);return ROOT/p.lstrip('/')/('index.html' if p.endswith('/') else '')
def main():
 generated=outputs();assert len(generated)==24
 legacy=json.loads((ROOT/'sitegen/legacy-integrity.json').read_text())
 for name,digest in legacy.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,'Protected legacy changed: '+name
 assert (ROOT/'CNAME').read_text().strip()=='taro.mom'
 robots=(ROOT/'robots.txt').read_text();assert 'https://taro.mom/sitemap.xml' in robots
 documents={route:Page(raw) for route,raw in generated.items()};titles=set();descriptions=set();links=0;images=0
 for code in REVISION['locales']:
  data=json.loads((ROOT/f'sitegen/content/{code}.json').read_text())
  for key in (*OLD_ROUTES,*ASTRO_ROUTES):
   route=path(code,key);raw=generated[route];p=documents[route];assert target(route).read_text()==raw,'Stale page '+route
   assert p.one('html')['lang']==code and len(p.all('h1'))==1
   assert p.one('link',rel='canonical')['href']==BASE+route
   actual={(x['hreflang'],x['href']) for x in p.all('link',rel='alternate')};assert actual==set(alternates(key)),route
   assert (route!='/en/') and all(url!=BASE+'/en/' for _,url in actual)
   assert p.one('meta',property='og:url')['content']==BASE+route
   title=data['pages'][key]['title'];description=p.one('meta',name='description')['content'];assert title not in titles and description not in descriptions; titles.add(title);descriptions.add(description)
   assert not p.all('meta',name='keywords') and not p.all('form') and not p.all('script',src='')
   assert len(p.all('script'))==1 and p.one('script')['type']=='application/ld+json'
   graph=json.loads(raw.split('<script type="application/ld+json">')[1].split('</script>')[0]);assert [x['@type'] for x in graph['@graph']]==['WebSite','SoftwareApplication','WebPage']
   for node in graph['@graph'][1:]:assert tuple(x['target'] for x in node['potentialAction'])==ENTRIES
   assert data['ui']['disclaimer'] in raw and '{{' not in raw
   entry=[x for x in p.all('a') if 'entry-link' in x.get('class','').split()];assert tuple(x['href'] for x in entry)==ENTRIES*2
   for x in p.all('a'):
    href=x.get('href','');assert href and not href.startswith(('javascript:','http:'))
    if x.get('target')=='_blank':assert set(x.get('rel','').split())>={'noopener','noreferrer'}
    u=urlsplit(href)
    if not u.netloc and u.path:
     assert href.startswith('/') and target(href).is_file(),'Missing link '+href
     if u.fragment:assert any(d.get('id')==u.fragment for t,d in Page(target(href).read_text()).tags),'Missing anchor '+href
    elif not u.netloc and u.fragment:assert any(d.get('id')==u.fragment for t,d in p.tags),'Missing local anchor'
    links+=1
   for tag,attrs in p.tags:
    for attribute in ('src','srcset'):
     if attribute in attrs:
      src=attrs[attribute];assert src.startswith('/') and target(src).is_file(),'Missing asset '+src
    if tag=='img':assert int(attrs['width'])>0 and int(attrs['height'])>0 and 'alt' in attrs;images+=1
   for x in p.all('link',rel='stylesheet')+p.all('link',rel='icon')+p.all('link',rel='manifest'):assert target(x['href']).is_file()
 ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
 rows=ET.parse(ROOT/'sitemap.xml').getroot();index={r.findtext('s:loc',namespaces=ns):r for r in rows};assert len(index)==len(rows) and BASE+'/en/' not in index
 for code in REVISION['locales']:
  for key in (*OLD_ROUTES,*ASTRO_ROUTES):
   r=index[BASE+path(code,key)];assert r.findtext('s:lastmod',namespaces=ns)==REVISION['updated'];assert {(x.attrib['hreflang'],x.attrib['href']) for x in r.findall('x:link',ns)}==set(alternates(key))
 manifest=json.loads((ROOT/'manifest.json').read_text())
 for icon in manifest['icons']:assert target(icon['src']).is_file()
 provenance=json.loads((ROOT/'sitegen/product-images.json').read_text());assert len(provenance['images'])==6
 for asset in provenance['images']:assert hashlib.sha256((ROOT/asset['file']).read_bytes()).hexdigest()==asset['sha256']
 print(json.dumps({'ok':True,'pages':len(generated),'new_astro':14,'protected_files':len(legacy),'internal_and_external_links':links,'images':images,'sitemap_urls':len(index)},ensure_ascii=False))
if __name__=='__main__':main()
