"""R92 bounded secondary pet-stat evidence verifier; not a pet runtime."""
import hashlib
import json
from pathlib import Path

P = (Path(__file__).resolve().parents[1] /
     'research/recovered/STONEAGE-CN2003-PET-GROWTH-PLAYER-CLAIMS-SOURCE-R1.json')
PINS = {
    'records': 'a93f276b29483f3ed1e4519cbe06d19dbec2914b442e93425db98a1d9faf8668',
    'source': '83c11e53744136f24b02c00ef6131d7b93ebf4448aa2dc8528d9b706c0d4fc35',
    'cross_source': '032edd7009e8cc63100de2713aec89517b357b1e38081f96ddf98085cb96ff82',
    'reported_skills': '064a598185f1a933cf0405c39e7e1f22bc596ab623ff9d0c9364db1a242f0226',
}
EXPECTED_KEYS = {'schema', 'task', 'source', 'scope', 'evidence_type', 'record_count',
                 'records', 'cross_source', 'reported_skills', 'negative_boundaries',
                 'missing_evidence', 'next'}

def _digest(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()

def verify(data):
    assert set(data) == EXPECTED_KEYS, 'unknown/missing contract fields'
    assert data['schema'] == 'stoneage.cn2003_player_pet_stats_claims.r1'
    assert data['task'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-92'
    assert data['next'] == 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-93'
    assert data['scope'] == '2003_MAINLAND_PLAYER_OPINION_MULTIPLE_RELEASES_UNKNOWN_EXACT_BUILD_NOT_TW10'
    assert data['evidence_type'] == 'FACT_OF_2003_SUBMITTED_CLAIMS_NOT_OFFICIAL_GAME_MASTER'
    assert data['record_count'] == 8 == len(data['records'])
    for k, wanted in PINS.items():
        assert _digest(data[k]) == wanted, f'changed source-bound {k}'
    src = data['source']
    assert src['original_html_authenticated'] is False
    assert src['raw_html_sha256'] is None and src['source_game_build'] is None
    cross = data['cross_source']
    assert cross['same_build_verified'] is False
    assert cross['publication_date'] is None
    assert cross['original_player_source_hp_lv1'] == [None, 61]
    assert cross['separate_source_hp_lv1'] == [55, 61]
    assert cross['fill_missing_player_lower_bound'] is False
    names = [x['name_in_source'] for x in data['records']]
    assert len(names) == len(set(names)) == 8
    for entry in data['records']:
        assert entry['original_pet_id'] is None
        assert entry['growth_values_official_caps_verified'] is False
        for pair in entry['lv1_reported_ranges'].values():
            assert len(pair) == 2
            assert all(isinstance(x, int) or x is None for x in pair)
            if None not in pair: assert pair[0] <= pair[1]
    assert all(x is None for x in data['records'][4]['reported_growth_max_text'].values())
    assert data['records'][4]['lv1_reported_ranges']['hp'] == [41, None]
    assert data['records'][5]['lv1_reported_ranges']['hp'] == [None, 61]
    assert data['records'][6]['reported_growth_max_text']['hp'].endswith('X')
    assert data['records'][7]['reported_growth_max_text']['hp'].endswith('X')
    assert data['reported_skills'][1]['original_server_formula_verified'] is False
    flags = data['negative_boundaries']
    assert set(flags) == {
        'original_pet_master_recovered', 'same_build_runtime_verified',
        'growth_maxima_are_official_limits', 'skill_formula_implemented',
        'sprites_matched', 'all_original_pet_ids', 'overall_restoration_percentage',
        'stage_a_accepted', 'stage_b_started',
    }
    assert all(v is False for k, v in flags.items() if k not in
               ('all_original_pet_ids', 'overall_restoration_percentage'))
    assert flags['all_original_pet_ids'] is None
    assert flags['overall_restoration_percentage'] is None
    assert len(data['missing_evidence']) >= 6
    return True

def main():
    data = json.loads(P.read_text(encoding='utf-8'))
    verify(data)
    print('R92 PASS: 8 bounded claims, uncertain numeric tokens, source separation; no original pet master')

if __name__ == '__main__':
    main()
