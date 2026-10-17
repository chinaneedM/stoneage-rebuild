"""Synthetic parser negatives and the permanent derived-content boundaries."""
import json
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


if __name__ == '__main__':
    unittest.main()
