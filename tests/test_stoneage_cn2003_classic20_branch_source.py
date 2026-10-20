import copy
import json
import unittest
from tools.stoneage_cn2003_classic20_branch_source import REPORT, ROOT, comparison, validate


class Classic20Branch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(REPORT.read_text())

    def reject(self, keys, value):
        r = copy.deepcopy(self.r)
        node = r
        for k in keys[:-1]:
            node = node[k]
        node[keys[-1]] = value
        with self.assertRaises(ValueError):
            validate(r)

    def test_six_versioned_source_records(self):
        validate(self.r)
        self.assertEqual(len({x['record_id'] for x in self.r['records']}), 6)
        self.reject(['records', 0, 'version_profile'], 'CN20_ORIGINAL_2001')
        self.reject(['records', 0, 'game_ids'], [2])

    def test_operator_label_not_binary_identity(self):
        self.reject(['extracted', 'label_kind'], 'RECOVERED_2001_BINARY')
        self.reject(['extracted', 'client_binary_build_authenticated'], True)
        self.reject(['source', 'authority'], 'ORIGINAL_CLIENT_EXECUTED')

    def test_maintenance_start_not_exact_opening(self):
        self.reject(['extracted', 'announced_opening_relation'], 'OPEN_EXACTLY_AT_09')
        self.reject(['extracted', 'earlier_launch_year_in_body'], 2001)
        self.reject(['extracted', 'time_zone'], 'Asia/Shanghai')

    def test_two_server_labels_have_distinct_roles(self):
        self.reject(['extracted', 'new_server_group_label'], '石器时代2.0(1)')
        self.reject(['extracted', 'existing_group_renamed_to'], '石器时代2.0(2)')

    def test_billing_scope_and_unfetched_tariffs(self):
        self.reject(['extracted', 'billing', 'announced_scope'], 'ALL_GROUPS')
        self.reject(['extracted', 'billing', 'existing_group_1_billing_rule'], 'START_CHARGING')
        self.reject(['extracted', 'billing', 'price_or_unit'], '1_POINT_PER_MINUTE')
        self.reject(['extracted', 'billing', 'linked_policy_retrieved'], True)

    def test_four_reported_manors_not_complete_names_or_nine_to_four_patch(self):
        self.reject(['extracted', 'family', 'remaining_manor_names'], ['玛丽娜丝', '卡鲁它那'])
        self.reject(['extracted', 'family', 'manor_total_reported'], 9)
        self.reject(['comparison', 'proves_five_manors_removed'], True)
        self.reject(['comparison', 'transfers_riding_rules'], True)

    def test_advertised_security_speed_not_benchmarks(self):
        self.reject(['extracted', 'security_or_performance_benchmarked'], True)
        self.reject(['extracted', 'actual_server_opening_or_billing_witnessed'], True)
        self.reject(['unproven', 'first_introduction_dates_verified'], True)

    def test_nine_row_comparison_requires_exact_derived_blob(self):
        self.assertEqual(comparison(self.r['comparison_input'])['cn40_table_row_count'], 9)
        self.reject(['comparison_input', 'sha256'], '0' * 64)
        self.reject(['comparison_input', 'git_blob'], '0' * 40)

    def test_thirteen_actual_body_mutations_bypass_digest_shortcut(self):
        local = json.loads((ROOT / 'research/recovered/STONEAGE-CN2003-CLASSIC20-BRANCH-LOCAL-REPLAY-R1.json').read_text())
        self.assertEqual(local['extracted'], self.r['extracted'])
        cases = local['audit']['real_body_mutations']
        self.assertEqual(len(cases), 13)
        self.assertEqual(len({x['input_sha256'] for x in cases}), 13)
        self.assertTrue(all(x['rejected_without_digest_gate'] for x in cases))
        self.assertTrue(local['audit']['outer_script_positive'])
        self.assertFalse(local['historical_server_or_client_executed'])

    def test_current_bytes_failed_other_source_and_stage_boundaries(self):
        self.reject(['source', 'current_bytes_are_authenticated_2003_original'], True)
        self.assertEqual(self.r['bounded_unavailable_source']['http_status'], 403)
        for key in self.r['unproven']:
            with self.subTest(key=key):
                self.reject(['unproven', key], True)
        self.reject(['status', 'stage_b_wiki'], 'OPEN')
        self.reject(['next'], 'CONTINUE_TARIFF_OR_MANOR_HELPERS')


if __name__ == '__main__':
    unittest.main()
