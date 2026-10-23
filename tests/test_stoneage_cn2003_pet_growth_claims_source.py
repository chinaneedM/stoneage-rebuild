"""Adversarial R92 data-contract tests: player claims never equal original master."""
import copy
import json
import unittest
from tools.stoneage_cn2003_pet_growth_claims_source import P, verify

class TestPetGrowthClaims(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(P.read_text(encoding='utf-8'))
    def reject(self, edit):
        x = copy.deepcopy(self.data)
        edit(x)
        with self.assertRaises(AssertionError): verify(x)
    def test_exact_baseline(self):
        self.assertTrue(verify(self.data))
        self.assertEqual(len(self.data['records']), 8)
    def test_missing_original_identity_and_version_boundary(self):
        self.reject(lambda x: x['source'].update(source_game_build='TW1.0'))
        self.reject(lambda x: x['records'][0].update(original_pet_id=999))
        self.reject(lambda x: x.update(scope='JSS1999'))
    def test_unknown_rubi_growth_and_partial_hp(self):
        self.reject(lambda x: x['records'][4]['reported_growth_max_text'].update(attack='2.1'))
        self.reject(lambda x: x['records'][4]['lv1_reported_ranges'].update(hp=[41, 51]))
    def test_cross_source_cannot_backfill_2003_unknown(self):
        self.reject(lambda x: x['cross_source'].update(fill_missing_player_lower_bound=True))
        self.reject(lambda x: x['records'][5]['lv1_reported_ranges'].update(hp=[55, 61]))
        self.reject(lambda x: x['cross_source'].update(same_build_verified=True))
    def test_imprecise_growth_not_exact_cap(self):
        self.reject(lambda x: x['records'][6]['reported_growth_max_text'].update(hp='12.30'))
        self.reject(lambda x: x['records'][0]['reported_growth_max_text'].update(hp='10.2'))
        self.reject(lambda x: x['negative_boundaries'].update(growth_maxima_are_official_limits=True))
    def test_named_skill_is_not_server_execution(self):
        self.reject(lambda x: x['reported_skills'][1].update(original_server_formula_verified=True))
        self.reject(lambda x: x['negative_boundaries'].update(skill_formula_implemented=True))
    def test_source_not_official_and_no_raw_html_hash(self):
        self.reject(lambda x: x['source'].update(original_html_authenticated=True))
        self.reject(lambda x: x['source'].update(raw_html_sha256='made-up'))
        self.reject(lambda x: x.update(evidence_type='OFFICIAL_GAME_MASTER'))
    def test_stage_gates_remain_open(self):
        self.reject(lambda x: x['negative_boundaries'].update(stage_a_accepted=True))
        self.reject(lambda x: x['negative_boundaries'].update(overall_restoration_percentage=90))
        self.reject(lambda x: x.update(record_count=99))
    def test_record_reordering_and_contract_injection(self):
        self.reject(lambda x: x['records'].reverse())
        self.reject(lambda x: x.update(original_server_formula='confirmed'))


class TestR92AcceptanceReceipt(unittest.TestCase):
    def test_accepted_derived_blob_and_bounded_actions(self):
        import hashlib
        from pathlib import Path
        root = P.parents[2]
        receipt = json.loads((root / 'research/recovered/STONEAGE-CN2003-PET-GROWTH-ACCEPTANCE-R92.json').read_text(encoding='utf-8'))
        raw = P.read_bytes()
        self.assertEqual(receipt['task'], 'OFFICIAL-VERSION-NAMED-CONTENT-MATERIAL-REVIEW-92')
        self.assertEqual(receipt['derived_json']['git_blob_sha1'], hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\x00' + raw).hexdigest())
        self.assertEqual(receipt['derived_json']['path'], 'research/recovered/STONEAGE-CN2003-PET-GROWTH-PLAYER-CLAIMS-SOURCE-R1.json')
        self.assertFalse(receipt['derived_json']['contains_original_html'])
        self.assertFalse(receipt['verification']['has_ci_artifacts'])
        self.assertEqual(receipt['verification']['candidate_content_run_id'], 39947773737)
        self.assertEqual(receipt['verification']['candidate_content_job_id'], 120394538483)
        self.assertEqual(receipt['verification']['main_dedicated_run_id'], 39948235290)
        self.assertEqual(receipt['verification']['main_dedicated_job_id'], 120396056316)
        for key, count in [('candidate_continuity_run_ids', 9), ('main_content_run_ids', 11)]:
            actual = receipt['verification'][key]
            self.assertEqual(len(actual), count)
            self.assertEqual(len(set(actual)), count)
        self.assertTrue(receipt['verification']['all_original_validation_runs_completed_success'])
        self.assertFalse(receipt['scope']['original_pet_master_recovered'])
        self.assertFalse(receipt['scope']['original_client_executed'])
        self.assertFalse(receipt['scope']['stage_a_accepted'])
        self.assertFalse(receipt['scope']['stage_b_open'])
        self.assertIsNone(receipt['scope']['overall_restoration_percentage'])

if __name__ == '__main__':
    unittest.main()
