import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch
from tools import stoneage_jp2004_named_village_r105_custody as c

class Custody(unittest.TestCase):
    def test_real_dual_source_custody(self):
        r = c.validate()
        self.assertEqual(r['evidence_pins'], 12)
        self.assertGreaterEqual(r['actual_source_runs'], 23)
        self.assertTrue(r['candidate_main_local_raw_equal'])
        self.assertFalse(r['operator_patch_bodies_recovered'])

    def test_equal_length_report_damage_rejected(self):
        d = json.loads(c.RECEIPT.read_bytes())
        target = c.ROOT / d['artifacts'][0]['path']
        real = Path.read_bytes
        def damaged(p):
            b = real(p)
            return b[:-1] + b' ' if p == target else b
        with patch.object(Path, 'read_bytes', damaged), self.assertRaisesRegex(ValueError, 'Evidence identity'):
            c.validate()

    def test_commit_zip_or_runtime_relabeling_rejected(self):
        d = json.loads(c.RECEIPT.read_bytes())
        for key, value in [('source_commit', '0' * 40), ('operator_patch_bodies_recovered', True), ('candidate_main_local_raw_equal', False)]:
            altered = copy.deepcopy(d)
            altered[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'Mutated receipt'):
                c.validate(altered)
        altered = copy.deepcopy(d)
        altered['artifacts'][0]['zip_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'Mutated receipt'):
            c.validate(altered)

    def test_repinning_receipt_is_not_trusted(self):
        real = Path.read_bytes
        d = json.loads(real(c.RECEIPT))
        d['evidence'][next(iter(d['evidence']))]['sha256'] = '0' * 64
        def damaged(p):
            return json.dumps(d).encode() if p == c.RECEIPT else real(p)
        with patch.object(Path, 'read_bytes', damaged), self.assertRaisesRegex(ValueError, 'Immutable receipt'):
            c.validate()

if __name__ == '__main__':
    unittest.main()
