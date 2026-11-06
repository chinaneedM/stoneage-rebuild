"""Validate a bounded, derived WORLD37-R2A original code-section receipt."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / 'research/recovered/STONEAGE-STAGE-A-WORLD37-R2A-ORIGINAL-COMPILED-CAPTURE-TAIL-STATIC-R1.json'


class World37R2ACompiledTailTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(RECEIPT.read_text(encoding='utf-8'))

    def test_original_member_crc_failure_never_reclassified_as_success(self):
        self.assertEqual(self.r['expected_original_gmsv_member_size'], 1897867)
        self.assertEqual(self.r['expected_original_gmsv_member_sha256'],
                         'd5b08dbcbf9e8736ba8598e38e5901f123d2bff544a9cae53a9ff88ce1971e00')
        recovery = self.r['local_libarchive_block_recovery']
        self.assertEqual(recovery['bytes'], 1897867)
        self.assertEqual(recovery['sha256'],
                         'e61c417b18f939a22d25b800240f1d2d0f889a78024a8657e06502ff0ccdff0f')
        self.assertNotEqual(recovery['sha256'], self.r['expected_original_gmsv_member_sha256'])
        self.assertFalse(recovery['complete_original_member_verified'])

    def test_original_code_section_full_sha_and_source_windows(self):
        sec = self.r['source_qualification']['four_file_backed_section_sha256_equal_previously_independently_verified_WORLD34_R2_R3']
        self.assertEqual(sec['.text'], '2a42c0ce1951b0963898e2a5c95be920b8eb3b42bf329b012ba03a6d4ebcd11d')
        self.assertEqual(set(sec), {'.text', '.data', '.rdata', '.idata'})
        self.assertEqual(len(self.r['original_x86_static_windows']), 6)
        for entry in self.r['original_x86_static_windows']:
            self.assertEqual(entry['end_va'] - entry['start_va'], entry['length'])
            self.assertRegex(entry['sha256'], r'^[0-9a-f]{64}$')
        self.assertTrue(self.r['source_qualification']['qualification_limited_to_file_backed_sections'])

    def test_capture_success_tail_calls_are_not_runtime_traces(self):
        edges = {e['name']: e for e in self.r['original_x86_direct_calls']}
        expected = {
            'capture_caller': (0x52de8a, 0x5380e0),
            'pet_create': (0x5383d6, 0x468de0),
            'required_item_delete': (0x538579, 0x537e50),
            'capture_count_get': (0x53858b, 0x42db90),
            'capture_count_set': (0x5385b8, 0x42dcf0),
            'battle_exit': (0x5385e3, 0x518b20),
            'inventory_delete_inside_helper': (0x538099, 0x433ab0),
            'enemy_release_branch': (0x519134, 0x42fa60),
        }
        self.assertEqual(set(edges), set(expected))
        for name, (source, target) in expected.items():
            self.assertEqual((edges[name]['source_va'], edges[name]['direct_target_va']), (source, target))
            self.assertRegex(edges[name]['five_byte_call_sha256'], r'^[0-9a-f]{64}$')

    def test_count_item_and_enemy_exit_are_conditional_code_paths(self):
        cfg = self.r['static_control_flow']
        self.assertEqual(cfg['counter_original_int_key'], 44)
        self.assertEqual(cfg['counter_inc_va'], 0x538590)
        self.assertEqual((cfg['success_target_va'], cfg['pet_create_failure_test_va']), (0x5383c3, 0x5383e1))
        self.assertEqual((cfg['enemy_type_original_int_key'], cfg['enemy_type_equal_to']), (54, 2))
        self.assertEqual(cfg['exit_enemy_role_release_call_va'], 0x519134)
        self.assertEqual(cfg['item_helper_contains_inventory_delete_call_va'], 0x538099)

    def test_stage_a_evidence_firewall(self):
        self.assertEqual(self.r['outcome'], 'SOURCE_QUALIFIED_STATIC_TAIL_CALL_CHAIN_ONLY')
        limits = self.r['evidence_boundaries']
        for key in ('native_tail_dynamic_execution_performed', 'original_character_pool_cleanup_observed',
                    'original_inventory_item_consumption_observed', 'original_capture_counter_value_change_observed',
                    'all_required_item_table_values_verified_in_compiled_build',
                    'same_build_TW1_or_JSS1999_official_server_proven', 'COFF_suffix_entirely_verified'):
            self.assertFalse(limits[key], key)
        self.assertEqual(limits['Stage_A'], '7_PARTIAL_2_OPEN')
        self.assertEqual(limits['overall_percent'], None)
        self.assertEqual(limits['historical_CURRENT_STATE_blob_unchanged'],
                         'c89e0e33537990aa2132b47c40fef49a985a935c')


class World37R2CCompiledReplayTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from tools.stoneage_world37_capture_tail_source import REPORT, R2B

        cls.receipt = json.loads(REPORT.read_bytes())
        cls.cases = cls.receipt['cases']
        cls.matrix = cls.receipt['compiled_requirement_replays']
        cls.previous = json.loads(R2B.read_bytes())

    def test_exact_private_source_and_retained_evidence_boundaries(self):
        report = self.receipt
        expected = json.loads(RECEIPT.read_bytes())
        self.assertEqual(report['source_exe_sha256'], expected['expected_original_gmsv_member_sha256'])
        self.assertEqual(report['source_exe_sha256'], report['source_member']['member_sha256'])
        self.assertEqual(report['source_archive_sha256'], self.previous['archive_expected_sha256'])
        self.assertEqual(report['source_member']['member_crc32'], 0x6e31b63a)
        self.assertEqual(report['extra_data_windows'][0], [
            0x58cd60, 0x58ed60, self.previous['original_condition_table']['raw_table_sha256'],
        ])
        self.assertEqual(report['function_entry_first_instruction'], 0x5380e0)
        self.assertEqual(report['successful_stop_before_instruction'], 0x5385e8)
        for key in ('standalone_server_process_started', 'network_messages_delivered', 'save_executed',
                    'historical_official_deployment_verified', 'requirement_probe_linked_through_original_dispatcher'):
            self.assertIs(report[key], False)

    def test_success_keeps_new_pet_and_clears_only_wild_seat(self):
        case = self.cases['entry_three_required_items']
        before, after = case['before'], case['after']
        self.assertEqual((case['capture_result_flag'], case['created_character'], case['roster_after']),
                         (1, 5, [3, 4, 5, 6, -1]))
        self.assertEqual((case['created_record_in_use'], case['created_record_type'], case['created_record_owner']),
                         (1, 3, 1))
        self.assertEqual((before['actor_int_44'], after['actor_int_44']), (7, 8))
        expected = before['battle_character_indices'].copy()
        expected[17] = -1
        self.assertEqual(after['battle_character_indices'], expected)
        self.assertEqual((before['wild_record_in_use'], after['wild_record_in_use']), (1, 0))
        self.assertEqual(after['wild_item_slots'], [-1] * 50)
        self.assertEqual(after['active_item_count'], 0)
        stores = case['guest_writes']
        self.assertIn([0x42dd3f, 'actor_int_44', 7, 8], stores)
        self.assertIn([0x518e74, 'wild_seat_17_character', 12, -1], stores)
        self.assertIn([0x518e7f, 'wild_seat_17_word_8', 73, 0], stores)
        self.assertEqual(stores[-1], [0x42fb23, 'wild_record_in_use', 1, 0])
        self.assertEqual(case['endpoint'], self.receipt['function_entry_guest_return_address'])
        self.assertEqual(case['guest_battle_buffer'], 'BT|a2|r11|f1|')

    def test_delete_order_and_duplicate_slots_are_native_guest_writes(self):
        case = self.cases['duplicate_required_item_slots']
        self.assertEqual(case['compiled_required_item_ids'], [20219])
        actual = [event[2] for event in case['call_sites'] if event[1] == 'delete_inventory_slot']
        self.assertEqual(actual, [[1, 7, 1, 1], [1, 11, 1, 1]])
        self.assertEqual(case['after']['live_item_records'], [2])
        order = [record[1] for record in case['call_sites']]
        self.assertLess(order.index('delete_inventory_slot'), order.index('write_capture_count'))
        self.assertLess(order.index('write_capture_count'), order.index('release_wild_record'))
        triple = self.cases['entry_three_required_items']
        self.assertEqual([event[2][1] for event in triple['call_sites'] if event[1] == 'delete_inventory_slot'],
                         [7, 19, 0])

    def test_failed_capture_and_absent_seat_boundaries(self):
        for key in ('comparison_equal', 'full_roster', 'exhausted_pet_partition',
                    'entry_full_roster', 'entry_exhausted_pet_partition'):
            with self.subTest(key=key):
                case = self.cases[key]
                self.assertEqual(case['capture_result_flag'], 0)
                self.assertEqual(case['created_character'], -1)
                self.assertEqual(case['roster_after'], case['roster_before'])
                self.assertEqual(case['before'], case['after'])
                self.assertEqual(case['guest_writes'], [])
                self.assertEqual(case['modifier_after'], 0)
        for key in ('inactive_battle', 'wild_not_seated'):
            with self.subTest(key=key):
                case = self.cases[key]
                self.assertEqual(case['capture_result_flag'], 1)
                self.assertEqual(case['guest_writes'], [[0x42dd3f, 'actor_int_44', 7, 8]])
                self.assertEqual(case['after']['wild_record_in_use'], 1)
                self.assertNotIn('release_wild_record', [event[1] for event in case['call_sites']])

    def test_all_compiled_rows_and_each_single_omission_from_native_entry(self):
        previous = self.previous['original_condition_table']['rows']
        self.assertEqual(len(self.matrix), 11)
        self.assertEqual(sum(len(row['missing_cases']) for row in self.matrix), 13)
        alternatives = []
        for row, source in zip(self.matrix, previous, strict=True):
            with self.subTest(key=row['target_key_53']):
                self.assertEqual(row['target_key_53'], source['char_int_key_53_value'])
                self.assertEqual(row['compiled_item_ids'], source['required_item_id_candidates'])
                self.assertEqual([v['omitted_item_id'] for v in row['missing_cases']], row['compiled_item_ids'])
                alternatives.extend(item for item, presence in zip(row['compiled_item_ids'], row['item_table_presence'])
                                    if presence == 'ONLY_ALTERNATE')
                complete = row['complete']
                self.assertEqual(complete['capture_result_flag'], 1)
                self.assertIn(0x53829e, complete['entry_milestones'])
                self.assertIn(0x5389ca, complete['entry_milestones'])
                self.assertEqual(complete['standalone_requirement_helper_return'], 1)
                self.assertEqual(complete['after']['wild_record_in_use'], 0)
                self.assertEqual(complete['after']['actor_item_slots'], [-1] * 20)
                for omission in row['missing_cases']:
                    missing = omission['trace']
                    self.assertEqual(missing['capture_result_flag'], 0)
                    self.assertIsNone(missing['score'])
                    self.assertIn(0x53829e, missing['entry_milestones'])
                    self.assertNotIn(0x5389ca, missing['entry_milestones'])
                    self.assertEqual(missing['standalone_requirement_helper_return'], 0)
                    self.assertEqual(missing['before'], missing['after'])
                    self.assertEqual(missing['call_sites'], [])
                    self.assertEqual(missing['guest_writes'], [])
                    self.assertEqual(missing['guest_battle_buffer'], 'BT|a2|r11|f0|')
        self.assertEqual(set(alternatives), {20247, 20253, 20259})

    def test_native_entry_level_and_diagnostic_frame_are_separate(self):
        allowed = self.cases['entry_target_at_owner_level_plus_five']
        refused = self.cases['entry_target_above_owner_level_plus_five']
        self.assertEqual((allowed['target_level'], allowed['score'], allowed['capture_result_flag']), (40, 3.5, 1))
        self.assertEqual((refused['target_level'], refused['score'], refused['capture_result_flag']), (41, None, 0))
        self.assertEqual(refused['before'], refused['after'])
        bypass = self.cases['entry_owner_work_146_bypasses_level_guard']
        self.assertEqual((bypass['target_level'], bypass['entry_actor_work_146'], bypass['capture_result_flag']),
                         (41, 1, 1))
        target_ineligible = self.cases['entry_target_work_83_zero']
        self.assertEqual((target_ineligible['entry_target_work_83'], target_ineligible['score'],
                          target_ineligible['capture_result_flag']), (0, None, 0))
        self.assertEqual(target_ineligible['before'], target_ineligible['after'])
        diagnostic = self.cases['missing_requirement_diagnostic']
        self.assertIs(diagnostic['started_at_original_function_entry'], False)
        self.assertEqual(diagnostic['standalone_requirement_helper_return'], 0)
        self.assertEqual(diagnostic['capture_result_flag'], 1)
        self.assertEqual(self.cases['entry_missing_required_items']['capture_result_flag'], 0)

    def test_guest_write_log_reconstructs_each_monitored_snapshot(self):
        def flatten(snapshot):
            return {
                'actor_int_44': snapshot['actor_int_44'],
                'wild_seat_17_character': snapshot['battle_character_indices'][17],
                'wild_seat_17_word_8': snapshot['wild_seat_word_8'],
                'wild_record_in_use': snapshot['wild_record_in_use'],
                'active_item_count': snapshot['active_item_count'],
                **{f'item_record_{i}_in_use': int(i in snapshot['live_item_records']) for i in range(7)},
                **{f'actor_item_slot_{i}': item for i, item in enumerate(snapshot['actor_item_slots'])},
                **{f'wild_item_slot_{i}': item for i, item in enumerate(snapshot['wild_item_slots'])},
            }
        cases = list(self.cases.values())
        cases.extend(row['complete'] for row in self.matrix)
        cases.extend(v['trace'] for row in self.matrix for v in row['missing_cases'])
        self.assertEqual(len(cases), 42)
        for index, case in enumerate(cases):
            with self.subTest(index=index):
                state = flatten(case['before'])
                for address, field, old, new in case['guest_writes']:
                    self.assertIn(address, {0x42dd3f, 0x433bfc, 0x4f7338, 0x4f7346, 0x518e74, 0x518e7f,
                                            0x42fac1, 0x42fb01, 0x42fb23})
                    self.assertEqual(state[field], old)
                    state[field] = new
                self.assertEqual(state, flatten(case['after']))


if __name__ == '__main__':
    unittest.main()
