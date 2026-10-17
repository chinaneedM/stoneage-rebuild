import unittest
from tools.stoneage_legacy_version_witness import SOURCES, SADE, COMPARISON, SETTINGS, derive, report


def fixture():
    bodies = {
        'sade': '部分更新过程 ' + ' '.join(v + ' ' + ' '.join(m for _, m in fs) for v, fs in SADE) + ' 截至到这个版本为止 chs做出0.2g版本 大顺移 法老版 大g版 这个时候在盒子论坛 全凭记忆',
        'comparison': ' '.join(m for _, _, _, ms in COMPARISON for m in ms),
        'sach123': 'SaCh1.23',
        'settings': ' '.join(m for _, _, ms in SETTINGS for m in ms),
    }
    return {k: f'<div id="newsriqi">{d}</div><div id="zhuozhe_left">{a}</div>{s} {bodies[k]} 本文言论' for k, (_, d, a, s) in SOURCES.items()}


class WitnessTests(unittest.TestCase):
    def test_g_is_not_inserted_into_linear_sequence(self):
        rows = derive(fixture())['sade_version_claims']
        self.assertEqual([r['version'] for r in rows[:8]], [v for v, _ in SADE])
        self.assertIsNone(rows[-1]['source_order'])
        self.assertTrue(all(r['release_date'] is None for r in rows))

    def test_feature_marker_in_other_version_cannot_pass(self):
        d = fixture()
        d['sade'] = d['sade'].replace('自动登入', '').replace('0.2c', '自动登入 0.2c', 1)
        # This remains in the 0.2b block: first ensure a genuine cross-version move.
        d['sade'] = d['sade'].replace('自动登入 0.2c', '0.2c 自动登入', 1)
        with self.assertRaises(ValueError): derive(d)

    def test_footer_cannot_supply_missing_feature(self):
        d = fixture(); d['comparison'] = d['comparison'].replace('自动逃跑功能', '') + ' 自动逃跑功能'
        with self.assertRaises(ValueError): derive(d)

    def test_absence_rumor_ambiguity_remain_separate(self):
        rows = {r['feature']: r for r in derive(fixture())['comparison']}
        self.assertEqual(rows['DETAILED_OPPONENT_INFO']['status'], 'USER_REPORTED_ABSENT')
        self.assertIn('HEARSAY', rows['FUTURE_TRAINING_METHOD']['status'])
        self.assertIn('AMBIGUOUS', rows['SCRIPT_COLLECTION']['status'])
        self.assertTrue(all(r['exact_versions'] is None for r in rows.values()))

    def test_luck_is_not_a_verified_rule_or_default(self):
        r = derive(fixture())
        self.assertIn('NOT_CAUSAL', r['settings'][-1]['status'])
        self.assertIn('NOT_DEFAULT', r['settings'][0]['status'])
        self.assertFalse(r['sach_version_attestation']['nearby_abuse_claims_attributed_to_this_build'])

    def test_identity_headers_and_source_completeness(self):
        for key in SOURCES:
            d = fixture(); d[key] = d[key].replace(SOURCES[key][1], '2099-01-01')
            with self.assertRaises(ValueError): derive(d)
        d = fixture(); del d['sach123']
        with self.assertRaises(ValueError): derive(d)

    def test_retrieval_origin_and_utf8_guard(self):
        d = fixture(); a = {k: (v.encode(), SOURCES[k][0]) for k, v in d.items()}
        self.assertFalse(report(a)['software_executed'])
        a['sade'] = (b'\xff', SOURCES['sade'][0])
        with self.assertRaises(UnicodeDecodeError): report(a)
        a['sade'] = (d['sade'].encode(), 'https://example.com/')
        with self.assertRaises(ValueError): report(a)


if __name__ == '__main__': unittest.main()
