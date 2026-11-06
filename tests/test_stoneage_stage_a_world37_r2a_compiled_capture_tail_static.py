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


if __name__ == '__main__':
    unittest.main()
