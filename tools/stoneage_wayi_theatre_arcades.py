"""One operator description of three entertainment loops; no runtime or shared-wallet claim."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
from urllib.error import HTTPError,URLError
from urllib.request import Request,urlopen
from tools.stoneage_wayi_intro_detail02_probe import Visible

ORIGINAL='http://www.wayi.com.tw/stoneage/game/game01_04.asp'
FINAL='https://web.archive.org/web/20050614011214id_/'+ORIGINAL
CAPTURE='20050614011214'
SOURCE_SHA='afaae72abf0ca60939c7e57a824cc556f0e24a2d8add77eff7f18caacb942a50'
REPORT=Path('research/recovered/STONEAGE-WAYI-THEATRE-ARCADES-R1.json')
ANCHORS=['劇場','魔法牌遊樂場','寵物轉轉輪遊樂場','公關新聞']
PINS=[(63,'0c11069d681365cf54ad2f07726b3b5c4095d8b7500f25629cfd5b7f22991021'),(47,'179bfbe851c0405f389c182f0c0c35afaf1479e95cf0172b1ce1419e73cf71de'),(55,'16de1a381ec8e5735a9b39e760295289bfcb5ac9c016cb671c9fef05e4531a3a')]


def require(v,m):
    if not v:raise ValueError(m)


def sections(pieces):
    positions=[]
    for anchor in ANCHORS:
        found=[i for i,s in enumerate(pieces) if ''.join(s.split())==anchor]
        require(len(found)==1,'Missing or duplicate source section anchor')
        positions.append(found[0])
    require(positions==sorted(positions),'Entertainment sections reordered')
    fingerprints=[]
    for a,b in zip(positions,positions[1:]):
        s=''.join(''.join(pieces[a:b]).split());fingerprints.append((len(s),sha256(s.encode()).hexdigest()))
    require(fingerprints==PINS,'Entertainment section content differs')
    return [{'normalized_characters':n,'sha256':h} for n,h in fingerprints]


def validate_contract(o):
    rs=o['records'];require(len(rs)==3,'Expected three source-described venues')
    theatre,card,wheel=rs
    require(theatre['points_label_as_written']=='藝術值' and theatre['rewards_mentioned']==['SPECIAL_ITEMS_UNIDENTIFIED'],'Theatre points/reward attribution changed')
    require(theatre['performance_examples_not_quest_catalog']==['小紅帽','白雪公主'],'Promotional play examples changed')
    require(card['points_label_as_written']==wheel['points_label_as_written']=='積分','Arcade point label differs')
    require(card['source_described_loop']==['REGISTER_CHALLENGE','DEFEAT_UNNAMED_BOSS','OBTAIN_POINTS','ACCUMULATE_AND_REDEEM'],'Card challenge is not a source-qualified boss/points loop')
    require(wheel['source_described_loop']==['PURCHASE_TICKET','PLACE_WAGER','POINTS_DESCRIBED_ACCORDING_TO_STATED_ODDS','ACCUMULATE_AND_REDEEM'],'Wheel ticket/wager/points loop changed')
    require(card['rewards_mentioned']==wheel['rewards_mentioned']==['SPECIAL_ITEMS_UNIDENTIFIED','PETS_UNIDENTIFIED'],'Arcade reward classes changed')
    for r in rs:
        require(r['point_wallet_id_and_cross_venue_sharing'] is None,'Shared point wallet invented')
        require(r['prices_odds_point_rates_eligibility_and_actual_transaction'] is None,'Invented numeric or runtime rule')
        require(r['map_npc_pet_item_skill_ids'] is None and r['cross_region_aliases'] is None,'Invented entity IDs/aliases')
        require(r['server_runtime_observed'] is False and r['rights_status']!='RELEASE_APPROVED','Runtime or rights promoted')
    require(o['boundaries']['unnamed_boss_is_earlier_named_worldline_antagonist'] is False,'Generic boss silently identified')
    require(o['boundaries']['theatre_fairytales_are_original_world_history_or_recovered_scripts'] is False,'Promotional theatre examples promoted to canon/scripts')


def build(raw,final):
    require(final==FINAL,'Wayi detail host/path/capture mismatch')
    require(len(raw)==21308 and sha256(raw).hexdigest()==SOURCE_SHA,'Wayi detail byte pin mismatch')
    v=Visible();v.feed(raw.decode('big5',errors='strict'))
    require(v.title==['石器時代--精靈的召喚'],'Unexpected site title')
    require(sum(''.join(x.split())=='劇場與賭場功能' for x in v.pieces)==1,'Actual entertainment topic missing')
    fingerprints=sections(v.pieces)
    names=['伊甸劇場','魔法牌遊樂場','寵物轉轉輪遊樂場']
    loops=[['REGISTER_PERFORMANCE','ART_VALUE_DESCRIBED_ACCORDING_TO_PERFORMANCE','ACCUMULATE_AND_REDEEM'],['REGISTER_CHALLENGE','DEFEAT_UNNAMED_BOSS','OBTAIN_POINTS','ACCUMULATE_AND_REDEEM'],['PURCHASE_TICKET','PLACE_WAGER','POINTS_DESCRIBED_ACCORDING_TO_STATED_ODDS','ACCUMULATE_AND_REDEEM']]
    rs=[]
    for i,name in enumerate(names):
        rs.append({'record_id':f'wayi2005-entertainment:web-section:{i+1:02d}','collection':'maps',
            'entity_type':'OPERATOR_DESCRIBED_VENUE_AND_POINT_LOOP_NOT_CLIENT_MAP_PAYLOAD','record_revision':1,
            'version_profile':'TAIWAN_WAYI_WEB_20050614_BODY_LABEL_80','source_refs':[{'source':ORIGINAL,'actual_capture':CAPTURE,'sha256':SOURCE_SHA,'evidence_role':'NAMED_OPERATOR_SECTION_AND_PARAPHRASED_LOOP','section_fingerprint':fingerprints[i]}],
            'verification_status':'SOURCE_DESCRIBED_ENTERTAINMENT_NOT_DEPLOYMENT_OR_TRANSACTION','rights_status':'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
            'name_as_written':name,'section_heading_as_written':ANCHORS[i],'points_label_as_written':'藝術值' if i==0 else '積分',
            'source_described_loop':loops[i],'rewards_mentioned':['SPECIAL_ITEMS_UNIDENTIFIED'] if i==0 else ['SPECIAL_ITEMS_UNIDENTIFIED','PETS_UNIDENTIFIED'],
            'other_unmentioned_rewards_remain_unknown':True,'performance_examples_not_quest_catalog':['小紅帽','白雪公主'] if i==0 else [],
            'point_wallet_id_and_cross_venue_sharing':None,'prices_odds_point_rates_eligibility_and_actual_transaction':None,
            'map_npc_pet_item_skill_ids':None,'cross_region_aliases':None,'server_runtime_observed':False})
    o={'schema':'stoneage.wayi.theatre_arcades.r1','date':'2026-10-19','task':'TW-WAYI-OFFICIAL-INTRO-DETAIL-04',
       'source':{'operator':'WAYI_TAIWAN','original_url':ORIGINAL,'requested_discovery_url':'https://web.archive.org/web/20050614002509id_/'+ORIGINAL,
           'strict_replay_url':final,'actual_capture':CAPTURE,'sha256':SOURCE_SHA,'bytes':len(raw),'encoding':'BIG5_STRICT',
           'parent_report':'research/recovered/STONEAGE-WAYI-OFFICIAL-WORLDLINE-R1.json','parent_detail_index':3,
           'parent_body_sha256':'c0a2f96c1d0232eb3f94328481ff512c3efed63daeab912fcc5dd0c397f1ba0d',
           'site_title_as_written':'石器時代--精靈的召喚','actual_body_version_label':'8.0','site_title_is_exact_client_build':False,
           'capture_is_publication_or_actual_deployment_date':False,'excluded_account_form_poll_and_corporate_footer':True},
       'records':rs,'coverage':{'named_venue_descriptions':3,'new_images_or_programs_acquired':0,'original_server_loops_executed':0},
       'boundaries':{'same_word_points_proves_shared_arcade_wallet':False,'theatre_art_value_equals_arcade_points':False,
           'theatre_fairytales_are_original_world_history_or_recovered_scripts':False,'unnamed_boss_is_earlier_named_worldline_antagonist':False,
           'ticket_odds_prize_ids_guaranteed_profit_or_draw_algorithm_recovered':False,'same_region_or_cross_region_exact_build_identity_proven':False,
           'original_html_images_or_programs_in_git':False,'stage_a_families':'7_PARTIAL_2_OPEN','stage_b_and_wiki':'GATED','r79':'PAUSED_NON_BLOCKING'},
       'next':'OFFICIAL-VERSION-COVERAGE-MATERIAL-REVIEW-08'}
    validate_contract(o);return o


def acquire():
    for attempt in range(2):
        try:
            with urlopen(Request(FINAL,headers={'User-Agent':'Mozilla/5.0 StoneAgeHistoricalEvidence'}),timeout=35) as r:return r.read(300001),r.url
        except HTTPError as e:
            if attempt or e.code not in (502,503,504):raise
            print('BOUNDED_RETRY_HTTP='+str(e.code),flush=True)
        except (URLError,TimeoutError) as e:
            if attempt:raise
            print('BOUNDED_RETRY_NETWORK='+type(e).__name__,flush=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input');ap.add_argument('--output',required=True);a=ap.parse_args()
    raw,final=(Path(a.input).read_bytes(),FINAL) if a.input else acquire();o=build(raw,final)
    payload=json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n';out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(payload,encoding='utf-8')
    print('VENUE_DESCRIPTIONS=3');print('PAGE_SHA256='+SOURCE_SHA);print('DERIVED_SHA256='+sha256(payload.encode()).hexdigest())


if __name__=='__main__':main()
