"""Offline semantic replay plus immutable provenance checks, no network needed."""
import copy
import hashlib
import json
from pathlib import Path
import unittest
from tests.test_stoneage_legacy_version_witness import fixture
from tools.stoneage_legacy_version_witness import derive, SOURCES

ROOT = Path(__file__).resolve().parents[1]
REPORT = 'research/recovered/STONEAGE-EARLY-ASSISTANT-VERSIONS-R1.json'
RECEIPT = 'research/recovered/STONEAGE-EARLY-ASSISTANT-VERSIONS-ACCEPTANCE-R1.json'


def semantics(report):
    result = copy.deepcopy(report)
    result.pop('sources', None)
    result.pop('body_sha256')
    for row in result['sade_version_claims']: row.pop('section_sha256')
    return result


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.report = json.loads((ROOT / REPORT).read_text())
        self.receipt = json.loads((ROOT / RECEIPT).read_text())

    def test_raw_bytes_and_producer_code_custody(self):
        for path, pin in self.receipt['reports'].items():
            raw = (ROOT / path).read_bytes()
            self.assertEqual(len(raw), pin['bytes'])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), pin['sha256'])
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest(), pin['git_blob'])

    def test_exact_semantic_replay(self):
        self.assertEqual(semantics(self.report), semantics(derive(fixture())))
        # Fingerprints are pinned bytes, not regenerated from synthetic fixtures.
        self.assertEqual(self.report['body_sha256'], self.receipt['source_body_sha256'])
        self.assertEqual([r['section_sha256'] for r in self.report['sade_version_claims']], self.receipt['version_section_sha256'])

    def test_source_identity_and_scope_without_version_promotion(self):
        for key, (url, date, author, _) in SOURCES.items():
            source = self.report['sources'][key]
            self.assertEqual((source['url'], source['final_url'], source['publication_date'], source['author']), (url, url, date, author))
            self.assertEqual(len(source['sha256']), 64)
            self.assertGreater(source['bytes'], 1000)
        self.assertEqual(len(self.report['sade_version_claims']), 9)
        self.assertEqual(len(self.report['comparison']), 7)
        self.assertEqual(len(self.report['settings']), 7)
        for key in ['software_executed', 'adoption_decided', 'all_tools_or_features_recovered', 'global_first_introductions_verified', 'developer_release_records_obtained', 'current_html_authenticated_at_publication', 'exact_official_client_compatibility_verified', 'new_game_production_started']:
            self.assertIs(self.report[key], False)


if __name__ == '__main__': unittest.main()
