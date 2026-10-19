"""Replay one dated player guide and its fixed 2003 HTML capture, without images or runtime."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import urllib.request

from tools.stoneage_cn2003_christmas_source import Visible, require

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-PIRATE-RELIC-GUIDE-SOURCE-R1.json'
URLS = (
    'https://games.sina.com.cn/zhqu/sta/sa6/rw/hzw.shtml',
    'https://web.archive.org/web/20031204053709id_/http://games.sina.com.cn:80/zhqu/sta/sa6/rw/hzw.shtml',
)


def extract(payload):
    html = payload.decode('gb18030')
    require('2003-05-21 22:27' in html, 'Dated guide identity missing')
    require('华义官方授权新浪石器' in html, 'Portal authorization label missing')
    p = Visible()
    p.feed(html)
    text = re.sub(r'\s+', '', ''.join(p.parts))
    start, end = '海贼王遗迹任务(可一转做一次)', '胜利后再次对话就会被传到下层开启宝箱了~。'
    require(text.count(start) == text.count(end) == 1, 'Missing or ambiguous guide body')
    core = text[text.index(start):text.index(end) + len(end)]
    recommendation = re.search(r'推荐等级：LV(\d+)', core)
    breath = re.search(r'鱼鳃草-使用后可在水底呼吸([^”]+)', core)
    loss = re.search(r'耐久力大概每分钟会减你总耐久力的(\d+/\d+)', core)
    shark = re.search(r'在\((\d+)(\d{3})\)遇到一只LV(\d+)的大白鲨', core)
    # Preserve the source coordinate pair, whose whitespace was normalized away.
    require(shark and shark[1] == '181' and shark[2] == '322', 'Guide shark coordinate changed')
    pets = re.search(r'需要(\d+)只等级不能超过(\d+)的人龙\(([^)]+)\)', core)
    payment = re.search(r'需要(\d+)万石币的报酬或者是([^改]+)改点酒\(必须是([^\)]+)\)', core)
    require(all((recommendation, breath, loss, pets, payment)), 'Guide material/rule clauses missing')
    require('1，不可思议的贝壳。2，解完海贼秘宝任务。' in core, 'Prerequisites changed')
    require('两个海贼王宝箱的钥匙' in core and '杰克森会随机收走你身上的人龙' in core, 'Key count/random hand-in warning missing')
    require('上述的时间为现实中的时间' in core and '一次总共可以在水底遨游两个小时' in core, 'Real-time/two-grass explanation missing')
    require('拿着钥匙，再次来到海底，并打败守门的鲨鱼，就可以见到贝克，与其对话，展开战斗' in core, 'Second shark/Baker combat transition missing')
    require('从(5417)进入' in core and '贝克(712)' in core and '奇喀喀村(4456)找到杰克森' in core, 'Guide route coordinates missing')
    facts = dict(recommended_level=int(recommendation[1]), recommendation_is_requirement=False,
                 repeat_claim_as_written='可一转做一次', prerequisites=['不可思议的贝壳', '解完海贼秘宝任务'],
                 breathing_item='鱼鳃草', breathing_duration_as_written=breath[1],
                 no_grass_hp_loss_per_real_minute_approx_fraction=loss[1],
                 two_hour_explanation='USE_ONE_THEN_REQUEST_ANOTHER_NOT_ONE_GRASS_LASTS_TWO_HOURS',
                 shark_level=int(shark[3]), source_coordinates={'shark':[181,322],'wreck_entry':[54,17],'贝克':[7,12],'杰克森':[44,56]},
                 pet_total=int(pets[1]), pet_level_max_inclusive=int(pets[2]), requested_pet_names=pets[3].split('，'),
                 payment_alternatives=[{'currency':'石币','amount':int(payment[1])*10000},{'item':payment[3],'quantity_as_written':payment[2]}],
                 keys_reported=2, random_pet_removal_warning=True,
                 flow=['FISHERMAN_GRASS','SHARK_THEN_WRECK','BAKER_REFERS_TO_JACKSON','JACKSON_MATERIAL_EXCHANGE','RETURN_SHARK_THEN_BAKER_FIGHT_TALK_CHEST'])
    return {'core_sha256':sha256(core.encode()).hexdigest(),'core_utf8_bytes':len(core.encode()),'facts':facts}


def validate(r):
    require(r['schema']=='stoneage.pirate_relic_guide_source.r1', 'Wrong schema')
    require([s['http']['url'] for s in r['inputs']]==list(URLS), 'Finite sources changed')
    require(r['authority']=='DATED_PORTAL_PLAYER_GUIDE_NOT_OPERATOR_AUTHORED_RELEASE', 'Player guide promoted to operator author')
    require(r['inputs'][0]['extracted']==r['inputs'][1]['extracted'], 'Era/current guide mismatch')
    require(len(r['records'])==8, 'Eight source records required')
    required={'record_id','entity_type','version_profile','source_refs','verification_status','rights_status','record_revision'}
    for row in r['records']:
        require(required<=row.keys() and row['game_ids'] is None, 'Original ID or contract changed')
        require(row['rights_status']=='RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED' and row['verification_status']=='PLAYER_GUIDE_REPORTED_NOT_RUNTIME','Evidence/rights promotion')
    q=r['records'][0]
    require(q['facts']==r['inputs'][0]['extracted']['facts'], 'Facts detached from source')
    require(q['minimum_character_level'] is None and q['reset_implementation'] is None and q['chest_contents'] is None,'Recommendation/reset/reward invented')
    recipe=r['records'][4]
    require(recipe['payment_logic']=='PETS_AND_EITHER_MONEY_OR_VODKA' and recipe['quantity_per_pet_name'] is None and recipe['random_selection_filter'] is None,'Payment conjunction or pet selection invented')
    require(r['boundaries']==dict(original_server_execution_verified=False,exact_region=None,exact_client_build=None,
        portal_sa6_path_certifies_cn60_or_tw45=False,portal_authorization_is_article_authorship=False,
        unnamed_tear_sea_lovers_are_evening_lorin=False,source_coords_are_original_map_ids=False,
        one_key_means_one_reward_item=False,original_images_fetched=False,original_html_or_assets_committed=False,
        tw10_or_jss1999_backfill=False,stage_a='7_PARTIAL_2_OPEN',stage_b_and_wiki='GATED',r79='PAUSED_NON_BLOCKING'),'Boundary changed')
    require(r['next']=='OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-25','Return to portfolio')


def replay(r,payloads):
    validate(r)
    require(len(payloads)==2,'Two fixed HTML required')
    got=[extract(b) for b in payloads]
    require(got==[s['extracted'] for s in r['inputs']], 'Source guide core/facts changed')
    h=r['inputs'][1]['http']
    require(len(payloads[1])==h['bytes'] and sha256(payloads[1]).hexdigest()==h['sha256'],'Wrong historical bytes; current page not substitute')
    return dict(schema='stoneage.pirate_relic_guide.replay.r1',inputs=[dict(source_id=s['id'],bytes=len(b),sha256=sha256(b).hexdigest()) for s,b in zip(r['inputs'],payloads)],guide=got[0],historical_capture_timestamp='20031204053709',historical_guide_matches=True,raw_html_or_images_in_output=False,original_server_execution_verified=False)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--fetch',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    require(a.fetch!=bool(a.source_dir),'Choose fixed fetch or supplied transient HTML')
    payloads=[]
    for url,name in zip(URLS,('pirate.html','pirate-era.html')):
        if a.fetch:
            with urllib.request.urlopen(url,timeout=45) as response:
                require(response.status==200 and response.url==url,'Unexpected HTTP/redirect')
                b=response.read(2_000_001);require(len(b)<=2_000_000,'Oversized source')
        else:b=(a.source_dir/name).read_bytes()
        payloads.append(b)
    result=replay(json.loads(REPORT.read_text()),payloads);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('DATED_PLAYER_GUIDE_VERIFIED=1 HISTORICAL_HTML_VERIFIED=1 IMAGES_FETCHED=0 ORIGINAL_SERVER_EXECUTIONS=0')


if __name__=='__main__':main()
