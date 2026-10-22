"""R75: source-qualified CINS mammoth boarding, chat departure and exit workflow."""
import argparse
import hashlib
import io
import json
import re
import urllib.request
from pathlib import Path
from PIL import Image
from tools.stoneage_cn2011_stall_source import Article
from tools.stoneage_jp2005_treasure_source import VisibleMarkup, one, plain, require, sha

ROOT=Path(__file__).resolve().parents[1]
STEM='STONEAGE-CN2011-MAMMOTH-BUS'
REPORT=ROOT/f'research/recovered/{STEM}-SOURCE-R1.json'
URL='https://games.sina.com.cn/o/n/2011-12-19/1108562894.shtml'
URLS={'S1':URL}
PROFILE='LATER_OFFICIAL_CN_CINS_2011_PROMOTIONAL_TRANSPORT_EXACT_BUILD_UNKNOWN'
PARENTS=['research/recovered/STONEAGE-EARLY-CONTENT-GUIDE-MANUAL-R1.json',
 'research/recovered/STONEAGE-CN2003-VILLAGE-TRAVEL-RECORD-SOURCE-R1.json',
 'research/recovered/STONEAGE-PREPRODUCTION-CONTENT-ARCHIVE-R1.json']
PARSERS=['tools/stoneage_cn2011_stall_source.py','tools/stoneage_jp2005_treasure_source.py']
BOUNDARIES={k:False for k in ('direct_original_operator_page_acquired','current_bytes_authenticated_as_2011_original',
 'original_server_runtime_verified','both_advertised_versions_share_transport_build','early_jss_go_command_backfilled',
 'early_fare_capacity_wait_encounter_rules_backfilled_to_2011','screenshot_is_completed_trip_or_command_execution',
 'displayed_endpoint_names_are_directed_route_edges','jpeg_size_is_native_client_resolution',
 'same_scene_means_before_after_or_animation','pixels_are_release_approved','original_html_or_assets_committed','stage_b_started')}


def parse(raw):
 text=raw.decode('gb18030',errors='strict');m=VisibleMarkup();m.feed(text);text=''.join(m.parts)
 title=plain(one(r'<h1 id="artibodyTitle">(.*?)</h1>',text,re.S))
 publication=plain(one(r'<span id="pub_date">(.*?)</span>',text,re.S))
 require(title=='长毛象公车有木有石器时代长毛象出动' and publication=='2011年12月19日11:08','Visible title/publication changed')
 p=Article();p.feed(text);require(p.roots==1 and p.article_depth==0 and p.p_depth==0,'Exactly one closed visible article required')
 starts=[i for i,v in enumerate(p.paragraphs) if v.startswith('在原始大陆上的')]
 require(len(starts)==1,'Unique transport section required');i=starts[0];parts=p.paragraphs[i:i+3]
 require(len(parts)==3 and parts[1].startswith('如何才能乘坐') and parts[2].startswith('一边乘坐'),'Ordered transit paragraphs missing')
 require(p.paragraphs[i+3]=='更多精彩，敬请继续锁定胜思网络《石器时代》！','Operator attribution detached')
 require(len(p.images)==3 and [v['alt'] for v in p.images]==['长毛象客运','长毛象公车','精美的石器时代壁纸'],'Article image scope changed')
 body=''.join(parts)
 require('href="http://sa.cins.cn"' in text and '后续研发以及运营由广东胜思网络科技有限公司全权负责' in ''.join(p.paragraphs),'Operator link/context changed')
 about=next(v for v in p.paragraphs if '后续研发以及运营由' in v)
 require('8.5魔域大冒险' in about and '2.5“精灵王传说”版本服务器' in about,'Mixed version context changed')
 return {'title':title,'publication_as_written':publication,'parts':parts,'core':body,'image_references':p.images}


