"""Check the derived field item receipt without private program bytes."""

import json
import unittest

from tools.stoneage_world34_field_item_replay import (
    CODE, DATA, ITEM_IDS, REPORT, SYMBOLS, WORLD34_R2,
)


class FieldItemReplayReceiptTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads(REPORT.read_bytes())
        cls.r2 = json.loads(WORLD34_R2.read_bytes())
        cls.cases = {(case['item'], case['scenario']): case for case in cls.report['cases']}

    def test_full_source_and_r2_mapped_sections(self):
        self.assertEqual(self.report['archive_sha256'], self.r2['archive']['sha256'])
        server = self.report['server_member']
        self.assertEqual(server['target'], 'gmsv/gmsv.exe')
        self.assertEqual(server['unpacked_bytes'], 1897867)
        self.assertEqual(server['member_sha256'], 'd5b08dbcbf9e8736ba8598e38e5901f123d2bff544a9cae53a9ff88ce1971e00')
        self.assertEqual(self.report['r2_mapped_section_sha256'],
                         {section['name']: section['sha256'] for section in self.r2['pe']['sections']})
        self.assertNotEqual(self.report['original_sha256_at_r2_prefix_length'],
                            self.r2['gmsv_decompression']['prefix_sha256'])
        for key, windows in (('server_code_windows', CODE), ('server_data_windows', DATA)):
            self.assertEqual([tuple(window[:2]) for window in self.report[key]], list(windows))
            for _, _, digest in self.report[key]:
                self.assertRegex(digest, r'^[0-9a-f]{64}$')
        self.assertEqual(self.report['symbols'], SYMBOLS)

    def test_original_row_identity_and_client_gate(self):
        items = self.report['items']
        self.assertEqual([item['id'] for item in items], list(ITEM_IDS))
        self.assertEqual([item['client_field_gate'] for item in items], [False, True, True])
        for item, source in zip(items, self.r2['item_original_rows'], strict=True):
            self.assertEqual(item['row_sha256'], source['row_sha256'])
            self.assertEqual(item['option_sha256'], source['argument_sha256'])
            self.assertEqual(item['ints'], {'0': item['id'], '3': 20, '4': source['fieldtype'], '5': source['target']})

    def test_valid_targets_return_and_update_original_fixture_memory(self):
        expected = {1232: ([640], [760]), 12530: ([388], [452]), 12555: ([266, 28], [303, 32])}
        for item in ITEM_IDS:
            for label, requested, who in (('self', 0, 8), ('pet', 1, 10), ('party', 6, 9)):
                for endpoint, gains in zip(('min', 'max'), expected[item], strict=True):
                    with self.subTest(item=item, target=label, endpoint=endpoint):
                        case = self.cases[item, f'{label}_{endpoint}']
                        trace = case['trace']
                        self.assertEqual(case['target_input'], requested)
                        self.assertEqual(trace['item_use_args'], [8, who, 7])
                        self.assertEqual(trace['callback_args'], [8, who, 7])
                        self.assertTrue(trace['field_callback_entered'])
                        self.assertTrue(trace['callback_returned'])
                        self.assertTrue(trace['intake_returned'])
                        values = gains[:1] if label == 'pet' else gains
                        self.assertEqual(trace['stat_writes'],
                                         [[who, field, value] for field, value in enumerate(values, 10)])
                        self.assertEqual(trace['delete_args'], [[8, 7, 1, 0]])
                        self.assertEqual(trace['inventory_writes'], [-1])
                        self.assertEqual((trace['slot_before'], trace['slot_after'],
                                          trace['item_live_after'], trace['active_item_count_after']), (0, -1, 0, 0))

    def test_scene_and_target_item_fields_not_read_in_any_trace(self):
        self.assertEqual(len(self.report['cases']), len(self.cases))
        self.assertEqual(len(self.cases), 45)
        for case in self.cases.values():
            trace = case['trace']
            self.assertFalse({4, 5}.intersection(trace['int_keys']))
            for offset, size in trace['item_reads']:
                self.assertFalse(offset < 0x1c and offset + size > 0x14)

    def test_invalid_targets_stop_at_the_unchecked_lookup(self):
        for item in ITEM_IDS:
            for scenario in ('invalid_target', 'empty_pet', 'empty_party'):
                trace = self.cases[item, scenario]['trace']
                self.assertEqual(trace['item_use_args'], [8, -1, 7])
                self.assertEqual(trace['guarded_target_read'], [0x42dba8, 0x710000 - 0x24a4 + 4 + 0x36 * 4])
                self.assertFalse(trace['intake_returned'])
                self.assertFalse(trace['callback_args'])
                self.assertFalse(trace['stat_writes'])
                self.assertFalse(trace['inventory_writes'])
                self.assertEqual(trace['slot_after'], 0)

    def test_early_returns_and_cure_denial_preserve_inventory(self):
        for item in ITEM_IDS:
            for scenario in ('empty_slot', 'work64_blocked', 'battle_mode_blocked', 'cure_denied'):
                trace = self.cases[item, scenario]['trace']
                self.assertTrue(trace['intake_returned'])
                self.assertEqual(trace['callback_returned'], scenario == 'cure_denied')
                self.assertFalse(trace['stat_writes'])
                self.assertFalse(trace['delete_args'])
                self.assertFalse(trace['inventory_writes'])
                self.assertEqual(trace['slot_after'], trace['slot_before'])

    def test_caps_and_empty_action_fixture_sensitivity(self):
        for item in ITEM_IDS:
            cap = self.cases[item, 'near_cap']['trace']
            expected = [[8, 10, 1000], [8, 11, 100]] if item == 12555 else [[8, 10, 1000]]
            self.assertEqual(cap['stat_writes'], expected)
            self.assertEqual(cap['inventory_writes'], [-1])
            zero = self.cases[item, 'self_min']['trace']
            minus_one = self.cases[item, 'no_useaction']['trace']
            self.assertIn('action_notice', zero['fixture_calls'])
            self.assertNotIn('action_notice', minus_one['fixture_calls'])
            for key in ('stat_writes', 'delete_args', 'inventory_writes', 'intake_returned'):
                self.assertEqual(zero[key], minus_one[key])

    def test_historical_scope_boundary(self):
        for flag in ('original_process_started', 'live_inventory_changed', 'network_messages_delivered',
                     'historical_official_deployment_verified'):
            self.assertIs(self.report[flag], False)
