"""One bounded adulthood-quest origin qualification, without replaying old web sources."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = 'research/recovered/'
REPORT = P+'STONEAGE-ADULT-QUEST-ORIGIN-QUALIFICATION-R117.json'
INPUTS = {
    'adult': ('STONEAGE-ADULT-CEREMONY-SOURCE-CONTRACT-R1.json', '27403615ac8f4f826db6926fb6c2fb9a60608fcc5dfd4c4d2a3d585ddd613b8b'),
    'adult_ci': ('STONEAGE-ADULT-CEREMONY-CI-DERIVED-R1.json', '27403615ac8f4f826db6926fb6c2fb9a60608fcc5dfd4c4d2a3d585ddd613b8b'),
    'adult_receipt': ('STONEAGE-ADULT-CEREMONY-ACCEPTANCE-R1.json', '0a1f9ad69d024ebbab586f6373a93e2f8a015e0335f582074f5de2f73d15b21d'),
    'xmas': ('STONEAGE-JP2004-XMAS-PARTY-COMBAT-R110.json', 'e6f15494d1da10e33f53abc5e23f7a23d37e89226e7b16c66c5bef6ba6d5185e'),
    'jss': ('STONEAGE-JSS-EARLY-QUEST-ORIGINS-R116.json', 'e66a477e6096babce940abaa62d33977c1a5912f547e320db07e62c4a3f4b894'),
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def load_inputs(root=ROOT):
    objects, pins = {}, []
    for key, (name, digest) in INPUTS.items():
        path = P+name
        raw = (root/path).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == digest, 'Source bytes changed: '+key)
        objects[key] = json.loads(raw)
        pins.append({'key': key, 'path': path, 'bytes': len(raw), 'sha256': digest,
                     'git_blob': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()})
    return objects, pins

def build(objects, pins):
    adult = objects['adult']
    require(adult == objects['adult_ci'], 'Old source and accepted CI payload differ')
    receipt = objects['adult_receipt']
    require(receipt['raw_json_sha256'] == INPUTS['adult'][1] and
            receipt['subsequent_validation']['header_guard_followup_complete'] is True,
            'Prior temporal-witness acceptance incomplete')
    observation = adult['observations']
    witness = observation['temporal_witness']
    require(witness['selected_task_block_matches_current'] and witness['actual_capture'] == '20011120063019',
            'Missing exact archived task witness')
    require(observation['lineage']['duplicate_of'] == {'duplicate': 'compilation'}, 'Text lineage changed')
    christmas = objects['xmas']['observations']['christmas']
    require(christmas['s1_required_quest'] == '成人の儀' and christmas['s1_requirement_is_media_claim'],
            'Event prerequisite evidence changed')
    genkou = next(r for r in objects['jss']['update_evidence']['records'] if r['archive_id'] == 'JSS-GENKOU-20000424')
    require(genkou['origin_class'] == 'ORIGIN_UNRESOLVED', 'Cave incorrectly promoted')
    return {
        'schema': 'stoneage.adult_quest_origin_qualification.r117', 'date': '2026-10-24',
        'baseline_head': 'e4f8f064678a7ef6bda59f03bf44738dd9da8a5b',
        'task': 'EARLY-BASE-QUEST-PROVENANCE-117', 'inputs': pins,
        'scope': 'ONE_ADULTHOOD_QUEST_ORIGIN_QUESTION_NOT_A_GLOBAL_QUEST_CENSUS',
        'qualification': {'documentary_label': '成人仪式／成人礼（中文文献标签）',
            'origin_class': 'ORIGIN_UNRESOLVED', 'record_kind': 'QUEST_ORIGIN_QUALIFICATION',
            'region': None, 'exact_release_or_build': None, 'operator': None,
            'first_introduced_date': None, 'native_quest_id': None, 'native_npc_ids': None,
            'native_reward_ids': None, 'launch_baseline_admission': False, 'permanence_proven': False,
            'is_operator_event_proven': False, 'original_server_executed': False},
        'documentary_time_evidence': {
            'accepted_capture': witness['actual_capture'],
            'archived_page': adult['sources']['archived_compilation'],
            'selected_block_sha256': observation['selected_block_sha256']['archived_compilation'],
            'selected_normalized_characters': witness['selected_normalized_characters'],
            'meaning': 'THIS_SELECTED_GUIDE_TEXT_EXISTED_BY_THE_ACCEPTED_CAPTURE_NOT_GAME_RELEASE_DATE',
            'earliest_capture_exhaustively_established': False,
            'page_directory_0101_proves_january_2001_text': False,
            'sina_and_17173_same_block_are_independent_rule_witnesses': False,
            'guide_host_language_proves_game_region_or_build': False,
            'newly_acquired_source_this_turn': False},
        'event_dependency_boundary': {
            'source_path': P+INPUTS['xmas'][0],
            'source_pointer': '/observations/christmas/s1_required_quest',
            'source_label': christmas['s1_required_quest'],
            'event_window': christmas['s1_announced_window'],
            'relation': 'REPORTED_REQUIRED_COMPLETION_BEFORE_CHRISTMAS_PARTICIPATION',
            'prerequisite_quest_inherits_event_origin_or_window': False,
            'prerequisite_is_base_or_permanent_proven': False,
            'jp2004_prerequisite_equals_2001_chinese_quest_native_entity_proven': False},
        'excluded_cross_quest_inference': {
            'jss_named_cave': genkou['source_label'],
            'operator_written_date': genkou['source_clauses'][0]['operator_written_date'],
            'evidence': 'NAMED_CAVE_PROGRESSION_FIX_NOT_ADULTHOOD_OR_LAUNCH_PROOF',
            'jss_cave_fix_dates_chinese_adulthood_quest': False},
        'new_acquisition_attempts': [{
            'url': 'https://groups.google.com/g/tw.bbs.rec.mud/c/A0YUU3uzAaQ',
            'search_title': 'SA....石器時代.....', 'index_display_date_claim': '2000-06-13',
            'indexed_quest_label': '成人禮', 'status': 'UNQUALIFIED_SEARCH_LEAD',
            'web_open': 'UNAVAILABLE', 'direct_http_status': 429,
            'original_message_headers_obtained': False, 'body_obtained': False,
            'raw_bytes': None, 'raw_sha256': None, 'independent_date_authenticated': False,
            'admitted_as_historical_date_or_release_evidence': False,
            'retry_after_429': False}],
        'bounded_search': {
            'targets': ['TW2000_ADULTHOOD_OFFICIAL_RELEASE_OR_MANUAL', 'JSS_ADULTHOOD_1999_2000',
                        'JSS_GENKOU_NOT_GBC_OR_LATER_PLAYER_GUIDE'],
            'new_qualifying_first_party_launch_or_permanence_evidence_found': False,
            'later_guides_or_cross_platform_matches_used_to_backfill_launch': False,
            'global_source_absence_established': False},
        'decision': {'outcome': 'BOUNDED_ORIGIN_QUESTION_REMAINS_OPEN_NO_PROMOTION',
            'reopen_on': ['DATED_SAME_REGION_RELEASE_MANUAL_WITH_NAMED_TASK',
                          'EXPLICIT_SAME_REGION_PERMANENT_TASK_ADDITION_NOTICE',
                          'AUTHENTICATED_SAME_BUILD_SCRIPT_OR_TASK_MASTER'],
            'do_not_repeat': ['OLD_SIX_ADULT_SOURCE_ACQUISITIONS_WITHOUT_NEW_MATERIAL',
                              'GOOGLE_GROUPS_RATE_LIMIT_RETRY_THIS_UNIT', 'R116_FROZEN_CENSUS',
                              'JSS_UNNAMED_UPDATE_HELPER_EXPANSION']},
        'boundaries': {'new_original_game_entities': 0, 'new_verified_launch_quests': 0,
            'new_verified_permanent_quests': 0, 'new_raw_historical_source_obtained': False,
            'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_wiki': 'GATED',
            'savedata_r79': 'PAUSED_NON_BLOCKING', 'overall_restoration_percentage': None},
        'next': {'task': 'EARLY-NPC-VISUAL-SOURCE-118',
            'deliverable': 'One early JSS or Taiwan official named NPC/interaction image with actual source attribution, or a precise acquisition gap',
            'stop': 'One source-qualified named visual contract; no guessing native IDs or repeating unqualified later event archives'}
    }

def verify(root=ROOT):
    objects, pins = load_inputs(root)
    expected = build(objects, pins)
    require(json.loads((root/REPORT).read_bytes()) == expected, 'Origin report differs from source-derived replay')
    return expected

if __name__ == '__main__':
    r = verify()
    print('R117 adulthood origin remains unresolved; accepted documentary witness '+r['documentary_time_evidence']['accepted_capture'])
    print('Event prerequisite, release baseline and unread search lead remain distinct: PASS')
