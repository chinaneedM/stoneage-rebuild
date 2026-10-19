"""Operator's dated newbie-riding plan, not a recovered original server rule."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen
from tools.stoneage_early_content_probe import plain, require

ROOT = 'http://www.wayi.com.tw/stoneage/producer/'
INDEX_ORIGINAL = ROOT + 'producer01.asp'
INDEX_CAPTURE = '20050612011406'
INDEX_URL = 'https://web.archive.org/web/' + INDEX_CAPTURE + 'id_/' + INDEX_ORIGINAL
INDEX_SHA = '19661e2acca046bf8c6dc86dc968107fe9935cd58a8f3cd8ce5e1de5aeba7f8b'
ORIGINAL = ROOT + 'producer02.asp?idno=66'
CAPTURE = '20051117143741'
URL = 'https://web.archive.org/web/' + CAPTURE + 'id_/' + ORIGINAL
SOURCE_SHA = 'b1f2163b80137e2140c36a6675a42e4ac1f2e3cc367e08b2a850cd15a6261790'
REPORT = Path('research/recovered/STONEAGE-WAYI2003-NEWBIE-RIDING-PLAN-R1.json')
PINS = [(14, 'e62de92b87e5f90dda54bf34ef1dfc83c6da57d4e1c171262b0c3d1f34107734'),
        (72, '4b20784a8ec41a01e3a8d220a3fefa45049810b1176e5a7cf5f72c8bc76fc943'),
        (77, 'd9dce47b135a1167caaf8a302f01015e2883f5f9fb137a66c8416c695069fdf3'),
        (96, '11436bbfec51c8b482c945f2f44b10a0df5d6ecfe1304b341c43ffca0feb88c4'),
        (79, '2b11df04002dda9e3e8951c232ee08302777312786232616aee9d9f67aae8e84'),
        (15, '040350f2d6551a430e036644e3ab0a91247afb2bc45396ce665e8b7bf7466fde')]


def index_rows(doc):
    rows = []
    for row in re.findall(r'<tr\b[^>]*>((?:(?!<tr\b).)*?)</tr>', doc, re.I | re.S):
        link = re.search(r'''<a\b[^>]*href=["']producer02\.asp\?idno=(\d+)["'][^>]*>(.*?)</a>''', row, re.I | re.S)
        if not link: continue
        dates = re.findall(r'(?<!\d)\d{4}-\d{1,2}-\d{1,2}(?!\d)', plain(row))
        require(len(dates) == 1, 'Column title/date must bind in one row')
        rows.append({'article_id_as_web_key': int(link.group(1)), 'title': plain(link.group(2)), 'index_date_as_written': dates[0]})
    require(len(rows) == 15, 'Exact fifteen column entries required')
    return rows


def paragraphs(doc):
    matches = re.findall(r'<span\b[^>]*>\s*(現在的石器是從騎寵開始玩的。.*?)</span>', doc, re.I | re.S)
    require(len(matches) == 1, 'One actual riding article body required')
    return [plain(p) for p in re.split(r'\r?\n\s*\r?\n', matches[0]) if plain(p)]


def validate_report(o):
    require(len(o['records']) == 5, 'Five source descriptions required')
    b = [r['source_described_claims'] for r in o['records']]
    require(b[1]['tiger_relative_acquisition_ease_as_written'] == [['黃虎', '綠虎'], ['紅虎'], ['金虎']]
            and b[1]['easier_thunder_label_as_written'] == '紅雷'
            and b[1]['species_ids_capture_rates_or_maps'] is None, 'Relative labels promoted to original roster or probability')
    require(b[2]['status'] == 'OPERATOR_STATED_PLAN'
            and b[2]['planned_tigers_per_newbie'] == 1
            and b[2]['protect_normal_quest_pet_value_as_stated_motive'] is True
            and b[2]['stat_loyalty_deltas_or_compatibility_matrix'] is None, 'Planned gift promoted to implemented numeric reward')
    require(b[3]['after_adulthood_rite_as_planned'] is True
            and b[3]['required_level_npc_or_quest_ids'] is None, 'Adulthood condition given invented level or quest IDs')
    require(b[4]['source_claimed_level_increase'] == 30 and b[4]['destination_level_is_30_proven'] is False
            and b[4]['caption_one_sexagenary_cycle_is_60_level_reward'] is False
            and b[4]['actual_award_cap_task_count_or_transaction'] is None, 'Thirty-level claim or metaphor misinterpreted')
    for r in o['records']:
        require(r['actual_server_rule_or_execution_verified'] is False
                and r['original_game_ids_or_same_build_binding'] is None, 'Operator prose promoted to server rule or original build')
    require(o['source']['index_date_is_original_body_release_or_deployment_proven'] is False,
            '2003 index date promoted to verified original release or deployment')


def build(index, index_final, body, final):
    require(index_final == INDEX_URL and final == URL, 'Exact index/detail original URL and captures required')
    require(len(index) == 28883 and sha256(index).hexdigest() == INDEX_SHA, 'Column index byte pin differs')
    require(len(body) == 19964 and sha256(body).hexdigest() == SOURCE_SHA, 'Riding article byte pin differs')
    rows = index_rows(index.decode('big5', errors='strict'))
    selected = next((r for r in rows if r['article_id_as_web_key'] == 66), None)
    require(selected == {'article_id_as_web_key': 66, 'title': '新手騎寵計劃', 'index_date_as_written': '2003-12-10'}, 'Selected title/date/actual link differs')
    follow = next(r for r in rows if r['article_id_as_web_key'] == 67)
    require(follow['title'] == '新手騎寵計劃（續）' and follow['index_date_as_written'] == '2003-12-23', 'Real successor link qualification differs')
    doc = body.decode('big5', errors='strict'); ps = paragraphs(doc)
    require([(len(p), sha256(p.encode()).hexdigest()) for p in ps] == PINS, 'Article paragraph fingerprints differ')
    require(all(x in ps[3] for x in ['酷哥的打算', '適合他所騎乘', '能力會稍弱', '忠誠度會很容易', '正常任務寵的價值', '解完成人禮']), 'Gift plan qualification missing')
    require(all(x in ps[4] for x in ['長毛象快遞', '老闆', '完成老闆交付的任務', '等級連跳三十級']), 'Task/level claim missing')
    claims = [
        {'topic': 'NEWBIE_RIDING_FRICTION', 'paragraphs': [0, 1],
         'speaker_as_written': '酷哥', 'newbie_riding_as_first_barrier_is_operator_framing': True,
         'riding_present_in_jss1999_or_tw10_from_this_text_proven': False},
        {'topic': 'QUALITATIVE_ACQUISITION_AND_LOYALTY', 'paragraphs': [2],
         'basic_mount_groups_as_written': ['老虎', '雷龍'],
         'tiger_relative_acquisition_ease_as_written': [['黃虎', '綠虎'], ['紅虎'], ['金虎']],
         'easier_thunder_label_as_written': '紅雷', 'rare_pet_loyalty_hard_to_raise_as_source_judgment': True,
         'species_ids_capture_rates_or_maps': None},
        {'topic': 'PLANNED_ACCESSIBLE_MOUNT_AND_QUEST_VALUE', 'paragraphs': [3],
         'status': 'OPERATOR_STATED_PLAN', 'planned_tigers_per_newbie': 1,
         'suited_to_player_riding_described_not_all_characters_all_tigers': True,
         'weaker_ability_and_easier_loyalty_described': True,
         'protect_normal_quest_pet_value_as_stated_motive': True,
         'stat_loyalty_deltas_or_compatibility_matrix': None},
        {'topic': 'PLANNED_GIFT_AFTER_ADULTHOOD_RITE', 'paragraphs': [3],
         'after_adulthood_rite_as_planned': True, 'implemented_delivery_proven': False,
         'required_level_npc_or_quest_ids': None},
        {'topic': 'MAMMOTH_COURIER_BOSS_TASK_LEVEL_CLAIM', 'paragraphs': [4, 5],
         'boss_is_named_individual': False, 'source_claimed_level_increase': 30,
         'destination_level_is_30_proven': False,
         'caption_one_sexagenary_cycle_is_60_level_reward': False,
         'actual_award_cap_task_count_or_transaction': None},
    ]
    records = []
    for i, c in enumerate(claims):
        records.append({'record_id': f'wayi-column2003:newbie-riding-plan:{i+1:02d}', 'collection': 'tutorials',
                        'entity_type': 'OFFICIAL_OPERATOR_PLAN_AND_DESIGN_RATIONALE_DESCRIPTION', 'record_revision': 1,
                        'version_profile': 'TW_WAYI_2003_DATED_COLUMN_PRESERVED_2005_NOT_EXACT_BUILD',
                        'source_refs': [{'source': ORIGINAL, 'actual_capture': CAPTURE, 'sha256': SOURCE_SHA,
                                         'paragraph_indices': c['paragraphs'],
                                         'normalized_paragraph_sha256': [PINS[n][1] for n in c['paragraphs']],
                                         'index_source': INDEX_ORIGINAL, 'index_capture': INDEX_CAPTURE,
                                         'index_sha256': INDEX_SHA, 'index_date_as_written': '2003-12-10'}],
                        'verification_status': 'OPERATOR_DESCRIPTION_OR_PLAN_NOT_ORIGINAL_SERVER_EXECUTION',
                        'rights_status': 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED', 'source_described_claims': c,
                        'actual_server_rule_or_execution_verified': False, 'original_game_ids_or_same_build_binding': None})
    o = {'schema': 'stoneage.wayi2003.newbie_riding_plan.r1', 'date': '2026-10-19',
         'task': 'TW-WAYI-NEWBIE-RIDING-PLAN-SOURCE-01',
         'source': {'original_url': ORIGINAL, 'strict_replay_url': URL, 'actual_capture': CAPTURE,
                    'bytes': len(body), 'sha256': SOURCE_SHA, 'encoding': 'BIG5_STRICT',
                    'index_title_as_written': selected['title'], 'index_date_as_written': '2003-12-10',
                    'index_date_is_original_body_release_or_deployment_proven': False,
                    'index': {'original_url': INDEX_ORIGINAL, 'strict_replay_url': INDEX_URL, 'actual_capture': INDEX_CAPTURE,
                              'bytes': len(index), 'sha256': INDEX_SHA, 'article_entries': len(rows)}},
         'paragraph_fingerprints': [{'index': i, 'normalized_characters': n, 'sha256': h} for i, (n, h) in enumerate(PINS)],
         'records': records,
         'unacquired_image_refs': ['http://www.wayi.com.tw/images02/sa1210-1.jpg', 'http://www.wayi.com.tw/images02/sa1210-2.jpg'],
         'qualified_successor': {**follow, 'original_url': ROOT + 'producer02.asp?idno=67', 'body_or_images_read': False},
         'coverage': {'original_body_and_index': 2, 'source_qualified_tutorials': 5,
                      'images_programs_or_new_game_entities': 0},
         'boundaries': {'source_motive_is_automatic_new_game_design_adoption': False,
                        'jss1999_tw10_cn182_same_build_or_earliest_riding_release_proven': False,
                        'raw_original_html_or_assets_in_git': False, 'stage_a': '7_PARTIAL_2_OPEN',
                        'stage_b_and_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'},
         'next': 'TW-WAYI-NEWBIE-RIDING-SUCCESSOR-GATE-01'}
    validate_report(o)
    return o


def fetch(url):
    with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 StoneAgeHistoricalEvidence'}), timeout=35) as response:
        return response.read(200001), response.url


def main():
    p = argparse.ArgumentParser(); p.add_argument('--input-index'); p.add_argument('--input-body'); p.add_argument('--output', required=True); a = p.parse_args()
    require(bool(a.input_index) == bool(a.input_body), 'Both local source objects or neither required')
    index, index_final = (Path(a.input_index).read_bytes(), INDEX_URL) if a.input_index else fetch(INDEX_URL)
    body, final = (Path(a.input_body).read_bytes(), URL) if a.input_body else fetch(URL)
    o = build(index, index_final, body, final); payload = json.dumps(o, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    out = Path(a.output); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(payload, encoding='utf-8')
    print('INDEX_SHA256=' + INDEX_SHA); print('ARTICLE_SHA256=' + SOURCE_SHA)
    print('SOURCE_PLAN_RECORDS=5 IMAGES_AND_RUNTIME=0'); print('DERIVED_SHA256=' + sha256(payload.encode()).hexdigest())


if __name__ == '__main__': main()
