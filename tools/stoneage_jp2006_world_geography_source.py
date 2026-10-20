"""Finite Japanese-2006 operator map-announcement verification; never run game code."""
import argparse, hashlib, json, re, urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-JP2006-WORLD-GEOGRAPHY-SOURCE-R1.json'
URLS=(
 'https://www.4gamer.net/news/history/2006.03/20060314171238detail.html',
 'https://www.4gamer.net/news/history/2006.05/20060501174657detail.html',
 'https://www.4gamer.net/games/013/G001377/20061207180354/'
)
PHRASES=(
 ('紅炎（こうえん）の地','第1回4月18日（火）予定','第2回5月2日（火）予定',
  '中・上級者向け','ミライア群島','北西に位置した火山島','火属性の恐竜','クエストも複数','第1回時から'),
 ('第1回2006年4月18日（火）終了','第2回2006年5月2日（火）予定','炎渦の頂（えんかのいただき）',
  '島の中央','ルートは多岐にわたり','特定の条件を満たしていないと入れない',
  '火属性の強力な恐竜','上層部','ボス','火口部'),
 ('ミライア群島','風の属性','標高が高く','年中風に吹き曝されている',
  '風化が進んだ大きな渓谷','ジャルガ島','川の水源','一年中雨が降っている','迷路のよう')
)
class Visible(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.parts=[];self.blocked=0
 def handle_starttag(self,tag,attrs):
  if tag in ('script','style'):self.blocked+=1
  if not self.blocked:self.parts.append(' ')
 def handle_endtag(self,tag):
  if tag in ('script','style') and self.blocked:self.blocked-=1
  if not self.blocked:self.parts.append(' ')
 def handle_data(self,data):
  if not self.blocked:self.parts.append(data)
def require(c,message):
 if not c:raise ValueError(message)
def decode(raw):
 for enc in ('utf-8-sig','cp932','euc_jp'):
  try:
   s=raw.decode(enc,'strict')
   if 'ストーンエイジ' in s and ('紅炎' in s or '香颯' in s):return s
  except UnicodeDecodeError:pass
 raise ValueError('Source Japanese encoding or identity not verified')
def compact(s):
 parser=Visible();parser.feed(s)
 return re.sub(r'\s+','', ''.join(parser.parts))
def extract(raw,i):
 require(i in (0,1,2),'Expected one of 3 source slots')
 t=compact(decode(raw))
 if i in (0,1):
  marker='以下リリースより'
  require(t.count(marker)==1,'Operator quotation start ambiguous/missing')
  t=t.split(marker,1)[1]
  t=t.split('ストーンエイジ■開発元',1)[0]
 else:
  a='香颯の地（リリースより）';b='雨祝の森（リリースより）'
  require(t.count(a)==1 and t.count(b)==1,'Both exact quoted map paragraphs required')
  t=t.split(a,1)[1].split('新しいマップでは',1)[0]
 missing=[p for p in PHRASES[i] if p not in t]
 require(not missing,'Quoted source phrase absent: '+str(missing))
 return {'source_id':f'M{i+1}','verified_quote_fragments':len(PHRASES[i]),
   'normalized_quoted_section_sha256':hashlib.sha256(t.encode()).hexdigest(),
   'current_http_bytes':len(raw),'current_http_sha256':hashlib.sha256(raw).hexdigest(),
   'historical_2006_original_bytes_authenticated':False}
def validate(r):
 require(r['schema']=='stoneage.jp2006_world_geography.source_contract.r1','Schema changed')
 require([s['url'] for s in r['sources']]==list(URLS),'Source locations changed')
 require(all(s['historical_original_2006_html_sha256'] is None for s in r['sources']),'Historical bytes invented')
 require(len(r['nodes'])==6 and len(r['relations'])==5 and len(r['timeline'])==4,'Source scope changed')
 require([x['name_as_written'] for x in r['nodes']]==['ミライア群島','紅炎の地','炎渦の頂','香颯の地','雨祝の森','ジャルガ島'],'Original written names changed')
 for x in r['nodes']:
  require(set(('record_id','entity_type','version_profile','source_refs','verification_status','rights_status','record_revision')) <= x.keys(),'Archive contract missing')
  require(x['game_ids'] is None and x['coordinate'] is None and x['asset_refs'] is None,'Original runtime IDs invented')
  require(x['version_profile']=='LATER_OFFICIAL:JP_GAIAX_2006','Original/other regional history promoted')
 require(r['relations'][0]['kind']=='NORTHWEST_RELATIVE_TO' and r['relations'][2]['actual_entry_conditions'] is None,'Route conditions or relative geography falsely completed')
 require(r['relations'][4]['kind']=='RIVER_HEADWATERS_ON_ISLAND','Watershed not preserved')
 require(all(not v['server_execution_verified'] for v in r['timeline']),'Contemporary release promoted to server execution')
 require(r['content']['boss_name'] is None and r['content']['exact_conditions'] is None and r['content']['fire_species_roster'] is None,'Unproven content inferred')
 require(all(v is False for v in r['boundaries'].values() if isinstance(v,bool)),'Unproven boundary upgraded')
 require((r['boundaries']['stage_a'],r['boundaries']['stage_b_wiki'],r['boundaries']['r79'])==('7_PARTIAL_2_OPEN','GATED','PAUSED_NON_BLOCKING'),'Stage altered')
 require(r['next']=='OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-41','Portfolio queue changed')
def replay(r,raw):
 validate(r);require(len(raw)==3,'Exactly 3 inputs required')
 return {'schema':'stoneage.jp2006_world_geography.derived_replay.r1',
 'sources':[extract(data,i) for i,data in enumerate(raw)],
 'map_ids_or_server_runtime_proven':False,'raw_html_in_output':False}
def main():
 p=argparse.ArgumentParser();p.add_argument('--fetch',action='store_true');p.add_argument('--html-dir',type=Path);p.add_argument('--output',type=Path,required=True)
 args=p.parse_args();require(args.fetch!=bool(args.html_dir),'Choose exactly one input method')
 r=json.loads(REPORT.read_text(encoding='utf-8'))
 if args.fetch:
  raw=[]
  for u in URLS:
   req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=45) as f:
    require(f.status==200,'Bad HTTP result')
    body=f.read(1500001);require(len(body)<=1500000,'Large source blocked')
    raw.append(body)
 else:raw=[(args.html_dir/f'M{i}.html').read_bytes() for i in range(1,4)]
 data=replay(r,raw)
 args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'verified_fragments':[s['verified_quote_fragments'] for s in data['sources']],'success':True},ensure_ascii=False))
if __name__=='__main__':main()
