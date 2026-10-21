import copy
import hashlib
import json
import unittest
from tools.stoneage_cn2003_group2_manor_report import REPORT, ROOT, STEM, comparison, inspect_image, validate


class Group2ManorReport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(REPORT.read_text())
        cls.local = json.loads((ROOT / ('research/recovered/' + STEM + '-LOCAL-REPLAY-R1.json')).read_text())

    def reject(self, keys, value):
        r = copy.deepcopy(self.r)
        node = r
        for key in keys[:-1]:
            node = node[key]
        node[keys[-1]] = value
        with self.assertRaises(ValueError):
            validate(r)

    def test_eight_searchable_records_have_source_order(self):
        validate(self.r)
        self.assertEqual([r['village_label'] for r in self.r['extracted']['manor_snapshot']], ['萨姆吉尔', '玛丽娜丝', '加加', '卡鲁它那'])
        self.reject(['records', 2, 'evidence'], self.r['records'][3]['evidence'])
        self.reject(['records', 1, 'game_ids'], [1])
        self.reject(['records', 0, 'version_profile'], 'TW10')

    def test_noon_not_exact_time_build_or_timezone(self):
        for key, value in [('exact_time', '12:00'), ('body_year', 2003), ('timezone', 'Asia/Shanghai')]:
            self.reject(['extracted', 'opening_report', key], value)
        self.reject(['extracted', 'label_is_authenticated_client_build'], True)

    def test_occupants_and_reputations_keep_order(self):
        self.assertEqual([r['reputation_reported'] for r in self.r['extracted']['manor_snapshot']], [4524, 2280, 4079, 2811])
        self.reject(['extracted', 'manor_snapshot', 1, 'occupying_family_label'], '龙族')
        self.reject(['extracted', 'reputations_are_eligibility_thresholds'], True)
        self.reject(['extracted', 'current_manor_owners_in_2026_proven'], True)

    def test_population_is_reported_ambiguous_and_unaudited(self):
        for key, value in [('headcount_scope', 'EACH_FAMILY'), ('per_family_counts', [90]*4), ('exact_window_start_end', ['11-19 16:43','11-20 16:43']), ('audited_statistics', True)]:
            self.reject(['extracted', 'population_report', key], value)

    def test_operations_claim_not_independent_uptime_or_compensation(self):
        self.reject(['extracted', 'operations_report', 'independent_uptime_or_compensation'], '100_PERCENT')
        self.reject(['extracted', 'opening_occupancy_or_statistics_independently_witnessed'], True)

    def test_riding_symbol_and_future_events_not_rules_or_results(self):
        self.reject(['extracted', 'family_riding', 'mount_names_ids_or_eligibility_rules'], {'level': 80})
        self.reject(['extracted', 'events', 'status_in_notice'], 'COMPLETED')
        self.reject(['extracted', 'events', 'schedule_rules_or_results'], {'winner':'龙族'})

    def test_prior_source_keeps_its_own_unknowns(self):
        c = comparison(self.r['prior_input'], self.r['extracted'])
        self.assertEqual(c['newly_named_villages_in_later_source'], ['玛丽娜丝','卡鲁它那'])
        self.reject(['comparison', 'prior_article_itself_now_contains_all_names'], True)
        self.reject(['comparison', 'prior_billing_execution_now_verified'], True)
        self.reject(['prior_input', 'sha256'], '0'*64)

    def test_actual_link_and_current_image_not_runtime_proof(self):
        self.reject(['image', 'requested_url'], 'https://example.com/wrong.jpg')
        self.reject(['image', 'capture_date'], '2003-11-19')
        self.reject(['image', 'native_client_resolution_proven'], True)
        self.reject(['visual_observation', 'proves_opening_occupancy_or_family_battle'], True)
        with self.assertRaises(ValueError):
            inspect_image(self.r, b'not a jpeg')

    def test_eighteen_real_source_changes_without_digest_gate(self):
        cases = self.local['audit']['real_source_mutations']
        self.assertEqual(len(cases), 18)
        self.assertEqual(len({x['input_sha256'] for x in cases}), 18)
        self.assertTrue(all(x['rejected_without_digest_gate'] for x in cases))
        self.assertTrue(self.local['audit']['outer_script_positive'])
        self.assertFalse(self.local['historical_server_executed'])
        self.assertFalse(self.local['raw_html_or_assets_in_output'])

    def test_authority_and_stage_queue_boundaries(self):
        self.reject(['source', 'authenticated_2003_original_bytes'], True)
        self.reject(['source', 'authority'], 'ORIGINAL_SERVER_EXECUTED')
        for key in self.r['unproven']:
            self.reject(['unproven', key], True)
        self.reject(['status', 'stage_b_wiki'], 'OPEN')
        self.reject(['next'], 'EXPAND_MANOR_HELPERS')


    def test_required_durable_custody_and_full_prefixes(self):
        p = ROOT / ('research/recovered/' + STEM + '-CUSTODY-R1.json')
        self.assertTrue(p.is_file(), 'Accepted material requires permanent custody')
        r = json.loads(p.read_text())
        self.assertEqual(r['schema'], 'stoneage.cn2003_group2_manor_report.custody.r1')
        for pin in r['source_pins']:
            b = (ROOT / pin['path']).read_bytes()
            self.assertEqual(len(b), pin['bytes'])
            self.assertEqual(hashlib.sha256(b).hexdigest(), pin['sha256'])
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(), pin['git_blob'])
        self.assertEqual(len(r['source_pins']), 10)
        self.assertEqual(len(r['startup_prefixes']), 9)
        for pin in r['startup_prefixes']:
            b = (ROOT / pin['path']).read_bytes()[:pin['bytes']]
            self.assertEqual(hashlib.sha256(b).hexdigest(), pin['sha256'])
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(), pin['git_blob'])
        self.assertEqual(len(r['workflow_runs']), 21)
        self.assertTrue(all(x['conclusion'] == 'success' for x in r['workflow_runs']))
        copies = []
        for label in ('candidate', 'main'):
            meta = r[label]
            self.assertEqual(meta['actual_unit_tests'], 10)
            self.assertEqual(meta['skipped_tests'], 0)
            self.assertEqual(meta['head'], r['content_head'])
            self.assertEqual(meta['tree'], r['content_tree'])
            self.assertTrue(meta['all_applicable_workflows_success'])
            b = (ROOT / meta['derived_git_path']).read_bytes()
            self.assertEqual(len(b), meta['raw_bytes'])
            self.assertEqual(hashlib.sha256(b).hexdigest(), meta['raw_sha256'])
            self.assertEqual(hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(), meta['raw_git_blob'])
            copies.append(b)
        for key in ('run_id', 'job_id', 'artifact_id'):
            self.assertNotEqual(r['candidate'][key], r['main'][key])
        self.assertEqual(copies[0], copies[1])
        self.assertEqual(copies[0], (ROOT / ('research/recovered/' + STEM + '-LOCAL-REPLAY-R1.json')).read_bytes())
        self.assertTrue(all(x is False for x in r['bounds'].values()))


if __name__ == '__main__':
    unittest.main()
