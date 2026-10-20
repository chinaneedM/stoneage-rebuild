import copy
import hashlib
import json
import unittest
from tools.stoneage_jp2007_starter_club_source import REPORT, ROOT, validate


class StarterClubSource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(REPORT.read_text())

    def reject(self, path, value):
        r = copy.deepcopy(self.r)
        node = r
        for key in path[:-1]:
            node = node[key]
        node[path[-1]] = value
        with self.assertRaises(ValueError):
            validate(r)

    def test_valid_versioned_six_record_contract(self):
        validate(self.r)
        self.assertEqual(len({r['record_id'] for r in self.r['records']}), 6)
        self.reject(['records', 0, 'version_profile'], 'TW10')
        self.reject(['records', 0, 'game_ids'], [2007])

    def test_integer_bonuses_not_prefix_matches(self):
        for key, wrong in [('attack_bonus', 90), ('agility_bonus', 10), ('unnamed_stat_bonus', 10)]:
            with self.subTest(key=key):
                self.reject(['extracted', 'operator', key], wrong)

    def test_hidden_attribute_and_zero_vigor_keep_unknowns(self):
        self.reject(['extracted', 'operator', 'hidden_stat_name'], 'LUCK')
        self.reject(['extracted', 'operator', 'spell_level'], 10)
        self.reject(['extracted', 'operator', 'spell_vigor_cost'], 1)
        self.reject(['unproven', 'zero_vigor_means_no_other_use_limits'], True)

    def test_editorial_not_primary_and_code_ui_unknown(self):
        self.reject(['extracted', 'editorial', 'is_operator_quote'], True)
        self.reject(['extracted', 'editorial', 'code_input_location'], 'WEB_ACCOUNT_FORM')
        self.assertEqual(self.r['records'][-1]['source_refs'], ['S1E'])

    def test_later_source_does_not_prove_earliest_build_or_live_service(self):
        for key in self.r['unproven']:
            with self.subTest(boundary=key):
                self.reject(['unproven', key], True)
        self.reject(['source', 'historical_2007_bytes_authenticated'], True)

    def test_permanent_derived_replay_and_actual_semantic_mutations(self):
        path = ROOT / 'research/recovered/STONEAGE-JP2007-STARTER-CLUB-LOCAL-REPLAY-R1.json'
        replay = json.loads(path.read_text())
        self.assertEqual(replay['extracted'], self.r['extracted'])
        self.assertEqual(replay['http_sha256'], self.r['source']['current_observed_sha256'])
        audit = replay['adversarial']
        self.assertEqual(len(audit['real_source_mutations']), 13)
        self.assertEqual(len({x['mutated_input_sha256'] for x in audit['real_source_mutations']}), 13)
        self.assertTrue(all(x['rejected_without_digest_gate'] for x in audit['real_source_mutations']))
        self.assertTrue(audit['outer_script_positive'])
        self.assertFalse(replay['server_execution_verified'])

    def test_stage_gate_unchanged(self):
        self.reject(['status', 'stage_b_wiki'], 'OPEN')
        self.reject(['status', 'r79'], 'COMPLETE')

    def test_required_custody_validates_every_pinned_file(self):
        path = ROOT / 'research/recovered/STONEAGE-JP2007-STARTER-CLUB-CUSTODY-R1.json'
        self.assertTrue(path.is_file(), 'The completed source milestone requires its permanent custody receipt')
        receipt = json.loads(path.read_text())
        self.assertEqual(receipt['candidate']['conclusion'], 'success')
        for pin in receipt['pins']:
            b = (ROOT / pin['path']).read_bytes()
            self.assertEqual(len(b), pin['bytes'])
            self.assertEqual(hashlib.sha256(b).hexdigest(), pin['sha256'])
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(), pin['git_blob'])
        for pin in receipt['startup_prefixes']:
            b = (ROOT / pin['path']).read_bytes()[:pin['bytes']]
            self.assertEqual(hashlib.sha256(b).hexdigest(), pin['sha256'])
        if receipt['main'] is not None:
            main = receipt['main']
            self.assertEqual(main['conclusion'], 'success')
            self.assertTrue(main['applicable_workflows_all_success'])
            self.assertNotEqual(main['run_id'], receipt['candidate']['run_id'])
            self.assertNotEqual(main['job_id'], receipt['candidate']['job_id'])
            raw = (ROOT / 'research/recovered/STONEAGE-JP2007-STARTER-CLUB-CI-MAIN-REPLAY-R1.json').read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), main['raw_sha256'])
            candidate = (ROOT / 'research/recovered/STONEAGE-JP2007-STARTER-CLUB-CI-CANDIDATE-REPLAY-R1.json').read_bytes()
            self.assertEqual(raw, candidate)


if __name__ == '__main__':
    unittest.main()