def extract(raw):
 p=parse(raw);a,b,c=p['parts']
 require('各大村庄门口设立了一个长毛象公交' in a and '根据各村庄人口密集程度、与下一个目的地的距离等因素而建立' in a,'Station scope or planning factors changed')
 require('先要找到设立了长毛象客运站的地方，并且选择需要前往的目的地的线路' in b and '在长毛象面前点击' in b,'Boarding preconditions changed')
 button=one(r'在长毛象面前点击“([^”]+)”按钮，即可以搭乘',b)
 channel,command=one(r'玩家只需在([^中]+)中输入“([^”]+)”',b)
 require('特设置了一个快速发车通道' in b,'Fast departure scope changed')
 timing=one(r'，长毛象公车就([^！]+)哦！$',b)
 exit_control=one(r'而中途想下车的乘客，你可以选择([^、]+)、这样你就能结束你的长毛象公交旅途',c)
 return {'title':p['title'],'publication_as_written':p['publication_as_written'],
  'source_layer':'CINS_NAMED_PROMOTIONAL_ARTICLE_PUBLISHED_BY_SINA_NOT_AUTHENTICATED_ISSUER_FILE',
  'operator':'广东胜思网络科技有限公司','official_link_as_written':'http://sa.cins.cn',
  'version_context':{'advertised':['8.5魔域大冒险','2.5精灵王传说'],'transport_bound_to_either_build':None},
  'station_scope':'VILLAGE_ENTRANCES_AS_PROMOTIONAL_DESCRIPTION_NOT_ENUMERATED_ALL_VILLAGES',
  'stated_planning_factors':['VILLAGE_POPULATION_DENSITY','DISTANCE_TO_NEXT_DESTINATION'],
  'boarding':{'steps':['FIND_BUS_STATION','SELECT_DESTINATION_ROUTE','FACE_MAMMOTH','CLICK_JOIN_PARTY'],
   'button_as_written':button,'exact_icon_or_coordinates':None},
  'fast_departure':{'channel_as_written':channel,'command_as_written':command,'timing_as_written':timing,
   'case_variants':None,'authorization_or_minimum_passengers':None,'accepted_server_command_observed':False},
  'exit':{'control_as_written':exit_control,'mid_trip_exit_described':True,'drop_location':None,'refund':None},
  'unknown_rules':{k:None for k in ('fare','passenger_capacity','normal_wait_minutes','random_encounters','named_stop_roster','route_edges','travel_duration','npc_ids','map_ids','original_build','server_save_result')},
  'core_fingerprint':{'characters':len(p['core']),'utf8_bytes':len(p['core'].encode()),'sha256':sha(p['core'].encode())},
  'image_references':p['image_references'],'original_server_runtime_verified':False}


