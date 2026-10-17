"""Finite first-party JSS manual page/link/image provenance inventory.
No original HTML/images retained. Unavailable pages stay unavailable, not absent.
"""
from __future__ import annotations
import argparse
from html.parser import HTMLParser
import hashlib
import json
import re
import urllib.request
from urllib.parse import urljoin,urlsplit,urldefrag

ROOT='http://www.titan.co.jp/stoneage/'
CAPTURE='20010418083149'
class Inventory(HTMLParser):
 def __init__(self):
  super().__init__();self.links=[];self.images=[];self.anchor='TOP';self.sections={'TOP':[]}
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='a':
   ident=a.get('name') or a.get('id')
   if ident:self.anchor=ident;self.sections.setdefault(ident,[])
   if a.get('href'):self.links.append(a['href'])
  if tag=='img' and a.get('src'):
   self.images.append({'src':a['src'],'section_anchor':self.anchor,
     'html_width':a.get('width'),'html_height':a.get('height')})
 def handle_data(self,data):self.sections[self.anchor].append(data)

def derive(body,final_url,page):
 m=re.search(r'/web/(\d{14})(?:id_)?/(https?://.*)$',final_url)
 if not m or urlsplit(m.group(2)).hostname!='www.titan.co.jp' or urlsplit(m.group(2)).path!='/stoneage/'+page:
  raise ValueError('unqualified original page/capture redirect')
 text=body.decode('shift_jis',errors='replace');p=Inventory();p.feed(text)
 plain={k:' '.join(' '.join(v).split()) for k,v in p.sections.items()}
 terms={'login':'ログイン','character':'キャラクタ','creation':'作成','password':'パスワード','name':'名前'}
 relevant=[k for k,s in plain.items() if any(t in s for t in terms.values())]
 contract=creation_contract(plain) if page=='manual01.html' else None
 return {'creation_contract':contract,'requested_page':page,'final_url':final_url,'actual_capture':m.group(1),
  'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'replacement_characters':text.count('\ufffd'),
  'section_count':len(plain),'relevant_section_anchors':relevant,
  'relevant_section_fingerprints':[{'anchor':k,'normalized_sha256':hashlib.sha256(plain[k].encode()).hexdigest(),
      'keyword_labels':[n for n,t in terms.items() if t in plain[k]]} for k in relevant],
  'manual_links':sorted(set(urljoin(ROOT+page,u) for u in p.links if re.search(r'manual\d*\.html',u))),
  'image_references':[{'original_url':urljoin(ROOT+page,x['src']),**{k:v for k,v in x.items() if k!='src'},
      'in_relevant_section':x['section_anchor'] in relevant,'image_bytes_acquired':False} for x in p.images],
  'tw10_exact_build_authenticated':False,'historical_layout_verified':False}

def creation_contract(sections):
 s=sections.get('1020',''); login=sections.get('1010',''); delete=sections.get('1040','')
 trans=str.maketrans('０１２３４５６７８９','0123456789');norm=s.translate(trans)
 def number(pattern):
  m=re.search(pattern,norm)
  if not m:raise ValueError('missing original creation numeric assertion '+pattern)
  return int(m.group(1))
 name=number(r'全角\s*(\d+)\s*文字');stats=number(r'能力値.*?(\d+)\s*ポイント');elements=number(r'属性値.*?(\d+)\s*ポイント')
 if (name,stats,elements)!=(8,20,10):raise ValueError('original creation values changed')
 if not all(t in s for t in ('三属性以上','できません','方向','カラー','顔','出身村')):raise ValueError('creation controls/element scope')
 if not all(t in login for t in ('ID NUMBER','パスワード','太陽','月','別の世界')):raise ValueError('original login-world separation')
 if not all(t in delete for t in ('削除確認','OK')):raise ValueError('delete confirmation')
 return {'source_profile':'JSS_FIRST_PARTY_MANUAL_2001_NOT_TW10_EXACT_BUILD',
  'max_fullwidth_name_characters':name,'initial_stat_allocation_points':stats,
  'initial_element_allocation_points':elements,'maximum_allocated_element_types':2,
  'direction_preview_control_documented':True,'body_color_selection_documented':True,
  'face_part_selection_documented':True,'home_village_selection_documented':True,
  'deletion_confirmation_documented':True,'sun_moon_separate_worlds_documented':True,
  'actual_client_or_server_enforcement_verified':False,'original_screen_coordinates':None,
  'original_character_census':None,'same_rules_proven_in_tw10':False,
  'section_anchors':['1010','1020','1040']}

def linked_manual01(links):
 return next((urldefrag(u)[0] for u in links if urldefrag(u)[0]==ROOT+'manual01.html'),None)

def main():
 out={'schema':'stoneage.jss.login_manual.provenance.r1','pages':{},'original_html_or_images_retained':False,
      'original_client_executed':False,'complete_character_roster_verified':False}
 # Known manual02 first: learn page01 from a real first-party link, not a guessed
 # unobserved page. At most two HTML requests and no image downloads.
 url=f'https://web.archive.org/web/{CAPTURE}id_/'+ROOT+'manual02.html'
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'StoneAgeHistoricalResearch/1.0'}),timeout=50) as r:
   body=r.read(2_000_001);final=r.url
  if len(body)>2_000_000:raise ValueError('source too large')
  out['pages']['manual02']=derive(body,final,'manual02.html')
  links=out['pages']['manual02']['manual_links']
  original=linked_manual01(links)
  if original:
   url=f'https://web.archive.org/web/{CAPTURE}id_/'+original
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'StoneAgeHistoricalResearch/1.0'}),timeout=50) as r:
    body=r.read(2_000_001);final=r.url
   if len(body)>2_000_000:raise ValueError('source too large')
   out['pages']['manual01']=derive(body,final,'manual01.html')
  else:out['manual01_status']='NOT_LINKED_AT_EXACT_EXPECTED_URL_IN_THIS_CAPTURE'
 except Exception as e:
  out['acquisition_error']={'request_url':url,'type':type(e).__name__,'message':str(e)[:250]}
 print(json.dumps(out,ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
