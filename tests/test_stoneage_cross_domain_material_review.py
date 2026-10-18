import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class CrossDomainMaterialReviewTests(unittest.TestCase):
    def test_prior_22_domain_historical_states_are_preserved(self):
        prior = json.loads((ROOT / 'research/recovered/STONEAGE-22-DOMAIN-SOURCE-READY-PORTFOLIO-R2.json').read_text())
        current = json.loads((ROOT / 'research/recovered/STONEAGE-CROSS-DOMAIN-MATERIAL-REVIEW-R3.json').read_text())
        self.assertEqual([(r['domain_id'], r['original_order'], r['baseline_evidence_status']) for r in prior['all_domain_rows']],
                         [(r['domain_id'], r['original_order'], r['baseline_evidence_status']) for r in current['reviewed_domains']])
        for r in current['reviewed_domains']:
            self.assertFalse(r['tw10_original_content_completed'])
            self.assertFalse(r['version_promotion_allowed'])
        self.assertEqual(current['reviewed_domains_count'], 22)
        self.assertIsNone(current['boundaries']['overall_restoration_percentage'])
        self.assertEqual(current['boundaries']['stage_b_production'], 'GATED')

    def test_all_claim_inputs_still_have_exact_original_custody(self):
        data = json.loads((ROOT / 'research/recovered/STONEAGE-CROSS-DOMAIN-MATERIAL-REVIEW-R3.json').read_text())
        for source in data['sources']:
            raw = (ROOT / source['path']).read_bytes()
            self.assertEqual(len(raw), source['bytes'], source['path'])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), source['sha256'], source['path'])
            self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(), source['git_blob'])
        old = data['continuity_input']
        prefix = (ROOT / old['path']).read_bytes()[:old['bytes']]
        self.assertEqual(hashlib.sha256(prefix).hexdigest(), old['sha256'])

if __name__ == '__main__':
    unittest.main()
