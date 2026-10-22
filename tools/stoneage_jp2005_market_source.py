"""R74: distinguish social venue, dated operator events and announcement eligibility."""
import argparse
import hashlib
import io
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from PIL import Image
from tools.stoneage_jp2005_treasure_source import VisibleMarkup, one, plain, require, sha

ROOT = Path(__file__).resolve().parents[1]
STEM = 'STONEAGE-JP2005-FLEA-MARKET'
REPORT = ROOT / f'research/recovered/{STEM}-SOURCE-R1.json'
PROFILE = 'LATER_OFFICIAL_JP_GAIAX_2005_REPORTED_BY_4GAMER_EXACT_BUILD_UNKNOWN'
URLS = {
 'S1': 'https://www.4gamer.net/news/history/2005.06/20050603191514detail.html',
 'S2': 'https://www.4gamer.net/news/history/2005.10/20051021150740detail.html'}
PARENTS = ['research/recovered/STONEAGE-JSS2001-MAIL-ITEMS-SHARED-VENUES-R1.json',
 'research/recovered/STONEAGE-CN2011-2012-STALL-SOURCE-R1.json',
 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json']
PARSER = 'tools/stoneage_jp2005_treasure_source.py'
BOUNDARIES = {k: False for k in ('direct_official_page_acquired', 'historical_2005_bytes_authenticated',
 'original_server_runtime_verified', 'paid_applicant_rule_is_market_entry_rule',
 'freely_trade_means_zero_tax', 'market_venue_proves_stall_or_offline_vending_ui',
 'two_posts_per_month_means_exact_fourteen_day_interval', 'scheduled_post_proves_published',
 'illustrations_are_market_screens_or_maps', 'jss_venue_or_cn_stall_entity_identity_proven',
 'footer_free_billing_backfilled_to_2005', 'original_html_or_assets_committed', 'stage_b_started')}

class Links(HTMLParser):
 def __init__(self):
  super().__init__(); self.anchors=[]; self.images=[]
 def handle_starttag(self, tag, attrs):
  attrs=dict(attrs)
  if tag=='a' and 'href' in attrs: self.anchors.append(attrs['href'])
  if tag=='img' and 'src' in attrs: self.images.append(attrs['src'])

def markup(raw):
 p=VisibleMarkup();p.feed(raw.decode('cp932',errors='strict'));return ''.join(p.parts)

def article(raw, ident):
 text=markup(raw)
 require(re.search(r'charset=shift_jis',text,re.I),'Charset changed')
 date=plain(one(r'<div class="news_txt1">(.*?)</div>',text,re.S))
 heading=one(r'<!--↓大見出し-->(.*?)<!--↑大見出し-->',text,re.S)
 title=plain(one(r'<h5>(.*?)</h5>',heading,re.S))
 c=one(r'<td class="newstext">(.*?)<!-- tDialy:END -->',text,re.S)
 blocks=[b for b in re.findall(r'<!-- 本文開始 -->(.*?)<!-- 本文終了 -->',c,re.S) if plain(b)]
 require(len(blocks)==1,'Exactly one visible article body required')
 body=plain(blocks[0]);p=Links();p.feed(c)
 links=[urljoin(URLS[ident],a) for a in p.anchors if re.search(r'_\d+big\.html$',a)]
 require(len(links)==(2 if ident=='S1' else 1) and len(set(links))==len(links),'Article image chain changed')
 return {'publication_as_written':date,'title':title,'body':body,'wrapper_urls':links,
  'body_fingerprint':{'characters':len(body),'utf8_bytes':len(body.encode()),'sha256':sha(body.encode())}}

def derive(raws):
 a,b=[article(raws[k],k) for k in ('S1','S2')];x,y=a.pop('body'),b.pop('body')
 require(a['publication_as_written']=='2005/06/0319:15' and b['publication_as_written']=='2005/10/2115:07','Publication changed')
 require(a['title']=='「ストーンエイジ」フリーマーケットを実装，イベントも開催' and b['title']=='MMORPG「ストーンエイジ」11月のイベント予定を発表','Title changed')
 require(x.startswith('ガイアックスが運営する') and y.startswith('ガイアックスは，同社の'),'Operator attribution changed')
 require(x.endswith('（Seirou）') and '（aueki）■' in y,'Media author changed')
 month,day=map(int,one(r'で，(\d+)月(\d+)日より"フリーマーケットスペース"が実装される',x))
 server=one(r'は，([^の]+)のチャットルームマップを新たにフリーマーケット用に改装したものとなる',x)
 require('プレイヤー間でアイテムやペットの取り引きを円滑に行うため' in x,'Trade targets/purpose changed')
 event,m,d,start,end=one(r'公式フリーマーケット「([^」]+)」を(\d+)月(\d+)日(\d+)時から(\d+)時まで開催すると発表した',x)
 require('当日は，ゲームマスターがフリーマーケットスペースを巡回しているとのこと' in x and '話しかけたり，記念撮影したり' in x,'GM patrol/report qualifier changed')
 ordinal=int(one(r'第(\d+)回目となる「'+re.escape(event)+'」',y))
 require('6月に行われて好評だったフリーマーケットと同じもの' in y,'Retrospective media account changed')
 require('チャットルーム内のフリーマーケット会場でユーザー相互にペットやアイテムの売買を自由に行う' in y,'Venue/player trade freedom changed')
 frequency=int(one(r'月に(\d+)回公式サイトにてユーザーイベントの告知サービス',y))
 em,ed,ew,et1,et2=one(r'日時：(\d+)月(\d+)日（(.)）(\d\d:\d\d)～(\d\d:\d\d)場所：',y)
 location=one(r'場所：(.*?)■11月度ユーザー主催イベント募集',y)
 require(location=='水星サーバーチャットルーム内フリーマーケット','Market location changed')
 ry,rm,rd,rw,rem,red,rew=one(r'募集日時：(\d+)年(\d+)月(\d+)日（(.)）～(\d+)月(\d+)日（(.)）対象：',y)
 ty,tm,td,tw,ted,tew=one(r'対象：(\d+)年(\d+)月(\d+)日（(.)）～(\d+)日（(.)）までに行われるイベント掲載日：',y)
 py,pm,pd,pw=one(r'掲載日：(\d+)年(\d+)月(\d+)日（(.)）を予定応募資格：',y)
 require(y.endswith('応募資格：ファンサイトないしBlogを運営しているストーンエイジの有料会員'),'Applicant conjunction/alternatives changed')
 def date(year,month,day,weekday=None):return {'year':int(year),'month':int(month),'day':int(day),'weekday_as_written':weekday}
 return {'articles':dict(S1=a,S2=b),'operator_attributed_by_media':'ガイアックス',
  'source_layer':'CONTEMPORARY_MEDIA_REPORT_OF_OPERATOR_ANNOUNCEMENT_NOT_DIRECT_RELEASE',
  'venue':{'label':'フリーマーケットスペース','server':server,'prior_map_role':'CHAT_ROOM_MAP',
   'conversion_date_announced':date(2005,month,day),'date_status':'FORWARD_LOOKING_AT_S1_PUBLICATION',
   'purpose':'FACILITATE_PLAYER_TO_PLAYER_ITEM_AND_PET_TRADE','map_id':None,'coordinates':None,'geometry':None},
  'official_markets':[{'name':event,'ordinal':None,'date':date(2005,m,d),'start':f'{int(start):02}:00','end':f'{int(end):02}:00',
    'timezone':None,'status':'ANNOUNCED_IN_S1','gm_patrol_as_reported':True,'gm_chat_photo_suggested':True,'source_refs':['S1']},
   {'name':event,'ordinal':ordinal,'date':date(2005,em,ed,ew),'start':et1,'end':et2,'timezone':None,
    'status':'SCHEDULED_IN_S2','location_as_written':location,'source_refs':['S2']}],
  'retrospective':{'source_ref':'S2','june_market_held_and_popular_as_reported':True,'independent_runtime_verification':False},
  'announcement_service':{'posts_per_month_as_reported':frequency,'channel':'OFFICIAL_WEBSITE',
   'application_start':date(ry,rm,rd,rw),'application_end':date(ry,rem,red,rew),
   'eligible_hosted_event_start':date(ty,tm,td,tw),'eligible_hosted_event_end':date(ty,tm,ted,tew),
   'planned_posting_date':date(py,pm,pd,pw),'posting_status':'PLANNED_NOT_OBSERVED',
   'applicant_logic':{'paid_member':True,'operates_any_of':['FAN_SITE','BLOG'],'join':'PAID_AND_ANY_SITE'},
   'scope':'ANNOUNCEMENT_APPLICANT_NOT_MARKET_ATTENDEE','exact_clock_timezone':None,
   'selection_or_acceptance_guarantee':None,'exact_posting_cadence_days':None},
  'trade_system':{'targets':['ITEMS','PETS'],'player_trade_freedom_as_reported':True,
   **{k:None for k in ('tax','entry_fee','listing_fee','stall_ui','offline_automation','auction','currency','settlement','pet_transfer_constraints')}},
  'market_attendee_eligibility':None,'exact_build':None,'original_server_runtime_verified':False}

def chain(raws, ex):
 out=[]
 for sid,ids in [('S1',['S1-MAP','S1-VIEW']),('S2',['S2-MAP'])]:
  for ident,url in zip(ids,ex['articles'][sid]['wrapper_urls']):
   p=Links();p.feed(markup(raws[ident+'-wrapper']))
   imgs=[urljoin(url,v) for v in p.images if 'news/image/' in urljoin(url,v)]
   require(len(imgs)==1 and imgs[0].endswith('.jpg'),'Exactly one actual original image required')
   raw=raws[ident]
   with Image.open(io.BytesIO(raw)) as im:
    im.load();require(im.format=='JPEG' and im.mode=='RGB','Original image format changed');size=list(im.size)
   out.append({'id':ident,'article':sid,'wrapper_url':url,'image_url':imgs[0],
    'wrapper_bytes':len(raws[ident+'-wrapper']),'wrapper_sha256':sha(raws[ident+'-wrapper']),
    'bytes':len(raw),'sha256':sha(raw),'format':'JPEG','mode':'RGB','size':size})
 return out

def pin(path):
 b=(ROOT/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}

def catalog(ex):
 entries=[('VENUE','maps','DOCUMENTARY_SOCIAL_VENUE',['S1','S2'],ex['venue']),
  ('MARKETS','tutorials','DOCUMENTARY_SCHEDULED_SOCIAL_EVENT',['S1','S2'],ex['official_markets']),
  ('ANNOUNCEMENT','tutorials','DOCUMENTARY_PLAYER_EVENT_ANNOUNCEMENT_SERVICE',['S2'],ex['announcement_service'])]
 return [{'record_id':'JP2005-R74-'+ident,'collection':coll,'entity_type':kind,'version_profile':PROFILE,
  'source_refs':refs,'verification_status':'MEDIA_DESCRIPTION_NOT_RUNTIME','rights_status':'RESEARCH_METADATA_NOT_RELEASE_APPROVED',
  'record_revision':1,'game_ids':None,'content':content} for ident,coll,kind,refs,content in entries]

def comparison():
 j=json.loads((ROOT/PARENTS[0]).read_text());c=json.loads((ROOT/PARENTS[1]).read_text())
 venue=next(r for r in j['records'] if r.get('topic')=='SHARED_CHAT_ROOMS') if any(r.get('topic')=='SHARED_CHAT_ROOMS' for r in j['records']) else next(r for r in j['records'] if r['record_id'].endswith(':8110'))
 stall=next(r for r in c['records'] if r['record_id']=='LISTING-FLOW')
 return {'relation':'VERSION_SEPARATION_NOT_LINEAGE_OR_SHARED_ID',
  'early_jss':{'report':PARENTS[0],'record':venue['record_id'],'profile':venue['version_profile'],'scope':'EARLY_SHARED_CHAT_ROOMS_NOT_2005_MARKET_MAP_ID'},
  'later_cn':{'report':PARENTS[1],'record':stall['record_id'],'profile':stall['version_profile'],'scope':'SEPARATE_LISTING_UI_EVIDENCE_NOT_2005_UI'},
  'same_map_id_proven':False,'same_stall_ui_proven':False,'historical_evolution_proven':False,'modern_adoption_decided':False}

def verify_report(r):
 require(r['version_profile']==PROFILE and r['negative_boundaries']==BOUNDARIES,'Version/evidence boundaries changed')
 require(r['catalog_records']==catalog(r['extraction']) and r['comparison']==comparison(),'Catalog/comparison detached')
 require(r['parent_pins']==[pin(p) for p in PARENTS] and r['parser_dependency_pin']==pin(PARSER),'Parent/parser identity changed')
 ex=r['extraction'];require(ex['source_layer']=='CONTEMPORARY_MEDIA_REPORT_OF_OPERATOR_ANNOUNCEMENT_NOT_DIRECT_RELEASE' and ex['original_server_runtime_verified'] is False,'Authority promoted')
 require(ex['market_attendee_eligibility'] is None and ex['exact_build'] is None and all(v is None for k,v in ex['trade_system'].items() if k not in ('targets','player_trade_freedom_as_reported')),'Trade/eligibility unknown promoted')
 require(all(ex['venue'][k] is None for k in ('map_id','coordinates','geometry')),'Map geometry invented')
 service=ex['announcement_service'];require(service['scope']=='ANNOUNCEMENT_APPLICANT_NOT_MARKET_ATTENDEE' and service['posting_status']=='PLANNED_NOT_OBSERVED' and service['applicant_logic']=={'paid_member':True,'operates_any_of':['FAN_SITE','BLOG'],'join':'PAID_AND_ANY_SITE'} and all(service[k] is None for k in ('exact_clock_timezone','selection_or_acceptance_guarantee','exact_posting_cadence_days')),'Announcement scope promoted')
 require([e['status'] for e in ex['official_markets']]==['ANNOUNCED_IN_S1','SCHEDULED_IN_S2'] and ex['venue']['date_status']=='FORWARD_LOOKING_AT_S1_PUBLICATION','Announcements became deployment proof')
 require(ex['retrospective']['independent_runtime_verification'] is False and all(e['timezone'] is None for e in ex['official_markets']),'Runtime/timezone invented')
 require(r['image_observations']==[
  {'id':'S1-MAP','actual_kind':'CHARACTER_ILLUSTRATION_NOT_MAP','manual_visual_review':True,'observed':'BLOND_FIGURE_HOLDING_COLORED_SMALL_CREATURES','game_entity_identity':None},
  {'id':'S1-VIEW','actual_kind':'CHARACTER_ILLUSTRATION_NOT_UI','manual_visual_review':True,'observed':'SMILING_FIGURE_HOLDING_A_GRAY_OBJECT','game_entity_identity':None},
  {'id':'S2-MAP','actual_kind':'CHARACTER_ILLUSTRATION_NOT_MAP','manual_visual_review':True,'observed':'SIMILAR_BLOND_FIGURE_COMPOSITION_DIFFERENT_IMAGE_BYTES_AND_GEOMETRY','game_entity_identity':None}], 'Image interpretation promoted')
 require([(i['bytes'],i['sha256'],i['size']) for i in r['images']]==[(72711,'26f7e4d4c9e0065e086cd280573179e63e4befd931a6c19891a627ad700151e7',[720,982]),(30525,'51ab163d6d190a11e60b2073fe30e80895aaa199c8e5bd450353b28ed6c33a73',[283,567]),(128375,'be45d403b623fd69b3810bc646489aaf6e117014c9f8fd83e6a8e851e56c89ce',[648,948])],'Manual observations detached from reviewed originals')

MUTATIONS={'S1': [('6月14日より','6月15日より'),('水星サーバー','金星サーバー'),('アイテムやペット','アイテムのみ'),('改装したものとなる','既存のままとなる'),('6月18日18時から20時','6月18日18時から21時'),('巡回しているとのこと','常駐しているとのこと'),('ニースフリーマーケット','別の市場')],
 'S2':[('第2回目','第3回目'),('6月に行われて好評だった','6月に開催されなかった'),('月に2回','月に3回'),('11月19日（土）18:00～22:00','11月20日（日）18:00～22:00'),('2005年10月20日（木）～10月25日（火）','2005年10月21日（金）～10月25日（火）'),('2005年11月1日（火）～15日（火）','2005年11月2日（水）～15日（火）'),('2005年10月28日（金）を予定','2005年10月29日（土）を予定'),('ファンサイトないしBlog','ファンサイトおよびBlog'),('有料会員','全会員'),('売買を自由に行う','売買を無税で行う')]}

def audit(raws,expected):
 for sid,changes in MUTATIONS.items():
  text=raws[sid].decode('cp932')
  for old,new in changes:
   require(old in text,'Real source mutation not matched: '+old)
   changed=dict(raws);changed[sid]=text.replace(old,new).encode('cp932')
   try: actual=derive(changed)
   except ValueError:continue
   require(actual!=expected,'Semantic mutation accepted: '+old)
 for sid in ('S1','S2'):
  changed=dict(raws);changed[sid]+=b'<script>unrelated=1</script>'
  require(derive(changed)==expected,'Peripheral script changed meaning')
 return {'semantic_mutations_rejected_without_digest_gate':sum(map(len,MUTATIONS.values())),'peripheral_script_positive_each_article':True}

def replay(raws,r):
 verify_report(r);ex=derive(raws);require(ex==r['extraction'],'Current source semantics changed')
 images=chain(raws,ex);require(images==r['images'],'Actual image chain/bytes changed')
 return {'schema':'stoneage.jp2005_market.replay.r1','inputs':[{'id':sid,'url':URLS[sid],'bytes':len(raws[sid]),'sha256':sha(raws[sid])} for sid in ('S1','S2')],
  'extraction':ex,'images':images,'image_observations':r['image_observations'],'catalog_records':catalog(ex),'comparison':comparison(),
  'audit':audit(raws,ex),'original_html_or_assets_in_output':False,'original_game_runtime_verified':False}

def read_inputs(directory=None):
 def get(url,name):
  if directory is not None:return (Path(directory)/name).read_bytes()
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'StoneAge-research/1.0'}),timeout=45) as response:
   require(response.status==200 and response.url==url,'HTTP source identity changed');raw=response.read(2_000_001)
  require(len(raw)<=2_000_000,'Input too large');return raw
 raws={sid:get(url,sid+'.html') for sid,url in URLS.items()};ex=derive(raws)
 for sid,ids in [('S1',['S1-MAP','S1-VIEW']),('S2',['S2-MAP'])]:
  for ident,url in zip(ids,ex['articles'][sid]['wrapper_urls']):
   raw=get(url,ident+'-wrapper.html');raws[ident+'-wrapper']=raw;p=Links();p.feed(markup(raw))
   urls=[urljoin(url,v) for v in p.images if 'news/image/' in urljoin(url,v)]
   require(len(urls)==1,'Original link ambiguous');raws[ident]=get(urls[0],ident+'.jpg')
 return raws

def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--fetch',action='store_true');g.add_argument('--input-dir');p.add_argument('--output',required=True);a=p.parse_args()
 r=json.loads(REPORT.read_text());out=replay(read_inputs(a.input_dir),r)
 custody=ROOT/f'research/recovered/{STEM}-CUSTODY-R1.json'
 if custody.exists():verify_custody()
 target=Path(a.output);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'articles':2,'linked_original_images':3,'catalog_records':3,'semantic_mutations':17}))

if __name__=='__main__':main()
