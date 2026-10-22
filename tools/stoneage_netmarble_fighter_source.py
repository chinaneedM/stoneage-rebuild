"""R76: one current official mobile fighter biography and actual attached artwork."""
import argparse
import hashlib
import io
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from PIL import Image
from tools.stoneage_jp2005_treasure_source import VisibleMarkup, one, plain, require, sha

ROOT=Path(__file__).resolve().parents[1]
STEM='STONEAGE-NETMARBLE-JA-WOODY'
REPORT=ROOT/f'research/recovered/{STEM}-SOURCE-R1.json'
URL='https://stoneage.netmarble.com/ja/gameinfo/character'
URLS={'S1':URL}
PROFILE='OFFICIAL_NETMARBLE_STONEAGE_IDLE_ADVENTURE_JA_CURRENT_20261022_BUILD_UNKNOWN'
PARENTS=['research/recovered/STONEAGE-JP2003-CHARACTER-VISUAL-SOURCE-R1.json',
 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json',
 'docs/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.md']
PARSER='tools/stoneage_jp2005_treasure_source.py'
BOUNDARIES={k:False for k in ('current_mobile_product_is_original_pc_build','official_name_backfilled_to_unnamed_2003_web_position',
 'residence_is_proven_spawn_or_original_map_id','personality_is_combat_stats','narrative_courage_is_levelup_or_buff',
 'duplicate_name_em_elements_are_two_characters','default_ssr_detail_is_full_roster','static_png_is_client_sprite_model_or_animation',
 'cdn_path_date_authenticates_publication_or_build','bgm_button_proves_audio_call_arguments','production_rights_granted',
 'original_html_or_assets_committed','original_game_runtime_verified','stage_b_started')}
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

class Detail(HTMLParser):
 def __init__(self):
  super().__init__();self.depth=0;self.section=self.detail=self.name=self.info=self.figure=self.em=0
  self.sections=self.roots=0;self.names=[];self.current=[];self.bio=[];self.images=[];self.meta=[];self.canonical=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);classes=a.get('class','').split()
  if tag not in VOID:self.depth+=1
  if tag=='meta' and a.get('property')=='og:title':self.meta.append(a.get('content'))
  if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
  if tag=='section' and 'character' in classes:self.sections+=1;self.section=self.depth
  if not self.section:return
  if tag=='div' and 'detail' in classes:self.roots+=1;self.detail=self.depth
  if not self.detail:return
  if tag=='div' and 'name' in classes:self.name=self.depth
  if tag=='div' and 'info' in classes:self.info=self.depth
  if tag=='figure' and 'image-main' in classes:self.figure=self.depth
  if tag=='em' and self.name:self.em=self.depth;self.current=[]
  if tag=='img' and self.figure:self.images.append(a.get('src'))
 def handle_endtag(self,tag):
  if tag=='em' and self.em==self.depth:self.names.append(''.join(self.current));self.em=0
  if self.name==self.depth and tag=='div':self.name=0
  if self.info==self.depth and tag=='div':self.info=0
  if self.figure==self.depth and tag=='figure':self.figure=0
  if self.detail==self.depth and tag=='div':self.detail=0
  if self.section==self.depth and tag=='section':self.section=0
  if tag not in VOID:self.depth-=1
 def handle_data(self,data):
  if self.em:self.current.append(data)
  if self.info:self.bio.append(data)


def parse(raw):
 m=VisibleMarkup();m.feed(raw.decode('utf8',errors='strict'));text=''.join(m.parts)
 title=plain(one(r'<title[^>]*>(.*?)</title>',text,re.S))
 lang=one(r'<html\b[^>]*\blang="([^"]+)"',text)
 copyright=plain(one(r'<p class="copyright"[^>]*>(.*?)</p>',text,re.S))
 p=Detail();p.feed(text)
 require(p.sections==p.roots==1 and p.section==p.detail==p.name==p.info==p.figure==p.em==0,'One closed visible character detail required')
 require(title=='ストーンエイジ：放置冒険' and lang=='ja' and p.meta==[title] and p.canonical==[URL],'Official product/locale/canonical changed')
 require(copyright=='ⓒNetmarbleCorp.&NetmarbleN2Inc.AllRightsReserved.','Official footer identity changed')
 require(len(p.names)==2 and p.names[0]==p.names[1] and p.names[0],'Repeated name presentation is missing or conflicting')
 require(len(p.images)==1 and p.images[0].startswith('https://sgimage.netmarble.com/images/netmarble/'),'Exactly one attached main artwork required')
 bio=''.join(''.join(p.bio).split());require(bio,'Biography absent')
 return {'title':title,'language':lang,'name':p.names[0],'name_render_instances':len(p.names),'biography':bio,'artwork_url':p.images[0]}


