"""Source-bound task contracts and material false-promotion regressions."""
import json
import hashlib
from pathlib import Path
import unittest
from tools.stoneage_adult_ceremony_probe import between, report, same_task_block, news_header, SOURCES

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'research/recovered/STONEAGE-ADULT-CEREMONY-SOURCE-CONTRACT-R1.json'


class AdultCeremonyTests(unittest.TestCase):
    def data(self):
        return json.loads(REPORT.read_text())

    def test_selected_claims_cannot_leak_from_footer_or_next_task(self):
        self.assertEqual(between('noise START claim END footer', 'START', 'END'), 'START claim ')
        for source in ('END before START', 'missing', 'START damaged\ufffd END'):
            with self.assertRaises(ValueError):
                between(source, 'START', 'END')

    def test_missing_or_redirected_sources_require_requalification(self):
        with self.assertRaisesRegex(ValueError, 'incomplete'):
            report({})
        from tools.stoneage_adult_ceremony_probe import SOURCES
        sources = {k: (b'invented', url) for k, (url, _) in SOURCES.items()}
        sources['compilation'] = (b'invented', 'https://example.invalid/other')
        with self.assertRaisesRegex(ValueError, 'redirect'):
            report(sources)

    def test_duplicate_block_is_not_an_independent_witness(self):
        d = self.data()['observations']
        self.assertEqual(d['lineage']['duplicate_of'], {'duplicate': 'compilation'})
        self.assertEqual(d['selected_block_sha256']['duplicate'], d['selected_block_sha256']['compilation'])
        self.assertFalse(d['lineage']['independent_origins_authenticated'])

    def test_task_equality_tolerates_spacing_but_rejects_rule_changes(self):
        same_task_block('invented LV 30', 'inventedLV30', 'synthetic')
        with self.assertRaisesRegex(ValueError, 'requalify'):
            same_task_block('invented LV 30', 'invented LV 35', 'synthetic')

    def test_footer_date_or_author_cannot_replace_publication_header(self):
        valid = '<div id="newsriqi">2001-06-14</div><div id="zhuozhe_left">作者：Atron</div>'
        news_header(valid, 'Atron')
        for changed in (valid.replace('2001-06-14', 'unknown') + ' footer 2001-06-14',
                        valid.replace('作者：Atron', 'unknown') + ' footer 作者：Atron'):
            with self.assertRaises(ValueError):
                news_header(changed, 'Atron')

    def test_archive_proves_selected_block_by_november_not_january(self):
        d = self.data()['observations']
        witness = d['temporal_witness']
        self.assertEqual(witness['actual_capture'], '20011120063019')
        self.assertEqual(d['selected_block_sha256']['archived_compilation'], d['selected_block_sha256']['compilation'])
        self.assertTrue(witness['selected_task_block_matches_current'])
        self.assertFalse(witness['january_2001_content_proven'])
        self.assertFalse(witness['archive_is_independent_rule_author'])
        self.assertFalse(witness['earliest_capture_exhaustively_established'])

    def test_archive_redirect_cannot_inherit_requested_capture_date(self):
        acquisitions = {k: (b'invented', url) for k, (url, _) in SOURCES.items()}
        acquisitions['archived_compilation'] = (b'invented', SOURCES['archived_compilation'][0].replace('20011120063019', '20030101000000'))
        with self.assertRaisesRegex(ValueError, 'redirect'):
            report(acquisitions)

    def test_reward_conflict_has_no_merged_default(self):
        d = self.data()['observations']
        profiles = d['profiles']
        self.assertEqual(profiles['compilation']['reward']['agility_delta'], -2)
        self.assertEqual(profiles['later_adult']['reward']['agility_delta'], -3)
        self.assertIsNone(profiles['levelguide']['reward']['agility_delta'])
        self.assertNotIn('default_profile', d)
        self.assertEqual(d['conflicts'][0]['resolution'], 'UNRESOLVED_KEEP_SEPARATE_PROFILES')

    def test_later_item_lifetime_is_not_backdated(self):
        p = self.data()['observations']['profiles']
        for field in ('drop_destroys_jade', 'logout_destroys_jade'):
            self.assertIsNone(p['compilation'][field])
            self.assertTrue(p['later_adult'][field])
        self.assertTrue(p['later_adult']['disconnect_destroys_jade'])

    def test_approach_party_and_trial_help_are_different_phases(self):
        p = self.data()['observations']['profiles']
        self.assertTrue(p['levelguide']['advises_party_on_approach'])
        self.assertFalse(p['levelguide']['party_allowed_inside_trial_proven'])
        self.assertFalse(p['later_adult']['party_inside_trial'])
        self.assertTrue(p['later_adult']['battle_help_allowed'])

    def test_level_recommendation_and_south_fee_are_not_universal_gates(self):
        p = self.data()['observations']['profiles']['compilation']
        self.assertEqual((p['reported_minimum_level'], p['recommendation_level']), (30, 35))
        self.assertFalse(p['recommendation_is_gate'])
        self.assertEqual(p['south_approach_pass_cost'], 200)
        self.assertFalse(p['all_approaches_pay'])
        self.assertTrue(self.data()['observations']['scope_distinctions']['empty_bag_at_collection_is_not_empty_bag_at_entry'])

    def test_publication_labels_do_not_authenticate_exact_build_or_item_identity(self):
        d = self.data()
        self.assertFalse(d['current_html_authenticated_in_asserted_publication_year'])
        self.assertFalse(d['catalog_date_authenticates_compilation_bytes'])
        self.assertEqual(d['early_exact_build_membership'], 'OPEN')
        self.assertTrue(all(v is None for v in d['observations']['unknown'].values()))
        for flag in ('original_server_executed', 'original_quest_script_recovered', 'stage_a_accepted'):
            self.assertFalse(d[flag])
        self.assertEqual(d['stage_b_gate'], 'GATED')
        self.assertIsNone(d['observations']['source_asserted_dates']['compilation'])

    def test_source_metadata_is_complete_without_retaining_proprietary_text(self):
        d = self.data()
        self.assertEqual(len(d['sources']), 6)
        for source in d['sources'].values():
            self.assertGreater(source['bytes'], 0)
            self.assertRegex(source['sha256'], r'^[0-9a-f]{64}$')
            self.assertEqual(set(source), {'url', 'final_url', 'bytes', 'sha256', 'decoding', 'replacement_characters'})

    def test_independent_artifact_survives_expiry_as_exact_git_blob(self):
        folder = ROOT / 'research/recovered'
        receipt = json.loads((folder / 'STONEAGE-ADULT-CEREMONY-ACCEPTANCE-R1.json').read_text())
        raw = (ROOT / receipt['permanent_path']).read_bytes()
        self.assertEqual(len(raw), receipt['raw_json_bytes'])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), receipt['raw_json_sha256'])
        self.assertEqual(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest(), receipt['permanent_git_blob'])
        self.assertEqual(json.loads(raw), self.data())
        self.assertEqual(receipt['source_acquisition_count'], 6)
        self.assertFalse(receipt['original_server_executed'])


if __name__ == '__main__':
    unittest.main()
