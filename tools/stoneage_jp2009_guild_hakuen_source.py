"""Independent limited source replay for JP2009 guild, Hakuen, and XP notices.

Read a single credited contemporary operator announcement. This verifies
announced content and attribution, never a live 2009 game server.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-JP2009-GUILD-HAKUEN-SOURCE-R1.json'
URL='https://www.4gamer.net/games/013/G001377/20090428039/'

def require(c,reason):
    if not c:raise ValueError(reason)
class Visible(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.text=[];self.block=0
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'):self.block+=1
        if not self.block:self.text.append(' ')
    def handle_endtag(self,tag):
        if tag in ('script','style') and self.block:self.block-=1
        if not self.block:self.text.append(' ')
    def handle_data(self,data):
        if not self.block:self.text.append(data)

PHRASES=(
    '株式会社デジパーク','ギルドシステムの実装','遠く離れた複数のお友達',
    '2009年4月28日（火）定期メンテナンス時','白炎チケット400Gstone',
    '白炎の袋','白炎スタンプ','便利商店スタッフ','すたんぷちゃん',
    'スタンプ5回','スタンプ10回','スタンプ15回','精霊の秘薬（日）',
    '24時間キャラクターの取得経験値2.0倍','プチ経験値イベント招待券',
    '※表1（白炎の袋出現アイテム）全7種類','白炎変身薬','白炎変身鎧チケット',
    '白炎再抽選チケット','白炎交換チケット','耐久のほら貝袋','気力のほら貝袋',
    'ログアウト/ドロップで消滅','はぐれシロベアル','低確率',
    'ギール採石場','虎追い山','閉ざされた氷窟','バルツ山',
    '秘薬の欠片','薬師','5つ渡した方','繰り返し行うことができます',
    '初回','二回目以降','60分間キャラクターの取得経験値3.0倍',
    '15分間キャラクターの取得経験値1.3倍'
)
def compact(b):
    p=Visible();p.feed(b.decode('utf-8-sig'))
    return re.sub(r'\s+','', ''.join(p.text))
def extract(payload):
    text=compact(payload)
    marker='メーカー発表文の内容をそのまま掲載しています'
    require(text.count(marker)==1,'Missing/ambiguous published operator-release boundary')
    body=text.split(marker,1)[1]
    # Stop only after the source publication disclaimer; do not source from site related articles.
    stop='※画像は、実際とは異なる場合があります。ご了承ください。'
    require(stop in body,'Release end disclaimer missing')
    body=body.split(stop,1)[0]+stop
    missing=[p for p in PHRASES if p not in body]
    require(not missing,'Operator body phrase missing: '+str(missing))
    require(body.count('ギルドシステム')>=2,'Guild section missing')
    return {'source_url':URL,'release_digest':hashlib.sha256(body.encode()).hexdigest(),
            'publisher':'デジパーク','verified_literal_fragments':len(PHRASES),
            'guild_long_distance_group_chat_mentioned':True,
            'hakuen_name':'ハクエン','ticket_price_gstone':400,
            'stamp_levels':[5,10,15],
            'declared_bag_variants':7,'visible_named_bag_variants':6,
            'lucky_enemy':'はぐれシロベアル','event_map_count_reported':15,
            'exchange_shards':5,'first_multiplier':3.0,'subsequent_multiplier':1.3,
            'authenticated_2009_original_official_html':False,
            'original_runtime_executed':False}
def validate(r):
    require(r['schema']=='stoneage.jp2009_guild_hakuen.source_contract.r1','Incorrect schema')
    require(len(r['sources'])==1 and r['sources'][0]['url']==URL,'Source scope changed')
    require(r['sources'][0]['issue_attribution']=='デジパーク','Misattributed issuer')
    require(r['sources'][0]['original_official_notice_html_sha256'] is None and r['sources'][0]['original_2009_capture_sha256'] is None,'Historical bytes falsely promoted')
    require(re.fullmatch(r'[0-9a-f]{64}',r['sources'][0]['current_release_core_sha256']) is not None,'Missing source core digest')
    require(r['sources'][0]['current_release_digest_does_not_authenticate_original_2009_html'] is True,'Current bytes claimed historical')
    g,h,e=r['guild'],r['hakuen'],r['limited_events']
    require(g['announced_maintenance_date']=='2009-04-28' and g['supported_function']=='MULTI_FRIEND_CHAT_ACROSS_DISTANCE','Guild function changed')
    require(g['guild_creation_prerequisites'] is None and g['guild_size_or_permissions'] is None,'Missing original guild rule invented')
    require(h['name']=='ハクエン' and h['ticket_price_gstone']==400 and h['ticket_name']=='白炎チケット','Pet/ticket changed')
    require(h['exchange_targets']==['白炎の袋','白炎スタンプ'],'Token exchange altered')
    require(h['bag_declared_distinct_item_types']==7 and h['bag_visible_named_rows']==6 and h['bag_seventh_name'] is None,'Seventh bag item fabricated')
    require([s['count'] for s in h['stamps']]==[5,10,15] and h['stamps'][1]['duration_hours']==24 and h['stamps'][1]['multiplier']==2,'Stamp milestones wrong')
    require(len(e['mentioned_spawns'])==15 and len(set(e['mentioned_spawns']))==15,'Original event venue count/duplicates')
    require(e['reported_low_probability'] and e['lucky_enemy']=='はぐれシロベアル','Event enemy claim changed')
    require(e['shards_per_exchange']==5 and e['repeatable'],'5-shard requirement changed')
    require((e['first_reward']['duration_minutes'],e['first_reward']['player_xp_multiplier'])==(60,3),'First-time XP claim changed')
    require((e['repeat_reward']['duration_minutes'],e['repeat_reward']['player_xp_multiplier'])==(15,1.3),'Repeat XP claim changed')
    require(len(r['records'])==7,'Wrong archival record count')
    for v in r['records']:
        require({'record_id','entity_type','version_profile','source_refs','verification_status','rights_status','record_revision'}<=v.keys(),'Archive record lacks required fields')
        require(v['version_profile']=='LATER_OFFICIAL:JP_DIGIPARK_2009' and v['source_refs']==['S1'] and v['game_ids'] is None,'Regional/source/ID scope elevated')
    for k,v in r['boundaries'].items():
        if isinstance(v,bool):require(v is False,'Forbidden promotion: '+k)
    require(r['boundaries']['stage_a']=='7_PARTIAL_2_OPEN' and r['boundaries']['stage_b_wiki']=='GATED' and r['boundaries']['r79']=='PAUSED_NON_BLOCKING','Stage changed')
    require(r['next']=='OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-40','Review queue changed')
def replay(report,payload):
    validate(report)
    fact=extract(payload)
    require(fact['release_digest']==report['sources'][0]['current_release_core_sha256'],'Release body digest differs from anchored source')
    assert fact['ticket_price_gstone']==report['hakuen']['ticket_price_gstone']
    return {'schema':'stoneage.jp2009_guild_hakuen.source_replay.r1',
            'current_http_bytes':len(payload),'current_http_sha256':hashlib.sha256(payload).hexdigest(),**fact}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--fetch',action='store_true');ap.add_argument('--html-file',type=Path);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();require(args.fetch!=bool(args.html_file),'Choose exactly one source')
    report=json.loads(REPORT.read_text(encoding='utf8'))
    if args.fetch:
        req=urllib.request.Request(URL,headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req,timeout=50) as rs:
            require(rs.status==200 and rs.url==URL,'Wrong HTTP response')
            data=rs.read(1_500_001)
            require(len(data)<=1_500_000,'Source too large')
    else:data=args.html_file.read_bytes()
    derived=replay(report,data)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(derived,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'result':'verified','source_sha':derived['current_http_sha256'],'checks':derived['verified_literal_fragments']},ensure_ascii=False))
if __name__=='__main__':main()
