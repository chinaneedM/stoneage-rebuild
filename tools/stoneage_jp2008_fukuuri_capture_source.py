"""Validate one bounded 2008 Gamania campaign press release without game-runtime inference."""
import argparse, hashlib, json, re, urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'research/recovered/STONEAGE-JP2008-FUKUURI-CAPTURE-SOURCE-R1.json'
URL='https://www.4gamer.net/games/013/G001377/20080715027/'
class Visible(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.parts=[];self.blocked=0
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'):self.blocked+=1
        if not self.blocked:self.parts.append(' ')
    def handle_endtag(self,tag):
        if tag in ('script','style') and self.blocked:self.blocked-=1
        if not self.blocked:self.parts.append(' ')
    def handle_data(self,data):
        if not self.blocked:self.parts.append(data)

def require(ok,why):
    if not ok:raise ValueError(why)

def validate(report):
    require(report['schema']=='stoneage.jp2008_fukuuri_capture_source.r1','schema mismatch')
    require(report['source']['url']==URL and report['source']['historical_original_html_sha256'] is None,'source/historic bytes mismatch')
    require(report['source']['release_issuer']=='ガマニアデジタルエンターテインメント','issuer mismatch')
    f=report['facts'];b=report['boundaries']
    require((f['reported_anniversary_year'],f['reported_pet_variety_count'],f['reported_ordinal_pet_name'])==(9,200,'フクゥーリ'),'milestone mismatch')
    require((f['event_start'],f['event_end'])==('2008-07-15 16:00','2008-07-29 13:00'),'campaign interval mismatch')
    require(f['eligibility_method']=='DIRECT_IN_GAME_CAPTURE_OF_FUKUURI_DURING_WINDOW' and f['traded_or_other_method_counts'] is False,'capture vs trade changed')
    require(f['requires_GASH_user'] and f['entries_per_account']==1,'GASH restriction changed')
    require((f['lottery_winner_slots'],f['prize_per_winner_label'])==(500,'100GASH ポイント'),'prize mismatch')
    require(f['prize_external_platform_not_in_game'] and f['distribution_actual_verified'] is False,'reward/distribution promotion')
    require(len(report['records'])==2 and {x['collection'] for x in report['records']}=={'pets','sources'},'archive records mismatch')
    for x in report['records']:
        require({'record_id','entity_type','version_profile','source_refs','verification_status','rights_status','record_revision'}<=x.keys(),'missing contract fields')
        require(x['source_refs']==['S1'] and x['game_ids'] is None and x['rights_status']=='RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED','source/game ID/rights promotion')
    require(all(v is False for k,v in b.items() if isinstance(v,bool)),'unsupported historical claim promoted')
    require((b['stage_a'],b['stage_b_wiki'],b['r79'])==('7_PARTIAL_2_OPEN','GATED','PAUSED_NON_BLOCKING'),'stage changed')
    require(report['next']=='OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-39','portfolio return changed')

def extract(html):
    p=Visible();p.feed(html.decode('utf-8-sig'))
    t=re.sub(r'\\s+','', ''.join(p.parts))
    mark='メーカー発表文の内容をそのまま掲載しています'
    require(t.count(mark)==1,'ambiguous release boundary')
    release=t.split(mark,1)[1].split('関連記事一覧へ',1)[0]
    fragments=[
      'ガマニアデジタルエンターテインメント','デジパーク',
      'サービス9周年目','ペットの種類が200種類を達成',
      '200種類目のペット「フクゥーリ」',
      '2008年7月15日火曜日16時','2008年7月29日火曜日13時',
      '抽選で500名','100GASHポイント',
      '捕獲以外の方法（トレード等）で入手した場合は対象外',
      '「GASH」ユーザーのみが対象','1アカウントにつき1回',
      '8月5日17時頃'
    ]
    missing=[x for x in fragments if x not in release]
    require(not missing,'Original attributed release phrase changed: '+','.join(missing))
    return {'source_url':URL,'release_boundary':'GAMANIA_OPERATOR_PRESS_BODY','evidence_flags_checked':len(fragments),
            'named_pet':'フクゥーリ','reported_species_varieties':200,'eligible_only_direct_capture':True,
            'trade_eligible':False,'external_gash_lottery_not_quest_reward':True,
            'source_body_digest_current':hashlib.sha256(release.encode()).hexdigest(),
            'historical_2008_original_page_authenticated':False}

def replay(report,payload):
    validate(report);actual=extract(payload)
    require(actual['reported_species_varieties']==report['facts']['reported_pet_variety_count'],'count mismatch')
    require(actual['named_pet']==report['facts']['reported_ordinal_pet_name'],'name mismatch')
    return {'schema':'stoneage.jp2008_fukuuri_capture.replay.r1','current_http_bytes':len(payload),
            'current_http_sha256':hashlib.sha256(payload).hexdigest(),**actual}
def main():
    a=argparse.ArgumentParser();a.add_argument('--fetch',action='store_true');a.add_argument('--html-file',type=Path);a.add_argument('--output',required=True,type=Path);args=a.parse_args()
    require(args.fetch != bool(args.html_file),'Select exactly one input')
    report=json.loads(REPORT.read_text(encoding='utf8'))
    if args.fetch:
        with urllib.request.urlopen(urllib.request.Request(URL,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as resp:
            require(resp.status==200 and resp.url==URL,'Unexpected URL/HTTP status')
            content=resp.read(1_500_001);require(len(content)<=1_500_000,'Oversize response')
    else:content=args.html_file.read_bytes()
    out=replay(report,content);args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\\n',encoding='utf8')
    print(json.dumps({'verified':True,'pet':out['named_pet'],'source_digest':out['current_http_sha256']},ensure_ascii=False))
if __name__=='__main__':main()
