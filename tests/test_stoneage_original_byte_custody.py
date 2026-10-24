"""Reject provenance drift and unsupported historical promotions."""
import copy
import json
import unittest
from tools.stoneage_original_byte_custody import ROOT, REPORT, validate, validate_report


class OriginalByteCustodyTests(unittest.TestCase):
    def setUp(self):
        self.report = json.loads((ROOT / REPORT).read_bytes())

    def test_archived_bytes_and_full_historical_prefixes(self):
        self.assertEqual(validate()['status'], 'PASS')

    def test_source_run_and_manifest_substitution_rejected(self):
        for field, value in [('github_head_sha', '0' * 40), ('github_run_id', '0'), ('historical_manifest_git_blobs', {})]:
            with self.subTest(field=field):
                report = copy.deepcopy(self.report)
                report[field] = value
                with self.assertRaises(ValueError):
                    validate_report(report)

    def test_file_and_path_counts_are_distinct(self):
        report = copy.deepcopy(self.report)
        report['counts']['original_core_matched_files'] = 237
        with self.assertRaises(ValueError):
            validate_report(report)

    def test_original_server_or_official_purity_not_inferred(self):
        for field in ('official_purity_of_bridge_qualified', 'original_payload_published', 'pet_npc_quest_server_data_inferred'):
            with self.subTest(field=field):
                report = copy.deepcopy(self.report)
                report[field] = True
                with self.assertRaises(ValueError):
                    validate_report(report)

    def test_partial_bytes_and_wrong_archive_rejected(self):
        report = copy.deepcopy(self.report)
        report['bridge_subtree_logical_bytes'] -= 1
        with self.assertRaises(ValueError):
            validate_report(report)
        report = copy.deepcopy(self.report)
        report['archive_digest_gates']['bridge_combined_sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            validate_report(report)
