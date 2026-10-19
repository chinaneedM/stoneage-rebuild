"""One authenticated Hangame world-premise page; no linked assets or game execution."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

from tools.stoneage_early_content_probe import plain, require

ORIGINAL = 'http://www.hangame.co.jp/publish/sa/game.asp'
CAPTURE = '20031214053427'
URL = 'https://web.archive.org/web/' + CAPTURE + 'id_/' + ORIGINAL
SOURCE_SHA = 'c3cb0c64811dfd2d83e5ab809119ddcf09b5ce5b709d1e3c8de1e58c3ec91bfb'
REPORT = Path('research/recovered/STONEAGE-JP2003-WORLD-PREMISE-R1.json')
PINS = [(158, '01ac8901ba170cb47a0ab69a2c991734ce83003ef423957d8f2b9290baab32ae'),
        (118, '7bc58380467274ecd01b26b3c098ac661b7e06049984082a878d90567d97af1f'),
        (115, 'c914324eabc5991c200e6c0c7835124d13458bb897479352bf639f4b399cca9c'),
        (91, '3fd7cf03aabba364986895a2ab110f246c50beedd02db48b16ea3457d9c0625a')]


def paragraphs(document):
    # Strip comment/script containers before locating the single visible content div.
    document = re.sub(r'<!--.*?-->', '', document, flags=re.S)
    document = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', document, flags=re.I | re.S)
    matches = re.findall(r'<div\b[^>]*>\s*<font\b[^>]*>(石器時代のような世界.*?)</font>\s*</div>',
                         document, re.I | re.S)
    require(len(matches) == 1, 'One visible world-premise div required')
    return [plain(p) for p in re.split(r'(?:<br\s*/?>\s*){2,}', matches[0], flags=re.I) if plain(p)]


def validate_report(o):
    require(len(o['records']) == 5, 'Five source-described premise records required')
    facts = [r['source_described_claims'] for r in o['records']]
    require(facts[1]['dinosaur_species_marketing_lower_bound_inclusive'] == 100
            and facts[1]['exact_species_count_or_complete_roster'] is None
            and facts[1]['equals_later_124_entry_catalog_proven'] is False,
            'Marketing lower bound promoted to exact or later roster')
    require(facts[1]['capture_can_be_recorded_in_album_described'] is True
            and facts[1]['automatic_capture_screenshot_or_all_encounters_recorded_proven'] is False,
            'Album capability promoted to automatic image capture')
    require(facts[2]['school_named_or_mapped_entity'] is None
            and facts[2]['school_curriculum_pet_trainer_or_quest_role'] is None
            and facts[2]['currency_item_id_prices_or_trade_algorithm'] is None,
            'Generic facility/economy prose promoted to NPC map or mechanics')
    require(facts[4]['cooperation_and_communication_emphasis_described'] is True
            and facts[4]['combat_absent_or_disabled_proven'] is False
            and facts[4]['epic_history_names_or_wayi_worldline_identity'] is None,
            'Tone promoted to no combat or imported world history')
    for r in o['records']:
        require(r['original_game_entity_ids_or_runtime_verified'] is False
                and r['client_build_or_cross_region_identity'] is None, 'Web description promoted to same-build runtime')
        require(r['rights_status'] == 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED', 'Reuse rights invented')


def build(raw, final):
    require(final == URL, 'Exact world-premise original/capture required')
    require(len(raw) == 12869 and sha256(raw).hexdigest() == SOURCE_SHA, 'World-premise source byte pin differs')
    text = raw.decode('cp932', errors='strict'); ps = paragraphs(text)
    require([(len(p), sha256(p.encode()).hexdigest()) for p in ps] == PINS, 'Visible premise paragraph fingerprint differs')
    require('世界観' in text and '<title>ストーンエイジ</title>' in text.lower(), 'Actual title or world heading missing')
    require(re.search(r'''onclick="location\.href='game2\.asp';"[^>]*>\s*ゲームの特徴\s*</font>''',
                      re.sub(r'<!--.*?-->', '', text, flags=re.S), re.I) is not None,
            'Actual labelled static next target missing')
    tokens = [('生活', '狩り', 'つかまえ', '飼育', '戦わせる', 'メール'),
              ('１００種類以上', '恐竜図鑑', '記録することが出来', 'コンプリート'),
              ('石のお金', '武器屋', '道具屋', '学校', '教育施設', 'パーティー', '泣く', '手を振る', 'チャット'),
              ('戦闘より', '協力やコミュニケーション中心', '和気あいあい', 'ほのぼの')]
    for p, required in zip(ps, tokens):
        require(all(token in p for token in required), 'Premise meaning changed')
    facts = [
        {'topic': 'DINOSAUR_COMPANIONS_AND_LIFE', 'paragraph': 0,
         'hunting_capture_and_pet_rearing_described': True, 'hunting_together_with_pet_described': True,
         'pet_battles_and_mail_carrying_described': True,
         'capture_probability_growth_or_mail_lifecycle': None},
        {'topic': 'MARKETING_VARIETY_AND_COLLECTION', 'paragraph': 1,
         'dinosaur_species_marketing_lower_bound_inclusive': 100,
         'exact_species_count_or_complete_roster': None, 'equals_later_124_entry_catalog_proven': False,
         'capture_can_be_recorded_in_album_described': True,
         'automatic_capture_screenshot_or_all_encounters_recorded_proven': False,
         'collection_completion_is_optional_enjoyment_described': True},
        {'topic': 'STONE_CURRENCY_AND_GENERIC_FACILITIES', 'paragraph': 2,
         'stone_money_circulation_described': True,
         'generic_facilities_as_written': ['武器屋', '道具屋', '学校'],
         'school_is_described_as_educational_facility': True, 'school_named_or_mapped_entity': None,
         'school_curriculum_pet_trainer_or_quest_role': None,
         'currency_item_id_prices_or_trade_algorithm': None},
        {'topic': 'PARTY_AND_EXPRESSIVE_COMMUNICATION', 'paragraph': 2,
         'party_adventure_described': True, 'chat_gesture_examples_as_written': ['泣く', '手を振る'],
         'gesture_ids_animations_and_party_rules': None},
        {'topic': 'COOPERATIVE_WORLD_TONE', 'paragraph': 3,
         'cooperation_and_communication_emphasis_described': True,
         'combat_absent_or_disabled_proven': False,
         'epic_history_names_or_wayi_worldline_identity': None,
         'rebuild_design_adoption_decided': False},
    ]
    records = []
    for i, f in enumerate(facts):
        n = f['paragraph']
        records.append({'record_id': f'jp2003-world-premise:{i+1:02d}', 'collection': 'sources',
                        'entity_type': 'OFFICIAL_WORLD_PREMISE_DESCRIPTION', 'record_revision': 1,
                        'version_profile': 'JAPAN_HANGAME_WEB_20031214_NOT_EXACT_CLIENT_BUILD',
                        'source_refs': [{'source': ORIGINAL, 'actual_capture': CAPTURE, 'sha256': SOURCE_SHA,
                                         'visible_paragraph_index': n, 'normalized_paragraph_sha256': PINS[n][1]}],
                        'verification_status': 'OPERATOR_WEB_DESCRIPTION_NOT_CLIENT_OR_SERVER_EXECUTION',
                        'rights_status': 'RESEARCH_METADATA_ONLY_NOT_RELEASE_APPROVED',
                        'source_described_claims': f, 'original_game_entity_ids_or_runtime_verified': False,
                        'client_build_or_cross_region_identity': None})
    o = {'schema': 'stoneage.jp2003.world_premise.r1', 'date': '2026-10-19',
         'task': 'JP2003-OFFICIAL-WORLD-PREMISE-SOURCE-01',
         'source': {'original_url': ORIGINAL, 'strict_replay_url': URL, 'actual_capture': CAPTURE,
                    'bytes': len(raw), 'sha256': SOURCE_SHA, 'encoding': 'CP932_STRICT',
                    'actual_title': 'ストーンエイジ', 'actual_visible_section': '世界観',
                    'original_entry_previously_qualified_by': 'STONEAGE-OFFICIAL-VERSION-COVERAGE-MATERIAL-REVIEW-R5.json',
                    'capture_is_release_or_same_build_date': False},
         'paragraph_fingerprints': [{'index': i, 'normalized_characters': n, 'sha256': h}
                                    for i, (n, h) in enumerate(PINS)],
         'records': records,
         'coverage': {'original_content_pages': 1, 'visible_paragraphs': 4, 'source_records': 5,
                      'images_or_programs_or_linked_content_pages_fetched': 0,
                      'named_npc_pet_species_maps_or_quests_recovered': 0},
         'acquisition_history': {'web_reader_initial_attempt': 'UNAVAILABLE_NOT_PROOF_OF_ABSENCE',
                                 'initial_requested_capture': '20031214055553',
                                 'initial_http_final_capture': CAPTURE,
                                 'strict_independent_replay_must_match_actual_capture': True},
         'qualified_next_target': {'label_as_written': 'ゲームの特徴',
                                    'original_url': 'http://www.hangame.co.jp/publish/sa/game2.asp',
                                    'qualification': 'STATIC_LITERAL_ONCLICK_NOT_EXECUTED',
                                    'target_body_or_images_acquired': False},
         'boundaries': {'raw_original_html_or_assets_committed': False,
                        'jss1999_tw10_cn182_or_174a_build_identity_proven': False,
                        'source_tone_automatically_becomes_rebuild_design': False,
                        'stage_a': '7_PARTIAL_2_OPEN', 'stage_b_and_wiki': 'GATED', 'r79': 'PAUSED_NON_BLOCKING'},
         'next': 'JP2003-OFFICIAL-GAME-FEATURES-SOURCE-01'}
    validate_report(o)
    return o


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--input'); parser.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.input:
        raw, final = Path(args.input).read_bytes(), URL
    else:
        with urlopen(Request(URL, headers={'User-Agent': 'Mozilla/5.0 StoneAgeHistoricalEvidence'}), timeout=35) as response:
            raw, final = response.read(150001), response.url
    o = build(raw, final); payload = json.dumps(o, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    path = Path(args.output); path.parent.mkdir(parents=True, exist_ok=True); path.write_text(payload, encoding='utf-8')
    print('SOURCE_SHA256=' + SOURCE_SHA); print('PREMISE_SOURCE_RECORDS=5 ORIGINAL_PAGES=1 ASSETS=0')
    print('DERIVED_SHA256=' + sha256(payload.encode()).hexdigest())


if __name__ == '__main__':
    main()