def extract(raw):
 p=parse(raw);bio=p.pop('biography')
 village=one(r'^([^で]+)で暮らしており',bio)
 traits=one(r'で暮らしており(.+?)な性格。',bio).split('、')
 qualities=one(r'冒険を経て(.+?)姿を徐々に見せるようになる。$',bio)
 require(len(traits)==3 and all(traits),'Three separately stated personality traits required')
 return {**p,'source_layer':'CURRENT_FIRST_PARTY_NETMARBLE_JAPANESE_MOBILE_PRODUCT_WEBSITE',
  'logical_characters_in_selected_detail':1,'publication_date':None,'exact_client_build':None,
  'residence':{'village_as_written':village,'scope':'NARRATIVE_RESIDENCE_NOT_SPAWN','map_id':None,'coordinates':None},
  'personality':{'traits_as_written':traits,'scope':'BIOGRAPHY_NOT_COMBAT_STATS'},
  'narrative_arc':{'experience':'ADVENTURES','qualities_as_written':qualities,'gradual_as_described':True,
   'scope':'NARRATIVE_CHARACTER_DEVELOPMENT_NOT_PROVEN_GAMEPLAY_PROGRESSION','level_or_quest_trigger':None,'stat_delta':None},
  'unknowns':{k:None for k in ('age','gender_as_stated_in_text','hp','attack','defense','skills','original_character_id','body_face_sprite_ids','animation_ids')},
  'biography_fingerprint':{'characters':len(bio),'utf8_bytes':len(bio.encode()),'sha256':sha(bio.encode())},
  'original_game_runtime_verified':False}


