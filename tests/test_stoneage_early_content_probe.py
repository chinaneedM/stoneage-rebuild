"""Synthetic parser negatives and the permanent derived-content boundaries."""
import json
import hashlib
from pathlib import Path
import unittest

from tools.stoneage_early_content_probe import JSS_CAPTURE, integer, report, section

ROOT = Path(__file__).resolve().parents[1]


class EarlyContentProbeTests(unittest.TestCase):
    def test_anchor_sections_do_not_bleed_into_next_business_rule(self):
        invented = '<A NAME="8010"></A>invented save text<A NAME="8100"></A>invented bus 3'
        self.assertEqual(section(invented, "8010"), "invented save text")
        with self.assertRaisesRegex(ValueError, "missing original manual anchor"):
            section(invented, "8070")

    def test_fullwidth_numeric_reading_and_absence_are_distinct(self):
        self.assertEqual(integer("invented ４人まで", r"([0-9０-９]+)人まで", "seats"), 4)
        with self.assertRaisesRegex(ValueError, "numeric observation"):
            integer("invented unknown seats", r"([0-9０-９]+)人まで", "seats")

    def test_wrong_archive_capture_cannot_inherit_expected_date(self):
        with self.assertRaisesRegex(ValueError, "capture redirect changed"):
            report({"jss_manual": (b"invented", "https://web.archive.org/web/20010303065824id_/http://www.titan.co.jp/stoneage/manual02.html")})

    def test_permanent_source_metadata_and_evidence_limits(self):
        data = json.loads((ROOT / 'research/recovered/STONEAGE-EARLY-CONTENT-GUIDE-MANUAL-R1.json').read_text())
        self.assertEqual(len(data['sources']), 7)
        self.assertEqual(data['manual_capture'], JSS_CAPTURE)
        for source in data['sources'].values():
            self.assertGreater(source['bytes'], 0)
            self.assertRegex(source['sha256'], r'^[a-f0-9]{64}$')
            self.assertNotIn('html', set(source))
        for flag in ('manual_is_1999_or_tw10_exact_build', 'catalog_date_authenticates_current_html_bytes_in_2001',
                     'guide_zip_obtained', 'original_server_executed', 'early_quest_scripts_recovered', 'stage_a_accepted'):
            self.assertIs(data[flag], False)
        self.assertEqual(data['stage_b_gate'], 'GATED')

    def test_business_unknowns_and_distinct_operations_stay_visible(self):
        d = json.loads((ROOT / 'research/recovered/STONEAGE-EARLY-CONTENT-GUIDE-MANUAL-R1.json').read_text())['observations']
        self.assertIsNone(d['manual_contracts']['bus']['fare'])
        self.assertFalse(d['manual_contracts']['bus']['direct_edge_topology_proven'])
        self.assertIsNone(d['manual_contracts']['ground_item']['duration'])
        profiles = {p['id']: p for p in d['guide_profiles']}
        self.assertTrue(all(p['early_version_membership'] == 'OPEN' for p in profiles.values()))
        self.assertIsNone(profiles['LOGGING_LICENCE']['guide_example']['exact_unit_price'])
        self.assertFalse(profiles['ADULT_CEREMONY']['pass_cost_required_for_all_approaches'])
        self.assertIsNone(profiles['FIVE_BROTHERS']['server_logout_flag'])
        self.assertTrue(d['comparison']['repeat_penalty_and_earlier_discard_penalty_are_different_operations'])
        self.assertTrue(d['comparison']['earlier_shell_to_flower_branch_is_not_disproved_by_reverse_branch'])

    def test_archived_independent_acquisition_matches_local_semantic_report(self):
        folder = ROOT / 'research/recovered'
        local = json.loads((folder / 'STONEAGE-EARLY-CONTENT-GUIDE-MANUAL-R1.json').read_text())
        remote = json.loads((folder / 'STONEAGE-EARLY-CONTENT-CI-DERIVED-R1.json').read_text())
        self.assertEqual(remote, local)
        self.assertFalse(remote['original_server_executed'])

    def test_first_party_manual_does_not_overwrite_descendant_configuration(self):
        from tools.stoneage_transport_core_model import DEFAULT_WAIT_SECONDS, init_state
        from tools.stoneage_savepoint_elder_model import begin_savepoint_talk
        from tools.stoneage_healer_recovery_model import window_healer_level_is_free
        folder = ROOT / 'research/recovered'
        data = json.loads((folder / 'STONEAGE-EARLY-CONTENT-GUIDE-MANUAL-R1.json').read_text())
        self.assertEqual(data['observations']['manual_contracts']['bus']['stop_minutes'] * 60,
                         DEFAULT_WAIT_SECONDS)
        configured = init_state(kind='bus', route_count=1, selected_route=1,
                                selected_route_points=3, now=0, waittime=120)
        self.assertEqual(configured.waittime, 120)
        noitem = begin_savepoint_talk(savepoint_mask=1, last_talk_elder=0,
                                      elder_id=6, noitem=True, requirement_available=False)
        self.assertEqual(noitem['stage'], 'activated')
        self.assertFalse(window_healer_level_is_free(10, 10))
        crosswalk = json.loads((folder / 'STONEAGE-EARLY-CONTENT-MODEL-CROSSWALK-R1.json').read_text())
        self.assertFalse(crosswalk['existing_runtime_code_changed'])
        for pin in crosswalk['source_pins'].values():
            body = (ROOT / pin['path']).read_bytes()
            self.assertEqual(hashlib.sha256(body).hexdigest(), pin['sha256'])
            self.assertEqual(len(body), pin['bytes'])


if __name__ == '__main__':
    unittest.main()
