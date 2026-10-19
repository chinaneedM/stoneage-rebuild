"""One operator sequel: adult/riding framing, ore-work lead and social anecdote."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from tools.stoneage_early_content_probe import plain, require
from tools.stoneage_wayi_newbie_riding_plan import INDEX_URL, INDEX_SHA, index_rows, fetch

ORIGINAL = 'http://www.wayi.com.tw/stoneage/producer/producer02.asp?idno=67'
CAPTURE = '20051113145307'
URL = 'https://web.archive.org/web/' + CAPTURE + 'id_/' + ORIGINAL
SOURCE_SHA = 'caf0ab5a51a87d0ddd6f3f6aea4be77cde4dbaed80b1c6e900f4946da703bea2'
PLAN = Path('research/recovered/STONEAGE-WAYI2003-NEWBIE-RIDING-PLAN-R1.json')
PLAN_SHA = 'b23c0220c58840ddb14ee9eea835687924cc16b42afe091af127f67472580fcd'
REPORT = Path('research/recovered/STONEAGE-WAYI2003-RIDING-SUCCESSOR-ORE-WORK-R1.json')
PINS = [(85, 'ec5bd4d4b920ef81ae2b1576ace0f7b6b0ae616a29c1f8be81e15babffa52cc7'),
        (45, 'dbce1ea6020fe5db877df09565d0a294b96cb4481eec61817eed91e17d453238'),
        (70, 'b258cce560bd7f51e577992392bdfa765b18ec2551fcbf9331f5a2d3b2d36ec7'),
        (22, '3002162fd6358fbe8fd35f227fd7a6bc387c4685863dd44f53bcc2c2c155a7e4')]


def paragraphs(doc):
    matches = re.findall(r'<span\b[^>]*>\s*(接上一篇.*?)</span>', doc, re.I | re.S)
    require(len(matches) == 1, 'One actual successor article body required')
    return [plain(p) for p in re.split(r'\r?\n\s*\r?\n', matches[0]) if plain(p)]


def validate_report(o):
    require(len(o['records']) == 3, 'Three successor source records required')
    b = [r['source_described_claims'] for r in o['records']]
    require(b[0]['adult_rite_completed_and_mounted_as_narrative_start'] is True
            and b[0]['specific_free_tiger_plan_implementation_or_stats_confirmed'] is False,
            'Narrative transition promoted to implemented gift plan')
    require(b[1]['role_label_as_written'] == '礦石研究者' and b[1]['settlement_as_written'] == '漁村'
            and b[1]['ore_location_as_written'] == '柯奧山' and b[1]['material_as_written'] == '奇怪礦石'
            and b[1]['personal_npc_name_ids_map_coordinates_or_reward'] is None
            and b[1]['fishing_village_equals_named_other_village_proven'] is False,
            'Ore work role or generic fishing village promoted to canonical entity/reward')
    require(b[1]['same_job_as_previous_mammoth_courier'] is False
            and b[1]['previous_thirty_level_claim_transferred_to_ore_job'] is False,
            'Previous courier reward projected onto different ore job')
    require(b[2]['setting_as_written'] == '石器博物館'
            and b[2]['narrator_anecdote_not_official_world_quest_script'] is True
            and b[2]['staff_account_identity_or_universal_museum_pvp_rule_proven'] is False,
            'Narrator anecdote promoted to staff identity or universal PvP rule')
    require(o['comparison_to_previous_plan']['same_author_series_is_independent_implementation_confirmation'] is False
            and o['comparison_to_previous_plan']['gift_species_level_loyalty_or_delivery_implemented_proven'] is False,
            'Related articles promoted to independent implementation witnesses')
    for r in o['records']:
        require(r['actual_server_script_or_execution_verified'] is False
                and r['original_game_ids_or_same_build_binding'] is None, 'Source story promoted to server implementation')


def build(index, index_final, body, final, plan_raw):
    require(index_final == INDEX_URL and final == URL, 'Exact index/successor originals and captures required')
    require(len(index) == 28883 and sha256(index).hexdigest() == INDEX_SHA, 'Index byte pin differs')
    require(len(body) == 19686 and sha256(body).hexdigest() == SOURCE_SHA, 'Successor byte pin differs')
    require(sha256(plan_raw).hexdigest() == PLAN_SHA, 'Previous plan report byte pin differs')
    plan = json.loads(plan_raw); require(plan['records'][2]['source_described_claims']['status'] == 'OPERATOR_STATED_PLAN', 'Prior plan status changed')
    selected = next(r for r in index_rows(index.decode('big5', errors='strict')) if r['article_id_as_web_key'] == 67)
    require(selected['title'] == '新手騎寵計劃（續）' and selected['index_date_as_written'] == '2003-12-23', 'Actual successor title/date missing')
    ps = paragraphs(body.decode('big5', errors='strict'))
    require([(len(p), sha256(p.encode()).hexdigest()) for p in ps] == PINS, 'Successor paragraphs differ')
    require(all(x in ps[0] for x in ['接上一篇', '完成成人禮', '騎上寵物', '漁村', '礦石研究者', '柯奧山', '奇怪礦石']), 'Adult/riding/ore lead missing')
    require('石器博物館' in ps[1] and '酷哥贏了這場ＰＫ' in ps[2], 'Anecdote context missing')
    claims = [
        {'topic': 'SUCCESSOR_NARRATIVE_AFTER_RITE_AND_RIDING', 'paragraphs': [0],
         'adult_rite_completed_and_mounted_as_narrative_start': True,
         'specific_free_tiger_plan_implementation_or_stats_confirmed': False},
        {'topic': 'ORE_RESEARCHER_COLLECTION_WORK_LEAD', 'paragraphs': [0],
         'role_label_as_written': '礦石研究者', 'settlement_as_written': '漁村',
         'ore_location_as_written': '柯奧山', 'material_as_written': '奇怪礦石',
         'source_relation': 'RESEARCHER_IN_SOURCE_SETTLEMENT_SEEKS_HELP_COLLECTING_SOURCE_MATERIAL_AT_SOURCE_MOUNTAIN',
         'personal_npc_name_ids_map_coordinates_or_reward': None,
         'fishing_village_equals_named_other_village_proven': False,
         'same_job_as_previous_mammoth_courier': False,
         'previous_thirty_level_claim_transferred_to_ore_job': False},
        {'topic': 'MUSEUM_SOCIAL_NARRATOR_ANECDOTE', 'paragraphs': [1, 2],
         'setting_as_written': '石器博物館',
         'narrator_anecdote_not_official_world_quest_script': True,
         'staff_account_identity_or_universal_museum_pvp_rule_proven': False},
    ]
    records = []
    for i, c in enumerate(claims):
        records.append({'record_id': f'wayi-column2003:riding-successor:{i+1:02d}',
                        'collection': 'quests' if i == 1 else 'tutorials' if i == 0 else 'sources',
                        'entity_type': 'OFFICIAL_OPERATOR_WORK_LEAD' if i == 1 else 'OFFICIAL_COLUMN_NARRATIVE_CONTEXT',
                        'record_revision': 1, 'version_profile': 'TW_WAYI_2003_DATED_COLUMN_PRESERVED_2005_NOT_EXACT_BUILD',
                        'source_refs': [{'source': ORIGINAL, 'actual_capture': CAPTURE, 'sha256': SOURCE_SHA,
                                         'index_date_as_written': '2003-12-23', 'paragraph_indices': c['paragraphs'],
                                         'normalized_paragraph_sha256': [PINS[n][1] for n in c['paragraphs']]}],
                        'verification_status': 'OPERATOR_NARRATIVE_AND_WORK_LEAD_NOT_ORIGINAL_SCRIPT',
                        'rights_status': 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED', 'source_described_claims': c,
                        'actual_server_script_or_execution_verified': False, 'original_game_ids_or_same_build_binding': None})
    o = {'schema': 'stoneage.wayi2003.riding_successor_ore_work.r1', 'date': '2026-10-19',
         'task': 'TW-WAYI-NEWBIE-RIDING-SUCCESSOR-GATE-01',
         'source': {'original_url': ORIGINAL, 'strict_replay_url': URL, 'actual_capture': CAPTURE, 'bytes': len(body),
                    'sha256': SOURCE_SHA, 'encoding': 'BIG5_STRICT', 'index_date_as_written': '2003-12-23',
                    'index_date_is_original_release_or_deployment_proven': False,
                    'index': {'strict_replay_url': INDEX_URL, 'sha256': INDEX_SHA, 'actual_capture': '20050612011406'}},
         'previous_plan_report': {'path': str(PLAN), 'sha256': PLAN_SHA},
         'paragraph_fingerprints': [{'index': i, 'normalized_characters': n, 'sha256': h} for i, (n, h) in enumerate(PINS)],
         'records': records,
         'comparison_to_previous_plan': {'shared_series_linkage_described': True,
                                        'same_author_series_is_independent_implementation_confirmation': False,
                                        'gift_species_level_loyalty_or_delivery_implemented_proven': False,
                                        'courier_and_ore_roles_are_distinct_source_contexts': True},
         'unacquired_image_refs': ['http://www.wayi.com.tw/images02/sa1220-1.jpg', 'http://www.wayi.com.tw/images02/sa1220-2.jpg'],
         'coverage': {'selected_successor_article': 1, 'known_index_reacquired': 1, 'prior_derived_report_pinned': 1,
                      'source_records': 3, 'source_qualified_ore_work_leads': 1, 'images_programs_or_original_entity_ids': 0},
         'boundaries': {'jss1999_tw10_cn182_same_build_or_original_server_recovered': False,
                        'original_html_or_assets_in_git': False, 'stage_a': '7_PARTIAL_2_OPEN',
                        'stage_b_and_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'},
         'next': 'OFFICIAL-VERSION-MATERIAL-COVERAGE-REVIEW-12'}
    validate_report(o)
    return o


def main():
    p = argparse.ArgumentParser(); p.add_argument('--input-index'); p.add_argument('--input-body'); p.add_argument('--output', required=True); a = p.parse_args()
    require(bool(a.input_index) == bool(a.input_body), 'Both local source objects or neither required')
    index, index_final = (Path(a.input_index).read_bytes(), INDEX_URL) if a.input_index else fetch(INDEX_URL)
    body, final = (Path(a.input_body).read_bytes(), URL) if a.input_body else fetch(URL)
    o = build(index, index_final, body, final, PLAN.read_bytes()); payload = json.dumps(o, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    out = Path(a.output); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(payload, encoding='utf-8')
    print('SUCCESSOR_SHA256=' + SOURCE_SHA); print('SOURCE_RECORDS=3 ORE_WORK_LEADS=1 IMAGES_OR_RUNTIME=0')
    print('DERIVED_SHA256=' + sha256(payload.encode()).hexdigest())


if __name__ == '__main__': main()
