import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_jp2004_osanpo_r106_custody as c

class Custody(unittest.TestCase):
    def test_real_dual_source_reports_and_local_audit(self):
        result = c.validate()
        self.assertEqual(result['evidence_pins'], 13)
        self.assertGreaterEqual(result['actual_source_runs'], 23)
        self.assertTrue(result['candidate_main_local_raw_equal'])
        self.assertFalse(result['positive_success_predicate_recovered'])

    def test_same_length_corrupt_report_or_audit_rejected(self):
        d = json.loads(c.RECEIPT.read_bytes())
        real = Path.read_bytes
        for path in [d['artifacts'][0]['path'], d['local_audit']]:
            target = c.ROOT / path
            def corrupt(p):
                b = real(p)
                return b[:-1] + b' ' if p == target else b
            with self.subTest(path=path), patch.object(Path, 'read_bytes', corrupt), self.assertRaisesRegex(ValueError, 'Evidence identity'):
                c.validate()

    def test_commit_zip_or_positive_success_relabeling_rejected(self):
        d = json.loads(c.RECEIPT.read_bytes())
        for key, value in [('source_commit', '0' * 40), ('positive_success_predicate_recovered', True), ('candidate_main_local_raw_equal', False)]:
            altered = copy.deepcopy(d)
            altered[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'Mutated receipt'):
                c.validate(altered)
        altered = copy.deepcopy(d)
        altered['artifacts'][0]['zip_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Mutated receipt'):
            c.validate(altered)

    def test_repinning_receipt_cannot_cover_missing_evidence(self):
        real = Path.read_bytes
        d = json.loads(real(c.RECEIPT))
        d['evidence'].pop(next(iter(d['evidence'])))
        def corrupt(p):
            return json.dumps(d).encode() if p == c.RECEIPT else real(p)
        with patch.object(Path, 'read_bytes', corrupt), self.assertRaisesRegex(ValueError, 'Immutable receipt'):
            c.validate()

if __name__ == '__main__':
    unittest.main()
