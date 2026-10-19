"""Finite official profession-access proposal; no deployed class/skill table."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from tools.stoneage_early_content_probe import plain, require
from tools.stoneage_wayi_newbie_riding_plan import INDEX_ORIGINAL, INDEX_CAPTURE, INDEX_URL, INDEX_SHA, index_rows, fetch

ORIGINAL = 'http://www.wayi.com.tw/stoneage/producer/producer02.asp?idno=64'
CAPTURE = '20041206141244'
URL = 'https://web.archive.org/web/' + CAPTURE + 'id_/' + ORIGINAL
SOURCE_SHA = 'cd725562731d4e74f9b90bbefe9c167d499b73511d9fee2d94186ec0b2d2d8a9'
REPORT = Path('research/recovered/STONEAGE-WAYI2003-PROFESSION-ACCESS-PLAN-R1.json')
PINS = [(37, 'dc24d7e1f1e64413576274faadaee4ca70b4b992b12695c28a6340196395ae45'),
        (117, '1519fb4da63a5dd080d2f4f82ac0fecaba91a3743608121749034e2626ce2135'),
        (132, '1513e6652169222eaa1dfe67c7ba001310f24746a8d1b94d485978e3413f509b'),
        (29, '4e12e50febf3589f1f8cb1b67b7e8cd1dd684a96392a21fff8ba4b047d74eeef'),
        (11, '9f55a27b6292ae8f10073519cfc545aee0537a1c5beec0fa6e03a180a411f1e0')]


def paragraphs(doc):
    matches = re.findall(r'<span\b[^>]*>\s*(酷哥在搭乘.*?研究了石器近期的計劃。.*?)</span>', doc, re.I | re.S)
    require(len(matches) == 1, 'One profession proposal body required')
    return [plain(p) for p in re.split(r'\r?\n\s*\r?\n', matches[0]) if plain(p)]


def validate_report(o):
    require(len(o['records']) == 5, 'Five bounded documentary records required')
    claims = [r['source_described_claims'] for r in o['records']]
    require(claims[0]['speaker_as_written'] == '酷哥'
            and claims[0]['airline_scene_is_verified_transport_or_npc'] is False,
            'Column frame promoted to transport or NPC implementation')
    require(claims[1]['newbie_participation_in_veteran_activities_is_stated_goal'] is True
            and claims[1]['easier_training_and_earning_exact_rates'] is None,
            'Stated catch-up motive promoted to numeric progression or economy')
    p = claims[2]
    require(p['status'] == 'OPERATOR_STATED_PLAN'
            and p['previous_entry_condition_as_written'] == '一轉成人禮'
            and p['proposed_entry_condition_as_written'] == '八十級成人禮'
            and p['lower_profession_quest_difficulty_planned'] is True
            and p['unreincarnated_entry_is_caption_and_plan_not_deployment'] is True
            and p['current_level_gte_80_alone_is_sufficient_proven'] is False
            and p['original_ceremony_quest_script_ids_rewards_or_exact_comparator'] is None,
            'Entry proposal promoted to deployed level-only ceremony or quest rule')
    s = claims[3]
    require(s['status'] == 'OPERATOR_STATED_PLAN'
            and s['skill_tier_as_written'] == '二級'
            and s['learning_condition_as_written'] == '一轉以上'
            and s['tier_is_character_level_2_or_two_skills'] is False
            and s['all_profession_access_still_requires_reincarnation'] is False
            and s['profession_names_skill_names_ids_costs_or_tree'] is None,
            'Skill-tier gate conflated with character level, entry gate or imported class list')
    require(claims[4]['status'] == 'FUTURE_DISCUSSION_INTENT'
            and claims[4]['label_as_written'] == '懷舊計劃'
            and claims[4]['content_or_release_implemented_proven'] is False,
            'Future nostalgia discussion promoted to defined feature or release')
    for r in o['records']:
        require(r['actual_server_rule_or_execution_verified'] is False
                and r['original_game_ids_or_same_build_binding'] is None,
                'Operator prose promoted to original execution or build')
    src = o['source']
    require(src['index_date_as_written'] == '2003-11-14'
            and src['actual_capture'] == CAPTURE
            and src['index']['actual_capture'] == INDEX_CAPTURE
            and src['index_date_is_verified_body_release_or_deployment'] is False,
            'Index date, body capture and actual deployment conflated')
    require(len(o['unacquired_image_refs']) == 2
            and all(r['actual_capture'] is None and r['sha256'] is None and r['actual_dimensions'] is None and not r['pixels_requested']
                    for r in o['unacquired_image_refs']), 'Image reference promoted to actual pixels')
    require(o['coverage']['original_npc_quest_skill_or_profession_entities_restored'] == 0
            and o['boundaries']['source_proposal_is_deployed_server_rule'] is False,
            'Source records counted as restored original classes or deployment')


def build(index, index_final, body, final):
    require(index_final == INDEX_URL and final == URL, 'Exact original URLs and capture identities required')
    require(len(index) == 28883 and sha256(index).hexdigest() == INDEX_SHA, 'Official index byte pin differs')
    require(len(body) == 17678 and sha256(body).hexdigest() == SOURCE_SHA, 'Profession article byte pin differs')
    rows = index_rows(index.decode('big5', errors='strict'))
    selected = next((r for r in rows if r['article_id_as_web_key'] == 64), None)
    require(selected == {'article_id_as_web_key': 64, 'title': '全民就職計劃', 'index_date_as_written': '2003-11-14'},
            'Selected article title, date and real link differ')
    ps = paragraphs(body.decode('big5', errors='strict'))
    require([(len(p), sha256(p.encode()).hexdigest()) for p in ps] == PINS, 'Normalized profession paragraph fingerprints differ')
    require(all(x in ps[2] for x in ['打算接著要調整', '一轉成人禮', '八十級成人禮', '降低就職任務的難度',
                                    '二級的技能需要一轉以上', '老手仍有可以更精進']), 'Plan and separate entry/learning conditions missing')
    claims = [
        {'topic': 'AUTHOR_AND_COLUMN_FRAME', 'paragraphs': [0], 'speaker_as_written': '酷哥',
         'framing_airdrop_label_as_written': '空投西吉魯', 'framing_airline_label_as_written': '加美航班',
         'airline_scene_is_verified_transport_or_npc': False},
        {'topic': 'ACCESS_AND_PARTICIPATION_RATIONALE', 'paragraphs': [1, 2],
         'newbie_participation_in_veteran_activities_is_stated_goal': True,
         'easier_training_and_earning_presented_as_prior_changes_by_author': True,
         'easier_training_and_earning_exact_rates': None,
         'retaining_further_veteran_progression_is_stated_goal': True},
        {'topic': 'PROPOSED_PROFESSION_ENTRY_CHANGE', 'paragraphs': [2, 4], 'status': 'OPERATOR_STATED_PLAN',
         'previous_entry_condition_as_written': '一轉成人禮',
         'proposed_entry_condition_as_written': '八十級成人禮',
         'lower_profession_quest_difficulty_planned': True,
         'unreincarnated_entry_is_caption_and_plan_not_deployment': True,
         'current_level_gte_80_alone_is_sufficient_proven': False,
         'original_ceremony_quest_script_ids_rewards_or_exact_comparator': None},
        {'topic': 'PROPOSED_HIGHER_SKILL_LEARNING_GATE', 'paragraphs': [2], 'status': 'OPERATOR_STATED_PLAN',
         'skill_tier_as_written': '二級', 'learning_condition_as_written': '一轉以上',
         'tier_is_character_level_2_or_two_skills': False,
         'all_profession_access_still_requires_reincarnation': False,
         'profession_names_skill_names_ids_costs_or_tree': None},
        {'topic': 'NOSTALGIA_AS_FUTURE_DISCUSSION', 'paragraphs': [3], 'status': 'FUTURE_DISCUSSION_INTENT',
         'label_as_written': '懷舊計劃', 'content_or_release_implemented_proven': False},
    ]
    records = []
    for i, c in enumerate(claims):
        records.append({'record_id': f'wayi-column2003:profession-access:{i+1:02d}',
                        'collection': 'sources' if i in [0, 4] else 'tutorials',
                        'entity_type': 'OFFICIAL_OPERATOR_PROFESSION_PROPOSAL_CONTEXT' if i in [0, 4] else 'OFFICIAL_OPERATOR_PROGRESSION_DESCRIPTION',
                        'record_revision': 1, 'version_profile': 'TW_WAYI_2003_DATED_COLUMN_PRESERVED_2004_NOT_EXACT_BUILD',
                        'source_refs': [{'original_url': ORIGINAL, 'actual_capture': CAPTURE, 'sha256': SOURCE_SHA,
                                         'paragraph_indices': c['paragraphs'],
                                         'normalized_paragraph_sha256': [PINS[n][1] for n in c['paragraphs']]}],
                        'verification_status': 'OPERATOR_PROPOSAL_AND_RATIONALE_NOT_DEPLOYED_RULE',
                        'rights_status': 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED', 'source_described_claims': c,
                        'actual_server_rule_or_execution_verified': False, 'original_game_ids_or_same_build_binding': None})
    o = {'schema': 'stoneage.wayi2003.profession_access_plan.r1', 'date': '2026-10-19',
         'task': 'TW-WAYI-PROFESSION-ACCESS-PLAN-SOURCE-01',
         'source': {'original_url': ORIGINAL, 'strict_replay_url': URL, 'actual_capture': CAPTURE,
                    'bytes': len(body), 'sha256': SOURCE_SHA, 'encoding': 'BIG5_STRICT',
                    'index_title_as_written': selected['title'], 'index_date_as_written': selected['index_date_as_written'],
                    'index_date_is_verified_body_release_or_deployment': False,
                    'index': {'original_url': INDEX_ORIGINAL, 'strict_replay_url': INDEX_URL,
                              'actual_capture': INDEX_CAPTURE, 'bytes': len(index), 'sha256': INDEX_SHA,
                              'qualified_article_entries_not_whole_column_census': len(rows)}},
         'paragraph_fingerprints': [{'index': i, 'normalized_characters': n, 'sha256': h} for i, (n, h) in enumerate(PINS)],
         'records': records,
         'unacquired_image_refs': [{'original_url': 'http://www.wayi.com.tw/images02/sa921113001'+v+'.jpg',
                                   'role': role, 'html_declared_dimensions': dims, 'pixels_requested': False,
                                   'actual_capture': None, 'sha256': None, 'actual_dimensions': None}
                                  for v, role, dims in [('b', 'LINKED_LARGER_IMAGE', None), ('s', 'INLINE_IMAGE', [300, 225])]],
         'coverage': {'new_article_bodies': 1, 'known_index_reacquired_not_new': 1,
                      'tutorial_records': 3, 'source_context_records': 2,
                      'original_npc_quest_skill_or_profession_entities_restored': 0, 'image_pixels_or_binaries_acquired': 0},
         'boundaries': {'same_build_jss1999_tw10_cn182_or_exact_first_profession_release': False,
                        'source_proposal_is_deployed_server_rule': False, 'automatic_new_game_design_adoption': False,
                        'raw_original_html_or_assets_in_git': False, 'stage_a': '7_PARTIAL_2_OPEN',
                        'stage_b_and_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'},
         'implementation_reopen_trigger': 'AUTHENTIC_SAME_PERIOD_OFFICIAL_PATCH_OR_VERSION_QUALIFIED_ORIGINAL_QUEST_SKILL_SERVER_SOURCE',
         'next': 'OFFICIAL-VERSION-RELEASE-SOURCE-COVERAGE-REVIEW-13'}
    validate_report(o)
    return o


def main():
    p = argparse.ArgumentParser(); p.add_argument('--input-index'); p.add_argument('--input-body'); p.add_argument('--output', required=True); a = p.parse_args()
    require(bool(a.input_index) == bool(a.input_body), 'Both local sources or neither required')
    index, index_final = (Path(a.input_index).read_bytes(), INDEX_URL) if a.input_index else fetch(INDEX_URL)
    body, final = (Path(a.input_body).read_bytes(), URL) if a.input_body else fetch(URL)
    o = build(index, index_final, body, final)
    payload = json.dumps(o, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    out = Path(a.output); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(payload, encoding='utf-8')
    print('INDEX_SHA256=' + INDEX_SHA); print('ARTICLE_SHA256=' + SOURCE_SHA)
    print('TUTORIALS=3 SOURCE_CONTEXT=2 ORIGINAL_CLASS_SKILL_ENTITIES=0')
    print('DERIVED_SHA256=' + sha256(payload.encode()).hexdigest())


if __name__ == '__main__': main()
