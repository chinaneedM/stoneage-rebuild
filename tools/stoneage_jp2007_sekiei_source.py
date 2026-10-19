"""Replay an attributed release, its 2007 capture and a 2008 operator-host capture.

Outputs contain derived source metadata only, never original HTML or images.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import urllib.request

from tools.stoneage_jp2008_shadow_release import compact, require
from tools.stoneage_cn2003_christmas_source import jpeg_dimensions

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-JP2007-SEKIEI-WORLD-EVENT-SOURCE-R1.json'
URLS = (
    'https://www.4gamer.net/games/013/G001377/20071120003/',
    'https://web.archive.org/web/20071223094402id_/http://www.4gamer.net:80/games/013/G001377/20071120003/',
    'https://web.archive.org/web/20080220173517id_/http://stoneage.to:80/update/20071120_update_08_sekiei.html',
    'https://www.4gamer.net/games/013/G001377/20071120003/TN/001.jpg',
)
NAMES = ('sekiei.html', 'sekiei-press-era.html', 'sekiei-official-era.html', 'sekiei-reference.jpg')
OFFICIAL_LINK = 'http://stoneage.to/update/20071120_update_08_sekiei.html'


def extract(payload, kind):
    require(kind in ('current_press', 'early_press', 'operator_capture'), 'Unknown source role')
    text = compact(payload.decode('euc_jp' if kind == 'early_press' else 'utf-8-sig'))
    if kind != 'operator_capture':
        marker = 'メーカー発表文の内容をそのまま掲載しています'
        require(text.count(marker) == 1, 'Missing/ambiguous publisher release boundary')
        text = text.split(marker)[1]
        require(text.startswith('＞株式会社デジパーク') or text.startswith('株式会社デジパーク'), 'Operator issuer missing inside release')
        require('2007年11月20日' in text and OFFICIAL_LINK in payload.decode('euc_jp' if kind == 'early_press' else 'utf-8-sig'), 'Date or actual operator link missing')
        require('数種類のペットの中からランダムでペットが1匹手に入る有料チケット' in text, 'Separate campaign description missing')
    else:
        require('赤影の迷宮[2007/11/20-アップデート]' in text, 'Operator page update label missing')
        require('画面写真は開発中のものです。実際とは異なる場合があります' in text, 'Development screenshot disclaimer missing')
    start, end = '◆赤影の角獣伝説', 'ニースの狩猟団員となり迷宮に挑め！'
    require(text.count(start) == text.count(end) == 1, 'Ambiguous narrative core')
    core = text[text.index(start):text.index(end) + len(end)]
    beast = re.search(r'「([^「」]+)」という怪物', core)
    souls = re.search(r'「精霊王」は、[^。]+「([^「」]+)」と「([^「」]+)」の分け、?2つの壷に封じ込めた', core)
    islands = re.search(r'「([^「」]+島)」「([^「」]+島)」「([^「」]+島)」を結ぶ海底洞窟内に亀裂が入り', core)
    require(beast and souls and islands, 'Named legend, soul split or island relationship missing')
    for clause in ('互いに干渉し合い封印の均衡を保った', '世界の海底火山が噴火し、大きな地震が起きた',
                   '2つの魂の壺は地底の迷宮へおさめられ',
                   '早々に狩猟団が組まれ', '唯一戻ってきた狩猟団員',
                   '魂の壺が眠っていると噂される洞窟', '海底火山の噴火により海底洞窟内に入り口が出現した'):
        require(clause in core, 'Material narrative clause missing: ' + clause)
    require(re.search(r'多くは、二度と洞窟から出てくることは(?:な|無)かった', core), 'Expedition disappearance statement missing')
    return dict(core_sha256=sha256(core.encode()).hexdigest(), core_utf8_bytes=len(core.encode()), facts=dict(
        beast_as_written=beast[1], sealing_actor_as_written='精霊王', soul_labels=list(souls.groups()),
        vessels_reported=2, seal_balance_reported=True, vessel_location_claim='UNDERGROUND_LABYRINTH_AS_LEGEND',
        islands_connected_by_source_seabed_passage=list(islands.groups()),
        eruption_to_earthquake_to_fissure_reported=True, expedition_formed=True,
        many_expedition_members_did_not_return_reported=True, unique_returnee_reported=True,
        dungeon_entry_cause='SEABED_VOLCANIC_ERUPTION', vessel_presence_in_current_dungeon='RUMORED_NOT_CONFIRMED',
        invitation_role='JOIN_NIIS_HUNTING_EXPEDITION', ending_and_vessel_recovery=None))


def validate(r):
    require(r['schema'] == 'stoneage.jp2007_sekiei_world_event.source.r1', 'Unknown schema')
    require([s['http']['url'] for s in r['inputs']] == list(URLS), 'Finite source list changed')
    require(r['inputs'][0]['authority'] == 'DIGIPARK_RELEASE_EXPLICITLY_REPUBLISHED_BY_4GAMER', 'Issuer authority changed')
    require(r['inputs'][2]['authority'] == 'CAPTURE_OF_RELEASE_LINKED_OPERATOR_HOST_PAGE', 'Operator host evidence lost')
    facts = [s['extracted']['facts'] for s in r['inputs'][:3]]
    require(facts[0] == facts[1] == facts[2], 'Cross-representation semantic mismatch')
    require(r['inputs'][0]['extracted'] == r['inputs'][1]['extracted'], 'Current/early press core mismatch')
    require(r['inputs'][0]['extracted']['core_sha256'] != r['inputs'][2]['extracted']['core_sha256'], 'Operator wording differences flattened')
    require(len(r['records']) == 8, 'Eight bounded research records expected')
    required = {'record_id', 'entity_type', 'version_profile', 'source_refs', 'verification_status', 'rights_status', 'record_revision'}
    for row in r['records']:
        require(required <= row.keys() and row['game_ids'] is None, 'Original IDs/contract changed')
        require(row['rights_status'] == 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED', 'Asset rights promoted')
        require(row['verification_status'] in ('OPERATOR_SOURCE_REPORTED_NOT_RUNTIME', 'MANUAL_IMAGE_REFERENCE_NOT_MAP_OR_SPRITE'), 'Evidence promotion')
    require(r['records'][0]['source_facts'] == facts[0], 'World narrative detached from evidence')
    require(r['records'][1]['final_map_ids'] is None and r['records'][1]['spawn_coordinates'] is None, 'Original map data invented')
    require(r['records'][3]['light_or_dark_king_identity'] is None, 'Unqualified spirit king joined to other versions')
    require(r['records'][4]['species_id'] is None and r['records'][4]['stats'] is None, 'Mythic beast promoted to species master')
    require(r['records'][5]['reward'] is None and r['records'][5]['minimum_level'] is None and r['records'][5]['script'] is None, 'Quest reward/eligibility/script invented')
    require(r['records'][7]['dimensions'] == [410, 410] and r['records'][7]['original_sprite_binding'] is None, 'Screenshot promoted to client binding')
    require(r['boundaries'] == dict(operator_page_capture_recovered=True, early_media_capture_recovered=True,
        original_server_execution_verified=False, exact_client_build=None, original_map_or_npc_master_recovered=False,
        historic_image_bytes_verified=False, current_press_image_is_operator_image_byte_match=False,
        two_host_representations_are_independent_factual_witnesses=False, unqualified_spirit_king_is_cn_light_or_dark_king=False,
        commercial_ticket_is_quest_reward=False, future_or_rumored_treasure_is_recovered_reward=False,
        production_screenshot_or_original_sprite_verified=False, raw_html_or_assets_committed=False,
        tw10_or_jss1999_backfill=False, stage_a='7_PARTIAL_2_OPEN', stage_b_and_wiki='GATED', r79='PAUSED_NON_BLOCKING'), 'Boundary changed')
    require(r['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-26', 'Portfolio return required')


def replay(r, payloads):
    validate(r)
    require(len(payloads) == 4, 'Three fixed HTML representations and one linked image required')
    extracted = [extract(b, kind) for b, kind in zip(payloads, ('current_press', 'early_press', 'operator_capture'))]
    require(extracted == [s['extracted'] for s in r['inputs'][:3]], 'Narrative core or derived facts changed')
    for i in (1, 2, 3):
        h, b = r['inputs'][i]['http'], payloads[i]
        require(len(b) == h['bytes'] and sha256(b).hexdigest() == h['sha256'], 'Historical/image byte pin changed; substitution forbidden')
    require(jpeg_dimensions(payloads[3]) == [410, 410], 'Actual image dimensions changed')
    require('/games/013/G001377/20071120003/TN/001.jpg' in payloads[0].decode(), 'Actual image link missing')
    return dict(schema='stoneage.jp2007_sekiei_world_event.replay.r1',
        inputs=[dict(source_id=s['id'], bytes=len(b), sha256=sha256(b).hexdigest()) for s,b in zip(r['inputs'],payloads)],
        extracted=extracted, press_core_matches_2007_capture=True, operator_semantics_match_media=True,
        operator_wording_preserved_separately=True, image_dimensions=[410,410],
        original_server_or_historical_image_verified=False, raw_html_or_images_in_output=False)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--fetch',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();require(a.fetch != bool(a.source_dir), 'Choose fixed URL fetch or supplied transient files')
    payloads=[]
    for url,name in zip(URLS,NAMES):
        if a.fetch:
            with urllib.request.urlopen(url,timeout=45) as response:
                require(response.status==200 and response.url==url, 'Unexpected HTTP/redirect')
                b=response.read(2_000_001);require(len(b)<=2_000_000, 'Oversized source')
        else:b=(a.source_dir/name).read_bytes()
        payloads.append(b)
    result=replay(json.loads(REPORT.read_text()),payloads)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('OPERATOR_CAPTURE_VERIFIED=1 EARLY_PRESS_CAPTURE_VERIFIED=1 NARRATIVE_REPRESENTATIONS=3 IMAGE_REFERENCES_VERIFIED=1 ORIGINAL_SERVER_EXECUTIONS=0')


if __name__=='__main__':main()
