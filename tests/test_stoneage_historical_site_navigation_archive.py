"""Immutable derived reports and exact link-graph replay, without original HTML."""
import hashlib
import json
from pathlib import Path
import unittest
from tools.stoneage_historical_site_navigation_catalog import build

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'research/recovered/STONEAGE-HISTORICAL-SITE-NAVIGATION'


class NavigationArchiveTests(unittest.TestCase):
    def test_raw_reports_and_code_match_custody_receipt(self):
        receipt = json.loads((ROOT / (PREFIX + '-ACCEPTANCE-R1.json')).read_text())
        for path, pin in receipt['reports'].items():
            raw = (ROOT / path).read_bytes()
            with self.subTest(path=path):
                self.assertEqual(len(raw), pin['bytes'])
                self.assertEqual(hashlib.sha256(raw).hexdigest(), pin['sha256'])
                self.assertEqual(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest(), pin['git_blob'])
        self.assertEqual(len(receipt['source_attempts']), 3)
        for attempt in receipt['source_attempts']:
            self.assertEqual(attempt['conclusion'], 'success')
            self.assertTrue(attempt['zip_digest'].startswith('sha256:'))
            self.assertTrue(attempt['source_head'])

    def test_exact_semantic_replay_and_target_fragment_boundaries(self):
        raw = (ROOT / (PREFIX + '-R1.json')).read_bytes()
        report = json.loads(raw)
        expected = build(report)
        expected['source_report_sha256'] = hashlib.sha256(raw).hexdigest()
        archived = json.loads((ROOT / (PREFIX + '-CATALOG-R1.json')).read_text())
        self.assertEqual(archived, expected)
        self.assertTrue(archived['pages'])
        self.assertFalse(archived['historical_layout_verified'])
        self.assertFalse(archived['linked_game_content_verified'])
        self.assertFalse(archived['public_export_enabled'])
        self.assertTrue(all(not e['historical_click_execution_verified'] for e in archived['links']))
        for source in report['targets'].values():
            if source['status'] == 'ARCHIVED_HTML_LINK_METADATA_QUALIFIED':
                self.assertTrue(source['actual_capture'].startswith(('1999', '2000', '2001', '2002')))
        # Earlier bounded queries remain visible after the fallback found pages.
        attempt1 = json.loads((ROOT / (PREFIX + '-ATTEMPT1-R1.json')).read_text())
        self.assertEqual(attempt1['qualified_pages'], 2)
        self.assertFalse(attempt1['source_absence_established'])


if __name__ == '__main__': unittest.main()