def pin(path):
 b=(ROOT/path).read_bytes();return {'path':path,'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}


def comparison():
 early=json.loads((ROOT/PARENTS[0]).read_text());cn=json.loads((ROOT/PARENTS[1]).read_text())
 bus=next(v for v in cn['transport_modes'] if v['id']=='MAMMOTH_BUS');air=next(v for v in cn['transport_modes'] if v['id']=='GAMI_AIR')
 return {'relation':'SOURCE_AND_REGION_SEPARATION_NOT_PROVEN_HISTORICAL_EVOLUTION',
  'jss2001':{'source_report':PARENTS[0],'actual_capture':early['manual_capture'],'bus':early['observations']['manual_contracts']['bus']},
  'cn2003_player_guide':{'source_report':PARENTS[1],'bus':bus,'aviation_departure_words':air['claims']['reported_departure_words'],
   'go_aviation_not_mammoth_in_that_guide':True},
  'same_original_npc_map_or_command_id_proven':False,'jss_go_support_proven':False,
  'early_numbers_fill_2011_unknowns':False,'both_2011_advertised_versions_verified':False,'modern_adoption_decided':False}


def inspect_images(raws,r):
 out=[]
 for i,p in enumerate(r['images']):
  b=raws[p['id']]
  with Image.open(io.BytesIO(b)) as im:im.load();actual={'bytes':len(b),'sha256':sha(b),'format':im.format,'mode':im.mode,'size':list(im.size)}
  require(all(actual[k]==p[k] for k in actual),'Actual linked original image changed')
  require(p['url_as_written']==r['extraction']['image_references'][i]['src'] and p['requested_url']==p['url_as_written'].replace('http://','https://',1),'Image URL not from selected body')
  out.append(p)
 return out


def catalog(ex,visual):
 entries=[('TRANSIT','tutorials','DOCUMENTARY_TRANSIT_INTERACTION',['S1'],{k:ex[k] for k in ('station_scope','boarding','fast_departure','exit','unknown_rules')})]
 entries += [(v['id'],'screens','DOCUMENTARY_TRANSPORT_SCENE',['S1',v['id']],v) for v in visual]
 return [{'record_id':'CN2011-R75-'+ident,'collection':collection,'entity_type':kind,'version_profile':PROFILE,
  'source_refs':refs,'verification_status':'SOURCE_DESCRIPTION_OR_STATIC_IMAGE_NOT_RUNTIME','rights_status':'RESEARCH_METADATA_NOT_RELEASE_APPROVED',
  'record_revision':1,'game_ids':None,'content':content} for ident,collection,kind,refs,content in entries]


def verify_report(r):
 require(r['version_profile']==PROFILE and r['negative_boundaries']==BOUNDARIES,'Version or authority promoted')
 require(r['parent_pins']==[pin(p) for p in PARENTS] and r['parser_dependency_pins']==[pin(p) for p in PARSERS],'Parent/shared parser bytes changed')
 require(r['comparison']==comparison() and r['catalog_records']==catalog(r['extraction'],r['image_observations']),'Comparison/catalog detached')
 ex=r['extraction'];require(ex['source_layer']=='CINS_NAMED_PROMOTIONAL_ARTICLE_PUBLISHED_BY_SINA_NOT_AUTHENTICATED_ISSUER_FILE' and ex['original_server_runtime_verified'] is False,'Source authority promoted')
 require(all(v is None for v in ex['unknown_rules'].values()) and len(ex['unknown_rules'])==11 and ex['version_context']['transport_bound_to_either_build'] is None,'Cross version unknown promoted')
 require(ex['boarding']['exact_icon_or_coordinates'] is None and all(ex['fast_departure'][k] is None for k in ('case_variants','authorization_or_minimum_passengers')) and ex['fast_departure']['accepted_server_command_observed'] is False and ex['exit']['drop_location'] is None and ex['exit']['refund'] is None,'UI/command execution invented')
 require(r['image_observations']==[
  {'id':'I1','manual_visual_review':True,'kind':'GAME_SCENE_WITH_TRANSPORT_STATION','observed':['TOP_ICON_TOOLBAR','MAMMOTH_NEAR_STONE_QUEUE_BAYS','CHARACTERS_AND_SIGNPOSTS','BOTTOM_LABEL_LONG_HAIRED_ELEPHANT_TRANSPORT'],
   'original_map_or_npc_id':None,'boarding_or_command_execution_observed':False,'native_client_resolution':None},
  {'id':'I2','manual_visual_review':True,'kind':'GAME_SCENE_WITH_MAMMOTH_AND_HOVER_LABEL','observed':['TOP_ICON_TOOLBAR','MAMMOTH_AT_QUEUE_BAY','CHARACTERS_AND_SIGNPOSTS'],
   'readable_endpoint_tokens':['萨姆吉尔','玛丽那丝'],'label_scope':'TWO_NAMES_IN_DISPLAYED_LABEL_NOT_DIRECTED_ROUTE_EDGES',
   'separator_and_full_line_not_transcribed':True,'original_map_or_npc_id':None,'boarding_or_command_execution_observed':False,'native_client_resolution':None}], 'Visual interpretation promoted')
 require([(p['bytes'],p['sha256'],p['size']) for p in r['images']]==[(74139,'2b95dc810d305fb58d0cb6132e5d6e0b26f6ac970c1146fa9907e940b698f21b',[550,413]),(72157,'3324aaaf92d8b7c39b4d5ea20f8bb60d09d276cc96aaaf5b2554dfece057b239',[550,413])],'Manual observation detached from exact JPEG')
 require(r['unselected_image']=={'source_reference_index':2,'role_as_written':'精美的石器时代壁纸','pixels_acquired':False},'Wallpaper evidence promoted')

MUTATIONS=[('各大村庄门口','各大村庄医院'),('人口密集程度、与下一个目的地的距离','玩家等级、与下一个目的地的距离'),
 ('选择需要前往的目的地的线路','随机选择任意线路'),('在长毛象面前点击','在长毛象背后点击'),('“加入队伍”按钮','“离开队伍”按钮'),
 ('普通聊天频道中输入','家族聊天频道中输入'),('输入“go”','输入“GO”'),('立即为你启动','十分钟后为你启动'),
 ('退出团队、这样','解散团队、这样'),('快速发车通道','付费发车通道'),('胜思网络《石器时代》！','其他网络《石器时代》！'),('8.5魔域大冒险','8.6魔域大冒险')]


def audit(raw,expected):
 text=raw.decode('gb18030');target={k:v for k,v in expected.items() if k!='core_fingerprint'}
 for old,new in MUTATIONS:
  require(old in text,'Real source mutation anchor absent')
  try:actual=extract(text.replace(old,new).encode('gb18030'))
  except ValueError:continue
  actual.pop('core_fingerprint');require(actual!=target,'Semantic mutation masked by source digest: '+old)
 require(extract(raw+b'<script>peripheral=1</script>')==expected,'Peripheral script changed meaning')
 require('1125个原始地图' in text and extract(text.replace('1125个原始地图','9999个原始地图').encode('gb18030'))==expected,'Unselected map boast leaked into transit')
 return {'semantic_mutations_rejected_without_digest_or_core_fingerprint_gate':len(MUTATIONS),'peripheral_script_positive':True,'unselected_map_count_positive':True}


def replay(raws,r):
 verify_report(r);ex=extract(raws['S1']);require(ex==r['extraction'],'Current transit semantics changed')
 images=inspect_images(raws,r)
 return {'schema':'stoneage.cn2011_mammoth.replay.r1','inputs':[{'id':'S1','url':URL,'bytes':len(raws['S1']),'sha256':sha(raws['S1'])}],
  'extraction':ex,'images':images,'image_observations':r['image_observations'],'catalog_records':catalog(ex,r['image_observations']),
  'comparison':comparison(),'audit':audit(raws['S1'],ex),'original_html_or_assets_in_output':False,'original_game_runtime_verified':False}


def read_inputs(directory=None):
 def get(url,name):
  if directory is not None:return (Path(directory)/name).read_bytes()
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'StoneAge-research/1.0'}),timeout=45) as response:
   require(response.status==200 and response.url==url,'HTTP identity changed');raw=response.read(2_000_001)
  require(len(raw)<=2_000_000,'Input too large');return raw
 raw=get(URL,'S1.html');ex=extract(raw);out={'S1':raw}
 for i,ref in enumerate(ex['image_references'][:2],1):out['I'+str(i)]=get(ref['src'].replace('http://','https://',1),'I'+str(i)+'.jpg')
 return out


def main():
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--fetch',action='store_true');g.add_argument('--input-dir');p.add_argument('--output',required=True);a=p.parse_args()
 r=json.loads(REPORT.read_text());out=replay(read_inputs(a.input_dir),r)
 if (ROOT/f'research/recovered/{STEM}-CUSTODY-R1.json').exists():verify_custody()
 target=Path(a.output);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'articles':1,'actual_scene_jpegs':2,'catalog_records':3,'semantic_mutations':12}))

if __name__=='__main__':main()
