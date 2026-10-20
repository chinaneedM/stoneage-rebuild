import copy
import json
import unittest
from tools.stoneage_jp2005_special_maps_source import REPORT, ROOT, comparison, validate


class SpecialMaps(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(REPORT.read_text())

    def reject(self, keys, value):
        r = copy.deepcopy(self.r)
        node = r
        for key in keys[:-1]:
            node = node[key]
        node[keys[-1]] = value
        with self.assertRaises(ValueError):
            validate(r)

    def test_three_tiered_maps_six_records_not_original_world(self):
        validate(self.r)
        self.assertEqual(len({x['record_id'] for x in self.r['records']}), 6)
        self.reject(['records', 0, 'game_ids'], [2005])
        self.reject(['records', 0, 'version_profile'], 'TW10')
        self.reject(['extracted', 'tier_labels_as_written'], ['1-20', '21-60', '61+'])

    def test_parent_dog_quantity_and_species_stay_unknown(self):
        self.reject(['extracted', 'map2', 'required_parent_quantity'], 3)
        self.reject(['extracted', 'map2', 'pet_species_ids'], [123])
        self.reject(['unproven', 'all_ice_dogs_same_species'], True)

    def test_boss_loot_possible_not_guaranteed(self):
        self.reject(['extracted', 'map3', 'reward'], 'GUARANTEED_RARE_ITEM')
        self.reject(['extracted', 'map3', 'drop_rate'], 1.0)

    def test_ticket_and_party_concern_are_editorial(self):
        self.reject(['extracted', 'editorial', 'is_operator_quote'], True)
        self.reject(['records', 4, 'source_refs'], ['S1Q'])
        self.reject(['records', 5, 'verification_status'], 'OPERATOR_QUOTATION_NOT_RUNTIME')
        self.reject(['unproven', 'editorial_party_concern_observed'], True)
        self.reject(['extracted', 'editorial', 'ticket_consumption_or_duration'], 'ONE_ENTRY')

    def test_cross_year_name_is_not_same_map_identity(self):
        self.assertEqual(comparison(self.r['later_derived_input']), self.r['comparisons'])
        self.reject(['comparisons', 0, 'relation'], 'SAME_MAP_ID')
        self.reject(['comparisons', 1, 'later'], 'バルツ山の洞窟')

    def test_later_input_requires_exact_native_git_identity(self):
        self.reject(['later_derived_input', 'sha256'], '0' * 64)
        self.reject(['later_derived_input', 'git_blob'], '0' * 40)

    def test_current_web_and_archive_503_do_not_prove_history_or_absence(self):
        self.reject(['source', 'original_2005_bytes_authenticated'], True)
        self.assertEqual([x['attempts'] for x in self.r['bounded_unavailable_attempts']], [2, 1])
        self.assertTrue(all(x['actual_http_status'] == 503 for x in self.r['bounded_unavailable_attempts']))
        for key in self.r['unproven']:
            with self.subTest(key=key):
                self.reject(['unproven', key], True)

    def test_real_source_semantic_mutations_without_digest_shortcut(self):
        r = json.loads((ROOT / 'research/recovered/STONEAGE-JP2005-SPECIAL-MAPS-LOCAL-REPLAY-R1.json').read_text())
        self.assertEqual(r['extracted'], self.r['extracted'])
        cases = r['audit']['real_source_mutations']
        self.assertEqual(len(cases), 13)
        self.assertEqual(len({x['input_sha256'] for x in cases}), 13)
        self.assertTrue(all(x['rejected_without_digest_gate'] for x in cases))
        self.assertTrue(r['audit']['outer_script_positive'])
        self.assertFalse(r['server_execution_verified'])

    def test_stage_does_not_advance_with_source_counts(self):
        self.reject(['status', 'stage_b_wiki'], 'OPEN')
        self.reject(['status', 'r79'], 'COMPLETE')

    def test_required_durable_independent_ci_custody(self):
        import hashlib
        p = ROOT / 'research/recovered/STONEAGE-JP2005-SPECIAL-MAPS-CUSTODY-R1.json'
        self.assertTrue(p.is_file(), 'The accepted source milestone must retain permanent custody')
        receipt = json.loads(p.read_text())
        for pin in receipt['source_pins']:
            b = (ROOT / pin['path']).read_bytes()
            self.assertEqual(len(b), pin['bytes'])
            self.assertEqual(hashlib.sha256(b).hexdigest(), pin['sha256'])
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(), pin['git_blob'])
        for pin in receipt['startup_prefixes']:
            b = (ROOT / pin['path']).read_bytes()[:pin['bytes']]
            self.assertEqual(hashlib.sha256(b).hexdigest(), pin['sha256'])
        c, m = receipt['candidate'], receipt['main']
        self.assertEqual((c['conclusion'], m['conclusion']), ('success', 'success'))
        self.assertNotEqual(c['run_id'], m['run_id'])
        self.assertNotEqual(c['job_id'], m['job_id'])
        for label, meta in [('CANDIDATE', c), ('MAIN', m)]:
            raw = (ROOT / ('research/recovered/STONEAGE-JP2005-SPECIAL-MAPS-CI-' + label + '-REPLAY-R1.json')).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), meta['raw_sha256'])
            self.assertEqual(json.loads(raw)['extracted'], self.r['extracted'])
            self.assertTrue(meta['all_applicable_workflows_success'])


if __name__ == '__main__':
    unittest.main()