def pin(path):
 b=(ROOT/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def comparison():
 old=json.loads((ROOT/PARENTS[0]).read_text())
 return {'relation':'DIFFERENT_OFFICIAL_PRODUCTS_NOT_AN_IDENTITY_OR_CANON_JOIN',
  'pc_hangame2003':{'source_report':PARENTS[0],'page_capture':old['page']['actual_capture'],
   'operator_describes_no_fixed_names':old['identity']['operator_explicitly_describes_no_fixed_names'],
   'player_naming_described':old['identity']['player_naming_described'],'web_positions':len(old['characters'])},
  'current_mobile':{'product':'ストーンエイジ：放置冒険','language':'ja','selected_character':'ウッディ','source':URL},
  'current_name_applied_to_pc_position':None,'same_original_model_or_body_id_proven':False,
  'same_worldline_or_retcon_proven':False,'early_naming_description_contradicted':False,'modern_adoption_decided':False}


def catalog(ex,images,visual):
 return [{'record_id':'NETMARBLE-JA-R76-WOODY','collection':'characters','entity_type':'OFFICIAL_MOBILE_FIGHTER_BIOGRAPHY_AND_WEB_ART_REFERENCE',
  'version_profile':PROFILE,'source_refs':['S1','I1'],'verification_status':'OFFICIAL_WEB_TEXT_AND_STATIC_ART_NOT_CLIENT_RUNTIME',
  'rights_status':'RESEARCH_METADATA_NOT_RELEASE_APPROVED','record_revision':1,'game_ids':None,
  'content':{'biography':{k:ex[k] for k in ('name','residence','personality','narrative_arc','unknowns')},'artwork':images[0],'visual_observation':visual[0]}}]


def inspect_image(raw,r):
 p=r['images'][0]
 with Image.open(io.BytesIO(raw)) as im:
  im.load();actual={'bytes':len(raw),'sha256':sha(raw),'format':im.format,'mode':im.mode,'size':list(im.size),'frames':getattr(im,'n_frames',1)}
  alpha=list(im.convert('RGBA').getchannel('A').getextrema())
 require(all(actual[k]==p[k] for k in actual) and alpha==[0,255],'Original artwork bytes/geometry/transparency changed')
 require(p['url']==r['extraction']['artwork_url'],'Artwork detached from active detail')
 return [p]


def verify_report(r):
 require(r['version_profile']==PROFILE and r['negative_boundaries']==BOUNDARIES,'Product or evidence boundaries promoted')
 require(r['parent_pins']==[pin(p) for p in PARENTS] and r['parser_dependency_pin']==pin(PARSER),'Parent or shared parser bytes changed')
 require(r['comparison']==comparison() and r['catalog_records']==catalog(r['extraction'],r['images'],r['image_observations']),'Comparison/catalog detached')
 ex=r['extraction'];require(ex['source_layer']=='CURRENT_FIRST_PARTY_NETMARBLE_JAPANESE_MOBILE_PRODUCT_WEBSITE' and ex['logical_characters_in_selected_detail']==1 and ex['name_render_instances']==2 and ex['original_game_runtime_verified'] is False,'Source scope or duplicate presentation promoted')
 require(ex['publication_date'] is None and ex['exact_client_build'] is None and len(ex['unknowns'])==9 and all(v is None for v in ex['unknowns'].values()),'Unknown dates/identity/stats promoted')
 require(ex['residence']['scope']=='NARRATIVE_RESIDENCE_NOT_SPAWN' and ex['residence']['map_id'] is None and ex['residence']['coordinates'] is None and ex['personality']['scope']=='BIOGRAPHY_NOT_COMBAT_STATS','Story became gameplay coordinates/stats')
 require(ex['narrative_arc']['scope']=='NARRATIVE_CHARACTER_DEVELOPMENT_NOT_PROVEN_GAMEPLAY_PROGRESSION' and ex['narrative_arc']['level_or_quest_trigger'] is None and ex['narrative_arc']['stat_delta'] is None,'Narrative arc became gameplay trigger')
 require(r['image_observations']==[{'id':'I1','manual_visual_review':True,'kind':'STATIC_FULL_FIGURE_OFFICIAL_WEB_ILLUSTRATION',
  'observed':['BROWN_HAIR_WITH_TOP_KNOT','FUR_TRIMMED_WRAPS','BARE_FEET','LARGE_STONE_BLADE_RESTING_OVER_SHOULDER'],
  'alpha_extrema':[0,255],'canonical_weapon_item_id':None,'client_model_or_sprite_binding':None,'animation_or_direction_set':None,'release_rights_granted':False}], 'Artwork interpretation promoted')
 require(len(r['images'])==1 and (r['images'][0]['bytes'],r['images'][0]['sha256'],r['images'][0]['size'],r['images'][0]['format'],r['images'][0]['mode'],r['images'][0]['frames'])==(133427,'623e33509df4f46aa7adaf8862d1d9676606579bc3b81fc4b13f66cf6ce5a62a',[960,1196],'PNG','P',1),'Manual observation detached from reviewed PNG')

MUTATIONS=[('ストーンエイジ：放置冒険','別のゲーム'),('lang="ja"','lang="en"'),('ウッディ','別人'),('サムギル村','別の村'),
 ('優柔不断','決断力豊か'),('天然','慎重'),('楽天的','悲観的'),('冒険を経て','戦闘勝利で'),('正義感溢れる勇敢な','冷酷で臆病な'),
 ('徐々に見せる','直ちに見せる'),('class="detail"','class="navigation"'),('class="image-main"','class="thumbnail"')]


def audit(raw,expected):
 text=raw.decode('utf8');target={k:v for k,v in expected.items() if k!='biography_fingerprint'}
 for old,new in MUTATIONS:
  require(old in text,'Real source mutation absent: '+old)
  try:actual=extract(text.replace(old,new).encode())
  except ValueError:continue
  actual.pop('biography_fingerprint');require(actual!=target,'Mutation accepted by semantic extraction: '+old)
 require(extract(raw+b'<script>peripheral=1</script>')==expected,'Peripheral script affected visible identity')
 p=parse(raw);url=p['artwork_url'];require('20260209' in url,'Actual CDN date mutation anchor absent');changed=text.replace(url,url.replace('20260209','20990101'))
 require(extract(changed.encode())['publication_date'] is None,'CDN path date became publication date')
 return {'semantic_mutations_rejected_without_digest_or_biography_fingerprint_gate':len(MUTATIONS),'peripheral_script_positive':True,'cdn_path_not_publication_date_positive':True}


def replay(raws,r):
 verify_report(r);ex=extract(raws['S1']);require(ex==r['extraction'],'Official detail semantics changed');images=inspect_image(raws['I1'],r)
 return {'schema':'stoneage.netmarble_ja_woody.replay.r1','inputs':[{'id':'S1','url':URL,'bytes':len(raws['S1']),'sha256':sha(raws['S1'])}],
  'extraction':ex,'images':images,'image_observations':r['image_observations'],'catalog_records':catalog(ex,images,r['image_observations']),
  'comparison':comparison(),'audit':audit(raws['S1'],ex),'original_html_or_assets_in_output':False,'original_game_runtime_verified':False}


def read_inputs(directory=None):
 def get(url,name):
  if directory is not None:return (Path(directory)/name).read_bytes()
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'StoneAge-research/1.0'}),timeout=45) as response:
   require(response.status==200 and response.url==url,'HTTP identity changed');b=response.read(2_000_001)
  require(len(b)<=2_000_000,'Input too large');return b
 raw=get(URL,'S1.html');ex=extract(raw);return {'S1':raw,'I1':get(ex['artwork_url'],'I1.png')}


def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--fetch',action='store_true');g.add_argument('--input-dir');p.add_argument('--output',required=True);a=p.parse_args()
 r=json.loads(REPORT.read_text());out=replay(read_inputs(a.input_dir),r)
 if (ROOT/f'research/recovered/{STEM}-CUSTODY-R1.json').exists():verify_custody()
 target=Path(a.output);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'official_detail':1,'logical_character':1,'static_png':1,'semantic_mutations':12}))

if __name__=='__main__':main()
